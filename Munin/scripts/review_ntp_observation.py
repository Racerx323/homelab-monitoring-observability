#!/usr/bin/python3
"""Seal separate, one-use read-only node and native-master observations."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import signal
import ssl
import stat
import tarfile
import time
import types
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent.parent
SOURCES = {'runner.py': Path(__file__), 'collector.py': ROOT/'scripts/observe_ntp.py',
           'helper.py': WORKSPACE/'homelab-ntp/ntpsec/scripts/run-production-inspection.py',
           'tls-probe.py': WORKSPACE/'homelab-network/Ubiquiti/munin-master-profile/qualify_dashboard.py',
           'tests.py': ROOT/'tests/test_ntp_observation.py',
           'growth.py': ROOT/'scripts/observe_ntp_growth.py',
           'statistics.py': WORKSPACE/'homelab-ntp/ntpsec/scripts/run-statistics-inspection.py',
           'growth-tests.py': ROOT/'tests/test_ntp_growth.py',
           'contract.md': WORKSPACE/'homelab-ntp/ntpsec/docs/PRODUCTION-OBSERVATION-CONTRACT.md'}
TARGETS = {'node': ('10.1.0.51', 'ama', '10.1.0.137', 'j2-svntp1'),
           'master': ('10.1.3.83', 'pi', 'svmf.local.theama.co', 'J1-SVMF')}
LIMITS_SOURCES = ('/usr/share/perl5/Munin/Master/Config.pm', '/usr/share/perl5/Munin/Common/Config.pm',
                 '/usr/share/perl5/Munin/Master/Utils.pm', '/usr/share/perl5/Munin/Master/LimitsOld.pm')
CONTACT_FILES = set(LIMITS_SOURCES) | {'/usr/share/perl5/Munin/Master/'+name+'.pm'
    for name in ('GraphOld', 'Update', 'UpdateWorker')} | {
    '/etc/apache2/sites-available/001-munin.theama.co-ssl.conf', '/etc/cron.d/munin',
    '/etc/munin/munin.conf', '/etc/munin/plugin-conf.d/ntp-transport.conf',
    '/usr/lib/munin/cgi/munin-cgi-graph', '/usr/lib/munin/cgi/munin-cgi-html',
    '/usr/lib/systemd/system/munin-node.service', '/usr/local/munin/lib/plugins/ntp_transport_j2',
    '/usr/local/libexec/munin-ntp-mailrise.py', '/usr/local/libexec/munin-ntp-contact-gate.py',
    '/var/lib/munin-ntp-contact-control/enabled.json'}
GROWTH_POLICY = {'duration_seconds': 172800, 'checkpoint_offsets_seconds': [0, 21600, 86400, 172800],
                 'retention_days': 31, 'headroom_factor': 2, 'minimum_free_bytes': 10737418240,
                 'minimum_free_inode_percent': 5}
GROWTH_FIELDS = {'ntp_free_bytes': {'root_bytes': 'g', 'stats_bytes': 'g'},
    'ntp_free_inodes': {'root_inodes': 'g', 'stats_inodes': 'g'},
    'ntp_storage_read': {'root_ok': 'g', 'stats_ok': 'g'},
    **{graph: {stream: kind for stream in ('loopstats', 'peerstats', 'clockstats', 'protostats')}
       for graph, kind in (('ntp_stats_bytes', 'g'), ('ntp_stats_growth', 'd'), ('ntp_stats_age', 'g'))},
    'ntp_stats_read': {'ok': 'g'},
    'ntp_job_evidence': {'retention_evidence': 'g', 'reporting_evidence': 'g'},
    'ntp_job_age': {'retention_age': 'g', 'reporting_age': 'g'}}
GROWTH_CHECKPOINTS = {'+6h': 21600, '+24h': 86400, '+48h': 172800}
GROWTH_PREVIOUS = {'+24h': '+6h', '+48h': '+24h'}
GROWTH_STAGES = {'timing': 'munin-generic-timing-20261022-v2',
                 'producers': 'munin-producer-followup-20261022-v1',
                 'mail': 'munin-contact-mail-observation-20261022-v1'}
GRAPHS = ['cpu', 'load', 'memory', 'uptime', 'processes', 'ntp_health', 'ntp_timing',
          'ntp_free_bytes', 'ntp_free_inodes', 'ntp_storage_read', 'ntp_stats_bytes',
          'ntp_stats_growth', 'ntp_stats_age', 'ntp_stats_read', 'ntp_job_evidence', 'ntp_job_age']
MEMBERS = set(SOURCES)|{'known_hosts', 'ca.pem', 'spec.json', 'review.md', 'manifest.json'}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True)+'\n').encode()


def module(raw, name):
    ns = {'__name__': name, '__file__': '/sealed/Munin/scripts/'+name+'.py'}
    exec(compile(raw, ns['__file__'], 'exec'), ns)
    return types.SimpleNamespace(**ns), ns


def private(path, limit=8388608):
    path = Path(path)
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('indirect private input')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        meta = os.fstat(stream.fileno())
        if not stat.S_ISREG(meta.st_mode) or meta.st_uid != os.getuid() or stat.S_IMODE(meta.st_mode) != 0o600:
            raise ValueError('owner-private regular input required')
        raw = stream.read(limit+1)
    if len(raw) > limit:
        raise ValueError('private input bound')
    return raw


def accepted(directory, flag):
    raw = private(directory/'deployment.tar')
    outcome_raw = private(directory/'outcome.json')
    outcome = json.loads(outcome_raw)
    if outcome.get(flag) is not True or outcome.get('archive_sha256') != sha(raw):
        raise ValueError('accepted stage required: '+flag)
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        rows = archive.getmembers()
        if len(rows) > 128 or any(not m.isfile() or m.size > 4194304 for m in rows):
            raise ValueError('bounded baseline archive required')
        if len({m.name for m in rows}) != len(rows):
            raise ValueError('duplicate baseline members')
        files = {m.name: archive.extractfile(m).read() for m in rows}
    return files, outcome, {'archive_sha256': sha(raw), 'outcome_sha256': sha(outcome_raw)}


def graph_fields(config, plugin):
    """Map qualified multigraph fields to native RRD names, excluding computed fields."""
    graph = plugin
    labels, computed, types = {}, set(), {}
    for line in config.splitlines():
        if line.startswith('multigraph '):
            graph = line.split(' ', 1)[1]
            if not re.fullmatch(r'[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)*', graph):
                raise ValueError('unsafe qualified graph name')
        match = re.fullmatch(r'([A-Za-z0-9_]+)\.(label|type|cdef) (.+)', line)
        if not match:
            continue
        field, key, value = match.groups()
        pair = (graph, field)
        if key == 'label':
            labels[pair] = True
        elif key == 'type':
            if value.upper() not in ('ABSOLUTE', 'COUNTER', 'DERIVE', 'GAUGE'):
                raise ValueError('unsupported qualified RRD type')
            types[pair] = value[0].lower()
        elif field not in value.split(','):
            computed.add(pair)
    result = {}
    for graph, field in sorted(labels.keys()-computed):
        result.setdefault(graph, {})[field] = types.get((graph, field), 'g')
    if not result:
        raise ValueError('qualified graph fields missing')
    return result


def expanded_stage(directory, role):
    raw = private(directory/'deployment.tar')
    outcome_raw = private(directory/'result.json')
    outcome = json.loads(outcome_raw)
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        rows = archive.getmembers()
        if (len(rows) > 128 or len({row.name for row in rows}) != len(rows)
                or any(not row.isfile() or row.size > 4194304 for row in rows)):
            raise ValueError('bounded expanded provenance required')
        files = {row.name: archive.extractfile(row).read() for row in rows}
    if json.loads(files['manifest.json']) != {name: sha(data) for name, data in files.items() if name != 'manifest.json'}:
        raise ValueError('expanded provenance member drift')
    spec = json.loads(files['spec.json'])
    status = json.loads(private(directory/'controller-status.json'))
    if (spec['worker']['role'] != role or outcome.get('archive_sha256') != sha(raw)
            or not all(outcome.get(key) is True for key in ('accepted', 'committed', 'repository_reconciled'))
            or status.get('exit_code') != 0 or not isinstance(status.get('finished_epoch'), (int, float))):
        raise ValueError('accepted committed expanded stage required')
    return files, spec, outcome, status['finished_epoch'], {'archive_sha256': sha(raw), 'result_sha256': sha(outcome_raw)}


def expand_observation(spec, node_directory, master_directory, native_directory):
    node_files, node, _, node_end, node_provenance = expanded_stage(node_directory, 'node')
    master_files, master, result, master_end, master_provenance = expanded_stage(master_directory, 'expanded')
    if (master['node_prerequisite']['archive_sha256'] != node_provenance['archive_sha256']
            or master['node_prerequisite']['worker_sha256'] != sha(encoded(node['worker']))):
        raise ValueError('expanded node/master predecessor mismatch')
    native_raw = private(native_directory/'qualification.tar')
    native_capture_raw = private(native_directory/'stdout.txt')
    native_capture = json.loads(native_capture_raw)
    if (sha(native_raw) != master['native_qualification_sha256']
            or native_capture.get('capture_complete') is not True
            or native_capture['before'] != native_capture['after']):
        raise ValueError('accepted expanded native graph provenance required')
    with tarfile.open(fileobj=io.BytesIO(native_raw)) as archive:
        native_spec_raw = archive.extractfile('spec.json').read()
    if native_capture['spec_sha256'] != sha(native_spec_raw):
        raise ValueError('native capture scope mismatch')
    families = result['protocol_after']['families']
    expected = set(master['new_plugins'])
    if len(expected) != 33 or len(families) != 2 or not result['protocol_after'].get('complete'):
        raise ValueError('complete expanded dual-family acceptance required')
    graph_map, dynamic = {}, {}
    for plugin in sorted(expected):
        fields = graph_fields(native_capture['individual']['plugins'][plugin]['config']['stdout'], plugin)
        counts = {family['plugins'][plugin]['configured_fields'] for family in families}
        if len(counts) != 1:
            raise ValueError('accepted family field counts differ')
        count = counts.pop()
        if plugin in ('df', 'df_inode'):
            if set(fields) != {plugin} or not 0 < count <= 64:
                raise ValueError('unexpected filesystem graph shape')
            dynamic[plugin] = count
            fields[plugin] = {}
        for family in families:
            if (not family.get('complete') or set(family['plugins']) != expected
                    or set(fields) != {graph or plugin for graph in family['plugins'][plugin]['graphs']}
                    or plugin not in dynamic and sum(map(len, fields.values())) != count):
                raise ValueError('qualified graph/field coverage differs from accepted expansion')
        if graph_map.keys() & fields.keys():
            raise ValueError('duplicate expanded graph')
        graph_map.update(fields)
    if sum(map(len, graph_map.values())) > 384 or len(graph_map) > 80:
        raise ValueError('expanded graph observation bound')
    selected = node['node_inspection'] if spec['kind'] == 'node' else master['master_inspection']
    if selected['boot_id'] != spec['boot_id']:
        raise ValueError('expanded boot provenance changed')
    spec['files'].update(selected['files'])
    if spec['kind'] == 'node':
        spec['files'].update(node['worker']['protected'])
        spec['files']['/etc/munin/plugin-conf.d/ntp'] = sha(node_files['settings-after'])
        spec['enabled_links'] = {**node['worker']['plugins_before'],
                                 **{name: ['link', path] for name, path in node['worker']['additions'].items()}}
    else:
        spec['files']['/usr/local/munin/lib/plugins/ntp_transport_j2'] = sha(master_files['expanded.py'])
    spec.update(purpose='expanded-observation', collection_after_epoch=max(node_end, master_end),
                graphs={'j2-svntp1': sorted(graph_map), 'J1-SVMF': ['ntp_transport_j2']},
                rrd_fields={'j2-svntp1': graph_map, 'J1-SVMF': {'ntp_transport_j2': {'v4': 'g', 'v6': 'g', 'mail': 'g'}}},
                dynamic_rrd_counts={'j2-svntp1': dynamic},
                expanded_provenance={'node': node_provenance, 'master': master_provenance,
                                     'native_capture_sha256': sha(native_capture_raw)},
                https_deadline_seconds=180)


def review(s):
    if s.get('purpose') == 'growth-checkpoint':
        checkpoint = s['checkpoint_scope']
        label = checkpoint['label']
        base = review(dict(s, purpose='growth-t0'))
        for old, new in (
                ('OBS-02 t0', 'OBS-02 '+label), ('This is one t0 snapshot', 'This is one '+label+' snapshot'),
                ('Capture completeness alone accepts neither t0 nor',
                 'Capture completeness alone accepts neither this checkpoint nor'),
                ('growth_t0_node_accepted', 'growth_checkpoint_node_accepted'),
                ('as node_t0_epoch', 'as checkpoint_node_epoch'),
                ('First require accepted node t0 archive', 'First require accepted '+label+' node archive'),
                ('bind its actual t0\nepoch', 'bind its actual checkpoint\nepoch'),
                ('Existing pre-t0 samples are explicitly labelled.',
                 'Existing samples remain timestamped; report those predating this checkpoint.'),
                ('it is not the +6h sample', 'it is not a later checkpoint')):
            base = base.replace(old, new)
        return base+f"""
