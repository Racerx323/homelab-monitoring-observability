#!/usr/bin/env python3
"""Exercise archive extraction boundaries; this does not simulate application acceptance."""

import importlib.util
import io
from pathlib import Path
import tarfile
import tempfile
import unittest

path = Path(__file__).resolve().parents[1] / "scripts/check-restore.py"
spec = importlib.util.spec_from_file_location("restore_checker", path)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class RestoreArchiveTests(unittest.TestCase):
    def test_missing_database_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive, destination = root / "backup.tar", root / "extracted"
            destination.mkdir()
            with tarfile.open(archive, "w") as stream:
                member = tarfile.TarInfo("data")
                member.type = tarfile.DIRTYPE
                stream.addfile(member)
            with self.assertRaisesRegex(ValueError, "database"):
                checker.extract_backup(archive, destination)

    def test_regular_data_bytes_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive, destination = root / "backup.tar", root / "extracted"
            destination.mkdir()
            with tarfile.open(archive, "w") as stream:
                member = tarfile.TarInfo("data/kuma.db")
                member.size = 7
                stream.addfile(member, io.BytesIO(b"payload"))
            data = checker.extract_backup(archive, destination)
            self.assertEqual((data / "kuma.db").read_bytes(), b"payload")

    def test_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive, destination = root / "backup.tar", root / "extracted"
            destination.mkdir()
            with tarfile.open(archive, "w") as stream:
                member = tarfile.TarInfo("../escape")
                member.size = 1
                stream.addfile(member, io.BytesIO(b"x"))
            with self.assertRaises(tarfile.FilterError):
                checker.extract_backup(archive, destination)
            self.assertFalse((root / "escape").exists())

    def test_external_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive, destination = root / "backup.tar", root / "extracted"
            destination.mkdir()
            with tarfile.open(archive, "w") as stream:
                member = tarfile.TarInfo("data/kuma.db")
                member.type, member.linkname = tarfile.SYMTYPE, "/etc/passwd"
                stream.addfile(member)
            with self.assertRaises(tarfile.FilterError):
                checker.extract_backup(archive, destination)

    def test_oversized_member_rejected_before_extraction(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive, destination = root / "backup.tar", root / "extracted"
            destination.mkdir()
            member = tarfile.TarInfo("data/kuma.db")
            member.size = 67108865
            archive.write_bytes(member.tobuf() + b"\x00" * 1024)
            with self.assertRaisesRegex(ValueError, "extraction budget"):
                checker.extract_backup(archive, destination)
            self.assertEqual(list(destination.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
