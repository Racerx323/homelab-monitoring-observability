# Change plan: initial Uptime Kuma deployment

## Objective and scope

Deploy and configure the Uptime Kuma service on `j2-svpi3bmf`, with an internal
HTTPS dashboard at **`uptime.local.theama.co`** through the existing Caddy
service. Aaron approved this dashboard name on November 9, 2026.

- Owning repository: `homelab-monitoring-observability`; component: `uptime-kuma/`.
- Target supplied by Aaron: IPv4 `10.1.3.75/22`; IPv6 ULA
  `fd36:5aa8:6971:1::75/64`; management FQDN not supplied.
- Hardware supplied by Aaron: Raspberry Pi 3B+, 1 GB RAM, 32 GB raw microSD,
  PoE HAT, Ethernet `eth0`, Wi-Fi and Bluetooth disabled.
- OS supplied by Aaron: Raspberry Pi OS Lite 64-bit, Debian 13.
- Include service installation, persistence, secure initial administration,
  startup/recovery, backup/restore procedure, internal HTTPS onboarding,
  appropriate resource controls, and repeatable deployment/operating procedures.
- Include host-installed fleet-managed needrestart, Webmin, msmtp and watchdog
  coverage, as Aaron requested November 10. Reuse existing fleet Apprise API and
  Mailrise services; Mailrise is the msmtp default, Mailgun requires explicit selection.
- Exclude Uptime Kuma monitors/alert activation, synthetic test notifications, public exposure, automatic
  application updates, unrelated OS maintenance, and unrelated changes to existing services.
  Aaron chose service installation first; monitor and alert selection comes later.

## Baseline and unknowns

| Fact or unknown | Observation/source and date | Consequence or required verification |
| --- | --- | --- |
| Host description and addresses | Aaron's project request, November 9, 2026 | User-supplied baseline; verify against target before design is final. |
| SSH account `ama` | Aaron's response to the read-only inspection question, November 9 | Bounded read-only inspection is permitted; no credentials belong in chat or Git. |
| Dashboard FQDN | Aaron explicitly agreed to `uptime.local.theama.co`, November 9 | Fixed requirement; DNS and Caddy configuration remain subject to their owning processes. |
| Architecture absent | Aaron's clarification, November 9 | Prepare one proposed governing architecture in `uptime-kuma/docs/ARCHITECTURE.md`; do not invent accepted design. |
| No existing Kuma record or inventory entry located | Scoped literal searches and current production inventory, November 9 | Start one change record; verify target for existing services/data before installing. |
| Current upstream stable release | GitHub `releases/latest` resolved to `2.5.9`, November 9 | Candidate version only; verify ARM64 image manifest and immutable digest before sealing. |
| Runtime, storage headroom and target load | First bounded read-only baseline, November 9 | No Podman found; about 745 MiB memory available, 24.65 GiB root free and load 0.00. Runtime capacity still needs measured acceptance. |
| Permanent ULA and memory control differ from prerequisites | Same baseline; W-013 and W-014 | Requested ULA absent; memory controller absent from cgroup v2. Prepare explicit prerequisite corrections before service deployment. |
| Fleet foundation baseline | November 10 bounded inspection | Cron active; Webmin/msmtp/needrestart absent; vendor systemd watchdog already active at 60/120 seconds. Reuse owner profiles and preserve existing files. |

## Approach

1. Inspect the host read-only and record a bounded private baseline. Check
   identity, OS/architecture, RAM/swap/storage, cgroups, runtime packages,
   listening services, network addresses, time, and available administration.
2. Prepare the proposed permanent architecture. Prefer the existing Podman and
   systemd/Quadlet conventions; evaluate a pinned slim ARM64 image with local
   SQLite storage for this service-only deployment. No browser monitors or
   extra database service are required by the current scope.
3. Prepare declarative deployment automation with preflight, installation,
   acceptance, cleanup and recovery beside its execution path. Use existing
   repository helpers rather than building another transaction framework.
