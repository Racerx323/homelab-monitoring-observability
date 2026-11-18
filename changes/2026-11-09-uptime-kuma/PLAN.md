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
   production acceptance is recorded in W-102/W-106 and W-124.
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

## Boot continuity policy — approved November 12, 2026

Aaron approved using boot IDs only for continuity within an operation. Future DNS
admission authenticates each host, captures its current boot ID and independently
checks the approved configuration and service/DNS readiness. A routine reboot
before admission does not invalidate the candidate merely because its boot ID
differs from preparation or historical evidence. Later phases must match the
admitted IDs; an unexpected reboot stops progression for reconciliation, including
whether recovery remains safe. Resuming an operation does not reset its admitted
IDs. Explicitly planned reboots require their own approved transition and acceptance.

This revises the future DNS contract. W-122 source implementation and local
qualification are complete; a new candidate must explicitly select
`boot_policy: operation-admission-v1`. Retained consumed scripts keep their
original historical-ID contract. Preserve all
consumed bundles and failures. Policy agreement does not authorize a live retry,
reboot, or deployment. The workspace and DNS AGENTS.md instructions carry the
permanent rule; WORK.md tracks implementation and evidence.

## DNS and dashboard acceptance — November 12, 2026

W-124 records the accepted secondary-first DNS operation using fresh admission
and operation-scoped boot continuity. Both nodes serve the six records; paired
DNS/service gates and normal-name trusted HTTPS `/dashboard` checks passed over
IPv4 and IPv6. Together with W-106 accepted private login/WebSocket and passive
observation, this satisfies AC-004. Existing service/backup acceptance is retained.
W-020/W-076 and permanent-document reconciliation still prevent project closeout;
W-096 remains deferred. Approval is consumed and grants no further live work.

## Closeout reconciliation — November 12, 2026

[RESULT.md](RESULT.md) records a Partial outcome from retained acceptance.
The service, foundation and dashboard are accepted; W-020 timed RA renewal and
W-076 host/network ownership disposition remain open under AC-008. AC-010 and
W-012 await those dispositions. Radio softblocks are evidenced before/after
reboot and at promotion; no daemon removal or hardware-disable claim follows.
This reconciliation changes no requirement and grants no live authority.

## Proposed final acceptance disposition — awaiting agreement

