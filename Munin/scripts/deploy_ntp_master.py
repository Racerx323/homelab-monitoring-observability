#!/usr/bin/python3
"""Seal guarded master commissioning, independent HTTPS commit and timed restoration."""
import argparse
import base64
import fcntl
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import signal
import socket
import ssl
import stat
import subprocess
import tarfile
import time
import types
from datetime import datetime
from zoneinfo import ZoneInfo

FLEET=Path(__file__).resolve().parents[1]
WORKSPACE=FLEET.parent.parent
STAGES=Path('/var/lib/munin-ntp-master-stages')
MAXIMUM=8*1048576
SOURCES={'runner.py':Path(__file__), 'worker.py':FLEET/'scripts/install_ntp_master.py',
    'base.py':FLEET/'scripts/install_ntp_node.py', 'qualifier.py':FLEET/'scripts/qualify_master.py',
    'baseline-sync.py':FLEET/'scripts/sync_master_baseline.py',
    'helper.py':WORKSPACE/'homelab-ntp/ntpsec/scripts/run-production-inspection.py',
    'tls-probe.py':WORKSPACE/'homelab-network/Ubiquiti/munin-master-profile/qualify_dashboard.py',
    'test-master.py':FLEET/'tests/test_master_deployment.py',
    'test-native.py':FLEET/'tests/test_master_native.py',
    'native-runner.py':FLEET/'tests/run_master_native.py',
    'Containerfile':FLEET/'tests/Containerfile.master'}
MEMBERS=set(SOURCES)|{'baseline.conf','candidate.conf','plugin','settings','ca.pem','known_hosts',
    'spec.json','review.md','manifest.json','qualification.json'}


def encoded(value):return (json.dumps(value,sort_keys=True)+'\n').encode()
def sha(raw):return hashlib.sha256(raw).hexdigest()


def private(path,limit=MAXIMUM):
    if any(p.is_symlink() for p in (path,*path.parents)):raise ValueError('indirect private input')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,'rb') as stream:
        m=os.fstat(stream.fileno())
        if (not stat.S_ISREG(m.st_mode) or m.st_uid!=os.geteuid()
                or stat.S_IMODE(m.st_mode)!=0o600 or m.st_size>limit):
            raise ValueError('bounded owner-private input required')
        raw=stream.read(limit+1);after=os.fstat(stream.fileno())
    if len(raw)>limit or (m.st_size,m.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):
        raise ValueError('private input drift/bound')
    return raw


def private_directory(path):
    m=path.lstat()
    if not stat.S_ISDIR(m.st_mode) or m.st_uid!=os.geteuid() or stat.S_IMODE(m.st_mode)!=0o700:
        raise ValueError('owner-private operation directory required')


def module(raw,name):
    namespace={'__name__':name,'__file__':'/sealed/'+name+'.py'}
    exec(compile(raw,namespace['__file__'],'exec'),namespace)
    return types.SimpleNamespace(**namespace)


def unpack(raw,digest,reserve=0):
    if len(raw)>MAXIMUM or sha(raw)!=digest:raise ValueError('approved archive hash/size mismatch')
    with tarfile.open(fileobj=io.BytesIO(raw),mode='r:') as archive:
        entries=archive.getmembers()
        if (len(entries)!=len(MEMBERS) or {m.name for m in entries}!=MEMBERS
                or any(not m.isfile() or m.size>1048576 for m in entries)):
            raise ValueError('closed bounded regular archive required')
        files={m.name:archive.extractfile(m).read() for m in entries}
    if json.loads(files['manifest.json'])!={n:sha(v) for n,v in files.items() if n!='manifest.json'}:
        raise ValueError('closed member manifest mismatch')
    spec=json.loads(files['spec.json']);pins=spec['worker']
    if (not re.fullmatch(r'munin-master-[a-z0-9-]{1,48}',spec['operation_id'])
            or pins['operation_id']!=spec['operation_id']
            or not spec['prepared_epoch']<=time.time()<spec['expires_epoch']-reserve
            or not 0<spec['expires_epoch']-spec['prepared_epoch']<=86400
            or files['review.md']!=review(spec).encode()
            or sha(files['baseline.conf'])!=pins['before_sha256']
            or sha(files['candidate.conf'])!=pins['candidate_sha256']
            or sha(files['qualification.json'])!=spec['qualification_sha256']
            or pins['artifacts']!={k:base64.b64encode(files[n]).decode() for k,n in
                (('config','candidate.conf'),('plugin','plugin'),('settings','settings'))}):
        raise ValueError('master scope/expiry/input binding')
    if not pins.get('fixture') and (pins['hostname']!='J1-SVMF' or spec['recovery_seconds']!=600
            or pins['transport_expected']!={'v4':'1','v6':'1','mail':'U'}):
        raise ValueError('fixed production master scope')
    if not pins.get('fixture'):
        qualified=json.loads(files['qualification.json'])
        if not qualified.get('passed') or any(qualified['sources'].get(n)!=sha(files[n]) for n in set(SOURCES)|{'plugin','settings'}):
            raise ValueError('archive lacks current qualified executable inputs')
    return spec,files


