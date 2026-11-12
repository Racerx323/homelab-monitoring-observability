#!/usr/bin/env python3
"""Exercise route preservation policy used by the real pre-start guard."""

import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / "scripts/check-network.py"
spec = importlib.util.spec_from_file_location("network_guard", path)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class NetworkTests(unittest.TestCase):
    def setUp(self):
        self.network = {"driver": "bridge", "ipv6_enabled": True, "network_interface": "podman1",
                        "subnets": [{"subnet": "10.89.0.0/24"}, {"subnet": "fd00:abcd:75::/64"}]}

    def test_defaults_and_owned_bridge_routes_do_not_conflict(self):
        routes = [{"dst": "default"}, {"dst": "::/0"},
                  {"dst": "10.89.0.0/24", "dev": "podman1"}, {"dst": "10.1.0.0/22", "dev": "eth0"}]
        self.assertEqual(guard.conflicts(self.network, routes), [])

    def test_host_route_overlap_rejected_for_both_families(self):
        for prefix in ("10.89.0.0/16", "fd00:abcd:75::1/128"):
            with self.subTest(prefix=prefix):
                self.assertTrue(guard.conflicts(self.network, [{"dst": prefix, "dev": "eth0"}]))

    def test_missing_ipv6_rejected(self):
        self.network["ipv6_enabled"] = False
        with self.assertRaises(ValueError):
            guard.conflicts(self.network, [])


if __name__ == "__main__":
    unittest.main()
