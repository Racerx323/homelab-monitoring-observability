#!/usr/bin/env python3
"""Passive Caddy acceptance: stream to a node; never install or control services."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import time

UNITS = ('caddy-sync-health.service', 'caddy-pihole-web-health.service')
PROPERTIES = ('ExecMainStartTimestampMonotonic', 'ExecMainExitTimestampMonotonic',
              'ExecMainCode', 'ExecMainStatus', 'Result', 'ActiveState')
LIMIT = 1024 * 1024


def require(ok, check):
    if not ok:
        raise ValueError(check)


class CommandFailure(ValueError):
    def __init__(self, details):
        self.details = details
        super().__init__('command-failure:' + json.dumps(details, sort_keys=True))


def command(argv, timeout=10):
    program = argv[0] if argv[0] in {'journalctl', 'curl', 'systemctl'} else 'other'
    operation = ('journal-follow' if '--after-cursor' in argv else 'journal-baseline') if program == 'journalctl' else program
    details = {'program': program, 'operation': operation, 'expected_exit': 0}
    try:
        completed = subprocess.run(argv, capture_output=True, timeout=timeout, text=True)
    except subprocess.TimeoutExpired:
        raise CommandFailure(dict(details, diagnostic='timeout', timeout_seconds=timeout)) from None
    except OSError:
        raise CommandFailure(dict(details, diagnostic='launch-error')) from None
    details.update(observed_exit=completed.returncode,
                   stdout_bytes=len(completed.stdout.encode()), stderr_bytes=len(completed.stderr.encode()))
    if details['stdout_bytes'] > LIMIT or details['stderr_bytes'] > LIMIT:
        raise CommandFailure(dict(details, diagnostic='output-limit'))
    if completed.returncode:
        message = completed.stderr.strip()
        diagnostic = 'unclassified'
        if not message and not completed.stdout:
            diagnostic = 'no-output'
        elif program == 'journalctl' and message == 'Failed to seek to cursor: Invalid argument':
            diagnostic = 'invalid-cursor'
        elif program == 'journalctl' and 'Permission denied' in message:
            diagnostic = 'permission-denied'
        # No raw argv/cursor, stdout, stderr or journal messages enter failures.
        raise CommandFailure(dict(details, diagnostic=diagnostic))
    return completed.stdout


def identity(spec):
    current = Path('/etc/caddy/current').resolve(strict=True)
    expected_path = '/etc/caddy/releases/' + spec['release']
    require(str(current) == expected_path, 'release-selection:expected=' + expected_path + ':observed=' + str(current))
    for name, expected in [('manifest.sha256', spec['manifest_sha256']),
                           ('conf.d/20-uptime-kuma.caddy', spec['fragment_sha256'])]:
        actual = hashlib.sha256((current / name).read_bytes()).hexdigest()
        require(actual == expected, 'release-identity:' + name + ':expected=' + expected + ':observed=' + actual)
    return {'release': spec['release'], 'manifest_sha256': spec['manifest_sha256'],
            'fragment_sha256': spec['fragment_sha256']}


def unit_state(unit):
    raw = command(['systemctl', 'show', unit, '--no-pager',
                   '--property=' + ','.join(PROPERTIES)])
    values = dict(line.split('=', 1) for line in raw.splitlines())
    require(set(values) == set(PROPERTIES), 'unit-properties')
    for key in PROPERTIES[:4]:
        values[key] = int(values[key])
    require(values['Result'] == 'success' and values['ExecMainStatus'] == 0,
            'unit-result:' + unit + ':expected=success/0:observed=' + values['Result'] + '/' + str(values['ExecMainStatus']))
    return values


def http_rows(node):
    rows = []
    for family, address, vip in [(4, node['ipv4'], '10.1.0.56'),
                                  (6, node['ipv6'], 'fd36:5aa8:6971:1::56')]:
        for label, host, target, path, expected in [
                ('node', 'uptime.local.theama.co', address, '/dashboard', 200),
                ('shared', 'uptime.local.theama.co', vip, '/dashboard', 200),
                ('health', node['fqdn'], address, '/healthz', 204)]:
            resolved = '[' + target + ']' if family == 6 else target
            status = command(['curl', '--noproxy', '*', '-' + str(family),
                              '--silent', '--show-error', '--fail', '--connect-timeout', '3',
                              '--max-time', '5', '--resolve', host + ':443:' + resolved,
                              '-o', '/dev/null', '-w', '%{http_code}', 'https://' + host + path])
            require(status == str(expected), 'http:' + label + ':' + str(family)
                    + ':expected=' + str(expected) + ':observed=' + status)
            rows.append({'path': label, 'family': family, 'expected': expected, 'observed': int(status)})
    return rows


def journal_summary(cursor):
    raw = command(['journalctl', '-u', 'caddy.service', '--after-cursor', cursor,
                   '--no-pager', '--quiet', '--output=json', '-n', '1001'])
    lines = raw.splitlines()
    events = [json.loads(line) for line in lines if not line.startswith('-- cursor: ')]
    require(len(events) < 1000, 'journal-truncated')
    # Reject conservatively: uncertain health/error events do not prove health.
    adverse = []
    for event in events:
        message = event.get('MESSAGE')
        require(isinstance(message, str), 'journal-message')
        lowered = message.lower()
        relevant = any(s in lowered for s in ('health', 'upstream', '10.1.3.75', '::75', 'reverse_proxy'))
        bad = re.search(r'fail|unhealthy|unavailable|excluded|"level"\s*:\s*"(?:error|warn)"|"healthy"\s*:\s*false', lowered)
        if relevant and bad:
            adverse.append(hashlib.sha256(message.encode()).hexdigest())
    return {'events': len(events), 'adverse': len(adverse), 'adverse_message_sha256': adverse,
            'raw_sha256': hashlib.sha256(raw.encode()).hexdigest()}


def observe(spec, node):
    result = {'node': node['name'], 'status': 'failed', 'samples': [], 'http': [],
              'spec_sha256': hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()}
    try:
        start = time.monotonic()
        baseline = int(start * 1000000)
        raw = command(['journalctl', '-n', '0', '--show-cursor', '--no-pager', '--quiet'])
        cursors = [line[11:] for line in raw.splitlines() if line.startswith('-- cursor: ')]
        require(len(cursors) == 1 and bool(cursors[0]), 'journal-cursor')
        result['initial_identity'] = identity(spec)
        result['baseline_monotonic_usec'] = baseline
        first_rows = http_rows(node)
        first_completed = time.monotonic()
        result['http'].append({'elapsed': first_completed-start, 'rows': first_rows})
        cycles = {unit: set() for unit in UNITS}
        while time.monotonic() - start < 320:
            sample = {'elapsed': time.monotonic()-start, 'units': {}}
            for unit in UNITS:
                state = unit_state(unit)
                sample['units'][unit] = state
                began, ended = (state[k] for k in PROPERTIES[:2])
                if began > baseline and ended >= began and state['ExecMainCode'] == 1:
                    cycles[unit].add(began)
            result['samples'].append(sample)
            if time.monotonic()-first_completed >= 65 and all(len(v) >= 2 for v in cycles.values()):
                break
            time.sleep(5)
        require(all(len(v) >= 2 for v in cycles.values()),
                'completed-cycles-timeout:expected=2:observed=' + json.dumps({k: len(v) for k, v in cycles.items()}))
        final_rows = http_rows(node)
        result['http'].append({'elapsed': time.monotonic()-start, 'rows': final_rows})
        result['final_identity'] = identity(spec)
        result['journal'] = journal_summary(cursors[0])
        require(result['journal']['adverse'] == 0, 'journal-health-failure')
        require(time.monotonic()-start <= 360, 'observation-deadline')
        result['status'] = 'passed'
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        result['failure'] = str(error) if isinstance(error, ValueError) else type(error).__name__
        if isinstance(error, CommandFailure):
            result['command_failure'] = error.details
    return result


def verify_node(spec, node, result):
    require(result['node'] == node['name'] and result['status'] == 'passed', 'node-result')
    require(result['spec_sha256'] == hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest(),
            'node-spec')
    expected = {k: spec[k] for k in ('release', 'manifest_sha256', 'fragment_sha256')}
    require(result['initial_identity'] == result['final_identity'] == expected, 'node-identity')
    http = result['http']
    require(len(http) == 2 and 0 <= http[0]['elapsed']
            and http[1]['elapsed'] - http[0]['elapsed'] >= 65
            and http[1]['elapsed'] <= 360, 'http-window')
    wanted = {(label, family, code, code) for family in (4, 6)
              for label, code in [('node', 200), ('shared', 200), ('health', 204)]}
    for checkpoint in http:
        require(len(checkpoint['rows']) == 6 and
                {(r['path'], r['family'], r['expected'], r['observed']) for r in checkpoint['rows']} == wanted,
                'http-results')
    for unit in UNITS:
        cycles = set()
        for sample in result['samples']:
            state = sample['units'][unit]
            require(state['Result'] == 'success' and state['ExecMainStatus'] == 0, 'cycle-result')
            begin, end = (state[k] for k in PROPERTIES[:2])
            if begin > result['baseline_monotonic_usec'] and end >= begin and state['ExecMainCode'] == 1:
                cycles.add(begin)
        require(len(cycles) >= 2, 'cycle-count')
    require(result['journal']['adverse'] == 0 and result['journal']['adverse_message_sha256'] == []
            and result['journal']['events'] < 1000, 'journal-result')


def ssh_command(spec, node):
    remote = 'cd / && sudo -n python3 - --node ' + shlex.quote(json.dumps(spec)) + ' ' + shlex.quote(json.dumps(node))
    return ['ssh', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes',
            '-o', 'ConnectTimeout=10', '-o', 'ServerAliveInterval=5',
            '-o', 'ServerAliveCountMax=3', node['ssh'], remote]


def run_nodes(spec, destination):
    destination.mkdir(mode=0o700)  # Existing evidence is consumed; never overwrite/retry.
    source = Path(__file__).read_bytes()
    for node in spec['nodes']:
        argv = ssh_command(spec, node)
        prefix = destination / node['name']
        prefix.with_suffix('.command.json').write_text(json.dumps(argv)+'\n')
        prefix.with_suffix('.source-sha256').write_text(hashlib.sha256(source).hexdigest()+'\n')
        with prefix.with_suffix('.stdout').open('wb') as out, prefix.with_suffix('.stderr').open('wb') as err:
            try:
                result = subprocess.run(argv, input=source, stdout=out, stderr=err, timeout=400)
                status = result.returncode
            except subprocess.TimeoutExpired:
                status = 124
        prefix.with_suffix('.status').write_text(str(status)+'\n')
        require(status == 0, 'ssh-status:' + node['name'])
        require(prefix.with_suffix('.stdout').stat().st_size <= LIMIT, 'ssh-output-limit')
        verify_node(spec, node, json.loads(prefix.with_suffix('.stdout').read_text()))


def verify_combined(spec, destination, receipt):
    module_spec = importlib.util.spec_from_file_location('private_login', Path(__file__).with_name('private-proxy-login.py'))
    helper = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(helper)
    helper.verify_receipt(receipt, standalone_operation=spec['operation'])
    for node in spec['nodes']:
        prefix = destination / node['name']
        for suffix in ('.stdout', '.status', '.command.json', '.source-sha256'):
            path = prefix.with_suffix(suffix)
            info = path.lstat()
            require(path.is_file() and not path.is_symlink() and info.st_uid == os.getuid()
                    and info.st_mode & 0o077 == 0 and info.st_size <= LIMIT, 'evidence-file')
        require(prefix.with_suffix('.status').read_text() == '0\n', 'evidence-status')
        require(json.loads(prefix.with_suffix('.command.json').read_text()) == ssh_command(spec, node), 'evidence-command')
        require(prefix.with_suffix('.source-sha256').read_text().strip() == hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'evidence-source')
        verify_node(spec, node, json.loads(prefix.with_suffix('.stdout').read_text()))
    return {'status': 'passed', 'operation': spec['operation'], 'dns': 'pending',
            'release': spec['release'], 'private_receipt_sha256': hashlib.sha256(receipt.read_bytes()).hexdigest()}


if __name__ == '__main__':
    os.umask(0o077)
    if sys.argv[1] == '--node':
        # An alarm bounds remote work even if the SSH controller disappears.
        import signal
        def deadline(_signum, _frame):
            raise TimeoutError('observation deadline')
        signal.signal(signal.SIGALRM, deadline)
        signal.alarm(360)
        observed = observe(json.loads(sys.argv[2]), json.loads(sys.argv[3]))
        print(json.dumps(observed))
        sys.exit(0 if observed['status'] == 'passed' else 1)
    elif sys.argv[1] == '--run':
        run_nodes(json.loads(Path(sys.argv[2]).read_text()), Path(sys.argv[3]))
    elif sys.argv[1] == '--verify-combined':
        print(json.dumps(verify_combined(json.loads(Path(sys.argv[2]).read_text()),
                                         Path(sys.argv[3]), Path(sys.argv[4]))))
    else:
        raise SystemExit('Expected --run SPEC EVIDENCE_DIRECTORY')
