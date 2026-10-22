"""Run only inside the isolated network=none systemd/Apache fixture container."""
import base64
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import signal
import socket
import subprocess
import sys
import tarfile
import time

SOURCE = Path('/repo/Apache2/scripts/deploy_acl.py')
LOADER = importlib.util.spec_from_file_location('acl', SOURCE)
d = importlib.util.module_from_spec(LOADER)
LOADER.loader.exec_module(d)
EVIDENCE = Path('/evidence')
TARGET = Path('/etc/apache2/sites-available/001-munin.theama.co-ssl.conf')
ADDRESSES = ['10.1.3.83', 'fd36:5aa8:6971:1:2cf5:3096:c5f:3283']
PATHS = ['/', '/static/style-new.css', '/munin-cgi/munin-cgi-graph/J1-SVMF/J1-SVMF/apache_accesses-day.png']


def cmd(argv):
    return subprocess.check_output(argv, stderr=subprocess.STDOUT, timeout=30).decode().strip()


def wait(check, seconds=25):
    deadline = time.monotonic()+seconds
    while time.monotonic() < deadline:
        value = check()
        if value:
            return value
        time.sleep(0.2)
    raise RuntimeError('native fixture deadline')


def setup():
    if os.geteuid() != 0 or not Path('/run/systemd/system').exists():
        raise ValueError('isolated root systemd fixture required')
    for address in (ADDRESSES[0]+'/32', ADDRESSES[1]+'/128'):
        cmd(['ip', 'address', 'add', address, 'dev', 'lo'])
    certdir = Path('/etc/ssl/local.theama.co')
    certdir.mkdir()
    cert = certdir/'STAR_local_theama_co.crt'
    key = certdir/'STAR_local_theama_co.key'
    cmd(['openssl', 'req', '-x509', '-nodes', '-newkey', 'rsa:2048', '-days', '2',
         '-keyout', str(key), '-out', str(cert), '-subj', '/CN=munin.local.theama.co',
         '-addext', 'subjectAltName=DNS:munin.local.theama.co'])
    (certdir/'STAR_local_theama_co.ca-bundle').write_bytes(cert.read_bytes())
    key.chmod(0o600)
    cmd(['a2enmod', 'ssl', 'rewrite', 'fcgid'])
    cmd(['a2dissite', '000-default'])
    Path('/var/cache/munin/www/static').mkdir(parents=True)
    Path('/var/cache/munin/www/static/style-new.css').write_text('body { color: black; }\n')
    Path('/etc/munin/static').mkdir(parents=True)
    scripts = Path('/usr/lib/munin/cgi')
    scripts.mkdir(parents=True)
    html = '<html><link href="/static/style-new.css"><img src="'+PATHS[-1]+'"></html>'
    png = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+a9mQAAAAASUVORK5CYII='
    for name, body in [('munin-cgi-html', 'print "Content-Type: text/html\\r\\n\\r\\n"; print '+json.dumps(html)+';'),
                       ('munin-cgi-graph', 'print "Content-Type: image/png\\r\\n\\r\\n"; print decode_base64("'+png+'");')]:
        path = scripts/name
        path.write_text('#!/usr/bin/perl\nuse FCGI; use MIME::Base64;\nmy $r = FCGI::Request();\nwhile ($r->Accept() >= 0) { '+body+' }\n')
        path.chmod(0o755)
    TARGET.write_bytes(Path('/baseline.conf').read_bytes())
    TARGET.chmod(0o644)
    Path('/etc/apache2/sites-enabled/001-munin.theama.co-ssl.conf').symlink_to(TARGET)
    cmd(['systemctl', 'start', 'apache2.service'])
    Path('/root/.ssh').mkdir(mode=0o700, exist_ok=True)
    cmd(['ssh-keygen', '-q', '-t', 'ed25519', '-N', '', '-f', '/root/.ssh/id_ed25519'])
    Path('/root/.ssh/authorized_keys').write_bytes(Path('/root/.ssh/id_ed25519.pub').read_bytes())
    Path('/etc/ssh/sshd_config.d/99-fixture.conf').write_text('PermitRootLogin prohibit-password\nPasswordAuthentication no\n')
    cmd(['systemctl', 'start', 'ssh.service'])
    # Fault injection delegates to the real package tools for every other command.
    for original in ('/usr/sbin/apache2ctl', '/usr/bin/systemctl'):
        path = Path(original)
        saved = Path('/usr/local/libexec')/(path.name+'-native')
        saved.parent.mkdir(exist_ok=True)
        saved.write_bytes(path.read_bytes())
        saved.chmod(0o755)
        kind = 'configtest' if path.name == 'apache2ctl' else 'reload'
        shim = ('#!/usr/bin/python3\nimport os,sys\nfrom pathlib import Path\n'
                'os.environ["APACHE_CONFDIR"]="/etc/apache2"\n'
                'os.environ["APACHE_ENVVARS"]="/etc/apache2/envvars"\n'
                'marker=Path("/run/acl-fail-'+kind+'")\n'
                'target=Path("'+str(TARGET)+'")\n'
                'if marker.exists() and '+repr(kind)+' in sys.argv[1:] and b"::1 fd36:" in target.read_bytes():\n'
                '    marker.unlink(); sys.exit(1)\n'
                'os.execv('+repr(str(saved))+', ['+repr(str(saved))+']+sys.argv[1:])\n')
        # apachectl is a symlink to apache2ctl; replacing the real path keeps that alias native.
        path.write_text(shim)
        path.chmod(0o755)


