#!/usr/bin/python3
"""Run the actual installer in a fresh isolated systemd container, never a host."""
import importlib.util
import json
import os
import pwd
import grp
from pathlib import Path
import socket
import subprocess
import sys
import time

assert Path('/run/.containerenv').exists(),'container required'
assert Path('/proc/1/comm').read_text().strip()=='systemd','systemd PID 1 required'
SPEC=importlib.util.spec_from_file_location('installer','/source/scripts/install_ntp_node.py')
m=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(m)
CASE=sys.argv[1]
assert CASE in ('success','dpkg-failure','guarded-failure','configured-failure','started-failure','foreign-policy','foreign-guard','foreign-config','resume-recovery','activation-drift','held-recovery')
os.umask(0o077)
ROOT=Path('/var/lib/munin-production-qualification');ROOT.mkdir(mode=0o700)


def run(argv,allowed=(0,)):
    p=subprocess.run(argv,capture_output=True,text=True,timeout=40)
    if p.returncode not in allowed:raise RuntimeError(repr(argv)+'\n'+p.stdout+'\n'+p.stderr)
    return p.stdout


unit=Path('/etc/systemd/system/timeservice-fixture.service')
unit.write_text('[Service]\nExecStart=/bin/sleep infinity\n')
run(['systemctl','daemon-reload']);run(['systemctl','start','timeservice-fixture.service'])
Path('/etc/ntp.conf').write_text('fixture protected configuration\n')
tool=Path('/usr/local/bin/ntpq')
tool.write_text("#!/bin/sh\n/usr/bin/id -u >> /var/lib/ntpq-qualification/uid\ncat <<'EOF'\nleap=00, stratum=1, offset=-0.125, sys_jitter=0.015\no127.127.22.0 .PPS. 0 l 4 16 377 0.000 -0.125 0.015\nEOF\n");tool.chmod(0o755)
stats=Path('/var/log/ntpstats');stats.mkdir(mode=0o750)
for stream in ('loopstats','peerstats','clockstats','protostats'):
    p=stats/stream;p.write_text('private fixture\n');os.link(p,stats/(stream+'.20261020'))
policy=Path('/usr/sbin/policy-rc.d');policy.write_text('#!/bin/sh\ncase "$1" in fixture-unrelated) exit 42;; *) exit 0;; esac\n');policy.chmod(0o755)
old_policy=policy.read_bytes()
manifest=json.loads(Path('/inputs/manifest.json').read_text())
packages=[next(p for p in manifest['packages'] if p['package']==name) for name in ('munin-common','munin-plugins-core','munin-node')]
names=['node/profiles/ntp/profile.json','node/plugin-conf.d/ntp.conf','node/plugins/ntp/ntp_metrics.py']+['node/plugins/ntp/'+p for p in m.CUSTOM_PLUGINS]
spec={'schema':1,'operation_id':'production-'+CASE,'profile':'ntp','fixture':True,
      'hostname':socket.gethostname(),'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
      'architecture':'amd64','source_root':'/source','package_root':'/inputs','packages':packages,
      'policy_before_sha256':m.sha(old_policy),
      'default_settings_sha256':m.sha(Path('/inputs/default-settings').read_bytes()),
      'settings_readme_sha256':m.sha(Path('/inputs/settings-readme').read_bytes()),
      'artifacts':{name:m.sha((Path('/source')/name).read_bytes()) for name in names},
      'listen_addresses':['127.0.0.1','::1'],'allow_addresses':['127.0.0.1','::1'],
      'protected_files':{p:m.sha(Path(p).read_bytes()) for p in ('/etc/ntp.conf','/usr/local/bin/ntpq')}}
inventory=run(['/usr/bin/dpkg-query','-W','-f=${binary:Package}\t${Version}\t${Architecture}\t${db:Status-Abbrev}\n'])
spec['package_inventory_sha256']=m.sha(inventory.encode())
probe=m.Installer(spec,'preparing');spec['service_identity']=probe.identity()
raw=m.encoded(spec);digest=m.sha(raw);(ROOT/'spec.json').write_bytes(raw)


