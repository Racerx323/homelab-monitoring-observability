#!/usr/bin/python3
"""Explicit local Podman qualification; retains each invocation, input hash and log."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import time

ROOT=Path(__file__).resolve().parents[1]
WORKSPACE=ROOT.parents[1]


def hashes():
    spec=importlib.util.spec_from_file_location('master',ROOT/'scripts/deploy_ntp_master.py')
    r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
    paths={**r.SOURCES,'plugin':ROOT/'master/plugins/ntp_transport_j2',
        'settings':ROOT/'master/configs/ntp-transport.plugin-conf.example'}
    return {n:hashlib.sha256(p.read_bytes()).hexdigest() for n,p in paths.items()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence',type=Path,required=True)
    parser.add_argument('--cases',nargs='+',required=True)
    parser.add_argument('--image',default='localhost/munin-master-validation:bookworm')
    args=parser.parse_args();os.umask(0o077)
    args.evidence.mkdir(mode=0o700)
    image=subprocess.check_output(['podman','image','inspect',args.image,'--format','{{.Id}}'],text=True).strip()
    results=[];native_hashes=None
    for case in args.cases:
        if case not in ('success','configured-failure','prepared-failure','foreign-config','foreign-link','preflight-drift','worker-loss','controller-loss','health-reject'):
            raise ValueError('unknown native case')
        directory=args.evidence/case;directory.mkdir(mode=0o700)
        name='munin-master-'+case+'-'+str(int(time.time()))
        run=['podman','run','--pull=never','-d','--name',name,'--network=none','--systemd=always',
            '--cap-add=NET_ADMIN','--cap-add=SYS_ADMIN','--volume',str(WORKSPACE)+':/workspace:ro',
            '--volume',str(directory)+':/evidence:rw',args.image]
        execute=['podman','exec',name,'/usr/bin/python3','-I','-B',
            '/workspace/homelab-monitoring-observability/Munin/tests/test_master_native.py',case]
        before=hashes()
        record={'run':run,'execute':execute,'image':image,'source_hashes':before,
            'environment':'inherited; network none; read-only workspace','epoch':time.time(),
            'log':str(directory/'native.log'),'next_checkpoint_seconds':30}
        (directory/'invocation.json').write_text(json.dumps(record,indent=2)+'\n')
        with (directory/'native.log').open('xb') as log:
            created=subprocess.run(run,stdout=subprocess.PIPE,stderr=log,text=True)
            log.write(created.stdout.encode());log.flush()
            if created.returncode:raise RuntimeError('container create failed; inspect retained log')
            (directory/'container.id').write_text(created.stdout)
            deadline=time.monotonic()+30
            while time.monotonic()<deadline:
                ready=subprocess.run(['podman','exec',name,'test','-S','/run/systemd/private'],stdout=log,stderr=log)
                if ready.returncode==0:break
                time.sleep(.5)
            row=subprocess.run(execute,stdout=log,stderr=subprocess.STDOUT)
        after=hashes();passed=row.returncode==0 and before==after
        if passed:
            native=json.loads((directory/'result.json').read_text())['native_hashes']
            if native_hashes is None:native_hashes=native
            elif native_hashes!=native:passed=False
        status={'case':case,'returncode':row.returncode,'passed':passed,'source_hashes_after':after,
            'source_inputs_unchanged':before==after,'container':name,'completed_epoch':time.time()}
        (directory/'status.json').write_text(json.dumps(status,indent=2)+'\n');results.append(status)
        print(json.dumps({'case':case,'passed':passed,'log':str(directory/'native.log')}),flush=True)
        if passed:
            subprocess.run(['podman','stop','--time','10',name],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30,check=True)
        else:break
    summary={'passed':len(results)==len(args.cases) and all(x['passed'] for x in results),
        'sources':hashes(),'image':image,'native_hashes':native_hashes,'cases':results}
    (args.evidence/'qualification.json').write_text(json.dumps(summary,indent=2)+'\n')
    if not summary['passed']:raise SystemExit(1)


if __name__=='__main__':main()
