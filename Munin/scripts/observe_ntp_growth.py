#!/usr/bin/python3
"""Read-only t0 records for the agreed four-stream growth contract."""
import json
import math
import os
from pathlib import Path
import pwd
import re
import time

observer = None
statistics = None
h = None
STREAMS = ('loopstats', 'peerstats', 'clockstats', 'protostats')
GRAPHS = ('ntp_free_bytes', 'ntp_free_inodes', 'ntp_storage_read', 'ntp_stats_bytes',
          'ntp_stats_growth', 'ntp_stats_age', 'ntp_stats_read', 'ntp_job_evidence', 'ntp_job_age')


def snapshot(directory=Path('/var/log/ntpstats')):
    started = time.time()
    if any(p.is_symlink() for p in (directory, *directory.parents)):
        raise ValueError('indirect statistics ancestry')
    result = statistics.inventory(directory)
    for row in result['files']:
        m = (directory/row['name']).lstat()
        if (m.st_dev, m.st_ino, m.st_size, m.st_mtime) != (
                row['device'], row['inode'], row['bytes'], row['mtime']):
            raise ValueError('statistics identity changed during snapshot')
        row.update(allocated_bytes=m.st_blocks*512, mtime_ns=m.st_mtime_ns, ctime_ns=m.st_ctime_ns)
    fs = os.statvfs(directory)
    result.update(started_epoch=started, finished_epoch=time.time(), monotonic=time.monotonic(),
                  directory_device=directory.stat().st_dev, directory_inode=directory.stat().st_ino,
                  total_inodes=fs.f_files, free_bytes=fs.f_bfree*fs.f_frsize,
                  filesystem_block_bytes=fs.f_frsize, free_inodes=fs.f_ffree)
    active, findings = {}, []
    for stream in STREAMS:
        rows = [r for r in result['files'] if r['name'] == stream]
        if len(rows) != 1 or not rows[0]['regular'] or rows[0]['symlink']:
            findings.append('missing/indirect active stream: '+stream)
        else:
            active[stream] = {'device': rows[0]['device'], 'inode': rows[0]['inode']}
    recognized = [r for r in result['files'] if r['recognized'] and r['regular']]
    unique = {(r['device'], r['inode']): r for r in recognized}
    result.update(active=active, findings=findings,
                  unique_statistics_bytes=sum(r['bytes'] for r in unique.values()),
                  unique_statistics_allocated_bytes=sum(r['allocated_bytes'] for r in unique.values()),
                  unique_statistics_inodes=len(unique),
                  unexpected_names=[r['name'] for r in result['files'] if not r['recognized']],
                  thresholds={'minimum_free_bytes': 10737418240, 'minimum_free_inode_percent': 5,
                              'bytes_pass': result['available_bytes'] >= 10737418240,
                              'inodes_pass': bool(fs.f_files and 100*fs.f_favail/fs.f_files >= 5)})
    return result


def mount_record(directory=Path('/var/log/ntpstats')):
    raw, _ = observer.read('/proc/'+str(os.getpid())+'/mountinfo', 1048576)
    lines = raw.decode().splitlines()
    if len(lines) > 4096:
        raise ValueError('mount inventory bound')
    candidates = []
    for line in lines:
        left, right = line.split(' - ', 1)
        fields, extra = left.split(), right.split()
        mountpoint = Path(re.sub(r'\\([0-7]{3})', lambda m: chr(int(m[1], 8)), fields[4]))
        if directory == mountpoint or mountpoint in directory.parents:
            candidates.append({'mountpoint': str(mountpoint), 'device_major_minor': fields[2],
                               'filesystem_type': extra[0], 'source': extra[1], 'options': fields[5]})
    if not candidates:
        raise ValueError('statistics mount not identified')
    return max(candidates, key=lambda row: len(row['mountpoint']))