class Fault(m.Installer):
    def checkpoint(self,phase):
        super().checkpoint(phase)
        if phase=='packages-installed':
            proof=Path('/var/lib/ntpq-qualification');proof.mkdir(mode=0o700)
            os.chown(proof,pwd.getpwnam('munin').pw_uid,grp.getgrnam('munin').gr_gid)
        if CASE in ('foreign-policy','held-recovery') and phase=='guarded':
            policy.write_text('#!/bin/sh\nexit 17\n');raise RuntimeError('injected '+CASE)
        if CASE=='foreign-guard' and phase=='guarded':
            m.GUARD.write_text('[Unit]\nConditionPathExists=/foreign\n');raise RuntimeError('injected foreign-guard')
        if CASE=='foreign-config' and phase=='configured':
            m.CONFIG.write_text('foreign configuration\n');raise RuntimeError('injected foreign-config')
        if CASE=='activation-drift' and phase=='configured':m.CONFIG.write_text('foreign configuration\n')
        if CASE==phase+'-failure' or CASE=='configured-failure' and phase=='configured':
            raise RuntimeError('injected '+CASE)
        if CASE=='resume-recovery' and phase=='packages-installed':raise RuntimeError('injected interruption')

    def command(self,argv,allowed=(0,),env=None):
        if CASE=='dpkg-failure' and argv[:4]==['/usr/bin/dpkg','--force-confdef','--force-confold','--install']:
            invalid=ROOT/'invalid.deb';invalid.write_bytes(b'invalid fixture archive')
            argv=argv[:4]+argv[4:5]+[str(invalid)]
        return super().command(argv,allowed,env)


instance=Fault(spec,digest);error=None;passed=False;checks={}
try:
    instance.install()
    assert CASE=='success','fault injection missed'
    checks['actual_installer_started']=True
    for name in (*m.PACKAGE_PLUGINS,*m.CUSTOM_PLUGINS):
        output=run(['/usr/sbin/munin-run',name,'config']);assert 'graph_title ' in output
        output=run(['/usr/sbin/munin-run',name]);assert '.value ' in output
        checks[name]=True
        if name=='ntp_storage':assert 'stats_ok.value 1' in output,output
        if name=='ntp_health':assert 'query_ok.value 1' in output,output
        if name=='ntp_jobs':assert 'retention_evidence.value 0' in output and 'reporting_evidence.value 0' in output
    for address in ('127.0.0.1','::1'):
        with socket.create_connection((address,4949),timeout=3) as connection:
            f=connection.makefile('rb');assert f.readline().startswith(b'# munin node')
            connection.sendall(b'fetch load\n');lines=[]
            for _ in range(100):
                line=f.readline()
                if line==b'.\n':break
                assert line;lines.append(line)
            assert b'load.value ' in b''.join(lines);connection.sendall(b'quit\n')
    checks['dual_stack_protocol']=True
    observed=Path('/var/lib/ntpq-qualification/uid').read_text().splitlines()
    assert observed and set(observed)=={str(pwd.getpwnam('munin').pw_uid)}
    checks['time_query_runs_as_munin']=True
    for job,name in [('retention','/var/lib/ntpstats-retention/last-success.json'),('reporting','/var/lib/needrestart-reporting/last-success.json')]:
        path=Path(name);path.parent.mkdir(mode=0o700,exist_ok=True)
        path.write_text(json.dumps({'schema':1,'job':job,'status':'success','completed_epoch':time.time()}));path.chmod(0o600)
    output=run(['/usr/sbin/munin-run','ntp_jobs'])
    assert 'retention_evidence.value 1' in output and 'reporting_evidence.value 1' in output
    checks['root_private_heartbeat_read']=True
    assert policy.read_bytes()==old_policy
    run([str(policy),'fixture-unrelated','start'],allowed=(42,));checks['unrelated_policy_preserved']=True
    instance.recover();assert instance.state['recovery']=='contained'
    passed=True
except Exception as failure:
    error=str(failure)
    if instance.root.exists():
        if CASE in ('resume-recovery','held-recovery'):
            # Exercise the actual CLI's durable state readback in a new process.
            run(['/usr/bin/python3','-I','-B','/source/scripts/install_ntp_node.py','recover','--spec',str(ROOT/'spec.json'),'--sha256',digest],allowed=(1,) if CASE=='held-recovery' else (0,))
            instance.state=json.loads((instance.root/'state.json').read_text())
        else:instance.recover()
    expected={'guarded-failure':'injected guarded-failure','configured-failure':'injected configured-failure',
              'started-failure':'injected started-failure','foreign-policy':'injected foreign-policy',
              'foreign-guard':'injected foreign-guard','foreign-config':'injected foreign-config',
              'resume-recovery':'injected interruption','held-recovery':'injected held-recovery'}.get(CASE)
    if CASE=='activation-drift':expected='configuration/guard drift before activation'
    if CASE=='dpkg-failure':expected=error if error.startswith('command failed:') and 'invalid.deb' in error else None
    if error==expected and instance.state.get('recovery')==('held' if CASE in ('foreign-policy','foreign-guard','held-recovery') else 'contained'):
        if CASE in ('foreign-config','activation-drift'):assert m.CONFIG.read_text()=='foreign configuration\n'
        passed=True
finally:
    result={'scenario':CASE,'passed':passed,'error':error,'checks':checks,'state':instance.state,
            'spec_sha256':digest,'protected_service_identity':spec['service_identity']}
    Path('/evidence/result.json').write_bytes(m.encoded(result))
    print(json.dumps({k:result[k] for k in ('scenario','passed','error')}),flush=True)
if not passed:raise SystemExit(1)