Accepted t0 remains epoch {checkpoint['node_t0_epoch']}; this operation never resets it.
Earliest execution: {datetime.fromtimestamp(checkpoint['not_before_epoch'], timezone.utc).isoformat()}
({datetime.fromtimestamp(checkpoint['not_before_epoch'], ZoneInfo('America/Chicago')).isoformat()}). Controller checks this before receipt/SSH;
the remote collector independently checks before observations.
Latest controller start (15-minute expiry reserve):
{datetime.fromtimestamp(s['expires_epoch']-900, timezone.utc).isoformat()}.
This new archive has its own execution expiry; historical proof expiry is not
extended. Expired archives remain ineligible for execution. Early execution
fails immediately, without sleeping or consuming the one-use receipt.
Both accepted t0 node/master archives, captures, receipts, results and reviewed
outcomes are pinned in checkpoint_scope.t0. Changed/missing proofs block access.
The master additionally requires reviewed acceptance of this exact {label} node
archive, its first snapshot epoch and complete protected continuity before SSH.
Review node growth_checkpoint_node_accepted and checkpoint_node_epoch separately;
record actual elapsed time and lateness, never infer punctuality from this label.
Compare retained inode metadata with t0 locally after capture; retain shrinkage,
reclamation, new files, races and quiet event-driven streams as findings. No
sustained-growth or budget acceptance is automatic. This is no approval for
another checkpoint, reminder, retry, scheduler change, notification or further access.
Daily/closing checkpoints also pin the preceding accepted node/master pair and
its chained operator-confirmed overnight Munin restart disposition. Earlier
samples were late; do not relabel them punctual or reset t0. Compare endpoint
metadata with t0 and the previous sample locally after capture; new/completed
files, removals and ordinary rollover must remain distinct from gross growth.
For +48h, review both daily intervals and the full elapsed window before
calculating the 31-day budget. Retain cadence/endpoint gaps, quiet protostats
and unknown non-statistics filesystem reserves. Capture success automatically
accepts neither sustained growth, storage budget nor overall host readiness.
"""
    if s.get('purpose') in ('growth-t0', 'growth-checkpoint'):
        common = f"""# Read-only OBS-02 t0 {s['kind']} baseline

Operation {s['operation_id']}; target {s['user']}@{s['endpoint']}, strict alias
{s['host_key_alias']}, pinned {s['hostname']} boot/service/configuration identities.
Expires {datetime.fromtimestamp(s['expires_epoch'], timezone.utc).isoformat()}.
Approve only inspection.tar SHA-256 in sealing.json. One fsynced local receipt;
no replay, private complete stdout/stderr/status, remote alarm 240s/SSH 270s.

This is one t0 snapshot, not a 48-hour collector or approval for later samples.
The embedded contract.md hash is {s['contract_sha256']}.
The selected window is 48h at t0/+6h/+24h/+48h; budget 31 days at 2x peak
daily-equivalent gross growth plus active allowance, retaining 10 GiB/5% floors.
Capture completeness alone accepts neither t0 nor sustained growth/budget.
No target contact or sampling occurred during preparation. Existing schedulers,
statistics writers, retention, reporting and gated contacts remain undisturbed.
"""
        if s['kind'] == 'node':
            return common+"""
Read /var/log/ntpstats depth-one metadata twice within this invocation (no sleep),
up to 5000 entries per snapshot. Read no statistics contents. Record all four
stream base/dated names, lstat types, ownership/mode, device/inode/link count,
size, allocated blocks, ns timestamps and filesystem byte/inode availability.
Deduplicate regular recognized files by inode; retain unexpected names and
missing/indirect active-stream findings. Record the statistics mount only from
bounded /proc/<collector-pid>/mountinfo (1 MiB/4096 lines), not unrelated mount
contents. The PID is this collector's own os.getpid(); retain the no-symlink guard.

Reuse the qualified writer scan: at most 4096 processes/65536 descriptors per
pass, before/after. Read only matching statistics FD paths/flags/inodes and
writer PID/comm/exe/UID/start identity; never arguments, environments or raw GPS.
Read the existing two root-private 4096-byte job-success records, filtered
cron/logrotate journal events (2 MiB each, latest two days), logrotate timer
properties and the exact 33 enabled plugin links. No plugin/job is invoked.
Verify accepted files/boot/NTP identity before/after and active Munin-node
identity during capture. The short second snapshot detects races/rollover;
it is not the +6h sample and provides no accepted sustained growth rate.

After evidence review, record growth_t0_node_accepted and the exact first
snapshot started_epoch as node_t0_epoch, plus archive/capture/receipt bindings.
Do not manufacture that acceptance if writers, active files, storage metadata
or continuity are missing. That accepted record anchors the master stage.

No staging, cleanup, rotation, file-content sampling, truncation, compression,
active probe, parser, plugin, collection/limits/contact invocation, message,
HTTP, service/timer/package/network change, renewal or reboot. Normal SSH/sudo
audit logging only. Future checkpoints need fresh separately reviewed archives.
"""
        return common+f"""
First require accepted node t0 archive {s['node_t0_prerequisite']['archive_sha256']}
at {s['node_t0_prerequisite']['directory']}. Before consuming this receipt/contact,
verify its completed capture and explicit reviewed outcome; bind its actual t0
epoch and receipt/capture/outcome hashes in runtime-context.json. Never infer
node acceptance from elapsed time or a successful SSH session. No node contact
is made by this master stage. Existing pre-t0 samples are explicitly labelled.

Read existing native update log (1 MiB tail), filtered cron journal (2 MiB/latest
two hours), selected RRD lastupdate and five-minute AVERAGE samples (25-minute
window) for the nine j2 storage/statistics/job graphs listed in spec.json plus
master transport v4/v6/mail. No timing/generic/other-host graph sweep or HTTPS.
RRD consolidation is not individual raw fetch data or proof of a 48-hour window.

Read committed contact state (65536 bytes, selected fields), current 4096-byte
submission status before/after, optional suppression state (65536 bytes),
native mail limits/sample snapshots (1 MiB each) and classified limits-log tail
(262144 bytes, at most 200 markers, no raw message/log bodies), as in the
accepted mail observation. Check empty includes and committed input hashes.
Additionally read /var/lib/munin/datafile.storable and limits.storable (4 MiB
each); decode in memory as munin, exporting only the selected j2 graph/field
labels/types/warning/critical/unknown limits, contact selectors and current
field states. Never execute cached contact commands or expose other nodes.

No status reset, SMTP/notification retry, HTTP, plugin, forced metric collection, parser or
limits evaluator invocation, target staging, service/container/network change,
package action or new schedule. Ordinary SSH/sudo/runuser audit logging only.
Missing/stale/racing evidence remains a finding. Record baseline acceptance
separately; this snapshot neither accepts the full growth budget nor proves
current client coverage or post-renewal/reboot persistence.
"""
    if s.get('purpose') == 'contact-observation':
        return f"""# Read-only committed contact, mail and native limits observation

Operation {s['operation_id']}; master pi@10.1.3.83, strict Ed25519 alias
svmf.local.theama.co; pinned J1-SVMF boot and protected service/file identities.
Expires {datetime.fromtimestamp(s['expires_epoch'], timezone.utc).isoformat()}.
Approve only inspection.tar SHA-256 in sealing.json. One fsynced receipt;
private complete stdout/stderr/status, no replay. Remote alarm 240s; SSH 270s.

Require the accepted/reconciled activation v3 and consumed problem/recovery v2
receipts plus both explicit operator delivery confirmations. Pin their retained
results, SMTP discrepancy and exact payload/receipt hashes as local provenance.
Before/after verify the committed main/helper/gate/enable-marker hashes and
protected boot/services/native modules. Read selected committed-state fields
from {s['contact_state_path']} (65536 bytes); no executable is invoked from it.

Read only current /var/lib/munin/ntp-alerts/status.json (4096 bytes), before and
after; export schema, submission_ok, attempt_epoch and metadata. Read selected
suppression fields if present (65536 bytes). Validate the status ownership,
mode, link count and schema; normal scheduled replacement remains an explicit
finding, never a reason to manufacture or reset status. Status has no message
identity: timestamp correlation alone does not prove which sender wrote it.

Read existing update-log tail (1048576 bytes) and cron journal evidence since
activation, capped at the latest two hours, plus only J1-SVMF transport mail RRD
lastupdate and five-minute AVERAGE samples from the existing 25-minute window.
Consolidated samples are not individual raw fetches. Read limits.storable and
state-J1-SVMF-J1-SVMF.storable (1048576 bytes each) from /var/lib/munin. Decode
the bounded in-memory snapshots as munin using Perl/Storable and pinned native
tree lookup; export only transport mail state/current samples. No state files
are opened for writing. Missing/unsupported/stale state remains a finding.

Read /var/log/munin/munin-limits.log tail (262144 bytes); export at most 200
classified event markers/timestamp prefixes/line hashes, no raw log, message
body, credentials or unrelated host state. Effective includes must remain empty.
Retain genuine scheduler drift; do not pause it or wait/retry for better data.

No staging, service/container/network change, package action, SMTP attempt,
message resend, status edit/reset, plugin, collection, parser, limits evaluation,
HTTP request or contact/gate/helper invocation. Ordinary SSH/sudo/runuser audit
logging only. Existing scheduled contacts remain enabled and undisturbed.
No Mailrise/provider configuration or container logs are read in this scope;
the SMTP 450 backend cause may remain unresolved. Separate capture completeness,
native transition evidence, SMTP submission and operator-confirmed delivery.
"""
    if s.get('purpose') == 'contact-metadata':
        return f"""# Read-only contact main-config metadata diagnostic

Operation {s['operation_id']}; target pi@10.1.3.83, strict Ed25519 alias
svmf.local.theama.co, pinned J1-SVMF boot and protected service/file continuity.
Expires {datetime.fromtimestamp(s['expires_epoch'], timezone.utc).isoformat()}.
Approve inspection.tar SHA-256 in sealing.json. One fsynced local receipt;
private stdout/stderr/status, no replay. Remote alarm 240s; SSH deadline 270s.

The consumed activation v2 rejected /etc/munin/munin.conf metadata in preflight,
before contact payload publication. Inspect that file and only the fixed
/var/lib/munin-ntp-master/munin-master-commissioning-20261021-v1/config-proof
predecessor proof: bounded 262144-byte reads each; SHA-256, numeric uid/gid,
mode, nlink, inode/device, size and mtime. Export no config/source bytes.
Report every expected predicate separately and whether both names share an
inode. Prior publication code suggests a retained proof link; this is a
hypothesis to verify, not permission to accept another link count.

Read only lstat presence/metadata for the helper/gate paths, gate-control and
private alert-state directories, /usr/local/libexec and /var/lib/munin. Never
read submission records or enumerate unrelated files. Repeat the metadata/hash
and protected continuity checks; drift/missing inputs remain explicit findings.

No staging, chmod/chown/link/unlink/write, correction, restore, parser, plugin,
limits/update/job, SMTP/message, package/service/timer/network or HTTPS action.
Normal SSH/sudo audit logging only. Contacts remain disabled; both controlled
tests remain blocked/unconsumed. This diagnostic authorizes no deployment,
metadata normalization or replay of activation. A corrected successor needs
new qualification, hashes and approval.
"""
    if s.get('purpose') == 'timing-observation':
        return f"""# Read-only corrected timing-health master acceptance

Operation `{s['operation_id']}`; target pi@10.1.3.83, strict alias
svmf.local.theama.co; expires epoch {s['expires_epoch']}.
Approve inspection.tar's exact SHA-256 in sealing.json. One receipt, no replay.
Require the separately sealed node correction to be accepted, committed and
repository-reconciled before contact. Bind its archive and private execution,
commit result and completion epoch; record the derived context before contact.
This review contacts only the master, not the node.

Read existing cron/update evidence for three consecutive eligible native cycles
strictly after that correction commit; no wait or forced collection. Allow time
for three completed five-minute cycles and the existing 240-second eligibility
margin before executing. Missing cycles remain inconclusive, never skipped.
Read exactly twelve GAUGE RRDs: eight ntp_health fields (including both new
timing flags) and the four unchanged ntp_timing seconds fields. Use native
lastupdate/fetch AVERAGE only; no create/update/tune or state deserialization.
Retain unknowns and missing fields. Require new flags=1, current raw numeric
values and genuine post-commit samples before accepting corrected collection.