def bundle(case):
    old = Path('/baseline.conf').read_bytes()
    now = int(time.time())
    output = cmd(['apache2ctl', '-t', '-D', 'DUMP_INCLUDES'])
    paths = list(dict.fromkeys(re.findall(r'^\s*\([^\n)]{1,80}\)\s+(/etc/apache2/[^\s]{1,256})\s*$', output, re.M)))
    configs = [{'path': p, 'resolved': str(Path(p).resolve()), 'sha256': d.sha(Path(p).read_bytes())} for p in paths]
    cert = Path('/etc/ssl/local.theama.co/STAR_local_theama_co.crt').read_bytes()
    der = __import__('ssl').PEM_cert_to_DER_cert(cert.decode())
    key = b' '.join(Path('/etc/ssh/ssh_host_ed25519_key.pub').read_bytes().split()[:2])
    files = {'deploy_acl.py': SOURCE.read_bytes(), 'tls_probe.py': Path('/tls_probe.py').read_bytes(),
             'baseline.conf': old, 'candidate.conf': old.replace(d.OLD_RULE, d.NEW_RULE), 'ca.pem': cert,
             'known_hosts': b'svmf-acl-fixture '+key+b'\n'}
    spec = {'operation_id': 'svmf-apache-acl-fixture-'+case, 'prepared_epoch': now, 'expires_epoch': now+86400,
            'hostname': socket.gethostname(), 'boot_id': Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
            'user': 'root', 'host_key_alias': 'svmf-acl-fixture', 'addresses': ADDRESSES,
            'target': str(TARGET), 'paths': PATHS, 'leaf_sha256': d.sha(der),
            'confirm_seconds': 8, 'worker_seconds': 18, 'guard_seconds': 25,
            'service': d.service(), 'version_sha256': d.sha(d.command(['/usr/sbin/apache2ctl', '-v']).encode()),
            'configs': configs, 'baseline_sha256': d.sha(old), 'candidate_sha256': d.sha(files['candidate.conf']),
            'members': {n: d.sha(v) for n, v in files.items()}}
    files['spec.json'] = d.encoded(spec)
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w') as archive:
        for name, data in sorted(files.items()):
            item = tarfile.TarInfo(name)
            item.size = len(data)
            archive.addfile(item, io.BytesIO(data))
    raw = buffer.getvalue()
    digest = d.sha(raw)
    d.unpack(raw, digest)
    directory = EVIDENCE/case
    directory.mkdir(mode=0o700)
    for name, data in files.items():
        d.write(directory/name, data)
    d.write(directory/'deployment.tar', raw)
    return spec, files, directory, raw, digest


def main():
    setup()
    EVIDENCE.mkdir(exist_ok=True)
    results = []
    for case in ('commit', 'controller-loss', 'worker-loss', 'health-reject', 'configtest-failure', 'reload-failure', 'foreign-drift', 'preflight-drift'):
        TARGET.write_bytes(Path('/baseline.conf').read_bytes())
        TARGET.chmod(0o644)
        cmd(['systemctl', 'reload', 'apache2.service'])
        spec, files, directory, raw, digest = bundle(case)
        before = d.https_observations(spec, directory, files, True)
        assert before['passed'], before
        stage = d.STATE/spec['operation_id']
        state = lambda: json.loads((stage/'state.json').read_bytes()) if (stage/'state.json').exists() else {}
        if case == 'commit':
            with (directory/'controller.log').open('wb') as log:
                p = subprocess.run(['/usr/bin/python3', '-I', '-B', str(directory/'deploy_acl.py'), 'execute',
                                    '--directory', str(directory), '--sha256', digest], stdout=log, stderr=subprocess.STDOUT, timeout=70)
            assert p.returncode == 0, (directory/'controller.log').read_text()
            assert json.loads((directory/'result.json').read_bytes())['accepted']
        else:
            if case in ('configtest-failure', 'reload-failure'):
                Path('/run/acl-fail-'+('configtest' if case == 'configtest-failure' else 'reload')).touch()
            if case == 'preflight-drift':
                TARGET.write_bytes(TARGET.read_bytes()+b'\n# foreign preflight\n')
            d.install(raw, digest)
            if case in ('worker-loss', 'health-reject', 'foreign-drift'):
                wait(lambda: state().get('phase') == 'awaiting_confirmation')
                if case == 'worker-loss':
                    cmd(['systemctl', 'kill', '--signal=SIGKILL', spec['operation_id']+'.service'])
                else:
                    if case == 'foreign-drift':
                        TARGET.write_bytes(TARGET.read_bytes()+b'\n# foreign post-write\n')
                    d.action(stage, 'reject')
            wait(lambda: state().get('phase') in d.TERMINAL, 45)
        final = state()
        expected = 'committed' if case == 'commit' else 'recovery_held' if case == 'foreign-drift' else 'preflight_failed' if case == 'preflight-drift' else 'restored'
        assert final['phase'] == expected, final
        if expected in ('committed', 'restored'):
            observation = d.https_observations(spec, directory, files, expected == 'restored')
            assert observation['passed'], observation
            assert TARGET.read_bytes() == files['candidate.conf' if expected == 'committed' else 'baseline.conf']
            assert d.service() == spec['service']
            assert TARGET.stat().st_mode & 0o777 == 0o644
            d.write(directory/'peer-readback.json', d.encoded(observation))
        if expected == 'recovery_held':
            assert TARGET.read_bytes().endswith(b'# foreign post-write\n')
        result = {'case': case, 'phase': final['phase'], 'service': d.service(), 'state': final,
                  'apache_version': d.command(['/usr/sbin/apache2ctl', '-v']), 'source_sha256': d.sha(SOURCE.read_bytes())}
        d.write(directory/'native-result.json', d.encoded(result))
        results.append({'case': case, 'phase': final['phase']})
        print(json.dumps(results[-1]), flush=True)
    d.write(EVIDENCE/'results.json', d.encoded(results))


if __name__ == '__main__':
    main()
