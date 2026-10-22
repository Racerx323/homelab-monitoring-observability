#!/usr/bin/python3
"""Actual native Munin publication/recovery and real independent systemd guards."""
import base64
import importlib.util
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT/'scripts'/name)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def run(argv, allowed=(0,)):
    row = subprocess.run(argv, capture_output=True, text=True, timeout=60)
    if row.returncode not in allowed:
        raise RuntimeError(repr(argv)+'\n'+row.stdout+'\n'+row.stderr)
    return row.stdout.strip()


def unit(name):
    return dict(line.split('=', 1) for line in run(['systemctl', 'show', name,
                '--property=ActiveState,SubState,MainPID,InvocationID,NRestarts']).splitlines())


def frame(command):
    with socket.create_connection(('127.0.0.1', 4949), timeout=5) as connection:
        with connection.makefile('rb') as stream:
            assert stream.readline().startswith(b'# munin node at ')
            connection.sendall(b'cap multigraph\n')
            assert b'multigraph' in stream.readline().split()
            connection.sendall(command.encode()+b'\n')
            if command.startswith('list'):
                return stream.readline().decode().strip()
            rows = []
            for _ in range(4096):
                raw = stream.readline()
                if not raw:
                    raise RuntimeError('native frame ended')
                row = raw.decode().strip()
                if row == '.':
                    return '\n'.join(rows)
                rows.append(row)
            raise RuntimeError('native frame bound')


def crash_worker(stage, digest):
    d = load('deploy_generic.py')
    _, files = d.unpack(d.private(stage/'deployment.tar'), digest)
    tx = d.transaction(files)
    original = tx.module
    def injected(raw, name):
        obj = original(raw, name)
        if name == 'worker':
            factory = obj.make_worker
            def crash_factory(base, qualifier):
                cls = factory(base, qualifier)
                publish = cls.publish
                def kill_after_publication(self, *args, **kwargs):
                    publish(self, *args, **kwargs)
                    os.kill(os.getpid(), signal.SIGKILL)
                cls.publish = kill_after_publication
                return cls
            obj.make_worker = crash_factory
        return obj
    tx.module = injected
    tx.locked_worker(stage, digest, 'apply')
    raise AssertionError('publication crash did not happen')


