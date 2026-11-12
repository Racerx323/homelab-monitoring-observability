#!/usr/bin/env python3
"""Run real Caddy/Kuma with synthetic TLS and credentials in an offline namespace."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
KUMA = '1bf189bcd6286c24facc94dcd12565b09e1cf0bdd523d3dc8852f6646be49c29'
CADDY = '1bab90ae19f4d9091b9529336ef023ecce44f96cf2bad6016ce95dbc04c64156'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--registration-delay-ms", type=int, choices=[0, 100], default=0)
    args = parser.parse_args()
    os.umask(0o077)
    evidence = Path(tempfile.mkdtemp(prefix='proxy-auth-',
                                   dir='/home/aaron/code/.local-evidence/uptime-kuma'))
    fixture = evidence / 'fixture'
    fixture.mkdir(mode=0o700)
    names = [evidence.name + '-kuma', evidence.name + '-caddy']
    result = {'scope': 'Local AMD64 only; no production data, hosts or DNS',
              'images': {'kuma': KUMA, 'caddy': CADDY}, 'verdict': 'failed',
              'registration_delay_ms': args.registration_delay_ms,
              'client_sha256': hashlib.sha256((ROOT / 'scripts/verify-proxy-login.cjs').read_bytes()).hexdigest()}
    sequence = 0

    def run(argv, timeout=30, check=True):
        nonlocal sequence
        sequence += 1
        with (evidence / f'{sequence:02d}.stdout').open('w') as out, \
                (evidence / f'{sequence:02d}.stderr').open('w') as err:
            completed = subprocess.run(argv, stdout=out, stderr=err, timeout=timeout)
        (evidence / f'{sequence:02d}.status').write_text(str(completed.returncode) + '\n')
        if check and completed.returncode:
            raise RuntimeError(f'command {sequence} failed: {completed.returncode}')
        return completed.returncode

    try:
        run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-days', '1',
             '-subj', '/CN=uptime.local.theama.co', '-addext', 'subjectAltName=DNS:uptime.local.theama.co',
             '-keyout', str(fixture / 'key.pem'), '-out', str(fixture / 'cert.pem')])
        (fixture / 'cert.pem').chmod(0o644)
        shutil.copyfile(ROOT / 'scripts/verify-proxy-login.cjs', fixture / 'client.cjs')
        (fixture / 'client.cjs').chmod(0o600)
        server_mount = []
        if args.registration_delay_ms:
            run(['podman', 'run', '--rm', '--pull', 'never', '--network', 'none',
                 '--read-only', '--entrypoint', 'node', KUMA, '-e',
                 'process.stdout.write(require("fs").readFileSync("/app/server/server.js"))'])
            original = (evidence / f'{sequence:02d}.stdout').read_text()
            needle = '        await sendInfo(socket, true);'
            assert original.count(needle) == 1
            delayed = original.replace(needle, '        await new Promise(resolve => setTimeout(resolve, 100));\n' + needle)
            (fixture / 'server.js').write_text(delayed)
            result['server_perturbation'] = {'original_sha256': hashlib.sha256(original.encode()).hexdigest(),
                                           'delayed_sha256': hashlib.sha256(delayed.encode()).hexdigest(),
                                           'change': '100ms before sendInfo; local scheduling fixture only'}
            server_mount = ['-v', str(fixture / 'server.js') + ':/app/server/server.js:ro']
        source = (ROOT / 'proposals/20-uptime-kuma.caddy').read_text()
        result['fragment_sha256'] = hashlib.sha256(source.encode()).hexdigest()
        replacements = {
            'https://uptime.local.theama.co {': 'https://uptime.local.theama.co:8443 {',
            'bind 10.1.0.56 fd36:5aa8:6971:1::56': 'bind 127.0.0.1 ::1',
            'import local_tls': 'tls /work/cert.pem /work/key.pem',
            'remote_ip 10.1.0.0/22 fd36:5aa8:6971:1::/64': 'remote_ip 127.0.0.1/32 ::1/128',
            'reverse_proxy 10.1.3.75:3001 [fd36:5aa8:6971:1::75]:3001':
                'reverse_proxy 127.0.0.1:3001 [::1]:3001',
        }
        for old, new in replacements.items():
            assert source.count(old) == 1
            source = source.replace(old, new)
        (fixture / 'Caddyfile').write_text('{\n admin off\n auto_https disable_redirects\n}\n' + source)
        result['fixture_substitutions'] = replacements
        result['fixture_sha256'] = hashlib.sha256((fixture / 'Caddyfile').read_bytes()).hexdigest()
        run(['podman', 'run', '-d', '--pull', 'never', '--name', names[0],
             '--label', 'homelab.proxy-auth=' + evidence.name, '--network', 'none',
             '--read-only', '--userns', 'keep-id', '--user', f'{os.getuid()}:{os.getgid()}', '--memory', '320m', '--memory-swap', '320m',
             '--env', 'UPTIME_KUMA_DB_TYPE=sqlite',
             '--tmpfs', '/tmp:rw,nosuid,nodev,size=64m',
             '--tmpfs', '/app/data:rw,nosuid,nodev,mode=1777,size=64m',
             '-v', str(fixture) + ':/work:ro', *server_mount, KUMA])
        until = time.monotonic() + 90
        while run(['podman', 'exec', names[0], 'node', '-e',
                   'fetch("http://127.0.0.1:3001/dashboard").then(r=>process.exit(r.status===200?0:1)).catch(()=>process.exit(1))'],
                  check=False) != 0:
            if time.monotonic() >= until:
                raise RuntimeError('Kuma readiness deadline')
            time.sleep(2)
        run(['podman', 'run', '-d', '--pull', 'never', '--name', names[1],
             '--label', 'homelab.proxy-auth=' + evidence.name, '--network', 'container:' + names[0],
             '--read-only', '--tmpfs', '/tmp:rw,nosuid,nodev,size=64m',
             '--tmpfs', '/root:rw,nosuid,nodev,size=16m', '-v', str(fixture) + ':/work:ro',
             '--entrypoint', '/usr/bin/caddy', CADDY, 'run', '--config', '/work/Caddyfile'])
        until = time.monotonic() + 20
        while run(['podman', 'exec', names[1], 'curl', '--noproxy', '*', '--silent', '--show-error',
                   '--fail', '--max-time', '3', '--cacert', '/work/cert.pem',
                   '--resolve', 'uptime.local.theama.co:8443:127.0.0.1',
                   '-o', '/dev/null', 'https://uptime.local.theama.co:8443/dashboard'], check=False) != 0:
            if time.monotonic() >= until:
                raise RuntimeError('Caddy readiness deadline')
            time.sleep(1)
        run(['podman', 'exec', names[0], 'node', '/work/client.cjs', '--staging'], timeout=160)
        result['verdict'] = 'passed'
    finally:
        failures = []
        for name in reversed(names):
            exists = run(['podman', 'container', 'exists', name], check=False)
            if exists == 0:
                run(['podman', 'logs', name], check=False)
                if run(['podman', 'rm', '--force', name], check=False):
                    failures.append(name)
            elif exists != 1:
                failures.append(name)
        result['cleanup_failures'] = failures
        if failures:
            result['verdict'] = 'failed'
        (evidence / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
        print(evidence, flush=True)
        if failures:
            raise RuntimeError('Fixture cleanup failed')


if __name__ == '__main__':
    main()
