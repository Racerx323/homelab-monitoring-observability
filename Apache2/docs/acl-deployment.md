# Sealed Munin Apache ACL deployment

## Scope and preparation

The [transaction](../scripts/deploy_acl.py) changes only the four existing
`Require ip` lists in the supplied vhost, adding `fd36:5aa8:6971:1::/64`.
`/` is the accepted candidate landing page; this change does not repair the
unused `/munin/` route or redesign CGI authorization. Approving deployment
accepts access from this LAN /64, not just one client.

Seal only after qualifying the current source. The sealer uses immutable
Apache/TLS and graph captures as data/provenance, current repository executable
source and candidate bytes, the pinned host key and public trust snapshot.
It makes no target contact. The resulting archive pins all execution inputs;
changing bytes, expiry, target or scope requires a new bundle and approval.

The controller first consumes its local receipt and checks the observed HTTPS
baseline through both original literal addresses with fixed SNI/hostname/Host.
Root must return 200 on both families; stylesheet/PNG must return IPv4 200 and
IPv6 403, with the previously observed certificate. Baseline drift stops before
SSH staging. No redirect following, credentials or TLS-verification bypass.

## Guarded target transaction

Pinned noninteractive IPv4 SSH stages into an exclusive, root-private operation
directory under `/var/lib/svmf-apache-acl/`. No existing directory is reused.
The stage keeps the frozen executable, archive, candidate, original backup and
durable state/logs. It arms an independent systemd recovery timer before starting
the detached worker. Production confirmation, worker runtime and recovery guard
limits are 90, 150 and 180 seconds respectively.

Preflight requires the captured root/hostname/boot, Apache parent identity and
version, exact included-file paths/resolutions/hashes and active/running service.
Runtime `ExecReload` must be one qualified Debian apachectl path with the single
`graceful` argument. This check precedes any vhost replacement. The worker runs
the full Apache configuration test, records the actual original UID/GID/mode and
backs up the exact original file with fsync. Only protected root-owned regular
vhosts with modes 0600, 0640 or 0644 qualify; the selected mode/group are preserved
explicitly rather than inferred from the earlier capture.

The enabled symlink must retain the captured resolution. Replace only the
reviewed sites-available file using an adjacent exclusive temporary file,
explicit metadata, fsync, atomic rename and parent-directory fsync. Persist
write/reload intent before the respective action. Retest the complete Apache
configuration before invoking `systemctl reload apache2.service`; no restart,
start, package change or certificate replacement is included.

The controller must confirm six verified responses: root, stylesheet and the
previously discovered daily PNG through each original literal family. Require
200, nonempty bounded bodies, correct types, PNG signature and the pinned leaf
certificate. The root worker validates the exact response set, archive identity,
fresh challenge and deadline, then rechecks service/configuration/metadata before
committing. A final controller readback must also pass. Graph freshness remains
a separate monitoring acceptance item.

If that final readback fails after commit, report the operation as unaccepted
and inspect the retained state. The timer does not undo a committed change;
later drift or another actor's changes must not be overwritten automatically.

## Restoration and holds

A failure before write intent records `preflight_failed` without restoration.
Syntax rejection after replacement restores the exact backup and retests it;
no reload is required if none was attempted. Failure after reload intent,
controller rejection or missing confirmation restores the backup, runs the full
configuration test and performs the qualified graceful reload. Independent
controller readback must match the old working baseline, including the original
IPv6 stylesheet/graph 403 responses; that is recovery, not IPv6 acceptance.

Worker loss is covered by the independent timer after the worker runtime limit.
The timer takes the same lock and runs the same restoration checks. A committed
transaction is a no-op for that timer. Frozen target code and durable backups
remain retained; no speculative cleanup or second installation is permitted.

If another actor changes the vhost, other included files, metadata, service or
host identity, hold as `recovery_held` and retain the backup. Do not overwrite
foreign changes, restart Apache or improvise restoration. Inspect the retained
state under a separate approved scope. Reboot, power loss and a failed systemd
manager are outside the transient timer guarantee; use the available local
console and a separately reviewed restoration if required.

An interrupted controller must never be rerun. Preserve its local receipt,
SSH transport receipts and target state. A missing controller result is not
evidence of commit or restoration. Further diagnostic retrieval requires its
own reviewed scope. DNS, host-static networking and Munin activation remain
held until dual-stack dashboard and their separate acceptance gates pass.

## Local qualification

Run `python3 -I -B Apache2/tests/test_deploy_acl.py` for offline contracts.
For native qualification, record the base/image IDs, source hashes, complete
Podman arguments, private log and retained container identity before execution.
Build [the image](../tests/Containerfile) and run the native fixture with
`--network=none`, private systemd runtime, NET_ADMIN/SYS_ADMIN inside that
container, and read-only source mounts. Run Podman outside the filesystem
sandbox as required by workspace policy. Never run the native setup on a host.

The fixture supplies its own certificate/key, FastCGI HTML/PNG, SSH identity and
LAN addresses on its isolated loopback. It tests commit, missing confirmation,
worker loss, rejected health, syntax-test failure, reload failure, foreign drift
and preflight drift. Test-only delegates inject tool failures while executing
the real package tools for other calls. Retain failed fixtures and diagnose
their evidence before changing inputs or rerunning.

## Repository checkpoint

The October 21 publication checkpoint normalized trailing whitespace and line
endings in imported vhost files. Operational directives and stanza placement
were preserved; no Apache configuration write, validation command or reload
was submitted to production. Retained deployment hashes refer to the accepted
live bytes, not these cosmetically normalized repository inputs. Compare live
state and bind fresh input hashes before any future reviewed deployment.
