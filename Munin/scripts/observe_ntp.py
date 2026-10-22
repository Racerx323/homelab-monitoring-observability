#!/usr/bin/python3
"""Bounded observation of existing NTP producer and native Munin evidence."""
from datetime import datetime
import hashlib
import json
import math
import os
import pwd
from pathlib import Path
import re
import socket
import stat
import time

h = None  # Supplied from the authenticated repository-owned helper.


def read(path, limit=1048576, tail=False):
    path = Path(path)
    if any(p.is_symlink() for p in path.parents):
        raise ValueError('indirect observation path')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode):
            raise ValueError('regular observation file required')
        if tail:
            stream.seek(max(0, before.st_size-limit))
        raw = stream.read(limit+1)
        after = os.fstat(stream.fileno())
    if len(raw) > limit:
        raise ValueError('observation byte bound')
    if not tail and (before.st_ino, before.st_size, before.st_mtime_ns) != (
            after.st_ino, after.st_size, after.st_mtime_ns):
        raise ValueError('observation changed during read')
    if tail and before.st_size > limit:
        raw = raw.split(b'\n', 1)[-1]
    return raw, {'uid': before.st_uid, 'gid': before.st_gid,
                 'mode': stat.S_IMODE(before.st_mode), 'mtime': before.st_mtime,
                 'size': before.st_size, 'inode': before.st_ino, 'nlink': before.st_nlink,
                 'device': before.st_dev, 'sha256': hashlib.sha256(raw).hexdigest(),
                 'tail_only': tail, 'tail_grew': after.st_size != before.st_size}


def command(argv, limit=1048576):
    row = h.bounded(argv, timeout=20, limit=limit)
    if row.get('returncode') != 0 or row.get('error'):
        raise ValueError('read-only command failed: '+argv[0])
    return row['stdout']


def continuity(spec):
    if (os.geteuid() != 0 or os.getegid() != 0
            or socket.gethostname() != spec['hostname']
            or Path('/proc/sys/kernel/random/boot_id').read_text().strip() != spec['boot_id']):
        raise ValueError('root/host/boot continuity mismatch')
    units = {}
    for name, expected in spec['units'].items():
        output = command(['/usr/bin/systemctl', 'show', name, '--property='+','.join(expected)])
        fields = dict(line.split('=', 1) for line in output.splitlines())
        if fields != expected:
            raise ValueError('service continuity mismatch: '+name)
        units[name] = fields
    output = command(['/usr/bin/systemctl', 'show', 'munin-node.service',
                      '--property=ActiveState,SubState,MainPID,InvocationID,NRestarts'])
    units['munin-node.service'] = dict(line.split('=', 1) for line in output.splitlines())
    if (units['munin-node.service'].get('ActiveState') != 'active'
            or units['munin-node.service'].get('SubState') != 'running'):
        raise ValueError('Munin-node is not running')
    hashes = {}
    for path, expected in spec['files'].items():
        raw, meta = read(path)
        if meta['uid'] != 0 or meta['mode'] & 0o022 or hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError('protected observation input drift: '+path)
        hashes[path] = expected
    return {'units': units, 'file_hashes': hashes}


def success(raw, meta, job, now, installed):
    try:
        value = json.loads(raw)
        epoch = value['completed_epoch']
        valid = (meta['uid'] == 0 and meta['gid'] == 0 and meta['mode'] == 0o600
                 and len(raw) <= 4096 and type(value.get('schema')) is int and value.get('schema') == 1
                 and value.get('job') == job and value.get('status') == 'success'
                 and type(epoch) in (int, float) and math.isfinite(epoch)
                 and installed < epoch <= now)
        return {'valid_completion': valid, 'completed_epoch': epoch if valid else None,
                'fresh': valid and now-epoch <= 172800,
                'age_seconds': now-epoch if valid else None,
                'scheduled_provenance_accepted': False}
    except (ValueError, KeyError, TypeError, AttributeError):
        return {'valid_completion': False, 'scheduled_provenance_accepted': False}


def journal(unit, start):
    text = command(['/usr/bin/journalctl', '--unit='+unit, '--since=@'+str(int(start)),
                    '--no-pager', '--output=json'], limit=2097152)
    rows = []
    for line in text.splitlines():
        row = json.loads(line)
        message = row.get('MESSAGE', '')
        if isinstance(message, str):
            rows.append((int(row['__REALTIME_TIMESTAMP'])/1000000, message))
    return rows


