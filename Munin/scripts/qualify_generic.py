#!/usr/bin/python3
"""Seal one-use native generic-plugin qualification without changing selection."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import io
import json
import math
import os
from pathlib import Path
import pwd
import grp
import re
import signal
import stat
import subprocess
import tarfile
import time

ROOT = Path(__file__).resolve().parents[1]
MEMBERS = {'runner.py', 'common.py', 'observer.py', 'helper.py', 'known_hosts',
           'candidate.json', 'spec.json', 'review.md', 'manifest.json'}
h = o = c = None  # Bound to frozen, repository-owned modules by the bootstrap.


def load(raw, name):
    ns = {'__name__': name, '__file__': '/sealed/'+name+'.py'}
    exec(compile(raw, ns['__file__'], 'exec'), ns)
    import types
    return types.SimpleNamespace(**ns), ns


def private_directory(path, uid, gid, mode):
    """Create only an absent direct child of trusted, non-writable ancestors."""
    path = Path(path)
    for parent in path.parents:
        meta = parent.lstat()
        if (not stat.S_ISDIR(meta.st_mode) or meta.st_uid != 0
                or stat.S_IMODE(meta.st_mode) & 0o022):
            raise ValueError('unsafe staging ancestor: '+str(parent))
    path.mkdir(mode=mode)
    os.chown(path, uid, gid)
    os.chmod(path, mode)


def direct_file(path, raw, mode=0o644):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    os.chmod(path, mode)


def settings(names, stage):
    rows = []
    for name in names:
        identity = 'root' if name in ('ntp_statistics', 'ntp_jobs') else 'munin'
        rows += ['['+name+']', 'user '+identity, 'group '+identity,
                 'env.MUNIN_PLUGSTATE '+str(stage/'state'/identity),
                 'env.MUNIN_STATEFILE '+str(stage/'state'/identity/name)]
    return ('\n'.join(rows)+'\n').encode()


def fields(config, fetch):
    """Validate multigraph field coverage and retain unknowns for disposition."""
    expected, computed, values = set(), set(), {}
    graph = ''
    for row in config.splitlines():
        if row.startswith('multigraph '):
            graph = row.split(' ', 1)[1]
        match = re.fullmatch(r'([A-Za-z0-9_]+)\.(label|cdef) (.+)', row)
        if match:
            if match[2] == 'label':
                expected.add((graph, match[1]))
            elif match[1] not in match[3].split(','):
                computed.add((graph, match[1]))
    expected -= computed
    if not expected or not any(r.startswith('graph_title ') for r in config.splitlines()):
        raise ValueError('missing configured graph/fields')
    graph = ''
    for row in fetch.splitlines():
        if row.startswith('multigraph '):
            graph = row.split(' ', 1)[1]
            continue
        if not row or row.startswith('#'):
            continue
        match = re.fullmatch(r'([A-Za-z0-9_]+)\.value (U|[-+]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][-+]?[0-9]+)?)', row)
        if not match:
            raise ValueError('invalid fetch value')
        key = (graph, match[1])
        if key in values:
            raise ValueError('duplicate fetch field')
        value = match[2]
        if value != 'U' and not math.isfinite(float(value)):
            raise ValueError('nonfinite fetch value')
        values[key] = value
    if not expected <= values.keys():
        raise ValueError('missing configured fetch field')
    return {'configured_fields': len(expected), 'unknown_fields': [list(k) for k in sorted(expected) if values[k] == 'U'],
            'numeric_fields': sum(values[k] != 'U' for k in expected),
            'graphs': sorted({g for g, _ in expected})}


def nfs_capability(raw):
    markers = {r.split()[0] for r in raw.decode('ascii').splitlines() if r.split()}
    return {'nfs_client': 'proc3' in markers, 'nfs4_client': 'proc4' in markers}


def nfs_proc_path():
    # /proc/net is Linux's self/net alias. Keep the no-symlink reader intact
    # and address this worker's current network namespace by its concrete PID.
    return Path('/proc')/str(os.getpid())/'net/rpc/nfs'


def invoke(stage, name, action=None, timeout=12):
    argv = ['/usr/sbin/munin-run', '--ignore-systemd-properties', '--config', str(stage/'node.conf'),
            '--servicedir', str(stage/'plugins'), '--sconffile', str(stage/'settings'), name]
    if action:
        argv.append(action)
    start = time.monotonic()
    row = h.bounded(argv, timeout=timeout, limit=262144)
    row['seconds'] = time.monotonic()-start
    return row


def workload(stage, names, lane, allow_diskstats_cold=False):
    start = time.monotonic()
    rows = {}
    for name in names:
        pair = {}
        for action in ('config', 'fetch'):
            remaining = 25-(time.monotonic()-start)
            if remaining <= 0:
                return {'lane': lane, 'seconds': time.monotonic()-start, 'plugins': rows, 'error': '25-second workload budget'}
            row = invoke(stage, name, None if action == 'fetch' else action, min(12, remaining))
            pair[action] = row
            if row.get('returncode') != 0 or row.get('error'):
                pair['error'] = 'native invocation failed'
                break
        if 'error' not in pair:
            try:
                if name == 'diskstats' and allow_diskstats_cold and not pair['fetch']['stdout'].strip():
                    pair['cold_start_no_sample'] = True
                else:
                    pair['fields'] = fields(pair['config']['stdout'], pair['fetch']['stdout'])
            except ValueError as error:
                pair['error'] = str(error)
        rows[name] = pair
    return {'lane': lane, 'seconds': time.monotonic()-start, 'plugins': rows,
            'complete': set(rows) == set(names) and all('error' not in r for r in rows.values())}


def snapshot_selection(spec):
    root = Path('/etc/munin/plugins')
    if root.is_symlink() or {p.name for p in root.iterdir()} != set(spec['enabled_links']):
        raise ValueError('production plugin selection drift')
    for name, target in spec['enabled_links'].items():
        link = root/name
        if not link.is_symlink() or os.readlink(link) != target:
            raise ValueError('production plugin link drift: '+name)
    directory = Path('/etc/munin/plugin-conf.d')
    if directory.is_symlink() or {p.name for p in directory.iterdir()} != set(spec['settings_files']):
        raise ValueError('production settings selection drift')


def state_snapshot(stage):
    result = {}
    for identity in ('munin', 'root'):
        directory = stage/'state'/identity
        entries = list(directory.iterdir())
        if len(entries) > 128:
            raise ValueError('state entry bound')
        for path in entries:
            raw, meta = o.read(path, 1048576)
            if meta['uid'] != pwd.getpwnam(identity).pw_uid or meta['mode'] & 0o077:
                raise ValueError('unsafe state ownership/mode')
            result[identity+'/'+path.name] = dict(meta, native_state_magic=raw.startswith(b'%MUNIN-STATE1.0\n'))
    return result


def qualify(spec):
    start = time.monotonic()
    result = {'operation_id': spec['operation_id'], 'spec_sha256': h.sha(h.encoded(spec)),
              'capture_complete': False, 'deployment_accepted': False, 'stage_created': False,
              'real_protocol_runtime_accepted': False}
    before = None
    try:
        before = o.continuity(spec)
        snapshot_selection(spec)
        result['before'] = before
        result['package_versions'] = h.bounded(['/usr/bin/dpkg-query', '-W', '-f=${Package}\t${Version}\n',
            'munin-node', 'munin-common', 'munin-plugins-core', 'net-tools', 'procps', 'coreutils', 'perl'], timeout=10, limit=8192)
        for name in ('munin-node', 'munin-common', 'munin-plugins-core'):
            if name+'\t2.0.76-5\n' not in result['package_versions']['stdout']:
                raise ValueError('native package version drift: '+name)
        result['dependencies'] = {}
        for path in ('/usr/bin/netstat', '/usr/bin/vmstat', '/usr/bin/who', '/usr/bin/df', '/usr/bin/perl'):
            try:
                _, meta = o.read(path, 8388608)
                result['dependencies'][path] = meta
            except (OSError, ValueError) as error:
                result['dependencies'][path] = {'error': str(error)}
        result['perl_modules'] = h.bounded(['/usr/bin/perl', '-MMunin::Plugin', '-MMIME::Base64', '-MStorable',
            '-e', 'print "native modules loaded\n"'], timeout=10, limit=8192)
        try:
            raw, _ = o.read(nfs_proc_path(), 65536)
            capability = nfs_capability(raw)
        except FileNotFoundError:
            capability = nfs_capability(b'')
        result['nfs_capability'] = capability
        names = [n for n in spec['plugins'] if capability.get(n, True)]
        result['not_applicable_pending_review'] = [n for n, supported in capability.items() if not supported]
        result['tested_plugins'] = names
        # Native munin-run calls mkdir_subdir before environment overrides. Require
        # both default user directories already present, never create them here.
        for identity in ('munin', 'root'):
            path = Path('/var/lib/munin-node/plugin-state')/identity
            for parent in (path, *path.parents):
                if parent.is_symlink():
                    raise ValueError('indirect default state directory')
            meta = path.stat()
            if not stat.S_ISDIR(meta.st_mode) or meta.st_uid != pwd.getpwnam(identity).pw_uid:
                raise ValueError('existing native state directory required')
        stage = Path(spec['stage'])
        private_directory(stage, 0, 0, 0o711)
        result['stage_created'] = True
        private_directory(stage/'plugins', 0, 0, 0o755)
        private_directory(stage/'state', 0, 0, 0o711)
        for identity in ('munin', 'root'):
            private_directory(stage/'state'/identity, pwd.getpwnam(identity).pw_uid,
                              grp.getgrnam(identity).gr_gid, 0o700)
        direct_file(stage/'node.conf', b'user munin\ngroup munin\n')
        direct_file(stage/'settings', settings(names, stage))
        for name in names:
            os.symlink(spec['plugins'][name], stage/'plugins'/name)
        result['individual'] = workload(stage, names, 'individual', allow_diskstats_cold=True)
        result['state_cold'] = state_snapshot(stage)
        # Genuine elapsed interval and native counters, no invented timestamps.
        due = time.monotonic()+305
        while time.monotonic() < due:
            time.sleep(min(30, due-time.monotonic()))
        with ThreadPoolExecutor(max_workers=3) as pool:
            result['concurrent'] = list(pool.map(lambda lane: workload(stage, names, lane),
                                               ('canonical-equivalent', 'transport-v4-equivalent', 'transport-v6-equivalent')))
        result['state_concurrent'] = state_snapshot(stage)
        result['diskstats_readback'] = invoke(stage, 'diskstats')
        result['state_readback'] = state_snapshot(stage)
        result['capture_complete'] = True
    except Exception as error:
        result['error'] = str(error)
    finally:
        try:
            snapshot_selection(spec)
            result['after'] = o.continuity(spec)
            if before is None or result['after'] != before:
                raise ValueError('continuity changed during qualification')
        except Exception as error:
            result['continuity_error'] = str(error)
            result['capture_complete'] = False
    result['seconds'] = time.monotonic()-start
    result['findings_require_review'] = True
    return result


def review(s):
    return f"""# Native generic-plugin qualification — j2-svntp1

