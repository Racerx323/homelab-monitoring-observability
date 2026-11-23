# Uptime Kuma operations

## Normal administration

Use the existing administrator at `https://uptime.local.theama.co`. Monitors and alerts remain unconfigured.

Accepted startup state permits ordinary systemd startup through the existing
permit dependency. Keep the firewall and permit guards; the deployment deadline
timer is disabled after acceptance. Do not use the contained-installation
continuations below as routine restart or maintenance commands. Their preconditions
and consumed operation definitions describe recovery states, not current startup.
Future maintenance needs a newly scoped operation and a verified data backup.

The daily 05:30 needrestart schedule and Mailrise default are accepted. No recurring
Kuma backup job or downstream notification delivery proof is claimed. Review the
service-only resource and backup limits before adding monitors or alerts.

## Initial installation

1. Start with the [deployment manifest](../manifests/deployment.yaml) and [installation inputs](../operations/initial-deployment.yaml). Bind the intended host, verified SSH host key, addresses, NetworkManager connection, storage, boot configuration, service limits and release digests. Check for existing data and administrator accounts before choosing bootstrap. The accepted Pi already has both.
2. Prepare a private bundle. Place the reviewed monitoring, server foundation, network and DNS owner files under `repositories/<repository>/`, preserving their relative paths. Include the server owner’s `foundation/` and `Needrestart/` trees and its statically imported `Webmin/ansible/{configure,accept}.yaml` files. The shared foundation skips those optional tasks on this host. Include the network owner’s `host-network/uptime-kuma/` and DNS owner’s `msmtp/` trees. Under the Kuma directory include `payload/known_hosts`, the reviewed `payload/memory-controller/{original,proposed}-cmdline.txt` files, and `payload/runtime/` with the hash-verified ARM64 OCI archive and offline Debian packages. The verified offline inputs for the accepted baseline are in `.local-evidence/uptime-kuma/installation-inputs/runtime/` on the workstation. Re-simulate package installation for the target OS and bind the exact new package/version list. Use fresh node and controller backup destinations. Record a fresh operation ID and a new mode-0700 evidence directory. Set `kuma_run_evidence_directory` in the frozen inputs to that absolute private path under the workspace’s `.local-evidence/uptime-kuma/`. Set the `operation`, `preserve_accepted_prerequisites` and `preserve_installed_foundation` keys in `bundle.json` to the reviewed values. Generate `INPUTS.sha256` for every other regular file relative to the bundle root. The controller rejects links and extra files.
   Use the exact native hostname and verified SSH host key at admission. For a staged continuation, bind fresh runtime observations and the actual preserved backup. Historical boot IDs and previous backup paths in the Pi examples are specific to their original operation.