Verify root/CSS/j2 index and these two day graphs over each explicit master
address: ten bounded HTTPS requests with hostname/CA/leaf verification, twelve
seconds/1 MiB per request and 90-second aggregate deadline. Ordinary CGI/cache
writes may occur. PNG serving is not numeric freshness; correlate the RRDs.
Pin accepted main-config contacts-none bytes, native module hashes and
protected service/files before/after; effective includes must remain empty.

No target staging, active node/protocol/plugin query, update/limits/contact/job
invocation, package/service/timer/network/configuration action, notification or
recovery. Normal SSH/sudo/native scheduler logging remains possible. Contacts
remain disabled. Remote alarm 240 seconds, SSH deadline 270 seconds. Accept
only this bounded field/graph capture; activation, delivered messages, sustained
budget, source/client persistence and final observation remain separate gates.
"""
    if s.get('purpose') == 'maintenance-observation':
        return f"""# Read-only native-master maintenance-field observation

Operation `{s['operation_id']}`. Target pi@10.1.3.83, strict Ed25519 alias
svmf.local.theama.co; accepted expanded host/boot/service/file pins.
Expires {datetime.fromtimestamp(s['expires_epoch'], timezone.utc).isoformat()}.
Approve inspection.tar's exact SHA-256 in sealing.json before execution.

Read existing native cron/update events to assess the latest three eligible
scheduled collection cycles after the accepted genuine producer completions.
Read only four exact direct RRDs under /var/lib/munin/j2-svntp1:
ntp_job_evidence retention_evidence/reporting_evidence, and ntp_job_age
retention_age/reporting_age (all GAUGE). Use bounded native rrdtool lastupdate
and fetch AVERAGE at 300-second resolution; no update, tune, create or write.
Preserve unknowns, timestamps and missing fields. Compare evidence=1 and numeric
ages against the sealed real producer completion epochs and collection times.
Consolidated samples do not prove a particular individual raw fetch.

Verify root/CSS/j2 index and only the two maintenance day PNGs over both explicit
master addresses: ten HTTPS requests total, fixed hostname/CA/leaf verification,
12 seconds/1 MiB each, 90-second aggregate deadline. Ordinary native CGI/cache
writes are possible; PNG success alone does not establish fresh measurements.

Protected checks also pin four native Config/Utils/LimitsOld module hashes from
the accepted installed-source capture. This checks applicability of the local
native-engine qualification; it executes no parser, limits or contact command.
Require the native effective includedir listing to remain empty before/after;
unexpected entries are findings, not permission to read or alter them. Main
configuration retains its accepted contacts-none bytes.
Check protected files/services before and after. No target staging, package,
plugin/protocol/job/update/limits invocation, state deserialization, configuration,
service/timer/network change, packet capture, notification or recovery.
Contacts remain disabled. One fsynced local receipt before contact; private
bounded capture; remote alarm 240 seconds, SSH deadline 270 seconds; no replay.
Missing or inconsistent evidence remains open. Capture completion does not
automatically accept maintenance consumption, limits or delivery.
"""
    if s.get('purpose') == 'source-attribution':
        return f"""# Read-only canonical collector source attribution

Operation `{s['operation_id']}`. Target pi@10.1.3.83, strict Ed25519 alias
svmf.local.theama.co, pinned J1-SVMF boot and accepted expanded continuity.
Expires {datetime.fromtimestamp(s['expires_epoch'], timezone.utc).isoformat()}.
Approve inspection.tar's exact SHA-256 in sealing.json before execution.

Observe existing established IPv4 TCP connections to 10.1.0.51:4949 for at most
360 monotonic seconds and 360 scans, one-second spacing. Read only the observer's
/proc/PID/net/tcp (512 KiB per read). Select the existing munin UID; retain actual
source/port, target/port, UID and inode. Expected canonical source: 10.1.3.83.
This canonical IPv4 series is distinct from the dual-family transport plugin.

For matching connections, enumerate at most 8192 /proc entries, inspect FD links
only for munin-owned processes (256 descriptors each), then matched owners' stat
and cmdline (4096 bytes) and at most six ancestors' stat/cmdline. Retain PID,
parent, start ticks, UID and only fixed munin-update/munin-cron/ntp_transport_j2
command tags; export no arbitrary arguments, environment or payload. Recheck
owner identity and socket tuples; retain at most 128 distinct observations.
Read the final 1 MiB of /var/log/munin/munin-update.log and bounded cron.service
journal evidence since capture start minus 60 seconds. Correlate the canonical
worker ancestry with native scheduled events. Missing/racing/ambiguous owners,
no captured connection or insufficient provenance remain inconclusive. Capture
completion does not automatically accept source attribution.

Check protected files/services before and after. No packet capture, target
staging/writes, active connection/probe, plugin/job/update/limits invocation,
RRD/HTTPS access, configuration or network change, service/timer action,
notification or recovery. Ordinary SSH/sudo audit logging remains possible.
Remote alarm 480 seconds; SSH deadline 510 seconds. One fsynced local receipt
before contact; private bounded stdout/stderr/result; no replay. Contacts stay
disabled. Execute only frozen runner.py with this directory and approved hash.
"""
    if s.get('purpose') == 'transport-metadata':
        return f"""# Read-only master transport metadata inspection

Operation `{s['operation_id']}`. Target pi@10.1.3.83, strict Ed25519 alias
svmf.local.theama.co; pinned J1-SVMF boot and protected service/file continuity.
Expires {datetime.fromtimestamp(s['expires_epoch'], timezone.utc).isoformat()}.
Approve inspection.tar's exact SHA-256 in sealing.json before execution.

Read only /usr/local/munin/lib/plugins/ntp_transport_j2 (262144-byte maximum),
reporting SHA-256, numeric uid/gid, permission mode, link count, inode/device,
size and mtime. Export no source bytes. Compare each sealed expected predicate
individually; a difference is a finding, not permission to correct it. Inspect
only the /etc/munin/plugins/ntp_transport_j2 symlink metadata and literal target.
Repeat metadata/hash reads and protected continuity checks across the capture;
fail if they change. The inspected source is excluded from protected hash pins
so a hash mismatch can be reported. All other pins remain required.

No target staging, lock, writes, chmod/chown, package action, plugin invocation,
protocol/HTTP query, service start/stop/restart/reload, timer/job, RRD access,
network change, recovery or notification. Ordinary SSH/sudo audit logging only.
Remote alarm 240 seconds; SSH deadline 270 seconds. One fsynced local receipt
before contact, private bounded stdout/stderr/result, no replay. Capture
completion is not deployment acceptance. Successor reviews require separately
approved new hashes; this review authorizes no deployment.
"""
    label = 'generic-statistics inventory' if s.get('purpose') == 'generic-profile' else 'scheduled-observation'
    j2_count = len(s.get('graphs', {'j2-svntp1': GRAPHS})['j2-svntp1'])
    common = f"""# {s['kind']} read-only {label} review

Operation `{s['operation_id']}`. Target {s['user']}@{s['endpoint']}, strict
Ed25519 alias {s['host_key_alias']}; exact host/boot and protected service/file
pins from accepted stages. Expires {datetime.fromtimestamp(s['expires_epoch'], timezone.utc).isoformat()}.
Approve inspection.tar's exact SHA-256 in sealing.json before execution.
This review authorizes one capture on this target only; no receipt replay.

Require root, host/boot, pinned file hashes and service identity before and after.
Capture Munin-node's current active/running PID/invocation/restart identity and
require it unchanged across this capture; its PID is not an old pre-restart pin.
Collect existing evidence only. No install, start/stop/reload/restart, job,
Munin update/limits/plugin/protocol invocation, RRD write, packet capture, lock
acquisition, success-record creation, clock change, DNS/network change or message.
SSH/sudo and ordinary service logging may write their normal audit records.
No target staging. Fixed PATH/C locale; bounded regular reads reject indirect
paths. Remote alarm 240 seconds, SSH deadline 270 seconds; capture findings and
missing evidence explicitly. A capture_complete result is not readiness approval.
The one-use local execution.json is fsynced before contact. Retain private
stdout/stderr/result and failures; do not retry a consumed inspection.
"""
    if s.get('purpose') == 'expanded-observation':
        field_count = sum(map(len, s['rrd_fields']['j2-svntp1'].values()))+sum(s['dynamic_rrd_counts']['j2-svntp1'].values())
        common += f"""
## Accepted expanded baseline

Pin the committed expanded node settings/sources and final master transport,
not the original nine-plugin configuration. Node scope additionally verifies
the exact 33 enabled links without invoking plugins. Post-expansion cycle cutoff
is epoch {s['collection_after_epoch']}, conservatively after both controllers
finished committed/reconciled stages. Earlier cycles cannot satisfy this review.
The sealed graph inventory has {len(s['graphs']['j2-svntp1'])} j2 graphs and
{field_count} configured j2 fields at deployment, plus the
master transport graph and three fields. Qualified fixed field names/types are
pinned for observation; graph/count coverage is cross-checked against both
accepted expanded protocol captures. Dotted diskstats
graphs use native hyphenated RRD names and nested CGI paths; no graph is omitted.
Missing fields/graphs or changed devices remain gaps, not silently reduced scope.
Repository main-config stanza placement is an intentional operator readability
edit. Keep production's accepted byte hash pinned; no configuration write or
attempt to copy the local presentation edit to production is included.

Exact j2 graph selection: {', '.join(s['graphs']['j2-svntp1'])}.
"""
    if s.get('purpose') == 'generic-profile':
        if s['kind'] == 'node':
            scope = """
## Generic-profile node inventory

List /etc/munin/plugins links (512 maximum), retaining only safe targets directly
under /usr/share/munin/plugins or /usr/local/munin/lib/plugins. Read those direct
regular source files for bounded metadata/hashes only (256 KiB each), never raw
code export. Read up to 64 standard plugin-conf.d files, 64 KiB each, exporting
hashes and section/user/group/timeout selectors only. Omit all environment and
command values. List up to 512 available package plugin names and query exact
munin-node/munin-plugins-core installed versions. List names only under the four
fixed sysfs class directories net, block, thermal and hwmon (128 entries each).
No sensor/device reads, smartctl, autoconf, munin-node-configure --suggest,
plugin config/fetch, protocol probe, recursive filesystem scan or reference-host contact.
Unexpected paths, indirect files or missing capabilities are findings, not a
reason to expand privileges, install software or silently drop required stats.
"""
        else:
            scope = """
## Reference generic-graph inventory on the native master

List only the two fixed native RRD directories /var/lib/munin/j2-svpi4mf and
/var/lib/munin/j2-svntp1 (512 entries each). Export safe RRD filenames, inferred
graph/field/type and regular-file mtimes only; do not read RRD contents or run
rrdtool. Historical RRD presence alone does not prove a plugin is still enabled.
This contacts svmf only; no SSH/protocol/HTTP request goes to j2-svpi4mf/.170.

After successful capture, request only each host's index page over both explicit
master literals with the pinned hostname/CA/leaf. Retain normal response metadata
and safe page/graph/asset links; no raw HTML export. Four HTTPS requests maximum,
12 seconds/1 MiB each, stopping at first failure. Normal CGI/access-cache writes
may occur. Cross-check current page links with recent RRD mtimes; stale graphs
or unsupported layouts stay gaps, not invented reference plugin assignments.
"""
        return common+scope+"""
## Decision after capture

Compare every reference graph with the target and classify generic OS/hardware
statistics separately from reference-only applications. Preserve all four NTP
readers. Map device/interface-specific instances to actual target capabilities;
record every unsupported item explicitly for review. This capture does not
select/enable plugins, authorize dependency changes or deploy an expanded profile.
Update the node selection, privileges, guarded continuation and master's strict
expected plugin set together in a later reviewed deployment; measure its full
protocol runtime rather than weakening the existing 25-second budget blindly.
Run frozen runner.py execute --directory DIRECTORY --sha256 APPROVED_SHA256.
No recovery/cleanup is authorized; consumed inspection cannot be replayed.
"""
    if s['kind'] == 'node':
        scope = """
## Node/producer scope

Read only the two root-owned mode-0600 schema-1 success records, at most 4096
bytes each. Validate job/status, finite completion after the accepted producer
installation and not in the future; report each job's age and 172800-second
freshness separately. Pin installed helper/reporter/retention rule, cron/trigger
and protected NTP inputs. Read bounded cron/logrotate journal records since
installation (at most 48 hours); export only matching event kinds and epochs.
Read logrotate timer properties only, not service-only PID/restart properties.
No credentials, raw mail, arbitrary home files, locks or raw journal export.