def write_archive(output,spec,files):
    files=dict(files);files.update({'spec.json':encoded(spec),'review.md':review(spec).encode()})
    files['manifest.json']=encoded({n:sha(v) for n,v in files.items()})
    output.mkdir(mode=0o700)
    for name,raw in files.items():
        with (output/name).open('xb') as stream:stream.write(raw)
    buffer=io.BytesIO()
    with tarfile.open(fileobj=buffer,mode='w') as archive:
        for name,raw in sorted(files.items()):
            m=tarfile.TarInfo(name);m.mode=0o600;m.size=len(raw);archive.addfile(m,io.BytesIO(raw))
    raw=buffer.getvalue();digest=sha(raw);unpack(raw,digest)
    (output/'deployment.tar').write_bytes(raw)
    (output/'sealing.json').write_bytes(encoded({'sha256':digest,'expires_epoch':spec['expires_epoch'],'target_contact':False}))
    return digest


def review(spec):
    expires=datetime.fromtimestamp(spec['expires_epoch'],ZoneInfo('America/Chicago')).isoformat()
    return f'''# Guarded native master commissioning review

Operation {spec['operation_id']}; expires {expires}. Begin with 900 seconds remaining.
Approve deployment.tar's SHA-256 before execution. SSH pi@10.1.3.83, strict key
alias svmf.local.theama.co; host/boot, native code, complete package inventory,
cron and Apache vhost are pinned. No packages, schedules, NTP-node configuration,
DNS, network, Apache configuration or messages change. Do not replay consumed stages.

## Exact change and preflight

Require the exact accepted production master baseline, no effective include
files, running existing master node/Apache, safe root-owned ancestry and absent
authored destinations. Preserve every unrelated plugin/link and existing node
configuration. Install only ntp_transport_j2 at
/usr/local/munin/lib/plugins/ntp_transport_j2, its exact
/etc/munin/plugin-conf.d/ntp-transport.conf and /etc/munin/plugins link.
The plugin enforces munin:munin, explicit sources .83/::83, both NTP-node literals
and a 25-second internal budget; settings allow 60 seconds. Config/fetch must
show IPv4=1 and IPv6=1. Absent alert-submission evidence stays U, never fabricated.

Atomically replace /etc/munin/munin.conf with the preserving candidate: remove
only the stale cache socket directive, merge transport limits/contacts none into
the existing master section and add one canonical j2-svntp1 IPv4 entry with
contacts none. No contact definitions/helper are activated or messages sent.
Validate with the installed parser as munin. Restart only munin-node. Refresh
only native Munin HTML/graph CGI descendants of the accepted Apache PID: validate
www-data uid, exact script/comm/start identity and ancestry, signal TERM via pidfd,
then prove old workers exited. Never kill by name, SIGKILL or restart Apache.
Require unchanged Apache identity, protected sources, cron/vhost and other plugins.

## Guard, commit and restoration

Retain exclusive root-private staged sources, backups, before/after hashes and
publication inode proofs. Arm an independent systemd recovery timer at 600
seconds before launching the detached worker (300-second runtime cap).
The worker stops at prepared. The controller independently verifies hostname-
checked HTTPS HTML/CSS/existing PNG over .83 and ::83 with the pinned CA/leaf,
both before mutation and after preparation. Missing/bad response fails acceptance.
Only then commit under the same exclusive lock and disarm the guard. Lost
controller/worker cannot commit; guard restores uncommitted authored changes.
The transient guard covers current-boot worker/controller loss; reboot or power
loss requires a fresh scoped inspection and recovery review.

On caught failure or known independent HTTPS failure, restore only matching
authored config backed by the verified baseline, remove only proven authored
source/settings/link, restart the original node when needed and recycle only
native CGI workers. Preserve foreign drift with explicit recovery-held status;
never clobber it. Keep RRD/history, actual records, private evidence, proofs and
created empty source directories. Restore parsed baseline and unrelated plugins;
Apache, cron, DNS and networking stay intact. Manual restoration after committed
state is a separate review. Unknown outcome permits one same-bundle read-only
inspection within expiry; no replay or blind retry.

After successful production commit/readback, synchronize the repository mirror
only if its baseline is unchanged (or already equals the candidate), privately
scan the exact payload and verify bytes. A concurrent repository edit is held,
not overwritten; production remains committed and reconciliation is reported open.

Frozen runner.py execute --directory DIRECTORY --sha256 APPROVED_SHA256 consumes
one receipt before any target contact. Preserve status after each phase. Local
qualification uses actual Bookworm packages/systemd/native CGI; it does not prove
production timing, both-family scheduled collection, new j2 graph freshness or
delivery. Existing-graph checks accept serving continuity only. Genuine scheduled
producer records, three later approved collection cycles, limits/transitions,
exact previewed delivered alerts, OBS-02/OBS-07, persistence, final observation
and later mandatory separate-host ntpviz remain separate gates.
'''


