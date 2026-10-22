#!/usr/bin/python3
"""Hash-bound guarded NTP Munin installation; no master or network mutation."""
import argparse
import hashlib
import json
import os
import grp
import pwd
from pathlib import Path
import re
import signal
import socket
import stat
import subprocess
import time

PACKAGE_PLUGINS=('cpu','load','memory','uptime','processes')
CUSTOM_PLUGINS=('ntp_health','ntp_storage','ntp_statistics','ntp_jobs')
GUARD=Path('/etc/systemd/system/munin-node.service.d/00-ntp-install.conf')
POLICY=Path('/usr/sbin/policy-rc.d')
CONFIG=Path('/etc/munin/munin-node.conf')
CUSTOM=Path('/usr/local/munin/lib/plugins')
LINKS=Path('/etc/munin/plugins')
SETTINGS=Path('/etc/munin/plugin-conf.d')
MAX_INPUT=16*1048576


def encoded(value):return (json.dumps(value,sort_keys=True,indent=2)+'\n').encode()
def sha(raw):return hashlib.sha256(raw).hexdigest()


def secure(path,limit=MAX_INPUT):
    path=Path(path)
    for parent in path.parents:
        info=parent.lstat()
        if not stat.S_ISDIR(info.st_mode) or info.st_uid!=0 or info.st_mode&0o022:
            raise ValueError('unsafe input ancestor: '+str(parent))
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,'rb') as stream:
        info=os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid!=0 or info.st_mode&0o022 or info.st_size>limit:
            raise ValueError('unsafe regular input: '+str(path))
        raw=stream.read(limit+1)
    if len(raw)>limit:raise ValueError('input size bound')
    return raw,info


def atomic(path,raw,mode=0o600):
    path=Path(path);parent=path.parent
    if any(p.is_symlink() for p in (parent,*parent.parents)):raise ValueError('indirect output parent')
    if path.exists() or path.is_symlink():
        info=path.lstat()
        if not stat.S_ISREG(info.st_mode) or info.st_nlink!=1:raise ValueError('indirect/shared output')
    temporary=parent/(path.name+'.new')
    fd=os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,mode)
    try:
        with os.fdopen(fd,'wb') as stream:
            stream.write(raw);stream.flush();os.fsync(stream.fileno())
        os.chown(temporary,0,0);os.chmod(temporary,mode);os.replace(temporary,path)
        directory=os.open(parent,os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(directory)
        finally:os.close(directory)
    finally:temporary.unlink(missing_ok=True)


def node_config(hostname,hosts,allows):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9.-]{0,62}',hostname):raise ValueError('hostname shape')
    import ipaddress
    if not hosts or len(hosts)>2:raise ValueError('one or two listener addresses required')
    hosts=[str(ipaddress.ip_address(x)) for x in hosts]
    allows=[str(ipaddress.ip_address(x)) for x in allows]
    if not allows or len(allows)>4:raise ValueError('bounded explicit poller addresses required')
    return (('log_level 4\nlog_file /var/log/munin/munin-node.log\npid_file /run/munin/munin-node.pid\n'
             'background 1\nsetsid 1\nuser root\ngroup root\nhost_name '+hostname+'\n')+
            ''.join('port '+('['+host+']' if ':' in host else host)+':4949\n' for host in hosts)+
            ''.join('allow ^'+re.escape(address)+'$\n' for address in allows)).encode()