A real completion record plus matching scheduled event is a provenance candidate
for review, never inferred from a global timer alone. Missing, invalid, stale,
future or unmatched records remain faults/open gates. Log absence/rotation or
journald not retaining cron events is inconclusive; do not invoke the job to
manufacture evidence. Reporting is normally 05:30 America/Chicago; this daytime
capture may correctly find no post-install scheduled reporting record. Correlate
retention's rule-specific record independently of global logrotate completion.
This does not accept failure-mail delivery or extended statistics growth.
"""
    else:
        scope = f"""
## Native-master scope and three-cycle rule

Read a bounded 1 MiB tail of munin-update.log and at most 2 MiB of cron journal
output since commissioning, limited to the last two hours. Export only fixed
start/finish/fault kinds, node identifiers and epochs; never raw log lines or
arbitrary cron commands. Require actual `(munin) CMD (.../usr/bin/munin-cron...)`
events; fixed cron source is pinned. Inspect the latest three eligible completed
post-commissioning runs: starts in consecutive 300-second slots within 60 seconds
of each boundary, cron correlation within 60 seconds, global finish and both
j2/master node finishes within 240 seconds, no intervening start or logged fault.
An eligible start is at least 240 seconds old. A missed/failed/intervening cycle,
clock/boot/service/config drift, unknown log format or missing cron provenance
leaves the three-cycle gate open. Do not skip failures, wait for cycles, force
updates, restart the window silently or accept elapsed time as evidence. A later
capture needs a separately approved successor review.

Read only fixed native /var/lib/munin/j2-svntp1 and /var/lib/munin/J1-SVMF RRD
directories (512 entries each), selecting the {j2_count} expected j2 graphs and the
master transport graph by bounded filename grammar. Use only rrdtool lastupdate
and fetch AVERAGE at resolution 300 over the latest aligned 25-minute range.
No daemon address/environment, flush, update, tune, graph command or state-file
deserialization. Preserve unknown/NaN as null; zero is not substituted. RRD
consolidation is not an exact individual raw fetch. Review per-field timestamps,
finite values and transport v4/v6=1 across the same three cycles; mail=U and
missing maintenance ages remain explicit unaccepted evidence. Files/graphs
missing or stale leave collection/freshness open. Retain actual RRD filenames.

After successful capture, controller makes hostname/CA/leaf-verified HTTPS
requests over .83 and ::83: root, CSS, j2 index, each of the {j2_count} j2 day PNGs and
the master transport PNG. No DNS lookup/fallback or insecure TLS. Ordinary CGI
requests may update native graph/HTML caches and access logs. Each request is
bounded (12 seconds, 1 MiB); stop on first failure. Serving needs 200/correct
types/PNG signature; it does not prove data freshness. Correlate every j2 graph
with fresh RRD evidence, not only HTTP success or image checksum changes.

Missing journal attribution or insufficient samples stays inconclusive. These
captures do not prove the canonical connection's actual source address;
accepted config/source-bound transport and RRDs are not packet attribution.
No contacts, delivery tests, limits transitions, synthetic faults or alert-helper
installation. Three-cycle acceptance remains subject to evidence review; it is
not the longer OBS-09 final observation window.
"""
        if s.get('purpose') == 'expanded-observation':
            scope = scope.replace('since commissioning', 'after expanded deployment').replace('post-commissioning', 'post-expansion')
            scope += f"""
Expanded limits: at most 384 RRD files across both hosts;
read only the sealed graph/field/type filenames for fixed fields. Report missing
fixed fields explicitly; do not substitute another file. For df and df_inode,
mount membership is dynamic: list/read direct native gauge filenames within
each exact graph prefix, at most 64 per graph. Deployment reported six fields
in each. Retain old/stale entries and current timestamps/counts, leaving exact
mount membership for review; old qualification labels and historical RRDs do
not establish today's enabled mounts. All {j2_count} j2 graphs are included,
with every qualified diskstats device subgraph and overview. Inspect recent
per-field RRD values/timestamps; consolidated averages do not attribute exact
raw values to a scheduler invocation. The three-cycle conclusion comes from
correlated cron/update events, separately from field freshness and PNG serving.
At most {2*(3+sum(map(len, s['graphs'].values())))} HTTPS requests, with an aggregate
180-second controller budget plus one in-flight request (12 seconds maximum).
All PNG paths are sealed, including nested device paths. Stop at first failure.
"""
    return common+scope+"""
## Execution and handoff