def safe_stage(stage):
    for p in (stage,*stage.parents):
        m=p.lstat()
        if not stat.S_ISDIR(m.st_mode) or m.st_uid!=0 or m.st_mode&0o022:
            raise ValueError('unsafe staged ancestry')


def locked_worker(directory,digest,action):
    if os.geteuid()!=0 or os.getegid()!=0:raise ValueError('root worker required')
    safe_stage(directory)
    raw=private(directory/'deployment.tar');spec,files=unpack(raw,digest)
    for name,data in files.items():
        if private(directory/name,1048576)!=data:
            raise ValueError('staged source drift')
    base=module(files['base.py'],'base');qualifier=module(files['qualifier.py'],'qualifier')
    worker=module(files['worker.py'],'worker');obj=worker.make_worker(base,qualifier)(spec['worker'],sha(encoded(spec['worker'])))
    if (socket.gethostname()!=spec['worker']['hostname'] or
        Path('/proc/sys/kernel/random/boot_id').read_text().strip()!=spec['worker']['boot_id']):
        raise ValueError('staged target identity drift')
    lock=os.open(directory/'lock',os.O_RDWR|os.O_NOFOLLOW)
    try:
        fcntl.flock(lock,fcntl.LOCK_EX)
        if action!='apply':
            if not (obj.root/'state.json').exists():
                return {'phase':'preflight-failed','accepted':False}
            obj.state=json.loads(base.secure(obj.root/'state.json')[0]);obj.owns_root=True
            if obj.state.get('spec_sha256')!=sha(encoded(spec['worker'])):raise ValueError('worker state digest')
        if action=='inspect':
            obj.continuity()
            result={k:obj.state.get(k) for k in ('phase','accepted','recovery','recovery_errors')}
            result['observed_config_sha256']=sha(base.secure(worker.CONFIG)[0])
            return result
        if action=='apply':
            def interrupted(_signal,_frame):raise TimeoutError('master worker deadline/signal')
            signal.signal(signal.SIGALRM,interrupted);signal.signal(signal.SIGTERM,interrupted);signal.alarm(240)
            try:obj.install()
            except BaseException as error:
                if obj.owns_root:
                    obj.state['error']=str(error);obj.recover()
                result={'accepted':False,'phase':obj.state['phase'] if obj.owns_root else 'preflight-failed','error':str(error),
                    'recovery':obj.state.get('recovery'),'recovery_errors':obj.state.get('recovery_errors',[])}
                base.atomic(directory/'result.json',encoded(result));return result
            finally:signal.alarm(0)
        elif action=='commit':
            obj.commit()
            obj.ctl('stop',spec['operation_id']+'-recover.timer')
        elif action=='recover':obj.recover()
        else:raise ValueError('worker action')
        result={k:obj.state.get(k) for k in ('phase','accepted','recovery','recovery_errors')}
        result.update(operation_id=spec['operation_id'],archive_sha256=digest)
        base.atomic(directory/'result.json',encoded(result));return result
    finally:os.close(lock)


