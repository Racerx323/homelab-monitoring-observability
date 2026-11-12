#!/usr/bin/env python3
"""Operator-only login check; prompt locally and retain only sanitized results."""
import getpass
import hashlib
import json
import os
from pathlib import Path
import subprocess
import stat
import sys
import time
import uuid

IMAGE = '1bf189bcd6286c24facc94dcd12565b09e1cf0bdd523d3dc8852f6646be49c29'


FAILURE_STAGES = {
    'bootstrap', 'dashboard', 'websocket-connect', 'transport', 'unauthenticated-denial',
    'wrong-password-denial', 'wrong-password-message', 'correct-login',
    'authenticated-list', 'second-connect', 'second-login', 'second-list',
    'logout', 'logout-denial', 'idle-wait', 'idle-dashboard', 'idle-list',
    'idle-logout', 'idle-logout-denial', 'setup',
    'source-read', 'source-parse', 'dependency-import',
}
FAILURE_CODES = {
    'ECONNREFUSED', 'ECONNRESET', 'ETIMEDOUT', 'ENETUNREACH', 'EHOSTUNREACH',
    'CERT_HAS_EXPIRED', 'DEPTH_ZERO_SELF_SIGNED_CERT',
    'UNABLE_TO_VERIFY_LEAF_SIGNATURE', 'ERR_TLS_CERT_ALTNAME_INVALID',
    'ERR_ASSERTION', 'CLIENT_DEADLINE', 'UNCLASSIFIED',
    'EACCES', 'ENOENT', 'MODULE_NOT_FOUND', 'SYNTAX_ERROR',
    'READINESS_TIMEOUT', 'SOCKET_DISCONNECTED', 'UNEXPECTED_READINESS', 'ACK_TIMEOUT', 'ACK_ERROR',
}


def safe_client_failure(stderr):
    """Accept only the exact enum-only client protocol; never retain raw output."""
    if len(stderr) > 1024:
        return {'report': 'oversized'}
    try:
        value = json.loads(stderr)
        if (type(value) is dict and set(value) == {'stage', 'family', 'code'}
                and type(value['stage']) is str and value['stage'] in FAILURE_STAGES
                and type(value['family']) is str and value['family'] in {'none', 'ipv4', 'ipv6'}
                and type(value['code']) is str and value['code'] in FAILURE_CODES):
            return value
    except (ValueError, TypeError):
        pass
    return {'report': 'unavailable'}


# Runs without network or credential stdin, before prompting. Node loads this
# bootstrap directly so unreadable source/module errors can still be classified.
PREFLIGHT = r"""
const fs = require('node:fs');
let stage = 'source-read';
try {
    const source = fs.readFileSync('/work/verify-proxy-login.cjs', 'utf8');
    stage = 'source-parse';
    new (require('node:vm').Script)(source);
    stage = 'dependency-import';
    require('/app/node_modules/socket.io-client');
    console.log(JSON.stringify({status: 'passed'}));
} catch (error) {
    const code = ['EACCES', 'ENOENT', 'MODULE_NOT_FOUND'].includes(error.code)
        ? error.code : (stage === 'source-parse' ? 'SYNTAX_ERROR' : 'UNCLASSIFIED');
    console.error(JSON.stringify({stage, family: 'none', code}));
    process.exitCode = 1;
}
"""


def container_command(client, name, network):
    # Keep the invoking user's numeric identity mapped to its host identity.
    # Owner-only sources stay private; no chmod, chown or writable bind mount.
    return ['podman', 'run', '--rm', '--pull', 'never', '--network', network,
            '--userns', 'keep-id', '--user', f'{os.getuid()}:{os.getgid()}',
            '--name', name, '--read-only', '--cap-drop', 'ALL',
            '--security-opt', 'no-new-privileges', '-i',
            '-v', str(client.parent) + ':/work:ro', '--entrypoint', 'node', IMAGE]


def startup_check(client, name):
    return subprocess.run(container_command(client, name, 'none') + ['-e', PREFLIGHT],
                          stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30)


