# Change result: initial Uptime Kuma deployment

## Outcome

- Verdict: **Partial — Kuma accepted; requested Webmin browser-access extension pending.**
- Review date: November 12, 2026. This is a local reconciliation of retained
  evidence, not a new inspection of the Pi or proxy/DNS nodes.
- Target: `j2-svpi3bmf`, with owner-governed Caddy/DNS on the existing pair.
- Delivered: installed foundation, authenticated persistent Kuma service,
  guarded backend, accepted startup/reboot and backup/restore, fleet schedule,
  Caddy HTTP/WebSocket application acceptance and dual-stack dashboard DNS/HTTPS.
- Deferred: W-020 timed RA renewal and W-096 legacy preflight diagnosis.
  W-076 is resolved by Aaron's approved no-service-change disposition; W-012
  reopened for the subsequent Webmin requirement.

The [plan](PLAN.md) owns requirements and the [ledger](WORK.md) preserves all
attempts, approval boundaries and failures. No consumed operation may be replayed.
Aaron approved the W-127 acceptance boundary on November 12, 2026.
This closeout authorizes no live work or publication.

## Executed identities and evidence

| Stage | Executed identity | Retained evidence under workspace `.local-evidence/` |
| --- | --- | --- |
| Startup reboot checkpoint | Staged continuation archive `e03e14dd7058dd58dee602d00eb719b3c2b799bf1dc1c5f4bedbc3f286252536`; later operator-window failure remains recorded | `uptime-kuma/remaining-staged-20261110-5i0l9c9t/execution/`; before/after-reboot runtime and combined receipts |
| Accepted backend/foundation | Archive `7824e4df0c13929baa6fcac0a78faada36b3100942131a8d314a9c92030882af` | `uptime-kuma/backend-completion-20261111-nin6u10h/execution/`; `outcome.json`, `EVIDENCE.sha256`, runtime, startup, foundation and restore receipts |
| Caddy and application | Release `20261111T213048Z-71b7deb8-bc71-45d5-8f33-98270af79d3b`; W-102/W-106 | `uptime-kuma/proxy-observation-review-c9vdnab_/`; accepted private receipt and combined passive verification |
| DNS and ordinary-name HTTPS | Archive `d89d3b0c252dc86173ef98603539189ca96dc46dff55c333e2352e004cbb8e2e`; W-124 | `homelab-dns/current/uptime-kuma-dns-admission-20261112-myuc3p0t/terminal-summary.json` and `dashboard-https.json` |
| Local reconciliation | Seven foundation/runtime receipts checked against their retained SHA-256 indexes | `uptime-kuma/closeout-reconciliation-t490dweo/evidence-index.json` |

Accepted runtime reports Kuma 2.5.9 on ARM64, image configuration ID
`sha256:315dfadc88ca9be7ba59515578363871bda93f7989a8e406f162acf36c9b0037`
and registry digest
`sha256:6be4ea6135b22947b463966ce115cc7725b1254ec47e892d3633620854556d7f`.
These are observed deployment identities, not a statement about the latest release.

## Acceptance results

Aaron subsequently required standard-browser Webmin access (W-128/AC-013).
Earlier W-127 network/radio dispositions remain approved; overall closeout waits
for this added requirement. Earlier loopback login is not proxy-login acceptance.

