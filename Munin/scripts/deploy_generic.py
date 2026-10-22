#!/usr/bin/python3
"""Seal ordered generic expansion stages using the existing timed transaction runner."""
import argparse
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tarfile
import time
import types

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent.parent
STAGES = Path('/var/lib/munin-generic-stages')
SOURCES = {'runner.py': Path(__file__), 'transaction.py': ROOT/'scripts/deploy_ntp_master.py',
           'worker.py': ROOT/'scripts/update_generic.py', 'base.py': ROOT/'scripts/install_ntp_node.py',
           'qualifier.py': ROOT/'scripts/qualify_master.py', 'observer.py': ROOT/'scripts/observe_ntp.py',
           'data-utils.py': ROOT/'scripts/review_ntp_observation.py', 'fields.py': ROOT/'scripts/qualify_generic.py',
           'probe.py': ROOT/'scripts/probe_generic.py', 'sync.py': ROOT/'scripts/sync_master_baseline.py',
           'helper.py': WORKSPACE/'homelab-ntp/ntpsec/scripts/run-production-inspection.py',
           'tls-probe.py': WORKSPACE/'homelab-network/Ubiquiti/munin-master-profile/qualify_dashboard.py',
           'tests.py': ROOT/'tests/test_generic_update.py', 'native-tests.py': ROOT/'tests/test_generic_update_native.py',
           'native-runner.py': ROOT/'tests/run_generic_native.py'}
DATA = {'known_hosts', 'ca.pem', 'compatible.py', 'expanded.py', 'profile-before.json', 'profile-after.json',
        'settings-before', 'settings-after', 'transport-before', 'qualification.json', 'spec.json', 'review.md', 'manifest.json'}
MEMBERS = set(SOURCES) | DATA


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True)+'\n').encode()


def private(path, limit=8388608):
    path = Path(path)
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('indirect private input')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        m = os.fstat(stream.fileno())
        if not stat.S_ISREG(m.st_mode) or m.st_uid != os.getuid() or stat.S_IMODE(m.st_mode) != 0o600:
            raise ValueError('owner-private regular input required')
        raw = stream.read(limit+1)
    if len(raw) > limit:
        raise ValueError('private input bound')
    return raw


def module(raw, name):
    result = types.ModuleType(name)
    result.__file__ = '/sealed/Munin/scripts/'+name+'.py'
    exec(compile(raw, result.__file__, 'exec'), result.__dict__)
    return result


def transaction(files):
    tx = module(files['transaction.py'], 'transaction')
    # Reuse its exact locking, detached worker, independent timer and bounded
    # root launcher. Only archive scope and update implementation differ.
    tx.STAGES, tx.unpack = STAGES, unpack
    return tx