3. From the frozen Kuma directory, run `ansible-playbook -i localhost, -c local ansible/initial-deployment.yaml --limit localhost --tags controller-preflight` with the controller version in the installation inputs. Review the exact bundled execution and recovery before target contact. Confirm physical boot recovery and an independent administrative path before a reboot or network change.
4. The [installation playbook](../ansible/initial-deployment.yaml) verifies memory control and network prerequisites, installs the fleet foundation and pinned runtime, then starts Kuma on loopback. Complete private administrator setup, a stopped-data backup, isolated restore and startup verification before promoting the guarded backend. Check service health and headroom with the intended workload. On failure preserve the data and startup guard. Follow the [installation recovery boundary](../../changes/2026-11-09-uptime-kuma/PLAN.md#recovery).
5. Submit the guarded backend to the [Caddy owner](../../../homelab-server-configs/Caddy/docs/APPLICATION_ONBOARDING.md). Verify primary activation, secondary replication, private login and WebSocket behavior. Use the [fleet DNS procedure](../../../homelab-dns/Unbound/docs/host-record-deployment.md) for the paired DNS update, verify A and AAAA answers and open the normal HTTPS name over both families. Record observed acceptance in the new change.

## Host foundation and notification configuration

Follow the [architecture ownership table](ARCHITECTURE.md#fleet-host-foundation-and-notifications)
and the owners' procedures. Needrestart and msmtp are host packages;
watchdog coverage uses the qualified fleet backend and must not introduce a
second device owner. The coordinator imports the [foundation owner tasks](../../../homelab-server-configs/foundation/README.md);
combined runtime/resource and operator authentication acceptance are required.

Resolve the effective msmtp default to the owner's `apprise` account at
`mailrise.local.theama.co:8025`; preserve Mailgun for explicit account selection.
Verify root and cron account/configuration precedence, frontend ownership and
aliases before enabling the needrestart schedule. Preserve unrelated accounts,
back up any existing files and retain secrets externally. Use the shared
Apprise/Mailrise platform; do not install duplicate servers on the Kuma host.
Configuration checks and SMTP greeting/QUIT are not downstream-delivery proof.
The retained Mailgun account definition references a secret that this operation
does not provision; its external-email route is not accepted by this installation.

The needrestart owner job runs daily at 05:30 within its 96 MiB scan scope; qualify its normal notification
side effects as part of revised operation scope. Do not run a test message or
an alert-producing scan to verify configuration. Review exact content and
recipient separately if an actual delivery test is required. Keep Uptime Kuma
monitors and notification settings empty during service-foundation acceptance.

## First administrator

For a new, unclaimed installation only; the accepted host already has its account.

Keep setup on loopback. In the operator's own terminal, use existing SSH access:

```bash
ssh -N -L 127.0.0.1:13001:127.0.0.1:3001 ama@10.1.3.75
```

Open `http://127.0.0.1:13001/`, create the administrator, log out and verify login.
Leave monitors and notifications empty. Passwords, cookies and recovery values
stay out of chat, Git and evidence logs. Tell the agent only that account creation
and login succeeded. The playbook checks non-secret account counts and the
authentication setting before exposing the backend.

The accepted host uses `https://uptime.local.theama.co`; the temporary Kuma
bootstrap tunnel is no longer required for normal dashboard access.

## Routine inspection

Run on the Pi; retain sensitive operational details privately. Inspection does
not authorize a restart or configuration change.

```bash
sudo systemctl status uptime-kuma.service uptime-kuma-firewall.service --no-pager
sudo podman logs --tail 100 uptime-kuma
sudo systemctl show uptime-kuma.service -p NRestarts -p MemoryCurrent -p MemoryMax
sudo nft list table inet uptime_kuma
```

The service requires UID 1000, local persistent data, a read-only root filesystem,
bounded resources/logs and no runtime socket mount. Record unexpected restarts,
OOM events, guard changes, published addresses or management-routing changes in
the ledger before dependent maintenance.

## Backup and restore

Stop the source and archive its complete data tree; do not copy open SQLite
files. Use a new mode-0700 snapshot directory and mode-0600 archive. Retain the
on-node backup and a protected off-node operational copy. The initial operation
uses `~/.local/state/uptime-kuma/backups/` on the workstation, without cloud upload
or a schedule. Secret-bearing backups are not source files or evidence logs.

The [backup tasks](../ansible/tasks/backup-and-restore.yaml) verify the fetched
archive, open it with the pinned image in an isolated instance, then restart and
check the source even when qualification fails. Keep the source stopped during
this initial restore check so only one application instance consumes its resource
budget. The restore publishes no ports and has no network access.

The initial checker rejects missing databases, unsafe paths/external links,
archives above 64 MiB and unexpected account/monitor/notification counts. Those
bounds match the service foundation. Review backup capacity and expectations when
introducing workloads. This is not a recurring-backup service. Preserve failed
receipts; never delete active data to make a restore pass.

## Updates and recovery

Use `change-control` for substantial updates. Inspect accepted live state,
prepare a pinned ARM64/runtime bundle and preserve a verified pre-upgrade backup.
An image rollback cannot undo a database migration: pair the old image with its
matching pre-upgrade data through the reviewed recovery procedure.

Original boot bytes are saved on-node and off-node. If the Pi does not return,
stop remote execution and use the physical console or microSD card to restore
that exact file. Copy bytes without changing encoding or line endings, then
verify the original checksum and management access. SSH loss is not recovery proof.

Runtime failure retains the guard/data and can leave packages, image and startup
definitions. Inspect actual residue before further mutation. Failed backend
promotion in remaining-deployment restores/reloads the loopback definition and
enters independently verified stopped containment without another start. Preserve
the three-start/300-second native limit; initial startup, source recovery after
backup and promotion already require three planned starts. Do not reset counters
or retry a refused start. The legacy initial-deployment path retains its separate
loopback recovery. Earlier accepted prerequisites
may remain; no whole-host rollback is implied. Keep actual outcomes in the
ledger and obtain revised authority for material departures or successors.

The backend reachability probe requests `/dashboard` directly over each family,
requires HTTP 200 and checks the expected backend and admitted source addresses.
It does not follow redirects: the pinned application normally redirects `/` to
`/dashboard`, so a 200-only root probe is not its response contract. This probe
does not replace administrator/authentication, ingress denial or final HTTPS and
WebSocket acceptance.

## Repository checks

Run `/bin/bash uptime-kuma/tests/check.sh` for the focused offline checks. Native
template/unit, packet and isolated image/restore qualification are retained in
the work ledger with their tested inputs. These checks do not contact the Pi
or substitute for target acceptance.

## Diagnose container and published network paths

Use the current change ledger's exact sealed diagnostic after scoped authorization.
Its preflight compares the installed source identities, image and stopped data,
existing network, service state and diagnostic resource budget. It does not
reinstall or load anything, modify ports/NAT/routing policy, or resume deployment.
Starting the unchanged service still causes ordinary Podman network rules and
application database/log activity.

The collector records IPv4 and IPv6 independently for container loopback,
host-to-container addresses and published host loopback ports. It saves private
Pi-side checkpoints and a controller receipt before containment. Bodies, cookies,
credentials, environments and command lines are excluded. Application log evidence
contains only fixed startup event labels and selected error codes; unknown text is
omitted and counted. A complete measurement with failed HTTP requests can pass the
diagnostic; it does not pass deployment acceptance.

Persistent unit drop-ins require an operation-owned permit beneath /run for both
generated units. Create the permit only after verifying the independent native
containment timer. Temporary runtime drop-ins limit startup, lifetime and shutdown
and suppress automatic restarts without raising memory caps. On completion/error,
remove the owned permit, stop both units, independently verify inactive units,
absent listeners/containers and intact guards, then cancel the fallback. Remove
only unchanged owned runtime overrides and verify the original timing policy.
The private observer/checkpoint and persistent guards may remain.

A subsequent reboot clears the permit, so the generated WantedBy definitions
remain blocked. Do not remove guards, recreate a permit or start/reboot for a retry
under a consumed approval. A later recovery/deployment operation must explicitly
review how to release containment. If actual containment cannot be proved, keep
the fallback armed and record manual intervention; do not claim a clean stop.

## Correct IPv6 loopback transport

Use the current ledger's separately sealed correction, not a consumed diagnostic.
The existing native lifecycle imports the owner correction tasks, preserves the
original checked Quadlet in protected operation storage, removes only its Podman
::1 publication and installs the IPv6-only loopback socket/proxy templates. The
application wants the socket; both proxy units stop with it. Never enable the
proxy separately or bind it to :: or a LAN address. The unchanged ingress guard
and dual-stack container network continue to govern backend access.

Preflight requires the exact stopped diagnostic residue and existing guards,
no new proxy units or conflicting permit, an installed root-owned systemd proxy
binary and 528 MiB available. The 320 MiB application and 96 MiB observer caps
remain unchanged; add 16 MiB for the proxy and retain the 96 MiB host reserve.
New continuations use staged admission, requiring later combined target
qualification rather than inferring capacity from an isolated trial.

Guard all four units with the existing ephemeral permit and extend independent
fallback/normal stop checks to the proxy socket and service. Require all six
path/family probes to return the expected setup redirect after startup; retain
actual proxy limits/state/peak and container publication identities. Then remove
the owned permit, stop and independently verify all four units, no listeners or
containers, empty database integrity and restored timing. Corrected definitions,
the original Quadlet backup and persistent guards remain after success or failure;
this is stopped corrective acceptance, not deployment completion or automatic
rollback. Any source restoration, new permit/start, guard release, administrator
setup, reboot or backend/DNS/Caddy work needs a new reviewed continuation.

## Measure observer overhead and scan-time headroom

Use `ansible/measure-capacity.yaml` only under its own exact-bundle authorization.
It compares three raw-before/Ansible-command/raw-after memory readings using the
same awk expression as deployment admission. Raw probes avoid a remote Python
module; all probes still include SSH/sudo and concurrent host activity. Paired
differences are observations, not a causal allocation measurement or permission
to subtract assumed overhead from any admission reading.

With all four Kuma units stopped, the coordinator verifies the pinned
scanner and reviewed owner policy, then runs one list-only scan through the
[foundation observer](../../../homelab-server-configs/foundation/README.md#measure-scan-time-headroom).
The isolated measurement needs 224 MiB available: scan 96, observer 32 and reserve
96. This is a different workload from deployment and does not qualify the staged deployment
gate. No notification producer, schedule, package action, application start,
reboot, proxy change or cache manipulation is included.
Both raw and Python-backed admission readings must meet 224 MiB. After the
observer is resident, a fresh 192 MiB host/finite-parent gate leaves room for
the full 96 MiB scan plus reserve before the scan is launched.

The coordinator retains paired readings, raw scan output, discrete headroom samples,
native scan peak and cleanup/application-state receipts. It stops only its two
measurement units and removes only its fresh protected directory under `/run`
after fetching evidence. The scan has a 90-second native start timeout; the
observer has a 120-second runtime limit, both with five-second stop timeouts.
If the controller disappears, those limits bound processes; volatile files or
an exited transient-unit record may remain. Do not claim remote cleanup without
its receipt or replay the operation to obtain one.

Review the native peak, host and finite-parent minima, actual sample gaps, paired
reading differences and any failures before preparing a continuation. A stopped-
application scan does not establish combined capacity: repeat the reusable scan
observation with services running during the future authorized acceptance stage.

### Staged scan admission

New working definitions follow the approved architecture's 624/224/192/96 MiB
stages. The foundation owner installs the same guard for combined acceptance and
the scheduled producer. Never replace a refused scan with a direct needrestart
invocation to bypass admission. A refusal or failure produces nonzero status;
cron's existing failure capture handles scheduled outcomes. Scheduled producer
notifications remain enabled only within the separately authorized schedule stage.

The guard refuses overlap and pre-existing unit names, keeps native bounds and
collects owned units after terminal readback. Acceptance retains admission, scan,
observer and cleanup evidence before assertion. If cleanup cannot be verified,
retain the private volatile directory and stop; do not remove unrelated units or
retry a consumed operation. The stage architecture defines deadlines and temporary
allowances, including restore and ingress. A local qualification pass is not a
Pi deployment or acceptance result.

## Private application acceptance after route activation

This is a separate application check after both Caddy nodes accept the same
release. It does not publish, reload, restart or roll back either node. Run only
after approval of the exact helper/client identities, endpoints and receipt path.
Do not reuse a consumed deployment command or its timed operator window.

Use a private **workstation WSL/Ubuntu terminal**, where rootless Podman and the
retained client image are available. The Pi does not need a browser. The helper
prompts locally; never put credentials in arguments, environment variables, chat
or a transcript. No deadline applies to entering credentials. Once submitted,
the client run is bounded to 180 seconds and cleans up its uniquely named container.
Use a new private receipt path for each separately authorized attempt.

```bash
python3 uptime-kuma/scripts/private-proxy-login.py --standalone OPERATION PRIVATE_RECEIPT
python3 uptime-kuma/scripts/private-proxy-login.py --verify-standalone-receipt OPERATION PRIVATE_RECEIPT
```

The client reaches the Proxy VIPs directly with the dashboard hostname
for TLS/SNI and Host, so DNS changes are unnecessary. It requires system trust,
IPv4 and IPv6 dashboard 200 responses, real WebSocket transport, unauthenticated
denial, incorrect-password rejection, immediate correct login, a second client,
65-second authenticated idle survival and denial after logout. It does not add
monitors or alerts. The receipt records only bounded result fields and the client
hash. A valid receipt proves this check only; it does not approve DNS.

On failure, the helper prints and retains the wrapper stage, client exit status
when available, cleanup outcome, and a strictly validated client stage, address
family and error code. Reports with extra fields, unknown enum values, malformed
JSON or more than 1,024 characters are discarded; only a fixed fallback category
is retained. Raw stdout/stderr, exception messages, usernames, passwords, tokens
and response bodies are never copied into failure evidence. An unavailable client
report leaves the underlying cause unknown; an exit status alone is not a login
or proxy diagnosis. Successful receipt fields and acceptance checks are unchanged.
Preserve failed receipts and pending files; do not retry a consumed attempt.

Before prompting for credentials, the helper runs a 30-second startup check in
its pinned image with networking disabled and stdin closed. It checks source
readability, JavaScript syntax and the Socket.IO client import. Failure stops
before credential entry and reports only the validated diagnostic fields above.
Both startup and login containers use rootless `--userns keep-id` and the invoking
user's UID/GID, preserving access to owner-private sources through a read-only
mount. Do not broaden file permissions or change ownership to make the image's
default user work. The startup container is removed before the login container
uses the same invocation-owned name; existing bounded cleanup covers failures.
The successful login receipt schema and 180-second client limit are unchanged.

The client waits up to 10 seconds for Kuma's `loginRequired` event before issuing
requests; transport connection alone is not application readiness. Initial local
setup must also receive `setup`; unexpected setup or automatic login rejects.
No arbitrary sleep or automatic reconnect is used. Safe error codes distinguish
`READINESS_TIMEOUT`, `UNEXPECTED_READINESS`, `ACK_TIMEOUT`, `ACK_ERROR` and
`SOCKET_DISCONNECTED`. An acknowledgement timeout never counts as denial.
The overall client limit still bounds connection/readiness and subsequent checks.

### Repeated observation and completion gate

The separate acceptance review must bind passive observation on both Caddy nodes
to the accepted release and manifest, plus the exact application fragment. Use
existing SSH access as `pi`, with no uploads or service-control commands. Capture
the journal cursor and service-cycle baseline before observation.

- Repeat trusted direct-node and shared-VIP dashboard requests in both families
  at the start and after at least 65 seconds. Retain expected/observed status
  and bounded request errors; do not retain response bodies or credentials.
- Check `/healthz` remains 204 on both nodes. Compare selected release/manifest
  at the start and end; drift rejects acceptance.
- Inspect cursor-bounded Caddy journal records for new application health failures
  or upstream exclusions. Retain sanitized counts and failure classification;
  missing journal access or truncated evidence rejects acceptance.
- Observe at least two actual completed cycles after baseline for each node's
  `caddy-sync-health.service` and `caddy-pihole-web-health.service`. Record unique
  monotonic start/end timestamps, successful result and zero exit status; an
  active timer or repeated unchanged timestamps do not prove completed cycles.
  Allow at most 360 seconds, sampling every five seconds. Do not start a timer
  or service to manufacture a cycle. Timeout is incomplete acceptance.
- Require the standalone private receipt and all observations to refer to the
  same accepted route. Two HTTP/WebSocket observations spanning the health
  intervals are bounded acceptance, not proof of every internal Caddy probe.

Any failure stops DNS progression and preserves the accepted running services.
Operator delay or missing receipt does not trigger rollback. Further repair,
inspection, publication or retry requires its own reviewed scope. Recheck the
DNS owner's conditional approval, candidate identities and expiry before DNS
execution; this application procedure neither renews nor consumes that authority.

The final journal read uses the baseline cursor and unit filter without requesting
an output cursor. A successful empty result is valid; a nonzero exit is never
accepted as an empty journal. The baseline still requires an explicit cursor.
Command failures retain only a fixed program/stage, expected/observed exit status,
output byte counts and diagnostic category. Raw argv/cursors, command output and
journal message text are excluded. A category is a diagnostic clue, not proof
of journal health; malformed, inaccessible or truncated evidence still rejects.

### Passive collector and combined receipt

`observe-proxy-acceptance.py --run SPEC EVIDENCE_DIRECTORY` streams its source over
existing strict-host-key SSH to `pi` on each Caddy node, then runs it with
`sudo -n python3 -`. It installs no target file. Each node reads the selected
release, manifest and fragment, uses trusted `curl`, `systemctl show` and
cursor-bounded `journalctl`, and exits within six minutes. The controller permits
400 seconds per node for transport and readback. Node A failure stops before B.
The 320-second cycle-poll phase leaves time within the node deadline for final
requests and journal readback. No service start, restart, reload or timer changes
are permitted; no backend SSH, DNS query or configuration change is included.

An existing evidence directory rejects replay. Retained samples include native
monotonic service timestamps and exit results. Journal output is summarized into
counts and integrity hashes; message text is not returned. Journal truncation,
unparseable records, access errors or relevant health warnings/failures reject.
Conservative rejection may require later review of unrelated proxy-health noise.

Run the sealed private operator command first, at the operator's convenience.
After its receipt passes, run the separately listed observer command. It verifies
the private receipt before SSH and runs `--verify-combined SPEC EVIDENCE RECEIPT`
afterward. Combined verification checks both nodes, exact command/source/spec
bindings and the private receipt. A combined pass leaves DNS pending. Neither
command can start a deployment or renew the DNS approval.