def root_launch(raw,digest):
    if os.geteuid()!=0 or os.getegid()!=0:raise ValueError('root launcher required')
    spec,files=unpack(raw,digest,900);stage=STAGES/spec['operation_id']
    pins=spec['worker']
    if pins.get('fixture') and (not Path('/run/.containerenv').exists() or Path('/proc/1/comm').read_text().strip()!='systemd'):
        raise ValueError('fixture requires real isolated systemd')
    if socket.gethostname()!=pins['hostname'] or Path('/proc/sys/kernel/random/boot_id').read_text().strip()!=pins['boot_id']:
        raise ValueError('launch host/boot drift')
    if not STAGES.exists():STAGES.mkdir(mode=0o700)
    safe_stage(STAGES);stage.mkdir(mode=0o700)
    base=module(files['base.py'],'base')
    for name,data in dict(files,**{'deployment.tar':raw,'lock':b''}).items():base.atomic(stage/name,data)
    def run(argv):subprocess.run(argv,check=True,capture_output=True,timeout=30)
    common=['/usr/bin/python3','-I','-B',str(stage/'runner.py'),'root',
        '--directory',str(stage),'--sha256',digest,'--action']
    run(['/usr/bin/systemd-run','--unit',spec['operation_id']+'-recover',
         '--on-active='+str(spec['recovery_seconds'])+'s','--timer-property=AccuracySec=1s',
         '--property=RuntimeMaxSec=180','--property=TimeoutStopSec=20',
         '--collect',*common,'recover'])
    try:
        run(['/usr/bin/systemd-run','--unit',spec['operation_id']+'-worker',
            '--property=Type=exec','--property=RuntimeMaxSec=300','--property=TimeoutStopSec=20',
            '--collect',*common,'apply'])
    except BaseException:
        return locked_worker(stage,digest,'recover')
    deadline=time.monotonic()+330
    while time.monotonic()<deadline:
        result=stage/'result.json'
        if result.exists():return json.loads(base.secure(result)[0])
        time.sleep(1)
    raise TimeoutError('worker result uncertain; timer armed, inspect without replay')