def review(s):
    w = s['worker']
    node = w['role'] == 'node'
    return f"""# Coordinated generic expansion — {w['role']}

Operation `{s['operation_id']}`; expires epoch {s['expires_epoch']}.
Approve deployment.tar's exact SHA-256 in sealing.json. Frozen runner.py execute
--directory DIRECTORY --sha256 APPROVED_SHA256. Start with at least 900 seconds
remaining. One fsynced local receipt before contact; no installer replay/retry.
Primary SSH {s['user']}@{s['endpoint']}, strict alias {s['host_key_alias']}.
Root/hostname/boot, protected service/file pins and exact baseline are required.
The node restart stage additionally pins the canonical package unit, accepted
startup-guard drop-in and original empty permit; unreviewed drop-ins fail closed.

## Exact change

Atomically replace only `{w['target']}` with the frozen reviewed candidate,
root:root mode {w['mode']:04o}. Before bytes and metadata are retained privately.
{'Briefly stop only munin-node; publish exactly 24 new package-plugin links and expanded privilege settings; start the enabled node. No NTP/GPS restart. All 29 generic readers remain munin:munin; only ntp_statistics/jobs root.' if node else 'Replace the existing transport source only. No master/node service restart, settings, main munin.conf, CGI, Apache or schedule change: native Munin executes plugin sources afresh. Preserve the main configuration mirror byte-for-byte.'}
Master transport accepts {'the exact old nine or complete expanded 33' if w['role']=='compatible' else 'exactly the expanded 33' if w['role']=='expanded' else 'the already-installed exact old-or-expanded compatibility sets'};
partial selections/arbitrary supersets are rejected. Self-referencing interface
CDEF counters remain mandatory. Keep the 25-second full per-family budget.

## Preconditions and acceptance

{'Require the committed compatible master transaction first. The review includes bounded read-only SSH acceptance on pi@10.1.3.83 (svmf.local.theama.co), private predecessor-state reads, native plugin execution as munin and ordinary plugin-state updates from direct node fetches.' if node else 'Require actual old-set master polling before compatibility, or the committed expanded-node transaction before finalization. Finalization includes a bounded read-only SSH check on ama@10.1.0.51 (alias 10.1.0.137) for its committed receipt, service/file continuity and exact selection.'}
Read current native state only. Verify installed file readback and exact links,
native CLI output, both source-bound master-to-node TCP config/fetch passes and
query_ok/synced/pps_selected=1. Unknown generic fields fail; the two already-pending
genuine job ages remain explicit unknowns, not invented completions.
{'After restart, seed genuine samples over both source-bound families, wait a real 305 seconds, then require complete warm output. Cold empty diskstats fetch is permitted only during seeding. Local CLI or isolated qualification state is never copied into production.' if node else 'No cold-output exception during acceptance. Master source updates must preserve its running daemon identity; no reload is needed or submitted.'}
Independently verify hostname/CA/leaf-checked HTTPS HTML/CSS/existing PNG over
both master literals before mutation and before commit. These preserve serving
continuity; three scheduled expanded cycles/new graphs remain a later gate.

## Independent guard and owned recovery

Root-private stage `/var/lib/munin-generic-stages/{s['operation_id']}` with frozen
inputs, verified archive, exclusive lock and transaction backup/state. Arm the
existing independent systemd recovery machinery at 600 seconds before a detached
apply worker (300-second process cap, internal 240-second alarm). Apply returns
prepared; the controller performs independent acceptance before commit under
the same lock. Node warm-up is in this guarded prepared interval, not inside
the apply worker. Commit requires prepared state younger than 480 seconds;
only then disarm the timer. Guard/worker/controller writes and normal logs are
included. A lost controller cannot commit. No power-loss/reboot recovery claim:
those require fresh inspection and a separately approved continuation.

Before each rename, fsync bytes and record the temporary inode in private state.
{'Compatibility starts from the inspected two-link commissioning source and verifies its retained proof has the same inode/hash/owner/mode. Atomic replacement leaves that historical proof intact; new and restored source files have one link. Recovery restores original bytes/mode/ownership, without rejoining the historical proof inode.' if w.get('before_proof') else 'Require a single-link baseline and single-link newly published/restored files.'}
Recovery restores only the matching authored file inode/hash/mode and removes
only proven authored symlink inodes. Restore the prior running selection/settings
and start only munin-node when this node stage stopped it. Preserve foreign
file/link/backup drift with recovery-held; never clobber it. Master finalization
restores the compatible source, not the obsolete nine-only source. Keep RRD
history and ordinary native state. Caught known acceptance failure recovers;
uncertain transport leaves the independent guard armed. One same-bundle,
within-expiry read-only inspect is allowed after uncertainty; no replay.

No package install, DNS/network/radio/NFS policy, maintenance job, Munin
update/limits invocation, contact activation or notification. Contacts stay
disabled by the pinned main configuration. No reference-node contact.
After committed readback, synchronize only the bound repository mirrors using
the existing private scan/compare-before-write synchronizer. Concurrent repo
edits are held; production stays committed and reconciliation is reported open.
This approval covers only this ordered stage and its specified companion reads.
"""


