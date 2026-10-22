#!/usr/bin/python3
"""Offline contracts for bounded scheduled-evidence observations; no target contact."""
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import tarfile
import tempfile
import time
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT/'scripts'/name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


o = load('observe_ntp.py')
r = load('review_ntp_observation.py')


class ObservationTests(unittest.TestCase):
    def test_graph_fields_keep_self_cdef_and_nested_device_types(self):
        config = '''multigraph diskstats_iops.loop0
graph_title Disk
reads.label Reads
reads.type DERIVE
reads.cdef reads,8,*
total.label Total
total.cdef reads,2,*
'''
        self.assertEqual(r.graph_fields(config, 'diskstats'), {'diskstats_iops.loop0': {'reads': 'd'}})
        with self.assertRaisesRegex(ValueError, 'unsafe'):
            r.graph_fields(config.replace('diskstats_iops.loop0', '../../etc/passwd'), 'diskstats')

    def test_expanded_https_uses_nested_paths_and_complete_selection(self):
        spec = {'graphs': {'j2-svntp1': ['cpu', 'diskstats_iops.loop0'], 'J1-SVMF': ['ntp_transport_j2']}}
        paths = r.https_paths(spec)
        self.assertEqual(len(paths), 6)
        self.assertIn('/munin-cgi/munin-cgi-graph/j2-svntp1/j2-svntp1/diskstats_iops/loop0-day.png', paths)
        self.assertEqual(len(paths), len(set(paths)))

    def test_exact_expanded_rrd_fields_do_not_read_other_fields(self):
        graph = 'diskstats_iops.loop0'
        spec = {'graphs': {'j2-svntp1': [graph]},
                'rrd_fields': {'j2-svntp1': {graph: {'rdio': 'g', 'wrio': 'g'}}}}
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            selected = directory/'j2-svntp1-diskstats_iops-loop0-rdio-g.rrd'
            selected.write_bytes(b'not interpreted by this test')
            other = directory/'j2-svntp1-diskstats_iops-loop0-old-g.rrd'
            other.write_bytes(b'preserve')
            real_path = Path
            def fixed_path(value):
                return directory if value == '/var/lib/munin' else real_path(value)
            # Redirect only the fixed host directory, preserving real filesystem metadata.
            host = directory/'j2-svntp1'
            host.mkdir()
            selected.rename(host/selected.name)
            other.rename(host/other.name)
            with patch.object(o, 'Path', side_effect=fixed_path), \
                    patch.object(o, 'command', return_value='300: 1\n') as command:
                result = o.rrds(spec, 1200)
            row = result['data']['j2-svntp1'][graph]
            self.assertTrue(row['missing'])
            self.assertEqual(row['missing_expected_files'], ['j2-svntp1-diskstats_iops-loop0-wrio-g.rrd'])
            self.assertEqual(command.call_count, 2)
            self.assertTrue(all('old' not in str(call) for call in command.call_args_list))

    def test_master_window_uses_expansion_cutoff(self):
        with patch.object(o, 'read', return_value=(b'', {})), patch.object(o, 'journal', return_value=[]) as journal, \
                patch.object(o, 'rrds', return_value={}):
            result = o.master({'commissioned_epoch': 10, 'collection_after_epoch': 900}, 1000)
        self.assertEqual(result['collection_after_epoch'], 900)
        self.assertEqual(journal.call_args.args, ('cron.service', 900))
        self.assertFalse(result['cycles']['three_scheduled_cycles_evidenced'])

    def test_transport_metadata_reports_each_mismatch_without_source_export(self):
        expected = {'sha256': 'a'*64, 'uid': 0, 'gid': 0, 'mode': 0o755, 'nlink': 1}
        actual = dict(expected, mode=0o700, nlink=2)
        info = types.SimpleNamespace(st_mode=stat.S_IFLNK | 0o777,
                                     st_uid=0, st_gid=0, st_ino=12, st_dev=1)
        with patch.object(o, 'read', return_value=(b'private source', actual)), \
                patch.object(Path, 'is_symlink', return_value=False), \
                patch.object(Path, 'lstat', return_value=info), \
                patch.object(o.os, 'readlink', return_value='/usr/local/munin/lib/plugins/ntp_transport_j2'):
            result = o.transport_metadata({'transport_expected': expected})
        self.assertEqual(result['matches'], dict.fromkeys(expected, True) | {'mode': False, 'nlink': False})
        self.assertNotIn('private source', json.dumps(result))

    def test_observation_read_reports_real_hardlink_count(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary)/'source'
            path.write_bytes(b'content')
            os.link(path, Path(temporary)/'link')
            self.assertEqual(o.read(path)[1]['nlink'], 2)

    def test_metadata_review_is_bounded_and_excludes_invocations(self):
        spec = {'purpose': 'transport-metadata', 'operation_id': 'munin-transport-test',
                'expires_epoch': int(time.time())+3600}
        text = r.review(spec)
        self.assertIn('No target staging', text)
        self.assertIn('Export no source bytes', text)
        self.assertIn('protocol/HTTP query', text)

    def test_generic_settings_export_only_privilege_selectors(self):
        raw = b'''[if_*]
user munin
group munin
timeout 60
env.password must-not-export
command secret-command
[smart_*]
user root
env.credentials another-secret
'''
        rows = o.configured_identities(raw)
        self.assertEqual(rows, [{'section': 'if_*', 'key': 'user', 'value': 'munin'},
                                {'section': 'if_*', 'key': 'group', 'value': 'munin'},
                                {'section': 'if_*', 'key': 'timeout', 'value': '60'},
                                {'section': 'smart_*', 'key': 'user', 'value': 'root'}])
        self.assertNotIn('secret', json.dumps(rows))

    def test_generic_reviews_do_not_authorize_reference_contact_or_enablement(self):
        for kind in ('node', 'master'):
            endpoint, user, alias, hostname = r.TARGETS[kind]
            spec = {'kind': kind, 'purpose': 'generic-profile', 'endpoint': endpoint,
                    'user': user, 'host_key_alias': alias, 'hostname': hostname,
                    'operation_id': 'munin-generic-test', 'expires_epoch': int(time.time())+3600}
            text = r.review(spec)
            self.assertIn('does not', text)
            self.assertIn('strict', text)
            self.assertIn('Preserve all four NTP', text)
            if kind == 'master':
                self.assertIn('no SSH/protocol/HTTP request goes to j2-svpi4mf', text)
            else:
                self.assertIn('No sensor/device reads', text)

    def test_records_do_not_accept_scheduling_or_delivery(self):
        meta = {'uid': 0, 'gid': 0, 'mode': 0o600}
        valid = {'schema': 1, 'job': 'retention', 'status': 'success', 'completed_epoch': 900}
        result = o.success(json.dumps(valid), meta, 'retention', 1000, 100)
        self.assertTrue(result['valid_completion'])
        self.assertFalse(result['scheduled_provenance_accepted'])
        for key, value in [('completed_epoch', True), ('completed_epoch', 1001),
                           ('completed_epoch', float('nan')), ('completed_epoch', 90),
                           ('status', 'failed'), ('job', 'reporting')]:
            self.assertFalse(o.success(json.dumps({**valid, key: value}), meta,
                                       'retention', 1000, 100)['valid_completion'])
        self.assertFalse(o.success(json.dumps(valid), {**meta, 'mode': 0o644},
                                   'retention', 1000, 100)['valid_completion'])

    def test_stale_record_remains_stale(self):
        row = o.success(json.dumps({'schema': 1, 'job': 'reporting', 'status': 'success',
                        'completed_epoch': 200}), {'uid': 0, 'gid': 0, 'mode': 0o600},
                        'reporting', 200000, 100)
        self.assertTrue(row['valid_completion'])
        self.assertFalse(row['fresh'])

    def test_nan_is_unknown_not_zero(self):
        self.assertEqual(o.rrd_rows(' value\n300: 1.0e+00\n600: -nan\n900: U\n'),
                         {300: 1, 600: None, 900: None})

    def test_three_cycles_require_actual_cron_and_both_nodes(self):
        starts = [1800, 2100, 2400]
        events = [{'epoch': start+offset, 'kind': kind} for start in starts
                  for offset, kind in [(1, 'start'), (8, 'j2-finish'), (9, 'master-finish'), (10, 'finish')]]
        self.assertTrue(o.cycles(events, starts, 1000, 3000)['three_scheduled_cycles_evidenced'])
        self.assertFalse(o.cycles(events, [], 1000, 3000)['three_scheduled_cycles_evidenced'])
        self.assertFalse(o.cycles(events, starts, 2200, 3000)['three_scheduled_cycles_evidenced'])
        self.assertFalse(o.cycles([e for e in events if e['kind'] != 'master-finish'],
                                  starts, 1000, 3000)['three_scheduled_cycles_evidenced'])
        failed = sorted(events+[{'epoch': 2105, 'kind': 'fault'}], key=lambda e: e['epoch'])
        self.assertFalse(o.cycles(failed, starts, 1000, 3000)['three_scheduled_cycles_evidenced'])
        skipped = [e for e in events if not 2100 <= e['epoch'] < 2400]
        self.assertFalse(o.cycles(skipped, starts, 1000, 3000)['three_scheduled_cycles_evidenced'])

    def test_log_export_omits_commands_and_secrets(self):
        raw = b'''2026/10/21-16:00:01 [123] Starting munin-update
2026/10/21-16:00:07 [123] Munin-update finished for node j2-svntp1/j2-svntp1 (6 sec)
2026/10/21-16:00:08 [123] Munin-update finished for node J1-SVMF/J1-SVMF (7 sec)
2026/10/21-16:00:09 [123] Munin-update finished (8 sec)
2026/10/21-16:00:09 [123] [ERROR] credential=do-not-export
'''
        rows = o.log_events(raw)
        self.assertEqual([row['kind'] for row in rows],
                         ['start', 'j2-finish', 'master-finish', 'finish', 'fault'])
        self.assertNotIn('credential', json.dumps(rows))

    def test_actual_stdin_bootstrap_reaches_identity_guard(self):
        files = {n: p.read_bytes() for n, p in r.SOURCES.items()}
        payload = r.payload({'kind': 'node', 'hostname': 'nonexistent-observation-host',
            'operation_id': 'munin-bootstrap-test'}, files)
        completed = subprocess.run(['python3', '-I', '-B', '-'], input=payload,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        capture = json.loads(completed.stdout)
        self.assertFalse(capture['capture_complete'])
        self.assertIn('continuity', capture['error'])

    def test_closed_archive_and_digest_binding(self):
        endpoint, user, alias, hostname = r.TARGETS['master']
        spec = {'kind': 'master', 'endpoint': endpoint, 'user': user, 'host_key_alias': alias,
                'hostname': hostname, 'operation_id': 'munin-offline-test',
                'prepared_epoch': int(time.time()), 'expires_epoch': int(time.time())+3600}
        files = {name: b'' for name in r.MEMBERS}
        files.update({'spec.json': r.encoded(spec), 'review.md': r.review(spec).encode()})
        files['manifest.json'] = r.encoded({n: r.sha(v) for n, v in files.items() if n != 'manifest.json'})
        def archive(inputs):
            buffer = io.BytesIO()
            with tarfile.open(fileobj=buffer, mode='w') as stream:
                for name, raw in inputs.items():
                    member = tarfile.TarInfo(name)
                    member.size = len(raw)
                    stream.addfile(member, io.BytesIO(raw))
            return buffer.getvalue()
        raw = archive(files)
        self.assertEqual(r.unpack(raw, r.sha(raw))[0], spec)
        with self.assertRaises(ValueError):
            r.unpack(raw, '0'*64)
        raw = archive({**files, 'collector.py': b'changed'})
        with self.assertRaises(ValueError):
            r.unpack(raw, r.sha(raw))
        raw = archive({**files, '../extra': b''})
        with self.assertRaises(ValueError):
            r.unpack(raw, r.sha(raw))

        spec.update(purpose='expanded-observation', commissioned_epoch=1,
                    collection_after_epoch=2, https_deadline_seconds=180,
                    expanded_provenance={'node': 'accepted', 'master': 'accepted'},
                    graphs={'j2-svntp1': ['df', 'df_inode', 'cpu'], 'J1-SVMF': ['ntp_transport_j2']},
                    rrd_fields={'j2-svntp1': {'df': {}, 'df_inode': {}, 'cpu': {'user': 'd'}},
                                'J1-SVMF': {'ntp_transport_j2': {'v4': 'g', 'v6': 'g', 'mail': 'g'}}},
                    dynamic_rrd_counts={'j2-svntp1': {'df': 6, 'df_inode': 6}})
        files.update({'spec.json': r.encoded(spec), 'review.md': r.review(spec).encode()})
        files['manifest.json'] = r.encoded({n: r.sha(v) for n, v in files.items() if n != 'manifest.json'})
        raw = archive(files)
        self.assertEqual(r.unpack(raw, r.sha(raw))[0]['collection_after_epoch'], 2)
        spec['rrd_fields']['j2-svntp1']['cpu']['../escape'] = 'g'
        files.update({'spec.json': r.encoded(spec), 'review.md': r.review(spec).encode()})
        files['manifest.json'] = r.encoded({n: r.sha(v) for n, v in files.items() if n != 'manifest.json'})
        raw = archive(files)
        with self.assertRaisesRegex(ValueError, 'filename scope'):
            r.unpack(raw, r.sha(raw))

    def test_receipt_is_consumed_even_for_incomplete_capture(self):
        spec = {'operation_id': 'munin-no-replay', 'kind': 'node', 'endpoint': '10.1.0.51',
                'user': 'ama', 'host_key_alias': '10.1.0.137'}
        calls = []
        def bounded(*args, **kwargs):
            calls.append(args)
            return {'returncode': 0, 'stdout': json.dumps({'operation_id': spec['operation_id'],
                'spec_sha256': r.sha(r.encoded(spec)), 'capture_complete': False}), 'stderr': ''}
        helper = types.SimpleNamespace(ssh_argv=lambda *args: ['ssh', 'ama@10.1.0.51', 'fixed'], bounded=bounded)
        with tempfile.TemporaryDirectory() as temporary, patch.object(r, 'prepare', return_value=(spec, {'helper.py': b''})), \
                patch.object(r, 'module', return_value=(helper, {})), patch.object(r, 'payload', return_value=b''):
            directory = Path(temporary)
            self.assertFalse(r.execute(directory, 'approved')['capture_complete'])
            with self.assertRaises(FileExistsError):
                r.execute(directory, 'approved')
        self.assertEqual(len(calls), 1)


if __name__ == '__main__':
    unittest.main()