def node(spec, now):
    records = {}
    for job, path in (('retention', '/var/lib/ntpstats-retention/last-success.json'),
                      ('reporting', '/var/lib/needrestart-reporting/last-success.json')):
        try:
            raw, meta = read(path, 4096)
            parents = [Path(path).parent.lstat()]
            safe = all(stat.S_ISDIR(m.st_mode) and m.st_uid == 0 and m.st_gid == 0 and not m.st_mode & 0o077
                       for m in parents)
            row = success(raw, meta, job, now, spec['producer_installed_epoch'])
            if not safe:
                row.update(valid_completion=False, fresh=False, unsafe_parent=True)
            records[job] = dict(row, metadata=meta)
        except (OSError, ValueError) as error:
            records[job] = {'valid_completion': False, 'fresh': False, 'finding': str(error)}
    events = {}
    for unit in ('cron.service', 'logrotate.service'):
        try:
            events[unit] = [{'epoch': epoch, 'event': 'reporting-cron' if unit == 'cron.service' else 'logrotate-unit'}
                            for epoch, message in journal(unit, max(now-172800, spec['producer_installed_epoch']))
                            if ((unit == 'cron.service' and re.search(
                                r'\(root\) CMD \([^\n]*?/usr/local/sbin/needrestart\.sh(?:\s|\))', message))
                                or unit == 'logrotate.service' and re.search(
                                    r'(?i)\b(starting|started|finished|failed|succeeded)\b', message))]
        except (OSError, ValueError) as error:
            events[unit] = {'finding': str(error)}
    selection = None
    if spec.get('purpose') == 'expanded-observation':
        actual = {}
        for name in listing('/etc/munin/plugins'):
            if name.startswith('.'):
                continue
            path = Path('/etc/munin/plugins')/name
            info = path.lstat()
            if not stat.S_ISLNK(info.st_mode) or info.st_uid != 0:
                raise ValueError('expanded selection is not a root-owned link')
            actual[name] = ['link', os.readlink(path)]
        if actual != spec['enabled_links']:
            raise ValueError('expanded enabled selection changed')
        selection = {'exact_enabled_links': actual, 'complete': True}
    return {'records': records, 'scheduler_events': events, 'expanded_selection': selection,
            'retention_timer': command(['/usr/bin/systemctl', 'show', 'logrotate.timer',
                '--property=ActiveState,SubState,LastTriggerUSec,NextElapseUSecRealtime']),
            'scheduler_only_is_not_rule_success': True,
            'scheduled_provenance_requires_review': True}


def log_events(raw):
    """Retain only event kinds, timestamps and fixed node identifiers."""
    events = []
    for line in raw.decode(errors='replace').splitlines():
        match = re.match(r'(20\d\d[-/]\d\d[-/]\d\d)[- T](\d\d:\d\d:\d\d)', line)
        if not match:
            continue
        epoch = datetime.fromisoformat(match[1].replace('/', '-')+'T'+match[2]).timestamp()
        kind = None
        if 'Starting munin-update' in line:
            kind = 'start'
        elif re.search(r'Munin-update finished \(', line):
            kind = 'finish'
        elif 'Munin-update finished for node' in line:
            if re.search(r'\bj2-svntp1(?:[/:;\s]|$)', line):
                kind = 'j2-finish'
            elif re.search(r'\bJ1-SVMF(?:[/:;\s]|$)', line):
                kind = 'master-finish'
        if re.search(r'\b(?:ERROR|FATAL|WARNING)\b', line):
            kind = 'fault'
        if kind:
            events.append({'epoch': epoch, 'kind': kind})
    return events


