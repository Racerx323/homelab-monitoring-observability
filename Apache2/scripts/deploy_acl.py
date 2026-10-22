"""Sealed Apache ACL transaction with detached worker and independent timed recovery."""
import argparse
import fcntl
import hashlib
import importlib.util
import io
import ipaddress
import json
import os
from pathlib import Path
import re
import secrets
import shlex
import socket
import ssl
import stat
import subprocess
import sys
import tarfile
import time

ROOT = Path(__file__).resolve().parent
STATE = Path('/var/lib/svmf-apache-acl')
MEMBERS = {'deploy_acl.py', 'tls_probe.py', 'candidate.conf', 'baseline.conf',
           'ca.pem', 'known_hosts', 'spec.json'}
OLD_RULE = b'Require ip 192.168.0.0/16 10.0.0.0/8 172.16.0.0/12 ::1'
NEW_RULE = OLD_RULE+b' fd36:5aa8:6971:1::/64'
TERMINAL = {'committed', 'restored', 'preflight_failed', 'recovery_held'}
ENV = {'PATH': '/usr/sbin:/usr/bin:/sbin:/bin', 'LC_ALL': 'C'}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True)+'\n').encode()


def sync(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write(path, raw):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    sync(path.parent)


def save(path, value):
    temporary = path.with_name('.'+path.name+'.'+secrets.token_hex(8))
    write(temporary, encoded(value))
    os.replace(temporary, path)
    sync(path.parent)


def command(argv, timeout=15):
    row = subprocess.run(argv, capture_output=True, timeout=timeout, env=ENV)
    if row.returncode or len(row.stdout)+len(row.stderr) > 262144:
        raise RuntimeError('command failed: '+Path(argv[0]).name)
    return row.stdout.decode().strip()


def service():
    row = dict(x.split('=', 1) for x in command(['/usr/bin/systemctl', 'show', 'apache2.service',
               '--property=MainPID,InvocationID,NRestarts,ActiveState,SubState']).splitlines())
    if row.get('ActiveState') != 'active' or row.get('SubState') != 'running' or int(row.get('MainPID', '0')) < 1:
        raise ValueError('Apache must remain active/running')
    return row


def identity(spec):
    if (os.geteuid() != 0 or socket.gethostname() != spec['hostname']
            or Path('/proc/sys/kernel/random/boot_id').read_text().strip() != spec['boot_id']):
        raise ValueError('root/hostname/boot drift')
    if service() != spec['service']:
        raise ValueError('Apache service identity drift')
    version = command(['/usr/sbin/apache2ctl', '-v'])
    if sha(version.encode()) != spec['version_sha256']:
        raise ValueError('Apache version drift')
    reload_spec = command(['/usr/bin/systemctl', 'show', 'apache2.service', '--property=ExecReload', '--value'])
    if not re.fullmatch(r'\{ path=(/usr/sbin/apache(?:2)?ctl) ; argv\[\]=\1 graceful ; ignore_errors=no ;[^{}]*\}', reload_spec):
        raise ValueError('unqualified Apache ExecReload')


def config_files(spec, candidate=False, parse=True):
    if parse:
        output = command(['/usr/sbin/apache2ctl', '-t', '-D', 'DUMP_INCLUDES'])
        paths = set(re.findall(r'^\s*\([^\n)]{1,80}\)\s+(/etc/apache2/[^\s]{1,256})\s*$', output, re.M))
        if paths != {row['path'] for row in spec['configs']}:
            raise ValueError('Apache include set drift')
    for row in spec['configs']:
        path = Path(row['path']).resolve(strict=True)
        info = path.stat()
        expected = spec['candidate_sha256'] if candidate and str(path) == spec['target'] else row['sha256']
        if (str(path) != row['resolved'] or not path.is_relative_to('/etc/apache2')
                or not stat.S_ISREG(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022
                or info.st_size > 131072 or sha(path.read_bytes()) != expected):
            raise ValueError('Apache included-file drift')


def target_info(spec):
    path = Path(spec['target'])
    for parent in (path, *path.parents):
        info = parent.lstat()
        if stat.S_ISLNK(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
            raise ValueError('protected target ancestry required')
        if parent == Path('/etc'):
            break
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) not in (0o600, 0o640, 0o644):
        raise ValueError('unexpected target type/mode')
    return {'uid': info.st_uid, 'gid': info.st_gid, 'mode': stat.S_IMODE(info.st_mode)}


def replace_target(spec, data, metadata):
    path = Path(spec['target'])
    temporary = path.with_name('.'+path.name+'.'+secrets.token_hex(8))
    write(temporary, data)
    os.chown(temporary, metadata['uid'], metadata['gid'])
    os.chmod(temporary, metadata['mode'])
    fd = os.open(temporary, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(temporary, path)
    sync(path.parent)


def unpack(raw, digest, expiry=True):
    if len(raw) > 1048576 or sha(raw) != digest:
        raise ValueError('archive hash/size')
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:') as archive:
        entries = archive.getmembers()
        if len(entries) != len(MEMBERS) or {e.name for e in entries} != MEMBERS or any(not e.isfile() or e.size > 524288 for e in entries):
            raise ValueError('closed regular member set')
        files = {e.name: archive.extractfile(e).read() for e in entries}
    spec = json.loads(files['spec.json'])
    if spec['members'] != {n: sha(d) for n, d in files.items() if n != 'spec.json'}:
        raise ValueError('member integrity')
    if not re.fullmatch(r'svmf-apache-acl-[a-z0-9-]{1,48}', spec['operation_id']):
        raise ValueError('operation id')
    if expiry and not spec['prepared_epoch'] <= time.time() < spec['expires_epoch']:
        raise ValueError('expired/future bundle')
    if (spec['expires_epoch']-spec['prepared_epoch'] != 86400
            or not 3 <= spec['confirm_seconds'] < spec['worker_seconds'] < spec['guard_seconds'] <= 240
            or spec['target'] != '/etc/apache2/sites-available/001-munin.theama.co-ssl.conf'
            or sha(files['baseline.conf']) != spec['baseline_sha256']
            or sha(files['candidate.conf']) != spec['candidate_sha256']
            or files['baseline.conf'].count(OLD_RULE) != 4
            or files['candidate.conf'] != files['baseline.conf'].replace(OLD_RULE, NEW_RULE)
            or [ipaddress.ip_address(a).version for a in spec['addresses']] != [4, 6]):
        raise ValueError('bounded four-list ACL scope')
    return spec, files


def load(directory):
    if os.geteuid() != 0 or directory.parent != STATE or directory.is_symlink():
        raise ValueError('root private operation directory required')
    for path in (STATE, directory):
        info = path.lstat()
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o077:
            raise ValueError('unsafe operation storage')
    state = json.loads((directory/'state.json').read_bytes())
    spec, files = unpack((directory/'deployment.tar').read_bytes(), state['sha256'], expiry=False)
    if files['deploy_acl.py'] != Path(__file__).read_bytes() or spec['operation_id'] != directory.name:
        raise ValueError('frozen worker identity')
    return spec, files, state


def record(directory, state, phase, **fields):
    state.update(fields, phase=phase, updated=time.time())
    save(directory/'state.json', state)


def reload_apache(spec):
    identity(spec)
    command(['/usr/bin/systemctl', 'reload', 'apache2.service'], timeout=30)
    identity(spec)


def restore(directory, spec, files, state):
    if not state.get('write_intent'):
        record(directory, state, 'preflight_failed')
        return
    try:
        identity(spec)
        current = sha(Path(spec['target']).read_bytes())
        if current not in (spec['baseline_sha256'], spec['candidate_sha256']):
            raise ValueError('foreign vhost drift; backup retained')
        # A failed syntax test must not block restoring our exact original bytes.
        config_files(spec, candidate=current == spec['candidate_sha256'], parse=False)
        metadata = state['metadata']
        if target_info(spec) != metadata or sha((directory/'original.conf').read_bytes()) != spec['baseline_sha256']:
            raise ValueError('backup/metadata drift')
        # Persist intent before each restoration write; a killed restore remains resumable by the guard.
        record(directory, state, 'restoring')
        replace_target(spec, (directory/'original.conf').read_bytes(), metadata)
        command(['/usr/sbin/apache2ctl', 'configtest'])
        if state.get('reload_intent'):
            reload_apache(spec)
        config_files(spec)
        identity(spec)
        record(directory, state, 'restored', target_sha256=spec['baseline_sha256'])
    except Exception as error:
        record(directory, state, 'recovery_held', recovery_error=type(error).__name__)


def valid_proof(spec, state, proof):
    expected = {(a, p) for a in spec['addresses'] for p in spec['paths']}
    rows = proof['rows']
    if (proof['sha256'] != state['sha256'] or proof['challenge'] != state['challenge']
            or time.time() >= state['deadline'] or len(rows) != len(expected)
            or {(r['address'], r['path']) for r in rows} != expected):
        raise ValueError('confirmation identity/scope/deadline')
    for row in rows:
        kind = 'image/png' if row['path'].endswith('.png') else 'text/css' if row['path'].endswith('.css') else 'text/html'
        if (not row.get('tls_verified') or not row.get('response_ok') or row.get('content_type') != kind
                or row.get('leaf_sha256') != spec['leaf_sha256']
                or kind == 'image/png' and not row.get('png_signature')):
            raise ValueError('confirmation response failed')


def worker(directory, recovery=False):
    spec, files, state = load(directory)
    with (directory/'lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        spec, files, state = load(directory)
        if state['phase'] in TERMINAL:
            return state
        if recovery:
            restore(directory, spec, files, state)
            return state
        try:
            identity(spec)
            config_files(spec)
            metadata = target_info(spec)
            command(['/usr/sbin/apache2ctl', 'configtest'])
            write(directory/'original.conf', Path(spec['target']).read_bytes())
            if sha((directory/'original.conf').read_bytes()) != spec['baseline_sha256']:
                raise ValueError('backup integrity')
            record(directory, state, 'write_intent', write_intent=True, metadata=metadata)
            replace_target(spec, files['candidate.conf'], metadata)
            command(['/usr/sbin/apache2ctl', 'configtest'])
            config_files(spec, candidate=True)
            record(directory, state, 'reload_intent', reload_intent=True)
            reload_apache(spec)
            record(directory, state, 'awaiting_confirmation', challenge=secrets.token_hex(24),
                   deadline=time.time()+spec['confirm_seconds'])
            while time.time() < state['deadline']:
                if (directory/'rejected.json').exists():
                    raise ValueError('controller rejected health')
                if (directory/'confirmation.json').exists():
                    valid_proof(spec, state, json.loads((directory/'confirmation.json').read_bytes()))
                    identity(spec)
                    config_files(spec, candidate=True)
                    if target_info(spec) != metadata:
                        raise ValueError('candidate metadata drift')
                    record(directory, state, 'committed', target_sha256=spec['candidate_sha256'])
                    return state
                time.sleep(0.25)
            raise TimeoutError('controller confirmation deadline')
        except Exception as error:
            record(directory, state, 'failed', error_type=type(error).__name__)
            restore(directory, spec, files, state)
            return state


def install(raw, digest):
    spec, files = unpack(raw, digest)
    identity(spec)
    os.umask(0o077)
    STATE.mkdir(mode=0o700, exist_ok=True)
    info = STATE.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o077:
        raise ValueError('private state root required')
    directory = STATE/spec['operation_id']
    directory.mkdir(mode=0o700)  # Exclusive on-target replay guard, before launching anything.
    for name, data in files.items():
        write(directory/name, data)
    write(directory/'deployment.tar', raw)
    state = {'phase': 'staged', 'sha256': digest, 'operation_id': spec['operation_id'], 'updated': time.time()}
    save(directory/'state.json', state)
    common = ['--quiet', '--property=Type=exec', '--property=Restart=no', '--property=UMask=0077',
              '--working-directory=/', '--property=StandardOutput=append:'+str(directory/'worker.log'),
              '--property=StandardError=append:'+str(directory/'worker.log')]
    # Independent systemd timer is armed before the worker can write the vhost.
    command(['/usr/bin/systemd-run', '--unit='+spec['operation_id']+'-recover',
             '--on-active='+str(spec['guard_seconds'])+'s', '--timer-property=AccuracySec=1s',
             *common, '/usr/bin/python3', '-I', '-B', str(directory/'deploy_acl.py'), 'recover', str(directory)])
    command(['/usr/bin/systemd-run', '--unit='+spec['operation_id'],
             '--property=RuntimeMaxSec='+str(spec['worker_seconds']), *common,
             '/usr/bin/python3', '-I', '-B', str(directory/'deploy_acl.py'), 'worker', str(directory)])
    return state


def action(directory, name, proof=None):
    spec, files, state = load(directory)
    if name == 'status':
        return state
    if state['phase'] != 'awaiting_confirmation':
        raise ValueError('not awaiting confirmation')
    if name == 'confirm':
        valid_proof(spec, state, proof)
        write(directory/'confirmation.json', encoded(proof))
    elif name == 'reject':
        write(directory/'rejected.json', encoded({'rejected': True}))
    return {'recorded': name}


def ssh(spec, known_hosts, remote):
    options = ['BatchMode=yes', 'StrictHostKeyChecking=yes', 'HostKeyAlgorithms=ssh-ed25519',
               'UpdateHostKeys=no', 'ProxyCommand=none', 'ProxyJump=none', 'ControlMaster=no',
               'ControlPath=none', 'ControlPersist=no', 'PermitLocalCommand=no', 'ClearAllForwardings=yes',
               'ForwardAgent=no', 'ForwardX11=no', 'GlobalKnownHostsFile=/dev/null',
               'UserKnownHostsFile='+str(known_hosts), 'HostKeyAlias='+spec['host_key_alias'], 'ConnectTimeout=5']
    return ['/usr/bin/ssh', '-F', '/dev/null', '-T', '-4',
            *[x for option in options for x in ('-o', option)], spec['user']+'@'+spec['addresses'][0], remote]


def transport(spec, directory, remote, data=b''):
    row = subprocess.run(ssh(spec, directory/'known_hosts', remote), input=data, capture_output=True, timeout=40)
    number = len(list(directory.glob('ssh-*.json')))
    receipt = {'returncode': row.returncode, 'stderr_sha256': sha(row.stderr)}
    if len(row.stdout)+len(row.stderr) > 1048576:
        raise ValueError('SSH response bound')
    write(directory/('ssh-'+str(number)+'.json'), encoded(receipt))
    if row.returncode:
        raise RuntimeError('SSH failed; inspect existing operation, never replay')
    return json.loads(row.stdout)


def remote(spec, directory, name, proof=None):
    argv = ['sudo', '-n', '/usr/bin/python3', '-I', '-B', str(STATE/spec['operation_id']/'deploy_acl.py'),
            name, str(STATE/spec['operation_id'])]
    return transport(spec, directory, 'cd / && '+shlex.join(argv), b'' if proof is None else encoded(proof))


def https_observations(spec, directory, files, baseline):
    loader = importlib.util.spec_from_file_location('tls_probe', directory/'tls_probe.py')
    helper = importlib.util.module_from_spec(loader)
    loader.loader.exec_module(helper)
    context = ssl.create_default_context(cadata=files['ca.pem'].decode('ascii'))
    rows = []
    for address in spec['addresses']:
        for path in spec['paths']:
            row, _ = helper.request(address, path, context)
            rows.append(row)
    expected = {(a, p): (403 if baseline and ':' in a and p != '/' else 200) for a in spec['addresses'] for p in spec['paths']}
    passed = True
    for row in rows:
        status = expected[(row['address'], row['path'])]
        kind = 'image/png' if row['path'].endswith('.png') else 'text/css' if row['path'].endswith('.css') else 'text/html'
        passed &= (row.get('tls_verified') is True and row.get('leaf_sha256') == spec['leaf_sha256'] and row.get('status') == status
                   and (status == 403 or row.get('response_ok') and row.get('content_type') == kind
                        and (kind != 'image/png' or row.get('png_signature'))))
    return {'passed': bool(passed), 'rows': rows}


BOOTSTRAP = "import sys,hashlib,tarfile,io; raw=sys.stdin.buffer.read(1048577); assert hashlib.sha256(raw).hexdigest()==sys.argv[1]; a=tarfile.open(fileobj=io.BytesIO(raw)); source=a.extractfile('deploy_acl.py').read(); ns={'__name__':'bootstrap','__file__':'/sealed/deploy_acl.py'}; exec(source,ns); print(ns['json'].dumps(ns['install'](raw,sys.argv[1])))"


def execute(directory, digest):
    spec, files = unpack((directory/'deployment.tar').read_bytes(), digest)
    if (files['deploy_acl.py'] != Path(__file__).read_bytes()
            or any((directory/n).read_bytes() != files[n] for n in ('tls_probe.py', 'known_hosts'))):
        raise ValueError('use frozen controller and inputs')
    write(directory/'execution.json', encoded({'sha256': digest, 'epoch': int(time.time())}))
    before = https_observations(spec, directory, files, True)
    write(directory/'before.json', encoded(before))
    if not before['passed']:
        raise ValueError('baseline HTTPS drift; no SSH staging attempted')
    bootstrap = 'cd / && sudo -n /usr/bin/python3 -I -B -c '+shlex.quote(BOOTSTRAP)+' '+digest
    transport(spec, directory, bootstrap, (directory/'deployment.tar').read_bytes())
    deadline = time.monotonic()+spec['guard_seconds']+45
    submitted = False
    while time.monotonic() < deadline:
        state = remote(spec, directory, 'status')
        save(directory/'remote-state.json', state)
        if state['phase'] in TERMINAL:
            baseline = state['phase'] != 'committed'
            after = https_observations(spec, directory, files, baseline)
            write(directory/'after.json', encoded(after))
            result = {'state': state, 'https_verified': after['passed'], 'accepted': state['phase'] == 'committed' and after['passed']}
            write(directory/'result.json', encoded(result))
            return result
        if state['phase'] == 'awaiting_confirmation' and not submitted:
            health = https_observations(spec, directory, files, False)
            write(directory/'candidate-health.json', encoded(health))
            proof = {'sha256': digest, 'challenge': state['challenge'], 'rows': health['rows']}
            remote(spec, directory, 'confirm' if health['passed'] else 'reject', proof if health['passed'] else None)
            submitted = True
        time.sleep(2)
    raise TimeoutError('controller deadline; retain state and inspect, no replay')


def seal(args):
    baseline_raw = (args.baseline/'inspection.tar').read_bytes()
    if sha(baseline_raw) != '87ba990d3cdbc21321f8aabfec18ea0e5549eaf985af7c4a81318ae0cc1f8ed2':
        raise ValueError('approved Apache baseline integrity')
    capture = json.loads((args.baseline/'result.json').read_bytes())
    apache = capture['apache']
    graph = json.loads((args.graph/'result.json').read_bytes())
    if (not apache['capture_complete'] or graph['sha256'] != 'f183d89b85872fe132a921043a7870731c1044cf1948bc5278fae9b4a246dbd8'
            or not graph['families'][0]['accepted'] or graph['families'][1]['accepted']):
        raise ValueError('accepted diagnostic baselines required')
    with tarfile.open(fileobj=io.BytesIO(baseline_raw), mode='r:') as archive:
        original = archive.extractfile('candidate.conf').read()
        trust = archive.extractfile('ca.pem').read()
        known_hosts = archive.extractfile('known_hosts').read()
    source = Path(__file__).resolve()
    helper = source.parents[3]/'homelab-network/Ubiquiti/munin-master-profile/qualify_dashboard.py'
    files = {'deploy_acl.py': source.read_bytes(), 'tls_probe.py': helper.read_bytes(),
             'baseline.conf': original, 'candidate.conf': (ROOT.parent/'configs/001-munin.theama.co-ssl.conf').read_bytes(),
             'ca.pem': trust, 'known_hosts': known_hosts}
    now = int(time.time())
    props = dict(x.split('=', 1) for x in apache['service_before'].strip().splitlines())
    spec = {'operation_id': 'svmf-apache-acl-20261020-v1', 'prepared_epoch': now, 'expires_epoch': now+86400,
            'hostname': 'J1-SVMF', 'boot_id': '63bb54d2-d6ea-44fb-ac15-825f10475868',
            'user': 'pi', 'host_key_alias': 'svmf.local.theama.co',
            'addresses': ['10.1.3.83', 'fd36:5aa8:6971:1:2cf5:3096:c5f:3283'],
            'target': '/etc/apache2/sites-available/001-munin.theama.co-ssl.conf',
            'paths': ['/', '/static/style-new.css', '/munin-cgi/munin-cgi-graph/J1-SVMF/J1-SVMF/apache_accesses-day.png'],
            'leaf_sha256': graph['families'][0]['observations'][0]['leaf_sha256'],
            'confirm_seconds': 90, 'worker_seconds': 150, 'guard_seconds': 180,
            'service': {k: props[k] for k in ('MainPID', 'InvocationID', 'NRestarts', 'ActiveState', 'SubState')},
            'version_sha256': sha(apache['version'].strip().encode()), 'configs': [
                {k: row[k] for k in ('path', 'resolved', 'sha256')} for row in apache['configs']],
            'baseline_sha256': sha(original), 'candidate_sha256': sha(files['candidate.conf']),
            'members': {n: sha(d) for n, d in files.items()}}
    files['spec.json'] = encoded(spec)
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w') as archive:
        for name, raw in sorted(files.items()):
            entry = tarfile.TarInfo(name)
            entry.size, entry.mode = len(raw), 0o600
            archive.addfile(entry, io.BytesIO(raw))
    raw = buffer.getvalue()
    digest = sha(raw)
    unpack(raw, digest)
    os.umask(0o077)
    args.output.mkdir(mode=0o700)
    for name, data in files.items():
        write(args.output/name, data)
    write(args.output/'deployment.tar', raw)
    write(args.output/'sealing.json', encoded({'sha256': digest, 'expires_epoch': now+86400, 'target_contact': False}))
    return {'sha256': digest, 'target_contact': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    p = sub.add_parser('seal')
    p.add_argument('--baseline', type=Path, required=True)
    p.add_argument('--graph', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    for name in ('execute', 'install'):
        p = sub.add_parser(name)
        p.add_argument('--sha256', required=True)
        if name == 'execute':
            p.add_argument('--directory', type=Path, required=True)
    for name in ('worker', 'recover', 'status', 'confirm', 'reject'):
        sub.add_parser(name).add_argument('directory', type=Path)
    args = parser.parse_args()
    if args.action == 'seal':
        result = seal(args)
    elif args.action == 'execute':
        result = execute(args.directory, args.sha256)
    elif args.action == 'install':
        result = install(sys.stdin.buffer.read(1048577), args.sha256)
    elif args.action in ('worker', 'recover'):
        result = worker(args.directory, args.action == 'recover')
    else:
        result = action(args.directory, args.action, json.load(sys.stdin) if args.action == 'confirm' else None)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
