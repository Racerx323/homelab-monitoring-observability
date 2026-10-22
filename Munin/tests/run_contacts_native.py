#!/usr/bin/python3
"""Retain isolated native contact qualification; run outside the filesystem sandbox."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent.parent
CASES = ('success', 'restore', 'rejection', 'worker-loss', 'controller-loss',
         'foreign-config', 'foreign-helper', 'foreign-state', 'preflight-drift', 'commit-loss', 'ambiguous-send',
         'publication-loss', 'suppressed-call', 'proof-preflight-drift',
         'proof-foreign-recovery', 'unexpected-main-link')


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--cases', nargs='+', choices=CASES, default=list(CASES))
    args = parser.parse_args()
    args.evidence.mkdir(mode=0o700)
    spec = importlib.util.spec_from_file_location('contacts', ROOT/'scripts/review_ntp_contacts.py')
    d = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(d)
    hashes = lambda: {n: d.sha(p.read_bytes()) for n, p in d.SOURCES.items()}
    before = hashes()
    image = subprocess.check_output(['podman', 'image', 'inspect', 'localhost/munin-master-validation:bookworm', '--format', '{{.Id}}'], text=True).strip()
    results = []
    native = None
    for case in args.cases:
        directory = args.evidence/case
        directory.mkdir(mode=0o700)
        name = 'munin-contacts-' + case + '-' + str(int(time.time()))
        create = ['podman', 'run', '--pull=never', '-d', '--name', name, '--network=none',
                  '--systemd=always', '--cap-add=SYS_ADMIN', '--volume', str(WORKSPACE)+':/workspace:ro',
                  '--volume', str(directory.absolute())+':/evidence:rw', image]
        execute = ['podman', 'exec', name, '/usr/bin/python3', '-I', '-B',
                   '/workspace/homelab-monitoring-observability/Munin/tests/test_contacts_native.py', case]
        record = {'case': case, 'create': create, 'execute': execute, 'image_id': image,
                  'sources': before, 'environment': 'inherited; network none; workspace read only',
                  'log': str(directory/'native.log'), 'started_epoch': time.time(), 'next_checkpoint_seconds': 30}
        (directory/'invocation.json').write_text(json.dumps(record, indent=2)+'\n')
        with (directory/'native.log').open('xb') as log:
            started = subprocess.run(create, stdout=subprocess.PIPE, stderr=log, text=True)
            log.write(started.stdout.encode())
            log.flush()
            if started.returncode:
                raise RuntimeError('container create failed; retained private log')
            (directory/'container.id').write_text(started.stdout)
            deadline = time.monotonic()+30
            while time.monotonic() < deadline:
                if subprocess.run(['podman', 'exec', name, 'test', '-S', '/run/systemd/private'], stdout=log, stderr=log).returncode == 0:
                    break
                time.sleep(.5)
            row = subprocess.run(execute, stdout=log, stderr=subprocess.STDOUT)
        passed = row.returncode == 0 and before == hashes()
        if passed:
            observed = json.loads((directory/'result.json').read_text())['native_module_hashes']
            if native is None:
                native = observed
            elif observed != native:
                passed = False
        result = {'case': case, 'passed': passed, 'returncode': row.returncode, 'container': name,
                  'finished_epoch': time.time(), 'source_inputs_unchanged': before == hashes()}
        (directory/'status.json').write_text(json.dumps(result, indent=2)+'\n')
        results.append(result)
        print(json.dumps(result), flush=True)
        if not passed:
            break
        subprocess.run(['podman', 'stop', '--time', '10', name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    summary = {'passed': len(results) == len(args.cases) and all(x['passed'] for x in results),
               'sources': before, 'source_inputs_unchanged': before == hashes(), 'image_id': image,
               'native_module_hashes': native, 'cases': results}
    (args.evidence/'qualification.json').write_text(json.dumps(summary, indent=2)+'\n')
    if not summary['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