def cycles(events, cron_events, after, now):
    """A log window is evidence only with native cron and both completed nodes."""
    result = []
    starts = [e['epoch'] for e in events if e['kind'] == 'start' and after < e['epoch'] < now-240]
    for start in starts:
        bucket = int(start)//300*300
        window = [e for e in events if start <= e['epoch'] < start+240]
        kinds = {e['kind'] for e in window}
        complete = (start-bucket <= 60 and {'finish', 'j2-finish', 'master-finish'} <= kinds
                    and 'fault' not in kinds and sum(e['kind'] == 'start' for e in window) == 1
                    and any(abs(t-start) <= 60 for t in cron_events))
        result.append({'start': start, 'bucket': bucket, 'complete': complete,
                       'event_kinds': sorted(kinds)})
    # Do not skip a failed/missing intervening cycle to manufacture a passing triple.
    latest = result[-3:]
    passed = (len(latest) == 3 and all(c['complete'] for c in latest)
              and len({c['bucket'] for c in latest}) == 3
              and [c['bucket']-latest[0]['bucket'] for c in latest] == [0, 300, 600])
    return {'latest_three': latest, 'three_scheduled_cycles_evidenced': passed}


def rrd_rows(text):
    result = {}
    for line in text.splitlines():
        match = re.fullmatch(r'\s*(\d+):\s+([^\s]+)\s*', line)
        if match:
            value = float('nan') if match[2].lower() in ('u', 'unknown', '-nan') else float(match[2])
            result[int(match[1])] = value if math.isfinite(value) else None
    return result


def rrds(spec, now):
    end = (int(now)-300)//300*300
    result = {}
    count = 0
    for host, graphs in spec['graphs'].items():
        directory = Path('/var/lib/munin')/host
        if directory.is_symlink() or not directory.is_dir():
            result[host] = {'finding': 'expected direct native RRD directory missing'}
            continue
        entries = list(directory.iterdir())
        if len(entries) > 512:
            raise ValueError('RRD directory bound')
        host_rows = {}
        for graph in graphs:
            expected = spec.get('rrd_fields', {}).get(host, {}).get(graph)
            dynamic = spec.get('dynamic_rrd_counts', {}).get(host, {}).get(graph)
            if dynamic is not None:
                selected = [p for p in entries if re.fullmatch(
                    re.escape(host+'-'+graph)+r'-[A-Za-z0-9_]{1,80}-g\.rrd', p.name)]
                if len(selected) > 64:
                    raise ValueError('filesystem RRD field bound')
                missing = []
            elif expected is not None:
                filenames = {host+'-'+graph.replace('.', '-')+'-'+field+'-'+kind+'.rrd'
                             for field, kind in expected.items()}
                selected = [p for p in entries if p.name in filenames]
                missing = sorted(filenames-{p.name for p in selected})
            else:
                selected = [p for p in entries if re.fullmatch(
                    re.escape(host+'-'+graph)+r'-[A-Za-z0-9_]{1,80}-[acdg]\.rrd', p.name)]
                missing = []
            rows = []
            for path in sorted(selected):
                count += 1
                if count > (384 if 'rrd_fields' in spec else 128):
                    raise ValueError('selected RRD file bound')
                if path.is_symlink() or not path.is_file():
                    raise ValueError('indirect RRD')
                before = path.stat()
                if any(p.is_symlink() for p in path.parents):
                    raise ValueError('indirect RRD ancestor')
                last = command(['/usr/bin/rrdtool', 'lastupdate', str(path)], limit=4096)
                fetched = command(['/usr/bin/rrdtool', 'fetch', str(path), 'AVERAGE',
                    '--resolution', '300', '--start', str(end-1500), '--end', str(end)], limit=16384)
                after = path.stat()
                if (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino):
                    raise ValueError('RRD replaced during read')
                rows.append({'filename': path.name, 'mtime': before.st_mtime, 'last_update': rrd_rows(last),
                             'average_300': rrd_rows(fetched)})
            host_rows[graph] = {'files': rows, 'missing': not rows or bool(missing),
                                'missing_expected_files': missing}
            if dynamic is not None:
                threshold = max(spec['collection_after_epoch'], now-900)
                recent = sum(bool(row['last_update']) and max(row['last_update']) >= threshold for row in rows)
                host_rows[graph].update(deployment_field_count=dynamic, recent_field_count=recent,
                                        field_membership_review_required=True)
        result[host] = host_rows
    return {'aligned_end': end, 'resolution': 300, 'data': result,
            'consolidation_is_not_individual_raw_fetch': True}


