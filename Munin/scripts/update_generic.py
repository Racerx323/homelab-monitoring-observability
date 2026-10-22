#!/usr/bin/python3
"""Guarded updates of an existing node profile or existing transport source."""
import base64
import json
import os
from pathlib import Path
import socket
import stat
import time

CONFIG = Path('/etc/munin/munin-node.conf')  # Stable inspection anchor on either host.
STAGES = Path('/var/lib/munin-generic-stages')


def make_worker(base, _qualifier):
    class Update(base.Installer):
        def __init__(self, spec, digest):
            super().__init__(spec, digest)
            self.root = STAGES/spec['operation_id']/'transaction'
            self.owns_root = False
            self.target = Path(spec['target'])
            self.candidate = base64.b64decode(spec['candidate'], validate=True)
            self.state.update(links={}, recovery_errors=[])

        def identity(self):
            if (os.geteuid() != 0 or os.getegid() != 0 or socket.gethostname() != self.spec['hostname']
                    or Path('/proc/sys/kernel/random/boot_id').read_text().strip() != self.spec['boot_id']):
                raise ValueError('update root/host/boot mismatch')
            if self.spec.get('fixture'):
                if not Path('/run/.containerenv').exists() or Path('/proc/1/comm').read_text().strip() != 'systemd':
                    raise ValueError('fixture requires real isolated systemd')

        def unit(self, name='munin-node.service'):
            output = self.ctl('show', name, '--property=ActiveState,SubState,MainPID,InvocationID,NRestarts')
            return dict(line.split('=', 1) for line in output.splitlines())

        def continuity(self):
            self.identity()
            if self.spec['role'] in ('node', 'timing'):
                raw = self.ctl('show', 'munin-node.service', '--property=FragmentPath,DropInPaths')
                layout = dict(line.split('=', 1) for line in raw.splitlines())
                expected = self.spec['node_unit_layout']
                if (layout.get('DropInPaths') != expected['DropInPaths']
                        or Path(layout['FragmentPath']).resolve(strict=True) != Path(expected['FragmentPath']).resolve(strict=True)):
                    raise ValueError('effective node unit/drop-ins changed')
            for name, expected in self.spec['units'].items():
                if self.unit(name) != expected:
                    raise ValueError('protected service changed: '+name)
            for path, digest in self.spec['protected'].items():
                if base.sha(base.secure(Path(path))[0]) != digest:
                    raise ValueError('protected input changed: '+path)
            if self.state.get('phase') in ('prepared', 'committed'):
                if not self.file_matches(self.target, base.sha(self.candidate), self.state['after_identity']):
                    raise ValueError('authored target changed')
                self.links_valid(self.spec['role'] in ('node', 'timing'))
                if self.settings_inventory() != self.state['settings_before']:
                    raise ValueError('unrelated settings changed')

        def inventory(self):
            result = {}
            directory = Path('/etc/munin/plugins')
            for parent in (directory, *directory.parents):
                m = parent.lstat()
                if not stat.S_ISDIR(m.st_mode) or m.st_uid != 0 or m.st_mode & 0o022:
                    raise ValueError('unsafe plugin directory')
            entries = list(directory.iterdir())
            if len(entries) > 512:
                raise ValueError('plugin inventory bound')
            for path in entries:
                if path.name.startswith('.'):
                    continue
                m = path.lstat()
                if m.st_uid != 0:
                    raise ValueError('plugin owner changed')
                result[path.name] = ('link', os.readlink(path)) if path.is_symlink() else ('file', base.sha(base.secure(path)[0]))
            return {n: list(v) for n, v in result.items()}

        def settings_inventory(self):
            result = {}
            for path in Path('/etc/munin/plugin-conf.d').iterdir():
                if len(result) > 64:
                    raise ValueError('settings bound')
                if path == self.target:
                    continue
                raw, m = base.secure(path, 65536)
                result[path.name] = [base.sha(raw), m.st_uid, m.st_gid, stat.S_IMODE(m.st_mode)]
            return result

        @staticmethod
        def fid(m):
            return [m.st_dev, m.st_ino]

        def file_matches(self, path, digest, identity):
            raw, m = base.secure(path)
            links = self.spec.get('before_nlink', 1) if identity == self.state.get('before_identity') else 1
            return (base.sha(raw) == digest and self.fid(m) == identity
                    and m.st_uid == 0 and m.st_gid == 0 and m.st_nlink == links
                    and stat.S_IMODE(m.st_mode) == self.spec['mode'])

        def retained_proof(self, target_info=None):
            if 'before_proof' not in self.spec:
                if self.spec.get('before_nlink', 1) != 1:
                    raise ValueError('shared baseline requires retained commissioning proof')
                return
            raw, info = base.secure(Path(self.spec['before_proof']))
            original = self.fid(target_info) if target_info is not None else self.state['before_identity']
            current = target_info if target_info is not None else base.secure(self.target)[1]
            links = self.spec['before_nlink'] if self.fid(current) == original else 1
            if (base.sha(raw) != self.spec['before_sha256'] or self.fid(info) != original
                    or info.st_nlink != links or info.st_uid != 0 or info.st_gid != 0
                    or stat.S_IMODE(info.st_mode) != self.spec['mode']):
                raise ValueError('retained commissioning proof changed')

        def publish(self, raw, key, expected_hash, expected_identity):
            """Record the temporary inode before atomic publication, including recovery."""
            temporary = self.target.parent/('.'+self.spec['operation_id']+'.'+key)
            digest = base.sha(raw)
            if key in self.state:
                intent = self.state[key]
                if self.file_matches(self.target, digest, intent):
                    return
                if not self.file_matches(temporary, digest, intent):
                    raise ValueError('publication temporary changed')
            else:
                fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, self.spec['mode'])
                with os.fdopen(fd, 'wb') as stream:
                    stream.write(raw)
                    stream.flush()
                    os.fchown(stream.fileno(), 0, 0)
                    os.fchmod(stream.fileno(), self.spec['mode'])
                    os.fsync(stream.fileno())
                    self.state[key] = self.fid(os.fstat(stream.fileno()))
                self.save()
            if not self.file_matches(self.target, expected_hash, expected_identity):
                raise ValueError('late target identity drift')
            os.replace(temporary, self.target)
            self.sync(self.target.parent)

        @staticmethod
        def sync(path):
            fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)

        def links_valid(self, expanded):
            expected = dict(self.state.get('plugins_before') or self.spec['plugins_before'])
            if expanded:
                expected.update({n: ['link', p] for n, p in self.spec['additions'].items()})
            if self.inventory() != expected:
                raise ValueError('exact plugin selection mismatch')

        def preflight(self):
            self.continuity()
            if self.root.exists() or self.root.is_symlink():
                raise ValueError('consumed update')
            raw, m = base.secure(self.target)
            if (base.sha(raw) != self.spec['before_sha256'] or stat.S_IMODE(m.st_mode) != self.spec['mode']
                    or m.st_uid != 0 or m.st_gid != 0 or m.st_nlink != self.spec.get('before_nlink', 1)):
                raise ValueError('update target baseline changed')
            self.retained_proof(m)
            if 'baseline_identity' in self.spec and self.fid(m) != self.spec['baseline_identity']:
                raise ValueError('inspected baseline inode changed')
            if self.unit()['ActiveState'] != 'active' or self.unit()['SubState'] != 'running':
                raise ValueError('existing node must be running')
            if self.spec['role'] not in ('node', 'timing'):
                self.state['plugins_before'] = self.inventory()
                if self.state['plugins_before'].get('ntp_transport_j2') != ['link', str(self.target)]:
                    raise ValueError('master transport link changed')
            self.links_valid(False)
            self.state.update(before_identity=self.fid(m), node_before=self.unit(),
                              settings_before=self.settings_inventory())
            if self.spec['role'] in ('node', 'timing') and self.ctl('is-enabled', 'munin-node.service').strip() != 'enabled':
                raise ValueError('node is not persistently enabled')
            for name, target in self.spec['additions'].items():
                if os.path.lexists(Path('/etc/munin/plugins')/name):
                    raise ValueError('addition already exists')
                if base.sha(base.secure(Path(target))[0]) != self.spec['source_hashes'][target]:
                    raise ValueError('package plugin source changed')
            return raw

        def add_links(self):
            directory = Path('/etc/munin/plugins')
            for name, target in self.spec['additions'].items():
                temporary = directory/('.'+self.spec['operation_id']+'-'+name)
                os.symlink(target, temporary)
                self.state['links'][name] = self.fid(temporary.lstat())
                self.save()
                os.link(temporary, directory/name, follow_symlinks=False)
                temporary.unlink()
                self.sync(directory)

        def validate(self):
            self.continuity()
            self.retained_proof()
            self.links_valid(self.spec['role'] in ('node', 'timing'))
            if self.settings_inventory() != self.state['settings_before']:
                raise ValueError('unrelated settings changed')
            if not self.file_matches(self.target, base.sha(self.candidate), self.state['after_identity']):
                raise ValueError('authored target changed')
            if self.unit()['ActiveState'] != 'active' or self.unit()['SubState'] != 'running':
                raise ValueError('node is not running')
            if self.spec['role'] not in ('node', 'timing') and self.unit() != self.state['node_before']:
                raise ValueError('master node identity changed')

        def local_check(self):
            if self.spec['role'] in ('node', 'timing'):
                # Warm source-bound TCP fetches, not a CLI state copy, are checked
                # by the controller before commit. Verify active serving here.
                raw = self.command(['/usr/bin/ss', '-H', '-lnt', 'sport = :4949'])
                for address in self.spec['listen_addresses']:
                    if address+':4949' not in raw and '['+address+']:4949' not in raw:
                        raise ValueError('node listener missing')
            else:
                for args in (['ntp_transport_j2', 'config'], ['ntp_transport_j2']):
                    output = self.command(['/usr/sbin/munin-run', *args])
                    if len(args) == 2:
                        if 'graph_title ' not in output:
                            raise ValueError('transport configuration missing')
                    elif dict(line.split('.value ', 1) for line in output.splitlines()) != self.spec['transport_expected']:
                        raise ValueError('transport acceptance failed')

        def install(self):
            before = self.preflight()
            self.root.mkdir(mode=0o700)
            self.owns_root = True
            base.atomic(self.root/'before', before)
            self.state.update(phase='backup', installed_epoch=time.time())
            self.save()
            if self.spec['role'] in ('node', 'timing'):
                self.state['stop_intent'] = True
                self.save()
                self.ctl('stop', 'munin-node.service')
                self.add_links()
            self.publish(self.candidate, 'after_identity', self.spec['before_sha256'], self.state['before_identity'])
            if self.spec['role'] in ('node', 'timing'):
                self.ctl('start', 'munin-node.service')
            self.validate()
            self.local_check()
            self.state.update(phase='prepared', prepared_epoch=time.time())
            self.save()
            return self.state

        def commit(self):
            if self.state['phase'] != 'prepared' or time.time()-self.state['prepared_epoch'] > 480:
                raise ValueError('not a fresh prepared update')
            self.validate()
            self.local_check()
            self.state.update(phase='committed', accepted=True)
            self.save()

        def recover(self):
            self.identity()
            if self.state.get('phase') in ('committed', 'restored'):
                return self.state
            errors = []
            try:
                self.continuity()
                self.retained_proof()
                before = base.secure(self.root/'before')[0]
                if base.sha(before) != self.spec['before_sha256']:
                    raise ValueError('backup changed')
                restoring = self.state.get('restore_identity', self.state['before_identity'])
                restored = self.file_matches(self.target, self.spec['before_sha256'], restoring)
                if not restored and not self.file_matches(self.target, base.sha(self.candidate), self.state.get('after_identity')):
                    raise ValueError('foreign target preserved')
                # Prove all current links before stopping/restoring anything.
                for name, identity in self.state['links'].items():
                    path = Path('/etc/munin/plugins')/name
                    if os.path.lexists(path) and (not path.is_symlink() or self.fid(path.lstat()) != identity
                                                  or os.readlink(path) != self.spec['additions'][name]):
                        raise ValueError('foreign link preserved: '+name)
                self.state['phase'] = 'restoring'
                self.save()
                if self.spec['role'] in ('node', 'timing') and self.state.get('stop_intent'):
                    self.ctl('stop', 'munin-node.service')
                if not restored:
                    self.publish(before, 'restore_identity', base.sha(self.candidate), self.state['after_identity'])
                for name, identity in self.state['links'].items():
                    for path in (Path('/etc/munin/plugins')/name,
                                 Path('/etc/munin/plugins')/('.'+self.spec['operation_id']+'-'+name)):
                        if os.path.lexists(path):
                            if not path.is_symlink() or self.fid(path.lstat()) != identity or os.readlink(path) != self.spec['additions'][name]:
                                raise ValueError('foreign temporary link preserved')
                            path.unlink()
                for key in ('after_identity', 'restore_identity'):
                    temporary = self.target.parent/('.'+self.spec['operation_id']+'.'+key)
                    if os.path.lexists(temporary):
                        digest = base.sha(self.candidate) if key == 'after_identity' else self.spec['before_sha256']
                        if not self.file_matches(temporary, digest, self.state.get(key)):
                            raise ValueError('foreign publication temporary preserved')
                        temporary.unlink()
                self.sync(self.target.parent)
                self.sync(Path('/etc/munin/plugins'))
                self.links_valid(False)
                if self.settings_inventory() != self.state['settings_before']:
                    raise ValueError('unrelated settings changed during recovery')
                if self.spec['role'] in ('node', 'timing') and self.state.get('stop_intent'):
                    self.ctl('start', 'munin-node.service')
                if self.unit()['ActiveState'] != 'active' or self.unit()['SubState'] != 'running':
                    raise ValueError('original node not running')
                if self.spec['role'] not in ('node', 'timing'):
                    self.local_check()
                self.continuity()
            except Exception as error:
                errors.append(str(error))
            self.state.update(accepted=False, phase='recovery-held' if errors else 'restored',
                              recovery='held' if errors else 'restored', recovery_errors=errors)
            self.save()
            return self.state
    return Update