def read_window(receipt, operation, client_hash, margin=0):
    """Reject closed, expired or orphaned windows, including PID reuse."""
    path = receipt.parent / 'operator-window.json'
    info = path.lstat()
    if path.is_symlink() or not path.is_file() or info.st_uid != os.getuid() or info.st_mode & 0o077 or info.st_size > 4096:
        raise ValueError('invalid window')
    window = json.loads(path.read_text())
    if (window.get('operation') != operation or window.get('status') != 'open'
            or window.get('client_sha256') != client_hash
            or window.get('deadline', 0) < time.time() + margin):
        raise ValueError('expired or mismatched window')
    pid = window['controller_pid']
    if type(pid) is not int or pid <= 1:
        raise ValueError('invalid controller')
    fields = Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()
    if fields[0] == 'Z' or fields[19] != window['controller_start']:
        raise ValueError('controller no longer active')
    return window


def expected_rows():
    return [dict(family=family, tls='verified-system-trust', transport='websocket',
                 dashboard=200, rejection='authIncorrectCreds', immediateRetry=True,
                 secondClient=True, idleSeconds=65, logoutDenial=True)
            for family in ['ipv4', 'ipv6']]


def verify_receipt(receipt, standalone_operation=None):
    info = receipt.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o600 or info.st_size > 8192:
        raise ValueError('invalid receipt file')
    record = json.loads(receipt.read_text())
    if standalone_operation is not None:
        expected_fields = {'operation', 'mode', 'status', 'started_at', 'finished_at', 'client_sha256', 'rows'}
        client_hash = hashlib.sha256(Path(__file__).with_name('verify-proxy-login.cjs').read_bytes()).hexdigest()
        if (set(record) != expected_fields or record['mode'] != 'standalone'
                or record['operation'] != standalone_operation or record['client_sha256'] != client_hash
                or record['status'] != 'passed' or record['rows'] != expected_rows()
                or not 0 < record['started_at'] <= record['finished_at'] <= time.time()
                or not 65 <= record['finished_at'] - record['started_at'] <= 180):
            raise ValueError('standalone receipt does not satisfy acceptance')
        return
    window = json.loads((receipt.parent / 'operator-window.json').read_text())
    if set(record) != {'operation', 'status', 'started_at', 'finished_at', 'client_sha256', 'rows'}:
        raise ValueError('unexpected receipt fields')
    read_window(receipt, record['operation'], record['client_sha256'])
    if (record['operation'] != window['operation'] or record['client_sha256'] != window['client_sha256']
            or record['status'] != 'passed' or record['rows'] != expected_rows()
            or not window['deadline'] - 600 <= record['started_at'] <= record['finished_at'] <= window['deadline']):
        raise ValueError('receipt does not satisfy acceptance')


