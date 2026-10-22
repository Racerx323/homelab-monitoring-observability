#!/usr/bin/python3
"""Guarded master commissioning; contacts disabled, no job/update/limits invocation."""
import base64
import json
import os
from pathlib import Path
import pwd
import re
import signal
import socket
import stat
import time

CONFIG=Path('/etc/munin/munin.conf')
PLUGIN=Path('/usr/local/munin/lib/plugins/ntp_transport_j2')
SETTINGS=Path('/etc/munin/plugin-conf.d/ntp-transport.conf')
LINK=Path('/etc/munin/plugins/ntp_transport_j2')
STATE=Path('/var/lib/munin-ntp-master')
CGI={'munin-cgi-html','munin-cgi-graph'}
ENV={'PATH':'/usr/sbin:/usr/bin:/sbin:/bin','LC_ALL':'C'}


def sync(directory):
    fd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:os.fsync(fd)
    finally:os.close(fd)


def make_worker(base, qualifier):
    class Installer(base.Installer):
        def __init__(self,spec,digest):
            super().__init__(spec,digest)
            self.root=STATE/spec['operation_id']
            self.owns_root=False
            self.artifacts={}
            self.state.update(changes=[],created_directories=[],cgi_recycled=[],recovery_errors=[])

        def unit(self,name):
            raw=self.ctl('show',name,'--property=ActiveState,SubState,MainPID,InvocationID,NRestarts')
            return dict(row.split('=',1) for row in raw.splitlines())

        def continuity(self):
            if self.unit(self.spec['continuity_unit'])!=self.spec['service_identity']:
                raise ValueError('master continuity changed')
            if self.unit('apache2.service')!=self.spec['apache_identity']:
                raise ValueError('Apache identity changed')
            if self.unit('cron.service')!=self.spec['cron_identity']:
                raise ValueError('native cron identity changed')
            for path,digest in self.spec['protected_files'].items():
                if base.sha(base.secure(Path(path))[0])!=digest:
                    raise ValueError('protected master input changed: '+path)
            self.includes_empty()
            if 'plugin_settings_before' in self.state and self.settings_metadata()!=self.state['plugin_settings_before']:
                raise ValueError('unrelated plugin settings metadata changed')

        def includes_empty(self):
            path=Path('/etc/munin/munin-conf.d')
            if path.is_symlink():raise ValueError('indirect include directory')
            if path.exists():
                count=0
                for p in path.iterdir():
                    count+=1
                    if count>64 or not p.name.startswith('.') and not p.name.endswith('~'):
                        raise ValueError('effective includes require separate review')

        def settings_metadata(self):
            result={}
            for p in Path('/etc/munin/plugin-conf.d').iterdir():
                if p==SETTINGS:continue
                if len(result)>=64:raise ValueError('plugin settings count bound')
                m=p.lstat()
                if not stat.S_ISREG(m.st_mode) or m.st_uid!=0 or m.st_mode&0o022:
                    raise ValueError('unreviewed plugin settings file type/owner/mode')
                result[p.name]=[m.st_dev,m.st_ino,m.st_size,m.st_mtime_ns,m.st_mode,m.st_uid,m.st_gid]
            return result

        def nodes(self):
            directory=Path('/etc/munin/plugins')
            result={}
            for p in directory.iterdir():
                if len(result)>=512:raise ValueError('plugin directory bound')
                if p==LINK:continue
                result[p.name]=os.readlink(p) if p.is_symlink() else base.sha(base.secure(p)[0])
            return result

        def checkpoint(self,phase):
            self.state['phase']=phase;self.continuity();self.save()

        def parser(self,raw):
            # No native startup, include expansion, logging or contact execution.
            import subprocess
            payload=json.dumps({'candidate':[raw.decode()]}).encode()
            row=subprocess.run(['/usr/sbin/runuser','-u','munin','--','/usr/bin/perl','-e',qualifier.PARSER],
                input=payload,capture_output=True,timeout=30,env=ENV)
            self.state['commands'].append({'argv':['native-in-memory-parser-as-munin'],
                'returncode':row.returncode,'stderr':row.stderr.decode(errors='replace')[:16384]})
            if (row.returncode or row.stderr or not json.loads(row.stdout)['candidate']['parsed']):
                raise ValueError('installed native parser rejected candidate')

        def preflight(self):
            s=self.spec
            if (os.geteuid()!=0 or os.getegid()!=0 or socket.gethostname()!=s['hostname']
                    or Path('/proc/sys/kernel/random/boot_id').read_text().strip()!=s['boot_id']):
                raise ValueError('master root/host/boot mismatch')
            if s.get('fixture'):
                if not Path('/run/.containerenv').exists() or Path('/proc/1/comm').read_text().strip()!='systemd':
                    raise ValueError('fixture requires isolated systemd container')
            elif (s['hostname']!='J1-SVMF' or s['transport_expected']!={'v4':'1','v6':'1','mail':'U'}
                  or s['continuity_unit']!='NetworkManager.service'):
                raise ValueError('production master scope mismatch')
            self.continuity()
            fd=os.pidfd_open(os.getpid())
            try:signal.pidfd_send_signal(fd,0)
            finally:os.close(fd)
            if self.root.exists() or self.root.is_symlink():raise ValueError('consumed master operation')
            if self.unit('munin-node.service')['ActiveState']!='active':
                raise ValueError('existing master node must be running')
            inventory=self.command(['/usr/bin/dpkg-query','-W','-f=${binary:Package}\t${Version}\t${Architecture}\t${db:Status-Abbrev}\n'])
            if base.sha(inventory.encode())!=s['package_inventory_sha256']:
                raise ValueError('master package inventory drift')
            before,info=base.secure(CONFIG)
            if base.sha(before)!=s['before_sha256'] or stat.S_IMODE(info.st_mode)!=0o644 or info.st_nlink!=1 or info.st_gid!=0:
                raise ValueError('master baseline drift or unsafe metadata')
            self.artifacts={n:base64.b64decode(v,validate=True) for n,v in s['artifacts'].items()}
            candidate=qualifier.commissioning_config(qualifier.without_rrdcached(before))
            if candidate!=self.artifacts['config'] or base.sha(candidate)!=s['candidate_sha256']:
                raise ValueError('candidate does not match preserving renderer')
            includes=Path('/etc/munin/munin-conf.d')
            if includes.is_symlink():raise ValueError('indirect include directory')
            if includes.exists() and any(not p.name.startswith('.') and not p.name.endswith('~') for p in includes.iterdir()):
                raise ValueError('effective includes require separate review')
            for path in (PLUGIN,SETTINGS,LINK):
                if os.path.lexists(path):raise ValueError('preexisting authored destination: '+str(path))
            for path in (PLUGIN.parent,SETTINGS.parent,LINK.parent,STATE):
                for parent in (path,*path.parents):
                    if os.path.lexists(parent):
                        info=parent.lstat()
                        if not stat.S_ISDIR(info.st_mode) or info.st_uid!=0 or info.st_mode&0o022:
                            raise ValueError('unsafe destination ancestry')
            device=Path('/var/lib').stat().st_dev
            for path in (PLUGIN.parent,SETTINGS.parent,LINK.parent,CONFIG.parent):
                while not path.exists():path=path.parent
                if path.stat().st_dev!=device:raise ValueError('publication proof requires one filesystem')
            self.state['plugins_before']=self.nodes()
            self.state['plugin_settings_before']=self.settings_metadata()
            self.state['node_config_sha256']=base.sha(base.secure(Path('/etc/munin/munin-node.conf'))[0])
            self.state['cgi_before']=self.cgi_workers()
            self.state['protocol_before']=self.native_protocol()
            self.parser(candidate)

        def mkdirs(self,directory):
            missing=[];p=directory
            while not p.exists():missing.append(p);p=p.parent
            for p in reversed(missing):
                self.state['created_directories'].append(str(p));self.save()
                p.mkdir(mode=0o755)
                sync(p.parent)
                self.state.setdefault('directory_identity',{})[str(p)]=[p.stat().st_dev,p.stat().st_ino]
                self.save()

        def publish(self,path,raw,mode):
            proof=self.root/('proof-'+path.name)
            base.atomic(proof,raw,mode)
            info=proof.stat()
            row={'path':str(path),'proof':str(proof),'sha256':base.sha(raw),'device':info.st_dev,'inode':info.st_ino}
            self.state['changes'].append(row);self.save()
            os.link(proof,path)  # no-clobber publication; proof records ownership before linking
            sync(path.parent)
            self.save()

        def file_set(self,candidate=True):
            expected=self.spec['candidate_sha256'] if candidate else self.spec['before_sha256']
            if base.sha(base.secure(CONFIG)[0])!=expected:raise ValueError('master config readback drift')
            if base.sha(base.secure(Path('/etc/munin/munin-node.conf'))[0])!=self.state['node_config_sha256']:
                raise ValueError('existing node config drift')
            if self.nodes()!=self.state['plugins_before']:raise ValueError('unrelated node plugin drift')
            if candidate:
                m=CONFIG.lstat()
                if [m.st_dev,m.st_ino]!=self.state['config_identity']:
                    raise ValueError('authored master config identity drift')
                for row in self.state['changes']:
                    p=Path(row['path']);m=p.lstat()
                    if [m.st_dev,m.st_ino]!=[row['device'],row['inode']] or base.sha(base.secure(p)[0])!=row['sha256']:
                        raise ValueError('authored file drift')
                if not LINK.is_symlink() or os.readlink(LINK)!=str(PLUGIN):raise ValueError('transport link drift')
            self.state['last_readback']={'config_sha256':base.sha(base.secure(CONFIG)[0]),
                'candidate':candidate,'epoch':time.time()}

        def cgi_identity(self,pid):
            p=Path('/proc')/str(pid)
            try:
                if (p/'comm').read_text().strip() not in CGI:return None
                fields=(p/'stat').read_text().rsplit(')',1)[1].split()
                if fields[0]=='Z':return None
                args=(p/'cmdline').read_bytes()[:8193].split(b'\0')
                scripts=[v.decode() for v in args if v in {('/usr/lib/munin/cgi/'+n).encode() for n in CGI}]
                if len(scripts)!=1:return None
                uid=p.stat().st_uid
                if uid!=pwd.getpwnam('www-data').pw_uid:raise ValueError('unreviewed native CGI uid')
                ancestor=int(fields[1]);main=int(self.spec['apache_identity']['MainPID'])
                for _ in range(16):
                    if ancestor==main:break
                    if ancestor<=1:raise ValueError('CGI not owned by accepted Apache')
                    ancestor=int((Path('/proc')/str(ancestor)/'stat').read_text().rsplit(')',1)[1].split()[1])
                else:raise ValueError('CGI ancestry bound')
                return {'pid':pid,'start':fields[19],'uid':uid,'script':scripts[0]}
            except (FileNotFoundError,ProcessLookupError):return None

        def cgi_workers(self):
            result=[];count=0
            for p in Path('/proc').iterdir():
                if not p.name.isdigit():continue
                count+=1
                if count>32768:raise ValueError('process enumeration bound')
                row=self.cgi_identity(int(p.name))
                if row:result.append(row)
                if len(result)>64:raise ValueError('native CGI worker bound')
            return result

        def refresh_cgi(self):
            self.continuity()
            workers=self.cgi_workers()
            for row in workers:
                try:fd=os.pidfd_open(row['pid'])
                except ProcessLookupError:continue
                try:
                    if self.cgi_identity(row['pid'])==row:
                        signal.pidfd_send_signal(fd,signal.SIGTERM)
                        self.state['cgi_recycled'].append(row);self.save()
                finally:os.close(fd)
            deadline=time.monotonic()+15
            while any(self.cgi_identity(r['pid'])==r for r in workers):
                if time.monotonic()>deadline:raise ValueError('native CGI did not terminate')
                time.sleep(.1)
            self.continuity()

        def plugin_check(self):
            output=self.command(['/usr/sbin/munin-run','ntp_transport_j2','config'])
            if not all(f'{x}.label ' in output for x in ('v4','v6','mail')):
                raise ValueError('transport config output incomplete')
            output=self.command(['/usr/sbin/munin-run','ntp_transport_j2'])
            rows=dict(line.split('.value ',1) for line in output.splitlines())
            if rows!=self.spec['transport_expected']:raise ValueError('master transport field acceptance failed')

        def native_protocol(self,after=False):
            deadline=time.monotonic()+10
            while True:
                try:
                    connection=socket.create_connection(('127.0.0.1',4949),timeout=1)
                    break
                except ConnectionRefusedError:
                    if time.monotonic()>=deadline:raise
                    time.sleep(.1)
            with connection:
                connection.settimeout(35)
                with connection.makefile('rb') as stream:
                    def line():
                        raw=stream.readline(8193)
                        if not raw or len(raw)>8192 or not raw.endswith(b'\n'):
                            raise ValueError('bounded local node protocol line required')
                        return raw.decode('ascii').strip()
                    def send(text):connection.sendall(text.encode()+b'\n')
                    def frame():
                        rows=[]
                        for _ in range(128):
                            row=line()
                            if row=='.':return rows
                            rows.append(row)
                        raise ValueError('local node protocol frame bound')
                    greeting=line()
                    if not re.fullmatch(r'# munin node at [A-Za-z0-9_.-]{1,96}',greeting):
                        raise ValueError('local node greeting')
                    send('list '+greeting.rsplit(' ',1)[1]);plugins=line().split()
                    self.state['last_protocol']={'greeting':greeting,'plugins':sorted(plugins)}
                    if self.owns_root:self.save()
                    if not plugins or len(plugins)>512 or len(plugins)!=len(set(plugins)):
                        raise ValueError('local plugin list bound/duplicate')
                    if after:
                        before=self.state['protocol_before']
                        if greeting!=before['greeting']:raise ValueError('native node greeting changed')
                        if set(plugins)!=set(before['plugins'])|{'ntp_transport_j2'}:
                            raise ValueError('native served plugin set changed')
                        send('config ntp_transport_j2');config=frame()
                        if not all(any(row.startswith(k+'.label ') for row in config) for k in ('v4','v6','mail')):
                            raise ValueError('served transport config missing')
                        send('fetch ntp_transport_j2');values=frame()
                        if sorted(values)!=sorted(k+'.value '+v for k,v in self.spec['transport_expected'].items()):
                            raise ValueError('served transport fetch acceptance')
                    send('quit')
            return {'greeting':greeting,'plugins':sorted(plugins)}

        def install(self):
            self.preflight()
            if not STATE.exists():STATE.mkdir(mode=0o700)
            sync(STATE.parent)
            self.root.mkdir(mode=0o700);sync(STATE);self.owns_root=True;self.save()
            base.atomic(self.root/'config.before',base.secure(CONFIG)[0])
            self.checkpoint('backed-up')
            self.mkdirs(PLUGIN.parent)
            self.publish(PLUGIN,self.artifacts['plugin'],0o755)
            self.publish(SETTINGS,self.artifacts['settings'],0o644)
            proof=self.root/'link-proof';proof.symlink_to(PLUGIN)
            m=proof.lstat();self.state['link_identity']=[m.st_dev,m.st_ino];self.save()
            os.link(proof,LINK,follow_symlinks=False)
            sync(LINK.parent)
            proof=self.root/'config-proof';base.atomic(proof,self.artifacts['config'],0o644)
            m=proof.lstat();self.state['config_identity']=[m.st_dev,m.st_ino]
            self.state['config_intent']=True;self.save()
            if base.sha(base.secure(CONFIG)[0])!=self.spec['before_sha256']:raise ValueError('late baseline drift')
            publication=self.root/'config-publication';os.link(proof,publication)
            os.replace(publication,CONFIG)
            sync(CONFIG.parent);sync(self.root)
            self.checkpoint('configured')
            self.parser(base.secure(CONFIG)[0]);self.file_set();self.plugin_check()
            self.state['node_restart_intent']=True;self.save()
            self.ctl('restart','munin-node.service')
            if self.unit('munin-node.service')['ActiveState']!='active':raise ValueError('master node did not restart')
            self.refresh_cgi();self.file_set();self.plugin_check();self.native_protocol(after=True)
            self.checkpoint('prepared')

        def commit(self):
            if self.state.get('phase')!='prepared':raise ValueError('prepared master stage required')
            self.continuity();self.file_set();self.native_protocol(after=True)
            if self.unit('munin-node.service')['ActiveState']!='active':raise ValueError('master node stopped before commit')
            self.state.update(phase='committed',accepted=True);self.save()
            return self.state

        def recover(self):
            if self.state.get('phase') in ('committed','restored'):return self.state
            errors=[]
            try:
                self.continuity()
                current=base.secure(CONFIG)[0]
                if base.sha(current)==self.spec['candidate_sha256'] and self.state.get('config_intent'):
                    m=CONFIG.lstat()
                    if [m.st_dev,m.st_ino]!=self.state.get('config_identity'):
                        raise ValueError('foreign master config inode; restoration held')
                    backup=base.secure(self.root/'config.before')[0]
                    if base.sha(backup)!=self.spec['before_sha256']:raise ValueError('baseline backup drift')
                    publication=self.root/'config-restoration'
                    if publication.exists() and base.sha(base.secure(publication)[0])!=self.spec['before_sha256']:
                        raise ValueError('foreign restoration publication')
                    base.atomic(publication,backup,0o644)
                    os.replace(publication,CONFIG);sync(CONFIG.parent);sync(self.root)
                elif base.sha(current)!=self.spec['before_sha256']:
                    raise ValueError('foreign master configuration; restoration held')
                if os.path.lexists(LINK):
                    m=LINK.lstat()
                    if (not LINK.is_symlink() or os.readlink(LINK)!=str(PLUGIN)
                            or self.state.get('link_identity')!=[m.st_dev,m.st_ino]):
                        raise ValueError('foreign plugin link; restoration held')
                    LINK.unlink()
                    sync(LINK.parent)
                for row in reversed(self.state['changes']):
                    path=Path(row['path'])
                    if not os.path.lexists(path):continue
                    m=path.lstat()
                    if ([m.st_dev,m.st_ino]!=[row['device'],row['inode']]
                            or base.sha(base.secure(path)[0])!=row['sha256']):
                        raise ValueError('foreign authored destination; restoration held')
                    path.unlink()
                    sync(path.parent)
                self.parser(base.secure(CONFIG)[0])
                if self.state.get('node_restart_intent'):
                    self.ctl('restart','munin-node.service')
                if self.state.get('config_intent'):self.refresh_cgi()
                self.file_set(candidate=False)
                if self.native_protocol()!=self.state['protocol_before']:
                    raise ValueError('restored native node protocol drift')
                if self.unit('munin-node.service')['ActiveState']!='active':raise ValueError('restored node not running')
            except BaseException as error:errors.append(str(error))
            self.state.update(accepted=False,recovery_errors=errors,
                recovery='held' if errors else 'restored',phase='recovery-held' if errors else 'restored')
            self.save();return self.state

    return Installer