Run frozen runner.py execute --directory DIRECTORY --sha256 APPROVED_SHA256.
Only the sealed source is imported. Preserve raw evidence privately. No recovery
or cleanup is authorized because this operation authors no production state.
Keep genuine job acceptance, collection/source attribution, fresh graphs,
limits/delivery, OBS-02/OBS-07, persistence and mandatory later separate-host
ntpviz individually open unless their actual evidence is reviewed and accepted.
"""


def unpack(raw, digest, *, historical=False):
    if len(raw) > 8388608 or sha(raw) != digest:
        raise ValueError('approved archive hash/size mismatch')
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        rows = archive.getmembers()
        if (len(rows) != len(MEMBERS) or {m.name for m in rows} != MEMBERS
                or any(not m.isfile() or m.size > 1048576 for m in rows)):
            raise ValueError('closed regular archive required')
        files = {m.name: archive.extractfile(m).read() for m in rows}
    if json.loads(files['manifest.json']) != {n: sha(v) for n, v in files.items() if n != 'manifest.json'}:
        raise ValueError('member digest mismatch')
    s = json.loads(files['spec.json'])
    if s.get('purpose') in ('growth-t0', 'growth-checkpoint'):
        common = {'schema', 'purpose', 'kind', 'operation_id', 'endpoint', 'user', 'host_key_alias',
                  'hostname', 'boot_id', 'prepared_epoch', 'expires_epoch', 'units', 'files',
                  'contract_sha256', 'growth_policy', 'growth_provenance', 'baseline_files_sha256'}
        extra = ({'producer_installed_epoch', 'enabled_links', 'enabled_links_sha256'} if s['kind'] == 'node'
                 else {'commissioned_epoch', 'collection_after_epoch', 'graphs', 'rrd_fields',
                       'contact_state_path', 'node_t0_prerequisite'})
        if s['purpose'] == 'growth-checkpoint':
            common.add('checkpoint_scope')
            checkpoint = s['checkpoint_scope']
            proof_keys = {'directory', 'archive_sha256', 'capture_sha256', 'receipt_sha256',
                          'result_sha256', 'outcome_sha256'}
            checkpoint_keys = {'label', 'offset_seconds', 'node_t0_epoch', 'not_before_epoch', 't0'}
            if checkpoint['label'] in GROWTH_PREVIOUS:
                checkpoint_keys.add('previous')
            proofs = list(checkpoint.get('t0', {}).values())
            if checkpoint.get('previous'):
                previous = checkpoint['previous']
                if (set(previous) != {'node', 'master', 'restart_disposition_sha256'}
                        or not re.fullmatch('[a-f0-9]{64}', previous['restart_disposition_sha256'])):
                    raise ValueError('closed previous checkpoint proof scope required')
                proofs += [previous['node'], previous['master']]
            if (set(checkpoint) != checkpoint_keys
                    or checkpoint['label'] not in GROWTH_CHECKPOINTS
                    or checkpoint['offset_seconds'] != GROWTH_CHECKPOINTS[checkpoint['label']]
                    or type(checkpoint['node_t0_epoch']) not in (int, float)
                    or not math.isfinite(checkpoint['node_t0_epoch'])
                    or not 0 < checkpoint['node_t0_epoch'] <= s['prepared_epoch']
                    or checkpoint['not_before_epoch'] != checkpoint['node_t0_epoch']+checkpoint['offset_seconds']
                    or not checkpoint['not_before_epoch'] < s['expires_epoch']-900
                    or set(checkpoint['t0']) != {'node', 'master'}
                    or checkpoint['label'] in GROWTH_PREVIOUS and not checkpoint.get('previous')
                    or any(set(proof) != proof_keys or not Path(proof['directory']).is_absolute()
                           or any(not re.fullmatch('[a-f0-9]{64}', proof[k]) for k in proof_keys-{'directory'})
                           for proof in proofs)):
                raise ValueError('closed checkpoint timing and historical proof scope required')
        if (set(s) != common | extra or s.get('growth_policy') != GROWTH_POLICY
                or s.get('contract_sha256') != sha(files['contract.md'])
                or s.get('baseline_files_sha256') != sha(encoded(s['files']))
                or set(s.get('growth_provenance', {})) != set(GROWTH_STAGES)
                or any(set(row) != {'archive_sha256', 'receipt_sha256', 'result_sha256', 'outcome_sha256'}
                       or any(not re.fullmatch('[a-f0-9]{64}', value) for value in row.values())
                       for row in s['growth_provenance'].values())):
            raise ValueError('closed growth t0 contract/baseline scope required')
        if s['kind'] == 'node':
            if (set(s['units']) != {'timeservice.service'} or len(s['enabled_links']) != 33
                    or s['enabled_links_sha256'] != sha(encoded(s['enabled_links']))
                    or '/etc/ntp.conf' not in s['files']
                    or type(s['producer_installed_epoch']) not in (int, float)):
                raise ValueError('closed node t0 scope required')
        else:
            fields = {'j2-svntp1': GROWTH_FIELDS, 'J1-SVMF': {'ntp_transport_j2': {'v4': 'g', 'v6': 'g', 'mail': 'g'}}}
            prerequisite = s['node_t0_prerequisite']
            if (s['rrd_fields'] != fields or s['graphs'] != {host: sorted(graphs) for host, graphs in fields.items()}
                    or set(s['files']) != CONTACT_FILES
                    or s['contact_state_path'] != '/var/lib/munin-ntp-contacts/munin-contacts-activate-20261022-v3/state.json'
                    or set(prerequisite) != {'directory', 'archive_sha256', 'contract_sha256'}
                    or prerequisite['contract_sha256'] != s['contract_sha256']
                    or not Path(prerequisite['directory']).is_absolute()
                    or not re.fullmatch('[a-f0-9]{64}', prerequisite['archive_sha256'])):
                raise ValueError('closed master t0 scope required')
    if s.get('purpose') == 'contact-observation':
        required = {'schema', 'purpose', 'kind', 'operation_id', 'endpoint', 'user', 'host_key_alias',
                    'hostname', 'boot_id', 'prepared_epoch', 'expires_epoch', 'units', 'files',
                    'commissioned_epoch', 'collection_after_epoch', 'graphs', 'rrd_fields',
                    'contact_state_path', 'contact_provenance'}
        fields = {'J1-SVMF': {'ntp_transport_j2': {'mail': 'g'}}}
        provenance = s.get('contact_provenance', {})
        if (set(s) != required or s['kind'] != 'master'
                or s.get('graphs') != {'J1-SVMF': ['ntp_transport_j2']} or s.get('rrd_fields') != fields
                or s.get('contact_state_path') != '/var/lib/munin-ntp-contacts/munin-contacts-activate-20261022-v3/state.json'
                or not 0 < s['commissioned_epoch'] == s['collection_after_epoch'] <= s['prepared_epoch']
                or set(provenance) != {'activation', 'problem', 'recovery'}
                or any(set(row) != ({'archive_sha256', 'receipt_sha256', 'result_sha256'} if kind == 'activation'
                       else {'archive_sha256', 'receipt_sha256', 'result_sha256', 'confirmation_sha256',
                             'message_sha256', 'submission_accepted'}) for kind, row in provenance.items())
                or any(type(provenance[k].get('submission_accepted')) is not bool for k in ('problem', 'recovery'))
                or any(not row or any(not re.fullmatch(r'[a-f0-9]{64}', value)
                       for key, value in row.items() if key.endswith('sha256')) for row in provenance.values())
                or set(s['files']) != CONTACT_FILES
                or any(not re.fullmatch(r'[a-f0-9]{64}', digest) for digest in s['files'].values())
                or set(s['units']) != {'NetworkManager.service', 'apache2.service', 'cron.service', 'munin-node.service'}):
            raise ValueError('closed contact observation scope required')
    if s.get('purpose') == 'contact-metadata':
        if (s['kind'] != 'master' or set(s.get('contact_expected', {})) != {'sha256', 'uid', 'gid', 'mode', 'nlink'}
                or {k: s['contact_expected'][k] for k in ('uid', 'gid', 'mode', 'nlink')}
                   != {'uid': 0, 'gid': 0, 'mode': 0o644, 'nlink': 1}
                or s['files'].get('/etc/munin/munin.conf') != s['contact_expected']['sha256']
                or not s.get('failed_activation_provenance')):
            raise ValueError('closed contact metadata diagnostic scope required')
    if s.get('purpose') == 'timing-observation':
        expected = {'ntp_health': {name: 'g' for name in ('query_ok','synced','pps_selected','reach','stratum','leap','selected_offset_ok','selected_jitter_ok')},
                    'ntp_timing': {name: 'g' for name in ('system_offset','system_jitter','selected_offset','selected_jitter')}}
        prerequisite = s.get('correction_prerequisite', {})
        if (s['kind'] != 'master' or s.get('graphs') != {'j2-svntp1': sorted(expected)}
                or s.get('rrd_fields') != {'j2-svntp1': expected} or s.get('https_deadline_seconds') != 90
                or not re.fullmatch('[a-f0-9]{64}', prerequisite.get('archive_sha256', ''))
                or type(prerequisite.get('prepared_epoch')) not in (int, float)
                or not 0 < prerequisite['prepared_epoch'] <= s['prepared_epoch']
                or not Path(prerequisite.get('directory', '')).is_absolute()):
            raise ValueError('timing observation boundary mismatch')
    if s.get('purpose') == 'maintenance-observation':
        fields = {'ntp_job_evidence': {'retention_evidence': 'g', 'reporting_evidence': 'g'},
                  'ntp_job_age': {'retention_age': 'g', 'reporting_age': 'g'}}
        if (s['kind'] != 'master' or s.get('rrd_fields') != {'j2-svntp1': fields}
                or s.get('graphs') != {'j2-svntp1': sorted(fields)}
                or s.get('https_deadline_seconds') != 90
                or set(s.get('producer_completions', {})) != {'retention', 'reporting'}
                or any(type(t) not in (int, float) or not s['producer_installed_epoch'] < t <= s['prepared_epoch']
                       for t in s['producer_completions'].values())
                or not s.get('producer_observation_provenance')
                or set(s.get('native_limits_sources', {})) != set(LIMITS_SOURCES)
                or not max(s['producer_completions'].values()) <= s['collection_after_epoch'] <= s['prepared_epoch']
                or any(s['files'].get(p) != digest for p, digest in s['native_limits_sources'].items())):
            raise ValueError('maintenance observation boundary mismatch')
    if s.get('purpose') == 'expanded-observation':
        if (set(s['graphs']) != {'j2-svntp1', 'J1-SVMF'} or set(s['rrd_fields']) != set(s['graphs'])
                or not s['commissioned_epoch'] <= s['collection_after_epoch'] <= s['prepared_epoch']
                or s.get('https_deadline_seconds') != 180
                or not s.get('expanded_provenance')):
            raise ValueError('expanded observation boundary mismatch')
        dynamic = s.get('dynamic_rrd_counts', {})
        if (set(dynamic) != {'j2-svntp1'} or set(dynamic['j2-svntp1']) != {'df', 'df_inode'}
                or any(type(value) is not int or not 0 < value <= 64 for value in dynamic['j2-svntp1'].values())):
            raise ValueError('dynamic filesystem scope mismatch')
        count = sum(dynamic['j2-svntp1'].values())
        for host, graphs in s['graphs'].items():
            if (not 0 < len(graphs) <= 80 or len(graphs) != len(set(graphs))
                    or set(graphs) != set(s['rrd_fields'][host])):
                raise ValueError('expanded graph coverage mismatch')
            for graph in graphs:
                fields = s['rrd_fields'][host][graph]
                if (not re.fullmatch(r'[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)*', graph)
                        or not fields and graph not in dynamic.get(host, {})
                        or fields and graph in dynamic.get(host, {})
                        or any(not re.fullmatch(r'[A-Za-z0-9_]{1,80}', field)
                            or kind not in ('a', 'c', 'd', 'g') for field, kind in fields.items())):
                    raise ValueError('expanded filename scope mismatch')
                count += len(fields)
        if count > 384 or s['kind'] == 'node' and len(s.get('enabled_links', {})) != 33:
            raise ValueError('expanded field/selection bound')
    if (s.get('purpose', 'scheduled-observation') not in ('scheduled-observation', 'generic-profile', 'transport-metadata', 'contact-metadata', 'contact-observation', 'growth-t0', 'growth-checkpoint', 'expanded-observation', 'source-attribution', 'maintenance-observation', 'timing-observation')
            or s.get('purpose') == 'source-attribution' and (s['kind'] != 'master' or not s.get('expanded_provenance'))
            or s.get('purpose') == 'transport-metadata' and (s['kind'] != 'master'
                or set(s['transport_expected']) != {'sha256', 'mode', 'uid', 'gid', 'nlink'}
                or '/usr/local/munin/lib/plugins/ntp_transport_j2' in s['files'])
            or s['kind'] not in TARGETS or tuple(s[k] for k in ('endpoint', 'user', 'host_key_alias', 'hostname')) != TARGETS[s['kind']]
            or not re.fullmatch(r'munin-[a-z0-9-]{1,55}', s['operation_id'])
            or not 0 < s['expires_epoch']-s['prepared_epoch'] <= 86400
            or historical and s.get('purpose') not in ('growth-t0', 'growth-checkpoint')
            or not historical and not s['prepared_epoch'] <= time.time() < s['expires_epoch']-900
            or not historical and files['review.md'] != review(s).encode()):
        raise ValueError('scope/expiry/review binding mismatch')
    return s, files


def seal(args):
    source_attribution = getattr(args, 'source_attribution', False)
    maintenance = getattr(args, 'maintenance_fields', False)
    timing = getattr(args, 'timing_fields', False)
    if timing and (args.kind != 'master' or source_attribution or maintenance or args.transport_metadata or args.generic_profile
                   or not args.node_correction):
        raise ValueError('timing observation requires separate master scope and node correction')
    if maintenance and (args.kind != 'master' or source_attribution or args.transport_metadata or args.generic_profile
                        or not args.producer_followup or not args.native_limits_capture):
        raise ValueError('maintenance requires separate master scope and accepted producer/native inputs')
    if source_attribution and (args.kind != 'master' or args.transport_metadata or args.generic_profile):
        raise ValueError('source attribution requires separate expanded master scope')
    if args.transport_metadata and (args.kind != 'master' or args.generic_profile):
        raise ValueError('transport metadata requires a separate master-only scope')
    expanded = any((args.expanded_node, args.expanded_master, args.native))
    if expanded and (not all((args.expanded_node, args.expanded_master, args.native))
                     or args.transport_metadata or args.generic_profile):
        raise ValueError('separate expanded node/master/native inputs required')
    commissioning, outcome, provenance = accepted(args.commissioning, 'accepted')
    ms = json.loads(commissioning['spec.json'])
    if not outcome.get('committed') or not outcome.get('repository_reconciled'):
        raise ValueError('committed reconciled master required')
    producer, po, pp = accepted(args.producers, 'installation_accepted')
    nsfiles, no, np = accepted(args.node, 'node_runtime_accepted')
    ps = json.loads(producer['spec.json'])['worker']
    ns = json.loads(nsfiles['spec.json'])['worker']
    if (ps['hostname'] != 'j2-svntp1' or ns['hostname'] != 'j2-svntp1'
            or ps['boot_id'] != ns['boot_id'] or ms['worker']['hostname'] != 'J1-SVMF'):
        raise ValueError('accepted target/boot provenance mismatch')
    kind = args.kind
    endpoint, user, alias, hostname = TARGETS[kind]
    now = int(time.time())
    spec = {'kind': kind, 'endpoint': endpoint, 'user': user, 'host_key_alias': alias,
            'purpose': 'transport-metadata' if args.transport_metadata else 'generic-profile' if args.generic_profile else 'scheduled-observation',
            'hostname': hostname, 'operation_id': args.output.name, 'prepared_epoch': now,
            'expires_epoch': now+86400, 'commissioned_epoch': datetime.fromisoformat(outcome['completed_local']).timestamp(),
            'producer_installed_epoch': datetime.fromisoformat(po['completed_local']).timestamp(),
            'provenance': {'commissioning': provenance, 'producers': pp, 'node': np},
            'graphs': {'j2-svntp1': GRAPHS, 'J1-SVMF': ['ntp_transport_j2']}}
    if kind == 'node':
        spec.update(boot_id=ns['boot_id'], units={'timeservice.service': ns['service_identity']},
                    files=dict(ns['protected_files']))
        spec['files'].update({p: v['after_sha256'] for p, v in ps['files'].items()})
        spec['files'].update({p: v['sha256'] for p, v in ps['job_inputs'].items()})
        spec['files']['/usr/local/munin/lib/plugins/ntp_metrics.py'] = ns['artifacts']['node/plugins/ntp/ntp_metrics.py']
        known = nsfiles['known_hosts']
    else:
        pins = ms['worker']
        spec.update(boot_id=pins['boot_id'], units={'NetworkManager.service': pins['service_identity'],
                    'apache2.service': pins['apache_identity'], 'cron.service': pins['cron_identity']},
                    files=dict(pins['protected_files']))
        spec['files'].update({'/etc/munin/munin.conf': pins['candidate_sha256'],
            '/usr/local/munin/lib/plugins/ntp_transport_j2': sha(commissioning['plugin']),
            '/etc/munin/plugin-conf.d/ntp-transport.conf': sha(commissioning['settings'])})
        known = commissioning['known_hosts']
    spec.update(leaf_sha256=ms['leaf_sha256'])
    if args.transport_metadata:
        target = '/usr/local/munin/lib/plugins/ntp_transport_j2'
        spec['transport_expected'] = {'sha256': spec['files'].pop(target),
                                      'mode': 0o755, 'uid': 0, 'gid': 0, 'nlink': 1}
    if expanded:
        expand_observation(spec, args.expanded_node, args.expanded_master, args.native)
    if source_attribution:
        if not expanded:
            raise ValueError('expanded provenance required for source attribution')
        spec['purpose'] = 'source-attribution'
    if maintenance:
        if not expanded:
            raise ValueError('expanded provenance required for maintenance observation')
        followup = args.producer_followup
        proof = private(followup/'outcome.json')
        capture_raw = private(followup/'stdout.txt')
        archived = private(followup/'inspection.tar')
        accepted_producer = json.loads(proof)
        capture = json.loads(capture_raw)
        result = json.loads(private(followup/'result.json'))
        if (not accepted_producer.get('genuine_success_records_accepted')
                or accepted_producer.get('archive_sha256') != sha(archived)
                or accepted_producer.get('capture_sha256') != sha(capture_raw)
                or result.get('bundle_sha256') != sha(archived)
                or not result.get('capture_complete') or result.get('returncode') != 0
                or not capture.get('capture_complete') or capture['kind'] != 'node'
                or capture['before'] != capture['after']):
            raise ValueError('accepted producer follow-up required')
        fields = {'ntp_job_evidence': {'retention_evidence': 'g', 'reporting_evidence': 'g'},
                  'ntp_job_age': {'retention_age': 'g', 'reporting_age': 'g'}}
        completions = {}
        for job in ('retention', 'reporting'):
            row = capture['observations']['records'][job]
            if not row.get('valid_completion') or not row.get('fresh'):
                raise ValueError('valid fresh producer records required')
            completions[job] = row['completed_epoch']
        source_raw = private(args.native_limits_capture)
        native = json.loads(source_raw)['native_sources']
        source_pins = {path: native[path]['sha256'] for path in LIMITS_SOURCES}
        spec['files'].update(source_pins)
        spec.update(purpose='maintenance-observation', graphs={'j2-svntp1': sorted(fields)},
                    rrd_fields={'j2-svntp1': fields}, https_deadline_seconds=90,
                    collection_after_epoch=max(spec['collection_after_epoch'], *completions.values()),
                    producer_completions=completions, native_limits_sources=source_pins,
                    producer_observation_provenance={'archive_sha256': sha(archived), 'outcome_sha256': sha(proof),
                                                     'capture_sha256': sha(capture_raw)},
                    native_limits_capture_sha256=sha(source_raw))
        spec.pop('dynamic_rrd_counts', None)
    if timing:
        if not expanded:
            raise ValueError('expanded provenance required')
        raw = private(args.node_correction/'deployment.tar')
        with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
            rows = archive.getmembers()
            if (len(rows) > 128 or len({m.name for m in rows}) != len(rows)
                    or any(not m.isfile() or m.size > 1048576 for m in rows)):
                raise ValueError('bounded correction provenance required')
            correction = {m.name: archive.extractfile(m).read() for m in rows}
        if json.loads(correction['manifest.json']) != {n: sha(v) for n, v in correction.items() if n != 'manifest.json'}:
            raise ValueError('correction provenance drift')
        scope = json.loads(correction['spec.json'])
        if (scope['worker']['role'] != 'timing' or scope.get('contacts_disabled') is not True
                or scope['worker']['hostname'] != 'j2-svntp1'
                or scope['worker']['target'] != '/usr/local/munin/lib/plugins/ntp_metrics.py'):
            raise ValueError('fixed node correction required')
        if scope['master_inspection']['boot_id'] != spec['boot_id']:
            raise ValueError('accepted master boot provenance changed')
        spec['files'].update(scope['master_inspection']['files'])
        spec['units'] = scope['master_inspection']['units']
        expected = {'ntp_health': {name: 'g' for name in ('query_ok','synced','pps_selected','reach','stratum','leap','selected_offset_ok','selected_jitter_ok')},
                    'ntp_timing': {name: 'g' for name in ('system_offset','system_jitter','selected_offset','selected_jitter')}}
        spec.update(purpose='timing-observation', graphs={'j2-svntp1': sorted(expected)},
                    rrd_fields={'j2-svntp1': expected}, https_deadline_seconds=90,
                    correction_prerequisite={'directory': str(args.node_correction.absolute()), 'archive_sha256': sha(raw),
                                             'prepared_epoch': scope['prepared_epoch']})
        spec.pop('dynamic_rrd_counts', None)
    files = {n: p.read_bytes() for n, p in SOURCES.items()}
    files.update({'known_hosts': known, 'ca.pem': commissioning['ca.pem'],
                  'spec.json': encoded(spec), 'review.md': review(spec).encode()})
    files['manifest.json'] = encoded({n: sha(v) for n, v in files.items()})
    os.umask(0o077)
    args.output.mkdir(mode=0o700)
    for name, raw in files.items():
        (args.output/name).write_bytes(raw)
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode='w') as archive:
        for name, raw in sorted(files.items()):
            meta = tarfile.TarInfo(name)
            meta.mode = 0o600
            meta.size = len(raw)
            archive.addfile(meta, io.BytesIO(raw))
    raw = stream.getvalue()
    unpack(raw, sha(raw))
    (args.output/'inspection.tar').write_bytes(raw)
    result = {'sha256': sha(raw), 'expires_epoch': spec['expires_epoch'], 'target_contact': False}
    (args.output/'sealing.json').write_bytes(encoded(result))
    return result


def prepare(directory, digest):
    meta = directory.lstat()
    if (not stat.S_ISDIR(meta.st_mode) or meta.st_uid != os.getuid()
            or stat.S_IMODE(meta.st_mode) != 0o700):
        raise ValueError('owner-private directory required')
    spec, files = unpack(private(directory/'inspection.tar'), digest)
    if files['runner.py'] != Path(__file__).read_bytes():
        raise ValueError('frozen controller required')
    for name, raw in files.items():
        if private(directory/name) != raw:
            raise ValueError('frozen local input drift: '+name)
    return spec, files


def seal_contact_metadata(args):
    raw = private(args.activation/'deployment.tar')
    receipt = json.loads(private(args.activation/'execution.json'))
    result_raw = private(args.activation/'result.json')
    result = json.loads(result_raw)
    if (receipt['sha256'] != sha(raw) or result['archive_sha256'] != sha(raw)
            or result.get('accepted') or result.get('apply', {}).get('phase') != 'preflight-failed'
            or result['apply'].get('error') != 'unsafe authored file metadata: /etc/munin/munin.conf'):
        raise ValueError('consumed exact activation metadata rejection required')
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        rows = archive.getmembers()
        if len(rows) > 64 or len({m.name for m in rows}) != len(rows) or any(not m.isfile() or m.size > 1048576 for m in rows):
            raise ValueError('closed bounded activation input required')
        previous = {m.name: archive.extractfile(m).read() for m in rows}
    if json.loads(previous['manifest.json']) != {n: sha(v) for n, v in previous.items() if n != 'manifest.json'}:
        raise ValueError('activation input manifest mismatch')
    original = json.loads(previous['spec.json'])
    if original['kind'] != 'activation' or original['operation_id'] != 'munin-contacts-activate-20261022-v2':
        raise ValueError('fixed rejected activation required')
    now = time.time()
    scope = original['worker']
    endpoint, user, alias, hostname = TARGETS['master']
    spec = {'schema': 1, 'purpose': 'contact-metadata', 'kind': 'master', 'operation_id': args.output.name,
            'endpoint': endpoint, 'user': user, 'host_key_alias': alias, 'hostname': hostname,
            'boot_id': scope['boot_id'], 'prepared_epoch': now, 'expires_epoch': now+86400,
            'units': scope['units'], 'files': dict(scope['protected_files'], **{'/etc/munin/munin.conf': scope['before_sha256']}),
            'contact_expected': {'sha256': scope['before_sha256'], 'uid': 0, 'gid': 0, 'mode': 0o644, 'nlink': 1},
            'failed_activation_provenance': {'archive_sha256': sha(raw), 'result_sha256': sha(result_raw),
                                             'receipt_sha256': sha(private(args.activation/'execution.json'))}}
    files = {n: p.read_bytes() for n, p in SOURCES.items()}
    files.update({'known_hosts': previous['known_hosts'], 'ca.pem': b'', 'spec.json': encoded(spec), 'review.md': review(spec).encode()})
    files['manifest.json'] = encoded({n: sha(v) for n, v in files.items()})
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w') as archive:
        for name, data in sorted(files.items()):
            m = tarfile.TarInfo(name)
            m.mode = 0o600
            m.size = len(data)
            archive.addfile(m, io.BytesIO(data))
    raw = buffer.getvalue()
    unpack(raw, sha(raw))
    args.output.mkdir(mode=0o700)
    for name, data in files.items():
        (args.output/name).write_bytes(data)
    (args.output/'inspection.tar').write_bytes(raw)
    sealed = {'sha256': sha(raw), 'expires_epoch': spec['expires_epoch'], 'target_contact': False}
    (args.output/'sealing.json').write_bytes(encoded(sealed))
    return sealed


def seal_contact_observation(args):
    provenance, stages = {}, {}
    for kind, directory in (('activation', args.activation), ('problem', args.problem), ('recovery', args.recovery)):
        raw = private(directory/'deployment.tar')
        with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
            members = archive.getmembers()
            if (len(members) > 64 or len({m.name for m in members}) != len(members)
                    or any(not m.isfile() or m.size > 1048576 for m in members)):
                raise ValueError('bounded closed consumed contact archive required')
            contents = {m.name: archive.extractfile(m).read() for m in members}
        if json.loads(contents['manifest.json']) != {n: sha(v) for n, v in contents.items() if n != 'manifest.json'}:
            raise ValueError('consumed contact manifest mismatch')
        original = json.loads(contents['spec.json'])
        receipt_raw, result_raw = private(directory/'execution.json'), private(directory/'result.json')
        receipt, result = json.loads(receipt_raw), json.loads(result_raw)
        expected_id = 'munin-contacts-'+('activate-20261022-v3' if kind == 'activation' else kind+'-20261022-v2')
        if (original['kind'] != kind or original['operation_id'] != expected_id
                or original['worker']['hostname'] != 'J1-SVMF'
                or receipt['sha256'] != sha(raw) or result['archive_sha256'] != sha(raw)):
            raise ValueError('fixed consumed contact operation required')
        proof = {'archive_sha256': sha(raw), 'receipt_sha256': sha(receipt_raw), 'result_sha256': sha(result_raw)}
        if kind == 'activation':
            if (not all(result.get(k) is True for k in ('accepted', 'committed', 'repository_reconciled'))
                    or result.get('commit', {}).get('phase') != 'committed'
                    or (ROOT/'master/configs/munin.conf').read_bytes() != contents['candidate.conf']):
                raise ValueError('accepted reconciled activation and current repository mirror required')
        else:
            confirmation_raw = private(directory/'delivery-confirmation.json')
            confirmation = json.loads(confirmation_raw)
            prerequisite = original['activation_prerequisite']
            if (prerequisite['archive_sha256'] != provenance['activation']['archive_sha256']
                    or not result.get('attempted') or not result.get('status_recorded')
                    or type(result.get('submission_accepted')) is not bool
                    or result['message_sha256'] != sha(contents['message.eml'])
                    or confirmation.get('source') != 'operator' or confirmation.get('delivered') is not True
                    or not confirmation.get('acknowledgement', '').strip()
                    or confirmation.get('archive_sha256') != sha(raw)
                    or confirmation.get('message_sha256') != result['message_sha256']
                    or confirmation.get('execution_receipt_sha256') != sha(receipt_raw)):
                raise ValueError('consumed exact send with explicit downstream receipt required')
            if kind == 'recovery' and original['problem_prerequisite']['archive_sha256'] != provenance['problem']['archive_sha256']:
                raise ValueError('recovery must bind the consumed problem')
            proof.update(confirmation_sha256=sha(confirmation_raw), message_sha256=result['message_sha256'],
                         submission_accepted=result['submission_accepted'])
        provenance[kind] = proof
        stages[kind] = (original, contents, receipt)
    original, previous, receipt = stages['activation']
    worker = original['worker']
    token = {'operation_id': original['operation_id'], 'worker_sha256': sha(encoded(worker)),
             'config_sha256': sha(previous['candidate.conf']), 'helper_sha256': sha(previous['mailrise.py']),
             'gate_sha256': sha(previous['gate.py'])}
    now = time.time()
    endpoint, user, alias, hostname = TARGETS['master']
    spec = {'schema': 1, 'purpose': 'contact-observation', 'kind': 'master', 'operation_id': args.output.name,
            'endpoint': endpoint, 'user': user, 'host_key_alias': alias, 'hostname': hostname,
            'boot_id': worker['boot_id'], 'prepared_epoch': now, 'expires_epoch': now+86400,
            'units': worker['units'], 'files': dict(worker['protected_files'], **{
                '/etc/munin/munin.conf': token['config_sha256'],
                '/usr/local/libexec/munin-ntp-mailrise.py': token['helper_sha256'],
                '/usr/local/libexec/munin-ntp-contact-gate.py': token['gate_sha256'],
                '/var/lib/munin-ntp-contact-control/enabled.json': sha(encoded(token))}),
            'commissioned_epoch': receipt['epoch'], 'collection_after_epoch': receipt['epoch'],
            'graphs': {'J1-SVMF': ['ntp_transport_j2']},
            'rrd_fields': {'J1-SVMF': {'ntp_transport_j2': {'mail': 'g'}}},
            'contact_state_path': '/var/lib/munin-ntp-contacts/'+original['operation_id']+'/state.json',
            'contact_provenance': provenance}
    files = {n: p.read_bytes() for n, p in SOURCES.items()}
    files.update({'known_hosts': previous['known_hosts'], 'ca.pem': b'',
                  'spec.json': encoded(spec), 'review.md': review(spec).encode()})
    files['manifest.json'] = encoded({n: sha(v) for n, v in files.items()})
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w') as archive:
        for name, data in sorted(files.items()):
            m = tarfile.TarInfo(name)
            m.mode, m.size = 0o600, len(data)
            archive.addfile(m, io.BytesIO(data))
    raw = buffer.getvalue()
    unpack(raw, sha(raw))
    args.output.mkdir(mode=0o700)
    for name, data in files.items():
        (args.output/name).write_bytes(data)
    (args.output/'inspection.tar').write_bytes(raw)
    sealed = {'sha256': sha(raw), 'expires_epoch': spec['expires_epoch'], 'execution_ready': True, 'target_contact': False}
    (args.output/'sealing.json').write_bytes(encoded(sealed))
    return sealed


def growth_baselines(parent):
    records, stages = {}, {}
    for key, name in GROWTH_STAGES.items():
        directory = parent/name
        archive_name = 'deployment.tar' if key == 'timing' else 'inspection.tar'
        raw = private(directory/archive_name)
        receipt_raw, result_raw, outcome_raw = (private(directory/n) for n in ('execution.json', 'result.json', 'outcome.json'))
        receipt, result, outcome = map(json.loads, (receipt_raw, result_raw, outcome_raw))
        with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
            rows = archive.getmembers()
            if (len(rows) > 128 or len({m.name for m in rows}) != len(rows)
                    or any(not m.isfile() or m.size > 1048576 for m in rows)):
                raise ValueError('bounded growth baseline archive required')
            frozen = {m.name: archive.extractfile(m).read() for m in rows}
        if (json.loads(frozen['manifest.json']) != {n: sha(v) for n, v in frozen.items() if n != 'manifest.json'}
                or receipt.get('sha256') != sha(raw) or outcome.get('archive_sha256') != sha(raw)
                or result.get('archive_sha256', result.get('bundle_sha256')) != sha(raw)):
            raise ValueError('consumed growth baseline binding')
        original = json.loads(frozen['spec.json'])
        if key == 'timing':
            if not all(result.get(k) is True for k in ('accepted', 'committed', 'repository_reconciled')) or not outcome.get('node_timing_correction_accepted'):
                raise ValueError('accepted timing correction required')
            capture = None
        else:
            capture_raw = private(directory/'stdout.txt')
            capture = json.loads(capture_raw)
            flag = 'genuine_success_records_accepted' if key == 'producers' else 'mail_observation_accepted'
            if (not outcome.get(flag) or outcome.get('capture_sha256') != sha(capture_raw)
                    or not result.get('capture_complete') or result.get('returncode') != 0
                    or not capture.get('capture_complete') or capture['before'] != capture['after']
                    or capture.get('operation_id') != original['operation_id']
                    or capture.get('spec_sha256') != sha(encoded(original))):
                raise ValueError('accepted completed growth observation baseline required')
        records[key] = {'archive_sha256': sha(raw), 'receipt_sha256': sha(receipt_raw),
                        'result_sha256': sha(result_raw), 'outcome_sha256': sha(outcome_raw)}
        stages[key] = (original, frozen, capture)
    return records, stages


def accepted_growth(directory, kind, label='t0'):
    """Read immutable accepted proof as data; archive expiry never grants execution."""
    names = {'archive_sha256': 'inspection.tar', 'capture_sha256': 'stdout.txt',
             'receipt_sha256': 'execution.json', 'result_sha256': 'result.json',
             'outcome_sha256': 'outcome.json'}
    raw = {key: private(directory/name) for key, name in names.items()}
    proof = {'directory': str(directory.absolute()), **{key: sha(value) for key, value in raw.items()}}
    spec, _ = unpack(raw['archive_sha256'], proof['archive_sha256'], historical=True)
    capture, receipt, result, outcome = (json.loads(raw[key]) for key in
        ('capture_sha256', 'receipt_sha256', 'result_sha256', 'outcome_sha256'))
    epoch = outcome.get('node_t0_epoch')
    flag = 'growth_t0_' if label == 't0' else 'growth_checkpoint_'
    expected_purpose = 'growth-t0' if label == 't0' else 'growth-checkpoint'
    started = receipt.get('epoch')
    captured = capture.get('captured_epoch')
    if (spec['purpose'] != expected_purpose or spec['kind'] != kind
            or label != 't0' and spec['checkpoint_scope']['label'] != label
            or outcome.get(flag+kind+'_accepted') is not True
            or type(epoch) not in (int, float) or not math.isfinite(epoch) or not 0 < epoch <= time.time()
            or type(started) not in (int, float) or type(captured) not in (int, float)
            or not spec['prepared_epoch'] <= started < spec['expires_epoch']-900
            or not started <= captured < spec['expires_epoch']
            or receipt.get('sha256') != proof['archive_sha256']
            or result.get('bundle_sha256') != proof['archive_sha256']
            or result.get('returncode') != 0 or result.get('capture_complete') is not True
            or capture.get('capture_complete') is not True or capture.get('target_mutation') is not False
            or capture.get('spec_sha256') != sha(encoded(spec)) or capture.get('before') != capture.get('after')
            or any(outcome.get(key) != proof[key] for key in ('archive_sha256', 'capture_sha256'))
            or outcome.get('execution_receipt_sha256') != proof['receipt_sha256']):
        raise ValueError('exact reviewed accepted growth '+kind+' evidence required')
    if kind == 'node':
        sample_epoch = capture['observations']['statistics_before']['started_epoch']
        key = 'node_t0_epoch' if label == 't0' else 'checkpoint_node_epoch'
        if (outcome.get(key) != sample_epoch
                or not captured <= sample_epoch < spec['expires_epoch']):
            raise ValueError('actual accepted node snapshot epoch required')
        if label != 't0' and (spec['checkpoint_scope']['node_t0_epoch'] != epoch
                or sample_epoch < spec['checkpoint_scope']['not_before_epoch']):
            raise ValueError('historical checkpoint must preserve t0 and its due time')
    else:
        context_raw = private(directory/'runtime-context.json')
        context = json.loads(context_raw)
        if (capture.get('runtime_context_sha256') != sha(context_raw)
                or context.get('node_t0_epoch') != epoch
                or context.get('node_archive_sha256') != spec['node_t0_prerequisite']['archive_sha256']):
            raise ValueError('exact accepted growth pair context required')
        if label != 't0' and (spec['checkpoint_scope']['node_t0_epoch'] != epoch
                or outcome.get('checkpoint_node_epoch') != context.get('checkpoint_node_epoch')
                or type(context.get('checkpoint_node_epoch')) not in (int, float)
                or not spec['checkpoint_scope']['not_before_epoch'] <= context['checkpoint_node_epoch'] <= captured):
            raise ValueError('accepted checkpoint master must preserve the due node epoch')
    return proof, spec, epoch


def accepted_t0(directory, kind):
    return accepted_growth(directory, kind)


def previous_checkpoint(node, master, epoch, t0, label='+6h'):
    if label not in ('+6h', '+24h'):
        raise ValueError('closed preceding growth checkpoint required')
    node_ref, ns, node_epoch = accepted_growth(node, 'node', label)
    master_ref, ms, master_epoch = accepted_growth(master, 'master', label)
    paired = json.loads(private(master/'runtime-context.json'))
    if (node_epoch != epoch or master_epoch != epoch
            or ns['contract_sha256'] != ms['contract_sha256']
            or ns['checkpoint_scope'] != ms['checkpoint_scope']
            or ns['checkpoint_scope']['t0'] != t0
            or paired.get('node_archive_sha256') != node_ref['archive_sha256']
            or paired.get('node_capture_sha256') != node_ref['capture_sha256']
            or paired.get('node_receipt_sha256') != node_ref['receipt_sha256']
            or paired.get('node_outcome_sha256') != node_ref['outcome_sha256']):
        raise ValueError('exact accepted late checkpoint pair required')
    if label == '+6h':
        disposition_sha256 = sha(private(node/'restart-disposition.json'))
        if json.loads(private(master/'outcome.json')).get('operator_restart_disposition_sha256') != disposition_sha256:
            raise ValueError('reviewed overnight restart disposition changed')
    else:
        previous = ns['checkpoint_scope']['previous']
        verified = previous_checkpoint(Path(previous['node']['directory']),
                                       Path(previous['master']['directory']), epoch, t0, '+6h')
        if verified != previous:
            raise ValueError('preceding daily checkpoint historical chain changed')
        disposition_sha256 = verified['restart_disposition_sha256']
    return {'node': node_ref, 'master': master_ref,
            'restart_disposition_sha256': disposition_sha256}


def seal_growth_t0(args):
    records, stages = growth_baselines(args.output.absolute().parent)
    timing, _, _ = stages['timing']
    producer, _, _ = stages['producers']
    mail, mail_files, _ = stages['mail']
    worker = timing['worker']
    if (worker['hostname'] != 'j2-svntp1' or worker['boot_id'] != producer['boot_id']
            or worker['role'] != 'timing' or worker['mode'] != 0o644
            or worker['target'] != '/usr/local/munin/lib/plugins/ntp_metrics.py'):
        raise ValueError('current accepted node timing baseline required')
    kind = args.kind
    endpoint, user, alias, hostname = TARGETS[kind]
    now = time.time()
    files = {n: p.read_bytes() for n, p in SOURCES.items()}
    spec = {'schema': 1, 'purpose': 'growth-t0', 'kind': kind, 'operation_id': args.output.name,
            'endpoint': endpoint, 'user': user, 'host_key_alias': alias, 'hostname': hostname,
            'prepared_epoch': now, 'expires_epoch': now+86400, 'contract_sha256': sha(files['contract.md']),
            'growth_policy': GROWTH_POLICY, 'growth_provenance': records}
    checkpoint_node = getattr(args, 'checkpoint_node', None)
    if checkpoint_node is not None:
        node_ref, node_spec, epoch = accepted_t0(checkpoint_node, 'node')
        master_ref, master_spec, master_epoch = accepted_t0(args.checkpoint_master, 'master')
        if (epoch != master_epoch or master_spec['node_t0_prerequisite']['archive_sha256'] != node_ref['archive_sha256']
                or node_spec['contract_sha256'] != spec['contract_sha256']
                or master_spec['contract_sha256'] != spec['contract_sha256']):
            raise ValueError('same accepted t0 pair and contract required')
        paired = json.loads(private(args.checkpoint_master/'runtime-context.json'))
        if (paired.get('node_capture_sha256') != node_ref['capture_sha256']
                or paired.get('node_receipt_sha256') != node_ref['receipt_sha256']
                or paired.get('node_outcome_sha256') != node_ref['outcome_sha256']):
            raise ValueError('master t0 must bind this exact reviewed node t0 proof')
        label = '+'+args.action.removeprefix('seal-growth-')
        offset = GROWTH_CHECKPOINTS[label]
        spec.update(purpose='growth-checkpoint', checkpoint_scope={
            'label': label, 'offset_seconds': offset, 'node_t0_epoch': epoch,
            'not_before_epoch': epoch+offset, 't0': {'node': node_ref, 'master': master_ref}})
        if label in GROWTH_PREVIOUS:
            previous_label = GROWTH_PREVIOUS[label]
            previous = previous_checkpoint(args.previous_node, args.previous_master, epoch,
                                           spec['checkpoint_scope']['t0'], previous_label)
            _, prior_spec, _ = accepted_growth(args.previous_node, 'node', previous_label)
            if prior_spec['contract_sha256'] != spec['contract_sha256']:
                raise ValueError('same contract required across growth observations')
            spec['checkpoint_scope']['previous'] = previous
    if kind == 'node':
        protected = dict(worker['protected'])
        protected[worker['target']] = sha(base64.b64decode(worker['candidate'], validate=True))
        spec.update(boot_id=worker['boot_id'], units=worker['units'], files=protected,
                    producer_installed_epoch=producer['producer_installed_epoch'],
                    enabled_links=timing['node_inspection']['enabled_links'])
        spec['enabled_links_sha256'] = sha(encoded(spec['enabled_links']))
        previous = args.output.parent/GROWTH_STAGES['producers']
        transport = private(previous/'known_hosts')
    else:
        if args.node_t0 is None:
            raise ValueError('separately sealed node t0 prerequisite required')
        node_raw = private(args.node_t0/'inspection.tar')
        ns, _ = unpack(node_raw, sha(node_raw))
        if (ns['purpose'] != spec['purpose'] or ns['kind'] != 'node'
                or ns.get('checkpoint_scope') != spec.get('checkpoint_scope')
                or ns['contract_sha256'] != spec['contract_sha256'] or ns['growth_provenance'] != records):
            raise ValueError('same contract and accepted baselines required for t0 pair')
        fields = {'j2-svntp1': GROWTH_FIELDS, 'J1-SVMF': {'ntp_transport_j2': {'v4': 'g', 'v6': 'g', 'mail': 'g'}}}
        if {g: timing['node_inspection']['rrd_fields']['j2-svntp1'][g] for g in GROWTH_FIELDS} != GROWTH_FIELDS:
            raise ValueError('accepted native growth field mapping changed')
        spec.update(boot_id=mail['boot_id'], units=mail['units'], files=mail['files'],
                    commissioned_epoch=mail['commissioned_epoch'],
                    collection_after_epoch=spec.get('checkpoint_scope', {}).get('node_t0_epoch', mail['collection_after_epoch']),
                    graphs={host: sorted(graphs) for host, graphs in fields.items()}, rrd_fields=fields,
                    contact_state_path=mail['contact_state_path'],
                    node_t0_prerequisite={'directory': str(args.node_t0.absolute()), 'archive_sha256': sha(node_raw),
                                          'contract_sha256': spec['contract_sha256']})
        transport = mail_files['known_hosts']
    spec['baseline_files_sha256'] = sha(encoded(spec['files']))
    files.update({'spec.json': encoded(spec), 'known_hosts': transport, 'ca.pem': b'', 'review.md': review(spec).encode()})
    files['manifest.json'] = encoded({n: sha(v) for n, v in files.items()})
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w') as archive:
        for name, data in sorted(files.items()):
            row = tarfile.TarInfo(name)
            row.mode, row.size = 0o600, len(data)
            archive.addfile(row, io.BytesIO(data))
    raw = buffer.getvalue()
    unpack(raw, sha(raw))
    args.output.mkdir(mode=0o700)
    for name, data in files.items():
        (args.output/name).write_bytes(data)
    (args.output/'inspection.tar').write_bytes(raw)
    sealed = {'sha256': sha(raw), 'expires_epoch': spec['expires_epoch'], 'execution_ready': True, 'target_contact': False}
    (args.output/'sealing.json').write_bytes(encoded(sealed))
    return sealed


def node_t0_context(spec):
    prerequisite = spec['node_t0_prerequisite']
    previous = Path(prerequisite['directory'])
    raw = private(previous/'inspection.tar')
    ns, _ = unpack(raw, prerequisite['archive_sha256'])
    receipt_raw, capture_raw, outcome_raw = (private(previous/n) for n in ('execution.json', 'stdout.txt', 'outcome.json'))
    receipt, capture, outcome = map(json.loads, (receipt_raw, capture_raw, outcome_raw))
    result = json.loads(private(previous/'result.json'))
    epoch = capture['observations']['statistics_before']['started_epoch']
    checkpoint = spec.get('checkpoint_scope')
    accepted_key = 'growth_checkpoint_node_accepted' if checkpoint else 'growth_t0_node_accepted'
    epoch_key = 'checkpoint_node_epoch' if checkpoint else 'node_t0_epoch'
    if (ns['purpose'] != spec['purpose'] or ns.get('checkpoint_scope') != checkpoint or ns['kind'] != 'node' or ns['contract_sha256'] != spec['contract_sha256']
            or receipt.get('sha256') != sha(raw) or result.get('bundle_sha256') != sha(raw)
            or result.get('returncode') != 0 or not result.get('capture_complete')
            or capture.get('spec_sha256') != sha(encoded(ns)) or not capture.get('capture_complete')
            or capture['before'] != capture['after'] or capture.get('target_mutation') is not False
            or outcome.get(accepted_key) is not True or outcome.get('archive_sha256') != sha(raw)
            or outcome.get('capture_sha256') != sha(capture_raw)
            or outcome.get('execution_receipt_sha256') != sha(receipt_raw)
            or outcome.get(epoch_key) != epoch
            or checkpoint and epoch < checkpoint['not_before_epoch']):
        raise ValueError('accepted exact node t0 capture/outcome required before master contact')
    return {'node_archive_sha256': sha(raw), 'node_t0_epoch': checkpoint['node_t0_epoch'] if checkpoint else epoch,
            'checkpoint_node_epoch': epoch,
            'node_capture_sha256': sha(capture_raw), 'node_receipt_sha256': sha(receipt_raw),
            'node_outcome_sha256': sha(outcome_raw)}


def payload(spec, files, context=None):
    alarm = 480 if spec.get('purpose') == 'source-attribution' else 240
    growth = b''
    call = b"cs['collect']"
    if spec.get('purpose') in ('growth-t0', 'growth-checkpoint'):
        growth = (b"ss={'__name__':'statistics','__file__':'/sealed/statistics.py'}\nexec("+
                  repr(files['statistics.py']).encode()+b",ss)\nss['h']=h\n"+
                  b"gs={'__name__':'growth','__file__':'/sealed/growth.py'}\nexec("+
                  repr(files['growth.py']).encode()+b",gs)\ngs.update(h=h,observer=types.SimpleNamespace(**cs),statistics=types.SimpleNamespace(**ss))\n")
        call = b"gs['collect']"
    return (b"ns={'__name__':'helper','__file__':'/sealed/helper.py'}\nexec("+
        repr(files['helper.py']).encode()+b",ns)\nimport types,signal,json\nh=types.SimpleNamespace(**ns)\n"+
        b"cs={'__name__':'collector','__file__':'/sealed/collector.py','h':h}\nexec("+
        repr(files['collector.py']).encode()+b",cs)\ncs['h']=h\n"+
        growth+b"signal.signal(signal.SIGALRM,h.expired)\nsignal.alarm("+str(alarm).encode()+b")\nprint(json.dumps("+call+b"("+
        repr(spec).encode()+b","+repr(context).encode()+b")))\n")


def https_paths(spec):
    if spec.get('purpose') == 'generic-profile':
        return ['/'+host+'/'+host+'/index.html' for host in ('j2-svpi4mf', 'j2-svntp1')]
    return ['/', '/static/style-new.css', '/j2-svntp1/j2-svntp1/index.html']+[
        '/munin-cgi/munin-cgi-graph/'+host+'/'+host+'/'+graph.replace('.', '/')+'-day.png'
        for host, graphs in spec['graphs'].items() for graph in graphs]


def execute(directory, digest):
    spec, files = prepare(directory, digest)
    context = None
    if spec.get('purpose') == 'growth-checkpoint':
        checkpoint = spec['checkpoint_scope']
        if time.time() < checkpoint['not_before_epoch']:
            raise ValueError(checkpoint['label']+' checkpoint is not due; no receipt consumed or target contact')
        for role, expected in checkpoint['t0'].items():
            proof, _, epoch = accepted_t0(Path(expected['directory']), role)
            if proof != expected or epoch != checkpoint['node_t0_epoch']:
                raise ValueError('accepted t0 proof changed before checkpoint access')
        if 'previous' in checkpoint:
            previous = checkpoint['previous']
            current = previous_checkpoint(Path(previous['node']['directory']),
                                          Path(previous['master']['directory']), checkpoint['node_t0_epoch'], checkpoint['t0'],
                                          GROWTH_PREVIOUS[checkpoint['label']])
            if current != previous:
                raise ValueError('accepted late checkpoint proof changed before target contact')
    if spec.get('purpose') in ('growth-t0', 'growth-checkpoint'):
        current, _ = growth_baselines(directory.parent)
        if current != spec['growth_provenance']:
            raise ValueError('accepted growth baseline provenance changed before target contact')
        if spec['kind'] == 'master':
            context = node_t0_context(spec)
    if spec.get('purpose') == 'contact-observation':
        for kind, expected in spec['contact_provenance'].items():
            stage_id = 'munin-contacts-'+('activate-20261022-v3' if kind == 'activation' else kind+'-20261022-v2')
            previous = directory.parent/stage_id
            inputs = {'archive_sha256': 'deployment.tar', 'receipt_sha256': 'execution.json', 'result_sha256': 'result.json'}
            if kind != 'activation':
                inputs.update(confirmation_sha256='delivery-confirmation.json', message_sha256='message.eml')
            if any(sha(private(previous/name)) != expected[key] for key, name in inputs.items()):
                raise ValueError('retained contact prerequisite drift before target contact')
    if spec.get('purpose') == 'timing-observation':
        prerequisite = spec['correction_prerequisite']
        previous = Path(prerequisite['directory'])
        result = json.loads(private(previous/'result.json'))
        receipt = json.loads(private(previous/'execution.json'))
        if (receipt.get('sha256') != prerequisite['archive_sha256']
                or result.get('archive_sha256') != prerequisite['archive_sha256']
                or not all(result.get(k) is True for k in ('accepted','committed','repository_reconciled'))
                or result.get('commit', {}).get('phase') != 'committed'
                or type(result.get('commit_finished_epoch')) not in (int,float)
                or not prerequisite['prepared_epoch'] < result['commit_finished_epoch'] <= time.time()):
            raise ValueError('accepted committed correction required before master contact')
        context = {'node_archive_sha256': prerequisite['archive_sha256'],
                   'commit_finished_epoch': result['commit_finished_epoch']}
    helper, _ = module(files['helper.py'], 'helper')
    argv = helper.ssh_argv({'endpoints': [spec['endpoint']], 'host_key_alias': spec['host_key_alias']}, directory)
    argv[-2] = spec['user']+'@'+spec['endpoint']
    submitted = payload(spec, files, context)
    if context is not None:
        (directory/'runtime-context.json').write_bytes(encoded(context))
    with (directory/'execution.json').open('xb') as stream:
        stream.write(encoded({'sha256': digest, 'epoch': time.time(), 'argv': argv,
                              'payload_sha256': sha(submitted)}))
        stream.flush()
        os.fsync(stream.fileno())
    row = helper.bounded(argv, timeout=510 if spec.get('purpose') == 'source-attribution' else 270,
                         limit=8388608, payload=submitted, env=os.environ.copy())
    for name in ('stdout', 'stderr'):
        (directory/(name+'.txt')).write_text(row.pop(name))
    row.update(bundle_sha256=digest, capture_complete=False, delivery_accepted=False)
    if row.get('returncode') == 0 and not row.get('error'):
        capture = json.loads((directory/'stdout.txt').read_text())
        if capture.get('operation_id') != spec['operation_id'] or capture.get('spec_sha256') != sha(encoded(spec)):
            raise ValueError('capture scope binding')
        if context is not None and capture.get('runtime_context_sha256') != sha(encoded(context)):
            raise ValueError('runtime correction context binding')
        row['capture_complete'] = capture.get('capture_complete') is True
        if (row['capture_complete'] and spec['kind'] == 'master'
                and spec.get('purpose') not in ('transport-metadata', 'contact-metadata', 'contact-observation', 'growth-t0', 'growth-checkpoint', 'source-attribution')):
            probe, _ = module(files['tls-probe.py'], 'probe')
            context = ssl.create_default_context(cadata=files['ca.pem'].decode('ascii'))
            paths = https_paths(spec)
            observations = []
            deadline = time.monotonic()+spec.get('https_deadline_seconds', 3600)
            for address in ('10.1.3.83', 'fd36:5aa8:6971:1::83'):
                for path in paths:
                    if time.monotonic() >= deadline:
                        row['https_complete'] = False
                        row['https_finding'] = 'aggregate HTTPS deadline reached'
                        break
                    result, links = probe.request(address, path, context)
                    if spec.get('purpose') == 'generic-profile':
                        result['safe_links'] = links
                    observations.append(result)
                    expected_type = 'image/png' if path.endswith('.png') else 'text/css' if path.endswith('.css') else 'text/html'
                    if (time.monotonic() > deadline or not result.get('tls_verified') or not result.get('response_ok')
                            or result.get('leaf_sha256') != spec['leaf_sha256']
                            or result.get('content_type') != expected_type
                            or expected_type == 'image/png' and not result.get('png_signature')):
                        row['https_complete'] = False
                        break
                else:
                    continue
                break
            else:
                row['https_complete'] = True
            (directory/'https.json').write_bytes(encoded(observations))
    row.update(readiness_accepted=False, evidence_review_required=True)
    (directory/'result.json').write_bytes(encoded(row))
    return row


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    q = sub.add_parser('seal')
    q.add_argument('--kind', choices=TARGETS, required=True)
    q.add_argument('--generic-profile', action='store_true')
    q.add_argument('--transport-metadata', action='store_true')
    q.add_argument('--source-attribution', action='store_true')
    q.add_argument('--maintenance-fields', action='store_true')
    q.add_argument('--producer-followup', type=Path)
    q.add_argument('--native-limits-capture', type=Path)
    q.add_argument('--timing-fields', action='store_true')
    q.add_argument('--node-correction', type=Path)
    for name in ('expanded-node', 'expanded-master', 'native'):
        q.add_argument('--'+name, type=Path)
    for name in ('commissioning', 'producers', 'node', 'output'):
        q.add_argument('--'+name, type=Path, required=True)
    q = sub.add_parser('seal-contact-metadata')
    q.add_argument('--activation', type=Path, required=True)
    q.add_argument('--output', type=Path, required=True)
    q = sub.add_parser('seal-contact-observation')
    for name in ('activation', 'problem', 'recovery', 'output'):
        q.add_argument('--'+name, type=Path, required=True)
    q = sub.add_parser('seal-growth-t0')
    q.add_argument('--kind', choices=TARGETS, required=True)
    q.add_argument('--output', type=Path, required=True)
    q.add_argument('--node-t0', type=Path)
    for stage in ('6h', '24h', '48h'):
        q = sub.add_parser('seal-growth-'+stage)
        q.add_argument('--kind', choices=TARGETS, required=True)
        q.add_argument('--output', type=Path, required=True)
        q.add_argument('--checkpoint-node', type=Path, required=True)
        q.add_argument('--checkpoint-master', type=Path, required=True)
        q.add_argument('--node-t0', type=Path)
        if stage in ('24h', '48h'):
            q.add_argument('--previous-node', type=Path, required=True)
            q.add_argument('--previous-master', type=Path, required=True)
    for action in ('check', 'execute'):
        q = sub.add_parser(action)
        q.add_argument('--directory', type=Path, required=True)
        q.add_argument('--sha256', required=True)
    args = parser.parse_args()
    if args.action == 'seal':
        result = seal(args)
    elif args.action == 'seal-contact-metadata':
        result = seal_contact_metadata(args)
    elif args.action == 'seal-contact-observation':
        result = seal_contact_observation(args)
    elif args.action in ('seal-growth-t0', 'seal-growth-6h', 'seal-growth-24h', 'seal-growth-48h'):
        result = seal_growth_t0(args)
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
