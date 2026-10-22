#!/usr/bin/python3
"""Seal dedicated gated contact activation and separate exact-payload send reviews."""
import argparse
import base64
import difflib
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import tarfile
import time
import types

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent.parent
STAGES = Path('/var/lib/munin-ntp-contact-stages')
PROOF = '/var/lib/munin-ntp-master/munin-master-commissioning-20261021-v1/config-proof'
SOURCES = {
    'runner.py': Path(__file__), 'worker.py': ROOT/'scripts/install_ntp_contacts.py',
    'gate.py': ROOT/'scripts/ntp_contact_gate.py', 'mailrise.py': ROOT/'scripts/ntp_mailrise.py',
    'engine.py': ROOT/'scripts/deploy_ntp_master.py', 'base.py': ROOT/'scripts/install_ntp_node.py',
    'qualifier.py': ROOT/'scripts/qualify_master.py', 'sync.py': ROOT/'scripts/sync_master_baseline.py',
    'helper.py': WORKSPACE/'homelab-ntp/ntpsec/scripts/run-production-inspection.py',
    'tls-probe.py': WORKSPACE/'homelab-network/Ubiquiti/munin-master-profile/qualify_dashboard.py',
    'test-native.py': ROOT/'tests/test_contacts_native.py',
    'test-offline.py': ROOT/'tests/test_contacts.py',
    'native-runner.py': ROOT/'tests/run_contacts_native.py',
    'contact-example.conf': ROOT/'master/configs/j2-svntp1.conf.example',
    'test-limits.py': ROOT/'tests/test_limits_native.py',
}
MEMBERS = set(SOURCES) | {'spec.json', 'review.md', 'manifest.json', 'qualification.json',
    'production-before.conf', 'repository-before.conf', 'candidate.conf', 'message.eml',
    'preview.txt', 'ca.pem', 'known_hosts', 'candidate.diff', 'metadata-evidence.json'}
CASES = {'success', 'restore', 'rejection', 'worker-loss', 'controller-loss',
         'foreign-config', 'foreign-helper', 'foreign-state', 'preflight-drift',
         'commit-loss', 'ambiguous-send', 'publication-loss', 'suppressed-call',
         'proof-preflight-drift', 'proof-foreign-recovery', 'unexpected-main-link'}
NATIVE_MODULES = {'/usr/share/perl5/Munin/' + p for p in ('Common/Config.pm', 'Master/Config.pm',
    'Master/Utils.pm', 'Master/LimitsOld.pm', 'Master/GraphOld.pm', 'Master/Update.pm', 'Master/UpdateWorker.pm')}


def encoded(value):
    return (json.dumps(value, sort_keys=True) + '\n').encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def module(raw, name):
    namespace = {'__name__': name, '__file__': '/sealed/Munin/scripts/' + name + '.py'}
    exec(compile(raw, namespace['__file__'], 'exec'), namespace)
    return types.SimpleNamespace(**namespace)


