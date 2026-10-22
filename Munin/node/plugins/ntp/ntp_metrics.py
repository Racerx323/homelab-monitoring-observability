"""Fixed-scope NTP metrics; no environment-selected paths or raw log reads."""
import json
import math
import os
from pathlib import Path
import re
import stat
import subprocess
import time

STREAMS=('loopstats','peerstats','clockstats','protostats')
JOB_PATHS={'retention':Path('/var/lib/ntpstats-retention/last-success.json'),
           'reporting':Path('/var/lib/needrestart-reporting/last-success.json')}
TIME_FIELDS=('query_ok','synced','pps_selected','reach','stratum','leap',
             'system_offset','system_jitter','selected_offset','selected_jitter')
TIMING_HEALTH_FIELDS=('selected_offset_ok','selected_jitter_ok')


def finite(value):
    value=float(value)
    if not math.isfinite(value):raise ValueError('non-finite metric')
    return value


def parse_ntpq(text):
    values={}
    for name in ('leap','stratum','offset','sys_jitter'):
        matches=re.findall(r'(?:^|[,\n ])'+name+r'\s*=\s*([^,\n]+)',text)
        if len(matches)!=1:raise ValueError('missing or duplicate system variable')
        values[name]=matches[0].strip()
    peers=[line.split() for line in text.splitlines() if line.startswith(('*','o'))]
    if len(peers)!=1 or len(peers[0])!=10:raise ValueError('one selected peer required')
    peer=peers[0];reach=int(peer[6],8);stratum=int(values['stratum']);leap=int(values['leap'],2)
    if not 0<=reach<=255 or not 0<=stratum<=16 or not 0<=leap<=3:raise ValueError('NTP field range')
    # GPSD's accepted SHM(2)/PPS association is an ordinary '*' system peer.
    # Keep native 'o' PPS support, but never classify a network refid as PPS.
    remote=peer[0][1:]
    native_pps=peer[0].startswith('o') and bool(re.fullmatch(r'(?:PPS\([0-9]+\)|127\.127\.22\.[0-9]+)',remote))
    pps=(peer[1]=='.PPS.' and peer[2]=='0' and peer[3]=='l' and
         (native_pps or remote in ('SHM(2)','127.127.28.2')))
    result={'query_ok':1,'synced':int(leap!=3 and 1<=stratum<=15 and reach>0),
            'pps_selected':int(pps),'reach':reach,'stratum':stratum,'leap':leap,
            'system_offset':finite(values['offset'])/1000,'system_jitter':finite(values['sys_jitter'])/1000,
            'selected_offset':finite(peer[8])/1000,'selected_jitter':finite(peer[9])/1000}
    if result['system_jitter']<0 or result['selected_jitter']<0:raise ValueError('negative jitter')
    # Native Munin 2.0.73 rounds values to two decimals before limits evaluation.
    # Evaluate timing policy here, retaining full-precision seconds for plotting.
    result['selected_offset_ok']=int(abs(result['selected_offset'])<=0.005)
    result['selected_jitter_ok']=int(result['selected_jitter']<=0.001)
    return result


def time_metrics():
    try:
        p=subprocess.run(['/usr/local/bin/ntpq','-n','-c','rv 0 leap,stratum,offset,sys_jitter',
                          '-c','peers','127.0.0.1'],capture_output=True,text=True,timeout=8,
                         env={'PATH':'/usr/bin:/bin','LC_ALL':'C'})
        if p.returncode or len(p.stdout)>65536:raise ValueError('query failure')
        return parse_ntpq(p.stdout)
    except (OSError,ValueError,subprocess.SubprocessError):
        return dict.fromkeys(TIME_FIELDS+TIMING_HEALTH_FIELDS,'U')|{'query_ok':0}


def storage_metrics(paths=('/', '/var/log/ntpstats'),statvfs=os.statvfs):
    result={}
    for label,path in zip(('root','stats'),paths):
        try:
            fs=statvfs(path)
            if fs.f_files<=0 or not 0<=fs.f_favail<=fs.f_files or fs.f_bavail<0 or fs.f_frsize<=0:
                raise ValueError('filesystem counters unavailable')
            result.update({label+'_bytes':fs.f_bavail*fs.f_frsize,
                           label+'_inodes':100*fs.f_favail/fs.f_files,label+'_ok':1})
        except (OSError,ValueError):result.update({label+'_bytes':'U',label+'_inodes':'U',label+'_ok':0})
    return result


def statistics_metrics(path=Path('/var/log/ntpstats'),now=None):
    now=time.time() if now is None else now
    totals=dict.fromkeys(STREAMS,0);latest=dict.fromkeys(STREAMS,None);seen={}
    try:
        if path.is_symlink():raise ValueError('indirect statistics directory')
        with os.scandir(path) as entries:
            for index,entry in enumerate(entries):
                if index>=4096:raise ValueError('directory bound')
                match=re.fullmatch(r'(loopstats|peerstats|clockstats|protostats)(?:\.\d{8}(?:\.gz)?)?',entry.name)
                if not match:continue
                info=entry.stat(follow_symlinks=False)
                if not stat.S_ISREG(info.st_mode) or info.st_mtime>now+60:raise ValueError('invalid statistics metadata')
                stream=match[1];identity=(info.st_dev,info.st_ino)
                if identity in seen:
                    if seen[identity]!=stream:raise ValueError('cross-stream hardlink')
                    continue
                seen[identity]=stream;totals[stream]+=info.st_size
                latest[stream]=max(latest[stream] or info.st_mtime,info.st_mtime)
        ages={name:max(0,now-latest[name]) if latest[name] is not None else 'U' for name in STREAMS}
        return {'ok':1,'bytes':totals,'age':ages}
    except (OSError,ValueError):return {'ok':0,'bytes':dict.fromkeys(STREAMS,'U'),'age':dict.fromkeys(STREAMS,'U')}


