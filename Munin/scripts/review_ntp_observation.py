#!/usr/bin/python3
"""Seal separate, one-use read-only node and native-master observations."""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re
import signal
import ssl
import stat
import tarfile
import time
import types

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent.parent
SOURCES = {'runner.py': Path(__file__), 'collector.py': ROOT/'scripts/observe_ntp.py',
           'helper.py': WORKSPACE/'homelab-ntp/ntpsec/scripts/run-production-inspection.py',
           'tls-probe.py': WORKSPACE/'homelab-network/Ubiquiti/munin-master-profile/qualify_dashboard.py',
           'tests.py': ROOT/'tests/test_ntp_observation.py'}
TARGETS = {'node': ('10.1.0.51', 'ama', '10.1.0.137', 'j2-svntp1'),
           'master': ('10.1.3.83', 'pi', 'svmf.local.theama.co', 'J1-SVMF')}
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


def unpack(raw, digest):
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
    if (s.get('purpose', 'scheduled-observation') not in ('scheduled-observation', 'generic-profile', 'transport-metadata', 'expanded-observation')
            or s.get('purpose') == 'transport-metadata' and (s['kind'] != 'master'
                or set(s['transport_expected']) != {'sha256', 'mode', 'uid', 'gid', 'nlink'}
                or '/usr/local/munin/lib/plugins/ntp_transport_j2' in s['files'])
            or s['kind'] not in TARGETS or tuple(s[k] for k in ('endpoint', 'user', 'host_key_alias', 'hostname')) != TARGETS[s['kind']]
            or not re.fullmatch(r'munin-[a-z0-9-]{1,55}', s['operation_id'])
            or not 0 < s['expires_epoch']-s['prepared_epoch'] <= 86400
            or not s['prepared_epoch'] <= time.time() < s['expires_epoch']-900
            or files['review.md'] != review(s).encode()):
        raise ValueError('scope/expiry/review binding mismatch')
    return s, files


def seal(args):
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


def payload(spec, files):
    return (b"ns={'__name__':'helper','__file__':'/sealed/helper.py'}\nexec("+
        repr(files['helper.py']).encode()+b",ns)\nimport types,signal,json\nh=types.SimpleNamespace(**ns)\n"+
        b"cs={'__name__':'collector','__file__':'/sealed/collector.py','h':h}\nexec("+
        repr(files['collector.py']).encode()+b",cs)\ncs['h']=h\n"+
        b"signal.signal(signal.SIGALRM,h.expired)\nsignal.alarm(240)\nprint(json.dumps(cs['collect']("+
        repr(spec).encode()+b")))\n")


def https_paths(spec):
    if spec.get('purpose') == 'generic-profile':
        return ['/'+host+'/'+host+'/index.html' for host in ('j2-svpi4mf', 'j2-svntp1')]
    return ['/', '/static/style-new.css', '/j2-svntp1/j2-svntp1/index.html']+[
        '/munin-cgi/munin-cgi-graph/'+host+'/'+host+'/'+graph.replace('.', '/')+'-day.png'
        for host, graphs in spec['graphs'].items() for graph in graphs]


def execute(directory, digest):
    spec, files = prepare(directory, digest)
    helper, _ = module(files['helper.py'], 'helper')
    argv = helper.ssh_argv({'endpoints': [spec['endpoint']], 'host_key_alias': spec['host_key_alias']}, directory)
    argv[-2] = spec['user']+'@'+spec['endpoint']
    submitted = payload(spec, files)
    with (directory/'execution.json').open('xb') as stream:
        stream.write(encoded({'sha256': digest, 'epoch': time.time(), 'argv': argv,
                              'payload_sha256': sha(submitted)}))
        stream.flush()
        os.fsync(stream.fileno())
    row = helper.bounded(argv, timeout=270, limit=8388608, payload=submitted, env=os.environ.copy())
    for name in ('stdout', 'stderr'):
        (directory/(name+'.txt')).write_text(row.pop(name))
    row.update(bundle_sha256=digest, capture_complete=False, delivery_accepted=False)
    if row.get('returncode') == 0 and not row.get('error'):
        capture = json.loads((directory/'stdout.txt').read_text())
        if capture.get('operation_id') != spec['operation_id'] or capture.get('spec_sha256') != sha(encoded(spec)):
            raise ValueError('capture scope binding')
        row['capture_complete'] = capture.get('capture_complete') is True
        if row['capture_complete'] and spec['kind'] == 'master' and spec.get('purpose') != 'transport-metadata':
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
    for name in ('expanded-node', 'expanded-master', 'native'):
        q.add_argument('--'+name, type=Path)
    for name in ('commissioning', 'producers', 'node', 'output'):
        q.add_argument('--'+name, type=Path, required=True)
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