| Plan criterion | Status | Observed result and evidence |
| --- | --- | --- |
| AC-001 Identity, OS, addresses, resources | Pass | Accepted platform/preflight and ARM64 runtime; required IPv4/ULA, storage and staged admission passed. Radio softblocks are accepted with existing services retained under W-127. |
| AC-002 Architecture and immutable runtime | Pass | Permanent architecture reconciled with accepted definitions; runtime image identities above and frozen backend inputs retained. |
| AC-003 Persistent local data | Pass | Runtime reports local ext4, `/var/lib/uptime-kuma/data` mounted at `/app/data`, UID 1000 and one persistent administrator; restore/source recovery accepted. |
| AC-004 Internal dual-stack dashboard | Pass | W-106 private authentication/WebSocket and passive acceptance plus W-124 DNS and normal-name IPv4/IPv6 HTTPS 200. |
| AC-005 Safe administration | Pass | One active administrator, authentication enabled, protected bootstrap and private login checks accepted; no credentials in this record. |
| AC-006 Startup/recovery and budget | Pass | Accepted reboot checkpoint, permanent startup state, native limits, combined scan sampling and source recovery. Final sampled minima 554968/566808 KiB; no observed OOM events. Empty-monitor workload only. |
| AC-007 Backup/restore | Pass | Consistent administrator-bearing archive, protected on/off-node copies and isolated pinned ARM64 restore accepted. No recurring backup schedule is installed. |
| AC-008 Preserve services/network policy | Pass | Scoped service/configuration preservation, required addresses/routes and radio softblocks passed through reboot/promotion. Aaron approved W-127: retain radio services and defer timed RA renewal to the network owner. Renewal remains untested; its residual risk is accepted for this initial deployment. |
| AC-009 Excluded workload/actions | Pass | Runtime counts are zero monitors and zero notifications; no synthetic messages or unattended application upgrade activation in accepted operations. |
| AC-010 Operability and finding disposition | Not tested | Initial-scope closeout was accepted. Expanded Webmin scope remains open under W-128/W-012; fleet DNS procedure routing is documented under W-129. W-020/W-096 retain approved deferrals. |
| AC-011 Fleet foundation | Not tested | Prior foundation and loopback Webmin acceptance retained. Revised direct-browser Webmin management policy awaits AC-013; other foundation capabilities remain accepted. |
| AC-012 Fleet notification transport | Pass | Mailrise default and owner consumer configuration accepted; greeting/QUIT only. No downstream message-delivery claim or provisioned Mailgun secret. |
| AC-013 Browser Webmin | Not tested | Newly requested dedicated trusted HTTPS endpoint without a tunnel; no new configuration or live acceptance yet. |

## Failure and recovery

Earlier installation, capacity, Webmin, loopback, proxy orchestration and client
acceptance failures remain in WORK.md with their consumed bundles. Later passes
do not erase them or retrospectively accept failed gates. Containment preserved
administrator data, predecessor states and backups; the final backend successor
passed without another reboot or account setup. The staged reboot operation's
operator-window failure does not invalidate its separately retained reboot checks.

Both earlier DNS attempts stopped before apply and required no rollback. The
accepted DNS operation completed all five phases with no recovery or forced
failover. Node backups remain in
`/var/backups/uptime-kuma-dns-admission-20261112-myuc3p0t`.
No backup cleanup or fresh recovery was performed during this reconciliation.

## Residual work and permanent documentation

- W-020 — Deferred, `homelab-network`/runtime owner: timed RA renewal is not
  demonstrated. Aaron accepted retained startup/reboot/promotion networking
  for this deployment and the residual risk of an unobserved later failure.
  Complete a separately reviewed bounded observation before the next host
  networking/container-runtime migration, or earlier if IPv6 route/address loss
  is reported. This ledger item remains the follow-up destination.
- W-076 — Resolved by Aaron's no-change decision: accept observed Bluetooth/Wi-Fi
  softblocks across reboot/promotion; preserve existing daemons and block policy.
  Dependency review is required before future service removal, not claimed
  completed here. No hardware-disablement or memory-savings claim; unexpected
  unblocking reopens this item under the host/network owner.
- W-096 — Deferred, Caddy owner: legacy preflight diagnosis remains deferred at
  Aaron's direction; W-098 replaced that path. Its failure remains archived.
- W-012 — In progress: initial-deployment closeout was accepted; the added Webmin scope remains open. Monitors/alerts, future
  workload qualification, recurring backups and actual notification delivery
  remain separately scoped work, not implied by this installation.

[Architecture](../../uptime-kuma/docs/ARCHITECTURE.md) now describes the accepted
runtime, watchdog, network path and startup state with evidence limits.
[Operations](../../uptime-kuma/docs/OPERATIONS.md) distinguishes normal dashboard/
Webmin access from first-time bootstrap and contained-state recovery procedures.

## Completion decision

