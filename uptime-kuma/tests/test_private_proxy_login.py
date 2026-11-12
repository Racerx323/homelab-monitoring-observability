"""Private handoff boundaries; no network, credentials or Podman execution."""
import contextlib
import io
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest import mock

spec = importlib.util.spec_from_file_location('private_login', Path(__file__).resolve().parents[1] / 'scripts/private-proxy-login.py')
client = importlib.util.module_from_spec(spec)
spec.loader.exec_module(client)


class WindowTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.receipt = self.root / 'receipt.json'
        self.window = self.root / 'operator-window.json'
        self.record = dict(operation='fixture', client_sha256='a'*64, status='open',
                           deadline=time.time()+600, controller_pid=os.getpid(),
                           controller_start=Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()[19])
        self.write()

    def write(self):
        self.window.write_text(json.dumps(self.record))
        self.window.chmod(0o600)

    def read(self, margin=180):
        return client.read_window(self.receipt, 'fixture', 'a'*64, margin)

    def test_current_controller(self):
        self.assertEqual(self.read(), self.record)

    def test_reject_expiry_identity_and_pid_reuse(self):
        for key, value in [('status', 'closed'), ('deadline', time.time()+10),
                           ('operation', 'other'), ('client_sha256', 'b'*64),
                           ('controller_start', '0'), ('controller_pid', 0),
                           ('controller_pid', '1/../self')]:
            with self.subTest(key=key, value=value):
                previous = self.record[key]
                self.record[key] = value
                self.write()
                with self.assertRaises(ValueError):
                    self.read()
                self.record[key] = previous

    def test_reject_symlink_or_public_window(self):
        self.window.chmod(0o644)
        with self.assertRaises(ValueError):
            self.read()
        self.window.rename(self.root/'other.json')
        self.window.symlink_to(self.root/'other.json')
        with self.assertRaises(ValueError):
            self.read()

    def test_receipt_rejects_tampering(self):
        valid = dict(operation='fixture', status='passed', client_sha256='a'*64,
                     started_at=time.time(), finished_at=time.time(), rows=client.expected_rows())
        self.receipt.write_text(json.dumps(valid)); self.receipt.chmod(0o600)
        client.verify_receipt(self.receipt)
        for key, value in [('operation', 'other'), ('status', 'failed'), ('rows', []),
                           ('started_at', 0), ('finished_at', time.time()+1000),
                           ('client_sha256', 'b'*64), ('extra', 'unexpected')]:
            with self.subTest(key=key):
                changed = dict(valid, **{key:value})
                self.receipt.write_text(json.dumps(changed))
                with self.assertRaises(ValueError):
                    client.verify_receipt(self.receipt)
        self.receipt.write_text(json.dumps(valid)); self.receipt.chmod(0o644)
        with self.assertRaises(ValueError):
            client.verify_receipt(self.receipt)
        self.receipt.unlink(); self.receipt.symlink_to(self.window)
        with self.assertRaises(ValueError):
            client.verify_receipt(self.receipt)


class StandaloneTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.receipt = Path(self.directory.name) / 'receipt.json'
        self.record = dict(operation='acceptance', mode='standalone', status='passed',
                           started_at=time.time()-66, finished_at=time.time(),
                           client_sha256=hashlib.sha256(Path(client.__file__).with_name('verify-proxy-login.cjs').read_bytes()).hexdigest(),
                           rows=client.expected_rows())

    def verify(self, record):
        self.receipt.write_text(json.dumps(record))
        self.receipt.chmod(0o600)
        client.verify_receipt(self.receipt, standalone_operation='acceptance')

    def test_no_window_or_controller_required(self):
        self.verify(self.record)

    def test_identity_result_duration_and_schema_rejections(self):
        for key, value in [('operation', 'other'), ('mode', 'window'), ('status', 'failed'),
                           ('client_sha256', '0'*64), ('rows', []), ('started_at', 0),
                           ('started_at', self.record['finished_at']-1),
                           ('finished_at', time.time()+1000), ('extra', 'unexpected')]:
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.verify(dict(self.record, **{key:value}))

    def test_legacy_verifier_does_not_accept_standalone_receipt(self):
        self.verify(self.record)
        with self.assertRaises((ValueError, FileNotFoundError)):
            client.verify_receipt(self.receipt)
        self.receipt.chmod(0o644)
        with self.assertRaises(ValueError):
            client.verify_receipt(self.receipt, standalone_operation='acceptance')

    def test_standalone_dispatch_uses_no_window_and_retains_no_credentials(self):
        process = mock.Mock(returncode=0)
        process.poll.return_value = 0
        process.communicate.return_value = ('\n'.join(json.dumps(row) for row in client.expected_rows()), '')
        with mock.patch.object(client.sys, 'argv', ['private-proxy-login.py', '--standalone', 'acceptance', str(self.receipt)]), \
                mock.patch.object(client.sys.stdin, 'isatty', return_value=True), \
                mock.patch.object(client, 'startup_check', return_value=mock.Mock(returncode=0, stdout='{"status":"passed"}')), \
                mock.patch('builtins.input', return_value='fixture-user'), \
                mock.patch.object(client.getpass, 'getpass', return_value='fixture-password'), \
                mock.patch.object(client, 'read_window', side_effect=AssertionError('window must not be read')), \
                mock.patch.object(client.subprocess, 'Popen', return_value=process) as spawn, \
                mock.patch.object(client.subprocess, 'run', return_value=mock.Mock(returncode=1)), \
                self.assertRaises(SystemExit) as result:
            client.main()
        self.assertEqual(result.exception.code, 0)
        record = self.receipt.read_text()
        self.assertEqual(json.loads(record)['mode'], 'standalone')
        self.assertNotIn('fixture-user', record)
        self.assertNotIn('fixture-password', record)
        self.assertNotIn('fixture-password', str(spawn.call_args.args))


