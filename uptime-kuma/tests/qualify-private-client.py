#!/usr/bin/env python3
"""Exercise the pinned client against private files offline; synthetic credentials only."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import uuid

spec = importlib.util.spec_from_file_location('helper', Path(__file__).resolve().parents[1] / 'scripts/private-proxy-login.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
os.umask(0o077)
root = Path(sys.argv[1])
root.mkdir(mode=0o700)  # Exclusive evidence destination; do not overwrite an earlier run.
source = Path(helper.__file__).with_name('verify-proxy-login.cjs')
results = []


def execute(label, path, args, expected, legacy=False, private_input=None):
    name = 'kuma-offline-' + uuid.uuid4().hex
    command = helper.container_command(path, name, 'none')
    if legacy:
        for option in ['--userns', '--user']:
            index = command.index(option)
            del command[index:index+2]
    command += args
    result = None
    try:
        result = subprocess.run(command, input=private_input, capture_output=True, text=True, timeout=40)
        # No raw runtime stderr is retained, including unexpected Podman diagnostics.
        diagnostic = helper.safe_client_failure(result.stderr) if result.returncode else None
        row = {'case': label, 'exit_status': result.returncode, 'diagnostic': diagnostic}
        results.append(row)
        if expected == 'pass':
            assert result.returncode == 0 and result.stdout.strip() == '{"status":"passed"}', row
        else:
            assert result.returncode != 0, row
            for key, value in expected.items():
                assert diagnostic.get(key) == value, row
    finally:
        probe = subprocess.run(['podman', 'container', 'exists', name], capture_output=True, timeout=15)
        if probe.returncode == 0:
            removed = subprocess.run(['podman', 'rm', '--force', name], capture_output=True, timeout=20)
            assert removed.returncode == 0, 'owned container cleanup failed'
        else:
            assert probe.returncode == 1, 'container cleanup inspection failed'


try:
    with tempfile.TemporaryDirectory(prefix='private-source-', dir=root) as directory:
        folder = Path(directory)
        path = folder/'verify-proxy-login.cjs'
        path.write_bytes(source.read_bytes()); path.chmod(0o600)
        original = (folder.stat().st_mode, path.stat().st_mode, path.stat().st_uid, path.stat().st_gid)
        execute('legacy-owner-private-denial', path, ['-e', helper.PREFLIGHT],
                {'stage': 'source-read', 'code': 'EACCES'}, legacy=True)
        execute('corrected-startup', path, ['-e', helper.PREFLIGHT], 'pass')
        # Actual production entrypoint and dependency run, but network namespace is empty.
        execute('actual-client-offline-failure', path, ['/work/verify-proxy-login.cjs', '--production'],
                {'stage': 'dashboard', 'family': 'ipv4'},
                private_input=json.dumps({'username': 'offline-fixture', 'password': 'offline-fixture-only'}))
        assert original == (folder.stat().st_mode, path.stat().st_mode, path.stat().st_uid, path.stat().st_gid)
        assert path.read_bytes() == source.read_bytes()
        path.write_text('function { invalid syntax')
        execute('syntax-rejected-before-credentials', path, ['-e', helper.PREFLIGHT],
                {'stage': 'source-parse', 'code': 'SYNTAX_ERROR'})
    status = 'passed'
finally:
    (root/'result.json').write_text(json.dumps({'status': locals().get('status', 'failed'),
        'image': helper.IMAGE, 'network': 'none', 'credentials': 'synthetic-only',
        'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in [Path(helper.__file__), source, Path(__file__)]},
        'cases': results}, indent=2)+'\n')
print('PASS: actual pinned container; private source unchanged; four offline cases; cleanup passed')