Aaron approved the [W-127 dispositions](WORK.md#proposed-w-020w-076-acceptance-decision--november-12-2026-w-127)
for initial-deployment closeout on November 12, 2026. The service and dashboard
are accepted and the initial deployment is closed. Timed renewal is explicitly
deferred, not represented as a passed test. W-076 is resolved without changing
services; W-096 retains its approved deferral. No target contact, mutation,
replay, commit or push occurred during closeout. Consumed bundles remain intact.

Host inventory records accepted installation/dashboard state and links this
result. The operator's subsequent failed login at the dashboard name's port
10000 addressed the Proxy VIP rather than the Pi's loopback-only Webmin endpoint.
The [operations guide](../../uptime-kuma/docs/OPERATIONS.md#host-foundation-and-notification-configuration)
provides the workstation SSH tunnel and Pi account login. No fresh authenticated
Pi check or credential reset was performed; prior accepted login evidence stands.

## Scope extension after disposition approval

Aaron approved W-127, then rejected tunnel-only Webmin access and requested a
normal browser connection using Caddy/DNS as needed. This extends accepted
service scope; it does not revoke the network/radio decisions or erase prior
acceptance. W-128 and W-012 remain in progress. No new live action is authorized.

W-133 local qualification corrected the interpretation of `referers_none=1`: it
rejects missing referrers on protected actions, rather than disabling checks.
The proposed profile preserves it and explicitly sets global `referer=0`; the
prior live global value was not captured. Native referrer/ingress checks and the
first-host review input are prepared locally. No Webmin browser deployment or
additional live acceptance is claimed; AC-013 and overall closeout remain pending.

November 12 local Webmin qualification (W-134/W-135): persistent guard ordering,
failure containment, container restart and ordered loopback recovery passed.
Partial dual-stack browser HTTP/session checks passed, but a fresh full-browser
fixture was OOM-killed at the preserved 192 MiB service cap before WebSocket tests.
AC-013 remains pending; no deployment is sealed. This AMD64 fixture result is not
an observed Pi failure. Actual proxy-source/path and production-unit acceptance
also remain pending. Both local fixtures were removed; no live contact occurred.

W-135 retained-evidence reconciliation: the OOM result and 192 MiB peak are
confirmed; allocation/process attribution and unit-versus-ancestor limit causality
are unknown. Owner caps/reserve remain unchanged. The existing sampler's bounded
charge/PSS/limit reporting is locally tested, but no instrumented browser run or
runtime retry has occurred. Fixture/native-unit equivalence and full acceptance
remain pending; no live contact or publication was performed.

W-135 aligned offline diagnostic: native package unit plus exact foundation
controls passed one IPv4 browser/WebSocket workload, with 48 correlated samples,
a 132.6 MiB Webmin peak, no max/OOM events and no restart. The original OOM cause
is not established. Sustained paired-proxy/dual-stack and Pi acceptance remain
pending; caps/reserve are unchanged. The diagnostic fixture was contained and
removed. AC-013 and deployment sealing remain pending; no live contact occurred.

W-135 paired-resource qualification failed locally: Node A/IPv4 completed the
native browser suite; Node A/IPv6 login/assets passed but the protected page
timed out. Both used the fixture's forced IPv4 upstream. Webmin peaked at
161.2 MiB with no hard-limit/OOM event or restart, but severe 128 MiB memory-high
throttling coincided with both proxies' health timeouts and HTTP 504. The remaining
browser paths and 95-second concurrent phase did not run. All source/evidence and
prior failures are preserved; containment and owned-container removal completed.
AC-013 remains pending, with caps/reserve unchanged and deployment unsealed.
Reconcile responsiveness under the Webmin/host owners before another workload;
this result does not establish the cause of historical failures or Pi capacity.

Aaron approved moving host-capacity qualification to the actual Pi. The fixture
failure remains evidence about that fixture; it neither accepts nor rejects Pi
capacity and no further fixture capacity pass is required. W-136 proposes the
durable workspace instruction. W-137 prepares the bounded real-host trial and
its missing installed-unit/proxy-source readiness capture. AC-013 remains pending;
no live contact, workload, deployment, publication or global harness installation
occurred in this preparation.

W-136's approved fixture-evidence rule is installed in workspace AGENTS.md. The
separately approved W-137 read-only capture passed once on the Pi and both Caddy
nodes: installed unit identities/controls, native modules, current proxy sources
and certificate coverage were retained. No per-user ama terminal ACL was present;
effective terminal privilege remains unestablished. These are readiness facts,
not capacity or browser acceptance. No mutation or workload ran, AC-013 remains
pending, and the inspection approval is consumed.

November 16 crash reconciliation: the local parent/path/workload implementation
survived, but AC-013 remains pending and the verdict remains Partial. Retained
native packet correctness and synthetic parent-flow checks passed; the parent
and supervisor subsequently changed, so the flow pass does not qualify their
current revision. Browser duration/session-denial gaps, native statistics
readiness review and final owner/input binding remain in W-143/W-137/W-141.
No actual-host trial or browser acceptance is claimed. No target was contacted
and no workload was launched during this reconciliation; see the ledger's
[crash checkpoint](WORK.md#november-16-crash-status-reconciliation-w-137w-141w-143).

November 16 combined local qualification: W-141/W-143 implementation checks passed
at recorded source identities, including all-six-path duration, fresh open-socket
readiness, old-session denial, client-to-parent receipts and ordered cleanup/
recovery. Native path tests retain matching inputs; the new browser tests use a
synthetic adapter and do not establish actual UI behavior or Pi capacity.
The fleet procedures are updated. W-137 final owner/input bindings and AC-013
live acceptance remain pending; the result stays Partial. No target contact,
native browser workload, sealing, replay or publication occurred.

November 16 exact candidate preparation: W-137/W-144 are complete for local
preparation and W-145's coverage contradiction is corrected. The single Caddy
owner candidate and combined parent are sealed for review in
[the ledger](WORK.md#november-16-combined-trial-sealed-for-review-w-137w-144w-145).
Owner qualification, authorization and final non-secret input verification pass.
No live trial, browser workload, permanent Webmin exposure or publication occurred;
AC-013 remains Not tested and the result remains Partial. The reviewed trial
must restore both owners even on success; permanent promotion remains separate.

November 16 approved combined Webmin trial: **Failed, recovery verified**. The
parent exited 2 after Caddy's first primary application IPv4 HTTPS check timed
out. Direct dual-stack backend source/guard checks passed. Caddy's paired
restoration/readback checks and the parent's Webmin loopback restoration assertion
passed; browser and scan workloads never started. AC-013 remains incomplete,
with browser/permission/scan-overlap/capacity acceptance Not tested. The timeout
cause is unconfirmed. Existing accepted Kuma scope remains unchanged and the
project verdict remains Partial. See [the terminal record](WORK.md#november-16-trial-failed-and-recovered-w-146w-147w-148).
The attempt is consumed; no replay, successor or publication is authorized.

November 16 retained-evidence reconciliation: W-147's failure cause remains
unknown. Passing direct HTTP `/` probes do not prove the timed-out HTTPS
`/session_login.cgi` path; phase timings and correlated request logs are absent.
No browser, authentication, scan or target-capacity conclusion follows. The
61-file W-148 historical terminal archive is prepared locally, with W-149's
isolated documentation-fixture validation gap recorded. No archive publication
or further live work occurred; the verdict and AC-013 remain unchanged.

November 16 archive-review disposition: Aaron deferred W-149 fixture repair for
this effort. Its failure remains recorded; the actual documentation check passes.
The unchanged 61-file W-148 archive is reviewed for separate publication approval.
No test bypass or production acceptance follows from this disposition. W-147 and
AC-013 remain unresolved; no publication or live action occurred.

November 16 W-148 publication: the approved 61-file terminal archive was committed
as `66d8ae5bbaea05587bd30d2be01f2682b3d5066c` and pushed with annotated tag
`caddy-webmin-first-host-trial-terminal-2026-11-16`. Remote branch/tag identities
match; applicable commit hooks passed. W-149 remains Deferred. This preserves
the failed attempt and verified recovery; it does not accept AC-013. Neutral
cleanup and further live work have not run.

November 16 W-150: local Caddy neutral cleanup passed focused owner checks after
verification against the published archive. The operation is inactive and stream
clean, with accepted production hashes unchanged. Cleanup is uncommitted; no
live work or publication occurred. W-147 diagnosis and AC-013 remain pending.

November 16 W-151: the diagnostic correction is locally qualified. Backend and
proxy probes use the same login path; bounded timing, sanitized journal metadata
and a later backend snapshot are retained without suppressing recovery. Tests
establish those contracts only. W-147's historical cause and actual-host/browser
acceptance remain unresolved; AC-013 is pending. No successor or live operation
is authorized, and changes remain uncommitted.

November 16 W-152: a separate diagnostic-only successor is sealed for review.
Local owner/parent qualification passes. It requires no password, browser or
scan, and restores both owners even on successful route readiness. No live
attempt is authorized or performed; W-153 is pending, W-147 remains unknown
and AC-013 remains unaccepted.

November 16 bounded Webmin diagnostic: **Failed; scoped recovery checks passed**.
All four direct login-path checks and both guard-denial checks passed. The primary
HTTPS request completed TCP/TLS but received no HTTP response within five seconds.
Both Caddy restoration/resume and exact Webmin loopback-restoration assertions
passed. A user-reported replication-health failure occurred during recovery;
subsequent monitor health remains unverified (W-154). The later Webmin snapshot
contains an OOM kill counter without a baseline delta or event timestamp; cause
and timing remain unconfirmed (W-155). No browser or scan ran; AC-013 remains
pending and the project verdict remains Partial. The attempt is consumed, all
230 inputs/receipts are preserved, and the Caddy terminal archive is pending
separate review (W-156). No additional live work or publication is authorized.

November 16 local reconciliation: W-154 remains open because retained evidence
cannot establish the replication-health failure predicate or a later successful
cycle. Recovery leaves the health timer running while stopping its sender; this
is a plausible interaction. W-157 records notifier state loss and static labels.
W-155's local review is complete, but timing, sequential-probe and untimed OOM
limitations leave W-147 unresolved. The exact 12-file terminal archive is prepared
and locally checked for separate publication approval. No target contact, fixture
load test, source behavior change, publication or AC-013 acceptance occurred.

November 16 archive publication: stopped before commit by the test-lifecycle hook.
A generated bytecode file caused the inventory mismatch; it is preserved privately
and removed locally, and the check now passes. The exact reviewed tree remains
staged and unchanged. No commit, tag or push occurred. W-156/W-158 await separate
publication-continuation approval; deployment acceptance is unchanged.

November 16 diagnostic archive publication completed: commit
`4e6b3d5a016e03d4ee2101d9fe745f7d63702de7` and annotated tag
`caddy-webmin-proxy-diagnostic-terminal-2026-11-16` are pushed and remote-verified.
The exact reviewed tree matches; mandatory local hooks passed. The original
publication failure remains preserved. Neutral cleanup has not run, W-159 CI
correction remains pending, and live acceptance/recovery-health limitations are
unchanged. No further live or publication authority follows.

November 16 CI dependency correction: the workflow now locally pins DNS 2ce7105.
Clean old/new checkouts prove the original missing-document failure is corrected.
Full CI qualification remains partial: W-149's deferred self-test and W-160's
stale accepted-zone hash still fail. Synchronization and remaining serving tests
pass. No production identity was changed and no publication occurred.

November 16 local CI reconciliation completed: W-149/W-159/W-160 pass all three
Caddy host CI profiles against pinned DNS 2ce7105. Retained accepted DNS receipts
correct the stale inventory while preserving distinct source/installed hashes;
negative identity checks reject both mismatch types. W-161 local neutral cleanup
preserves the published diagnostic archive and leaves no active operation.
Changes are uncommitted; no hosted CI run, publication or live acceptance is
claimed. W-154/W-147/W-157 and AC-013 remain pending.

November 16 reconciliation publication: server commit 722bc45 is pushed and
remote-verified. Repository validation 43933039649 and CodeQL 43933039034 pass.
The approved monitoring publication carries PLAN/WORK/RESULT; its publication
receipts remain in the private W-162 review directory. Source publication does
not resolve W-154/W-147/W-157 or AC-013 and grants no live authority.

November 16 post-publication reconciliation (W-163): retained evidence and current
owner source confirm a notifier reporting defect and a possible recovery/health
monitor interaction, but do not establish the exact alert predicate, subsequent
monitor health or primary HTTPS timeout cause. W-154/W-147/W-157 remain open;
AC-013 remains pending. Next work separates local notifier correction from a
separately reviewed read-only health check and any later target diagnostic. No
new target contact, source behavior change or publication occurred.

November 16 W-157 source correction: the existing notifier passes local reporting
cases and three focused Caddy host profiles. Installed identities remain unchanged;
no notification was sent. W-164 read-only Node A health capture is prepared for
separate approval. W-154/W-147 and AC-013 remain unresolved. No live work or
publication occurred.

November 16 W-164 read-only Node A capture passed once. Journal evidence explains
W-154: sender validation failed immediately before recovery finished starting
lsyncd; the next scheduled health cycle passed. Two further natural cycles passed
during the bounded observation with stable sender PID, zero restarts and boot
continuity. W-154 is resolved for this alert and subsequent monitor health.
Unchanged status-file age does not prove fresh transfer or stalled replication;
W-165 tracks that limitation and recovery/monitor coordination. Node B and the Pi
were not contacted. W-147/AC-013 remain pending, and W-157 is not installed. The
inspection approval is consumed; no further live action or publication follows.

November 16 W-165 local reconciliation completed. The shared procedure now
distinguishes restored configuration/transport from a fresh successful scheduled
monitor cycle. Status-report mtime alone is not a heartbeat criterion. W-166
tracks executable integration and focused qualification; no implementation or
live acceptance of that added boundary is claimed. W-147/AC-013 remain pending.
No live work, fixture load, retry or publication occurred.

November 16 W-166 source integration and local qualification completed. Trial
recovery now separates restored service from a fresh natural monitor cycle,
retains failure evidence and reads both nodes without repeating recovery. Nine
observer cases, a coordinator failure case and all 16 offline application cases
pass; initial fixture timer-output failure is preserved. Parent deadlines and
installed state are unchanged. No successor is sealed, no live use is accepted,
and W-147/AC-013 remain pending. Changes remain uncommitted.

November 16: W-167 diagnostic instrumentation passes focused local correctness
checks, including native Caddy timing/privacy and parent recovery sequencing.
No live diagnostic ran. W-168 aggregate deadline and clock-correlation bindings
are implemented and locally qualified. Exact successor preparation remains
pending; W-147 attribution and AC-013 remain unresolved.

November 16 W-169: the exact temporary timing-diagnostic successor is locally
qualified and sealed for separate live review. The defined Caddy graph passes
16 offline owner cases; the sealed parent verifies its 236 inputs without target
contact. W-167/W-168 diagnostic and W-166 recovery bindings are included. No live
attempt occurred, W-147 attribution and AC-013 remain unresolved, and the accepted
Kuma/loopback Webmin state is unchanged. WORK.md owns the exact command and scope.

November 16 W-170: the approved diagnostic ran once and failed at primary HTTPS
(parent 2, Caddy 1). Direct backend/denial passed; paired Caddy release/inventory
restoration, both fresh post-resume natural monitor cycles and native Webmin
loopback restoration passed. The new replication alert was followed by accepted
health on both nodes (W-172). No browser or scan acceptance started.

Original request/resource correlation failed because the nonzero owner path
omitted its evidence marker (W-171). Separate local correlation of hash-verified
readbacks retains overlapping memory.high increments but does not establish the
timeout cause. Original failed receipts remain unchanged. W-147/AC-013 remain
pending; the consumed operation is terminal-pending for separate archival (W-173).
No retry, new inspection, promotion or publication is authorized.

November 16 W-174: Aaron approved narrowing the next diagnostic to the primary
IPv4 path, sequential equivalent direct/proxy requests and bounded request/resource
evidence. No production health-check serialization decision was made. W-173's
23-file terminal archive is prepared and locally checked for separate publication
authority; consumed inputs are unchanged. No new candidate is sealed and no target
contact occurred. This scope decision supplies no new evidence for W-147 or
AC-013; the result remains Partial.

November 16 W-173: the approved exact terminal archive was committed at
`a6491d0795e4493e000f3afe81be09d01514fffd` and atomically pushed with annotated tag
`caddy-webmin-proxy-timing-diagnostic-terminal-2026-11-16`. Remote branch/tag
identities match; mandatory commit hooks passed and the server worktree is clean.
Consumed operation inputs remain present pending local cleanup. No new diagnostic
or target acceptance occurred; W-147/AC-013 remain unresolved and the result remains
Partial. Monitoring record updates are local, outside this publication scope.

November 16 W-175/W-171: archived-operation cleanup and failed-path evidence
handoff are locally qualified. W-174's primary/IPv4 control path passes focused
local checks, including immediate restoration without secondary exposure. Native
backend request/received-header evidence remains open as W-176; no complete
successor is sealed. The stream is clean and operation inactive; changes remain
uncommitted. No target contact, retry, promotion or publication occurred. W-147
and AC-013 remain unresolved; this result remains Partial.

November 16 W-176: bounded backend-interface evidence is implemented and locally
qualified in the existing collector/parent. Both foreground request IDs, safe
received-header comparisons, response/close events, possible health overlap and
resource coverage are linked. Native offline capture, privacy, correlation and
parent recovery checks passed. Interface receipt does not prove internal CGI
execution or complete HTTP-body delivery; missing response evidence stays unknown.
No candidate is sealed and no live contact occurred. W-147/AC-013 remain unresolved;
this result remains Partial.

November 16 W-177/W-178: routine onboarding no longer stages the application
fragment or publisher on the secondary. The secondary control recipe remains;
application contents arrive through managed replication after primary acceptance.
All 18 offline owner cases pass, including primary-only success/failure restoration
without secondary contact. The existing Webmin observer/parent qualification hashes
still match, and the exact primary/Pi input syntax passes. W-178's review command
and seal are tracked in WORK.md. No live execution or publication occurred;
W-147 and AC-013 remain unresolved and W-157 remains uninstalled.

November 16 W-179: the approved W-178 parent ran once and exited 2 before Caddy
launch. The direct primary-to-backend login-page request returned HTTP 401 in
about 51 ms, failing the expected HTTP-200/login-page gate. Backend-interface
capture confirms a matching request, prompt 401 and connection close, with no
reported capture issues/drops. Resource samples show no Webmin high/max/OOM events;
this is not capacity acceptance or attribution of the historical timeout.
Exact Webmin loopback restoration and terminal-state verification passed. No
Caddy activation, secondary contact, browser/scan workload or DNS change occurred.
The approval is consumed and inputs/receipts are preserved. W-180 must reconcile
the response contract and not-run proxy evidence locally; W-147/AC-013 remain open.

November 16 W-180: login-response contract reconciliation found a diagnostic
User-Agent defect. Native pinned Webmin 2.670 forces HTTP authentication for agents
containing `webmin`. An offline header-only A/B/A comparison returned 401 Basic,
200 with login form, then 401 Basic. The existing 200/login requirement remains;
a three-site neutral-User-Agent patch is prepared but unapplied (W-181). This is
consistent with W-179's direct 401 and does not explain the earlier HTTPS timeout.
Fleet onboarding instructions now preserve this request-contract distinction.
No live work occurred; W-147/AC-013 remain unresolved.

November 16 W-181: the three-site User-Agent correction is integrated locally.
The parent now reports a pre-Caddy comparison as not run while preserving failure
and backend restoration. Three primary parent-flow scenarios, focused client/wire
checks and neutral owner checks pass. The never-executed Caddy child definition
is withdrawn; the stream is clean/inactive. The consumed parent's 241 retained
inputs and receipts remain preserved. No new candidate, live retry or publication
is authorized; W-147/AC-013 remain unresolved.

November 16 W-182: a new 241-input primary/Pi diagnostic candidate is sealed
from W-181's corrected sources. Current owner execution/recovery qualification,
evidence rejection checks and exact parent/input checks pass locally. The candidate
is unexecuted and requires separate live approval. Prior attempts remain preserved;
no new target result, timeout attribution or Webmin browser acceptance is claimed.
W-147/AC-013 remain unresolved and W-157 is uninstalled.

November 16 W-183: the approved primary/Pi diagnostic ran once and failed-consumed
(parent 2, Caddy 1). Direct login HTTP passed; primary HTTPS timed out after TLS
and delivery of the marked request to the backend. Recorded foreground headers
match. Actual Webmin samples show memory pressure and a later OOM kill at the
unchanged cap, followed by cgroup replacement; the cause remains unconfirmed.
Aggregate correlation rejected close-only flows (W-184), so it is not accepted.
Primary restoration/readback, natural monitor acceptance and exact Webmin loopback
restoration passed. No secondary or browser/scan work occurred. W-147/AC-013 remain
open; W-185 tracks the required terminal archive. No retry or publication authority.

November 16 W-186: Aaron authorized publishing all pending changes. Server commit
`bda63a4` and its annotated primary-login diagnostic terminal tag are pushed and
remote-verified. This monitoring commit publishes the corresponding tracking
record and narrow verified-hash exclusions. Current-production CI profiles and
publication hooks pass locally; the separate terminal coverage-profile failure
remains recorded. Private evidence is excluded. Neutral cleanup and further live
work have not run; Webmin acceptance remains pending.