Operation `{s['operation_id']}`; one contact to ama@10.1.0.51 using the pinned
Ed25519 alias 10.1.0.137. Approve qualification.tar's SHA-256 in sealing.json.
Expires epoch {s['expires_epoch']}. Frozen runner.py execute --directory DIRECTORY
--sha256 APPROVED_SHA256; one-use receipt fsynced before contact. No retry/replay.

## Scope and writes

Require accepted root/host/boot/time-service/file identities before and after.
Verify all selected installed package sources and native Munin helpers against
the approved 2.0.76-5 Debian package bytes. Query package versions, command file
metadata and hashes; load Munin::Plugin/MIME::Base64/Storable; read only NFS
proc3/proc4 capability markers from /proc/WORKER_PID/net/rpc/nfs in this worker's
network namespace. WORKER_PID is os.getpid(), never an input-selected PID/path.
This avoids the normal /proc/net -> self/net alias while retaining the protected
reader's symlink rejection. Missing dependencies/capabilities are findings.

Create only the absent directory `{s['stage']}` (root:root 0711), plugins
(root:root 0755), state (root:root 0711), and state/munin and state/root (their
respective user/group, 0700). Root-owned 0644 alternate native node/settings
files contain no secrets. Plugin links reference pinned installed sources.
Native state files and private evidence are retained. This is a scoped writing
qualification, not a read-only inspection. No deletion or recovery is needed:
the selected production files, links, state, daemon and master are not changed.
Failure holds the isolated stage for inspection; no automatic retry/cleanup.