def unpack(raw, digest, reserve=0):
    if len(raw) > 8388608 or sha(raw) != digest:
        raise ValueError('approved archive hash/size mismatch')
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:') as archive:
        entries = archive.getmembers()
        if (len(entries) != len(MEMBERS) or {m.name for m in entries} != MEMBERS
                or any(not m.isfile() or m.size > 1048576 for m in entries)):
            raise ValueError('closed bounded regular archive required')
        files = {m.name: archive.extractfile(m).read() for m in entries}
    if json.loads(files['manifest.json']) != {n: sha(v) for n, v in files.items() if n != 'manifest.json'}:
        raise ValueError('member digest mismatch')
    s = json.loads(files['spec.json'])
    w = s['worker']
    if (not re.fullmatch(r'munin-generic-(compatible|node|expanded)-[0-9]{8}-v[0-9]+', s['operation_id'])
            or w['operation_id'] != s['operation_id'] or w['role'] not in ('compatible', 'node', 'expanded')
            or not s['prepared_epoch'] <= time.time() < s['expires_epoch']-reserve
            or not 0 < s['expires_epoch']-s['prepared_epoch'] <= 86400
            or s['recovery_seconds'] != (20 if w.get('fixture') else 600)
            or files['review.md'] != review(s).encode()
            or sha(files['qualification.json']) != s['qualification_sha256']):
        raise ValueError('update scope/expiry/review mismatch')
    candidate = files['settings-after'] if w['role'] == 'node' else files['compatible.py' if w['role'] == 'compatible' else 'expanded.py']
    if base64.b64decode(w['candidate'], validate=True) != candidate:
        raise ValueError('candidate binding mismatch')
    if not w.get('fixture'):
        node = w['role'] == 'node'
        expected = ('10.1.0.51', 'ama', '10.1.0.137', 'j2-svntp1') if node else ('10.1.3.83', 'pi', 'svmf.local.theama.co', 'J1-SVMF')
        if tuple(s[k] if k != 'hostname' else w[k] for k in ('endpoint', 'user', 'host_key_alias', 'hostname')) != expected:
            raise ValueError('fixed target scope')
        if (w['target'] != ('/etc/munin/plugin-conf.d/ntp' if node else '/usr/local/munin/lib/plugins/ntp_transport_j2')
                or w['mode'] != (0o644 if node else 0o755) or w['transport_expected'] != {'v4': '1', 'v6': '1', 'mail': 'U'}
                or len(s['old_plugins']) != 9 or len(s['new_plugins']) != 33
                or len(w['additions']) != (24 if node else 0)):
            raise ValueError('fixed production selection/change boundary')
        if w['role'] == 'compatible':
            expected_proof = '/var/lib/munin-ntp-master/munin-master-commissioning-20261021-v1/proof-ntp_transport_j2'
            if (w.get('before_nlink') != 2 or w.get('before_proof') != expected_proof
                    or len(w.get('baseline_identity', [])) != 2 or not s.get('transport_metadata')):
                raise ValueError('inspected commissioning proof baseline required')
        elif w.get('before_nlink', 1) != 1 or 'before_proof' in w:
            raise ValueError('single-link successor baseline required')
        qualification = json.loads(files['qualification.json'])
        if (not qualification.get('passed') or any(qualification['sources'].get(n) != sha(files[n]) for n in SOURCES)
                or any(qualification['artifacts'].get(n) != sha(files[n]) for n in ('compatible.py', 'expanded.py', 'settings-after'))):
            raise ValueError('current executable inputs lack qualification')
    return s, files


def remote_program(files, raw, digest, action, operation):
    program = b"__name__='sealed_generic'\n__file__='/sealed/Munin/scripts/runner.py'\n"+files['runner.py']
    expression = (b'root_launch('+repr(raw).encode()+b','+repr(digest).encode()+b')') if action == 'apply' else (
        b'locked_worker(Path('+repr(str(STAGES/operation)).encode()+b'),'+repr(digest).encode()+b','+repr(action).encode()+b')')
    return program+b'\nprint(json.dumps('+expression+b'))\n'


def archive_files(raw):
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:') as archive:
        entries = archive.getmembers()
        if len(entries) > 128 or len({m.name for m in entries}) != len(entries) or any(not m.isfile() or m.size > 1048576 for m in entries):
            raise ValueError('bounded provenance archive required')
        return {m.name: archive.extractfile(m).read() for m in entries}


def root_launch(raw, digest):
    _, files = unpack(raw, digest, 900)
    return transaction(files).root_launch(raw, digest)


