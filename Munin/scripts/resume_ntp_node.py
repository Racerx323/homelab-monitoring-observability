#!/usr/bin/python3
"""One-file correction and guarded startup; never reinstall or replay first install."""
import json
import os
from pathlib import Path
import socket
import stat

METRICS = 'node/plugins/ntp/ntp_metrics.py'
TARGET = Path('/usr/local/munin/lib/plugins/ntp_metrics.py')


def make_worker(base):
    class Installer(base.Installer):
        def __init__(self, spec, digest):
            super().__init__(spec['installation'], digest)
            self.resume = spec
            # Retain the original guard/permit relationship, with separate state.
            self.root = Path(spec['state_root'])
            self.proof = self.root/'permit-proof'
            self.final = base.node_config(self.spec['hostname'], self.spec['listen_addresses'], self.spec['allow_addresses'])
            self.artifacts = {}

        def load_artifacts(self):
            for name, expected in self.resume['artifacts'].items():
                raw = base.secure(Path(self.resume['input_root'])/name)[0]
                if base.sha(raw) != expected:
                    raise ValueError('resume input drift')
                self.artifacts[name] = raw

        def unit(self):
            raw = self.ctl('show', 'munin-node.service', '--property=ActiveState,SubState,UnitFileState')
            return dict(line.split('=', 1) for line in raw.splitlines())

        def contained(self):
            if self.unit() != {'ActiveState': 'inactive', 'SubState': 'dead', 'UnitFileState': 'disabled'}:
                raise ValueError('node no longer contained')
            if os.path.lexists(self.permit) or self.command(['/usr/bin/ss', '-H', '-lnt', 'sport = :4949']).strip():
                raise ValueError('unexpected permit/listener')

        def original_state(self):
            raw = base.secure(Path(self.resume['original_state_path']))[0]
            state = json.loads(raw)
            if (base.sha(raw) != self.resume['original_state_sha256'] or state.get('accepted') is not False
                    or state.get('recovery') != 'contained' or state.get('recovery_errors')
                    or state.get('spec_sha256') != self.resume['original_spec_sha256']):
                raise ValueError('original consumed state drift')

        def preflight(self):
            if (os.geteuid() != 0 or os.getegid() != 0 or socket.gethostname() != self.spec['hostname']
                    or Path('/proc/sys/kernel/random/boot_id').read_text().strip() != self.spec['boot_id']):
                raise ValueError('resume root/host/boot mismatch')
            self.continuity(); self.contained(); self.original_state()
            self.load_artifacts()
            if os.path.lexists(base.POLICY):
                raise ValueError('unexpected package policy; no overwrite')
            if self.command(['/usr/bin/dpkg', '--audit']).strip():
                raise ValueError('package audit not clean')
            wanted = {row['package']: row for row in self.spec['packages']}
            raw = self.command(['/usr/bin/dpkg-query', '-W', '-f=${binary:Package}\t${Version}\t${Architecture}\t${Status}\n', *sorted(wanted)])
            observed = {}
            for line in raw.splitlines():
                name, version, arch, status = line.split('\t')
                name = name.split(':', 1)[0]
                if name in observed or name not in wanted or status != 'install ok installed':
                    raise ValueError('node package state drift')
                observed[name] = (version, arch)
            if observed != {name: (row['version'], row['architecture']) for name, row in wanted.items()}:
                raise ValueError('pinned node package versions changed')
            # Observation only: the old pre-install inventory pin is not reused.
            self.command(['/usr/bin/dpkg-query', '-W', '-f=${binary:Package}\t${Version}\t${Architecture}\t${db:Status-Abbrev}\n'])
            old = base.secure(TARGET)[0]
            if base.sha(old) != self.resume['before_sha256']:
                raise ValueError('classifier before hash changed')
            candidate = self.artifacts[METRICS]
            self.artifacts[METRICS] = old
            try:
                self.validate_installed()
            finally:
                self.artifacts[METRICS] = candidate
            if self.root.exists() or self.root.is_symlink():
                raise ValueError('resume already exists')
            for parent in self.root.parents:
                if parent.exists():
                    info = parent.lstat()
                    if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
                        raise ValueError('unsafe resume ancestor')

        def verify_local(self):
            for name in (*base.PACKAGE_PLUGINS, *base.CUSTOM_PLUGINS):
                for arguments in ([name, 'config'], [name]):
                    output = self.command(['/usr/sbin/munin-run', *arguments])
                    if ('graph_title ' if len(arguments) == 2 else '.value ') not in output:
                        raise ValueError('installed plugin output invalid: '+name)
                    if name == 'ntp_health' and len(arguments) == 1:
                        for field in ('query_ok', 'synced', 'pps_selected'):
                            if field+'.value 1' not in output.splitlines():
                                raise ValueError('live health assertion failed: '+field)

        def install(self):
            self.preflight()
            self.root.parent.mkdir(mode=0o700, exist_ok=True)
            self.root.mkdir(mode=0o700); self.owns_root = True; self.save()
            base.atomic(self.root/'metrics.before', base.secure(TARGET)[0])
            self.state['patch_intent'] = True; self.save()
            if base.sha(base.secure(TARGET)[0]) != self.resume['before_sha256']:
                raise ValueError('late classifier drift')
            base.atomic(TARGET, self.artifacts[METRICS], 0o644)
            self.validate_installed(); self.continuity(); self.contained(); self.verify_local()
            base.atomic(self.proof, b'')
            proof_info = self.proof.stat()
            self.state.update(permit_intent=True, permit_identity=[proof_info.st_dev, proof_info.st_ino])
            self.save()
            # Atomic no-clobber publication; the private proof identifies our inode
            # even if interrupted before the next state write.
            os.link(self.proof, self.permit, follow_symlinks=False)
            directory = os.open(self.permit.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            try: os.fsync(directory)
            finally: os.close(directory)
            self.ctl('enable', 'munin-node.service'); self.ctl('start', 'munin-node.service')
            if self.unit() != {'ActiveState': 'active', 'SubState': 'running', 'UnitFileState': 'enabled'}:
                raise ValueError('resumed unit state invalid')
            listeners = self.command(['/usr/bin/ss', '-H', '-lnt', 'sport = :4949'])
            for address in self.spec['listen_addresses']:
                if address+':4949' not in listeners and '['+address+']:4949' not in listeners:
                    raise ValueError('resumed listener absent: '+address)
            if any(token in listeners for token in ('0.0.0.0:4949', '*:4949', '[::]:4949')):
                raise ValueError('resumed wildcard listener')
            self.verify_local(); self.validate_installed(); self.continuity(); self.original_state()
            self.state.update(accepted=True, phase='node-resumed', polling_accepted=False, delivery_accepted=False)
            self.save(); return self.state

        def recover(self):
            if (os.geteuid() != 0 or socket.gethostname() != self.spec['hostname']
                    or Path('/proc/sys/kernel/random/boot_id').read_text().strip() != self.spec['boot_id']):
                raise ValueError('recovery host/boot drift')
            errors = []
            self.load_artifacts()
            try:
                if os.path.lexists(self.permit):
                    if (not self.state.get('permit_intent') or self.permit.is_symlink() or self.proof.is_symlink()
                            or not self.proof.exists() or base.secure(self.proof)[0]
                            or self.state.get('permit_identity') != [self.proof.stat().st_dev, self.proof.stat().st_ino]
                            or not os.path.samefile(self.permit, self.proof) or base.secure(self.permit)[0]):
                        raise ValueError('foreign permit preserved')
                    self.permit.unlink()
                    directory = os.open(self.permit.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
                    try: os.fsync(directory)
                    finally: os.close(directory)
            except Exception as error: errors.append(str(error))
            try:
                self.ctl('stop', 'munin-node.service', allowed=(0, 5))
                self.ctl('disable', 'munin-node.service', allowed=(0, 1, 5))
            except Exception: errors.append('service containment failed')
            try:
                actual = base.sha(base.secure(TARGET)[0])
                if actual == self.resume['artifacts'][METRICS] and self.state.get('patch_intent'):
                    old = base.secure(self.root/'metrics.before')[0]
                    if base.sha(old) != self.resume['before_sha256']:
                        raise ValueError('backup changed')
                    base.atomic(TARGET, old, 0o644)
                elif actual != self.resume['before_sha256']:
                    raise ValueError('foreign classifier preserved')
                self.artifacts[METRICS] = base.secure(TARGET)[0]
                self.validate_installed(); self.contained(); self.continuity(); self.original_state()
            except Exception as error: errors.append(str(error))
            self.state.update(accepted=False, recovery='held' if errors else 'contained', recovery_errors=errors)
            self.save(); return self.state
    return Installer
