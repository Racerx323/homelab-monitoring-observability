# Active monitoring work ledger

## Current position

**Accepted November 25, 2026.** All four acceptance criteria passed. [Result](RESULT.md). The monitoring owner repeats the delivery test after alert-route changes (W-005).

## Activation and review history

November 23 activation used the authenticated dashboard. Eight public service checks and six private host checks were UP. All fourteen use Apprise Alert. DNS now matches the expected record on the IPv4 and IPv6 VIP paths, proxy HTTPS requires 204, and the five existing fast checks use two retries 30 seconds apart. The NTP checks retain their five-minute schedules. The Apprise check already used /status. ICMP from Kuma failed with spawn EPERM. All six hosts answered management TCP/22, including the primary NTP host at .50 confirmed from the NTP owner. Host notifications were enabled after successful TCP checks. The status page contains only the eight service checks.

Kuma recorded a private test monitor UP at 23:43:42 UTC, DOWN at 23:43:54 and UP at 23:44:03. Only its expected HTTP response changed. The temporary monitor was removed after recovery. Aaron confirmed receipt of both the DOWN and UP messages on Discord, email and Pushover for this test. A subsequent Pi sample showed Kuma active, zero restarts, about 214 MiB charged against the 320 MiB limit, zero cgroup high/max/OOM events and about 581 MiB host memory available. This is an early workload sample.

Aaron approved the proposed service/host coverage, retry settings and end-to-end delivery strategy. The proxy currently accepts HTTP 200–299; the intended health response is exactly 204. The application database was opened read-only for this review.

Aaron selected user-visible availability for services and individual reachability for hosts. The Caddy owner defines HTTP 204 for the proxy root. The DNS owner publishes the resolver VIP at 10.1.0.55 and the selected local A answer at 10.1.0.55. The production host inventory lists six distinct machines across its overlapping roles. Proposed settings and delivery verification are in the plan. The live results above supersede this pre-change observation.

On November 23 the status page published seven monitors in three groups. Each had 100 successful recent heartbeats and a reported 24-hour uptime of 100%. The dashboard returned its application shell. Private settings and any unpublished monitors were outside the observed inventory.

| Status-page group | Published monitors and probe types |
| --- | --- |
| Monitoring & Observability | Munin Master (keyword) |
| Notification | Apprise-API (HTTP), SMTP Relay (TCP port) |
| Core Services | DNS Cluster (DNS), NTP and NTP1 (NTP), Proxy Cluster (HTTP) |

One approved read-only Pi inventory on November 23 found seven configured monitors, all enabled and all published. Each uses notification assignment 1 and zero retries. Five poll every 60 seconds and both NTP monitors poll every 300 seconds. The stored timeout field was 48 seconds throughout. Notification destination and delivery were outside this check.

DNS Cluster requests the A record for `pihole.local.theama.co` from `10.1.0.55:53`. Proxy Cluster checks the root of `https://proxy.local.theama.co` with TLS verification. The inventory did not establish an expected DNS answer or the accepted HTTP status ranges. Munin checks its HTTPS root for the keyword `munin`. Apprise HTTP and SMTP TCP probe the same host on different ports.

[PLAN.md](PLAN.md) owns scope, acceptance and recovery. Record observed outcomes in `RESULT.md` at closeout.

| ID | Status | Work and closure condition |
| --- | --- | --- |
| W-001 | Resolved | AC-001 passed. Aaron accepted the observed public membership of all 15 monitors. |
| W-002 | Resolved | AC-003 passed on November 23. Aaron confirmed both transitions through Apprise Alert on all three destinations. |
| W-003 | Resolved | AC-002 passed for the normal polling window recorded below. |
| W-004 | Resolved | AC-004 passed. The first scheduled archive on svmf passed isolated restore verification and the dashboard returned HTTP 200. |
| W-005 | Deferred | Aaron deferred recurring end-to-end notification tests. The monitoring owner repeats the verified DOWN/UP test after an alert-route change. Revisit scheduled delivery checks here if automatic detection of silent delivery failures becomes necessary. |

The private Kuma monitor `External heartbeat` (ID 16) sent an accepted first ping to the Healthchecks.io check `Uptime Kuma heartbeat`. Its period is five minutes with ten minutes of grace and a direct email integration. The attended test paused the sender at 18:02 CST on November 23. Healthchecks reported DOWN at 18:17:20 CST and Aaron confirmed the direct DOWN email. After resuming the monitor, Kuma recorded a successful check and Healthchecks returned to UP. The public status page still lists eight service checks. Aaron received the direct recovery email showing UP at 18:17:43 CST and 22 seconds of reported downtime. This completes the external heartbeat test.

## Active workload on the Pi

On November 23 from 18:25 to 18:37 CST, all 15 monitors were active across 13 one-minute samples. The local dashboard returned HTTP 200 on every probe. The service kept the same invocation, recorded zero restarts and had zero memory high, max or OOM events. Sampled service memory ranged from 210.5 to 211.7 MiB against the 256 MiB high threshold and 320 MiB limit. Host available memory stayed above 579 MiB.

