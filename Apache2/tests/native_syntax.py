"""Additional real-parser rejection check; isolated native fixture only."""
import importlib.util
import json
from pathlib import Path
import subprocess
import ssl

loader = importlib.util.spec_from_file_location('native', '/repo/Apache2/tests/native_acl.py')
n = importlib.util.module_from_spec(loader)
loader.loader.exec_module(n)
n.setup()
n.cmd(['systemctl', 'reload', 'apache2.service'])
before = n.d.service()
original = n.TARGET.read_bytes()
tls_loader = importlib.util.spec_from_file_location('tls', '/tls_probe.py')
tls = importlib.util.module_from_spec(tls_loader)
tls_loader.loader.exec_module(tls)
context = ssl.create_default_context(cadata=Path('/etc/ssl/local.theama.co/STAR_local_theama_co.crt').read_text())
rows = []
def ready():
    sample = [tls.request(address, '/', context)[0] for address in n.ADDRESSES]
    rows.extend(sample)
    Path('/evidence/http-syntax.json').write_text(json.dumps(rows)+'\n')
    return all(row['tls_verified'] and row.get('status') == 200 for row in sample)
n.wait(ready, 10)
n.TARGET.write_bytes(original+b'\nUnknownDirectiveForACLTest yes\n')
check = subprocess.run(['/usr/sbin/apache2ctl', 'configtest'], capture_output=True, timeout=15)
reload = subprocess.run(['/usr/bin/systemctl', 'reload', 'apache2.service'], capture_output=True, timeout=30)
assert check.returncode != 0 and reload.returncode != 0
assert n.d.service() == before
for address in n.ADDRESSES:
    row, _ = tls.request(address, '/', context)
    rows.append(row)
    Path('/evidence/http-syntax.json').write_text(json.dumps(rows)+'\n')
    assert row['tls_verified'] and row.get('status') == 200, row
n.TARGET.write_bytes(original)
assert n.d.command(['/usr/sbin/apache2ctl', 'configtest']) == ''
n.d.reload_apache({'hostname': n.socket.gethostname(),
                  'boot_id': Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
                  'service': before, 'version_sha256': n.d.sha(n.d.command(['/usr/sbin/apache2ctl', '-v']).encode())})
assert n.d.service() == before
result = {'invalid_config_rejected': True, 'graceful_reload_rejected_invalid_config': True,
          'parent_identity_preserved': True, 'original_config_restored_and_reloaded': True,
          'old_root_still_served_dual_stack_after_rejected_reload': True,
          'source_sha256': n.d.sha(n.SOURCE.read_bytes())}
Path('/evidence/syntax-result.json').write_text(json.dumps(result, sort_keys=True)+'\n')
print(json.dumps(result), flush=True)