def master(spec, now):
    findings = []
    after = spec.get('collection_after_epoch', spec['commissioned_epoch'])
    try:
        raw, meta = read('/var/log/munin/munin-update.log', 1048576, tail=True)
        start = max(now-7200, after)
        events = [event for event in log_events(raw) if start <= event['epoch'] <= now]
    except (OSError, ValueError) as error:
        meta = {'finding': str(error)}
        events = []
    try:
        cron = [epoch for epoch, message in journal('cron.service', max(now-7200, after))
                if re.search(r'\(munin\) CMD \([^\n]*?/usr/bin/munin-cron(?:[\s;)]|$)', message)]
    except (OSError, ValueError) as error:
        cron = []
        findings.append('cron provenance unavailable: '+str(error))
    try:
        data = rrds(spec, now)
    except (OSError, ValueError) as error:
        data = {'finding': str(error)}
    return {'update_log': meta, 'events': events, 'cron_epochs': cron,
            'cycles': cycles(events, cron, after, now), 'collection_after_epoch': after,
            'rrd': data, 'findings': findings,
            'source_address_attribution_accepted': False,
            'limits_and_delivery_accepted': False}


def listing(path, limit=512):
    """List a fixed directory, without opening the objects named by its entries."""
    p = Path(path)
    if p.is_symlink() or any(parent.is_symlink() for parent in p.parents):
        raise ValueError('indirect inventory directory')
    entries = []
    with os.scandir(p) as stream:
        for entry in stream:
            if len(entries) >= limit:
                raise ValueError('inventory directory entry bound')
            entries.append(entry.name)
    return sorted(entries)


def configured_identities(raw):
    """Export privilege selectors only; omit every environment/command value."""
    result = []
    section = None
    for line in raw.decode(errors='replace').splitlines():
        match = re.fullmatch(r'\s*\[([A-Za-z0-9_*?.-]{1,100})\]\s*', line)
        if match:
            section = match[1]
        elif section:
            match = re.fullmatch(r'\s*(user|group|timeout)\s+([A-Za-z0-9_.-]{1,64})\s*', line)
            if match:
                result.append({'section': section, 'key': match[1], 'value': match[2]})
    return result


def generic_node():
    enabled = []
    directory = Path('/etc/munin/plugins')
    for name in listing(directory):
        if not re.fullmatch(r'[A-Za-z0-9_.-]{1,100}', name):
            raise ValueError('unexpected enabled plugin name')
        path = directory/name
        row = {'name': name, 'symlink': path.is_symlink()}
        target = os.readlink(path) if row['symlink'] else str(path)
        if re.fullmatch(r'/(?:usr/share/munin/plugins|usr/local/munin/lib/plugins)/[A-Za-z0-9_.-]{1,100}', target):
            row['target'] = target
            try:
                _, row['source'] = read(target, 262144)
            except (OSError, ValueError) as error:
                row['finding'] = str(error)
        else:
            row['finding'] = 'unrecognized target omitted; not followed'
        enabled.append(row)
    settings = []
    for name in listing('/etc/munin/plugin-conf.d', 64):
        if not re.fullmatch(r'[A-Za-z0-9_.-]{1,100}', name):
            raise ValueError('unexpected plugin settings name')
        try:
            raw, meta = read(Path('/etc/munin/plugin-conf.d')/name, 65536)
            settings.append({'name': name, 'metadata': meta, 'identities': configured_identities(raw)})
        except (OSError, ValueError) as error:
            settings.append({'name': name, 'finding': str(error)})
    capabilities = {}
    for path in ('/sys/class/net', '/sys/class/block', '/sys/class/thermal', '/sys/class/hwmon'):
        try:
            capabilities[path] = listing(path, 128)
        except (OSError, ValueError) as error:
            capabilities[path] = {'finding': str(error)}
    return {'enabled_plugins': enabled, 'settings': settings, 'environment_values_omitted': True,
            'available_package_plugin_names': listing('/usr/share/munin/plugins'),
            'package_versions': command(['/usr/bin/dpkg-query', '-W',
                '-f=${binary:Package}\t${Version}\t${Architecture}\n', 'munin-node', 'munin-plugins-core']),
            'capability_entry_names': capabilities, 'plugins_executed': False,
            'autoconf_executed': False, 'sensor_device_reads': False}


