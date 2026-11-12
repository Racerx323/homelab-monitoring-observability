#!/usr/bin/env python3
"""Native offline systemd/Caddy qualification of the passive observer."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def run(*args, **kwargs):
    return subprocess.run(args, check=True, capture_output=True, text=True, timeout=30, **kwargs)


def native():
    assert os.geteuid() == 0 and Path('/run/.containerenv').is_file()
    assert Path('/proc/1/comm').read_text().strip() == 'systemd'
    assert os.environ.get('KUMA_OBSERVER_FIXTURE') == '1'
    run('systemctl', 'stop', 'caddy.service')  # Image's default site is not the fixture.
    run('ip', 'addr', 'add', '10.1.0.56/32', 'dev', 'lo')
    run('ip', '-6', 'addr', 'add', 'fd36:5aa8:6971:1::56/128', 'dev', 'lo')
    run('openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-days', '1',
        '-subj', '/CN=uptime.local.theama.co', '-addext',
        'subjectAltName=DNS:uptime.local.theama.co,DNS:pihole0.local.theama.co',
        '-keyout', '/tmp/key.pem', '-out', '/usr/local/share/ca-certificates/fixture.crt')
    run('update-ca-certificates')
    Path('/tmp/Caddyfile').write_text('''{
 admin off
 auto_https disable_redirects
}
https://uptime.local.theama.co, https://pihole0.local.theama.co {
 tls /usr/local/share/ca-certificates/fixture.crt /tmp/key.pem
 respond /dashboard 200
 respond /healthz 204
}
''')
    Path('/etc/systemd/system/caddy.service').write_text('[Service]\nExecStart=/usr/bin/caddy run --config /tmp/Caddyfile\n')
    for unit in ('caddy-sync-health', 'caddy-pihole-web-health'):
        Path('/etc/systemd/system/'+unit+'.service').write_text('[Service]\nType=oneshot\nExecStart=/bin/true\n')
        Path('/etc/systemd/system/'+unit+'.timer').write_text('[Timer]\nOnActiveSec=2s\nOnUnitInactiveSec=15s\nAccuracySec=100ms\n')
    run('systemctl', 'daemon-reload')
    run('systemctl', 'start', 'caddy.service', 'caddy-sync-health.timer', 'caddy-pihole-web-health.timer')
    for attempt in range(20):
        ready = subprocess.run(['curl', '--noproxy', '*', '--fail', '--silent', '--max-time', '1',
                                '--resolve', 'uptime.local.theama.co:443:127.0.0.1',
                                'https://uptime.local.theama.co/dashboard'], capture_output=True)
        if ready.returncode == 0:
            break
        time.sleep(1)
    else:
        print(run('journalctl', '-u', 'caddy.service', '--no-pager').stdout)
        raise RuntimeError('synthetic Caddy did not become ready')
    # Real journalctl empty-result behavior, after the fixture bus is ready.
    module_spec = importlib.util.spec_from_file_location('observer', ROOT/'scripts/observe-proxy-acceptance.py')
    observer = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(observer)
    baseline = run('journalctl', '-n', '0', '--show-cursor', '--no-pager', '--quiet').stdout
    cursor = [line[11:] for line in baseline.splitlines() if line.startswith('-- cursor: ')][0]
    empty = ['journalctl', '-u', 'fixture-no-records.service', '--after-cursor', cursor,
             '--no-pager', '--quiet', '--output=json', '-n', '1001']
    previous = subprocess.run(empty + ['--show-cursor'], capture_output=True, text=True, timeout=10)
    assert previous.returncode == 1 and previous.stdout == '' and previous.stderr == ''
    assert observer.command(empty) == ''
    invalid = list(empty)
    invalid[invalid.index('--after-cursor')+1] = 'invalid'
    try:
        observer.command(invalid)
        raise AssertionError('invalid cursor accepted')
    except observer.CommandFailure as error:
        assert error.details['diagnostic'] == 'invalid-cursor'
        diagnostic = error.details
    Path('/qual/journal-contract.json').write_text(json.dumps({
        'old_empty_status': previous.returncode, 'corrected_empty_status': 0,
        'invalid_cursor': diagnostic,
        'version': run('journalctl', '--version').stdout.splitlines()[0]})+'\n')
    release = Path('/etc/caddy/releases/fixture-accepted')
    (release/'conf.d').mkdir(parents=True)
    (release/'manifest.sha256').write_text('fixture manifest\n')
    (release/'conf.d/20-uptime-kuma.caddy').write_text('fixture fragment\n')
    Path('/etc/caddy/current').symlink_to(release)
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    spec = dict(operation='fixture', release=release.name,
                manifest_sha256=sha(release/'manifest.sha256'),
                fragment_sha256=sha(release/'conf.d/20-uptime-kuma.caddy'))
    node = dict(name='node-a', fqdn='pihole0.local.theama.co', ipv4='127.0.0.1', ipv6='::1')
    command = ['python3', str(ROOT/'scripts/observe-proxy-acceptance.py'), '--node', json.dumps(spec), json.dumps(node)]
    with Path('/qual/native.stdout').open('w') as out, Path('/qual/native.stderr').open('w') as err:
        completed = subprocess.run(command, stdout=out, stderr=err, timeout=380)
    Path('/qual/native.status').write_text(str(completed.returncode)+'\n')
    assert completed.returncode == 0
    result = json.loads(Path('/qual/native.stdout').read_text())
    assert result['status'] == 'passed' and result['http'][1]['elapsed'] >= 65


def main():
    os.umask(0o077)
    evidence = Path(tempfile.mkdtemp(prefix='proxy-observer-native-', dir='/home/aaron/code/.local-evidence/uptime-kuma'))
    print(evidence, flush=True)
    name = evidence.name
    result = {'status': 'failed', 'scope': 'offline synthetic AMD64 systemd/Caddy; not live acceptance'}
    try:
        image = run('podman', 'image', 'inspect', '--format', '{{.Id}}', 'localhost/caddy-application-validation:local').stdout.strip()
        result['image'] = image
        result['source_sha256'] = hashlib.sha256((ROOT/'scripts/observe-proxy-acceptance.py').read_bytes()).hexdigest()
        run('podman', 'run', '-d', '--pull=never', '--name', name, '--network=none',
            '--cap-add=NET_ADMIN', '--systemd=always', '--env', 'KUMA_OBSERVER_FIXTURE=1',
            '--volume', str(ROOT)+':/source:ro', '--volume', str(evidence)+':/qual', image)
        with (evidence/'qualification.log').open('w') as log:
            completed = subprocess.run(['podman', 'exec', name, 'python3', '/source/tests/qualify-proxy-observation.py', '--native'], stdout=log, stderr=log, timeout=420)
        result['exit'] = completed.returncode
        if completed.returncode == 0:
            result['status'] = 'passed'
    finally:
        exists = subprocess.run(['podman', 'container', 'exists', name], capture_output=True).returncode
        result['cleanup'] = subprocess.run(['podman', 'rm', '--force', name], capture_output=True).returncode if exists == 0 else (0 if exists == 1 else exists)
        if result['cleanup']:
            result['status'] = 'failed'
        (evidence/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    raise SystemExit(0 if result['status'] == 'passed' else 1)


if __name__ == '__main__':
    native() if sys.argv[1:] == ['--native'] else main()