Run actual installed munin-run with --ignore-systemd-properties, --config,
--servicedir and --sconffile against this isolated selection. All generic and
ntp_health/storage readers run munin:munin; only ntp_statistics/jobs root:root.
Every plugin gets explicit isolated MUNIN_PLUGSTATE/MUNIN_STATEFILE overrides.
Require native default root/munin state directories already present because
munin-run checks them before overrides. No production state path is selected.

One full sequential config/fetch pass; wait a genuine 305 seconds; then three
concurrent full passes sharing isolated state to exercise native diskstats
atomic-write collisions; finally one diskstats fetch to check readable state.
Each full pass has a 25-second budget, each subprocess at most 12 seconds and
256 KiB per stream. Root alarm 600 seconds, outer SSH bound 660 seconds and
8 MiB retained output. Capture native stdout/stderr, field coverage, unknowns,
durations and state hashes/ownership. No made-up records, timestamps or counters.

## Boundaries and interpretation

No production package install, plugin selection, daemon/config/unit change,
start/reload/restart, autoconfiguration, NFS activation, Wi-Fi activation,
network/DNS change, maintenance job, RRD write, master contact or notification.
Native scripts can read sensors, proc/sysfs, mounts, process counters and invoke
their normal read-only helpers (including interface link-speed discovery).
SSH/sudo audit writes occur normally. No reference-node contact.

