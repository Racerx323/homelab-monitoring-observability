"""Exercise passive observation decisions with causal clock/service substitutes."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest import mock

module = importlib.util.spec_from_file_location('observer', Path(__file__).resolve().parents[1] / 'scripts/observe-proxy-acceptance.py')
observer = importlib.util.module_from_spec(module)
module.loader.exec_module(observer)
SPEC = dict(operation='fixture', release='fixture-release', manifest_sha256='a'*64,
            fragment_sha256='b'*64)
NODE = dict(name='node-a', ssh='pi@10.1.0.53', ipv4='10.1.0.53',
            ipv6='fd36:5aa8:6971:1::53', fqdn='pihole0.local.theama.co')
SPEC['nodes'] = [NODE]


class ObservationTests(unittest.TestCase):
    def exercise(self, fault=None):
        elapsed = [100.0]
        calls = []
        identities = []

        def identity(spec):
            identities.append(1)
            if fault == 'drift' and len(identities) == 2:
                raise ValueError('release-selection')
            return {k: spec[k] for k in ('release', 'manifest_sha256', 'fragment_sha256')}

        def command(argv, timeout=10):
            calls.append(argv)
            if argv[0] == 'curl':
                if fault == 'http':
                    return '503'
                return '204' if argv[-1].endswith('/healthz') else '200'
            if argv[0] == 'journalctl':
                if '--after-cursor' not in argv:
                    return '' if fault == 'cursor' else '-- cursor: retained-cursor\n'
                if fault == 'journal-access':
                    raise ValueError('command-exit:journalctl')
                if fault == 'journal-truncated':
                    return (json.dumps({'MESSAGE': 'ordinary'})+'\n')*1001
                return json.dumps({'MESSAGE': 'upstream health check failed'})+'\n' if fault == 'journal-health' else ''
            self.assertEqual(argv[:2], ['systemctl', 'show'])
            # Native timestamps advance only after simulated timer completions.
            cycle = int((elapsed[0]-100)//30)
            began = 90000000 if fault == 'stale' else int((100+cycle*30)*1000000)
            props = dict(ExecMainStartTimestampMonotonic=began,
                         ExecMainExitTimestampMonotonic=began+1000,
                         ExecMainCode=1, ExecMainStatus=1 if fault == 'cycle-failed' else 0,
                         Result='success', ActiveState='inactive')
            if fault == 'malformed':
                del props['Result']
            return '\n'.join(str(k)+'='+str(v) for k, v in props.items())

        with mock.patch.object(observer, 'identity', side_effect=identity), \
                mock.patch.object(observer, 'command', side_effect=command), \
                mock.patch.object(observer.time, 'monotonic', side_effect=lambda: elapsed[0]), \
                mock.patch.object(observer.time, 'sleep', side_effect=lambda n: elapsed.__setitem__(0, elapsed[0]+n)):
            result = observer.observe(SPEC, NODE)
        return result, calls

    def test_success_requires_real_distinct_completions(self):
        result, calls = self.exercise()
        observer.verify_node(SPEC, NODE, result)
        self.assertGreaterEqual(result['http'][1]['elapsed'], 65)
        self.assertEqual(len([c for c in calls if c[0] == 'curl']), 12)
        self.assertTrue(all(c[0] in ('curl', 'journalctl', 'systemctl') for c in calls))
        self.assertTrue(all(c[1] == 'show' for c in calls if c[0] == 'systemctl'))

    def test_failures_never_become_acceptance(self):
        for fault in ('http', 'cursor', 'journal-access', 'journal-truncated',
                      'journal-health', 'stale', 'cycle-failed', 'malformed', 'drift'):
            with self.subTest(fault=fault):
                result, _ = self.exercise(fault)
                self.assertEqual(result['status'], 'failed')
                with self.assertRaises(ValueError):
                    observer.verify_node(SPEC, NODE, result)

    def test_tampered_summary_rejected(self):
        original, _ = self.exercise()
        for mutation in ('http', 'cadence', 'cycles', 'spec', 'identity', 'journal'):
            result = copy.deepcopy(original)
            if mutation == 'http':
                result['http'][1]['rows'][0]['observed'] = 503
            elif mutation == 'cadence':
                result['http'][0]['elapsed'] = result['http'][1]['elapsed']-20
            elif mutation == 'cycles':
                result['samples'] = [result['samples'][0]]*20
            elif mutation == 'spec':
                result['spec_sha256'] = '0'*64
            elif mutation == 'identity':
                result['final_identity']['release'] = 'other'
            else:
                result['journal']['adverse'] = 1
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                observer.verify_node(SPEC, NODE, result)

    def test_controller_stops_on_transport_failure_and_refuses_replay(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary)/'observation'
            def transport(argv, **kwargs):
                self.assertIn('StrictHostKeyChecking=yes', argv)
                self.assertTrue(argv[-1].startswith('cd / && sudo -n python3 - --node '))
                self.assertEqual(kwargs['input'], Path(observer.__file__).read_bytes())
                return mock.Mock(returncode=255)
            with mock.patch.object(observer.subprocess, 'run', side_effect=transport) as run:
                with self.assertRaises(ValueError):
                    observer.run_nodes(SPEC, destination)
                self.assertEqual(run.call_count, 1)
                with self.assertRaises(FileExistsError):
                    observer.run_nodes(SPEC, destination)

    def test_combined_receipt_requires_private_and_observed_acceptance(self):
        observed, _ = self.exercise()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            receipt = root/'private.json'
            helper_spec = importlib.util.spec_from_file_location('helper', Path(observer.__file__).with_name('private-proxy-login.py'))
            helper = importlib.util.module_from_spec(helper_spec)
            helper_spec.loader.exec_module(helper)
            private = dict(operation='fixture', mode='standalone', status='passed',
                           started_at=time.time()-66, finished_at=time.time(),
                           client_sha256=hashlib.sha256(Path(observer.__file__).with_name('verify-proxy-login.cjs').read_bytes()).hexdigest(),
                           rows=helper.expected_rows())
            receipt.write_text(json.dumps(private)); receipt.chmod(0o600)
            for suffix, content in [('.stdout', json.dumps(observed)), ('.status', '0\n'),
                                    ('.command.json', json.dumps(observer.ssh_command(SPEC, NODE))),
                                    ('.source-sha256', hashlib.sha256(Path(observer.__file__).read_bytes()).hexdigest())]:
                path = root/('node-a'+suffix); path.write_text(content); path.chmod(0o600)
            self.assertEqual(observer.verify_combined(SPEC, root, receipt)['status'], 'passed')
            saved = (root/'node-a.command.json').read_text()
            (root/'node-a.command.json').write_text('[]')
            with self.assertRaises(ValueError):
                observer.verify_combined(SPEC, root, receipt)
            (root/'node-a.command.json').write_text(saved)
            (root/'node-a.status').write_text('1\n')
            with self.assertRaises(ValueError):
                observer.verify_combined(SPEC, root, receipt)
            (root/'node-a.status').write_text('0\n')
            private['operation'] = 'other'
            receipt.write_text(json.dumps(private))
            with self.assertRaises(ValueError):
                observer.verify_combined(SPEC, root, receipt)


class CommandDiagnosticsTests(unittest.TestCase):
    def test_final_empty_read_needs_no_cursor_output(self):
        with mock.patch.object(observer.subprocess, 'run', return_value=mock.Mock(returncode=0, stdout='', stderr='')) as run:
            self.assertEqual(observer.journal_summary('private-cursor')['events'], 0)
        argv = run.call_args.args[0]
        self.assertIn('--after-cursor', argv)
        self.assertNotIn('--show-cursor', argv)
        self.assertEqual(argv[-2:], ['-n', '1001'])

    def test_failed_empty_read_is_not_accepted(self):
        with mock.patch.object(observer.subprocess, 'run', return_value=mock.Mock(returncode=1, stdout='', stderr='')):
            with self.assertRaises(observer.CommandFailure) as caught:
                observer.journal_summary('SENTINEL-CURSOR')
        self.assertEqual(caught.exception.details['diagnostic'], 'no-output')
        self.assertNotIn('SENTINEL', str(caught.exception))

    def test_error_classification_retains_counts_not_messages(self):
        for stderr, category in [('Failed to seek to cursor: Invalid argument', 'invalid-cursor'),
                                 ('SENTINEL-SECRET: Permission denied', 'permission-denied'),
                                 ('SENTINEL-TOKEN', 'unclassified')]:
            with self.subTest(category=category), mock.patch.object(observer.subprocess, 'run', return_value=mock.Mock(returncode=1, stdout='SENTINEL-JOURNAL', stderr=stderr)):
                with self.assertRaises(observer.CommandFailure) as caught:
                    observer.journal_summary('SENTINEL-CURSOR')
                details = caught.exception.details
                self.assertEqual(details['operation'], 'journal-follow')
                self.assertEqual(details['observed_exit'], 1)
                self.assertEqual(details['diagnostic'], category)
                self.assertEqual(details['stderr_bytes'], len(stderr.encode()))
                self.assertNotIn('SENTINEL', str(caught.exception))

    def test_timeout_launch_and_size_failure_are_bounded(self):
        cases = [(observer.subprocess.TimeoutExpired('secret', 10, output='SENTINEL'), 'timeout'),
                 (OSError('SENTINEL'), 'launch-error')]
        for error, category in cases:
            with mock.patch.object(observer.subprocess, 'run', side_effect=error), self.assertRaises(observer.CommandFailure) as caught:
                observer.command(['journalctl'])
            self.assertEqual(caught.exception.details['diagnostic'], category)
            self.assertNotIn('SENTINEL', str(caught.exception))
        with mock.patch.object(observer.subprocess, 'run', return_value=mock.Mock(returncode=0, stdout='x'*(observer.LIMIT+1), stderr='')):
            with self.assertRaises(observer.CommandFailure) as caught:
                observer.command(['journalctl'])
            self.assertEqual(caught.exception.details['diagnostic'], 'output-limit')

    def test_observer_retains_safe_command_failure(self):
        with mock.patch.object(observer.subprocess, 'run', return_value=mock.Mock(returncode=1, stdout='', stderr='SENTINEL')):
            result = observer.observe(SPEC, NODE)
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['command_failure']['operation'], 'journal-baseline')
        self.assertNotIn('SENTINEL', json.dumps(result))


if __name__ == '__main__':
    unittest.main()
