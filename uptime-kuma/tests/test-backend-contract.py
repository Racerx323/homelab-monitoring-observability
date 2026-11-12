#!/usr/bin/env python3
"""Exercise real curl paths and the coordinator's response/recovery decisions."""
import copy
import http.server
import json
from pathlib import Path
import socket
import subprocess
import threading
import unittest

from jinja2 import Environment
import yaml

ROOT = Path(__file__).resolve().parents[1]
TASKS = yaml.safe_load((ROOT / 'ansible/tasks/complete-deployment.yaml').read_text())
PROMOTION = next(t for t in TASKS if 'rescue' in t and 'Promote' in t.get('name', ''))
ASSERTIONS = next(t['ansible.builtin.assert']['that'] for t in PROMOTION['block']
                  if t.get('name') == 'Require actual successful responses and admitted source identities')
ENV = Environment()
ENV.filters['from_json'] = json.loads


def admitted(rows):
    context = dict(item=dict(stdout_lines=[json.dumps(r) for r in rows]),
                   host=dict(ipv4='127.0.0.1', permanent_ula='::1'),
                   proxy=dict(backend_ipv4_sources=['127.0.0.1'], backend_ipv6_sources=['::1']))
    return all(ENV.compile_expression(rule)(**context) for rule in ASSERTIONS)


class V6Server(http.server.HTTPServer):
    address_family = socket.AF_INET6

    def server_bind(self):
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
        super().server_bind()


class BackendTests(unittest.TestCase):
    def probe(self, status):
        requests = []

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                requests.append(self.path)
                self.send_response(status)
                if status == 302:
                    self.send_header('Location', '/must-not-follow')
                self.send_header('Content-Length', '0')
                self.end_headers()

            def log_message(self, *_):
                pass

        with http.server.HTTPServer(('127.0.0.1', 0), Handler) as v4:
            port = v4.server_port
            with V6Server(('::1', port), Handler) as v6:
                workers = [threading.Thread(target=s.serve_forever, daemon=True) for s in (v4, v6)]
                for worker in workers:
                    worker.start()
                try:
                    result = subprocess.run(['bash', str(ROOT / 'scripts/probe-backend.sh'),
                                             '127.0.0.1', '::1', str(port)],
                                            capture_output=True, text=True, timeout=25)
                finally:
                    v4.shutdown()
                    v6.shutdown()
                    for worker in workers:
                        worker.join()
        return result, requests

    def test_both_families_use_fixed_dashboard_and_preserve_addresses(self):
        result, requests = self.probe(200)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(requests, ['/dashboard', '/dashboard'])
        rows = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertTrue(admitted(rows))
        for field, bad in [('status', 302), ('source', '192.0.2.1'), ('backend', '192.0.2.2'),
                           ('family', 'ipv6'), ('path', '/')]:
            changed = copy.deepcopy(rows)
            changed[0][field] = bad
            with self.subTest(field=field):
                self.assertFalse(admitted(changed))
        self.assertFalse(admitted(rows[:1]))
        self.assertFalse(admitted(rows + rows))

    def test_redirect_is_not_followed_or_accepted(self):
        result, requests = self.probe(302)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(requests, ['/dashboard', '/dashboard'])
        self.assertFalse(admitted([json.loads(line) for line in result.stdout.splitlines()]))

    def test_server_error_fails_command(self):
        result, requests = self.probe(500)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(requests, ['/dashboard'])

    def test_continuation_rescue_stops_before_any_recovery_start(self):
        for remaining in (True, False):
            reached_start = False
            stopped = False
            restored = False
            for task in PROMOTION['rescue']:
                if not ENV.compile_expression(task.get('when', 'true'))(remaining_deployment=remaining):
                    continue
                service = task.get('ansible.builtin.systemd_service', {})
                stopped |= service.get('state') == 'stopped'
                restored |= task.get('vars', {}).get('expose_backend') is False
                reached_start |= service.get('state') in ('started', 'restarted')
                if 'ansible.builtin.fail' in task:
                    break
            self.assertTrue(stopped and restored)
            self.assertEqual(reached_start, not remaining)
        coordinator = yaml.safe_load((ROOT / 'ansible/remaining-deployment.yaml').read_text())
        rescue = next(t['rescue'] for play in coordinator for t in play.get('tasks', []) if 'rescue' in t)
        self.assertEqual(rescue[0]['ansible.builtin.command']['argv'][-1], 'contain')
        self.assertEqual(rescue[1]['ansible.builtin.import_tasks'], 'tasks/verify-remaining-containment.yaml')


if __name__ == '__main__':
    unittest.main()