def generic_master(now):
    result = {}
    for host in ('j2-svpi4mf', 'j2-svntp1'):
        directory = Path('/var/lib/munin')/host
        rows = []
        unparsed = []
        for name in listing(directory):
            match = re.fullmatch(re.escape(host)+r'-([A-Za-z0-9_]+)-([A-Za-z0-9_]+)-([acdg])\.rrd', name)
            if not match:
                if name.endswith('.rrd'):
                    unparsed.append(name)
                continue
            meta = (directory/name).lstat()
            if not stat.S_ISREG(meta.st_mode):
                raise ValueError('reference RRD is not a direct regular file')
            rows.append({'filename': name, 'graph': match[1], 'field': match[2],
                         'type': match[3], 'mtime': meta.st_mtime, 'age_seconds': now-meta.st_mtime})
        result[host] = {'series': rows, 'graphs': sorted({row['graph'] for row in rows}),
                        'unparsed_rrd_names': unparsed, 'complete_filename_parsing': not unparsed}
    return {'reference_host': 'j2-svpi4mf', 'target_host': 'j2-svntp1', 'native_rrd_inventory': result,
            'reference_node_contacted': False, 'historical_rrds_are_not_enabled_plugin_proof': True,
            'generic_classification_requires_review': True}


def transport_metadata(spec):
    path = Path('/usr/local/munin/lib/plugins/ntp_transport_j2')
    _, meta = read(path, 262144)
    link = Path('/etc/munin/plugins/ntp_transport_j2')
    if any(p.is_symlink() for p in link.parents):
        raise ValueError('indirect transport link directory')
    info = link.lstat()
    if not stat.S_ISLNK(info.st_mode):
        raise ValueError('transport selection must be a symlink')
    expected = spec['transport_expected']
    return {'path': str(path), 'metadata': meta,
            'expected': expected,
            'matches': {key: meta[key] == value for key, value in expected.items()},
            'selection': {'target': os.readlink(link), 'uid': info.st_uid,
                          'gid': info.st_gid, 'inode': info.st_ino, 'device': info.st_dev}}


def contact_metadata(spec):
    paths = {'main': Path('/etc/munin/munin.conf'),
             'predecessor_proof': Path('/var/lib/munin-ntp-master/munin-master-commissioning-20261021-v1/config-proof')}
    result = {}
    for label, path in paths.items():
        try:
            _, meta = read(path, 262144)
        except FileNotFoundError:
            result[label] = {'path': str(path), 'missing': True}
            continue
        row = {'path': str(path), 'metadata': meta,
               'matches': {k: meta[k] == v for k, v in spec['contact_expected'].items()}}
        result[label] = row
    a = result['main'].get('metadata', {})
    b = result['predecessor_proof'].get('metadata', {})
    result['same_inode_as_predecessor_proof'] = bool(a and b and (a['device'], a['inode']) == (b['device'], b['inode']))
    presence = {}
    for path in ('/usr/local/libexec/munin-ntp-mailrise.py', '/usr/local/libexec/munin-ntp-contact-gate.py',
                 '/var/lib/munin-ntp-contact-control', '/var/lib/munin/ntp-alerts',
                 '/usr/local/libexec', '/var/lib/munin'):
        p = Path(path)
        if any(parent.is_symlink() for parent in p.parents):
            raise ValueError('indirect contact metadata ancestor')
        try:
            m = p.lstat()
        except FileNotFoundError:
            presence[path] = {'missing': True}
            continue
        presence[path] = {'uid': m.st_uid, 'gid': m.st_gid, 'mode': stat.S_IMODE(m.st_mode),
                          'nlink': m.st_nlink, 'inode': m.st_ino, 'device': m.st_dev,
                          'is_directory': stat.S_ISDIR(m.st_mode), 'is_symlink': stat.S_ISLNK(m.st_mode)}
    result['presence'] = presence
    return result


def contact_status():
    identity = pwd.getpwnam('munin')
    try:
        raw, meta = read('/var/lib/munin/ntp-alerts/status.json', 4096)
        data = json.loads(raw)
        if (meta['uid'] != identity.pw_uid or meta['gid'] != identity.pw_gid
                or meta['mode'] != 0o600 or meta['nlink'] != 1
                or set(data) != {'schema', 'submission_ok', 'attempt_epoch'}
                or data['schema'] != 1 or type(data['submission_ok']) is not bool
                or type(data['attempt_epoch']) not in (int, float) or not math.isfinite(data['attempt_epoch'])):
            raise ValueError('invalid private submission-status contract')
        return {'metadata': meta, 'value': data,
                'sender_attribution_available': False, 'downstream_delivery_proven': False}
    except (OSError, ValueError, TypeError) as error:
        return {'finding': str(error)}


