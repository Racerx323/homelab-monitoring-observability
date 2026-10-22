#!/usr/bin/python3
"""Dedicated contact transaction and exact-message sender; no collection or limits."""
import base64
from email import policy
from email.parser import BytesParser
import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import signal
import smtplib
import socket
import stat
import subprocess
import time
import types

CONFIG = Path('/etc/munin/munin.conf')
HELPER = Path('/usr/local/libexec/munin-ntp-mailrise.py')
GATE = Path('/usr/local/libexec/munin-ntp-contact-gate.py')
CONTROL = Path('/var/lib/munin-ntp-contact-control')
STATUS = Path('/var/lib/munin/ntp-alerts')
STATE = Path('/var/lib/munin-ntp-contacts')
SENDS = Path('/var/lib/munin-ntp-contact-sends')
PROOF = Path('/var/lib/munin-ntp-master/munin-master-commissioning-20261021-v1/config-proof')
ENV = {'PATH': '/usr/sbin:/usr/bin:/sbin:/bin', 'LC_ALL': 'C'}
GRAPHS = {'ntp_health', 'ntp_free_bytes', 'ntp_free_inodes', 'ntp_storage_read',
          'ntp_stats_age', 'ntp_stats_read', 'ntp_job_evidence', 'ntp_job_age'}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True) + '\n').encode()


def module(raw, name):
    namespace = {'__name__': name, '__file__': '/sealed/' + name + '.py'}
    exec(compile(raw, namespace['__file__'], 'exec'), namespace)
    return types.SimpleNamespace(**namespace)


