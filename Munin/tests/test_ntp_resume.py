#!/usr/bin/python3
"""Focused one-file correction, permit ownership and conditional recovery tests."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT/'scripts'/name)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


b = load('install_ntp_node.py'); r = load('resume_ntp_node.py')
Resume = r.make_worker(b)


class Local(Resume):
    def __init__(self, spec, root):
        super().__init__(spec, 'resume-digest')
        self.permit = root/'original-permit'; self.enabled = False; self.running = False
        self.bad_health = False; self.calls = []

    def continuity(self): pass

    def preflight(self):
        self.load_artifacts(); self.contained(); self.original_state()
        if b.sha(b.secure(r.TARGET)[0]) != self.resume['before_sha256']:
            raise ValueError('before hash drift')

    def validate_installed(self):
        if r.TARGET.read_bytes() != self.artifacts[r.METRICS]:
            raise ValueError('source readback')

    def ctl(self, *args, allowed=(0,)):
        self.calls.append(args)
        if args[0] == 'show':
            return ('ActiveState='+('active' if self.running else 'inactive')+'\nSubState='+
                    ('running' if self.running else 'dead')+'\nUnitFileState='+('enabled' if self.enabled else 'disabled')+'\n')
        if args[0] in ('enable', 'disable'): self.enabled = args[0] == 'enable'
        if args[0] in ('start', 'stop'): self.running = args[0] == 'start'
        return ''

    def command(self, args, **kwargs):
        self.calls.append(tuple(args))
        if args[0].endswith('/ss'):
            return '10.1.0.51:4949 [fd36:5aa8:6971:1::51]:4949' if self.running else ''
        return ('graph_title Local\nx.value 1\nquery_ok.value 1\nsynced.value 1\npps_selected.value '+
                ('0' if self.bad_health else '1'))


class Tests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup); self.root = Path(temp.name)
        target = self.root/'metrics.py'; target.write_bytes(b'original')
        inputs = self.root/'inputs'; candidate = inputs/r.METRICS; candidate.parent.mkdir(parents=True); candidate.write_bytes(b'corrected')
        old = self.root/'old-state.json'; raw = json.dumps({'spec_sha256': 'old-digest', 'accepted': False, 'recovery': 'contained', 'recovery_errors': []}).encode(); old.write_bytes(raw)
        original = {'operation_id': 'original', 'hostname': 'node', 'listen_addresses': ['10.1.0.51','fd36:5aa8:6971:1::51'],
                    'allow_addresses': ['10.1.3.83'], 'boot_id': 'boot'}
        spec = {'installation': original, 'state_root': str(self.root/'resume'), 'input_root': str(inputs),
                'artifacts': {r.METRICS: b.sha(b'corrected')}, 'before_sha256': b.sha(b'original'),
                'original_state_path': str(old), 'original_state_sha256': b.sha(raw), 'original_spec_sha256': 'old-digest'}
        for obj, name, value in ((r, 'TARGET', target), (b, 'secure', lambda path: (Path(path).read_bytes(), Path(path).stat())),
                                 (b, 'atomic', self.atomic)):
            h = patch.object(obj, name, value); h.start(); self.addCleanup(h.stop)
        self.worker = Local(spec, self.root)

    @staticmethod
    def atomic(path, raw, mode=0o600):
        path = Path(path); temporary = path.with_name(path.name+'.test-new'); temporary.write_bytes(raw)
        temporary.chmod(mode); temporary.replace(path)

    def recover(self):
        read = Path.read_text
        with patch.object(r.os, 'geteuid', return_value=0), patch.object(r.socket, 'gethostname', return_value='node'), \
                patch.object(Path, 'read_text', lambda path, *a, **k: 'boot' if str(path)=='/proc/sys/kernel/random/boot_id' else read(path,*a,**k)):
            return self.worker.recover()

    def test_success_and_conditional_reverse_recovery(self):
        result = self.worker.install(); self.assertTrue(result['accepted'])
        self.assertTrue(self.worker.permit.samefile(self.worker.proof))
        self.assertEqual(r.TARGET.read_bytes(), b'corrected')
        self.assertEqual(self.recover()['recovery'], 'contained')
        self.assertEqual(r.TARGET.read_bytes(), b'original'); self.assertFalse(self.worker.permit.exists())

    def test_health_failure_before_start_restores_only_classifier(self):
        self.worker.bad_health = True
        with self.assertRaisesRegex(ValueError, 'pps_selected'): self.worker.install()
        self.assertFalse(self.worker.permit.exists()); self.assertFalse(self.worker.running)
        self.assertEqual(self.recover()['recovery'], 'contained'); self.assertEqual(r.TARGET.read_bytes(), b'original')

    def test_foreign_classifier_is_preserved_and_held(self):
        self.worker.install(); r.TARGET.write_bytes(b'foreign')
        self.assertEqual(self.recover()['recovery'], 'held'); self.assertEqual(r.TARGET.read_bytes(), b'foreign')
        self.assertFalse(self.worker.running); self.assertFalse(self.worker.enabled)

    def test_foreign_empty_permit_is_never_deleted(self):
        self.worker.install(); self.worker.permit.unlink(); self.worker.permit.touch()
        self.assertEqual(self.recover()['recovery'], 'held'); self.assertTrue(self.worker.permit.exists())

    def test_interruption_after_permit_link_is_recoverable(self):
        original = self.worker.ctl
        def fail(*args, **kwargs):
            if args[0] == 'enable': raise RuntimeError('interrupted')
            return original(*args, **kwargs)
        with patch.object(self.worker, 'ctl', side_effect=fail):
            with self.assertRaises(RuntimeError): self.worker.install()
        self.assertEqual(self.recover()['recovery'], 'contained'); self.assertFalse(self.worker.permit.exists())

    def test_indirect_proof_is_held_without_deleting_permit(self):
        self.worker.install(); self.worker.proof.unlink(); self.worker.proof.symlink_to(self.worker.permit)
        self.assertEqual(self.recover()['recovery'], 'held'); self.assertTrue(self.worker.permit.exists())

    def test_preflight_state_or_classifier_drift_has_no_write(self):
        Path(self.worker.resume['original_state_path']).write_text('{}')
        with self.assertRaises(ValueError): self.worker.install()
        self.assertFalse(self.worker.root.exists()); self.assertEqual(r.TARGET.read_bytes(), b'original')


if __name__ == '__main__': unittest.main()