def locked_worker(directory, digest, action):
    # Staged caller verification precedes loading any executable from disk.
    raw = private(directory/'deployment.tar')
    _, files = unpack(raw, digest)
    return transaction(files).locked_worker(directory, digest, action)


def prerequisite_program(files, inspection, prerequisite, master, names=None, seed=False):
    """Root checks continuity/state; native protocol code itself runs as munin."""
    program = b'import types,json,os,base64\n'
    for key, name in (('helper.py', 'h'), ('observer.py', 'o'), ('base.py', 'b')):
        program += name.encode()+b'ns={"__name__":"module","__file__":"/sealed/module.py"}\nexec('+repr(files[key]).encode()+b','+name.encode()+b'ns)\n'+name.encode()+b'=types.SimpleNamespace(**'+name.encode()+b'ns)\n'
    program += b'ons["h"]=h\nspec='+repr(inspection).encode()+b'\nbefore=o.continuity(spec)\n'
    if prerequisite:
        program += (b'proof=json.loads(b.secure(__import__("pathlib").Path('+repr(prerequisite['path']).encode()+b'))[0])\n'
                    +b'assert proof.get("phase")=="committed" and proof.get("accepted") is True and proof.get("spec_sha256")=='+repr(prerequisite['worker_sha256']).encode()+b',"ordered predecessor is not committed"\n')
    if master:
        inner = b'import types,json,socket\n'
        for key, name in (('fields.py', 'f'), ('probe.py', 'p')):
            inner += name.encode()+b'ns={"__name__":"module","__file__":"/sealed/Munin/scripts/module.py"}\nexec('+repr(files[key]).encode()+b','+name.encode()+b'ns)\n'+name.encode()+b'=types.SimpleNamespace(**'+name.encode()+b'ns)\n'
        endpoints = [(2, '10.1.0.51', '10.1.3.83'), (10, 'fd36:5aa8:6971:1::51', 'fd36:5aa8:6971:1::83')]
        inner += b'print(json.dumps(p.both('+repr(endpoints).encode()+b','+repr(names).encode()+b',f.fields,'+repr(seed).encode()+b')))\n'
        program += (b'row=h.bounded(["/usr/sbin/runuser","-u","munin","--","/usr/bin/python3","-I","-B","-"],timeout=60,limit=2097152,payload='
                    +repr(inner).encode()+b')\nassert row.get("returncode")==0 and not row.get("error") and not row["stderr"],"native probe process failed"\nresult=json.loads(row["stdout"])\n')
    else:
        program += b'result={"complete":True,"prerequisite_committed":True}\n'
    program += b'after=o.continuity(spec)\nassert before==after,"companion continuity changed"\nprint(json.dumps(result))\n'
    return program


