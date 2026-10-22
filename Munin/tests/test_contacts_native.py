#!/usr/bin/python3
"""Real systemd recovery, installed parser/gate and loopback SMTP; container only."""
import importlib.util
import json
import os
from pathlib import Path
import signal
import socket
import socketserver
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


class SMTP(socketserver.StreamRequestHandler):
    def handle(self):
        self.wfile.write(b'220 isolated qualification\r\n')
        while True:
            line = self.rfile.readline(16385)
            if not line:
                return
            command = line.split(None, 1)[0].upper()
            if command in (b'EHLO', b'HELO', b'MAIL', b'RCPT', b'RSET', b'NOOP'):
                self.wfile.write(b'250 OK\r\n')
            elif command == b'DATA':
                self.wfile.write(b'354 data\r\n')
                rows = []
                while True:
                    row = self.rfile.readline(16385)
                    if not row or row == b'.\r\n':
                        break
                    rows.append(row[1:] if row.startswith(b'..') else row)
                self.server.messages.append(b''.join(rows))
                if self.server.ambiguous:
                    return  # DATA arrived, but its acknowledgement is lost.
                self.wfile.write(b'250 accepted\r\n')
            elif command == b'QUIT':
                self.wfile.write(b'221 bye\r\n')
                return
            else:
                self.wfile.write(b'500 unsupported\r\n')


