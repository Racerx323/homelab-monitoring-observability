#!/usr/bin/env python3
"""Deadline decisions fail closed; native lifecycle is qualified separately."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
import yaml
from jinja2 import Environment

spec = importlib.util.spec_from_file_location('startup_permit', Path(__file__).parents[1] / 'scripts/startup-permit.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PendingTests(unittest.TestCase):
    def test_valid_pending_interval(self):
        module.pending(dict(status='pending', armed_at=100, deadline=2500), 200)

    def test_refuse_boundaries_and_clock_rollback(self):
        state = dict(status='pending', armed_at=100, deadline=2500)
        for now in (99, 2500, 2501):
            with self.subTest(now=now), self.assertRaises(ValueError):
                module.pending(state, now)

    def test_commit_needs_two_minute_margin(self):
        with self.assertRaises(ValueError):
            module.pending(dict(status='pending', armed_at=100, deadline=2500), 2380, margin=120)

    def test_terminal_states_cannot_be_reused(self):
        for status in ('accepted', 'contained', 'unknown'):
            with self.subTest(status=status), self.assertRaises(ValueError):
                module.pending(dict(status=status, armed_at=100, deadline=2500), 200)


class AdmissionTests(unittest.TestCase):
    def test_startup_floor_rejects_shortfall_before_file_access(self):
        operation = yaml.safe_load((Path(__file__).parents[1] / 'operations/remaining-deployment.yaml').read_text())
        expected = operation['diagnostic']
        self.assertEqual(expected['minimum_available_kib'], (320 + 192 + 16 + 96) * 1024)
        spec = importlib.util.spec_from_file_location('network_preflight', Path(__file__).parents[1] / 'scripts/diagnose-network.py')
        preflight = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(preflight)
        values = [expected[k] for k in ('hostname', 'architecture', 'boot_id', 'podman_version', 'netavark_version')]
        for available in (638974, 638975):
            with self.subTest(available=available), patch.object(preflight, 'successful', side_effect=values + [str(available)]) as commands:
                with self.assertRaisesRegex(ValueError, 'insufficient reviewed operation headroom'):
                    preflight.preflight(expected)
                self.assertEqual(commands.call_count, 6)


class RoutingTests(unittest.TestCase):
    def test_renewal_mode_routes_both_predecessor_hashes(self):
        tasks = yaml.safe_load((Path(__file__).parents[1] / 'ansible/tasks/arm-remaining-deployment.yaml').read_text())
        task = next(t for t in tasks if t.get('name') == 'Arm one forty-minute continuation without replay')
        expression = task['ansible.builtin.command']['argv'].strip()[2:-2]
        env = Environment()
        env.filters['from_json'] = __import__('json').loads
        receipt = dict(stdout=__import__('json').dumps(dict(contained_predecessor=dict(
            state_sha256='current', previous_state_sha256='original'))))
        for resume, successor, expected in [(False, False, ['arm']),
                                            (True, False, ['resume', 'current']),
                                            (True, True, ['resume-successor', 'current', 'original'])]:
            result = env.compile_expression(expression)(resume_contained=resume, resume_successor=successor,
                                                         kuma_remaining_preflight=receipt)
            self.assertEqual(result[2:], expected)

    def test_contained_completion_skips_reboot_and_interactive_setup(self):
        tasks = yaml.safe_load((Path(__file__).parents[1] / 'ansible/tasks/complete-deployment.yaml').read_text())
        gated = tasks[:7]
        self.assertIn('ansible.builtin.reboot', gated[0])
        self.assertIn('ansible.builtin.wait_for', gated[5])
        for task in gated:
            with self.subTest(task=task.get('name')):
                condition = Environment().compile_expression(task['when'])
                self.assertFalse(condition(resume_contained=True, remaining_deployment=True))
        self.assertTrue(Environment().compile_expression(gated[0]['when'])(resume_contained=False))
        self.assertTrue(Environment().compile_expression(gated[5]['when'])(resume_contained=False, remaining_deployment=True))
        # Administrator-bearing runtime acceptance and backup remain unconditional.
        self.assertNotIn('when', tasks[7])
        self.assertTrue(tasks[7]['vars']['require_administrator'])
        self.assertNotIn('when', tasks[8])


if __name__ == '__main__':
    unittest.main()
