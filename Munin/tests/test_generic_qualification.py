#!/usr/bin/python3
"""Offline qualification boundaries; native plugin testing is separate."""
import importlib.util
import io
import json
import os
from pathlib import Path
import tarfile
import time
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT/'scripts'/name)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


q = module('qualify_generic.py')
q.c = module('review_ntp_observation.py')


class GenericQualificationTests(unittest.TestCase):
    def test_native_settings_isolate_every_plugin_and_preserve_privileges(self):
        names = json.loads((ROOT/'node/profiles/ntp/generic-parity.candidate.json').read_text())['requires_coordinated_master_expected_set']
        text = q.settings(names, Path('/var/lib/qualification')).decode()
        self.assertEqual(text.count('env.MUNIN_PLUGSTATE '), len(names))
        self.assertEqual(text.count('env.MUNIN_STATEFILE '), len(names))
        self.assertEqual(text.count('user root\n'), 2)
        for name in names:
            identity = 'root' if name in ('ntp_statistics', 'ntp_jobs') else 'munin'
            self.assertIn('['+name+']\nuser '+identity+'\ngroup '+identity+'\n', text)

    def test_fields_keep_unknowns_and_cover_multigraphs(self):
        config = 'multigraph a\ngraph_title test\nx.label X\ny.label Y\ny.cdef x,2,*\nmultigraph b\ngraph_title other\nz.label Z\n'
        fetch = 'multigraph a\nx.value 0\nmultigraph b\nz.value U\n'
        row = q.fields(config, fetch)
        self.assertEqual(row['configured_fields'], 2)
        self.assertEqual(row['numeric_fields'], 1)
        self.assertEqual(row['unknown_fields'], [['b', 'z']])
        for bad in ('multigraph a\nx.value nan\n', fetch+'z.value 1\n', 'x.value 0\n'):
            with self.assertRaises(ValueError):
                q.fields(config, bad)

    def test_nfs_dispositions_follow_actual_markers(self):
        self.assertEqual(q.nfs_capability(b''), {'nfs_client': False, 'nfs4_client': False})
        self.assertEqual(q.nfs_capability(b'proc3 22 1 2\nproc4 77 0\n'), {'nfs_client': True, 'nfs4_client': True})
        self.assertFalse(q.nfs_capability(b'proc30 1\nproc40 1\n')['nfs_client'])

    def test_nfs_read_uses_concrete_current_process_namespace(self):
        path = q.nfs_proc_path()
        self.assertEqual(path, Path('/proc')/str(os.getpid())/'net/rpc/nfs')
        self.assertFalse(any(p.is_symlink() for p in path.parents))
        self.assertNotIn('/self/', str(path))
        self.assertNotEqual(str(path), '/proc/net/rpc/nfs')

    def test_missing_native_command_does_not_escalate_or_hide_failure(self):
        failure = {'returncode': 1, 'stdout': '', 'stderr': 'missing dependency'}
        with patch.object(q, 'invoke', return_value=failure):
            row = q.workload(Path('/unused'), ['netstat'], 'test')
        self.assertFalse(row['complete'])
        self.assertIn('error', row['plugins']['netstat'])

    def test_self_referencing_cdef_requires_raw_counter(self):
        config = 'graph_title traffic\ndown.label received\ndown.cdef down,8,*\nup.label sent\nup.cdef up,8,*\n'
        self.assertEqual(q.fields(config, 'down.value 0\nup.value 42\n')['configured_fields'], 2)
        with self.assertRaises(ValueError):
            q.fields(config, 'up.value 42\n')

    def test_diskstats_cold_exception_is_explicit_and_limited(self):
        config = {'returncode': 0, 'stdout': 'graph_title disk\nx.label X\n', 'stderr': ''}
        fetch = {'returncode': 0, 'stdout': '', 'stderr': ''}
        with patch.object(q, 'invoke', side_effect=[config, fetch]):
            row = q.workload(Path('/unused'), ['diskstats'], 'cold', allow_diskstats_cold=True)
        self.assertTrue(row['plugins']['diskstats']['cold_start_no_sample'])
        with patch.object(q, 'invoke', side_effect=[config, fetch]):
            self.assertFalse(q.workload(Path('/unused'), ['diskstats'], 'warm')['complete'])

    def test_real_budget_cannot_be_bypassed(self):
        with patch.object(q.time, 'monotonic', side_effect=[0, 26, 26]):
            row = q.workload(Path('/unused'), ['cpu'], 'test')
        self.assertIn('25-second', row['error'])

    def test_failed_preflight_still_records_continuity_check(self):
        observer = types.SimpleNamespace(continuity=lambda _: {'unchanged': True})
        with patch.object(q, 'h', q.c), patch.object(q, 'o', observer), patch.object(q, 'snapshot_selection', side_effect=ValueError('drift')):
            row = q.qualify({'operation_id': 'test'})
        self.assertFalse(row['capture_complete'])
        self.assertFalse(row['stage_created'])
        self.assertIn('continuity_error', row)

    def test_remote_bootstrap_has_no_controller_main_or_local_source_import(self):
        helper = b'def expired(*args): pass\ndef sha(x): return "digest"\ndef encoded(x): return b"spec"\n'
        observer = b'h=None\n'
        spec = {'operation_id': 'test'}
        namespace = {'load': q.load, 'signal': types.SimpleNamespace(SIGALRM=1, signal=lambda *x: None, alarm=lambda *x: None),
                     'json': json, 'qualify': lambda s: {'operation_id': s['operation_id']}}
        code = q.payload(spec, {'helper.py': helper, 'observer.py': observer})
        # Replace only signal registration locally; executing payload itself does not contact a host.
        with patch('signal.signal'), patch('signal.alarm'), patch('builtins.print') as output:
            exec(code, namespace)
        self.assertEqual(json.loads(output.call_args.args[0])['operation_id'], 'test')
        self.assertIs(namespace['on']['h'], namespace['h'])

    def test_hash_closed_members_and_review_are_bound(self):
        now = int(time.time())
        spec = dict(kind='node', endpoint='10.1.0.51', user='ama', host_key_alias='10.1.0.137',
                    hostname='j2-svntp1', operation_id='munin-generic-qualification-20261021-v1',
                    stage='/var/lib/munin-generic-qualification-20261021-v1',
                    prepared_epoch=now, expires_epoch=now+86400)
        files = {name: b'data' for name in q.MEMBERS-{'manifest.json'}}
        files.update({'spec.json': q.c.encoded(spec), 'review.md': q.review(spec).encode()})

        def archive(extra=False):
            files['manifest.json'] = q.c.encoded({n: q.c.sha(v) for n, v in files.items() if n != 'manifest.json'})
            stream = io.BytesIO()
            with tarfile.open(fileobj=stream, mode='w') as tar:
                for name, data in list(files.items())+([('extra', b'bad')] if extra else []):
                    row = tarfile.TarInfo(name)
                    row.size = len(data)
                    tar.addfile(row, io.BytesIO(data))
            return stream.getvalue()

        raw = archive()
        self.assertEqual(q.unpack(raw, q.c.sha(raw))[0], spec)
        with self.assertRaises(ValueError):
            q.unpack(raw, '0'*64)
        raw = archive(True)
        with self.assertRaises(ValueError):
            q.unpack(raw, q.c.sha(raw))
        files['review.md'] += b'altered'
        raw = archive()
        with self.assertRaises(ValueError):
            q.unpack(raw, q.c.sha(raw))


if __name__ == '__main__':
    unittest.main()