def job_metrics(paths=JOB_PATHS,now=None):
    now=time.time() if now is None else now;result={}
    for job,path in paths.items():
        try:
            if any(p.is_symlink() for p in (path,*path.parents)):raise ValueError('indirect heartbeat')
            fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
            with os.fdopen(fd,'rb') as stream:
                info=os.fstat(stream.fileno())
                if not stat.S_ISREG(info.st_mode) or info.st_uid!=0 or info.st_mode&0o077 or info.st_size>4096:
                    raise ValueError('heartbeat ownership/type/size')
                raw=stream.read(4097)
            if len(raw)>4096:raise ValueError('heartbeat bound')
            d=json.loads(raw)
            if d.get('schema')!=1 or d.get('job')!=job or d.get('status')!='success':raise ValueError('heartbeat schema')
            completed=finite(d['completed_epoch'])
            if completed<=0 or completed>now+60:raise ValueError('heartbeat time')
            result.update({job+'_evidence':1,job+'_age':max(0,now-completed)})
        except (OSError,ValueError,KeyError,TypeError):result.update({job+'_evidence':0,job+'_age':'U'})
    return result


def graph(name,title,label,fields):
    lines=['multigraph '+name,'graph_title '+title,'graph_category ntp','graph_vlabel '+label]
    for field,description,critical,kind in fields:
        lines.extend((field+'.label '+description,field+'.type '+kind))
        if critical:lines.append(field+'.critical '+critical)
        if kind=='DERIVE':lines.append(field+'.min 0')
    return lines


def config(kind):
    if kind=='health':
        status=[('query_ok','Query succeeded','1:1','GAUGE'),('synced','Synchronized','1:1','GAUGE'),
                ('pps_selected','PPS selected','1:1','GAUGE'),('reach','Selected reach','1:255','GAUGE'),
                ('stratum','Stratum','1:15','GAUGE'),('leap','Leap state','0:2','GAUGE'),
                ('selected_offset_ok','Selected offset within 5 ms','1:1','GAUGE'),
                ('selected_jitter_ok','Selected jitter within 1 ms','1:1','GAUGE')]
        offset=[(name,name.replace('_',' '),None,'GAUGE') for name in TIME_FIELDS[6:]]
        return graph('ntp_health','NTP source health','state',status)+graph('ntp_timing','NTP timing','seconds',offset)
    if kind=='storage':
        return (graph('ntp_free_bytes','NTP filesystems available bytes','bytes',[(n+'_bytes',n+' available','10737418240:','GAUGE') for n in ('root','stats')])+
                graph('ntp_free_inodes','NTP filesystems available inodes','percent',[(n+'_inodes',n+' free','5:','GAUGE') for n in ('root','stats')])+
                graph('ntp_storage_read','NTP filesystem collection','state',[(n+'_ok',n+' collection','1:1','GAUGE') for n in ('root','stats')]))
    if kind=='statistics':
        return (graph('ntp_stats_bytes','NTP statistics unique storage','bytes',[(n,n,None,'GAUGE') for n in STREAMS])+
                graph('ntp_stats_growth','NTP statistics positive net growth','bytes / second',[(n,n,None,'DERIVE') for n in STREAMS])+
                graph('ntp_stats_age','NTP statistics newest modification','seconds',[(n,n,'0:3600' if n!='protostats' else None,'GAUGE') for n in STREAMS])+
                graph('ntp_stats_read','NTP metadata collection','state',[('ok','Metadata readable','1:1','GAUGE')]))
    if kind=='jobs':
        return (graph('ntp_job_evidence','NTP maintenance success evidence','state',[(n+'_evidence',n+' evidence','1:1','GAUGE') for n in JOB_PATHS])+
                graph('ntp_job_age','NTP maintenance last success','seconds',[(n+'_age',n+' age','0:172800','GAUGE') for n in JOB_PATHS]))
    raise ValueError('unsupported metric')


def values(name,fields):return ['multigraph '+name]+[key+'.value '+str(value) for key,value in fields.items()]


def fetch(kind):
    if kind=='health':
        d=time_metrics();return values('ntp_health',{k:d[k] for k in TIME_FIELDS[:6]+TIMING_HEALTH_FIELDS})+values('ntp_timing',{k:d[k] for k in TIME_FIELDS[6:]})
    if kind=='storage':
        d=storage_metrics();return sum((values(name,{k:v for k,v in d.items() if k.endswith(suffix)}) for name,suffix in
                                     (('ntp_free_bytes','_bytes'),('ntp_free_inodes','_inodes'),('ntp_storage_read','_ok'))),[])
    if kind=='statistics':
        d=statistics_metrics();return values('ntp_stats_bytes',d['bytes'])+values('ntp_stats_growth',d['bytes'])+values('ntp_stats_age',d['age'])+values('ntp_stats_read',{'ok':d['ok']})
    if kind=='jobs':
        d=job_metrics();return values('ntp_job_evidence',{k:v for k,v in d.items() if k.endswith('_evidence')})+values('ntp_job_age',{k:v for k,v in d.items() if k.endswith('_age')})
    raise ValueError('unsupported metric')


def main(kind,args):
    if args not in ([],['config']):raise SystemExit('only config or fetch is supported')
    print('\n'.join(config(kind) if args else fetch(kind)))
