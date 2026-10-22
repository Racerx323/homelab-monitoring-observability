#!/usr/bin/python3
"""Scheduled contact gate; absence of a committed enable marker sends nothing."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import time
import types

CONTROL = Path('/var/lib/munin-ntp-contact-control')
CONFIG = Path('/etc/munin/munin.conf')
HELPER = Path('/usr/local/libexec/munin-ntp-mailrise.py')
GATE = Path('/usr/local/libexec/munin-ntp-contact-gate.py')
STATUS = Path('/var/lib/munin/ntp-alerts')


def secure(path, mode=None, limit=1048576):
    path = Path(path)
    for parent in path.parents:
        m = parent.lstat()
        if not stat.S_ISDIR(m.st_mode) or m.st_uid != 0 or m.st_mode & 0o022:
            raise ValueError('unsafe contact ancestor')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        m = os.fstat(stream.fileno())
        if (not stat.S_ISREG(m.st_mode) or m.st_uid != 0 or m.st_gid != 0
                or m.st_nlink != 1 or m.st_mode & 0o022 or m.st_size > limit
                or mode is not None and stat.S_IMODE(m.st_mode) != mode):
            raise ValueError('unsafe contact input')
        raw = stream.read(limit + 1)
        after = os.fstat(stream.fileno())
    if len(raw) > limit or (m.st_size, m.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError('contact input changed')
    return raw, m


def lock(exclusive=False):
    raw, before = secure(CONTROL/'lock', 0o644)
    if raw:
        raise ValueError('contact lock must be empty')
    fd = os.open(CONTROL/'lock', os.O_RDONLY | os.O_NOFOLLOW)
    try:
        current = os.fstat(fd)
        if (current.st_dev, current.st_ino) != (before.st_dev, before.st_ino):
            raise ValueError('contact lock replaced')
        deadline = time.monotonic() + 20
        while True:
            try:
                fcntl.flock(fd, (fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH) | fcntl.LOCK_NB)
                return fd
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise TimeoutError('contact lock deadline')
                time.sleep(.05)
    except BaseException:
        os.close(fd)
        raise


def enabled():
    raw, _ = secure(CONTROL/'enabled.json', 0o644, 4096)
    token = json.loads(raw)
    if set(token) != {'operation_id', 'worker_sha256', 'config_sha256', 'helper_sha256', 'gate_sha256'}:
        raise ValueError('closed contact enable marker required')
    for path, key, mode in ((CONFIG, 'config_sha256', 0o644),
                            (HELPER, 'helper_sha256', 0o755), (GATE, 'gate_sha256', 0o755)):
        data, _ = secure(path, mode)
        if hashlib.sha256(data).hexdigest() != token[key]:
            raise ValueError('enabled contact input drift')
    return token


def record_suppression():
    m = STATUS.lstat()
    if (not stat.S_ISDIR(m.st_mode) or m.st_uid != os.geteuid()
            or stat.S_IMODE(m.st_mode) != 0o700 or any(p.is_symlink() for p in (STATUS, *STATUS.parents))):
        raise ValueError('private suppression directory required')
    try:
        fd = os.open(STATUS/'suppressed.json', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    except FileExistsError:
        return  # Preserve the first actual suppressed call; never preseed success.
    with os.fdopen(fd, 'wb') as stream:
        stream.write((json.dumps({'schema': 1, 'suppressed_epoch': time.time(), 'reason': 'gate or pinned input absent'})+'\n').encode())
        stream.flush()
        os.fsync(stream.fileno())
    fd = os.open(STATUS, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def main():
    if len(sys.argv) != 1:
        raise ValueError('no contact arguments supported')
    # Suppressed input never reaches SMTP and never creates a success record.
    fd = lock()
    try:
        try:
            enabled()
        except FileNotFoundError:
            record_suppression()
            raise
        raw, _ = secure(HELPER, 0o755)
        namespace = {'__name__': 'contact_helper', '__file__': str(HELPER)}
        exec(compile(raw, str(HELPER), 'exec'), namespace)
        types.SimpleNamespace(**namespace).main()
    finally:
        os.close(fd)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('Munin contact disabled or rejected: ' + str(error), file=sys.stderr)
        raise SystemExit(75)