def main():
    args = sys.argv[1:]
    standalone = args[:1] == ['--standalone']
    if standalone:
        args = args[1:]
    if len(args) != 2 or not sys.stdin.isatty():
        raise SystemExit('Run in your private terminal: private-proxy-login.py [--standalone] OPERATION RECEIPT')
    operation, destination = args
    if not operation or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in operation):
        raise SystemExit('Invalid operation identity')
    receipt = Path(destination)
    if not receipt.is_absolute() or receipt.parent.is_symlink() or not receipt.parent.is_dir():
        raise SystemExit('Receipt requires an existing private absolute parent directory')
    metadata = receipt.parent.stat()
    if metadata.st_uid != os.getuid() or metadata.st_mode & 0o077:
        raise SystemExit('Receipt parent must be owned by you and mode 0700')
    os.umask(0o077)
    # Reserve before prompts/contact. Failure leaves a consumed failed receipt.
    if receipt.exists() or receipt.is_symlink():
        raise SystemExit('Receipt already exists; no replay')
    pending = receipt.with_name(receipt.name + '.pending')
    with pending.open('x') as output:
        record = {'operation': operation, 'status': 'failed', 'started_at': time.time()}
        name = 'kuma-private-login-' + uuid.uuid4().hex
        client = Path(__file__).with_name('verify-proxy-login.cjs')
        record['client_sha256'] = hashlib.sha256(client.read_bytes()).hexdigest()
        stage = 'input'
        process = None
        stderr = ''
        cleanup_status = 'passed'
        try:
            stage = 'startup-check'
            preflight = startup_check(client, name)
            if preflight.returncode or preflight.stdout.strip() != '{"status":"passed"}':
                record['client_exit_status'] = preflight.returncode
                record['client_failure'] = safe_client_failure(preflight.stderr)
                raise ValueError('startup check failed')
            stage = 'input'
            username = input('Kuma username: ')
            password = getpass.getpass('Kuma password (never retained): ')
            if not username or not password or len(username) > 256 or len(password) > 4096:
                raise ValueError('invalid input')
            stage = 'window'
            if standalone:
                # Human input has no deadline; only the subsequent client run is bounded.
                record.update(mode='standalone', started_at=time.time())
            else:
                read_window(receipt, operation, record['client_sha256'], margin=180)
            command = container_command(client, name, 'host') + ['/work/verify-proxy-login.cjs', '--production']
            stage = 'client-start'
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, text=True)
            stage = 'client-wait'
            deadline = time.monotonic() + 180
            private_input = json.dumps({'username': username, 'password': password})
            del password
            try:
                while True:
                    if not standalone:
                        read_window(receipt, operation, record['client_sha256'])
                    if time.monotonic() >= deadline:
                        stage = 'client-deadline'
                        raise ValueError('client deadline')
                    try:
                        stdout, stderr = process.communicate(input=private_input, timeout=1)
                        break
                    except subprocess.TimeoutExpired:
                        private_input = None
                if not standalone:
                    read_window(receipt, operation, record['client_sha256'])
            finally:
                private_input = None
                if process.poll() is None:
                    process.kill()
                process.communicate(timeout=10)
            stage = 'client-result'
            if process.returncode:
                raise ValueError('client failed')
            if len(stdout) > 8192:
                stage = 'client-output-limit'
                raise ValueError('client output exceeds limit')
            stage = 'client-receipt'
            rows = [json.loads(line) for line in stdout.splitlines()]
            if rows != expected_rows():
                raise ValueError('unexpected receipt')
            record.update(status='passed', rows=rows, finished_at=time.time())
        except (Exception, KeyboardInterrupt):
            # No provider stderr, exception values, input or tokens enter evidence.
            record['status'] = 'failed'
            record['failure_stage'] = stage
            if process is not None:
                record['client_exit_status'] = process.returncode
                record['client_failure'] = safe_client_failure(stderr)
        finally:
            # The fixed, unique name belongs to this invocation only.
            try:
                exists = subprocess.run(['podman', 'container', 'exists', name], capture_output=True, timeout=15)
                if exists.returncode == 0:
                    removed = subprocess.run(['podman', 'rm', '--force', name], capture_output=True, timeout=20)
                    if removed.returncode:
                        cleanup_status = 'remove-failed'
                elif exists.returncode != 1:
                    cleanup_status = 'inspection-failed'
            except Exception:
                cleanup_status = 'exception'
            if cleanup_status != 'passed':
                record['status'] = 'failed'
                record.setdefault('failure_stage', 'cleanup')
            if record['status'] == 'failed':
                record['cleanup_status'] = cleanup_status
                if process is not None:
                    record.setdefault('client_exit_status', process.returncode)
                record['finished_at'] = time.time()
            output.write(json.dumps(record, indent=2) + '\n')
    os.replace(pending, receipt)
    print('Private login checks: ' + record['status'])
    if record['status'] == 'failed':
        print(json.dumps({key: record[key] for key in
                          ('failure_stage', 'client_exit_status', 'client_failure', 'cleanup_status')
                          if key in record}, sort_keys=True))
    raise SystemExit(0 if record['status'] == 'passed' else 1)


if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == '--verify-standalone-receipt':
        try:
            verify_receipt(Path(sys.argv[3]), standalone_operation=sys.argv[2])
        except Exception:
            raise SystemExit('Private receipt rejected')
    elif len(sys.argv) == 3 and sys.argv[1] == '--verify-receipt':
        try:
            verify_receipt(Path(sys.argv[2]))
        except Exception:
            raise SystemExit('Private receipt rejected')
    else:
        main()