def execute(args):
    directory = args.directory.absolute()
    m = directory.lstat()
    if not stat.S_ISDIR(m.st_mode) or m.st_uid != os.getuid() or stat.S_IMODE(m.st_mode) != 0o700:
        raise ValueError('owner-private operation directory required')
    raw = private(directory/'deployment.tar')
    s, files = unpack(raw, args.sha256, 900 if args.action == 'execute' else 0)
    if s['worker'].get('fixture') or files['runner.py'] != Path(__file__).read_bytes():
        raise ValueError('frozen production controller required')
    for name, data in files.items():
        if private(directory/name) != data:
            raise ValueError('local frozen input drift')
    helper = module(files['helper.py'], 'helper')
    if args.action == 'inspect' and json.loads(private(directory/'execution.json'))['sha256'] != args.sha256:
        raise ValueError('same consumed approval required')
    receipt = 'inspection.json' if args.action == 'inspect' else 'execution.json'
    with (directory/receipt).open('xb') as stream:
        stream.write(encoded({'sha256': args.sha256, 'epoch': time.time()}))
        stream.flush()
        os.fsync(stream.fileno())
    def contact(target, program, label, timeout=390):
        argv = helper.ssh_argv({'endpoints': [target['endpoint']], 'host_key_alias': target['host_key_alias']}, directory)
        argv[-2] = target['user']+'@'+target['endpoint']
        row = helper.bounded(argv, timeout=timeout, limit=8388608, payload=program, env=os.environ.copy())
        (directory/(label+'-transport.json')).write_bytes(encoded(row))
        if row.get('returncode') != 0 or row.get('error'):
            raise RuntimeError('uncertain '+label+'; guard remains armed, inspect without replay')
        result = json.loads(row['stdout'])
        (directory/(label+'-result.json')).write_bytes(encoded(result))
        return result
    def remote(action):
        return contact(s, remote_program(files, raw, args.sha256, action, s['operation_id']), action)
    if args.action == 'inspect':
        return remote('inspect')
    result = {'archive_sha256': args.sha256, 'committed': False, 'accepted': False, 'repository_reconciled': False}
    def save():
        (directory/'result.json').write_bytes(encoded(result))
    def master_probe(label, names, seed=False):
        inspection = dict(s['master_inspection'])
        inspection['files'] = dict(inspection['files'])
        if s['worker']['role'] != 'compatible':
            inspection['files']['/usr/local/munin/lib/plugins/ntp_transport_j2'] = sha(files['compatible.py'])
        if label == 'after' and s['worker']['role'] == 'expanded':
            inspection['files']['/usr/local/munin/lib/plugins/ntp_transport_j2'] = sha(files['expanded.py'])
        if label == 'after' and s['worker']['role'] == 'compatible':
            inspection['files']['/usr/local/munin/lib/plugins/ntp_transport_j2'] = sha(files['compatible.py'])
        program = prerequisite_program(files, inspection, s.get('master_prerequisite') if s['worker']['role'] == 'node' else None,
                                       True, names, seed)
        value = contact(s['master_target'], program, 'protocol-'+label, 100)
        if not value.get('complete'):
            raise ValueError('known protocol acceptance failure: '+label)
        return value
    try:
        if s.get('predecessor_directory'):
            prior = json.loads(private(Path(s['predecessor_directory'])/'result.json'))
            required = s.get('master_prerequisite') or s['node_prerequisite']
            if prior.get('accepted') is not True or prior.get('archive_sha256') != required['archive_sha256']:
                raise ValueError('predecessor must be committed and repository-reconciled')
        if s.get('node_prerequisite'):
            program = prerequisite_program(files, s['node_inspection'], s['node_prerequisite'], False)
            contact(s['node_target'], program, 'node-prerequisite', 60)
        result['protocol_before'] = master_probe('before', s['old_plugins'] if s['worker']['role'] != 'expanded' else s['new_plugins'])
        tx = transaction(files)
        result['https_before'] = tx.health(s, files)
    except Exception as error:
        result.update(phase='preflight-failed', error=str(error))
        save()
        return result
    try:
        applied = remote('apply')
    except Exception as error:
        result.update(error=str(error), recovery='outcome uncertain; inspect, do not replay')
        save()
        raise
    result['apply'] = applied
    save()
    if applied.get('phase') != 'prepared':
        return result
    try:
        if s['worker']['role'] == 'node':
            result['seed'] = master_probe('seed', s['new_plugins'], True)
            save()
            due = time.monotonic()+305
            while time.monotonic() < due:
                time.sleep(min(30, due-time.monotonic()))
            result['warm_interval_complete'] = True
        result['protocol_after'] = master_probe('after', s['new_plugins'] if s['worker']['role'] != 'compatible' else s['old_plugins'])
        result['https_after'] = transaction(files).health(s, files)
    except ValueError as error:
        result.update(acceptance_error=str(error), recovery=remote('recover'))
        save()
        return result
    except Exception as error:
        # Unknown transport must not create a second concurrent mutation.
        result.update(acceptance_error=str(error), recovery='independent guard armed; inspect')
        save()
        raise
    try:
        result['commit'] = remote('commit')
    except Exception as error:
        result.update(error=str(error), recovery='commit uncertain; inspect, do not replay')
        save()
        raise
    result['committed'] = result['commit'].get('phase') == 'committed' and result['commit'].get('accepted') is True
    save()
    if result['committed']:
        sync = module(files['sync.py'], 'synchronizer')
        try:
            for mirror in s['mirrors']:
                sync.synchronize(files[mirror['after']], Path(mirror['path']), write=True, expected_before=files[mirror['before']])
            result['repository_reconciled'] = True
        except Exception as error:
            result['repository_reconciliation_error'] = str(error)
    result['accepted'] = result['committed'] and result['repository_reconciled']
    save()
    return result


