#!/usr/bin/env python3
"""Exercise the real boot renderer's preservation and rejection boundaries."""

import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

path = Path(__file__).resolve().parents[1] / "scripts/prepare-memory-controller.py"
spec = importlib.util.spec_from_file_location("memory_controller", path)
planner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(planner)


def render(value):
    return planner.render(value, hashlib.sha256(value).hexdigest())


class MemoryControllerTests(unittest.TestCase):
    def test_cli_creates_private_output_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output = root / "original", root / "proposed"
            original = b"root=/dev/mmcblk0p2 rootwait"
            source.write_bytes(original)
            argv = [sys.executable, str(path), str(source), str(output),
                    "--expected-sha256", hashlib.sha256(original).hexdigest()]
            result = subprocess.run(argv, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(output.stat().st_mode & 0o777, 0o600)
            self.assertEqual(hashlib.sha256(output.read_bytes()).hexdigest(), result.stdout.strip())
            snapshot = output.read_bytes()
            self.assertNotEqual(subprocess.run(argv, capture_output=True).returncode, 0)
            self.assertEqual(output.read_bytes(), snapshot)

    def test_exact_append_preserves_root_whitespace_and_line_ending(self):
        for ending in (b"", b"\n", b"\r\n"):
            original = b"console=serial0,115200  root=PARTUUID=12345678-02\trootwait" + ending
            with self.subTest(ending=ending):
                self.assertEqual(render(original), original[:-len(ending)] + b" cgroup_enable=memory" + ending
                                 if ending else original + b" cgroup_enable=memory")

    def test_micro_sd_needs_no_usb_quirk(self):
        self.assertEqual(render(b"root=/dev/mmcblk0p2 rootwait"),
                         b"root=/dev/mmcblk0p2 rootwait cgroup_enable=memory")

    def test_drift_rejected_before_rendering(self):
        with self.assertRaises(ValueError):
            planner.render(b"root=/dev/mmcblk0p2", "0" * 64)

    def test_unsafe_or_conflicting_inputs_rejected(self):
        cases = (b"", b"root=/dev/a\nrootwait", b"root=/dev/a\x00", b"root=/dev/a # comment",
                 b"root=/dev/a root=/dev/b", b"console=tty1", b"root=/dev/a cgroup_disable=cpu,memory",
                 b"root=/dev/a cgroup_memory=1", b"root=/dev/a cgroup_enable=memory",
                 b"root=/dev/a cgroup_enable=cpu,memory", b"root=/dev/a " + b"x" * 16384)
        for value in cases:
            with self.subTest(value=value[:100]), self.assertRaises(ValueError):
                render(value)


if __name__ == "__main__":
    unittest.main()
