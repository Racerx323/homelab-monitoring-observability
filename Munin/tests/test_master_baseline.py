#!/usr/bin/python3
"""Repository import atomicity, secret-scan and drift rejection checks."""
import importlib.util
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

SOURCE=Path(__file__).resolve().parents[1]/'scripts/sync_master_baseline.py'
spec=importlib.util.spec_from_file_location('baseline',SOURCE)
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)


class BaselineTests(unittest.TestCase):
    def test_compare_does_not_scan_or_change_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'munin.conf';path.write_bytes(b'old\r\n')
            with patch.object(b.subprocess,'run',side_effect=AssertionError('scan')):
                self.assertFalse(b.synchronize(b'production\n',path))
            self.assertEqual(path.read_bytes(),b'old\r\n')

    def test_import_scans_exact_bytes_and_preserves_lf_tabs_and_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'munin.conf';path.write_bytes(b'old\r\n');path.chmod(0o644)
            raw=b'# production\n[J1-SVMF]\n\taddress 127.0.0.1\n'
            def scan(argv,**kwargs):
                sample=Path(argv[argv.index('--source')+1])/'munin.conf'
                self.assertEqual(sample.read_bytes(),raw)
                self.assertEqual(sample.stat().st_mode&0o777,0o600)
                return types.SimpleNamespace(returncode=0)
            with patch.object(b.subprocess,'run',side_effect=scan):
                self.assertTrue(b.synchronize(raw,path,write=True))
            self.assertEqual(path.read_bytes(),raw)
            self.assertEqual(path.stat().st_mode&0o777,0o644)

    def test_secret_scan_failure_leaves_repository_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'munin.conf';path.write_bytes(b'old')
            with patch.object(b.subprocess,'run',return_value=types.SimpleNamespace(returncode=1)):
                with self.assertRaises(ValueError):b.synchronize(b'secret',path,write=True)
            self.assertEqual(path.read_bytes(),b'old')

    def test_concurrent_repository_edit_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'munin.conf';path.write_bytes(b'old')
            def scan(*args,**kwargs):
                path.write_bytes(b'operator edit')
                return types.SimpleNamespace(returncode=0)
            with patch.object(b.subprocess,'run',side_effect=scan):
                with self.assertRaises(ValueError):b.synchronize(b'production',path,write=True)
            self.assertEqual(path.read_bytes(),b'operator edit')
            self.assertEqual([p.name for p in path.parent.iterdir()],['munin.conf'])

    def test_symlink_destination_and_wrong_archive_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);root.chmod(0o700);path=root/'munin.conf';other=root/'other'
            other.write_bytes(b'unchanged');path.symlink_to(other)
            with self.assertRaises(ValueError):b.synchronize(b'production',path,write=True)
            archive=root/'inspection.tar';archive.write_bytes(b'changed');archive.chmod(0o600)
            with self.assertRaisesRegex(ValueError,'archive mismatch'):
                b.captured_baseline(root,'0'*64)
            self.assertEqual(other.read_bytes(),b'unchanged')


if __name__=='__main__':unittest.main()
