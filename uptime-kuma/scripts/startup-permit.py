#!/usr/bin/env python3
"""Keep existing start guards effective across one pending deployment reboot."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import time

ROOT = Path('/var/lib/uptime-kuma-maintenance/remaining-deployment')
PERMIT = Path('/run/uptime-kuma-network-diagnostic/permit')
UNITS = ['uptime-kuma.service', 'uptime-kuma-network.service',
         'uptime-kuma-loopback.socket', 'uptime-kuma-loopback.service', 'webmin.service']
TIMER = 'uptime-kuma-deployment-containment.timer'


def regular(path, mode):
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('symlink in startup authority')
    s = path.stat()
    if not stat.S_ISREG(s.st_mode) or s.st_uid != 0 or stat.S_IMODE(s.st_mode) != mode:
        raise ValueError('unprotected startup authority')


def save(state):
    target = ROOT / 'state.json'
    temporary = ROOT / 'state.new'
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as stream:
        json.dump(state, stream)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, target)
    fd = os.open(ROOT, os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def pending(state, now, margin=0):
    if state['status'] != 'pending' or not state['armed_at'] <= now < state['deadline'] - margin:
        raise ValueError('startup authority expired, contained or clock moved backward')


def action(mode, predecessor_sha256=None, original_predecessor_sha256=None):
    if os.geteuid() != 0:
        raise ValueError('root required')
    if any(p.is_symlink() for p in (ROOT, *ROOT.parents)):
        raise ValueError('symlink in startup directory')
    info = ROOT.stat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or stat.S_IMODE(info.st_mode) != 0o700:
        raise ValueError('startup directory must be root 0700')
    fd = os.open(ROOT / 'lock', os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        path = ROOT / 'state.json'
        if mode in ('grant', 'check', 'accept') and (ROOT / 'contained').exists():
            raise ValueError('startup authority contained')
        now = int(time.time())
        boot = Path('/proc/sys/kernel/random/boot_id').read_text().strip()
        if mode == 'arm':
            if path.exists() or path.is_symlink():
                raise ValueError('operation already armed; no replay')
            state = dict(status='pending', armed_at=now, deadline=now + 2400,
                         boot_id=boot, reboot_count=0)
            save(state)
        else:
            regular(path, 0o600)
            state = json.loads(path.read_text())
            if mode in ('resume', 'resume-successor'):
                regular(ROOT / 'contained', 0o600)
                if (not predecessor_sha256 or hashlib.sha256(path.read_bytes()).hexdigest() != predecessor_sha256
                        or state['status'] != 'contained' or state['reboot_count'] != 1
                        or state['boot_id'] != boot or (ROOT / 'accepted').exists()):
                    raise ValueError('contained predecessor or accepted reboot differs')
                previous = ROOT / 'previous-state.json'
                if mode == 'resume-successor':
                    regular(previous, 0o600)
                    if (not original_predecessor_sha256
                            or hashlib.sha256(previous.read_bytes()).hexdigest() != original_predecessor_sha256
                            or state.get('predecessor_sha256') != original_predecessor_sha256
                            or 'original_predecessor_sha256' in state):
                        raise ValueError('original predecessor differs or successor already consumed')
                    previous = ROOT / 'completion-state.json'
                fd = os.open(previous, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
                with os.fdopen(fd, 'wb') as out:
                    out.write(path.read_bytes())
                    out.flush()
                    os.fsync(out.fileno())
                state = dict(status='pending', armed_at=now, deadline=now + 2400,
                             boot_id=boot, reboot_count=1, predecessor_sha256=predecessor_sha256)
                if mode == 'resume-successor':
                    state['original_predecessor_sha256'] = original_predecessor_sha256
                save(state)
                (ROOT / 'contained').unlink()
            elif mode == 'grant':
                if state['status'] != 'accepted':
                    pending(state, now)
                    if state['boot_id'] != boot:
                        if state['reboot_count'] != 0:
                            raise ValueError('only one pending reboot permitted')
                        state.update(boot_id=boot, reboot_count=1)
                        save(state)
                    subprocess.run(['systemctl', 'is-active', '--quiet', TIMER], check=True, timeout=5)
                PERMIT.parent.mkdir(mode=0o700, exist_ok=True)
                if any(p.is_symlink() for p in (PERMIT, *PERMIT.parents)):
                    raise ValueError('symlink in ephemeral permit')
                fd = os.open(PERMIT, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
                with os.fdopen(fd, 'w') as out:
                    out.write('Owner startup authority: remaining-deployment/state.json\n')
            elif mode == 'accept':
                pending(state, now, margin=120)
                if state['reboot_count'] != 1 or state['boot_id'] != boot:
                    raise ValueError('planned reboot not observed')
                state.update(status='accepted', accepted_at=now)
                save(state)
                fd = os.open(ROOT / 'accepted', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
                os.fsync(fd)
                os.close(fd)
                directory = os.open(ROOT, os.O_DIRECTORY)
                try:
                    os.fsync(directory)
                finally:
                    os.close(directory)
            elif mode in ('contain', 'expire'):
                if mode == 'expire' and state['status'] == 'accepted':
                    return state
                fd = os.open(ROOT / 'contained', os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW, 0o600)
                os.close(fd)
                (ROOT / 'accepted').unlink(missing_ok=True)
                state.update(status='contained', contained_at=now)
                save(state)
                for p in (PERMIT, Path('/etc/webmin/.installation-accepted'),
                          Path('/etc/cron.d/needrestart_check')):
                    p.unlink(missing_ok=True)
            elif mode == 'check':
                pending(state, now, margin=120)
            else:
                raise ValueError('unknown action')
    # Never hold the lock while waiting for units whose startup acquires it.
    if mode in ('contain', 'expire'):
        subprocess.run(['systemctl', 'stop', *UNITS], check=True, timeout=100)
        subprocess.run(['systemctl', 'disable', 'webmin.service'], check=True, timeout=10)
        # Stop only task-labelled temporary probes from this otherwise empty baseline.
        for label in ['homelab.uptime-kuma.restore', 'homelab.uptime-kuma.ingress']:
            rows = json.loads(subprocess.check_output(
                ['podman', 'ps', '-a', '--filter', 'label=' + label, '--format', 'json'],
                text=True, timeout=10))
            for row in rows:
                ident = row['Id']
                detail = json.loads(subprocess.check_output(['podman', 'inspect', ident], text=True, timeout=10))[0]
                value = detail['Config']['Labels'].get(label, '')
                if label.endswith('.restore'):
                    owned = bool(value) and any(m.get('Destination') == '/app/data' and
                            Path(m['Source']).is_relative_to(ROOT / 'restore') for m in detail['Mounts'])
                else:
                    owned = len(value) == 32 and all(c in '0123456789abcdef' for c in value) and \
                            detail['Name'] == 'kuma-ingress-' + value[:12]
                if not owned:
                    raise ValueError('unexpected labelled container; manual containment required')
                subprocess.run(['podman', 'stop', '--time', '20', ident], check=True, timeout=30)
                subprocess.run(['podman', 'rm', ident], check=True, timeout=10)
    return state


if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == 'resume-successor':
        print(json.dumps(action('resume-successor', sys.argv[2], sys.argv[3])))
    elif len(sys.argv) == 3 and sys.argv[1] == 'resume':
        print(json.dumps(action('resume', sys.argv[2])))
    elif len(sys.argv) == 2 and sys.argv[1] in ('arm', 'grant', 'accept', 'contain', 'expire', 'check'):
        print(json.dumps(action(sys.argv[1])))
    else:
        raise SystemExit('usage: startup-permit.py arm|grant|check|accept|contain|expire or resume PREDECESSOR_SHA256 or resume-successor PREDECESSOR_SHA256 ORIGINAL_SHA256')
