#!/usr/bin/python3
"""Fixed-route Munin contact; no command interpolation, credentials or retries."""
from email.message import EmailMessage
import json
import os
from pathlib import Path
import re
import smtplib
import stat
import sys
import tempfile
import time

STATUS=Path('/var/lib/munin/ntp-alerts/status.json')
GRAPHS={'cpu','load','memory','uptime','processes','ntp_health','ntp_timing',
        'ntp_free_bytes','ntp_free_inodes','ntp_storage_read','ntp_stats_bytes',
        'ntp_stats_growth','ntp_stats_age','ntp_stats_read','ntp_job_evidence','ntp_job_age'}


def message(raw):
    if len(raw)>16384:raise ValueError('alert input bound')
    rows=raw.decode('ascii').strip().split('|')
    if len(rows)!=6:raise ValueError('six fixed alert fields required')
    state,host,plugin,warnings,criticals,unknowns=rows;state=state.upper()
    if state not in ('OK','WARNING','CRITICAL','UNKNOWN'):raise ValueError('unknown alert state')
    if host not in ('j2-svntp1','J1-SVMF') or not re.fullmatch(r'[A-Za-z0-9_]{1,96}',plugin):raise ValueError('unreviewed alert origin')
    if host=='J1-SVMF' and plugin!='ntp_transport_j2':raise ValueError('unreviewed master alert')
    if host=='j2-svntp1' and plugin not in GRAPHS:raise ValueError('unreviewed node graph')
    if any(not re.fullmatch(r'[A-Za-z0-9_ ]{0,2048}',x) for x in (warnings,criticals,unknowns)):raise ValueError('invalid field names')
    msg=EmailMessage();msg['From']='munin@local.theama.co'
    msg['To']='notify@mailrise.xyz' if state=='OK' else 'notify.failure@mailrise.xyz'
    msg['Subject']=f'Munin {state}: {host}/{plugin}'
    msg.set_content(f'Munin state: {state}\nHost: {host}\nPlugin: {plugin}\nWarning fields: {warnings or "none"}\nCritical fields: {criticals or "none"}\nUnknown fields: {unknowns or "none"}\nOperator: Aaron\nSMTP submission does not establish downstream delivery.\n')
    return msg


def save_status(ok,path=STATUS):
    directory=path.parent;m=directory.lstat()
    if any(p.is_symlink() for p in (directory,*directory.parents)) or not stat.S_ISDIR(m.st_mode) or m.st_uid!=os.geteuid() or stat.S_IMODE(m.st_mode)!=0o700:
        raise ValueError('private alert-state directory required')
    if os.path.lexists(path):
        m=path.lstat()
        if not stat.S_ISREG(m.st_mode) or m.st_uid!=os.geteuid() or m.st_nlink!=1 or stat.S_IMODE(m.st_mode)!=0o600:raise ValueError('unsafe alert status')
    fd,tmp=tempfile.mkstemp(prefix='.submission-',dir=directory)
    try:
        with os.fdopen(fd,'w') as f:
            os.fchmod(f.fileno(),0o600);json.dump({'schema':1,'submission_ok':ok,'attempt_epoch':time.time()},f);f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
        fd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:os.fsync(fd)
        finally:os.close(fd)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)


def deliver(msg,smtp=smtplib.SMTP):
    # The installed Mailrise loopback port was established by the accepted network stage.
    with smtp('127.0.0.1',8025,timeout=10) as connection:
        refused=connection.send_message(msg)
        if refused:raise RuntimeError('Mailrise recipient refused')


def main():
    if len(sys.argv)!=1:raise SystemExit('no arguments supported')
    try:
        msg=message(sys.stdin.buffer.read(16385))
        deliver(msg)
    except Exception as error:
        try:save_status(False)
        except Exception as failure:print('Alert-state write failed: '+str(failure),file=sys.stderr)
        print('Munin alert submission failed: '+str(error),file=sys.stderr)
        raise SystemExit(1)
    save_status(True)


if __name__=='__main__':main()
