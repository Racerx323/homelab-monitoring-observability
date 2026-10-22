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
    def test_contact_status_reads_real_private_snapshot_without_delivery_inference(self):
        with tempfile.TemporaryDirectory() as tmp:
            status = Path(tmp)/'status.json'
            status.write_text(json.dumps({'schema': 1, 'submission_ok': True, 'attempt_epoch': 100.5}))
            status.chmod(0o600)
            real_read = o.read
            identity = types.SimpleNamespace(pw_uid=os.getuid(), pw_gid=os.getgid())
            with patch.object(o.pwd, 'getpwnam', return_value=identity), \
                    patch.object(o, 'read', side_effect=lambda path, limit: real_read(status, limit)):
                value = o.contact_status()
                self.assertTrue(value['value']['submission_ok'])
                self.assertFalse(value['downstream_delivery_proven'])
                self.assertFalse(value['sender_attribution_available'])
                os.link(status, Path(tmp)/'unreviewed-link')
                self.assertIn('finding', o.contact_status())
                (Path(tmp)/'unreviewed-link').unlink()
                status.write_text(json.dumps({'schema': 1, 'submission_ok': 1, 'attempt_epoch': 100.5}))
                self.assertIn('finding', o.contact_status())
                status.chmod(0o644)
                self.assertIn('finding', o.contact_status())

    def test_contact_observation_archive_is_closed_to_paths_graphs_and_provenance(self):
        endpoint, user, alias, hostname = r.TARGETS['master']
        now = time.time()
        provenance = {'activation': dict.fromkeys(('archive_sha256', 'receipt_sha256', 'result_sha256'), 'a'*64)}
        for kind in ('problem', 'recovery'):
            provenance[kind] = dict(provenance['activation'], confirmation_sha256='b'*64,
                                    message_sha256='c'*64, submission_accepted=kind == 'recovery')
        spec = {'schema': 1, 'purpose': 'contact-observation', 'kind': 'master',
                'operation_id': 'munin-contact-observation-test', 'endpoint': endpoint, 'user': user,
                'host_key_alias': alias, 'hostname': hostname, 'boot_id': 'boot',
                'prepared_epoch': now, 'expires_epoch': now+3600,
                'units': dict.fromkeys(('NetworkManager.service', 'apache2.service', 'cron.service', 'munin-node.service'), {}),
                'files': dict.fromkeys(r.CONTACT_FILES, 'd'*64), 'commissioned_epoch': now-60,
                'collection_after_epoch': now-60, 'graphs': {'J1-SVMF': ['ntp_transport_j2']},
                'rrd_fields': {'J1-SVMF': {'ntp_transport_j2': {'mail': 'g'}}},
                'contact_state_path': '/var/lib/munin-ntp-contacts/munin-contacts-activate-20261022-v3/state.json',
                'contact_provenance': provenance}
        def archive(scope):
            files = {n: p.read_bytes() for n, p in r.SOURCES.items()}
            files.update({'spec.json': r.encoded(scope), 'review.md': r.review(scope).encode(),
                          'known_hosts': b'local test only', 'ca.pem': b''})
            files['manifest.json'] = r.encoded({n: r.sha(v) for n, v in files.items()})
            output = io.BytesIO()
            with tarfile.open(fileobj=output, mode='w') as stream:
                for name, raw in files.items():
                    member = tarfile.TarInfo(name)
                    member.size = len(raw)
                    stream.addfile(member, io.BytesIO(raw))
            return output.getvalue()
        raw = archive(spec)
        self.assertEqual(r.unpack(raw, r.sha(raw))[0], spec)
        for change in ('extra-file', 'extra-graph', 'missing-confirmation', 'arbitrary-state', 'extra-option'):
            altered = json.loads(json.dumps(spec))
            if change == 'extra-file':
                altered['files']['/etc/shadow'] = 'e'*64
            elif change == 'extra-graph':
                altered['rrd_fields']['J1-SVMF']['ntp_transport_j2']['v4'] = 'g'
            elif change == 'missing-confirmation':
                del altered['contact_provenance']['problem']['confirmation_sha256']
            elif change == 'arbitrary-state':
                altered['contact_state_path'] = '/foreign/state.json'
            else:
                altered['smtp_probe'] = True
            raw = archive(altered)
            with self.assertRaises(ValueError):
                r.unpack(raw, r.sha(raw))

    def test_contact_metadata_exposes_real_hardlink_predicate_without_exporting_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            main = Path(tmp)/'main'
            proof = Path(tmp)/'proof'
            main.write_bytes(b'contacts none\n')
            main.chmod(0o600)
            os.link(main, proof)
            real_read = o.read
            expected = {'sha256': r.sha(main.read_bytes()), 'mode': 0o600,
                        'uid': os.getuid(), 'gid': os.getgid(), 'nlink': 1}
            def local_read(path, limit):
                return real_read(main if str(path) == '/etc/munin/munin.conf' else proof, limit)
            with patch.object(o, 'read', side_effect=local_read):
                result = o.contact_metadata({'contact_expected': expected})
            self.assertTrue(result['same_inode_as_predecessor_proof'])
            self.assertFalse(result['main']['matches']['nlink'])
            self.assertEqual(result['main']['metadata']['nlink'], 2)
            self.assertTrue(all(value for key, value in result['main']['matches'].items() if key != 'nlink'))
            self.assertNotIn('contacts none', json.dumps(result))
            linked = Path(tmp)/'symlink'
            linked.symlink_to(main)
            with self.assertRaises(OSError):
                real_read(linked)

    def test_contact_metadata_archive_rejects_broadened_predicates(self):
        endpoint, user, alias, hostname = r.TARGETS['master']
        now = time.time()
        spec = {'kind': 'master', 'purpose': 'contact-metadata', 'endpoint': endpoint,
                'user': user, 'host_key_alias': alias, 'hostname': hostname,
                'operation_id': 'munin-contact-metadata-test', 'prepared_epoch': now, 'expires_epoch': now+3600,
                'files': {'/etc/munin/munin.conf': 'a'*64},
                'contact_expected': {'sha256': 'a'*64, 'uid': 0, 'gid': 0, 'mode': 0o644, 'nlink': 1},
                'failed_activation_provenance': {'archive_sha256': 'b'*64}}
        def archive(scope):
            files = {n: p.read_bytes() for n, p in r.SOURCES.items()}
            files.update({'spec.json': r.encoded(scope), 'review.md': r.review(scope).encode(),
                          'known_hosts': b'local test only', 'ca.pem': b''})
            files['manifest.json'] = r.encoded({n: r.sha(v) for n, v in files.items()})
            output = io.BytesIO()
            with tarfile.open(fileobj=output, mode='w') as stream:
                for name, raw in files.items():
                    member = tarfile.TarInfo(name)
                    member.size = len(raw)
                    stream.addfile(member, io.BytesIO(raw))
            return output.getvalue()
        raw = archive(spec)
        self.assertEqual(r.unpack(raw, r.sha(raw))[0]['purpose'], 'contact-metadata')
        for change in ('nlink', 'extra', 'missing-provenance'):
            altered = json.loads(json.dumps(spec))
            if change == 'nlink':
                altered['contact_expected']['nlink'] = 2
            elif change == 'extra':
                altered['contact_expected']['extra'] = 'unreviewed'
            else:
                del altered['failed_activation_provenance']
            raw = archive(altered)
            with self.assertRaises(ValueError):
                r.unpack(raw, r.sha(raw))

    def test_timing_observation_rejects_missing_or_wrong_commit_context(self):
        helper = types.SimpleNamespace(sha=r.sha, encoded=r.encoded)
        spec = {'operation_id':'test','kind':'master','purpose':'timing-observation',
                'prepared_epoch':1,'correction_prerequisite':{'archive_sha256':'a'*64}}
        with patch.object(o,'h',helper),patch.object(o,'continuity',return_value={}):
            for context in (None,{'node_archive_sha256':'b'*64,'commit_finished_epoch':2}):
                result=o.collect(spec,context)
                self.assertFalse(result['capture_complete'])
                self.assertIn('context',result['error'])

    def test_timing_observation_uses_actual_commit_cutoff_without_changing_spec_binding(self):
        helper = types.SimpleNamespace(sha=r.sha, encoded=r.encoded)
        spec = {'operation_id':'test','kind':'master','purpose':'timing-observation',
                'prepared_epoch':200,'collection_after_epoch':2,
                'correction_prerequisite':{'archive_sha256':'a'*64,'prepared_epoch':1}}
        context={'node_archive_sha256':'a'*64,'commit_finished_epoch':100}
        with patch.object(o,'h',helper),patch.object(o,'continuity',return_value={}), \
                patch.object(o,'listing',return_value=[]),patch.object(o,'master',return_value={}) as master:
            result=o.collect(spec,context)
        self.assertTrue(result['capture_complete'])
        self.assertEqual(master.call_args.args[0]['collection_after_epoch'],100)
        self.assertEqual(spec['collection_after_epoch'],2)
        self.assertEqual(result['spec_sha256'],r.sha(r.encoded(spec)))
        self.assertEqual(result['runtime_context_sha256'],r.sha(r.encoded(context)))
    def test_maintenance_https_is_ten_requests_for_only_two_job_graphs(self):
        spec = {'purpose': 'maintenance-observation',
                'graphs': {'j2-svntp1': ['ntp_job_age', 'ntp_job_evidence']},
                'operation_id': 'munin-maintenance-test', 'expires_epoch': time.time()+3600}
        paths = r.https_paths(spec)
        self.assertEqual(len(paths)*2, 10)
        self.assertEqual(sum(path.endswith('.png') for path in paths), 2)
        text = r.review(spec)
        self.assertIn('four exact direct RRDs', text)
        self.assertIn('Contacts remain disabled', text)
        self.assertIn('no parser, limits or contact command', text)

    def test_maintenance_archive_rejects_broadened_fields_and_missing_native_pins(self):
        endpoint, user, alias, hostname = r.TARGETS['master']
        now = int(time.time())
        spec = {'kind': 'master', 'purpose': 'maintenance-observation', 'endpoint': endpoint,
                'user': user, 'host_key_alias': alias, 'hostname': hostname,
                'operation_id': 'munin-maintenance-test', 'prepared_epoch': now,
                'expires_epoch': now+3600, 'producer_installed_epoch': now-7200,
                'producer_completions': {'retention': now-3600, 'reporting': now-1800},
                'collection_after_epoch': now-1800, 'https_deadline_seconds': 90,
                'producer_observation_provenance': {'capture_sha256': 'a'*64},
                'native_limits_sources': dict.fromkeys(r.LIMITS_SOURCES, 'b'*64),
                'files': dict.fromkeys(r.LIMITS_SOURCES, 'b'*64),
                'graphs': {'j2-svntp1': ['ntp_job_age', 'ntp_job_evidence']},
                'rrd_fields': {'j2-svntp1': {
                    'ntp_job_age': {'retention_age': 'g', 'reporting_age': 'g'},
                    'ntp_job_evidence': {'retention_evidence': 'g', 'reporting_evidence': 'g'}}}}
        def archive(scope):
            files = dict.fromkeys(r.MEMBERS, b'')
            files.update({'spec.json': r.encoded(scope), 'review.md': r.review(scope).encode()})
            files['manifest.json'] = r.encoded({k: r.sha(v) for k, v in files.items() if k != 'manifest.json'})
            output = io.BytesIO()
            with tarfile.open(fileobj=output, mode='w') as stream:
                for name, raw in files.items():
                    member = tarfile.TarInfo(name)
                    member.size = len(raw)
                    stream.addfile(member, io.BytesIO(raw))
            return output.getvalue()
        raw = archive(spec)
        self.assertEqual(r.unpack(raw, r.sha(raw))[0]['purpose'], 'maintenance-observation')
        for key in ('extra-field', 'missing-module', 'old-cutoff'):
            altered = json.loads(json.dumps(spec))
            if key == 'extra-field':
                altered['rrd_fields']['j2-svntp1']['ntp_job_age']['other'] = 'g'
            elif key == 'missing-module':
                altered['native_limits_sources'].pop(r.LIMITS_SOURCES[0])
            else:
                altered['collection_after_epoch'] = now-5000
            raw = archive(altered)
            with self.assertRaisesRegex(ValueError, 'maintenance observation boundary'):
                r.unpack(raw, r.sha(raw))

    def test_maintenance_rejects_unexpected_effective_include_without_reading_it(self):
        helper = types.SimpleNamespace(sha=r.sha, encoded=r.encoded)
        with patch.object(o, 'h', helper), patch.object(o, 'continuity', return_value={}), \
                patch.object(o, 'listing', return_value=['new-contact.conf']), \
                patch.object(o, 'master') as master:
            result = o.collect({'operation_id': 'test', 'kind': 'master', 'purpose': 'maintenance-observation'})
        self.assertFalse(result['capture_complete'])
        self.assertIn('contacts-disabled', result['error'])
        master.assert_not_called()

    def test_maintenance_uses_native_hidden_and_backup_exclusion_rules(self):
        helper = types.SimpleNamespace(sha=r.sha, encoded=r.encoded)
        with patch.object(o, 'h', helper), patch.object(o, 'continuity', return_value={}), \
                patch.object(o, 'listing', return_value=['.hidden', 'backup~']), \
                patch.object(o, 'master', return_value={}) as master:
            result = o.collect({'operation_id': 'test', 'kind': 'master', 'purpose': 'maintenance-observation'})
        self.assertTrue(result['capture_complete'])
        self.assertTrue(result['observations']['effective_includes_empty'])
        master.assert_called_once()

    def test_source_socket_filter_keeps_actual_source_and_rejects_other_flows(self):
        header = 'sl local_address rem_address st tx_queue rx tr uid timeout inode\n'
        row = '0: 5303010A:C001 3300010A:1355 01 0:0 00:0 0 108 0 123\n'
        result = o.canonical_sockets((header+row).encode())
        self.assertEqual(result[0]['source'], '10.1.3.83')
        self.assertEqual(result[0]['inode'], 123)
        for altered in (row.replace('1355', '0016'), row.replace(' 01 ', ' 06 '),
                        row.replace('3300010A', '3600010A')):
            self.assertEqual(o.canonical_sockets((header+altered).encode()), [])
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            o.canonical_sockets((header+'broken\n').encode())

    def test_source_review_requires_passive_scope_and_separate_timeout(self):
        spec = {'purpose': 'source-attribution', 'operation_id': 'munin-source-test',
                'expires_epoch': int(time.time())+3600}
        text = r.review(spec)
        self.assertIn('360 monotonic seconds', text)
        self.assertIn('no captured connection', text)
        self.assertIn('No packet capture', text)
        self.assertIn('Contacts stay', text)
        payload = r.payload(spec, {'helper.py': b'', 'collector.py': b''})
        self.assertIn(b'signal.alarm(480)', payload)
        self.assertNotIn(b'signal.alarm(240)', payload)

    def test_process_classification_does_not_export_arbitrary_arguments(self):
        # Exercise the live local proc reader against this test process only.
        identity = o.process_identity(os.getpid())
        self.assertEqual(identity['pid'], os.getpid())
        self.assertGreater(identity['start_ticks'], 0)
        self.assertEqual(set(identity), {'pid', 'ppid', 'start_ticks', 'uid', 'command_tags'})
        self.assertEqual(identity['command_tags'], [])

    def test_passive_sampling_miss_remains_unaccepted(self):
        with patch.object(o.pwd, 'getpwnam', return_value=types.SimpleNamespace(pw_uid=108)), \
                patch.object(o.time, 'monotonic', side_effect=[0, 0, 360, 360]), \
                patch.object(o.time, 'sleep') as sleep, \
                patch.object(o, 'read', side_effect=[(b'header\n', {}), (b'', {})]), \
                patch.object(o, 'journal', return_value=[]), \
                patch.object(o, 'socket_owners') as owners:
            result = o.source_attribution({})
        self.assertEqual(result['scans'], 1)
        self.assertEqual(result['connections'], [])
        self.assertFalse(result['source_address_attribution_accepted'])
        owners.assert_not_called()
        sleep.assert_called_once_with(0)

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