def sync(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def directives(raw):
    result = {'global': {}}
    section = 'global'
    for line in raw.decode('utf-8').splitlines():
        text = line.strip()
        if not text or text.startswith('#'):
            continue
        if text.startswith('['):
            if not re.fullmatch(r'\[[A-Za-z0-9_.-]+\]', text) or text[1:-1] in result:
                raise ValueError('unique simple host sections required')
            section = text[1:-1]
            result[section] = {}
        else:
            key, value = text.split(None, 1)
            if key in result[section]:
                raise ValueError('duplicate configuration directive')
            result[section][key] = value
    return result


def render(raw):
    before = directives(raw)
    if (any(k.startswith('contact.') for k in before['global'])
            or before.get('j2-svntp1', {}).get('contacts') != 'none'
            or before.get('J1-SVMF', {}).get('ntp_transport_j2.contacts') != 'none'):
        raise ValueError('inactive contact baseline required')
    prefix = ('contacts none\n'
              'contact.ntp_mailrise.command /usr/bin/python3 -I -B ' + str(GATE) + '\n'
              'contact.ntp_mailrise.text ${var:worst}|${var:host}|${var:plugin}|${var:wfields}|${var:cfields}|${var:ufields}\n'
              'contact.ntp_mailrise.max_messages 1\n\n')
    if 'contacts' in before['global']:
        raise ValueError('existing global contacts require a separately reviewed merge')
    text = raw.decode('utf-8')
    text, count = re.subn(r'(?m)^\[J1-SVMF\]$', lambda m: prefix + m[0], text, count=1)
    if count != 1:
        raise ValueError('one master section required')
    text, count = re.subn(r'(?m)^([ \t]*ntp_transport_j2\.contacts) none$', r'\1 ntp_mailrise', text)
    if count != 1:
        raise ValueError('one inactive master graph required')
    additions = ''.join('    ' + g + '.contacts ntp_mailrise\n' for g in sorted(GRAPHS))
    text, count = re.subn(r'(?m)^\[j2-svntp1\]\n', lambda m: m[0] + additions, text, count=1)
    if count != 1:
        raise ValueError('one canonical j2 section required')
    after = directives(text.encode())
    if (after['global'].get('contacts') != 'none'
            or after['global'].get('contact.ntp_mailrise.command') != '/usr/bin/python3 -I -B ' + str(GATE)
            or after['global'].get('contact.ntp_mailrise.max_messages') != '1'):
        raise ValueError('global inactive defaults and one-message gated command required')
    for host, values in before.items():
        for key, value in values.items():
            expected = 'ntp_mailrise' if (host, key) == ('J1-SVMF', 'ntp_transport_j2.contacts') else value
            if after[host].get(key) != expected:
                raise ValueError('unrelated configuration changed')
    selected = {(host, k[:-9]) for host, values in after.items()
                for k, value in values.items() if k.endswith('.contacts') and value == 'ntp_mailrise'}
    if selected != {('j2-svntp1', g) for g in GRAPHS} | {('J1-SVMF', 'ntp_transport_j2')}:
        raise ValueError('contact graph scope differs')
    return text.encode()


def validate_message(raw, label):
    if label not in ('problem', 'recovery') or len(raw) > 16384 or b'\n' in raw.replace(b'\r\n', b''):
        raise ValueError('bounded canonical CRLF message required')
    msg = BytesParser(policy=policy.default).parsebytes(raw)
    expected = {'From', 'To', 'Subject', 'MIME-Version', 'Content-Type',
                'Content-Transfer-Encoding', 'Date', 'Message-ID'}
    if (msg.defects or set(msg.keys()) != expected or any(len(msg.get_all(k)) != 1 for k in expected)
            or msg.is_multipart() or msg.get_content_type() != 'text/plain'):
        raise ValueError('closed plain-text message headers required')
    recipient = 'notify.failure@mailrise.xyz' if label == 'problem' else 'notify@mailrise.xyz'
    state = 'CRITICAL' if label == 'problem' else 'OK'
    if (str(msg['From']) != 'munin@local.theama.co' or str(msg['To']) != recipient
            or str(msg['Subject']) != '[DELIVERY TEST] Munin ' + state + ': j2-svntp1/ntp_health'
            or 'No production fault was induced.' not in msg.get_content()
            or 'Munin state: ' + state not in msg.get_content()):
        raise ValueError('fixed controlled test message required')
    return recipient


def make_worker(base, qualifier):
    class Installer(base.Installer):
        def __init__(self, spec, digest):
            super().__init__(spec, digest)
            self.root = STATE/spec['operation_id']
            self.artifacts = {k: base64.b64decode(v, validate=True) for k, v in spec['artifacts'].items()}
            self.state.update(changes=[], directories=[], recovery_errors=[])

        def unit(self, name):
            output = self.ctl('show', name, '--property=ActiveState,SubState,MainPID,InvocationID,NRestarts')
            return dict(line.split('=', 1) for line in output.splitlines())

        def continuity(self):
            for name, expected in self.spec['units'].items():
                if self.unit(name) != expected:
                    raise ValueError('protected service identity changed: ' + name)
            for path, digest in self.spec['protected_files'].items():
                if base.sha(base.secure(Path(path))[0]) != digest:
                    raise ValueError('protected input changed: ' + path)
            include = Path('/etc/munin/munin-conf.d')
            base.secure(CONFIG)
            for parent in (include, *include.parents):
                m = parent.lstat()
                if not stat.S_ISDIR(m.st_mode) or m.st_uid != 0 or m.st_mode & 0o022:
                    raise ValueError('unsafe include ancestry')
            names = list(include.iterdir())
            if len(names) > 64 or any(not p.name.startswith('.') and not p.name.endswith('~') for p in names):
                raise ValueError('effective include files require a new review')

        def parser(self, raw):
            row = subprocess.run(['/usr/sbin/runuser', '-u', 'munin', '--', '/usr/bin/perl', '-e', qualifier.PARSER],
                                 input=json.dumps({'candidate': [raw.decode()]}).encode(),
                                 capture_output=True, timeout=30, env=ENV)
            if row.returncode or row.stderr or not json.loads(row.stdout)['candidate']['parsed']:
                raise ValueError('native in-memory parser rejected configuration')

        def metadata(self, path, mode, uid=0, gid=0):
            m = path.lstat()
            if (not stat.S_ISREG(m.st_mode) or m.st_uid != uid or m.st_gid != gid
                    or stat.S_IMODE(m.st_mode) != mode or m.st_nlink != 1):
                raise ValueError('unsafe authored file metadata: ' + str(path))
            return [m.st_dev, m.st_ino]

        def predecessor(self):
            expected = self.spec.get('predecessor_proof')
            if expected is None:
                return None
            raw, m = base.secure(PROOF, limit=262144)
            current = CONFIG.lstat()
            same = (current.st_dev, current.st_ino) == (m.st_dev, m.st_ino)
            observed = {'device': m.st_dev, 'inode': m.st_ino, 'size': m.st_size,
                        'mtime': m.st_mtime, 'sha256': sha(raw)}
            if (observed != expected or m.st_uid != 0 or m.st_gid != 0
                    or stat.S_IMODE(m.st_mode) != 0o644 or m.st_nlink != (2 if same else 1)):
                raise ValueError('retained commissioning proof drift')
            return [m.st_dev, m.st_ino] if same else None

        def original_metadata(self):
            identity = self.predecessor()
            if identity is not None:
                return identity
            return self.metadata(CONFIG, 0o644)

        def preflight(self):
            if (os.geteuid() != 0 or os.getegid() != 0 or socket.gethostname() != self.spec['hostname']
                    or Path('/proc/sys/kernel/random/boot_id').read_text().strip() != self.spec['boot_id']):
                raise ValueError('contact root/host/boot mismatch')
            if self.spec.get('fixture'):
                if not Path('/run/.containerenv').exists() or Path('/proc/1/comm').read_text().strip() != 'systemd':
                    raise ValueError('isolated native systemd fixture required')
            elif self.spec['hostname'] != 'J1-SVMF' or self.spec.get('test_fault'):
                raise ValueError('fixed production contact target required')
            self.continuity()
            raw, _ = base.secure(CONFIG)
            if base.sha(raw) != self.spec['before_sha256']:
                raise ValueError('production main-config drift')
            self.state['before_identity'] = self.original_metadata()
            if self.spec.get('predecessor_proof') and self.predecessor() is None:
                raise ValueError('main config no longer shares the pinned proof inode')
            if render(self.artifacts['repository']) != self.artifacts['config'] or directives(raw) != directives(self.artifacts['repository']):
                raise ValueError('preserving candidate/baseline mismatch')
            for path in (HELPER, GATE, CONTROL, STATUS, self.root):
                if os.path.lexists(path):
                    raise ValueError('preexisting contact destination: ' + str(path))
            parent = STATUS.parent.lstat()
            identity = pwd.getpwnam('munin')
            if (not stat.S_ISDIR(parent.st_mode) or parent.st_uid != identity.pw_uid
                    or parent.st_gid != identity.pw_gid or parent.st_mode & 0o002):
                raise ValueError('native munin state parent metadata mismatch')
            self.state['status_parent_identity'] = [parent.st_dev, parent.st_ino, parent.st_uid, parent.st_gid, parent.st_mode]
            for path in (HELPER.parent, GATE.parent, CONTROL.parent, STATUS.parent.parent, STATE):
                while not path.exists():
                    path = path.parent
                for parent in (path, *path.parents):
                    m = parent.lstat()
                    if not stat.S_ISDIR(m.st_mode) or m.st_uid != 0 or m.st_mode & 0o022:
                        raise ValueError('unsafe contact destination ancestry')
            state_parent = STATE if STATE.exists() else STATE.parent
            if state_parent.stat().st_dev != CONFIG.parent.stat().st_dev:
                raise ValueError('recovery publication requires one filesystem')
            self.parser(self.artifacts['config'])

        def mkdir(self, path, mode, uid=0, gid=0):
            if not path.parent.exists():
                self.mkdir(path.parent, 0o755)
            path.mkdir(mode=mode)
            os.chown(path, uid, gid)
            os.chmod(path, mode)
            m = path.stat()
            self.state['directories'].append({'path': str(path), 'identity': [m.st_dev, m.st_ino], 'uid': uid, 'gid': gid, 'mode': mode})
            sync(path.parent)
            self.save()

        def publish(self, path, raw, mode, replace=False):
            temporary = path.parent/('.' + path.name + '.' + self.spec['operation_id'])
            fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
            with os.fdopen(fd, 'wb') as stream:
                os.fchmod(stream.fileno(), mode)
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
                m = os.fstat(stream.fileno())
            row = {'path': str(path), 'temporary': str(temporary), 'identity': [m.st_dev, m.st_ino], 'sha256': sha(raw), 'mode': mode}
            self.state['changes'].append(row)
            self.save()
            if replace:
                current, _ = base.secure(path)
                if sha(current) != self.spec['before_sha256'] or self.original_metadata() != self.state['before_identity']:
                    raise ValueError('late main-config drift')
                os.replace(temporary, path)
            else:
                os.link(temporary, path)
                if self.spec.get('fixture') and self.spec.get('test_fault') == 'publication-loss' and path == HELPER:
                    os.kill(os.getpid(), signal.SIGKILL)
                temporary.unlink()
            sync(path.parent)
            self.save()
            return row

        def check_row(self, row, recovery=False):
            path = Path(row['path'])
            temporary = Path(row['temporary'])
            if recovery and os.path.lexists(temporary):
                m = path.lstat()
                t = temporary.lstat()
                if (stat.S_ISREG(m.st_mode) and m.st_uid == m.st_gid == 0 and m.st_nlink == 2
                        and stat.S_IMODE(m.st_mode) == row['mode']
                        and [m.st_dev, m.st_ino] == [t.st_dev, t.st_ino] == row['identity']
                        and sha(base.secure(path)[0]) == row['sha256']):
                    return
            if self.metadata(path, row['mode']) != row['identity'] or sha(base.secure(path)[0]) != row['sha256']:
                raise ValueError('foreign authored contact file: ' + str(path))

        def file_set(self):
            self.continuity()
            self.predecessor()
            parent = STATUS.parent.lstat()
            if [parent.st_dev, parent.st_ino, parent.st_uid, parent.st_gid, parent.st_mode] != self.state['status_parent_identity']:
                raise ValueError('native munin state parent changed')
            for row in self.state['changes']:
                self.check_row(row)
            for row in self.state['directories']:
                m = Path(row['path']).lstat()
                if (not stat.S_ISDIR(m.st_mode) or [m.st_dev, m.st_ino] != row['identity']
                        or m.st_uid != row['uid'] or m.st_gid != row['gid'] or stat.S_IMODE(m.st_mode) != row['mode']):
                    raise ValueError('foreign contact state directory')

        def checkpoint(self, phase):
            self.state['phase'] = phase
            self.continuity()
            self.save()
            if self.spec.get('fixture') and phase == 'configured':
                if self.spec.get('test_fault') == 'failure':
                    raise ValueError('qualified configured rejection')
                if self.spec.get('test_fault') == 'worker-loss':
                    os.kill(os.getpid(), signal.SIGKILL)

        def install(self):
            self.preflight()
            if not STATE.exists():
                STATE.mkdir(mode=0o700)
                sync(STATE.parent)
            self.root.mkdir(mode=0o700)
            sync(STATE)
            self.owns_root = True
            self.save()
            base.atomic(self.root/'config.before', base.secure(CONFIG)[0])
            self.checkpoint('backed-up')
            self.mkdir(CONTROL, 0o755)
            self.publish(CONTROL/'lock', b'', 0o644)
            identity = pwd.getpwnam('munin')
            self.mkdir(STATUS, 0o700, identity.pw_uid, identity.pw_gid)
            if not HELPER.parent.exists():
                self.mkdir(HELPER.parent, 0o755)
            self.publish(HELPER, self.artifacts['helper'], 0o755)
            self.publish(GATE, self.artifacts['gate'], 0o755)
            self.publish(CONFIG, self.artifacts['config'], 0o644, replace=True)
            self.checkpoint('configured')
            self.file_set()
            self.parser(base.secure(CONFIG)[0])
            if os.path.lexists(CONTROL/'enabled.json'):
                raise ValueError('contact gate unexpectedly enabled before commit')
            self.checkpoint('prepared')

        def commit(self):
            if self.state.get('phase') != 'prepared':
                raise ValueError('prepared contact stage required; commit cannot replay')
            self.file_set()
            gate = module(self.artifacts['gate'], 'contact_gate')
            fd = gate.lock(exclusive=True)
            try:
                if os.path.lexists(CONTROL/'enabled.json'):
                    raise ValueError('foreign enable marker')
                if os.path.lexists(STATUS/'suppressed.json'):
                    raise ValueError('actual pre-commit contact suppressed; inspect transition evidence before activation')
                # Irreversible decision precedes the first possible send. A lost
                # committer here stays disabled/held; the timer must not undo it.
                self.state.update(phase='committed', accepted=False, enable_pending=True)
                self.save()
                if self.spec.get('fixture') and self.spec.get('test_fault') == 'commit-loss':
                    os.kill(os.getpid(), signal.SIGKILL)
                token = {'operation_id': self.spec['operation_id'], 'worker_sha256': self.digest,
                         'config_sha256': sha(self.artifacts['config']), 'helper_sha256': sha(self.artifacts['helper']),
                         'gate_sha256': sha(self.artifacts['gate'])}
                self.publish(CONTROL/'enabled.json', encoded(token), 0o644)
                self.file_set()
                gate.enabled()
                self.state.update(accepted=True, enable_pending=False, enabled_epoch=time.time())
                self.save()
            finally:
                os.close(fd)
            return self.state

        def recover(self):
            if self.state.get('phase') in ('committed', 'restored'):
                return self.state
            errors = []
            try:
                self.continuity()
                self.predecessor()
                if os.path.lexists(CONTROL/'enabled.json'):
                    raise ValueError('unexpected uncommitted enable marker; preserve foreign state')
                current, _ = base.secure(CONFIG)
                config_rows = [r for r in self.state['changes'] if r['path'] == str(CONFIG)]
                if sha(current) == self.spec['candidate_sha256'] and config_rows:
                    self.check_row(config_rows[-1])
                    backup = base.secure(self.root/'config.before')[0]
                    if sha(backup) != self.spec['before_sha256']:
                        raise ValueError('contact backup drift')
                    restoration = self.root/'config.restoration'
                    if not restoration.exists():
                        base.atomic(restoration, backup, 0o644)
                    m = restoration.lstat()
                    if sha(base.secure(restoration)[0]) != self.spec['before_sha256']:
                        raise ValueError('restoration input drift')
                    self.state['restored_identity'] = [m.st_dev, m.st_ino]
                    self.save()
                    os.replace(restoration, CONFIG)
                    sync(CONFIG.parent)
                    sync(self.root)
                elif sha(current) != self.spec['before_sha256'] or self.original_metadata() not in (self.state['before_identity'], self.state.get('restored_identity')):
                    raise ValueError('foreign main-config; restoration held')
                for row in reversed(self.state['changes']):
                    if row['path'] == str(CONFIG):
                        temporary = Path(row['temporary'])
                        if os.path.lexists(temporary):
                            if ([temporary.stat().st_dev, temporary.stat().st_ino] != row['identity']
                                    or sha(base.secure(temporary)[0]) != row['sha256']):
                                raise ValueError('foreign main publication')
                            temporary.unlink()
                            sync(temporary.parent)
                        continue
                    path = Path(row['path'])
                    if os.path.lexists(path):
                        self.check_row(row, recovery=True)
                        path.unlink()
                        sync(path.parent)
                    temporary = Path(row['temporary'])
                    if os.path.lexists(temporary):
                        if [temporary.stat().st_dev, temporary.stat().st_ino] != row['identity'] or sha(base.secure(temporary)[0]) != row['sha256']:
                            raise ValueError('foreign contact publication')
                        temporary.unlink()
                        sync(temporary.parent)
                for row in reversed(self.state['directories']):
                    path = Path(row['path'])
                    if not path.exists():
                        continue
                    m = path.lstat()
                    if (not stat.S_ISDIR(m.st_mode) or [m.st_dev, m.st_ino] != row['identity']
                            or m.st_uid != row['uid'] or m.st_gid != row['gid'] or stat.S_IMODE(m.st_mode) != row['mode']):
                        raise ValueError('foreign state directory; restoration held')
                    if any(path.iterdir()):
                        if path == STATUS:
                            continue  # Genuine submission evidence is never deleted.
                        raise ValueError('nonempty authored contact directory')
                    path.rmdir()
                    sync(path.parent)
                self.parser(base.secure(CONFIG)[0])
                self.predecessor()
                self.continuity()
            except BaseException as error:
                errors.append(str(error))
            self.state.update(accepted=False, phase='recovery-held' if errors else 'restored',
                              recovery='held' if errors else 'restored', recovery_errors=errors)
            self.save()
            return self.state

    return Installer


def send_exact(spec, digest, files, base):
    """Root preflight, durable receipt, permanent munin UID drop, one SMTP attempt."""
    worker = spec['worker']
    if (os.geteuid() != 0 or os.getegid() != 0 or socket.gethostname() != worker['hostname']
            or Path('/proc/sys/kernel/random/boot_id').read_text().strip() != worker['boot_id']):
        raise ValueError('send root/host/boot mismatch')
    if worker.get('fixture') and not Path('/run/.containerenv').exists():
        raise ValueError('fixture send requires isolated container')
    if not worker.get('fixture') and worker['hostname'] != 'J1-SVMF':
        raise ValueError('fixed production send target required')
    for name, expected in worker['units'].items():
        row = subprocess.run(['/usr/bin/systemctl', 'show', name,
            '--property=ActiveState,SubState,MainPID,InvocationID,NRestarts'],
            capture_output=True, text=True, timeout=15, env=ENV)
        if row.returncode or dict(line.split('=', 1) for line in row.stdout.splitlines()) != expected:
            raise ValueError('send service continuity changed')
    for path, expected in worker['protected_files'].items():
        if sha(base.secure(Path(path))[0]) != expected:
            raise ValueError('send protected input changed')
    gate = module(files['gate.py'], 'contact_gate')
    fd = gate.lock(exclusive=True)
    try:
        token = gate.enabled()
        prerequisite = spec['activation_prerequisite']
        state = json.loads(base.secure(STATE/prerequisite['operation_id']/'state.json')[0])
        if (not state.get('accepted') or state.get('phase') != 'committed'
                or state.get('enable_pending') or state['spec_sha256'] != token['worker_sha256']
                or token['worker_sha256'] != prerequisite['worker_sha256']
                or token['operation_id'] != prerequisite['operation_id']
                or token['config_sha256'] != prerequisite['config_sha256']
                or token['helper_sha256'] != sha(files['mailrise.py']) or token['gate_sha256'] != sha(files['gate.py'])):
            raise ValueError('accepted enabled activation prerequisite required')
        raw = files['message.eml']
        recipient = validate_message(raw, spec['message_label'])
        if sha(raw) != spec['message_sha256']:
            raise ValueError('exact message drift')
        if not SENDS.exists():
            SENDS.mkdir(mode=0o700)
            sync(SENDS.parent)
        base.secure(STATE/prerequisite['operation_id']/'state.json')
        for parent in (SENDS, *SENDS.parents):
            m = parent.lstat()
            if not stat.S_ISDIR(m.st_mode) or m.st_uid != 0 or m.st_mode & 0o022:
                raise ValueError('unsafe remote send receipt ancestry')
        receipt = SENDS/spec['operation_id']
        receipt.mkdir(mode=0o700)
        sync(SENDS)
        base.atomic(receipt/'receipt.json', encoded({'archive_sha256': digest, 'message_sha256': sha(raw), 'attempt_epoch': time.time()}))
        identity = pwd.getpwnam('munin')
        os.setgroups([])
        os.setgid(identity.pw_gid)
        os.setuid(identity.pw_uid)
        helper = module(files['mailrise.py'], 'contact_helper')
        result = {'attempted': True, 'message_sha256': sha(raw), 'submission_accepted': False,
                  'status_recorded': False, 'delivery_accepted': False}
        try:
            with smtplib.SMTP('127.0.0.1', 8025, timeout=10) as smtp:
                if smtp.sendmail('munin@local.theama.co', [recipient], raw):
                    raise ValueError('Mailrise recipient refusal')
            result['submission_accepted'] = True
        except Exception as error:
            result.update(error=str(error), submission_uncertain=True)
        try:
            helper.save_status(result['submission_accepted'])
            result['status_recorded'] = True
        except Exception as error:
            result['status_error'] = str(error)
        return result
    finally:
        os.close(fd)
