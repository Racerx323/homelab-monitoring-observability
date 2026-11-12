#!/usr/bin/env python3
"""Bounded read-only Kuma network evidence; never emit credentials or HTTP bodies."""
import argparse
import hashlib
import http.client
import ipaddress
import json
import os
from pathlib import Path
import re
import selectors
import signal
import sqlite3
import stat
import subprocess
import tempfile
import threading
import time
from urllib.parse import quote

UNIT = 'uptime-kuma.service'
NETWORK_UNIT = 'uptime-kuma-network.service'
DEADLINE = float('inf')


def command(argv, timeout=8, limit=131072):
    """Kill a bounded client process group; discard stderr rather than expose it."""
    until = min(DEADLINE, time.monotonic() + timeout)
    process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               start_new_session=True)
    selector = selectors.DefaultSelector()
    for stream in (process.stdout, process.stderr):
        selector.register(stream, selectors.EVENT_READ)
    streams = {process.stdout: bytearray(), process.stderr: bytearray()}
    error = None
    try:
        while selector.get_map():
            remaining = until - time.monotonic()
            if remaining <= 0:
                error = 'command_timeout'
                break
            for key, _ in selector.select(min(remaining, 0.2)):
                chunk = os.read(key.fileobj.fileno(), 16384)
                if not chunk:
                    selector.unregister(key.fileobj)
                elif sum(map(len, streams.values())) + len(chunk) > limit:
                    error = 'output_limit'
                    break
                else:
                    streams[key.fileobj].extend(chunk)
            if error:
                break
        if error:
            os.killpg(process.pid, signal.SIGKILL)
        process.wait(timeout=2)
        return {'rc': process.returncode, 'error': error,
                'stdout': streams[process.stdout].decode(errors='replace'),
                'stderr': streams[process.stderr].decode(errors='replace')}
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=2)
        selector.close()
        process.stdout.close()
        process.stderr.close()


def successful(argv):
    result = command(argv)
    if result['rc'] or result['error']:
        raise ValueError(Path(argv[0]).name + ' observation unavailable')
    return result['stdout']


def database(path, administrator=False):
    for parent in (path, *path.parents):
        if parent.is_symlink():
            raise ValueError('symlink in data path')
    if not path.is_file() or path.stat().st_size > 67108864 or (path.with_name(path.name + '-wal').exists()
                              and path.with_name(path.name + '-wal').stat().st_size):
        raise ValueError('stopped database or checkpoint required')
    with sqlite3.connect('file:' + quote(str(path)) + '?mode=ro&immutable=1', uri=True) as conn:
        counts = {n: conn.execute('SELECT COUNT(*) FROM "' + n + '"').fetchone()[0]
                  for n in ('user', 'monitor', 'notification')}
        integrity = conn.execute('PRAGMA quick_check').fetchone()[0]
        if administrator:
            active = conn.execute('SELECT COUNT(*) FROM "user" WHERE active = 1').fetchone()[0]
            auth = conn.execute("SELECT value FROM setting WHERE key = 'disableAuth'").fetchone()
            disabled = bool(json.loads(auth[0])) if auth and isinstance(auth[0], str) else bool(auth[0]) if auth else False
            if not (integrity == 'ok' and counts['user'] >= 1 and active >= 1
                    and counts['monitor'] == counts['notification'] == 0 and not disabled):
                raise ValueError('administrator or empty monitored-workload requirement failed')
    return {'counts': counts, 'quick_check': integrity}