class Installer:
    def __init__(self,spec,digest):
        self.spec=spec;self.digest=digest
        if not re.fullmatch(r'[a-z][a-z0-9-]{0,63}',spec['operation_id']):raise ValueError('operation identity')
        self.root=Path('/var/lib/munin-ntp-install')/spec['operation_id']
        self.permit=self.root/'permit';self.state={'spec_sha256':digest,'accepted':False,'phase':'new','commands':[]}
        self.guard=('[Unit]\nConditionPathExists='+str(self.permit)+'\n').encode()
        self.owns_root=False

    def save(self):atomic(self.root/'state.json',encoded(self.state))

    def command(self,argv,allowed=(0,),env=None):
        p=subprocess.run(argv,capture_output=True,text=True,timeout=120,
                         env=env or {'PATH':'/usr/sbin:/usr/bin:/sbin:/bin','LC_ALL':'C'})
        self.state['commands'].append({'argv':argv,'returncode':p.returncode,'stdout':p.stdout[-65536:],'stderr':p.stderr[-65536:]})
        if p.returncode not in allowed:raise RuntimeError('command failed: '+repr(argv))
        return p.stdout

    def ctl(self,*args,allowed=(0,)):return self.command(['/usr/bin/systemctl',*args],allowed)

    def identity(self):
        unit='timeservice-fixture.service' if self.spec.get('fixture') else 'timeservice.service'
        raw=self.ctl('show',unit,'--property=MainPID,InvocationID,NRestarts,ActiveState,SubState')
        return dict(line.split('=',1) for line in raw.splitlines())

    def continuity(self):
        if self.identity()!=self.spec['service_identity']:raise ValueError('time service identity changed')
        for name,digest in self.spec['protected_files'].items():
            if name not in ('/etc/ntp.conf','/usr/local/bin/ntpq'):raise ValueError('protected path scope')
            if sha(secure(Path(name))[0])!=digest:raise ValueError('protected file changed')

    def checkpoint(self,phase):
        self.state['phase']=phase;self.continuity();self.save()

    def preflight(self):
        s=self.spec
        if os.geteuid()!=0 or s.get('schema')!=1 or s.get('profile')!='ntp':raise ValueError('root/schema/profile required')
        identity=s['service_identity']
        if identity.get('ActiveState')!='active' or identity.get('SubState')!='running' or not str(identity.get('MainPID','')).isdigit() or int(identity['MainPID'])<=0:
            raise ValueError('accepted running time service required')
        if set(s['protected_files'])!={'/etc/ntp.conf','/usr/local/bin/ntpq'}:raise ValueError('complete protected file set required')
        if socket.gethostname()!=s['hostname'] or Path('/proc/sys/kernel/random/boot_id').read_text().strip()!=s['boot_id']:
            raise ValueError('host/boot changed')
        arch=self.command(['/usr/bin/dpkg','--print-architecture']).strip()
        if arch!=s['architecture']:raise ValueError('architecture changed')
        if s.get('fixture'):
            if not Path('/run/.containerenv').exists() or Path('/proc/1/comm').read_text().strip()!='systemd':
                raise ValueError('fixture requires isolated systemd container')
        elif arch!='arm64':raise ValueError('production target must be arm64')
        inventory=self.command(['/usr/bin/dpkg-query','-W','-f=${binary:Package}\t${Version}\t${Architecture}\t${db:Status-Abbrev}\n'])
        if sha(inventory.encode())!=s['package_inventory_sha256']:raise ValueError('package inventory changed')
        if any(line.startswith(('munin-node\t','munin-common\t','munin-plugins-core\t')) for line in inventory.splitlines()):
            raise ValueError('new installation only')
        if self.ctl('show','munin-node.service','--property=LoadState').strip()!='LoadState=not-found':
            raise ValueError('preexisting Munin unit')
        if self.command(['/usr/bin/ss','-H','-lnt','sport = :4949']).strip():raise ValueError('preexisting listener')
        expected_policy=s['policy_before_sha256']
        if POLICY.exists() or POLICY.is_symlink():
            raw,info=secure(POLICY)
            if sha(raw)!=expected_policy or info.st_nlink!=1 or not info.st_mode&0o111:raise ValueError('preexisting policy differs from approved executable')
        elif expected_policy is not None:raise ValueError('approved policy missing')
        for path in (GUARD.parent,CONFIG.parent,CUSTOM, self.root):
            if path.exists() or path.is_symlink():raise ValueError('preexisting installation path: '+str(path))
            for parent in path.parents:
                if parent.is_symlink() or parent.exists() and (parent.stat().st_uid!=0 or parent.stat().st_mode&0o022):
                    raise ValueError('unsafe installation ancestor')
        source=Path(s['source_root']);expected={'node/profiles/ntp/profile.json','node/plugin-conf.d/ntp.conf',
                'node/plugins/ntp/ntp_metrics.py'}|{'node/plugins/ntp/'+p for p in CUSTOM_PLUGINS}
        if set(s['artifacts'])!=expected:raise ValueError('closed artifact set required')
        self.artifacts={}
        for name,digest in s['artifacts'].items():
            raw=secure(source/name)[0]
            if sha(raw)!=digest:raise ValueError('artifact integrity')
            self.artifacts[name]=raw
        profile=json.loads(self.artifacts['node/profiles/ntp/profile.json'])
        if profile['package_plugins']!=list(PACKAGE_PLUGINS) or profile['custom_plugins']!=list(CUSTOM_PLUGINS) or profile['root_plugins']!=['ntp_statistics','ntp_jobs']:
            raise ValueError('profile selection drift')
        expected_packages={'munin-common','munin-plugins-core','munin-node'}
        if not s.get('fixture'):
            expected_packages|={'libcgi-pm-perl','libexporter-tiny-perl','libhtml-parser-perl','libhtml-tagset-perl',
                'libio-multiplex-perl','libio-socket-inet6-perl','libio-socket-ssl-perl','liblist-moreutils-perl',
                'liblist-moreutils-xs-perl','libnet-cidr-perl','libnet-server-perl','liburi-perl'}
        if len(s['packages'])!=len(expected_packages) or {p['package'] for p in s['packages']}!=expected_packages:
            raise ValueError('exact package set required')
        self.packages=[]
        for row in s['packages']:
            p=Path(s['package_root'])/row['filename']
            if Path(row['filename']).name!=row['filename'] or sha(secure(p)[0])!=row['sha256']:raise ValueError('package integrity')
            metadata=self.command(['/usr/bin/dpkg-deb','-f',str(p),'Package','Version','Architecture'])
            fields=dict(line.split(': ',1) for line in metadata.splitlines())
            if any(fields[k]!=row[v] for k,v in [('Package','package'),('Version','version'),('Architecture','architecture')]):
                raise ValueError('package metadata drift')
            if row['architecture'] not in ('all',arch):raise ValueError('package architecture')
            self.packages.append(str(p))
        self.final=node_config(s['hostname'],s['listen_addresses'],s['allow_addresses'])
        self.continuity()

    def prepare(self):
        self.root.parent.mkdir(mode=0o700,exist_ok=True);self.root.mkdir(mode=0o700)
        self.owns_root=True
        atomic(self.root/'spec.json',encoded(self.spec));self.save()
        previous=None
        if POLICY.exists() or POLICY.is_symlink():
            raw,info=secure(POLICY)
            if info.st_nlink!=1:raise ValueError('shared policy file')
            previous={'hex':raw.hex(),'mode':stat.S_IMODE(info.st_mode),'uid':info.st_uid,'gid':info.st_gid}
            atomic(self.root/'original-policy',raw,0o700)
        wrapper=('#!/bin/sh\ncase "$1" in munin-node|munin-node.service) exit 101;; esac\n'+
                 ('exec '+str(self.root/'original-policy')+' "$@"\n' if previous else 'exit 0\n')).encode()
        self.state.update(previous_policy=previous,wrapper_hex=wrapper.hex(),guard_hex=self.guard.hex(),policy_intent=True)
        self.save();atomic(POLICY,wrapper,0o755)
        GUARD.parent.mkdir(parents=True);atomic(GUARD,self.guard,0o644)
        CONFIG.parent.mkdir(parents=True,mode=0o755);CONFIG.parent.chmod(0o755)
        atomic(CONFIG,node_config(self.spec['hostname'],['127.0.0.1'],['127.0.0.1']),0o644)
        bindir=self.root/'guard-bin';bindir.mkdir(mode=0o700)
        atomic(bindir/'munin-node-configure',b'#!/bin/sh\nprintf "%s\\n" "$*" >> "'+str(self.root).encode()+b'/autoconf-calls"\nexit 0\n',0o700)
        self.ctl('daemon-reload');self.checkpoint('guarded')

    def restore_policy(self):
        if not self.state.get('policy_intent'):return
        wrapper=bytes.fromhex(self.state['wrapper_hex'])
        if not POLICY.exists():
            if self.state.get('policy_restored') and self.state['previous_policy'] is None and not POLICY.is_symlink():return
            raise ValueError('policy missing; recovery held')
        raw,_=secure(POLICY)
        old=self.state['previous_policy']
        if self.state.get('policy_restored'):
            if old and raw==bytes.fromhex(old['hex']):return
            raise ValueError('restored policy drift; recovery held')
        if raw!=wrapper:raise ValueError('foreign policy; recovery held')
        if old:
            atomic(POLICY,bytes.fromhex(old['hex']),old['mode']);os.chown(POLICY,old['uid'],old['gid'])
        else:POLICY.unlink()
        self.state['policy_restored']=True;self.save()

    def install(self):
        self.preflight();self.prepare()
        self.state['dpkg_intent']=True;self.save()
        env={'PATH':str(self.root/'guard-bin')+':/usr/sbin:/usr/bin:/sbin:/bin','LC_ALL':'C','DEBIAN_FRONTEND':'noninteractive'}
        self.command(['/usr/bin/dpkg','--force-confdef','--force-confold','--install',*self.packages],env=env)
        if (self.root/'autoconf-calls').read_text().splitlines()!=['--shell']:raise ValueError('autoconfiguration boundary')
        if list(LINKS.iterdir()):raise ValueError('unreviewed plugin links')
        if self.command(['/usr/bin/ss','-H','-lnt','sport = :4949']).strip():raise ValueError('premature listener')
        self.checkpoint('packages-installed')
        if pwd.getpwnam('munin').pw_uid==0 or grp.getgrnam('munin').gr_gid==0:
            raise ValueError('Munin plugin identity must be unprivileged')
        for p in (Path('/usr/local/munin'),Path('/usr/local/munin/lib'),CUSTOM):
            if not p.exists():p.mkdir(mode=0o755);p.chmod(0o755)
            if p.is_symlink() or p.stat().st_uid!=0 or p.stat().st_mode&0o022:raise ValueError('unsafe custom directory')
        for name in (*CUSTOM_PLUGINS,'ntp_metrics.py'):
            atomic(CUSTOM/name,self.artifacts['node/plugins/ntp/'+name],0o644 if name.endswith('.py') else 0o755)
        defaults=list(SETTINGS.iterdir())
        if {p.name for p in defaults}!={'README','munin-node'}:raise ValueError('unexpected package settings')
        if sha(secure(SETTINGS/'README')[0])!=self.spec['settings_readme_sha256']:raise ValueError('package settings README drift')
        default=SETTINGS/'munin-node';raw,_=secure(default)
        if sha(raw)!=self.spec['default_settings_sha256']:raise ValueError('package default settings drift')
        atomic(self.root/'package-default-settings',raw,0o600);default.unlink()
        atomic(SETTINGS/'ntp',self.artifacts['node/plugin-conf.d/ntp.conf'],0o644)
        for name in PACKAGE_PLUGINS:(LINKS/name).symlink_to('/usr/share/munin/plugins/'+name)
        for name in CUSTOM_PLUGINS:(LINKS/name).symlink_to(CUSTOM/name)
        atomic(CONFIG,self.final,0o644);self.state['final_config_sha256']=sha(self.final);self.save()
        self.restore_policy();self.checkpoint('configured')
        self.validate_installed()
        atomic(self.permit,b'',0o600);self.state['activation_intent']=True;self.save()
        self.ctl('daemon-reload');self.ctl('enable','munin-node.service');self.ctl('start','munin-node.service')
        self.checkpoint('started')
        status=self.ctl('show','munin-node.service','--property=ActiveState,SubState')
        if set(status.splitlines())!={'ActiveState=active','SubState=running'}:raise ValueError('node not running')
        listeners=self.command(['/usr/bin/ss','-H','-lnt','sport = :4949'])
        for address in self.spec['listen_addresses']:
            if address+':4949' not in listeners and '['+address+']:4949' not in listeners:raise ValueError('required listener missing')
        if any(token in listeners for token in ('0.0.0.0:4949','*:4949','[::]:4949')):raise ValueError('wildcard listener')
        self.state.update(accepted=True,phase='node-running',polling_accepted=False,delivery_accepted=False);self.save()
        return self.state

    def validate_installed(self):
        if secure(CONFIG)[0]!=self.final or secure(GUARD)[0]!=self.guard:raise ValueError('configuration/guard drift before activation')
        if {p.name for p in LINKS.iterdir()}!=set(PACKAGE_PLUGINS+CUSTOM_PLUGINS):raise ValueError('plugin selection drift')
        for name in PACKAGE_PLUGINS+CUSTOM_PLUGINS:
            expected=Path('/usr/share/munin/plugins')/name if name in PACKAGE_PLUGINS else CUSTOM/name
            if not (LINKS/name).is_symlink() or (LINKS/name).readlink()!=expected:raise ValueError('plugin link drift')
        if {p.name for p in SETTINGS.iterdir()}!={'README','ntp'}:raise ValueError('plugin settings selection drift')
        if secure(SETTINGS/'ntp')[0]!=self.artifacts['node/plugin-conf.d/ntp.conf']:raise ValueError('plugin privilege settings drift')
        if sha(secure(SETTINGS/'README')[0])!=self.spec['settings_readme_sha256']:raise ValueError('package README drift')
        for name in (*CUSTOM_PLUGINS,'ntp_metrics.py'):
            if secure(CUSTOM/name)[0]!=self.artifacts['node/plugins/ntp/'+name]:raise ValueError('custom source drift')

    def recover(self):
        if os.geteuid()!=0 or socket.gethostname()!=self.spec['hostname'] or Path('/proc/sys/kernel/random/boot_id').read_text().strip()!=self.spec['boot_id']:
            raise ValueError('recovery root/host/boot drift; no recovery mutation submitted')
        errors=[]
        if self.permit.exists() or self.permit.is_symlink():
            try:
                raw,_=secure(self.permit)
                if raw:raise ValueError('foreign permit')
                self.permit.unlink()
            except Exception:errors.append('permit changed; held')
        try:self.ctl('stop','munin-node.service',allowed=(0,5));self.ctl('disable','munin-node.service',allowed=(0,1,5))
        except Exception:errors.append('service containment failed')
        try:self.restore_policy()
        except Exception as error:errors.append(str(error))
        try:
            if secure(GUARD)[0]!=self.guard:errors.append('foreign/missing startup guard')
            if self.command(['/usr/bin/ss','-H','-lnt','sport = :4949']).strip():errors.append('listener remains')
            self.continuity()
        except Exception:errors.append('guard/listener/continuity check failed')
        self.state.update(accepted=False,recovery='held' if errors else 'contained',recovery_errors=errors)
        self.save();return self.state


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=('apply','recover'))
    p.add_argument('--spec',type=Path,required=True);p.add_argument('--sha256',required=True);args=p.parse_args()
    os.umask(0o077);raw=secure(args.spec)[0]
    if sha(raw)!=args.sha256:raise SystemExit('approved spec digest mismatch')
    installer=Installer(json.loads(raw),args.sha256)
    def interrupted(signum,frame):raise InterruptedError('installation interrupted')
    signal.signal(signal.SIGTERM,interrupted)
    if args.action=='recover':
        state=json.loads(secure(installer.root/'state.json')[0])
        if state['spec_sha256']!=args.sha256:raise SystemExit('recovery scope mismatch')
        installer.state=state;result=installer.recover()
    else:
        try:result=installer.install()
        except BaseException:
            if installer.owns_root:installer.recover()
            raise
    print(json.dumps({k:result.get(k) for k in ('accepted','phase','recovery')}))
    if args.action=='recover' and result.get('recovery')!='contained':raise SystemExit(1)


if __name__=='__main__':main()
