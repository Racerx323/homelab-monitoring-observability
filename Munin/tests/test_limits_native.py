#!/usr/bin/python3
"""Native package limits/contact qualification, only inside a networkless container.

Synthetic measurements exercise the installed engine; no evaluator is replaced.
The only contact command records stdin locally and has no delivery capability.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import pwd
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
SEED = r'''
use strict; use warnings; use JSON::PP; use Munin::Master::Utils;
my $d=decode_json(do {local $/; <STDIN>});
my $root=$d->{root}; my $host=$d->{host};
my $cfg=munin_readconfig_base("$root/munin.conf");
munin_writeconfig_storable("$root/db/datafile.storable",$cfg);
my %state;
for my $row (@{$d->{fields}}) {
    my $field=munin_get_node($cfg,[$host,$host,$row->{graph},$row->{field}]);
    die 'missing native field' unless ref($field) eq 'HASH';
    my $filename=munin_get_rrd_filename($field);
    $state{value}{"$filename:42"}{current}=[$row->{epoch},$row->{value}];
}
munin_writeconfig_storable("$root/db/state-$host-$host.storable",\%state);
'''
NOTES = r'''
use strict; use warnings; use JSON::PP; use Munin::Master::Utils;
my $notes=munin_read_storable($ARGV[0]); my %out; my $host=$ARGV[1]; my $field=$ARGV[2];
for my $graph (@ARGV[3..$#ARGV]) {
 my $node=munin_get_node($notes,[$host,$host,$graph,$field]);
 $out{$graph}=$node->{state};
}
print encode_json(\%out);
'''
SINK = '''import pathlib,sys,time
p=pathlib.Path(sys.argv[1])/(str(time.time_ns())+'.txt')
p.write_bytes(sys.stdin.buffer.read(16385))
'''


def run(argv, data=None):
    row = subprocess.run(argv, input=data, capture_output=True, timeout=20)
    if row.returncode:
        raise RuntimeError(repr(argv)+'\n'+row.stderr.decode(errors='replace'))
    return row.stdout


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    if not Path('/run/.containerenv').is_file():
        raise RuntimeError('container-only native qualification')
    expected = json.load(sys.stdin)
    actual = {path: hashlib.sha256(Path(path).read_bytes()).hexdigest() for path in expected}
    if actual != expected:
        raise RuntimeError('native package source differs from accepted master capture')
    identity = pwd.getpwnam('munin')
    os.setgroups([])
    os.setgid(identity.pw_gid)
    os.setuid(identity.pw_uid)
    os.umask(0o077)
    root = Path(tempfile.mkdtemp(prefix='limits-native-', dir='/tmp'))
    for name in ('db', 'log', 'run', 'contacts'):
        (root/name).mkdir(mode=0o700)
    sink = root/'capture.py'
    sink.write_text(SINK)
    contact = load(ROOT/'scripts/ntp_mailrise.py')
    metrics = load(ROOT/'node/plugins/ntp/ntp_metrics.py')
    traces = []

    def step(label, value, critical='0:172800', warning=None, contacts='capture',
             expected_state=None, notifications=0, graphs=('ntp_job_age',), stale=False,
             field='reading', host='j2-svntp1', candidate_scope=False, reset=False):
        if reset:
            for name in ('limits', 'limits.storable'):
                (root/'db'/name).unlink(missing_ok=True)
        lines = [f'dbdir {root}/db', f'logdir {root}/log', f'rundir {root}/run',
                 f'contact.capture.command /usr/bin/python3 -I -B {sink} {root}/contacts',
                 'contact.capture.text ${var:worst}|${var:host}|${var:plugin}|${var:wfields}|${var:cfields}|${var:ufields}',
                 'contact.capture.max_messages 1', '['+host+']',
                 ' address 10.1.0.51', ' unknown_limit 0', ' contacts '+contacts]
        if candidate_scope:
            candidate=(ROOT/'master/configs/j2-svntp1.conf.example').read_text()
            command='/usr/bin/python3 -I -B /usr/local/libexec/munin-ntp-contact-gate.py'
            if candidate.count(command) != 1:
                raise ValueError('one fixed candidate contact command required')
            candidate=candidate.replace(command,f'/usr/bin/python3 -I -B {sink} {root}/contacts')
            lines=lines[:3]+[candidate.replace('ntp_mailrise','capture')]
        for graph in graphs:
            prefix=f'.{host};{host}:{graph}'
            lines += [f'{prefix}.graph_title Native qualification',
                      f'{prefix}.{field}.label Reading', f'{prefix}.{field}.type GAUGE',
                      f'{prefix}.{field}.critical {critical}']
            if warning:
                lines += [f'{prefix}.{field}.warning {warning}']
        (root/'munin.conf').write_text('\n'.join(lines)+'\n')
        fields = [{'graph': graph, 'field': field, 'value': value,
                   'epoch': int(time.time())-(601 if stale else 0)} for graph in graphs]
        before = set((root/'contacts').iterdir())
        run(['/usr/bin/perl', '-e', SEED], json.dumps({'root': str(root), 'host': host, 'fields': fields}).encode())
        run(['/usr/share/munin/munin-limits', '--config', str(root/'munin.conf')])
        states = json.loads(run(['/usr/bin/perl', '-e', NOTES, str(root/'db/limits.storable'), host, field, *graphs]))
        if states != dict.fromkeys(graphs, expected_state):
            raise AssertionError((label, states, expected_state))
        deadline = time.monotonic()+2
        while time.monotonic() < deadline:
            paths = set((root/'contacts').iterdir())-before
            if len(paths) >= notifications and all(p.stat().st_size for p in paths):
                break
            time.sleep(.02)
        messages = [path.read_bytes() for path in sorted(set((root/'contacts').iterdir())-before)]
        if len(messages) != notifications:
            raise AssertionError((label, len(messages), notifications))
        for raw in messages:
            contact.message(raw)  # Parse actual native expansion, without deliver/save_status.
        traces.append({'case': label, 'states': states,
                       'messages': [m.decode().strip() for m in messages]})

    step('healthy', 100, expected_state='ok')
    step('warning', 120000, warning='0:100000', expected_state='warning', notifications=1)
    step('warning-repeat', 120000, warning='0:100000', expected_state='warning')
    step('critical', 172801, expected_state='critical', notifications=1)
    step('unknown-immediate', 'U', expected_state='unknown', notifications=1)
    step('unknown-repeat', 'U', expected_state='unknown')
    step('recovery', 100, expected_state='ok', notifications=1)
    step('healthy-repeat', 100, expected_state='ok')
    step('stale-sample', 100, stale=True, expected_state='unknown', notifications=1)
    step('contacts-none', 172801, contacts='none', expected_state='critical')
    # Two simultaneous graph messages must reach two separate EOF-delimited processes.
    step('separate-pipes', 0, critical='1:1', graphs=('ntp_job_evidence', 'ntp_stats_read'),
         expected_state='critical', notifications=2)
    # These demonstrate native behavior that conflicts with the desired seconds policy.
    step('jitter-4ms-rounds-to-zero', .004, critical='0:0.001',
         graphs=('ntp_timing',), contacts='none', expected_state='ok')
    step('offset-5ms-boundary-rounds-up', .005, critical='-0.005:0.005',
         graphs=('ntp_timing',), contacts='none', expected_state='critical')
    step('signed-offset-minus-5ms-boundary', -.005, critical='-0.005:0.005',
         graphs=('ntp_timing',), contacts='none', expected_state='critical')
    for offset, jitter, flag, healthy in (
            ('5','0','selected_offset_ok',True),('-5','0','selected_offset_ok',True),
            ('5.000001','0','selected_offset_ok',False),('-5.000001','0','selected_offset_ok',False),
            ('0','0','selected_jitter_ok',True),('0','1','selected_jitter_ok',True),
            ('0','1.000001','selected_jitter_ok',False),('0','4','selected_jitter_ok',False)):
        raw=(f'leap=00, stratum=1, offset=0, sys_jitter=0\n'
             f'o127.127.22.0 .PPS. 0 l 4 16 377 0.000 {offset} {jitter}\n')
        value=metrics.parse_ntpq(raw)[flag]
        assert value==int(healthy)
        step(f'corrected-{flag}-{offset}-{jitter}',value,critical='1:1',field=flag,
             graphs=('ntp_health',),expected_state='ok' if healthy else 'critical',
             notifications=0 if healthy else 1,reset=True)
    for flag in metrics.TIMING_HEALTH_FIELDS:
        step('corrected-unknown-'+flag,'U',critical='1:1',field=flag,graphs=('ntp_health',),
             expected_state='unknown',notifications=1,reset=True)
    step('candidate-exact-node-contact-scope',0,critical='1:1',candidate_scope=True,
         graphs=tuple(sorted(contact.GRAPHS))+('df',),expected_state='critical',
         notifications=len(contact.GRAPHS),reset=True)
    step('candidate-master-transport-contact',0,critical='1:1',candidate_scope=True,
         host='J1-SVMF',graphs=('ntp_transport_j2',),field='v4',expected_state='critical',
         notifications=1,reset=True)
    step('candidate-unselected-master-graph',0,critical='1:1',candidate_scope=True,
         host='J1-SVMF',graphs=('load',),expected_state='critical',reset=True)
    step('candidate-unrelated-host',0,critical='1:1',candidate_scope=True,
         host='unrelated-host',graphs=('df',),expected_state='critical',reset=True)
    generic_rejected = False
    try:
        contact.message(b'CRITICAL|j2-svntp1|df||root|')
    except ValueError:
        generic_rejected = True
    assert generic_rejected
    print(json.dumps({'native_hashes': actual, 'uid': os.getuid(), 'cases': traces,
                      'native_semantics_qualified': True, 'corrected_candidate_qualified': True,
                      'production_alert_ready': False,
                      'production_contact_enabled': False, 'network_or_delivery_attempted': False,
                      'remaining_gates': ['guarded node/master deployment and fresh-field acceptance',
                                          'separate contact activation and exact-message delivery approval']}))


if __name__ == '__main__':
    main()