def main():
    assert os.geteuid() == 0 and Path('/run/.containerenv').exists()
    assert Path('/proc/1/comm').read_text().strip() == 'systemd'
    os.umask(0o077)
    if sys.argv[1] == 'crash':
        crash_worker(Path(sys.argv[2]), sys.argv[3])
        return
    case = sys.argv[1]
    assert case in ('node-success', 'node-recover', 'node-worker-loss', 'node-foreign-link',
                    'master-success', 'master-controller-loss', 'master-foreign-file', 'master-foreign-proof', 'preflight-drift',
                    'timing-success', 'timing-recover', 'timing-worker-loss', 'timing-controller-loss',
                    'timing-foreign-file', 'timing-foreign-link', 'timing-foreign-settings', 'timing-preflight-drift')
    for filename in sys.argv[2:]:
        run(['dpkg-deb', '-x', filename, '/'])
    import pwd
    import grp
    try:
        pwd.getpwnam('munin')
    except KeyError:
        run(['groupadd', '--system', 'munin'])
        run(['useradd', '--system', '--gid', 'munin', '--no-create-home', 'munin'])
    d, base = load('deploy_generic.py'), load('install_ntp_node.py')
    wmod = load('update_generic.py')
    for path in ('/var/log/munin', '/var/lib/munin-node/plugin-state', '/usr/local/munin',
                 '/usr/local/munin/lib', '/usr/local/munin/lib/plugins'):
        Path(path).mkdir(parents=True, exist_ok=True)
        Path(path).chmod(0o755)
    run(['systemctl', 'stop', 'munin-node.service'], (0, 5))
    for path in Path('/etc/munin/plugins').iterdir():
        if path.is_symlink() or path.is_file():
            path.unlink()
    for path in Path('/etc/munin/plugin-conf.d').iterdir():
        if path.is_file():
            path.unlink()
    base.atomic(Path('/etc/munin/munin-node.conf'),
                base.node_config('j2-svntp1', ['127.0.0.1', '::1'], ['127.0.0.1', '::1']), 0o644)
    for name in ('cpu', 'load'):
        os.symlink('/usr/share/munin/plugins/'+name, Path('/etc/munin/plugins')/name)
    timing = case.startswith('timing')
    node = case.startswith('node') or case == 'preflight-drift' or timing
    role = 'timing' if timing else 'node' if node else 'expanded'
    before_settings = b'[cpu]\nuser munin\ngroup munin\n[load]\nuser munin\ngroup munin\n'
    base.atomic(Path('/etc/munin/plugin-conf.d/ntp'), before_settings, 0o644)
    before_source = (ROOT/'master/plugins/ntp_transport_j2.compatible.candidate').read_bytes()
    after_source = (ROOT/'master/plugins/ntp_transport_j2.expanded.candidate').read_bytes().replace(
        b'graph_title j2-svntp1 scheduled transport and alert submission', b'graph_title Native publication marker')
    if not node:
        base.atomic(Path('/usr/local/munin/lib/plugins/ntp_transport_j2'), before_source, 0o755)
        proof = Path('/var/lib/munin-native-commissioning-proof')
        os.link('/usr/local/munin/lib/plugins/ntp_transport_j2', proof)
        os.symlink('/usr/local/munin/lib/plugins/ntp_transport_j2', '/etc/munin/plugins/ntp_transport_j2')
        base.atomic(Path('/etc/munin/plugin-conf.d/transport'), b'[ntp_transport_j2]\nuser munin\ngroup munin\ntimeout 60\n', 0o644)
    run(['systemctl', 'daemon-reload'])
    run(['systemctl', 'enable', '--now', 'munin-node.service'])
    assert unit('munin-node.service')['ActiveState'] == 'active'
    before_unit = unit('munin-node.service')
    operation = 'munin-generic-'+role+'-20261021-v99'
    before = before_settings if node else before_source
    after = before_settings+b'[diskstats]\nuser munin\ngroup munin\n' if node else after_source
    target = '/etc/munin/plugin-conf.d/ntp' if node else '/usr/local/munin/lib/plugins/ntp_transport_j2'
    if timing:
        before=b'# original native transaction reader\n'
        after=(ROOT/'node/plugins/ntp/ntp_metrics.py').read_bytes()
        target='/usr/local/munin/lib/plugins/ntp_metrics.py'
        base.atomic(Path(target), before, 0o644)
    now = int(time.time())
    specimen = {'operation_id': operation, 'role': role, 'target': target, 'mode': 0o644 if node else 0o755,
        'hostname': socket.gethostname(), 'boot_id': Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
        'units': {'systemd-journald.service': unit('systemd-journald.service')},
        'protected': {'/etc/munin/munin-node.conf': base.sha(Path('/etc/munin/munin-node.conf').read_bytes())},
        'plugins_before': {'cpu': ['link', '/usr/share/munin/plugins/cpu'], 'load': ['link', '/usr/share/munin/plugins/load']} if node else None,
        'additions': {'diskstats': '/usr/share/munin/plugins/diskstats'} if node and not timing else {},
        'source_hashes': {'/usr/share/munin/plugins/diskstats': base.sha(Path('/usr/share/munin/plugins/diskstats').read_bytes())},
        'before_sha256': base.sha(before), 'candidate': base64.b64encode(after).decode(),
        'transport_expected': {'v4': '0', 'v6': '0', 'mail': 'U'}, 'listen_addresses': ['127.0.0.1', '::1'], 'fixture': True}
    if node:
        specimen['node_unit_layout'] = dict(line.split('=', 1) for line in run([
            'systemctl', 'show', 'munin-node.service', '--property=FragmentPath,DropInPaths']).splitlines())
    else:
        info = Path(target).stat()
        specimen.update(before_nlink=2, before_proof=str(proof), baseline_identity=[info.st_dev, info.st_ino])
    if case in ('preflight-drift', 'timing-preflight-drift'):
        specimen['before_sha256'] = '0'*64
    spec = {'operation_id': operation, 'prepared_epoch': now, 'expires_epoch': now+3600,
            'recovery_seconds': 20, 'worker': specimen, 'endpoint': 'local', 'user': 'local', 'host_key_alias': 'local',
            'qualification_sha256': d.sha(b'{}')}
    files = {n: path.read_bytes() for n, path in d.SOURCES.items()}
    files.update({n: b'' for n in d.DATA-{'spec.json', 'review.md', 'manifest.json'}})
    files.update({'expanded.py': after_source, 'settings-after': after if node else b'', 'qualification.json': b'{}'})
    if node:
        spec['worker']['candidate'] = base64.b64encode(files['settings-after']).decode()
    output = Path('/evidence/bundle')
    tx = d.transaction(files)
    tx.review, tx.MEMBERS = d.review, d.MEMBERS
    digest = tx.write_archive(output, spec, files)
    archive = (output/'deployment.tar').read_bytes()
    if case in ('node-worker-loss', 'timing-worker-loss'):
        # Actual worker publication, injected SIGKILL, then the unmodified real
        # independent timer/restorer. No fake state or successful result.
        stage = d.STAGES/operation
        d.STAGES.mkdir(mode=0o700, exist_ok=True)
        stage.mkdir(mode=0o700)
        staged = d.archive_files(archive)
        for n, raw in dict(staged, **{'deployment.tar': archive, 'lock': b''}).items():
            base.atomic(stage/n, raw)
        run(['systemd-run', '--unit', operation+'-recover', '--on-active=20s', '--timer-property=AccuracySec=1s',
             '--property=RuntimeMaxSec=180', '--collect', '/usr/bin/python3', '-I', '-B', str(stage/'runner.py'),
             'root', '--directory', str(stage), '--sha256', digest, '--action', 'recover'])
        crashed = subprocess.run(['/usr/bin/python3', '-I', '-B', str(Path(__file__)), 'crash', str(stage), digest],
                                 capture_output=True, timeout=30)
        assert crashed.returncode == -signal.SIGKILL, crashed.stderr
        assert Path(target).read_bytes() == after
    else:
        result = d.root_launch(archive, digest)
        if case in ('preflight-drift', 'timing-preflight-drift'):
            assert result['phase'] == 'preflight-failed'
            assert Path(target).read_bytes() == before
            assert unit('munin-node.service') == before_unit
            Path('/evidence/result.json').write_text(json.dumps({'passed': True, 'case': case})+'\n')
            return
        assert result['phase'] == 'prepared', result
        assert Path(target).read_bytes() == after
        if not node:
            assert unit('munin-node.service') == before_unit
            assert 'Native publication marker' in frame('config ntp_transport_j2')
        else:
            assert set(frame('list j2-svntp1').split()) == ({'cpu', 'load'} if timing else {'cpu', 'load', 'diskstats'})
        if case in ('node-success', 'master-success', 'timing-success'):
            result = d.locked_worker(d.STAGES/operation, digest, 'commit')
            assert result['phase'] == 'committed', result
            # A delayed guard cannot undo a committed transaction.
            assert d.locked_worker(d.STAGES/operation, digest, 'recover')['phase'] == 'committed'
        elif case in ('node-recover', 'timing-recover'):
            assert d.locked_worker(d.STAGES/operation, digest, 'recover')['phase'] == 'restored'
        elif case in ('node-foreign-link', 'timing-foreign-link'):
            path = Path('/etc/munin/plugins/cpu' if timing else '/etc/munin/plugins/diskstats')
            path.unlink()
            os.symlink('/usr/share/munin/plugins/load' if timing else '/usr/share/munin/plugins/cpu', path)
            result = d.locked_worker(d.STAGES/operation, digest, 'recover')
            assert result['phase'] == 'recovery-held'
            assert os.readlink(path) == ('/usr/share/munin/plugins/load' if timing else '/usr/share/munin/plugins/cpu')
            assert Path(target).read_bytes() == after
        elif case == 'master-foreign-proof':
            proof.write_bytes(before_source+b'\n# foreign proof\n')
            result = d.locked_worker(d.STAGES/operation, digest, 'recover')
            assert result['phase'] == 'recovery-held'
            assert proof.read_bytes().endswith(b'# foreign proof\n')
            assert Path(target).read_bytes() == after
        elif case in ('master-foreign-file', 'timing-foreign-file'):
            base.atomic(Path(target), after+b'\n# foreign change\n', 0o644 if timing else 0o755)
            result = d.locked_worker(d.STAGES/operation, digest, 'recover')
            assert result['phase'] == 'recovery-held'
            assert Path(target).read_bytes().endswith(b'# foreign change\n')
        elif case == 'timing-foreign-settings':
            settings=Path('/etc/munin/plugin-conf.d/ntp')
            settings.write_bytes(before_settings+b'# foreign settings\n')
            result=d.locked_worker(d.STAGES/operation, digest, 'recover')
            assert result['phase']=='recovery-held'
            assert settings.read_bytes().endswith(b'# foreign settings\n')
            assert Path(target).read_bytes()==after
    if case in ('node-worker-loss', 'master-controller-loss', 'timing-worker-loss', 'timing-controller-loss'):
        deadline = time.monotonic()+45
        state = d.STAGES/operation/'transaction/state.json'
        while time.monotonic() < deadline:
            current = json.loads(state.read_text())
            if current['phase'] == 'restored':
                break
            time.sleep(.5)
        else:
            raise AssertionError('independent guard failed: '+state.read_text())
        assert Path(target).read_bytes() == before
        assert unit('munin-node.service')['ActiveState'] == 'active'
        if node:
            assert set(frame('list j2-svntp1').split()) == {'cpu', 'load'}
    if case in ('node-recover', 'timing-recover'):
        assert Path(target).read_bytes() == before
        assert set(frame('list j2-svntp1').split()) == {'cpu', 'load'}
        stable=unit('munin-node.service')
        assert d.locked_worker(d.STAGES/operation,digest,'recover')['phase']=='restored'
        assert unit('munin-node.service')==stable
    if not node:
        assert proof.read_bytes() == before_source+(b'\n# foreign proof\n' if case == 'master-foreign-proof' else b'')
        assert proof.stat().st_nlink == 1
        assert Path(target).stat().st_ino != proof.stat().st_ino
        assert Path(target).stat().st_nlink == 1
    Path('/evidence/result.json').write_text(json.dumps({'passed': True, 'case': case,
        'node_before': before_unit, 'node_after': unit('munin-node.service'), 'archive_sha256': digest,
        'production_timing_or_hardware_accepted': False})+'\n')
    print(json.dumps({'case': case, 'passed': True}))


if __name__ == '__main__':
    main()