def main():
    os.umask(0o077)
    if (not Path('/run/.containerenv').exists() or os.geteuid() != 0
            or Path('/proc/1/comm').read_text().strip() != 'systemd'):
        raise ValueError('isolated native systemd container required')
    case = sys.argv[1]
    tests = load(ROOT/'tests/test_contacts.py')
    d, c = tests.d, tests.c
    base = load(ROOT/'scripts/install_ntp_node.py')
    stopped = subprocess.run(['/usr/bin/systemctl', 'stop', 'cron.service'], capture_output=True)
    assert stopped.returncode in (0, 5), stopped.stderr
    before = tests.inactive_baseline()
    base.atomic(c.CONFIG, before, 0o644)
    c.PROOF.parent.mkdir(parents=True, mode=0o700)
    os.link(c.CONFIG, c.PROOF)
    pm = c.PROOF.stat()
    proof = {'device': pm.st_dev, 'inode': pm.st_ino, 'size': pm.st_size,
             'mtime': pm.st_mtime, 'sha256': d.sha(before)}
    Path('/etc/munin/munin-conf.d').mkdir(exist_ok=True)
    for path in Path('/etc/munin/munin-conf.d').iterdir():
        path.unlink()  # Reset only this disposable image's packaged include files.
    native_paths = sorted(d.NATIVE_MODULES)
    protected = {p: d.sha(Path(p).read_bytes()) for p in native_paths}
    if case == 'success':
        limits = subprocess.run(['/usr/bin/python3', '-I', '-B', str(ROOT/'tests/test_limits_native.py')],
                                input=json.dumps(protected).encode(), capture_output=True, timeout=60)
        Path('/evidence/native-limits.stdout').write_bytes(limits.stdout)
        Path('/evidence/native-limits.stderr').write_bytes(limits.stderr)
        assert limits.returncode == 0, limits.stderr
    identity = subprocess.check_output(['/usr/bin/systemctl', 'show', 'systemd-journald.service',
        '--property=ActiveState,SubState,MainPID,InvocationID,NRestarts'], text=True)
    units = {'systemd-journald.service': dict(x.split('=', 1) for x in identity.splitlines())}
    fault = {'rejection': 'failure', 'worker-loss': 'worker-loss', 'commit-loss': 'commit-loss',
             'publication-loss': 'publication-loss'}.get(case)
    bundle = Path('/evidence/activation')
    s, files, digest = tests.fixture(bundle, units=units, protected=protected, fault=fault, proof=proof)
    raw = (bundle/'deployment.tar').read_bytes()
    if case == 'preflight-drift':
        c.CONFIG.unlink()
        base.atomic(c.CONFIG, before+b'\n# foreign baseline\n', 0o644)
    elif case == 'proof-preflight-drift':
        c.PROOF.unlink()
        base.atomic(c.PROOF, before, 0o644)
    elif case == 'unexpected-main-link':
        os.link(c.CONFIG, c.PROOF.with_name('extra-link'))
    if case == 'controller-loss':
        submitted = d.payload(files, raw, digest, 'apply', s, {}) + b'\nimport time; time.sleep(120)\n'
        with Path('/evidence/lost-controller.log').open('xb') as log:
            child = subprocess.Popen(['/usr/bin/python3', '-I', '-B', '-'], stdin=subprocess.PIPE, stdout=log, stderr=log)
            child.stdin.write(submitted)
            child.stdin.close()
            deadline = time.monotonic()+20
            state = c.STATE/s['operation_id']/'state.json'
            while not state.exists() or json.loads(state.read_text())['phase'] != 'prepared':
                assert time.monotonic() < deadline, 'controller never reached prepared'
                time.sleep(.1)
            child.kill()
            assert child.wait() == -signal.SIGKILL
        time.sleep(5)
        result = d.locked_worker(d.STAGES/s['operation_id'], digest, 'inspect')
        assert result['phase'] == 'restored' and c.CONFIG.read_bytes() == before, result
    else:
        result = d.root_launch(raw, digest)
        if case in ('worker-loss', 'rejection', 'publication-loss'):
            assert result['phase'] == 'restored' and c.CONFIG.read_bytes() == before, result
        elif case == 'preflight-drift':
            assert result['phase'] == 'preflight-failed' and c.CONFIG.read_bytes() == before+b'\n# foreign baseline\n', result
        elif case in ('proof-preflight-drift', 'unexpected-main-link'):
            assert result['phase'] == 'preflight-failed' and c.CONFIG.read_bytes() == before, result
            assert not c.CONTROL.exists() and not c.HELPER.exists(), result
        else:
            assert result['phase'] == 'prepared', result
            # Real installed gate process cannot submit or manufacture success before commit.
            assert not (c.CONTROL/'enabled.json').exists() and not (c.STATUS/'status.json').exists()
            stage = d.STAGES/s['operation_id']
            if case == 'suppressed-call':
                gated = subprocess.run(['/usr/sbin/runuser', '-u', 'munin', '--', '/usr/bin/python3', '-I', '-B', str(c.GATE)],
                                       input=b'CRITICAL|j2-svntp1|ntp_health||selected_offset_ok|', capture_output=True)
                assert gated.returncode == 75 and (c.STATUS/'suppressed.json').exists() and not (c.STATUS/'status.json').exists()
                try:
                    d.locked_worker(stage, digest, 'commit')
                except ValueError as error:
                    assert 'suppressed' in str(error)
                else:
                    raise AssertionError('suppressed transition incorrectly committed')
                result = d.locked_worker(stage, digest, 'recover')
                assert result['phase'] == 'restored' and (c.STATUS/'suppressed.json').exists()
            elif case == 'proof-foreign-recovery':
                extra = c.PROOF.with_name('foreign-proof-link')
                os.link(c.PROOF, extra)
                snapshot = c.CONFIG.read_bytes()
                result = d.locked_worker(stage, digest, 'recover')
                assert result['phase'] == 'recovery-held' and c.CONFIG.read_bytes() == snapshot, result
                assert extra.exists() and c.PROOF.stat().st_nlink == 2 and not (c.CONTROL/'enabled.json').exists()
            elif case.startswith('foreign-'):
                if case == 'foreign-config':
                    base.atomic(c.CONFIG, c.CONFIG.read_bytes()+b'\n# foreign config\n', 0o644)
                elif case == 'foreign-helper':
                    base.atomic(c.HELPER, c.HELPER.read_bytes()+b'\n# foreign helper\n', 0o755)
                elif case == 'foreign-state':
                    original = c.STATUS.with_name('ntp-alerts-original')
                    c.STATUS.rename(original)
                    c.STATUS.mkdir(mode=0o700)
                    (c.STATUS/'foreign.json').write_text('preserve me')
                snapshot = c.CONFIG.read_bytes() if case == 'foreign-config' else c.HELPER.read_bytes() if case == 'foreign-helper' else (c.STATUS/'foreign.json').read_bytes()
                result = d.locked_worker(stage, digest, 'recover')
                assert result['phase'] == 'recovery-held', result
                observed = c.CONFIG.read_bytes() if case == 'foreign-config' else c.HELPER.read_bytes() if case == 'foreign-helper' else (c.STATUS/'foreign.json').read_bytes()
                assert snapshot == observed and not (c.CONTROL/'enabled.json').exists()
            elif case == 'restore':
                result = d.locked_worker(stage, digest, 'recover')
                assert result['phase'] == 'restored' and c.CONFIG.read_bytes() == before
                identity = c.CONFIG.stat().st_ino
                again = d.locked_worker(stage, digest, 'recover')
                assert again['phase'] == 'restored' and c.CONFIG.stat().st_ino == identity
            elif case == 'commit-loss':
                row = subprocess.run(['/usr/bin/python3', '-I', '-B', '-'], input=d.payload(files, raw, digest, 'commit', s, {}), capture_output=True)
                assert row.returncode == -signal.SIGKILL
                time.sleep(5)
                result = d.locked_worker(stage, digest, 'inspect')
                assert result['phase'] == 'committed' and result['enable_pending'] and not result['contacts_enabled'], result
            else:
                result = d.locked_worker(stage, digest, 'commit')
                assert result['phase'] == 'committed' and result['accepted'], result
                prerequisite = {'operation_id': s['operation_id'], 'archive_sha256': digest,
                    'config_sha256': d.sha(files['candidate.conf']), 'worker_sha256': d.sha(d.encoded(s['worker']))}
                _, send_files, send_digest = tests.fixture(Path('/evidence/problem'), kind='problem', units=units,
                                                          protected=protected, prerequisite=prerequisite)
                send_raw = Path('/evidence/problem/deployment.tar').read_bytes()
                send_spec, send_files = d.unpack(send_raw, send_digest)
                server = socketserver.TCPServer(('127.0.0.1', 8025), SMTP)
                server.messages = []
                server.ambiguous = case == 'ambiguous-send'
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                command = d.payload(send_files, send_raw, send_digest, 'send', send_spec, {})
                try:
                    sent = subprocess.run(['/usr/bin/python3', '-I', '-B', '-'], input=command, capture_output=True, timeout=30)
                    assert sent.returncode == 0, sent.stderr
                    submitted = json.loads(sent.stdout)
                    assert submitted['attempted'] and submitted['status_recorded'] and not submitted['delivery_accepted']
                    assert submitted['submission_accepted'] is (case != 'ambiguous-send'), submitted
                    assert server.messages == [send_files['message.eml']], 'wire bytes changed'
                    replay = subprocess.run(['/usr/bin/python3', '-I', '-B', '-'], input=command, capture_output=True, timeout=30)
                    assert replay.returncode != 0 and len(server.messages) == 1, 'one-use receipt failed'
                    status = json.loads((c.STATUS/'status.json').read_text())
                    assert status['submission_ok'] is (case != 'ambiguous-send')
                    if case == 'success':
                        scheduled = subprocess.run(['/usr/sbin/runuser', '-u', 'munin', '--', '/usr/bin/python3', '-I', '-B', str(c.GATE)],
                            input=b'OK|j2-svntp1|ntp_health|||', capture_output=True, timeout=30)
                        assert scheduled.returncode == 0 and len(server.messages) == 2, scheduled.stderr
                finally:
                    server.shutdown()
                    server.server_close()
    assert c.PROOF.read_bytes() == before, 'historical proof content changed'
    if case != 'proof-preflight-drift':
        retained = c.PROOF.stat()
        assert (retained.st_dev, retained.st_ino, retained.st_mtime) == (pm.st_dev, pm.st_ino, pm.st_mtime)
    if result['phase'] in ('restored', 'committed'):
        same = c.PROOF.stat().st_ino == c.CONFIG.stat().st_ino
        assert same is (case == 'publication-loss'), 'only pre-replacement loss retains original main inode'
        assert c.PROOF.stat().st_nlink == c.CONFIG.stat().st_nlink == (2 if same else 1)
    final = {'case': case, 'passed': True, 'result': result, 'native_module_hashes': protected,
             'production_target_contacted': False, 'external_delivery_attempted': False}
    Path('/evidence/result.json').write_text(json.dumps(final, indent=2)+'\n')
    print(json.dumps({'case': case, 'passed': True}), flush=True)


if __name__ == '__main__':
    main()