class FailureReportingTests(unittest.TestCase):
    def run_failure(self, returncode=1, stderr='', stdout='', launch_error=None,
                    timeout=False, cleanup=1):
        with tempfile.TemporaryDirectory() as directory:
            receipt = Path(directory) / 'receipt.json'
            process = mock.Mock(returncode=returncode)
            process.poll.return_value = returncode
            process.communicate.return_value = (stdout, stderr)
            if timeout:
                process.communicate.side_effect = [client.subprocess.TimeoutExpired('private', 1), ('', '')]
            console = io.StringIO()
            with mock.patch.object(client.sys, 'argv', ['helper', '--standalone', 'fixture', str(receipt)]), \
                    mock.patch.object(client.sys.stdin, 'isatty', return_value=True), \
                mock.patch.object(client, 'startup_check', return_value=mock.Mock(returncode=0, stdout='{"status":"passed"}')), \
                    mock.patch('builtins.input', return_value='SENTINEL-USER'), \
                    mock.patch.object(client.getpass, 'getpass', return_value='SENTINEL-PASSWORD'), \
                    mock.patch.object(client.subprocess, 'Popen', side_effect=launch_error, return_value=process), \
                    mock.patch.object(client.subprocess, 'run', return_value=mock.Mock(returncode=cleanup)), \
                    mock.patch.object(client.time, 'monotonic', side_effect=[0, 1, 181] if timeout else None, return_value=0), \
                    contextlib.redirect_stdout(console), self.assertRaises(SystemExit) as result:
                client.main()
            self.assertEqual(result.exception.code, 1)
            self.assertEqual(receipt.stat().st_mode & 0o777, 0o600)
            saved = receipt.read_text()
            for secret in ['SENTINEL-USER', 'SENTINEL-PASSWORD', 'SENTINEL-TOKEN']:
                self.assertNotIn(secret, saved + console.getvalue())
            with self.assertRaises(ValueError):
                client.verify_receipt(receipt, standalone_operation='fixture')
            # Existing failed receipt is still a consumed attempt, not retry permission.
            with mock.patch.object(client.sys, 'argv', ['helper', '--standalone', 'fixture', str(receipt)]), \
                    mock.patch.object(client.sys.stdin, 'isatty', return_value=True), \
                mock.patch.object(client, 'startup_check', return_value=mock.Mock(returncode=0, stdout='{"status":"passed"}')), \
                    mock.patch.object(client.subprocess, 'Popen') as spawn, self.assertRaises(SystemExit):
                client.main()
            spawn.assert_not_called()
            return json.loads(saved)

    def test_client_stage_family_code_and_exit_retained(self):
        report = dict(stage='correct-login', family='ipv6', code='ERR_ASSERTION')
        record = self.run_failure(stderr=json.dumps(report))
        self.assertEqual(record['client_failure'], report)
        self.assertEqual(record['client_exit_status'], 1)
        self.assertEqual(record['cleanup_status'], 'passed')

    def test_readiness_and_acknowledgement_codes_are_retained(self):
        for code in ['READINESS_TIMEOUT', 'SOCKET_DISCONNECTED', 'UNEXPECTED_READINESS', 'ACK_TIMEOUT', 'ACK_ERROR']:
            report = dict(stage='websocket-connect', family='ipv4', code=code)
            self.assertEqual(client.safe_client_failure(json.dumps(report)), report)

    def test_untrusted_reports_are_never_retained(self):
        valid = dict(stage='dashboard', family='ipv4', code='ECONNREFUSED')
        cases = ['SENTINEL-PASSWORD', json.dumps(dict(valid, token='SENTINEL-TOKEN')),
                 json.dumps(dict(valid, stage='SENTINEL-USER')), json.dumps(dict(valid, code=['secret'])),
                 json.dumps(valid) + '\n' + json.dumps(valid), 'x' * 1025, 'null']
        for raw in cases:
            with self.subTest(raw=raw[:40]):
                record = self.run_failure(returncode=125, stderr=raw, stdout='SENTINEL-TOKEN')
                self.assertEqual(record['client_exit_status'], 125)
                self.assertIn(record['client_failure']['report'], ['oversized', 'unavailable'])

    def test_launch_timeout_and_cleanup_are_distinct(self):
        self.assertEqual(self.run_failure(launch_error=OSError('SENTINEL-PASSWORD'))['failure_stage'], 'client-start')
        self.assertEqual(self.run_failure(timeout=True)['failure_stage'], 'client-deadline')
        record = self.run_failure(cleanup=125)
        self.assertEqual(record['cleanup_status'], 'inspection-failed')
        self.assertEqual(record['failure_stage'], 'client-result')

    def test_successful_client_with_invalid_or_oversized_rows_fails(self):
        self.assertEqual(self.run_failure(returncode=0, stdout='SENTINEL-TOKEN')['failure_stage'], 'client-receipt')
        self.assertEqual(self.run_failure(returncode=0, stdout='x' * 8193)['failure_stage'], 'client-output-limit')

    def test_cleanup_failure_overrides_client_success(self):
        record = self.run_failure(returncode=0, stdout='\n'.join(json.dumps(r) for r in client.expected_rows()), cleanup=125)
        self.assertEqual(record['failure_stage'], 'cleanup')
        self.assertEqual(record['cleanup_status'], 'inspection-failed')