NFS plugins without their respective native markers are withheld and explicitly
reported for disposition; this does not silently remove their requirements.
Individual/concurrent failures or U fields remain findings, not root escalation
or acceptance. Polling measurements are native-workload estimates: this stage
does not reproduce the production daemon sandbox, TCP framing, source routing,
actual canonical/family scheduling or master RRD work. Those require deployment
acceptance. Keep the 25-second production protocol budget pending measurement.

## Next gate

Review actual capabilities, each graph/field, privileges, diskstats cold/warm
state and concurrent output. Then seal the coordinated node/master continuation
with the exact qualified selection and owned-file restoration. No production
deployment is authorized by this qualification. Contacts stay disabled.
"""


def package_pins(paths, expected):
    pins = {}
    for path in paths:
        raw = path.read_bytes()
        if c.sha(raw) != expected[path.name]:
            raise ValueError('approved package digest mismatch: '+path.name)
        data = subprocess.check_output(['/usr/bin/dpkg-deb', '--fsys-tarfile', str(path)])
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:
            for member in archive:
                name = '/'+member.name.removeprefix('./')
                if member.isfile() and (name.startswith('/usr/share/munin/plugins/')
                    or name.startswith('/usr/share/perl5/Munin/') or name == '/usr/sbin/munin-run'):
                    pins[name] = c.sha(archive.extractfile(member).read())
    return pins


def unpack(raw, digest):
    if len(raw) > 8388608 or c.sha(raw) != digest:
        raise ValueError('approved archive hash/size mismatch')
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        rows = archive.getmembers()
        if (len(rows) != len(MEMBERS) or {m.name for m in rows} != MEMBERS
                or any(not m.isfile() or m.size > 1048576 for m in rows)):
            raise ValueError('closed regular archive required')
        files = {m.name: archive.extractfile(m).read() for m in rows}
    if json.loads(files['manifest.json']) != {n: c.sha(v) for n, v in files.items() if n != 'manifest.json'}:
        raise ValueError('member digest mismatch')
    s = json.loads(files['spec.json'])
    if (s['kind'] != 'node' or (s['endpoint'], s['user'], s['host_key_alias'], s['hostname']) != c.TARGETS['node']
            or not re.fullmatch(r'munin-generic-qualification-[0-9]{8}-v[0-9]+', s['operation_id'])
            or s['stage'] != '/var/lib/'+s['operation_id']
            or not 0 < s['expires_epoch']-s['prepared_epoch'] <= 86400
            or not s['prepared_epoch'] <= time.time() < s['expires_epoch']-900
            or files['review.md'] != review(s).encode()):
        raise ValueError('scope/expiry/review binding mismatch')
    return s, files


def seal(args):
    baseline = c.private(args.inventory/'inspection.tar')
    receipt = json.loads(c.private(args.inventory/'execution.json'))
    inventory_spec, inventory_files = c.unpack(baseline, receipt['sha256'])
    capture = json.loads(c.private(args.inventory/'stdout.txt'))
    terminal = json.loads(c.private(args.inventory/'result.json'))
    if (inventory_spec['purpose'] != 'generic-profile' or inventory_spec['kind'] != 'node'
            or capture.get('capture_complete') is not True or terminal.get('capture_complete') is not True
            or terminal.get('returncode') != 0 or terminal.get('error')
            or terminal.get('bundle_sha256') != c.sha(baseline)
            or capture.get('spec_sha256') != c.sha(c.encoded(inventory_spec))):
        raise ValueError('accepted completed node inventory required')
    node, _, node_provenance = c.accepted(args.node, 'node_runtime_accepted')
    installation = json.loads(node['spec.json'])['worker']['installation']
    expected = {p['filename']: p['sha256'] for p in installation['packages']}
    pins = package_pins(args.packages, expected)
    candidate = (ROOT/'node/profiles/ntp/generic-parity.candidate.json').read_bytes()
    profile = json.loads(candidate)
    spec = dict(inventory_spec)
    now = int(time.time())
    spec.update(operation_id=args.output.name, prepared_epoch=now, expires_epoch=now+86400,
                purpose='native-generic-qualification', stage='/var/lib/'+args.output.name,
                inventory_sha256=c.sha(baseline), node_provenance=node_provenance,
                plugins={}, enabled_links={}, settings_files=[])
    base_source = (ROOT/'scripts/install_ntp_node.py').read_bytes()
    base, _ = load(base_source, 'base')
    spec['node_config_renderer_sha256'] = c.sha(base_source)
    spec['files']['/etc/munin/munin-node.conf'] = c.sha(base.node_config(
        installation['hostname'], installation['listen_addresses'], installation['allow_addresses']))
    selected = set(profile['proposed_package_plugins']) | set(profile['retained_custom_plugins'])
    for name in selected:
        template = profile['package_template_sources'].get(name)
        path = '/usr/share/munin/plugins/'+template if template else '/usr/local/munin/lib/plugins/'+name
        spec['plugins'][name] = path
        if template:
            spec['files'][path] = pins[path]
    spec['plugins'] = dict(sorted(spec['plugins'].items()))
    for path, digest in pins.items():
        if path.startswith('/usr/share/perl5/Munin/') or path.endswith('/plugin.sh') or path == '/usr/sbin/munin-run':
            spec['files'][path] = digest
    for row in capture['observations']['enabled_plugins']:
        spec['enabled_links'][row['name']] = row['target']
        spec['files'][row['target']] = row['source']['sha256']
    for row in capture['observations']['settings']:
        spec['settings_files'].append(row['name'])
        spec['files']['/etc/munin/plugin-conf.d/'+row['name']] = row['metadata']['sha256']
    files = {'runner.py': Path(__file__).read_bytes(), 'common.py': (ROOT/'scripts/review_ntp_observation.py').read_bytes(),
             'observer.py': (ROOT/'scripts/observe_ntp.py').read_bytes(),
             'helper.py': (ROOT.parent.parent/'homelab-ntp/ntpsec/scripts/run-production-inspection.py').read_bytes(),
             'known_hosts': inventory_files['known_hosts'], 'candidate.json': candidate,
             'spec.json': c.encoded(spec), 'review.md': review(spec).encode()}
    files['manifest.json'] = c.encoded({n: c.sha(v) for n, v in files.items()})
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode='w') as archive:
        for name, raw in sorted(files.items()):
            member = tarfile.TarInfo(name)
            member.size, member.mode = len(raw), 0o600
            archive.addfile(member, io.BytesIO(raw))
    raw = stream.getvalue()
    unpack(raw, c.sha(raw))
    args.output.mkdir(mode=0o700)
    for name, data in files.items():
        direct_file(args.output/name, data, 0o600)
    direct_file(args.output/'qualification.tar', raw, 0o600)
    result = {'sha256': c.sha(raw), 'expires_epoch': spec['expires_epoch'], 'target_contact': False}
    direct_file(args.output/'sealing.json', c.encoded(result), 0o600)
    return result


def prepare(directory, digest):
    meta = directory.lstat()
    if not stat.S_ISDIR(meta.st_mode) or meta.st_uid != os.getuid() or stat.S_IMODE(meta.st_mode) != 0o700:
        raise ValueError('owner-private directory required')
    spec, files = unpack(c.private(directory/'qualification.tar'), digest)
    if files['runner.py'] != Path(__file__).read_bytes():
        raise ValueError('frozen controller required')
    for name, raw in files.items():
        if c.private(directory/name) != raw:
            raise ValueError('frozen local input drift: '+name)
    return spec, files


def payload(spec, files):
    return (b'import signal\n'+b'h,hn=load('+repr(files['helper.py']).encode()+b',"helper")\n'
        +b'o,on=load('+repr(files['observer.py']).encode()+b',"observer")\non["h"]=h\n'
        +b'signal.signal(signal.SIGALRM,h.expired)\nsignal.alarm(600)\n'
        +b'print(json.dumps(qualify('+repr(spec).encode()+b')))\n')


def execute(directory, digest):
    spec, files = prepare(directory, digest)
    helper, _ = load(files['helper.py'], 'helper')
    argv = helper.ssh_argv({'endpoints': [spec['endpoint']], 'host_key_alias': spec['host_key_alias']}, directory)
    argv[-2] = spec['user']+'@'+spec['endpoint']
    submitted = (b'ns={"__name__":"qualification","__file__":"/sealed/Munin/scripts/runner.py"}\nexec('
                 +repr(files['runner.py']).encode()+b',ns)\nexec('+repr(payload(spec, files)).encode()+b',ns)\n')
    with (directory/'execution.json').open('xb') as stream:
        stream.write(c.encoded({'sha256': digest, 'epoch': time.time(), 'argv': argv, 'payload_sha256': c.sha(submitted)}))
        stream.flush()
        os.fsync(stream.fileno())
    row = helper.bounded(argv, timeout=660, limit=8388608, payload=submitted, env=os.environ.copy())
    for name in ('stdout', 'stderr'):
        direct_file(directory/(name+'.txt'), row.pop(name).encode(), 0o600)
    row.update(bundle_sha256=digest, capture_complete=False, deployment_accepted=False)
    if row.get('returncode') == 0 and not row.get('error'):
        capture = json.loads((directory/'stdout.txt').read_text())
        if capture.get('operation_id') != spec['operation_id'] or capture.get('spec_sha256') != c.sha(c.encoded(spec)):
            raise ValueError('qualification scope binding')
        row['capture_complete'] = capture.get('capture_complete') is True
    direct_file(directory/'result.json', c.encoded(row), 0o600)
    return row


def main():
    global c
    os.umask(0o077)
    common = Path(__file__).with_name('common.py')
    if not common.exists():
        common = ROOT/'scripts/review_ntp_observation.py'
    c, _ = load(common.read_bytes(), 'common')
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    q = sub.add_parser('seal')
    for name in ('inventory', 'node', 'output'):
        q.add_argument('--'+name, type=Path, required=True)
    q.add_argument('--packages', type=Path, nargs=3, required=True)
    for action in ('check', 'execute'):
        q = sub.add_parser(action)
        q.add_argument('--directory', type=Path, required=True)
        q.add_argument('--sha256', required=True)
    args = parser.parse_args()
    if args.action == 'seal':
        result = seal(args)
    elif args.action == 'check':
        prepare(args.directory, args.sha256)
        result = {'verified': True, 'target_contact': False}
    else:
        result = execute(args.directory.absolute(), args.sha256)
    print(json.dumps(result))
    if args.action == 'execute' and not result.get('capture_complete'):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
