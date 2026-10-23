#!/usr/bin/python3
"""Local filesystem and closed-scope checks; never contact a target."""
import importlib.util
import io
import json
import os
from pathlib import Path
import tarfile
import tempfile
import time
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


r = load(ROOT/'scripts/review_ntp_observation.py')
g = load(ROOT/'scripts/observe_ntp_growth.py')
g.statistics = load(r.SOURCES['statistics.py'])


def archive(spec):
    files = {n: p.read_bytes() for n, p in r.SOURCES.items()}
    files.update({'spec.json': r.encoded(spec), 'review.md': r.review(spec).encode(),
                  'known_hosts': b'local-only test', 'ca.pem': b''})
    files['manifest.json'] = r.encoded({n: r.sha(v) for n, v in files.items()})
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode='w') as stream:
        for name, raw in files.items():
            row = tarfile.TarInfo(name)
            row.size = len(raw)
            stream.addfile(row, io.BytesIO(raw))
    return output.getvalue(), files


def scope():
    now = time.time()
    endpoint, user, alias, hostname = r.TARGETS['node']
    spec = {'schema': 1, 'purpose': 'growth-t0', 'kind': 'node', 'operation_id': 'munin-growth-t0-test',
            'endpoint': endpoint, 'user': user, 'host_key_alias': alias, 'hostname': hostname,
            'boot_id': 'local-test', 'prepared_epoch': now, 'expires_epoch': now+3600,
            'units': {'timeservice.service': {}}, 'files': {'/etc/ntp.conf': 'a'*64},
            'contract_sha256': r.sha(r.SOURCES['contract.md'].read_bytes()), 'growth_policy': r.GROWTH_POLICY,
            'growth_provenance': {key: dict.fromkeys(('archive_sha256', 'receipt_sha256', 'result_sha256', 'outcome_sha256'), 'b'*64)
                                  for key in r.GROWTH_STAGES},
            'producer_installed_epoch': now-3600, 'enabled_links': {str(i): ['link', '/local-test'] for i in range(33)}}
    spec['baseline_files_sha256'] = r.sha(r.encoded(spec['files']))
    spec['enabled_links_sha256'] = r.sha(r.encoded(spec['enabled_links']))
    return spec