SQLite used six more 4 KiB pages (24 KiB) from its free list as the latest heartbeat ID advanced by 152. The main database stayed at 3,108,864 bytes, the WAL at 4,478,472 bytes and shared memory at 32,768 bytes across all samples. The filesystem retained 23.7 GiB free. This establishes normal polling headroom over two complete five-minute intervals. A daily storage rate or retention forecast requires a longer baseline. Private sample receipt: `operational-receipts/active-workload-0gNhp3qW.jsonl`.

## November 24 inventory and backup review

The Pi’s read-only inventory showed 15 enabled monitors, each with a latest UP result. The two DNS checks have explicit answer-equality conditions. IDs 1–14 use notification assignment 1. ID 16 uses the separately verified external email path. The [operations guide](../../uptime-kuma/docs/OPERATIONS.md#monitor-ownership-and-coverage) maps checks to their component owners.

Fast service and host checks poll every 60 seconds with two retries at 30 seconds. The configured timeout field is 48 seconds for the original seven service checks and 10 seconds for IPv6 DNS and the six host checks. Both NTP endpoints poll every 300 seconds with zero retries. The external heartbeat polls every 300 seconds with zero retries and a 15-second timeout.

Both the stored membership and anonymous status-page response included all 15 monitors. This supersedes the November 23 eight-service observation. The external monitor is now named Healthchecks.IO Heartbeat. The earlier plan selected private host and external checks. Aaron accepted the current 15-monitor membership on November 24.

The administrator and backend completion backups on the workstation cover installation. Neither contains the current monitors or alert assignments. No verified recurring copy covers the active workload. Proposed policy for owner decision: nightly off-node backup, seven daily copies, with an isolated restore of the populated data before claiming coverage.

Aaron selected svmf (10.1.3.83) for recurring backups. Its host inventory identifies the Munin and notification roles and supplies no Kuma backup directory. The proposed policy is in [PLAN.md](PLAN.md#recurring-backup-policy).

The read-only destination check reached J1-SVMF at 10.1.3.83 via host-key-verified SSH as pi. The local NVMe ext4 root filesystem reported 1.7 TiB available. The existing parent `/var/backups` is root:root mode 0755. The pi account could inspect metadata through noninteractive sudo and had no direct write access to the parent. No Kuma destination was found in the inspected storage roots. Use `/var/backups/uptime-kuma/` for implementation, with a dedicated writer, directory mode 0700 and archive mode 0600. Provisioning, a transfer under the actual writer identity and populated restore verification remain pending.

The [nightly backup procedure](../../uptime-kuma/docs/OPERATIONS.md#nightly-populated-backup) prepares a receiver-initiated pull, a brief stopped-data archive, seven daily copies and isolated database restoration. The proposed time is 02:30 America/Chicago. Production identities, timer activation, recovery timing and the first off-node populated restore await deployment.

Local qualification restored a populated sample, retained seven of eight daily archives with mode 0600, and rejected both a truncated transfer and a restored assignment referencing a missing notification. Both failure cases preserved the seven completed copies and removed temporary extraction data. The shell syntax, SSH configuration, systemd units and calendar were checked locally. Target SSH enrollment, transfer, service interruption duration and scheduled execution remain untested.

The first-install review confirmed the restore query columns against the retained installation database. Two paths need explicit first-run evidence: a same-day receiver invocation can succeed without transferring data, and counts alone cannot prove that memberships or notification assignments survived. The [attended procedure](../../uptime-kuma/docs/OPERATIONS.md#attended-first-transfer) now checks a fresh archive and restore receipt, compares source and restored rows, and measures dashboard availability across the source stop/start. Installation, the first transfer and AC-004 acceptance remain pending.

## First attended backup attempt, November 24

Installed the dedicated receiver, key, private directory and disabled timer on svmf, and the restricted export account, forced command and sudo rule on the Pi. The receiver’s Python 3.11.2 lacks the tar extraction filter used in the prepared code. Before installation the receiver was adjusted to copy regular-file contents into private scratch, accepting directories and rejecting links and traversal. A local populated restore and both rejection checks passed.

The single authorized attempt reached the exporter and restarted Kuma. Its local HTTP probe exhausted 15 one-second retries while the listener was starting, so the exporter exited before sending the checksum or archive. The receiving unit failed; the backup directory contained only its lock. No populated restore or comparison ran. The workstation saw dashboard failures spanning at least 23.0 seconds. The continuous sampler stopped when the receiver failed, so the exact recovery time was missed. Follow-up checks confirmed the Pi unit active and both loopback and normal HTTPS dashboard returning 200. The installed receiver timer was inactive and disabled. No retry ran.

The local exporter now uses the existing startup acceptance cadence (initial probe and 60 retries three seconds apart) and requires HTTP 200. Its checksum stream stays clean, and exhaustion reports the final HTTP result and curl exit on stderr. The attended workstation observer records the receiver exit and keeps sampling the public-facing dashboard until recovery or a bounded timeout, preserving transfer failures when the dashboard recovers. Local checks exercised delayed readiness beyond the old limit, probe exhaustion, transfer failure followed by recovery, persistent dashboard failure and successful completion. Production still has the previously installed exporter. No live transfer, installation or timer change was part of this review.

## Attended retry review

At 11:56 CST November 24, host-key-verified reads confirmed stable boot identity within the inspection on each host. Kuma was active and both the loopback and fleet HTTPS dashboards returned 200. The installed Pi exporter (root:root 0755) had SHA-256 `6511d4674d4019455e5b9c1c8eed5f90e9536d7d1ccaa77ebab745831f9a28cd`. The reviewed replacement is `c379557c3a71bd5010dace346d75599d6bbab691f6bf00e2ef3bf336f129d7d2`; the workstation observer is `dd416ccd675da39cb18b1b6924d1d2028f5f9a8293e3209163feffe48c013acf`.

The svmf receiver, service, timer and SSH configuration matched their repository hashes. The service still showed the earlier failed attempt. The timer was inactive and disabled. The writer verified its 0700 destination and the absence of the receiver-local November 24 archive, including a dangling link at that name.

Proposed scope: admit both hosts with fresh boot identities and verify continuity during execution. Recheck the revisions, dashboard, timer and unused archive path for the receiver’s current date. Replace only the expected Pi exporter and read back its digest. Capture the source inventory, then run one receiver start under the reviewed observer. Confirm dashboard recovery, receiver status and restored rows from the fresh archive per the [attended procedure](../../uptime-kuma/docs/OPERATIONS.md#attended-first-transfer). Preserve failures and keep scheduling disabled.

## Attended populated backup accepted

On November 24 the corrected exporter was installed and verified by hash. One attended transfer succeeded. The dedicated writer on svmf saved `/var/backups/uptime-kuma/2026-11-24.tar` (3,891,200 bytes, mode 0600). The receiver verified the source checksum and restored SQLite integrity. An independent read of the received archive matched the source rows for 15 monitors, four groups, 15 status-page memberships and 14 notification assignments. The restored database had one status page.

Kuma returned to active and the fleet dashboard recovered to HTTP 200. The successful dashboard samples bracketing the interruption were 20.7 seconds apart (2026-11-24T17:58:25.723904+00:00 to 2026-11-24T17:58:46.411026+00:00). Both hosts retained their admitted boot identities. The timer was inactive and disabled at exit. The earlier failed attempt is preserved separately. Private receipts: `operational-receipts/attended-retry-_z3x2qhf/`. AC-004 has one verified populated copy; a scheduled run remains open.

## Nightly timer activation review

The attended run verified the installed receiver and populated archive. The reviewed timer selects 02:30 America/Chicago with persistent catch-up. At the November 24 review, the next calendar occurrence was November 25 at 02:30 CST (08:30 UTC). The prior attended archive covers November 24. A same-day catch-up can exit successfully without writing another archive.

On approval, recheck the installed timer and service against their reviewed hashes on svmf, enable and start only the timer, then read back its enabled, waiting state and next elapse. After the first natural firing, correlate the timer’s last trigger with the new service invocation, successful exit, dated archive and populated restore receipt. Verify writer ownership, mode 0600 and dashboard recovery. If the invocation fails, preserve its journal and prior archives, disable scheduling pending review, and check Kuma availability. Record AC-004 as passed only after a fresh scheduled archive meets these checks.

Aaron approved activation on November 24. The installed service, timer and receiver matched the reviewed hashes. On svmf the timer is enabled, active and waiting for November 25 at 02:30 CST. Its last-trigger field was empty at activation. The workstation scheduled a one-time verification at 02:47 CST, after the receiver’s 15-minute timeout; SSH from the verification service context passed. The verifier checks the natural trigger, receiver result, dated archive, restore receipt, owner/mode and dashboard. It records the outcome in `.local-evidence/uptime-kuma/operational-receipts/nightly-activation-l5EgpUrl/first-scheduled.json`. The workstation session and SSH agent must remain available for that scheduled verification. If interrupted, reconcile the retained svmf journal and archive directly.

## First scheduled backup accepted

On November 25 at 02:30:18 CST the timer on svmf triggered the receiver. The service exited 0 and its invocation ID matched the restore journal entry for `2026-11-25.tar`. The archive was a 5,488,640-byte regular file owned by `kuma-backup`, mode 0600. The isolated restore counted 15 monitors, one status page, four groups, 15 memberships and 14 notification assignments, matching the attended baseline. At 02:47 CST the verifier recorded dashboard HTTP 200 and an enabled, active timer. Private receipt: `operational-receipts/nightly-activation-l5EgpUrl/first-scheduled.json`.