def contained_predecessor(expected):
    root = Path('/var/lib/uptime-kuma-maintenance/remaining-deployment')
    paths = [(root, 0o700, True), (root / 'state.json', 0o600, False),
             (root / 'contained', 0o600, False), (root / 'lock', 0o600, False),
             (Path('/run/uptime-kuma-network-diagnostic/operator-ready'), 0o600, False)]
    if expected.get('resume_successor', False):
        paths.insert(-1, (root / 'previous-state.json', 0o600, False))
    for path, mode, directory in paths:
        if any(p.is_symlink() for p in (path, *path.parents)):
            raise ValueError('symlink in contained authority or operator acknowledgement')
        info = path.stat()
        kind = stat.S_ISDIR if directory else stat.S_ISREG
        if not (kind(info.st_mode) and info.st_uid == info.st_gid == 0 and stat.S_IMODE(info.st_mode) == mode):
            raise ValueError('unprotected contained authority or operator acknowledgement')
        if not directory and info.st_size > 4096:
            raise ValueError('oversized authority input')
    raw = (root / 'state.json').read_bytes()
    state = json.loads(raw)
    baseline = expected['contained_state']
    if (set(state) != set(baseline) or any(state[k] != v for k, v in baseline.items() if k != 'contained_at')
            or not baseline['contained_at'] <= state['contained_at'] <= int(time.time())):
        raise ValueError('contained predecessor drift')
    ack = paths[-1][0].read_text().strip()
    if ack != 'Kuma and Webmin login verified; monitors and alerts empty':
        raise ValueError('operator acknowledgement differs')
    result = {'state': state, 'state_sha256': hashlib.sha256(raw).hexdigest(), 'operator_acknowledgement': True}
    if expected.get('resume_successor', False):
        previous_sha = hashlib.sha256((root / 'previous-state.json').read_bytes()).hexdigest()
        if (previous_sha != expected['previous_state_sha256']
                or state.get('predecessor_sha256') != previous_sha
                or 'original_predecessor_sha256' in state):
            raise ValueError('original predecessor differs or successor already consumed')
        result['previous_state_sha256'] = previous_sha
    return result


