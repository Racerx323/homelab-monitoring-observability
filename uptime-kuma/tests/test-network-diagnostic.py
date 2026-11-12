import contextlib
import http.server
import importlib.util
import io
import json
from pathlib import Path
import socket
import sqlite3
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
import yaml

spec = importlib.util.spec_from_file_location('diagnostic', Path(__file__).parents[1] / 'scripts/diagnose-network.py')
diagnostic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagnostic)


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Set-Cookie', 'private_session=must-not-escape')
        self.end_headers()
        self.wfile.write(b'password=must-not-escape')

    def log_message(self, *args):
        pass


class DiagnosticTests(unittest.TestCase):
    def test_claimed_database_requires_active_user_and_enabled_authentication(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'kuma.db'
            with sqlite3.connect(path) as conn:
                conn.executescript('CREATE TABLE user(active INTEGER); CREATE TABLE monitor(id INTEGER); '
                                   'CREATE TABLE notification(id INTEGER); CREATE TABLE setting(key TEXT,value TEXT);')
            with self.assertRaisesRegex(ValueError, 'administrator'):
                diagnostic.database(path, administrator=True)
            with sqlite3.connect(path) as conn:
                conn.execute('INSERT INTO user VALUES(1)')
            before = path.read_bytes()
            self.assertEqual(diagnostic.database(path, administrator=True)['counts']['user'], 1)
            self.assertEqual(before, path.read_bytes())
            with sqlite3.connect(path) as conn:
                conn.execute("INSERT INTO setting VALUES('disableAuth','true')")
            with self.assertRaisesRegex(ValueError, 'administrator'):
                diagnostic.database(path, administrator=True)
            with sqlite3.connect(path) as conn:
                conn.execute('DELETE FROM setting')
                conn.execute('UPDATE user SET active=0')
            with self.assertRaisesRegex(ValueError, 'administrator'):
                diagnostic.database(path, administrator=True)
            with sqlite3.connect(path) as conn:
                conn.execute('UPDATE user SET active=1')
                conn.execute('INSERT INTO monitor VALUES(1)')
            with self.assertRaisesRegex(ValueError, 'administrator'):
                diagnostic.database(path, administrator=True)

    def test_native_play_registers_cannot_replace_policy_variables(self):
        plays = yaml.safe_load((Path(__file__).parents[1] / 'ansible/diagnose-network.yaml').read_text())
        def registrations(value):
            if isinstance(value, dict):
                if 'register' in value:
                    yield value['register']
                for child in value.values():
                    yield from registrations(child)
            elif isinstance(value, list):
                for child in value:
                    yield from registrations(child)
        for play in plays:
            self.assertFalse(set(play.get('vars', {})) & set(registrations(play)))

    def test_each_family_records_status_without_body_or_cookie(self):
        class IPv6Server(http.server.ThreadingHTTPServer):
            address_family = socket.AF_INET6
        for host, server_type in [('127.0.0.1', http.server.ThreadingHTTPServer), ('::1', IPv6Server)]:
            with server_type((host, 0), Handler) as server:
                worker = threading.Thread(target=server.serve_forever)
                worker.start()
                try:
                    row = diagnostic.http_probe(host, server.server_port)
                    self.assertEqual(row['status'], 200)
                    self.assertNotIn('private_session', json.dumps(row))
                    self.assertNotIn('must-not-escape', json.dumps(row))
                finally:
                    server.shutdown()
                    worker.join()

    def test_timeout_remains_measurement(self):
        with socket.socket() as listener:
            listener.bind(('127.0.0.1', 0))
            listener.listen()
            row = diagnostic.http_probe('127.0.0.1', listener.getsockname()[1], timeout=0.05)
            self.assertEqual(row['error_type'], 'TimeoutError')
            self.assertLess(row['elapsed_seconds'], 1)

    def test_command_bounds_output_and_time(self):
        result = diagnostic.command([sys.executable, '-c', 'print("x"*100000)'], limit=512)
        self.assertEqual(result['error'], 'output_limit')
        started = time.monotonic()
        result = diagnostic.command([sys.executable, '-c', 'import time;time.sleep(30)'], timeout=0.1)
        self.assertEqual(result['error'], 'command_timeout')
        self.assertLess(time.monotonic() - started, 2)

    def test_startup_events_never_retain_unknown_or_injected_text(self):
        raw = 'Listening on: password=secret\nStored JWT secret into database\nNo user, need setup\nENOENT /private/path\n'
        result = diagnostic.log_events(raw)
        encoded = json.dumps(result)
        for text in ['password', 'secret', '/private/path', 'JWT']:
            self.assertNotIn(text, encoded)
        self.assertEqual(result['unclassified_lines_omitted'], 1)
        self.assertIn({'event': 'startup_error', 'code': 'ENOENT'}, result['events'])

    def test_failed_family_does_not_discard_other_paths_or_checkpoint(self):
        def probe(address):
            return {'status': 200} if ':' not in address else {'error_type': 'TimeoutError'}
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'observation.json'
            with patch.object(diagnostic, 'container', return_value={'addresses': {'ipv4': '10.1.1.2', 'ipv6': 'fd00::2'}}), \
                    patch.object(diagnostic, 'snapshot', return_value={'ports': {'rc': 0, 'stdout': ''}}), \
                    patch.object(diagnostic, 'command', return_value={'rc': 0, 'stdout': '{"status":200}', 'error': None}), \
                    patch.object(diagnostic, 'http_probe', side_effect=probe), \
                    patch.object(diagnostic.time, 'sleep'), contextlib.redirect_stdout(io.StringIO()):
                diagnostic.observe(target)
            result = json.loads(target.read_text())
            self.assertTrue(result['completed'])
            self.assertEqual(len(result['requests']), 12)
            self.assertEqual(len([r for r in result['requests'] if r.get('error_type') == 'TimeoutError']), 4)
            self.assertEqual(target.stat().st_mode & 0o777, 0o600)
            self.assertEqual(list(Path(directory).glob('.observation-*')), [])
        diagnostic.DEADLINE = float('inf')

    def test_checkpoint_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'observation.json'
            original = Path(directory) / 'original'
            original.write_text('unchanged')
            target.symlink_to(original)
            with self.assertRaisesRegex(ValueError, 'symlink'):
                diagnostic.save_receipt(target, {})
            self.assertEqual(original.read_text(), 'unchanged')


if __name__ == '__main__':
    unittest.main()