4. Prepare Caddy and DNS onboarding under their owners. Keep the dashboard name
   fixed and distinguish management identity from the service alias. Routine
   onboarding follows the approved primary-first contract in
   [the Caddy guide](../../../homelab-server-configs/Caddy/docs/APPLICATION_ONBOARDING.md#routine-release-sequence):
   prepare one immutable candidate, activate/verify Node A before transport
   exposure, then replicate the same revision and independently accept Node B.
   Primary service does not wait for Node B; HA completion and DNS do. This
   sequence is implemented and locally qualified in the existing machinery;
   deployment and production acceptance remain pending.
   Preserve platform maintenance separately and do not reuse the consumed
   certificate-derived onboarding operation. Keep login/WebSocket completion
   checks separate from activation, without a timed human receipt window.
5. Qualify the Pi foundation locally and present one exact SHA-256 offline bundle
   and native Ansible command. Include preflight, boot/address/runtime changes,
   fleet host foundation configuration, reviewed reboot count, operator account setup, backup/restore, backend acceptance
   and recovery. DNS/Caddy use their owner-governed operations; final HTTPS
   acceptance remains required for this project.
6. Requalify the combined foundation/application resource budget and package closure.
   The prior Pi-only candidate was withdrawn without execution on November 10;
   do not reuse its hash or qualification as approval for this expanded operation.
7. Execute only after that approval, establish safe initial administration, and
   evaluate acceptance. Record results and reconcile permanent documentation.

Architecture will own enduring design. `uptime-kuma/docs/OPERATIONS.md` will own
repeatable procedures. This plan owns the initial transition; `WORK.md` owns
all current tasks, decisions, findings and next actions. Link executable assets
in their normal component locations as they are prepared. Raw evidence stays
outside Git beneath the workspace's protected `.local-evidence/uptime-kuma/`.

The November 10 attempt accepted the boot and permanent-address prerequisites,
then stopped before package installation at the offline APT simulation. Its exact
bundle and terminal receipt are preserved. The continuation verifies those
prerequisites read-only, disables APT repository sources for local-file acquisition,
and performs the remaining installation and acceptance with one planned startup
reboot. It does not repeat the accepted boot-file or NetworkManager changes.

The continuation installed the pinned packages but stopped at Webmin HTTP
acceptance. Before further installation, qualify one bounded diagnostic with
request timing and cgroup pressure/process evidence under the existing limits.
Its acceptance is complete evidence and independently verified return to stopped,
disabled, no-listener/no-permit containment. A native timer must provide containment
if the controller disconnects. This diagnostic does not accept Webmin, change its
configuration/limits, reboot, or continue application installation.

The diagnostic completed with verified containment and measured memory-high
reclaim waits. The proposed correction disables only automatic package-update
collection in Webmin's system-status dashboard (`collect_pkgs=0`), retaining its
128/192 MiB/no-swap limits. This removes the dashboard update summary; fleet
package maintenance and needrestart retain their separate roles. This proposal
is subject to exact-bundle review and actual Pi acceptance.

The next continuation verifies all 29 installed package pins, unchanged accepted
mail/needrestart/guard files and stopped Webmin before applying that owner profile.
It verifies boot/address prerequisites read-only, performs no package action,
and verifies the retained image before import. Corrected Webmin startup has a
native five-minute containment fallback until foundation acceptance passes.
Only then continue the previously planned application installation, one startup
reboot, private operator setup, backup/restore and guarded backend acceptance.
Consumed definitions and archives remain preserved; DNS/Caddy retain their
separate live boundaries.

The initial Kuma observer failed at a loopback TCP connection without preserving
which family failed. The next operation is diagnostic only: probe each family
inside the container, from the host to its actual container address, and through
the host's published loopback port. Retain per-probe status/timing/errors, actual
ports/NAT/routes, cgroup samples and allowlisted application startup events before
stopping. HTTP failures are measurements; they do not discard other results or
relax service acceptance. Save checkpoints privately on the Pi as well as fetching
the final receipt to the controller.

Before startup, add persistent ConditionPathExists guards to both generated units,
requiring one operation-owned permit under /run. Arm native independent containment
before creating that permit. Temporary runtime controls disable retries and bound
start/runtime/stop; the 256/320 MiB Kuma limits remain unchanged. Use at most
96 MiB/no swap/20% CPU for the observer and require 512 MiB available for the
320 MiB application, 96 MiB observer and 96 MiB host reserve. Remove the permit,
stop both units, verify no listeners/containers, retain the permanent guards, and
restore only the owned temporary overrides after stop. Thus a later reboot loses
the ephemeral permit and cannot start the guarded generated units unattended.
No reboot or corrective network change is part of this diagnostic.

The November 10 network diagnostic retained working container/direct IPv6 and
published IPv4, with repeatable published ::1 timeouts. The proposed correction
uses the installed systemd socket proxy for the IPv6 loopback frontend, forwarding
to 127.0.0.1:3001. Remove only the ineffective Podman ::1 publication; retain the
dual-stack container network, ingress table and future explicit backend bindings.
The socket is IPv6-only on ::1 and is wanted/stopped with Kuma. The proxy adds a
16 MiB/no-swap/10% CPU/16-task cap; existing Kuma and observer limits stay unchanged.
Require 528 MiB available for this isolated application/proxy/observer trial and
96 MiB host reserve. Combined foundation operation needs a separate measured
resource check; the previous 704 MiB gate does not account for this extra 16 MiB.

Reuse the native bounded diagnostic lifecycle as one corrective continuation.
Verify the original consumed diagnostic residue and guards before changes, save
the original Quadlet, install owner templates and guard both proxy units on the
same ephemeral permit. The fallback and normal containment must stop and verify
all four units and all application listeners. Pass all six paths after startup,
retain resource/proxy evidence and stop with data integrity/timing restoration.
Do not remove existing guards, raise application limits, reboot, start Webmin,
create an administrator or proceed to backend/DNS/Caddy activation. On failure,
retain corrected definitions and the original source backup with all units
stopped/guarded; restoring old definitions is not automatic whole-host rollback.

The remaining-deployment continuation skips package/image/bootstrap installation
and the consumed boot/address mutations. Preserve all four guard files; use a
protected deadline-bound startup dependency and persistent native containment
across one planned reboot. Give the operator a fifteen-minute private login
window inside the forty-minute operation bound. Reuse the existing backup/restore,
backend and owner schedule checks. Permanent startup authority is written only
after these gates pass; failure retains data and configuration in stopped
containment. DNS/Caddy and final HTTPS remain separately governed.

For completion after an accepted reboot and operator-verified login, require the
same retained boot identity, protected contained authority, exact predecessor
control files, the operator's protected acknowledgement and an active-user,
authentication-enabled database with no monitors/notifications. Renew startup
once from the freshly verified state hash, retaining its original bytes. Preserve
the recorded reboot count; another pending reboot is refused. Skip account setup,
the completed reboot and the timed operator wait. Repeat current runtime and
combined scan acceptance before backup/restore and after guarded promotion. This
is a separately sealed continuation, not permission to replay a consumed bundle.
If that completion is consumed, the successor must preserve its original
`previous-state.json` and exclusively archive the failed completion as
`completion-state.json`. Verify both hashes before renewal and during terminal
acceptance/containment. Preserve the verified administrator backup on both sides;
use distinct unused destinations for the next consistent backup/restore. Reuse
the accepted reboot evidence and retain the no-reboot/account-setup boundary.

## Acceptance criteria

| ID | Required observed outcome | Verification method and evidence required |
| --- | --- | --- |
| AC-001 | Target identity, Debian 13 ARM64, supplied network addresses and adequate resources are verified. | Bounded host baseline and reviewed resource/storage budget; discrepancies resolved explicitly. |
| AC-002 | One agreed architecture and a reproducible, immutable runtime definition exist. | Architecture review, pinned upstream release and ARM64 digest, local parser/policy tests; no mutable-tag-only deployment. |
| AC-003 | The service uses local persistent data with correct ownership and a suitable filesystem. | Target mount/ownership observations, service write/read check and persistence after restart; no NFS data directory. |
| AC-004 | The internal dashboard works at `https://uptime.local.theama.co` over both intended address families. | Owning DNS/Caddy validation, trusted TLS, HTTP and WebSocket/application checks from the intended client path. |
| AC-005 | Initial administration is safely established and protected. | Controlled bootstrap, authenticated dashboard, unauthenticated access behavior and absence of public setup exposure; no secrets in tracked artifacts. |
| AC-006 | Startup and recovery work within a measured resource budget on this Pi. | Actual systemd/Quadlet acceptance, bounded restart/reboot test where approved, memory/storage observations and absence of OOM/restart loops. |
| AC-007 | Backup and restore are documented and qualified without corrupting the active database. | Consistent full data-directory backup and isolated restore check; limitations and off-node backup destination explicit. |
| AC-008 | Existing services, network policy and unrelated configuration are preserved. | Before/after comparison limited to affected state, conflict checks and rollback/residue verification. |
| AC-009 | No Uptime Kuma monitors/alerts, synthetic test notifications or unattended application upgrades are activated. | Configuration review and target application/service observations; later scope remains separate. |
| AC-010 | The deployment is operable and all findings have a durable disposition. | Permanent operations/architecture references, reconciled ledger and criterion-by-criterion result; no unsupported claim of live acceptance. |
| AC-011 | All requested host foundation capabilities are installed/configured through their fleet owners. | Verify needrestart package/script/cron and Debian 13/Pi 3 reporting; Webmin package/service and reviewed management policy; msmtp/sendmail frontend and effective default; qualified watchdog device/owner/settings without competing daemon. Reconcile proposed versus accepted policy. |
| AC-012 | Host notifications use existing fleet Mailrise/Apprise, with Mailrise selected by default in msmtp. | Inspect effective account/aliases and consumer invocation; qualify SMTP greeting/QUIT without sending. Preserve Mailgun for explicit external email. Real test messages and downstream delivery require separately reviewed content; do not claim receipt from configuration or SMTP connectivity. |

Foundation configuration uses owner profiles: Webmin SSH-only loopback with
explicit `ama` authentication, msmtp Mailrise default, list-only v8 needrestart
and adoption of the existing vendor watchdog without installing another daemon.
The approved staged policy keeps Kuma 320 MiB, Webmin 192 MiB, scan 96 MiB and
proxy 16 MiB caps, with 96 MiB observed reserve and a separately bounded 32 MiB
scan observer. Startup requires 624 MiB, with fresh scan admission at 224/192 MiB.
The [stage budget](../../uptime-kuma/docs/ARCHITECTURE.md#meaning-and-limits-of-the-admission-budget)
defines the accounting and sampling limitations. Aaron approved local implementation
and qualification, not live execution. The previous failed 720 MiB gate and all
consumed bundles remain historical evidence; no retrospective acceptance is claimed.
No alternate host is available. Do not add back observer costs, drop caches or
remove required services to force admission. Actual Pi combined acceptance remains
required at all three checkpoints, including scan-time observation.

The daily 05:30 needrestart job is enabled only after combined acceptance; normal
operational notifications then use the shared fleet transport. Synthetic tests
and downstream delivery proof are outside this operation.

## Approved staged admission policy — local qualification only

Aaron approved this admission-policy change for local implementation and
qualification only. Candidate preparation is separately approved; live execution
requires exact-bundle authorization recorded in WORK.md. Keep the same Pi, required
foundation services, service-first scope, all current service caps and no-swap
settings. Do not trim radios, add back observer costs or drop caches.

Use these stage-specific checks in new working definitions:

| Stage | Unadjusted available-memory requirement | Basis |
| --- | --- | --- |
| Before starting stopped application services, with no scan/scan observer running | 624 MiB (638976 KiB) | Kuma 320 + Webmin 192 + proxy 16 + host reserve 96. |
| Before launching a scan observer alongside running services | 224 MiB (229376 KiB) | Scan 96 + separate observer 32 + reserve 96; running-service use is already reflected in availability. |
| Immediately before the scan, after the observer is resident | 192 MiB (196608 KiB) | Scan 96 + reserve 96, with actual observer/orchestration costs included. This is an additional check, not a replacement for the prior 224 MiB check. |
| During the scan | At least 96 MiB (98304 KiB) at every retained sample | Check host and applicable finite ancestor headroom; retain failures and stop the scan on breach. |

Use the actual Ansible execution path and retain raw readings before assertions.
A stage fails on its first unmet gate; no averaging, correction factor or admission
retry loop. The retained 705.88–708.66 MiB Ansible observations exceed the proposed
startup gate by 81.88–84.66 MiB, but are historical comparisons only. They do not
establish current admission, running-service headroom or successful deployment.

Tradeoff: the proposal gives up the original full simultaneous-cap capacity test.
During a scan, resident services may grow toward their unchanged caps; available
memory can fall faster than a sampled observer detects it. Native service caps and
scan termination do not guarantee a hard 96 MiB host reservation or exclude OOM.
The separate 32 MiB observer is explicitly budgeted, not taken from the reserve.
Its future growth and other host activity remain part of the monitored risk.
Acceptance is for the initial service-only workload; monitors/browser checks and
future workload growth require capacity review. No claim of continuous protection
outside the bounded observation windows is made.

Implementation and qualification required before a live candidate:

- Integrate the existing owner scan observer at all three combined acceptance
  checkpoints, preserving native deadlines, no-swap controls, exact native peak,
  maximum one-second sampling gap, kernel reporting, health and pressure checks,
  failure evidence, owned cleanup and existing application containment.
- Apply the same staged scan admission and observation to the actual daily
  Needrestart producer and its children. The existing cron scope has only a cap;
  it is insufficient for this proposal. Refuse overlapping runs. On insufficient
  headroom, skip that day's scan and retain a clear failure record; no tight retry
  or claim that a skipped scan passed. Preserve fleet notification semantics and
  account for notification children within the owner budget. Do not silently
  replace the producer with the diagnostic list-only command.
- Do not enable the daily schedule until the guarded production path is locally
  qualified and the authorized combined Pi acceptance passes. Confirm runtime
  deadlines against the producer's existing five-minute scan bound; do not copy
  the diagnostic's 90-second limit over it without owner qualification.
- Reconcile the complete execution order, including startup/reboot, consistent
  backup/restore and the 64 MiB ingress probe. Keep transient jobs serialized;
  the restore replaces the stopped source. Account for any concurrently resident
  observer explicitly. Do not infer safety for these stages from a scan-only test.
- Test numeric boundaries, unavailable evidence, finite-parent limits, low reserve,
  observer/scan failure, delayed sampling, overlap, deadline and cleanup paths.
  Exercise the real producer with local notification substitutes, not live mail.
  Then seal one operation with actual Pi acceptance and failure containment.

Decision: approved for local implementation and qualification, accepting the
stated change from simultaneous-cap budgeting to measured stage admission. This
does not authorize service starts, scans, reboot, schedule enablement, messages
or any other live action. If qualification fails, stop and record the result;
do not lower another threshold automatically.

## Recovery and stop conditions

Stop before mutation for wrong identity/architecture, resource or port conflicts,
existing unreviewed Kuma data, unexpected network/controller state, image/digest
mismatch, failed prerequisites, or an incomplete authorized operation.

The candidate must preserve any existing target state before changes, define
reverse-order rollback for only its owned changes, and verify cleanup/residue.
Never delete a database or existing service to make a new installation succeed.
Do not replay a consumed failed operation for a cleaner result. Recovery and
service restart/reboot authority must be explicit in the reviewed candidate.

The [Pi coordinator](../../uptime-kuma/ansible/initial-deployment.yaml) and
[operation inputs](../../uptime-kuma/operations/initial-deployment.yaml) define
the candidate. Boot recovery restores the original when reachable or stops for
physical intervention. Address recovery uses the native checkpoint and readback.
Runtime/foundation failure retains guard/data and requests Webmin containment
through its persistent permit. Packages/configuration and, after partial install,
a temporary policy-rc.d may remain and require residue review. For remaining-deployment, failed backend
promotion restores/reloads the loopback definition without another start, then
enters the existing outer containment and independent stopped-state verification.
This avoids a fourth planned start against the unchanged three-per-300-second
limit. Any earlier rate refusal also fails closed; no counter reset or wait/retry
is part of recovery. The legacy initial-deployment path retains checked loopback
recovery and is not selected for the installed-foundation continuation. Earlier accepted prerequisites
may remain after a later failure; this is not whole-host rollback. The exact
bundle, command, approval and consumption state belong in `WORK.md`.

Aaron confirmed physical access to the device, its microSD card and a console
KVM on November 9. Preserve the original boot command line both off-node and on
the node before any boot correction. If the Pi does not return, stop with a
manual-intervention result and use the console/card to restore the saved file;
do not claim remote recovery. This recovery availability is not reboot approval.

## Execution boundary

- Authorized now: repository preparation, upstream research and local qualification.
  The November 11 backend-completion operation is consumed; it grants no further
  target access, mutation or replay. Historical inspection scopes are retained
  in the ledger and do not authorize another live operation.
- Live installation, package changes, transfer, service start/restart, firewall
  edits, DNS and Caddy publication/reload require exact-bundle authorization under
  the owning repository/component rules.
- Aaron approved bounded read-only Caddy inspection on November 9; it completed
  and its evidence is retained. It grants no new inspection authority.
  Network-controller access is not included.
- No Uptime Kuma monitor/notification activation, synthetic message sending or
  external publication is authorized. Foundation schedules and their normal
  notification effects must be explicit in the revised live operation.
- Record the exact candidate, approved command and approval consumption in
  `WORK.md`; this plan is not a live-execution approval.

## DNS/Caddy onboarding contract

Prepared November 11 from the accepted backend. This is the review inventory
required by the [Caddy application owner](../../../homelab-server-configs/Caddy/docs/APPLICATION_ONBOARDING.md),
not an approved production release. Candidate files remain in
[`uptime-kuma/proposals`](../../uptime-kuma/proposals/).

| Field | Prepared choice and acceptance |
| --- | --- |
| Application/owner | Uptime Kuma; homelab-monitoring-observability. |
| Public name/fragment | Approved `uptime.local.theama.co`; `conf.d/20-uptime-kuma.caddy`. |
| Client listener | HTTPS on existing Proxy VIPs `10.1.0.56` and `fd36:5aa8:6971:1::56`, plus protected `NODE_IPV4`/`NODE_IPV6` bindings for independent per-node acceptance. Client ACLs remain unchanged. |
| Client TLS | Preserve the complete accepted TLS inventory and existing trust model. Verify leaf/fullchain identity, validity, hostname coverage and trusted client chain before publication. No key export, certificate replacement or disabled verification. November 11 read-only inspection verified hostname coverage, matching leaf/fullchain fingerprints on both nodes and validity through January 19, 2027 23:59:59 UTC; client chain/handshake acceptance remains pending. |
| Backend/TLS | HTTP to `10.1.3.75:3001` and `[fd36:5aa8:6971:1::75]:3001`; backend TLS/SNI/CA not applicable. Keep accepted source guards. |
| Availability | One application with two addresses, `first` policy; IPv4 preferred, IPv6 alternate. This provides no second application replica. Test each backend family independently. |
| Active health | GET `/dashboard`, exact 200, every 30s, timeout 3s, one pass/three failures. Root `/` redirects after account creation and is not the health endpoint. This is HTTP availability, not authenticated application acceptance. |
| Passive health | Disabled (`fail_duration 0s`); retained `max_fails 1`/`unhealthy_status 5xx` do not activate exclusion. Do not exclude the sole application for normal login rejection. |
| Transport | Dial 3s, response headers 60s, HTTP keepalive off. No automatic login replay. Verify WebSocket upgrade and continued application use separately. |
| Request headers | `Host uptime.local.theama.co` for requests and health checks; standard Caddy forwarded headers; no additional overrides. |
| Authentication | Kuma-owned existing administrator. No bootstrap/account reset. Operator privately verifies wrong-password rejection, immediate correct retry, authenticated page, logout, and WebSocket use over each client family; secrets and request bodies stay out of evidence. Staging must first establish the exact rejection/session contract with synthetic credentials. |
| Clients | Direct clients in `10.1.0.0/22` and `fd36:5aa8:6971:1::/64`; other clients 403, unknown hosts retain 421. No inferred VPN/public access or forwarded-header ACL. |
| DNS | Six append-only records in the proposal: dashboard A/AAAA to Proxy VIPs; host A/AAAA and IPv4/IPv6 PTR to the Pi. Preserve Proxy PTRs and every unrelated record. |
| Recovery | DNS owner restores each node's exact saved bytes with both full restarts. Caddy owner restores the preserved immutable parent through its reviewed activation/recovery path. Do not uninstall or stop the accepted Pi backend as DNS/Caddy recovery. |

Prepare the two owner operations separately; do not bypass either owner's
approval or combine their mutations into the Pi installer. Preserve protocol-v2
transfer/finalization, the original candidate parent and all TLS files. Activate
and verify Node A before exposing that exact revision to managed replication.
Node B independently validates, activates and checks it. The current repository
implementation is locally qualified. The current exact operation, evidence and
approval state are recorded in WORK.md. Installed production and acceptance
records remain unchanged until a separately approved execution passes.

Prefer Caddy route acceptance using explicit hostname/address resolution before
DNS publication. Complete private login/WebSocket acceptance outside the release
transaction, without a timed human receipt or rollback solely for operator delay.
Credentials remain in the operator's terminal. Node B rejection or timeout leaves
a partial outcome with healthy Node A retained; it does not authorize DNS or
prove complete HA acceptance. Unknown mutation or recovery requires manual
reconciliation from retained evidence, never replay or assumed rollback.

After Caddy acceptance, apply the six-record addition through the DNS owner's
atomic per-node transaction, current non-owner first. Fully restart Unbound,
verify it, then fully restart Pi-hole DNS on each node, including rollback.
Allow normal cluster-driven movement of the coupled four VIPs within the owner
contract; no forced failover or concurrent node restart. Reuse existing DNS
qualification; add no DNS fixtures or simulated failover tests. The existing
conditional DNS approval remains unused with its original expiry; this plan
neither renews it nor accepts a revised Caddy operation.

Final acceptance requires trusted HTTPS over both client families, the private
authentication sequence, a usable second client, actual WebSocket acceptance,
preserved existing sites/DNS and coherent VIP ownership. Retain bounded repeated
HTTP/WebSocket checks across at least two configured active-health intervals and
check for health failures or backend exclusions. This does not claim observation
of every successful Caddy active-health request. Under the approved streamlined
design, unrelated platform monitor-cycle observation and the ten-minute private
receipt gate are removed from routine release activation. Platform qualification
remains with its owner; private application acceptance remains required for
onboarding completion.

W-020 remains network-owner work: retained startup/reboot checks establish
addresses/routes, not a separately timed RA renewal. W-076 remains host/network
ownership work: retained wlan0 DOWN and resident radio daemons do not establish
persistent radio disablement or justify removing services. Neither finding
authorizes an unrelated network/radio change, and neither is silently waived
by DNS/Caddy success. Keep both tracked until evidenced or explicitly deferred
with an agreed acceptance decision. This plan grants no live authority.