def seal(args):
    sources = {name: path.read_bytes() for name, path in SOURCES.items()}
    common = module(sources['data-utils.py'], 'data')
    qraw = common.private(args.native/'qualification.tar')
    qfiles = archive_files(qraw)
    qs = json.loads(qfiles['spec.json'])
    qo = json.loads(common.private(args.native/'outcome.json'))
    capture = json.loads(common.private(args.native/'stdout.txt'))
    if (not qo.get('native_qualification_accepted') or qo['archive_sha256'] != sha(qraw)
            or not capture.get('capture_complete') or capture['spec_sha256'] != sha(qfiles['spec.json'])
            or capture['before'] != capture['after'] or len(capture['tested_plugins']) != 33):
        raise ValueError('accepted full native qualification required')
    commission, mo, mp = common.accepted(args.commissioning, 'accepted')
    if not mo.get('committed') or not mo.get('repository_reconciled'):
        raise ValueError('committed reconciled master required')
    master_raw = common.private(args.master_inventory/'inspection.tar')
    master_files = archive_files(master_raw)
    ms = json.loads(master_files['spec.json'])
    mr = json.loads(common.private(args.master_inventory/'result.json'))
    mc = json.loads(common.private(args.master_inventory/'stdout.txt'))
    if (not mr.get('capture_complete') or mr['bundle_sha256'] != sha(master_raw) or mr['returncode'] != 0
            or mc['spec_sha256'] != sha(master_files['spec.json']) or ms['kind'] != 'master'):
        raise ValueError('accepted master inventory required')
    role = args.role
    files = dict(sources)
    files.update({'known_hosts': b'\n'.join(sorted(set((qfiles['known_hosts']+b'\n'+commission['known_hosts']).splitlines())))+b'\n',
                  'ca.pem': commission['ca.pem'], 'compatible.py': (ROOT/'master/plugins/ntp_transport_j2.compatible.candidate').read_bytes(),
                  'expanded.py': (ROOT/'master/plugins/ntp_transport_j2.expanded.candidate').read_bytes(),
                  'profile-before.json': (ROOT/'node/profiles/ntp/profile.json').read_bytes(),
                  'settings-before': (ROOT/'node/plugin-conf.d/ntp.conf').read_bytes(),
                  'settings-after': (ROOT/'node/plugin-conf.d/ntp-expanded.candidate.conf').read_bytes(),
                  'transport-before': commission['plugin'], 'qualification.json': common.private(args.qualification)})
    profile = json.loads(files['profile-before.json'])
    candidate = json.loads((ROOT/'node/profiles/ntp/generic-parity.candidate.json').read_text())
    profile.update(package_plugins=candidate['proposed_package_plugins'], status='expanded profile; assignment and deployment acceptance recorded separately')
    files['profile-after.json'] = (json.dumps(profile, indent=2)+'\n').encode()
    now = int(time.time())
    old, new = sorted(qs['enabled_links']), sorted(capture['tested_plugins'])
    if set(new) != set(candidate['requires_coordinated_master_expected_set']):
        raise ValueError('native qualified selection drift')
    before = files['settings-before'] if role == 'node' else files['transport-before'] if role == 'compatible' else files['compatible.py']
    after = files['settings-after'] if role == 'node' else files['compatible.py' if role == 'compatible' else 'expanded.py']
    inspection = qs if role == 'node' else ms
    target = '/etc/munin/plugin-conf.d/ntp' if role == 'node' else '/usr/local/munin/lib/plugins/ntp_transport_j2'
    protected = dict(inspection['files'])
    protected.pop(target, None)
    plugins_before = {n: ['link', p] for n, p in qs['enabled_links'].items()} if role == 'node' else None
    additions = {n: qs['plugins'][n] for n in new if n not in old} if role == 'node' else {}
    w = {'operation_id': args.output.name, 'role': role, 'target': target, 'mode': 0o644 if role == 'node' else 0o755,
         'hostname': inspection['hostname'], 'boot_id': inspection['boot_id'], 'units': inspection['units'],
         'protected': protected, 'plugins_before': plugins_before, 'additions': additions,
         'source_hashes': {p: qs['files'][p] for p in additions.values()}, 'before_sha256': sha(before),
         'candidate': base64.b64encode(after).decode(), 'transport_expected': {'v4': '1', 'v6': '1', 'mail': 'U'},
         'listen_addresses': ['10.1.0.51', 'fd36:5aa8:6971:1::51'], 'fixture': False}
    metadata_provenance = None
    if role == 'compatible':
        if not args.transport_metadata:
            raise ValueError('accepted read-only transport metadata required')
        directory = args.transport_metadata
        inspection_raw = common.private(directory/'inspection.tar')
        inventory = archive_files(inspection_raw)
        metadata_spec = json.loads(inventory['spec.json'])
        metadata_result = json.loads(common.private(directory/'result.json'))
        metadata_raw = common.private(directory/'stdout.txt')
        metadata_capture = json.loads(metadata_raw)
        observed = metadata_capture['observations']
        meta = observed['metadata']
        if (not metadata_result.get('capture_complete') or metadata_result.get('returncode') != 0
                or metadata_result['bundle_sha256'] != sha(inspection_raw)
                or metadata_spec.get('purpose') != 'transport-metadata' or metadata_spec['boot_id'] != ms['boot_id']
                or metadata_capture['spec_sha256'] != sha(inventory['spec.json'])
                or not metadata_capture.get('capture_complete') or metadata_capture['before'] != metadata_capture['after']
                or observed['path'] != target or observed['selection']['target'] != target
                or {k: meta[k] for k in ('sha256', 'mode', 'uid', 'gid', 'nlink')} !=
                    {'sha256': sha(before), 'mode': 0o755, 'uid': 0, 'gid': 0, 'nlink': 2}):
            raise ValueError('inspected metadata does not establish expected shared baseline')
        w.update(before_nlink=2, baseline_identity=[meta['device'], meta['inode']],
                 before_proof='/var/lib/munin-ntp-master/'+json.loads(commission['spec.json'])['worker']['operation_id']+'/proof-ntp_transport_j2')
        metadata_provenance = {'archive_sha256': sha(inspection_raw), 'capture_sha256': sha(metadata_raw)}
    spec = {'operation_id': args.output.name, 'prepared_epoch': now, 'expires_epoch': now+86400,
            'recovery_seconds': 600, 'worker': w, 'old_plugins': old, 'new_plugins': new,
            'endpoint': inspection['endpoint'], 'user': inspection['user'], 'host_key_alias': inspection['host_key_alias'],
            'master_inspection': ms, 'node_inspection': qs,
            'master_target': {k: ms[k] for k in ('endpoint', 'user', 'host_key_alias')},
            'node_target': {k: qs[k] for k in ('endpoint', 'user', 'host_key_alias')},
            'qualification_sha256': sha(files['qualification.json']),
            'native_qualification_sha256': sha(qraw), 'commissioning': mp,
            'addresses': ['10.1.3.83', 'fd36:5aa8:6971:1::83'], 'leaf_sha256': ms['leaf_sha256'],
            'paths': ['/', '/static/style-new.css', '/munin-cgi/munin-cgi-graph/J1-SVMF/J1-SVMF/apache_accesses-day.png']}
    if metadata_provenance:
        spec['transport_metadata'] = metadata_provenance
    if role != 'compatible':
        if not args.previous:
            raise ValueError('ordered predecessor bundle required')
        previous_raw = common.private(args.previous/'deployment.tar')
        previous, _ = unpack(previous_raw, sha(previous_raw))
        if previous['worker']['role'] != ('compatible' if role == 'node' else 'node'):
            raise ValueError('wrong ordered predecessor')
        requirement = {'path': str(STAGES/previous['operation_id']/'transaction/state.json'),
                       'worker_sha256': sha(encoded(previous['worker'])), 'archive_sha256': sha(previous_raw)}
        spec['master_prerequisite' if role == 'node' else 'node_prerequisite'] = requirement
        spec['predecessor_directory'] = str(args.previous.absolute())
    # The node will restart: pin its actual package unit and accepted original
    # permit guard, not just the process that happens to be running now.
    node_archive, _, node_provenance = common.accepted(args.node_baseline, 'node_runtime_accepted')
    if node_provenance['archive_sha256'] != qs['provenance']['node']['archive_sha256']:
        raise ValueError('accepted startup-guard provenance mismatch')
    original_worker = json.loads(node_archive['spec.json'])['worker']
    package = next(p for p in original_worker['installation']['packages'] if p['package'] == 'munin-node')
    if sha(args.node_package.read_bytes()) != package['sha256']:
        raise ValueError('approved native unit package mismatch')
    archive = subprocess.check_output(['/usr/bin/dpkg-deb', '--fsys-tarfile', str(args.node_package)])
    with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
        unit_raw = stream.extractfile('./usr/lib/systemd/system/munin-node.service').read()
    permit = str(Path(original_worker['original_state_path']).parent/'permit')
    guard = '/etc/systemd/system/munin-node.service.d/00-ntp-install.conf'
    guard_raw = ('[Unit]\nConditionPathExists='+permit+'\n').encode()
    startup = {'/usr/lib/systemd/system/munin-node.service': sha(unit_raw), guard: sha(guard_raw), permit: sha(b'')}
    if role == 'node':
        w['protected'].update(startup)
        w['node_unit_layout'] = {'FragmentPath': '/usr/lib/systemd/system/munin-node.service', 'DropInPaths': guard}
    if role == 'expanded':
        spec['node_inspection'] = dict(qs, files=dict(qs['files'], **startup))
        spec['node_inspection']['files']['/etc/munin/plugin-conf.d/ntp'] = sha(files['settings-after'])
    if role == 'node':
        spec['mirrors'] = [{'path': str(ROOT/'node/plugin-conf.d/ntp.conf'), 'before': 'settings-before', 'after': 'settings-after'},
                           {'path': str(ROOT/'node/profiles/ntp/profile.json'), 'before': 'profile-before.json', 'after': 'profile-after.json'}]
    else:
        spec['mirrors'] = [{'path': str(ROOT/'master/plugins/ntp_transport_j2'),
                            'before': 'transport-before' if role == 'compatible' else 'compatible.py',
                            'after': 'compatible.py' if role == 'compatible' else 'expanded.py'}]
    tx = transaction(files)
    tx.review, tx.MEMBERS = review, MEMBERS
    digest = tx.write_archive(args.output, spec, files)
    return {'sha256': digest, 'target_contact': False, 'role': role, 'expires_epoch': spec['expires_epoch']}


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    q = sub.add_parser('seal')
    q.add_argument('--role', choices=('compatible', 'node', 'expanded'), required=True)
    for name in ('native', 'commissioning', 'master-inventory', 'node-baseline', 'node-package', 'qualification', 'output'):
        q.add_argument('--'+name, type=Path, required=True)
    q.add_argument('--previous', type=Path)
    q.add_argument('--transport-metadata', type=Path)
    for action in ('check', 'execute', 'inspect', 'root'):
        q = sub.add_parser(action)
        q.add_argument('--directory', type=Path, required=True)
        q.add_argument('--sha256', required=True)
        if action == 'root':
            q.add_argument('--action', dest='root_action', choices=('apply', 'commit', 'recover', 'inspect'), required=True)
    args = parser.parse_args()
    if args.action == 'seal':
        result = seal(args)
    elif args.action == 'root':
        result = locked_worker(args.directory, args.sha256, args.root_action)
    elif args.action == 'check':
        raw = private(args.directory/'deployment.tar')
        spec, files = unpack(raw, args.sha256)
        if files['runner.py'] != Path(__file__).read_bytes():
            raise ValueError('frozen controller required')
        result = {'verified': True, 'target_contact': False, 'role': spec['worker']['role']}
    else:
        result = execute(args)
    print(json.dumps(result))
    if args.action == 'execute' and not result.get('accepted'):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
