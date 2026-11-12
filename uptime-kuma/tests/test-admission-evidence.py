#!/usr/bin/env python3
"""Run the real receipt and gate tasks locally with supplied resource readings."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]


class AdmissionEvidenceTests(unittest.TestCase):
    def test_boundary_and_failed_readings_are_retained(self):
        tasks = yaml.safe_load((ROOT / 'uptime-kuma/ansible/tasks/preflight-host.yaml').read_text())
        start = next(i for i, task in enumerate(tasks)
                     if task['name'] == 'Retain admission readings before evaluating the resource gate')
        for available, accepted in [('638975', False), ('638976', True), ('638977', True), ('invalid', False)]:
            with self.subTest(available=available), tempfile.TemporaryDirectory(prefix='kuma-admission-') as directory:
                evidence = Path(directory)
                play = [{
                    'hosts': 'localhost', 'connection': 'local', 'gather_facts': False,
                    'vars': {
                        'operation_evidence_directory': directory,
                        'kuma_platform': {'ansible_facts': {
                            'ansible_architecture': 'aarch64', 'ansible_distribution': 'Debian',
                            'ansible_distribution_major_version': '13', 'ansible_memtotal_mb': 920,
                            'ansible_kernel': 'fixture-kernel'}},
                        'memory_controller': {'expected_kernel': 'fixture-kernel'},
                        'kuma_board': {'stdout': 'Raspberry Pi 3 Model B Plus Rev 1.3'},
                        'kuma_available_memory': {'stdout': available},
                        'kuma_available_storage': {'stdout_lines': ['Avail', '5000000000']},
                    },
                    'tasks': tasks[start:],
                }]
                playbook = evidence / 'fixture.yaml'
                playbook.write_text(yaml.safe_dump(play))
                result = subprocess.run([
                    '/bin/bash', str(ROOT.parent / 'homelab-server-configs/tests/repository/run-with-ansible-local-temp.sh'),
                    'ansible-playbook', '-i', 'localhost,', str(playbook),
                ], cwd=ROOT, capture_output=True, text=True, timeout=60)
                self.assertEqual(result.returncode, 0 if accepted else 2, result.stdout + result.stderr)
                receipt = evidence / 'admission-resources.json'
                observed = json.loads(receipt.read_text())
                self.assertEqual(observed['memory_available_kib_raw'], available)
                self.assertEqual(observed['minimum_available_kib'], 638976)
                self.assertEqual(receipt.stat().st_mode & 0o777, 0o600)
                if not accepted:
                    self.assertIn('MemAvailable=' + available + ' KiB', result.stdout)


if __name__ == '__main__':
    unittest.main()