def contact_observation(spec, now):
    def selected_json(path, keys):
        try:
            raw, meta = read(path, 65536)
            data = json.loads(raw)
            return {'metadata': meta, 'value': {k: data.get(k) for k in keys}}
        except (OSError, ValueError, TypeError) as error:
            return {'finding': str(error)}

    def native_state(path, mode):
        try:
            raw, meta = read(path, 1048576)
            identity = pwd.getpwnam('munin')
            if (meta['uid'] != identity.pw_uid or meta['mode'] & 0o022 or meta['nlink'] != 1):
                raise ValueError('unsafe native state metadata')
            # Decode the bounded snapshot in memory as munin; never call limits,
            # update, a plugin, or any contact command. Export only selected data.
            code = r'''
use strict; use warnings; use Storable qw(fd_retrieve); use JSON::PP;
use Munin::Master::Utils;
binmode STDIN; my $d=fd_retrieve(\*STDIN); my %out;
if ($ARGV[0] eq 'limits') {
 my $n=munin_get_node($d,['J1-SVMF','J1-SVMF','ntp_transport_j2','mail']);
 if (ref($n) eq 'HASH') { for my $k (qw(state)) {
  $out{$k}=$n->{$k} if exists($n->{$k}) && !ref($n->{$k});
 }}
} else {
 my $v=$d->{value}; die 'native value map missing' unless ref($v) eq 'HASH';
 for my $k (keys %$v) {
  next unless $k =~ m{\A(?:/var/lib/munin/J1-SVMF/)?J1-SVMF-ntp_transport_j2-mail-g\.rrd:\d+\z};
  my $c=$v->{$k}{current}; next unless ref($c) eq 'ARRAY' && @$c==2 && !grep {ref($_)} @$c;
  $out{$k}=$c; die 'selected native sample bound' if keys(%out)>4;
 }
}
print encode_json(\%out);
'''
            row = h.bounded(['/usr/sbin/runuser', '-u', 'munin', '--', '/usr/bin/perl', '-e', code, mode],
                            timeout=20, limit=16384, payload=raw)
            if row.get('returncode') != 0 or row.get('error'):
                raise ValueError('bounded native snapshot decoder failed')
            return {'metadata': meta, 'selected': json.loads(row['stdout'])}
        except (OSError, ValueError, TypeError) as error:
            return {'finding': str(error)}

    result = {'status_before': contact_status(),
              'committed_state': selected_json(spec['contact_state_path'],
                  ('phase', 'accepted', 'enable_pending', 'enabled_epoch', 'spec_sha256')),
              'suppression': selected_json('/var/lib/munin/ntp-alerts/suppressed.json',
                  ('schema', 'suppressed_epoch', 'reason'))}
    if [n for n in listing('/etc/munin/munin-conf.d') if not n.startswith('.') and not n.endswith('~')]:
        raise ValueError('unexpected effective include')
    result['collection'] = master(spec, now)
    result['limits_state'] = native_state('/var/lib/munin/limits.storable', 'limits')
    result['sample_state'] = native_state('/var/lib/munin/state-J1-SVMF-J1-SVMF.storable', 'sample')
    try:
        raw, meta = read('/var/log/munin/munin-limits.log', 262144, tail=True)
        events = []
        for line in raw.decode('utf-8', errors='replace').splitlines():
            categories = [name for name, pattern in (
                ('smtp_450', r'\b450\b'), ('send_failure', r'failed to send notification'),
                ('transport', r'ntp_transport_j2'), ('mail', r'\bmail\b'),
                ('error', r'\b(?:error|fatal|critical)\b')) if re.search(pattern, line, re.I)]
            if categories:
                events.append({'timestamp_prefix': line[:32] if re.match(r'^\d{4}[-/]', line) else None,
                               'categories': categories, 'line_sha256': hashlib.sha256(line.encode()).hexdigest()})
        result['limits_log'] = {'metadata': meta, 'classified_events': events[-200:],
                                'raw_log_or_message_content_exported': False}
    except (OSError, ValueError) as error:
        result['limits_log'] = {'finding': str(error)}
    result['status_after'] = contact_status()
    result['status_changed_during_capture'] = result['status_before'] != result['status_after']
    result['effective_includes_empty'] = not [n for n in listing('/etc/munin/munin-conf.d')
                                             if not n.startswith('.') and not n.endswith('~')]
    if not result['effective_includes_empty']:
        raise ValueError('effective include appeared during capture')
    result['mailrise_backend_cause_accepted'] = False
    return result