def seal(args):
    os.umask(0o077)
    original=(args.baseline/'inspection.tar').read_bytes()
    result=json.loads((args.baseline/'result.json').read_text())
    capture=json.loads((args.baseline/'stdout.txt').read_text())
    outcome=json.loads((args.baseline/'outcome.json').read_text())
    with tarfile.open(fileobj=io.BytesIO(original),mode='r:') as archive:
        previous=json.loads(archive.extractfile('spec.json').read());known=archive.extractfile('known_hosts').read()
    if (sha(original)!=result.get('bundle_sha256') or result.get('returncode')!=0
            or not result.get('capture_complete') or not capture.get('capture_complete')
            or capture.get('operation_id')!=previous['operation_id']
            or capture.get('spec_sha256')!=sha(encoded(previous)) or previous.get('mode')!='master-baseline'
            or not outcome.get('repository_mirror_accepted')):raise ValueError('accepted exact master baseline required')
    qualifier=module(SOURCES['qualifier.py'].read_bytes(),'qualifier')
    baseline=base64.b64decode(capture['master_qualification']['production_baseline']['base64'],validate=True)
    if (sha(baseline)!=previous.get('production_baseline_sha256')
            or sha(baseline)!=outcome.get('production_config_sha256')
            or outcome.get('archive_sha256')!=sha(original)):
        raise ValueError('accepted baseline byte/hash provenance mismatch')
    if (FLEET/'master/configs/munin.conf').read_bytes()!=baseline:raise ValueError('repository baseline drift')
    candidate=qualifier.commissioning_config(qualifier.without_rrdcached(baseline))
    if sha(candidate)!=capture['master_qualification']['direct_rrd_candidate_sha256']:
        raise ValueError('native-parsed commissioning candidate changed')
    files={n:p.read_bytes() for n,p in SOURCES.items()}
    files['qualification.json']=args.qualification.read_bytes()
    qualification=json.loads(args.qualification.read_text())
    if not qualification.get('passed') or any(qualification['sources'].get(n)!=sha(files[n]) for n in SOURCES):
        raise ValueError('current closed executable inputs require qualification')
    apache_raw=(args.apache_baseline/'deployment.tar').read_bytes()
    apache_outcome=json.loads((args.apache_baseline/'outcome.json').read_text())
    if not apache_outcome.get('accepted') or apache_outcome.get('archive_sha256')!=sha(apache_raw):
        raise ValueError('accepted Apache TLS provenance required')
    with tarfile.open(fileobj=io.BytesIO(apache_raw),mode='r:') as archive:
        ca=archive.extractfile('ca.pem').read();apache_spec=json.loads(archive.extractfile('spec.json').read())
        if known!=archive.extractfile('known_hosts').read():raise ValueError('master SSH key continuity')
    fields=('ActiveState','SubState','MainPID','InvocationID','NRestarts')
    service_blocks=capture['commands']['master_services']['stdout'].strip().split('\n\n')
    services=[dict(line.split('=',1) for line in block.splitlines()) for block in service_blocks]
    apache=next(x for x in services if x.get('FragmentPath','').endswith('/apache2.service'))
    cron=next(x for x in services if x.get('FragmentPath','').endswith('/cron.service'))
    protected={p:row['sha256'] for p,row in capture['native_sources'].items() if 'sha256' in row}
    if any(qualification.get('native_hashes',{}).get(p)!=digest for p,digest in protected.items()):
        raise ValueError('qualified native text/unit sources differ from production capture')
    protected.update({'/etc/cron.d/munin':capture['cron']['record']['sha256'],
        '/etc/apache2/sites-available/001-munin.theama.co-ssl.conf':capture['apache_vhost']['sha256']})
    pins={'operation_id':args.output.name,'hostname':'J1-SVMF','boot_id':previous['boot_id'],
        'continuity_unit':'NetworkManager.service','service_identity':previous['service_identity'],
        'apache_identity':{k:apache[k] for k in fields},'cron_identity':{k:cron[k] for k in fields},'protected_files':protected,
        'package_inventory_sha256':sha(capture['commands']['packages']['stdout'].encode()),
        'before_sha256':sha(baseline),'candidate_sha256':sha(candidate),'fixture':False,
        'transport_expected':{'v4':'1','v6':'1','mail':'U'}}
    files.update({'baseline.conf':baseline,'candidate.conf':candidate,'plugin':(FLEET/'master/plugins/ntp_transport_j2').read_bytes(),
        'settings':(FLEET/'master/configs/ntp-transport.plugin-conf.example').read_bytes(),'ca.pem':ca,'known_hosts':known})
    pins['artifacts']={k:base64.b64encode(files[n]).decode() for k,n in
        (('config','candidate.conf'),('plugin','plugin'),('settings','settings'))}
    # Plugin and settings are also executable/privilege qualification inputs.
    for name in ('plugin','settings'):
        if qualification['sources'].get(name)!=sha(files[name]):raise ValueError('qualified plugin/settings changed')
    now=int(time.time());spec={'operation_id':args.output.name,'prepared_epoch':now,'expires_epoch':now+86400,
        'recovery_seconds':600,'worker':pins,'baseline_archive_sha256':sha(original),
        'qualification_sha256':sha(args.qualification.read_bytes()),
        'repository_target':str(FLEET/'master/configs/munin.conf'),
        'addresses':['10.1.3.83','fd36:5aa8:6971:1::83'],'leaf_sha256':apache_spec['leaf_sha256'],
        'paths':['/','/static/style-new.css','/munin-cgi/munin-cgi-graph/J1-SVMF/J1-SVMF/apache_accesses-day.png']}
    digest=write_archive(args.output,spec,files)
    return {'sha256':digest,'target_contact':False,'expires_epoch':spec['expires_epoch']}


class HealthRejected(ValueError):
    def __init__(self,observations):
        super().__init__('independent HTTPS continuity failed')
        self.observations=observations


def health(spec,files):
    probe=module(files['tls-probe.py'],'probe')
    context=ssl.create_default_context(cadata=files['ca.pem'].decode('ascii'));observations=[]
    for address in spec['addresses']:
        for index,path in enumerate(spec['paths']):
            row,_=probe.request(address,path,context);observations.append(row)
            if (not row.get('tls_verified') or not row.get('response_ok')
                    or row.get('leaf_sha256')!=spec['leaf_sha256']
                    or index==0 and row.get('content_type')!='text/html'
                    or index==1 and row.get('content_type')!='text/css'
                    or index==2 and (row.get('content_type')!='image/png' or not row.get('png_signature'))):
                raise HealthRejected(observations)
    return observations


def payload(files,raw,digest,action,operation):
    program=b"__name__='sealed_master'\n__file__='/sealed/Munin/scripts/runner.py'\n"+files['runner.py']
    expression=(b'root_launch('+repr(raw).encode()+b','+repr(digest).encode()+b')') if action=='apply' else (
        b'locked_worker(Path('+repr(str(STAGES/operation)).encode()+b'),'+repr(digest).encode()+b','+repr(action).encode()+b')')
    return program+b'\nprint(json.dumps('+expression+b'))\n'