class GrowthTests(unittest.TestCase):
    def checkpoint_scope(self, label='+6h'):
        spec = scope()
        epoch = time.time()-(30*3600 if label == '+48h' else 3600)
        proof = {'directory': '/local-only', **dict.fromkeys(
            ('archive_sha256', 'capture_sha256', 'receipt_sha256', 'result_sha256', 'outcome_sha256'), 'a'*64)}
        spec.update(purpose='growth-checkpoint', expires_epoch=spec['prepared_epoch']+86400,
                    checkpoint_scope={'label': label, 'offset_seconds': r.GROWTH_CHECKPOINTS[label],
                        'node_t0_epoch': epoch, 'not_before_epoch': epoch+r.GROWTH_CHECKPOINTS[label],
                        't0': {'node': proof, 'master': proof}})
        if label in r.GROWTH_PREVIOUS:
            spec['checkpoint_scope']['previous'] = {
                'node': proof, 'master': proof, 'restart_disposition_sha256': 'c'*64}
        return spec

    def test_checkpoint_archive_closes_timing_proofs_and_payload(self):
        spec = self.checkpoint_scope()
        raw, files = archive(spec)
        self.assertEqual(r.unpack(raw, r.sha(raw))[0], spec)
        compile(r.payload(spec, files), '<sealed-checkpoint>', 'exec')
        for key, value in [('offset_seconds', 1), ('not_before_epoch', time.time()),
                           ('label', '+24h'), ('node_t0_epoch', float('nan'))]:
            bad = json.loads(json.dumps(spec))
            bad['checkpoint_scope'][key] = value
            raw, _ = archive(bad)
            with self.assertRaises(ValueError):
                r.unpack(raw, r.sha(raw))
        bad = json.loads(json.dumps(spec))
        bad['checkpoint_scope']['t0']['node']['extra_path'] = '/etc/shadow'
        raw, _ = archive(bad)
        with self.assertRaises(ValueError):
            r.unpack(raw, r.sha(raw))

    def test_early_checkpoint_blocks_both_roles_before_receipt_or_transport(self):
        for kind in ('node', 'master'):
            with tempfile.TemporaryDirectory() as tmp:
                spec = dict(self.checkpoint_scope(), kind=kind)
                with patch.object(r, 'prepare', return_value=(spec, {})), \
                        patch.object(r, 'accepted_t0') as proof, patch.object(r, 'module') as module:
                    with self.assertRaisesRegex(ValueError, 'not due'):
                        r.execute(Path(tmp), 'a'*64)
                    proof.assert_not_called()
                    module.assert_not_called()
                self.assertFalse((Path(tmp)/'execution.json').exists())

    def test_checkpoint_proof_drift_blocks_before_receipt_or_transport(self):
        spec = self.checkpoint_scope()
        spec['checkpoint_scope']['not_before_epoch'] = time.time()-1
        with tempfile.TemporaryDirectory() as tmp, \
                patch.object(r, 'prepare', return_value=(spec, {})), \
                patch.object(r, 'accepted_t0', return_value=({}, {}, spec['checkpoint_scope']['node_t0_epoch'])), \
                patch.object(r, 'module') as module:
            with self.assertRaisesRegex(ValueError, 'proof changed'):
                r.execute(Path(tmp), 'a'*64)
            module.assert_not_called()
            self.assertFalse((Path(tmp)/'execution.json').exists())

    def test_target_early_checkpoint_does_not_observe(self):
        spec = self.checkpoint_scope()
        helper = types.SimpleNamespace(sha=r.sha, encoded=r.encoded)
        with patch.object(g, 'h', helper), patch.object(g, 'observer') as observer:
            result = g.collect(spec)
            self.assertFalse(result['capture_complete'])
            self.assertIn('not due', result['error'])
            observer.continuity.assert_not_called()

    def test_missing_reviewed_checkpoint_node_blocks_master(self):
        spec = dict(self.checkpoint_scope(), kind='master')
        spec['checkpoint_scope']['not_before_epoch'] = time.time()-1
        def retained(directory, role):
            return spec['checkpoint_scope']['t0'][role], {}, spec['checkpoint_scope']['node_t0_epoch']
        with tempfile.TemporaryDirectory() as tmp, \
                patch.object(r, 'prepare', return_value=(spec, {})), \
                patch.object(r, 'accepted_t0', side_effect=retained), \
                patch.object(r, 'growth_baselines', return_value=(spec['growth_provenance'], {})), \
                patch.object(r, 'node_t0_context', side_effect=ValueError('checkpoint not accepted')), \
                patch.object(r, 'module') as module:
            with self.assertRaisesRegex(ValueError, 'not accepted'):
                r.execute(Path(tmp), 'a'*64)
            module.assert_not_called()
            self.assertFalse((Path(tmp)/'execution.json').exists())

    def test_checkpoint_master_requires_exact_reviewed_due_node_capture(self):
        spec = self.checkpoint_scope('+24h')
        spec['checkpoint_scope']['node_t0_epoch'] = time.time()-90000
        spec['checkpoint_scope']['not_before_epoch'] = spec['checkpoint_scope']['node_t0_epoch']+86400
        raw, _ = archive(spec)
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            epoch = time.time()-10
            capture = {'capture_complete': True, 'target_mutation': False,
                       'spec_sha256': r.sha(r.encoded(spec)), 'before': {'boot': 'same'},
                       'after': {'boot': 'same'},
                       'observations': {'statistics_before': {'started_epoch': epoch}}}
            receipt = r.encoded({'sha256': r.sha(raw)})
            outcome = {'growth_checkpoint_node_accepted': True, 'archive_sha256': r.sha(raw),
                       'capture_sha256': r.sha(r.encoded(capture)),
                       'execution_receipt_sha256': r.sha(receipt), 'checkpoint_node_epoch': epoch}
            data = {'inspection.tar': raw, 'execution.json': receipt, 'stdout.txt': r.encoded(capture),
                    'result.json': r.encoded({'returncode': 0, 'capture_complete': True,
                                             'bundle_sha256': r.sha(raw)}),
                    'outcome.json': r.encoded(outcome)}
            for name, value in data.items():
                (directory/name).write_bytes(value)
                (directory/name).chmod(0o600)
            master = dict(spec, kind='master', node_t0_prerequisite={
                'directory': str(directory), 'archive_sha256': r.sha(raw)})
            context = r.node_t0_context(master)
            self.assertEqual(context['node_t0_epoch'], spec['checkpoint_scope']['node_t0_epoch'])
            self.assertEqual(context['checkpoint_node_epoch'], epoch)
            for key, value in [('growth_checkpoint_node_accepted', False),
                               ('capture_sha256', 'f'*64), ('checkpoint_node_epoch', epoch-1)]:
                bad = dict(outcome, **{key: value})
                (directory/'outcome.json').write_bytes(r.encoded(bad))
                with self.assertRaises(ValueError):
                    r.node_t0_context(master)

    def test_daily_scope_requires_exact_offset_and_previous_pair(self):
        spec = self.checkpoint_scope('+24h')
        raw, files = archive(spec)
        self.assertEqual(r.unpack(raw, r.sha(raw))[0], spec)
        compile(r.payload(spec, files), '<daily-checkpoint>', 'exec')
        for change in ('offset', 'missing-previous', 'restart-hash', 'previous-extra'):
            bad = json.loads(json.dumps(spec))
            cp = bad['checkpoint_scope']
            if change == 'offset':
                cp['offset_seconds'] = 21600
            elif change == 'missing-previous':
                del cp['previous']
            elif change == 'restart-hash':
                cp['previous']['restart_disposition_sha256'] = 'unbound'
            else:
                cp['previous']['node']['unreviewed'] = True
            raw, _ = archive(bad)
            with self.assertRaises(ValueError):
                r.unpack(raw, r.sha(raw))

    def test_daily_early_guard_on_both_controller_roles_and_target(self):
        for kind in ('node', 'master'):
            spec = dict(self.checkpoint_scope('+24h'), kind=kind)
            with tempfile.TemporaryDirectory() as tmp, \
                    patch.object(r, 'prepare', return_value=(spec, {})), \
                    patch.object(r, 'module') as module, patch.object(r, 'accepted_t0') as proof:
                with self.assertRaisesRegex(ValueError, 'not due'):
                    r.execute(Path(tmp), 'a'*64)
                module.assert_not_called()
                proof.assert_not_called()
                self.assertFalse((Path(tmp)/'execution.json').exists())
            with patch.object(g, 'h', types.SimpleNamespace(sha=r.sha, encoded=r.encoded)), \
                    patch.object(g, 'observer') as observer:
                capture = g.collect(spec)
                self.assertFalse(capture['capture_complete'])
                self.assertIn('+24h checkpoint is not due', capture['error'])
                observer.continuity.assert_not_called()

    def test_changed_daily_previous_proof_blocks_before_receipt_or_transport(self):
        spec = self.checkpoint_scope('+24h')
        spec['checkpoint_scope']['not_before_epoch'] = time.time()-1
        def retained(directory, role):
            return spec['checkpoint_scope']['t0'][role], {}, spec['checkpoint_scope']['node_t0_epoch']
        with tempfile.TemporaryDirectory() as tmp, \
                patch.object(r, 'prepare', return_value=(spec, {})), \
                patch.object(r, 'accepted_t0', side_effect=retained), \
                patch.object(r, 'previous_checkpoint', return_value={}), \
                patch.object(r, 'module') as module:
            with self.assertRaisesRegex(ValueError, 'late checkpoint proof changed'):
                r.execute(Path(tmp), 'a'*64)
            module.assert_not_called()
            self.assertFalse((Path(tmp)/'execution.json').exists())

    def test_daily_master_missing_acceptance_blocks_before_receipt_or_transport(self):
        spec = dict(self.checkpoint_scope('+24h'), kind='master')
        spec['checkpoint_scope']['not_before_epoch'] = time.time()-1
        def retained(directory, role):
            return spec['checkpoint_scope']['t0'][role], {}, spec['checkpoint_scope']['node_t0_epoch']
        with tempfile.TemporaryDirectory() as tmp, \
                patch.object(r, 'prepare', return_value=(spec, {})), \
                patch.object(r, 'accepted_t0', side_effect=retained), \
                patch.object(r, 'previous_checkpoint', return_value=spec['checkpoint_scope']['previous']), \
                patch.object(r, 'growth_baselines', return_value=(spec['growth_provenance'], {})), \
                patch.object(r, 'node_t0_context', side_effect=ValueError('daily node not accepted')), \
                patch.object(r, 'module') as module:
            with self.assertRaisesRegex(ValueError, 'daily node not accepted'):
                r.execute(Path(tmp), 'a'*64)
            module.assert_not_called()
            self.assertFalse((Path(tmp)/'execution.json').exists())

    def test_closing_scope_binds_48h_and_previous_pair(self):
        spec = self.checkpoint_scope('+48h')
        raw, files = archive(spec)
        self.assertEqual(r.unpack(raw, r.sha(raw))[0], spec)
        compile(r.payload(spec, files), '<closing-checkpoint>', 'exec')
        for change in ('offset', 'missing-previous', 'missing-t0'):
            bad = json.loads(json.dumps(spec))
            if change == 'offset':
                bad['checkpoint_scope']['offset_seconds'] = 86400
            elif change == 'missing-previous':
                del bad['checkpoint_scope']['previous']
            else:
                del bad['checkpoint_scope']['t0']['master']
            raw, _ = archive(bad)
            with self.assertRaises(ValueError):
                r.unpack(raw, r.sha(raw))

    def test_closing_early_and_master_acceptance_guards(self):
        for kind in ('node', 'master'):
            spec = dict(self.checkpoint_scope('+48h'), kind=kind)
            with tempfile.TemporaryDirectory() as tmp, \
                    patch.object(r, 'prepare', return_value=(spec, {})), \
                    patch.object(r, 'accepted_t0') as proof, patch.object(r, 'module') as module:
                with self.assertRaisesRegex(ValueError, 'not due'):
                    r.execute(Path(tmp), 'a'*64)
                module.assert_not_called()
                proof.assert_not_called()
                self.assertFalse((Path(tmp)/'execution.json').exists())
            with patch.object(g, 'h', types.SimpleNamespace(sha=r.sha, encoded=r.encoded)), \
                    patch.object(g, 'observer') as observer:
                capture = g.collect(spec)
                self.assertFalse(capture['capture_complete'])
                self.assertIn('+48h checkpoint is not due', capture['error'])
                observer.continuity.assert_not_called()
        spec = dict(self.checkpoint_scope('+48h'), kind='master')
        spec['checkpoint_scope']['not_before_epoch'] = time.time()-1
        def retained(directory, role):
            return spec['checkpoint_scope']['t0'][role], {}, spec['checkpoint_scope']['node_t0_epoch']
        with tempfile.TemporaryDirectory() as tmp, \
                patch.object(r, 'prepare', return_value=(spec, {})), \
                patch.object(r, 'accepted_t0', side_effect=retained), \
                patch.object(r, 'previous_checkpoint', return_value=spec['checkpoint_scope']['previous']), \
                patch.object(r, 'growth_baselines', return_value=(spec['growth_provenance'], {})), \
                patch.object(r, 'node_t0_context', side_effect=ValueError('closing node not accepted')), \
                patch.object(r, 'module') as module:
            with self.assertRaisesRegex(ValueError, 'closing node not accepted'):
                r.execute(Path(tmp), 'a'*64)
            module.assert_not_called()
            self.assertFalse((Path(tmp)/'execution.json').exists())

    def test_previous_daily_proof_checks_the_full_earlier_chain(self):
        epoch = time.time()-100000
        t0 = {'node': 'original', 'master': 'original'}
        def proof(directory, token):
            return {'directory': str(directory), **dict.fromkeys(
                ('archive_sha256', 'capture_sha256', 'receipt_sha256', 'result_sha256', 'outcome_sha256'), token*64)}
        node6, master6, node24, master24 = map(Path, ('/prior6/node', '/prior6/master', '/prior24/node', '/prior24/master'))
        n6, m6, n24, m24 = proof(node6, 'a'), proof(master6, 'b'), proof(node24, 'c'), proof(master24, 'd')
        note = b'operator-confirmed overnight restart'
        previous = {'node': n6, 'master': m6, 'restart_disposition_sha256': r.sha(note)}
        six = {'contract_sha256': 'e'*64, 'checkpoint_scope': {'t0': t0}}
        daily = {'contract_sha256': 'e'*64, 'checkpoint_scope': {'t0': t0, 'previous': previous}}
        proofs = {node6: (n6, six, epoch), master6: (m6, six, epoch),
                  node24: (n24, daily, epoch), master24: (m24, daily, epoch)}
        def context(node):
            return r.encoded({'node_archive_sha256': node['archive_sha256'],
                              'node_capture_sha256': node['capture_sha256'],
                              'node_receipt_sha256': node['receipt_sha256'],
                              'node_outcome_sha256': node['outcome_sha256']})
        data = {master6/'runtime-context.json': context(n6), master24/'runtime-context.json': context(n24),
                node6/'restart-disposition.json': note,
                master6/'outcome.json': r.encoded({'operator_restart_disposition_sha256': r.sha(note)})}
        def accepted(directory, kind, label):
            expected = '+6h' if directory in (node6, master6) else '+24h'
            self.assertEqual(label, expected)
            return proofs[directory]
        with patch.object(r, 'accepted_growth', side_effect=accepted), \
                patch.object(r, 'private', side_effect=lambda path: data[path]):
            result = r.previous_checkpoint(node24, master24, epoch, t0, '+24h')
            self.assertEqual(result, {'node': n24, 'master': m24, 'restart_disposition_sha256': r.sha(note)})
            data[master6/'runtime-context.json'] = context(dict(n6, outcome_sha256='f'*64))
            with self.assertRaisesRegex(ValueError, 'exact accepted late checkpoint pair'):
                r.previous_checkpoint(node24, master24, epoch, t0, '+24h')

    def test_expired_accepted_proof_remains_data_and_never_becomes_executable(self):
        spec = scope()
        raw, files = archive(spec)
        captured = spec['prepared_epoch']+1
        epoch = captured+0.1
        capture = {'capture_complete': True, 'target_mutation': False, 'captured_epoch': captured,
                   'spec_sha256': r.sha(r.encoded(spec)), 'before': {'pid': 'stable'},
                   'after': {'pid': 'stable'}, 'observations': {'statistics_before': {'started_epoch': epoch}}}
        receipt = {'sha256': r.sha(raw), 'epoch': captured-0.5}
        outcome = {'growth_t0_node_accepted': True, 'node_t0_epoch': epoch,
                   'archive_sha256': r.sha(raw), 'capture_sha256': r.sha(r.encoded(capture)),
                   'execution_receipt_sha256': r.sha(r.encoded(receipt))}
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            def write(name, value):
                (directory/name).write_bytes(value)
                (directory/name).chmod(0o600)
            for name, value in files.items():
                write(name, value)
            write('inspection.tar', raw)
            write('stdout.txt', r.encoded(capture))
            write('execution.json', r.encoded(receipt))
            write('outcome.json', r.encoded(outcome))
            write('result.json', r.encoded({'bundle_sha256': r.sha(raw), 'returncode': 0, 'capture_complete': True}))
            with patch.object(r.time, 'time', return_value=spec['expires_epoch']+100):
                self.assertEqual(r.accepted_t0(directory, 'node')[2], epoch)
                with self.assertRaises(ValueError):
                    r.prepare(directory, r.sha(raw))
                with patch.object(r, 'module') as module:
                    with self.assertRaises(ValueError):
                        r.execute(directory, r.sha(raw))
                    module.assert_not_called()
                bad_receipt = dict(receipt, epoch=spec['expires_epoch'])
                write('execution.json', r.encoded(bad_receipt))
                bad_outcome = dict(outcome, execution_receipt_sha256=r.sha(r.encoded(bad_receipt)))
                write('outcome.json', r.encoded(bad_outcome))
                with self.assertRaisesRegex(ValueError, 'accepted growth'):
                    r.accepted_t0(directory, 'node')
                write('execution.json', r.encoded(receipt))
                write('outcome.json', r.encoded(dict(outcome, growth_t0_node_accepted=False)))
                with self.assertRaises(ValueError):
                    r.accepted_t0(directory, 'node')

    def test_historical_mode_still_rejects_corruption_and_scope_expansion(self):
        spec = scope()
        raw, _ = archive(spec)
        with patch.object(r.time, 'time', return_value=spec['expires_epoch']+100):
            with self.assertRaises(ValueError):
                r.unpack(raw+b'changed', r.sha(raw), historical=True)
            bad = dict(spec, unreviewed_path='/etc/shadow')
            raw, _ = archive(bad)
            with self.assertRaises(ValueError):
                r.unpack(raw, r.sha(raw), historical=True)

    def test_real_mount_inventory_uses_direct_collector_pid_path(self):
        o = load(ROOT/'scripts/observe_ntp.py')
        paths = []
        def checked_read(path, limit):
            paths.append(path)
            return o.read(path, limit)
        with patch.object(g, 'observer', types.SimpleNamespace(read=checked_read)):
            result = g.mount_record(Path('/tmp'))
        self.assertEqual(paths, ['/proc/'+str(os.getpid())+'/mountinfo'])
        self.assertTrue(result['mountpoint'].startswith('/'))
        self.assertTrue(result['filesystem_type'])
        with self.assertRaises(ValueError):
            o.read('/proc/self/mountinfo', 1048576)

    def test_real_snapshot_deduplicates_hardlinks_and_retains_allocations(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for stream in g.STREAMS:
                dated = root/(stream+'.20261022')
                dated.write_bytes(b'private statistics content\n')
                os.link(dated, root/stream)
            (root/'unexpected').symlink_to('/not-read')
            result = g.snapshot(root)
            self.assertEqual(result['unique_statistics_inodes'], 4)
            self.assertEqual(result['unique_statistics_bytes'], 4*len(b'private statistics content\n'))
            self.assertEqual(len(result['active']), 4)
            self.assertEqual(result['unexpected_names'], ['unexpected'])
            self.assertEqual(result['findings'], [])
            self.assertIn('allocated_bytes', result['files'][0])
            self.assertNotIn('private statistics content', json.dumps(result))
            (root/'protostats').unlink()
            (root/'protostats').symlink_to(root/'protostats.20261022')
            self.assertIn('missing/indirect active stream: protostats', g.snapshot(root)['findings'])

    def test_indirect_statistics_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'actual').mkdir()
            (root/'link').symlink_to(root/'actual')
            with self.assertRaises(ValueError):
                g.snapshot(root/'link')

    def test_archive_and_payload_bind_the_selected_contract(self):
        spec = scope()
        raw, files = archive(spec)
        self.assertEqual(r.unpack(raw, r.sha(raw))[0], spec)
        compile(r.payload(spec, files), '<sealed-growth-payload>', 'exec')
        for change in ('cadence', 'extra-path', 'extra-probe', 'contract', 'selection'):
            bad = json.loads(json.dumps(spec))
            if change == 'cadence':
                bad['growth_policy']['checkpoint_offsets_seconds'] = [0, 60]
            elif change == 'extra-path':
                bad['files']['/etc/shadow'] = 'c'*64
            elif change == 'extra-probe':
                bad['smtp_probe'] = True
            elif change == 'contract':
                bad['contract_sha256'] = 'd'*64
            else:
                bad['enabled_links']['0'] = ['link', '/foreign']
            raw, _ = archive(bad)
            with self.assertRaises(ValueError):
                r.unpack(raw, r.sha(raw))

    def test_missing_reviewed_node_t0_blocks_master_before_receipt_or_ssh(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            spec = dict(scope(), kind='master')
            with patch.object(r, 'prepare', return_value=(spec, {})), \
                    patch.object(r, 'growth_baselines', return_value=(spec['growth_provenance'], {})), \
                    patch.object(r, 'node_t0_context', side_effect=ValueError('node t0 not accepted')), \
                    patch.object(r, 'module') as module:
                with self.assertRaisesRegex(ValueError, 'not accepted'):
                    r.execute(directory, 'e'*64)
                module.assert_not_called()
            self.assertFalse((directory/'execution.json').exists())


if __name__ == '__main__':
    unittest.main()
