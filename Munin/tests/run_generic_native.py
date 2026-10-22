#!/usr/bin/python3
"""Retain actual local native update/recovery qualification; never contact production."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent.parent
CASES = ('node-success', 'node-recover', 'node-worker-loss', 'node-foreign-link',
         'preflight-drift', 'master-success', 'master-controller-loss', 'master-foreign-file', 'master-foreign-proof', 'timing-success', 'timing-recover', 'timing-worker-loss',
         'timing-controller-loss', 'timing-foreign-file', 'timing-foreign-link',
         'timing-foreign-settings', 'timing-preflight-drift')
ARTIFACTS = {'compatible.py': ROOT/'master/plugins/ntp_transport_j2.compatible.candidate',
             'expanded.py': ROOT/'master/plugins/ntp_transport_j2.expanded.candidate',
             'settings-after': ROOT/'node/plugin-conf.d/ntp-expanded.candidate.conf',
             'timing-reader': ROOT/'node/plugins/ntp/ntp_metrics.py'}


def hashes(paths):
    return {n: hashlib.sha256(p.read_bytes()).hexdigest() for n, p in paths.items()}


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--cases', choices=CASES, nargs='+', default=list(CASES))
    args = parser.parse_args()
    args.evidence.mkdir(mode=0o700)
    spec = importlib.util.spec_from_file_location('deployment', ROOT/'scripts/deploy_generic.py')
    d = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(d)
    initial = hashes(d.SOURCES)
    artifacts = hashes(ARTIFACTS)
    data = WORKSPACE/'.local-evidence/homelab-ntp/current'
    packages = [data/'munin-generic-qualification-preparation-20261021-v1'/name for name in
                ('munin-common_2.0.76-5_all.deb', 'munin-node_2.0.76-5_all.deb')]
    packages += [data/'munin-generic-node-inventory-20261021-v1/package-source-review/munin-plugins-core_2.0.76-5_all.deb',
                 data/'munin-node-install-20261021-v3/packages/libio-multiplex-perl_1.16-3_all.deb']
    record = {'sources': initial, 'artifacts': artifacts, 'cases': args.cases,
              'environment': 'network none; read-only workspace; root-private evidence; native systemd',
              'package_hashes': hashes({str(p): p for p in packages})}
    (args.evidence/'invocation.json').write_text(json.dumps(record, indent=2)+'\n')

    def run(case):
        directory = args.evidence/case
        directory.mkdir(mode=0o700)
        node = case.startswith(('node','timing')) or case == 'preflight-drift'
        image = 'localhost/munin-ntp-install-validation:trixie' if node else 'localhost/munin-master-validation:bookworm'
        identity = subprocess.check_output(['podman', 'image', 'inspect', image, '--format', '{{.Id}}'], text=True).strip()
        name = 'munin-generic-'+case+'-'+str(int(time.time()))
        create = ['podman', 'run', '--pull=never', '-d', '--name', name, '--network=none', '--systemd=always',
                  '--cap-add=SYS_ADMIN', '--volume', str(WORKSPACE)+':/workspace:ro',
                  '--volume', str(directory.absolute())+':/evidence:rw', identity]
        execute = ['podman', 'exec', name, '/usr/bin/python3', '-I', '-B',
                   '/workspace/homelab-monitoring-observability/Munin/tests/test_generic_update_native.py', case]
        if node:
            execute += ['/workspace/'+str(p.relative_to(WORKSPACE)) for p in packages]
        before = hashes(d.SOURCES)
        invocation = dict(record, image=image, image_id=identity, create=create, execute=execute,
                          source_hashes_before=before, epoch=time.time(), log=str(directory/'native.log'))
        (directory/'invocation.json').write_text(json.dumps(invocation, indent=2)+'\n')
        with (directory/'native.log').open('xb') as log:
            started = subprocess.run(create, stdout=subprocess.PIPE, stderr=log, text=True)
            log.write(started.stdout.encode())
            log.flush()
            (directory/'container.id').write_text(started.stdout)
            code = started.returncode
            if code == 0:
                deadline = time.monotonic()+40
                while time.monotonic() < deadline:
                    ready = subprocess.run(['podman', 'exec', name, 'test', '-S', '/run/systemd/private'], stdout=log, stderr=log)
                    if ready.returncode == 0:
                        break
                    time.sleep(.5)
                try:
                    code = subprocess.run(execute, stdout=log, stderr=subprocess.STDOUT, timeout=150).returncode
                except subprocess.TimeoutExpired:
                    code = 124
        after = hashes(d.SOURCES)
        native = json.loads((directory/'result.json').read_text()) if code == 0 else {}
        passed = code == 0 and native.get('passed') is True and before == after == initial and hashes(ARTIFACTS) == artifacts
        result = {'case': case, 'exit_code': code, 'passed': passed, 'container': name,
                  'source_hashes_after': after, 'source_inputs_unchanged': before == after == initial,
                  'log': str(directory/'native.log'), 'finished_epoch': time.time()}
        (directory/'status.json').write_text(json.dumps(result, indent=2)+'\n')
        if passed:
            subprocess.run(['podman', 'stop', '--time', '10', name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, check=True)
        print(json.dumps({'case': case, 'passed': passed, 'log': str(directory/'native.log')}), flush=True)
        return result

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run, args.cases))
    passed = set(args.cases) == set(CASES) and all(x['passed'] for x in results)
    summary = dict(record, passed=passed, cases=results, production_timing_or_hardware_accepted=False)
    (args.evidence/'qualification.json').write_text(json.dumps(summary, indent=2)+'\n')
    if not passed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