def canonical_sockets(raw):
    """Select established canonical-endpoint sockets; ownership distinguishes probes."""
    rows = []
    for line in raw.decode('ascii').splitlines()[1:]:
        fields = line.split()
        if len(fields) < 10:
            raise ValueError('incomplete proc TCP row')
        if fields[2] != '3300010A:1355' or fields[3] != '01':
            continue
        address, port = fields[1].split(':')
        address = socket.inet_ntoa(bytes.fromhex(address)[::-1])
        rows.append({'source': address, 'source_port': int(port, 16),
                     'destination': '10.1.0.51', 'destination_port': 4949,
                     'uid': int(fields[7]), 'inode': int(fields[9])})
    return rows


def process_identity(pid):
    """Export fixed command classifications, never arbitrary process arguments."""
    base = Path('/proc')/str(pid)
    before = (base/'stat').read_text()
    fields = before[before.rindex(')')+2:].split()
    raw, _ = read(base/'cmdline', 4096)
    tokens = raw.replace(b'\x00', b' ').decode(errors='replace').split()
    tags = [name for name in ('munin-update', 'munin-cron', 'ntp_transport_j2')
            if any(re.fullmatch(r'(?:[^\s]*/)?'+name, token) for token in tokens)]
    if (base/'stat').read_text().split(') ', 1)[1].split()[19] != fields[19]:
        raise ValueError('process identity changed')
    return {'pid': int(pid), 'ppid': int(fields[1]), 'start_ticks': int(fields[19]),
            'uid': base.stat().st_uid, 'command_tags': tags}


def socket_owners(inodes, uid):
    owners = []
    entries = list(Path('/proc').iterdir())
    if len(entries) > 8192:
        raise ValueError('process directory bound')
    for base in entries:
        if not base.name.isdecimal():
            continue
        try:
            if base.stat().st_uid != uid:
                continue
            descriptors = list((base/'fd').iterdir())
            if len(descriptors) > 256:
                raise ValueError('process descriptor bound')
            matched = set()
            for descriptor in descriptors:
                try:
                    target = os.readlink(descriptor)
                except FileNotFoundError:
                    continue
                if target in inodes:
                    matched.add(target)
            if not matched:
                continue
            identity = process_identity(base.name)
            ancestors, parent = [], identity['ppid']
            for _ in range(6):
                if parent <= 1:
                    break
                ancestor = process_identity(parent)
                ancestors.append(ancestor)
                parent = ancestor['ppid']
            if process_identity(base.name) != identity:
                continue
            owners.append({'identity': identity, 'ancestors': ancestors,
                           'sockets': sorted(matched)})
        except (FileNotFoundError, ProcessLookupError):
            continue  # A naturally exiting worker is a sampling miss.
    return owners


def source_attribution(spec):
    uid = pwd.getpwnam('munin').pw_uid
    tcp_path = '/proc/'+str(os.getpid())+'/net/tcp'
    started, deadline = time.time(), time.monotonic()+360
    observations, seen, scans = [], set(), 0
    while time.monotonic() < deadline and scans < 360:
        scans += 1
        raw, _ = read(tcp_path, 524288)
        sockets = [row for row in canonical_sockets(raw) if row['uid'] == uid]
        if sockets:
            owners = socket_owners({'socket:['+str(row['inode'])+']' for row in sockets}, uid)
            # Re-read the socket table after PID/FD inspection to reject vanished/reused sockets.
            current, _ = read(tcp_path, 524288)
            stable = canonical_sockets(current)
            for row in sockets:
                selected = [owner for owner in owners
                            if 'socket:['+str(row['inode'])+']' in owner['sockets']]
                key = (row['inode'], tuple((o['identity']['pid'], o['identity']['start_ticks']) for o in selected))
                if row in stable and key not in seen:
                    seen.add(key)
                    observations.append({'epoch': time.time(), 'socket': row, 'owners': selected,
                                         'expected_source': row['source'] == '10.1.3.83'})
                    if len(observations) > 128:
                        raise ValueError('socket evidence bound')
        time.sleep(min(1, max(0, deadline-time.monotonic())))
    raw, meta = read('/var/log/munin/munin-update.log', 1048576, tail=True)
    events = [event for event in log_events(raw) if started-60 <= event['epoch'] <= time.time()]
    cron = [epoch for epoch, message in journal('cron.service', started-60)
            if re.search(r'\(munin\) CMD \([^\n]*?/usr/bin/munin-cron(?:[\s;)]|$)', message)]
    return {'started_epoch': started, 'finished_epoch': time.time(), 'scans': scans,
            'connections': observations, 'events': events, 'cron_epochs': cron, 'update_log': meta,
            'source_address_attribution_accepted': False, 'evidence_review_required': True,
            'finding': 'Correlate socket owners and ancestry with native scheduled events; sampling misses remain inconclusive.'}


