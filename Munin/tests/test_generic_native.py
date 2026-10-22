#!/usr/bin/python3
"""Disposable Trixie container only: actual munin-run isolation and state I/O."""
import importlib.util
import os
from pathlib import Path
import pwd
import grp
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
import time

ROOT = Path(__file__).resolve().parents[1]


def module(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def main():
    if not Path('/run/.containerenv').exists() or os.geteuid() != 0:
        raise SystemExit('disposable root container required')
    for path in sys.argv[1:]:
        subprocess.run(['dpkg-deb', '-x', path, '/'], check=True)
    subprocess.run(['groupadd', '--system', 'munin'], check=True)
    subprocess.run(['useradd', '--system', '--gid', 'munin', '--no-create-home', 'munin'], check=True)
    q = module(ROOT/'scripts/qualify_generic.py')
    q.h = module(ROOT.parent.parent/'homelab-ntp/ntpsec/scripts/run-production-inspection.py')
    q.o = module(ROOT/'scripts/observe_ntp.py')
    stage = Path('/var/lib/native-generic-test')
    q.private_directory(stage, 0, 0, 0o711)
    q.private_directory(stage/'plugins', 0, 0, 0o755)
    q.private_directory(stage/'state', 0, 0, 0o711)
    for identity in ('root', 'munin'):
        q.private_directory(stage/'state'/identity, pwd.getpwnam(identity).pw_uid, grp.getgrnam(identity).gr_gid, 0o700)
        default = Path('/var/lib/munin-node/plugin-state')/identity
        default.mkdir(parents=True)
        os.chown(default, pwd.getpwnam(identity).pw_uid, grp.getgrnam(identity).gr_gid)
    names = ['cpu', 'diskstats', 'if_lo']
    q.direct_file(stage/'node.conf', b'user munin\ngroup munin\n')
    q.direct_file(stage/'settings', q.settings(names, stage))
    for name in names:
        os.symlink('/usr/share/munin/plugins/'+('if_' if name == 'if_lo' else name), stage/'plugins'/name)
    row = q.workload(stage, names, 'native', allow_diskstats_cold=True)
    if not row['complete']:
        print({name: pair.get('error') for name, pair in row['plugins'].items()})
        raise SystemExit('native workload failed')
    assert q.state_snapshot(stage)['munin/diskstats']['native_state_magic']
    assert not any(Path('/var/lib/munin-node/plugin-state/munin').iterdir())
    time.sleep(2)  # Native elapsed counters; the target qualification uses 305s.
    with ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(lambda _: q.workload(stage, names, 'native-concurrent'), range(3)))
    for row in rows:
        if not row['complete']:
            print({name: pair.get('error') for name, pair in row['plugins'].items()})
            raise SystemExit('native concurrent workload failed')
    assert q.state_snapshot(stage)['munin/diskstats']['native_state_magic']
    result = q.invoke(stage, 'diskstats')
    assert result['returncode'] == 0 and not result.get('error')
    assert not any(Path('/var/lib/munin-node/plugin-state/munin').iterdir())
    print('Native Munin 2.0.76-5: interface instance, unprivileged diskstats, isolated state, three concurrent runs and readback passed; target capability and 300s warm-up not accepted.')


if __name__ == '__main__':
    main()
