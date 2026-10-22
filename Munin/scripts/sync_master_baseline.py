#!/usr/bin/python3
"""Compare/import exact master bytes from an approved successful private capture."""
import argparse
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import tarfile
import tempfile

TARGET = Path(__file__).resolve().parents[1]/'master/configs/munin.conf'
LIMIT = 16*1048576


def read_private(path, limit=LIMIT):
    if any(p.is_symlink() for p in (path,*path.parents)):
        raise ValueError('indirect private input')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,'rb') as stream:
        before=os.fstat(stream.fileno())
        if (not stat.S_ISREG(before.st_mode) or before.st_uid!=os.getuid()
                or stat.S_IMODE(before.st_mode)!=0o600 or before.st_size>limit):
            raise ValueError('bounded owner-private regular input required')
        raw=stream.read(limit+1); after=os.fstat(stream.fileno())
    if len(raw)>limit or (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):
        raise ValueError('private input changed or exceeded bound')
    return raw


def captured_baseline(directory, digest):
    info=directory.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid!=os.getuid() or stat.S_IMODE(info.st_mode)!=0o700:
        raise ValueError('owner-private capture directory required')
    raw=read_private(directory/'inspection.tar',8*1048576)
    if hashlib.sha256(raw).hexdigest()!=digest:
        raise ValueError('approved archive mismatch')
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        members=archive.getmembers()
        if (len({m.name for m in members})!=len(members)
                or any(not m.isfile() or m.size>1048576 for m in members)):
            raise ValueError('regular bounded unique archive members required')
        member=archive.getmember('spec.json')
        spec=json.loads(archive.extractfile(member).read())
    receipt=json.loads(read_private(directory/'execution.json'))
    result=json.loads(read_private(directory/'result.json'))
    capture=json.loads(read_private(directory/'stdout.txt'))
    spec_hash=hashlib.sha256((json.dumps(spec,sort_keys=True)+'\n').encode()).hexdigest()
    if (spec.get('mode')!='master-baseline' or spec.get('endpoint')!='10.1.3.83'
            or spec.get('hostname')!='J1-SVMF' or receipt.get('sha256')!=digest
            or result.get('bundle_sha256')!=digest or result.get('returncode')!=0
            or not result.get('capture_complete') or not capture.get('capture_complete')
            or capture.get('operation_id')!=spec.get('operation_id')
            or capture.get('spec_sha256')!=spec_hash or capture.get('error')):
        raise ValueError('successful approved master-baseline capture required')
    snapshot=capture['master_qualification']['production_baseline']
    raw=base64.b64decode(snapshot['base64'],validate=True)
    if (not raw or len(raw)>65536 or snapshot['path']!='/etc/munin/munin.conf'
            or hashlib.sha256(raw).hexdigest()!=spec['production_baseline_sha256']
            or snapshot['sha256']!=spec['production_baseline_sha256']):
        raise ValueError('production bytes/hash mismatch')
    return raw


def synchronize(raw, target, write=False, expected_before=None):
    if any(p.is_symlink() for p in (target,*target.parents)):
        raise ValueError('indirect repository destination')
    info=target.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_uid!=os.getuid() or info.st_nlink!=1:
        raise ValueError('owned single-link repository file required')
    before=target.read_bytes()
    if before==raw:
        return True
    if expected_before is not None and before!=expected_before:
        raise ValueError('repository differs from approved baseline; no overwrite')
    if not write:
        return False
    # Scan the exact byte payload privately before it enters a tracked location.
    with tempfile.TemporaryDirectory(prefix='munin-baseline-scan-') as tmp:
        scratch=Path(tmp); scratch.chmod(0o700)
        sample=scratch/'munin.conf'; sample.write_bytes(raw); sample.chmod(0o600)
        scanned=subprocess.run(['gitleaks','detect','--source',str(scratch),'--no-git',
            '--redact','--no-banner'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
        if scanned.returncode!=0:
            raise ValueError('exact production payload secret scan failed; repository unchanged')
    fd,name=tempfile.mkstemp(prefix='.munin-baseline-',dir=target.parent)
    try:
        with os.fdopen(fd,'wb') as stream:
            os.fchmod(stream.fileno(),stat.S_IMODE(info.st_mode))
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        current=target.lstat()
        if (current.st_dev,current.st_ino)!=(info.st_dev,info.st_ino) or target.read_bytes()!=before:
            raise ValueError('repository changed during import; no overwrite')
        os.replace(name,target)
        directory_fd=os.open(target.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:os.fsync(directory_fd)
        finally:os.close(directory_fd)
    finally:
        if os.path.exists(name):os.unlink(name)
    if target.read_bytes()!=raw:
        raise ValueError('repository import readback mismatch')
    return True


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('check','import'))
    parser.add_argument('--directory',type=Path,required=True)
    parser.add_argument('--sha256',required=True)
    args=parser.parse_args()
    raw=captured_baseline(args.directory,args.sha256)
    matched=synchronize(raw,TARGET,write=args.action=='import')
    print(json.dumps({'matches_production_capture':matched,'sha256':hashlib.sha256(raw).hexdigest(),
                      'target_contact':False,'destination':str(TARGET)}))
    if not matched:raise SystemExit(2)


if __name__=='__main__':main()