def cached_limits(path, mode):
    try:
        raw, meta = observer.read(path, 4194304)
        identity = pwd.getpwnam('munin')
        if meta['uid'] != identity.pw_uid or meta['mode'] & 0o022 or meta['nlink'] != 1:
            raise ValueError('unsafe native snapshot')
        code = r'''
use strict; use warnings; use Storable qw(fd_retrieve); use JSON::PP;
use Munin::Master::Utils;
binmode STDIN; my $d=fd_retrieve(\*STDIN); my %out;
for my $graph (@ARGV[1..$#ARGV]) {
 my $n=munin_get_node($d,['j2-svntp1','j2-svntp1',$graph]);
 next unless ref($n) eq 'HASH'; my %selected;
 for my $k (keys %$n) {
  my $v=$n->{$k};
  if ($ARGV[0] eq 'config' && $k eq 'contacts' && !ref($v)) { $selected{$k}=$v; }
  next unless ref($v) eq 'HASH'; my %field;
  for my $f ($ARGV[0] eq 'config' ? qw(label type warning critical unknown_limit) : qw(state)) {
   $field{$f}=$v->{$f} if exists($v->{$f}) && !ref($v->{$f});
  }
  $selected{$k}=\%field if keys %field;
 }
 $out{$graph}=\%selected;
}
print encode_json(\%out);
'''
        row = h.bounded(['/usr/sbin/runuser', '-u', 'munin', '--', '/usr/bin/perl', '-e', code, mode, *GRAPHS],
                        timeout=20, limit=65536, payload=raw)
        if row.get('returncode') != 0 or row.get('error'):
            raise ValueError('selected native snapshot decoder failed')
        return {'metadata': meta, 'selected': json.loads(row['stdout'])}
    except (OSError, ValueError, TypeError) as error:
        return {'finding': str(error)}


def collect(spec, context=None):
    wall, monotonic = time.time(), time.monotonic()
    result = {'operation_id': spec['operation_id'], 'spec_sha256': h.sha(h.encoded(spec)),
              'capture_complete': False, 'kind': spec['kind'], 'captured_epoch': wall,
              'target_mutation': False, 'checkpoint': spec.get('checkpoint_scope', {}).get('label', 't0'), 'sustained_growth_accepted': False}
    try:
        checkpoint = spec.get('checkpoint_scope')
        if checkpoint:
            if time.time() < checkpoint['not_before_epoch']:
                raise ValueError('+6h checkpoint is not due on target')
            result.update(node_t0_epoch=checkpoint['node_t0_epoch'],
                          actual_elapsed_seconds=wall-checkpoint['node_t0_epoch'],
                          lateness_seconds=wall-checkpoint['not_before_epoch'])
        result['before'] = observer.continuity(spec)
        if spec['kind'] == 'node':
            first = snapshot()
            inodes = {(r['device'], r['inode']) for r in first['files'] if r['regular']}
            writers_before = statistics.writer_snapshot(inodes=inodes)
            jobs = observer.node(dict(spec, purpose='expanded-observation'), time.time())
            writers_after = statistics.writer_snapshot(inodes=inodes)
            last = snapshot()
            result['observations'] = {'statistics_before': first, 'statistics_after': last,
                'mount': mount_record(), 'writers_before': writers_before, 'writers_after': writers_after,
                'maintenance': jobs, 'gross_growth_from_this_capture_accepted': False}
        else:
            if (not context or context.get('node_archive_sha256') != spec['node_t0_prerequisite']['archive_sha256']
                    or type(context.get('node_t0_epoch')) not in (int, float)
                    or not math.isfinite(context['node_t0_epoch']) or not 0 < context['node_t0_epoch'] <= time.time()
                    or checkpoint and context['node_t0_epoch'] != checkpoint['node_t0_epoch']):
                raise ValueError('accepted node t0 context required')
            result['runtime_context_sha256'] = h.sha(h.encoded(context))
            result['observations'] = observer.contact_observation(spec, time.time())
            result['observations']['cached_limits_configuration'] = cached_limits('/var/lib/munin/datafile.storable', 'config')
            result['observations']['storage_statistics_limits'] = cached_limits('/var/lib/munin/limits.storable', 'limits')
            result['observations']['baseline_may_include_pre_t0_samples'] = not bool(checkpoint)
        result['after'] = observer.continuity(spec)
        if result['before'] != result['after']:
            raise ValueError('service identity changed during t0 capture')
        result['clock_delta_seconds'] = (time.time()-wall)-(time.monotonic()-monotonic)
        if abs(result['clock_delta_seconds']) > 2:
            raise ValueError('wall clock stepped during t0 capture')
        result['capture_complete'] = True
    except Exception as error:
        result['error'] = str(error)
    return result