def private(path):
    path = Path(path)
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('indirect private input')
    with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK), 'rb') as stream:
        m = os.fstat(stream.fileno())
        if not stat.S_ISREG(m.st_mode) or m.st_uid != os.getuid() or stat.S_IMODE(m.st_mode) != 0o600 or m.st_nlink != 1 or m.st_size > 8*1048576:
            raise ValueError('bounded owner-private regular input required')
        raw = stream.read(8*1048576 + 1)
        after = os.fstat(stream.fileno())
    if len(raw) > 8*1048576 or (m.st_size, m.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError('private input changed')
    return raw


def private_directory(path):
    m = path.lstat()
    if not stat.S_ISDIR(m.st_mode) or m.st_uid != os.getuid() or stat.S_IMODE(m.st_mode) != 0o700 or path.is_symlink():
        raise ValueError('owner-private operation directory required')


def proof_from_evidence(evidence, worker):
    """Bind the sole shared-file exception to the completed read-only diagnostic."""
    capture, spec = evidence['capture'], evidence['spec']
    result, receipt, outcome = (evidence[k] for k in ('result', 'receipt', 'outcome'))
    observed = capture['observations']
    main, proof = observed['main'], observed['predecessor_proof']
    expected_matches = {'uid': True, 'gid': True, 'mode': True, 'sha256': True, 'nlink': False}
    if (spec.get('purpose') != 'contact-metadata' or spec.get('kind') != 'master'
            or spec.get('operation_id') != 'munin-contact-config-metadata-20261022-v1'
            or spec.get('hostname') != worker['hostname'] or spec.get('endpoint') != '10.1.3.83'
            or spec.get('boot_id') != worker['boot_id'] or spec.get('units') != worker['units']
            or capture.get('spec_sha256') != sha(encoded(spec))
            or capture.get('operation_id') != spec['operation_id']
            or capture.get('target_mutation') is not False or not capture.get('capture_complete')
            or capture['before'] != capture['after'] or capture['before']['units'] != worker['units']
            or capture['before']['file_hashes'] != spec['files']
            or {p: h for p, h in spec['files'].items() if p != '/etc/munin/munin.conf'} != worker['protected_files']
            or spec['files']['/etc/munin/munin.conf'] != worker['before_sha256']
            or result.get('returncode') != 0 or not result.get('capture_complete')
            or result.get('bundle_sha256') != evidence['archive_sha256']
            or receipt.get('sha256') != evidence['archive_sha256']
            or outcome.get('archive_sha256') != evidence['archive_sha256']
            or not outcome.get('diagnosis_accepted') or outcome.get('target_mutation') is not False
            or main['path'] != '/etc/munin/munin.conf'
            or proof['path'] != PROOF
            or main['metadata'] != proof['metadata']
            or main['matches'] != expected_matches or proof['matches'] != expected_matches
            or observed.get('same_inode_as_predecessor_proof') is not True):
        raise ValueError('accepted exact contact metadata provenance required')
    m = main['metadata']
    if ((m['uid'], m['gid'], m['mode'], m['nlink'], m['sha256']) != (0, 0, 0o644, 2, worker['before_sha256'])
            or type(m['inode']) is not int or m['inode'] <= 0 or type(m['device']) is not int
            or not 0 < m['size'] <= 262144 or type(m['mtime']) not in (int, float)):
        raise ValueError('fixed proof metadata required')
    for path in ('/usr/local/libexec/munin-ntp-mailrise.py', '/usr/local/libexec/munin-ntp-contact-gate.py',
                 '/var/lib/munin-ntp-contact-control', '/var/lib/munin/ntp-alerts'):
        if observed['presence'][path] != {'missing': True}:
            raise ValueError('contact destinations must have been absent')
    return {k: m[k] for k in ('device', 'inode', 'size', 'mtime', 'sha256')}


def review(spec):
    header = ('Operation ' + spec['operation_id'] + '; expires epoch ' + str(spec['expires_epoch']) + '.\n'
              'Approve only deployment.tar SHA-256 in sealing.json. One receipt, no replay.\n'
              'Fixed master pi@10.1.3.83, strict alias svmf.local.theama.co, J1-SVMF.\n')
    if spec['kind'] == 'activation':
        return ('# Dedicated gated contact activation and conditional restoration\n\n' + header + '''
Preserve the operator's repository stanza layout. Install the pinned helper
and gate root:root 0755, private munin:munin 0700 alert-state directory, root
0755 gate directory/0644 lock, and the preserving main-config candidate.
Global/j2 contacts remain none; only eight explicit NTP graphs plus master
transport select ntp_mailrise. No packages, collection, limits, jobs, cron,
Apache, Munin-node, NTP-node, network or RRD action. Never preseed status success.

All effective includes must stay empty. Pin boot, protected units/files,
native modules, original main bytes/metadata, source and both before hashes.
The sole shared-file exception pins the observed commissioning proof path,
device/inode, bytes, size, mtime, root:root 0644 and exactly two links while
main still shares it. Before replacement recheck that relationship; afterwards
the untouched proof must have exactly one link. Other authored files remain
single-link only. Never write, unlink or normalize the historical proof.
Uncommitted restoration republishes saved original bytes as an independent
root:root 0644 single-link main file; the proof remains unchanged/single-link.
Foreign proof changes or extra links hold recovery without overwriting them.
Native in-memory parsing and six verified HTTPS checks before/after precede
commit; no contact command is invoked for acceptance. Ordinary scheduler
contact calls before enable fail closed with exit 75, no SMTP or status write.
They are not queued/retried/backfilled; scheduled activation remains a later
acceptance gate. No timer/schedule is stopped to manufacture quietness.
An actual pre-commit call records suppression evidence and prevents commit;
the guard restores inactive configuration and preserves that evidence.

An exclusive stage lock, durable publication inode intents and independent
600-second systemd guard protect the uncommitted change. Known rejection
restores only matching authored main/helper/gate bytes and empty directories.
Preserve real submission records and foreign edits; mismatch holds recovery.
Completed recovery is idempotent. Controller/worker loss before durable commit
recovers independently. Never replay; one same-bundle read-only inspect is allowed.

First-send boundary: persist the committed decision while the gate is disabled,
then publish the hash-bound enable marker under the gate's exclusive lock.
This approval authorizes ordinary automatic notifications for exactly those
nine graph origins only after marker publication, including real state changes
which occur immediately afterwards. It does not authorize the controlled tests.
If the committer dies after the decision but before enabling, contacts remain
disabled/held; the guard does not undo or complete a committed decision. Inspect
and prepare a new continuation. A submitted message cannot be recalled.
Post-commit rollback requires a new inspected review. Long-lived contact calls
validate the marker and current config/helper/gate hashes under a shared lock.

After accepted commit reconcile the repository against its separate pinned
before bytes. Foreign local edits hold reconciliation. Preserve all evidence.
Genuine scheduled use and downstream alert delivery are not accepted here.
''')
    label = spec['message_label']
    return ('# One-use exact ' + label + ' delivery test\n\n' + header + '''
Only message.eml may be submitted, exactly as pinned by message_sha256 in
spec.json; preview.txt exposes every header/body and confirms no attachments.
Sender munin@local.theama.co; target is only master-loopback Mailrise
127.0.0.1:8025, SMTP timeout ten seconds, one attempt and no retries. No real
fault, limits/update/plugin/job/service/config/network or RRD action.

Require accepted/committed/reconciled activation, its exact worker token and
installed helper/gate/config hashes. A separate local fsynced receipt is
consumed before target contact; a root-private remote receipt is fsynced
before dropping permanently to munin UID/GID and attempting SMTP. Hold the
gate lock during the attempt so ordinary contact submissions cannot race this
test's status update. Write genuine helper submission status only after the
attempt; a status-write failure never permits a repeat send. Capture all
stdout/stderr/transport status privately. No Proton Mail/sendmail/alternate route.

Changing Date, Message-ID, bytes, recipient, body or attachments requires a
new hash and approval. Timeout or lost transport leaves the receipt consumed
and submission uncertain; do not replay. SMTP acceptance proves submission
only; Aaron's explicit downstream receipt confirmation is still required.
Recovery additionally requires an operator confirmation bound to the exact
problem archive/message/consumed receipt. No confirmation is synthesized.
No contact activation approval substitutes for either exact-message approval.

Exact reviewed payload SHA-256: ''' + spec['message_sha256'] + '\n\n' + spec['preview'])


def unpack(raw, digest, reserve=0):
    if len(raw) > 8*1048576 or sha(raw) != digest:
        raise ValueError('approved archive hash/size mismatch')
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:') as archive:
        entries = archive.getmembers()
        if len(entries) != len(MEMBERS) or {m.name for m in entries} != MEMBERS or any(not m.isfile() or m.size > 1048576 for m in entries):
            raise ValueError('closed bounded regular archive required')
        files = {m.name: archive.extractfile(m).read() for m in entries}
    if json.loads(files['manifest.json']) != {n: sha(v) for n, v in files.items() if n != 'manifest.json'}:
        raise ValueError('closed manifest mismatch')
    s = json.loads(files['spec.json'])
    w = s['worker']
    control = module(files['worker.py'], 'contact_control')
    kind = s.get('kind')
    if (kind not in ('activation', 'problem', 'recovery')
            or not re.fullmatch(r'munin-contacts-(?:activate|problem|recovery)-[0-9]{8}-v[1-9][0-9]*', s['operation_id'])
            or w['operation_id'] != s['operation_id']
            or not s['prepared_epoch'] <= time.time() < s['expires_epoch'] - reserve
            or not 0 < s['expires_epoch'] - s['prepared_epoch'] <= 86400
            or files['review.md'] != review(s).encode()
            or sha(files['production-before.conf']) != w['before_sha256']
            or sha(files['candidate.conf']) != w['candidate_sha256']
            or files['candidate.conf'] != control.render(files['repository-before.conf'])
            or control.directives(files['production-before.conf']) != control.directives(files['repository-before.conf'])
            or w['artifacts'] != {k: base64.b64encode(files[n]).decode() for k, n in
                (('config', 'candidate.conf'), ('repository', 'repository-before.conf'), ('helper', 'mailrise.py'), ('gate', 'gate.py'))}):
        raise ValueError('closed contact scope/baseline/expiry binding')
    identity_kind = 'activate' if kind == 'activation' else kind
    if not s['operation_id'].startswith('munin-contacts-' + identity_kind + '-'):
        raise ValueError('operation kind mismatch')
    if not w.get('fixture'):
        if (w['hostname'] != 'J1-SVMF' or w.get('test_fault') or s['recovery_seconds'] != 600
                or s['repository_target'] != '/home/aaron/code/homelab-monitoring-observability/Munin/master/configs/munin.conf'):
            raise ValueError('fixed production scope required')
        if w.get('predecessor_proof') != proof_from_evidence(json.loads(files['metadata-evidence.json']), w):
            raise ValueError('exact observed proof binding required')
        q = json.loads(files['qualification.json'])
        native = {p: h for p, h in w['protected_files'].items() if p.startswith('/usr/share/perl5/Munin/')}
        if (not q.get('passed') or not q.get('source_inputs_unchanged')
                or set(native) != NATIVE_MODULES
                or set(w['units']) != {'NetworkManager.service', 'apache2.service', 'cron.service', 'munin-node.service'}
                or q.get('sources') != {n: sha(files[n]) for n in SOURCES}
                or {c['case'] for c in q.get('cases', []) if c.get('passed')} != CASES
                or q.get('native_module_hashes') != native):
            raise ValueError('all current executable inputs must be qualified')
    if kind != 'activation':
        if s['message_label'] != kind or sha(files['message.eml']) != s['message_sha256']:
            raise ValueError('one exact message required')
        control.validate_message(files['message.eml'], kind)
        if files['preview.txt'] != s['preview'].encode():
            raise ValueError('reviewed preview drift')
        if s['activation_prerequisite']['config_sha256'] != w['candidate_sha256']:
            raise ValueError('activation configuration binding')
    elif files['message.eml'] or files['preview.txt']:
        raise ValueError('activation authorizes no controlled test')
    return s, files


def write_archive(output, spec, files):
    files = dict(files, **{'spec.json': encoded(spec), 'review.md': review(spec).encode()})
    files['manifest.json'] = encoded({n: sha(v) for n, v in files.items()})
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w') as archive:
        for name, data in sorted(files.items()):
            info = tarfile.TarInfo(name)
            info.mode = 0o600
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
    raw = buffer.getvalue()
    digest = sha(raw)
    unpack(raw, digest)
    output.mkdir(mode=0o700)
    for name, data in files.items():
        with (output/name).open('xb') as stream:
            stream.write(data)
    (output/'deployment.tar').write_bytes(raw)
    (output/'sealing.json').write_bytes(encoded({'sha256': digest, 'expires_epoch': spec['expires_epoch'],
                                               'execution_ready': True, 'target_contact': False, 'messages_sent': False}))
    return digest


def engine(files):
    e = module(files['engine.py'], 'contact_engine')
    # Reuse only the repository engine's qualified launch/lock/timer mechanics;
    # its commissioning scope/installer are never selected or replayed.
    e.unpack = unpack
    e.STAGES = STAGES
    e.root_launch.__globals__.update(unpack=unpack, STAGES=STAGES)
    return e


def root_launch(raw, digest):
    spec, files = unpack(raw, digest, 900)
    if spec['kind'] != 'activation':
        raise ValueError('send stages cannot launch a mutation worker')
    return engine(files).root_launch(raw, digest)


def locked_worker(directory, digest, action):
    raw = private(directory/'deployment.tar')
    spec, files = unpack(raw, digest)
    if spec['kind'] != 'activation' or directory != STAGES/spec['operation_id']:
        raise ValueError('fixed contact activation stage required')
    result = engine(files).locked_worker(directory, digest, action)
    if action == 'inspect':
        state_path = Path('/var/lib/munin-ntp-contacts')/spec['operation_id']/'state.json'
        if state_path.exists():
            result['enable_pending'] = json.loads(module(files['base.py'], 'base').secure(state_path)[0]).get('enable_pending', False)
        gate = module(files['gate.py'], 'contact_gate')
        try:
            result['contacts_enabled'] = gate.enabled()['operation_id'] == spec['operation_id']
        except Exception as error:
            result.update(contacts_enabled=False, gate_finding=str(error))
    return result


def confirmation(spec, context):
    if spec['kind'] != 'recovery':
        return
    ack = context.get('problem_confirmation', {})
    if (ack.get('archive_sha256') != spec['problem_prerequisite']['archive_sha256']
            or ack.get('message_sha256') != spec['problem_prerequisite']['message_sha256']
            or ack.get('source') != 'operator' or ack.get('delivered') is not True
            or not isinstance(ack.get('acknowledgement'), str) or not ack['acknowledgement'].strip()
            or not re.fullmatch(r'[a-f0-9]{64}', ack.get('execution_receipt_sha256', ''))):
        raise ValueError('explicit operator confirmation of the exact problem delivery required')


def send_root(raw, digest, context):
    spec, files = unpack(raw, digest)
    if spec['kind'] == 'activation':
        raise ValueError('activation is not a test send')
    confirmation(spec, context)
    return module(files['worker.py'], 'contact_control').send_exact(spec, digest, files, module(files['base.py'], 'base'))


def payload(files, raw, digest, action, spec, context):
    code = b"__name__='sealed_contact'\n__file__='/sealed/Munin/scripts/runner.py'\n" + files['runner.py']
    if action == 'apply':
        call = 'root_launch(' + repr(raw) + ',' + repr(digest) + ')'
    elif action == 'send':
        call = 'send_root(' + repr(raw) + ',' + repr(digest) + ',' + repr(context) + ')'
    else:
        call = 'locked_worker(Path(' + repr(str(STAGES/spec['operation_id'])) + '),' + repr(digest) + ',' + repr(action) + ')'
    return code + b'\nprint(json.dumps(' + call.encode() + b'))\n'


def execute(args):
    directory = args.directory.absolute()
    private_directory(directory)
    raw = private(directory/'deployment.tar')
    spec, files = unpack(raw, args.sha256, 900 if args.action == 'execute' else 0)
    if files['runner.py'] != Path(__file__).read_bytes() or spec['worker'].get('fixture'):
        raise ValueError('frozen production controller required')
    for name, data in files.items():
        if private(directory/name) != data:
            raise ValueError('local frozen input drift')
    context = {}
    if spec['kind'] != 'activation':
        previous = Path(spec['activation_prerequisite']['directory'])
        prior = json.loads(private(previous/'result.json'))
        receipt = json.loads(private(previous/'execution.json'))
        if (not all(prior.get(k) is True for k in ('accepted', 'committed', 'repository_reconciled'))
                or prior.get('archive_sha256') != spec['activation_prerequisite']['archive_sha256']
                or receipt.get('sha256') != prior['archive_sha256']):
            raise ValueError('accepted exact activation required before send contact')
        context['activation_result_sha256'] = sha(private(previous/'result.json'))
        if spec['kind'] == 'recovery':
            problem = Path(spec['problem_prerequisite']['directory'])
            ack = json.loads(private(problem/'delivery-confirmation.json'))
            if ack.get('execution_receipt_sha256') != sha(private(problem/'execution.json')):
                raise ValueError('problem receipt confirmation mismatch')
            context['problem_confirmation'] = ack
        confirmation(spec, context)
    if args.action == 'inspect' and spec['kind'] != 'activation':
        raise ValueError('send receipt cannot be replayed; inspect retained evidence separately')
    if args.action == 'inspect' and json.loads(private(directory/'execution.json'))['sha256'] != args.sha256:
        raise ValueError('same consumed activation approval required')
    (directory/'runtime-context.json').write_bytes(encoded(context))
    with (directory/('execution.json' if args.action == 'execute' else 'inspection.json')).open('xb') as stream:
        stream.write(encoded({'sha256': args.sha256, 'epoch': time.time(), 'runtime_context_sha256': sha(encoded(context))}))
        stream.flush()
        os.fsync(stream.fileno())
    sync_fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(sync_fd)
    finally:
        os.close(sync_fd)
    helper = module(files['helper.py'], 'inspection_helper')
    argv = helper.ssh_argv({'endpoints': ['10.1.3.83'], 'host_key_alias': 'svmf.local.theama.co'}, directory)
    argv[-2] = 'pi@10.1.3.83'
    def remote(action):
        row = helper.bounded(argv, timeout=390 if spec['kind'] == 'activation' else 90,
                             limit=8*1048576, payload=payload(files, raw, args.sha256, action, spec, context), env=os.environ.copy())
        (directory/(action+'-transport.json')).write_bytes(encoded(row))
        if row.get('returncode') != 0 or row.get('error'):
            raise RuntimeError('uncertain ' + action + '; receipt consumed; inspect, never replay')
        value = json.loads(row['stdout'])
        (directory/(action+'-result.json')).write_bytes(encoded(value))
        return value
    if args.action == 'inspect':
        return remote('inspect')
    result = {'archive_sha256': args.sha256, 'accepted': False, 'delivery_accepted': False}
    try:
        if spec['kind'] != 'activation':
            result.update(remote('send'))
            result['accepted'] = result.get('submission_accepted') is True and result.get('status_recorded') is True
        else:
            e = engine(files)
            result['https_before'] = e.health(spec, files)
            result['apply'] = remote('apply')
            if result['apply'].get('phase') == 'prepared':
                try:
                    result['https_after'] = e.health(spec, files)
                except Exception as error:
                    result.update(acceptance_error=str(error), recovery=remote('recover'))
                    return result
                result['commit'] = remote('commit')
                result['committed'] = result['commit'].get('phase') == 'committed' and result['commit'].get('accepted') is True
                result['repository_reconciled'] = False
                if result['committed']:
                    try:
                        syncer = module(files['sync.py'], 'baseline_sync')
                        syncer.synchronize(files['candidate.conf'], Path(spec['repository_target']), write=True,
                                           expected_before=files['repository-before.conf'])
                        result['repository_reconciled'] = True
                    except Exception as error:
                        result['repository_reconciliation_error'] = str(error)
                result['accepted'] = bool(result.get('committed') and result.get('repository_reconciled'))
    except Exception as error:
        result.update(error=str(error), continuation='inspect retained state without replay')
    finally:
        (directory/'result.json').write_bytes(encoded(result))
    return result


def seal(args):
    os.umask(0o077)
    baseline = args.observation
    captured = json.loads(private(baseline/'stdout.txt'))
    observed_spec = json.loads(private(baseline/'spec.json'))
    outcome = json.loads(private(baseline/'outcome.json'))
    observed_result = json.loads(private(baseline/'result.json'))
    receipt = json.loads(private(baseline/'execution.json'))
    archive_sha = sha(private(baseline/'inspection.tar'))
    if (not outcome.get('corrected_timing_collection_accepted') or not outcome.get('contacts_disabled')
            or outcome.get('archive_sha256') != archive_sha or receipt.get('sha256') != archive_sha
            or observed_result.get('bundle_sha256') != archive_sha or observed_result.get('returncode') != 0
            or not observed_result.get('capture_complete') or observed_spec.get('purpose') != 'timing-observation'
            or observed_spec.get('hostname') != 'J1-SVMF' or observed_spec.get('endpoint') != '10.1.3.83'
            or captured.get('spec_sha256') != sha(encoded(observed_spec))
            or outcome['capture_sha256'] != sha(private(baseline/'stdout.txt'))
            or captured['before'] != captured['after'] or not captured['capture_complete']):
        raise ValueError('accepted corrected-timing master capture required')
    files = {n: p.read_bytes() for n, p in SOURCES.items()}
    control = module(files['worker.py'], 'contact_control')
    production = private(args.production)
    repository = (ROOT/'master/configs/munin.conf').read_bytes()
    if sha(production) != observed_spec['files']['/etc/munin/munin.conf']:
        raise ValueError('accepted production baseline required')
    candidate = control.render(repository)
    files.update({'production-before.conf': production, 'repository-before.conf': repository,
                  'candidate.conf': candidate, 'message.eml': b'', 'preview.txt': b'',
                  'ca.pem': private(baseline/'ca.pem'), 'known_hosts': private(baseline/'known_hosts'),
                  'qualification.json': private(args.qualification),
                  'metadata-evidence.json': b'{}',
                  'candidate.diff': ''.join(difflib.unified_diff(production.decode().splitlines(True), candidate.decode().splitlines(True),
                                             fromfile='production-before.conf', tofile='candidate.conf')).encode()})
    now = time.time()
    kind = args.kind
    spec = {'schema': 1, 'kind': kind, 'operation_id': args.output.name, 'prepared_epoch': now,
            'expires_epoch': now+86400, 'recovery_seconds': 600,
            'repository_target': str(ROOT/'master/configs/munin.conf'),
            'addresses': ['10.1.3.83', 'fd36:5aa8:6971:1::83'],
            'paths': ['/', '/static/style-new.css', '/munin-cgi/munin-cgi-graph/j2-svntp1/j2-svntp1/ntp_health-day.png'],
            'leaf_sha256': observed_spec['leaf_sha256'],
            'worker': {'operation_id': args.output.name, 'hostname': 'J1-SVMF', 'boot_id': observed_spec['boot_id'],
                       'fixture': False, 'before_sha256': sha(production), 'candidate_sha256': sha(candidate),
                       'units': captured['before']['units'],
                       'protected_files': {p: h for p, h in observed_spec['files'].items() if p != '/etc/munin/munin.conf'},
                       'artifacts': {k: base64.b64encode(files[n]).decode() for k, n in
                           (('config', 'candidate.conf'), ('repository', 'repository-before.conf'), ('helper', 'mailrise.py'), ('gate', 'gate.py'))}}}
    if args.metadata is None:
        raise ValueError('completed read-only metadata diagnostic required')
    diagnostic = args.metadata
    archive = private(diagnostic/'inspection.tar')
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:') as inspection:
        members = inspection.getmembers()
        if (len(members) > 32 or len({m.name for m in members}) != len(members)
                or any(not m.isfile() or m.size > 1048576 for m in members)):
            raise ValueError('bounded diagnostic archive required')
        frozen = {m.name: inspection.extractfile(m).read() for m in members}
    if (json.loads(frozen['manifest.json']) != {n: sha(v) for n, v in frozen.items() if n != 'manifest.json'}
            or private(diagnostic/'spec.json') != frozen['spec.json']):
        raise ValueError('diagnostic manifest binding')
    evidence = {k: json.loads(private(diagnostic/n)) for k, n in
                (('capture', 'stdout.txt'), ('spec', 'spec.json'), ('result', 'result.json'),
                 ('receipt', 'execution.json'), ('outcome', 'outcome.json'))}
    evidence['archive_sha256'] = sha(archive)
    spec['worker']['predecessor_proof'] = proof_from_evidence(evidence, spec['worker'])
    files['metadata-evidence.json'] = encoded(evidence)
    if kind != 'activation':
        if args.activation is None or args.draft is None:
            raise ValueError('sealed activation and exact-message draft required')
        activation = json.loads(private(args.activation/'sealing.json'))['sha256']
        previous, previous_files = unpack(private(args.activation/'deployment.tar'), activation)
        if previous['kind'] != 'activation' or previous_files['candidate.conf'] != candidate:
            raise ValueError('same activation candidate required')
        raw = private(args.draft/(kind+'.eml'))
        # Canonicalize line endings before sealing; never re-render approved content at send time.
        raw = raw.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
        control.validate_message(raw, kind)
        preview = private(args.draft/(kind+'-preview.txt')).decode()
        files.update({'message.eml': raw, 'preview.txt': preview.encode()})
        spec.update(message_label=kind, message_sha256=sha(raw), preview=preview,
                    activation_prerequisite={'directory': str(args.activation.absolute()), 'archive_sha256': activation,
                        'operation_id': previous['operation_id'], 'config_sha256': sha(candidate),
                        'worker_sha256': sha(encoded(previous['worker']))})
        if kind == 'recovery':
            if args.problem is None:
                raise ValueError('sealed problem operation required')
            ps = json.loads(private(args.problem/'sealing.json'))['sha256']
            problem, _ = unpack(private(args.problem/'deployment.tar'), ps)
            if problem['kind'] != 'problem':
                raise ValueError('exact problem prerequisite required')
            spec['problem_prerequisite'] = {'directory': str(args.problem.absolute()), 'archive_sha256': ps,
                                             'message_sha256': problem['message_sha256']}
    return {'sha256': write_archive(args.output, spec, files), 'execution_ready': True, 'target_contact': False}


def confirm_delivery(args):
    private_directory(args.directory)
    spec, _ = unpack(private(args.directory/'deployment.tar'), args.sha256)
    receipt = private(args.directory/'execution.json')
    if (spec['kind'] not in ('problem', 'recovery')
            or json.loads(receipt)['sha256'] != args.sha256 or not args.acknowledgement.strip()):
        raise ValueError('exact consumed test send and explicit operator acknowledgement required')
    acknowledgement = {'archive_sha256': args.sha256, 'message_sha256': spec['message_sha256'],
        'execution_receipt_sha256': sha(receipt), 'source': 'operator', 'delivered': True,
        'acknowledgement': args.acknowledgement, 'confirmed_epoch': time.time()}
    with (args.directory/'delivery-confirmation.json').open('xb') as stream:
        stream.write(encoded(acknowledgement))
        stream.flush()
        os.fsync(stream.fileno())
    fd = os.open(args.directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    return {'operator_confirmation_recorded': True, 'target_contact': False}


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    q = sub.add_parser('seal')
    q.add_argument('--kind', choices=('activation', 'problem', 'recovery'), required=True)
    for name in ('observation', 'production', 'qualification', 'output'):
        q.add_argument('--'+name, type=Path, required=True)
    for name in ('activation', 'draft', 'problem', 'metadata'):
        q.add_argument('--'+name, type=Path)
    q = sub.add_parser('confirm-delivery')
    q.add_argument('--directory', type=Path, required=True)
    q.add_argument('--sha256', required=True)
    q.add_argument('--acknowledgement', required=True)
    for action in ('check', 'execute', 'inspect', 'root'):
        q = sub.add_parser(action)
        q.add_argument('--directory', type=Path, required=True)
        q.add_argument('--sha256', required=True)
        if action == 'root':
            q.add_argument('--action', dest='root_action', choices=('apply', 'commit', 'recover', 'inspect'), required=True)
    args = parser.parse_args()
    if args.action == 'seal':
        result = seal(args)
    elif args.action == 'confirm-delivery':
        result = confirm_delivery(args)
    elif args.action == 'root':
        result = locked_worker(args.directory, args.sha256, args.root_action)
    elif args.action == 'check':
        private_directory(args.directory)
        _, files = unpack(private(args.directory/'deployment.tar'), args.sha256, 900)
        if files['runner.py'] != Path(__file__).read_bytes() or any(private(args.directory/n) != b for n, b in files.items()):
            raise ValueError('frozen local inputs required')
        result = {'verified': True, 'target_contact': False}
    else:
        result = execute(args)
    print(json.dumps(result))
    if args.action == 'execute' and not result.get('accepted'):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