class StartupTests(unittest.TestCase):
    def test_command_preserves_identity_privacy_and_no_network_preflight(self):
        with mock.patch.object(client.subprocess, 'run', return_value=mock.Mock()) as run:
            client.startup_check(Path('/private/scripts/client.cjs'), 'fixture')
        command = run.call_args.args[0]
        self.assertEqual(command[command.index('--network')+1], 'none')
        self.assertEqual(command[command.index('--userns')+1], 'keep-id')
        self.assertEqual(command[command.index('--user')+1], f'{os.getuid()}:{os.getgid()}')
        self.assertIn('/private/scripts:/work:ro', command)
        self.assertEqual(run.call_args.kwargs['stdin'], client.subprocess.DEVNULL)
        self.assertEqual(run.call_args.kwargs['timeout'], 30)

    def test_startup_failure_or_timeout_never_prompts_or_launches_client(self):
        for failure in [mock.Mock(returncode=1, stdout='', stderr=json.dumps(
                dict(stage='source-read', family='none', code='EACCES'))),
                client.subprocess.TimeoutExpired('podman', 30)]:
            with tempfile.TemporaryDirectory() as directory:
                receipt = Path(directory)/'receipt.json'
                with mock.patch.object(client.sys, 'argv', ['helper', '--standalone', 'fixture', str(receipt)]), \
                        mock.patch.object(client.sys.stdin, 'isatty', return_value=True), \
                        mock.patch.object(client, 'startup_check', side_effect=failure if isinstance(failure, Exception) else None, return_value=failure), \
                        mock.patch('builtins.input') as username, \
                        mock.patch.object(client.getpass, 'getpass') as password, \
                        mock.patch.object(client.subprocess, 'Popen') as spawn, \
                        mock.patch.object(client.subprocess, 'run', return_value=mock.Mock(returncode=1)), \
                        contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit):
                    client.main()
                username.assert_not_called(); password.assert_not_called(); spawn.assert_not_called()
                record = json.loads(receipt.read_text())
                self.assertEqual(record['failure_stage'], 'startup-check')
                if not isinstance(failure, Exception):
                    self.assertEqual(record['client_failure']['code'], 'EACCES')


if __name__ == '__main__':
    unittest.main()