def execute(args):
    os.umask(0o077);directory=args.directory.absolute()
    private_directory(directory)
    raw=private(directory/'deployment.tar');spec,files=unpack(raw,args.sha256,900 if args.action=='execute' else 0)
    if spec['worker'].get('fixture'):raise ValueError('controller cannot execute a fixture')
    if files['runner.py']!=Path(__file__).read_bytes():raise ValueError('frozen controller required')
    helper=module(files['helper.py'],'helper')
    for name,data in files.items():
        if helper.private(directory/name)!=data:raise ValueError('local frozen input drift')
    if args.action=='inspect':
        if json.loads(helper.private(directory/'execution.json'))['sha256']!=args.sha256:
            raise ValueError('same consumed approval required')
    receipt=directory/('execution.json' if args.action=='execute' else 'inspection.json')
    with receipt.open('xb') as stream:stream.write(encoded({'sha256':args.sha256,'epoch':time.time()}));stream.flush();os.fsync(stream.fileno())
    argv=helper.ssh_argv({'endpoints':['10.1.3.83'],'host_key_alias':'svmf.local.theama.co'},directory)
    argv[-2]='pi@10.1.3.83'
    def remote(action):
        submitted=payload(files,raw,args.sha256,action,spec['operation_id'])
        row=helper.bounded(argv,timeout=390,limit=8*1048576,payload=submitted,env=os.environ.copy())
        (directory/(action+'-transport.json')).write_bytes(encoded(row))
        if row.get('returncode')!=0 or row.get('error'):raise RuntimeError('uncertain '+action+'; inspect, never replay')
        value=json.loads(row['stdout']);(directory/(action+'-result.json')).write_bytes(encoded(value));return value
    if args.action=='inspect':return remote('inspect')
    result={'archive_sha256':args.sha256,'committed':False,'repository_reconciled':False}
    try:result['https_before']=health(spec,files)
    except HealthRejected as error:
        result.update(accepted=False,phase='preflight-health-failed',https_before=error.observations)
        (directory/'result.json').write_bytes(encoded(result));return result
    applied=remote('apply');result['apply']=applied
    if applied.get('phase')!='prepared':
        result['accepted']=False;(directory/'result.json').write_bytes(encoded(result));return result
    try:result['https_after']=health(spec,files)
    except Exception as error:
        result['acceptance_error']=str(error)
        result['https_after']=getattr(error,'observations',[])
        result['recovery']=remote('recover')
        try:result['https_restored']=health(spec,files)
        except HealthRejected as failure:result.update(https_restored=failure.observations,serving_restoration_accepted=False)
        result['accepted']=False;(directory/'result.json').write_bytes(encoded(result));return result
    committed=remote('commit');result['commit']=committed
    result['committed']=committed.get('phase')=='committed' and committed.get('accepted') is True
    if result['committed']:
        synchronizer=module(files['baseline-sync.py'],'baseline_sync')
        try:
            result['repository_reconciled']=synchronizer.synchronize(files['candidate.conf'],Path(spec['repository_target']),
                write=True,expected_before=files['baseline.conf'])
        except Exception as error:result['repository_reconciliation_error']=str(error)
    result['accepted']=bool(result['committed'] and result['repository_reconciled'])
    result.update(polling_accepted=False,delivery_accepted=False)
    (directory/'result.json').write_bytes(encoded(result));return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='action',required=True)
    q=sub.add_parser('seal')
    for name in ('baseline','apache-baseline','qualification','output'):q.add_argument('--'+name,type=Path,required=True)
    for action in ('check','execute','inspect','root'):
        q=sub.add_parser(action);q.add_argument('--directory',type=Path,required=True);q.add_argument('--sha256',required=True)
        if action=='root':q.add_argument('--action',dest='root_action',choices=('apply','commit','recover','inspect'),required=True)
    args=parser.parse_args()
    if args.action=='seal':result=seal(args)
    elif args.action=='root':result=locked_worker(args.directory,args.sha256,args.root_action)
    elif args.action=='check':
        private_directory(args.directory)
        spec,files=unpack(private(args.directory/'deployment.tar'),args.sha256,900)
        if files['runner.py']!=Path(__file__).read_bytes():raise ValueError('frozen controller required')
        for name,data in files.items():
            if private(args.directory/name,1048576)!=data:raise ValueError('local frozen input drift')
        result={'verified':True,'target_contact':False}
    else:result=execute(args)
    print(json.dumps(result))
    if args.action=='execute' and not result.get('accepted'):raise SystemExit(1)


if __name__=='__main__':main()