def collect(spec, context=None):
    wall_start, monotonic_start = time.time(), time.monotonic()
    result = {'operation_id': spec['operation_id'], 'spec_sha256': h.sha(h.encoded(spec)),
              'capture_complete': False, 'kind': spec['kind'], 'captured_epoch': time.time(),
              'timezone': time.strftime('%z %Z'), 'target_mutation': False}
    try:
        result['before'] = continuity(spec)
        if spec.get('purpose') == 'source-attribution':
            result['observations'] = source_attribution(spec)
        elif spec.get('purpose') == 'transport-metadata':
            result['observations'] = transport_metadata(spec)
        elif spec.get('purpose') == 'contact-metadata':
            result['observations'] = contact_metadata(spec)
        elif spec.get('purpose') == 'contact-observation':
            result['observations'] = contact_observation(spec, time.time())
        elif spec.get('purpose') == 'generic-profile':
            result['observations'] = generic_node() if spec['kind'] == 'node' else generic_master(time.time())
        elif spec.get('purpose') == 'maintenance-observation':
            def effective_includes():
                return [name for name in listing('/etc/munin/munin-conf.d')
                        if not name.startswith('.') and not name.endswith('~')]
            if effective_includes():
                raise ValueError('unexpected native include; contacts-disabled scope not established')
            result['observations'] = master(spec, time.time())
            if effective_includes():
                raise ValueError('native include appeared during capture')
            result['observations']['effective_includes_empty'] = True
        elif spec.get('purpose') == 'timing-observation':
            if (not context or context.get('node_archive_sha256') != spec['correction_prerequisite']['archive_sha256']
                    or type(context.get('commit_finished_epoch')) not in (int, float)
                    or not spec['correction_prerequisite'].get('prepared_epoch', 0) < context['commit_finished_epoch'] <= time.time()):
                raise ValueError('committed correction context required')
            effective = [n for n in listing('/etc/munin/munin-conf.d')
                         if not n.startswith('.') and not n.endswith('~')]
            if effective:
                raise ValueError('unexpected effective include')
            result['runtime_context_sha256'] = h.sha(h.encoded(context))
            result['observations'] = master(dict(spec, collection_after_epoch=context['commit_finished_epoch']), time.time())
            if [n for n in listing('/etc/munin/munin-conf.d') if not n.startswith('.') and not n.endswith('~')]:
                raise ValueError('effective includes changed')
            result['observations']['effective_includes_empty'] = True
        else:
            result['observations'] = node(spec, time.time()) if spec['kind'] == 'node' else master(spec, time.time())
        result['after'] = continuity(spec)
        if spec.get('purpose') == 'transport-metadata' and result['observations'] != transport_metadata(spec):
            raise ValueError('transport metadata changed during observation')
        if spec.get('purpose') == 'contact-metadata' and result['observations'] != contact_metadata(spec):
            raise ValueError('contact metadata changed during observation')
        if result['before'] != result['after']:
            raise ValueError('service identity changed during observation')
        result['clock_delta_seconds'] = (time.time()-wall_start)-(time.monotonic()-monotonic_start)
        if abs(result['clock_delta_seconds']) > 2:
            raise ValueError('wall clock stepped during observation')
        result['capture_complete'] = True
    except Exception as error:
        result['error'] = str(error)
    return result
