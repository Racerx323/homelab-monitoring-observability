"""Offline Apache ACL state-machine and integrity rejection contracts."""
import importlib.util
import io
from pathlib import Path
import tarfile
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
LOADER = importlib.util.spec_from_file_location('acl', ROOT/'scripts/deploy_acl.py')
d = importlib.util.module_from_spec(LOADER)
LOADER.loader.exec_module(d)


class ACLTests(unittest.TestCase):
    def test_proof_needs_exact_six_rows_and_valid_png_tls_leaf(self):
        spec = {'addresses': ['10.1.3.83', 'fd36:5aa8:6971:1::83'],
                'paths': ['/', '/static/a.css', '/graph-day.png'], 'leaf_sha256': 'leaf'}
        state = {'sha256': 'bundle', 'challenge': 'challenge', 'deadline': time.time()+20}
        rows = [{'address': a, 'path': p, 'tls_verified': True, 'response_ok': True,
                 'leaf_sha256': 'leaf', 'png_signature': True,
                 'content_type': 'image/png' if p.endswith('.png') else 'text/css' if p.endswith('.css') else 'text/html'}
                for a in spec['addresses'] for p in spec['paths']]
        proof = {'sha256': 'bundle', 'challenge': 'challenge', 'rows': rows}
        d.valid_proof(spec, state, proof)
        for field, value in [('tls_verified', False), ('leaf_sha256', 'foreign'), ('png_signature', False)]:
            broken = dict(proof, rows=[dict(row) for row in rows])
            broken['rows'][-1][field] = value
            with self.assertRaises(ValueError):
                d.valid_proof(spec, state, broken)
        with self.assertRaises(ValueError):
            d.valid_proof(spec, state, dict(proof, rows=rows+rows[:1]))
        with self.assertRaises(ValueError):
            d.valid_proof(spec, dict(state, deadline=1), proof)

    def test_prewrite_failure_requires_no_restoration_or_reload(self):
        state = {}
        with tempfile.TemporaryDirectory() as temp, patch.object(d, 'identity') as identity:
            d.restore(Path(temp), {}, {}, state)
            self.assertEqual(state['phase'], 'preflight_failed')
            identity.assert_not_called()

    def test_syntax_failure_restores_without_parsing_broken_candidate_first(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            target = directory/'vhost'
            target.write_bytes(b'candidate')
            (directory/'original.conf').write_bytes(b'original')
            spec = {'target': str(target), 'baseline_sha256': d.sha(b'original'), 'candidate_sha256': d.sha(b'candidate')}
            state = {'write_intent': True, 'metadata': {'uid': 0, 'gid': 0, 'mode': 0o644}}
            with patch.object(d, 'identity'), patch.object(d, 'config_files') as configs, patch.object(d, 'target_info', return_value=state['metadata']), patch.object(d, 'replace_target') as replace, patch.object(d, 'command'), patch.object(d, 'reload_apache') as reload:
                d.restore(directory, spec, {}, state)
                self.assertEqual(state['phase'], 'restored')
                self.assertEqual(configs.call_args_list[0].kwargs, {'candidate': True, 'parse': False})
                replace.assert_called_once()
                reload.assert_not_called()

    def test_post_reload_failure_restores_and_gracefully_reloads_original(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            target = directory/'vhost'
            target.write_bytes(b'candidate')
            (directory/'original.conf').write_bytes(b'original')
            spec = {'target': str(target), 'baseline_sha256': d.sha(b'original'), 'candidate_sha256': d.sha(b'candidate')}
            state = {'write_intent': True, 'reload_intent': True, 'metadata': {}}
            with patch.object(d, 'identity'), patch.object(d, 'config_files'), patch.object(d, 'target_info', return_value={}), patch.object(d, 'replace_target'), patch.object(d, 'command'), patch.object(d, 'reload_apache') as reload:
                d.restore(directory, spec, {}, state)
                self.assertEqual(state['phase'], 'restored')
                reload.assert_called_once_with(spec)

    def test_foreign_vhost_drift_holds_without_overwrite_or_reload(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            target = directory/'vhost'
            target.write_bytes(b'foreign')
            state = {'write_intent': True}
            with patch.object(d, 'identity'), patch.object(d, 'replace_target') as replace:
                d.restore(directory, {'target': str(target), 'baseline_sha256': 'old', 'candidate_sha256': 'new'}, {}, state)
                self.assertEqual(state['phase'], 'recovery_held')
                replace.assert_not_called()

    def test_archive_tamper_rejected_before_unpack(self):
        with self.assertRaises(ValueError):
            d.unpack(b'not an archive', 'wrong')

    def archive(self, change=None, extra=False):
        old = b'\n'.join([d.OLD_RULE]*4)
        files = {'deploy_acl.py': (ROOT/'scripts/deploy_acl.py').read_bytes(), 'tls_probe.py': b'',
                 'baseline.conf': old, 'candidate.conf': old.replace(d.OLD_RULE, d.NEW_RULE),
                 'ca.pem': b'', 'known_hosts': b''}
        now = int(time.time())
        spec = {'operation_id': 'svmf-apache-acl-offline', 'prepared_epoch': now, 'expires_epoch': now+86400,
                'confirm_seconds': 90, 'worker_seconds': 150, 'guard_seconds': 180,
                'target': '/etc/apache2/sites-available/001-munin.theama.co-ssl.conf',
                'baseline_sha256': d.sha(old), 'candidate_sha256': d.sha(files['candidate.conf']),
                'addresses': ['10.1.3.83', 'fd36:5aa8:6971:1::83'],
                'members': {n: d.sha(v) for n, v in files.items()}}
        if change:
            change(spec)
        files['spec.json'] = d.encoded(spec)
        if extra:
            files['extra'] = b'bad'
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode='w') as stream:
            for name, raw in files.items():
                entry = tarfile.TarInfo(name)
                entry.size = len(raw)
                stream.addfile(entry, io.BytesIO(raw))
        return buffer.getvalue(), files

    def test_expiry_members_timer_and_scope_rejected(self):
        for change in [lambda s: s.update(prepared_epoch=1, expires_epoch=86401),
                       lambda s: s.update(worker_seconds=200), lambda s: s.update(target='/tmp/other'),
                       lambda s: s['members'].update({'candidate.conf': 'wrong'})]:
            raw, _ = self.archive(change)
            with self.assertRaises(ValueError):
                d.unpack(raw, d.sha(raw))
        raw, _ = self.archive(extra=True)
        with self.assertRaises(ValueError):
            d.unpack(raw, d.sha(raw))

    def test_controller_receipt_consumed_once_before_failed_baseline_no_ssh(self):
        raw, files = self.archive()
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            (directory/'deployment.tar').write_bytes(raw)
            for name in ('tls_probe.py', 'known_hosts'):
                (directory/name).write_bytes(files[name])
            with patch.object(d, 'https_observations', return_value={'passed': False}), patch.object(d, 'transport') as ssh:
                with self.assertRaises(ValueError):
                    d.execute(directory, d.sha(raw))
                with self.assertRaises(FileExistsError):
                    d.execute(directory, d.sha(raw))
                ssh.assert_not_called()


if __name__ == '__main__':
    unittest.main()
