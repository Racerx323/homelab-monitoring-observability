#!/usr/bin/python3
"""Opt-in real-package first-start/recovery fixture; isolated systemd container only."""
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time

ROOT=Path('/var/lib/munin-first-start-qualification')
PERMIT=ROOT/'permit'
POLICY=Path('/usr/sbin/policy-rc.d')
GUARD=Path('/etc/systemd/system/munin-node.service.d/00-qualification.conf')
GUARD_BYTES=b'[Unit]\nConditionPathExists=/var/lib/munin-first-start-qualification/permit\n'
CONFIG=Path('/etc/munin/munin-node.conf')
CONFIG_BYTES=b'''log_level 4
log_file /var/log/munin/munin-node.log
pid_file /run/munin/munin-node.pid
background 1
setsid 1
user root
group root
host_name fixture-node
host 127.0.0.1
port 4949
allow ^127\\.0\\.0\\.1$
'''


def sha(raw):return hashlib.sha256(raw).hexdigest()


class Fixture:
    def __init__(self,scenario):
        self.scenario=scenario
        self.state={'scenario':scenario,'passed':False,'commands':[],'checks':{},'recovery':'not-needed'}
        self.policy_before=None
        self.policy_wrapper=None
        self.wrapper_installed=False

    def cmd(self,args,allowed=(0,),env=None):
        p=subprocess.run(args,capture_output=True,text=True,timeout=40,env=env)
        self.state['commands'].append({'argv':args,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
        if p.returncode not in allowed:raise RuntimeError('command failed: '+repr(args)+'\n'+p.stderr)
        return p.stdout

    def ctl(self,*args,allowed=(0,)):return self.cmd(['/usr/bin/systemctl',*args],allowed)

    def identity(self):
        text=self.ctl('show','timeservice-fixture.service','--property=MainPID,InvocationID,NRestarts,ActiveState,SubState')
        return dict(line.split('=',1) for line in text.splitlines())

    def connected(self):
        try:
            with socket.create_connection(('127.0.0.1',4949),timeout=.5):return True
        except OSError:return False

    def restore_policy(self):
        if not self.wrapper_installed:return
        if POLICY.is_symlink() or POLICY.read_bytes()!=self.policy_wrapper:
            raise RuntimeError('foreign policy; restoration held')
        POLICY.write_bytes(self.policy_before);POLICY.chmod(0o755);self.wrapper_installed=False

    def recover(self):
        self.ctl('stop','munin-node.service',allowed=(0,5))
        PERMIT.unlink(missing_ok=True)
        failures=[]
        try:self.restore_policy()
        except Exception as e:failures.append(str(e))
        if GUARD.read_bytes()!=GUARD_BYTES:failures.append('foreign guard; restoration held')
        self.ctl('daemon-reload')
        assert not self.connected(),'recovery left a listener'
        assert self.identity()==self.before,'unrelated service identity changed'
        self.state['recovery']='held' if failures else 'contained'
        self.state['recovery_errors']=failures

    def setup(self):
        assert Path('/run/.containerenv').exists(),'container required'
        assert Path('/proc/1/comm').read_text().strip()=='systemd','systemd PID 1 required'
        assert not ROOT.exists(),'single-use fixture required'
        ROOT.mkdir(mode=0o700)
        self.state['architecture']=self.cmd(['/usr/bin/dpkg','--print-architecture']).strip()
        self.state['systemd']=self.ctl('--version').splitlines()[0]
        unit=Path('/etc/systemd/system/timeservice-fixture.service')
        unit.write_text('[Service]\nExecStart=/bin/sleep infinity\n')
        self.ctl('daemon-reload');self.ctl('start','timeservice-fixture.service');self.before=self.identity()
        # A pre-existing fixture policy tests restoration and delegation, not just absence.
        POLICY.write_text('#!/bin/sh\ncase "$1" in fixture-unrelated) exit 42;; *) exit 0;; esac\n');POLICY.chmod(0o755)
        self.policy_before=POLICY.read_bytes()
        backup=ROOT/'original-policy';backup.write_bytes(self.policy_before);backup.chmod(0o700)
        self.policy_wrapper=(f'#!/bin/sh\ncase "$1" in munin-node|munin-node.service) exit 101;; esac\nexec {backup} "$@"\n').encode()
        POLICY.write_bytes(self.policy_wrapper);POLICY.chmod(0o755);self.wrapper_installed=True
        GUARD.parent.mkdir(parents=True);GUARD.write_bytes(GUARD_BYTES);GUARD.chmod(0o644)
        CONFIG.parent.mkdir(parents=True,exist_ok=True);CONFIG.write_bytes(CONFIG_BYTES);CONFIG.chmod(0o644)
        bindir=ROOT/'guard-bin';bindir.mkdir(mode=0o700)
        shim=bindir/'munin-node-configure'
        shim.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> /var/lib/munin-first-start-qualification/autoconf-calls\nexit 0\n');shim.chmod(0o700)
        self.env={'PATH':str(bindir)+':/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
                  'LC_ALL':'C','DEBIAN_FRONTEND':'noninteractive'}
        self.ctl('daemon-reload')
        self.cmd([str(POLICY),'munin-node','start'],allowed=(101,))
        self.cmd([str(POLICY),'fixture-unrelated','start'],allowed=(42,))
        self.state['checks']['policy_scope']=True

    def packages(self):
        manifest=json.loads(Path('/inputs/manifest.json').read_text())
        paths=[]
        for name in ('munin-common','munin-plugins-core','munin-node'):
            rows=[r for r in manifest['packages'] if r['package']==name]
            assert len(rows)==1 and rows[0]['architecture']=='all'
            p=Path('/inputs')/rows[0]['filename']
            assert sha(p.read_bytes())==rows[0]['sha256'],'package integrity'
            paths.append(str(p))
        return paths

    def fetch(self,command):
        with socket.create_connection(('127.0.0.1',4949),timeout=2) as s:
            s.settimeout(3);f=s.makefile('rb');greeting=f.readline()
            assert greeting.startswith(b'# munin node'),greeting
            s.sendall(command.encode()+b'\n');rows=[]
            for _ in range(500):
                line=f.readline()
                if line==b'.\n':break
                assert line,'unexpected close';rows.append(line)
            else:raise AssertionError('protocol bound')
            s.sendall(b'quit\n')
        return b''.join(rows).decode()

    def apply(self):
        self.setup();paths=self.packages()
        if self.scenario=='dpkg-failure':
            invalid=ROOT/'invalid.deb';invalid.write_bytes(b'intentionally invalid fixture')
            self.cmd(['/usr/bin/dpkg','--force-confdef','--force-confold','--install',paths[0],str(invalid)],allowed=(1,2),env=self.env)
            raise RuntimeError('injected real dpkg partial-install failure')
        self.cmd(['/usr/bin/dpkg','--force-confdef','--force-confold','--install',*paths],env=self.env)
        assert (ROOT/'autoconf-calls').read_text().splitlines()==['--shell'],'uncontrolled autoconf calls'
        assert not list(Path('/etc/munin/plugins').iterdir()),'automatic plugin links created'
        assert CONFIG.read_bytes()==CONFIG_BYTES,'package replaced restricted first-start config'
        assert not self.connected(),'package installation started listener'
        self.ctl('start','munin-node.service')
        assert not self.connected(),'condition guard allowed premature start'
        assert 'MainPID=0' in self.ctl('show','munin-node.service','--property=MainPID')
        self.state['checks']['blocked_first_start']=True
        self.state['checks']['autoconf_suppressed']=True
        assert self.identity()==self.before
        self.state['checks']['continuity']=True
        if self.scenario=='foreign-policy':
            POLICY.write_text('#!/bin/sh\nexit 17\n');raise RuntimeError('injected foreign policy edit')
        self.restore_policy()
        assert POLICY.read_bytes()==self.policy_before
        if self.scenario=='configuration-failure':raise RuntimeError('injected post-install configuration failure')
        settings=Path('/etc/munin/plugin-conf.d/qualification')
        settings.write_text('[load]\nuser nobody\ngroup nogroup\n')
        link=Path('/etc/munin/plugins/load');link.symlink_to('/usr/share/munin/plugins/load')
        PERMIT.touch(mode=0o600)
        self.ctl('daemon-reload');self.ctl('start','munin-node.service')
        deadline=time.monotonic()+10
        while not self.connected() and time.monotonic()<deadline:time.sleep(.1)
        assert self.connected(),'reviewed first start did not listen'
        listeners=self.cmd(['/usr/bin/ss','-lnt','sport = :4949'])
        assert '127.0.0.1:4949' in listeners and '0.0.0.0:4949' not in listeners and '*:4949' not in listeners,listeners
        assert 'graph_title Load average' in self.fetch('config load')
        assert 'load.value ' in self.fetch('fetch load')
        self.state['checks']['restricted_activation_and_fetch']=True
        assert self.identity()==self.before
        if self.scenario=='started-failure':raise RuntimeError('injected failure after real first start')
        self.state['passed']=True
        # Even successful qualification ends non-serving and retains all evidence.
        self.recover();assert self.state['recovery']=='contained'

    def run(self):
        try:self.apply()
        except Exception as e:
            self.state['error']=str(e)
            if hasattr(self,'before'):
                try:self.recover()
                except Exception as failure:self.state.update(recovery='held',recovery_error=str(failure))
            expected='held' if self.scenario=='foreign-policy' else 'contained'
            expected_error={'dpkg-failure':'injected real dpkg partial-install failure',
                            'configuration-failure':'injected post-install configuration failure',
                            'started-failure':'injected failure after real first start',
                            'foreign-policy':'injected foreign policy edit'}.get(self.scenario)
            if str(e)==expected_error and self.state['recovery']==expected:
                self.state['passed']=True
        finally:
            Path('/evidence/result.json').write_text(json.dumps(self.state,indent=2)+'\n')
        print(json.dumps({'scenario':self.scenario,'passed':self.state['passed'],'recovery':self.state['recovery']}),flush=True)
        if not self.state['passed']:raise SystemExit(1)


if __name__=='__main__':
    assert Path('/run/.containerenv').exists(),'container required'
    assert Path('/proc/1/comm').read_text().strip()=='systemd','systemd PID 1 required'
    assert sys.argv[1:] and sys.argv[1] in ('success','dpkg-failure','configuration-failure','started-failure','foreign-policy')
    Fixture(sys.argv[1]).run()