The [W-127 decision](WORK.md#proposed-w-020w-076-acceptance-decision--november-12-2026-w-127)
proposes accepting the evidenced radio softblocks with unchanged services, and
explicitly deferring timed RA-renewal proof to the network owner before the next
host networking/container-runtime migration or an earlier reported IPv6 failure.
This would accept initial-deployment network preservation from existing startup,
reboot and promotion checks while retaining the unmeasured-renewal risk. It is
not yet approved and does not change current AC-008/AC-010 results. No live action,
requirement waiver or project closure follows from this proposal alone.

## Final acceptance decision — approved November 12, 2026

Aaron approved W-127 for initial-deployment closeout. Accept observed radio
softblocks across reboot/promotion with existing services unchanged (W-076
Resolved). Accept initial-deployment network preservation from retained startup,
reboot and promotion checks; defer timed RA-renewal proof (W-020) to the network/
runtime owner before the next host networking/container-runtime migration, or
earlier if IPv6 route/address loss is reported. Retain this follow-up in W-020.
The risk of an unobserved later renewal failure is explicitly accepted; the
measurement is not marked passed. No sysctl change, forced renewal, reboot or
live inspection is authorized. This decision supersedes the pending proposal
and prior partial-closeout assessments above. AC-008/AC-010 pass within this
agreed boundary; W-096 stays deferred and future workload remains separate.

## Webmin browser access — requirement added November 12, 2026

Aaron rejected tunnel-only Webmin administration. Provide a normal trusted HTTPS
browser URL through the existing Caddy pair and dedicated DNS if needed, without
requiring a workstation SSH tunnel. Preserve Pi-account authentication, existing
Kuma access, resource limits and unrelated fleet configuration. W-127 dispositions
remain approved; they do not authorize a Webmin/Caddy/DNS execution.

| ID | Required observed outcome | Verification method and evidence required |
| --- | --- | --- |
| AC-013 | Webmin is usable from an ordinary LAN workstation browser through the trusted fleet hostname and VIP. | Verify both client families reach the VIP and the replicated route is healthy. In one existing-account browser session verify redirects/assets, login, live statistics WebSocket, logout and protected-page denial. Preserve restricted ingress, verified backend TLS, working recovery and unrelated routes. Assess Pi capacity and guarded scan coexistence separately before permanent service promotion. |

AC-011's earlier package/loopback acceptance remains evidence, but the revised
management-access policy also requires AC-013. Local preparation is authorized;
any live inspection or deployment needs its concrete owner-governed scope.

The browser-access workflow is fleet-wide and reusable. The approved first URL
is `https://webmin-j2-svpi3bmf.local.theama.co`. Webmin owns the shared profile,
backend restriction and [operator procedure](../../../homelab-server-configs/Webmin/docs/OPERATIONS.md);
Caddy retains its existing primary-first replication path and DNS retains its
owner transaction. SSH is optional recovery only. Other hosts require explicit
selection and their own baseline/acceptance; this task grants no fleet-wide live
access. No duplicate publisher, replication engine or project ledger is created.

## Fleet DNS procedure — requirement added November 12, 2026

All fleet DNS additions, updates, deletions and other changes must enter through
[the existing DNS owner procedure](../../../homelab-dns/Unbound/docs/host-record-deployment.md).
Adapt that procedure in place, preserving its qualified atomic transaction,
operation-scoped boot continuity and owner boundaries. Webmin and future
application onboarding link to it. Broader resolver/package/HA changes select
the appropriate owner runbook there; unsupported record types require explicit
implementation qualification. No new application-specific DNS orchestrator.
W-129 tracks documentation/routing, while W-128 retains Webmin implementation
and live acceptance. This requirement grants no inspection or deployment authority.

## Target qualification boundary — November 12, 2026

Aaron approved preparation of a bounded actual-host qualification after reviewing
fixture evidence limits. Local tests establish configuration behavior and defects;
they do not accept or reject j2-svpi3bmf capacity. W-135's fixture failures remain
risk evidence, not a requirement for another fixture capacity pass. Correctness,
authentication, ingress, resource controls and recovery requirements remain.
No live action is authorized by this strategy decision.

Prepare the following operation through the existing Webmin, Caddy and host owners:

1. Reconcile readiness once: exact installed Pi unit/drop-in identities, effective
   controls, native module availability and terminal ACL disposition; both proxies'
   current routes to both Pi addresses, accepted release identity and certificate
   coverage. A read-only capture is separately reviewable because retained evidence
   lacks these inputs. Fresh operation-start boot IDs provide continuity only.
   Drift stops preparation for owner review; no historical boot ID is required.
2. Bind exact before-files and backups, source-restricted browser profile, guard,
   native start dependencies and Caddy child release. Reuse configure-miniserv.py,
   the profile renderer, native Ansible/systemd and Caddy primary-first publication.
   Do not replay the original installer, rebuild a fixture, add a publisher or
   change accounts, caps, reserve, packages, startup authority or unrelated routes.
3. Apply guard before opening the selected backend listener. Verify both backend
   families from each proxy and actual Pi-observed sources/counters; verify a
   selected unlisted client's denial. Keep strict TLS through Caddy, selected
   hostname and both node addresses. Normal dual-upstream production policy stays
   intact: direct backend checks prove each upstream family, while per-node browser
   checks prove proxy integration. Do not publish successive production releases
   merely to force upstream families for a test.
4. Start measurement only after Aaron is ready for private browser acceptance.
   Use one browser on the workstation; no Chromium on the Pi, no synthetic account,
   no password/session capture and no mandatory wrong-password attempt against the
   real account. Test ordinary login, dashboard/assets, the protected referrer page,
   logout and session invalidation on each frontend family/node. Confirm applicable
   WebSocket behavior only through a reviewed existing-account capability; never
   launch a root terminal merely as a probe. Bind any missing capability disposition
   before sealing; do not silently mark required WebSocket acceptance passed.
5. Bound workload observation to ten minutes, including a 30-second unloaded
   baseline and at least 95 seconds of ordinary authenticated use with both proxies'
   normal health checks running. Sample once per second: host MemAvailable, Webmin/
   Kuma/proxy cgroup usage/events/pressure, restart counters and sampler overhead;
   correlate browser/HTTP timings without capturing bodies or secrets. Reuse the
   existing sampler's passive function, not its extra HTTP probe loop. One scheduled
   needrestart scan may overlap only through the already accepted guard/observer;
   do not add a second scan or competing sampler. Capture scan admission and reserve.
6. Preserve the accepted 128/192 MiB Webmin high/max and no-swap controls, Kuma and
   loopback-proxy caps, staged scan admission (224 MiB before observer; 192 MiB after)
   and 96 MiB sampled host reserve. Startup's 624 MiB admission applies only at its
   defined stopped-service boundary; do not require it while accepted services run.
   Stop load on reserve breach, OOM/max event, restart, missing safety samples,
   guard/source drift, operator abort, browser failure or proxy timeout. Record
   memory-high/PSI with latency; high events alone neither pass nor fail capacity.
   No extended timeout or assumed overhead correction may turn failure into a pass.
7. Arm host-side bounded recovery before mutation, independent of controller
   connectivity, using native systemd/Ansible recovery. Restore only this change:
   stop Webmin, restore exact saved configuration and unit/drop-in state, verify
   loopback listeners and health before removing only the added Webmin guard.
   Preserve Kuma/data/accounts and unrelated firewall tables. Caddy uses its owner
   recovery for the added route; DNS remains unchanged during qualification. If
   restoration fails, keep backend restriction and report recovery incomplete.
   Operator availability is confirmed before the measured trial; waiting for the
   operator outside a trial is not a release-transaction failure.
8. Accept only the measured target workload with complete observations and verified
   recovery/disposition. No claim of unlimited or long-running capacity. Failed
   capacity leaves DNS pending and retains evidence; no automatic retry. Successful
   target/application acceptance permits preparation of the separate DNS owner
   change and normal-name verification, not automatic DNS execution.

The concrete mutation bundle remains unsealed until installed identities, actual
sources, browser capability and exact recovery bindings are reconciled. The
readiness capture grants no backend mutation, browser load, restart, publication
or DNS authority. It is preparation for one bounded trial, not a capacity verdict.

### First-host trial bindings after readiness capture

Use W-137's November 12 accepted capture in
`webmin-target-readiness-fe7cvab0/attempt/` as preparation evidence. Preserve the
consumed bundle. Recheck relevant identities at the future operation's preflight;
capture fresh boot IDs and enforce continuity only within that operation.

| Boundary | Prepared binding and remaining work |
| --- | --- |
| Target and frontend | Native hostname j2-svpi3bmf; ama@10.1.3.75; backend addresses 10.1.3.75 and fd36:5aa8:6971:1::75, port 10000; approved browser name webmin-j2-svpi3bmf.local.theama.co. |
| Installed controls | Bind the three installed file hashes recorded in W-137: vendor webmin.service, 10-fleet-foundation.conf and 60-startup-authority.conf. Preserve the latter two and all effective controls; add only the reviewed ingress dependency. Repository identity is not installed identity. |
| Proxy sources | Node A selects 10.1.0.53 and fd36:5aa8:6971:1::56; node B selects 10.1.0.54 and fd36:5aa8:6971:1::54, all via eth0. The proposal's additional ::53 is a node-owned address, not an observed selected source in this capture. Reconcile its intended role explicitly; do not claim failover acceptance. |
| Caddy parent | Bind accepted release 20261111T213048Z-71b7deb8-bc71-45d5-8f33-98270af79d3b and manifest identity from W-137. The proposal remains outside production; prepare the exact child through the existing Caddy owner entrypoint. Certificate coverage passed, but target trusted-browser acceptance is pending. |
| Backend producer | Reuse Webmin/scripts/render-proxy-profile.py and configure-miniserv.py with the reviewed first-host profile. Preserve authentication, collect_pkgs=0, unrelated settings and loopback access; install the source restriction before opening network listeners. |
| Browser capability | Aaron confirms existing ama access to System Information and real-time statistics graphs. Select that native statistics WebSocket, not xterm. Permission and traffic must still pass during actual acceptance; no account/ACL or statistics setting changes. |

The reusable acceptance requirements live in
[the fleet Webmin procedure](../../../homelab-server-configs/Webmin/docs/CADDY_ONBOARDING.md#safe-websocket-method-for-each-host).
For this host, use the existing Authentic Theme System Information graphs.
Aaron confirms both the page and real-time graphs are already available to ama;
this is operator-reported capability, not a new live permission inspection.
The pinned native stats endpoint checks System Status access and authenticates
its WebSocket session. Do not visit xterm: the retained terminal implementation
starts a shell before accepting its connection.

Use an isolated workstation browser session with trusted TLS and the approved
hostname, following the Caddy owner's pre-DNS route selection. At each reviewed
node/frontend-family path, log in privately, open System Information, observe an
authenticated wss upgrade and continuing graph updates for at least 95 seconds
without administrative actions, then close that test connection and log out.
Verify that the prior session cannot access the protected page. Retain connection
status, timing and frame counts only; do not export frames, cookies, HAR files,
screenshots of private data or credentials. Permission denial or absent native
statistics traffic stops acceptance; no fallback to a terminal or ACL edit.

Preserve the graph interval/history and shutdown settings. The collector can
register a loopback backend and write ordinary statistics cache/history; include
that work in observation. Do not invoke global statistics shutdown/disable, which
can affect other clients. Close only trial-owned browser sessions. The selected
trial ends by restoring loopback through native Webmin recovery; its service stop
also ends the collector under the reviewed maintenance scope. Do not claim that
closing one tab necessarily stops a shared collector. Normal graph availability
and target resource acceptance still require the authorized trial.

### Native backend execution and recovery binding

This is an active loopback baseline, not the stopped baseline used by the earlier
installation diagnostic. Do not reuse that diagnostic's stop/disable/permit-removal
disposition. Preserve accepted startup authority, enabled state and unrelated Kuma
services throughout the new recovery design.

| Failure boundary | Required disposition |
| --- | --- |
| Before mutation | Stop with bounded expected/observed diagnostics; remove only trial-owned staging. Do not restart an unchanged service. |
| Backend changed, controller lost or deadline reached | A pre-armed native host-side recovery action stops Webmin, restores the exact saved config and changed unit/drop-in before-state, reloads systemd as needed and restores the prior active loopback service. Verify loopback-only listeners and HTTP health before restoring the previous guard state. |
| Recovery cannot prove loopback restoration | Keep the restrictive guard, stop further workload, retain diagnostics and report recovery incomplete. Do not expose the old or new network listener by removing protection. |
| Caddy child partly or fully activated | Use the Caddy owner's recorded recovery/partial-state procedure for this child. Preserve unrelated routes/TLS and record each node's resulting release. Backend recovery must remain effective even if Caddy/controller recovery is unavailable. |
| Trial completed | Verify application/resource results and explicit accepted-or-restored disposition before disarming recovery. DNS remains unchanged and separately governed. |

The reusable backend includes are now implemented as
[proxy-trial.yaml](../../../homelab-server-configs/Webmin/ansible/proxy-trial.yaml)
and [proxy-trial-restore.yaml](../../../homelab-server-configs/Webmin/ansible/proxy-trial-restore.yaml),
using [recover-proxy.py](../../../homelab-server-configs/Webmin/scripts/recover-proxy.py).
The private preparation directory is
`webmin-trial-preparation-h3qt9wvn/`: binding.json contains installed config/unit
hashes, metadata and normalized effective controls from W-137; miniserv.json,
webmin.json and ingress.nft are generated by the existing profile renderer.
This directory is preparation, not a sealed or executable parent operation.

Proposed host storage is `/run/webmin-proxy-trial/webminfirsthost`, root-only 0700;
config-0.before/config-1.before and state.json are root-only 0600. The binding
requires exact installed FragmentPath/all DropInPaths and the observed config
identities. Existing ingress artifacts or an inet webmin table reject before
mutation. The extra allowed ::53 remains Node A's captured permanent address;
retaining it is a proposed role-preservation choice, not post-failover acceptance.
Fresh route-selected sources must still match before any exposure.

The native apply service has a 180-second start/15-second stop deadline; the
independent recovery timer starts before apply and expires at 1800 seconds with
one-second accuracy. Recovery has 300 seconds. Each helper is capped at 48 MiB,
no swap and 64 tasks. These are control bounds, not measured Pi overhead. The
parent must allocate the Caddy stage and ten-minute workload within that deadline.
Recovery stops the apply service before locking/restoring, and a cancelled or
restored state rejects late apply. An expired transient apply unit is accepted
only as the exact not-found state. All backend writes occur in the native service;
Ansible stages inputs before arming and cannot resume configuration writes later.

This qualification trial restores loopback even after a passing workload; it does
not promote an unreviewed final browser deployment. The finish include verifies
restored state before stopping the timer. The timer survives controller loss,
not reboot/power loss. No reboot is included. Preserve the before-state and
receipts, and report unexpected reboot or incomplete recovery for owner handling.

Before sealing the combined trial, bind and qualify the Caddy child/recovery and
pre-DNS browser paths, real-source/guard observations, and the passive resource/
guarded-scan acceptance path. Neither parent boolean gates nor these backend
includes implement those missing owner checks. No parent operation or live
command is sealed, and no inspection or execution authority is implied.

### Combined trial owner integration

The parent remains unsealed. Reuse the existing Caddy outer
`Caddy/scripts/run-serving-health-deployment-outer.sh` and its neutral transaction;
Webmin's Ansible includes must not publish or select Caddy releases themselves.
The owner recipe now supports the exact Webmin proposal source and basename.
Keep accepted production inventories unchanged while preparing the trial.

| Parent phase | Owner entrypoint and required evidence |
| --- | --- |
| Admission | Exact installed unit/config/guard identities, fresh operation boot continuity, current route-selected sources and operator readiness. Historical readiness is preparation, not permission to contact targets. |
| Backend preparation | Webmin `proxy-trial.yaml`: private snapshot, independent recovery timer, bounded native apply. Its readiness flags must be backed by the admission results. |
| Real backend paths | One request from each proxy to each backend family, with route-selected source and target-side allow/deny evidence; reject drift before publishing. No forced-family production release or second backend pool. |
| Proxy activation | Existing Caddy primary-first outer: one original parent and child, primary acceptance before exposure, secondary and shared-endpoint acceptance. Preserve restoration inputs until the temporary trial ends. |
| Application/resource trial | Existing ama System Information statistics method, trusted per-node/VIP paths before DNS, bounded timings and phase-correlated service/cgroup/host observations. One guarded scan with the accepted staged thresholds and a single observation owner. |
| Finish or failure | Stop owned browser load. Contain transport of the exact Caddy child, restore and verify both prior selections and unrelated routes through the Caddy owner, then invoke Webmin `proxy-trial-restore.yaml`. Backend deadline recovery acts independently even if Caddy recovery cannot complete. |
| Terminal decision | Report workload acceptance separately from both recovery results. Missing or failed recovery is incomplete/manual intervention, never a passing trial. Preserve all receipts and source identities; no DNS or permanent browser-profile promotion. |

W-140's application-owned paired restoration is locally qualified through the
actual offline primary-first entrypoints, including incomplete transfer,
post-exposure lost reply, failed restoration and late exposure rejection. Use
[Caddy's temporary trial interface](../../../homelab-server-configs/Caddy/docs/APPLICATION_ONBOARDING.md#temporary-application-trials).
Its 660-second window and machine finish signal do not establish application
acceptance. Controller loss can leave paired Caddy recovery incomplete; native
backend deadline recovery remains independent.

W-141's resource/scan component now stages reviewed source and profile without
reinstalling the accepted guard. One existing locked observer covers baseline,
workload and scan; 224/192/96 MiB thresholds and caps remain unchanged. See the
[foundation interface](../../../homelab-server-configs/foundation/README.md#combined-workload-observation-without-changing-the-installed-guard).
Local tests establish sampling, admission, failure and cleanup control flow, not
this host's capacity. W-137 still must bind the parent to actual source/path and
browser receipts, prove workload/scan overlap, stop owned load on failure, and
join both recovery outcomes before sealing. No boolean or finish signal replaces
those receipts. No parent operation or live command is sealed.

### November 16 preparation checkpoint

Crash reconciliation found the combined parent/path/workload drafts present but
not qualified as one final revision. The existing acceptance above is unchanged:
all reviewed browser paths require the specified sustained observation, prior
sessions must lose access after logout, and the scan must overlap the selected
paired workload. Current draft gaps and exact-input qualification remaining are
tracked in [WORK.md](WORK.md#november-16-crash-status-reconciliation-w-137w-141w-143).
No sealed parent or live authority results from this checkpoint.

### Combined implementation qualified locally, November 16

The parent now joins native backend recovery, the Caddy temporary-trial interface,
actual-path collectors and the single observer. Browser implementation matches
the existing all-six-path duration and prior-session rejection requirements.
See [the reusable contract](../../../homelab-server-configs/Webmin/docs/CADDY_ONBOARDING.md#combined-parent-and-browser-receipt-contract)
for native navigation, bounded pairing and clock-bracket acceptance. Local tests
qualify these contracts and failure ordering; they do not establish host capacity
or native UI acceptance. Final Caddy owner/input bindings and live review remain
before the trial. No threshold, deadline, workload criterion or authority is waived.

### First-host combined trial candidate, November 16

The sole Caddy operation is `20261116-webmin-first-host-trial`, defined in the
existing owner manifests. The private parent inputs and operator handoff are in
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-combined-review-0ve83yjr`.
The ledger records the final seal, qualification and exact approval command;
this preparation grants no live authority.

The operation covers ama at `10.1.3.75` and pi at `10.1.0.53`/`10.1.0.54`, using
accepted SSH keys, exact native host/configuration/control checks and fresh
operation boot continuity. Reviewed readiness binds retained evidence, not a
waiver of current admission. Route/socket/counter checks must confirm the bound
proxy sources and both direct-client denial paths after guarded backend exposure.

The existing parent temporarily configures the Webmin backend and ingress guard,
then invokes the Caddy owner to add only the selected Webmin fragment to the
accepted release. Primary activation/verification precedes managed replication
and independent secondary acceptance. Existing TLS, Kuma and unrelated routes
remain covered by owner checks. No installed Caddy tool is replaced.

The workstation client privately authenticates as ama over both address families
on each proxy and both VIPs, using the approved name without changing DNS. It
opens only native System Information statistics, with two simultaneous clients,
at least 95 seconds on every path and a 180-second final pair. Logout must
invalidate each owned prior session. The one existing scan observer covers the
600-second resource window and one list-only scan, gated by actual paired
readiness with a 400-second readiness deadline. Every running scan sample
must overlap both final clients. Missing overlap, slow readiness, resource
failure or incomplete cleanup fails the trial; no time extension or retry.

Webmin remains at 128/192 MiB high/max, Kuma at 256/320 MiB and its loopback
helper at 16 MiB max, with zero swap. Scan admission stays 224 MiB before the
observer, 192 MiB afterward, and 96 MiB sampled reserve. Caddy exposure is
bounded to 660 seconds. The backend's independent 1800-second recovery timer,
300-second recovery limit and 48 MiB helper limit remain unchanged.

On success or failure, stop owned browser load, cancel/finish the owned scan,
restore the paired Caddy baseline and outgoing inventories through its owner,
then restore the exact Webmin loopback baseline. Verify both owners separately.
The parent retains independent outcomes even when Caddy recovery is incomplete;
controller loss can still require manual Caddy recovery. A successful trial does
not leave browser ingress promoted or prove long-term capacity.

The private operator command verifies the non-secret manifest and owner gate
before prompting. Its interactive invocation confirms readiness only after
exact-bundle approval. The password is an external owner-private runtime file,
created exclusively and removed after parent exit; never enter it in chat.
Preserve the one-attempt marker and receipts on failure. No DNS, reboot, forced
failover, account/ACL change, terminal workload, resource-limit change, permanent
promotion, consumed-operation replay or Git publication is included.

### W-147 diagnostic successor boundary

Prepare one temporary route diagnostic using the existing combined parent with
`proxy_trial.diagnostic_only: true`. Admit fresh boot continuity and exact installed
controls, qualify direct dual-stack backend sources and denial, then activate the
reviewed Caddy fragment through its existing primary-first owner. On failure retain
bounded safe timing/journal evidence before recovery. On successful readiness,
signal finish immediately. Retain a timestamped later backend resource snapshot
and verify paired Caddy restoration and exact Webmin loopback restoration.

No password, browser, scan, monitor/notification, DNS, reboot, forced failover,
resource-cap change or permanent promotion is included. Existing 660-second Caddy
exposure safety deadline and 1800-second independent backend recovery timer remain;
normal successful diagnostic readiness ends exposure immediately. Controller loss
can still require manual Caddy recovery. AC-013 remains pending even if this
diagnostic passes. Source preparation grants no live authority; use the exact
bundle/command review in WORK.md before one execution attempt.

### Post-restoration monitor acceptance for future trials

Use the existing Caddy trial recovery and its locally qualified W-166 monitor
phase. Follow the shared application-onboarding procedure's post-restoration
acceptance boundary; distinguish restored service from completed monitor
acceptance. The next exact candidate must fit activation, workload/diagnosis,
restoration, observation and readback within unchanged parent deadlines. This
source integration does not authorize a successor or resolve AC-013.

### Diagnostic timing and resource evidence before sealing

Use the existing diagnostic-only parent and collector. A random ID binds each
Caddy client probe to its sanitized native access record and upstream timing.
Webmin's upstream latency is observed by Caddy; it is not an internal CGI phase
trace. Missing upstream timing is unknown, including cancellation before headers.
The target sampler records one-second memory/event intervals with boot/cgroup
continuity. No credential, browser, scan or notifier workload is added.

| Existing bound | Required interpretation |
| --- | --- |
| Client request: 5 seconds; connect: 3 seconds | Unchanged; do not extend to obtain a response. |
| Journal projection: 3 seconds, 128 entries, 64 KiB input | Capture before recovery; retain failure status and incomplete evidence. |
| Resource observation: 300 seconds, one MiB | Require compared requests to fall within the observed interval; no implicit restart or extension. |
| Caddy recovery monitor: completion within 150 seconds of each resume | Both nodes resume first; retain bounded-query/readback overhead in the whole-operation budget. |
| Caddy child: 1200 seconds; terminal wait: 900 polling retries | Reserve restoration, monitor observation and readback inside the 840-second owner budget; retries are not a wall-clock bound. |
| Caddy exposure: 660 seconds; backend recovery timer: 1800 seconds | Safety backstops, not additional execution time or permission to defer normal recovery. |

W-168 binds wall-clock cancellation/containment for stalled owner commands and
clock-offset uncertainty for comparing proxy and Pi intervals.
SSH connect/keepalive settings do not establish a whole-command bound. Missing
coverage, unknown cross-clock order or incomplete recovery remains unknown/failure;
do not turn event proximity into OOM attribution. This preparation changes no
accepted host state and does not resolve AC-013.

W-168 local implementation binds diagnostic forward work to 240 seconds and the
whole Caddy diagnostic/recovery path to an aggregate 840-second admission
boundary. The existing child limit and terminal retry count remain unchanged;
terminal retries are not themselves a precise wall-clock timer. Remote process
groups, local SSH and uploads now receive bounded execution time inside that
budget. A timeout is not proof of remote quiescence; missing independent owner
recovery evidence remains incomplete/manual intervention. W-166 observation uses
the recovery reserve, never a renewed forward window.

The private diagnostic specification binds three reviewed SSH prefixes for fixed
read-only clock queries before sampling and after collection. Boottime/boot IDs,
controller round-trip intervals, request-index readback hashes and resource
intervals feed the existing handoff verifier. Its output is an estimated offset
envelope with explicit unobserved intervening drift and no causal attribution.
Unknown coverage cannot pass. The shared Webmin onboarding procedure owns the
repeatable command limits and evidence rules. A successor still requires exact
input/owner bindings, local qualification and separate live authorization.

W-168 implementation and focused qualification are complete locally. The ledger
retains exact qualification evidence. W-169 prepares the exact successor using
these bindings; its seal and any execution authority belong in WORK.md. These
source bindings grant no live access and do not establish the timeout cause.

### Narrow primary-only request diagnosis (W-174)

Aaron approved this replacement diagnostic scope on November 16. It supersedes
the earlier dual-stack/paired diagnostic workload for the next candidate, not
the preserved consumed attempts or final Webmin acceptance requirements.

Question: where does one unauthenticated login-page response stall between the
primary Caddy frontend and the Pi? Limit target work to Node A and the Pi, IPv4,
using the existing backend guard and Caddy owner mechanisms. Do not expose the
candidate to replication, contact the secondary, alter DNS, authenticate, launch
a browser/scan, move VIPs or promote the route. A successful request ends diagnosis;
it must not advance the existing onboarding coordinator to secondary exposure.

Use one direct request followed by one proxied request for `/session_login.cgi`,
with the same method, public Host and relevant forwarded headers. Send no cookies,
credentials or request body. Retain only an allowlisted projection of the headers
actually reaching the backend; do not retain arbitrary traffic or headers. The
candidate must specify a safe native way to obtain that projection and backend
request arrival/completion before sealing. Caddy's selected upstream label alone
does not prove delivery to Webmin. Missing phase evidence remains unknown.

Use only the IPv4 upstream in the temporary diagnostic fragment. Preserve the
existing health-check method/path, interval and timeout for that upstream and
observe its overlap with the foreground requests; do not silently disable checks.
The foreground requests are sequential, not a claim that background work is
serialized. This isolation changes the prior dual-address workload: a pass is
not proof of the historical failure's cause or acceptance of the dual-stack route.
Do not add a custom serial health-check scheduler or select production health
policy without evidence. A controlled follow-up may vary one demonstrated factor
under its own reviewed scope; no automatic retries or extra comparisons follow.

Correlate client connect/TLS/first-byte/total time, Caddy upstream timing when
available, Webmin request arrival/completion and concurrent health requests with
the existing bounded Pi sampler and cgroup identity/event deltas. Distinguish
memory.high pressure from hard-limit/OOM events. Preserve clock uncertainty and
coverage checks. Keep five-second request deadlines, resource limits, forward
240-second and aggregate 840-second recovery/readback bounds, and existing
independent recovery backstops; do not extend them to manufacture a response.
Stop after the request pair, or earlier on a safety failure, and restore.

Reuse the existing primary preparation/activation and restoration mechanisms.
Before sealing, ensure their selected path cannot publish, mutate or inspect
Node B; document precisely which Node A services it touches. Preserve recovery
checks for those actual changes, including a subsequent natural monitor cycle
if synchronization was stopped/resumed. Do not repeat replication acceptance or
paired restoration for an untouched secondary. If the owner cannot express this
scope safely, correct that existing path locally rather than adding a competing
transaction framework or silently expanding target scope.

W-173 archival precedes changes to executed owner inputs. W-171's failure-path
handoff must work for the next diagnostic. Focus local tests on the changed
request/header contract, primary-only stop boundary, safe evidence and recovery;
no new load fixture can accept or reject Pi capacity. This is approved design,
not a sealed executable or exact-bundle live authorization. AC-013 remains pending.

W-174 implementation status, November 16: primary-only execution and recovery
controls are locally qualified after W-173 archival/W-175 cleanup. W-171's failed
handoff is corrected. W-176 now adds bounded backend-interface observation in the
existing collector. Bind its exact source and the temporary health-marker fragment
in each separately reviewed primary/IPv4 candidate. Its exact command and authorization status
are owned by WORK.md; defining or sealing it does not grant live authority.

For the selected native 64-bit Linux host, the observer requires a root packet
socket with nanosecond kernel timestamps on `eth0`. It starts before either
foreground request and shares the existing 300-second resource observer. Only the
reviewed primary IPv4/backend port pair is parsed. No packet file, credentials or
body is retained; only reviewed header matches, request markers, response status
and connection-close events survive. The exact implementation bounds buffers,
connections, records and duration; resource limits and parent cutoffs are unchanged.
Failure to initialize capture prevents readiness. Loss, gaps, unsupported streams,
missing receipts and out-of-window evidence prevent a complete diagnostic claim;
owner restoration still runs.

This boundary proves packets reaching/leaving the backend interface, not Webmin
accepting them in CGI code. Connection close/reset does not establish full HTTP
body completion. Missing response events remain unknown. Correlate both marked
foreground requests and marked health probes without attributing resource events
causally. No conclusion about the Pi's capacity or the historical timeout follows
from local qualification. AC-013 remains pending.

Routine onboarding package transport (W-177): only the primary receives the
application fragment and publisher. The secondary receives a control recipe for
expected identities and recovery, then obtains the application through existing
replication after primary verification. The narrow diagnostic excludes even that
secondary control transfer, admission and recovery. No installed notifier or
accepted production route changes are included.

W-181 local source reconciliation: direct and proxied diagnostic requests and
backend header comparison use the same neutral User-Agent. Browser readiness
still requires HTTP 200/login content. If the direct prerequisite fails before
Caddy starts, the comparison is explicitly not run and cannot pass acceptance;
backend evidence/recovery still complete. The unexecuted W-178 child is withdrawn
and owner bindings are neutral/inactive. A future candidate requires new exact
operation/parent bindings and qualification; consumed approvals cannot be reused.

W-182 prepares a new primary/Pi diagnostic from W-181's corrected sources.
The owner operation is defined but unexecuted; its current exact bindings and
command belong to WORK.md. Neutral User-Agent and HTTP-200/login requirements,
primary-only IPv4 transport, 240-second forward/840-second aggregate child
cutoffs, independent backend restoration and all workload exclusions remain.
Admission must revalidate current host/configuration/health and capture fresh
boot continuity; retained readiness does not establish current target health.
No live authority follows from definition, local qualification or sealing.

W-187 retained-evidence reconciliation, November 17: before any successor,
reconcile the published terminal archive to neutral and qualify W-184's explicit
no-observed-payload connection classification. Preserve rejection of partial HTTP,
missing markers, capture loss and incomplete clock/resource coverage. Trace the
observed eight-request startup health burst before choosing a single-factor target
comparison. Retained evidence establishes pressure during the request and a later
OOM kill, not causation or fleet capacity. Keep existing caps, request deadlines
and recovery; no new inspection or live comparison is authorized by this analysis.

W-188/W-184 completion, November 17: the published archive is reconciled to clean,
inactive owner bindings. Close-only classification and full retained-data
correlation are locally qualified without replacing original receipts. W-189
traces immediate health checks during repeated validation/provisioning; startup
probe traffic requires an owner-reviewed disposition before a new controlled
comparison. Keep full validation, normal health checks, resource limits and
recovery. No revised live operation or policy is defined by this source trace.

W-190 owner review proposes validation-process network isolation, retaining full
exact-config/module/TLS validation and normal runtime health checks. W-191 must
qualify both root and unprivileged finalizer contexts without changing privilege,
file access, deadlines or recovery. Isolation failure stops progression; there is
no networked fallback. This is a preparation proposal, not an approved runtime
policy, qualified implementation or live operation. Any target comparison remains
separately reviewed after the local mechanism and owner bindings are complete.

W-191 qualification now combines W-197's passed actual-primary read-only
capability check on 2.11.9 with W-198's focused local caller integration. Root
retains its user namespace; caddy-sync uses current-user mapping and existing
groups. The publisher/finalizer/reconciler sources invoke the fixed isolation
helper without changing runtime health or reload behavior. No helper or caller
was deployed. W-199 must bind helper delivery before caller activation, exact
identities, prior-state recovery and aggregate deadlines in the existing owner
path before any target comparison. Host boundary tests do not qualify complete
writable transactions or prove the historical timeout cause; no further fixture
capacity or root-container capability work is required. Live boundaries remain.

### Primary-host validation capability check (W-192; prepared scope)

Aaron approved preparation on November 17. This replaces the earlier requirement
to make root isolation pass inside the local container. It does not authorize
execution, helper installation or the later primary/Pi comparison.

**Decision:** Can the primary's existing root and caddy-sync callers perform full
Caddy validation inside the proposed isolated network context, with required file
access and applicable installed service restrictions preserved? A pass supports
owner integration preparation only; it does not explain the Webmin timeout.

**Target and admission:** One session to `pi@10.1.0.53`, native hostname
`j1-svpihole0`, using retained strict SSH host-key verification and existing sudo
authority. Capture a fresh boot ID and require continuity within this check.
Resolve and bind the accepted current release and installed Caddy executable,
caller UID/GID/groups, relevant unit/drop-in restrictions and non-secret node
environment. Compare configuration and installed identities against the reviewed
owner inventory; stop on drift. Historical boot IDs are not admission inputs.
Read only the files needed for these decisions; do not dump private keys.
For a future W-192 successor, require successful version-command status and the
exact v2.11.9 version token, with an optional build suffix. Retain bounded escaped
observed output and status separately before stopping on failure. The historical
package inventory is version provenance, not proof of current CLI output or
binary identity; preserve fresh binary/serving-process identity checks. W-194's
prepared correction does not modify the consumed attempt or authorize execution.

**Sequence:** First prove namespace creation and required file access without
running Caddy. Root retains its original user namespace; caddy-sync uses only
its existing UID/GID mapping and groups. Any failed isolation or access check
stops the operation before validation, with status and expected/observed evidence.
Then validate the exact accepted release once per applicable caller context,
sequentially: root publisher context, unprivileged finalizer context, and root
reconciler sandbox. Preserve full module/TLS validation and relevant environment.
The root reconciler check must reproduce its actual installed restrictions; a
plain sudo shell must not be reported as service-context qualification. Never
start the real reconciler, publisher, finalizer or serving Caddy entrypoints.

**Temporary execution:** If reproducing the reconciler sandbox needs a transient
validation unit, bind its exact properties/name/lifetime in the execution bundle.
It may run only the validator and its bounded identity/isolation checks, with no
production OnFailure hook. This is temporary process execution, not a claim of
strictly read-only inspection. Do not copy TLS secrets, modify production files,
relax controls or grant capabilities/sudo rights. Any required temporary writable
output must be named, private and owned by this check; if the exact configuration
requires an unreviewed write, stop rather than grant access.

**Bounds and evidence:** Maximum 30 seconds per validation process and five minutes
for the complete check including cleanup; no automatic retries. Retain caller and
namespace identities, config/executable hashes, required-file access outcomes,
command status and bounded sanitized validator diagnostics. Prove the validator
uses a distinct network namespace without external interfaces/routes before its
execution. Do not collect secret contents or claim fixture timing is host evidence.
Failure to represent the installed restrictions is an explicit unresolved result.

**Cleanup and stop:** Terminate only this check's owned processes/transient unit,
remove only its private temporary files and confirm no owned process remains.
Check boot continuity and unchanged accepted release/configuration identities.
There is no release rollback because the check never activates a release. Record
cleanup failure explicitly; do not restart or reset any existing service.

**Excluded:** Secondary or Pi contact, backend requests, release publication,
replication changes, existing service start/reload/restart, DNS, notifications,
authentication/browser/scan workloads, capacity acceptance and permanent changes.
If compatibility passes, prepare owner integration and then a separately reviewed
single-factor primary/Pi comparison with unchanged runtime health policy, caps,
request deadlines and recovery. A failed check returns for local review, not a
networked validation fallback or a privilege increase.

W-192 execution binding: one private SSH bundle runs namespace/file-access
prechecks in all three contexts before any full validation. It uses temporary
validation-only units with native process-group cleanup and collection. Each
precheck has a 10-second runtime cap; each validator has 30 seconds, plus a
three-second termination limit. The remote supervisor stops work at 240 seconds
and allows 30 seconds for termination; the controller stops at 295 seconds with
a five-second kill margin. Any timeout is failure, not permission to resume.

All temporary contexts make production files read-only and use private temporary
logs; the reconciler additionally preserves its NoNewPrivileges/ProtectHome
restrictions. Its installed ReadWritePaths are admitted unchanged but deliberately
not granted to this validation-only process. A pass proves read-only validation
compatibility, not writable reconciliation or end-to-end owner integration.
Unexpected need for a production write stops the check. A transient unit is not
the real reconciler and has no production OnFailure hook.

The exact accepted release and owner-installed tool/environment/unit hashes are
bound from owner inventories. Caddy's owner-confirmed production version is 2.11.9 (W-196); its executable
hash is captured at admission, compared with the running service executable and
required unchanged afterward. This does not invent an absent historical binary
hash. A fresh boot ID is admitted; no old boot ID is carried forward.

The private child uses the proposed helper's namespace flags and exact validation
argv, adding namespace/file-access evidence before Caddy runs. The proposed helper
is retained as an input reference; it is not installed or invoked by existing
owner callers. This qualifies the mechanism only, not owner integration.

WORK.md records the sealed bundle, command and authorization boundary. Preparation
and local static/integrity checks do not authorize live execution.

### Isolated-validator delivery and restoration bindings (W-199)

This is local implementation preparation for the primary/IPv4 diagnostic, not
an operation definition or authorization. The existing Caddy outer runner and
transaction now implement these bindings; no separate installer was introduced.
W-197 proves read-only capability and W-198 proves caller wiring. W-199's focused
local tests exercise payload/filesystem/recovery decisions with mapped privileged
paths and service/process stand-ins. Writable owner execution remains unaccepted;
only a separately authorized target operation can establish it.

**Delivery:** The primary application payload already carries the staged publisher
and fragment. Add the helper, finalizer and reconciler to that same payload, with
exact hashes checked before transfer and again before installation. Do not upload
them to Node B or put executable tools into replicated configuration releases.
The publisher remains staged; its installed production copy is not replaced.

These are the current source bindings, relative to `homelab-server-configs/Caddy/scripts/`:

| Source | SHA-256 | Execution destination |
| --- | --- | --- |
| `validate-caddy-isolated.sh` | `6932013a928108d2a08cfdc5b6de5d87975c4753474350f13d000f1264ae9004` | `/usr/local/libexec/validate-caddy-isolated.sh` |
| `publish-release-v2.sh` | `af5117fa16e46d516e33a5b82ff4c728c4935652955ead28c021b2c01f222feb` | Existing primary payload; execute with Bash |
| `finalize-incoming-release-v2.sh` | `70e54ac2187ebd982eff27fda078353c111e79ca6fa5b81b3d87c9aa4e3a619e` | `/usr/local/libexec/finalize-incoming-release-v2.sh` |
| `reconcile-release-v2.sh` | `5a12d4b87e2484f15493b364e4eb3decc661aaa6a2be09bf4d1a253da86dc962` | `/usr/local/libexec/reconcile-release.sh` |

Admission must match the installed finalizer hash
`fcff15db5b4ea971846a798028f40d2dce86db9cc331825d046dd5321d5f33bd`
and reconciler hash
`e777c2fe6932090d717b5ac9e50ef706d6b90c753293ad7eec4e396f2f6ea073`.
These remain accepted deployed identities, separate from candidate hashes. Require
the helper path to be absent, including absence of a dangling symlink; unexpected
presence stops admission for review. Do not assume that absence was observed by
W-197. Capture and bind existing file type, owner/group, permissions and any ACLs
or extended attributes needed for exact restoration; reject unsupported metadata
instead of silently dropping it. Preserve the installed publisher and unit files.

**Installation boundary:** First admit the unchanged release, tools, services,
fresh boot and executable identities. Quiesce sender/reconciler activity using
the existing owner service controls and require receiver/finalizer inactivity
before replacing files; do not kill unrelated processes. Keep the sender and
reconcile path stopped during the trial, but allow the explicit reconciler service
start after candidate preparation. Do not use the recovery cancellation marker
to enter this forward phase. Record prior service state and verified private
backups before the first file mutation. Bind the exact backup location beneath
the existing protected operation root when preparing the executable candidate.

Install the helper first as root:root:0755, then replace finalizer and reconciler
using atomic same-directory rename after hash/metadata checks, preserving the
original callers' ownership and permissions. Record each
replacement independently; a partial install must remain recoverable. Use the
existing privileges and restrictions, without unit/drop-in edits, privilege
additions or networked validation fallback. Before publisher preparation, verify
all three installed candidate identities. Subsequent candidate-phase checks must
expect those identities; admission and post-restoration checks must expect the
original identities. Do not rewrite the accepted inventory to satisfy trial checks.

**Restoration boundary:** Tool recovery must not require `application-target.tsv`.
Publisher validation can fail after tool installation but before producing a
release ID. The outer failure branch now accepts an explicit empty target receipt
only for this bound primary diagnostic. It dispatches tool-only restoration and
independent baseline/prepared-state checks before service resume. A missing or
malformed receipt still stops. Never invent a target ID or infer no mutation from
missing output.

For tool-only failure, prove the selected release and sync inventories remain at
the admitted baseline, restore any replaced callers and remove only the exact
owned helper. For a verified release mutation, keep the existing containment,
quiescence and release restoration, then restore callers and helper before resume.
Restore callers first while the helper remains available; remove the helper last.
Verify original hashes/metadata, helper absence, baseline release and sync inventory
before resuming admitted services and observing W-166's natural monitor cycle.
No restoration receipt means incomplete/manual intervention, not success. Preserve
backups and evidence on incomplete recovery; do not delete them in payload cleanup.
The Pi parent still owns its separate backend restoration.

**Deadlines:** Installation, validation and the request comparison share the
existing 240-second forward budget. Failure switches to recovery without resetting
the monotonic origin. Tool restoration, release restoration, service resume,
W-166 observation, readback and owned cleanup share the existing 840-second total.
Keep the existing 20-second margin, 60-second transfer cap, 90-second remote cap,
170-second monitor-command cap and remote process-group termination. The parent's
1200-second child limit and terminal-wait controls remain unchanged. Installation
must enter recovery on failure or cancellation even when no release ID exists;
an exhausted recovery budget reports incomplete state and retains evidence.

**Focused qualification before sealing:** Exercise the actual existing payload
builder and transaction branches for helper-before-caller ordering, source versus
installed identities, rejection before mutation, partial installation, publisher
failure before a release ID, later request failure and successful restoration.
Include interruption/aggregate-deadline handling and a restoration failure that
prevents service resume and backup removal. Reuse existing owner tests; do not
build a platform emulator or repeat root-isolation/capacity fixtures. These tests
prove code ordering and recovery decisions only. Writable owner execution and the
primary/Pi request comparison still need separately scoped actual-target authority.

Implementation binding: the inactive recipe remains empty. A future candidate must
explicitly set `validation_tools_trial` to `primary` and bind
`validation_helper_sha256`, `validation_finalizer_sha256` and
`validation_reconciler_sha256` to the table above. Existing
`publisher_candidate_sha256`, `finalizer_sha256` and
`reconciler_installed_sha256` retain their distinct candidate/baseline roles.
Only primary/IPv4, 240-second diagnostic/660-second trial recipes accept this
option. The helper and callers use the existing primary payload; the secondary
control archive contains no tools. Source identities are verified during payload
construction and remote dispatch. No operation is populated or sealed here.

Verified caller backups and their metadata live beneath the operation's protected
payload root in `validation-tools/`, with a `ready` marker written before service
or file mutation. Restore ordering uses that marker and observed file hashes,
including partially written staging files. Failed recovery preserves this directory.
Python 3 must already be available for metadata checks; no dependency installation
or metadata relaxation is permitted. Absent and empty prepared directories are
valid; unexpected prepared entries require manual reconciliation. The existing
remote process-group timeout, lock, boot continuity and recovery budget remain.

W-200 preparation uses a new private parent input set and an exact proposed owner
recipe, with no registered operation or live launcher. Before sealing, the owner
qualification must exercise the `validation_tools_trial=primary` path through the
existing execution/transport/recovery boundaries. Existing whole-path scenarios
omit this option; prior source-graph evidence cannot be relabeled for the changed
implementation. Keep the scope primary-only and reuse W-197 mechanism evidence.
Do not expand fixtures to requalify target kernel isolation or capacity. Focused
W-199 filesystem tests remain partial evidence; actual writable host execution
remains part of a separately authorized, bounded trial.

W-200's primary-only tool-delivery branch is now covered by three current-source
whole-path cases: successful request, failed HTTP acceptance and partial install
failure before a release ID. Use the existing launcher's
`--primary-validation-tools` mode and its separate effect/source verifier. Namespace
creation is explicitly substituted here; W-197 remains actual-host capability
evidence. This focused summary does not satisfy the full authorization gate.
Reconcile exact candidate/coverage bindings before sealing; do not relabel earlier
receipts or infer writable target acceptance from this result.

W-200 authorization uses the explicit `primary-validation-diagnostic` profile in
the existing owner gate. Selection requires the exact single-primary Webmin recipe,
validation tools, request contract and 240/660-second bounds; paired onboarding
retains complete coverage. Fresh evidence must bind the private candidate's complete
source graph and pass the ordinary authorization gate. Earlier focused summaries
remain non-authorizing. The parent binds this same private owner projection and
evidence; sealing must include those exact sources, parent inputs and recovery
controls. Main registration and live approval have not occurred.

W-200 sealing update (November 17): exact qualified owner registration and the
private parent bundle are now sealed for separate one-attempt review. WORK.md owns
the final manifest, command, targets, deadlines and recovery/exclusions. The main
stream is defined; no live authority or writable-host acceptance follows. Earlier
preparation-status paragraphs above describe their respective checkpoints.

Controller evidence admission (W-201): prepare the private mode-0700 output
directory before sealing. The parent must reject absent/unsafe/unwritable storage
before any target command, using the existing receipt writer/readback. Do not
repair the output path of a consumed attempt and replay it. Later storage failure
must not suppress owner recovery; retain the controller log and distinguish
observed recovery from unavailable terminal receipts.

W-202 preparation retains the unchanged unexecuted Caddy child under the single
existing definition. Original qualification is reusable only while its complete
graph matches and the actual authorization gate passes. The fresh parent binds
W-201 storage admission, new paths/token and prepared private output storage.
WORK.md owns the sealed command/scope; this grants no live authority.

W-212 review boundary (November 17): the retained primary-only run has matching
foreground request headers but overlapping health requests with a different,
partly redacted header contract. Concurrency is a hypothesis, not attribution.
Before defining another comparison, select one factor. The recommended question
is actual-backend response to identical requests alone versus bounded overlap,
using existing native backend controls and recovery without Caddy publication.
This is an unapproved proposal, not a replacement acceptance criterion or live
scope. Preserve deadlines/caps, safe evidence and all consumed attempts; no
fixture can accept the Pi's capacity. WORK.md owns the evidence and limitations.

W-213 preparation design (November 17): review recommends a backend-only,
primary/IPv4 single-versus-three-identical-request comparison with at most one
conditional single-request control, five requests total. Reuse native Webmin
apply/restore and observation; the Caddy-bound combined parent cannot serve as a
no-op wrapper. Apply one five-second total request deadline uniformly and preserve
all service controls, recovery and resource stop rules. Do not advance without
bounded workload quiescence. WORK.md records scope, stop conditions and limited
interpretations. This is a local preparation design, not an executable or
live-approved operation, and does not change AC-013 acceptance.

W-214 preparation checkpoint (November 17): the backend-only implementation
reuses native apply/restore and the existing probe/observer. Its execution gate
must remain closed until aggregate forward/recovery supervision, independent
cleanup and final observer coverage are qualified. Per-request deadlines and
local component tests do not establish complete parent recovery. WORK.md records
the exact gaps and local evidence; no live scope or acceptance changes follow.

W-214 qualified preparation (November 17): the backend-only candidate must invoke
the supervisor in `Webmin/scripts/compare-backend.py`, not the raw playbook.
Separate forward/recovery invocations enforce aggregate controller budgets of
240/840 seconds. Recovery preserves independent native fallback if readback fails;
a controller cutoff is not proof of remote completion. At most five comparison
requests retain the five-second total deadline; native owner readbacks remain.
Require client stop/worker cleanup, observer exit, terminal resource/wire coverage
and post-recovery boot continuity. Existing limits and 96 MiB reserve remain.
Local control-flow qualification is complete; exact inventory/input/path bindings,
sealing and live approval remain required. This does not change AC-013 or establish
target capacity or historical timeout causation. WORK.md owns qualification logs.

W-215 sealed preparation (November 17): WORK.md owns the exact 33-input
backend-only candidate and one-attempt command. Retained installed identities
are distinct from frozen current owner sources. Restrict temporary ingress to
primary IPv4 with loopback retained; recheck the primary route before exposure.
Keep W-213/W-214 workload, caps, reserve, aggregate deadlines, native fallback
and restoration requirements. No Caddy operation is defined. Local qualification
is complete; execution needs separate exact-scope approval. No historical boot
pin, sustained-capacity acceptance or AC-013 change follows.

W-216/W-217 checkpoint (November 17): the backend-only attempt stopped before
observation or comparison requests; native restoration was verified. Before any
successor, locally reconcile the quiescence gate's missing expected/observed
process/socket evidence and explicitly classify observation-not-started in the
terminal path. Keep existing stop conditions, limits, deadlines and acceptance;
no repeat inspection or workload is authorized by this reconciliation.

W-218 diagnostic reset (November 17): Aaron requested a consolidated audit after
repeated non-diagnostic failures. Preparation should now target a bounded native
loopback measurement on the existing Pi listener, with CPU/throttling/process-wait
and request timing evidence. Do not default to another ingress-changing/Caddy
transaction or a singleton-process assumption. Loopback can test backend workload
but cannot reproduce all remote-peer/proxy behavior. Preserve service limits,
request bounds, stop conditions and separate live review; no operation is defined.
The earlier comparison remains consumed and restored. WORK.md records the evidence,
confirmed tooling defects and unproven hypotheses.

W-220 prepared loopback scope (November 17): WORK.md owns a six-input one-Pi
capture through the existing HTTP diagnostic, with no deployment/service change.
At most four fixed-contract unauthenticated requests (one, then conditional three)
use five-second curl bounds. Stream numeric CPU/throttling/process-wait/resource
and request evidence before checks; keep accepted caps and reserve. Permit
standing helpers and ordinary process exit, require main-process continuity,
and stop additional work when activity/evidence is unresolved. Kill only owned
clients; no Webmin restart or assumed server-side cancellation. No live authority
follows from local tests or Aaron's agreement with the loopback direction.
W-219's durable-instruction addition is proposed separately, not installed.

November 17 checkpoint: W-219 is now approved and installed. W-220 was approved and consumed once; W-221 supplies actual loopback evidence. W-222 requires owner review of concurrency/CPU policy before any new comparison or correction. Existing caps and AC-013 remain unchanged.

November 17 owner review: W-222 proposes local preparation of a temporary 100% to 200% Webmin CPU-quota comparison only after owner agreement. Retain the existing loopback workload, deadlines, memory controls and explicit original-quota restoration. No permanent budget or execution authority is selected. Keep health-contract changes separate.

November 17 W-223 checkpoint: Aaron approved W-222 local preparation. W-223 binds the temporary CPU-only change to a native transient service with independent ExecStopPost restoration, including the prior runtime override and manager reload. The unchanged measurement remains one-plus-three requests with five-second deadlines. WORK.md owns exact input identities, command and bounded staging/collection scope. No live or permanent-budget authority follows.

November 17 W-224 result: W-224 completed the approved temporary quota comparison successfully and restored the admitted baseline. W-225 now governs review of a host-specific 200% CPU candidate and compatible health contract before browser onboarding. Do not promote the temporary limit to fleet defaults or infer authenticated/sustained capacity. No new operation or live authority follows.

November 17 W-225 review: W-225 proposes, but does not approve, a selected-host 200% Webmin CPU ceiling and an explicit unauthenticated health request with health_timeout=5s. The foreground deadline and memory controls stay unchanged. Preserve paired/dual-stack browser acceptance and account for combined health/browser load. The existing health request differs from W-224; its failure at 3s is not established. Policy agreement precedes local implementation; exact live approval remains separate.

November 17 W-225/W-226 checkpoint: Aaron approved local implementation/preparation. The selected Pi 200% CPU profile and explicit 5s unauthenticated health policy are implemented in the existing owner sources and locally checked; fleet default and memory/foreground limits remain unchanged. Native recovery restores the prior CPU baseline. No target change or acceptance follows. Final paired/dual-stack browser candidate and exact parent/owner binding remain preparation work; no bundle is sealed. W-147/AC-013 remain open.

### W-227 paired browser candidate binding and W-228 owner dependency

Prepare the browser trial on the existing three targets: Pi ama@10.1.3.75,
primary pi@10.1.0.53 and secondary pi@10.1.0.54. The proposal now includes both
Pi backend families. Bind all four proxy-to-backend paths and six browser paths
(A, B and VIP over IPv4/IPv6), the existing ama statistics-only method, prior
session denial, 600-second resource observation and guarded scan overlap.
Select j2-svpi3bmf-cpu200 explicitly, preserve memory/foreground criteria, and
restore both owners and the original CPU baseline on either success or failure.
This temporary trial does not promote the route or make DNS changes.

The fresh private draft uses current source hashes and predecessor bindings,
not old operation authority or old qualification receipts. Current target state
still requires live admission under a future exact approval. WORK.md records
its path and local checks. No launcher, authorization hash or operation is sealed.

W-228 is a concrete owner integration prerequisite. The current publisher calls
the isolated validator; existing delivery only permits a primary/IPv4 diagnostic.
Do not remove the helper dependency, ship application files to the secondary,
reuse diagnostic qualification as paired evidence, or reset the work to another
capacity test. Reconcile primary-only tool installation/restoration with the
paired trial in the existing owner path. The secondary must receive configuration
through replication and retain its accepted installed callers. Cover failure
before a release ID separately from recovery after paired exposure, including
natural monitor acceptance, before defining a live operation. Do not silently
carry the diagnostic's 240-second forward cutoff into the longer browser workload;
retain and verify the existing browser parent/recovery deadlines.

November 17 W-228 checkpoint: the existing owner path now implements paired-trial
primary-only tool delivery, explicit pre-ID primary restoration with paired payload
cleanup, and unchanged post-ID paired restoration/monitor acceptance. Focused local
boundary tests and the host onboarding profile pass. The secondary retains its
installed callers and receives the route through replication; no secondary isolation
claim follows. W-227 must qualify and bind the exact current paired owner/parent
candidate before sealing. Browser, resource and recovery deadlines are unchanged;
no live approval or target acceptance follows.

November 17 W-227 qualification checkpoint: the exact private paired owner and
parent bindings pass local qualification, including current tool delivery,
accepted secondary callers, paired recovery, real payload construction and the
owner authorization gate. The six browser paths, four backend paths, selected
CPU profile and existing limits remain the planned live scope. Readiness flags
remain false; final immutable parent manifest/launcher and separate live review
are still required. No target browser/capacity or writable recovery acceptance
follows from these tests.

November 18 W-235: Aaron approved local implementation and qualification of
GET /robots.txt as the first-host active health URI. Keep per-address HTTP 200,
existing headers, intervals and thresholds. The foreground login-page and
AC-013 browser requirements retain their existing scope. Live use requires
separate review.

November 18 W-245 measurement scope: one marked foreground GET /session_login.cgi
over primary IPv6 HTTPS, five-second client deadline. Keep the existing direct
IPv4 owner admission control separate. Require the IPv6 client receipt and
marker-matched Caddy journal row selecting 10.1.3.75:10000, then compare
arrival and first outbound payload on that marked Pi flow. GET /robots.txt
with the browser-health header is background traffic. Require capture before
the request, zero reported drops and clock-bounded coverage at least five
seconds beyond client exit inside the existing 300-second sampler. Missing
response bytes mean no first response observed within coverage; ambiguous
timing or route evidence cannot localize the delay. Stop after this request;
retain bounded evidence, restore the primary and native backend, and verify
existing recovery checks. No secondary activation, DNS, browser or scan.

W-249 exact temporary access for this measurement: Webmin listens on TCP
10000 on 127.0.0.1, ::1, 10.1.3.75 and fd36:5aa8:6971:1::75. Ingress
accepts loopback. For the Pi LAN IPv4 destination it permits 10.1.0.53 and
10.1.0.54; for the Pi ULA destination it permits fd36:5aa8:6971:1::53,
fd36:5aa8:6971:1::54 and fd36:5aa8:6971:1::56 (VIP). Webmin permits
those sources and both loopbacks. The guard drops other local-destination
IPv4/IPv6 TCP 10000 traffic. Secondary and VIP reachability is temporary;
neither adds an active test. Restore the loopback baseline. Attribute the
marked upstream only on a successful journal command with a unique matching
row. Collection failures leave attribution unknown and recovery mandatory.

W-259 paired timing: use the existing final Node A IPv6 HTTPS request after
secondary convergence. Match its own fresh marker and journal-selected Pi
upstream; admit both observed primary source paths and preserve clock bounds,
packet loss and recovery intervals. Stop and join the pre-login packet collector
before handing credentials to the existing ama statistics browser trial. Keep
the foreground deadline, four backend paths, six browser paths, scan overlap,
caps and both owners’ recovery. No new diagnostic request, DNS or promotion.

W-267: The approved browser-first contract supersedes prior paired browser/scan
trial criteria for future onboarding. Plan persistent, independently verifiable
owner steps with explicit keep/rollback conditions. No old trial is converted
into permanent authority. Capacity acceptance and live deployment remain pending.
