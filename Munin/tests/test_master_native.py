#!/usr/bin/python3
"""Actual Bookworm package/systemd/CGI commissioning and recovery in network=none."""
import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import pwd
import grp
import socket
import ssl
import subprocess
import sys
import threading
import time

assert os.geteuid()==0 and Path('/run/.containerenv').exists()
assert Path('/proc/1/comm').read_text().strip()=='systemd'
ROOT=Path('/workspace/homelab-monitoring-observability/Munin')


def load(path):
    spec=importlib.util.spec_from_file_location(path.stem,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


r=load(ROOT/'scripts/deploy_ntp_master.py');base=load(ROOT/'scripts/install_ntp_node.py')
q=load(ROOT/'scripts/qualify_master.py');w=load(ROOT/'scripts/install_ntp_master.py')
CASE=sys.argv[1]
assert CASE in ('success','configured-failure','prepared-failure','foreign-config','foreign-link','preflight-drift','worker-loss','controller-loss','health-reject')
os.umask(0o077)


def run(argv,allowed=(0,)):
    p=subprocess.run(argv,capture_output=True,text=True,timeout=60,umask=0o022)
    if p.returncode not in allowed:raise RuntimeError(repr(argv)+'\n'+p.stdout+'\n'+p.stderr)
    return p.stdout.strip()


def unit(name):
    raw=run(['systemctl','show',name,'--property=ActiveState,SubState,MainPID,InvocationID,NRestarts'])
    return dict(v.split('=',1) for v in raw.splitlines())


def wait(check,seconds=30):
    end=time.monotonic()+seconds
    while time.monotonic()<end:
        result=check()
        if result:return result
        time.sleep(.2)
    raise TimeoutError('native qualification checkpoint')


def setup():
    run(['systemctl','stop','cron.service'],allowed=(0,5))
    clock=Path('/etc/systemd/system/master-continuity-fixture.service')
    clock.write_text('[Service]\nExecStart=/bin/sleep infinity\n')
    run(['systemctl','daemon-reload']);run(['systemctl','start',clock.name])
    for address in ('10.1.3.83/32','fd36:5aa8:6971:1::83/128'):
        run(['ip','address','add',address,'dev','lo'])
    for p in Path('/etc/munin/plugins').iterdir():p.unlink()
    for name in ('load','uptime'):
        (Path('/etc/munin/plugins')/name).symlink_to('/usr/share/munin/plugins/'+name)
    Path('/etc/munin/munin-node.conf').write_text('''log_level 4
log_file /var/log/munin/munin-node.log
pid_file /run/munin/munin-node.pid
background 1
setsid 1
user root
group root
host_name J1-SVMF
host 127.0.0.1
port 4949
allow ^127\\.0\\.0\\.1$
''')
    baseline=b'''dbdir /var/lib/munin
htmldir /var/cache/munin/www
logdir /var/log/munin
rundir /run/munin
tmpldir /etc/munin/templates
staticdir /etc/munin/static
cgitmpdir /var/lib/munin/cgi-tmp
includedir /etc/munin/munin-conf.d
graph_strategy cgi
html_strategy cgi
rrdcached_socket /var/run/rrdcached.sock
[J1-SVMF]
    address 127.0.0.1
    use_node_name yes
'''
    w.CONFIG.write_bytes(baseline);w.CONFIG.chmod(0o644)
    for p in Path('/etc/munin/munin-conf.d').iterdir():p.unlink()
    run(['usermod','-a','-G','munin','www-data'])
    cgitmp=Path('/var/lib/munin/cgi-tmp');cgitmp.mkdir(exist_ok=True)
    os.chown(cgitmp,pwd.getpwnam('www-data').pw_uid,grp.getgrnam('munin').gr_gid);cgitmp.chmod(0o770)
    run(['systemctl','stop','rrdcached.service'])
    cache_unit=Path('/etc/systemd/system/rrdcached.service')
    cache_unit.write_text('''[Service]
Type=simple
User=munin
Group=munin
RuntimeDirectory=munin-rrdcached
RuntimeDirectoryMode=0775
ExecStart=/usr/bin/rrdcached -g -m 0660 -l unix:/run/munin-rrdcached/rrdcached.sock -p /run/munin-rrdcached/rrdcached.pid
''');cache_unit.chmod(0o644)
    run(['systemctl','daemon-reload']);run(['systemctl','start','rrdcached.service'])
    native_socket=Path('/run/munin-rrdcached/rrdcached.sock');wait(native_socket.exists)
    cache=Path('/run/rrdcached.sock')
    if os.path.lexists(cache):cache.unlink()
    cache.symlink_to(native_socket)
    certdir=Path('/etc/ssl/local.theama.co');certdir.mkdir(exist_ok=True)
    cert=certdir/'STAR_local_theama_co.crt';key=certdir/'STAR_local_theama_co.key'
    run(['openssl','req','-x509','-nodes','-newkey','rsa:2048','-days','2',
        '-keyout',str(key),'-out',str(cert),'-subj','/CN=munin.local.theama.co',
        '-addext','subjectAltName=DNS:munin.local.theama.co'])
    key.chmod(0o600);(certdir/'STAR_local_theama_co.ca-bundle').write_bytes(cert.read_bytes())
    run(['a2enmod','ssl','rewrite','fcgid']);run(['a2dissite','000-default'])
    vhost=Path('/etc/apache2/sites-available/001-munin.theama.co-ssl.conf')
    vhost.write_bytes((ROOT.parent/'Apache2/configs/001-munin.theama.co-ssl.conf').read_bytes())
    link=Path('/etc/apache2/sites-enabled')/vhost.name
    if not link.exists():link.symlink_to(vhost)
    run(['systemctl','restart','munin-node.service']);run(['systemctl','restart','apache2.service'])
    # Actual native cycle initializes both data and limits; there are no contacts.
    run(['runuser','-u','munin','--','/usr/bin/munin-cron'])
    (Path('/var/lib/munin')/'preserved-history').write_bytes(b'preserve all historical data\n')
    return baseline,cert,vhost


def main():
    baseline,cert,vhost=setup()
    before_apache=unit('apache2.service');before_node=unit('munin-node.service');cache_before=unit('rrdcached.service')
    files={n:p.read_bytes() for n,p in r.SOURCES.items()}
    candidate=q.commissioning_config(q.without_rrdcached(baseline))
    files.update({'baseline.conf':baseline,'candidate.conf':candidate,'ca.pem':cert.read_bytes(),
        'plugin':(ROOT/'master/plugins/ntp_transport_j2').read_bytes(),
        'settings':(ROOT/'master/configs/ntp-transport.plugin-conf.example').read_bytes(),
        'qualification.json':r.encoded({'fixture_only':True,'production_qualification':False}),
        'known_hosts':b'fixture no SSH transport\n'})
    operation='munin-master-fixture-'+CASE
    pins={'operation_id':operation,'hostname':socket.gethostname(),
        'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
        'continuity_unit':'master-continuity-fixture.service','service_identity':unit('master-continuity-fixture.service'),
        'apache_identity':before_apache,'cron_identity':unit('cron.service'),
        'protected_files':{str(vhost):r.sha(vhost.read_bytes()),'/etc/cron.d/munin':r.sha(Path('/etc/cron.d/munin').read_bytes())},
        'package_inventory_sha256':r.sha(subprocess.check_output(['/usr/bin/dpkg-query','-W','-f=${binary:Package}\t${Version}\t${Architecture}\t${db:Status-Abbrev}\n'])),
        'before_sha256':r.sha(baseline),'candidate_sha256':r.sha(candidate),'fixture':True,
        'transport_expected':{'v4':'0','v6':'0','mail':'U'},
        'artifacts':{k:base64.b64encode(files[n]).decode() for k,n in
            (('config','candidate.conf'),('plugin','plugin'),('settings','settings'))}}
    if CASE in ('configured-failure','prepared-failure','foreign-config','foreign-link','worker-loss'):
        phase='prepared' if CASE=='prepared-failure' else 'configured'
        effect=("CONFIG.write_bytes(b'foreign master config\\n')" if CASE=='foreign-config' else
                "LINK.unlink(); LINK.symlink_to('/foreign/source')" if CASE=='foreign-link' else
                "time.sleep(300)" if CASE=='worker-loss' else 'pass')
        files['worker.py']+=('''
_original_factory=make_worker
def make_worker(base,qualifier):
    Original=_original_factory(base,qualifier)
    class Fault(Original):
        def checkpoint(self,phase):
            super().checkpoint(phase)
            if phase=='''+repr(phase)+''':
                '''+effect+'''
                raise RuntimeError('qualification injected failure')
    return Fault
''').encode()
    now=int(time.time());spec={'operation_id':operation,'prepared_epoch':now,'expires_epoch':now+86400,
        'recovery_seconds':60 if CASE=='success' else 10,'worker':pins,'addresses':['10.1.3.83','fd36:5aa8:6971:1::83'],
        'qualification_sha256':r.sha(files['qualification.json']),
        'leaf_sha256':r.sha(ssl.PEM_cert_to_DER_cert(cert.read_text())),
        'paths':['/','/static/style-new.css','/munin-cgi/munin-cgi-graph/J1-SVMF/J1-SVMF/load-day.png']}
    before_https=r.health(spec,files)
    history_before={str(p):p.stat().st_ino for p in Path('/var/lib/munin').rglob('*.rrd')}
    assert history_before,'native cycle must create genuine RRD files'
    operation_input=Path('/var/lib/qualification-input');digest=r.write_archive(operation_input,spec,files)
    raw=(operation_input/'deployment.tar').read_bytes();state_dir=w.STATE/operation
    if CASE=='preflight-drift':w.CONFIG.write_bytes(baseline+b'# foreign baseline edit\n')
    if CASE=='worker-loss':
        results=[];errors=[]
        def launch():
            try:results.append(r.root_launch(raw,digest))
            except BaseException as error:errors.append(str(error))
        thread=threading.Thread(target=launch);thread.start()
        wait(lambda:(state_dir/'state.json').exists() and json.loads((state_dir/'state.json').read_text()).get('phase')=='configured')
        run(['systemctl','kill','--signal=SIGKILL',operation+'-worker.service'])
        thread.join(45);assert not thread.is_alive() and not errors,errors
        result=results[0]
    else:result=r.root_launch(raw,digest)
    stage=r.STAGES/operation
    if CASE=='controller-loss':
        assert result['phase']=='prepared',result
        def restored():
            current=json.loads((stage/'result.json').read_text())
            return current if current.get('phase')=='restored' else None
        result=wait(restored,seconds=30)
    if CASE=='health-reject':
        assert result['phase']=='prepared',result
        rejected=dict(spec,paths=['/','/static/style-new.css','/munin-cgi/not-a-graph'])
        try:r.health(rejected,files)
        except r.HealthRejected as error:
            assert error.observations[-1].get('status') in (403,404)
        else:raise AssertionError('native rejected response was not rejected')
        result=r.locked_worker(stage,digest,'recover')
    if CASE=='success':
        assert result['phase']=='prepared',result
        after_https=r.health(spec,files)
        result=r.locked_worker(stage,digest,'commit');assert result['phase']=='committed' and result['accepted'],result
        assert w.CONFIG.read_bytes()==candidate
        assert unit('munin-node.service')['MainPID']!=before_node['MainPID']
        assert r.locked_worker(stage,digest,'recover')['phase']=='committed'
        result['https_after']=after_https
    elif CASE.startswith('foreign-'):
        assert result['phase']=='recovery-held' and result['recovery_errors'],result
        if CASE=='foreign-config':assert w.CONFIG.read_bytes()==b'foreign master config\n'
        else:assert w.LINK.is_symlink() and os.readlink(w.LINK)=='/foreign/source'
    elif CASE=='preflight-drift':
        assert result['phase']=='preflight-failed',result
        assert not state_dir.exists()
        assert w.CONFIG.read_bytes()==baseline+b'# foreign baseline edit\n'
    else:
        assert result['phase']=='restored' and not result['recovery_errors'],result
        assert w.CONFIG.read_bytes()==baseline
        assert all(not os.path.lexists(p) for p in (w.PLUGIN,w.SETTINGS,w.LINK))
        result['https_restored']=r.health(spec,files)
        if CASE=='prepared-failure':
            restored_node=unit('munin-node.service')
            wait(lambda:run(['systemctl','is-active',operation+'-recover.timer'],allowed=(0,3,4))!='active',seconds=20)
            wait(lambda:run(['systemctl','is-active',operation+'-recover.service'],allowed=(0,3,4))!='active',seconds=20)
            assert unit('munin-node.service')==restored_node
            result['later_guard_noop_accepted']=True
    assert all(Path(p).stat().st_ino==inode for p,inode in history_before.items())
    assert unit('apache2.service')==before_apache
    assert unit('rrdcached.service')==cache_before
    assert (Path('/var/lib/munin')/'preserved-history').read_bytes()==b'preserve all historical data\n'
    result.update(case=CASE,passed=True,actual_packages=run(['dpkg-query','-W','munin','munin-node','apache2']),
                  fixture_transport_values={'v4':0,'v6':0,'mail':'U'},
                  production_transport_or_polling_accepted=False,https_before=before_https)
    native_paths=['/usr/lib/munin/cgi/munin-cgi-html','/usr/lib/munin/cgi/munin-cgi-graph',
        '/usr/lib/systemd/system/munin-node.service',
        *['/usr/share/perl5/Munin/'+p for p in ('Common/Config.pm','Master/Config.pm','Master/Utils.pm',
            'Master/GraphOld.pm','Master/UpdateWorker.pm','Master/Update.pm','Master/LimitsOld.pm')]]
    result['native_hashes']={p:r.sha(Path(p).read_bytes()) for p in native_paths}
    if (state_dir/'state.json').exists():
        result['worker_state']=json.loads((state_dir/'state.json').read_text())
        if CASE in ('success','prepared-failure','worker-loss','controller-loss','health-reject'):
            assert {Path(x['script']).name for x in result['worker_state']['cgi_recycled']}==w.CGI
    Path('/evidence/result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'case':CASE,'passed':True,'phase':result['phase']}))


if __name__=='__main__':
    try:main()
    except BaseException as error:
        Path('/evidence/failure.json').write_text(json.dumps({'case':CASE,'error':str(error),
            'observations':getattr(error,'observations',[])},indent=2)+'\n')
        raise