def preflight(expected):
    global DEADLINE
    DEADLINE = time.monotonic() + 90
    identity = {key: successful(argv).strip() for key, argv in {
        'hostname': ['hostname'], 'architecture': ['uname', '-m'],
        'boot_id': ['cat', '/proc/sys/kernel/random/boot_id'],
        'podman_version': ['podman', '--version'],
        'netavark_version': ['dpkg-query', '--show', '--showformat=${Version}', 'netavark']}.items()}
    for key, value in identity.items():
        if value != expected[key]:
            raise ValueError('target identity drift: ' + key)
    available = int(successful(['awk', '/^MemAvailable:/ {print $2}', '/proc/meminfo']))
    if available < expected.get('minimum_available_kib', 524288):
        raise ValueError('insufficient reviewed operation headroom')
    for row in expected['files']:
        path = Path(row['path'])
        if any(parent.is_symlink() for parent in (path, *path.parents)):
            raise ValueError('symlink in owned input')
        info = path.stat()
        if not (stat.S_ISREG(info.st_mode) and info.st_uid == 0 and info.st_gid == 0
                and stat.S_IMODE(info.st_mode) == int(row['mode'], 8)
                and hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']):
            raise ValueError('owned input drift: ' + row['path'])
    for path in expected['absent_paths']:
        candidate = Path(path)
        if candidate.exists() or any(x.is_symlink() for x in (candidate, *candidate.parents)):
            raise ValueError('diagnostic/permit/override path already exists')
    for unit in (UNIT, NETWORK_UNIT):
        props = dict(line.split('=', 1) for line in successful(
            ['systemctl', 'show', unit, '--property=LoadState,ActiveState,MainPID,UnitFileState']).splitlines())
        if not (props['LoadState'] == 'loaded' and props['ActiveState'] in ('inactive', 'failed')
                and props['MainPID'] == '0' and props['UnitFileState'] == 'generated'):
            raise ValueError('application unit not stopped/generated')
    if not stat.S_ISSOCK(Path('/run/dbus/system_bus_socket').stat().st_mode):
        raise ValueError('system bus unavailable')
    if 'memory' not in Path('/sys/fs/cgroup/cgroup.controllers').read_text().split():
        raise ValueError('memory controller unavailable')
    data_dir = Path('/var/lib/uptime-kuma/data').stat()
    if data_dir.st_uid != 1000 or data_dir.st_gid != 1000 or stat.S_IMODE(data_dir.st_mode) != 0o700:
        raise ValueError('data ownership drift')
    props = successful(['systemctl', 'show', UNIT, '--property=MemoryHigh,MemoryMax,MemorySwapMax'])
    if any(value not in props.splitlines() for value in ('MemoryHigh=268435456', 'MemoryMax=335544320', 'MemorySwapMax=0')):
        raise ValueError('application resource limit drift')
    for unit in ('uptime-kuma-network-diagnostic-containment.timer',
                 'uptime-kuma-network-diagnostic-containment.service',
                 'uptime-kuma-network-diagnostic-observer.service'):
        result = command(['systemctl', 'show', unit, '--property=LoadState', '--value'])
        if result['stdout'].strip() != 'not-found':
            raise ValueError('diagnostic unit already exists')
    firewall = successful(['systemctl', 'show', 'uptime-kuma-firewall.service', '--property=ActiveState,UnitFileState'])
    if 'ActiveState=active' not in firewall.splitlines() or 'UnitFileState=enabled' not in firewall.splitlines():
        raise ValueError('guard is not active/enabled')
    for flag in ('-lnt', '-lnu'):
        if successful(['ss', '-H', flag, '( sport = :3001 or sport = :10000 )']).strip():
            raise ValueError('unexpected application listener')
    if json.loads(successful(['podman', 'ps', '-a', '--format', 'json'])):
        raise ValueError('existing container state')
    network = json.loads(successful(['podman', 'network', 'inspect', 'uptime-kuma']))[0]
    if any(network.get(key) != value for key, value in expected['network'].items()):
        raise ValueError('network baseline drift')
    image = json.loads(successful(['podman', 'image', 'inspect', expected['image_id']]))[0]
    if image['Architecture'] != expected['image_architecture'] or image['Id'].removeprefix('sha256:') != expected['image_id'].removeprefix('sha256:'):
        raise ValueError('image baseline drift')
    resume = expected.get('resume_contained', False)
    predecessor = contained_predecessor(expected) if resume else None
    db = database(Path('/var/lib/uptime-kuma/data/kuma.db'), administrator=resume)
    if not resume and db != {'counts': {'user': 0, 'monitor': 0, 'notification': 0}, 'quick_check': 'ok'}:
        raise ValueError('unexpected application data')
    if expected['require_webmin_contained']:
        webmin = successful(['systemctl', 'show', 'webmin.service', '--property=ActiveState,MainPID,UnitFileState'])
        if not ('MainPID=0' in webmin.splitlines() and 'UnitFileState=disabled' in webmin.splitlines()
                and any('ActiveState=' + value in webmin.splitlines() for value in ('inactive', 'failed'))):
            raise ValueError('Webmin containment drift')
    timing = {unit: dict(line.split('=', 1) for line in successful(
        ['systemctl', 'show', unit, '--property=Restart,RuntimeMaxUSec,TimeoutStartUSec,TimeoutStopUSec']).splitlines())
        for unit in (UNIT, NETWORK_UNIT)}
    print(json.dumps({'format': 'kuma-network-preflight-v1', 'identity': identity,
                      'available_kib': available, 'data': db, 'files_verified': len(expected['files']),
                      'network': expected['network'], 'image_id': expected['image_id'], 'original_timing': timing,
                      'contained_predecessor': predecessor}))


def http_probe(address, port=3001, timeout=4):
    ipaddress.ip_address(address)
    started = time.monotonic()
    connection = http.client.HTTPConnection(address, port, timeout=timeout)
    try:
        connection.request('GET', '/', headers={'Connection': 'close', 'User-Agent': 'kuma-network-diagnostic'})
        response = connection.getresponse()
        return {'status': response.status, 'elapsed_seconds': round(time.monotonic() - started, 3)}
    except (OSError, http.client.HTTPException) as exc:
        return {'error_type': type(exc).__name__, 'elapsed_seconds': round(time.monotonic() - started, 3)}
    finally:
        connection.close()


def log_events(raw):
    """Retain only fixed startup event labels; unknown log text is never emitted."""
    events, omitted = [], 0
    patterns = [('server_listening', r'Listening on:'),
                ('setup_required', r'No user, need setup'),
                ('database_connected', r'(?:Connected to the database|Database connected)'),
                ('database_migration', r'(?:Database Patch|Migration|migration).*?(?:start|complete|done|success)'),
                ('server_ready', r'(?:Server Type: HTTP|Uptime Kuma Version: 2\.5\.9)'),
                ('nscd_start_failed', r'Failed to start nscd')]
    for line in raw.splitlines()[:100]:
        event = next((label for label, pattern in patterns if re.search(pattern, line)), None)
        code = next((code for code in ('EACCES', 'ENOENT', 'EADDRINUSE', 'ENOMEM') if code in line), None)
        if event or code:
            events.append({'event': event or 'startup_error', **({'code': code} if code else {})})
        else:
            omitted += 1
    return {'events': events, 'unclassified_lines_omitted': omitted}


def container():
    data = json.loads(successful(['podman', 'inspect', 'uptime-kuma']))[0]
    network = data['NetworkSettings']['Networks']['uptime-kuma']
    addresses = {}
    for family, key in [('ipv4', 'IPAddress'), ('ipv6', 'GlobalIPv6Address')]:
        value = network.get(key)
        if value:
            parsed = ipaddress.ip_address(value)
            if parsed.version != (4 if family == 'ipv4' else 6) or not parsed.is_private:
                raise ValueError('unexpected container address')
            addresses[family] = value
    return {'name': data['Name'], 'image': data['Image'],
            'state': {k: data['State'].get(k) for k in ('Running', 'Pid', 'OOMKilled', 'StartedAt')},
            'port_bindings': data['HostConfig']['PortBindings'], 'addresses': addresses}


def snapshot():
    rows = {}
    commands = {'unit': ['systemctl', 'show', UNIT, '--property=ActiveState,SubState,MainPID,NRestarts,ControlGroup,MemoryPeak'],
                'ports': ['ss', '-H', '-lnt', 'sport = :3001'],
                'nat': ['nft', '--json', 'list', 'ruleset'],
                'addresses': ['ip', '--json', 'address', 'show'],
                'routes4': ['ip', '-4', '--json', 'route', 'show'],
                'routes6': ['ip', '-6', '--json', 'route', 'show']}
    for key, argv in commands.items():
        result = command(argv)
        rows[key] = {k: result[k] for k in ('rc', 'error', 'stdout')}
    try:
        rows['container'] = container()
    except (ValueError, KeyError, IndexError):
        rows['container'] = {'error_type': 'container_observation_unavailable'}
    logs = command(['podman', 'logs', '--tail', '100', '--timestamps', 'uptime-kuma'], limit=32768)
    rows['logs'] = {**log_events(logs['stdout'] + logs['stderr']), 'rc': logs['rc'], 'error': logs['error']}
    rows['loopback_proxy'] = {}
    for role in ('socket', 'service'):
        result = command(['systemctl', 'show', 'uptime-kuma-loopback.' + role,
                          '--property=LoadState,ActiveState,MainPID,MemoryMax,MemorySwapMax,MemoryPeak,NRestarts,Listen'])
        rows['loopback_proxy'][role] = dict(line.split('=', 1) for line in result['stdout'].splitlines() if '=' in line)
    rows['sysctls'] = {}
    for relative in ('ipv4/ip_forward', 'ipv6/conf/all/forwarding',
                     'ipv4/conf/all/route_localnet', 'ipv4/conf/lo/route_localnet',
                     'ipv4/conf/podman1/route_localnet', 'ipv6/conf/all/disable_ipv6'):
        path = Path('/proc/sys/net') / relative
        rows['sysctls'][relative] = path.read_text().strip() if path.is_file() else 'unavailable'
    return rows


NODE_PROBE = r'''const http=require('node:http'); const host=process.argv[1]; const start=Date.now();
let done=false; const finish=(x)=>{if(!done){done=true;console.log(JSON.stringify({...x,elapsed_seconds:(Date.now()-start)/1000}));}};
const req=http.get({host,port:3001,path:'/',headers:{Connection:'close'}},r=>{finish({status:r.statusCode});r.destroy();});
req.setTimeout(4000,()=>{finish({error_type:'TimeoutError'});req.destroy();});
req.on('error',e=>finish({error_type:['ECONNREFUSED','ECONNRESET','EHOSTUNREACH','ENETUNREACH','EADDRNOTAVAIL'].includes(e.code)?e.code:'ConnectionError'}));
setTimeout(()=>{finish({error_type:'TimeoutError'});req.destroy();},5000).unref();'''


def save_receipt(path, value):
    if path is None:
        return
    for parent in (path, *path.parents):
        if parent.is_symlink():
            raise ValueError('symlink in evidence path')
    info = path.parent.stat()
    if not (stat.S_ISDIR(info.st_mode) and info.st_uid == os.geteuid()
            and stat.S_IMODE(info.st_mode) == 0o700 and path.name == 'observation.json'):
        raise ValueError('unsafe evidence directory')
    encoded = json.dumps(value, separators=(',', ':')).encode()
    if len(encoded) > 524288:
        raise ValueError('receipt exceeds 512 KiB')
    fd, temporary = tempfile.mkstemp(prefix='.observation-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def observe(output_path=None):
    global DEADLINE
    start = time.monotonic()
    DEADLINE = start + 150
    output = {'format': 'kuma-network-diagnostic-v1', 'requests': [], 'snapshots': [], 'samples': [], 'completed': False}
    done = threading.Event()
    def sample():
        root = Path('/sys/fs/cgroup/system.slice/uptime-kuma.service')
        while not done.is_set() and len(output['samples']) < 150:
            row = {'elapsed_seconds': round(time.monotonic() - start, 3)}
            for key in ('memory.current', 'memory.peak', 'memory.events', 'cpu.stat', 'pids.current'):
                try:
                    row[key] = (root / key).read_text().strip()
                except OSError:
                    row[key] = 'unavailable'
            output['samples'].append(row)
            done.wait(1)
    worker = threading.Thread(target=sample)
    worker.start()
    try:
        for round_number, at in enumerate((0, 45)):
            time.sleep(max(0, at - (time.monotonic() - start)))
            try:
                addresses = container()['addresses']
            except (ValueError, KeyError, IndexError):
                addresses = {}
            for family, loopback in [('ipv4', '127.0.0.1'), ('ipv6', '::1')]:
                result = command(['podman', 'exec', 'uptime-kuma', 'node', '-e', NODE_PROBE, loopback], timeout=8, limit=2048)
                try:
                    internal = json.loads(result['stdout']) if result['rc'] == 0 else {'error_type': result['error'] or 'container_exec_failed'}
                    if set(internal) - {'status', 'error_type', 'elapsed_seconds'}:
                        raise ValueError('unexpected probe output')
                except (ValueError, TypeError):
                    internal = {'error_type': 'invalid_container_probe'}
                output['requests'].append({'round': round_number, 'path': 'container-loopback', 'family': family, **internal})
                address = addresses.get(family)
                output['requests'].append({'round': round_number, 'path': 'host-to-container', 'family': family,
                                           **(http_probe(address) if address else {'error_type': 'address_unavailable'})})
                output['requests'].append({'round': round_number, 'path': 'host-published-loopback', 'family': family,
                                           **http_probe(loopback)})
                save_receipt(output_path, output)
            output['snapshots'].append({'round': round_number, 'elapsed_seconds': round(time.monotonic() - start, 3), **snapshot()})
            save_receipt(output_path, output)
        time.sleep(max(0, 90 - (time.monotonic() - start)))
        output['completed'] = len(output['requests']) == 12 and len(output['snapshots']) == 2
    except Exception as exc:
        output['collection_error_type'] = type(exc).__name__
    finally:
        done.set()
        worker.join(timeout=2)
        output['elapsed_seconds'] = round(time.monotonic() - start, 3)
        encoded = json.dumps(output, separators=(',', ':'))
        if len(encoded.encode()) > 524288:
            raise ValueError('receipt exceeds 512 KiB')
        save_receipt(output_path, output)
        print(encoded, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path)
    parser.add_argument('--preflight-json')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.preflight_json:
        preflight(json.loads(args.preflight_json))
    elif args.database:
        print(json.dumps(database(args.database)))
    else:
        observe(args.output)
