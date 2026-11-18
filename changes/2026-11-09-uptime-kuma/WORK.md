# Work ledger: initial Uptime Kuma deployment

## Current position

- Status: Existing Kuma service/dashboard accepted. Aaron approved W-127's
  network/radio dispositions, then required standard-browser Webmin access;
  the SSH-only profile does not satisfy this revised requirement (W-128).
- Last updated: November 17, 2026 (America/Chicago).
- Next action: Seal W-227's locally qualified paired browser candidate for
  separate live review. Exact private owner authorization passes with 19 current
  whole-path cases and nine altered-evidence rejections. Actual payload and parent
  bindings pass; W-229/W-230 are resolved. Only the private review projection is
  defined; main Caddy remains clean/inactive. No live bundle or launcher is sealed.
  W-147/AC-013 remain open and W-157 is not installed. W-231 source publication
  is in progress under Aaron's all-changes approval; the server commit is remote-
  verified. No live contact, browser workload or retry occurred.
- Document roles: [PLAN.md](PLAN.md) owns scope/criteria; this ledger owns work and
  decisions; [RESULT.md](RESULT.md) owns the accepted scope and pending Webmin extension. Permanent design and
  procedures remain in [architecture](../../uptime-kuma/docs/ARCHITECTURE.md) and
  [operations](../../uptime-kuma/docs/OPERATIONS.md).

## Tasks and findings

| ID | Task or finding | Acceptance/scope link | State | Closure requirement | Resolution / evidence / follow-up |
| --- | --- | --- | --- | --- | --- |
| W-001 | Define initial functional scope. | AC-009 | Resolved | Explicit service/monitor/notification boundary. | Aaron chose service first; monitors and alerts follow later. No test alert is included. |
| W-002 | Fix the dashboard name and access path. | AC-004 | Resolved | User agrees to one internal HTTPS name. | Aaron approved `uptime.local.theama.co` through existing Caddy on November 9. This does not approve source publication or live reload. |
| W-003 | Establish SSH identity and read-only host baseline. | AC-001, AC-008 | Resolved | Confirm intended target and collect bounded, non-mutating resource/runtime/network observations. | Read-only SSH succeeded with strict existing host-key verification. Host/model/OS/ARM64 and IPv4 match; hostname reports `j2-svpi3bmf.local.theama.co`. About 745 MiB memory available and 24.65 GiB root free at observation. No Podman or Kuma account/path was found by the scoped checks. Findings W-013 through W-016 retain limitations. |
| W-004 | No governing architecture exists. | AC-002, AC-010 | Resolved | Prepare one proposed permanent architecture, with rationale and unresolved choices explicit. | Permanent architecture and operations drafts now define the complete candidate. Live approval reviews this design; reconcile observed behavior at closeout. November 12 W-125: architecture reconciled with accepted runtime, watchdog, startup and DNS/Caddy paths; remaining network/radio evidence limits explicit. |
| W-005 | Qualify a pinned ARM64 image for the Pi 3B+ resource envelope. | AC-001, AC-002, AC-006 | Resolved | Verify upstream stable release, actual architecture manifest/digest and resource budget. | ARM64 registry digest, local configuration ID and offline archive identity are separately verified in the sealed manifest. runtime-smoke-pxk7g5w0 passed actual AMD64 startup/restart/restore under the proposed controls; about 115 MB initial memory is an observation, not ARM64 capacity proof. Actual Pi execution and resource acceptance remain pending.  The proposed IPv6 loopback proxy adds a 16 MiB cap: the isolated corrective gate is 528 MiB and the future combined-foundation floor is 720 MiB. Requalify on the Pi; do not infer combined capacity from the isolated diagnostic.  Actual isolated corrective trial passed: Kuma peak 117.73 MiB, proxy 2.04 MiB, no memory-high/max/OOM events. Preflight available 728,184 KiB (711.12 MiB) exceeded the 528 MiB isolated floor but was 9,096 KiB below the future 720 MiB combined floor. Reconcile admission/capacity locally before a remaining-deployment candidate; no combined acceptance is claimed. November 11: actual pinned ARM64 runtime passed both combined checkpoints and scan-time reserve/pressure checks under the user-approved staged admission policy. Initial-service workload only; later monitors/load need review. |
| W-006 | Define runtime ownership, local persistence and safe initial administration. | AC-003, AC-005, AC-008 | Resolved | Establish runtime/service identity, filesystem/ownership, backend restriction and bootstrap path without stored chat credentials. | Proposed Quadlet uses UID/GID 1000, protected local data, read-only rootfs and loopback-only bootstrap. Native observer checks actual mounts, ports, limits, user counts and authentication setting without reading credentials. Actual target acceptance and operator account creation remain pending. November 11: actual runtime/administrator, persistent data, mounts/identity, backup/restore, guarded backend and ingress-denial checks passed. One active user, authentication enabled, no monitors/notifications; no credentials collected. |
| W-007 | Prepare DNS and Caddy onboarding under their owners. | AC-004, AC-008 | Resolved | Reuse current application onboarding and source ownership; qualify both address families and WebSockets. | Preparation history: DNS read-only baseline completed; append-only six-record proposal and application fragment remain outside accepted production configuration. Existing immutable local image 1bab90ae19f4d9091b9529336ef023ecce44f96cf2bad6016ce95dbc04c64156 passed Unbound 1.17.1 candidate checking and Caddy 2.11.4 adaptation for both node environments. native-config-gwfqkdh5 retains inputs/status. No target staging, TLS provisioning or live application/auth/WebSocket acceptance. Owner execution definitions remain to prepare; application authority now homelab-monitoring-observability. November 12: accepted primary-first Caddy release and W-106 private/passive evidence are joined by W-124 accepted DNS deployment and normal-name HTTPS 200 over both families. |
| W-008 | Prepare simple declarative deployment, acceptance and rollback. | AC-002, AC-006, AC-008 | Resolved | Reuse repository automation conventions; validate real entrypoints and failure boundaries. | Complete native coordinator includes controller integrity checks, boot/address prerequisites, offline runtime, boot proof, private administrator pause, actual backup/restore and guarded backend promotion. Frozen controller-only preflight passed. Runtime failure retains guard/data and requires residue review; earlier accepted prerequisites may remain. Actual execution/recovery acceptance pending. November 12 W-125: accepted native backend successor, retained recovery/containment evidence and separately accepted owner proxy/DNS operations satisfy implementation/qualification. Consumed definitions are not reusable maintenance commands. |
| W-009 | Define and qualify consistent backup/restore and retention. | AC-003, AC-007 | Resolved | Full local-data backup method, isolated restore proof, storage policy and off-node destination explicit. | Production restore checker passed against actual stopped application data in restore-final-khncnm5o/restore-cnpz4fqz/receipt.json, including immutable configuration-ID execution, database/authentication counts and cleanup. First-deployment archive budget is 64 MiB/10,000 members with no monitors/notifications; future workloads need review. Live administrator-bearing backup and protected controller copy remain pending; no recurring backup service is claimed. November 10 administrator-completion actual ARM64 backup/off-node identity, isolated restore, cleanup and source recovery passed; protected 307200-byte controller archive retained. No recurring backup service is claimed. |
| W-010 | Qualify and seal the concrete operation. | AC-001 through AC-009 | Resolved | Local checks pass; remaining target checks, immutable inputs, exact command and complete scoped bundle are reviewable. | One expanded offline candidate is sealed; frozen controller and actual boot-input checks pass locally. Exact hash, graph, command, scope, target acceptance and recovery are recorded below. Aaron approved and executed this exact bundle November 10; terminal APT simulation failure retained below. Approval is consumed; no replay or changed-input retry is authorized. |
| W-011 | Execute the authorized operation and independently accept or recover. | AC-001 through AC-009 | Resolved | Required observed criteria pass, or failed/partial outcome and recovery/residue are recorded honestly. | Partial installation accepted boot/address prerequisites and all 29 package pins; Webmin remains contained after failed HTTP acceptance. Kuma image/definitions/data were installed and started, but loopback observer connection timed out; native rescue and independent inspection confirm stopped services. Private administrator acceptance, startup reboot, backup/restore, guarded backend, schedule and final DNS/Caddy HTTPS remain pending. Consumed operations are preserved; only a newly authorized continuation may proceed.  Subsequent approved loopback correction passed actual Pi HTTP acceptance over every container/direct/published family path, then returned all four units to verified stopped/guarded state. Remaining criteria above are still pending. November 11 successor exited 0: service foundation, preserved reboot identity, administrator, fresh backup/restore, guarded backend, combined scans, schedule and permanent startup accepted. DNS/Caddy HTTPS still pending; this is service-stage acceptance, not project closeout. November 12 W-124 accepted DNS/Caddy HTTPS; service execution is complete. Final AC-008 disposition remains with W-020/W-076; see partial RESULT.md. November 12: W-127 approval accepts the initial-deployment preservation boundary; all required service criteria are reconciled in RESULT.md. |
| W-012 | Reconcile permanent documentation and close the record. | AC-010 | In progress | Operations and architecture are current; every finding has disposition; write criterion-linked RESULT.md. | Keep repeatable procedures and enduring design out of the change journal. November 12 W-125 reconciled permanent documents and wrote criterion-linked Partial RESULT.md. Final closure waits on W-020/W-076; no scope waiver. November 12: Aaron approved W-127; permanent docs, criterion-linked accepted result and all ledger dispositions reconciled. No publication authorized. Reopened for Aaron's W-128 standard-browser Webmin requirement; prior dispositions remain approved. |
| W-013 | Requested permanent ULA is not configured. | AC-001, AC-004, AC-008 | Resolved | Establish the network owner's persistent address design and review the exact correction before deployment. | Native NetworkManager checkpoint operation prepared by the network owner appends only the permanent ULA, preserves automatic methods/routes and verifies a fresh SSH connection before committing. Source is included in the sealed bundle. No address change has occurred. Accepted November 10 through native checkpoint/reapply, fresh SSH, DAD and preserved route checks; independently retained after the later failure. |
| W-014 | Memory cgroup controller is unavailable. | AC-001, AC-006 | Resolved | Verify kernel/boot cause; prepare and authorize any needed correction/reboot, then observe the actual controller and resource enforcement. | Exact original/proposed boot bytes and native reboot/recovery play are included in the sealed candidate. Actual memory-controller availability and resource enforcement must pass after authorized reboot. No boot change has occurred. Accepted November 10 after the first reboot: changed boot ID, exact stored boot bytes, memory controller present, radio softblocks retained. Later residue inspection confirms controller remains active. |
| W-015 | Radio-disable claim needs finer verification. | AC-001, AC-008 | Resolved | Distinguish interface/rfkill/firmware state from daemon state without changing either. | Both Wi-Fi and Bluetooth are soft-blocked by rfkill. Daemon activity did not mean enabled radios. Preserve this policy; no radio changes needed. |
| W-016 | The first collector did not resolve sbin-only swap tooling or the firmware boot mount. | AC-001 | Resolved | Read `/proc/swaps` or the absolute swapon path and inspect the actual firmware mount. | Absolute swapon and /proc/swaps identify unused zram swap; firmware is mounted separately at /boot/firmware on vfat. Initial PATH/mount limitations retained; no package repair needed. |
| W-017 | A bridged container's published port may bypass an INPUT-only firewall rule. | AC-005, AC-008 | Resolved | Qualify the guard against the actual DNAT/forwarding path, including allowed proxy sources, denied direct clients and unchanged SSH. | Final actual-Ansible-rendered guard passed packet-y9e7vocf: native IPv4/IPv6 DNAT/forwarding packets, all five allowed proxy sources, both denied sources, production counter parser, unchanged SSH/unrelated table, and removal recovery. Target Podman path still requires acceptance. November 11 actual Pi ingress trial accepted: both proxy nodes returned dashboard 200 over both families; unapproved source HTTP timed out, deny counters rose by 6 IPv4/3 IPv6, SSH remained reachable, and temporary client was removed. |
| W-018 | Caddy source selection and current release need target observation. | AC-004, AC-008 | Resolved | Inspect both proxies read-only; establish actual per-family routes to Kuma and current immutable-release identity before defining the final guard/onboarding operation. | Both inspections succeeded; Caddy/Keepalived are active and native release-hash checks pass on the same release. IPv4 selects node .53/.54; active-node IPv6 selects shared Proxy ULA ::56, standby selects ::54. Proposed guard explicitly allows observed Proxy ULA plus both permanent node ULAs, avoiding unnecessary proxy route changes. No reload or failover occurred. Private proxy0/proxy1 receipts retain the baseline. |
| W-019 | Recovery access for the required boot prerequisite was unknown. | AC-001, AC-006, AC-008 | Resolved | Identify an independent way to recover a Pi that fails to return after reboot. | Aaron confirmed physical device/microSD access and console KVM. Candidate must preserve the original boot file and distinguish manual recovery from verified remote recovery. This does not authorize reboot. |
| W-020 | A rootful dual-stack bridge may change IPv6 forwarding/RA behavior. | AC-004, AC-008 | Deferred | Verify the target runtime's effects and preserve existing Router Advertisement routes and global IPv6 throughout installation and reboot. | Netavark enables global forwarding; this NetworkManager-managed host already uses kernel eth0 accept_ra=0 with automatic IPv6. No generic accept_ra=2 edit is proposed. Native observer requires preserved automatic methods, persistent ULA, global addresses and IPv6 default routes after runtime start and reboot. A separately timed periodic RA renewal has not been qualified. November 11 runtime/preflight again accepted required addresses and routes after startup and promotion. Separately timed RA renewal remains unqualified; no new live observation authorized. November 12 W-125 re-read before/after-reboot and backend-promotion receipts: auto/auto methods, permanent ULA, global IPv6 and RA default route retained with forwarding=1/accept_ra=0. No timed renewal series exists in these receipts; no new probe or sysctl change. Network/runtime owner must establish renewal evidence or obtain an explicit acceptance decision. November 12: Aaron approved initial-deployment acceptance from retained startup/reboot/promotion evidence without claiming timed renewal. homelab-network/runtime owner retains this record; timed observation due before the next host networking/container-runtime migration or earlier reported IPv6 route/address failure. Residual unobserved-renewal risk accepted; no live work authorized. |
| W-021 | The local smoke helper could lose its failure receipt or leave a container after a launch timeout. | AC-002, AC-007, AC-008 | Resolved | Register attempted container names before launch, clean only matching task labels, preserve the original failure and always retain cleanup results. | Cleanup corrected; revised test records its own source hash. runtime-smoke-pxk7g5w0 passed startup, restart and restored-data checks; both task containers removed. No homelab target contacted. |
| W-022 | Native local Quadlet rejected the proposed LogOpt key. | AC-002, AC-006 | Resolved | Use a log-bound configuration accepted by the relevant generator and preserve the first failed parse. | Target 5.4.2 documentation supports LogOpt, but the older local generator does not. The equivalent native PodmanArgs log bound passes both; definitions-n44a_l_4 generated bootstrap and exposed services successfully. definitions-d22wf7ed preserves the first failed parse. |
| W-023 | Local packet fixture could not inspect PID 1's network namespace after entering a user namespace. | AC-002, AC-005 | Resolved | Compare against the caller's captured network namespace identity and rerun in disposable namespaces. | Caller now supplies its captured namespace identity, checked before any network setup. packet-gr102hne passed under isolated namespaces; no host firewall was touched. |
| W-024 | Local forwarded IPv6 packet test timed out for an allowed proxy source. | AC-004, AC-005 | Resolved | Establish whether the fixture path or candidate guard is responsible and retain the failing observation. | Initial packet-0vhme_n4 failure retained. packet-b946stla confirmed failure even without the guard and an unresolved backend neighbor. Fixture now waits for link-local DAD; packet-gr102hne passed both address families. Target acceptance is still required. |
| W-025 | Minimal runtime package simulation does not establish which firewall driver the installed Netavark will use. | AC-002, AC-004, AC-008 | Resolved | Explicitly qualify a supported driver and its complete package/configuration inputs before sealing the operation. | Explicit nftables driver is supported by the pinned containers-common/Netavark versions. All nine packages were downloaded and verified against target APT metadata; ARM64 OCI archive is acquired and separately hashed. Native offline APT simulation rejects upgrades/removals; target installed driver and port behavior remain pending. November 11 accepted pinned installed package/configuration identities and actual dual-stack runtime, published backend and denied-source packet behavior. No package/driver change was needed. |
| W-026 | Existing Pi memory-controller planner is specific to Nautobot's USB storage baseline. | AC-001, AC-006 | Resolved | Prepare an exact append-only boot correction bound to this Pi's saved original bytes and recovery path. | MicroSD-specific planner preserves exact original bytes/line endings, rejects drift/conflicts and passed five regression tests. Native phase preserves on/off-node copies and verifies controller/file/boot identities; reachable recovery restores the original, otherwise stops for physical intervention. Definitions and frozen controller locally qualified; target reboot/recovery not executed. November 12 W-125: W-014 accepted boot correction and the retained staged reboot/runtime evidence supersede this stale pending status. Actual controller enforcement and startup reboot passed; emergency physical recovery was not exercised. |
| W-027 | DNS readiness is outside the approved Caddy-only inspection scope. | AC-004, AC-008 | Resolved | Obtain bounded read-only authority for the owning Unbound/Pi-hole readiness procedure, then establish exact source/live baselines and conflicts before preparing mutation. | Aaron approved bounded read-only DNS inspection; both node receipts passed, all four services active and VIPs coherent, dashboard A/AAAA NXDOMAIN. W-028/029 reconcile ordering differences and the effective include graph without conflicts. Bounded readiness is complete; DNS mutation and final HTTPS remain W-007. |
| W-028 | Both live Unbound local-zone files differ from the repository source. | AC-004, AC-008 | Resolved | Explain exact byte/semantic differences and preserve unrelated deployed records; do not overwrite drift with repository content. | Both live files have identical saved SHA-256 and root:root 0644. Parsed directives match repository content; ordering differs. Private proposal appends six records to exact live bytes without removal/reordering. Native Unbound candidate check passed in native-config-gwfqkdh5; no live mutation. |
| W-029 | Unbound 1.17.1 does not return its include graph through the attempted -o include query. | AC-004, AC-008 | Resolved | Read only include directives and file identities through a bounded, symlink-aware traversal, retaining the failed native query. | Both -o include and -o local-data queries failed and remain retained. includes0/includes1 collected the active process's main config and all five regular config files, 70 relevant directives per node, without reading private key files. No Kuma host/service/address conflicts. Native active configuration checks passed separately. |
| W-030 | The include collector's controller display assumed a different JSON shape. | AC-004, AC-008 | Resolved | Preserve successful target receipts, recover existing output locally and correct presentation without replaying SSH. | Both target collections exited 0 with no truncation before local KeyError. Read their retained files offline and corrected optional checks handling; no remote replay. |
| W-031 | A restore must reject an archive that contains a data directory but omits the database. | AC-007 | Resolved | Require a real kuma.db before starting the isolated application, so it cannot initialize an empty replacement and appear restored. | Restore checker now requires a real kuma.db before application startup. Five archive regressions passed, including missing database, unsafe entries and budget rejection. Final actual checker passed in restore-final-khncnm5o/restore-cnpz4fqz; no live backup was created. |
| W-032 | The local Ansible renderer could not start its RPC server inside the controller sandbox. | AC-002 | Resolved | Inspect the retained native error and qualify the same local-only producer with the required controller permissions. | native-render-i4vwdt98 exited 250 before tasks; retained. The same producer passed outside the sandbox in native-render-12yn_4bq: actual templates, selected setup facts, byte-limit filters and parser against the real retained APT observation. Both resulting variants passed native Quadlet generation and systemd verification. No workstation configuration change or target deployment. |
| W-033 | The initial YAML serialization used indentation that fails repository policy. | AC-002 | Resolved | Format only the new project YAML with indented sequences, prove parsed values unchanged and rerun the affected checks. | Semantics-preserving sequence indentation applied only to new project YAML. precommit-final-status.json and network-precommit-status.json both exit 0; focused-final-status.json exit 0 covers 13 unit regressions, native syntax, shell policy/format and collision checks. Initial failure remains retained. |

| W-034 | Local-only controller qualification selected no hosts with an implicit localhost and --limit. | AC-002 | Resolved | Qualify the unchanged frozen coordinator without contacting a target. | First invocation exited before tasks. Added an explicit localhost inventory only to the local qualification command; controller-localhost-qualification-status.json exits 0. No bundle input or target changed. |

| W-035 | Move application/file-store ownership to homelab-monitoring-observability. | AC-002, AC-010 | Resolved | One canonical application tree/change record, valid cross-owner links and runnable local checks. | Moved uptime-kuma/ and the existing change record, updated repository README/instructions and cross-links; fleet components remain with owners. Historical immutable bundles/evidence retain their original paths. Qualification recorded below. |
| W-036 | Add fleet host foundation requested November 10. | AC-001, AC-006, AC-011 | Resolved | Owner-governed needrestart/Webmin/msmtp/watchdog installation and effective configuration, combined resource/package qualification and target acceptance. | Requirements are explicit in plan, architecture and operation inputs. Existing application coordinator cannot install these capabilities yet and now rejects execution before target contact while qualification is pending. November 11 owner-governed host foundation accepted: needrestart scan/report and guarded daily schedule, loopback Webmin, preserved Mailrise msmtp configuration and adopted vendor watchdog. Combined scan-time/resource gates passed. |
| W-037 | Resolve actual watchdog backend and per-host adoption. | AC-008, AC-011 | Resolved | Passive device/descriptor-owner/configuration inspection; qualified policy/activation/restoration for this Pi. | Prepared unchanged-policy adoption: PID 1 holds active BCM2835 watchdog0; vendor policy and manager/sysfs report 60/120 seconds with no pretimeout/kexec. No extra daemon or setting change. One disappearing descriptor limits exhaustive snapshot attribution. Native tasks recheck owner/policy after reboot; hardware-expiry recovery remains untested and outside this operation. |
| W-038 | Webmin owner source is a storage diagnostic lifecycle, not a generic fleet installation profile. | AC-005, AC-008, AC-011 | Resolved | Identify owner-reviewed Debian 13 ARM64 package, signing/source inputs, initial configuration, management listener/access and service impact; qualify exact install/rollback. | Prepared pinned Webmin 2.670 and owner SSH-loopback profile with explicit ama PAM/sudo login, disabled localauth, persistent first-start guard, 192 MiB bound and control-group/OOM containment. Native actual-unit producer plus synthetic authenticated dashboard/resource/mail/containment qualification passes (package-network-status.json). No Pi installation or operator-login acceptance yet. |
| W-039 | Fleet msmtp default must be Mailrise. | AC-012 | Resolved | Desired template and effective host default select the Mailrise account; root/cron aliases route correctly and unrelated explicit accounts survive. | Aaron explicitly selected Mailrise November 10. Owner template now uses account default: apprise; root and unmatched local aliases use `notify@mailrise.xyz`. Mailgun remains explicit. Owner docs updated. Current host configuration/precedence and real route acceptance remain unobserved; no mail sent. November 11 retained owner file identities and configured Mailrise default/aliases passed host foundation checks; SMTP greeting/QUIT connectivity passed. No synthetic message was submitted and downstream delivery is not claimed. |
| W-040 | Shared notification ownership and expanded acceptance. | AC-009, AC-012 | Resolved | Reuse fleet Apprise API/Mailrise, verify non-sending connectivity and configured consumer route, leave Kuma monitors/alerts empty. | Existing mailrise.local.theama.co:8025 is desired endpoint; do not duplicate servers on the Pi. Synthetic messages/downstream receipt require exact-content review; local configuration is not delivery proof. Needrestart schedule effects must be explicit in revised live scope. November 11 shared-service consumer configuration and non-sending SMTP check passed; no notification server was installed on the Pi, and Kuma monitors/notifications remain empty. Normal guarded daily needrestart notification schedule is enabled as approved; delivery is not independently demonstrated. |

| W-041 | Select the host and requested foundation components in shared inventory. | AC-010, AC-011 | Resolved | One monitoring host record, explicit pending status, no duplicate notification servers or inferred Munin role. | Server inventory selects j2-svpi3bmf and uptime_kuma/needrestart/webmin/msmtp/watchdog. Application and fleet owners are linked; watchdog backend remains pending qualification. Selection grants no live authority. |

| W-042 | Working-tree secret scan reported a generated index entry. | AC-010 | Resolved | Diagnose the redacted finding without exposing a secret; scan intended source artifacts. | Full working-tree scan found one generic-api-key match in ignored .vexp/manifest.json:16. It is a 64-hex source-file digest keyed by Apache2/docs/munin-ipv6-access-review.md, not a credential. No source suppression or policy change added. Private report retained. |

| W-043 | Capture the selected Pi foundation baseline under the November 10 inspection request. | AC-011, AC-012 | Resolved | Bounded non-mutating metadata/package/controller/configuration capture; no secrets or device opening. | Inspection exited 0, including package/metadata/controller state, active vendor watchdog and non-sending Mailrise greeting/QUIT. Follow-up preserved exact vendor policy bytes and installed dpkg status for offline resolution. All collectors and hashes retained in foundation-prepare-20261110-bcvgim9k; no target mutation or secret-value collection. |

| W-044 | Python APT cache marking included recommended packages unlike native --no-install-recommends simulation. | AC-011 | Resolved | Use the actual native resolver delta and exact package metadata without importing recommendations. | Native simulation exits 0: 28 new packages, zero upgrades/removals; selected-debian-packages.json intersects native Inst/version rows with captured authenticated APT metadata. Do not treat Python marked_upgrade on an uninstalled candidate as a real upgrade. |

| W-045 | Pi vendor needrestart file disables kernel hints; it is not a v8 filename filter. | AC-011 | Resolved | Preserve vendor file; prepare a v8-only list-mode override and prove meaningful kernel reporting without service restarts. | Confirmed vendor file contains kernelhints=0. Exact needrestart 3.11 source shows batch mode still performs kernel checks; the initial disabled-report interpretation was incomplete. Preserve vendor hints unchanged. Owner rpi-v8-list-only profile adds only the actual v8 image filter and list-only mode; actual kernel/reporting acceptance is in the revised native tasks. |

| W-046 | Native AMD64 Webmin startup passed the first-start condition but failed loopback HTTP readiness. | AC-011 | Resolved | Capture actual service/resource/socket diagnostics, fix the demonstrated cause and requalify the same profile. | 96 MiB caused genuine local OOM; preserved diagnostics. Final 192 MiB guard includes KillMode=control-group, OOMPolicy=stop and bounded restart/stop. Native package-unit producer plus explicit login/dashboard passes at about 137 MiB peak with no restart; final probe, stop and permit containment pass. Earlier closed-network failures remain W-052; actual Pi acceptance still pending. |

| W-047 | apt-listchanges may email independently of needrestart during package installation. | AC-009, AC-012 | Resolved | Suppress messages through install-scoped native configuration while preserving global host config/hooks. | Target parser source supports Dir::Etc::apt-listchanges-main/parts. Native-listchanges test loads the actual captured ALCConfig with the scoped profile: frontend none, email_address None, no send. Normal fleet configuration is untouched. |
| W-048 | Isolated APT qualification initially inherited default directory suffixes. | AC-011 | Resolved | Set all local cache/list/config paths explicitly and resolve the exact real snapshot without touching host APT state. | First local update failed before resolution; retained. Corrected native update/simulation succeeds with 29 new packages, no upgrades/removals. |
| W-049 | Native producer qualification loaded deployment-relative paths from a private test directory. | AC-011 | Resolved | Supply explicit local qualification paths and rerun actual assertion/producer; do not alter correct production paths to satisfy the fixture. | Native render context corrected with explicit qualification-only extra-vars; exact 29-package assertion now passes. Actual unit producer needs its absolute script path and socket readiness synchronization; fixture corrections retained. Complete Quadlet dependency graph includes the actual firewall unit and both modes pass native systemd verification. |
| W-050 | Frozen boot inputs must retain the mode required by their preflight. | AC-001, AC-008 | Resolved | New sealed stage preserves mode 0600 for boot payloads and qualifies actual stat/assert expectations. | Replacement archive preserves boot-input mode 0600. Actual stat/assert tasks executed against the frozen stage on explicit localhost and passed both modes/hashes; controller file graph and archive identity pass. Earlier withdrawn archive stays unchanged and unexecuted. |

| W-051 | Webmin can authenticate loopback peer identities without an explicit login when localauth is enabled. | AC-005, AC-011 | Resolved | Require explicit operator authentication in the SSH-only profile and qualify anonymous versus authenticated access. | Owner SSH-loopback profile explicitly disables localauth. Native test uses a transient synthetic password only inside the disposable container: explicit login and authenticated dashboard HTTP 200, both loopback paths and real Type=simple package unit pass. No homelab password or session cookie collected; operator login remains a live acceptance requirement. |

| W-052 | Closed-network Webmin qualification stalls on background package metadata queries. | AC-011 | Resolved | Distinguish a fixture restriction from service failure and retain actual native-unit diagnostics. | At 192 MiB the native unit remained healthy around 143 MiB while the page stalled. With ordinary package-metadata networking, explicit login/dashboard and containment pass. Before startup the fixture redirects its MTA to unreachable loopback port 9, restores owner config only after service stop for --pretend parsing, and sends no real message. |

| W-053 | Native APT local-file acquisition fails with `--no-download`. | AC-001, AC-003, AC-006 | Resolved | Preserve terminal failure, verify residue and qualify an offline correction before defining further live work. | November 10 approved bundle consumed, Ansible exit 2 during actual transferred-file simulation. No package installation reached. Independent inspection confirms unchanged dpkg status, no foundation/application state or listeners, accepted memory controller/ULA retained. Source-isolated target simulation passes; disposable actual-install qualification exposed a second local-file acquisition error with the flag. Corrected local automation disables repository sources and permits local-file acquisition. Exact corrected target simulation matches all 29 pins and unchanged dpkg status. Disposable AMD64 APT 3.0.3 completes actual all-architecture package installation with network disabled and rejects an incomplete dependency closure. ARM64 APT 3.0.4 qualification remains simulation only; no target install acceptance. See private `execution/apt-correction-status.json`; continuation tracked in W-054. |
| W-054 | Continue installation after consumed partial operation. | AC-001 through AC-009 | Resolved | Review observed residue, qualify a continuation that verifies accepted prerequisites without repeating them, then seal exact remaining inputs and obtain scoped authorization. | Continuation reuses existing installation/acceptance with read-only accepted-prerequisite verification and one remaining startup reboot. Qualified, sealed and approved November 10; executed once and consumed. All 29 pins installed and verified, then Webmin HTTP acceptance failed. Terminal outcome archived; unresolved recovery is W-055. Preserve the consumed archive, native receipt and failed local qualification receipts. The earlier pre-install residue was superseded by this continuation: all 29 pinned packages are now installed; Kuma remains absent. DNS/Caddy and operator checks remain pending. |
| W-055 | Webmin loopback HTTP acceptance times out on the Pi. | AC-005, AC-006, AC-008 | Resolved | Preserve the failed receipt, establish service/package/network residue, determine cause and qualify bounded recovery before further live changes. | Approved continuation installed and independently verified all 29 pins, configured Mailrise/Webmin, then both 30-second login-page checks timed out. Rescue stopped/disabled Webmin, removed permit and verified no listener. No image import, Kuma start, reboot, account check, backup/restore, backend promotion or schedule reached. Native log and independent residue/diagnosis retained. No OOM/proxy/hostname-resolution problem found. Exact-URI native AMD64 reproduction passed (IPv4 3.6 s, IPv6 9.7 s and authenticated dashboard); this does not establish Pi cause or capacity. No verified fix or new live authority. | November 10 bounded Pi diagnostic confirms memory-high events/reclaim waits during HTTP stalls: peak 155.17 MiB below 192 MiB hard cap, 9,902 high events, no OOM kill; IPv4 login 43.31 s, IPv6 75.077 s timeout. Memory throttling is a supported contributor; sole cause/fix not proven. See diagnostic terminal outcome below. The approved correction set collect_pkgs=0 and passed actual Pi loopback HTTP/cgroup acceptance under unchanged caps: peak 79.84 MiB, zero high/OOM events and zero restarts. Later bootstrap failure intentionally stopped Webmin again. This resolves initial HTTP recovery; post-reboot/private login remains W-011/AC-011.
| W-056 | Prepare a bounded Webmin diagnostic with Pi-side timing/resource evidence and verified containment. | AC-005, AC-006, AC-008 | Resolved | Exercise actual collector/Ansible lifecycle and disconnect fallback locally, qualify read-only target baseline, then seal exact inputs and obtain authorization before one live diagnostic. | Owner-native Ansible and a read-only stdlib collector prepared. Existing settings/192 MiB cap retained; requests are unauthenticated loopback only. PID1 fallback arms before start and normal cleanup verifies stopped/disabled/no listeners/no permit before cancelling it. Aaron approved the exact diagnostic November 10; executed once with Ansible exit 0, complete Pi evidence and independently verified containment. Diagnostic preparation/execution accepted; service recovery remains W-055. |

| W-057 | Correct Webmin startup pressure and qualify the remaining installation against accepted package residue. | AC-001, AC-005, AC-006, AC-008, AC-011 | Resolved | Verify supported package-query controls, exercise actual native Webmin and simultaneous Kuma/scan budget locally, preserve existing limits, then seal one new continuation with residue preflight and bounded failure containment. | Pinned package confirms supported collect_pkgs=0. Cold and combined native AMD64 tests pass under unchanged caps; 51 Webmin tests, 13 Kuma regressions, native guard/release/containment/fallback and frozen controller checks pass. One 117-input continuation sealed below. No new live target contact, mutation or authority. W-055 retains actual Pi acceptance. |

| W-058 | Native startup fallback cancellation can return rc 5 after an inactive transient service is collected. | AC-005, AC-008 | Resolved | Independently verify timer/service inactivity and accepted Webmin state after cancellation; qualify the actual release path before sealing. | Local native fixture passed configuration and both HTTP/resource checks, then cancellation returned service-not-loaded after stopping the timer. No Pi access or mutation. Preserve that failed qualification receipt. | Corrected release accepts command status only after independently proving timer/service inactive and Webmin active with a positive PID. Actual native guard/configure/accept/release completed 27 tasks, exit 0; failed receipt preserved.

| W-059 | Kuma first runtime observation exhausts retries with a loopback TCP connection timeout. | AC-002, AC-005, AC-006, AC-008 | Resolved | Preserve the exact failure and independent residue; qualify a bounded per-family/container-versus-published-path diagnosis before any further service start. | November 10 correction continuation consumed, exit 2. Image and native unit startup succeeded, observer timed out connecting before complete JSON. The emitted traceback does not identify which address family failed. Native rescue stopped services; independent inspection confirms no live containers or port 3001/10000 listeners, Webmin disabled/permit absent and application/network inactive. Kuma peak 214.4 MiB, zero recorded restarts; cause unconfirmed. Data, image, generated definitions and enabled guard remain. No reboot or private operator pause reached.  November 10 approved network diagnostic now isolates a reproducible published IPv6 loopback timeout: after startup both internal/direct families and published IPv4 return 302. Original failure family remains unavailable; correction and final service acceptance remain open in W-063.  Approved correction now passes all six Pi HTTP paths after startup, including published IPv6; complete diagnostic/corrective receipts and four-unit containment are archived. The original lost family detail and kernel mechanism are not reconstructed. Remaining full deployment acceptance is W-011/W-063. |

| W-060 | Prepare a per-family Kuma network diagnostic with evidence retained before shutdown and future-boot containment. | AC-002, AC-005, AC-006, AC-008 | Resolved | Qualify actual collector and native guard/timer/start/stop lifecycle locally, cover partial HTTP failure and controller loss, then seal exact inputs for one proposed live operation. | Qualified and sealed November 10; exact candidate and command below. Full frozen native lifecycle passed (43 tasks, zero failures), 20 focused regressions passed, wrong-source preflight refused before mutation, active-service fallback and future-start guards proved locally. Repository/local preparation only. Compare container loopbacks, host-to-container addresses and published host loopbacks separately; preserve ports/NAT/routes/resources and allowlisted startup-log events. Proposed persistent ConditionPathExists guard uses an ephemeral /run permit so generated units cannot start unattended after containment or reboot. No live target contact authorized for this preparation.  Aaron approved the exact sealed candidate; native Pi execution passed with complete per-family evidence and independently verified containment. Approval consumed; terminal outcome below. |

| W-061 | Offline systemd verification does not resolve the Quadlet-generated units by basename. | AC-002, AC-008 | Resolved | Verify the observed generated fragment paths natively and rerun the real lifecycle without weakening parser or containment checks. | First disposable lifecycle stopped before permit/start at systemd-analyze verify by name. Always cleanup passed and preserved guards, restored runtime overrides and checked the empty stopped database. No live target contacted.  Corrected verification selects actual /run/systemd/generator fragment paths and validates typed a(sbbsi) PID1 Conditions through D-Bus. Final frozen native lifecycle passed. |

| W-062 | Permit ownership comparison differed from the copied content in native qualification. | AC-008 | Resolved | Use one literal permit-content variable for creation and ownership hashing, then pass actual removal/containment and disconnect fallback tests. | Local collector retained all 12 measurements, including IPv6 published-loopback timeouts with other paths healthy. Cleanup refused to claim containment while the permit remained; fallback was left armed. No production contact. Failed receipt preserved. A subsequent native run also caught content-variable/register aliasing; policy content now has a distinct name and a neutral collision regression.  Final frozen lifecycle passed matching-permit removal, independent stop/listener/container/guard checks, fallback cancellation, original timing restoration and empty database integrity. Active-service fallback and restart-with-cleared-/run proofs also passed. |

| W-063 | Correct the observed host-published IPv6 loopback path without weakening access policy. | AC-002, AC-004, AC-006, AC-008 | Resolved | Qualify an owner-governed correction against the observed IPv6 DNAT/hairpin evidence, retain limits/guards and obtain new exact-bundle authority before live work; then pass both loopback families and remaining service acceptance. | Actual Pi diagnostic returns 302 internally and host-to-container over both families, and published IPv4, while published IPv6 times out in both rounds. A corresponding IPv6 loopback-source mark/masquerade rule is absent from retained NAT evidence; this is a supported hypothesis, not packet-trace proof or an authorized firewall fix. No new continuation is defined or approved.  Preparation complete: native systemd IPv6-only loopback socket/proxy replaces only the ineffective Podman ::1 publication; application/container IPv6 and ingress policy remain. The exact frozen corrective lifecycle, all 12 HTTP probes, both WebSocket upgrades/ping-pong, preflight refusal, four-unit fallback and restart guards passed locally. Candidate sealed below; actual Pi corrective acceptance remains pending.  Aaron approved and executed this corrective bundle once; actual ARM64 acceptance passed all six paths after startup, effective proxy limits and four-unit containment. Source correction accepted; the broader remaining-service-acceptance closure is still pending under W-011, so this row remains In progress until that criterion is satisfied. No new live authority. November 11 corrected IPv6 loopback path and both remaining-service runtime checkpoints passed with unchanged guards/caps; service foundation accepted. Final DNS/Caddy HTTPS is separately tracked by W-007. |

| W-064 | Offline verification of new proxy units must include their Quadlet-generated dependencies. | AC-002, AC-008 | Resolved | Pass systemd-analyze verify with all four explicit fragment paths and rerun the actual local corrective lifecycle. | First local correction run refused before permit/start: systemd-analyze did not search the generated Kuma dependency for standalone proxy verification. Native cleanup proved all units stopped/guarded and no listeners/containers. Failed candidate and receipt retained; no production contact.  Corrected verification includes generated app/network and proxy socket/service fragments together. Final frozen lifecycle passed 55 native tasks with zero failures; failed predecessor qualification remains preserved. |

| W-065 | Prepare the remaining deployment from accepted corrected sources without replaying installation. | AC-001, AC-003, AC-005 through AC-012 | Resolved | Qualify and seal one continuation with strict 720 MiB admission, installed-state preflight, bounded startup/reboot/operator setup, backup/restore, backend checks and owner schedule activation. | Preparation only; consumed bundles remain untouched. No live target contact or new authority. Private preparation: `/home/aaron/code/.local-evidence/uptime-kuma/remaining-deployment-20261110-dqpr9b40`. The last 711.12 MiB observation fails the combined gate; fresh admission must pass without changing limits or claiming capacity from the isolated trial. |
| W-066 | Ephemeral diagnostic permits cannot support the remaining reboot, and the original coordinator lacks whole-operation disconnect containment. | AC-006, AC-008 | Resolved | Preserve all four guard files; qualify a deadline-bound boot permit and persistent native containment across controller loss/reboot, then retain normal startup only after all continuation acceptance passes. | Prepare one native systemd startup dependency and persistent deadline timer. Pending/expired/contained states must fail closed; operator readiness must be bounded and credentials remain outside evidence. No production change. |

| W-067 | Remaining-operation budget and containment must include temporary restore/ingress containers. | AC-006 through AC-008 | Resolved | Verify stage budgets and cleanup of only owned temporary containers on controller loss. | The 320 MiB restore replaces the stopped source; the 64 MiB ingress client runs before the 96 MiB daily scan is enabled. Neither adds to the 720 MiB simultaneous maximum. The bounded fallback must also stop/remove matching restore and ingress containers without deleting data or backups. |

| W-068 | First combined fixture check reports Kuma memory-high events. | AC-006 | Resolved | Retain the failed check, distinguish first database initialization from the already-installed target baseline, and qualify the combined running services without raising limits or hiding pressure counters. | Disposable AMD64 startup succeeded, but the strict combined check failed with Kuma peak 270,725,120 bytes and 1,883 high events; max/OOM/OOM-kill remained zero. Webmin peak 105,005,056 bytes, proxy 3,010,560 bytes, no pressure events. No Pi observation or capacity claim follows. The failed qualification remains retained; final settled checks and native acceptance passed without relaxing limits. Existing-data restart also recorded startup high events (4,407), with no increase across the 34-second combined sample and no max/OOM events. Zero lifetime high events was an unnecessarily strict new check: MemoryHigh is the existing throttle threshold, not the hard limit. Retain cumulative high counts, require zero max/OOM/OOM-kill and no new pressure events during settled acceptance, plus HTTP health and host reserve. This preserves existing limits and AC-006; it does not erase either failed qualification. |
| W-069 | Approved remaining deployment fails the actual 720 MiB admission gate. | AC-001, AC-006, AC-008 | Resolved | Reconcile the measured capacity mismatch and retain numeric admission evidence before qualifying a new continuation; preserve the existing limits and consumed attempt. | One approved attempt exited 2 at `kuma_available_memory.stdout | int >= 737280`; target recap: five successful read-only tasks, zero changes, one failure. Default output does not retain the exact numeric reading. No service startup, reboot, proxy contact or mutable block was reached. Do not substitute the older 711.12 MiB reading for this attempt or replay it. Private terminal evidence is retained under the remaining-deployment execution directory. Follow-up approved read-only snapshots measured 745848, 745040 and 745040 KiB available, all above the floor but with only 7760 KiB minimum margin. The SSH/Python workload differs from the failed Ansible gate; observer overhead or other transient activity remains an unconfirmed explanation. Retain the floor and reconcile sampling plus W-070 before a replacement.  November 10 paired measurement now confirms raw 714.50–717.43 MiB and Ansible 705.88–708.66 MiB: all below 720 MiB. Paired differences span 5.84–11.55 MiB, including concurrent activity; observer difference is real in these pairs but cannot alone explain the earlier failure or be added back. Admission remains unresolved; no floor adjustment.  Later attribution measured 725.95–727.14 MiB available under a different collector, with only 5.95 MiB minimum margin. File/slab dominate large slice charges; no verified reclaimable gain or admission acceptance follows.  Aaron explicitly approved staged admission for new definitions. The 624 MiB startup gate and separately guarded scans are locally qualified; this resolves the policy mismatch, not actual Pi acceptance or the missing historical reading. W-011 and W-070 retain live criteria. |
| W-070 | Combined acceptance does not sample host reserve during the needrestart scan. | AC-006, AC-011 | Resolved | Observe host and relevant cgroup headroom/pressure during the bounded scan, and retain failures before deciding combined Pi acceptance. | The foundation task checks MemAvailable before the scan; accept-combined samples after it. Their success cannot prove a continuous 96 MiB reserve through the transient peak. The AMD64 fixture's reported MemAvailable belongs to its host, not proof of the 720 MiB parent cgroup's unused allowance. Preserve fixture results with this limitation; do not use them to lower Pi admission.  Approved stopped-workload scan passed with a 41.39 MiB native peak and 686.34 MiB minimum sampled host availability. This closes scan-only observation, not combined running-services reserve; integrate the owner observer into later combined acceptance.  Owner guard now instruments every foundation acceptance call and the scheduled producer. Local real-scan, notification-substitute and failure tests pass. Actual combined Pi scan-time reserve remains unaccepted until a separately authorized continuation. November 11 both running-service scan observations passed, with sampled host minima 554968 and 566808 KiB, maximum gaps below 0.257 s, no new pressure/OOM events, retained native scan peaks and verified transient cleanup. Actual daily guarded schedule enabled after acceptance. Discrete samples do not exclude between-sample dips; no synthetic producer notification test was performed. |
| W-071 | A failed platform resource assertion omitted its registered numeric reading. | AC-001, AC-008 | Resolved | Retain exact readings before the assertion, including rejection, without changing the threshold. | Working preflight writes controller-private mode-0600 admission-resources.json and includes readings/thresholds in its failure message. Local native Ansible fixtures passed for 737279, 737280, 737281 KiB and malformed input. No historical reading was reconstructed; consumed bundles are unchanged. Sandbox RPC startup failed before task execution on the first local test; the outside-sandbox localhost run passed. |
| W-072 | Inspect stopped-host capacity under the separately approved read-only scope. | AC-001, AC-006, AC-008 | Resolved | Retain three timed snapshots, exact readings and read limitations without service changes. | One authenticated SSH inspection completed in 20.16 seconds on the same boot/kernel. Memory available 727.58–728.37 MiB; selected reclaim/swap/OOM and all 13 sampled cgroup event counters had zero deltas. The PSI memory file was absent in every sample; this is unavailable telemetry, not zero pressure. Four Kuma units inactive; Webmin failed, a state already allowed by the owner stopped-foundation preflight. MainPID/listeners/guards were outside this inspection. Initial transport failed before authentication because the working known_hosts file was absent; manifest-verified existing hashed host keys resolved transport without enrollment or weaker checking. |
| W-073 | Measure observer differences and scan-time reserve without replaying deployment. | AC-001, AC-006, AC-008, AC-011 | Resolved | Retain paired readings, scan-time headroom and verified cleanup; reconcile W-069/W-070 without claiming combined acceptance. | Exact approved measurement completed once on November 10, exit 0. Three pairs, 17 samples including 15 while scanner PID was live, exact native scan peak, successful kernel report, unchanged application states and owned cleanup retained under capacity-measurement-hbvxmkz9/execution. W-069 admission and W-070 combined reserve remain open work. |
| W-074 | Reconcile admission using measured observer differences and baseline variability. | AC-001, AC-006 | Resolved | Keep the floor and raw numeric evidence; explain why changing observers cannot qualify the latest baseline; define prerequisites for a continuation. | Local source/evidence review retained the 737280 KiB Ansible-path gate. Raw readings also fail; no correction factor or retry policy adopted. Architecture now distinguishes admission from combined scan acceptance and explicitly accounts for the separate observer. W-069 capacity remedy and W-070 integration remain pending; no candidate sealed. |
| W-075 | Attribute stopped-host memory without replaying deployment or changing capacity policy. | AC-001, AC-006, AC-008 | Resolved | Execute the approved bounded inspection and retain hierarchy-aware attribution and gaps before proposing a remedy. | Exact approved bundle ran once, exit 0, three samples, unchanged stopped application state. No enumeration truncation; PSI and some root/udev-child memory interfaces absent. Full evidence retained under host-memory-attribution-ydppox2d/execution. No sufficient safe capacity remedy established; W-069 remains unresolved. |
| W-076 | Radio-related daemons have resident processes despite the radio-disabled host requirement. | AC-001, AC-008 | Resolved | Review fleet ownership/dependencies locally before proposing any service change; preserve Ethernet/NetworkManager and do not infer radio state from daemon presence. | Attribution observed wpa_supplicant and bluetooth service cgroups/processes. Combined current charge about 7.03 MiB, anonymous charge about 1.51 MiB; neither total is guaranteed recoverable or sufficient for the prior admission deficit. Inspection did not re-read rfkill or dependency policy. No stop/disable action authorized.  Local owner review found no target-specific radio-service disable profile in the searched fleet/network sources. Nautobot Bluetooth masking belongs to a different host and grants no authority here; no wpa_supplicant removal rule was found. Dependencies remain unverified; no action proposed. November 12 W-125: exact runtime receipts show wlan and bluetooth soft-blocked before/after the accepted reboot and at backend promotion. This corrects the earlier incomplete evidence summary, but does not prove hardware disablement or resolve service dependencies. Preserve the existing daemons; host/network owner must finish dependency/ownership review or explicitly accept a no-change disposition. No service change or capacity credit proposed. November 12: Aaron approved retaining existing radio daemons and accepting observed softblocks across reboot/promotion. No dependency-completeness, hardware-disablement or memory-recovery claim. Host/network owner must review dependencies before any future removal proposal; unexpected unblocking reopens this finding. |
| W-077 | Review capacity options while preserving the floor, caps and reserve. | AC-001, AC-006, AC-011 | Resolved | Assess retained footprint and owner policies; state a supported path or the unresolved decision without pretending admission passed. | No sufficient supported footprint remedy identified. Radio service charges do not establish needed recovery; required foundation services and caps remain. Aaron confirmed no alternative host is available. Deployment is on hold pending an explicitly reviewed capacity/design decision; no continuation or new inspection prepared. |
| W-078 | Review and implement staged admission for the only available host. | AC-001, AC-006, AC-011 | Resolved | Explicit policy agreement and locally qualified owner implementation; live acceptance remains separately governed. | Aaron approved 624/224/192/96 MiB with unchanged caps and sampling tradeoff. Shared guard, all three acceptance checkpoints, scheduled producer, restore/ingress fresh gates and failure receipts implemented. 41 tests, five syntax playbooks and native isolated success/failure qualification passed. No continuation sealed or Pi execution performed. |

| W-079 | Prepare the remaining deployment under approved staged admission. | AC-001, AC-006, AC-008, AC-011, AC-012 | Resolved | Freeze the current owner guard and complete import graph, qualify the exact candidate locally, preserve consumed bundles and present exact live scope. | Preparation approved by Aaron; 120-input candidate sealed below. Frozen 41 tests/five syntax checks, controller-only integrity, archive byte/mode equality and bundle secret scan passed. Fresh evidence/backup destinations and unexpected-helper preflight are included. No target contact or live authority; actual acceptance remains W-070/W-011. |

| W-080 | Private login succeeded according to the operator, but the required acknowledgement file did not arrive within the bounded wait. | AC-005, AC-007, AC-011 | Resolved | Preserve contained administrator data and accepted reboot/scan receipts; qualify a continuation and workable operator handoff before new exact-bundle authority. November 10 attempt exited 2 after 903-second file wait. Aaron reported Kuma account creation and successful Webmin login after workstation tunnel clarification. Independent administrator acceptance was not reached. Sealed rescue verified stopped/guarded services, no application listeners/containers and absent daily schedule. No replay; backup/restore, promotion and final acceptance remain pending. | November 10 completion verified the protected late acknowledgement and independently accepted active administrator/authentication with empty workload; no repeated setup, timed wait or reboot. |

| W-081 | Prepare completion from contained administrator-bearing data without replaying bootstrap or reboot. | AC-005, AC-006, AC-007, AC-008, AC-011 | Resolved | Bind retained controls and reboot evidence, reconcile the late acknowledgement, qualify safe one-time renewal and remaining acceptance, then seal for review. | Local preparation completed; exact seal below. 43 tests, five syntax checks, native helper/control lifecycle, actual predecessor template rendering, frozen controller integrity and bundle secret scan passed. No live contact. Protected acknowledgement and actual administrator data remain fresh live gates. |

| W-082 | Both approved proxy nodes returned HTTP 302 on both families against the backend gate's 200 requirement. | AC-004, AC-008, AC-011 | Resolved | Qualify the actual administrator-bearing response/redirect contract and bounded source-preserving probe locally before any new live attempt. | Four retained responses confirm reachability; the gate refused them. Redirect destination/body were not collected, so expected application redirect is not yet established. See private proxy-probes.json and terminal outcome below. November 11: pinned AMD64 claimed fixture proves root 302 to /dashboard and direct dashboard 200 on both families. Working probe requests only /dashboard, requires 200 and validates family/path/source/backend. Local positive, redirect, server-error and identity-rejection checks pass; actual proxy acceptance remains pending. November 11 both approved proxy nodes returned dashboard HTTP 200 over IPv4 and IPv6 with expected backend and admitted source identities. Actual response rows retained in execution/proxy-probes.json; no redirect broadening or final HTTPS claim. |
| W-083 | Loopback recovery restart hit the native service start-rate limit. | AC-006, AC-008 | Resolved | Reconcile the complete startup/backup/promotion/recovery sequence against native rate limits and qualify bounded recovery without weakening guards or replaying a consumed operation. | The loopback-only definition was restored, but restart failed with attempted-too-often. Outer rescue independently verified stopped units, no listeners/containers, guards intact and no schedule. No reset-failed or retry was performed. November 11: native enabled-unit fixture reproduces fourth-start rejection at unchanged 3/300-second limits. Remaining-deployment rescue now restores/reloads loopback definitions and fails into existing verified outer containment without another start. Local routing/native tests pass; live successor acceptance remains pending. November 11 successor completed its three planned starts without rate-limit failure. Stop-only promotion recovery was locally qualified and remains the failure path; it was not invoked during this successful attempt. Native rate limits unchanged, no reset-failed or retry. |
| W-084 | The consumed administrator-completion renewal already archived its predecessor; its one-time resume cannot be reused. | AC-006, AC-008, AC-010 | Resolved | Before sealing a successor, qualify explicit preservation of both existing state records and renewal from the exact retained contained state, without replay, reboot or account setup. | November 11: successor mode preserves previous-state.json, exclusively archives the failed completion, binds both hashes and refuses consumed state/replay. Native local lifecycle and final frozen qualification passed; exact successor sealed below, not authorized. Live acceptance remains with W-082/W-083 and the outstanding deployment gates. |
| W-085 | Proposed Caddy active health still requested root with status 200 after the backend became administrator-bearing. | AC-004 | Resolved | Use the accepted direct dashboard response and qualify both node configurations. | November 11 proposal now requests /dashboard with exact 200. Network-disabled Caddy 2.11.4 adaptation and independent JSON assertions passed for both node environments. Production configuration remains unchanged. |
| W-086 | Retained Caddy inspection lacks public certificate coverage/validity and effective health-monitor timing for onboarding. | AC-004, AC-008 | Resolved | Authorize and review the bounded read-only readiness collection below; establish certificate name/validity/leaf identity and observation intervals before sealing activation. | Prior release hash verification alone does not prove certificate coverage or timing. At preparation, the collector and scope were locally qualified and sealed without target contact. No certificate replacement or private-key collection is proposed. November 11 approved inspection completed once, both nodes exit 0: wildcard certificate covers uptime, leaf/fullchain fingerprints match across both nodes, validity includes inspection time, accepted release identity matches, and effective timer properties were captured. See terminal outcome below; client TLS/application acceptance remains W-007/W-087. |
| W-087 | Current Caddy neutral deployment entrypoints have no application-onboarding scope. | AC-004, AC-008 | Resolved | Extend the owner implementation in place, causally qualify publication/activation/recovery, and register one authorization-ready successor after readiness is resolved. | Owner implementation now extends the neutral runner/transaction in place. One defined-unexecuted application successor passes the authorization-ready policy, with 18 release and six native application cases independently verified. No live Caddy acceptance is claimed; that remains W-007. |
| W-088 | Application acceptance integration is not yet covered by the closed qualification graph. | AC-004, AC-008 | Resolved | Hash-bind private operator inputs; qualify the actual application outer path, receipt rejection, observer failures and recovery before sealing. | Operator helper/client are hash-bound; four receipt boundary tests pass. Six actual application-outer cases cover success, operator rejection, HTTP failure, native journal failure, failed native cycle and corrupted readback, including reverse recovery. Independent current-graph verification and owner authorization-ready policy pass. Native application services/receipts are real; transport/node views and helper container invocation remain controlled substitutes. |
| W-089 | Observer duration could pass before the last HTTP sample reached the 65-second boundary. | AC-004 | Resolved | Sample both families again after the elapsed-time/cycle gate and pass independent outer readback. | Final HTTP samples follow the elapsed-time/cycle gate. Independent successful outer readback verifies at least 65 seconds between first and last sample for each family on both nodes. Earlier rejection and reverse recovery remain retained in application-qualification-orcoiqqu. |
| W-090 | Native health-journal failure scenario produced a real Caddy error but did not reject acceptance. | AC-004, AC-008 | Resolved | Bind native journal cursors to the requested node/cursor and prove the real failure reaches the transaction rejection and reverse recovery. | Retained native comparison proved both numbered journal queries missed a matching post-cursor entry. The observer now uses --no-tail with a separate 100-line cap, preserving query/truncation rejection. The actual Caddy health failure is retained, rejects the transaction, and completes reverse recovery in application-final-uu0r37uy; independent verification passes. Earlier cursor and +N hypotheses remain recorded below. |
| W-091 | Standby Caddy preflight stopped without recording the failed installed-file identity. | AC-004, AC-008 | Resolved | Use retained evidence to identify the failure, or prepare a bounded non-secret metadata/hash inspection under new authority; qualify any correction before a successor. | Retained sealed manifests prove reconciler_sha256 incorrectly used repository-source f840892f… instead of accepted installed e777c2fe…. Git revision d131b9da63ad supplies exact accepted bytes. Seven checks with the frozen hash predicate reproduce rejection by the sealed pin, acceptance by the owner pin, and rejection of changed/missing/symlinked inputs. The fixture masked this by installing repository bytes and deriving the expectation from them. Exact live failed-file identity was not logged; no fresh host state or sole live cause is asserted. Correction and observability are W-092/W-093. |
| W-092 | Baseline qualification conflates repository source and accepted installed reconciler identities. | AC-004, AC-008 | Resolved | Prepare an owner-governed correction using accepted-live pins, preserve the installed reconciler, and qualify with independently pinned accepted bytes plus a source/installed mismatch case before a successor. | Local correction uses reconciler_installed_sha256 from the accepted owner registry and independently verified external accepted bytes. All 22 release scenarios pass, including repository-byte mismatch rejection; native application success passes. Integrated locally after verified terminal archival (W-094). Current-source host checks and 22 container scenarios pass with independent verification. The archived consumed inputs and production remain unchanged. |
| W-093 | Preflight file checks return failure without identifying the file or observed identity. | AC-004, AC-008 | Resolved | Qualify bounded non-secret failure evidence for expected/actual hash and file type, including missing/symlink cases, before another execution candidate. | Local correction emits one bounded failed-file metadata line on captured stderr. Eleven predicate cases and four full outer-path file-drift cases pass; independent verification checks exact diagnostics, standby rejection before primary preflight, zero publication/reload, and staging disposition. Six launcher argument cases pass. Integrated locally under W-094 and requalified through the current-source container wrapper; no claim is made about the unlogged original live assertion. |
| W-094 | Consumed Caddy operation must be archived before applying the locally qualified correction or defining a successor. | AC-004, AC-008 | Resolved | Publish the exact terminal-result commit and annotated tag, verify remote archive identity, then integrate the correction in place and qualify current neutral bindings before a successor. | Approved 17-file terminal tree committed as 8999dde79a4bc3ad202876ee98a7a4bbe89221ce and atomically pushed with annotated tag caddy-uptime-kuma-onboarding-terminal-2026-11-11. Remote main, tag object and peeled commit verified. All commit hooks pass with a temporary exact-label exception for the independently verified nonsecret outer digest; a synthetic credential still rejects. Archive gate is satisfied. The qualified correction is applied, consumed recipe/result removed, operation reset inactive and neutral hashes rebound. Host profiles and all 22 current-source container cases pass with independent verification; authorization-ready correctly rejects. Stream is locally clean, with no successor or live authority. Changes remain uncommitted. |
| W-095 | Prepare one current Caddy application candidate after terminal cleanup. | AC-004, AC-008 | Resolved | Bind accepted installed identities, qualify all release and native application cases, independently verify the exact graph, then seal for review. | Candidate 20261111-uptime-kuma-application-onboarding was sealed and approved once; its attempt is now failed-consumed. All 22 release cases, six native application cases and four handoff tests pass; independent evidence verification and authorization-readiness pass. Standby preflight passed; primary preflight rejected before publication. Both staging dispositions passed. W-096 owns diagnosis; no production acceptance. |
| W-096 | Primary Caddy preflight rejected after incoming namespace checks without identifying the exact remaining assertion. | AC-004, AC-008 | Deferred | Caddy owner: retire the legacy onboarding predicate through W-098; do not spend more effort diagnosing this consumed attempt unless a retained safety requirement makes the evidence necessary. | Aaron directed that investigation stop in favor of streamlined onboarding. Exact cause remains unconfirmed; original failure, cleanup and terminal archive requirements remain recorded. This does not waive drift or release-integrity checks in the replacement design and does not establish live acceptance. |
| W-097 | Separate routine proxy-target onboarding from platform/certificate-repair orchestration and record primary-first activation. | AC-004, AC-008 | Resolved | Reconcile architecture, onboarding procedure, entry-point documentation and change plan with Aaron's approved ordering and retained checks. | Approved design: verify Node A before exposing the same candidate to replication; independently verify Node B and report partial outcomes. Documentation routes routine onboarding to its own guide. Installed behavior is explicitly distinguished from the approved, not-yet-implemented design. |
| W-098 | Implement and qualify the streamlined primary-first onboarding path in existing release machinery. | AC-004, AC-008 | Resolved | Preserve/archive consumed inputs; separate candidate preparation/local activation from outbound exposure; retain one revision/parent/manifest; qualify primary failure with no propagation, success, secondary drift/rejection and bounded recovery before a new exact live review. | Integrated both retained patches after the published archive; clean stream, inactive operation and exact neutral/source bindings are reconciled. Nine final primary-first cases, 20 platform certificate cases, synchronization and owner policy profiles pass. Accepted installed identities remain unchanged. Exact local candidate/evidence is retained below; W-100 separately tracks authorization coverage required before successor sealing. |
| W-099 | Integrated platform regression still invokes retired standby-first application cases. | AC-004, AC-008 | Resolved | Keep certificate repair coverage scoped to platform behavior; replace obsolete application assertions with the primary-first fixture and rerun both against the final source. | Removed two obsolete application cases and their unreachable assertions from the platform suite while preserving shared fixture helpers. Final platform suite passes all 20 cases; the current primary-first suite passes all nine against the same shared helper. The onboarding guide names its separate native launcher. |
| W-100 | Successor authorization coverage still selects the retired certificate-derived application scenarios. | AC-004, AC-008 | Resolved | Before defining or sealing a primary-first successor, update the application-specific coverage/evidence validation to the qualified primary-first stages and prove fail-closed checks against exact retained evidence. Preserve certificate-repair requirements separately. | Application scope now uses the primary-first definition/evidence verifier and its own coverage contract. Certificate-repair requirements remain separate. Nine exact-source runtime scenarios and nine evidence-tampering controls pass through the actual authorization policy; missing, stale, forged or symlinked evidence rejects. Qualification preceded successor binding and was repeated against the final bound graph. |
| W-101 | Prepare the primary-first successor from the qualified local implementation. | AC-004, AC-008 | Resolved | Bind current inputs after W-100 qualification, pass exact-candidate runtime and authorization checks, then seal one reviewable unexecuted bundle with explicit recovery and deferred work. | One primary-first successor is defined, qualified and sealed for review. Exact source/plan snapshot, archive, review, command and qualification index are retained privately and bound below. Authorization-readiness passes; no live approval, execution, commit or push occurred. |
| W-102 | Reconcile accepted Caddy production inventories and prepare terminal archive. | AC-004, AC-008, AC-010 | Resolved | Match both node manifest readbacks, preserve consumed inputs and installed-tool identities, validate inventories, and prepare an exact local archive review without publication. | Both node payload hashes and exact fragment reconciled; installed-tool identities and consumed inputs preserved. A 35-file terminal archive, patch, candidate tree and publication review are prepared locally below. Publication is not authorized. |
| W-103 | Release-source policy hardcodes exactly five files and rejects the accepted added route. | AC-004, AC-010 | Resolved | Replace fixed count with complete source/registry equality; retain hash/payload checks and reject omitted or unregistered sources. | Fixed count replaced with complete source/registry equality. Accepted six-file inventory and focused host profile pass; missing and unregistered source regressions reject. No live implementation or executed input changed. |
| W-104 | Reconcile the published primary-first operation to neutral state. | AC-004, AC-008 | Resolved | Verify the published archive, preserve accepted configuration, remove consumed operation data and reconcile all neutral bindings under owner checks. | Archive commit/tag receipt verified locally; operation inactive, recipe/coverage empty, terminal data archived, stream clean, accepted identities preserved and focused owner checks pass. Changes are uncommitted. |
| W-105 | Prepare independent private application acceptance after the accepted route. | AC-004, AC-008 | Resolved | Qualify and seal standalone login/WebSocket receipt plus bounded passive HTTP/journal/completed-cycle observation before requesting live authority. | Eight private-helper tests and five observer/integration tests pass. The final observer passes native offline systemd/Caddy HTTPS qualification and independent receipt verification. One frozen scope is sealed below; no live check occurred. W-106 owns execution. |
| W-106 | Execute separately authorized private and passive application acceptance. | AC-004, AC-008 | Resolved | After exact approval, require a valid private login/WebSocket receipt and both nodes' complete bounded HTTP/journal/service-cycle evidence for the accepted release; retain failures and keep DNS pending. | Aaron approved the exact sealed scope November 11. One operator attempt failed at client-result; failed receipt retained. Passive observation did not start. Approval consumed; W-107 must be addressed before a separately reviewed attempt. No human deadline, service mutation, backend SSH, DNS execution or automatic rollback is included.  November 11: corrected observation-only continuation passed both nodes and independent combined verification using the accepted private receipt. HTTP spans 85.64/130.81 seconds, at least two completed cycles per monitored unit, unchanged release identities and zero journal adverse events. Earlier failures remain recorded; DNS pending. |

| W-107 | Private helper loses diagnostic evidence on client failure. | AC-004, AC-008 | Resolved | Locally qualify credential-safe structured failure reporting, including client exit status and bounded allowlisted stage/code; retain the failed attempt without inventing a root cause. | The frozen wrapper discards stderr and records only client-result for nonzero client exit or oversized stdout. The failed receipt cannot distinguish container/client execution, transport/TLS, authentication or assertion failure. No evidence establishes incorrect credentials or a broken proxy. Observation was gated off. Local correction now retains enum-only client stage/family/code, exit status and cleanup outcome; 13 wrapper tests, seven JavaScript failure scenarios plus success, and five observer tests pass. Original cause remains unknown; this resolves reporting only. |

| W-108 | Prepare successor application acceptance with corrected private failure reporting. | AC-004, AC-008 | Resolved | Freeze new helper/client identities and receipt paths, qualify the exact source and preserve the consumed predecessor before live review. | New scope sealed in proxy-acceptance-review-82p7lr6b; 13 helper tests, seven client failure scenarios plus success, five observer tests, syntax and exact-snapshot secret scan pass. Observer and owner identities are unchanged; prior native observer qualification is retained. No live approval or execution. |

| W-109 | Pinned private client cannot read owner-private sealed script. | AC-004, AC-008 | Resolved | Preserve private file modes; qualify actual container UID/mount access and pre-credential startup in the pinned image before preparing another attempt. | Successor failed with exit 1, unavailable client report and successful cleanup. Two offline local probes show dependency import passes, but sealed source read fails EACCES at container UID 1000. Existing mocked tests and host syntax checks missed this boundary. No credentials or network used; no later application behavior is established. Corrected rootless keep-id/explicit UID:GID mapping and pre-credential offline startup check pass actual pinned-container qualification. Four cases cover original EACCES, corrected startup, actual client reaching an expected network-disabled error, and syntax rejection. Private modes/ownership preserved; cleanup passes. |

| W-110 | Prepare application acceptance after actual-container source-access qualification. | AC-004, AC-008 | Resolved | Freeze corrected helper and new receipt identity, verify native qualification applicability, run exact-source checks and seal scope for review. | Candidate proxy-acceptance-review-8ek3s67y passes 15 helper tests, seven client failure cases plus success, five observer tests, syntax and secret scan. Actual pinned-container evidence matches helper/client/qualifier hashes and owner-private modes. Two consumed predecessors preserved; no live authorization or execution. |

| W-111 | Third private check fails at unauthenticated monitor-list acknowledgement. | AC-004, AC-008 | Resolved | Reproduce the pinned unauthenticated Socket.IO path locally; retain a safe distinction between acknowledgement timeout, disconnect and unexpected response before proposing another live attempt. | Receipt: IPv4 unauthenticated-denial, UNCLASSIFIED, exit 1, cleanup passed, about 12.4 seconds. Prior dashboard/TLS and WebSocket transport assertions passed by control flow; credential login and IPv6 were not reached. Pinned getMonitorList handler has an explicit false acknowledgement for checkLogin failure, so denial-as-timeout must not be assumed valid. Historical root cause unconfirmed; observation not launched. Local diagnosis: unmodified pinned server passes six probes; controlled 100 ms registration delay yields three connect-triggered ACK_TIMEOUT failures versus three expected false acknowledgements after loginRequired. Client readiness defect established; correction tracked in W-112, without claiming historical production causation. |

| W-112 | Gate requests on application readiness and classify acknowledgement failures safely. | AC-004, AC-008 | Resolved | Wait for the appropriate server readiness event with bounded timeout/disconnect handling; preserve explicit denial assertions and qualify real pinned-server delayed-registration behavior before sealing any successor. | Existing connect resolves on transport connection before the server has necessarily registered handlers. Do not accept timeout as denial or add arbitrary sleeps. Keep setup readiness separate and preserve private diagnostics and all three consumed bundles. Corrected client waits for loginRequired with a 10-second gate, requires setup only for the synthetic bootstrap, rejects unexpected readiness/disconnects and classifies acknowledgement timeout safely. Full real offline Kuma/Caddy delayed-registration run passed IPv4/IPv6 authentication and 65-second idle/logout checks; cleanup succeeded. |

| W-113 | Prepare readiness-gated application acceptance after W-112 qualification. | AC-004, AC-008 | Resolved | Freeze corrected client/helper and operation identity, verify offline qualification applicability and exact-source startup before sealing for review. | Candidate proxy-acceptance-review-t_v4hx55 passed 16 helper tests, 13 client failures plus readiness successes, five observer tests, syntax/secret checks and four actual pinned-container startup cases. Client matches full offline delayed-registration Kuma/Caddy success; three predecessors preserved. No live authority or execution. |

| W-114 | Passive Node A acceptance stops at final journalctl read. | AC-004, AC-008 | Resolved | Reconcile final journal command behavior from retained/local evidence; distinguish bounded read failure causes without disclosing raw journal content, and qualify before any separately approved retry. | Remote observer returned failure command-exit:journalctl:expected=0:observed=1. Collector discarded command stderr, so cause is unknown. Node A HTTP/identity/cycle evidence retained; journal acceptance unknown, Node B not contacted. No health failure or clean journal may be inferred from this exit status. Local journalctl 252 reproduced the same empty exit 1 with show-cursor; removing the unused final output-cursor flag yields successful empty output. Corrected full native observer and invalid-cursor rejection pass; bounded command diagnostics are retained. Historical cause remains unproven; live acceptance is still pending. |

| W-115 | Prepare observation-only continuation after W-114. | AC-004, AC-008 | Resolved | Bind corrected observer, accepted private receipt and fresh attempt/evidence identity; qualify and seal without repeating login or live observation. | Candidate proxy-observation-review-c9vdnab_ passes frozen-source tests, receipt verification, syntax and secret scan. Observer matches the full successful native journal/systemd/Caddy qualification. Four consumed attempts preserved; no live approval or execution. |
| W-116 | Publish reviewed pending changes and reconcile reported CI failures. | Repository publication; AC-010 | Resolved | Validate and secret-scan intended sources, commit/push to verified owner repositories and verify remote refs; preserve private evidence and deployment boundaries. | Aaron requested commit and push of all changes. Four owner repositories contain pending work. Latest server-config Caddy/Nautobot jobs passed; baseline secret scanning flags the exact archived runner SHA-256, independently verified and narrowly excepted. The older Nautobot failure is superseded by later passes. CodeQL startup failure has no jobs/annotations; the October 12 Webmin run has no available logs. All four source commits are pushed and remote-verified; their Repository validation and CodeQL runs passed. Private evidence and the empty oom scratch file remain excluded. No live change or retry is included. |

| W-117 | Reconcile the unused DNS candidate and conditional authority after Caddy acceptance. | AC-004, AC-008 | Resolved | Verify frozen inputs, unused phase state, original expiry, owner-source applicability and retained Caddy acceptance without target contact. | November 12 local archive/member/index checks and retained combined acceptance verification passed. Owner helpers match; repository zone differs only in record ordering, with an identical directive multiset. Preserve the sealed live-baseline bytes. Approval remains unused with its original expiry; current instructions pause live execution. See the reconciliation entry below. |

| W-118 | Initial DNS paired gate loses the underlying snapshot failure diagnostics. | AC-004, AC-008 | Resolved | Diagnose from retained/local evidence where possible; qualify bounded safe reporting of the actual subprocess status and failure category before a separately reviewed successor. | Approved before phase exited 1 after repeated snapshot_transport_failed and the bounded convergence deadline. Gate accepted=false; no apply invocation exists. The verifier combines nonzero remote exit and output-size rejection into one message and discards the underlying status/output. No DNS fault or SSH cause is established; no mutation/recovery occurred. Approval consumed; preserve all inputs and receipts. Current owner source now reports bounded exit/count/category/hint diagnostics; 34 existing-suite tests pass, including actual local streamed Python rejection and safe paired-timeout reporting. Historical cause remains unknown; no successor or retry is authorized. |

| W-119 | Prepare the DNS successor with qualified snapshot diagnostics. | AC-004, AC-008 | Resolved | Freeze current qualified verifier with unchanged candidate and checks, fresh operation/backup identity, preserved predecessor evidence and exact commands for review. | Successor uptime-kuma-dns-20261112-q8i4a51n is sealed and locally checked. Exact archive/indices, qualified verifier identity, reviewed operation delta, predecessor preservation and secret scan pass; wrong digest is rejected. No target contact or execution authority; original November 14 expiry retained. |

| W-120 | DNS successor rejects the secondary boot identity. | AC-004, AC-008 | Resolved | Reconcile retained identity provenance and define any needed bounded refresh before a separately reviewed successor; preserve exact checks and both consumed attempts. | Approved successor before gate exited 1 with secondary boot_identity_mismatch, expected exit 0 / observed 1, stdout 0 bytes / stderr 191 bytes. Gate accepted=false; no apply invocation or mutation receipt. Primary was not reached because the secondary snapshot failed first. No restarts or recovery; approval consumed. Current boot value and timing/cause of the boot change were not captured. Earlier attempt cause remains unknown. Local provenance reconciliation confirms the expected secondary ID in the October 20 capture and October 21 accepted operation, inherited unchanged by both attempts. Later reviewed DNS/proxy evidence supplies no new boot ID. Existing owner readiness refresh is required; W-121 tracks preparation. |

| W-121 | Refresh paired DNS readiness before another deployment candidate. | AC-004, AC-008 | Resolved | Prepare and separately authorize bounded read-only owner readiness, capture both boot identities and current DNS baseline/health, then reconcile before sealing a successor. | Existing owner collector extended with Uptime-only readiness mode; v2 node archives sealed for separate review. 27 readiness and 34 transaction tests pass; exact streamed Python rejects the workstation identity before collection, archive/member and negative-digest checks pass, and secret scans pass. No new platform fixtures or simulated failover. Both approved v2 captures completed once, secondary then primary. Fresh boot/service stability, unchanged bound configuration/launcher identities, native validation, exact local DNS controls, expected absent Uptime records, public resolution and coherent primary-owned four-VIP state passed local reconciliation. Projection limitations retained below; no deployment acceptance or successor authorization. |

| W-122 | Replace historical boot pinning with operation-scoped continuity. | AC-004, AC-008 | Resolved | Capture current IDs at fresh authenticated admission; bind them through existing gates/dispatch and resumed phases; stop on unexpected mid-operation changes. Existing tests prove pre-admission reboot allowed, mid-operation reboot blocked and host/configuration drift still rejected. | Aaron approved the policy November 12. Workspace and DNS AGENTS.md instructions plus PLAN.md now distinguish durable identity from runtime continuity. Source implementation and local qualification are complete: initial paired gate binds admitted IDs to operation/digest; later gates, apply and rollback reuse them. Incomplete initial discovery and boot changes stop without re-admission. 42 transaction and 27 readiness tests pass; syntax, working-tree secret scan and preserved-archive/receipt hashes pass. No candidate is sealed, frozen bundle changed or live authority granted. |

| W-123 | Prepare DNS successor using fresh admission and reconciled readiness. | AC-004, AC-008 | Resolved | Bind qualified source, current readiness provenance, unchanged six-record candidate and exact operation/recovery scope into one reviewable archive. | Sealed uptime-kuma-dns-admission-20261112-myuc3p0t. Qualified W-122 source hashes match; paired-readiness and consumed evidence hashes verify; closed archive and input checks pass, wrong digest and missing admission are rejected, secret scan passes. Expiry retained. No phase, successor execution authority or deployment acceptance. |
| W-124 | Execute the approved DNS admission-policy successor. | AC-004, AC-008 | Resolved | One ordered attempt; accepted paired gates, unchanged admitted boots, exact records, both full restarts per node and ordinary-name HTTPS over both families. | November 12: all five phases exited 0, secondary before primary; no recovery or forced failover. Both final gates accepted, all four VIPs remained on .53 in retained samples, and both dashboard HTTPS checks returned 200. Private terminal summary binds receipts; backups retained. Approval consumed; no replay or publication. |
| W-125 | Reconcile retained acceptance and permanent documentation for closeout. | AC-002, AC-008, AC-010 | Resolved | Verify retained evidence, update stale task states and permanent docs, and report remaining acceptance gaps without fresh live work. | Seven indexed receipts verified; architecture/operations and Partial RESULT.md reconciled. W-004/W-008/W-026 resolved from completed work; W-020/W-076 remain explicit. No consumed input, live state or acceptance requirement changed. |

| W-126 | Host inventory still describes accepted foundation/application as not deployed. | AC-010, AC-011 | Resolved | Reconcile only accepted metadata with retained receipts under the inventory owner; preserve host/profile selection and partial project status. | Found during W-020/W-076 owner review; no target drift is implied by stale source metadata. Inventory now records accepted foundation/watchdog and service/dashboard dates with an explicit partial-closeout status and shared result link. Only five metadata fields changed; selections unchanged. Owner YAML/Markdown checks passed. |
| W-127 | Select final W-020/W-076 acceptance dispositions. | AC-008, AC-010 | Resolved | Present a concrete owner-supported no-change decision and explicit unmeasured-renewal deferral for Aaron's agreement; do not silently waive required acceptance. | Owner source requires softblocks and automatic addresses/routes, not daemon removal. Retained checks pass those properties. Proposed decision below; W-020/W-076 remain unchanged pending agreement. November 12: Aaron explicitly approved the presented W-020/W-076 dispositions for initial-deployment closeout. Plan and result now reflect that decision; no inspection or mutation is included. |

| W-128 | Replace tunnel-only Webmin access with a normal HTTPS browser endpoint. | AC-011, AC-013 | In progress | Owner-governed backend restriction, dedicated Caddy/DNS route, trusted TLS, private login/session/WebSocket acceptance and unrelated-service preservation. | Aaron rejected the SSH-only access policy and requested direct browser access through Caddy/DNS as needed. Prepare locally; existing operation approvals remain consumed. |

| W-129 | Make the existing DNS procedure the entry point for all fleet DNS changes. | AC-010, fleet DNS requirement | Resolved | Shared intake, add/edit/delete query contract, broader-change owner routing and consumer links; local documentation checks. | Existing procedure adapted in place; DNS instructions/index and Caddy/Webmin onboarding point to it. No new execution engine, live authority or claim of support for unqualified record types. |

| W-130 | Complete shared Webmin backend profile and focused local qualification. | AC-013, W-128 | Resolved | Preserve auth/TLS/referers; exact listeners/sources and native redirect/rejection checks with limitations stated. | Renderer and example added in place; 4 profile, 7 readiness and 7 existing atomic-helper tests pass. Native Webmin 2.670 tests passed with networking disabled. Two fixture failures expected a redirect from an internally served login path; corrected to exercise native explicit redirect mapping. No login/TLS/Caddy/CSRF/WebSocket acceptance claimed. |
| W-131 | Prepare bounded first-host Webmin readiness capture. | AC-013, W-128 | Resolved | Exact read-only scope approved, one complete safe capture reviewed before host binding. | One-use sealed bundle below; strict retained SSH host-key pin, fresh boot continuity and selected non-secret settings. Local syntax, ShellCheck, manifest and collector tests passed. Aaron approved one capture; it exited 1 with hostname_mismatch before configuration reads/diagnostic commands. No mutation; approval consumed. W-132 resolved locally; the separately approved corrected successor completed once with all seven commands successful, stable boot/configuration identity and no mutation. Collection accepted; W-133 and actual proxy-source/ingress qualification remain. |

| W-132 | Readiness hostname gate failed without retaining the observed hostname. | AC-013, W-131 | Resolved | Reconcile the exact expected identity and qualify bounded credential-safe expected/observed reporting before separately reviewing another capture. | Sealed expectation was j2-svpi3bmf.local.theama.co. Strict SSH transport reached the collector; hostname_mismatch receipt contains no observed name. Do not infer short-name equivalence, relax the gate or retry. Retained promoted/foundation JSON supplied no hostname value. Subsequent frozen-operation reconciliation establishes j2-svpi3bmf as the previously accepted native expectation; exact-match semantics remain. Bounded expected/observed CLI reporting and 11 local tests pass. Failed live observation remains unknown; see reconciliation below. |

| W-133 | Reconcile the observed Webmin referrer policy and shared renderer rejection. | AC-013, W-128 | Resolved | Native source/behavior qualification, correct policy semantics and preserved legitimate access before host binding. | Earlier description that referers_none=1 disables checking was incorrect. Native 2.670 proves it rejects missing referrers; referer controls the global bypass. Renderer preserves referers_none, explicitly sets referer=0 and extends trusted names. Seven native CGI cases and local tests pass. Prior live referer value was not captured; full browser acceptance remains W-128. |
| W-134 | Qualify persistent ingress and full native browser/proxy behavior before sealing. | AC-013, W-128 | In progress | Native guard ordering/failure/recovery, trusted HTTPS login/logout/referrer/assets and applicable WebSocket checks; actual source/path and production-unit gaps explicitly closed before sealing. | Guard lifecycle, container restart and ordered loopback recovery passed. Earlier IPv4/IPv6 browser HTTP/session checks passed; the fresh full-browser fixture failed with OOM before WebSocket. W-135 blocks full acceptance. Actual target sources/paths and native unit equivalence remain unqualified. November 12 strategy revision: fixture capacity is not a prerequisite for the bounded target trial; actual-source/unit/browser acceptance still remains. |
| W-135 | Full-browser qualification exceeded the preserved Webmin service memory cap. | AC-013, W-128, W-134 | In progress | Webmin/host-owner footprint or capacity reconciliation and reliable native browser/resource qualification without weakening accepted controls; then close the actual target-path gaps. | Fresh isolated AMD64 fixture timed out opening the protected referrer settings page and subsequently ended Result=oom-kill, MemoryPeak=201326592 bytes, MemoryHigh=134217728, MemoryMax=201326592, NRestarts=0. WebSocket stage never ran. This is a local failure, not proof of Pi failure; preserve limits and evidence before choosing a remedy. Retained-evidence reconciliation confirms matching source hashes and owner memory/swap/CPU/task controls, but no allocation/event timeline exists. A cap increase or specific cause is not justified. Existing sampler attribution fields are locally qualified; align the native fixture and capture causal evidence next. One aligned native-unit/foundation diagnostic now passed IPv4 including WebSocket: 139042816-byte peak, no OOM/max events or restart. Sustained paired-proxy/dual-stack capacity and historical causality remain unqualified; see phase capture below. The subsequent paired fixture failed its second path at trusted-referrer: 169021440-byte peak, 12440 memory-high events, severe reclaim stalls, paired health timeouts and HTTP 504, with no max/OOM event or restart. The sustained phase never began; see paired resource evidence below. This supports current-run throttling, not attribution of earlier failures.  Aaron approved moving capacity acceptance to the actual host; no further substitute-fixture capacity pass is required. |
| W-136 | Propose a durable boundary between fixture testing and target-host capacity acceptance. | Validation policy, AC-006, AC-013 | Resolved | Review the exact workspace instruction below; install only after its approval, with one canonical rule and skill/repository references as needed. | Aaron approved the exact proposal; installed verbatim in /home/aaron/code/AGENTS.md on November 12, 2026. Direct mechanism/resource regression and controlled comparisons remain allowed with bounded, explicit claims. |
| W-137 | Prepare bounded actual-host browser/resource qualification from accepted evidence. | W-128, W-134, W-135, AC-013 | Resolved | Reconcile installed unit identities and actual proxy sources; bind one target workload, unchanged controls, acceptance and independent recovery before exact live review. | PLAN.md defines the trial. Extended owner collector and one three-target read-only readiness bundle are locally qualified and ready for separate review. No target contact or mutation bundle sealing.  Approved capture passed once on the Pi and both proxies; installed controls/identities and current sources retained. No per-user ama terminal ACL exists; capability/recovery binding remains before mutation sealing. Approval consumed. Native backend apply/restore includes and private first-host bindings are locally qualified; Caddy parent/recovery and combined observation integration remain before sealing.  November 16: exact combined trial sealed for review under W-144. Preparation closure is satisfied; this does not resolve AC-013 live acceptance or authorize execution. |
| W-138 | Define safe per-host WebSocket acceptance and retain reusable onboarding discoveries. | W-128, W-137, AC-013 | Resolved | Fleet procedure defines effective capability, safe action, expected results and cleanup; selected host has an evidenced safe method or owner-reviewed applicability disposition before sealing. | Aaron confirms existing ama access to System Information and real-time statistics. Select that native authenticated statistics WebSocket; pinned source checks module/session access and does not launch a terminal. Record ordinary collector/cache side effects, preserve settings, close only test sessions and never invoke global shutdown/disable. Live permission/traffic/resource acceptance remains pending; method selection is not a live pass. |
| W-139 | Prevent late backend writes after timed recovery and qualify native lifecycle handling. | W-137, AC-013 | Resolved | Bounded apply is stoppable by independent recovery; exact baseline and unrelated state survive, late apply rejects, and diagnostics remain bounded. | Backend writes moved into one native systemd service; recovery stops it before locking/restoring. A transient unit may disappear after completion, and the guard contributes a reverse After edge until unloaded. Native tests and failure regressions retain earlier failed runs; final exact-input native qualification passed with restored controls/listeners, preserved unrelated table and rejected late apply; 14 focused regressions pass. |

| W-140 | Complete the fleet Caddy application binding and temporary paired-release recovery. | W-137, AC-013 | Resolved | Build the selected owner fragment rather than a hard-coded Kuma fragment; qualify post-exposure restoration and transport residue before sealing the combined trial. | Local integration review found a Kuma-only payload source and 20-prefix restriction. Existing application_restore covers local activation failure; the application outer cleans its payload on success and has no paired temporary-trial restoration phase. Do not call certificate repair rollback or claim that backend restoration restores Caddy. Local disposition: selected-fragment binding and actual offline paired restoration now pass through the existing owner entrypoints; normal finish, timeout, lost exposure reply, partial convergence, failed recovery, incomplete candidate and late exposure are covered. Controller-loss Caddy recovery remains explicitly manual/incomplete, independent of native backend recovery. |

| W-141 | Integrate the combined trial with the existing guarded-scan observer without reinstalling the guard or adding a competing sampler. | W-137, AC-013 | Resolved | Exact installed scan entrypoint, single observer, service/cgroup/host samples throughout the workload and scan, real-path/source evidence and owned cleanup are executable and locally qualified. | Existing guarded-scan.yaml imports installation tasks; observe-needrestart.py explicitly reports scan-only acceptance. The parent must retain the 224/192 MiB admission and 96 MiB reserve, include workload samples during scans and stop owned load on failure. No new installed identity or target measurement is assumed. Local component qualification now passes: separately staged source/profile, installed guard preservation, one locked observer, pre/workload/scan/post samples and failure receipts. Real-path/source and browser overlap/owned-load cleanup still require the W-137 parent; no combined acceptance claim. November 16: local parent integration passes token-gated readiness, all-path browser/session receipts, cross-clock scan overlap and owned cleanup. This closes local implementation qualification only; actual-host AC-013 remains pending. |

| W-142 | Reject incomplete candidate copies when recovery calls validation in a conditional shell context. | W-140, AC-013 | Resolved | Actual owner restoration rejects a missing manifest, retains incoming state and stopped transport, and returns recovery incomplete. | The new offline incomplete-transfer case recovered instead of rejecting. certificate_verify_candidate relied on errexit for intermediate commands; its conditional recovery caller disables that behavior. Add explicit failure returns and rerun the real entrypoints; no live state was involved. Explicit failure propagation now rejects the incomplete manifest in the actual native recovery case with exit 125 and stopped transport; all 16 application cases pass. |
| W-143 | Bind the combined parent to real path counters and the statistics-only client without fixed-time scan races. | W-137, W-141, AC-013 | Resolved | Exact owner interfaces, gated paired workload, conservative cross-clock overlap, process cleanup and recovery ordering pass focused local tests before sealing. | The old browser fixture uses xterm and cannot be reused for W-138. A fixed scan start can precede browser readiness. The guard has no per-source accept counters. Prepare a native statistics-only client, parent-supervised workload readiness/cancellation and named per-source counters; preserve ordinary collector settings and all earlier evidence. Changing the rendered guard requires renewed correctness checks, not a fixture capacity workload. November 16: fresh open-socket frames, all-six-path sustained checks, old-session denial and two-client bounded concurrency pass local regressions. Real client receipt logic joins the parent verifier; exact final source hashes and affected-test rechecks are retained below. No native browser or target acceptance is claimed. |

| W-144 | Complete the exact Caddy temporary-trial candidate and combined parent authorization graph. | W-137, AC-013 | Resolved | Current owner qualification and authorization policy pass; every parent non-secret execution input and external secret/readiness reference is bound; exact command, acceptance and recovery are reviewable before live approval. | Preparing one 20261116-webmin-first-host-trial definition from the clean stream. No live authority or publication. Retain definition-check failures and baseline snapshots in webmin-combined-review-0ve83yjr.  November 16: sealed 236-file parent manifest and exact Caddy outer identity below. Sixteen offline Caddy cases, owner authorization/negative-evidence checks, final parent syntax/module checks and six private-handoff cases passed. Source graph and external credential/readiness references bound; no live authority. |
| W-145 | Caddy temporary-trial coverage labels a successful restoration as reject, contradicting exit 0 and blocking authorization. | W-144, AC-013 | Resolved | Success expectations derive from the existing expected statuses; actual owner qualification and authorization/negative-evidence checks agree. | Discovered during final candidate checks. Original 16-case run passed but authorization failed at application-trial-success. Retain original evidence and policy-diagnostic.log; correct the coverage generator without changing deployment behavior.  Corrected coverage expectations to use existing expected exit statuses. Final 16-case qualification, exact authorization-ready gate and evidence-mutation checks all pass. Preserve original policy mismatch, failed pre-scenario wrapper/fixture hash binding and both original qualification runs; no live behavior or threshold changed. |
| W-146 | Execute the approved combined Webmin/Caddy trial once and reconcile independent acceptance/recovery outcomes. | W-128, AC-013 | Resolved | Preserve approved inputs and one-attempt marker; verify native browser, source/path and scan-overlap/resource evidence plus Caddy and backend restoration separately. | November 16 exact-bundle approval recorded in private approval.json. Input and owner preflight passed without contact; awaiting private workstation operator launch. No attempt has started; do not relaunch after a marker or failure.  Attempt completed with parent exit 2 and Caddy exit 1; primary IPv4 HTTPS timed out before browser/scan. Both owner recovery checks passed. Execution disposition resolved as failed-consumed, not application acceptance; W-147/W-148 carry remaining diagnosis/archive work. |
| W-147 | Primary Webmin HTTPS route times out after activation despite passing direct backend paths. | W-146, AC-013 | Open | Reconcile retained failing request, route/configuration and recovery evidence locally; identify supported cause or the precise missing observation before any separately reviewed successor. | curl 28 after 5001 ms, HTTP 000, zero response bytes on Node A. No application IPv6, browser or scan acceptance ran. Cause is unconfirmed; do not extend deadlines or infer capacity/authentication failure. Local reconciliation below identifies the request-path difference and missing timing/correlated logs; no further fixture load can establish the historical cause. November 17 W-187: eight health requests precede the marked proxy request; pressure begins during its bounded interval, while OOM follows the timeout. Backend delivery is proven, internal CGI/process attribution is absent. Trace the startup request burst before selecting one controlled comparison; no capacity waiver or retry. |
| W-148 | Preserve and prepare the consumed combined trial terminal archive under the Caddy owner. | W-146, Caddy lifecycle | Resolved | Exact executed inputs and sanitized terminal record remain preserved; review any archive commit/tag/push separately before cleanup or implementation changes. | All 236 non-secret inputs copied and hashes checked in executed-inputs. Caddy is terminal-pending/failed-consumed with planned archive tag. A 61-file exact archive is prepared below; core lifecycle checks and actual documentation check pass, but the broader policy self-test has W-149’s missing sibling-tree fixture failure. No publication authorized. November 16: approved archive published as commit 66d8ae5 and annotated tag caddy-webmin-first-host-trial-terminal-2026-11-16; remote branch/tag/peeled commit verified. Hooks passed; W-149 remains explicitly deferred. Cleanup not performed. |
| W-149 | Documentation self-test omits the sibling DNS owner tree referenced by the fleet onboarding guide. | W-148, local validation | Resolved | Caddy test owner retains follow-up here for future documentation-test maintenance; do not repair or repeat the fixture for this historical archive. | Aaron explicitly declined fixture repair for this effort on November 16. The actual workspace link check passes; the isolated self-test failure remains recorded. It does not establish production behavior or block preservation of the failed attempt. No test disabled, pass fabricated or publication authorized; mandatory publication hooks remain intact. November 16 current request authorizes resolving this CI blocker: fixture now preserves the real server/DNS sibling layout and copies the actual linked owner document. Missing-document rejection and all existing negative checks pass. Earlier archive deferral remains historical. |
| W-150 | Clear archived Webmin trial bindings and restore the neutral Caddy stream locally. | W-148, W-147 preparation | Resolved | Verify the published archive identity, reset consumed operation/recipe/terminal evidence, preserve implementation and accepted state, and pass focused owner checks. | November 16: archive bytes matched the annotated tag and retained remote-verification receipt. Inactive operation and clean stream retain the archive tag; recipe is header-only, terminal manifest/registration removed, outer operation hash rebound. Runtime transaction and accepted-state manifests unchanged. Eight focused checks passed; uncommitted, no live contact or publication. |
| W-151 | Prepare W-147 diagnostic correction in the existing Webmin/Caddy paths. | W-147, AC-013 | Resolved | Align request paths; retain safe timed failure evidence before recovery; qualify exit preservation, confidentiality and parent recovery ordering locally. | Matching session_login.cgi backend request, direct/curl phase timing, filtered bounded Caddy journal metadata and parent pre-restoration numeric snapshot implemented. Focused tests cover curl failure retention, private-text exclusion and recovery despite unavailable diagnostics. Final six-scenario parent test passes. Source hashes and results retained below. No historical root-cause attribution, successor or live authority. |
| W-152 | Seal a bounded diagnostic successor using existing Webmin/Caddy owners. | W-147, W-151, AC-013 | Resolved | Exact owner graph, diagnostic-only parent, immutable input/command bindings and focused qualification ready for separate live review. | Diagnostic-only mode skips all credential/browser/scan work and immediately finishes after owner readiness. Sixteen offline Caddy cases, eight parent scenarios, helper tests, syntax, owner authorization and sealed preflight pass. Exact review below; no live authority. |
| W-153 | Execute the separately reviewed route diagnostic once if authorized and reconcile both recoveries. | W-152, AC-013 | Resolved | Explicit exact-bundle approval, one-attempt marker, retained original failure/timing and independent owner recovery results; no production acceptance inferred. | Aaron approved WORK.md:7311. One attempt exited 2 (Caddy child 1); primary HTTPS curl 28 after successful TCP/TLS. Both Caddy restore/resume and native Webmin restore assertions passed. All 230 inputs and receipts retained. No browser/scan. Replication-health alert remains W-154; no acceptance or replay follows. |
| W-154 | Aaron reported replication-health failure during diagnostic recovery. | W-153, Caddy owner | Resolved | Reconcile retained chronology and recovery coverage; establish subsequent monitor health through separately reviewed authority if evidence is insufficient. | User notification at 17:53:23 UTC reports caddy-sync-health.service exit-code, lsyncd unknown, Caddy active, no VIP movement. Recovery checks do not prove a later successful monitor cycle. No fresh inspection or reset/restart authorized. Local reconciliation completed: sender containment leaves health timer running; inactive sender or invalid status snapshot can reject. Exact failing predicate and post-resume health are absent. Static notification labels are not measured transitions. Remains Open. W-164 accepted capture now retains the failed sender-validation message at 17:53:23.458 UTC, sender start at 17:53:23.911 and successful next health cycle at 17:54:26.674; two further natural cycles passed during observation. Historical unknowns above are superseded for this alert, not the Webmin timeout. W-165 tracks recurrence/acceptance design. |
| W-155 | Diagnostic narrows HTTPS failure to after TLS; later snapshot includes Webmin OOM counters without event timing. | W-147, W-151, AC-013 | Resolved | Review retained evidence and actual request/control paths locally; distinguish missing observations from established cause before proposing another bounded operation. | Four direct login requests passed in 2.36–2.54 s; primary TCP 0.000118 s, TLS 0.052676 s, no first byte by 5.002007 s. Journal projection retained 32 other-category entries. Later Webmin peak 192 MiB, oom 3, oom_kill 1; no before/after counter or event timestamp establishes when or why. Neither historical nor current cause is proved. Local source/evidence review complete: direct probes were sequential, while the activated fragment defines two backend health probes alongside proxy requests; actual overlap was not recorded. Client TLS timing does not measure upstream connection. The bounded journal projection cannot recover discarded messages. Missing evidence and uncertainty are explicit; W-147/AC-013 remain unresolved. |
| W-156 | Preserve the consumed diagnostic in its required terminal archive. | W-153, Caddy lifecycle | Resolved | Review exact terminal commit/tag/push separately before publication or neutral cleanup. | All 230 executed inputs copied and hash-verified; three Caddy readback streams decoded with byte/hash verification. Terminal result/history recorded, successor/coverage cleared, stream terminal-pending. Operation/recipe/implementation bytes preserved. No publication authorized. Exact 12-file archive prepared with temporary index, source hashes, patch, messages and guarded command; nine focused checks pass. Normal index unchanged; publication requires separate approval below. Approved continuation published commit 4e6b3d5 and annotated diagnostic terminal tag; exact tree and remote branch/tag verified. Mandatory hooks passed, server worktree/index clean. Original failed attempt retained. No neutral cleanup or live authority. |
| W-157 | Replication notifier loses nonactive sender status and presents static transition/VIP labels as event context. | W-154, Caddy notification owner | Resolved | Owner review should preserve command status and safe observed state separately; distinguish static context from measured transitions and qualify the existing notifier before any deployment. | Pure local reproduction of the current expression converts inactive plus exit 3 into unknown. No notifier execution, message send or source change. Track here for follow-up after terminal archival; do not infer the exact live sender state from unknown. November 16: existing notifier corrected and seven reporting cases pass locally through actual producer invocation with captured enqueue. Source and installed hashes remain distinct. Three focused profiles, syntax/lint/format and collision checks pass. No installed rollout or live acceptance claimed. |
| W-158 | Approved terminal archive publication stopped at test-inventory hook. | W-156, Caddy archive | Resolved | Preserve failure, resolve generated-file mismatch without changing executed source, review continuation from exact staged tree. | One ignored Python bytecode file was unregistered. Preserved privately, removed locally; inventory check passes. Base and 12-file tree unchanged, no commit/tag/push. Continuation prepared below; no replay. Approved continuation published commit 4e6b3d5 and annotated diagnostic terminal tag; exact tree and remote branch/tag verified. Mandatory hooks passed, server worktree/index clean. Original failed attempt retained. No neutral cleanup or live authority. |
| W-159 | Two published commits fail CI because the pinned DNS dependency lacks the linked owner procedure. | Repository validation, Caddy CI | Resolved | Update and qualify the immutable DNS dependency pin separately from the preserved terminal archive; retain W-149's independent self-test limitation. | Runs 43913820717 (c88c77b) and 43913190025 (66d8ae5), jobs 133462505168/133460271387, fail Repository policies at the APPLICATION_ONBOARDING.md link to Unbound/docs/host-record-deployment.md. Workflow pins DNS 9ae13d0, which lacks that file; published 2ce7105 contains it. No workflow edit, rerun or publication performed. Approved pin correction now selects 2ce710544c96479da2d79ab058a023646dd33c92. Exact clean old/new checkouts prove document check fail/pass. Full qualification is partial: W-149 still fails and W-160 exposes stale accepted-zone hash. Synchronization and remaining serving regressions pass. No publication. November 16 final qualification passes all three Caddy host CI profiles with DNS 2ce7105 and corrected W-149/W-160 dependencies; workflow syntax passes. Local only, no remote CI success claimed. |
| W-160 | New DNS checkout exposes a stale accepted-zone hash in Caddy serving-health validation. | W-159, DNS/Caddy ownership | Resolved | Reconcile accepted deployed DNS evidence and repository-source identity before changing the manifest or test; qualify the exact owner decision. | serving-health-regression.sh:316 compares current DNS zone source to f1f422d64a55a77af4d77a829ed3360341cf89f5f78c8e87419f01c3e593054d. Selected published DNS source is 4659dde5e93786ab144cb5a4f31b40de99faece7500303fcbde9ac65968158d9. Every other serving-health manifest input matches its expected hash. No runtime/hash waiver applied. Verified November 12 terminal evidence index, both apply results and paired gate. Installed hash is 2df1be44a9ea39a35df1e75db16d72a4138b4ab3048fdc7bcf58bd7ff1a959dc; source remains 4659dde5. Reconciled canonical/serving inventory and typed source/deployed comparison. Wrong source and installed hashes both reject. |
| W-161 | Complete published diagnostic neutral cleanup before rebinding reconciled inventories. | Caddy lifecycle, W-160 | Resolved | Verify consumed inputs against published terminal tag; clear operation/recipe/terminal record, preserve archive, refresh inactive/state hashes and pass owner policy. | Exact operation, recipe, transaction, outer and terminal record matched tag at 4e6b3d5 before cleanup. Stream now clean, operation inactive, successor absent; no transaction behavior changed. Full three-profile qualification passes. Local changes uncommitted; no live authority. |
| W-162 | Review qualified CI/inventory reconciliation for later publication. | W-149/W-159/W-160/W-161 | Resolved | Confirm exact changed paths, qualification identities, ownership, archive preservation and secret disposition; keep publication separate. | Reviewed 15 server files and three monitoring records; source hashes match final qualification, full three profiles passed. Server secret scan passes; one monitoring finding is the verified diagnostic-manifest digest, not a credential. No commit/push or live work. Publication remains awaiting explicit instruction. |

| W-163 | Reconcile remaining replication alert, HTTPS timeout and notifier findings after publication. | W-154/W-147/W-157, AC-013 | Resolved | Separate established defects from missing target evidence and identify the next owner actions without replay. | Current owner source and retained reconciliation confirm the notifier defect and possible recovery/monitor overlap. Neither exact alert predicate, post-resume health nor timeout cause is established. Preserve all attempts; correct notifier locally, then separately prepare read-only health review before another Webmin trial. No source behavior or live state changed. |

| W-164 | Prepare read-only evidence to assess Node A replication health after the retained alert. | W-154, Caddy owner | Resolved | Separate authorization, one bounded capture, independent review of installed identities, continuity, worker evidence and natural completed cycles. | Local inspection bundle prepared below; syntax and ShellCheck pass. No target contact. Exact historical cause may remain unavailable if journals rotated. Notifier rollout is excluded. Approved once and executed: exit 0, empty stderr, continuity and installed worker/notifier identities checked; unit definitions match source. Historical failure and later successful cycles retained. Independent Node A monitor review passed with status-file age limitation below. Approval consumed, no replay. |

| W-165 | Reconcile recovery/monitor overlap and the limits of status-snapshot acceptance before another trial. | W-154, Caddy owner | Resolved | Review the existing recovery boundary locally; define explicit natural post-resume monitor acceptance and preserve honest reporting of intentional sender containment. Resolve status-file update semantics before claiming freshness; qualify any implementation change separately. | W-164 proves the health check ran before sender restart completed, then recovered naturally. Status file stayed at 17:53:36 while later cycles passed; current worker checks structure, not age. This does not by itself establish stalled replication. No monitor suppression, freshness threshold, forced cycle or new transfer is authorized. Reconciled locally: separate restoration from fresh natural-cycle acceptance; preserve reporting during intentional containment and do not infer stale health from report mtime. Upstream 2.2.3 source explains write throttling, not a guaranteed heartbeat. W-166 owns unimplemented observation integration. |

| W-166 | Integrate bounded natural monitor acceptance after Caddy trial restoration. | W-165, Caddy owner | Resolved | Extend existing recovery/observation path, qualify fresh success, failed/missing cycles, stale success and boot change; retain distinct restoration and monitor results within total owner deadline. | Procedure reconciled; executable integration remains pending. Keep timer and failure reporting unchanged. No new orchestrator, forced cycle, monitor suppression, repeated rollback or target contact. Local implementation complete: pre-resume identity/time, stable sender and boot checks, natural completed cycle within original 150-second cutoff, both readbacks on monitor failure and no repeated recovery. Nine observer cases and coordinator failure test pass; all 16 offline application cases pass after fixing the fixture timer stdout contract. Neutral pins refreshed, no successor. See final qualification below. |
| W-167 | Prepare request-correlated Webmin diagnostic evidence and bind post-resume monitor acceptance within existing deadlines. | W-147/W-166, AC-013 | Resolved | Qualify safe upstream timing, timestamped resource-event deltas, collector cleanup and the exact parent/recovery budget before sealing. | Local instrumentation and focused qualification complete. Native Caddy timing/privacy and resource reset/stop cases pass; parent restoration sequencing passes. W-168 completes the aggregate deadline and cross-clock bindings locally; exact successor preparation remains separate. No live contact or successor authority; preserve all consumed attempts. |
| W-168 | Bind diagnostic coverage and recovery to actual wall-clock limits before sealing. | W-167/W-166, Caddy and Webmin owners | Resolved | Bound responsive stalled remote commands, reserve recovery/readback time inside the unchanged 1200-second child and 900-retry parent wait, and retain clock uncertainty for cross-host interval comparisons. Qualify expiry and incomplete-evidence handling in existing paths. | SSH ConnectTimeout/keepalives do not bound a responsive remote command. W-166 checks completion within 150 seconds but sequential bounded queries may finish later. A 300-second sampler must cover the compared requests; timestamps from different hosts alone are not a clock-offset proof. No deadline extension or live inspection is authorized. Local implementation and qualification complete: hash-selected 240/840-second owner budgets, bounded remote process groups/SSH/uploads, unchanged W-166 recovery, boottime clock brackets and actual request-index/resource coverage. Missing receipts remain incomplete; no target acceptance or live authority. |
| W-169 | Prepare the exact bounded timing diagnostic successor. | W-147, W-167/W-168, AC-013 | Resolved | Bind current owner sources, fresh private inputs and exact qualification; seal for separate live review. | Exact 236-input candidate sealed; 16 native offline owner cases, current authorization-ready graph, unchanged W-168 parent/helper qualification and sealed verify-only pass. Exact command and scope below require separate live approval. Preserve archived attempts and accepted installed identities. |
| W-170 | Execute the approved timing diagnostic once and reconcile independent evidence/recovery outcomes. | W-169, W-147, AC-013 | Resolved | Exact approved command once; retain original result, timing/resource coverage and both recovery receipts; archive consumed owner inputs before cleanup. | Aaron approved WORK.md:8160; executed once, parent 2/owner 1. Primary HTTPS timed out; direct/denial passed. Both owner restorations and fresh natural monitor cycles independently verified. Original correlation failed; local supplemental correlation retained separately. Inputs/receipts preserved, stream terminal-pending. No replay or promotion follows. |
| W-171 | Failed owner path omits the evidence-directory marker needed by the correlation consumer. | W-168/W-170, Caddy/Webmin owners | Resolved | After terminal archival, correct the existing producer/consumer contract and exercise its actual nonzero exit path before any successor. | Parent failed with owner_evidence_directory. Outer prints that marker only after run_live; its nonzero primary result exits first. Exact local evidence was independently bound through payload hashes and target revision, then correlated separately; the original receipt remains failed. After W-173 archival, the existing outer emits its private evidence directory before fallible phases. Actual bottom-level dispatch tests preserve exit 0/28/125 and a usable mode-0700 evidence directory. No live retry ran. |
| W-172 | New replication-health alert during the approved timing diagnostic. | W-170, Caddy owner | Resolved | Retain the alert and prove post-resume health without treating notifier transition/VIP labels as evidence. | Aaron supplied the November 16 21:15:23 UTC Node A alert. Both fresh natural monitor cycles subsequently passed, 66.719 and 40.997 seconds after their respective resumes, with active timers and stable senders. Exact alert predicate was not retained; static notification assertions remain unsupported and W-157 is not installed. No additional inspection needed to establish subsequent health. |
| W-173 | Archive the consumed timing diagnostic before changing its executed inputs. | W-170/W-171, Caddy lifecycle | Resolved | Prepare exact terminal commit/tag/push review and publish only under separate authority; preserve current inputs until verified archive. | Terminal record/history added, successor/coverage cleared, stream terminal-pending. All 236 reviewed bytes and three hash-verified readbacks retained privately. Exact 23-file archive published under Aaron's WORK.md:8357 approval: commit a6491d0795e4493e000f3afe81be09d01514fffd and annotated tag caddy-webmin-proxy-timing-diagnostic-terminal-2026-11-16 remote-verified. Mandatory hooks passed; consumed-input cleanup has not run. |

| W-174 | Narrow W-147 diagnosis to one primary IPv4 request path. | W-147, AC-013, Aaron's November 16 scope approval | In progress | After W-173 archival, correct W-171 and qualify only the changed request/evidence/recovery boundaries; bind a primary-only direct/proxy comparison for exact live review. | Scope approved: sequential equivalent requests, bounded target timing/resources, no secondary exposure or application acceptance. Production probe serialization is a hypothesis, not an approved fleet policy. Preserve controls and failed attempts; PLAN.md records the diagnostic boundary. Primary-only owner/parent scope and W-176 backend-interface observation are locally qualified. W-178 seals the primary/Pi candidate for review; no live attempt exists. |

| W-175 | Return the archived timing operation to neutral source state. | W-173, Caddy lifecycle | Resolved | Verify the published archive identity, remove consumed bindings and terminal metadata, refresh neutral hashes and pass owner clean-state policies. | Local cleanup complete; latest archive retained, no successor, operation inactive. Window/lifecycle/successor checks pass. No installed identities or source publication changed. |
| W-176 | Complete native backend request evidence for the narrow diagnostic. | W-174/W-147, AC-013 | Resolved | Implement bounded backend request/header/response evidence and correlate both foreground requests with health probes and resource intervals; qualify privacy and incomplete-result handling before sealing. | Existing collector now uses a bounded native Linux packet socket on the backend interface, with no packet files or vendor-source changes. Marked direct/proxy requests retain safe header comparisons, kernel timestamps, response status and connection close/reset; marked health probes retain possible overlap. Both request IDs and resource coverage are required. Gaps/drops/missing receipts fail completeness; absent responses remain unknown. Network receipt is not proof of CGI execution or full HTTP-body completion. Focused native offline, parent and correlation tests pass; no host capacity or historical-cause conclusion. |
| W-177 | Remove duplicate application-package transport during routine onboarding. | Aaron November 16 direction; Caddy application owner | Resolved | Send application fragment/publisher only to the primary; retain exact control metadata on the secondary and verify its replicated release through existing installed machinery. Qualify ordinary and temporary-trial paths before binding the diagnostic. | Current outer builds a primary application package and a recipe-only secondary control archive. The transaction rejects application fragment/publisher files in secondary staging and verifies the replicated fragment separately. All 18 offline owner cases pass; primary-only success/failure restores without secondary SSH. Source-qualified, not deployed. |
| W-178 | Prepare the exact primary/IPv4 diagnostic candidate. | W-174/W-176, AC-013 | Resolved | Bind current owner sources, primary-only private inputs, qualification and exact review command; preserve all consumed attempts. | 241-input candidate sealed; owner authorization-readiness and private verify-only pass. The review below binds one primary/Pi diagnostic; live execution remains unauthorized. |
| W-179 | Execute the approved primary/Pi diagnostic once. | W-178 exact authorization; W-174/W-147 | Resolved | Retain direct/proxy evidence actually produced, preserve failure, and verify owner recovery without replay. | Parent exited 2 before Caddy launch: direct login-page HTTP 401, 51 ms. Interface capture confirms 401/close, no capture loss/issues; 33 resource samples retain stable Webmin identity and zero high/max/OOM events. Webmin exact loopback restoration passed and independent timer was disarmed. No proxy request, secondary contact or application acceptance. Receipt identities retained below. |
| W-180 | Reconcile the unauthenticated login-page contract and pre-Caddy diagnostic outcome. | W-179/W-174, AC-013 | Resolved | Compare retained native Webmin response/configuration with the selected direct/proxy acceptance contract; distinguish a valid authentication response from a defect before any successor. Treat absent proxy evidence as not run. | Direct client currently requires HTTP 200 plus login-page markers; actual matched request returned 401 promptly. No response body/authentication challenge was retained, so its cause/validity is not yet established. The final comparison checker reported unavailable because Caddy output did not exist; it did not cause the initial stop. Do not weaken the check or repeat live work without reconciliation. | November 16: pinned native handler forces HTTP authentication for `/webmin/i` User-Agents. Exact-header A/B/A returned 401 Basic / 200 login form / 401 Basic. Keep HTTP-200/login-form acceptance and correct the probe header; historical HTTPS timeout remains unconfirmed. W-181 tracks source integration and early-exit reporting.
| W-181 | Integrate the reconciled probe contract without weakening acceptance. | W-180/W-174, AC-013 | Resolved | Use the neutral User-Agent in direct/proxy probes and wire comparison; retain HTTP-200/login acceptance, represent pre-Caddy exit as not run, then refresh/qualify owner bindings before any successor. | Neutral User-Agent integrated at all three sites. Pre-Caddy coverage reports not-run and preserves failure/restoration. Three primary parent scenarios and focused HTTP/privacy/owner checks pass. Withdrawn child was never executed; neutral hashes and clean stream pass owner policies. All 241 consumed input copies verified. No successor or live authority. |
| W-182 | Prepare corrected primary/Pi diagnostic candidate | W-147; AC-013; W-181 | Resolved | Qualify current owner graph and exact parent/input bindings; seal for separate live review. | New 241-input candidate sealed; 18 owner cases and nine evidence rejection cases pass. No live authority; W-147/AC-013 remain unresolved. |
| W-183 | Execute approved corrected primary/Pi diagnostic once | W-147; W-182; AC-013 | Resolved | Retain terminal evidence and both owner restoration results; reconcile remaining uncertainty. | One attempt exited 2. Direct HTTP 200; primary curl 28. Recorded headers match; Webmin memory pressure and later OOM kill observed. Both restorations and natural primary monitor acceptance passed. W-147 remains unresolved. |
| W-184 | Close-only unmarked flows reject aggregate diagnostic correlation | W-147; W-176; AC-013 | Resolved | Reconcile retained flows and qualify a bounded completeness contract without discarding real capture gaps or changing consumed inputs. | Both marked header records exist; strict per-flow header requirement rejects flows containing only connection close events. Original rejected receipt remains preserved. November 17 W-187 reproduces the rejection with the unchanged checker; flows 3/5 contain only FIN events. A separate no-observed-payload classification is specified below; implementation and focused qualification remain pending after neutral cleanup. W-188 cleanup completed; corrected parser and 14 existing workload tests pass. Full retained-data correlation now passes in a separate derived receipt, retaining flows 3/5 and rejecting partial/unknown events and coverage failures. Original operation acceptance remains failed. |
| W-185 | Archive the consumed primary login diagnostic | W-183; Caddy lifecycle | Resolved | Prepare and review exact terminal archive; obtain separate commit/tag/push authority and verify publication before neutral cleanup. | Aaron authorized all-changes publication. Server commit bda63a4 and annotated terminal tag published and remote-verified; cleanup has not run. |
| W-186 | Publish all pending owner and tracking changes | Aaron publication request; W-185 | Resolved | Review scope, preserve private evidence, validate, commit/push and verify remote refs. | Server archive published; this monitoring commit records the authorized tracking publication. Final remote/CI receipts retained in the private publication review. |
| W-187 | Reconcile retained request, memory and close-only-flow evidence | W-147; W-184; AC-013 | Resolved | Verify retained integrity, establish bounded temporal facts and specify remaining causal/classification gaps without live contact. | All 71 receipt hashes pass; unchanged checker reproduces W-184. Clock-envelope checks place pressure during the request and OOM afterward. Eight pre-request health flows and two no-observed-payload flows are reconciled below. W-147 causation and W-184 implementation remain open. |
| W-188 | Reconcile published diagnostic archive to neutral Caddy state | W-185; W-187 | Resolved | Verify archive and retained publication receipts; clear consumed current bindings, preserve archive/private inputs, pass neutral owner checks. | Local cleanup authorized by the current next action; no successor or live authority. Annotated archive/retained remote identities verified; neutral operation/recipe/outer pins and lifecycle reconciled. Current repository-policy profile, neutral owner gates and shell checks pass. |
| W-189 | Trace startup health-request burst through the existing owner path | W-147; W-187 | Resolved | Identify source paths capable of generating the observed burst, distinguish source inference from target attribution, and record a narrow next decision. | Local source and retained evidence only; no new target or capacity fixture. Publisher validation, two finalizer validations, installed-identity reconciler validation and reload traced. Pinned Caddy source starts health checks during provisioning and checks immediately. This explains a burst mechanism, not which process produced each retained connection or caused the timeout; W-147 remains open. |
| W-190 | Review validation-probe containment under the Caddy owner contract | W-147; W-189 | Resolved | Identify a minimal proposed correction, caller/permission constraints, qualification decisions and unchanged live boundaries. | Validation subprocess network isolation is proposed; full validation and serving health checks remain required. Existing root/caddy-sync identity and file access must be preserved; no privilege expansion or networked fallback. See review below. |
| W-191 | Implement and qualify validation-only network isolation | W-190; W-147 | In progress | Preserve exact-config/module/TLS validation, existing privileges, runtime health and bounded recovery through actual owner delivery. | W-197 passed actual-primary read-only capability on 2.11.9; W-198 caller wiring and twelve boundary cases pass locally. W-199 delivery and pre-release restoration are implemented and locally qualified. Writable owner execution and a controlled target comparison remain separately scoped and unaccepted. Root fixture expansion is closed; no rollout or timeout attribution follows. |
| W-192 | Prepare a bounded primary-host validation-isolation check | W-191; W-147 | Resolved | Bind one non-activating primary-only execution to exact inputs, existing caller identities/restrictions, deadlines, safe evidence and owned cleanup before live review. | Prepared and authorized once; execution exited 1 at inspect.sh:60 before namespace/transient work. Expected version prefix was v2.11.4 with a space; actual output and version-command status were not retained. Release/boot exit checks passed, but capability remains untested. Approval consumed; W-194 owns local reconciliation. Successor W-197 completed the bounded target check; read-only capability passed. Owner integration remains W-191. |
| W-193 | Clarify fixture stopping rule beyond capacity | Workspace harness; W-191 | Resolved | Aaron reviews the proposed wording; preserve the existing rule and distinguish a fixture limitation from a real safety defect. | Aaron approved the exact clarification; installed in workspace AGENTS.md under the existing fixture section. Exact wording verified; no live or publication authority added. |
| W-194 | Reconcile capability-check version admission and missing observed evidence | W-192; W-191 | Resolved | Reconcile the expected version against retained evidence and preserve bounded observed version plus command status before reviewing any successor; do not infer target drift or bypass identity checks. | Local reconciliation: owner inventory records package 2.11.4, not the lost target CLI output. Pinned upstream Version() permits an absent build suffix. Old scalar gate rejects bare v2.11.4 and ignores nonzero command status with matching text. Minimal patch prepared, not applied to consumed inputs; 12 scalar cases and full-script syntax/static checks pass. Historical failure attribution remains unknown; any successor requires integration and separate review. |
| W-195 | Integrate and seal corrected primary-only capability successor | W-192; W-194 | Blocked | Bind corrected admission to one unchanged primary-only capability scope, qualify exact inputs and obtain separate one-attempt authority before execution. | Approved and executed once; version command returned v2.11.9/status 0 against required v2.11.4. Admission stopped before namespace/transient/validation work. Release/boot exit checks passed; remaining checks not reached. Approval consumed; W-196 owns baseline reconciliation. |
| W-196 | Reconcile observed primary Caddy version with owner baseline | W-195; W-191 | Resolved | Establish the applicable owner version/build baseline before preparing a successor; preserve exact identity checks and consumed receipts. | Aaron confirmed production-host upgrades and requested inventory update to 2.11.9. Owner inventory/current-state hash and future plan prerequisite reconciled; Node A CLI independently observed, Node B/package attribution operator-confirmed. Original package-set digest retained as historical; no fresh running-process or capability acceptance claimed. Consumed bundles unchanged. |
| W-197 | Seal capability successor with reconciled production version | W-196; W-192 | Resolved | Bind current owner inventory and exact 2.11.9 admission to the unchanged primary-only capability scope; qualify locally before separate execution approval. | Fourteen-input validation-capability-review-upci2q6g sealed; twelve scalar cases and shell/static/integrity checks pass. No live contact. Awaiting one-attempt approval; prior bundles unchanged. Approved and executed once: all six phases passed on primary Caddy 2.11.9, cleanup/continuity passed; session 84010 exited 0. Authority consumed; no owner integration or timeout attribution claimed. |
| W-198 | Integrate isolated validation at existing owner call sites | W-191; W-197 | Resolved | Preserve exact configuration/environment and caller failure behavior; qualify focused wiring without target contact or fixture expansion. | Publisher/finalizer/reconciler invoke the fixed helper path. Twelve extracted boundary cases and current-synchronization host profile pass; source identities refreshed, accepted installed identities unchanged. Helper remains undeployed; W-199 owns deployment bindings. |
| W-199 | Bind isolated-helper delivery and recovery to the existing owner operation | W-191; W-147 | Resolved locally | Provide exact helper identity/path/mode before caller activation, explicit prior-state restoration and aggregate deadline/recovery before any separately reviewed comparison. | Existing payload/transaction implement a hash-bound primary-only opt-in, verified backups, helper-first install, caller-first restoration and explicit empty-ID recovery. Fifteen real-file cases and application-onboarding host profile pass, including partial install, interruption, drift, failed restore and absent prepared directory. Original installed identities, controls and 240/840-second limits preserved; no deployment or writable-host acceptance. |
| W-200 | Prepare the validation-isolated primary/Pi diagnostic candidate | W-199; W-191; W-147 | In progress | Bind exact current parent/owner inputs and proportional execution coverage before sealing for separate review. | Private unsealed draft prepared with fresh token/paths, current candidate hashes and unchanged installed baselines/limits. Payload/parent syntax and three current primary-only whole-path tool-delivery cases pass; current graph/effect verification and four negative evidence checks pass. The missing-option gap and exact candidate authorization bindings are reconciled: a strict primary-only profile, fresh exact-candidate execution, actual authorization-gate rejection tests and parent bindings pass in a private projection. Main remains clean/inactive; sealing and live review remain. Prior receipts are unchanged. No target capacity/isolation fixture expansion or live authority. |

## Execution record

| W-201 | Approved diagnostic lacks its controller evidence directory; clock and terminal receipt writes fail after backend preparation. | AC-013; W-200 | Resolved | Qualify required private output-directory admission before mutation and reliable failure/recovery receipt persistence in the existing path; reconcile the unexecuted child before another candidate. | One approved attempt exited 2 before Caddy launch. Native backend restoration and restored-state assertion passed in parent.log; final local receipt could not be written. No HTTP comparison or timeout attribution. Preserve exact consumed inputs and review source locally; no retry authority. Local correction: prepared mode-0700 controller-owned storage is admitted before target contact using the actual receipt writer/readback. Six path cases, write-error propagation, three primary parent cases and clock-before-failure recovery pass. Frozen consumed inputs and unexecuted child remain unchanged; future bindings require separate review. |

| W-202 | Reconcile unexecuted Caddy child and prepare fresh parent after W-201. | AC-013; W-201 | Resolved | Preserve consumed parent, verify unchanged child graph and prepare fresh private inputs/storage with exact pre-contact qualification and separate approval. | Child never launched; same single definition retained. Exact graph and original qualification gate pass without relabeling evidence. New 263-input parent is sealed for review; actual pre-contact tasks pass. No live authority or target acceptance. |

| W-203 | Reconcile delayed backend response in isolated-validation diagnostic. | W-147; AC-013 | Resolved | Review retained direct/proxy timing, headers, health overlap and resource evidence; distinguish measured delay from cause before any controlled successor. | Direct returned 200; proxied first bytes arrived about 7.5 seconds after request, beyond five-second client timeout. Correlation passed; no sampled high/max/OOM events. Both owners restored. No new live authority. |
| W-204 | Preserve W-202 consumed Caddy operation in required terminal archive. | AC-013; Caddy lifecycle | Resolved | Publish exact reviewed archive and verify remote before cleanup. | November 17: approved W-207 command published the exact 32-file archive as 4986722 with annotated terminal tag; remote main/tag/peeled commit verified. Original failed attempts preserved; cleanup not run. |
| W-205 | Reconcile archive commit-hook lifecycle failure. | W-204; Caddy lifecycle | Resolved | Exact corrected tree approval, normal hooks and remote verification. | November 17: approved W-207 command published the exact 32-file archive as 4986722 with annotated terminal tag; remote main/tag/peeled commit verified. Original failed attempts preserved; cleanup not run. |
| W-206 | Remove Git repositories from evidence-only storage. | Workspace evidence policy | Resolved within accessible scan scope | Preserve evidence, relocate discovered Git metadata and prevent new evidence repositories. | Twelve discovered Git metadata entries reversibly relocated outside .local-evidence; former roots no longer recognized as repositories. Both consumed input manifests rehashed unchanged. Durable workspace rule added. Protected fixture subdirectories were not searched. |
| W-207 | Correct publication launcher initial-index binding. | W-204/W-205 publication | Resolved | Review corrected command, publish exact unchanged tree and verify remote. | November 17: approved W-207 command published the exact 32-file archive as 4986722 with annotated terminal tag; remote main/tag/peeled commit verified. Original failed attempts preserved; cleanup not run. |
| W-208 | Inspect and retire temporary Git metadata archive. | W-206; evidence-only workspace | Resolved | Preserve unique local history, remove stale registrations without deleting source, delete archive. | User authorized deletion after history review. All locally present objects preserved in verified inert packs; seven stale registrations retired, server refs/status unchanged and metadata archive deleted. |
| W-209 | Audit Git retirement artifacts for deletion and reconcile source ownership. | W-208; evidence-only workspace | Resolved | Verify unique work has a repository home before deleting redundant recovery artifacts. | Webmin combined module trees exactly match three currently published fork branches; owner publication document records identities. Other artifacts are synthetic baselines, duplicated source, superseded preparation or committed worktree indexes. Retirement directory deleted; original evidence retained. |
| W-210 | Reconcile published W-202 operation to neutral Caddy state. | Caddy lifecycle; W-204 | Resolved | Verify archive, clear consumed operation/recipe/result and qualify neutral bindings. | Archive commit/tag and retained remote receipt verified. Stream clean, inactive operation/current hashes, header-only recipe, no successor/coverage; terminal result preserved in tag. Focused state and current-tree docs checks pass. |
| W-211 | Repository-policy documentation self-test omits Webmin onboarding dependency. | Repository validation | Resolved | Repair the existing temporary-copy dependency coverage when separately scoped; retain failed profile. | Current-tree documentation check passes; full profile stops at missing Webmin/docs/CADDY_ONBOARDING.md in its temporary fixture. No production defect or target-capacity claim; fixture work not expanded during cleanup. November 17: Aaron authorized repair. Added Webmin onboarding document to the self-test copy; removal must fail specifically with relative_link_broken, restoration must pass. Full host repository-policy profile, canonical formatting and readonly/local collision check pass. Local only; historical CI failure retained. |
| W-212 | Review concurrent health/foreground request contract from retained evidence. | W-147; AC-013 | Resolved | Separate observed request equivalence/timing from causal hypotheses before proposing comparison. | Foreground header maps match; health maps differ and raw unexpected values are unavailable. Two overlapping health flows precede foreground by 177 ms; response payloads arrive after client deadlines. Proposed fixed-contract actual-backend concurrency comparison remains unapproved and undefined. |
| W-213 | Review scope and interpretation of a backend-only concurrency comparison. | W-147; AC-013 | Resolved | Specify one-factor comparison, access/recovery boundary, stop conditions and conclusions before implementation. | Recommend one/three/conditional-one identical requests using native Webmin tasks, not the Caddy-bound combined parent. No executable bundle or live authority. Preparation must prove aggregate deadlines and workload cleanup without capacity fixtures. |
| W-214 | Implement the narrow backend comparison using native Webmin components. | W-213; W-147; AC-013 | Resolved | Qualify aggregate deadlines, independent recovery/cleanup and terminal evidence before removing the execution gate or sealing. | Local integration complete: supervised 240-second forward and 840-second recovery invocations, client stop latch/lock, verified native restoration, observer exit and complete terminal coverage. Thirteen comparison tests (including five localhost Ansible recovery cases), fifteen native recovery tests and fifteen workload tests pass; host repository-policy profile and syntax pass. Exact candidate preparation and live acceptance remain separate. |
| W-215 | Bind and seal the W-213 backend-only comparison candidate. | W-213/W-214; W-147; AC-013 | Resolved | Bind exact inventory, owner inputs, private paths, limits and supervisor; qualify locally before separate live review. | Sealed 33-input private candidate webmin-backend-review-2k86wh8y. Primary-only IPv4 profile and pre-exposure route admission are explicit. Frozen comparison tests, actual localhost route-expression checks, exact syntax, source/privacy/manifest checks and secret scan pass. No live authority or target acceptance; exact command/scope below. |
| W-216 | Execute the approved W-215 backend comparison once. | W-213/W-215; W-147 | Resolved | Retain actual outcome and independent restoration evidence; consume approval without replay. | Failed before observation or comparison requests at backend_not_quiescent. Exact native restoration, timer disarm, primary stop latch/client cleanup and final boot continuity passed. Parent exit 1; terminal evidence rejected because observation never started. Sealed inputs unchanged. |
| W-217 | Quiescence rejection omits observations and terminal analysis assumes observation started. | W-147; W-214/W-216; AC-013 | Open | Reconcile the conservative gate against retained owner behavior; qualify bounded expected/observed process/socket reporting and explicit not-started evidence classification before any successor. Do not weaken quiescence or infer host load from the bare code. | Gate failed after 10.645403 seconds with backend_not_quiescent; no sampled counts/PID identities/socket states were persisted. Observer and all comparison phases were skipped. Later terminal FileNotFoundError is an evidence-path rejection, separate from successful restoration. No live retry or inspection authorized. |
| W-218 | Audit the diagnostic approach after repeated non-diagnostic failures. | W-147/W-217; AC-013 | Resolved | Separate application observations from tooling defects; identify concrete unsupported gates, missing evidence and a materially simpler next measurement. | Existing singleton gate rejects both a stable two-process idle state and that state's later settling to one process. Native 2.670 miniserv supports persistent log-clearing/authentication children. Original current-host process state was not retained, so exact W-216 trigger is unknown. Recommend bounded existing-loopback request measurement with CPU/throttling/process-wait evidence, no Caddy/ingress/restart. No new operation defined or approved. |
| W-219 | Propose durable evidence-first/minimal-test instructions. | Workspace harness; W-218 | Resolved | Provide a concise addition to the existing fixture rule, without creating another workflow or weakening safety boundaries. | Approved and installed November 17 in workspace AGENTS.md; exact proposal preserved below. |
| W-220 | Prepare a bounded Pi loopback measurement using the existing diagnostic. | W-218; W-147; AC-013 | Resolved | Bind one host, fixed requests, CPU/throttling/wait evidence, stop/cleanup, exact source and local correctness checks for separate live review. | Existing diagnose-http.py extended; six-input candidate sealed below, not authorized. Native curl/local control checks pass. No deployment playbook or target configuration change. Local tests use an ordinary HTTP endpoint solely for measurement/control correctness. |
| W-221 | Execute approved Pi-only loopback measurement. | W-220; W-147 | Resolved | Preserve request/resource evidence, client cleanup and terminal disposition from the one attempt. | Single request HTTP 200 in 2.34s; three concurrent requests timed out at 5s. CPU throttling increased; no memory high/max/OOM events. Clients reaped, final activity settled, no service changes. Exit 1 is the recorded HTTP outcome, not a missing measurement. |
| W-222 | Review backend concurrency and CPU policy using actual loopback evidence. | W-147; AC-013; Webmin/host owners | Resolved | Select a justified corrective design or single-factor comparison under owner review; do not assume historical causation or silently alter limits. | The backend alone reproduces delay under concurrent requests. One-CPU quota and 88 throttled periods out of 91 during overlap/settling support CPU contention; no CPU-policy intervention was performed. Serial/less costly health requests and quota policy require review, not automatic deployment. |
| W-223 | Prepare the approved temporary 200% CPU comparison. | W-222; W-147; Webmin/foundation owners | Resolved | Reuse measurement, bind native lifetime/recovery, preserve original runtime override, qualify changed boundaries and seal for live review. | Nine-input candidate below. Four control/file tests and existing one/two-CPU measurement branches pass. Aaron approved preparation only. Native transient execution and restoration remain target checks. No live authority or permanent CPU-policy change. |
| W-224 | Execute the approved temporary CPU comparison and verify restoration. | W-223; W-147 | Resolved | Retain actual request/resource receipts and independent restoration/cleanup from one attempt. | Exit 0. Single HTTP 200 in 2.327s; three concurrent HTTP 200 in 3.832-3.853s. No new memory high/max/OOM events. Original 100% quota/runtime override and unchanged main/unit identities verified; temporary files removed. Approval consumed. |
| W-225 | Select host-specific CPU policy and compatible health contract for browser onboarding. | W-147; AC-013; Webmin/foundation/Caddy owners | Resolved | Explicit owner approval of policy before implementation. | Aaron approved local implementation/preparation: selected Pi 200%, explicit unauthenticated health headers and 5s health timeout; memory controls and foreground deadline unchanged. W-226 tracks implementation; deployment and sustained browser capacity are not accepted. |
| W-226 | Implement selected-host CPU and explicit health policy in existing owners. | W-225; AC-013 | Resolved | Host-scoped selection, default preservation, native restore and adapted health contract locally checked. | CPU-only drop-in is explicitly selected in existing backend trial/recovery; 20 recovery tests pass. Offline Caddy 2.11.4 adaptation verifies proposed headers/thresholds. Production is 2.11.9; exact final owner candidate still requires its normal validation and paired/dual-stack/browser acceptance. No live authority. |
| W-227 | Bind the paired/dual-stack browser candidate after W-225. | AC-013; W-226 | In progress | Exact owner/parent bindings and relevant qualification before a live review. | Fresh private draft selects the Pi CPU profile, four backend paths, six browser paths and existing observer/recovery. No executable seal or authority. Exact paired owner/parent qualification now passes: 19 whole-path cases, nine evidence rejections and actual authorization gate. Private definition and inputs are bound; final seal/launcher and separate live review remain. |
| W-228 | Isolated-validator delivery is restricted to the earlier primary/IPv4 diagnostic. | W-191; W-227; Caddy owner | Resolved | Reconcile primary tool delivery with paired browser activation and pre-release-ID recovery in the existing owner path; retain secondary replication and unchanged installed secondary callers. | Primary-only tool delivery now accepts the paired recipe. Explicit empty-ID recovery restores A tools and cleans both payloads; post-ID recovery retains B-before-A restoration and monitor checks. Eighteen file/payload/recovery cases, focused paired dispatch checks and the host onboarding profile pass. Exact candidate qualification and writable target execution remain outside this local result; see checkpoint below. |
| W-229 | Paired whole-path qualification omitted primary validation-tool delivery and seeded the secondary with the source finalizer. | W-227; W-228 | Resolved | Exercise the exact paired recipe option with hash-verified accepted secondary tools and independently verify restoration in existing owner cases. | Existing paired cases now select primary delivery, accepted finalizer/reconciler bytes and secondary preservation. All 19 current cases and exact authorization pass; no capacity or namespace qualification is added. |
| W-230 | Private test-wrapper umask removed the deliberately public directory mode from the parent admission test. | W-227; controller evidence privacy | Resolved | Set the intended test mode explicitly and rerun only the admission test; preserve the failed run. | Existing paired and primary parent-flow tests passed. Public-mode case created 0700 under umask 077, so it never tested public input. Test setup now applies chmod; the admission-only rerun passed all six directory cases. Production admission is unchanged; failed receipt retained. |
| W-231 | Publish all accumulated server and monitoring changes at Aaron's request. | Source publication only | In progress | Required hooks pass; both commits pushed and remote refs verified. | November 17: both Racerx323 destinations and visibility verified; 31 server paths and three monitoring records selected. Private evidence and unsealed candidate remain outside Git. |

### Current preparation

- Owning repository/file store: `/home/aaron/code/homelab-monitoring-observability`.
- Consumed operation is `uptime-kuma-initial-deployment-20261109`; preserve its exact frozen definition. Historical preparation instruction: amend its then-unexecuted
  definition in place. No second active operation or parallel change record.
- Current approval state: **Both installation bundles consumed; diagnostic qualified but not approved or consumed.**
- Replacement candidate is qualified and recorded below. The November 9 archive
  remains withdrawn and must not be executed.
- November 10 user changes: move application ownership, require fleet-managed
  needrestart/Webmin/msmtp/watchdog and shared Apprise API/Mailrise, and make
  Mailrise the msmtp default. PLAN AC-011/012 bind these requirements.
- The coordinator requires locally qualified foundation inputs and a complete
  frozen input graph before contacting targets. Qualification is now complete;
  that status supplies no live authority.
- Retain previously authorized bounded read-only scopes; this revision grants no
  service/package/firewall/boot mutation, notification send or publication.
- Reuse Ansible private-temp and readonly/local collision checks from the sibling
  server-configs checkout; use this repository's pinned shfmt flags. Bundle the
  exact helper and network-owner task inputs when sealing the replacement.

### Consumed foundation bundle

- State: **Approved; consumed; terminal failure (Ansible exit 2).** Qualification is local;
  this record does not claim installed services or actual ARM64 acceptance.
- Archive: `/home/aaron/code/.local-evidence/uptime-kuma/foundation-prepare-20261110-bcvgim9k/candidate/uptime-kuma-foundation.tar`.
- SHA-256: `a3cc3fa6f6574e9aebf54505d690529c91987d64c6cfa75fea68be7b9595ed2b`.
- Size: 246,507,520 bytes; 106 non-secret declared input files.
- INPUTS.sha256 identity: `9c23399c8837a29d04e6494479def9723a25f2eabdd3eb2c71eb66d294eda7f7`.
- Frozen execution root: `/home/aaron/code/.local-evidence/uptime-kuma/foundation-prepare-20261110-bcvgim9k/candidate/bundle`.
- Includes the plan snapshot, complete application/controller definitions,
  component-owner tasks/profiles/helpers, public known-host entries, boot inputs,
  29 pinned packages and pinned ARM64 OCI archive. SSH identities remain external;
  no private keys, operator passwords or Mailgun/Apprise secrets are included.
- `frozen-qualification/status.json` verifies the exact frozen coordinator against
  localhost only and executes its real boot-input stat/assert tasks successfully.
  Archive and input-manifest identities were independently rechecked afterward.

Execute with an interactive PTY outside the controller filesystem sandbox, in the
frozen `repositories/homelab-monitoring-observability` working directory. Preserve
this exact command; no target-limiting override or mutable checkout substitution.

```sh
env ANSIBLE_CONFIG=/home/aaron/code/.local-evidence/uptime-kuma/foundation-prepare-20261110-bcvgim9k/candidate/bundle/ansible.cfg \
  ANSIBLE_LOG_PATH=/home/aaron/code/.local-evidence/uptime-kuma/foundation-prepare-20261110-bcvgim9k/execution/ansible.log \
  ANSIBLE_NOCOLOR=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  /bin/bash /home/aaron/code/.local-evidence/uptime-kuma/foundation-prepare-20261110-bcvgim9k/candidate/bundle/repositories/homelab-server-configs/tests/repository/run-with-ansible-local-temp.sh \
  /home/aaron/.local/bin/ansible-playbook \
  -i /home/aaron/code/.local-evidence/uptime-kuma/foundation-prepare-20261110-bcvgim9k/candidate/bundle/repositories/homelab-monitoring-observability/uptime-kuma/ansible/inventory.yaml \
  /home/aaron/code/.local-evidence/uptime-kuma/foundation-prepare-20261110-bcvgim9k/candidate/bundle/repositories/homelab-monitoring-observability/uptime-kuma/ansible/initial-deployment.yaml
```

Approval requested for this one Pi operation:

- Mutate `ama@10.1.3.75` only. Existing `pi@10.1.0.53` and `pi@10.1.0.54`
  are used only for bounded backend HTTP/source observations; no proxy mutation.
- Perform identity/state/resource preflight, preserve exact boot data, enable the
  memory controller and reboot. Apply the owner checkpoint-protected permanent
  ULA while preserving existing automatic addressing, routes and radio blocks.
- Transfer/install only the 29 pinned packages and ARM64 archive; deploy owned
  configuration and ingress guard. Adopt the unchanged existing vendor systemd
  watchdog; do not install another daemon or perform a reset/expiry test.
- Configure Webmin on loopback with explicit existing ama authentication and
  msmtp with the fleet Mailrise default. Keep temporary package-start denial until
  successful package/configuration checks; suppress install-time messages through
  the scoped native APT hook profile. Webmin's ordinary repository metadata
  checks may use outgoing network access; no unreviewed package upgrade is allowed.
- Install Kuma with the final resource bounds and loopback-only bootstrap.
  A second planned reboot verifies startup of the combined foundation.
- Pause for Aaron to verify Webmin login through its SSH tunnel and create/verify
  Kuma's first administrator privately. No password/cookie in chat or controller
  input; reply only `ready` after both checks. Do not expose an unclaimed setup.
- Back up stopped application data on/off-node, qualify real isolated restore,
  verify source recovery and administrator persistence, then promote the guarded
  dual-stack backend. Require actual cgroups, sockets, both proxy paths, denied
  direct clients/counters, preserved management/network/radios and healthy services.
- Enable the bounded daily needrestart schedule only after combined acceptance:
  05:30 America/Chicago, normal operational notifications through shared Mailrise/
  Apprise. Existing timezone is preserved and checked. No synthetic email/alert.
- Controller operational backup destination remains
  `/home/aaron/.local/state/uptime-kuma/backups/initial-20261109`, protected with
  0700 directories and 0600 secret-bearing archives, outside Git/evidence logs.

Two planned reboots can interrupt SSH. Reachable boot recovery can require an
additional reboot. Save original bytes on/off-node; if the Pi fails to return,
stop for the confirmed physical microSD/KVM recovery path. Do not infer recovery
from SSH loss. Address recovery uses its native checkpoint and independent readback.

On foundation/runtime failure, contain Webmin through the persistent guard/permit
and verified listener shutdown, remove the owned schedule and request application
stops while keeping the guard/data. Packages, image and configuration can remain;
a partial install can retain temporary policy-rc.d. Review exact residue before
recovery. Accepted prerequisites may remain. Failed backend promotion restores
and checks loopback operation. This is not whole-host rollback, and a consumed
operation is never replayed for a cleaner receipt.

Live ARM64 capacity/enforcement, actual kernel reporting, real operator logins and
administrator-bearing restore remain acceptance requirements. Hardware watchdog
expiry and downstream notification receipt are not established by local tests.
DNS/Caddy deployment, failover, Uptime Kuma monitors/alerts, synthetic messages,
unrelated maintenance and publication remain outside this approval. Final trusted
HTTPS/application/WebSocket acceptance (AC-004) is still required for the project.

### Withdrawn historical candidate

The November 9 candidate was locally qualified but **never approved or executed**.
It was withdrawn November 10 because its ownership and required foundation scope
are obsolete. Its archive stays immutable at
`/home/aaron/code/.local-evidence/uptime-kuma/initial-deployment-20261109-9jtrff4m/pi-candidate/uptime-kuma-pi-foundation.tar`,
SHA-256 `cac60c5781637d4c7883cc9fb8a00ab6ba60653cd5cf6d740f27e7d17f24994a`.
The external candidate descriptor is marked withdrawn; archived source and plan
snapshots retain historical paths/provenance. The previous command is withdrawn,
not rewritten to imply the old bundle implements the new scope.

Earlier read-only host/DNS/Caddy baselines and local runtime/restore/packet/native
parser results remain private evidence. They qualify only their recorded inputs;
they do not qualify the expanded combined workload or establish any live state.
The new candidate must re-evaluate package side effects, memory/storage budget,
Webmin management access, watchdog activation/recovery and needrestart/mail routing.
Reboot count, exact changes, acceptance, restoration/residue, administrative pause
and later DNS/Caddy scope must be explicit before replacement approval.

### Earlier local qualification

All paths below are relative to the private evidence root at the top of this ledger.

- `focused-final-status.json`: exit 0; 13 regressions, native Ansible syntax,
  shell formatting/static policy and repository readonly/local collision checks.
- `precommit-final-status.json`, `network-precommit-status.json`: exit 0;
  targeted repository policy and secret scanning. Initial YAML failure retained.
- `native-render-12yn_4bq`: actual Ansible templates/facts/filters and real APT
  output parsing; both generated service modes pass native Quadlet/systemd checks.
- `packet-y9e7vocf/status.json`: final rendered guard passes actual dual-stack
  DNAT/forward packet tests and production deny-counter parsing in local namespaces.
- `restore-final-khncnm5o/restore-cnpz4fqz/receipt.json`: final real restore
  checker passes on AMD64 data, with immutable configuration ID and cleanup proof.
- `runtime-smoke-pxk7g5w0/result.json`: AMD64 nonroot/read-only application,
  startup/restart/persistence and real database archive/restore proof.
- `native-config-gwfqkdh5`: native Unbound candidate check and Caddy adaptation
  pass without target staging, certificate provisioning or live acceptance.
- `pi-candidate/controller-localhost-qualification-status.json`: exit 0;
  actual frozen coordinator verifies all declared inputs and private evidence
  directory against explicit localhost only. First inventory-selection failure retained.
- vexp completion helper was unavailable from the parent workspace (`not a git
  repository`); it supplies no success evidence. Focused repository checks above
  provide validation. No target mutation or publication has occurred.

### November 10 relocation and scope checks

Private receipts: `/home/aaron/code/.local-evidence/uptime-kuma/ownership-foundation-20261110-2ulvcapd/`.

- Focused checker passed from the new repository: 13 regressions, native Ansible
  syntax, ShellCheck/shfmt and readonly/local collision policy. Existing sibling
  Ansible helper and network task resolve without copying their implementations.
- All 26 local Markdown references checked before the final ledger update exist;
  no active old application-owner path remains. Frozen historical evidence stays
  at its original location and is explicitly withdrawn from execution.
- Native localhost-only coordinator test stops at the pending-foundation gate,
  before input verification or any target play. Expected rejection passed; this
  is a containment check, not successful deployment qualification.
- Server inventory and mail-owner targeted hooks passed. Monitoring's first run
  found one unquoted email in the ledger; corrected. Alias-file whitespace from
  the edited original was also normalized. Final affected hooks passed for both
  repositories; intended-source secret scan exited 0, including the moved
  component, change record, mail-owner sources and host selection.
- Full monitoring working-tree secret scan found only the diagnosed generated
  source digest (W-042); staged-hook scans passed. No new secret was exposed.
- vexp verification remains unavailable at the parent workspace (`not a git
  repository`); it provides no success evidence. No live mutation, mail send,
  commit or push occurred.

### Expanded foundation qualification, November 10

Private receipts: `/home/aaron/code/.local-evidence/uptime-kuma/foundation-prepare-20261110-bcvgim9k/`.

- `inspection-status.json`, `followup-status.json`: read-only Pi collection exits 0;
  original vendor files, passive watchdog ownership and package baseline retained.
  `account-status.json` contains only the non-secret ama password-status flag.
  Earlier time baseline already confirms America/Chicago; no timezone change needed.
- `package-manifest.json`: all 29 official package blobs verified against exact
  recorded size/hash; Webmin asset identity reuses the NTP-reviewed 2.670 record.
  `apt-qualification/corrected-status.json`: native APT with the real ARM64 dpkg
  snapshot resolves exactly 29 new packages, zero upgrades/removals, entirely local.
- `native-listchanges/status.json`: actual target ALCConfig reads the scoped profile,
  with frontend none and email_address None. No global host configuration changed.
- `native-render/context-corrected-status.json`: actual package-closure assertion
  and native guard/cron producers pass. `complete-graph-status.json` verifies both
  current Quadlet modes with their real firewall dependency. Prior failures retained.
- `native-image/package-network-status.json`: actual Webmin package systemd producer,
  first-start guard, explicit synthetic login/dashboard, 192 MiB cap, msmtp default
  parser, bounded 96 MiB process scan and stop containment pass. Owned container
  removed. AMD64 fixture only; kernel checking is skipped inside the container and
  must pass the real Pi batch-report acceptance. No operator credentials or alerts.
- `320m-smoke-status.json` and `runtime-smoke-sbll2fxm/result.json`: real Kuma 2.5.9
  nonroot/read-only startup, restart, persistence and restored data pass at 320 MiB.
  `64m-client-status.json`: actual transient Node probe program runs under 64 MiB
  against unreachable documentation addresses; this is not target guard acceptance.
- The steady combined caps are 608 MiB (Kuma 320, Webmin 192, daily scan 96);
  preflight requires 704 MiB available to retain 96 MiB reserve. Observed available
  memory was about 741 MiB. Restore stops the source; the transient ingress client
  uses 64 MiB before the daily schedule is installed. Actual ARM64 enforcement,
  peaks and combined healthy operation remain required live checks.
- Existing native forwarding/firewall-counter qualification is retained: guard and
  counter-parser code are unchanged; only transient client memory was reduced and
  separately qualified. Source-restricted backend acceptance remains live work.
- Final affected hooks and intended-source secret scan exit 0; relative source
  links exist. New helper has five boundary regressions; focused Kuma checks have
  13 regressions plus native syntax and shell/collision policy. No commit or push.

Final frozen verification: both localhost checks exit 0 and archive/manifest hashes
remain unchanged. Full working-tree Gitleaks scan reports only the already diagnosed
`.vexp/manifest.json:16` generated source-file digest; intended-source scan exits 0.
The completion helper remains unavailable from the parent workspace and provides
no verification success. No live operation has started.

Approval received November 10, 2026: Aaron approved the exact-bundle request in
chat. Scope and command are the qualified replacement above. Archive, manifest
and every declared file were independently verified immediately before launch.

### Approved operation execution

- Started UTC: 2026-11-10T17:20:32.838595+00:00; live PTY session `65301`.
- Command: exact frozen `env` / repository Ansible helper / initial-deployment playbook recorded above; no overrides.
- Input revision: archive `a3cc3fa6f6574e9aebf54505d690529c91987d64c6cfa75fea68be7b9595ed2b`; all 106 declared inputs verified before launch.
- Native private log: `/home/aaron/code/.local-evidence/uptime-kuma/foundation-prepare-20261110-bcvgim9k/execution/ansible.log`.
- Log unread offset: 0; next checkpoint: native progress or first failure/operator pause.
- Terminal result: Ansible exit 2 at 2026-11-10 11:25:54 America/Chicago (17:25:54 UTC); session 65301 completed and retired. Do not relaunch this consumed operation.
- Native log fully retained (119578 bytes at completion); diagnostic review covers all task boundaries and failure/containment records.
- Accepted before failure: memory-controller prerequisite after first reboot; permanent ULA after fresh SSH, DAD, address and routing checks.
- Failed task: `Simulate the actual transferred local packages without downloading`, APT rc 100, `Unable to fetch some archives`. This was simulation, before foundation preparation or any package-install task.
- Completed containment: no notification schedule, Webmin stop/disable request, no Webmin TCP listener, application/network stop requests. Independent residue inspection follows.
- Not reached: package installation, foundation configuration, image import, application startup, second reboot, operator account checks, backup/restore, backend promotion or scheduled notifications.

- Read-only diagnosis: sessions `73702` and `9363` completed (exit 0) and retired; private `residue-inspection.log` and `isolated-sources-simulation.log` retain complete observations. No target changes were made by those simulations.
- Local qualification sessions `42963`, `4417`, `18357` and `50726` completed and retired. Session 42963 outer process exited 0 but native APT exited 100; retain its failed receipt. Session 4417 focused tests passed; local fixture outcomes are recorded separately, never as target installation acceptance.

- Correction qualification: `execution/apt-correction-status.json` records exact 29-pin ARM64 simulation and unchanged package database; `offline-sources-native-status.json` records successful actual network-disabled AMD64 installation/missing-dependency rejection. Neither is target installation acceptance.
- Local fixture sessions 18357 (cached-archive alternative) and 50726 (source-isolated correction) native exit 0. Chosen correction avoids extra target cache copies. Earlier local source-isolation-plus-`--no-download` failure is retained.
- Corrected target simulation completed without a live session; its full private log is mode 0600. Session 68851 completed and retired: YAML and Gitleaks passed, Markdown found one extra blank line, now corrected.

### Continuation preparation

- Private preparation root: `/home/aaron/code/.local-evidence/uptime-kuma/continuation-20261110-7o422m2f`.
- Terminal predecessor is archived in the prior preparation root under `terminal-archive/`: exact operation definition, input manifest, candidate descriptor and sanitized outcome/evidence hashes. The original tar and native evidence remain intact; their hashes were rechecked. No consumed source definition was removed from the repository; publication and any required tag remain outside this task.
- The continuation uses a small sealed extra-vars definition with native Ansible precedence. The existing coordinator conditionally replaces boot/address mutation with read-only platform, foundation, boot/radio and NetworkManager/address/route verification. The install, startup reboot, private login, backup/restore, backend and schedule path is reused.

- Source qualification: native local Ansible executed the actual coordinator imports with continuation mode and a local target group; all original prerequisite tasks skipped, with zero changes. Native read-only Pi preflight then passed platform/resources, unchanged package/foundation/watchdog baseline, exact accepted boot ID/file/controller/radios, active NM profile, persistent/live ULA and default routing with zero changes.
- Qualification sessions `63060` (syntax), `42611` (corrected local skip test) and `89330` (corrected read-only Pi preflight) completed, exit 0, and are retired. Earlier sandbox RPC failure, missing trust file, missing local group and split SSH-option fixtures were not acceptance; failed receipts are retained.

### Approved continuation

- Operation: `uptime-kuma-foundation-continuation-20261110`.
- State: **Approved; consumed; terminal failure (Ansible exit 2).**
- Archive: `/home/aaron/code/.local-evidence/uptime-kuma/continuation-20261110-7o422m2f/candidate/uptime-kuma-continuation.tar`.
- SHA-256: `deec2aeac744977fc8d4fbfd427c3e46aaf30dfbacd49f8e0dc3e713c4195324`.
- Size: 246,568,960 bytes; 109 declared non-secret input files.
- INPUTS.sha256 identity: `b142ac94ce77a1c62ee055e527eefe1e759a3f7c552accf75bf5574fde1ef091`.
- Qualification: `/home/aaron/code/.local-evidence/uptime-kuma/continuation-20261110-7o422m2f/qualification/qualification.json`.
- Frozen inputs include the plan snapshot, current application/coordinator,
  small continuation extra-vars definition, unchanged owner tasks/profiles/helpers,
  public host keys, the same 29 pinned packages/ARM64 image, and sanitized predecessor
  provenance. Original operation definitions and exact predecessor archive remain
  preserved; no old executable implementation is imported from private evidence.
- Native frozen checks: 7 controller and 21 read-only Pi checks passed with zero
  target changes. All 66 original prerequisite tasks skip in continuation mode.
  Missing overlay and mismatched mode fail at the controller before target contact.
  Native Ansible rendered the actual frozen APT expressions; a disposable
  network-disabled AMD64 container completed actual all-architecture package
  installation. Earlier ARM64 simulation matched all 29 exact pins with unchanged
  dpkg status; neither local test claims ARM64 package installation acceptance.
- Thirteen focused regression tests, Ansible syntax, shell format/ShellCheck and
  readonly/local collision checks passed. Working-tree secret scan passed. The
  parent-workspace vexp completion helper was unavailable (not a Git repository);
  repository checks provide the qualification evidence.
- Sessions `80604`, `70973`, `66966` and `79383` completed, exit 0, and are retired.
  No qualification sessions remain active. No live execution session exists.

Exact future command, with an interactive PTY outside the controller filesystem
sandbox, working directory `/home/aaron/code/.local-evidence/uptime-kuma/continuation-20261110-7o422m2f/candidate/bundle/repositories/homelab-monitoring-observability`:

```sh
env ANSIBLE_CONFIG=/home/aaron/code/.local-evidence/uptime-kuma/continuation-20261110-7o422m2f/candidate/bundle/ansible.cfg \
  ANSIBLE_LOG_PATH=/home/aaron/code/.local-evidence/uptime-kuma/continuation-20261110-7o422m2f/execution/ansible.log \
  ANSIBLE_NOCOLOR=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  /bin/bash /home/aaron/code/.local-evidence/uptime-kuma/continuation-20261110-7o422m2f/candidate/bundle/repositories/homelab-server-configs/tests/repository/run-with-ansible-local-temp.sh \
  /home/aaron/.local/bin/ansible-playbook \
  -i /home/aaron/code/.local-evidence/uptime-kuma/continuation-20261110-7o422m2f/candidate/bundle/repositories/homelab-monitoring-observability/uptime-kuma/ansible/inventory.yaml \
  /home/aaron/code/.local-evidence/uptime-kuma/continuation-20261110-7o422m2f/candidate/bundle/repositories/homelab-monitoring-observability/uptime-kuma/ansible/initial-deployment.yaml \
  --extra-vars @/home/aaron/code/.local-evidence/uptime-kuma/continuation-20261110-7o422m2f/candidate/bundle/repositories/homelab-monitoring-observability/uptime-kuma/operations/continuation.yaml
```

Authorization requested for this one bounded continuation:

- Mutate only `ama@10.1.3.75`. Use `pi@10.1.0.53` and `pi@10.1.0.54`
  solely for the existing bounded backend HTTP/source probes; no proxy mutation.
- Verify identity, resources, unchanged package/foundation/watchdog state, exact
  accepted boot ID/file/memory controller/radio blocks, persistent ULA and routing.
  Do not rewrite the boot file, create a network checkpoint, reapply addresses or
  repeat the prerequisite reboot. Any prerequisite drift stops the continuation.
- Verify/reuse or transfer the same hash-pinned offline payload; install exactly
  the 29 new packages with repository sources disabled and exact-closure readback.
  Configure owned needrestart/Webmin/msmtp settings, adopt the existing vendor
  systemd watchdog, import the pinned ARM64 image and install the contained Kuma
  runtime/ingress guard. Preserve the temporary package-start/message controls.
- Keep Webmin on dual-stack loopback with existing ama authentication, msmtp's
  default on shared Mailrise, and Kuma on loopback until its first administrator
  is claimed. One planned reboot verifies combined startup. Ordinary Webmin
  repository metadata checks may use outgoing access; no package upgrade allowed.
- Pause for private Webmin login and Kuma first-administrator logout/login checks
  through SSH tunnels. No password/cookie is entered in chat or controller input.
- Back up stopped administrator-bearing data on/off-node, qualify isolated restore,
  recover source service, then promote and verify the source-restricted dual-stack
  backend. Keep the same limits: Kuma 320 MiB, Webmin 192 MiB, bounded scans 96 MiB;
  verify actual cgroups, sockets, proxy reachability, denied clients/counters,
  resource reserve, kernel reporting, persistence and preserved management/radios.
- Enable needrestart at 05:30 America/Chicago only after combined acceptance;
  ordinary operational notifications use shared Mailrise/Apprise. No synthetic send.
- Keep the previously reviewed protected operational backup destinations
  `/var/backups/uptime-kuma/initial-20261109` and
  `/home/aaron/.local/state/uptime-kuma/backups/initial-20261109` (0700 directories,
  0600 administrator-bearing archives); refuse any prior backup collision.

Recovery remains bounded to the existing runtime/foundation containment: remove
only the owned schedule/first-start permit, stop/disable Webmin and independently
verify no listener, request Kuma/network stop, retain the ingress guard and data.
Packages, payload, image, configuration or a temporary policy-rc.d can remain after
partial failure; inspect their actual state before any further mutation. Failed
backend promotion restores and verifies loopback. Accepted boot/address changes
remain; no rollback or extra reboot for those prerequisites is authorized here.
If the single startup reboot does not return, stop for the confirmed physical
microSD/console-KVM recovery path. Never replay this continuation after consumption.

DNS/Caddy deployment/reload/failover, Kuma monitors/alerts, synthetic notification
tests, unrelated maintenance and repository publication remain unauthorized. Final
HTTPS acceptance is still required for the overall project. This request is required
by `homelab-server-configs/AGENTS.md`'s exact-bundle policy; the previous approval
covered different consumed inputs and does not authorize this continuation.

### Continuation authorization and execution

- Aaron approved the exact bundle and command linked at WORK.md line 343 on November 10, 2026. Approval binds archive `deec2aeac744977fc8d4fbfd427c3e46aaf30dfbacd49f8e0dc3e713c4195324` and the scope above.
- Prelaunch verification UTC: 2026-11-10T17:57:31.620580+00:00; archive, input manifest and every declared file match; execution directory unused.
- Live PTY session: `94515`; command is exactly the frozen env/helper/Ansible command above, including the sealed continuation extra-vars file.
- Input revision: `deec2aeac744977fc8d4fbfd427c3e46aaf30dfbacd49f8e0dc3e713c4195324`; approved operation consumed at launch.
- Private native log: `/home/aaron/code/.local-evidence/uptime-kuma/continuation-20261110-7o422m2f/execution/ansible.log`.
- Log unread offset 0; next checkpoint native progress/failure/operator pause. Terminal result: Ansible exit 2; session 94515 completed and retired. Do not relaunch.

- Execution checkpoint 2026-11-10T18:04:27.844123+00:00: frozen integrity and read-only accepted-prerequisite checks passed; original prerequisite tasks skipped. Exact local-file APT simulation passed. Webmin first-start guard, temporary policy-rc.d, list-only kernel policy and scoped package notification controls installed; offline package installation task in progress.
- Session `94515` remains active; native log reviewed through byte 118017; next checkpoint package-install return/version verification. No retry or competing operation launched.

- Terminal continuation checkpoint 2026-11-10T18:07:28.598766+00:00: offline installation and exact-version readback passed; owner mail/configuration and Webmin startup completed. Both loopback login-page GETs timed out after 30 seconds. Native rescue stopped/disabled Webmin, removed its permit and verified no TCP listener; no owned schedule existed. Temporary package-start control had already been verified and removed after configuration success. Actual residue inspection follows; no whole-host rollback is claimed.

- Independent read-only residue: `execution/webmin-residue.log` confirms all selected packages installed, Webmin disabled with no listener and no permit, policy-rc.d/schedule absent, Kuma unit/data/runtime paths absent and firewall empty. No kernel OOM entries; Webmin peak 173867008 bytes, no restarts. Unit exit-code failure is recorded at cleanup shutdown, not evidence of a prior spontaneous crash. No proxy environment variables were present.
- Local exact-URI reproduction session `49108` is active; command/inputs and private logs are under `qualification/webmin-exact-uri/status.json`. Frozen helper/profile and actual guard are mounted read-only. The synthetic fixture redirects SMTP to unreachable loopback before starting Webmin; no messages. Next checkpoint terminal qualification/cleanup.

- Final continuation outcome: private `terminal-archive/outcome.json` binds the consumed archive/input identities and hashes of the complete native log and independent residue receipts. Exact base operation/continuation definitions and candidate/input manifests are preserved. Original archive hash remains unchanged. No consumed repository definition was removed or published.
- Read-only follow-up confirms accepted IPv4/ULA/default routing, memory controller and radio softblocks remain; cron and NetworkManager are active. Hostname/localhost resolution completes in milliseconds. No proxy setting or kernel OOM event explains the timeout; prior service peak was 165.8 MiB, no restart/swap, within 192 MiB max. Cause remains unconfirmed; no blanket timeout/resource increase applied.
- Exact-URI local session `49108` completed and retired (launch/qualification/cleanup exit 0); disposable container removed. Both actual login-page paths and synthetic authenticated dashboard passed under the frozen guard/profile/helper; no messages or live changes. Read-only follow-up commands completed without persistent sessions.
- Native live session `94515` is terminal/retired, log fully retained/reviewed through 129417 bytes. No sessions remain active. No image import, Kuma deployment, startup reboot, operator login, backup/restore, backend promotion, scheduled notifications or DNS/Caddy changes occurred.

### Webmin diagnostic preparation

- Scope is one bounded start/observe/stop cycle under the existing Webmin settings and limits, with native disconnect containment and no authenticated requests or notification tests. It does not continue Kuma installation or change limits/timeouts in its acceptance path.
- Capture request timing, cgroup memory/CPU/I/O pressure/events and process states without command lines, environment, response bodies, cookies or credentials. Preserve both consumed bundles and their terminal archives.

- Diagnostic preparation uses private `/home/aaron/code/.local-evidence/uptime-kuma/webmin-diagnostic-20261110-m2m4zwre/`. Native lifecycle qualification session `43451` is active; complete stdout/stderr/native log and command are retained under `qualification/native/`. Local loopback regressions passed outside the sandbox; earlier sandbox socket denial was unavailable testing, not a code failure. Private qualification-only Podman connection collection 1.21.2 was installed under that preparation directory; no global tooling or target package changes.

- Native disposable qualification reached timer arm/start and proved stop/disable/no-listener/no-permit cleanup after the observer launch failed. Its base image lacked the D-Bus system socket required by `systemd-run --wait --pipe`; timer arming used the manager private socket and succeeded. The diagnostic now refuses a missing system socket before mutation. Complete the disposable fixture with native D-Bus and requalify; no target package dependency change is proposed. Session `43451` completed (native play exit 2), retired, failed receipt retained. Session `34086` read-only local bus diagnosis completed/retired.

- Native disconnect fallback passed in the disposable fixture with a two-second test deadline: after arming, no controller cleanup was performed; the native timer removed the permit and stopped/disabled Webmin, with no TCP/UDP listener. The production deadline remains 240 seconds. Session `69005` completed/retired (exit 0). `53523` completed/retired after local fixture D-Bus installation/start; no target package changes. Requalification session `78844` is active, using the actual playbook at production bounds and a fresh private fixture work/evidence path; failed receipts remain.

- The corrected native fixture added D-Bus successfully. A subsequent preflight correctly rejected its mounted guard mode 0600 before mutation; the fixture was corrected to production 0644 and full qualification session `92530` is running. No executable/source bypass or relaxed production precondition was used. Sessions `78844` and `62400` are terminal/retired.
- Full working-tree scans flagged only generated `.vexp/manifest.json` source-file SHA256 entries (16 server, 1 monitoring); the cache includes stale source hashes. Private `qualification/working-tree-secrets-classification.json` records that classification. The intended diagnostic source scan passed; no suppression or index change was made.

### Approved Webmin diagnostic

- Operation: `webmin-http-diagnostic-20261110`.
- State: **Consumed; diagnostic accepted; Webmin service unaccepted.**
- Archive: `/home/aaron/code/.local-evidence/uptime-kuma/webmin-diagnostic-20261110-m2m4zwre/candidate/webmin-http-diagnostic.tar`.
- SHA-256: `acb5903be2e86410ea99299b61be78900681498c16cceaffbabafc4199cb5119`.
- Size: 102,400 bytes; 16 declared non-secret input files.
- INPUTS.sha256 identity: `91e3a596e884b0334d298bd16b808b5baa432c3511573cda07659108927e2338`.
- Qualification: `/home/aaron/code/.local-evidence/uptime-kuma/webmin-diagnostic-20261110-m2m4zwre/qualification/qualification.json`.
- Owner: `homelab-server-configs/Webmin`; this remains the sole project ledger.
  Inputs include the native playbook, read-only stdlib observer, selected operation
  and existing profile, public host keys, Ansible helper/configuration, governing
  instructions/docs, plan snapshot and sanitized predecessor outcome. No application
  image/packages, private keys, credentials or archived executable are included.
- Four neutral tests passed, including real loopback success/timeout and exclusion
  of response data. The actual Ansible target path completed in a disposable
  systemd/D-Bus Podman fixture: 28 tasks, complete bounded timing/resource receipt,
  and independently verified stop/disable/no TCP or UDP listener/no permit. Slow
  and failed HTTP requests were retained; this is diagnostic qualification, not
  service acceptance. The observer used 11.8 MiB and emitted 230,097 bytes/97 samples.
- The local trace observed high-limit reclaim waits, 7,880 high events and one
  OOM kill within the Webmin cgroup. These are measured AMD64 findings; the Pi
  cause remains unconfirmed. No limit/timeout change is included.
  The native disconnect fallback also passed with a two-second test deadline and
  no controller cleanup after arming; production uses 240 seconds.
- Frozen controller and read-only Pi preflight passed: 5 localhost and 7 Pi tasks,
  zero target changes, package/architecture/stopped state, guard identity/mode,
  actual memory controller/reserve, absent listeners/permit/workdir/diagnostic units
  and a live system-bus socket verified. No target staging or service start occurred.
- Source policy/format checks and intended-source secret scan passed. Complete
  working-tree scans found only 17 generated vexp source-hash entries, classified
  privately; stale cache digests were not treated as credentials or authority.
  No suppression was added. The parent vexp completion helper was unavailable
  because its workspace is not a Git repository; focused native checks are retained.
- Earlier failed fixture receipts remain: sandbox socket denial, missing fixture
  system bus (with successful cleanup), and wrong mounted guard mode (zero-change
  preflight refusal). Source preconditions were retained. Private qualification
  transport uses containers.podman 1.21.2; production uses only Ansible built-ins.
- Sessions `92530` and `70040` completed, exit 0, and are retired. The disposable
  container was removed. Other qualification sessions are terminal/retired;
  no live or local qualification process remains active.

Exact executed command, outside the controller filesystem sandbox, working directory
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-diagnostic-20261110-m2m4zwre/candidate/bundle/repositories/homelab-server-configs`:

```sh
env ANSIBLE_CONFIG=/home/aaron/code/.local-evidence/uptime-kuma/webmin-diagnostic-20261110-m2m4zwre/candidate/bundle/ansible.cfg \
  ANSIBLE_LOG_PATH=/home/aaron/code/.local-evidence/uptime-kuma/webmin-diagnostic-20261110-m2m4zwre/execution/ansible.log \
  ANSIBLE_NOCOLOR=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  /bin/bash /home/aaron/code/.local-evidence/uptime-kuma/webmin-diagnostic-20261110-m2m4zwre/candidate/bundle/repositories/homelab-server-configs/tests/repository/run-with-ansible-local-temp.sh \
  /home/aaron/.local/bin/ansible-playbook \
  -i /home/aaron/code/.local-evidence/uptime-kuma/webmin-diagnostic-20261110-m2m4zwre/candidate/bundle/repositories/homelab-server-configs/Webmin/operations/http-diagnostic-inventory.yaml \
  /home/aaron/code/.local-evidence/uptime-kuma/webmin-diagnostic-20261110-m2m4zwre/candidate/bundle/repositories/homelab-server-configs/Webmin/ansible/diagnose-http.yaml
```

Authorized scope for this one diagnostic on `ama@10.1.3.75` only:

- Require the observed stopped/disabled/no-listener/no-permit baseline, Webmin
  2.670, unchanged exact guard/profile, memory control, at least 336 MiB available
  for the 192 MiB service + 48 MiB observer + 96 MiB reserve, system bus, and no
  existing diagnostic state. Do not run concurrent Webmin operations.
- Stage only the observer/profile under root-owned 0700
  `/var/lib/webmin-http-diagnostic`, with 0600 files. Verify existing managed
  Webmin settings without exposing unmanaged configuration. Do not rewrite them.
- Arm a native PID1 containment timer and independently verify its deadline before
  creating the temporary start permit. Make one explicit service-start request
  while retaining disabled boot startup and the existing native restart policy
  and 3-start/300-second guard. Leave MemoryHigh=128 MiB, MemoryMax=192 MiB, no
  swap, one CPU, KillMode=control-group and OOMPolicy=stop unchanged.
- Run a separate 48 MiB/no-swap/20%-CPU observer with a 190-second native runtime
  bound. For at most 180 seconds, sample cgroup memory/CPU/I/O pressure/events and
  up to 16 process states per second; output is capped at 512 KiB. Issue only
  unauthenticated loopback GETs: root at up to 5 seconds, then each family's actual
  login page at up to 75 seconds each. These are diagnostic measurement bounds;
  they do not relax the application's acceptance checks.
- Capture status, timing and non-secret resource/process metadata only. Never
  collect response bodies/cookies, credentials, process command lines or environments.
  Store observation/containment receipts in the private controller evidence directory
  (0700 directory, 0600 files). Webmin may write its ordinary logs/cache and perform
  its ordinary outgoing repository metadata checks while running.
- On completion or error, remove only the matching owned permit, stop/disable
  Webmin, and independently verify MainPID=0, disabled boot startup, no TCP/UDP
  listener on port 10000 and no permit. Only then cancel the independent fallback.
  A complete failed-request receipt plus proven containment is a successful
  diagnostic; it does not accept Webmin or resume Kuma.
- If the controller disconnects, the timer fires after 240 seconds to remove the
  permit and stop/disable Webmin through native ExecStopPost. Existing service
  shutdown has a 20-second bound; the fallback has a 30-second stop-post bound.
  If containment cannot be independently confirmed, leave fallback armed, record
  manual intervention and use the previously confirmed physical/console access.

The staged observer/profile and ordinary Webmin logs/cache may remain. No service
configuration/limit change, package action, reboot, authenticated login, synthetic
message, notification schedule, Kuma operation, DNS/Caddy/HA change, unrelated
maintenance or publication is included. Preserve the previous consumed bundles;
never replay this diagnostic after consumption.

This new service-start operation requires exact-bundle authorization under
`homelab-server-configs/AGENTS.md:70`; prior consumed approvals do not authorize it.

- Final qualification: all source policy checks passed; the exact frozen Pi preflight made zero changes. Native full lifecycle session `92530` passed, with actual failed-request/resource evidence and proven cleanup; session `70040` read-only preflight passed. Both are retired. The fixture removal command completed successfully. No qualification sessions or containers remain active, and the diagnostic execution directory is unused.

### Diagnostic authorization and execution

- Aaron approved the exact bundle and command linked at WORK.md line 471 on November 10, 2026. Archive `acb5903be2e86410ea99299b61be78900681498c16cceaffbabafc4199cb5119` and the bounded scope above are authorized once.
- Prelaunch UTC 2026-11-10T19:10:20.789875+00:00: archive, manifest and every declared input verified; execution directory unused.
- Launched the exact frozen command above once, outside the controller filesystem sandbox. Shell session `50841` completed with exit 0 and is retired; archive and manifest identities are unchanged. Private native log: `/home/aaron/code/.local-evidence/uptime-kuma/webmin-diagnostic-20261110-m2m4zwre/execution/ansible.log`. Controller/target preflight passed, native containment armed and independently checked, and one Webmin start reached the bounded observer. The full native log is retained; terminal evidence and consumption are recorded below. No replay is authorized.

### Diagnostic terminal outcome

- Exact approved command ran once; shell session `50841` completed with exit 0
  and is retired. Native recap: 28 Pi tasks (10 changed), five controller tasks,
  zero failed/unreachable. No diagnostic or qualification session remains active.
- Private terminal archive: `/home/aaron/code/.local-evidence/uptime-kuma/webmin-diagnostic-20261110-m2m4zwre/terminal-archive/`.
  It preserves the unchanged tar, input manifest, preterminal candidate descriptor
  and `outcome.json` with evidence hashes. Qualification remains a historical
  preauthorization receipt; mutable candidate state now records consumption.
- Observation: 124.42 seconds, 122 samples, none omitted. TCP ready in 1.013 s;
  root request timed out at 5.007 s, IPv4 login returned HTTP 200 in 43.31 s,
  IPv6 login timed out at 75.077 s. These do not pass service acceptance.
- Pi cgroup peak: 162,709,504 bytes (155.17 MiB). Memory-high events began at
  8.1 seconds and reached 9,902; hard-limit and OOM counters remained zero.
  In 111 samples, processes including miniserv, Webmin helpers and apt-get waited
  in `__mem_cgroup_handle_over_high`. The trace supports memory reclaim/throttling
  as a contributor to the stalls, without proving it is the only cause. Pressure
  stall information files were unavailable; no PSI measurements are claimed.
  The observer's native receipt reports 12.1 MiB peak and successful completion.
- Independent containment readback: MainPID=0, ActiveState=failed, boot startup
  disabled, no TCP or UDP listener on 10000, permit absent. Only after those
  checks did the play cancel its own fallback and verify it was no longer armed.
  Staged private observer/profile and ordinary Webmin logs/cache remain permitted
  residue. No service limit/configuration change or Kuma operation occurred.
- W-056 is resolved. W-055 remains in progress: the proposed correction must
  address measured startup pressure and qualify the combined budget, rather than
  treat longer diagnostic request bounds as service acceptance. No new live
  operation is defined or approved; both installation approvals and this
  diagnostic approval are consumed.

### Sealed Webmin correction and remaining-installation continuation

- Operation: `uptime-kuma-webmin-correction-20261110`.
- State: **Consumed; partial failure; independent residue verified and terminally archived.**
- Owner specification: `uptime-kuma/operations/webmin-correction.yaml`.
  The consumed `operations/continuation.yaml` and diagnostic definition remain
  unchanged. Their exact archives and terminal outcomes remain private and intact.
- Archive: `/home/aaron/code/.local-evidence/uptime-kuma/webmin-correction-20261110-zm7ga2ct/candidate/uptime-kuma-webmin-correction.tar`.
- SHA-256: `67616df300f19d695ee2761d889bd9a4e147a04580a6d83056d951ef12cd0b72`.
- Size: 246,528,000 bytes; 117 declared non-secret inputs.
- INPUTS.sha256 identity: `af3f30a2e54226f122a72b7e5849a62aac82a592255a764e538e1cf728cba7d7`.
- Qualification: `/home/aaron/code/.local-evidence/uptime-kuma/webmin-correction-20261110-zm7ga2ct/qualification/qualification.json`.
  The frozen file graph and archive were independently rechecked; execution storage
  is protected, empty and unused. No live target was contacted during preparation.

The correction uses the existing atomic owner helper for the supported Webmin
2.670 system-status setting `collect_pkgs=0`. It removes automatic dashboard
package-update collection and its update summary. It preserves collection interval,
temperature policy, APT/package maintenance, fleet notifications and the existing
128 MiB soft/192 MiB hard/no-swap Webmin limits. Manual package actions remain
separately reviewed maintenance. This is a locally qualified proposal; it is not
an accepted correction on the Pi.

Local qualification:

- First cold start under unchanged limits: root HTTP 200 in 2.162 s; IPv4/IPv6
  login HTTP 200 in 0.383/0.378 s. Peak 126.18 MiB, no memory-high/OOM events;
  no APT process appeared in the samples. This alone does not prove Pi behavior.
- Actual AMD64 Kuma 2.5.9, non-root with initialized SQLite, and native Webmin ran
  together in a shared 704 MiB/no-swap pod while a native 96 MiB needrestart scan
  completed. Both Webmin login pages and authenticated dashboards passed;
  authenticated requests took 0.362/0.299 s. Webmin peak 86.21 MiB; zero high,
  hard-limit or OOM events and zero restarts. Kuma peak about 159.25 MiB;
  shared-pod recorded peak about 457.82 MiB, including fixture setup activity.
  Kuma HTTP setup redirect and Socket.IO polling passed. The fixture uses a
  temporary filesystem; neither ARM64 performance, Pi microSD, hardware watchdog,
  real kernel reporting nor fleet SMTP reachability is accepted locally.
- Existing arithmetic is retained: 192 MiB Webmin + 320 MiB Kuma + 96 MiB scan
  and 96 MiB host reserve = 704 MiB required available before mutation. Actual
  target reserve, cgroup enforcement and combined service acceptance remain gates.
- Actual owner configuration/acceptance and native startup timer/release completed
  27 selected tasks, exit 0. Full hardware/kernel/SMTP foundation checks were
  explicitly excluded from that disposable run; production retains them.
  Exact frozen Webmin acceptance, including the actual cgroup OOM counter, passed.
  Failure containment passed with actual stopped/disabled state, no TCP/UDP
  listener and absent permit. Independent native fallback passed with no
  controller cleanup after arming, using a two-second local deadline; production
  remains 300 seconds. The actual production deadline was armed/checked in the
  native lifecycle test.
- Installed-foundation mode skipped all 62 selected initial package/configuration
  tasks through the actual coordinator: zero changes/failures. Frozen controller
  checks passed; changing installed-foundation mode was rejected before target
  tasks (expected exit 2). No check bypass enters the live command.
- All 51 Webmin tests and 13 focused Kuma regressions passed, along with Ansible
  parsing, relevant repository hooks and raw whitespace checks. vexp completion
  was unavailable because the parent workspace is not a Git repository.
- Working-tree scans: monitoring clean; server findings are 16 generated vexp
  source hashes. Full bundle has one classified public signing-keyring SHA256
  in `webmin-source-assets.json`; no credential finding or suppression. Private
  classification retains scan statuses and provenance.
- Failed local receipts remain: fixture namespace/mount/SQLite/readiness issues,
  YAML/import mistakes, transient-unit cancellation return status and sandbox
  denial of Ansible's local RPC socket. Corrected paths were exercised natively.
  None was a live target attempt. Qualification sessions are terminal; disposable
  fixture cleanup is recorded privately.

Exact proposed command, outside the controller filesystem sandbox with a terminal,
working directory
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-correction-20261110-zm7ga2ct/candidate/bundle/repositories/homelab-monitoring-observability`:

```sh
env ANSIBLE_CONFIG=/home/aaron/code/.local-evidence/uptime-kuma/webmin-correction-20261110-zm7ga2ct/candidate/bundle/ansible.cfg \
  ANSIBLE_LOG_PATH=/home/aaron/code/.local-evidence/uptime-kuma/webmin-correction-20261110-zm7ga2ct/execution/ansible.log \
  ANSIBLE_NOCOLOR=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  /bin/bash /home/aaron/code/.local-evidence/uptime-kuma/webmin-correction-20261110-zm7ga2ct/candidate/bundle/repositories/homelab-server-configs/tests/repository/run-with-ansible-local-temp.sh \
  /home/aaron/.local/bin/ansible-playbook \
  -i uptime-kuma/ansible/inventory.yaml \
  uptime-kuma/ansible/initial-deployment.yaml \
  --extra-vars @uptime-kuma/operations/webmin-correction.yaml
```

Authorization requested for this exact command and bundle, once:

- Mutating target: `ama@10.1.3.75` only. Read-only backend/source-route checks from
  the previously inspected Caddy nodes `pi@10.1.0.53` and `pi@10.1.0.54` are also
  included; no proxy/DNS configuration or role change is included.
- Preflight independently requires accepted boot ID/file, memory controller,
  radio softblocks, automatic networking/permanent ULA, all 29 package pins and
  clean package audit, original vendor watchdog/needrestart inputs, unchanged
  mail/needrestart/guard files, stopped/disabled Webmin, absent permit/package
  policy/schedule, absent Kuma state/listeners and the original empty firewall.
  Drift stops execution. No package action, first reboot, boot-file change or
  NetworkManager checkpoint/reapply is repeated.
- Apply only owner Webmin profiles, preserving unmanaged settings. Before service
  start, arm/check PID1's 300-second fallback to remove the permit and stop/disable
  Webmin. Verify both loopback login paths with the existing acceptance timeout,
  service/cgroup limits, real needrestart report (96 MiB/no swap/90-second bound),
  non-sending SMTP greeting/QUIT, timezone, watchdog owner and memory reserve.
  Only successful foundation acceptance releases the startup fallback.
- Verify the retained image's exact hash and protected regular-file identity
  before loading it. Continue the reviewed offline image/Quadlet/ingress-guard
  installation, actual loopback runtime acceptance and **one startup reboot**.
  Preserve automatic routing, management access and radio blocks throughout.
- Pause for Aaron's private Kuma administrator creation and Webmin login through
  SSH tunnels; no password/session belongs in chat, Git or logs. Then require
  actual claimed/authenticated Kuma state, stopped-data backup and protected
  controller copy, isolated restore with source stopped for the Pi budget,
  and recovered source availability. Promote only to the reviewed proxy source
  addresses and verify actual dual-stack allowed/denied traffic and counters.
- Recheck the combined foundation after boot/promotion. Enable the existing
  05:30 America/Chicago needrestart schedule only at final combined acceptance.
  This enables normal fleet Mailrise notifications; it does not send a synthetic
  message or enable Kuma monitors/alerts. Apprise API/Mailrise servers are reused.
- On startup/bootstrap failure, remove the owned schedule/permit, stop and disable
  Webmin and independently verify unit, TCP/UDP and permit state before cancelling
  an owned startup fallback. Stop Kuma/network where present, retain the ingress
  guard and all evidence/configuration/package/data residue for review. No package
  removal or whole-host rollback. Promotion failure uses the existing verified
  loopback recovery path; an incomplete final schedule is removed.
- Controller loss during correction startup leaves the native fallback armed.
  Its service shutdown is bounded by the existing 20-second stop and 30-second
  fallback stop-post limits. After startup acceptance, ordinary installed service
  persistence is intended; a later interruption requires residue inspection and
  new review, never replay. Aaron's confirmed device/microSD/console KVM is the
  manual recovery path if the planned reboot does not return.

DNS deployment, Caddy release/reload/failover, HTTPS acceptance, Kuma monitor/alert
configuration, synthetic messages, unrelated maintenance and publication remain
outside this authorization. Final project HTTPS acceptance remains required.

Repository policy requires authorization for this new live stage:
[AGENTS.md](../../../homelab-server-configs/AGENTS.md:70) says,
“Require scoped authorization for every live stage” and requires one exact
SHA-256 bundle. Existing consumed approvals do not authorize this continuation.

### Correction continuation authorization and execution

- Aaron approved the exact bundle, command and scope linked at line 682 on November 10, 2026. Archive `67616df300f19d695ee2761d889bd9a4e147a04580a6d83056d951ef12cd0b72` is authorized once.
- Prelaunch UTC 2026-11-10T20:00:18.805664+00:00: archive, manifest and all 117 declared inputs verified; evidence directory was protected and unused.
- Exact frozen command launched once outside the controller filesystem sandbox with a terminal; shell session `24703` active. Native log: `/home/aaron/code/.local-evidence/uptime-kuma/webmin-correction-20261110-zm7ga2ct/execution/ansible.log`. Inputs remain the sealed revision; complete stdout/stderr/status retained by the native log and session. Next checkpoint: one blocking 30-second session poll; terminal result pending. No replay authorized.

- Correction checkpoint: actual Pi loopback HTTP checks, unchanged Webmin caps/cgroup and zero OOM kills, vendor watchdog, native list-only kernel report, non-sending SMTP greeting/QUIT, timezone and reserve passed. Independent timer release and positive running PID passed. Receipt: `webmin-correction-20261110-zm7ga2ct/execution/foundation-configured.json`. Session `24703` remains active at retained-image hash verification; native log checkpoint 100,763 bytes. No package/boot/address mutation repeated.

- Runtime checkpoint: retained image hash/import and guard/Quadlet installation passed. First Kuma readiness observation is still retrying within the sealed playbook bounds; no startup reboot or private administrator pause has been reached. Webmin correction passed its Pi foundation check before this phase. Session `24703` remains active; do not launch a competing operation.

- Terminal: shell session `24703` completed with Ansible exit 2 and is retired. The first runtime observer exhausted its sealed retry budget; no startup reboot or private operator setup was reached. Native rescue output retained in full; independent residue assessment pending.

### Correction continuation terminal outcome

- Session `24703` completed with exit 2 and is retired. No active execution
  sessions remain. Native recap: 109 Pi tasks passed, 26 changed, 138 skipped,
  one rescued failure; seven controller tasks passed. No second launch occurred.
- Preserved exact archive, operation snapshot, manifest and outcome:
  `/home/aaron/code/.local-evidence/uptime-kuma/webmin-correction-20261110-zm7ga2ct/terminal-archive/`.
  `outcome.json` binds native logs, authorization and independent residue/data
  receipts by SHA256. The archive/manifest identities above remain unchanged.
- Pi Webmin correction first-start acceptance passed: both loopback login paths,
  unchanged 128/192 MiB/no-swap limits, zero OOM/high events and restarts, peak
  83,718,144 bytes (79.84 MiB). Vendor watchdog, list-only kernel report, non-sending
  Mailrise connectivity, timezone and host reserve passed. Startup fallback was
  independently released with a positive Webmin PID. W-055 is resolved for this
  initial correction; later reboot/operator acceptance remains required.
- Exact ARM64 image import, native nftables guard and Quadlet startup completed.
  Kuma's observer exhausted its bounded retry budget with TCP connect timeout at
  the loopback HTTP phase. It did not emit complete JSON or identify the failed
  family. No diagnosis of firewall, IPv6 or application failure is established.
- Native rescue removed the permit/schedule, stopped/disabled Webmin, verified its
  TCP/UDP/unit/permit containment, then requested Kuma/network stop. Independent
  SSH readback confirmed MainPID=0 and stopped application/network, Webmin disabled,
  no containers and no 3001/10000 TCP/UDP listeners. The guard remains enabled/active;
  Netavark base rules and the empty network definition remain. Deny counters in
  the owned guard were zero at readback; that alone does not diagnose the timeout.
- Kuma unit recorded peak 224,903,168 bytes (214.4 MiB), zero restarts and successful
  intentional stop. Current cgroup counters no longer exist after stop; no claim
  of complete runtime pressure coverage is made. The image's ARM64/configuration
  identity is independently verified. Stopped SQLite quick_check is OK, with zero
  users, monitors and notifications; no credentials or application rows collected.
- Original boot ID is unchanged: no new reboot, private administrator setup,
  administrator-bearing backup/restore, backend promotion or notification schedule
  occurred. No DNS/Caddy change or publication occurred.
- Image, empty application data, source definitions, persistent guard and network
  metadata remain. Generated WantedBy startup definitions can start Kuma on a
  future reboot; no masking/removal or extra stop/start beyond approved recovery
  was performed. Preserve this residue when qualifying the next diagnostic.
- W-059 owns the remaining failure. No new live operation is defined or approved.
  Actual final HTTPS and all untested project acceptance criteria remain pending;
  this is a partial deployment outcome, not project completion.

### Sealed Kuma network diagnostic, November 10

Preparation is complete; this operation is **not approved or consumed**. No live
host was contacted during this preparation. The earlier correction remains
consumed, including its failed Kuma observation and verified stopped residue.
W-059 remains open: neither the original failing address family nor Pi cause is
established. Existing Pi startup definitions remain capable of starting Kuma on
a later reboot until this proposed guard is actually installed; no reboot or
start is currently authorized.

The owner-native implementation is
[diagnose-network.yaml](../../uptime-kuma/ansible/diagnose-network.yaml), using
[the operation definition](../../uptime-kuma/operations/network-diagnostic.yaml)
and [bounded collector](../../uptime-kuma/scripts/diagnose-network.py).
[OPERATIONS.md](../../uptime-kuma/docs/OPERATIONS.md) owns the repeatable procedure;
this record owns the specific candidate and approval boundary.

Private candidate root:
`/home/aaron/code/.local-evidence/uptime-kuma/kuma-network-diagnostic-20261110-385lrsk0`.

- Archive: `candidate/kuma-network-diagnostic.tar`, **143,360 bytes**, 23 input files.
- Archive SHA-256: `5985aed9c563e14f97d9a9a7c380b3fc63414e51c6583af530abbd70a17e474f`.
- `INPUTS.sha256` SHA-256: `dbcec69294644ac93509b6aba482301392155b3c3e1cda39abd338c26fb75cd9`.
- Frozen execution root: `candidate/bundle`; source definitions, public host keys,
  expected installed identities, predecessor provenance and plan snapshot are bound.
  No image import, package payload, private key or credential is included.
- Protected future execution evidence: `execution/`, currently unused, mode 0700.
- Qualification: `qualification/qualification.json`, `sealed-native-stdout.log`,
  `sealed-native.log`, `sealed-evidence/`, fallback proofs and `restart-guard-proof.json`.

Local qualification used a disposable Debian 13 AMD64 systemd fixture with native
Podman 5.4.2, Netavark 1.14.0-2 and the corresponding actual AMD64 Kuma image.
The final frozen play passed all controller and target tasks: localhost 5 ok,
fixture 38 ok/17 changed, zero failed/unreachable/rescued. Its explicit fixture
profile substituted only fixture identity, image, network, paths and absent
Webmin qualification; the sealed production profile remains ARM64/Pi-specific.
The fixture has nested VFS storage, no external network and no aardvark-dns.
This is not ARM64, microSD, host DNS, Pi capacity or production acceptance.

The final receipt retained 12 path/family measurements, two network/log snapshots
and 90 one-second resource samples over 90 seconds. In both rounds, container
loopback and host-to-container HTTP returned 302 over both families; published
IPv4 loopback returned 302, while published IPv6 loopback timed out at four seconds.
This demonstrates partial-failure evidence retention, not the Pi failure family.
Fixture application memory peak was 270,266,368 bytes (257.75 MiB), with 4,348
memory-high events and zero max/OOM/OOM-kill events. Observer peak was 39.6 MiB.
The actual Pi must supply its own evidence; no increased application limit or
claim of combined resource acceptance follows from this diagnostic.

Normal cleanup independently proved absent permit, listeners and containers,
both generated units stopped with MainPID 0, persistent guards intact, original
application/network timing restored and database quick_check=ok with zero users,
monitors and notifications. A wrong installed-source checksum refused before
mutation. The real 300-second fallback removed its permit after controller
cleanup had already stopped the service; a separate two-second accelerated test
of the same native fallback stopped an actively running application without
controller cleanup. These are distinct proofs, not a claim that the full-deadline
test began with an active service. Restarting the fixture with tmpfs /run cleared
then proved both generated units skipped (ConditionResult=no), inactive/MainPID 0,
no containers/listeners and multi-user.target active. The disposable fixture was
removed after proof retention. Failed local receipts, including permit/register
collision and generated-fragment corrections, remain preserved; no failed
candidate is authorized for replay.

Twenty focused regressions, native syntax checks, shell formatting/ShellCheck,
readonly/local collision checks and focused source hooks passed. Secret scanning
is recorded in the private qualification evidence: the bundle scanner's sole
finding is a verified predecessor authorization-receipt SHA-256, not a credential;
no suppression was added. The vexp completion helper was unavailable from the
parent workspace, so its result is not counted as validation.

#### Exact command and requested live scope

Authorization is requested for **one execution** of this exact bundle and command,
including its strict preflight, bounded observation and containment. Run from:

```text
/home/aaron/code/.local-evidence/uptime-kuma/kuma-network-diagnostic-20261110-385lrsk0/candidate/bundle/repositories/homelab-monitoring-observability
```

```bash
env \
  ANSIBLE_CONFIG=/home/aaron/code/.local-evidence/uptime-kuma/kuma-network-diagnostic-20261110-385lrsk0/candidate/bundle/ansible.cfg \
  ANSIBLE_LOG_PATH=/home/aaron/code/.local-evidence/uptime-kuma/kuma-network-diagnostic-20261110-385lrsk0/execution/ansible.log \
  ANSIBLE_NOCOLOR=1 PYTHONDONTWRITEBYTECODE=1 \
  /bin/bash /home/aaron/code/.local-evidence/uptime-kuma/kuma-network-diagnostic-20261110-385lrsk0/candidate/bundle/repositories/homelab-server-configs/tests/repository/run-with-ansible-local-temp.sh \
  /home/aaron/.local/bin/ansible-playbook \
  -i uptime-kuma/operations/network-diagnostic-inventory.yaml \
  uptime-kuma/ansible/diagnose-network.yaml
```

Do not add tags, limits, extra variables or substitute working-tree files. Verify
the archive, manifest and every frozen input before execution. Repository policy
requires this exact-bundle authorization:
[server AGENTS.md](../../../homelab-server-configs/AGENTS.md#definition-and-authorization)
requires scoped authorization for every live stage and binding to one SHA-256
bundle; [this repository's AGENTS.md](../../AGENTS.md) retains that contract.
The change-control skill adds no approval gate of its own.

The only target is **ama@10.1.3.75 (j2-svpi3bmf)**, with existing host-key checking
and noninteractive sudo. Preflight must match the last accepted boot ID, stopped
Webmin/Kuma residue, source hashes/ownership, Podman/Netavark/image identities,
network and empty database, with at least 512 MiB available memory. Refuse drift;
do not repair or refresh inputs under this approval.

Proposed target changes are restricted to the diagnostic observer/receipt,
persistent ConditionPathExists guards on both existing generated units, temporary
runtime timing overrides, one ephemeral permit, one native fallback, and one
application start/stop. Ordinary existing-service runtime NAT, database and log
writes are expected. Existing application memory.high=256 MiB, memory.max=320 MiB
and no-swap limits remain; the observer has 96 MiB/no swap and CPUQuota=20%.
Temporary application controls are Restart=no, startup 60 seconds, stop 20 seconds
and maximum runtime 240 seconds; network startup is bounded to 30 seconds and stop
to 20 seconds. Original timing must be independently restored after containment.

Arm and verify the independent 300-second containment timer before creating the
permit or starting Kuma. The collector compares container-loopback HTTP,
host-to-actual-container-IP HTTP and published host-loopback HTTP separately for
IPv4 and IPv6, twice during a 90-second window. Requests are unauthenticated root
GETs with four-second bounds; bodies, cookies, credentials and unknown raw log
text are excluded. Retain actual ports/NAT/routing, selected container metadata,
resource samples and allowlisted application-log event labels. The collector has
a 150-second deadline, the native observer 165 seconds, and receipt 512 KiB maximum.
Atomic Pi-side checkpoints are fetched before containment; partial HTTP failures
remain evidence rather than aborting the other family.

Always remove only the matching owned permit and stop both units. Independently
verify stopped MainPID 0, no listeners or containers, absent permit and intact
persistent guards before cancelling the fallback. Its PID1 path removes the
permit and stops both units even if controller collection is lost; stop-post has
a 50-second bound. Verify empty database integrity and timing restoration.
On containment failure retain the fallback and receipts, report observed residue
and stop for bounded recovery; no automatic retry is authorized. Guards and the
private target diagnostic receipt remain. Clearing /run on a later reboot leaves
no permit and blocks generated startup; removing the guards or starting again
requires separately reviewed work.

No networking correction, source Quadlet rewrite, port/NAT policy change, image
import, package change, Webmin start, reboot, administrator setup, monitor/alert,
notification send, backup promotion, schedule activation, Caddy/DNS contact or
publication is included. This diagnostic cannot complete deployment acceptance.

### Network diagnostic authorization and execution

Aaron explicitly approved the exact bundle, command and scope linked at the
preceding authorization section on November 10, 2026. Archive, manifest and all
23 inputs were reverified before launch. Private `execution/authorization.json`
binds this approval to that unchanged SHA-256 and one execution on ama@10.1.3.75.
The native command is being launched once; preserve its complete stdout, Ansible
log and terminal status. Approval becomes consumed on this attempt; no replay,
network correction, second start or reboot follows from it.

### Network diagnostic terminal outcome

The approved diagnostic ran **once**, shell/Ansible exit **0**, against the unchanged
bundle above. All 43 native tasks passed: Pi 38 ok/17 changed, localhost 5 ok,
zero failed/unreachable/rescued. The approval is consumed. Full stdout, native
Ansible log, authorization, preflight, observation and containment receipts are
retained under the same private `execution/` directory; immutable copies and
SHA-256 identities are in `execution/terminal-archive/outcome.json`.

Preflight confirmed the accepted ARM64 identity/boot ID, source/image/network
identities, stopped Webmin/Kuma and 728,004 KiB available memory. Both persistent
permit guards, finite diagnostic controls and the independent native timer were
verified before the single start. No package/image import, reboot, Webmin start,
corrective networking, notification or Caddy/DNS action occurred.

The actual Pi receipt contains all 12 probes, two network/log snapshots and 89
resource samples over 90.001 seconds (75,017 bytes). Early probes found the
application still starting: internal/direct paths and published IPv4 refused
connections, while published IPv6 timed out. At the second round:

| HTTP path | IPv4 | IPv6 |
| --- | --- | --- |
| Container loopback | 302 | 302 |
| Host to actual container address | 302 | 302 |
| Published host loopback | 302 | Timeout after 4.005 seconds |

The actual container addresses were 10.89.0.3 and fd1e:eecd:b4a1:44b::3. Both
host loopback publication sockets were present. Retained rules include IPv6 DNAT
from ::1:3001 to the actual container address. The custom ingress deny counters
remained zero. Published IPv6 failed in both rounds, including after every other
path returned 302. This localizes the observed fault to the published IPv6
loopback path; it does not establish the original observer's lost family detail.

The IPv4 DNAT chain includes a loopback-source mark for masquerade; the IPv6
chain marks container-subnet sources but has no corresponding ::1-source rule.
That asymmetry is a supported hairpin/NAT hypothesis. No packet trace or isolated
correction test was performed, so the exact drop mechanism and remedy remain
unconfirmed. Do not apply an ad hoc nftables rule from this observation. W-063
owns correction qualification and subsequent acceptance.

Kuma memory peaked at **149,327,872 bytes (142.41 MiB)**, with zero memory-high,
max, OOM or OOM-kill events and zero restarts in both snapshots. Observer peak was
30.3 MiB, no swap. These are actual isolated diagnostic observations; Webmin
remained stopped, so they do not accept the combined operating budget. Fixed
startup event labels retained database connection/setup-required and nscd-start
failure; omitted unknown raw log lines were not exported. Successful subsequent
HTTP paths do not support treating that nscd label as the timeout cause.

Native post-collection readback independently verified both generated units
inactive/MainPID 0, no application containers or listeners, absent permit and
intact persistent guards. Only after that verification was the independent
fallback cancelled and checked inactive. Owned runtime timing overrides were
removed; original application/network timing was independently restored.
Stopped database quick_check was ok, with zero users, monitors and notifications.
The diagnostic is accepted for evidence and containment; Kuma remains unaccepted
for operation and stopped. Persistent guards prevent unattended generated startup
without a new permit, including after /run is cleared by a future reboot. No
reboot test was performed on the Pi and no further live action is authorized.

### Sealed IPv6 loopback corrective continuation, November 10

This candidate is **qualified and sealed, not approved or consumed**. No live
host was contacted during preparation. The consumed diagnostic, its source and
terminal receipts remain unchanged. The Pi's last observed state is stopped,
permit absent and generated units persistently guarded; no new start or reboot
is authorized.

The correction uses the installed systemd-socket-proxyd through owner
[socket](../../uptime-kuma/ansible/templates/uptime-kuma-loopback.socket.j2) and
[service](../../uptime-kuma/ansible/templates/uptime-kuma-loopback.service.j2)
templates. The socket binds only [::1]:3001, forwarding TCP to the working
127.0.0.1:3001 publication. Remove only Podman's ineffective ::1 mapping and make
the socket wanted/stopped with Kuma. Keep the dual-stack container, direct IPv6,
future explicit backend bindings, ingress guard and application limits. This
avoids introducing a custom NAT exception. It does not prove the underlying
kernel packet-drop mechanism or accept the future Caddy/backend path.

[correct-loopback.yaml](../../uptime-kuma/ansible/correct-loopback.yaml) selects
the [new operation](../../uptime-kuma/operations/network-correction.yaml) and
reuses the existing bounded observation/containment play with owner correction
and proxy-containment tasks. Default installation templates and runtime checks
also use this transport, so a later backend render cannot silently recreate the
broken ::1 publication. The permanent design and repeatable procedure remain in
[ARCHITECTURE.md](../../uptime-kuma/docs/ARCHITECTURE.md) and
[OPERATIONS.md](../../uptime-kuma/docs/OPERATIONS.md).

Private candidate root:
`/home/aaron/code/.local-evidence/uptime-kuma/kuma-network-correction-20261110-1qyk9qhi`.

- Archive: `candidate/kuma-network-correction.tar`, **194,560 bytes**, 33 input files.
- Archive SHA-256: `fc4cac6743c4449726c424ebdfbb9e9c5060b4888394f9924872f1684702b5bd`.
- `INPUTS.sha256` SHA-256: `1d1a63d308aa34b8fe2e896d2a05f5e81a6e0fdeffb8ed0d000390b7909101f3`.
- Frozen root: `candidate/bundle`; includes runtime inputs, owner templates,
  related installation/runtime-check changes, plan, predecessor provenance,
  public host keys and server Ansible helper. No package/image payload or secret.
- Seal proof: `qualification/seal-verification.json`; archive mode 0400, frozen
  files read-only, every input/manifest/archive verified against current source.
- Future execution evidence: `execution/`, mode 0700 and unused.

Qualification first reproduced the failure natively: IPv4 published loopback 302,
IPv6 published loopback timeout. The final **unchanged frozen candidate** then
passed the full native Ansible lifecycle: fixture 50 ok/21 changed, controller
5 ok, zero failed/unreachable/rescued. All **12 HTTP probes returned 302**, with
90 samples/two snapshots over 90 seconds; the retained receipt is 67,697 bytes.
Both loopbacks also passed actual WebSocket upgrades (101) and control ping/pong.
Wrong-source preflight refused before mutation (zero changed). Twenty focused
regressions, all three native playbook syntax checks, shell formatting/ShellCheck,
readonly/local collision checks, focused hooks and Markdown/YAML checks passed.
The vexp helper reported parent-workspace verification unavailable; it is not
counted as passing validation. Working-tree secret scan found nothing; the sole
bundle finding is a verified predecessor authorization-receipt SHA-256, not a
credential. No suppression was added.

Kuma fixture memory peak was 270,761,984 bytes (258.22 MiB), with 2,998 memory-high
events and zero max/OOM/OOM-kill events. Proxy peak was 4,022,272 bytes (3.84 MiB),
below its unchanged proposed 16 MiB hard cap. VFS/AMD64 fixture resource behavior
is not Pi capacity proof. The trial requires **528 MiB** available: 320 MiB Kuma,
96 MiB observer, 16 MiB proxy and 96 MiB host reserve. Existing Kuma 256/320 MiB,
CPU and no-swap controls remain unchanged. The later full-foundation floor is
now **720 MiB**, adding the proxy to the earlier 704 MiB budget; W-005 still
requires actual combined Webmin/Kuma/scan acceptance rather than assuming fit.

Native normal cleanup verified all four units stopped, no listeners/containers,
absent permit, intact original/additional guards, restored timing and empty
stopped database integrity. A separate test armed the same frozen native fallback
with all four units active and changed only its deadline from 300 seconds to two:
PID1 removed the permit and stopped all four without controller cleanup (9.389
seconds observed to containment). This is an accelerated active-service proof,
not a new full-300-second active-service test. Restart with tmpfs /run cleared,
plus explicit guarded fixture start attempts, left all four units stopped with
the effective unnegated permit conditions. No Pi reboot test is claimed.

Evidence is grouped in `qualification/qualification.json`, `qualified-native*`,
`qualified-evidence/`, `websocket-proof.json`, `fallback-proof.json`,
`restart-guard-proof.json`, source/secret check logs and session registry. The
failed before-start verifier candidate/receipt are preserved under
`qualification/failed-before-start`; the correction included all generated
fragment dependencies rather than weakening verification. The disposable fixture
was removed after proof retention. Native versions match the target Podman 5.4.2
and Netavark 1.14.0-2, but qualification uses AMD64, nested VFS and no external
network/aardvark-dns. It does not accept ARM64, microSD, Pi reboot, host DNS,
combined foundation capacity or external backend/HTTPS behavior.

#### Exact corrective command and live scope

Approval is requested for **one execution** of this bundle and command, including
strict preflight, owner changes, bounded acceptance and containment. Run from:

```text
/home/aaron/code/.local-evidence/uptime-kuma/kuma-network-correction-20261110-1qyk9qhi/candidate/bundle/repositories/homelab-monitoring-observability
```

```bash
env \
  ANSIBLE_CONFIG=/home/aaron/code/.local-evidence/uptime-kuma/kuma-network-correction-20261110-1qyk9qhi/candidate/bundle/ansible.cfg \
  ANSIBLE_LOG_PATH=/home/aaron/code/.local-evidence/uptime-kuma/kuma-network-correction-20261110-1qyk9qhi/execution/ansible.log \
  ANSIBLE_NOCOLOR=1 PYTHONDONTWRITEBYTECODE=1 \
  /bin/bash /home/aaron/code/.local-evidence/uptime-kuma/kuma-network-correction-20261110-1qyk9qhi/candidate/bundle/repositories/homelab-server-configs/tests/repository/run-with-ansible-local-temp.sh \
  /home/aaron/.local/bin/ansible-playbook \
  -i uptime-kuma/operations/network-diagnostic-inventory.yaml \
  uptime-kuma/ansible/correct-loopback.yaml
```

No extra variables, tags, limits or working-tree substitutions. Verify the seal
before execution. The sole target is **ama@10.1.3.75 (j2-svpi3bmf)** with existing
strict host-key checking and noninteractive sudo. Refuse baseline drift, missing
528 MiB headroom, source/guard/image/network/data mismatch, existing conflicting
proxy inputs or permit. Verify the installed proxy binary is executable,
root-owned, not writable by other users and owned by the systemd package before
changing application sources. Do not install a missing package under this scope.

Save the checked original Quadlet under protected new operation storage, install
the corrected owner Quadlet and two proxy units, and guard the new units with
the existing ephemeral permit condition. Keep both existing guards intact. The
proxy uses DynamicUser, no capabilities, 16 MiB/no swap, CPUQuota=10%, TasksMax=16,
startup 10 seconds and stop five seconds. It has no independently enabled boot
unit. The application wants the socket and native stop propagation covers both.

Use the existing temporary bounds: application startup 60 seconds, stop 20 seconds,
runtime 240 seconds and Restart=no; network startup 30 seconds and stop 20 seconds.
Arm and verify the independent 300-second timer before issuing the matching permit
and one start. Its stop-post explicitly stops app, network, socket and proxy with
a 50-second bound. Observe for 90 seconds using the 96 MiB/no-swap/20% CPU observer,
150-second collector and 165-second native observer bounds. Retain per-family HTTP,
actual ports/NAT/routes, safe log labels and proxy/application resource evidence.
Require all six paths to return the setup redirect after startup, correct proxy
limits/active state and only the intended container IPv4 loopback publication.
WebSocket proof is local qualification; live external WebSocket acceptance is
still deferred with backend/HTTPS work.

Always remove only the owned permit and stop all four units. Independently verify
proxy and generated units stopped, no listeners/containers, absent permit and
all guards intact before cancelling the fallback; restore only unchanged owned
runtime timing files and verify original timing and empty database integrity.
On failure, retain fallback and receipts if containment is unproved and stop for
bounded recovery. Corrected definitions, protected original-source backup and
persistent guards remain after success/failure; no automatic source restoration,
guard removal, new start or whole-host rollback is included. A later reboot loses
the permit and leaves these guarded units blocked.

No live read-only inspection before this approval, package/image action, firewall
policy/route change, Webmin start, reboot, administrator setup, monitor/alert,
notification send, schedule/backup promotion, Caddy/DNS contact or publication is
included. This operation accepts the loopback correction while returning Kuma
to stopped containment; remaining installation criteria stay pending. Repository
[authorization policy](../../../homelab-server-configs/AGENTS.md#definition-and-authorization)
requires the new exact-bundle approval; the change-control skill adds no gate.

### IPv6 loopback correction authorization and execution

Aaron explicitly approved the exact corrective bundle, command and scope linked
at the preceding section on November 10, 2026. Archive, manifest, all 33 input
identities and archive-to-frozen-file equality were reverified before launch.
Private `execution/authorization.json` binds this approval to the unchanged
SHA-256 and one execution on ama@10.1.3.75. Preserve complete stdout/native log
and terminal status. This attempt consumes the approval, including on failure;
no second start, reboot or remaining-installation work follows from it.

### IPv6 loopback corrective terminal outcome

The unchanged approved bundle ran **once**, native Ansible/shell exit **0**:
Pi 50 ok/21 changed, controller 5 ok, zero failed/unreachable/rescued. Approval
is consumed. Complete stdout, native log, authorization, preflight, observation,
proxy and generated-unit containment receipts are retained in private
`execution/`; immutable copies and SHA-256 identities are in
`execution/terminal-archive/outcome.json`. No replay or further live stage is
covered by this approval.

Preflight matched the accepted ARM64 identity/boot ID, original source hashes,
guards, image/network and empty stopped data, with 728,184 KiB available. The
root-owned executable proxy was verified as installed systemd package content.
The checked original Quadlet was saved under protected operation storage. Only
the reviewed source change and two proxy units were installed; both original
permit guards remained intact and the proxy units received matching guards.
Native unit/dependency syntax, effective original guards, unchanged application
limits and the independent timer were verified before one permit/start.

The actual ARM64 receipt contains all 12 measurements, two snapshots and 90
resource samples over 90.001 seconds (72,880 bytes). The early round captured
application startup refusal/reset responses. In the second round, **every path
returned HTTP 302**:

| HTTP path | IPv4 | IPv6 |
| --- | --- | --- |
| Container loopback | 302 | 302 |
| Host to actual container address | 302 | 302 |
| Published host loopback | 302 | 302 (0.010 seconds) |

The IPv6 socket was active on **[::1]:3001 only**; its proxy was active with
MemoryMax=16 MiB, MemorySwapMax=0 and zero restarts. Podman retained only the
intended 127.0.0.1 bootstrap publication; the dual-stack container/direct paths
continued to pass. This accepts the specific local transport correction, not
the original packet-drop hypothesis or the future external Caddy/HTTPS path.
Live WebSocket acceptance was outside this scope; its local qualification remains
distinct.

Kuma peak was **123,445,248 bytes (117.73 MiB)**; proxy peak was **2,138,112 bytes
(2.04 MiB)**, and observer peak 29.2 MiB with no swap. Application memory-high,
max, OOM and OOM-kill counters were all zero; both snapshots reported zero
application restarts. Existing service limits were not raised. Webmin remained
contained, so these observations do not qualify the combined foundation budget.
The measured preflight availability was below its future 720 MiB admission floor;
W-005 retains that gate/capacity reconciliation before remaining deployment.

After receipt collection, native cleanup removed only the matching permit and
stopped app, network, socket and proxy. Independent readback verified all four
inactive (service MainPID 0), no port 3001/10000 listeners or application
containers, absent permit and intact original/additional guards. Only then was
the fallback cancelled and checked inactive. Owned temporary timing overrides
were removed and original app/network timing independently restored. Database
quick_check was ok with zero users, monitors and notifications.

The corrected Quadlet, proxy units, protected original-source backup and all
persistent guards remain. Kuma is stopped; a later cleared-/run boot has no
permit for these guarded units. No Pi reboot test, Webmin start, administrator
creation, monitor/alert, notification, backup/restore, schedule, backend/Caddy/DNS
activation or publication occurred. The next continuation must explicitly
review combined resources and release/startup authority for the remaining work.

### Remaining-deployment local preparation

Preparation is confined to repositories and disposable local containers. All
consumed archives and Pi terminal receipts remain unchanged. W-065 through W-068
track this continuation; no live operation is sealed or approved yet.

The native startup producer passed 21 tasks against the combined fixture after
repairing its omitted package-native Webmin unit. Earlier fixture/parser failures
are retained privately. Settled HTTP, authenticated Webmin, WebSocket and bounded
needrestart checks passed without new pressure events. Startup memory-high
throttling remains visible; limits were not raised. Administrator setup/login and the actual administrator-bearing restore checker
have passed locally, including the native restore lifetime bound. Native expiry, helper-failure stop-post, future-start denial and labelled probe
cleanup passed. A later contained restart retained no service listener or permit. A container restart clears /run
but retains its supplied boot ID; that is not proof of a physical Pi reboot.

### Remaining-deployment qualification and proposed scope

Local qualification passed with the real owner producer and installed native
services: 21 startup tasks, four final acceptance tasks, 25 focused regressions,
YAML/shell/collision checks and Markdown validation. The working-tree secret scan
passed. vexp completion verification is unavailable from the parent workspace;
these source and native checks are the verification evidence.

The disposable AMD64 fixture used a 720 MiB/no-swap outer limit. Settled Kuma,
IPv6 proxy and authenticated Webmin requests passed during a bounded needrestart
scan. Recorded Kuma peak was 270,786,560 bytes (258.24 MiB); its 4,407 startup
memory-high events remained unchanged during the settled sample. No memory-max,
OOM, OOM-kill or service restart occurred in that sample. Webmin peak was
73,641,984 bytes and proxy peak 2,580,480 bytes. Keep the failed strict-zero-high
checks; they prompted the documented settled-pressure criterion, not raised
limits or concealed counters.

Actual fixture administrator creation/login, complete-data backup and isolated
restore passed, including the native 300-second restore lifetime bound. Both
loopback WebSocket upgrades/ping-pong passed. Native expiry, later-start denial,
second-pending-boot refusal, helper-failure stop-post and contained-restart checks
passed. Owned labelled restore/ingress containers were removed while preserving
backup/data; the native container lifetime kill also passed. The final native
readback found all guards/dependencies intact and the pending timer disabled in
accepted state.

A container restart clears /run but retains its assigned boot ID. The changed-boot
branch was tested with an explicitly synthetic previous identity. This is not a
physical Pi reboot or ARM64 acceptance. Actual watchdog/kernel reporting, SMTP
connectivity, proxy-source HTTP, denied-source/SSH observations, operator browser
verification and Pi capacity remain mandatory live gates. The full hardware-bound
coordinator was syntax-checked; it was not claimed to run end-to-end in the fixture.

The proposed operation targets `ama@10.1.3.75`, with backend HTTP/source probes
only from `pi@10.1.0.53` and `pi@10.1.0.54`. It verifies accepted boot/address,
29 package pins, corrected runtime hashes, empty unclaimed data and stopped
four-unit guards, then requires **720 MiB available** before service mutation.
The last retained Pi availability was **711.12 MiB**. That does not pass; no cache
reclaim, budget reduction, package/image action or new inspection is implied by
preparing this candidate. An approved attempt must stop if fresh admission fails.

After admission: install only startup-authority/containment artifacts, reapply
the accepted owner Webmin profile, start existing services, verify combined
resources, perform one planned reboot, allow at most fifteen minutes for private
operator setup, verify the administrator-bearing backup/restore, promote guarded
backend bindings, run both proxy/denial probes, and enable the fleet daily scan.
The pending authority expires after forty minutes; native shutdown/probe lifetime
bounds remain in force during cleanup. Permanent startup is accepted only after
all continuation checks pass. No first boot-file/address correction is repeated.

Failure retains data, packages, backups, corrected definitions and all guard files.
It removes permits/schedule, stops owned services/probes and denies future startup;
malformed authority still triggers native stop-post containment. If unreachable,
retain the fallback and report physical recovery/manual verification. No DNS/Caddy
mutation, final HTTPS acceptance, monitor/alert activation, synthetic notification,
repository publication, source rollback or replay of a consumed operation is included.
Normal scheduled needrestart notifications are included only after acceptance.

Private preparation and qualification: `/home/aaron/code/.local-evidence/uptime-kuma/remaining-deployment-20261110-dqpr9b40`.
Consumed predecessor bundle identity was reverified unchanged before sealing.
The following exact bundle is the only candidate for new live authorization.

### Remaining-deployment exact bundle, command and scope — approval required

Status: **sealed, not authorized; never executed**. This supersedes only the
unreviewed intermediate seal retained under private qualification; all consumed
installation/diagnostic/corrective bundles remain untouched.

- Archive: `/home/aaron/code/.local-evidence/uptime-kuma/remaining-deployment-20261110-dqpr9b40/candidate/remaining-deployment.tar`.
- SHA-256: `520f6a40a80047d7408958fa06b80c6f722e71ffdfb0fd0641f9fcfa8a308240`.
- Input-manifest SHA-256: `68771cfaeac4de76e493e4c1d8c6c78ec8e75883d09416d5f5c095f8cd5e6aa9`.
- Size: **778240 bytes**, **109 declared inputs** plus the manifest.
- Frozen root: `/home/aaron/code/.local-evidence/uptime-kuma/remaining-deployment-20261110-dqpr9b40/candidate/bundle`.
- Evidence destination: `/home/aaron/code/.local-evidence/uptime-kuma/remaining-deployment-20261110-dqpr9b40/execution` (already protected; no live receipts yet).

The exact proposed command, from that frozen root, is:

```bash
ANSIBLE_CONFIG=./ansible.cfg \
  /bin/bash repositories/homelab-server-configs/tests/repository/run-with-ansible-local-temp.sh \
  ansible-playbook \
  -i repositories/homelab-monitoring-observability/uptime-kuma/ansible/inventory.yaml \
  repositories/homelab-monitoring-observability/uptime-kuma/ansible/remaining-deployment.yaml
```

Approval covers one attempt of the preceding proposed scope: Pi preflight,
guarded existing-service startup, one reboot, private operator setup, backup and
restore, source-restricted backend promotion/probes, owner schedule activation,
acceptance and bounded containment. The proxy nodes receive read-only backend
probes only. It authorizes neither a package/image operation nor any consumed
bundle replay. **A fresh memory reading below 720 MiB stops before service changes.**

During the post-reboot setup window, the operator must verify Kuma and Webmin
logins privately through SSH loopback forwarding. After those checks, create the
root-owned acknowledgement using the following command from your own terminal;
it contains no credential and must not be issued before verifying both logins:

```bash
ssh ama@10.1.3.75 'sudo -n /bin/sh -s' <<'ACK'
umask 077
printf '%s\n' 'Kuma and Webmin login verified; monitors and alerts empty' > /run/uptime-kuma-network-diagnostic/operator-ready
ACK
```

The controller waits at most fifteen minutes for this acknowledgement within the
forty-minute pending authority. The independent timer remains armed through the
reboot and operator wait. Expiry or failure stops owned services/probes and leaves
data, backups, corrected sources and all guards. If the Pi is unreachable,
physical recovery/manual verification may be necessary; do not claim remote
containment was observed. Successful continuation leaves the source-restricted
backend and normal daily needrestart schedule active, with accepted guarded
startup. Final DNS/Caddy HTTPS remains W-007/W-011 and requires its owner stage.

Frozen controller integrity/mode checks and the final bundle secret scan passed.
One scanner hit on the full predecessor receipt was an independently verified
SHA-256 file identity, not a credential. The bundle now contains minimal predecessor
provenance bound to the original archived receipt hash; that source is unchanged.
The complete local qualification, failed fixture attempts and cleanup receipts
remain private. No production target was contacted while preparing this candidate.

[Repository authorization policy](../../../homelab-server-configs/AGENTS.md#definition-and-authorization)
requires this exact-bundle approval for live changes. The change-control skill
adds no additional approval gate. Approval has not yet been given.

### Remaining-deployment authorization received — November 10, 2026

Aaron explicitly approved the exact bundle, command and scope at line 1332.
Archive and manifest hashes above, all 109 inputs and archived bytes were verified
before target contact; the execution directory was empty and mode 0700.
The private `execution/authorization.json` binds this approval to one attempt.
The sealed snapshot remains unchanged. All earlier approval text above describes
its preparation-time state; this entry records the new authority.

### Remaining-deployment terminal outcome — November 10, 2026

The approved archive above was executed once with the exact frozen command.
All eight controller checks passed. The Pi preflight stopped at the required
`MemAvailable >= 737280 KiB` assertion; Ansible exited 2 and reported five successful
target tasks, zero changes, zero unreachable targets and one failed assertion.
The native output establishes memory below 720 MiB but does not expose the numeric
reading. The older 711.12 MiB observation is not this attempt's measurement.

No service mutation, startup authority, reboot, operator setup, backup/restore,
backend promotion, proxy probe or schedule activation was reached. Containment
was unnecessary because execution stopped before the mutable block. No independent
post-attempt inspection was performed; the last accepted stopped/guarded state
remains the prior observation, not a newly verified state.

This approval is consumed. No replay or changed-input retry is authorized.
W-069 tracks capacity reconciliation and the missing numeric evidence; required
ARM64 combined and final DNS/Caddy acceptance remain pending.
Private `execution/terminal-archive/` preserves authorization, full Ansible log,
start/end timestamps, exit status, retired session registry and outcome, with
SHA-256 identities. The approved archive and frozen input tree are unchanged.

### Capacity reconciliation — local analysis, November 10, 2026

The [architecture stage budget](../../uptime-kuma/docs/ARCHITECTURE.md#meaning-and-limits-of-the-admission-budget)
now distinguishes simultaneous hard caps, measured demand and host overhead.
The arithmetic is correct: 624 MiB of bounded services plus 96 MiB of reserve.
The largest included stage is a scan alongside Kuma/Webmin/proxy; restore replaces
stopped Kuma, and ingress finishes before scheduling. Removing the scan allowance
because scheduling happens last would under-budget ordinary operation.

The gate is our conservative deployment policy, not a measured application minimum.
Existing host memory consumption is already reflected in MemAvailable; the reserve
is additional allowance for growth, orchestration and runtime processes outside
the application caps. Remote notification servers add no local resident service.
There is no justified numerical correction or proven double count that permits
lowering 720 MiB under the existing policy.

Retained evidence establishes these limits:

- The isolated Pi correction measured 728184 KiB available (711.12 MiB), 9096 KiB
  below the combined floor. Kuma peaked at 123445248 bytes (117.73 MiB) and the
  proxy at 2138112 bytes (2.04 MiB); this omitted the combined foundation workload.
- The latest approved attempt proves only availability below 737280 KiB. Its
  exact reading was not logged and cannot be recovered from retained evidence.
- The combined AMD64 fixture exercised service caps and requests. Its retained
  `combined-final-local.json` reports 5214652 KiB host MemAvailable, exceeding
  the fixture's entire parent allowance; this is not fixture reserve proof.
  It neither measures the Pi nor closes the transient scan gap in W-070.

Keep the floor and limits unchanged. First establish whether the stopped-host
shortfall is persistent and attributable to resident services, reclaimable memory,
kernel memory or current activity. Any service removal, reduced cap, revised
admission policy or host change needs an explicit reviewed decision. Do not add
swap, drop caches or retry deployment as a substitute for that evidence.

Local qualification and failed sandbox-test disposition are retained at
`/home/aaron/code/.local-evidence/uptime-kuma/capacity-reconciliation-1qoxvzq9`.
All 26 local regressions (including four admission cases), four playbook syntax
checks, Markdown/YAML validation, shell checks/collision policy and the working-tree
secret scan passed. Vexp verification remained unavailable because its session
is rooted at the parent workspace, which is not a Git repository; it contributes
no validation claim. The consumed archive and all frozen inputs were reverified
unchanged. No production target was contacted for this reconciliation. No new
deployment candidate is sealed or authorized.

The preflight reads MemAvailable while its SSH/Ansible observer is resident.
Transient observation overhead may affect admission; its size on this Pi is not
measured. Do not subtract an assumed amount or confuse an idle SSH snapshot with
an identical Ansible preflight workload.

### Proposed bounded read-only capacity inspection — authorization required

One SSH session as `ama` to `10.1.3.75`, bounded to 60 seconds, with three
snapshots ten seconds apart. Read only hostname/kernel/boot identity, uptime,
`/proc/meminfo`, `/proc/pressure/memory`, selected VM counters (swap activity,
reclaim and OOM), and cgroup memory current/peak/limits/events for existing top-level
slices and service groups. Read the active state of the four Kuma units and Webmin.
Retain exact timestamps, numeric readings and permission/read failures privately;
rank service-group current memory without summing overlapping ancestor/child
cgroups or treating process RSS as uniquely owned memory.

No credentials, command lines, environment variables, application data or service
configuration contents are collected. No package command, scan, service start/stop,
cache manipulation, reboot, file staging or remote persistent write is included.
Only local evidence files may be created. SSH/observation has transient overhead;
report it as a measurement limit. The inspection diagnoses stopped-host capacity,
not workload acceptance, and grants no continuation authority.

The original read-only baseline and every installation/diagnostic attempt are
historical; the most recent approval is consumed. The owner policy in
`homelab-server-configs/AGENTS.md`, Definition and authorization, states:
"A definition-only task must not contact a live target unless the user has
explicitly requested or authorized a read-only inspection."
This proposed inspection therefore awaits explicit approval.

### Approved capacity inspection outcome — November 10, 2026

Aaron approved the preceding bounded read-only scope. One authenticated SSH
session completed three snapshots ten seconds apart in 20.16 seconds. Capture
ran at 20:01:24–20:01:44 America/Chicago on November 10 (02:01:24–02:01:44 UTC
on November 11). Target hostname, ARM64, kernel and boot ID matched the retained
accepted identity. No service/package/cache/boot action or remote file staging
was performed. This inspection authority is consumed.

| Snapshot | MemAvailable (KiB) | MiB | Margin above 720 MiB (KiB) |
| --- | --- | --- | --- |
| 1 | 745848 | 728.37 | 8568 |
| 2 | 745040 | 727.58 | 7760 |
| 3 | 745040 | 727.58 | 7760 |

The kernel reports 926640 KiB total memory (904.92 MiB). The final snapshot
includes 206476 KiB free, 419868 KiB cached, 53844 KiB buffers and 138608 KiB
reclaimable slab. These counters overlap in accounting; do not sum them with
MemAvailable or add ancestor and child cgroup charges. The largest inspected
named service groups were NetworkManager (about 20.2 MiB), udev (16.2–16.5 MiB)
and journald (9.4 MiB). Slice charges include descendants/cache and do not identify
an equivalent amount of unreclaimable process memory. This scope did not collect
memory.stat or recursive process attribution, so it cannot assign all host usage.

Selected reclaim, swap-in/out and OOM counters did not increase. All thirteen
sampled cgroups had unchanged memory.events counters. Existing system.slice
high/max counts are cumulative history, not new pressure during this inspection.
There was 32 KiB of existing swap use, unchanged; no new swapping was observed.
`/proc/pressure/memory` returned FileNotFoundError in all samples. No PSI result
or continuous absence of pressure is claimed.

All four Kuma units reported inactive/dead; Webmin reported failed/failed. The
owner installed-foundation preflight already allows inactive or failed Webmin
with additional checks. This inspection did not check its MainPID, listeners,
disabled state or guard files, so it does not independently reaccept containment
or establish when Webmin entered that failed state.

Capacity conclusion: a persistent stopped-host shortfall below 720 MiB is not
established. The three current samples exceed the floor, with a narrow margin.
They do not recover the failed deployment's missing reading or reproduce its
SSH/Ansible process footprint. Observer overhead and other transient activity
remain possible explanations, not a confirmed cause. No evidence justifies
lowering the floor, deleting resident services, adding swap or changing hardware
solely from the failed gate. Keep the current budget and resolve comparable
admission sampling and scan-time reserve measurement before another continuation.

The first transport connection refused strict host-key verification before
SSH authentication because the working repository's ignored payload path had
no known_hosts file. Its failed receipt is retained. The existing hashed target
entry was resolved with ssh-keygen and verified against the preserved bundle's
manifest, then used for the first authenticated inspection. No key was enrolled
and no checking was weakened. The first receipt's automatically written
approval_consumed flag referred to that failed transport launch; the outcome
records one completed authenticated inspection under the approved scope.

Private evidence: `/home/aaron/code/.local-evidence/uptime-kuma/capacity-inspection-qzkkg6gr`.
The directory retains approval, collector source/hash, original transport failure,
corrected transport definition, all JSONL snapshots, stderr, terminal status,
retired session registry, parsed outcome and SHA256SUMS. Raw evidence remains
outside Git. No replacement deployment bundle was prepared or authorized.

### Observer and scan measurement preparation — November 10, 2026

The existing evidence cannot causally assign the failed gate to Ansible overhead.
The proposed native playbook runs three paired lightweight raw/Ansible-command/raw
readings, retaining both raw timestamps and the command module's start/end times.
It reuses the gate's awk expression. SSH/sudo and other activity remain present;
no inferred overhead is subtracted and no admission floor is changed.

The owner observer runs the installed `needrestart -bkl` with list-only mode under
96 MiB/no swap/one CPU. Its native oneshot start timeout is 90 seconds plus at
most five seconds for stop. RemainAfterExit retains systemd's exact scan peak
until collected, then the unit is stopped. The observer itself has 32 MiB/no swap,
a 120-second runtime bound and five-second stop timeout. Before measurement,
require at least 224 MiB for this stopped-application workload (96 + 32 + 96);
this does not replace the deployment's 720 MiB requirement.

At nominal 200 ms intervals, record host MemAvailable and finite ancestor cgroup
headroom, plus available scan cgroup counters. Stop on a sampled reserve below
96 MiB. Reject native scan failure, invalid peak/no-swap evidence, no sample while
the scan is running, sample gaps over one second, or cleanup failure. Discrete
samples cannot rule out shorter dips between samples. Source and observer overhead
remain in the measurement. Applications remain stopped; combined acceptance still
requires repeating this observation alongside services in a later continuation.

Local qualification uses a cached, disposable AMD64 Podman/systemd fixture with
720 MiB outer memory and no swap. The real installed needrestart scan completed;
final-source native peak was 25497600 bytes, with three samples while running and maximum
sample gap about 0.228 seconds. This is fixture evidence, not a Pi sizing result.
A 160 MiB parent limit rejected the scan before launch despite ample host memory.
An injected sleeping scanner was stopped by the actual 90-second native timeout;
the failed observation and cleanup were retained. Both measurement units were
independently not-found/inactive with MainPID zero. The disposable fixture was
removed after preserving all receipts. No production service was touched.

Six focused regression tests exercise finite-parent/host reserve, the fresh
observer-resident pre-scan budget, refusal to
adopt an existing unit, mid-scan failure retention and cleanup failure. The actual
paired Ansible tasks passed on localhost. The complete hardware-specific playbook
is syntax-checked; it is not represented as an end-to-end local Pi execution.
The localhost/AMD64 results do not establish current Pi overhead, kernel reporting
or scan headroom. Prior failed/successful bundles remain unchanged.

Preparation and qualification evidence:
`/home/aaron/code/.local-evidence/uptime-kuma/capacity-measurement-hbvxmkz9`.
The new operation permits only target identity/policy/stopped-state preflight,
paired observations, temporary protected `/run` staging, two bounded transient
units, one list-only scan, receipt collection, owned cleanup and stopped-state
readback. No package operation, mail submission, application start/stop, reboot,
DNS/Caddy/proxy contact, schedule activation, cap change, cache manipulation or
repository publication is included. If unreachable after startup, native timeouts
remain the process bound; retain an explicit unverified-cleanup/residue outcome.

Final local checks passed: 32 regressions, five playbook syntax checks, paired
localhost tasks, YAML/Markdown and shell/collision checks. The application working-
tree secret scan passed. The broad server scan reported sixteen 64-hex values
under the generated `.vexp/manifest.json` file_hashes map; that index metadata is
outside the operation and excluded from its candidate, with no blanket allowlist
change. Candidate scanning remains a separate sealing check. Vexp mechanical
verification was unavailable in its parent-workspace session; it adds no validation
claim. All disposable containers and local test sessions are finished.

Final budget review added a fresh pre-scan gate after the observer is resident:
require at least 192 MiB host and finite-parent headroom, covering the full 96 MiB
scan plus 96 MiB reserve. The earlier 224 MiB gate must pass for both the raw and
Python-backed readings. This avoids assuming the observer/orchestrator footprint
can be ignored. No amount is added back to an observed reading. A new boundary
regression and a fresh native scan passed; the earlier native parent-limit and
90-second timeout tests remain evidence for those unchanged failure paths. The
unreviewed intermediate seal is retained privately and superseded before approval.

### Exact observer/scan measurement bundle, command and scope — approval required

Status: **sealed, not authorized; never executed on the Pi**. This supersedes
only the unreviewed intermediate measurement seal retained under qualification.
Every consumed installation, diagnostic, corrective and inspection record remains
preserved. This is a measurement operation, not a deployment continuation.

- Archive: `/home/aaron/code/.local-evidence/uptime-kuma/capacity-measurement-hbvxmkz9/candidate/capacity-measurement.tar`.
- SHA-256: `64acf58217479f92e54319058b89c1dac95ab95f554bf8c5311e83bea9a82982`.
- Input-manifest SHA-256: `8b0d8f2e30da3bd87aad4b47c7108c8e7e7b27c106bcec17ce62536ed7b460ab`.
- Size: **307200 bytes**, **23 declared inputs** plus the manifest.
- Frozen root: `/home/aaron/code/.local-evidence/uptime-kuma/capacity-measurement-hbvxmkz9/candidate/bundle`.
- Evidence destination: `/home/aaron/code/.local-evidence/uptime-kuma/capacity-measurement-hbvxmkz9/execution` (mode 0700, no live receipts).
- Target: `ama@10.1.3.75`, with non-interactive sudo and the existing manifest-verified pinned host key.

Exact command, from that frozen root:

```bash
ANSIBLE_CONFIG=./ansible.cfg \
  /usr/bin/timeout --signal=TERM --kill-after=10s 240s \
  /bin/bash repositories/homelab-server-configs/tests/repository/run-with-ansible-local-temp.sh \
  ansible-playbook \
  -i repositories/homelab-monitoring-observability/uptime-kuma/ansible/inventory.yaml \
  repositories/homelab-monitoring-observability/uptime-kuma/ansible/measure-capacity.yaml
```

Approval covers **one attempt**: exact Pi/kernel/boot/scanner and list-only policy
preflight; stopped application and unused measurement-unit checks; three paired
raw/Ansible/raw readings; one private `/run/kuma-capacity-*` directory and observer
source transfer; the bounded observer and one list-only needrestart transient
service; receipt collection, owned-unit/directory cleanup and application-state
readback. Normal SSH/Ansible temporary execution is included. No credentials or
application data are collected; only non-secret scan/resource evidence is retained.

Both initial raw and Python-backed readings must meet the isolated 224 MiB budget.
Once the observer is resident, require fresh 192 MiB host/finite-parent headroom
before starting the 96 MiB scan, then at least 96 MiB reserve at each sample.
The scan has no swap and a 90-second native start timeout plus five-second stop;
the observer has 32 MiB/no swap, a 120-second runtime bound plus five-second stop.
The controller is bounded to 240 seconds plus at most ten seconds for termination.
Missing/invalid evidence, sample gaps above one second, failed native scan/kernel
reporting, reserve failure, changed application state or cleanup failure prevents
acceptance. No automatic retry, cap/floor adjustment or cache manipulation is allowed.

Cleanup touches only the two initially absent measurement units and this attempt's
fresh protected directory. It never starts, stops or resets Kuma/Webmin. If the
controller cannot reach the Pi, native timeouts bound processes; volatile evidence
or an exited/failed unit record may remain and cleanup must be reported unverified.
No deployment, package action, schedule activation, notification producer/message,
application start/stop, reboot, DNS/Caddy/proxy operation or publication is included.

The scan runs with applications stopped. Its result can reconcile observer-method
differences and scan-only headroom; it cannot accept combined application capacity
or silently lower the 720 MiB deployment floor. W-069/W-070 remain pending actual
measurement and, for combined reserve, a later authorized running-services stage.

All seven frozen controller checks passed using localhost-only inventory. Archive,
manifest, all input hashes and archive-to-tree equality passed; the final candidate
secret scan found no leaks. There are no active test sessions or disposable
containers. These checks do not contact the target or grant execution authority.

[Owner repository policy](../../../homelab-server-configs/AGENTS.md#definition-and-authorization)
requires scoped live authorization bound to the exact SHA-256 bundle, command,
target, mutation, acceptance and recovery boundaries. The change-control skill
adds no extra approval gate. Approval for this measurement has not yet been given.

### Measurement authorization received

Aaron explicitly approved the exact bundle, command and scope at the preceding
approval section (line 1634 when reviewed). Archive and manifest hashes, all 23
inputs and archive-to-tree equality were reverified before launch. The private
`execution/authorization.json` binds this one attempt to the approved command and
SHA-256. Prior preparation-status wording above is historical, not current authority.

### Approved observer/scan measurement outcome — November 10, 2026

The exact approved archive `64acf58217479f92e54319058b89c1dac95ab95f554bf8c5311e83bea9a82982`
ran once at 21:21:20–21:22:17 America/Chicago (November 11, 03:21:20–03:22:17 UTC).
Exit 0; target recap 41 successful tasks, 12 changes, no failures/unreachable;
controller seven successful checks. Changes were confined to measurement setup,
execution, private receipts and owned cleanup. Approval is consumed; no replay.

Private evidence: `/home/aaron/code/.local-evidence/uptime-kuma/capacity-measurement-hbvxmkz9/execution/`.
`authorization.json`, `terminal.json`, complete `ansible.log`, three paired receipts,
`observation.json`, scan output, cleanup/application readbacks and `outcome.json`
are bound by `EVIDENCE.sha256`. Frozen inputs and every earlier consumed bundle remain intact.

| Pair | Raw before (KiB) | Ansible command (KiB) | Raw after (KiB) |
| --- | --- | --- | --- |
| 1 | 734652 | 722820 | 732392 |
| 2 | 731648 | 725668 | 734036 |
| 3 | 733072 | 723964 | 731772 |

The command readings were 5980–11832 KiB (5.84–11.55 MiB) below their adjacent raw
readings. This supports an observer-method effect but includes concurrent activity;
it is not a calibrated overhead allowance. All nine readings were below 737280 KiB
(720 MiB), including raw observations. Command shortfalls were 11612–14460 KiB
(11.34–14.12 MiB). The earlier read-only snapshots above 720 MiB and this lower raw
baseline also show variability; Python overhead alone cannot reconcile admission.
The original failed gate's exact reading remains unknown. No number is added back,
no cache is dropped and the floor remains unchanged.

The bounded list-only needrestart scan succeeded with current/expected kernel
`6.18.60+rpt-rpi-v8`, KSTA 1 and empty stderr. Native peak was **43397120 bytes
(41.39 MiB)**, swap peak zero, within the 96 MiB cap. The observer reported an
8.1 MiB peak within its separate 32 MiB cap. There were 17 samples, including 15
with a live scanner PID; minimum available host memory during scanning was
**702808 KiB (686.34 MiB)**. Maximum sample gap was 0.255 seconds. Sampled scan
memory events were all zero; this is not a claim about all host pressure counters.
`system.slice` had unlimited memory.max, so no finite parent bound was exercised.
Discrete samples cannot exclude shorter dips, and observer/SSH/Ansible costs remain
included in the observed availability.

Both owned measurement units were read back not-found/inactive/dead with MainPID 0.
The playbook successfully removed its allocated `/run/kuma-capacity-h6t_q8zj`
directory. Application before/after state matched exactly: four Kuma units inactive,
Webmin failed, and all service MainPID values zero. No application start/stop,
reboot, package action, notification, DNS/Caddy operation or deployment occurred.

W-073 is resolved. W-069 remains in progress because actual admission still fails
the unchanged floor. W-070 remains open because the measurement deliberately kept
applications stopped. Preserve this evidence while reconciling admission locally;
a later proposed continuation must retain numeric admission evidence and observe
scan-time reserve with the combined running workload. No new continuation or live
authority is defined by this successful measurement.

### Local admission reconciliation — November 10, 2026

Decision: preserve the existing admission implementation and 720 MiB floor. The
latest actual Ansible readings miss admission by 11.34–14.12 MiB; adjacent raw
readings also miss it. Changing the reader cannot qualify this observed baseline.
The difference between earlier passing raw snapshots and later failing raw
snapshots also rules out treating a fixed Python allowance as the whole problem.
These observations do not identify the responsible host consumer or establish a
safe amount of reclaimable memory. Recovering exactly the largest observed deficit
would only reach the threshold for those samples, not establish durable margin.

Reviewed execution paths: `accepted-prerequisites.yaml` imports the existing
`preflight-host.yaml` gate before mutation and retains its numeric receipt.
`remaining-deployment.yaml` and `tasks/complete-deployment.yaml` call the owner's
foundation acceptance and combined checkpoints before reboot, after reboot and
after guarded backend promotion. The owner
currently runs an unobserved scan; `accept-combined.yaml` reads reserve afterward
at two checkpoints. These paths cannot establish the minimum reserve during scan.
No executable input or consumed bundle was changed in this reconciliation.

The architecture now specifies reuse of the qualified owner observer in place of
the existing acceptance scan, with running applications, native bounds, retained
failure evidence, cleanup and the existing application containment. This remains
implementation work under W-070, not accepted live behavior. The isolated observer
has its own 32 MiB cap: the full worst-case instrumented stage totals 752 MiB if
that allowance is additional to the existing 720 MiB budget. This is a disclosed
planning consequence, not a raised admission floor or permission to consume the
96 MiB reserve. Temporary observer accounting must be resolved before sealing.

W-074 is resolved. W-069 remains in progress: there is no supported host-footprint
remedy in the retained evidence, and no evidence authorizes disabling a service,
dropping caches, changing swap or reducing caps. The next useful preparation is a
bounded read-only attribution inspection: aligned MemAvailable samples, relevant
service/cgroup current/peak/stat and finite-parent limits, distinguishing anonymous,
file and kernel charges without summing overlapping parent/child accounting.
Retain timing and the inspection's own footprint; avoid credentials, application
data and unrestricted process arguments. No target contact is authorized by this
proposal. If attribution provides no sustainable owner-approved remedy, a larger
host or an explicitly reviewed design change is the remaining decision; neither
is selected by this local reconciliation. Repeating admission alone is not a remedy.

Only PLAN.md, WORK.md and the existing architecture were updated. The plan links
the durable design; this ledger retains the measured outcome and unresolved work.
No continuation, new live bundle or approval request was created.

Validation: Markdown lint passed for all three changed documents; Git whitespace
checks passed. vexp verification was unavailable because its parent workspace is
not a Git repository; direct source reads confirmed all three acceptance call sites.
No runtime tests were needed for these documentation-only changes.

### Exact host-memory attribution inspection — approval required

Prepared from Aaron's request to inspect attribution before proposing a capacity
remedy. This is a new read-only inspection; every prior approval remains consumed.
No deployment candidate is prepared, and no host remedy is selected.

- Archive: `/home/aaron/code/.local-evidence/uptime-kuma/host-memory-attribution-ydppox2d/inspection.tar`.
- SHA-256: `88ef942a560b3bf71dc6c718e701694336ea9877f78a572647bdebfe42fc4b2c`.
- Input-manifest SHA-256: `c7d94633a3c6b103d1c389ec322364b57eae62db3fe40aa6e9a2dcbd20144718`.
- Size: 30720 bytes; four inputs plus `INPUTS.sha256`.
- Frozen inputs: `/home/aaron/code/.local-evidence/uptime-kuma/host-memory-attribution-ydppox2d/bundle`.
- Private evidence: `/home/aaron/code/.local-evidence/uptime-kuma/host-memory-attribution-ydppox2d/execution` (0700, empty).
- Target: `ama@10.1.3.75`, no sudo. Existing pinned host key copied from the
  verified consumed bundle; no trust enrollment or relaxed verification.

Exact command, from `/home/aaron/code/.local-evidence/uptime-kuma/host-memory-attribution-ydppox2d`:

```bash
/usr/bin/timeout --signal=TERM --kill-after=5s 55s ssh -T -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=8 -o ServerAliveInterval=5 -o ServerAliveCountMax=2 -o UserKnownHostsFile=/home/aaron/code/.local-evidence/uptime-kuma/host-memory-attribution-ydppox2d/bundle/known_hosts -o GlobalKnownHostsFile=/dev/null ama@10.1.3.75 '/usr/bin/timeout --signal=TERM --kill-after=5s 45s /usr/bin/python3 -I -B -' < /home/aaron/code/.local-evidence/uptime-kuma/host-memory-attribution-ydppox2d/bundle/inspect-host-memory.py > /home/aaron/code/.local-evidence/uptime-kuma/host-memory-attribution-ydppox2d/execution/inspection.jsonl 2> /home/aaron/code/.local-evidence/uptime-kuma/host-memory-attribution-ydppox2d/execution/stderr.log
```

Approval covers one attempt with controller-side start/exit receipts and complete
stdout/stderr retained privately. Before launch, verify archive/manifest/input
hashes and absence of an earlier execution receipt. No automatic retry or changed
input execution is permitted. Record the terminal code even on a timeout or failure.

The collector checks the exact retained hostname, ARM64 architecture, kernel and
boot ID, then requires the four Kuma units and Webmin stopped with service PIDs
zero. It takes three snapshots with starts scheduled ten seconds apart, followed
by application-state readback. Each snapshot includes:

- MemAvailable and the rest of `/proc/meminfo` before and after sequential reads;
  memory pressure if present, selected swap/reclaim/OOM counters and timing.
- Up to 256 existing cgroups, with parent paths, current/peak/high/max/swap charges,
  events, memory.stat and memory.pressure. No symlink traversal. Keep hierarchical
  charges separate; neither parent/child totals nor memory.stat subcategories are
  independent quantities to sum blindly.
- Up to 1024 process IDs with short names, numeric IDs, RSS anonymous/file/shared
  breakdown, swap, thread count and cgroup membership. No command lines,
  environments, credentials, service configuration or application data.
- The collector's own PID, cgroup, RSS components and high-water RSS. SSH and
  collector overhead remain included; none is added back to admission readings.

Each file read is limited to 65536 characters; total JSON output is limited to
2 MiB. Missing, unreadable, disappearing or oversized files and enumeration
truncation are explicit evidence gaps. Collection is sequential, not an atomic
snapshot; process RSS is not unique ownership and file cache is not proof of
safely reclaimable capacity. An exit-zero receipt requires three samples, a
completion marker and unchanged stopped application state; it does not establish
complete attribution if visibility is limited, or acceptance of the workload.

The remote collector has a 45-second alarm and a 45-second native timeout with
five-second kill allowance. The controller allows 55 seconds plus five-second
kill allowance, including connection time. Each systemctl show is bounded to
three seconds. The script reads kernel/systemd metadata and writes only stdout;
no remote file staging or persistent write is requested. Ordinary SSH session
accounting may occur. No package operation, needrestart scan, service action,
cache/swap modification, reboot, message, DNS/Caddy contact or deployment is included.
On failure preserve partial evidence and stop. There is no target configuration
to roll back; timeouts bound collection, and loss of transport may leave final
completion unobserved. Additional inspection requires separately scoped authority.

Local qualification: seven synthetic tests passed for field allowlisting, read
limits/missing files, hierarchy and enumeration bounds, process bounds with no
argument collection, output limit, identity rejection before collection and the
complete three-sample fixture path. Host-key lookup and source hash checks passed;
archive-to-tree equality and all declared hashes passed; candidate secret scan
found no leaks. These tests did not contact the Pi or establish its current state.
Private test source/log and qualification metadata are retained beside the bundle.

Approval is required by [the owner policy](../../../homelab-server-configs/AGENTS.md#definition-and-authorization):
"A definition-only task must not contact a live target unless the user has
explicitly requested or authorized a read-only inspection." The current request
is preparation. The change-control skill adds no additional approval gate.

### Approved host-memory attribution outcome — November 10, 2026

Aaron approved the exact preceding bundle, command and scope. Archive, manifest,
all four inputs and archive-to-tree equality were checked before the single attempt.
Bundle SHA-256 `88ef942a560b3bf71dc6c718e701694336ea9877f78a572647bdebfe42fc4b2c`
ran at 21:44:46–21:45:07 America/Chicago (November 11, 03:44:46–03:45:07 UTC).
Exit 0; three snapshots completed in 20.33 seconds, empty stderr, no enumeration
truncation. Approval is consumed. Private authorization, terminal, JSONL, outcome
and SHA-256 evidence manifest are under
`/home/aaron/code/.local-evidence/uptime-kuma/host-memory-attribution-ydppox2d/execution/`.
No package, scan, service, cache, swap, boot or configuration action occurred.

| Sample | MemAvailable before (KiB) | After (KiB) | Capture seconds |
| --- | --- | --- | --- |
| 1 | 744596 | 744144 | 0.197 |
| 2 | 743368 | 743368 | 0.247 |
| 3 | 743368 | 743368 | 0.234 |

Availability ranged 725.95–727.14 MiB; minimum margin above 720 MiB was 6088 KiB
(5.95 MiB). This is the approved standalone Python/SSH collector, not the actual
Ansible admission task. It cannot overturn the earlier failed admission or justify
subtracting observer costs. Its own RSS grew from 12464 to 12624 KiB; RSS includes
shared pages and is not its unique host-memory cost. Observations across operations
remain evidence of variability, not a deterministic correction factor.

All samples enumerated 44 cgroups and 127–128 processes. The large system.slice
charge (about 546 MiB) comprised about 447.81 MiB file, 16.27 MiB anonymous and
79.13 MiB kernel memory, including about 75.38 MiB reclaimable slab. These are
hierarchical charges; kernel includes slab, and parent charges include children.
They are not independent quantities to add or a safely recoverable allowance.
The largest named service groups were NetworkManager (about 20 MiB), udev (16.21
MiB) and journald (9.94–10.19 MiB), with much of their charge in file pages.
Nothing here supports disabling network or core system services to pass admission.
File cache and reclaimable slab must not be added to MemAvailable as new headroom.

The radio-related service finding is tracked separately in W-076. Daemon presence
does not establish that either radio is enabled. Even their combined current
charges are smaller than the prior 11.34–14.12 MiB Ansible shortfalls; removal is
neither selected nor demonstrated to restore durable margin.

Selected VM reclaim/swap/OOM counters and readable cgroup memory.events did not
change across samples. Existing swap use remained 32 KiB. Host and cgroup PSI files
were absent; root cgroup interfaces and the udev child cgroup also had absent memory
files. The collector retained 62 missing-file entries per sample; none were hidden
or treated as zero pressure. Parent udev accounting and process fields remained
readable. No finite memory.max was present among readable groups. These gaps and
sequential reads prevent a claim of complete instantaneous memory attribution.

Application state readback matched exactly: four Kuma units inactive/dead,
Webmin failed/failed, all service MainPID values zero. No target files were staged,
so no artifact cleanup was required. The collector exited; no further contact was
made to inspect post-disconnection SSH accounting.

W-075 is resolved; W-069 and W-070 remain unresolved. No sufficient low-risk
capacity recovery is demonstrated. Preserve the 720 MiB floor, service caps and
96 MiB reserve; do not seal a continuation or repeat admission merely to capture
a passing sample. The next capacity decision needs an owner-supported footprint
change or an explicitly reviewed host/design change. No new operation is authorized.

### Capacity decision review — November 10, 2026

Aaron confirmed **no other hosts are available**. A replacement-host review is
therefore not an actionable next step. The current target remains the Pi 3B+;
no inventory, address, foundation profile or accepted prerequisite was changed.

Local owner review covered the selected host inventory, foundation ownership,
Webmin small-host profile, network-owned Uptime Kuma configuration and fleet
radio references. The application preserves the network owner's radio-block
policy. No target-specific policy was found permitting removal or disabling of
Bluetooth or wpa_supplicant. Nautobot's host-baseline plan masks Bluetooth for
its own target and explicitly protects NetworkManager; this is not a fleet-wide
rule and does not cover wpa_supplicant. W-076 retains the unresolved dependency
review, but no radio-service change is proposed as the capacity solution.

| Option | Evidence and decision |
| --- | --- |
| Repeat admission or switch readers | Does not establish sustainable margin. Keep the unadjusted Ansible-path gate; no retry-until-pass operation. |
| Disable radio-related daemons | About 7.03 MiB combined current charge, much less anonymous charge, and unknown recoverable gain. This does not establish recovery of the earlier 11.34–14.12 MiB shortfalls, still less temporary observer allowance. No owner-supported target change selected. |
| Reclaim cache or trim core host services | Large file/slab charges are not additive free capacity. No demonstrated safe reclaimable gain; preserve NetworkManager, SSH and system services. No cache drops. |
| Reduce or omit required foundation services | Conflicts with current service scope unless explicitly revised. Webmin's package-query reduction is already part of the selected owner profile; it is not a new unclaimed saving. Keep all current caps and required components. |
| Move the deployment | No alternative host is available, per Aaron. No target selected or replacement inspection requested. |
| Change concurrency or capacity policy | A separate design decision, not a footprint fix under current requirements. On-demand Webmin or mutually exclusive maintenance could alter concurrent demand, but cannot satisfy or replace the unchanged 720 MiB gate by assumption. No such change selected or implemented. |

Decision: **hold deployment under the current requirements**. This is a limit of
the evidence and permitted remedies, not proof that Uptime Kuma cannot run on the
Pi. The recent isolated scan passed and some standalone readings exceeded 720 MiB;
neither accepts the actual Ansible admission workload or combined services.
The 32 MiB temporary observer allowance also remains an explicit integration
requirement, not a hidden reduction of the 96 MiB reserve.

W-077 is resolved. W-069 remains unresolved capacity work; W-070 remains the
combined-observation implementation/acceptance requirement. No additional live
inspection is the default next step. Resuming deployment requires either a newly
available suitable host or an explicit review of requirements/admission policy,
followed by local qualification and exact live authorization. Until then, preserve
the current stopped baseline, service limits, floor, reserve and consumed evidence.
No executable changes, new bundle, host contact or deployment occurred in this review.

### Concrete admission-policy proposal — November 10, 2026

The requested capacity/design review now has one recommended policy alternative
in [PLAN.md](PLAN.md#approved-staged-admission-policy--local-qualification-only).
It keeps the only available host and all required services, avoiding an unproven
radio-service remedy. Its thresholds follow stage allowances rather than selecting
a number just below a historical observation. It expressly changes the existing
720 MiB admission policy; this is not a claim that the old gate passed.

Reviewed source confirms an important production gap: Needrestart's current
`enable-schedule.yaml` applies a 96 MiB scope to the daily producer but does not
perform the proposed headroom admission/observation. Deployment-only observation
would therefore be insufficient. W-078 includes the guarded owner production
path and its distinct five-minute producer timeout; W-070 still owns all three
combined acceptance checkpoints. A skipped scan must remain a failed/deferred
operational check, not be reported as successful maintenance.

Systemd's primary resource-control documentation was consulted through Context7
(`/systemd/systemd`, `man/systemd.resource-control.xml`): MemoryHigh throttles and
reclaims, while MemoryMax is a hard limit whose breach can invoke unit OOM handling.
These mechanisms do not make the proposed sampled reserve an enforced reservation.
The proposal states the resulting burst risk and absence of a simultaneous-cap
guarantee rather than presenting this policy change as equivalent protection.

No executable input, architecture acceptance claim or consumed bundle was changed.
No target inspection or live action occurred. Decision agreement is needed because
this changes the acceptance policy previously retained by Aaron; the change-control
skill requires the user's agreement for changed acceptance or scope. This is a
policy decision before local implementation, not another deployment authorization.

### Staged policy approved for local implementation

Aaron explicitly approved the preceding 624/224/192/96 MiB proposal, unchanged
service caps and stated sampling tradeoff for local implementation/qualification.
This supersedes the old 720 MiB admission policy in new working definitions only;
consumed frozen operations remain unchanged and cannot be replayed. No target
contact, start, scan, reboot, schedule enablement or message is authorized.

### Staged admission implementation and local qualification — November 10, 2026

Implemented the approved policy in new working definitions. The startup receipt
and both startup admission paths now use 638976 KiB (624 MiB); tests exercise
below/at/above and malformed readings. The existing remaining-operation source
is marked preparing, invalidating its prior qualification claim. Its consumed
frozen bundle and every earlier archive remain unchanged.

The foundation owns one guard/observer. Both acceptance and the owner daily
schedule use it: 224 MiB before observer launch, fresh 192 MiB once resident,
then 96 MiB sampled host/finite-parent reserve. Nonblocking lock and unused-unit
checks refuse overlap or stale adoption. Failure, late sampling, missing evidence,
scan memory-limit/OOM events, invalid peak/no-swap state or unverified cleanup
cannot become acceptance. Native bounds stop the scan and observer; acceptance
fetches private receipts before assertion and existing application containment.

Scheduled mode invokes the actual notification producer, including its children,
inside the unchanged 96 MiB/no-swap/one-CPU unit. It preserves the internal
five-minute scan timeout plus 30-second kill grace, adds a 420-second producer
unit bound, a 440-second observer bound and a 470-second cron command bound.
This is deliberately distinct from the 90-second list-only acceptance scan.
The existing cron flock, Mailrise recipient and failure transport are preserved.
Refused/failed runs are nonzero; successful runs remain quiet. Only verified
terminal cleanup permits scheduled temporary-directory removal; cleanup failure
retains evidence. No schedule or notification was activated on the Pi.

All three combined checkpoints reach the shared owner scan task through existing
foundation imports. Restore now requires fresh 416 MiB after the source stops
(320 MiB replacement + 96 reserve); ingress requires fresh 160 MiB (64 MiB client
plus 96 reserve). These checks retain raw readings before assertion. Execution order
keeps these transients separate from scans and enables the daily schedule last.
Native lifetime, service health/pressure checks, restore cleanup and application
containment remain required; stage admission is not continuous host protection.

Private qualification: `/home/aaron/code/.local-evidence/uptime-kuma/staged-admission-zg_oesm1/`.
`qualification.json`, `source-hashes.json`, complete logs, fixture scripts and
native receipts retain the tested inputs and limits. Validation:

- 41 tests passed, including actual localhost Ansible startup gate execution and
  rendering of the real cron expression; five playbook syntax checks passed.
  ShellCheck, canonical shell format, readonly/local collision, YAML, Markdown
  and whitespace checks passed for the affected inputs.
- In a disposable AMD64 systemd fixture with no network, 720 MiB parent cap and
  no swap, the final real installed needrestart scan passed. Exact peak was
  25317376 bytes (24.14 MiB); maximum observed sample gap was 0.217 seconds.
  Host MemAvailable was not mistaken for the fixture's finite parent headroom.
- The actual producer and actual cron shell body passed with local scanner/mail
  substitutes. No real notification was sent. Producer failure, native scan OOM,
  finite-parent shortage and lock overlap were rejected with retained evidence.
- A real sleeping scanner was terminated by the native 90-second acceptance
  timeout; failure and owned cleanup were retained. Scheduled 420/440/470-second
  settings and producer execution were checked, but no seven-minute wall-clock
  soak is claimed. The timeout trial preceded only unrelated final CLI handling;
  its scan deadline/cleanup path was unchanged.
- The fixture was removed and all local execution sessions completed. The hardware
  coordinator was syntax checked, not executed end-to-end against a simulated Pi;
  actual ARM64 kernel, combined application load and notification route acceptance
  remain live gates. Discrete samples cannot exclude shorter dips.
- Application and isolated changed-source secret scans passed. The full server
  scan reported 16 entries, all verified as 64-hex generated file_hashes values in
  `.vexp/manifest.json`; no source suppression or blanket allowlist was added.
  vexp verification was unavailable because its session root is the parent
  workspace, not a Git repository; repository checks supply the validation here.

W-078 and the policy reconciliation in W-069 are resolved. W-070 remains in
progress for actual combined Pi observation; W-011 retains deployment acceptance.
The architecture, plan and operations now describe the approved staged policy
without rewriting historical outcomes. No new live bundle, target contact,
application start, reboot, schedule activation, message, commit or push occurred.

### Remaining deployment under staged admission — preparation approved

Aaron approved preparing the remaining-deployment candidate for review. This
approval covers local preparation and qualification only. It does not authorize
contact with the Pi or proxies, startup, a scan, reboot, or schedule activation.
W-079 owns preparation; W-070 still requires actual combined Pi acceptance.

The candidate uses the approved staged policy and unchanged service caps. It
requires a fresh unadjusted 624 MiB startup reading, 224 MiB before each observer,
192 MiB once the observer is resident, and a sampled 96 MiB reserve during scans.
All three combined checkpoints use the owner guard. Restore requires fresh
416 MiB after stopping the source; the ingress client requires fresh 160 MiB.
The daily producer uses the same guard and retains the distinct production
420/440/470-second bounds, fleet recipient, failure reporting and cron lock.
No assumed observer add-back, cache manipulation, averaging or admission retry
is included. Sub-sample dips remain possible under the approved tradeoff.

The operation starts from the retained stopped baseline, but fresh target identity,
boot, package, source-hash, network, data and guard checks must pass before changes.
An unexpected existing fleet observer helper now refuses preflight. Existing
startup/containment paths must also be absent; this prevents adopting a prior
attempt. Consumed operations remain unchanged. No package/image installation,
boot-file correction or address mutation is repeated.

Proposed scope after preflight: install the owner scan helper and pending startup
controls, reapply the accepted Webmin profile, start existing Webmin/Kuma, run
combined acceptance, perform one reboot, and repeat acceptance. The operator then
has at most fifteen minutes to verify Kuma and Webmin logins privately and create
the acknowledgement described in the earlier operator instructions in this ledger.
The agent must not create that acknowledgement on the operator's behalf. No
password or session cookie belongs in chat or evidence. Monitors and alerts remain
empty. The independent forty-minute pending authority remains armed throughout.

The continuation then creates a consistent administrator-bearing backup and a
protected off-node copy, verifies isolated restore and source recovery, promotes
only the approved source-restricted backend, checks both families from
`pi@10.1.0.53` and `pi@10.1.0.54`, and tests ingress denial. The proxy nodes receive
read-only backend probes only. Combined acceptance runs again before enabling the
05:30 fleet daily Needrestart schedule and committing permanent startup authority.
Normal scheduled owner notifications are included after acceptance; synthetic
messages and Kuma notification/monitor activation are excluded.

Failure retains data, backups, packages and guards. Existing bounded containment
removes permits/schedule, stops owned application/probe units and prevents future
startup; the scan guard separately stops only its owned transient units. The
installed helper can remain as an inert owner artifact. If cleanup cannot be
verified or the Pi is unreachable, retain evidence/fallback and report manual
recovery; physical device, microSD and console access are available. Do not replay
this or any consumed bundle. DNS deployment, Caddy release/reload/failover, final
HTTPS acceptance and publication remain outside the operation.

Fresh private preparation: `/home/aaron/code/.local-evidence/uptime-kuma/remaining-staged-20261110-5i0l9c9t/`.
Evidence uses its protected `execution/` directory. Backup destinations are
`/var/backups/uptime-kuma/remaining-staged-20261110` on the Pi and
`/home/aaron/.local/state/uptime-kuma/backups/remaining-staged-20261110` on the
controller. Both require absence before creation. The restore workspace remains
under the exclusively owned remaining-deployment state directory.

The frozen source passed 41 tests and five playbook syntax checks, including real
localhost Ansible admission execution and cron rendering. Shell formatting,
ShellCheck and readonly/local collision checks passed. Retained native staged
qualification remains applicable: guard, producer and observer bytes match their
qualified source hashes. Its AMD64, finite-parent, no-network limitations and
scheduled-timeout qualification limits above still apply; no new native soak or
Pi acceptance is claimed. Consumed remaining-deployment, accepted correction and
latest attribution archives were rehashed unchanged. All three SSH identities
were found in the retained pinned known-hosts file without network contact.

### Staged remaining-deployment exact bundle, command and scope — approval required

Status: **sealed, not authorized; never executed**. The preparation approval is
consumed by preparation only and grants no live authority. This is the sole new
candidate; all historical operations remain consumed and cannot be replayed.
The preceding preparation section defines its targets, mutation scope, acceptance,
operator participation, failure containment and excluded later stages.

- Archive: `/home/aaron/code/.local-evidence/uptime-kuma/remaining-staged-20261110-5i0l9c9t/candidate/remaining-deployment.tar`.
- SHA-256: `e03e14dd7058dd58dee602d00eb719b3c2b799bf1dc1c5f4bedbc3f286252536`.
- Input-manifest SHA-256: `d8dcac5fb5703b5bf1a28ccb15972ac380ffa178c48fa9875016b29477c4f1fd`.
- Size: **931840 bytes**, **120 declared inputs** plus the manifest.
- Frozen root: `/home/aaron/code/.local-evidence/uptime-kuma/remaining-staged-20261110-5i0l9c9t/candidate/bundle`.
- Operation: `uptime-kuma-remaining-staged-20261110`.
- Evidence destination: `/home/aaron/code/.local-evidence/uptime-kuma/remaining-staged-20261110-5i0l9c9t/execution` (0700, empty).

Exact proposed command, from that frozen root:

```bash
ANSIBLE_CONFIG=./ansible.cfg \
  /bin/bash repositories/homelab-server-configs/tests/repository/run-with-ansible-local-temp.sh \
  ansible-playbook \
  -i repositories/homelab-monitoring-observability/uptime-kuma/ansible/inventory.yaml \
  repositories/homelab-monitoring-observability/uptime-kuma/ansible/remaining-deployment.yaml
```

Approval would authorize **one attempt** on `ama@10.1.3.75`, including one planned
reboot, private operator login/setup, normal daily owner schedule activation after
acceptance, and the bounded backend probes on the two named proxy nodes. A fresh
startup reading below **624 MiB** refuses before changes. Every later stage has
its own specified admission/acceptance checks; a failed gate is not retried.
DNS/Caddy changes, final HTTPS, package/image operations, synthetic messages,
Kuma monitors/alerts and publication remain unauthorized.

Frozen controller preflight ran with explicit localhost-only inventory and the
controller-preflight tag: eight successful tasks, zero changes, zero failures;
both production plays had no matching hosts. Archive members, modes and bytes
match the verified input manifest exactly. The bundle secret scan passed. The
separate application working-tree scan found one generated `.vexp/manifest.json`
file hash, independently checked as a 64-hex value under `file_hashes`; no source
credential or suppression was added. Full receipts and terminal session records
are in private `qualification/`; no live receipts exist. The frozen ledger is the
pre-seal preparation snapshot; this working ledger records the resulting seal.

The [repository authorization policy](../../../homelab-server-configs/AGENTS.md#definition-and-authorization)
requires approval of this exact bundle, command and scope before live mutation.
The change-control skill adds no separate gate. No live authorization has been
received for this candidate.

### Staged remaining-deployment authorization received

Aaron explicitly approved the exact bundle, command and scope above, including
one reboot and private operator login verification. Archive and every input were
reverified unchanged immediately before execution. This authorizes one attempt;
no consumed operation may be replayed. Authorization is retained in the private
execution directory. Live acceptance is pending.

### Staged continuation checkpoint — operator login pending

The approved command was launched once; session 1671 owns the running process.
The 624 MiB startup gate passed at 721464 KiB (704.55 MiB). Fresh installed-state
and accepted-prerequisite checks passed. Pending startup controls were armed,
Webmin/Kuma started and the one planned reboot completed. No boot/address
correction or package/image action was repeated.

Combined before/after-reboot acceptance passed. The guarded scans observed
minimum host availability of 561620 and 566140 KiB respectively; native scan
peaks were 43114496 and 43937792 bytes. Maximum sample gaps were 0.257 seconds
or less; both scan/observer cleanup receipts passed. Post-reboot Kuma recorded
eight memory.high events with no increase across the settling window; no
max/OOM events were observed. This satisfies the sealed settling check and does
not establish absence of earlier throttling or capacity for future monitors.

Execution is waiting at the bounded private operator login checkpoint. The
operator received tunnel, browser and acknowledgement instructions; no credentials
are requested. Backup/restore, backend promotion, final combined acceptance and
schedule activation remain pending. Do not launch a second operation or manufacture
the operator acknowledgement. The persistent pending-authority deadline remains
armed; preserve the existing process and receipts across any handoff.

### Staged remaining-deployment terminal outcome — November 10, 2026

The exact approved command ran once from 22:35:16 to 22:56:58 America/Chicago
and exited 2. Approval is consumed. Ansible reported Pi ok=127, changed=37,
unreachable=0, failed=1, rescued=1; controller ok=8, changed=0, failed=0.
The frozen archive and executable inputs remain unchanged. Private
`execution/outcome.json`, `ansible.log`, `containment.json` and `EVIDENCE.sha256`
retain the result and receipt identities. Session 1671 completed and is retired.

Startup admission, accepted prerequisites, installed-state checks, service startup,
one reboot and before/after-reboot combined scan acceptance passed as recorded
above. Aaron initially attempted browser access from the headless-host context;
workstation tunnel/browser instructions were clarified. He then reported creating
the Kuma login and logging into Webmin. No credentials were collected. The
required root-owned operator acknowledgement file did not arrive within the
903-second wait, so the independent administrator-bearing acceptance gate was
never reached. W-080 records this handoff failure; it is not a new capacity failure.

The sealed rescue ran and independently verified containment: Kuma/network/proxy
units inactive, Webmin failed with MainPID=0 and disabled, no application TCP/UDP
listeners or Podman containers, original guards intact, permits absent, and no
Needrestart cron schedule. Startup state is contained with reboot_count=1 and
boot ID `d8ea7780-d747-458e-b5fd-d6eda6cfa009`. Data, packages and definitions were
preserved. This is containment, not reversal of the installation or deletion of
the operator-created account. Any late acknowledgement grants no startup authority.

Backup/off-node copy/restore, backend promotion, both proxy probes, ingress denial,
third combined scan, schedule activation and permanent startup acceptance were
not reached. No DNS/Caddy change, synthetic notification, monitor/alert activation
or publication occurred. W-070 remains in progress for the final combined
checkpoint; W-011 and AC-005/007/011 remain incomplete. The user was told not to
create the acknowledgement after expiry. No further live action is authorized.

A future continuation must account for the retained startup-control artifacts,
changed boot ID and operator-reported administrator data; the old empty-data and
absent-control preconditions no longer apply. Preserve this attempt and the
accepted reboot evidence, resolve the operator handoff and qualify the remaining
work before requesting a new exact-bundle authorization. Do not reset the account,
remove data or repeat the reboot merely to satisfy a consumed preflight.

### Administrator completion preparation authorized

Aaron subsequently confirmed the acknowledgement was created after the timed
attempt ended. This is a human confirmation of both logins, not retroactive
acceptance or startup authority. Its live presence is unverified. The new request
authorizes local preparation from the contained state, preserving administrator
data and the completed reboot. W-081 owns the new candidate; W-080 remains open
until the revised handoff is qualified and actual administrator acceptance passes.

### Administrator-bearing completion candidate — local qualification

The new working definition reuses the remaining-deployment coordinator in
`resume_contained` mode. It preserves the consumed archive and accounts for the
changed boot identity and retained startup controls. Fresh preflight requires the
original contained state's fields, root-owned protected control files and exact
source hashes, the operator-created acknowledgement, and a stopped healthy database
with active administrator, authentication enabled and no monitors/notifications.
Only `contained_at` may advance when the old deadline invokes containment again;
no other predecessor field may differ. Symlinks, wrong modes, drift or missing
acknowledgement refuse before service changes. No credentials are read into logs.

The frozen command will stop the verified old timer/containment service, renew the
forty-minute pending authority once using the fresh state hash, and preserve the
original state bytes in exclusive `previous-state.json`. Intervening state drift
or an existing predecessor archive refuses renewal. The retained boot count stays
one; another pending reboot is refused. Account setup, reboot and the timed login
wait are skipped. The human login confirmation is retained, while actual active
administrator/authentication configuration must pass both stopped preflight and
running application acceptance. The acknowledgement is never created by the agent.

Proposed remaining scope: guarded existing-service start, current runtime and
combined foundation/scan acceptance, consistent administrator-bearing backup and
protected off-node copy, isolated restore and source recovery, source-restricted
backend promotion, both proxy probes, ingress denial, final combined scan and
owner daily schedule activation, then permanent startup acceptance. All stage
floors, resource caps, no-swap settings and containment boundaries are unchanged.
There is no additional operator timer or reboot. A failed stage stops the attempt;
there is no capacity retry, account reset, data deletion, package/image action,
DNS/Caddy mutation, synthetic notification, monitor/alert activation or publication.

New private preparation: `/home/aaron/code/.local-evidence/uptime-kuma/administrator-completion-20261110-giwtjnmy/`.
Evidence uses its protected `execution/` directory. New backup destinations are
`/var/backups/uptime-kuma/administrator-completion-20261110` and
`/home/aaron/.local/state/uptime-kuma/backups/administrator-completion-20261110`;
both must be absent before creation. Existing application data is never replaced.
The restore workspace stays within the original owned continuation directory.

Local qualification exercised the actual startup helper and native systemd
startup/containment templates in an isolated AMD64 fixture with no network and a
720 MiB/no-swap parent limit. It passed protected-acknowledgement validation,
advanced old containment time, wrong acknowledgement/mode/symlink refusal,
contained-state refusal, wrong predecessor hash, preserved original state,
renewal replay refusal, native startup grant, second-boot refusal, acceptance,
accepted expiry-service no-op and native containment-service failure cleanup.
Application services were harmless substitute units, not an actual Pi deployment.
No physical reboot, full forty-minute wall-clock expiry or end-to-end application
completion is claimed. The fixture was removed; complete private logs remain.

The existing local suite passed after implementation; the added SQLite regression
checks active-user/authentication/workload requirements without modifying the
inspected database. Routing regression checks that completion skips all seven
reboot/setup/wait tasks while retaining administrator acceptance and backup.
Final frozen-source checks and controller integrity are recorded with the seal.
vexp verification remains unavailable because its session root is the parent
workspace, not a Git repository. No target contact or live authority occurred.

### Administrator-completion exact bundle, command and scope — approval required

Status: **sealed, not authorized; never executed**. This is the sole new candidate.
The consumed staged attempt and all earlier archives remain unchanged. Local
preparation approval does not authorize target contact or startup.

- Archive: `/home/aaron/code/.local-evidence/uptime-kuma/administrator-completion-20261110-giwtjnmy/candidate/remaining-deployment.tar`.
- SHA-256: `7c64d7047d55b5aeade840412a3595a7f91ca775bd14ff584a8b68e8dd28b28b`.
- Input-manifest SHA-256: `9eed0c9b41b8fe40fd48f2eff750c159f0946e8f882b8c54e3422d0e9c0b0094`.
- Size: **962560 bytes**, **123 declared inputs** plus the manifest.
- Frozen root: `/home/aaron/code/.local-evidence/uptime-kuma/administrator-completion-20261110-giwtjnmy/candidate/bundle`.
- Operation: `uptime-kuma-administrator-completion-20261110`.
- Evidence destination: `/home/aaron/code/.local-evidence/uptime-kuma/administrator-completion-20261110-giwtjnmy/execution` (0700, empty).

Exact proposed command, from that frozen root:

```bash
ANSIBLE_CONFIG=./ansible.cfg \
  /bin/bash repositories/homelab-server-configs/tests/repository/run-with-ansible-local-temp.sh \
  ansible-playbook \
  -i repositories/homelab-monitoring-observability/uptime-kuma/ansible/inventory.yaml \
  repositories/homelab-monitoring-observability/uptime-kuma/ansible/remaining-deployment.yaml
```

Approval would authorize **one attempt** on `ama@10.1.3.75`, plus read-only backend
probes from `pi@10.1.0.53` and `pi@10.1.0.54`. Scope includes the preceding
preflight, controlled renewal/startup, current combined scan acceptance,
backup/off-node copy/restore, backend promotion and ingress checks, final combined
scan, normal owner daily notification schedule activation, permanent startup
acceptance and bounded failure containment. It includes **no reboot, account
setup or timed private login handoff**. The existing protected acknowledgement
must validate; the agent must not create or repair it to bypass that gate.

Fresh unadjusted floors remain 624 MiB before startup, 224/192 MiB before the
observer/scan, sampled 96 MiB reserve, 416 MiB for source-stopped restore and
160 MiB for ingress. Caps, no-swap and failure rules remain unchanged. On failure,
preserve administrator data, backups, guards and predecessor state, stop owned
services/probes and remove permits/schedule. No replay or automatic re-renewal.
If containment is unreachable/unverified, retain the fallback and report physical
recovery requirements. DNS/Caddy changes, final HTTPS, package/image actions,
synthetic messages, Kuma monitors/alerts and publication remain excluded.

Final frozen qualification: **43 tests**, **five syntax checks**, native AMD64
helper/control lifecycle, actual localhost Ansible rendering of all three
predecessor unit templates with matching expected hashes, ShellCheck, shell
format and collision policy passed. Controller-only frozen preflight passed
with eight successful tasks, zero changes and zero failures; production plays
had no matching hosts. Archive members, modes and bytes match the manifest.
The bundle secret scan passed. The separate working-tree scan reported one
generated 64-hex `file_hashes` value in `.vexp/manifest.json`, independently
verified; no credential or suppression was added. Native limitations are stated
above; actual Pi application completion remains untested. The fixture was removed
and all local sessions ended. No live evidence exists.

The frozen ledger is the pre-seal preparation snapshot; this working ledger
records the resulting seal. Private `candidate/candidate.json`, qualification
logs, source hashes and evidence manifest bind these results to the candidate.
The [repository policy](../../../homelab-server-configs/AGENTS.md#definition-and-authorization)
requires exact-bundle authorization for live changes. No such authorization has
been received for this candidate.

### Administrator-completion authorization received

Aaron approved the exact bundle, command and scope above for one attempt. Archive,
manifest, all input bytes and archive modes were reverified unchanged before launch.
The private execution authorization binds this approval to the sealed archive.
No consumed attempt is replayed; current live acceptance remains pending.

### Administrator-completion terminal outcome — November 10, 2026

The exact approved command ran once from 23:16:55 to 23:23:01 America/Chicago
and exited 2. Approval is consumed. Pi recap: ok=135, changed=43, unreachable=0,
failed=1, rescued=2; controller ok=8, changed=0, failed=0. Session 52514 ended and
is retired. The archive and executable inputs remain unchanged. Private
`execution/outcome.json`, `proxy-probes.json`, `restore-receipt.json`,
`containment.json`, full `ansible.log` and `EVIDENCE.sha256` bind the result.

Fresh preflight verified the protected late acknowledgement, contained authority,
retained boot ID and administrator-bearing database. Startup admission passed at
746060 KiB (728.57 MiB). One-time renewal preserved the predecessor; no reboot,
account setup or timed login wait was repeated. Running administrator acceptance
and combined foundation/scan acceptance passed. The scan's minimum sampled host
availability was 562188 KiB, peak 15585280 bytes, maximum sample gap 0.257 seconds
or less, with verified transient cleanup. No observer overhead was subtracted.

The consistent administrator-bearing backup, protected matching off-node copy,
actual isolated ARM64 restore, extracted-data/container cleanup and source
recovery all passed. Restore found one active user, no monitors/notifications and
authentication enabled. The 307200-byte controller backup remains mode 0600 at
`/home/aaron/.local/state/uptime-kuma/backups/administrator-completion-20261110/data.tar`;
its SHA-256 was independently rechecked against the retained restore receipt after
execution. The archive was not opened or copied into chat or repository evidence.
W-009 and W-080 now have actual acceptance evidence.

Promoted runtime checks passed, then both proxy nodes reached the backend over
both address families and returned HTTP 302. The explicit 200-only assertion
failed. Sources were 10.1.0.53 / fd36:5aa8:6971:1::56 and
10.1.0.54 / fd36:5aa8:6971:1::54. No Location header or redirect destination was
retained, so do not claim an expected login/dashboard redirect or simply widen
acceptance without qualification. W-082 tracks that contract.

Promotion rescue stopped Kuma and restored the loopback-only Quadlet, but the
restart failed because native start-rate protection rejected another start.
The recovery runtime check therefore did not pass. Outer rescue independently
verified all five owned units stopped (Kuma/Webmin failed with MainPID=0), no
application TCP/UDP listeners or Podman containers, intact guards, absent permits
and schedule, disabled Webmin and contained startup state. W-083 tracks the
recovery gap. The account, backup, source definitions and predecessor-state
archive remain preserved; this is verified containment, not full rollback.

Ingress denial, final combined scan, daily schedule activation and permanent
startup acceptance were not reached. No DNS/Caddy mutation, synthetic message,
Kuma monitor/alert activation or publication occurred. The accepted reboot identity
is unchanged. Do not replay this command, reset rate limits or renew authority
again under consumed approval. A future candidate must reconcile both failures
and the new retained state/artifacts before requesting exact-bundle authority.

### Local proxy/recovery reconciliation — November 11, 2026

Scope was repository edits and disposable local qualification only. No SSH,
Pi/proxy access, live start, reset-failed, reboot, DNS/Caddy change or replay
occurred. The consumed archive, account, administrator backup and predecessor
records were not modified. No new continuation or approval command is sealed.

Private evidence is under
`/home/aaron/code/.local-evidence/uptime-kuma/proxy-recovery-reconcile-lr7p1nco/`.
`qualification.json`, `input-hashes.json` and `EVIDENCE.sha256` bind the tested
working inputs, results and fixture identities. The two network-isolated local
containers used synthetic data and were removed with their anonymous volumes.
No live backup was opened. All shell sessions are terminal.

**Proxy contract.** The cached pinned AMD64 Kuma 2.5.9 image
`sha256:1bf189bcd6286c24facc94dcd12565b09e1cf0bdd523d3dc8852f6646be49c29`
contains an explicit root redirect to `/dashboard` when no status-page entry is
selected. After creating a synthetic administrator through the application's
setup event, both loopback families returned root 302 with `Location: /dashboard`
and direct dashboard 200. See `pinned-routing.txt`, `claimed-http.log` and
`candidate-probe.jsonl`. The first synthetic setup request raced server readiness
and timed out; waiting for its setup-ready event succeeded. This does not recover
the missing Location headers from the Pi's previous attempt or establish ARM64,
proxy-source, browser login, HTTPS or WebSocket acceptance.

The working probe now requests the fixed `/dashboard` path and never follows a
redirect. The coordinator still requires 200, exactly two response records,
correct family/path/backend, and admitted per-family source addresses. A 302 is
still rejected. This gate establishes backend HTTP reachability only; the separate
administrator/authentication, ingress, runtime and eventual HTTPS/WebSocket gates
remain required. Regression tests exercise real IPv4/IPv6 curl requests, refusal
to follow/accept redirects, server errors and source/backend/path/family mismatch.

**Recovery contract.** Existing native limits remain three starts per 300 seconds,
with Restart=on-failure and a ten-second restart delay. The continuation's initial
start, source restart after backup/restore and backend promotion use three planned
starts; rescue previously requested a fourth. Fast completion can exhaust the
burst without any crash loop. Automatic failures can consume additional starts;
the candidate must fail into containment if any planned start is refused, without
resetting counters, waiting for a passing sample or raising the limit.

A network-isolated systemd 257.13 fixture with enabled, target-referenced units
reproduced the fourth-start refusal (`Result=start-limit-hit`, MainPID=0).
The otherwise identical stop/reload-only recovery stayed inactive with MainPID=0.
See `native-rate.json`. The first test lacked an active target reference, allowing
unit garbage collection to discard rate history; it did not reproduce the limit.
Its source is retained as `native-rate-first.py`; the corrected fixture matches
installed-unit retention. Native tests use sleep services, not actual ARM64 Kuma
or a full Ansible deployment, and do not measure Pi timing or capacity.

For remaining-deployment only, promotion rescue now stops Kuma, restores and
reloads the loopback-only definition, then fails into the existing outer rescue.
That rescue revokes permits and independently verifies all owned units, listeners,
containers and schedule are contained. It does not start Kuma to prove availability
immediately before shutting it down again. The legacy initial-deployment path keeps
its existing loopback recovery behavior; it is not selected for this continuation.
The new routing regression checks the stop/restore/fail boundary and the outer
containment import. No guards, resource caps, reserve floors, native rate limits
or accepted reboot requirements changed.

The focused suite passed 47 tests, all five Ansible syntax checks, shell formatting,
ShellCheck and the readonly/local-variable collision policy. Working-tree secret
scan, focused document/YAML lint and final hash/cleanup checks are recorded in the
private qualification receipt. These changes are locally qualified inputs only;
W-082/W-083 remain pending actual successor acceptance. W-084 records the necessary
one-time renewal redesign before any successor is sealed. Ingress denial, final
combined scan, daily schedule, permanent startup and DNS/Caddy HTTPS remain pending.

### Backend-completion successor preparation — November 11, 2026

Aaron requested local preparation of the successor preserving both predecessor
records. No live action is authorized. Operation
`uptime-kuma-backend-completion-20261111` uses retained terminal evidence from the
consumed administrator-completion archive; its exact archive is preserved.
Private preparation is under
`/home/aaron/code/.local-evidence/uptime-kuma/backend-completion-20261111-nin6u10h/`.

The successor requires the same accepted boot, contained administrator-bearing
state, existing operator acknowledgement, guarded stopped runtime and package
pins. It checks the original `previous-state.json` hash against the failed
completion's predecessor field, preserves that file and exclusively creates
`completion-state.json` from the freshly hashed failed completion state. The
new pending state references both hashes and preserves reboot_count=1. Existing
successor archives, state drift, wrong hashes, unprotected files, symlinks or a
consumed successor refuse renewal. The old timer may only advance contained_at;
intervening changes after preflight fail closed. No reset-failed or counter
adjustment is included. Final acceptance/containment rechecks both archives.

The previous administrator backup remains at its original node/controller paths,
with SHA-256 `e8d953730b3a5bbaa6fc1c3d4b7efee1d841b3cac8a660b219375e6aca275ead`.
Controller preflight verifies its protected bytes/size without extracting it;
host preflight verifies the source archive. The new backup destinations use
`backend-completion-20261111`, are distinct from the retained originals and must
not already exist. The existing backup/restore tasks remain responsible for a
fresh consistent archive, isolated restore, cleanup and source recovery.

Carry forward the fixed dashboard probe and stop-only promotion rescue qualified
in the preceding section. Resource caps/floors, ingress denial, both combined
scan checkpoints, owner daily notification schedule and permanent startup gates
remain unchanged. No package/image installation, reboot, account setup or timed
operator handoff is included. DNS/Caddy and final HTTPS remain separate.

### Backend-completion local qualification

The final frozen suite passed **48 tests**, **five Ansible syntax checks**, shell
formatting, ShellCheck and the readonly/local collision policy. Native systemd
qualification passed protected-acknowledgement handling, state drift and invalid
hash/mode/symlink refusal, preservation of both predecessor byte streams, exclusive
archive/replay refusal, guarded startup, second-boot refusal, acceptance and native
expiry containment. It used network-isolated AMD64 substitute application units;
it does not establish actual Pi timing, ARM64 completion, a new reboot or a full
forty-minute expiry soak. The previous pinned-image HTTP and native rate-limit
qualifications remain bound through their retained evidence.

The consumed predecessor's actual control templates were rendered with its retained
deadline using localhost Ansible; all three hashes matched successor preflight.
All frozen fleet-owner inputs match the previous qualified bundle. The trusted
private known_hosts payload is reused unchanged. Final controller-only preflight
passed ten tasks with zero changes/failures, including the protected accepted
backup hash/size. Only localhost was in its inventory; production plays had no
matching hosts. The native fixture was removed and all sessions ended.

Local preparation failures are retained privately: the first graph copy expected
the private SSH payload in the working tree; rebuilding then encountered readonly
staging copies. Neither produced a runnable candidate. Ansible refused an implicit
localhost selection, and later rejected undeclared test-generated bytecode. The
completed staging graph reuses the preserved private payload; exactly those six
bytecode files were removed, without changing tested source. Final integrity ran
with bytecode disabled against the sealed graph. No live retry occurred.

Focused Markdown/YAML checks and the working-tree secret scan passed. The bundle
scan flagged one source-hash value in `provenance/renewal-source-hashes.json`;
independent recomputation confirms it is the SHA-256 of
`verify-startup-authority.yaml`, not a credential. No suppression was added.
The source manifest, private test logs, native receipt and scan review are retained
in `qualification/`. The frozen ledger is the preparation snapshot; this working
ledger records the final seal and pending approval.

### Backend-completion exact bundle, command and scope — approval required

Status: **sealed, not authorized; never executed**. This is the sole successor
candidate. Earlier approvals and archives remain consumed and unchanged.

- Archive: `/home/aaron/code/.local-evidence/uptime-kuma/backend-completion-20261111-nin6u10h/candidate/remaining-deployment.tar`.
- SHA-256: `7824e4df0c13929baa6fcac0a78faada36b3100942131a8d314a9c92030882af`.
- Input-manifest SHA-256: `d2914e06394f4df1ea8ebbe53530a7d13fcdd25d45474b10870d40e99ba65088`.
- Size: **890880 bytes**, **125 declared inputs** plus the manifest.
- Frozen root: `/home/aaron/code/.local-evidence/uptime-kuma/backend-completion-20261111-nin6u10h/candidate/bundle`.
- Operation: `uptime-kuma-backend-completion-20261111`.
- Evidence destination: `/home/aaron/code/.local-evidence/uptime-kuma/backend-completion-20261111-nin6u10h/execution` (0700, empty).

Exact proposed command, from that frozen root:

```bash
PYTHONDONTWRITEBYTECODE=1 ANSIBLE_CONFIG=./ansible.cfg \
  /bin/bash repositories/homelab-server-configs/tests/repository/run-with-ansible-local-temp.sh \
  ansible-playbook \
  -i repositories/homelab-monitoring-observability/uptime-kuma/ansible/inventory.yaml \
  repositories/homelab-monitoring-observability/uptime-kuma/ansible/remaining-deployment.yaml
```

Approval would authorize **one attempt** on `ama@10.1.3.75`, plus read-only backend
probes from `pi@10.1.0.53` and `pi@10.1.0.54`. It covers exact preflight, one-time
successor renewal preserving both predecessor records, guarded service startup,
current combined scan acceptance, fresh backup/off-node copy/isolated restore,
backend promotion with direct dashboard HTTP 200 and source/backend verification,
unapproved-source ingress denial, final combined scan, normal owner daily
notification schedule activation, permanent startup acceptance and bounded failure
containment. The accepted administrator backup and original predecessor remain
unchanged; new archives use unused `backend-completion-20261111` destinations.

No reboot, account setup or timed login handoff is included. The existing protected
acknowledgement must pass; do not create or repair it to satisfy preflight. Resource
floors remain 624 MiB before startup, 224/192 MiB for observer/scan admission,
96 MiB sampled reserve, 416 MiB for source-stopped restore and 160 MiB for ingress.
Caps, no-swap, native three-start/300-second limits and failure rules are unchanged.
A refused start terminates into containment; no reset-failed, wait/retry to obtain
a passing sample, automatic renewal or replay is authorized.

Promotion failure stops Kuma, restores/reloads its loopback-only definition and
enters the existing outer containment without a fourth recovery start. Preserve
data, both predecessor records and backups; stop owned units/probes, remove
permits/schedule and independently verify stopped containment. If unreachable or
unverified, retain the fallback and report the physical-recovery requirement.
Package/image actions, DNS/Caddy mutation, final HTTPS, synthetic messages, Kuma
monitors/alerts and repository publication remain excluded. No live authority has
been received for this sealed successor.

### Backend-completion authorization received — November 11, 2026

Aaron confirmed approval for one execution attempt of the exact sealed bundle
and scope above. Archive, manifest, input bytes and archive modes were reverified
unchanged before launch. The private execution authorization binds this approval
to the seal. This does not renew any earlier consumed operation.

### Backend-completion terminal outcome — November 11, 2026

The exact approved command executed once from **01:00:13 to 01:07:41
America/Chicago**, exited **0**, and consumed its approval. Pi recap: ok=180,
changed=54, unreachable=0, failed=0, skipped=47, rescued=0. Controller: ok=10,
changed=0, failed=0. Session 28875 ended and is retired; no live session remains.
Private `execution/outcome.json`, full `ansible.log`, response/acceptance receipts
and `EVIDENCE.sha256` retain provenance. No new reboot or private login handoff
occurred. The accepted boot ID and reboot_count=1 remain unchanged.

Preflight verified the accepted packages, guarded stopped runtime, predecessor
control files, protected operator acknowledgement, original predecessor archive
and prior administrator backup. Startup admission measured **732600 KiB**, above
the unchanged 638976 KiB gate. The old timer had advanced contained_at; the fresh
hash was bound before renewal. The successor preserved `previous-state.json`,
archived the actual failed-completion state as `completion-state.json`, and
independent final verification checked both hashes and protected files.

Both combined service checkpoints and scan-time observations passed. Minimum
sampled host availability was **554968 KiB** at initial combined acceptance and
**566808 KiB** after promotion; native scan peaks were **15634432** and **15409152
bytes**, with maximum sample gaps below **0.257 seconds**. Scan cleanup passed.
Kuma, Webmin and the loopback proxy retained their configured caps/no-swap, with
zero observed high/max/OOM events at the combined checkpoints. These are bounded
sampled observations for the empty-monitor workload, not continuous headroom or
future-load guarantees.

A fresh consistent administrator-bearing backup and isolated pinned ARM64 restore
passed, including extracted-data/container cleanup and restarted source acceptance.
The new controller archive is
`/home/aaron/.local/state/uptime-kuma/backups/backend-completion-20261111/data.tar`,
307200 bytes, mode 0600, SHA-256
`81d1eadde467c476e48d45c00ae8d0fb365639666fc40643cd0036b74fb11a32`.
Its hash was independently rechecked after execution. The previous 307200-byte
administrator-completion archive also remains mode 0600 with its original hash.
Neither archive was extracted or copied into repository/chat evidence during
receipt reconciliation. Restore/runtime checks found one active administrator,
authentication enabled and no monitors/notifications.

Both approved proxies returned **HTTP 200 for /dashboard over both families**.
The actual source/backend identities passed the sealed assertions; complete rows
were extracted from the native log into `proxy-probes.json` with its log hash.
Unapproved-source HTTP timed out over both families while SSH remained reachable;
IPv4/IPv6 denial counters rose by 6/3 and the temporary client was removed.
The prior 302 and rate-limit failures remain in their consumed attempt records.
No failure recovery or counter reset was needed in this successful attempt.

The reviewed guarded daily needrestart notification schedule was installed after
final combined acceptance. Mailrise remains the fleet default. SMTP acceptance
used greeting/QUIT only; no synthetic message was sent and downstream delivery is
not claimed. Vendor watchdog policy and unrelated foundation inputs were preserved.
All five owned application/network/proxy/Webmin units were independently active,
startup state was accepted, guards/dependencies remained present, and the pending
containment timer was inactive/disabled. Permanent startup acceptance is complete.

**Service foundation and guarded backend accepted; overall project remains partial.**
DNS/Caddy deployment and final trusted dual-stack HTTPS/WebSocket acceptance were
not authorized or performed. W-020/W-076 and permanent-document closeout remain
tracked. Do not replay this consumed command or treat it as authority for Caddy,
DNS, additional diagnostics, synthetic messages, monitors/alerts or publication.

### DNS/Caddy preparation — November 11, 2026

The [onboarding contract](PLAN.md#dnscaddy-onboarding-contract) records all Caddy
review fields, the six-record DNS addition, private acceptance and owner recovery
boundaries. It is proposed, not a production approval. Existing production
configuration, accepted manifests, consumed bundles and the running Pi were
untouched. The Caddy stream remains clean with its operation inactive.

The proposal previously checked root `/` for 200. W-085 corrects it to the actual
accepted `/dashboard` response. Candidate fragment SHA-256:
`85602544e70c276a25ab11063366c55ac57c298ef0a0887d6b635d3fe45fd016`.
Native Caddy 2.11.4 adaptation passed for both node environments in the existing
immutable qualification image, network disabled. Parsed output independently
requires one Kuma proxy with `/dashboard` and exact 200. This proves syntax and
the rendered health contract, not client trust, authentication or WebSockets.
The six DNS additions are unchanged; retained Unbound qualification is reused.
No additional DNS fixture or simulated failover test was created.

Private evidence and the sealed readiness candidate are under
`/home/aaron/code/.local-evidence/uptime-kuma/proxy-onboarding-20261111-obvrdg2j/`.
`qualification-status.json`, stdout/stderr and `local-checks.json` retain local
results. Readiness collector/remote payload Bash syntax, ShellCheck, format and
readonly/local collision checks passed. Invalid arguments and an already-used
evidence directory fail before SSH. No live acceptance is claimed.
Working-tree Gitleaks passed. Markdown and whitespace checks passed after
removing an extra blank line introduced with the new ledger rows. vexp completion
verification was unavailable because its session remains the parent workspace,
not a Git repository; focused native and repository checks provide validation.

W-020 remains owned by the network/runtime boundary. Required addresses/routes
passed accepted startup and reboot checks; timed RA renewal remains unqualified.
Do not change NetworkManager, forwarding or accept_ra as part of onboarding.
W-076 remains host/network ownership review: the initial baseline had wlan0
DOWN/no addresses, while later attribution showed radio-related daemons. Neither
proves persistent radio disablement. No target-specific disable profile or
verified dependency disposition was found in the retained owner review. Preserve
those services; do not treat their charges as a capacity remedy. Both findings
remain tracked here and require evidence or an explicit acceptance/deferral
decision before project closeout. DNS/Caddy success will not close them silently.

### Prepared read-only proxy readiness — subsequently approved and consumed

Missing inputs are public certificate hostname coverage, validity and matching
leaf/fullchain identity, plus effective health/notification timer intervals for
the required two-cycle authentication observation. The November 9 release-hash
inspection did not collect them. A release hash cannot supply their contents.

**Approve this exact inspection bundle, command and scope for one attempt.**

- Archive: `proxy-onboarding-20261111-obvrdg2j/readiness.tar` beneath the private
  evidence root above; SHA-256
  `f0e561b4b8b1a027d964f5e7ebf1c0a49e78318d502dbe4500757ef8d486f3b3`.
- Extracted manifest SHA-256:
  `a2ebc62a55852d2cedc63431320d907f0ee97cbe9f5d831850e81f4d3dcbb37e`.
- Collector SHA-256:
  `73c42f2f6438438c2250fa08cd1434cef61d2deb54e9cd4cb80f105d03b23436`.
  Frozen source and `scope.json` are in the protected `readiness/` directory.
- Targets: `pi@10.1.0.53`, then `pi@10.1.0.54`, existing SSH identity and strict
  host-key verification. One connection each; no retry; stop on first failure.
- Reads: hostname/time, selected release path and manifest-file hash; public
  leaf/fullchain certificate subject, issuer, dates, SANs, fingerprint, hostname
  and expiry checks; selected Caddy/Keepalived service status and Caddy health,
  certificate and notification timer timing properties; unchanged release pointer.
- Bounds: 70-second remote timeout and 90-second SSH timeout per node, with
  five-second kill grace. Node commands have additional bounded timeouts.
  Local evidence directory must be new; existing directory refuses replay.
- Excluded: private-key contents/hashes, certificate export, DNS inspection or
  changes, Pi access, authentication attempts, staging, publication, transfers,
  service transitions, reloads, failover, synthetic messages and automatic repair.
  Normal SSH/sudo access logging is expected; no remote helper file is installed.
- Review: verify exact hostnames and accepted release identity, both leaf
  fingerprints, hostname match/validity and complete timer properties. Exit zero
  means collection only. Missing data, mismatch, expiry or drift stops preparation
  for review; it never authorizes a certificate change or another attempt.

After archive/manifest/source verification, the exact command is:

```bash
bash /home/aaron/code/.local-evidence/uptime-kuma/proxy-onboarding-20261111-obvrdg2j/readiness/inspect-proxy-onboarding.sh /home/aaron/code/.local-evidence/uptime-kuma/proxy-onboarding-20261111-obvrdg2j/execution
```

This request follows the owner rule in
[server-configs AGENTS.md](../../../homelab-server-configs/AGENTS.md#definition-and-authorization):
"A definition-only task must not contact a live target unless the user has
explicitly requested or authorized a read-only inspection."
Historical approvals are consumed. This inspection would not approve the
proposed proxy contract or DNS/Caddy activation; the owner implementation,
authentication staging, causal recovery qualification and exact mutation bundle
remain to prepare after the missing inputs are resolved.

### Proxy-readiness terminal outcome — November 11, 2026

Aaron approved the exact bundle, command and scope above for one attempt.
Archive, manifest, frozen source and all archive members were verified unchanged
before launch. The approved command executed once and exited **0**. Remote
observations ran **09:53:19–09:53:20 America/Chicago** (15:53:19–15:53:20 UTC).
Both SSH commands exited 0 with empty stderr. No live session remains, and this
approval is consumed. No service/configuration mutation, DNS inspection, Pi
access, private-key collection, authentication attempt or message occurred.

Both expected hostnames and the selected immutable release matched retained
acceptance. Manifest-file SHA-256 remains
`8bf60cce81615c254262611ad7dde80cf5719e0b30f7679aade2f2556a11d22d`;
the selected release pointer was unchanged during each collection. This scope
hashed the manifest file, not the entire current payload.

Both nodes' public certificates include `*.local.theama.co` and
`local.theama.co`; hostname checks explicitly matched `uptime.local.theama.co`.
Validity is July 5, 2026 00:00:00 UTC through January 19, 2027 23:59:59 UTC,
covering the inspection time. All four leaf/fullchain readings share SHA-256
fingerprint `9480cfd689e5804a103ca192849e3ef5810b4e1c37918fbcc2815e864da5580c`.
No certificate replacement is indicated. This is public certificate metadata
acceptance, not a client TLS-chain/handshake test or final HTTPS acceptance.

Caddy and Keepalived were active/running on both nodes. All four inspected
Caddy timers were loaded, active and waiting; their associated oneshot services
were inactive/dead with Result=success at observation.

| Timer | Observed recurrence | Accuracy / randomized delay |
| --- | --- | --- |
| Pi-hole web health | 30s after unit becomes inactive | 2s / zero |
| Sync health | 1min after unit activation | 1min / 10s |
| Apprise worker | 1min after unit becomes inactive | 1min / 10s |
| Certificate expiry | Daily at midnight | 1min / 30min |

The inspected oneshot services report TimeoutStartUSec=infinity. Timer periods
alone therefore do not bound two completed checks. W-087 must qualify a bounded
acceptance observer that confirms actual completed applicable cycles and stops
on missing/late completion; a fixed 60-second sleep is not acceptance. Daily
certificate monitoring is distinct from the authentication-related health cycle;
run the owner's required certificate acceptance check only within a future
approved mutation operation. Do not send synthetic notifications.

Private `execution/review.json` records the independent hostname, certificate,
validity, release-identity and timer review. `execution/EVIDENCE.sha256` indexes
complete command outputs/statuses, and `authorization.json` records one consumed
attempt. All evidence remains beneath the sealed candidate's private root.
W-086 is resolved. W-007/W-087 retain owner implementation, staging, causal
recovery qualification and final HTTPS/authentication/WebSocket acceptance.
W-020/W-076 remain unchanged; no additional inspection is authorized.

### Onboarding acceptance clarification — November 11, 2026

Aaron approved the bounded acceptance alternative: repeated verified HTTP and
WebSocket checks across two Caddy health intervals, no health failures or
exclusions, and actual completed applicable systemd monitor cycles. PLAN.md
records this distinction. Native synthetic-credential staging and the owner
transaction remain local work; no new live authority is granted.

### Local onboarding implementation checkpoint — November 11, 2026

The neutral Caddy release transaction now has an application-fragment variant:
copy the accepted release, append only the hash-bound fragment, retain the full
TLS inventory, and preserve the installed publisher. Existing publication,
standby-first promotion and rollback are reused. No live application scope is
registered; the Caddy stream remains clean/inactive and no bundle is sealed.

The existing release regression passed 18 scenarios, including application
publication and failure rollback. Raw evidence is named by
`application-release-qualification.log` in the private Uptime evidence root.
Later cycle-observer changes require final graph qualification before sealing.

Synthetic Caddy 2.11.4/Kuma 2.5.9 staging passed both families in
`proxy-auth-6n0qr6q9`: trusted synthetic TLS, actual WebSocket authentication,
`authIncorrectCreds` rejection followed by immediate correct retry, protected
monitor-list access, usable second client, logout denial, and continued use
following 65 seconds. Monitors/alerts were not created. Both fixtures were
removed. Earlier fixture failures in `proxy-auth-u2j752lv` (unsupported tmpfs uid
option) and `proxy-auth-cq85kqz5` (missing explicit SQLite configuration) are
retained; both are corrected locally. Neither involved production.

Native systemd qualification in `application-cycles-jd94u8zl` passed the actual
transaction cycle mode: distinct successful oneshot start/exit timestamps,
minimum 65-second observation and immediate failed-unit rejection. Source hash
and rows are retained in result.json. The native container was removed. Later
integration changes still need qualification; timestamp sampling does not claim
to observe every invocation or every Caddy health request.

Remaining implementation is the owner outer-path integration, private operator
receipt handling, HTTP/journal observation and failure coverage, the DNS owner's
separate candidate, and final closed-graph authorization checks. A private login
client is being prepared with in-memory credentials and fixed proxy destinations;
it has not been authorized or run against production. W-020/W-076 remain open.

### Bounded-acceptance qualification checkpoint — November 11, 2026

The approved alternative remains repeated verified HTTP/WebSocket use spanning
at least two 30-second health intervals, no observed health failure/exclusion,
and distinct completed applicable systemd monitor cycles. It does not claim
literal observation of every successful Caddy active check.

Operator scripts now enter the application contract by SHA-256. The private
helper rejects closed, expired, mismatched or orphaned controller windows,
including PID reuse, and rechecks the window while its bounded client runs.
Credentials remain in process memory/stdin; retained receipts contain fixed
acceptance fields only. Three local boundary tests pass. Actual production-mode
client execution and full outer receipt/recovery integration remain unqualified;
this checkpoint does not authorize a login attempt.

The observer now explicitly propagates HTTP, service and journal failures even
when invoked in a Bash conditional. Native systemd qualification passed again
in `application-cycles-yzx942e0`: successful distinct cycles, at least 65 seconds,
and failed-service rejection. The fixture container was removed. The HTTP and
journal integration still needs its own coverage through the application path.

All 18 release scenarios passed against the current neutral transaction, including
application publication and worker-failure reverse rollback. Independent evidence
verification passed; the private copy is
`application-release-window-evidence/certificate-release`. Its source graph now
includes the application fragment and both operator scripts. These application
variants exercise the release transaction, not the application-only outer gate;
W-088 remains in progress. The earlier independent verifier omitted those variants;
that omission is corrected without relabeling partial coverage as authorization.

Current dual-stack synthetic authentication/WebSocket staging passed in
`proxy-auth-5fyh7lb8`; both containers were removed. This exercises staging mode
with synthetic TLS and credentials, not production trust or the real account.
Source identities are retained in `proxy-auth-window-session.json`.

Bash syntax, ShellCheck, canonical formatting, shell collision policy and the
clean/inactive successor policy passed. No successor is registered, no accepted
production manifest changed, and no host was contacted. Sessions 61549, 86791
and 20044 completed with status 0 and are retired. W-020/W-076 are unchanged.

Final checkpoint checks: Markdown and diff whitespace checks passed; Python
sources compile. The application working-tree Gitleaks scan found no secrets.
The Caddy scan reported four unchanged `HISTORY.md` entries (lines 86, 111, 135,
166); each is an explicitly labeled authorized outer SHA-256, not a credential.
No suppression was added. Private scan reports retain these findings. Scan
session 48326 completed with status 0 and is retired.

### Application outer-path qualification — November 11, 2026

W-088 qualification now uses actual local Kuma/Caddy, the production-mode private
client and receipt producer, and native systemd timestamps. Transport and node
views remain isolated substitutes. The first fixture launch
`application-qualification-9c1hdzn8` failed before the outer runner: copying the
native systemctl binary omitted its executable mode. The fixture now preserves
metadata; the failed evidence is retained and its container was removed. This
was local-only and did not consume production authority. Qualification continues.

The next fixture (`application-qualification-du92mc0y`) exposed a missing curl
binary in the earlier minimal systemd image. The fixture now uses the retained
Caddy validation image's native systemd executable and packages, plus the pinned
Kuma application. No package download or live contact is needed. Both failed
fixture containers were removed; source and failure evidence remain retained.

The Caddy base selected in `application-qualification-r1jeouo5` lacked Python.
The source now pins the already-qualified Caddy authentication image by its
local image ID; it contains the required interpreter. That failed container was
removed before any outer-path execution. Native fixture composition failures
remain separate from application acceptance.

`application-qualification-51pois9p` reached the real outer path and rejected a
failed private-helper receipt; reverse recovery completed. The failure stage was
not retained, so the helper now records only a fixed stage name (never exception
values or credentials). Native synthetic-client stderr/status will identify the
fixture failure without weakening receipt acceptance. W-088 remains open.

The synthetic client failure is now identified: the fixture image's default
Caddy service occupied admin port 2019, so the qualification proxy could not
start and the client correctly rejected ECONNREFUSED. The isolated fixture now
stops that default service before launching its own proxy. Failed receipt and
reverse-recovery evidence remain in `application-qualification-q1fkd4xu` and
`application-qualification-fhrjv562`; neither involved a live node.

The DNS draft is `homelab-dns/current/uptime-kuma-dns-20261111-8xbay_ox`
under private workspace evidence. Its before bytes match both November 9 DNS
observations and the October 21 accepted owner candidate. The six-record
candidate matches the retained native-parser qualification exactly. Node,
dispatcher and paired-gate sources are byte-identical to the accepted owner
bundle. Boot/non-zone pins retain their October provenance and must pass live
preflight; they are not represented as newly observed. No additional DNS fixture
or target access was performed. The draft is not sealed.

The defined-operation host checks found two local metadata issues: proposed
manifest rows must remain non-production (`deployable=no`), and Python compilation
had left three unregistered bytecode files beneath the strict test inventory.
The rows are corrected, only those generated files were removed, and the new
fixture disables local bytecode writes. No runtime or accepted-production artifact
was changed by these corrections.

The final application batch `application-final-rm17vo6r` passed five cases but
still accepted the journal-failure case. Changing the query to forward reading
(`-n +100`) was insufficient; the actual rejection cause remains under local
investigation. This corrects the earlier causal inference. All six containers
were removed. The matching 18-case release suite passed in
`/tmp/caddy-focused-container-evidence.mt8Rf1/certificate-release`; native
application authorization is still blocked by W-090. No live authority is requested.

The isolated native journal experiment now distinguishes the cause. A real
unit emitted a matching message after the captured cursor. Both numbered
queries (`-n 100` and `-n +100`) returned no match; `--no-tail` returned it.
The observer now queries forward without a numbered tail and independently
caps retained output at 100 lines, rejecting cap exhaustion or errors.
`journal-query-no-tail-diagnosis.json` retains the comparison and cleanup.
The first transient-unit probe lacked D-Bus and is retained separately; the
comparison uses a native unit file/start instead. Final graph qualification
is running in sessions 61913 and 56763.

### Owner qualification and sealed review — November 11, 2026

**Prepared only; no live approval, target contact or deployment occurred.**
The application owner change record remains canonical. The Caddy and DNS
operations keep separate identities, commands and recovery boundaries.

Current-source qualification passed: all 18 release cases and all six native
application cases, followed by both independent evidence verifiers and the
Caddy authorization-ready policy. The corrected real journal-failure case now
rejects and restores the parent; successful acceptance passes the full HTTP
sample span and completed-cycle checks. The private receipt suite passes four
boundary tests. Host syntax, ShellCheck, canonical formatting, readonly/local
collision, lifecycle and deployment-window policies pass.

Evidence is private under
`/home/aaron/code/.local-evidence/uptime-kuma/application-owner-qualification-3_zpasr4/`.
Its `certificate-release/application/assembly-provenance.json` records each
original scenario root and terminal cleanup result. Copying protected rootless
node views required the local Podman user namespace; incomplete copies are
retained separately. Evidence content and source identities were independently
verified after assembly. All fixture containers were removed. Sessions 61913,
56763, 61879 and 20737 completed with status 0 and are retired; earlier failed
qualification runs remain retained and are not authorization evidence.

The application tests use actual local Kuma/Caddy/TLS, production-mode client,
private receipt producer, systemd timestamps and journal messages. Transport,
node views and the helper's container invocation are controlled substitutes.
They do not establish live ARM64 timing, production trust, actual SSH failure,
controller-loss recovery or future monitor workload capacity. DNS reuses its
accepted owner implementation and retained candidate/parser qualification;
no new DNS fixture or simulated failover was built. Its local sealed-archive
check passed without target contact. Retained boot/non-zone identities remain
admission expectations with their original provenance, not fresh observations.

#### Exact owner bundles, commands and scope — awaiting approval

Caddy action: `20261111-uptime-kuma-onboarding`; scope: `application-onboarding`.

- Authoritative outer SHA-256: `8e9e63a4a6c03a7d5e3d1fd5b50e4c60fa7a52db2b65d287798c8c671e47d818`.
- Closed snapshot archive SHA-256: `0a05defbe6b836e4003c6956f437e7630772f10b412ee8f00045b8e1be7b253c`.
- Source manifest SHA-256: `68b2b7df3e6b11d0a3d3be502daf88aa0c2703e37605b190f2c799bf23ea807b`.
- Private bundle: `/home/aaron/code/.local-evidence/uptime-kuma/caddy-onboarding-20261111-ud_ok6wu`.
- Exact scope/recovery/operator review: `/home/aaron/code/.local-evidence/uptime-kuma/caddy-onboarding-20261111-ud_ok6wu/review.md`.

Run from `/home/aaron/code/homelab-server-configs`, once, after exact approval
and confirmation that Aaron can complete the private terminal check:

```bash
printf '%s  %s\n' 68b2b7df3e6b11d0a3d3be502daf88aa0c2703e37605b190f2c799bf23ea807b \
  /home/aaron/code/.local-evidence/uptime-kuma/caddy-onboarding-20261111-ud_ok6wu/SOURCE.SHA256SUMS | sha256sum --check - &&
sha256sum --check /home/aaron/code/.local-evidence/uptime-kuma/caddy-onboarding-20261111-ud_ok6wu/SOURCE.SHA256SUMS &&
env -i HOME="$HOME" USER="$USER" PATH=/usr/bin:/bin SSH_AUTH_SOCK="${SSH_AUTH_SOCK:-}" \
  /bin/bash Caddy/scripts/run-serving-health-deployment-outer.sh
```

This covers protected staging, protocol-v2 child publication, standby-first
activation/reload on pi@10.1.0.54 then pi@10.1.0.53, existing certificate/reconcile
checks, private dual-family authentication/WebSocket acceptance, bounded
HTTP/journal/completed-cycle observation, and checked reverse recovery.
Preserve the publisher, TLS inventory, unrelated fragments and accepted backend.
Publication containment/resumption is included; forced failover is excluded.

When the runner prints its private operator command, Aaron runs it on this
workstation and enters the existing Kuma credentials only at the prompts.
The window is ten minutes; start with at least three minutes remaining.
Do not paste credentials into chat or create the receipt by hand. Failed,
missing, late or mismatched receipts reject acceptance and enter owner recovery.
A lost controller or unproved recovery requires manual intervention, not replay.

Only after independent Caddy acceptance may the approved DNS operation begin.

DNS archive SHA-256: `620d307ced006fb84755b4e735048170ed25e394320c2c677c08f93878a338bf`.
Private bundle: `/home/aaron/code/.local-evidence/homelab-dns/current/uptime-kuma-dns-20261111-8xbay_ox`. Its `review.md` binds exact
phases, prerequisite/provenance, both full restarts, paired gates and recovery.
The operation expires at
`2026-11-14T17:02:35+00:00`;
the existing runner also requires more than five minutes remaining when invoked.
Expired inputs require a new reviewed seal, not an automatic timestamp change.

```bash
dns_bundle=/home/aaron/code/.local-evidence/homelab-dns/current/uptime-kuma-dns-20261111-8xbay_ox
reviewed_dns_sha256=620d307ced006fb84755b4e735048170ed25e394320c2c677c08f93878a338bf
python3 -I -B "$dns_bundle/runner.py" step --directory "$dns_bundle" --sha256 "$reviewed_dns_sha256" --phase before
python3 -I -B "$dns_bundle/runner.py" step --directory "$dns_bundle" --sha256 "$reviewed_dns_sha256" --phase apply-secondary
python3 -I -B "$dns_bundle/runner.py" step --directory "$dns_bundle" --sha256 "$reviewed_dns_sha256" --phase after-secondary
python3 -I -B "$dns_bundle/runner.py" step --directory "$dns_bundle" --sha256 "$reviewed_dns_sha256" --phase apply-primary
python3 -I -B "$dns_bundle/runner.py" step --directory "$dns_bundle" --sha256 "$reviewed_dns_sha256" --phase after-all
```

Execute phases individually and stop at the first failure; this is not an
unconditional shell paste. Each phase is one-use. Initial ownership must match
.53 primary/.54 standby. Apply the six bound additions atomically on .54 first,
fully restart Unbound, establish health, then fully restart Pi-hole DNS. Require
fresh paired acceptance before progressing to .53. Preserve all unrelated
records and Proxy PTRs; allow only normal cluster-driven coupled VIP movement.

On failure, inspect mutation/automatic recovery receipts. Restore only changed
nodes from exact backups, primary before secondary if both changed. Use the same
runner command with `rollback-primary`, `after-rollback-primary`,
`rollback-secondary`, `after-rollback-all` as applicable. If only secondary
changed, use only `rollback-secondary` then `after-rollback-all`. Do not repeat
an already verified automatic restoration. Unknown state or unproved recovery
requires manual intervention. Keep accepted Caddy and backend state intact.

After successful `after-all`, the sealed DNS review permits one trusted
ordinary-name `/dashboard` request per family from the workstation, each bounded
to 15 seconds and requiring 200. Client-resolution failure remains distinct from
owner DNS acceptance. The exact curl commands are in that review; they do not
replace the private authenticated Caddy receipt.

One approval may name both exact owner identities and their conditional order;
it grants one Caddy attempt and one DNS phase sequence, including their reviewed
recovery. It grants no Pi restart/reboot, account change, monitor/alert creation,
synthetic message, route/radio mutation, forced failover or Git publication.
W-020/W-076 remain open even if these operations pass. Project closeout and
accepted-production inventory reconciliation require actual live results.

The exact-bundle approval requirement comes from
[server repository policy](../../../homelab-server-configs/AGENTS.md#definition-and-authorization),
[Caddy authorization cadence](../../../homelab-server-configs/Caddy/AGENTS.md#authorization-cadence)
and the [DNS owner procedure](../../../homelab-dns/Unbound/docs/host-record-deployment.md).
The change-control skill does not add another approval stage.

Final seal verification passed: both archives match their reviewed bytes, every
Caddy source/evidence hash and retained symlink matches, command syntax is valid,
and the DNS owner archive check again reports no target contact. Private receipt
tests, Markdown/YAML/whitespace checks and selected host policies pass. The app
source secret scan is clean; Caddy reports the same four labeled historical
outer SHA-256 entries in HISTORY.md, with no new finding or suppression.
Vexp completion verification was unavailable for the parent workspace; the
owner tests and independent verifiers above provide the recorded validation.
No commit, push, live execution or project closeout was performed.

### Owner execution authorization — November 11, 2026

Aaron approved both exact owner bundles/commands/scope in the preceding review
(annotation 1), then confirmed Ready now for the private check. The helper runs
in a separate workstation WSL/Ubuntu terminal. Both sealed archives, current
Caddy source manifest and DNS expiry/archive check passed before launch.
Authorization is one Caddy attempt, then DNS only after accepted Caddy evidence,
with the already reviewed recovery. No broader authority is inferred.

### Caddy attempt terminal outcome — November 11, 2026

The approved attempt executed once and exited 1 at `certificate-preflight-b`.
All four workstation node HTTPS health requests passed. Both payload transfers
and upload checks passed. Standby output confirms the certificate validity
command ran; the remote preflight then exited without a per-file diagnostic.
No serving-check evidence was produced and primary preflight was not reached.
The retained source narrows the unobserved interval to installed helper/unit
file checks after certificate validity, but it does not identify the failed
check or prove drift. W-091 records the missing evidence.

The outer read back both evidence directories and completed both staging
disposition commands with status 0. No publisher installation/publication,
promotion, reload, private login window or DNS phase was reached. No release
rollback was needed. This is a failed-consumed attempt, not application
acceptance. The existing backend/account/data and accepted reboot evidence remain
outside this failed preflight's mutation boundary.

Private evidence and terminal result are retained under
`/home/aaron/code/.local-evidence/uptime-kuma/caddy-onboarding-20261111-ud_ok6wu/`.
Session 39291 is complete and retired. Caddy is terminal-pending with the exact
executed specification preserved and the deployable registry cleared. Its
archive tag is planned only; no commit or push occurred. The DNS approval has
not been consumed, but its acceptance prerequisite is unsatisfied and its
existing expiry still applies. No further live action or replay is authorized.

### W-091 retained-evidence diagnosis — November 11, 2026

**Resolved as a baseline-contract preparation error; no new host access.**
The sealed candidate's own copy of `runtime-production.tsv` distinguishes the
accepted installed reconciler from the current repository source. The candidate
incorrectly selected the source identity for its installed-file preflight.
The accepted-live and production-artifact manifests independently agree on both
nodes' accepted installed identity. All four other helper/unit pins in the
failing source interval match their accepted identities.

| Reconciler identity | SHA-256 |
| --- | --- |
| Accepted installed `/usr/local/libexec/reconcile-release.sh` | `e777c2fe6932090d717b5ac9e50ef706d6b90c753293ad7eec4e396f2f6ea073` |
| Repository source and incorrectly selected candidate pin | `f840892f0c05069e4ca4da8633d773d9876ef738e4e350ef42ea13d64e50ac78` |

Git revision `d131b9da63ad` retains the exact accepted file. Its difference from
`d048013f9db8` is one self-test fixture directory name; this onboarding did not
authorize a reconciler installation. Changing a production file to satisfy the
repository-source pin would be the wrong remedy.

The retained local experiment extracted `regular_file` and `certificate_hash`
unchanged from the sealed transaction and ran only those functions against
private files. Seven cases passed: accepted bytes reject the consumed pin and
pass the accepted pin; repository bytes pass the test-derived source pin but
reject the accepted pin; tampered, absent and symlinked inputs reject. No
transaction, SSH call, service operation or deployment was executed. Evidence:
`/home/aaron/code/.local-evidence/uptime-kuma/w091-retained-44sa8_pm/diagnosis.json`.

The earlier release fixture copied the repository reconciler into both modeled
nodes and derived `reconciler_sha256` from that same source. Therefore its passing
scenarios did not test the actual accepted installed/source distinction. The
recorded 18/six scenario outcomes remain valid for their tested inputs; they are
insufficient for the corrected baseline contract. W-092 requires independent
accepted-byte qualification; W-093 requires useful failed-file diagnostics.

This proves a candidate defect that deterministically rejects the accepted
baseline and explains the observed failure interval. The live attempt did not
record which individual file check failed, so the exact assertion and absence
of additional live drift remain unproved. No new inspection is needed to
establish or correct this known contract error. Future authorized preflight
must still verify actual state and stop on unrelated drift.

The consumed specification, transaction, outer runner, input recipe, sealed
archives and terminal receipt remain unchanged. Caddy stays terminal-pending;
DNS has not run. This diagnosis does not define or approve another operation.

### W-092/W-093 local correction and terminal archive review — November 11, 2026

The correction is prepared and locally qualified, but **not applied** to the
owner repository. Its six-file patch changes the neutral transaction, input
recipe, release fixture, both fixture launchers and onboarding procedure.
`reconciler_installed_sha256` uses the accepted deployed identity; the fixture
requires externally retained accepted bytes, independently checked against both
nodes' owner records. The application operation does not install a reconciler.

Failed file checks now report a bounded, escaped path, file type, expected hash
and observed hash or unavailable/unreadable status on captured stderr. They
never print contents or follow symlinks. Full-path tests prove rejection before
publication and retain actual outer stderr/status and staging disposition.

Qualification: 22 release scenarios passed and independent evidence verification
passed; 11 isolated file-check cases and six launcher argument cases passed.
One native application success scenario passed through the updated launcher,
including container cleanup. This is a success smoke check, not renewal of the
six-scenario application acceptance graph. Syntax, ShellCheck, canonical format,
readonly/local collision and Markdown checks passed. The candidate scan has no
new secret finding: the five matches are labeled historical outer SHA-256 values.
The initial missing-Python image launch and fixture path-assertion failure remain
retained; neither involved a live target. All local sessions are complete.

Private preparation and evidence:
`/home/aaron/code/.local-evidence/uptime-kuma/caddy-correction-h75gh_gw/`.
`correction.patch` SHA-256:
`25d5d02af79fbae94e53d0a547a10680a2b79537a15ba2bc4783dd27ae9d0b96`.
`correction-review.json` binds before/after identities; `qualification.json`
indexes results. The private checkout uses an inactive operation and locally
rebound outer hashes solely for tests; these are excluded from the correction
patch. It is not a registered successor, deployment bundle or live authorization.
The patch applies cleanly to the preserved owner files. Current transaction,
outer, executed specification and recipe still exactly match the consumed seal.

#### Terminal Git publication scope for approval

The owner [lifecycle](../../../homelab-server-configs/Caddy/docs/DEPLOYMENT_LIFECYCLE.md#close-an-operation)
requires an annotated, pushed terminal tag before consumed operation cleanup.
The prepared archive is the current Caddy terminal state, **not the correction**:

- Repository: `homelab-server-configs`; configured destination `origin`,
  `Racerx323/homelab-server-configs`. Verify remote identity/visibility before push.
- Parent commit: `eca1d0c7b42b77f2b72561b5d4697157e1686e5e`.
- Prepared Git tree: `9b9b7276d731c5831085f66407909348381148c0`.
- Planned annotated tag: `caddy-uptime-kuma-onboarding-terminal-2026-11-11`.
- Exactly 17 changed Caddy paths are listed and hashed in private
  `terminal-archive-review.json`; `terminal-archive.patch` is the reviewable diff.
  A separate temporary index prepared the tree; the user's index is unchanged.
- Publish only the terminal-result commit and its annotated tag. Preserve the
  exact consumed implementation/specification and sanitized terminal result.
  Exclude the private correction/evidence, application repository, foundation
  components, inventory and other unrelated working-tree changes.

No commit, tag or push has occurred. Owner terminal-window/successor policies
and whitespace checks pass. Publication must preserve this reviewed tree and
parent; any changed archive content needs reconciliation before publishing.
After the remote archive is verified, W-094 owns applying the correction and
reconciling clean-state operation/hash bindings. A future deployable candidate
still needs its own full qualification and exact live authorization. Existing
DNS approval is not consumed or renewed; its prerequisite remains unsatisfied.

### Terminal archive publication — November 11, 2026

Aaron approved committing and pushing the exact 17-file terminal archive and
annotated tag specified above. GitHub metadata confirmed the public destination
`Racerx323/homelab-server-configs`; remote main matched the approved parent and
the tag was absent before publication.

The isolated-worktree commit is
`8999dde79a4bc3ad202876ee98a7a4bbe89221ce`, with the exact approved tree
`9b9b7276d731c5831085f66407909348381148c0` and parent
`eca1d0c7b42b77f2b72561b5d4697157e1686e5e`. Its diff contains exactly the
17 approved Caddy paths. No correction, private evidence, foundation, inventory,
or application-repository changes were included.

All applicable installed commit hooks passed. The first attempt stopped only
because Gitleaks classified the labeled outer SHA-256 in HISTORY.md as an API
key. Its value was independently matched to the frozen script. A private,
one-invocation configuration retained the repository rules and allowed only
that exact labeled nonsecret hash. Controls accepted that label and rejected
a synthetic credential; the complete hook suite then passed. The approved
archive tree and repository scan configuration were not changed. The original
rejection and classification evidence remain retained.

Atomic push published main and annotated tag
`caddy-uptime-kuma-onboarding-terminal-2026-11-11`. Remote readback verified:

- main: `8999dde79a4bc3ad202876ee98a7a4bbe89221ce`;
- annotated tag object: `1e34819d474140f3c540b7cb378655967d8fa213`;
- tag peeled commit: `8999dde79a4bc3ad202876ee98a7a4bbe89221ce`.

Local main now matches the published commit. All pre-existing working-file
contents and modes were verified unchanged; unrelated edits remain local and
unstaged. The isolated archive worktree was removed after confirming it was
clean. Commit sessions 73089/32720 and push session 61823 are complete and
retired. Evidence and receipts are under the existing correction preparation's
`publication/` directory; `publication-result.json` records verified identities.

The archive prerequisite is satisfied. W-094 still owns terminal cleanup,
correction integration and current neutral-binding qualification. The qualified
patch remains unapplied, no successor is registered, and no live action or DNS
phase was performed. The archived HISTORY.md's planned-tag wording describes
its pre-publication state; reconcile current history with cleanup rather than
altering the immutable terminal archive.

### W-094 correction integration and terminal cleanup — November 11, 2026

Applied the reviewed W-092/W-093 patch to the owner files after verifying the
published terminal tag against the retained publication receipt. The consumed
operation remains reconstructible from that immutable tag. Current cleanup
removed its terminal-result file and consumed recipe values, restored the
neutral inactive specification and set the stream to clean while retaining the
archive tag. The successor registry remains none and coverage remains empty.

Rebound the empty recipe hash in the transaction, the transaction hash in the
inactive specification, and both transaction/specification hashes in the outer
runner. The recipe is intentionally header-only: no application operation or
baseline is silently carried into the clean state. The reusable fixture and
procedure retain the explicit installed reconciler identity contract for future
candidates. Installed/accepted production identities are unchanged.

Validation against the actual updated repository passed:

- Host profiles `certificate-release` and `current-repository-policies`.
- Container profile `certificate-release`, invoked through the updated owner
  wrapper with an independently verified, read-only accepted reconciler fixture:
  all 22 scenarios passed; independent retained-evidence verification passed.
- Inactive-definition check, readonly/local collision check, canonical shell
  format, ShellCheck, lifecycle/registry checks, Markdown and whitespace checks.
- Authorization-ready rejected the inactive/no-successor state as required.
- Working-tree secret scan: only the same five labeled historical outer hashes;
  no new finding. No suppression was added to repository scan configuration.

Private evidence:
`/home/aaron/code/.local-evidence/uptime-kuma/caddy-integration-tzz_eqqq/`.
`integration.json` binds the tested source graph; the container evidence was
copied from its temporary test directory into this durable private store.
Host session 71275 and container session 63358 completed with exit 0 and are
retired. The prior unavailable parent-workspace vexp verification is not treated
as evidence; owner checks and the independent verifier establish this result.

W-094 is resolved for local integration and cleanup. The 12 changed Caddy paths
and this ledger remain uncommitted; no additional publication was requested or
performed. No live node was contacted, no DNS phase ran, no successor was created,
and the DNS approval expiry was not renewed. The six-scenario native application
acceptance graph must be qualified against any future exact deployment candidate;
this neutral cleanup does not claim that candidate is ready or live-accepted.

### W-095 Caddy application candidate — November 11, 2026

Prepared one operation, `20261111-uptime-kuma-application-onboarding`, in the
existing owner transaction and outer runner. The local stream is now `defined`;
there is no second pending operation. W-094's cleanup and this replacement remain
uncommitted. The consumed attempt stays in published tag
`caddy-uptime-kuma-onboarding-terminal-2026-11-11`, commit
`8999dde79a4bc3ad202876ee98a7a4bbe89221ce`.

The new recipe binds the accepted installed reconciler independently from current
repository source. Both owner node entries and the retained accepted fixture agree.
The operation verifies and preserves that installed file. Four coverage rows now
bind repository-byte mismatch, missing-file, symlink and tamper rejection with
precise failed-file metadata. Existing guards, target order, acceptance and recovery
remain intact. No new live inspection was performed or required for preparation;
retained accepted state is a prerequisite, checked again by the prospective preflight.

Qualification against the exact current graph passed:

- Host `certificate-release` and `current-repository-policies` profiles.
- All 22 release scenarios through the current owner container wrapper, including
  installed-file drift, publication/readback/reload failures and reverse recovery.
- All six native application cases: success, operator rejection, HTTP failure,
  journal failure, incomplete cycles and evidence-readback failure. Each ran in a
  fresh network-disabled container. Original per-case roots, source graphs, native
  observations, runner results and cleanup results remain in assembly provenance.
- Four private-handoff boundary tests; canonical shell formatting, ShellCheck and
  readonly/local collision checks; source snapshot secret scan with no findings.
- Independent release and application evidence verifiers, followed by owner
  `--authorization-ready`, passed against the combined evidence.

These local AMD64 tests use real Kuma/Caddy/TLS, the production-mode private client,
receipt producer, systemd cycle timestamps and journal events. SSH/node views and
helper container invocation are controlled substitutes. They do not accept live
ARM64 behavior, production trust, normal workload capacity or controller-loss
recovery. Those boundaries remain in the live gates and stop rules.

Private candidate, source snapshot and evidence:
`/home/aaron/code/.local-evidence/uptime-kuma/caddy-application-candidate-tmlyha_f/`.
`qualification.json` indexes retained evidence; `source-provenance.json` records
current source identities and the independently pinned accepted runtime fixture.
`review.md` defines scope and operator handoff. `seal.json` binds the archive and
review. No raw private evidence or credentials were added to Git.

#### Exact bundle, command and scope for review

Status: **sealed, unexecuted, not approved**. One attempt only. No prior approval
or consumed runner session applies to this operation.

- Outer-runner SHA-256 (Caddy authorization identity): `6fefc1e15d0a579d0a56e9f479bf9ace17a492057ce1afa63feb4376ae0438a7`.
- Private deployment.tar SHA-256: `ac295b316f751ed8b25203ca499fae97a555b582c5b0243ff4bc90cd112b6186`.
- SOURCE.SHA256SUMS SHA-256: `9a2ae35bc7c0d258eef2c9a17333a3fd5a0ab5c5788750de54662c579298b87b`.
- Qualification index SHA-256: `d6d0472d74d9cd575ad6742b116b3557ca57a9a81f75d3054f177131cbb81c0b`.
- Review SHA-256: `705c7650c34c9c67d78229fb1075c922172827539d04ee811ba0e7f8a6e0b93d`.

Targets: `pi@10.1.0.54` standby, then `pi@10.1.0.53` primary. Use the retained
accepted release/TLS baseline, rejecting drift before mutation. Transfer the
protected payload; append only the bound Kuma fragment through protocol-v2;
activate/reload standby before primary; preserve unrelated fragments, installed
publisher/reconciler, TLS inventory, Kuma account/data and running backend.
The bounded owner operation may pause/resume publication and invoke existing
reconcile and certificate-expiry units.

Acceptance retains existing release, certificate, paired ownership/service and
proxy health gates. The operator must be available before launch and use the
runner's private command in a separate **workstation WSL/Ubuntu terminal**. Enter
existing Kuma credentials only at its prompts; do not send them to chat or create
a receipt manually. The window is ten minutes, with at least three minutes
remaining at client start. Both families must pass login/session denial and
WebSocket checks. Both nodes then require trusted HTTP samples spanning at least
65 seconds per family, two distinct completed native web/sync-health cycles and
no health failures/exclusions in bounded forward journal observations. This is
the approved bounded acceptance, not proof of every successful active-health cycle.

Failure after publication invokes existing containment and reverse recovery:
restore primary then standby as applicable, verify preserved parent/service state,
and finish checked disposition. Pre-mutation rejection permits cleanup only.
Unknown mutation state, controller loss or unproved recovery requires explicit
manual intervention; no automatic retry or replay.

No DNS mutation, backend restart/stop, reboot, forced failover, certificate
replacement, account reset, monitors/alerts, synthetic notifications, route/radio
change or Git publication is included. W-020/W-076 remain open.

Run once from `/home/aaron/code/homelab-server-configs`, only after exact approval
and fresh operator availability confirmation:

```bash
printf '%s  %s\n' 9a2ae35bc7c0d258eef2c9a17333a3fd5a0ab5c5788750de54662c579298b87b \
  /home/aaron/code/.local-evidence/uptime-kuma/caddy-application-candidate-tmlyha_f/SOURCE.SHA256SUMS | sha256sum --check - &&
sha256sum --check /home/aaron/code/.local-evidence/uptime-kuma/caddy-application-candidate-tmlyha_f/SOURCE.SHA256SUMS &&
env -i HOME="$HOME" USER="$USER" PATH=/usr/bin:/bin SSH_AUTH_SOCK="${SSH_AUTH_SOCK:-}" \
  /bin/bash Caddy/scripts/run-serving-health-deployment-outer.sh
```

Capture full stdout/stderr and terminal status privately from launch. Register the
execution session, retain its printed evidence directory and operator command,
and resume polling that same session if interrupted. Do not launch a second attempt.

Repository [authorization policy](../../../homelab-server-configs/AGENTS.md#definition-and-authorization)
requires approval of this exact bundle, command, targets, acceptance and recovery
scope before live execution. Preparation approval does not satisfy that boundary.

DNS remains conditional and unused under its original approved bundle. Its expiry
is `2026-11-14T17:02:35+00:00`, with more than five minutes required at invocation.
Caddy must independently pass first; this candidate does not renew, reseal or
consume DNS authority. An expiry or changed input requires owner re-review.

Local sessions 45529 (host), 39364 (policies), 89255 (shell checks), 22553 (release),
61464 (six native cases), 47738/56516 (evidence retention/assembly), 52446 (combined
verification) and 58880 (sealing) completed exit 0 and are retired. The earlier
unavailable parent-workspace vexp check is not counted as verification; owner
checks and independent evidence verifiers establish the local result.

Final seal readback verified all 42 current source inputs, their archived bytes,
archive/review/index hashes, the exact ledger command and the owner-policy link.
The final deployment-window check, both changed-document Markdown checks and
whitespace checks passed. No session remains active; no live target was contacted.

### W-095 approved attempt — November 11, 2026

Aaron approved the exact bundle, command and scope above, then confirmed readiness
for the private workstation WSL/Ubuntu check. All sealed inputs matched immediately
before launch. One attempt started in session 71628; complete output is retained in
the candidate's `execution.log`, with `execution-start.json` recording ownership and
read offsets. The original sealed review remains immutable. No replay is authorized.

### W-095 terminal result and W-096 evidence gap — November 11, 2026

The approved command ran once and exited 1. Standby `certificate-preflight-b`
passed; primary `certificate-preflight-a` rejected. Workstation trusted node-health
checks passed over IPv4 and IPv6, and both payload uploads passed. Both preflight
readbacks returned status 0 with individually verified lengths/hashes. Both staging
dispositions returned status 0 with empty stderr. The runner's preserved control
flow confirms that publication, activation, private login, application observation
and DNS were not reached. No rollback was needed before publication.

Primary stdout proves completed ownership and incoming namespace checks. It stops
after `certificate_incoming_node_b_metadata=true`; certificate-service capture is
absent. No failed-file diagnostic was emitted. The remaining code region includes
incoming-root entries/trigger metadata, primary outbound root metadata/inventory
and release integrity, and lsyncd KillMode. The retained record does not identify
which assertion rejected; do not label a particular outbound state as the cause.
The earlier installed-reconciler check was passed on both nodes during this attempt.

Evidence was copied from `/tmp/caddy-ssh-evidence-serving_health.tt9rns` into the
candidate's `execution-evidence/` without replaying any operation. Decoded node
readbacks are retained beside it. `execution-evidence-manifest.json` indexes exact
retained bytes; `terminal-result.json` records the bounded result. Session 71628
completed exit 1 and is retired. The private operator window never opened, so no
operator command or credentials were requested.

Caddy is now `terminal-pending` / `failed-consumed`; successor and coverage registries
are cleared. The exact executed specification, recipe, transaction and runner are
preserved, with a sanitized terminal result and lifecycle/history entries. Planned
tag: `caddy-uptime-kuma-application-onboarding-terminal-2026-11-11`; it has not been
committed or published. No publication was authorized in this attempt. The previous
published archive remains intact. A future correction must respect this terminal
archive boundary; no successor or new live inspection is defined or approved.

DNS was not started. Its prior conditional approval remains unused, expires
`2026-11-14T17:02:35+00:00`, and still requires accepted Caddy plus more than five
minutes remaining. No expiry was renewed. W-020/W-076 remain open.

Terminal current-repository policy checks pass after correcting the required
`Tag:` history label; the initial metadata-only rejection is retained. Both changed
Markdown files and whitespace checks pass. Exact executed transaction, outer,
specification and recipe bytes still match the sealed snapshot. Local validation
sessions 12840/95277 are complete and retired; no execution session remains active.

### Approved routine-onboarding redesign — November 11, 2026

Aaron clarified that the primary must activate and verify the new route before
sending it to the secondary. Secondary acceptance independently checks local
compatibility/drift and the final route result; it does not gate primary activation.
He approved separating routine onboarding from the convoluted platform deployment
workflow, keeping targeted safety checks, removing the timed human gate, and revising
the current contract. He directed that W-096 diagnosis stop rather than spend more
effort explaining an obsolete orchestration failure.

The governing Caddy plan and existing application-onboarding guide now define:

- One candidate, with one revision, original parent and payload manifest.
- Node A activation and trusted dual-family new/existing-route checks before
  transport exposure; no propagation on primary failure.
- Managed lsyncd transfer of that same candidate, followed by independent Node B
  validation/activation and final per-node release/route checks.
- Primary service can proceed while Node B verifies; full HA completion and new
  DNS activation wait for secondary acceptance. A secondary failure is a partial
  result, not a successful deployment and not an automatic rollback of healthy
  primary service. Existing routes and each node's last proven state are preserved.
- Exact changed inputs, TLS validation, finite convergence, existing-route checks,
  explicit recovery and expected/observed failure details remain required.
- Private login/WebSocket checks remain onboarding completion work, without a
  ten-minute operator receipt window or rollback solely for operator delay.

Caddy README, agent instructions, operations, protocol lifecycle, deployment
lifecycle and project handoff now direct routine additions to this guide. Platform
installation, certificate repair, HA maintenance and their historical evidence keep
their own scope. No parallel runbook or transaction framework was created.

This is an approved design/documentation change, not an implemented runtime or
accepted deployment. The installed publisher currently exposes outbound immediately.
W-098 must provide activation-before-exposure in the existing machinery and qualify
its actual effects. Reordering calls after the current publish command would still
allow early replication and would not satisfy Aaron's requirement. Rebuilding after
primary activation would change the parent and is also not equivalent.

The primary-first tradeoff is a temporary mixed-revision interval: failover can
lose the new route until Node B accepts. Node B must reject real drift; its success
cannot be inferred from Node A's tests. Unknown mutation/recovery still requires
manual intervention. No existing safety failure is retroactively accepted.

W-096 is deferred by user decision to retirement of the old path under W-098; its
cause remains unconfirmed. No further diagnostic was run. The exact consumed
specification, recipe, transaction and outer runner remain unchanged. The terminal
archive prerequisite still applies before replacing executed artifacts; no commit,
push, new bundle, live contact or replay was authorized or performed by this change.

Documentation qualification passed: owner operator-documentation policy (including
relative-link and authority checks), Markdown lint for changed runbooks/plan/ledger,
and whitespace checks. A duplicate blank line in the ledger was corrected. Hash
comparison against the consumed snapshot confirms unchanged transaction, outer
runner, operation specification and recipe. Documentation-check sessions 61213 and
19523 completed exit 0 and are retired. No runtime test or production acceptance
is claimed for the unimplemented primary-first sequence.

### Primary-first implementation prepared and locally qualified — November 11, 2026

W-098 has a tested implementation draft in an isolated detached checkout. All
142 main Caddy files remain byte-identical to this task's starting state. The
consumed transaction, outer runner, specification and recipe also match their
sealed provenance. No live contact, commit, tag, push or replay occurred.

Private preparation root:
`/home/aaron/code/.local-evidence/uptime-kuma/caddy-primary-first-4kfz8w9k`.
The checkout is `workspace/homelab-server-configs` beneath it. Changes extend the
existing publisher, transaction and outer runner, and replace the old application
fixture/launcher. No parallel transaction framework was added.

The publisher prepares outside outbound, then exposes the same revision, original
parent and manifest only after primary activation and route checks. The application
coordinator activates Node A, checks the secondary baseline, exposes once, waits
for managed replication/reconciliation and checks both nodes plus the shared
endpoint. Secondary checking follows primary activation. Secondary rejection or
timeout reports a partial result without automatically reversing healthy primary
service. Primary failure before exposure restores the previous release; uncertain
recovery returns manual-intervention status and retains staging.

This path omits certificate workers, unrelated platform inventories, completed
monitor-cycle gates and timed human receipts. It retains TLS/integrity validation,
trusted HTTPS over both families, representative existing-route checks, bounded
convergence, expected/observed diagnostics and explicit recovery. Known outcomes
remove staging after evidence readback. Non-serving prepared/installed immutable
candidates can remain as evidence; they are not authorized for replay. Private
login/WebSocket completion and separately owned DNS activation remain pending.

Per-node route checks require node listeners. The isolated application proposal
adds node IPv4/IPv6 bindings alongside the shared VIPs, preserving client restrictions
and upstream definitions. The main proposal is unchanged. Include this listener
change in the later exact owner review.

Review artifacts, relative to the preparation root:

- `owner-implementation.patch`, SHA-256
  `13305f3b4c3795ef47c2e2c04e905eae4d11150fcad25717cb9126070eca56a6`.
- `application-proposal.patch`, SHA-256
  `8a0769147dc97b774378b1df053f94e7c9884297245f05ca882f16a33678df63`.
- `implementation.json`: changed paths and baseline/candidate identities.
- `qualified-evidence/result.json` and `qualification-summary.json`: input identities,
  image, checks, statuses and retained evidence.
- `consumed-preservation.json`: comparison with sealed consumed provenance.

Both patches pass `git apply --check` against their owning repositories; neither
was applied there. This is not a sealed successor. Consumed operation/recipe data
were deliberately preserved. Neutral bindings, lifecycle/coverage reconciliation
and authorization-ready checks remain part of post-archive candidate preparation.
The private checkout is not a live execution entry point.

Nine offline scenarios pass: publisher compatibility/early-exposure rejection,
normal convergence, primary reload failure, primary HTTP failure, secondary parent
drift, secondary HTTP failure, convergence timeout, failed recovery and candidate
tampering before exposure. Tests execute the actual outer/transaction, publisher,
finalizer and independently retained accepted reconciler. Native Caddy reloads and
trusted IPv4/IPv6 HTTPS produce observations; assertions verify selections, retained
TLS/route content, no early exposure and staging disposition.

SSH serialization, node filesystems and service/replication scheduling are local
substitutes; the backend is a disposable HTTP fixture. These tests do not prove
production ARM64/systemd/lsyncd behavior, real Kuma authentication/WebSockets or live
HA acceptance. Existing receiver/finalizer and reconciler drain regressions also
pass in Debian. ShellCheck, canonical formatting, readonly/local collision and
multi-file grep checks pass. Whitespace passes after a test-file space correction.
Earlier fixture/status and cleanup refinements are retained in private evidence.
No W-096 investigation occurred.

The final offline launcher exited 0 and removed its container. Evidence from
`/tmp/caddy-application-qualification-bdsyl0nt` is retained in `qualified-evidence`.
All sessions are retired in `sessions.json`. W-098 remains in progress until the
required terminal archive permits integration and exact candidate preparation.
DNS remains conditional and unused, expiring `2026-11-14T17:02:35+00:00`; no authority
was renewed. W-020/W-076 remain open.

### Consumed-attempt terminal archive review — November 11, 2026

The terminal archive is ready for publication approval. This review checked retained
inputs and evidence only; it did not investigate W-096 or contact either HA node.
The consumed transaction, runner, specification and recipe still match the sealed
attempt. The sanitized terminal result matches its three execution hashes and the
retained execution-evidence manifest. Failed-consumed state, empty successor/
coverage registries and the planned archive tag are consistent.

The 19 changed Caddy files comprise the consumed candidate/terminal record, its
qualification support and the already-approved W-097 design/runbook revision.
Those documents distinguish the future primary-first contract from the executed
standby-first attempt. W-098 implementation, raw evidence, the application repository,
foundation components, inventory and unrelated changes are excluded. Accepted live
identities and runtime/configuration files are unchanged.

#### Exact terminal publication scope for approval

- Repository/destination: `Racerx323/homelab-server-configs`, `origin`, branch `main`.
  Read-only GitHub metadata confirms the repository is public.
- Parent commit: `8999dde79a4bc3ad202876ee98a7a4bbe89221ce`.
- Prepared Git tree: `22b90f0606059dc46e037f65241e4b8f48aebb14`.
- Annotated tag: `caddy-uptime-kuma-application-onboarding-terminal-2026-11-11`.
- Commit subject: `Archive consumed Uptime Kuma Caddy application onboarding attempt`.
- Commit exactly this tree on the stated parent, annotate that commit with the
  specified tag, atomically push `main` and that tag, and verify both remote refs.
  Do not force-push or replace a tag. Stop if the parent, reviewed inputs or tag
  availability changes. Run applicable commit hooks; retain any verified exact-hash
  scan exception as a private invocation setting, not a repository policy change.

Private review directory:
`/home/aaron/code/.local-evidence/uptime-kuma/caddy-terminal-archive-review-9c5brw5x`.
`terminal-archive-review.json` lists and hashes every included path, records the
exact tag message and identifies the reviewed tree/parent. `terminal-archive.patch`
is the full reviewable diff, SHA-256:
`6bb38649135198db949f334378327d9068561783c00ee95e0d5f1303e100e6df`.

A separate temporary index prepared this tree. The user's index and current branch
were unchanged; no commit or tag was created. Remote `main` matched the parent,
and the proposed remote/local tag was absent at review. Publication must repeat
these drift checks before writing refs. This approval scope covers only the archive;
it creates no deployment or replay authority.

Terminal-window, successor, lifecycle, accepted-live-hash and operator-documentation
policies pass. Changed Markdown and whitespace checks pass. The exact-tree secret
scan found one existing historical digest label under repository rules. Its digest
was independently recomputed from the earlier annotated archive. A private exact-label
exception passes the snapshot scan and accepts the known-hash control while still
rejecting a synthetic credential. Repository scan configuration is unchanged;
`scan-review.json` retains the classification and control results. No secret finding
was waived without verification.

The archive review does not integrate W-098 or define a successor. Its two prepared
patches remain untouched until the required archive is published and remote-verified.
No original DNS expiry or live authority changed. DNS remains conditional and unused,
expiring `2026-11-14T17:02:35+00:00`; W-020/W-076 remain open.

### Application-onboarding terminal archive published — November 11, 2026

Aaron approved the exact terminal archive and annotated tag in the publication scope
above. Published the reviewed 19-file tree in commit
`54eb788e01b244baaf029b7595540a97b5ebdb24` on the approved parent, with annotated tag
`caddy-uptime-kuma-application-onboarding-terminal-2026-11-11`.
The atomic push completed; remote `main`, the tag object and its peeled commit were
independently verified. The committed tree remains
`22b90f0606059dc46e037f65241e4b8f48aebb14`.

All 18 applicable commit hooks passed, including the secret scan with the reviewed
private exact-digest exception. The isolated commit preserved the reviewed tree;
local `main` and its index now match the published commit. All 56 previously changed
or untracked file contents were preserved, including unrelated foundation work.
The initial interrupted commit request did not launch; its stale execution cell was
retired without replaying an active process. Commit session `42124` and atomic-push
session `33090` completed with exit 0 and are retired.

Private review evidence now includes `publication-authorization.json`, `commit.log`,
`commit.exit`, `published-remote-refs.txt` and `publication-result.json` in the existing
`caddy-terminal-archive-review-9c5brw5x` directory. No raw evidence was published.
W-098 patches remain retained and unapplied. Consumed operation cleanup and neutral
binding reconciliation remain pending; publication does not itself make the stream
clean or establish production acceptance. No live target was contacted and no DNS
operation ran. DNS expiry remains `2026-11-14T17:02:35+00:00`.

### W-098 integration qualification in progress — November 11, 2026

Applied both retained patches after verifying the published archive and their
reviewed SHA-256 identities. Cleared the consumed operation, recipe and terminal
manifest; retained its archive tag and reconciled the inactive operation/outer
hash bindings. Initial clean-state checks pass. The source-inventory check found
the expected publisher source-hash change; reconciliation updates only repository
source identity, preserving accepted deployed hashes. Current project-plan wording
also needs to remove superseded standby-first and timed-human acceptance language.
These are W-098 integration tasks, not new live findings or W-096 investigation.

Private integration evidence: `.local-evidence/uptime-kuma/caddy-primary-first-integration-6sdpuij4`
under the workspace root. The network-disabled fixture is testing the integrated
owner source and application proposal. No publication or live operation is authorized.

The integrated nine-scenario application fixture passed with its exact source hashes
and cleanup status 0. Host synchronization and current repository policy profiles
passed. Debian synchronization cases passed; the first certificate regression
invocation omitted its required accepted-reconciler environment input and failed
before exercising a scenario. The corrected certificate-only invocation is running.
The failed invocation is retained rather than counted as qualification.

### W-098 integrated candidate qualification complete — November 11, 2026

The owner source is integrated in place and locally qualified after terminal archive
`caddy-uptime-kuma-application-onboarding-terminal-2026-11-11`. The operation is
inactive, its recipe and coverage are empty, and the stream is clean with the
archive tag retained. The consumed terminal manifest is removed from the current
worktree and remains in that tag. No successor is defined or sealed.

The publisher supports preparation before exposure; Node A activation and route
checks precede replication of the same revision/parent/manifest. Node B independently
accepts it. The application proposal includes node listener bindings for these
checks while preserving VIP listeners and client ACLs. Source inventory records
the new publisher bytes separately from unchanged accepted deployed hashes.
Runbooks and the project plan distinguish this local implementation from installed
production and remove superseded routine standby-first/timed-human instructions.

Final qualification passes:

- All nine native primary-first scenarios, with exact input identities and container
  cleanup status 0.
- All 20 platform certificate scenarios after W-099 removed retired application
  expectations; existing receiver/finalizer and reconciler regressions pass in Debian.
- Host synchronization and current repository policy profiles; clean-state pins,
  source inventory, ShellCheck, canonical formatting and readonly/local collision checks.
- Changed-document Markdown, whitespace and secret scans. The owner scan uses the
  previously verified private historical-digest exception; repository rules are unchanged.

The first Debian command omitted the required fixture environment; a corrected run
then exposed W-099. Both failures remain in the private evidence. Final passing runs
supersede neither that history nor the consumed live failure. The parent-workspace
vexp completion helper was unavailable (`not a git repository`); direct source
identity checks and the owner validation above provide local verification.

Private evidence: `.local-evidence/uptime-kuma/caddy-primary-first-integration-6sdpuij4`
under the workspace root. `candidate-identities.json` records every current owner
file, the application proposal and unchanged live-state registries. The exact owner
diff is `integrated-owner.patch`, SHA-256
`9c48da6d31f8dd8484bcc99c5232709ddfe068ce5a4c1d930f9f4ba60455b7dd`.
Final application evidence, platform logs and session results are retained there.
All execution sessions completed and are retired. No live host was contacted,
no new commit/tag was made, and no push or DNS operation occurred.

W-100 remains a prerequisite to successor review: current authorization coverage
still requires the retired application workflow. Clean-state checks are not an
authorization-ready result. Convert that coverage and independently validate the
new operation's exact evidence before sealing; do not waive the gate. W-096 remains
deferred; W-020/W-076 remain open. DNS expiry remains
`2026-11-14T17:02:35+00:00`. Native fixture success does not prove production
ARM64/systemd/lsyncd behavior, private Kuma authentication/WebSockets or live HA acceptance.

### W-100 evidence contract preparation — November 11, 2026

Separated application authorization from the certificate-repair scenario list and
verifier. The application fixture now retains source identities, real phase status,
serialized commands, primary route readback, selected releases, recovery and
disposition evidence. Its independent verifier recomputes each decision from those
producers. Missing, symlinked, stale or changed evidence must reject. Native
qualification is running with the operation still inactive, before any new binding.
Private work: `.local-evidence/uptime-kuma/caddy-primary-first-successor-3w7l_m9t`.
No live action, source publication or replay is authorized.

Inactive W-100 qualification passed all nine native scenarios and nine rejection
controls (stale graph, changed outer/phase status, forged observation, missing
command/decision/readback, symlinked file and symlinked directory). Only after that
qualification was `20261111-uptime-kuma-primary-first` bound to current recipe,
transaction, operation, fixture and authorization policy identities. Exact-candidate
qualification is running; the operation is not yet sealed or approved. Lifecycle
rows now identify the new unexecuted operation/recipe rather than the archived attempt.

### Primary-first successor sealed for review — November 11, 2026

Operation `20261111-uptime-kuma-primary-first` is locally defined, qualified and sealed.
W-100 separates application authorization from certificate-repair checks. The
current application verifier validates exact source/operation bindings and
independently derives decisions from serialized commands, actual phase status,
primary-before-exposure ordering, HTTP readback, release manifests, recovery and
staging disposition. W-101 binds this qualified contract to the retained baseline.

All nine native scenarios pass against the bound successor. Nine tampered-evidence
controls reject through the actual authorization gate, including a stale graph,
changed outer/phase status, forged observation, missing command/decision/readback
and symlinked file/directory. Valid and restored controls pass. Owner host profiles,
ShellCheck, canonical formatting, readonly/local collision, Markdown, whitespace
and source secret checks pass. The known historical digest exception stays private;
repository scan rules are unchanged. A task-generated Python bytecode file briefly
failed inventory validation; it was removed and the final profile passes. The
parent-workspace vexp helper remains unavailable; exact source checks and the owner
qualification supply the recorded verification.

Evidence and review root: `/home/aaron/code/.local-evidence/uptime-kuma/caddy-primary-first-successor-3w7l_m9t`.
`qualified-evidence` retains the final native run; `candidate-negative.log` and
`authorization-ready.log` record gate qualification. `qualification.json` hashes
that evidence index, and `source-provenance.json`/`SOURCE.SHA256SUMS` bind 146
non-secret source/plan files. `deployment.tar` contains that source snapshot,
not raw evidence. `review.md` and `seal.json` bind the operation's scope and command.
Accepted live identities, the published consumed archive and unrelated work remain
unchanged. The new definition wrapper has executable intent-to-add metadata only;
no source commit/tag/push occurred. All sessions are complete and retired.

#### Exact primary-first bundle, command and scope for approval

Status: **accepted once; approval consumed; terminal archive pending**. Earlier approvals
and consumed sessions provide no authority for this successor.

- Outer-runner SHA-256 (owner authorization identity): `fe7a7c9d3815f4b4e9893545bbd5b6aea7724d91511afaea747e5418a8d3e980`.
- Deployment archive SHA-256: `232214da2b5530a92019d3a229b0afccb00a196f3cebf9ea5ba2bd5947986a3e`.
- Source manifest SHA-256: `7a2de0285cca4f8e195a5308338bf9678e4b1ed3e5098c421c85ef42aa5fa90c`.
- Qualification index SHA-256: `a9c7fd9b7379e38ef27d07ebb50026affe35d57e888a4df924464bdcf70450bf`.
- Review SHA-256: `0617554aef044169dd04858aecde254a739b58f7cc1a365755dbca7423593c07`.

Targets: `pi@10.1.0.53` (Node A), then `pi@10.1.0.54` (Node B).
Stage protected temporary payloads on both nodes; verify retained parent integrity,
accepted finalizer/reconciler identities and local serving state. Run the pinned
publisher from the payload without replacing installed tools. Add only the Kuma
fragment, including node-address listeners alongside the Proxy VIPs; preserve
client ACLs, complete TLS, unrelated routes and the accepted backend/account/data.

Activate and verify Node A before exposing the same revision, original parent and
manifest to managed replication. Independently finalize/reconcile/accept Node B.
Require trusted dual-family new/existing-route responses, matching release manifests,
shared-endpoint responses and checked evidence/disposition. Convergence permits
sixty one-second polls; each HTTP request is bounded to five seconds. This is not
a claimed global deadline for native service jobs. **No timed private login window
or operator availability confirmation is part of this route operation.**

A known primary failure before exposure restores and verifies its parent. A known
secondary post-selection failure restores its parent. Secondary rejection/timeout
retains the previously verified primary and stops with partial acceptance and DNS
pending. Final-check failure stops progression without automatic cross-node rollback.
Unknown mutation, controller loss, lost evidence or unproved recovery requires
manual intervention; never replay. Known terminal paths remove owned staging;
uncertain paths retain evidence. Immutable prepared/installed candidates may remain.

Excluded: DNS mutation; backend start/stop/restart; reboot; forced failover;
certificate or installed-tool replacement; account reset; monitors/alerts; synthetic
notifications; platform monitor-cycle gates; unrelated route/radio changes; and Git
publication. Private login/WebSocket and repeated application acceptance remain
separate completion work. DNS is still conditional and unused, expiring
`2026-11-14T17:02:35+00:00`; this operation neither renews nor automatically executes
that approval. W-096 remains deferred; W-020/W-076 remain open.

Run once from the owner repository **only after exact approval**:

```bash
cd /home/aaron/code/homelab-server-configs &&
printf '%s  %s\n' 7a2de0285cca4f8e195a5308338bf9678e4b1ed3e5098c421c85ef42aa5fa90c \
  /home/aaron/code/.local-evidence/uptime-kuma/caddy-primary-first-successor-3w7l_m9t/SOURCE.SHA256SUMS \
  232214da2b5530a92019d3a229b0afccb00a196f3cebf9ea5ba2bd5947986a3e \
  /home/aaron/code/.local-evidence/uptime-kuma/caddy-primary-first-successor-3w7l_m9t/deployment.tar | sha256sum --check - &&
sha256sum --check /home/aaron/code/.local-evidence/uptime-kuma/caddy-primary-first-successor-3w7l_m9t/SOURCE.SHA256SUMS &&
CADDY_APPLICATION_QUALIFICATION_ROOT=/home/aaron/code/.local-evidence/uptime-kuma/caddy-primary-first-successor-3w7l_m9t/qualified-evidence \
  Caddy/tests/deployable-successor-policy.sh --authorization-ready &&
bash Caddy/scripts/run-serving-health-deployment-outer.sh
```

Local fixture success does not establish production ARM64/systemd/lsyncd behavior,
real Kuma authentication/WebSockets or live HA acceptance. No live host was contacted
while preparing this bundle. The repository's exact-bundle authorization rule
remains the live boundary; this sealed review is not approval.

### Primary-first execution authorization

Aaron approved the exact bundle, command and scope at the review section above
for one attempt. All sealed source/review/qualification/archive identities were
rechecked locally before launch. The original seal remains unchanged; private
`caddy-primary-first-successor-3w7l_m9t/execution/authorization.json` records this
authority separately. No operator attendance is required by this operation.

### Primary-first route activation accepted — November 11, 2026

The approved command ran once and exited 0. Session 81061 is retired.
Release `20261111T213048Z-71b7deb8-bc71-45d5-8f33-98270af79d3b` is selected on both nodes, with
payload manifest SHA-256 `b972d15185960fc219d09c1c047cd5c2269be97f42e6cc5eef6a3b691aa7d52d`.
Node A activation and verification preceded exposure to managed replication;
Node B independently converged and passed acceptance. Retained, decoded remote
readbacks match their byte counts and SHA-256 envelopes. Both node dashboard
paths returned 200 over IPv4/IPv6; existing health paths returned 204. Shared
application endpoints returned 200 over both families. All outer phase, readback
and owned-staging disposition statuses are zero; no rollback was required.

Complete stdout/stderr, decoded readbacks, copied outer evidence and the evidence
index remain under private `caddy-primary-first-successor-3w7l_m9t/execution/`.
The sealed source snapshot remains intact. Owner terminal records retain the
executed operation and clear its deployable registries pending archival.

This accepts route activation and replication only. Private login/WebSocket and
repeated application acceptance are pending; DNS was not executed. No account,
backend, certificate or installed-tool replacement was performed. Current live
state records the new release; complete production source-inventory reconciliation
and terminal archive preparation are next local work. W-020/W-076 remain open,
and W-096 remains deferred. No new live authority or Git publication is implied.

### Production reconciliation and terminal archive review — November 11, 2026

The accepted payload identities and production source inventory now describe the
same release on both nodes. `20-uptime-kuma.caddy` is the exact executed fragment;
all parent source bytes and installed publisher/reconciler identities are preserved.
The terminal lifecycle is `accepted-executed-definition`. The local release-source
policy now compares the complete source inventory instead of requiring five files.
Missing and unregistered-source regressions reject; current repository-policy host
checks, ShellCheck, canonical formatting, collision policy, Markdown and whitespace
checks pass. The archive snapshot passes the retained reviewed Gitleaks policy.
Vexp verification remains unavailable from the parent workspace; focused owner
checks provide local validation. No live target was contacted.

#### Exact terminal archive for separate publication approval

Status: **approved once, committed, tagged, pushed and remote-verified**.
The publication authority is consumed; the original reviewed scope follows.

- Repository: `Racerx323/homelab-server-configs`; branch `main`.
- Base commit: `54eb788e01b244baaf029b7595540a97b5ebdb24`.
- Candidate tree: `eb49be7ab093ab2a4e10a504c6f3d4560b96374e`.
- Scope: exactly **35 Caddy files**, including the already qualified primary-first
  implementation/design, consumed operation and sanitized result, reconciled
  production inventory, accepted fragment and local inventory-policy correction.
- File-manifest SHA-256: `edf04256031720b1a1dc33fdaad8e418240274e4cc102d626d22884c7d3075b4`.
- Patch SHA-256: `8a640e4eea4f56c5dbd101dd2466be623127736c31d399393957bc1fa519be95`.
- Planned annotated tag: `caddy-uptime-kuma-primary-first-terminal-2026-11-11`.
- Private review: `/home/aaron/code/.local-evidence/uptime-kuma/caddy-primary-first-terminal-review-nd150l5j`.

`files.txt`, `FILES.SHA256SUMS`, `archive.patch`, `review.json`, commit/tag messages
and `review-command.sh` define the exact proposed publication. The command checks
base, clean staged content, source hashes and candidate tree; any mismatch or
hook failure stops progression. Verify destination identity/visibility and remote
base before execution, then verify pushed commit/tag identities afterward. Do not
force-push or recreate an existing tag. Command SHA-256:
`013e1f7aaefc3eb61fa0285fa3f3ecfe017d1060b8616a22e0c71bf674788aac`.

The temporary review index did not stage changes in the normal worktree index.
Unrelated foundation/inventory files remain untouched and excluded. Raw evidence,
application WORK.md and other repository changes are excluded from this owner
archive. Exact executed publisher, transaction, outer runner, operation and recipe
remain unchanged. Current post-execution inventory/policy edits are distinguished
from the sealed pre-execution snapshot retained privately.

This review authorizes nothing by itself. If separately approved, the scope is one
terminal-result commit, one annotated tag and their push to the named repository,
with remote verification. It includes no cleanup of consumed inputs, successor,
live target access, DNS mutation or private login/WebSocket acceptance. Those
remain pending; DNS retains its original `2026-11-14T17:02:35+00:00` expiry.

### Terminal archive local review

The 35-file publication candidate passed local review. All source/snapshot, patch,
file-list, command and message hashes match the prepared review. The temporary
index produces the recorded tree; normal index and base commit are unchanged.
Executed inputs match the consumed seal, the terminal evidence-index hash matches,
and unrelated foundation work remains preserved. Existing focused qualification
and secret-scan receipts pass; no changed archive input required rerunning them.
The publication command passes Bash syntax checking.

Private `caddy-primary-first-terminal-review-nd150l5j/local-review-result.json`
retains the result. Configured remote matches the review; destination visibility
and remote refs still require read-only verification before any approved publication.
No commit, tag, push, live host access, DNS action or replay occurred. The exact
publication review above is unchanged and awaits Aaron's explicit authorization.

### Approved terminal archive publication completed

Aaron approved the exact archive, command and scope at the publication review
above for one commit, annotated tag and push. Destination verification confirmed
the public `Racerx323/homelab-server-configs` repository, unchanged remote base
and absent planned tag before launch. The reviewed command completed once with
status 0; session 4313 is retired.

- Commit: `e6fa5310d292e6cce2209902dc2c7e70b05adde7`.
- Annotated tag: `caddy-uptime-kuma-primary-first-terminal-2026-11-11`.
- Tag object: `71438a01c0c16e98cc3dd6064f7dfc7464381748`.
- Committed tree: `eb49be7ab093ab2a4e10a504c6f3d4560b96374e` (exact reviewed tree).

Remote `main`, tag object and peeled tag commit match the local identities.
Pre-commit checks passed; the normal index is clear, Caddy has no remaining
uncommitted changes, and unrelated foundation files retain their reviewed hashes.
Private authorization, complete log, status and verification receipt are retained
in `caddy-primary-first-terminal-review-nd150l5j/`. No raw evidence was published.

The archived commit intentionally retains terminal-pending metadata and consumed
inputs. Returning the stream to neutral is subsequent local work, not a second
publication under this approval. No cleanup, live host access, DNS mutation or
login/WebSocket check occurred. DNS retains its original
`2026-11-14T17:02:35+00:00` expiry; application acceptance remains pending.

### Neutral cleanup and separate application acceptance preparation

The published primary-first archive remains unchanged. Current owner sources now
have an inactive operation, empty recipe/coverage, no successor and clean stream;
accepted release references point to the annotated archive. Only neutral hash
bindings changed in the reusable transaction/runner. Accepted production source
and installed artifact identities are unchanged. Focused owner policy checks pass.

The existing private-login helper now supports `--standalone`; legacy window
handling remains isolated for compatibility. Eight offline tests cover old-window
rejections, standalone receipt identity/schema/duration, no-controller dispatch and
credential exclusion. The WebSocket client is unchanged. No synthetic or live
result is represented as current production login acceptance.

The new section in `uptime-kuma/docs/OPERATIONS.md` defines untimed operator
readiness, bounded client execution, repeated dual-family HTTP/WebSocket checks,
cursor-bounded health observations and actual completed systemd cycles. It does
not put a human deadline or rollback back into the release transaction. Private
`caddy-neutral-acceptance-h4hju_eg/` retains neutral-check evidence, the concrete
operator command and input identities. The passive capture/receipt integration
still needs qualification before one combined scope can be sealed for approval.
No live target was contacted, no Podman client was launched against production,
and no commit/push or DNS action occurred. W-105 owns the remaining preparation.

### Passive observer qualification and acceptance seal — November 11, 2026

The final observer uses native `systemctl show` timestamps/statuses, trusted
dual-family HTTP and cursor-bounded journals. It never starts a service or timer.
Five observer/integration tests exercise success and reject failed HTTP, missing
cursor, inaccessible/truncated/adverse journals, stale/failed cycles, release
drift, transport failure, replay and altered combined receipt bindings. Eight
private-helper tests pass. Expected and observed command statuses and identity
mismatches are reported without credentials or response bodies.

Native offline qualification ran the exact observer against systemd timers and
Caddy HTTPS in a disposable network-isolated AMD64 container. It observed real
completed cycles, 12 trusted node/shared/health requests and a 65.43-second
interval after the first completed HTTP batch. The independent verifier accepted its receipt. This is
parser/runtime qualification, not live ARM64, SSH, Kuma authentication or HA proof.
Earlier fixture runs encountered the image's prestarted default Caddy site; the
fixture now stops that disposable service before starting synthetic HTTPS. Final
qualification and cleanup passed; all failed logs remain private. No production
service was touched.

Private evidence: `proxy-observer-native-mimq8rhv/` and
`proxy-acceptance-review-awfwq0wh/`. The whole-worktree secret scan reported one
generated `.vexp/manifest.json` integrity-hash entry; that cache is excluded from
the bundle. The exact frozen source snapshot passes the retained reviewed scan
policy. Python syntax, helper/observer tests and Markdown/whitespace checks pass.
Vexp verification remains unavailable from the non-repository parent workspace.

#### Exact application-acceptance bundle, commands and scope for approval

Status: **consumed; operator check failed; passive observation not started**. This is separate application
acceptance, not another Caddy deployment operation. One operator check and one
ordered Node A/Node B observation attempt; no retry under consumed approval.

- Bundle SHA-256: `e9135feb2d86780b8b2b407d7a3947b2918d598709c31ca90a72088454e2cd30`.
- Frozen input manifest SHA-256: `68f45a758def2de897e584a22a7a83a9fe9200ce1bcdbe532e44a73bad94d733`.
- Operator command SHA-256: `788ba0fac6d71d31a0de855973beafd1a6b3e339c45ede0b0a9d979c572442d8`.
- Observation command SHA-256: `8a5964078df6bb3cc480988d7f2259980dc7bd93d3a559f56cc77489faee6598`.
- Qualification SHA-256: `61ce6f8f0b2f35f343430f2cf698f88aeaf72145a0e0064ffc088bc8c3ee3afb`.
- Private root: `/home/aaron/code/.local-evidence/uptime-kuma/proxy-acceptance-review-awfwq0wh`.
- Accepted release: `20261111T213048Z-71b7deb8-bc71-45d5-8f33-98270af79d3b`.
- Accepted payload manifest: `b972d15185960fc219d09c1c047cd5c2269be97f42e6cc5eef6a3b691aa7d52d`.

**Operator command**, only after approval, in a private workstation WSL/Ubuntu
terminal. Start when ready; no controller/window needs to be running. Credentials
are entered locally and sent through the client's private stdin, never chat,
arguments, environment variables or saved logs. Do not record the terminal.

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/proxy-acceptance-review-awfwq0wh/operator.sh
```

This uses the already retained pinned local Podman client image with `--pull never`
and host networking. It contacts only Proxy VIPs `10.1.0.56` and
`fd36:5aa8:6971:1::56` as `uptime.local.theama.co`, using normal TLS validation.
It checks dashboard 200, real WebSocket transport, unauthenticated denial, one
wrong-password rejection per family, immediate correct login, a second client,
65-second authenticated survival and logout denial. Transient authentication
sessions and ordinary server logs are expected; no accounts, monitors, alerts or
data settings are changed. Human credential entry is untimed; the client has a
180-second limit plus bounded local container cleanup. Only a sanitized private
receipt is retained.

**Observer command**, after that receipt passes, under the same exact approval:

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/proxy-acceptance-review-awfwq0wh/observe.sh
```

The command first verifies the private receipt and frozen inputs. It then streams
the observer through strict-existing-host-key SSH as `pi` to `10.1.0.53`, then
`10.1.0.54`, using `sudo -n python3 -` without target file staging. Each node reads
its selected release/manifest/fragment, issues trusted IPv4/IPv6 dashboard and
existing `/healthz` requests to its own addresses and the shared VIPs, and reads
`systemctl show` plus cursor-bounded `journalctl`. Two distinct successful cycles
for each `caddy-sync-health.service` and `caddy-pihole-web-health.service` must
complete after the observer baseline. Cycle polling is five-second cadence, up
to 320 seconds; each node has a six-minute overall alarm and the controller
allows 400 seconds for SSH/readback. No timer/service is invoked to create cycles.

Acceptance requires start/end HTTP observations spanning at least 65 seconds,
unchanged release identities, no relevant journal health failures/exclusions,
completed native cycles and independent combined verification of both node
records and the private receipt. Journal access, parse/size failures and missing
cycles reject. Conservative journal rejection may include unrelated proxy-health
noise; it is not waived automatically. This remains bounded sampled acceptance,
not proof of every internal Caddy health probe.

A failed operator receipt stops before SSH. A failed Node A observation stops
before B. Any later failure retains evidence and stops DNS progression; running
services remain untouched. Existing receipt/evidence paths reject replay. A lost
controller does not trigger rollback; the remote alarm bounds observation.

Excluded: backend SSH; deployment, staging or configuration changes; service or
timer control; publication; failover; account reset; monitor/alert changes;
synthetic notification sending; DNS queries/mutation; automatic retry or rollback.
The helper's uniquely named local container is the only cleanup target. No commit
or push is included. DNS remains conditional and unused with its original
`2026-11-14T17:02:35+00:00` expiry; a combined pass neither executes nor renews it.

Final seal refinement: the repeat interval starts after the first HTTP batch
completes, so slow first requests cannot shorten the required 65-second span.
The cadence rejection test and final exact-source native run pass. The provisional
seal was replaced before any authorization; only the identities above are current.

#### Application-acceptance authorization recorded — November 11

Aaron approved the exact bundle, commands and scope above for one private login
check followed by bounded passive observation. All six seal bindings and the
frozen input manifest passed local verification. The original preapproval seal
is preserved; `execution-authorization.json` in the private review root records
this authorization separately. Neither receipt nor observation directory existed
at authorization recording. Operator credential entry remains private and untimed;
observation starts only after the standalone receipt verifies. DNS is excluded.

#### Standalone operator attempt failed — November 11

The operator reported failure after credential entry. The private receipt for the
sealed operation confirms `status=failed`, `failure_stage=client-result`; no
observation directory exists. Authorization state now records one operator
attempt and zero observer attempts, with the failed receipt hash. Frozen inputs
and receipt are preserved; no retry or target inspection was performed.

Source review confirms the wrapper discards client stderr and does not retain
the exit status or completed check stages. The JavaScript client produces a
stage/error-code summary, but that output was not persisted. The retained evidence
cannot identify the underlying failure. W-107 tracks this diagnostic gap; do not
attribute the outcome to credentials, TLS, WebSockets or Caddy without evidence.
DNS remains pending; running services were not changed by the agent.

#### W-107 credential-safe reporting qualified locally — November 11

The working helper now retains client exit status, distinct wrapper failure stages
(including deadline and output limit), cleanup status and finish time. The client
emits only locally assigned stage/family/code enums; Python accepts an exact
three-field schema up to 1,024 characters. Unknown, malformed, multiple or oversized
reports become fixed fallback categories. Raw output, exception messages/names,
credentials, tokens and response bodies are not copied to receipts or terminal
diagnostics. Successful receipt schema and acceptance requirements are unchanged.

Qualification: 13 Python helper tests cover failure capture, secret sentinels,
malformed/oversized reports, launch/deadline/cleanup failures and replay rejection.
The actual JavaScript client runs against in-memory transport doubles for seven
failure scenarios and dual-family success. Five existing passive-observer tests
pass. These are local simulations, not production TLS/authentication acceptance.
No Podman container, SSH session or live request was launched. The first JavaScript
fixture had an incorrect transport shape and timer scheduling; corrected fixtures
pass. A documentation blank-line lint finding was also corrected.

Exact-source snapshots, command statuses and logs are retained privately under
`private-failure-reporting-b3ap_bje` in the existing Uptime Kuma evidence root.
The original `proxy-acceptance-review-awfwq0wh` frozen inputs and failed receipt
remain intact. No successor is sealed; W-106 and DNS remain pending.

#### Successor application-acceptance bundle, commands and scope for approval

Status: **consumed; operator check failed; passive observation not started**. This is separate application
acceptance, not another Caddy deployment operation. One operator check and one
ordered Node A/Node B observation attempt; no retry under consumed approval.

- Bundle SHA-256: `ac9e2079e695d255bac812685f1f2ea147e2f6b43343691dc6fb597fddb07893`.
- Frozen input manifest SHA-256: `b8a170aa58cd36d03836767edf67ad9c5981625bc9e6a290ee7fc619acc289eb`.
- Operator command SHA-256: `d211c006e77a0113597afc408d953037e043a9c3fb40a0aa7bb35fec18803165`.
- Observation command SHA-256: `b7904e9da73be5ec0a882e58fb7994e4ac6bdb4d5c90cbaea4b230e09a693f1a`.
- Qualification SHA-256: `088268f23736b8ee042ce52b2c3a9af401c2d147e00fe02daaeeb9dec5ee44ea`.
- Private root: `/home/aaron/code/.local-evidence/uptime-kuma/proxy-acceptance-review-82p7lr6b`.
- Accepted release: `20261111T213048Z-71b7deb8-bc71-45d5-8f33-98270af79d3b`.
- Accepted payload manifest: `b972d15185960fc219d09c1c047cd5c2269be97f42e6cc5eef6a3b691aa7d52d`.

**Operator command**, only after approval, in a private workstation WSL/Ubuntu
terminal. Start when ready; no controller/window needs to be running. Credentials
are entered locally and sent through the client's private stdin, never chat,
arguments, environment variables or saved logs. Do not record the terminal.

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/proxy-acceptance-review-82p7lr6b/operator.sh
```

This uses the already retained pinned local Podman client image with `--pull never`
and host networking. It contacts only Proxy VIPs `10.1.0.56` and
`fd36:5aa8:6971:1::56` as `uptime.local.theama.co`, using normal TLS validation.
It checks dashboard 200, real WebSocket transport, unauthenticated denial, one
wrong-password rejection per family, immediate correct login, a second client,
65-second authenticated survival and logout denial. Transient authentication
sessions and ordinary server logs are expected; no accounts, monitors, alerts or
data settings are changed. Human credential entry is untimed; the client has a
180-second limit plus bounded local container cleanup. Only a sanitized private
receipt is retained.

**Observer command**, after that receipt passes, under the same exact approval:

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/proxy-acceptance-review-82p7lr6b/observe.sh
```

The command first verifies the private receipt and frozen inputs. It then streams
the observer through strict-existing-host-key SSH as `pi` to `10.1.0.53`, then
`10.1.0.54`, using `sudo -n python3 -` without target file staging. Each node reads
its selected release/manifest/fragment, issues trusted IPv4/IPv6 dashboard and
existing `/healthz` requests to its own addresses and the shared VIPs, and reads
`systemctl show` plus cursor-bounded `journalctl`. Two distinct successful cycles
for each `caddy-sync-health.service` and `caddy-pihole-web-health.service` must
complete after the observer baseline. Cycle polling is five-second cadence, up
to 320 seconds; each node has a six-minute overall alarm and the controller
allows 400 seconds for SSH/readback. No timer/service is invoked to create cycles.

Acceptance requires start/end HTTP observations spanning at least 65 seconds,
unchanged release identities, no relevant journal health failures/exclusions,
completed native cycles and independent combined verification of both node
records and the private receipt. Journal access, parse/size failures and missing
cycles reject. Conservative journal rejection may include unrelated proxy-health
noise; it is not waived automatically. This remains bounded sampled acceptance,
not proof of every internal Caddy health probe.

A failed operator receipt stops before SSH. A failed Node A observation stops
before B. Any later failure retains evidence and stops DNS progression; running
services remain untouched. Existing receipt/evidence paths reject replay. A lost
controller does not trigger rollback; the remote alarm bounds observation.

Excluded: backend SSH; deployment, staging or configuration changes; service or
timer control; publication; failover; account reset; monitor/alert changes;
synthetic notification sending; DNS queries/mutation; automatic retry or rollback.
The helper's uniquely named local container is the only cleanup target. No commit
or push is included. DNS remains conditional and unused with its original
`2026-11-14T17:02:35+00:00` expiry; a combined pass neither executes nor renews it.

This successor incorporates W-107's enum-only failure reporting and preserves
successful acceptance requirements. A failure now retains wrapper/client stage,
address family, safe error code, client exit status when available and cleanup
outcome. Raw error text and credential values are not retained. The consumed
predecessor and its failed receipt remain unchanged; its root cause is unknown.

Qualification ran against these frozen sources: 13 helper tests, seven JavaScript
failure scenarios plus success, five passive-observer tests, command syntax and
an exact-snapshot secret scan passed. The scan reused the previously reviewed
nonsecret integrity-hash exceptions. The unchanged observer retains its verified
native offline systemd/Caddy qualification; that is synthetic local evidence,
not production acceptance. `qualification.json` binds test commands and logs;
`predecessor.json` binds the consumed attempt. No live check or publication ran.

#### Successor authorization recorded — November 11

Aaron approved the exact successor bundle, commands and scope above. All seal
bindings and frozen inputs passed local verification; receipt/pending/observation
paths were absent. The original seal is preserved, with approval recorded in
`execution-authorization.json` under `proxy-acceptance-review-82p7lr6b`. One private
operator attempt is authorized, followed only on success by one ordered passive
observation attempt. No login check or SSH observation has started. DNS is excluded.

#### Successor failed; local startup blocker reproduced — November 11

The retained receipt records client exit 1, unavailable structured diagnostics
and successful cleanup, about 3.5 seconds after client start. Observation was
not launched. Approval is consumed; the sealed inputs and receipt are preserved.

Two disposable local containers used the pinned image, `--pull never`,
`--network none`, read-only root and dropped capabilities. The dependency import
passed. Reading/parsing the exact mounted sealed client failed with `EACCES` at
container UID 1000, before parsing or entering the diagnostic handler. Neither
probe used credentials or contacted a live target. Results are recorded in
`local-startup-diagnosis.json` beside the failed receipt.

This reproduces a concrete startup blocker, not evidence that credentials or
Caddy failed. W-107's reporting tests did not exercise actual container source
permissions; W-109 owns that missing boundary. Do not relax file privacy or replay
either attempt. A correction needs actual offline container qualification before
a separately reviewed live candidate. DNS remains pending.

#### W-109 private source access corrected and qualified — November 11

The helper uses the invoking user's rootless `keep-id` mapping and explicit UID/GID
for both startup and login containers. No chmod/chown workaround was applied.
Before credential prompts, a network-disabled, closed-stdin startup check reads
and parses the client and imports its dependency. The check is bounded at 30
seconds and shares the existing invocation-owned cleanup path. Its fixed
stage/code diagnostics distinguish source access, syntax and module failures;
startup failure or timeout prevents prompting and launching the login client.

Actual pinned-image qualification is retained at
`/home/aaron/code/.local-evidence/uptime-kuma/private-client-access-20261111-a`.
It reproduces default-user EACCES on 0700/0600 source storage, passes corrected
startup, runs the actual production entrypoint with synthetic credentials and
no network (expected dashboard/IPv4 ENETUNREACH), and rejects malformed source.
File modes, ownership and client bytes remain unchanged in the access test.
All owned containers were removed and execution session 24119 is retired, exit 0.
This proves local startup/access and reporting, not live TLS/authentication.

Fifteen helper tests cover pre-credential failure/timeout gates and existing
receipt/failure/replay contracts. The seven client failure cases plus success
and five observer tests remain required local regression checks. Both consumed
bundles and failed receipts are preserved; no new operation is sealed or approved.

#### Application acceptance with corrected source access: exact bundle, commands and scope

Status: **operator-executed; failed before login; observation not started**. This is separate application
acceptance, not another Caddy deployment operation. One operator check and one
ordered Node A/Node B observation attempt; no retry under consumed approval.

- Bundle SHA-256: `da5ca02cb7b085b5154345eb18054c4e32ccb99e3321b644877e11bce933916b`.
- Frozen input manifest SHA-256: `37f2aa6527b4054f20dc006dafb699137871b0a1473bfa0231e6495986d3682f`.
- Operator command SHA-256: `bfcde22212d410c357fdacb3f7af299f1b1a520e0399510a4d9923068f7a84b9`.
- Observation command SHA-256: `c8c0b9158312f67b3ea589f75c038bb33c46622873a8c129869a8c04a89f3d61`.
- Qualification SHA-256: `9d113ea8a5675c8f661a4ecdac884111c4a89f7140bc5a945157af2843b7e8cb`.
- Private root: `/home/aaron/code/.local-evidence/uptime-kuma/proxy-acceptance-review-8ek3s67y`.
- Accepted release: `20261111T213048Z-71b7deb8-bc71-45d5-8f33-98270af79d3b`.
- Accepted payload manifest: `b972d15185960fc219d09c1c047cd5c2269be97f42e6cc5eef6a3b691aa7d52d`.

**Operator command**, only after approval, in a private workstation WSL/Ubuntu
terminal. Start when ready; no controller/window needs to be running. Credentials
are entered locally and sent through the client's private stdin, never chat,
arguments, environment variables or saved logs. Do not record the terminal.

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/proxy-acceptance-review-8ek3s67y/operator.sh
```

The operator command first uses the pinned local Podman image with `--pull never`
and networking disabled for a 30-second startup check, before credential prompts.
It checks private source readability, JavaScript syntax and dependency loading;
startup failure stops the attempt before credentials or live contact. Both local
containers use rootless `--userns keep-id` with the invoking user's explicit UID/GID,
read-only source mounts, read-only root, dropped capabilities and no-new-privileges.
File modes and ownership are preserved. Startup completes before the login client
uses the same invocation-owned container name with host networking. It contacts only Proxy VIPs `10.1.0.56` and
`fd36:5aa8:6971:1::56` as `uptime.local.theama.co`, using normal TLS validation.
It checks dashboard 200, real WebSocket transport, unauthenticated denial, one
wrong-password rejection per family, immediate correct login, a second client,
65-second authenticated survival and logout denial. Transient authentication
sessions and ordinary server logs are expected; no accounts, monitors, alerts or
data settings are changed. Human credential entry is untimed; the client has a
180-second limit plus bounded local container cleanup. Only a sanitized private
receipt is retained.

**Observer command**, after that receipt passes, under the same exact approval:

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/proxy-acceptance-review-8ek3s67y/observe.sh
```

The command first verifies the private receipt and frozen inputs. It then streams
the observer through strict-existing-host-key SSH as `pi` to `10.1.0.53`, then
`10.1.0.54`, using `sudo -n python3 -` without target file staging. Each node reads
its selected release/manifest/fragment, issues trusted IPv4/IPv6 dashboard and
existing `/healthz` requests to its own addresses and the shared VIPs, and reads
`systemctl show` plus cursor-bounded `journalctl`. Two distinct successful cycles
for each `caddy-sync-health.service` and `caddy-pihole-web-health.service` must
complete after the observer baseline. Cycle polling is five-second cadence, up
to 320 seconds; each node has a six-minute overall alarm and the controller
allows 400 seconds for SSH/readback. No timer/service is invoked to create cycles.

Acceptance requires start/end HTTP observations spanning at least 65 seconds,
unchanged release identities, no relevant journal health failures/exclusions,
completed native cycles and independent combined verification of both node
records and the private receipt. Journal access, parse/size failures and missing
cycles reject. Conservative journal rejection may include unrelated proxy-health
noise; it is not waived automatically. This remains bounded sampled acceptance,
not proof of every internal Caddy health probe.

A failed operator receipt stops before SSH. A failed Node A observation stops
before B. Any later failure retains evidence and stops DNS progression; running
services remain untouched. Existing receipt/evidence paths reject replay. A lost
controller does not trigger rollback; the remote alarm bounds observation.

Excluded: backend SSH; deployment, staging or configuration changes; service or
timer control; publication; failover; account reset; monitor/alert changes;
synthetic notification sending; DNS queries/mutation; automatic retry or rollback.
The helper's uniquely named local container is the only cleanup target. No commit
or push is included. DNS remains conditional and unused with its original
`2026-11-14T17:02:35+00:00` expiry; a combined pass neither executes nor renews it.

This successor includes W-107's credential-safe reporting and W-109's source
access/startup correction. Failure receipts retain bounded stage/family/code,
exit status when available and cleanup outcome, never raw provider errors or
credential values. Startup failures also consume the attempt; no automatic retry
is included. Both earlier bundles and failed receipts remain unchanged.

Qualification: 15 frozen-source helper tests, seven JavaScript failure scenarios
plus success, five observer tests, shell syntax and exact-snapshot secret scan
pass. The scan retains the reviewed nonsecret integrity-hash exceptions. The
helper/client/qualifier hashes and private source modes match the completed four-case
actual pinned-container qualification: original EACCES, corrected startup, actual
client with expected network-disabled failure, and syntax rejection. Its result
is included as `native-client-result.json`. Unchanged observer native qualification
is retained by verified hash. This is local evidence, not live authentication or
production acceptance. `qualification.json` binds evidence; `predecessors.json`
binds both consumed attempts. No live work, commit or push occurred.

#### Third operator attempt: unauthenticated acknowledgement failed — November 11

Aaron ran the presented command and supplied its failure output. There was no
separate preceding approval message or agent authorization record for this bundle;
this records the actual operator execution without retroactively authorizing
observation. The receipt and execution-reconciliation.json retain the outcome.
No passive observation directory exists and no live agent operation ran.

Source control flow establishes that startup, IPv4 trusted dashboard 200 and real
WebSocket transport passed before the unauthenticated getMonitorList request
failed. The client had not reached wrong-password or correct-login checks, nor
IPv6. The 12.4-second elapsed time and 10-second acknowledgement timeout are
consistent with a timeout, but UNCLASSIFIED does not prove that cause.

Offline, network-disabled reads of the pinned image confirm getMonitorList calls
checkLogin and catches its unauthenticated error with an explicit false callback.
Bounded excerpts are retained in local-handler-source.jsonl beside the receipt.
A timeout cannot therefore be accepted as the expected denial without further
evidence. W-111 tracks local reproduction and precise safe error classification.
All local containers exited; no credentials, service changes or live retries were
used in this diagnosis. All three frozen attempts remain preserved.

#### W-111 local acknowledgement diagnosis — November 11

Two isolated actual-image experiments used the pinned Kuma image with networking
disabled, ephemeral database/tmpfs and a generated synthetic account. No Caddy,
production endpoint or real credential was used. The unmodified server returned
explicit false acknowledgements for all six unauthenticated monitor-list probes,
including three issued on transport connect and three after loginRequired.
Evidence: `ack-contract-xmc_qks8` under the private Uptime Kuma evidence root.

Server source awaits sendInfo before registering handlers and emits loginRequired
after registration. A second fixture changed only the connection handler by
adding 100 ms before sendInfo; source hashes and the exact perturbation are retained
in `ack-delay-9mslozdt/perturbation.json`. All three requests sent on connect timed
out at 10 seconds despite loginRequired arriving about 100 ms later. All three
requests sent after loginRequired returned explicit denial within 1–3 ms. The
probe identifies the client's fixed Socket.IO timeout text as ACK_TIMEOUT without
retaining arbitrary exception values.

This demonstrates a timing-sensitive client readiness defect and a correction
direction, but does not prove the historical live UNCLASSIFIED error was this
race. No production timing was measured. Do not waive denial checks, accept a
timeout as denial, or treat this diagnostic as live acceptance. W-112 tracks the
bounded readiness/diagnostic correction and qualification before a new candidate.

Both experiments completed with exit 0 and cleanup 0; sessions 66540 and 63515
are retired. All three frozen manifests and failed-receipt hashes were rechecked
and remain intact. No executable repository source was changed and no new bundle
was sealed. Passive observation and DNS remain pending.

#### W-112 readiness correction qualified — November 11

The client installs listeners before connecting and waits for loginRequired,
which follows server handler registration. Initial synthetic setup additionally
requires setup; unexpected setup/automatic login rejects. Readiness is bounded
at 10 seconds inside the unchanged overall client deadline. Disconnects before
readiness or during an acknowledgement fail explicitly. An acknowledgement error
is classified only into fixed timeout/disconnect/error codes, with no arbitrary
server text retained. Explicit negative acknowledgements are still required for
denial; no sleep or timeout-as-success workaround was added.

The actual corrected client passed the real pinned Kuma/Caddy offline qualifier
with the documented 100 ms server-registration delay, synthetic TLS and generated
account: IPv4 and IPv6 dashboard/TLS, WebSocket, unauthenticated denial, wrong then
correct password, second client, 65-second authenticated idle and logout denial.
Evidence: `proxy-auth-gtwfvnj_` in the existing private Uptime Kuma evidence root;
result binds client and original/perturbed server hashes and fixture substitutions.
Session 12555 exited 0, both containers were removed and no live target was contacted.

The repository's existing native qualifier now supports the explicit local delay
option and owner-private sources through keep-id mapping. JavaScript regressions
cover 13 failure scenarios plus immediate/delayed readiness success; Python tests
cover acceptance of the new enum-only diagnostics. The historical live failure
remains unconfirmed; this qualifies the demonstrated local client correction.
No successor is sealed. W-106, DNS and other open findings remain pending.

#### Application acceptance with readiness gate: exact bundle, commands and scope

Status: **private login passed; approved observation failed on Node A; authority consumed**. This is separate application
acceptance, not another Caddy deployment operation. One operator check and one
ordered Node A/Node B observation attempt; no retry under consumed approval.

- Bundle SHA-256: `d47b44ed51c345f3eb48c7a5a4d78ae144854926dfecc491c61d927027ec8b2e`.
- Frozen input manifest SHA-256: `50a7aef67f61b1a76ef38d6ca247328b62f5e63537c4d55dc9c2628b06e74ee5`.
- Operator command SHA-256: `e1c51150fb0a3c8377ecf4f4022928dd46edb733b8b11141143d4f4ee987a5b2`.
- Observation command SHA-256: `34024c1099d7d1b1f2b95236faffb6b924eab96388e1e8615f6ec5c6be0fd6e6`.
- Qualification SHA-256: `d4de6bdd67539ad6de882090fe1fc1eeff8b3f8b41ac1dbde2c008819764d2c3`.
- Private root: `/home/aaron/code/.local-evidence/uptime-kuma/proxy-acceptance-review-t_v4hx55`.
- Accepted release: `20261111T213048Z-71b7deb8-bc71-45d5-8f33-98270af79d3b`.
- Accepted payload manifest: `b972d15185960fc219d09c1c047cd5c2269be97f42e6cc5eef6a3b691aa7d52d`.

**Operator command**, only after approval, in a private workstation WSL/Ubuntu
terminal. Start when ready; no controller/window needs to be running. Credentials
are entered locally and sent through the client's private stdin, never chat,
arguments, environment variables or saved logs. Do not record the terminal.

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/proxy-acceptance-review-t_v4hx55/operator.sh
```

The operator command first uses the pinned local Podman image with `--pull never`
and networking disabled for a 30-second startup check, before credential prompts.
It checks private source readability, JavaScript syntax and dependency loading;
startup failure stops the attempt before credentials or live contact. Both local
containers use rootless `--userns keep-id` with the invoking user's explicit UID/GID,
read-only source mounts, read-only root, dropped capabilities and no-new-privileges.
File modes and ownership are preserved. Startup completes before the login client
uses the same invocation-owned container name with host networking.
The client installs listeners before connecting and waits up to 10 seconds for
Kuma's `loginRequired` event before any protected request. Unexpected setup or
automatic login rejects; readiness timeouts and disconnects fail explicitly.
Acknowledgement timeout never counts as denial. The existing overall client
limit still applies; no fixed sleep, reconnect or automatic retry is added. It contacts only Proxy VIPs `10.1.0.56` and
`fd36:5aa8:6971:1::56` as `uptime.local.theama.co`, using normal TLS validation.
It checks dashboard 200, real WebSocket transport, unauthenticated denial, one
wrong-password rejection per family, immediate correct login, a second client,
65-second authenticated survival and logout denial. Transient authentication
sessions and ordinary server logs are expected; no accounts, monitors, alerts or
data settings are changed. Human credential entry is untimed; the client has a
180-second limit plus bounded local container cleanup. Only a sanitized private
receipt is retained.

**Observer command**, after that receipt passes, under the same exact approval:

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/proxy-acceptance-review-t_v4hx55/observe.sh
```

The command first verifies the private receipt and frozen inputs. It then streams
the observer through strict-existing-host-key SSH as `pi` to `10.1.0.53`, then
`10.1.0.54`, using `sudo -n python3 -` without target file staging. Each node reads
its selected release/manifest/fragment, issues trusted IPv4/IPv6 dashboard and
existing `/healthz` requests to its own addresses and the shared VIPs, and reads
`systemctl show` plus cursor-bounded `journalctl`. Two distinct successful cycles
for each `caddy-sync-health.service` and `caddy-pihole-web-health.service` must
complete after the observer baseline. Cycle polling is five-second cadence, up
to 320 seconds; each node has a six-minute overall alarm and the controller
allows 400 seconds for SSH/readback. No timer/service is invoked to create cycles.

Acceptance requires start/end HTTP observations spanning at least 65 seconds,
unchanged release identities, no relevant journal health failures/exclusions,
completed native cycles and independent combined verification of both node
records and the private receipt. Journal access, parse/size failures and missing
cycles reject. Conservative journal rejection may include unrelated proxy-health
noise; it is not waived automatically. This remains bounded sampled acceptance,
not proof of every internal Caddy health probe.

A failed operator receipt stops before SSH. A failed Node A observation stops
before B. Any later failure retains evidence and stops DNS progression; running
services remain untouched. Existing receipt/evidence paths reject replay. A lost
controller does not trigger rollback; the remote alarm bounds observation.

Excluded: backend SSH; deployment, staging or configuration changes; service or
timer control; publication; failover; account reset; monitor/alert changes;
synthetic notification sending; DNS queries/mutation; automatic retry or rollback.
The helper's uniquely named local container is the only cleanup target. No commit
or push is included. DNS remains conditional and unused with its original
`2026-11-14T17:02:35+00:00` expiry; a combined pass neither executes nor renews it.

This successor includes the source-access, safe-reporting and application-readiness
corrections. Safe failures retain only bounded stage/family/code, exit status when
available and cleanup outcome. All three earlier attempts and failed receipts are
preserved. Their authority does not authorize this candidate.

Qualification against frozen inputs: 16 helper tests, 13 JavaScript failure cases
plus immediate/delayed readiness success, five observer tests, shell syntax and
exact-snapshot secret scan passed. The scan retains the reviewed nonsecret
integrity-hash exceptions. The exact frozen helper/client also passed four actual
pinned-container source/startup cases with networking disabled and private files.
The client matches the completed real offline Kuma/Caddy qualification with a
100 ms registration delay: both address families passed full authentication,
65-second idle and logout checks. Synthetic CA/account and fixture substitutions
are explicit; this does not establish production trust or authentication.

`qualification.json` binds the checks, `native-auth-result.json` and
`native-auth-rows.jsonl` retain the applicable full offline result, and
`startup-qualification/result.json` binds the new exact-source container check.
Unchanged native observer qualification is retained by hash. `predecessors.json`
binds all three prior attempts. No live work or publication occurred.

#### Private login acceptance passed — November 11

Aaron executed the presented operator command and reported success. The frozen
helper independently verified its owner-private receipt: correct operation and
client identity, exact expected IPv4/IPv6 rows, valid timestamps and 70.03-second
duration. All seal and frozen-input hashes passed local verification. Accepted
checks include trusted TLS/dashboard, WebSocket transport, unauthenticated denial,
wrong-password rejection, correct login, second client, 65-second authenticated
idle survival and logout denial. No credential values were read or retained.

`execution-reconciliation.json` in `proxy-acceptance-review-t_v4hx55` binds the
verified receipt and seal. There is no preceding separate approval message or
execution-authorization.json for this scope, so the operator action establishes
its own completed login check without inferring authority for further target
inspection. The observation directory is absent. The same sealed observer command
above remains reviewable for one ordered Node A/Node B attempt; do not rerun login.
DNS remains excluded and pending; no project closeout is claimed.

#### Remaining passive observation authorized and launched — November 11

Aaron explicitly approved the remaining passive observation under the sealed
scope above. Seal/input hashes and the passing private receipt were reverified;
the destination was absent. execution-authorization.json records this remaining
scope and one launched attempt. Session 61489 owns the exact observe.sh execution;
observer-execution.log/status and per-node records retain its output. DNS and
repeat login are excluded. Await this session; do not replay.

#### Passive observation terminal result — November 11

The approved observe.sh ran once and exited 1. Node A completed two passing
dual-stack HTTP batches about 80.67 seconds apart, retained the accepted release/
manifest/fragment at both ends, and recorded two distinct successful completed
cycles for each monitored unit. These are partial results, not full acceptance.

The final cursor-following journalctl command returned exit 1. The observer
retained the expected/observed exit status but discarded command stderr, so the
reason is not established. This does not show either adverse journal events or
a clean journal. Node B was not contacted and combined verification did not run.
The previously verified private login remains accepted.

Private evidence: observation/node-a.* and terminal-summary.json under
proxy-acceptance-review-t_v4hx55; observer-execution.log/status capture the
controller failure. W-114 tracks local diagnosis and diagnostic qualification.
Session 61489 is complete and retired; approval is consumed. No service was
changed, no retry occurred and DNS remains excluded/pending.

#### W-114 journal read and safe diagnostics qualified — November 11

Offline journalctl 252 returned exit 1 with empty stdout/stderr for a cursor-bounded
query with no matching unit entries when show-cursor was requested; removing
that flag returned exit 0. An invalid cursor returned exit 1 with a distinct
seek error. The final collector does not use an output cursor, so that flag was
removed only from the final read. Baseline cursor capture remains required.
A nonzero final read still rejects, including when both output streams are empty.

The initial probe is retained under journal-contract-m2pftkn1. Its optional seed
unit command ran before the container bus was ready and failed; cursor capture
and no-match probes still ran. The final native qualification repeated the
contract checks after fixture readiness, so that initial seed failure is not
used as proof of successful service setup.

Command failures now retain fixed program/operation labels, expected/observed
exit status, output byte counts and a fixed diagnostic category (no-output,
invalid-cursor, permission-denied, timeout, launch-error, output-limit or
unclassified). No raw argv, cursor, stdout/stderr or journal messages enter the
reported failure. Existing size, parse, journal-health, service-cycle and cadence
gates remain. The recorded live failure cannot be conclusively attributed to
the empty-result behavior because its stderr and cursor were not retained.

Ten observer tests passed, including empty success, failed-empty rejection,
invalid/private diagnostic redaction, timeout/launch/size errors, stale cycles
and tampered evidence. Actual offline systemd/Caddy qualification at
proxy-observer-native-l5ewq_mt passed the full corrected observation with zero
journal events and a 65.44-second HTTP span; the old empty read failed, corrected
empty read passed and invalid cursor was rejected. Source/image hashes and exact
results are retained there. Session 53761 exited 0 with cleanup 0; initial
diagnostic session 58360 also completed and was retired. No live target was used.

The previously accepted private login remains valid. All consumed bundles and
receipts remain preserved. No observation successor is sealed or authorized;
W-106 and DNS remain pending.

#### Observation-only continuation: exact bundle, command and scope

Status: **executed once and passed; authority consumed**. One ordered Node A/Node B passive
observation attempt, followed by local combined verification. No login repeat.

- Private root: `/home/aaron/code/.local-evidence/uptime-kuma/proxy-observation-review-c9vdnab_`.
- Observation attempt: `uptime-kuma-passive-observation-c9vdnab-`.
- Acceptance identity: `uptime-kuma-application-acceptance-t-v4hx55` (retained for the accepted login receipt).
- Bundle SHA-256: `51d32023d71063d5562feb7cd3537e57c3713a74f12d40f5a09fb453785badc8`.
- Frozen input manifest SHA-256: `467a7fbecfbdf5a338add7408b3f2ca7efb34b8b7a46aa75f0af06028392b080`.
- Observation command SHA-256: `9fa1b1e8e1f260016a32ad79a80c6d3eb8ac2f9de4ee7d012e6c0f432156f1d2`.
- Qualification SHA-256: `4f628554e70dd180f5d9b63dbfe208dca837b8a30849dc66492d438655f5b1ec`.
- Accepted private receipt SHA-256: `f5d0cbbca9857c36071715f140e92be2da4b9779b1feda0550bc368c17595d8c`.
- Accepted release: `20261111T213048Z-71b7deb8-bc71-45d5-8f33-98270af79d3b`.
- Accepted payload manifest: `b972d15185960fc219d09c1c047cd5c2269be97f42e6cc5eef6a3b691aa7d52d`.

**Exact command, only after approval:**

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/proxy-observation-review-c9vdnab_/observe.sh
```

The command verifies frozen inputs and an unchanged owner-private copy of the
previously accepted login receipt before SSH. The copy's original path and hash
are bound in predecessors.json and the input manifest. Its original acceptance
identity stays unchanged; observation_attempt and a fresh exclusive evidence
directory distinguish this continuation. Prior observation records are not reused.
No credential prompt or client container runs. Approval covers one attempt only.

Targets: strict-existing-host-key SSH as pi to 10.1.0.53, then 10.1.0.54 only if
Node A passes. The collector is streamed to sudo -n python3 without target staging.
It reads accepted release/manifest/fragment identities, requests trusted IPv4/IPv6
dashboard HTTP from each node and Proxy VIPs (10.1.0.56 and
fd36:5aa8:6971:1::56), checks each node's existing healthz route, and reads systemctl
show plus cursor-bounded Caddy journal data. No service or timer is triggered.

Each node requires two successful completed cycles after its observation baseline
for caddy-sync-health.service and caddy-pihole-web-health.service, two passing HTTP
batches spanning at least 65 seconds, unchanged identities and no relevant journal
health failures/exclusions. Cycle sampling remains five-second cadence, up to
320 seconds; the remote overall alarm is six minutes and controller timeout is
400 seconds per node. This is bounded sampled acceptance, not proof of every
internal Caddy health probe. Combined verification checks both nodes and the
accepted private receipt; a pass still leaves DNS pending.

The final journal read omits unused show-cursor output. Baseline cursor capture
is still mandatory. Empty output is accepted only on exit 0; nonzero exits,
inaccessible/malformed/truncated journal evidence and adverse events still fail.
Command failures retain safe stage/status/count/category fields, never raw
journal messages or command stderr. No failure condition is waived.

Any failure stops the attempt and retains evidence; Node A failure prevents B.
The fresh directory rejects replay. Running services remain untouched; controller
loss triggers no rollback, and the remote alarm bounds any in-flight observation.
No automatic retry, repair, reset-failed, restart, failover, deployment, backend
SSH, account/monitor/alert change, notification send, DNS query/change or Git
publication is included. DNS's original conditional expiry remains
2026-11-14T17:02:35+00:00; this approval neither executes nor renews it.

Qualification: ten frozen observer tests and sixteen helper tests pass, along
with unchanged-receipt verification, command syntax and exact-source secret scan
using the reviewed nonsecret integrity-hash exceptions. Corrected observer bytes
match the full successful offline systemd/Caddy run; its journal empty-result and
invalid-cursor checks are retained by hash. That is synthetic local qualification,
not production acceptance. No new live work ran. All four predecessor bundles,
failed observations and private receipts remain preserved.

#### Observation-only continuation approved and launched — November 11

Aaron approved the exact bundle, command and scope above. Frozen inputs and
accepted private receipt were verified; the destination was absent. Approval
and one launched attempt are recorded in execution-authorization.json under
proxy-observation-review-c9vdnab_. Session 34421 owns observe.sh; its private
log/status and per-node records retain output. No repeat login or DNS is included.

#### Observation-only continuation accepted — November 11

The approved observe.sh exited 0. Node A and Node B each passed trusted IPv4/IPv6
node/shared-dashboard and existing healthz checks, with unchanged accepted release,
manifest and fragment identities. The HTTP spans were 85.64 seconds on A and
130.81 seconds on B. Successful distinct completed cycles: sync-health 2/2 and
pihole-web-health 3/4 (A/B). Both final journal reads succeeded with zero matching
events and zero adverse events. This is bounded-window evidence, not a guarantee
of every internal health probe or future uptime.

Combined verification passed through the sealed command and again independently
from retained local evidence, binding both nodes to the accepted private-login
receipt and release 20261111T213048Z-71b7deb8-bc71-45d5-8f33-98270af79d3b. W-106
is resolved. Private evidence is retained under proxy-observation-review-c9vdnab_: per-node
records, combined-result.json, terminal-summary.json and observer-execution.log/status.
The prior failed attempts and original login receipt remain preserved.

Session 34421 is retired with exit 0; approval is consumed. No login was repeated,
no service changed, and no DNS or Git publication ran. DNS remains separately
governed and pending; its original conditional expiry is 2026-11-14T17:02:35+00:00.
Reconcile the DNS owner's candidate/conditions before progression. W-020/W-076
and documentation/closeout remain open; W-096 remains deferred.

### Repository publication qualification — November 11

Aaron authorized commit and push of all pending source changes. Reviewed scope:
Kuma application/change record, host foundation and Webmin/needrestart profiles,
neutral Caddy archive cleanup, Mailrise defaults and the guarded permanent ULA
owner tasks. Private evidence and the empty server-config scratch file `oom`
are excluded. The consumed operation archives remain intact.

Source-only snapshots of all four repositories passed Gitleaks. Working-tree
findings outside those snapshots were ignored local index hashes. Server CI's
secret-scan finding was the documented outer-runner digest, verified against
its published terminal tag; the exception matches only that digest. All staged
pre-commit hooks passed. Kuma foundation/backend tests, five Ansible syntax
checks, 26 Python client/observer tests, JavaScript contract tests and 51 Webmin
tests passed locally. Tests needing loopback sockets ran outside the filesystem
sandbox; no production host was contacted.

Caddy repository-policy checks passed. Serving-health initially rejected the
adjacent newer DNS source hash; an isolated workspace using CI's accepted DNS
revision `9ae13d0b03a4cec4124d411dd86b273462370129` passed serving-health and
synchronization checks. Production hash contracts were not changed to hide that
dependency difference.

The reported November 11 Nautobot failure at `eca1d0c` is superseded by successful
Nautobot jobs at `8999dde` and `e6fa531`. The reported CodeQL startup failure has
no jobs or annotations available. The Webmin PR notification refers to an
October 12 run whose logs are unavailable; no cause or repair is claimed for it.
Publication evidence, checks and remote receipts are retained privately under
`/home/aaron/code/.local-evidence/homelab-publication-wp4gyd4h/`.

Network commit `0ab74630cb38afb7fd6bbaf77210f9260519c7ed` and DNS commit
`b1bdd9077e4621db82cdecf65c59635c340e0ee6` are pushed and remote-verified; each
passed Repository validation and CodeQL. Server-config commit
`3a27837f2a7dce023fc77154aff65aae7863106c` is pushed and remote-verified; its
CI is running. Monitoring publication is in progress. DNS activation remains
separately governed and pending.

### Source publication accepted — November 11

All reviewed source changes are published and remote-verified:

| Repository | Published source commit | Repository validation | CodeQL |
| --- | --- | --- | --- |
| homelab-server-configs | 3a27837f2a7dce023fc77154aff65aae7863106c | 43124149510: success | 43124148826: success |
| homelab-monitoring-observability | 406349aa5d3bb4725416ebb5812ab5eeeb8e9c9f | 43124324323: success | 43124323435: success |
| homelab-dns | b1bdd9077e4621db82cdecf65c59635c340e0ee6 | 43123734307: success | 43123733191: success |
| homelab-network | 0ab74630cb38afb7fd6bbaf77210f9260519c7ed | 43123731133: success | 43123730083: success |

W-116 is resolved. The later documentation-only commit records these outcomes;
its source ancestor is identified above. Server validation includes successful
Caddy, baseline and Nautobot/Restic jobs; the prior secret-scan failure is fixed.
The new CodeQL run passed, without establishing the historical startup failure's
cause. The old upstream Webmin run remains unverified because its logs are
unavailable; no upstream code or workflow was changed.

Private evidence and the empty `homelab-server-configs/oom` scratch file were not
committed. Temporary qualification worktrees were removed. Publication does not
activate DNS or close the remaining project findings. W-020/W-076 and permanent
documentation/closeout remain open; W-096 is deferred. No live host action occurred.

### DNS candidate and authority reconciliation — November 12

W-117 is resolved locally. The unchanged DNS archive identified in
[the exact owner review](#exact-owner-bundles-commands-and-scope--awaiting-approval)
passes the owner runner's non-contact `check` action. Every frozen member and the
internal index match. The three execution helpers match current DNS owner source;
the retained qualification and six provenance files also match their bound hashes.
No invocation marker, gate, controller result or node receipt exists in the
sealed directory. The original approval remains unused; no timestamp was renewed.

The preserved W-106 private receipt, specification, frozen input indexes and both
node observation records pass the existing combined verifier locally. Accepted
release `20261111T213048Z-71b7deb8-bc71-45d5-8f33-98270af79d3b` satisfies the DNS
review's application-acceptance prerequisite. The DNS operation does not bind
execution to the failed earlier Caddy attempt. This is reconciliation of retained
acceptance, not a fresh observation or permission to replay any consumed Caddy
operation.

The current repository zone differs from the sealed baseline only in directive
ordering; comparison including duplicate counts confirms identical record
content. The six-record candidate remains an append-only extension of the exact
retained live baseline. Preserve these sealed bytes. Do not substitute the
repository file, infer current live identity, or weaken preflight to accommodate
a mismatch. After accepted DNS execution, reconcile owner source record content
and live-state documentation.

Original expiry: November 14, 2026 at 11:02:35 a.m. CST
(`2026-11-14T17:02:35+00:00`). Every runner invocation, including recovery,
requires more than five minutes remaining; therefore it must begin before
10:57:35 a.m. CST. Start with enough time for the complete operation and recovery.
Do not extend timestamps, replay a phase or bypass an expired guard.

Recommended progression remains the existing `before`, `apply-secondary`,
`after-secondary`, `apply-primary`, `after-all` sequence, with the reviewed
conditional recovery and ordinary-name HTTPS checks. The original approval is
not consumed by this local review and need not be requested again. Aaron's
current instruction explicitly excludes live work; wait for his instruction to
resume execution. Exact live file/binary/boot checks, fresh paired gates,
expected initial VIP ownership and native candidate validation remain mandatory.
Retained identity provenance does not establish today's target state.

Private reconciliation evidence:
`/home/aaron/code/.local-evidence/uptime-kuma/dns-reconciliation-20261112-y4jntav7/reconciliation.json`.
The DNS [owner review](../../../homelab-dns/Unbound/docs/uptime-kuma-host-record-review.md#local-reconciliation--november-12-2026)
records the same disposition. No new fixtures, seal, SSH/DNS/HTTPS requests,
service actions, commit or push occurred. W-020/W-076 and documentation/closeout
remain open; W-096 stays deferred. No execution session is active.

### DNS execution resumed — November 12

Aaron approved resuming the existing DNS sequence. The original archive and
local expiry check passed; no prior invocation or node receipt exists. The
unchanged conditional scope covers the five phases, reviewed recovery and final
ordinary-name HTTPS checks. Authorization is recorded privately in the sealed
review directory's execution-authorization.json; frozen inputs are unchanged.

### DNS initial gate failed before mutation — November 12

Session 89316 completed with exit 1. The one-use `before` phase exhausted its
180-second paired-gate convergence window, repeatedly retaining only
`snapshot_transport_failed`. Its gate receipt remains `accepted=false`. The
verifier raises that category for a nonzero remote command exit or oversized
output; it does not retain the underlying return code, stdout or stderr. Thus
SSH transport, remote preflight rejection and other remote-command failure
cannot be distinguished from this evidence. The deadline label does not prove
an HA convergence or DNS service failure.

Neither apply phase was invoked. No zone replacement, Unbound/Pi-hole restart,
rollback, ordinary-name HTTPS check or later phase ran. Recovery is unnecessary
because the executed phase is read-only. The original operation is now
failed-consumed: its unused later phases are not permission to bypass the failed
gate, remove the receipt or retry. Preserve the frozen archive, before invocation,
controller log/exit, rejected gate and terminal-summary.json in the existing
private bundle. W-118 records the diagnostic gap. No additional live inspection
or successor is authorized; DNS remains pending. Session 89316 is retired.

### DNS snapshot diagnostics corrected and qualified — November 12

W-118 local reconciliation confirms the reporting defect in the consumed
verifier: nonzero subprocess status and oversized output both became
snapshot_transport_failed, with the underlying status and output discarded.
Retained evidence cannot distinguish transport failure from remote preflight
rejection. No historical cause is inferred from a synthetic reproduction.

The DNS owner's current verify-host-records.py reports a bounded JSON diagnostic
with node label, failure category, expected/observed exit status, stream byte
counts, launch errno where applicable and an allowlisted error hint. Raw stderr,
stdout, credentials, arbitrary RuntimeError messages and command arguments are
not echoed. Timeout, launch failure, malformed/non-object output and size-limit
failure remain rejected. Existing identity/hash/trust checks and paired-gate
convergence behavior are unchanged; no automatic bypass or replay was added.

The existing owner test suite passes 34 tests. Added cases cover safe SSH/sudo
and remote RuntimeError hints, unknown-message suppression, secret canaries,
local-launch and subprocess timeout, output limits, empty/malformed/non-object
results, normal event-prefixed result decoding and safe diagnostics at the
paired deadline without advancing to the peer. The actual streamed node source
was executed through local Python and rejected a deliberately invalid identity
with an accurately classified exit; this used no SSH, DNS or service operation.
No additional DNS fixture or simulated failover was built.

Qualification and exact source identities are retained privately at
`/home/aaron/code/.local-evidence/uptime-kuma/dns-diagnostics-qualification-fdihlcwa/`.
Every frozen member of the consumed archive remains byte-identical; failed
receipt/log identities are recorded there. Local correction does not modify the
consumed runner or renew its approval. No successor has been prepared or sealed.
Vexp completion verification is unavailable from the parent workspace; focused
owner tests provide the mechanical check. DNS remains pending and no live
contact, publication or replay occurred. All local checks are complete.

### DNS successor sealed for review — November 12

Preparation is complete under W-119; this is not execution authorization.

- Operation: `uptime-kuma-dns-20261112-q8i4a51n`.
- Archive SHA-256: `0cc507728f976d0b51acb30803e785428b901c3fe4a68d6bedd3d77acc45c089`.
- Private directory: `/home/aaron/code/.local-evidence/homelab-dns/current/uptime-kuma-dns-20261112-q8i4a51n`.
- Exact scope, individual phase commands, recovery and ordinary-name HTTPS checks:
  `review.md` in that directory. `provenance.json` binds the consumed predecessor,
  failed receipt/log identities, retained application acceptance and W-118 qualification.
- Expiry: November 14, 2026 at 11:02:35 a.m. CST
  (`2026-11-14T17:02:35+00:00`), unchanged from the predecessor.
  Every invocation, including recovery, must begin before **10:57:35 a.m. CST**;
  allow time for the entire operation and recovery, not just initial admission.

#### Exact successor bundle, commands and scope — awaiting approval

One approval covers this archive and the following individually gated sequence:

```bash
dns_bundle=/home/aaron/code/.local-evidence/homelab-dns/current/uptime-kuma-dns-20261112-q8i4a51n
reviewed_dns_sha256=0cc507728f976d0b51acb30803e785428b901c3fe4a68d6bedd3d77acc45c089
python3 -I -B "$dns_bundle/runner.py" step --directory "$dns_bundle" --sha256 "$reviewed_dns_sha256" --phase before
python3 -I -B "$dns_bundle/runner.py" step --directory "$dns_bundle" --sha256 "$reviewed_dns_sha256" --phase apply-secondary
python3 -I -B "$dns_bundle/runner.py" step --directory "$dns_bundle" --sha256 "$reviewed_dns_sha256" --phase after-secondary
python3 -I -B "$dns_bundle/runner.py" step --directory "$dns_bundle" --sha256 "$reviewed_dns_sha256" --phase apply-primary
python3 -I -B "$dns_bundle/runner.py" step --directory "$dns_bundle" --sha256 "$reviewed_dns_sha256" --phase after-all
```

This is not an unconditional shell paste. Execute one phase at a time, inspect
its result, and stop on the first failure. Each phase consumes its own receipt;
no retry or receipt deletion is permitted. Initial paired acceptance must place
all four coupled VIPs on .53; apply on pi@10.1.0.54 first, then pi@10.1.0.53.
Each mutation requires a successful paired gate no older than 120 seconds.

The only DNS change is the existing six-record addition: dashboard A/AAAA to
Proxy VIP .56/::56, host A/AAAA to .75/::75 and both host PTRs. Preserve unrelated
records and Proxy PTRs. Exact baseline file/binary/boot/include checks and native
candidate validation remain mandatory. On each changed node, atomically replace
the zone file, fully restart Unbound, establish health, then fully restart
Pi-hole DNS. Require paired DNS/Caddy health, exact answers over both families
and coherent ownership of the four linked VIPs before advancing. Normal
cluster-driven movement is permitted; forced failover is not.

On failure, inspect mutation and automatic recovery evidence. A failed `before`
gate makes no mutation and needs no rollback. For changed nodes, restore only
those requiring recovery using their own exact backups, primary before secondary
if both changed. Use the same runner and digest with `rollback-primary`,
`after-rollback-primary`, `rollback-secondary`, `after-rollback-all` as applicable;
if only the secondary changed, use only `rollback-secondary` and
`after-rollback-all`. Restoration includes both full restarts and paired acceptance.
Do not repeat verified automatic restoration. Lost workers, changed destination,
unknown write state, unavailable backup or unproved recovery require manual
intervention; do not restart the sequence.

After successful `after-all`, run the two exact ordinary-name HTTPS commands in
the sealed review: one IPv4 and one IPv6 request to the dashboard, each bounded
to 15 seconds, with normal certificate verification and expected HTTP 200.
A workstation resolution failure remains separate from accepted owner DNS state;
do not roll back accepted DNS solely to hide that client-path failure.

Excluded: Caddy configuration/restart, backend mutation, package changes, account
changes, monitors/alerts, synthetic notifications, route/radio changes, forced
failover, reboot, unrelated DNS changes and Git publication. W-020/W-076 and
project closeout remain separate. Existing Caddy/private-login/passive evidence
satisfies the application prerequisite; retained health is not a fresh live check.

Only the W-118 diagnostic verifier, fresh operation/backup namespace, preparation
time and provenance differ from the consumed candidate. Candidate, baseline,
expanded configuration, host-key pins, node transaction, dispatcher, runner and
expiry are unchanged. The new sealed review states these differences; the old
archive and failed receipts remain byte-identical. The historical live cause
remains unknown and may cause this new attempt to reject too.

Local qualification: closed-archive/member/index check passed, the verifier/test
hashes match the recorded 34-test W-118 qualification, an invalid archive digest
was rejected, and the exact candidate secret scan passed. No new platform
fixture or live probe was run. The fresh directory has no phase/dispatch receipts.
The local preparation and negative-check records are beside the new seal.
The previous approval was consumed by its failed before gate; this successor
requires fresh exact-bundle authorization under the
[DNS owner procedure](../../../homelab-dns/Unbound/docs/host-record-deployment.md#deployment-readiness).
No approval, target contact, commit or push occurred during preparation.

### November 12: DNS successor authorized and started

Aaron approved the exact bundle, commands and scope in the successor section
above for one attempt. Archive identity and original expiry were verified before
launch. The exclusive authorization receipt is retained beside the sealed bundle.
The `before` phase started in session 3863; its controller log, invocation and
terminal status belong to `uptime-kuma-dns-20261112-q8i4a51n`. No apply phase has
started. Preserve the consumed predecessor. Advance only after each successful
fresh gate; no replay or expanded inspection is authorized.

### November 12: DNS successor stopped before mutation — W-120

The approved `uptime-kuma-dns-20261112-q8i4a51n` attempt completed its bounded
`before` phase with exit 1. The corrected diagnostics retain repeated secondary
`boot_identity_mismatch` failures: expected command exit 0, observed 1, zero
stdout bytes and 191 stderr bytes. The remote guard compares the current boot ID
with the sealed expected boot ID. This establishes a stale boot-identity
prerequisite for this attempt, not a DNS service failure. It does not establish
the cause of the earlier attempt, whose underlying diagnostics were discarded.
The observed boot ID and when or why it changed remain unknown.

The paired gate returned `accepted=false`. The secondary snapshot failed before
the primary snapshot; primary contact and paired health acceptance did not occur.
Only `before-invocation.json` exists; there are no apply receipts. No zone write,
Unbound/Pi-hole restart, rollback or final dashboard request ran. No recovery is
required. Approval is consumed; no retry or additional inspection is authorized.

The unchanged sealed archive and its predecessor remain retained. The successor
contains `before-controller.log`, `before-controller.exit`, `gate-before.json`,
its invocation and authorization, and `terminal-summary.json` binding their
hashes. Session 3863 exited 1 and is retired. W-120 tracks identity reconciliation;
DNS remains pending. Existing private/application acceptance is unchanged.

### November 12: retained boot-identity reconciliation — W-120

The sealed secondary boot identity traces to the October 20 DNS readiness
capture (`ntp1-dns54-readiness-20261020-v1/transport-4.json`). Its before/after
identity agrees, and its hash matches the successor's retained provenance.
The October 21 `munin-svmf-dns-deployment-20261021-v1` operation binds the same
identity and has an accepted final paired gate. Both November DNS attempts
inherited that value unchanged. Their primary boot identities were also inherited.

The November 9 `initial-deployment-20261109-9jtrff4m/dns0-stdout.log` and
`dns1-stdout.log` captures do not record a boot identity. Neither does the
accepted `proxy-observation-review-c9vdnab_` observation output. These records
cannot supply a replacement or establish when or why the secondary boot changed.
This is a bounded review of the relevant retained records, not a claim that
no other workspace record could contain a boot identity.

The actual node guard rejects immediately after hostname/root checks, before
binary, include, file and service checks. The failed gate therefore does not
qualify those later prerequisites or the primary. A boot-only substitution
would leave readiness incomplete. Use the existing DNS owner's bounded read-only
readiness procedure for both nodes: current identity, exact zone and metadata,
effective include graph and non-secret binary/service identities, local/node/VIP
DNS health and coherent coupled ownership. Compare with retained expectations;
review drift rather than overwriting it. Preserve six-record scope and existing
acceptance/recovery policy. W-121 tracks preparation for separate inspection
review; no inspection command or deployment successor is sealed here.

Private `dns-boot-reconciliation-kyqtl28p/reconciliation.json` under the Uptime
Kuma evidence store binds the inspected provenance and source hashes. Both
archive digests and both attempts' retained failed-evidence hashes were verified.
No consumed member or receipt was changed. No target contact, code change,
service action, publication or replay occurred. W-120 is resolved for local
reconciliation; DNS readiness and deployment remain pending.

### November 12: paired DNS readiness prepared — W-121

The DNS owner's existing `inspect-ntp-dns-readiness.py` now has an explicit
`--uptime` mode. It retains the existing protected file/include handling, strict
established host-key transport, bounded in-memory collector and exclusive
one-use receipt. It reads current boot identity and requires before/after
stability; it does not relax the deployment's exact boot checks. No deployment
candidate is generated, and neither consumed deployment is changed.

The mode adds current Caddy service state, all four coupled VIP roles, Uptime
record queries, executable hashes, sanitized launch definitions and a cursor-only
journal read. Current configuration is checked natively; its identical expanded
copy is checked through stdin. Existing NTP controls and local/public DNS checks
remain. All observations require local reconciliation before deployment.

Local qualification: 27 readiness tests and 34 transaction tests passed. Tests
extend the existing suite and capture harness; no new platform fixture or
simulated failover was built. Tests cover scope/boot bindings, fixed query counts,
proxy-VIP drift, baseline preservation and credential-safe launch projection.
Both exact frozen payloads ran through actual local isolated Python and rejected
the workstation identity before collection; this proves startup/identity rejection,
not the live collection path. Closed archive/member checks, invalid-digest rejection
and per-archive secret scans passed. `vexp verify_done` was unavailable because
its session root is the non-Git parent workspace; owner checks were used.

Evidence: private `dns-readiness-qualification-4mbr3m3u/final-result.json` and
adjacent logs under the Uptime Kuma evidence store. The unapproved v1 preparation
archives were superseded during local review; v2 below is the only review candidate.
No phase receipt exists in either v2 archive directory. No host contact, service
change, commit or push occurred. Local sessions 10276 and 69657 ended with exit 0
and are retired.

#### Exact paired read-only readiness scope — awaiting approval

One approval covers one capture per node, secondary first, using these two
private directories under `/home/aaron/code/.local-evidence/homelab-dns/current/`:

| Node | Directory | inspection.tar SHA-256 |
| --- | --- | --- |
| pi@10.1.0.54 | uptime-kuma-dns54-readiness-20261112-v2 | `689c3b603b64ff3f524e4fab9997969852378f21b90bd3156b5926fffd9eafc1` |
| pi@10.1.0.53 | uptime-kuma-dns53-readiness-20261112-v2 | `3a752a4cb1e09b548a57e74a047b10f6a4f1e0d2b6572fd79e7f2fbef0632467` |

Both expire **November 13, 2026 at 9:59:03 a.m. CST**
(`2026-11-13T15:59:03+00:00`). The runner's five-minute margin makes the invocation
cutoff **9:54:03 a.m. CST**. Start with enough time for both bounded captures.

```bash
readiness_root=/home/aaron/code/.local-evidence/homelab-dns/current
python3 -I -B "$readiness_root/uptime-kuma-dns54-readiness-20261112-v2/runner.py" execute --directory "$readiness_root/uptime-kuma-dns54-readiness-20261112-v2" --sha256 689c3b603b64ff3f524e4fab9997969852378f21b90bd3156b5926fffd9eafc1
python3 -I -B "$readiness_root/uptime-kuma-dns53-readiness-20261112-v2/runner.py" execute --directory "$readiness_root/uptime-kuma-dns53-readiness-20261112-v2" --sha256 3a752a4cb1e09b548a57e74a047b10f6a4f1e0d2b6572fd79e7f2fbef0632467
```

Run individually, not as an unconditional paste. Inspect .54's result first;
stop on a failed/incomplete capture. Each command consumes an exclusive receipt;
never replay or remove receipts. Capture success alone is not DNS health or
deployment acceptance. After both captures, reconcile identities, native checks,
answers, effective include/zone records and coherent four-VIP ownership together.
Unexpected drift, conflicting/duplicate records, missing required evidence or
unhealthy services hold deployment. Expected absent Uptime answers are recorded;
they do not authorize insertion.

Per node scope: one IPv4 SSH session as pi with strict existing Ed25519 keys;
current hostname/boot before/after; Unbound/Pi-hole/Keepalived/Caddy identity;
addresses and DNS .55/::55 plus Proxy .56/::56 ownership; protected local-zone
bytes/metadata and bounded effective .conf include graph; current native config
validation; Unbound version/control help; executable and Pi-hole launcher/version
metadata; sanitized service launch/reload definitions; journal cursor without
entries; existing bounded sync identity/path hints. Full local-zone bytes stay
private; other configuration contents are not exported wholesale. No credentials,
private keys, environment files, setupVars or arbitrary home directories.

Each node issues 60 fixed single-attempt UDP queries: NTP A/AAAA/PTR controls,
dashboard and host A/AAAA plus host PTRs through loopback Unbound, node addresses
and DNS VIPs; plus four public A controls through loopbacks and DNS VIPs. No DNS
queries target proxy-only VIPs. Per-command bounds are eight seconds/64 KiB per
stream, DNS three seconds; remote capture 240 seconds, controller 270 seconds
and 16 MiB per stream. Configuration limits remain 64 files/4 MiB aggregate/
1 MiB each; three executable reads allow 16 MiB each and export only metadata.

Excluded: target staging or file writes, package actions, reload/restart, sync
runs or suspension, failover, reboot, notifications, backend/Caddy mutation,
record publication, deployment retry and Git publication. Ordinary SSH/sudo
audit records and DNS cache activity may occur. Read-only failure needs no
rollback; retain partial evidence and stop. Inspection findings cannot silently
change deployment expectations. A new deployment bundle remains separate.

This fresh scope requires exact approval under the
[DNS owner readiness procedure](../../../homelab-dns/Unbound/docs/host-record-deployment.md#deployment-readiness).
Both previous DNS approvals are consumed and do not authorize these captures.

### November 12: approved paired DNS readiness completed — W-121

Aaron approved the two exact archives and secondary-first scope above. Both
archives/member sets and expiry were checked before execution. Secondary session
77362 and primary session 72386 each exited 0; both exclusive captures completed
and their approvals are consumed. No retry, staging, zone write, service restart,
failover, recovery or publication occurred. Both sessions are retired.

Observed and locally reconciled:

- Both current boot IDs differ from the inherited October values and are stable
  before/after their respective captures. Current values remain in private evidence.
  This confirms the stale boot prerequisite on both nodes; change timing/cause and
  the original diagnostic-poor attempt's cause remain unknown.
- All five effective configuration files and every previously bound metadata field
  match. Both local-zone files are byte-identical to the consumed baseline. The
  Pi-hole launcher hash is unchanged. Expanded current configuration matches the
  retained expanded candidate after locally replacing its candidate zone with the
  original zone; the different candidate/current hash is expected, not drift.
- Native current/expanded configuration checks pass on both nodes. Unbound,
  Pi-hole FTL, Keepalived and Caddy remain active with stable captured identities.
  Both cursor reads succeed. All four coupled VIPs are owned by .53; .54 owns none,
  unchanged within each capture. These are sequential samples, not continuous HA proof.
- Each node completed 60 DNS queries: preserved NTP A/AAAA/PTR answers are exact;
  dashboard/host A/AAAA and both host PTRs return expected NXDOMAIN through every
  planned endpoint. All four public controls per node return successful A answers.
  No conflicting Uptime record appears in the selected effective record projection.

The protected read of `/etc/pihole/versions` was unavailable, and the alternate
`/opt/pihole/pihole` path was absent. These are retained limitations, not missing
service assumptions: the actual `/usr/local/bin/pihole` hash matches the accepted
owner input and current local Git reports v5.18.3. Sync projection is incomplete;
retain the existing owner contract that local-zone synchronization is not implemented
and prior restart/control qualification. Do not claim a new comprehensive writer
or restart-chain qualification from this capture. A successor must reconcile any
required scope beyond these observations locally before review.

Private evidence: both v2 readiness directories contain authorization, exclusive
execution, bounded streams, transport/result and terminal summaries. The combined
`dns-paired-readiness-result-3_ajijte/reconciliation.json` under the Uptime Kuma
evidence store binds their hashes and comparison results. W-121 is resolved for
read-only readiness and reconciliation. Existing Caddy/application acceptance
remains retained; DNS deployment and ordinary-name dashboard acceptance are still
pending. No new deployment candidate or live authority is implied.

### November 12: boot continuity made a permanent harness rule

Aaron confirmed that normal patching/reboots must not be blocked by historical
boot IDs and asked to make the distinction permanent. The workspace AGENTS.md
now governs durable host identity, fresh operation admission and runtime continuity.
The DNS AGENTS.md adds the owner-specific gate/dispatch and regression-test
requirements. PLAN.md records the accepted contract change; W-122 tracks its
implementation before another candidate. No extra skill, hook, tracker or runtime
framework was introduced. These instructions guide future agent work; executable
enforcement is still pending and must not be claimed from documentation alone.

No live contact, source execution change, publication or consumed-bundle edit
occurred. The workspace instruction file is local workspace policy; the DNS owner
instructions and project records are repository changes awaiting publication.

### November 12: operation-scoped DNS boot continuity qualified — W-122

The existing owner node/verifier/dispatcher now implement the approved policy.
New source entrypoints require `boot_policy: operation-admission-v1`. The first
paired gate ignores historical node boot values, authenticates the intended hosts,
and observes current IDs while preserving configuration, binary, DNS and HA checks.
It retains those IDs across its convergence samples. Incomplete initial discovery
stops; it cannot retry into a different admitted boot.

The accepted private `gate-before.json` binds both IDs to the operation ID and
approved input digest. Later gates and dispatch load that receipt and reject
missing, unsafe, foreign or incomplete admission evidence. Apply still requires
paired acceptance no older than 120 seconds, now with matching operation/boot
bindings. Apply/rollback receipts also record the admitted IDs. Resume does not
reset admission. Node-side continuity checks run at inspection completion and
around mutation/recovery; boot mismatch stops convergence and blocks automatic
restoration on a different boot. Existing recovery rules otherwise remain.

Qualification in the existing suite passed 42 transaction tests and 27 readiness
tests. Added cases cover fresh node admission without writes, changed-boot rejection
before apply/rollback, persisted gate bindings and resumed phases, one-use initial
gate, incomplete admission, immediate boot-change stop, strict host/configuration
rejection, and missing/foreign admission records. Existing transaction, native
streamed-Python rejection, recovery and exact DNS tests still pass. No new platform
fixture, simulated failover, container or live contact was used.

Private `dns-boot-continuity-qualification-482zwv4b/result.json` under the Uptime
Kuma evidence store binds final source hashes and logs. Syntax checks, working-tree
secret scan and whitespace checks passed. Both consumed deployment archives and
both completed readiness archives/recorded receipt hashes were verified unchanged.
`vexp verify_done` remained unavailable from its non-Git parent workspace session;
owner checks supplied qualification. Session 40171 exited 0 and is retired.

W-122 is resolved for source and local qualification. These changes are uncommitted;
no deployment candidate was sealed and no live acceptance is claimed. The next
candidate must use the new policy and fresh operation identity; consumed inputs
remain immutable. No retry, reboot, publication or other live work is authorized.

### November 12: DNS admission-policy successor prepared — W-123

Private directory: `/home/aaron/code/.local-evidence/homelab-dns/current/uptime-kuma-dns-admission-20261112-myuc3p0t`.
Archive SHA-256: `d89d3b0c252dc86173ef98603539189ca96dc46dff55c333e2352e004cbb8e2e`.
Internal input-index SHA-256: `16b6740ceaeef6cd8a15ee3e040281486dd7f9e8f2cea1186c5fc1759337b12f`.

The candidate freezes the qualified W-122 node/verifier/dispatcher and unchanged
owner runner. It declares `boot_policy: operation-admission-v1`; node boot fields
are null at preparation. November 12 observed IDs remain provenance only. Fresh
live admission captures current IDs, and subsequent phases use the accepted initial
gate's operation/digest-bound IDs. Neither a preparation-time reboot nor an old
inventory value is a permanent admission requirement. Unexpected reboot after
admission stops progression and requires reconciliation, including recovery safety.

Both completed readiness results are bound by hash. Their exact zone bytes,
configuration/include set and previously bound metadata, and Pi-hole launcher
identity match the predecessor inputs. The baseline, six-record candidate,
expanded candidate bytes and SSH host-key file are unchanged. Operation identity,
backup paths, preparation time, boot policy and readiness/qualification provenance
are new; expiry and DNS/HA/restart requirements are unchanged. No observed file
identity was silently refreshed or replaced. Readiness projection limitations
remain as recorded under W-121; this is not a new comprehensive writer proof.

Local qualification reused the exact W-122 source hashes and retained passing
42 transaction/27 readiness tests. The frozen runner's closed archive/member/index
check passed. The frozen verifier accepted the input policy/manifest locally and
rejected absent admission evidence; an incorrect archive digest was rejected.
The reviewed operation delta was checked against the allowed field list; preserved
input bytes and all four consumed archive/recorded evidence hashes verify.
The exact new directory passed secret scanning. No phase invocation or gate receipt
exists. `preparation.json`, local check logs and `seal.json` are beside the archive.
No new platform fixture, target probe, commit or push occurred.

#### Exact DNS admission-policy bundle, commands and scope — awaiting approval

Approve this archive for **one attempt**, individually gated in this order:

```bash
dns_bundle=/home/aaron/code/.local-evidence/homelab-dns/current/uptime-kuma-dns-admission-20261112-myuc3p0t
reviewed_dns_sha256=d89d3b0c252dc86173ef98603539189ca96dc46dff55c333e2352e004cbb8e2e
python3 -I -B "$dns_bundle/runner.py" step --directory "$dns_bundle" --sha256 "$reviewed_dns_sha256" --phase before
python3 -I -B "$dns_bundle/runner.py" step --directory "$dns_bundle" --sha256 "$reviewed_dns_sha256" --phase apply-secondary
python3 -I -B "$dns_bundle/runner.py" step --directory "$dns_bundle" --sha256 "$reviewed_dns_sha256" --phase after-secondary
python3 -I -B "$dns_bundle/runner.py" step --directory "$dns_bundle" --sha256 "$reviewed_dns_sha256" --phase apply-primary
python3 -I -B "$dns_bundle/runner.py" step --directory "$dns_bundle" --sha256 "$reviewed_dns_sha256" --phase after-all
```

This is not an unconditional paste. Inspect each terminal result and stop on
failure. No receipt deletion or replay. Initial paired acceptance must show .53
owning all four coupled VIPs; update pi@10.1.0.54 before pi@10.1.0.53. Each apply
requires paired acceptance no older than 120 seconds, bound to this operation
and the same admitted boot IDs. Missing/unsafe admission evidence or a boot
change stops before further mutation; resuming cannot reset admission.

Expiry remains **November 14, 2026 at 11:02:35 a.m. CST**
(`2026-11-14T17:02:35+00:00`); every invocation, including recovery, requires more
than five minutes remaining. Effective cutoff is **10:57:35 a.m. CST**. Leave
enough time for the complete operation and scoped recovery.

Change only the existing six-record addition in the local-zone file on each node:
dashboard A/AAAA to Proxy VIP .56/::56, host A/AAAA to .75/::75, and both host PTRs.
Preserve unrelated records and Proxy PTRs. Require exact host/configuration/binary
checks and native validation, atomic zone replacement, full Unbound restart,
healthy Unbound, then full Pi-hole DNS restart. Require exact paired/node/VIP DNS
answers over both families, healthy Caddy, preserved public/local DNS and coherent
ownership of DNS .55/::55 plus Proxy .56/::56. Normal cluster-driven movement is
allowed; no forced failover. Each node's backup path is
`/var/backups/uptime-kuma-dns-admission-20261112-myuc3p0t`.

On failure inspect mutation and automatic-recovery receipts first. Before-gate
failure needs no rollback. Restore only changed nodes requiring recovery from
their own exact backups, under unchanged admitted boots. If both changed, use
`rollback-primary`, `after-rollback-primary`, `rollback-secondary`, then
`after-rollback-all`; secondary only uses `rollback-secondary` then
`after-rollback-all`. Invoke the same runner/digest with the applicable phase.
Recovery includes both full restarts and paired acceptance. Do not repeat verified
automatic restoration. Lost workers, unknown write state, changed destination,
missing backup, changed boot or unproved recovery require manual reconciliation;
no automatic re-admission or replay is authorized.

After accepted `after-all`, run each command once, expecting HTTP 200 with normal
TLS validation:

```bash
curl -4 --noproxy '*' --fail --silent --show-error --connect-timeout 5 --max-time 15 --output /dev/null --write-out '%{http_code}\n' https://uptime.local.theama.co/dashboard
curl -6 --noproxy '*' --fail --silent --show-error --connect-timeout 5 --max-time 15 --output /dev/null --write-out '%{http_code}\n' https://uptime.local.theama.co/dashboard
```

A workstation resolution failure is separate from accepted owner DNS state;
do not roll back accepted DNS solely for that failure. Preserve accepted private
login and passive application evidence; no new login check is included.

Excluded: Caddy configuration/restart, backend mutation, packages, accounts,
monitors/alerts, notifications, route/radio work, forced failover, reboot,
unrelated DNS edits and Git publication. W-020/W-076 and project closeout remain
separate. Prior deployment and inspection approvals are consumed. This exact
successor requires fresh authorization under the
[DNS owner procedure](../../../homelab-dns/Unbound/docs/host-record-deployment.md#deployment-readiness).
Its frozen `review.md` carries the same scope and recovery boundary.

### DNS admission-policy deployment accepted — November 12, 2026 (W-124)

Aaron approved the exact bundle and scope at line 5449 for one attempt. Archive
`d89d3b0c252dc86173ef98603539189ca96dc46dff55c333e2352e004cbb8e2e`
passed sealed-input/expiry verification. All five ordered phases exited 0:
`before`, `apply-secondary`, `after-secondary`, `apply-primary`, `after-all`.

Fresh admission recorded current boot IDs; every later phase retained them.
The secondary and then primary atomically installed the six-record candidate,
validated configuration and fully restarted Unbound followed by Pi-hole DNS.
Both mutation receipts report candidate SHA-256
`2df1be44a9ea39a35df1e75db16d72a4138b4ab3048fdc7bcf58bd7ff1a959dc`.
Paired gates accepted exact node/VIP answers over both families, preserved
local/public DNS controls and service health, including Caddy. Every retained
ownership sample has all four linked VIPs on .53. These samples do not claim
uninterrupted availability during service restarts.

The two approved ordinary-name `/dashboard` requests each exited 0 and returned
HTTP 200 with normal TLS validation, IPv4 and IPv6. Existing accepted private
login/WebSocket and passive application receipts remain the application evidence;
no new login occurred. AC-004 is satisfied by those receipts and this DNS/HTTPS
acceptance. W-020/W-076 and documentation reconciliation remain before closeout.

Private evidence: `.local-evidence/homelab-dns/current/uptime-kuma-dns-admission-20261112-myuc3p0t/`
under the workspace, including `authorization.json`, all invocation/controller
and node receipts, `gate-before.json`, `gate-secondary.json`, `gate-all.json`,
`dashboard-https.json` and the hash-indexed `terminal-summary.json`.
Both node backups remain at `/var/backups/uptime-kuma-dns-admission-20261112-myuc3p0t`.
No rollback, forced failover, reboot or Caddy mutation ran. Repository zone source
now contains the same directives as the accepted candidate, preserving its prior
ordering and unrelated content; its bytes therefore differ from installed bytes.

Sessions 60203, 18605, 2752, 18801 and 4956 all exited 0 and are retired; the two
HTTPS checks completed synchronously. Approval is consumed. Both earlier failed
DNS bundles and all readiness receipts remain unchanged. No further live work,
backup cleanup, replay or Git publication is authorized.

Local reconciliation checks passed: DNS transaction/readiness contracts,
Markdown checks in both repositories and whitespace checks. The repository
zone's directives match the accepted installed candidate; unrelated source bytes
are preserved. Local check sessions 12006 and 27264 exited 0 and are retired.
These local source/document changes remain uncommitted and unpublished.

### Local closeout reconciliation — November 12, 2026 (W-125)

Re-read retained runtime/foundation/startup/restore receipts and compared seven
files with their original evidence indexes; all hashes matched. The private
reconciliation index is `closeout-reconciliation-t490dweo/evidence-index.json`
under `.local-evidence/uptime-kuma/`. No live command or new observation ran.

W-020 snapshots establish required networking after startup/reboot/promotion,
not a timed RA-renewal series. W-076 evidence is stronger than the earlier ledger
summary: `runtime-remaining-before-reboot.json` and
`runtime-bootstrap-after-reboot.json` in `remaining-staged-20261110-5i0l9c9t/execution/`,
plus `runtime-backend-promoted.json` in `backend-completion-20261111-nin6u10h/execution/`,
all report Bluetooth and WLAN soft-blocked. Daemon presence alone is not a radio
failure. Keep both services and NetworkManager unchanged; their target-specific
ownership/dependency disposition remains unverified. Neither finding is waived.

W-004/W-008/W-026 were stale pending rows and are reconciled with completed work.
Architecture now describes accepted Podman resources, vendor watchdog coverage,
Caddy/DNS, loopback transport and ordinary accepted startup. Operations separates
normal access from new installation and contained-state recovery; it no longer
instructs the accepted host to repeat account setup. RESULT.md records all twelve
criteria, accepted service scope and incomplete AC-008/AC-010. W-012 remains in
progress and W-096 remains deferred at Aaron's direction. No new candidate is
sealed and no approval is requested for an undefined operation.

Focused pre-commit documentation checks passed; session 95357 exited 0 and is
retired. Relative file links, all twelve acceptance IDs and changed ledger-row
structure were checked; whitespace checks passed. An initial whole-ledger cell
counter rejected the existing escaped pipe in W-069; the corrected scoped check
passed without changing that historical row. No code or executable input changed.
The vexp completion helper remains unavailable for this parent-workspace session;
focused repository checks provide verification. Changes remain uncommitted.

### Proposed W-020/W-076 acceptance decision — November 12, 2026 (W-127)

Local owner review covered the network-owned
[ULA procedure](../../../homelab-network/host-network/uptime-kuma/ansible/permanent-ula.yaml),
[fleet foundation ownership](../../../homelab-server-configs/foundation/README.md),
[selected host profile](../../../homelab-server-configs/inventory/prod/hosts/j2-svpi3bmf.yaml),
and the application's accepted-prerequisite/runtime checks. The latter require
both radio types soft-blocked and automatic networking, persistent ULA, global
IPv6 and default routes. They do not require radio-daemon removal. The network
procedure preserves existing automatic methods/routes through its checkpoint;
it does not define a timed RA-renewal proof. No new executable rule is proposed.

**Recommended decision, awaiting Aaron's explicit agreement:**

1. **W-076: resolve with no service change.** Accept the retained before/after-reboot
   and promotion softblocks as the initial deployment's radio-disabled outcome.
   Keep Bluetooth, wpa_supplicant, NetworkManager and existing block policy intact.
   Dependency analysis is a prerequisite for a future removal/disable proposal,
   not evidence that these unchanged daemons must be removed now. Do not claim
   hardware disablement, complete dependency discovery or memory savings. Host/
   network ownership remains unchanged; any radio/service change needs its own
   review. Unexpected unblocking reopens this item before dependent maintenance.
2. **W-020: explicitly defer the unmeasured timed-renewal check.** Accept the
   observed startup/reboot/promotion addresses and routes for this initial
   service deployment, retaining the fact that continuous RA-renewal behavior
   was not measured. This accepts a residual risk of an unobserved later
   renewal/routing failure; dashboard ULA success alone does not remove it.
   `homelab-network` owns follow-up in this existing W-020 record, due before
   the next host networking or container-runtime migration, or earlier if IPv6
   route/address loss is reported. That work must define a bounded read-only
   observation using actual advertised lifetimes and preserve host identity,
   automatic methods, required addresses and default routes across renewal.
   No observation, forced renewal, reapply, sysctl edit or reboot is authorized
   by this decision. Successful future evidence can resolve the deferred item.
3. **Closeout effect:** after agreement, amend the plan to record this acceptance
   boundary, mark W-076 Resolved and W-020 Deferred with the owner/trigger above,
   and reconcile AC-008/AC-010, W-011/W-012 and RESULT.md. Close the initial service
   deployment using its existing evidence and explicit limitation; do not call
   the timed-renewal test passed. W-096 stays Deferred. Monitors/alerts, future
   workload qualification, actual notification delivery and Git publication
   remain separate. No further live work follows automatically.

Alternative: retain both findings as closeout blockers and prepare a separately
reviewed network/host observation. No such executable operation is prepared or
approved here. The recommendation avoids service changes unsupported by the
observed radio state and leaves the remaining measurement obligation visible.

Agreement is needed because this changes the remaining acceptance boundary,
not because repository editing needs permission. The change-control rule states:
“A decision that changes acceptance or authorized scope requires the user's
agreement.” The existing plan likewise requires evidence or explicit deferral.

W-126 reconciles stale inventory metadata with accepted foundation/runtime and
DNS/dashboard receipts. It does not assert fresh live state, change selected
components, or remove the project's partial-closeout limitation. No secret/raw
evidence was copied into inventory; the shared result is its evidence reference.

Local review checks passed: both repositories' applicable pre-commit hooks,
relative file links, metadata-only comparison and whitespace checks. The
monitoring check session 34488 exited 0 and is retired; the inventory checks
completed synchronously. No code, deployment inputs or target state changed.
All work remains uncommitted and unpublished. W-127 awaits the explicit decision
above; W-020/W-076 are not marked resolved/deferred by preparation alone.

### Initial-deployment closeout approved — November 12, 2026

Aaron approved the exact W-127 dispositions in the response annotation. W-076
is resolved with existing radio services retained; W-020 is explicitly deferred
with its network owner, maintenance trigger and residual risk preserved above.
W-096 remains deferred at the prior instruction. AC-008/AC-010 now pass under the
approved initial-deployment acceptance boundary; no timed RA test is claimed.
All remaining initial-deployment tasks have final dispositions. RESULT.md is
Accepted with those explicit follow-ups. No live operation or publication follows.

Aaron also reported failed login at `https://uptime.local.theama.co:10000`.
That name maps to the Proxy VIP, not this Pi. The accepted Webmin profile binds
only IPv4/IPv6 loopback on port 10000, with TLS off inside the SSH tunnel and
`ama` selected for existing Unix/sudo authentication. The operating guide now
explicitly separates these endpoints and credentials. Use its workstation tunnel
and `http://127.0.0.1:11000/`; no password reset, new login attempt, endpoint
inspection or claim about which remote Webmin answered was made. Prior accepted
Webmin login evidence remains unchanged; the newly reported wrong-endpoint
failure does not establish a failure on the Pi.

### Fleet browser and DNS procedures — November 12, 2026

Aaron approved `webmin-j2-svpi3bmf.local.theama.co` and required normal browser
access for fleet Webmin. The shared Webmin operations guide documents HTTPS as
normal access and SSH tunneling as optional recovery, with workstation steps and
credential/endpoint distinctions. The onboarding procedure reuses primary-first
Caddy publication and its existing replication/secondary acceptance. The URL is
approved but not deployed; W-128 remains in progress. A local read-only collector
and tests are prepared, but no inspection bundle is sealed or authorized.

W-129 promotes the existing DNS procedure to the fleet entry point. Additions,
edits and deletions use exact before/after/intermediate/recovery query matrices;
other DNS changes route to their owner runbook. Current record-checker support
is A/AAAA/PTR, not every DNS type. Application-specific readiness modes require
coverage review for new consumers. Historical bundles and approvals remain
unchanged. No target contact, new attempt or publication occurred.

Local validation passed: applicable pre-commit hooks for DNS, server and monitoring
procedure/document changes (sessions 25236, 9816 and 87050, all exit 0 and retired),
and relative file-link checks for the shared procedures and plan. The vexp
completion helper reported unavailable from the parent workspace, so no graph
verification is claimed. No execution session remains active. Changes remain
local and uncommitted; Webmin implementation and live acceptance remain pending.

### Shared Webmin profile qualification — November 12, 2026

The owner renderer `Webmin/scripts/render-proxy-profile.py` produces two policies
for the existing atomic configuration helper. Explicit backend/source addresses,
selected current settings and approved browser hostname are reviewed inputs.
Authentication, SSL/key settings and unrelated configuration remain untouched;
referers are extended rather than replaced. Conflicting redirects, access policy,
subpaths and disabled referer/session checks stop for review. First-host source
addresses and transport are not inferred or sealed by the fictional example.

Qualification: four profile tests, seven readiness tests and seven existing atomic
configuration tests passed. Final native session 18819 exited 0; pre-commit session
2863 exited 0. Earlier native sessions 72651/83175 exited 1 because the fixture
expected a redirect from an internally served login path; the corrected explicit
redirect fixture passed in session 49742 and again against final inputs in 18819.
Final ledger pre-commit session 58250 also exited 0 and is retired.
All sessions are retired. Actual native miniserv 2.670 in local image 126c2a383378
ran with networking disabled, read-only root and disposable temporary files. Its
miniserv source hashes match the retained package (SHA-256
`67ddbbeb415daa44643b91c2b4c7ce65c29f3170bd88cf37c6b2b516542c9839`).
It passed dual-stack canonical HTTPS/443 redirects, selected listener access and
403 rejection of an unlisted source. Containers used `--rm`; processes were
terminated in the fixture's cleanup. No live target was contacted.

Private evidence: `/home/aaron/code/.local-evidence/uptime-kuma/webmin-profile-qualification-e43eyzx8/`
contains exact source hashes, native result and pre-commit output. YAML, relative
file links and whitespace checks pass. This is backend-policy qualification only:
full Webmin login, cookies/CSRF, Caddy TLS/WebSockets, real ingress and Pi resource
acceptance remain pending. Operations now warns that canonical redirects may
leave a localhost tunnel; independent browser recovery is not claimed. SSH
command-line recovery and owner-reviewed saved-profile restoration remain available.

### Exact Webmin readiness inspection for review — W-131

**Prepared, not authorized.** One read-only capture on `ama@10.1.3.75`, expected
hostname `j2-svpi3bmf.local.theama.co`, interface `eth0`. No other host is contacted.
The frozen collector runs through SSH standard input with `sudo -n python3`;
there is no target staging file. Strict retained SSH host-key validation is
required. Fresh boot identity and selected configuration identities must remain
stable during capture. Existing consumed operations remain unchanged.

Bundle: `/home/aaron/code/.local-evidence/uptime-kuma/webmin-readiness-review-zmzk_x1o/`

`INPUTS.SHA256SUMS` SHA-256:
`799c8cece351a30a1ff78a0b134d2d91508e81ce532f4c048491464a89e4d766`

Exact command, after verifying that manifest digest and the approved scope:

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/webmin-readiness-review-zmzk_x1o/run.sh
```

The command verifies all four frozen inputs and consumes one exclusive local
attempt directory before SSH. Total controller timeout is 90 seconds plus a
five-second termination grace; each remote command has an eight-second timeout.
Captured command output is checked against 64 KiB per stream, configuration reads
against 256 KiB per file; launcher file-size limits bound retained output. Receipts,
transport diagnostics and exit status remain in the owner-private local store.
Do not automatically retry a partial or failed capture.

Reads: selected non-secret settings and file identities from miniserv, Webmin and
system-status configuration; Webmin package version; native service state and
resource properties; TCP port 10000 listeners; eth0 addresses and IPv4/IPv6 routes;
and the nftables ruleset. It does not read password/user databases, session data or
private keys. Stderr is not copied into collector JSON. No HTTP/login probe, write,
package change, firewall edit, service action, reboot, Caddy/DNS operation or new
network test is included. No recovery is needed for these reads.

After capture, review effective settings, listeners, routes and ingress policy to
bind the first host's candidate; this receipt alone does not establish actual proxy
source addresses or accept a deployed route. Further owner qualification and exact
live authority remain separate. Repository policy requires scoped live inspection
authority; see `homelab-server-configs/AGENTS.md`, Definition and authorization.

### W-131 approved read-only attempt — November 12, 2026

Aaron approved the exact bundle, command and scope referenced at line 5747 for
one capture on `10.1.3.75`. Before launch, the manifest digest matched
`799c8cece351a30a1ff78a0b134d2d91508e81ce532f4c048491464a89e4d766`,
all four frozen files matched and no attempt directory existed. The exact reviewed
command ran once with the required network permission; it exited 1 synchronously.
No execution session was created or remains active. This approval is consumed.

The private `attempt/receipt.json` is 69 bytes and reports `complete: false`,
`error: hostname_mismatch`, `mutation: false`. Transport stderr is empty. The
strict SSH host-key check completed and the collector reached its first hostname
comparison. It stopped before configuration reads, boot capture, root-read checks
or diagnostic subprocesses. The expected hostname was
`j2-svpi3bmf.local.theama.co`; the observed value is unavailable because the
collector omitted it. Neither a renamed host nor short-name/FQDN equivalence is
established. No readiness or backend acceptance is claimed.

The receipt, empty transport stderr and exit status remain in the sealed bundle's
private `attempt/` directory with an evidence-hash index. No original input was
changed. No retry, additional live query, write, restart or recovery ran. W-132
tracks the missing diagnostic and prerequisite reconciliation; W-131 is blocked
and W-128 remains open. Review locally before proposing another exact scope.

### W-132 local hostname reconciliation and reporting — November 12, 2026

The earlier readiness scope incorrectly used the DNS FQDN as the native hostname
expectation. The accepted backend operation's frozen
`operations/remaining-deployment.yaml` selects `target_hostname: j2-svpi3bmf`.
Its frozen `ansible/accepted-prerequisites.yaml` reads `/usr/bin/hostname` and
requires exact equality to that value. Both files match their retained
`candidate/bundle/INPUTS.sha256` entries. The retained `execution/ansible.log`
records the hostname read followed by the accepted boot/radio assertion passing.
These files reside under the previously accepted private
`backend-completion-20261111-nin6u10h` evidence directory.

This reconciles the next candidate's native identity expectation to
`j2-svpi3bmf`, separately from DNS `j2-svpi3bmf.local.theama.co` and the approved
Webmin browser hostname. It does not reconstruct the failed W-131 observation,
prove today's hostname or authorize accepting arbitrary short-name aliases.
Strict SSH key and exact native hostname checks remain required; no DNS lookup,
normalization or automatic expectation update is introduced.

The existing collector now reads the native hostname once and retains an
allowlisted failure object containing the source, expected value and observed
value. Only ASCII hostname characters up to 253 characters are reported;
malformed/overlong observed strings are redacted, invalid expected values are
not echoed and unknown exception text remains suppressed. Mismatch still exits
1 before config reads or diagnostic subprocesses.

Qualification: all 11 readiness tests pass, including the actual local CLI
mismatch path, short-name/FQDN rejection, no downstream reads/commands, bounded
JSON, control/overlong redaction, invalid expected-input suppression and existing
configuration-drift/privacy cases. Focused pre-commit passed synchronously.
No target contact or native service action occurred. The consumed inspection
manifest, script and receipt remain unchanged and retain their prior hashes.
No successor was prepared or sealed; W-131 remains blocked awaiting a separately
reviewed capture, while W-132's local correction and prerequisite reconciliation
are complete. Full Webmin browser acceptance remains pending under W-128.

### Exact Webmin readiness successor for review — November 12, 2026

**Prepared and locally qualified; not authorized.** This is one new read-only
capture on `ama@10.1.3.75`, expected native hostname `j2-svpi3bmf`, interface
`eth0`. It uses the corrected bounded expected/observed reporting and preserves
exact hostname matching and strict SSH host-key verification. No other host is
included. The approved browser name remains
`webmin-j2-svpi3bmf.local.theama.co`; it is not the native hostname expectation.

Bundle: `/home/aaron/code/.local-evidence/uptime-kuma/webmin-readiness-review-rl27up6b/`

`INPUTS.SHA256SUMS` SHA-256:
`01918d621cc5cebffedaf7c3c4a48f4e033b2e11fa222597b7c33ed4ed8f8037`

Frozen collector SHA-256:
`5351e3b929f17973ffbabd253d9b8151b5ea840af6318c1502e76e1126bd3c61`

Exact command after approval and verification of the manifest digest:

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/webmin-readiness-review-rl27up6b/run.sh
```

The four bound inputs are the collector, retained known-hosts file, scope JSON
and launcher. The launcher verifies them and claims one exclusive local attempt
directory before SSH. Existing credentials are used without prompting or collection.
The remote command streams the collector to `sudo -n /usr/bin/python3 -I -B -`
with the explicit native hostname and interface; no remote staging file is created.

Authorized scope, if approved: selected non-secret settings and identities from
`/etc/webmin/miniserv.conf`, `/etc/webmin/config` and
`/etc/webmin/system-status/config`; installed Webmin version; service state and
resource properties; TCP port 10000 listeners; eth0 addresses, IPv4/IPv6 routing
and nftables rules. Capture current boot identity and require continuity during
this operation; do not compare a historical boot ID. Configurations must remain
unchanged during collection. This is observation, not readiness acceptance by
itself or evidence of actual proxy source addresses.

Limits remain 90 seconds plus a five-second controller termination grace,
eight seconds per remote command, 256 KiB per configuration and a 64 KiB
post-capture check per command stream. The launcher's file-size limit bounds
retained output. Failure stops; do not automatically retry. A hostname mismatch
reports bounded expected/observed values and exits before configuration reads or
diagnostic commands. Malformed observed names and arbitrary exception text remain
redacted. Receipts, transport diagnostics and exit status stay in the owner-private
bundle's `attempt/` directory.

Excluded: password/user databases, sessions, private keys, HTTP/login probes,
remote staging or writes, package/configuration/firewall changes, service actions,
restarts/reloads/reboots, Caddy/DNS operations and other targets. No recovery is
needed for these reads. Any later host/profile binding, proxy-source inspection,
backend deployment, Caddy/DNS work or publication requires its own applicable scope.

Qualification passed: 11 collector tests including real local CLI mismatch,
launcher `bash -n` and ShellCheck, strict manifest verification and local validation
that the retained SSH pin covers the exact target. Frozen collector bytes match
the tested owner source. No attempt directory exists. The consumed predecessor's
input manifest and every retained receipt hash were reverified unchanged. No
live target contact occurred and no local execution session remains active.

Repository policy requires explicit scoped live inspection authority under
`homelab-server-configs/AGENTS.md`, Definition and authorization. Approving this
successor grants one read-only capture only; the prior approval remains consumed.

### W-131 successor capture accepted — November 12, 2026

Aaron approved the exact bundle, command and scope at line 5851 for one read-only
capture. Before execution, all four input hashes matched manifest SHA-256
`01918d621cc5cebffedaf7c3c4a48f4e033b2e11fa222597b7c33ed4ed8f8037`
and the attempt directory was absent. The exact command ran once and exited 0
synchronously; no execution session was created. The approval is consumed.

The private receipt reports `complete: true`, native hostname `j2-svpi3bmf`,
interface `eth0`, and `mutation: false`. Strict SSH host-key validation and native
hostname checks passed; fresh boot identity and all three configuration identities
remained stable across collection. All seven commands completed with exit 0 and
zero stderr bytes; SSH transport stderr is empty. No login/HTTP probe was run.

Observed baseline:

- Webmin 2.670, active/running, NRestarts=0. Native service properties retain
  MemoryHigh 128 MiB, MemoryMax 192 MiB and MemorySwapMax 0. These are configured
  limits, not measured workload/resource acceptance.
- TCP 10000 listens only on 127.0.0.1 and ::1. The allowlist contains those two
  addresses; ssl=0, session=1, localauth empty, allowusers=ama, sudo=1. Existing
  foundation/startup-authority drop-ins remain listed. collect_pkgs=0 persists.
- Webmin configuration has referers_none=1, no explicit referers and empty
  webprefix. W-133 tracks the required explicit referrer-policy transition;
  the current renderer rejects this baseline, as designed.
- eth0 retains 10.1.3.75/22 and fd36:5aa8:6971:1::75/64, with IPv4 and IPv6 default
  routes. Additional observed addresses stay in private evidence; this snapshot
  does not qualify timed RA renewal or actual Caddy-to-Webmin source selection.
- Captured nftables contains the existing Kuma and Netavark tables. No rule
  explicitly naming port 10000 was found. No claim is made about upstream network
  controls; restricted ingress and actual proxy source identities remain required
  before opening Webmin network listeners. Existing Kuma rules are preserved.

Receipt, transport stderr and exit status remain under the new bundle's
`attempt/` directory with `evidence-hashes.json`. Frozen inputs still match after
execution. The consumed predecessor remains unchanged. No remote file, setting,
service, firewall, DNS or Caddy change occurred; no recovery or retry was needed.
W-131 closes the scoped collection only. Webmin browser deployment/acceptance
remains pending under W-128; W-133 must be reconciled locally before a candidate.

### W-133 corrected semantics and first-host proposal — November 12, 2026

The prior interpretation of `referers_none=1` was wrong. Unmodified Webmin 2.670
`web-lib-funcs.pl` distinguishes the two controls: truthy `referer` bypasses checks
globally; `referers_none=1` rejects missing referrers on protected actions, subject
to native login/index/module exceptions. The earlier capture did not project
`referer`, so its live value is unknown. Historical notes above retain the mistaken
assessment; this correction supersedes it. No weakening of the observed
missing-referrer policy is proposed or necessary.

The shared renderer now preserves `referers_none`, deliberately sets `referer=0`
and adds only the approved browser hostname to existing trusted names. It retains
backend SSL/authentication keys and unrelated settings. The collector now includes
both referrer controls for future reviewed captures; neither consumed collector
nor receipt was modified. The full candidate must bind the deliberate global-check
write to the exact before-file identity and verify effective policy after apply.

Local native qualification calls unmodified `init_config` with isolated CGI inputs
in the existing network-none container. Seven cases passed: a known global-bypass
positive control; the approved HTTPS name across frontend/backend port differences;
a preserved existing trusted name; rejection of foreign and suffix-spoofed names;
rejection of missing referrers on a protected action; and the native login exemption.
This tests real native policy decisions, not authentication or full HTTP/CSRF flow.
The library hash matches the retained Webmin 2.670 package source:
`c39aa5219939d29804bcfbfdee2a766705b15428427ed0ecf7527aed9ea42ba3`.

First-host review input:
`homelab-server-configs/Webmin/configs/hosts/j2-svpi3bmf-proxy.json`.
It binds the approved browser hostname, observed port/loopback/authentication/TLS
settings, 10.1.3.75 and fd36:5aa8:6971:1::75. Proposed proxy sources are copied from
the captured existing Kuma guard: IPv4 .53/.54 and IPv6 ::53/::54/::56. This is a
retained policy basis, not proof of current Webmin connection source selection.
The proposal preserves backend HTTP with source-restricted LAN access and frontend
HTTPS. The backend leg would be plaintext; this trust boundary belongs in the live
operation review and must not be mistaken for end-to-end TLS acceptance.

`--format ingress` on the shared renderer emits only the Webmin-owned nftables
table, using the existing fleet pre-routing guard pattern. It permits loopback
and reviewed source/destination pairs on port 10000 and drops other traffic to
that local port. Native nftables check, apply/reapply and preservation of an
unrelated sentinel table passed in a disposable network-none container with
NET_ADMIN limited to its namespace. No host network namespace or target was used.
This does not qualify packet paths, guard persistence, boot ordering or Pi resources.

Private qualification evidence:
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-referrer-qualification-ehxgfx5b/`.
It retains native logs/status, source hashes, rendered policy/guard and first-host
binding with the observed configuration hashes/modes/ownership. Its source receipt
SHA-256 is `efc66ea4335e9df7a987aed67eaac05dd5e5e1cfd32c4e82d4c5dd859f1abd3a`.
Both inspections' frozen inputs and receipts remain preserved. No executable live
operation or new inspection was sealed or run, and nothing was published.

Qualification: six profile tests, twelve readiness tests and seven existing atomic
configuration tests pass (25 total), alongside the native referrer and ingress
checks above. Native sessions 10034 and 31317 exited 0 and are retired; containers
used `--rm` with temporary-only writable storage. Full authenticated browser,
cookies/CSRF, WebSocket, Caddy/DNS, actual proxy-source/path, persistent ingress
ordering/recovery and Pi resource acceptance remain under W-128. Preparing those
checks in the complete owner candidate is the next action; no separate platform
or replication engine is introduced.

The first documentation hook passes found extra blank lines in the onboarding,
architecture and result updates. Those formatting defects were corrected locally;
no executable input changed. Sessions 80002/61585 are retired (their final shell
status was 0, but the Markdown hooks inside them failed, so that shell status is
not counted as a successful hook run). Final scoped checks are recorded below.

Final scoped documentation pre-commit runs passed for both owners; monitoring
session 91373 exited 0 and is retired, and server checks completed synchronously.
Executable profile/readiness hooks, JSON validation, configuration YAML, relative
links and whitespace checks passed. No execution session remains active. Changes
are local and uncommitted; no live operation or publication is authorized.

## November 12 — W-134 guard/browser qualification and W-135 stop

Aaron requested guard persistence/recovery, actual proxy paths and full browser
acceptance before sealing. Work remained local. No production Webmin listener,
Caddy release, DNS record, account or service was changed. Both consumed readiness
bundles remain intact; no new deployment bundle was defined or sealed.

Added the proposed Webmin-owned guard unit/dependency and one Caddy fragment outside
its accepted tree. The native systemd/nft fixture passed:

- stopping the guard stops Webmin while retaining its rules;
- invalid rules block startup and invalid reload retains the last valid table;
- each Webmin start reasserts the guard, preserving an unrelated sentinel table;
- restarting the owned container restores the enabled guard and Webmin;
- restoring exact saved loopback configuration, verifying IPv4/IPv6 HTTP and only
  loopback listeners, then removing only the owned table preserves the service
  and unrelated rules.

The first stop assertion expected inactive, but native miniserv exited nonzero
on stop. The corrected check accepts inactive/failed only with MainPID=0. Its
failed receipt remains retained; subsequent lifecycle and recovery checks passed.
This does not bypass a running-service check. The oneshot guard is not continuous
integrity monitoring: deleting its table externally while Webmin runs is not
automatically detected. Native allowlisting remains a separate control.

Private evidence:
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-browser-qualification-mpcul8ux/`.
`qualified-source-hashes.json` binds the tested sources. Native Webmin 2.670 and
Caddy 2.11.4 ran under systemd in a network-none container with namespace-local
NET_ADMIN. Chromium 156 trusted only the fixture CA; no TLS verification bypass
was used. Browser credentials were randomly generated, fixture-only and private.
The explicit miniserv fixture unit replaces the image's SysV-generated unit; it
is not proof of production unit equivalence or ARM64 resource acceptance.

The production-shaped proposed Caddy fragment was used with declared local
hostname/address/client-network/TLS substitutions. Both frontend families passed
rejected-password/valid login, eight assets, Secure/HttpOnly session cookie,
approved/foreign/missing referrer checks, and logout with old-session rejection.
The first protected-page attempt timed out at 15 seconds; a bounded 60-second
check later passed. First-choice upstream selection means these receipts do not
prove each backend family independently. These were partial HTTP/session passes;
WebSocket was not included and full application acceptance was not claimed.

The standalone Perl dependency probe initially omitted Webmin's vendor_perl path
and wrongly suggested a missing WebSocket module. Native package source contains
the module; the corrected Perl load of Net::WebSocket::Server and IO::Pty exited 0.
A disposable dependency-image build failed because the guessed Debian package
name was unavailable. Its log is retained, the build was abandoned, and no added
package or production dependency change is proposed from that invalid probe.

A fresh fixture used the existing image, full browser test and a fixture-only
non-root terminal account. No terminal command was sent. Its private evidence is
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-browser-complete-tqseeb19/`.
`source-hashes.json`, `image-id.txt`, the browser receipt and `terminal-service.json`
retain input and outcome identities. It again passed login/assets, then timed out
at the protected settings page and ultimately recorded the W-135 OOM state.
WebSocket testing never started. The same workload is therefore not reliably
qualified within the preserved service cap. No cap increase, narrowed acceptance,
production retry or inferred Pi failure follows from this local result.

Actual Caddy-to-Pi source/path checks remain pending: retained Kuma source policy
is only a proposal basis. Before sealing, reconcile native unit/drop-in identity
and route-selected sources under bounded target authority. Actual HTTP ingress,
unlisted-client rejection, each upstream family, both proxy nodes/VIP, existing
PAM/sudo account, WebSocket and Pi resource acceptance must be staged in the one
owner-reviewed operation after the restricted listener exists. A route lookup or
local loopback test cannot replace those gates. Updated owner onboarding and
operations documents describe that boundary and ordered guard recovery.

All shell sessions exited and are retired: 34819/1635 exited 1 (browser failures),
21913 exited 1 (fixture stop assertion), 55849/33194/40737/86422/83107 exited 0
(lifecycle, browser and restart/recovery), 10298 exited 100 (abandoned image build),
55831/98074 exited 0 (fresh fixture start/preparation). Both owned containers were
removed. No browser, container or execution session from this work remains active.
Local tests: 18 profile/readiness and 7 configuration tests passed; browser script
syntax passed. Full native browser/resource qualification remains failed, not
superseded by these smaller checks. Source changes remain uncommitted.

Scoped pre-commit checks passed in both owner repositories; monitoring session
30181 exited 0 and is retired. Qualification Python syntax and browser JavaScript
syntax passed. Whitespace checks passed. No source was committed or published.

## November 12 — W-135 retained-evidence reconciliation

This work reviewed retained local receipts and owner sources only. No browser
acceptance, container workload, live inspection, service change or publication was
replayed. The prior guard and partial-browser results remain intact. No architecture or accepted resource-policy change was made.

Six current source hashes match the failed fixture's recorded bindings. The
private reconciliation store is
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-memory-reconciliation-r8zm5_tv/`.
`retained-evidence.json` preserves comparisons and hashes of the original safe
receipts; `unit-source-comparison.json` records declared owner/fixture differences.
The original evidence directories were read, not rewritten.

The terminal receipt establishes Result=oom-kill, MemoryPeak=201326592 bytes,
MemoryMax=201326592, MemoryHigh=134217728 and NRestarts=0. The browser receipt
establishes a timeout at trusted-referrer after successful login/assets. Neither
receipt contains contemporaneous memory.events, anonymous/file/kernel charge
breakdown, process PSS or an ancestor-limit timeline. They do not establish which
process allocated memory, whether the service or an ancestor triggered the OOM,
or whether that page alone caused the failure. A memory leak, package-query
regression, required larger cap and Pi failure remain unproven.

The foundation-owned drop-in source hashes to
`2cf5ef73617a668b7f39bd8f75da0694735c9dfefa763661de3bd08a61c9071b`, matching the
retained correction operation's guard identity. Its memory/swap/CPU/task controls,
installation condition and control-group kill mode match the fixture declarations.
The fixture substitutes direct foreground miniserv for the installed native unit,
uses 30/15-second startup/stop timeouts instead of 60/20, and omits explicit start
rate, OOMPolicy and SendSIGKILL declarations. Defaults or inheritance may match
some effective values; this source comparison does not establish effective drift
or attribute the OOM to those differences. The successful target capture retained
unit/drop-in paths, not enough unit content to close equivalence. The native
miniserv source still forks request handlers with --nofork; that flag does not disable
request forking and is not evidence of serialized requests.

The first fixture's successful browser sequence and the fresh fixture's failure
used different histories. The latter added a synthetic Unix account and future
WebSocket branch, but never reached that branch. Neither a clean restart alone
nor that account change is an established remedy or cause. One local Caddy and
its two upstream health paths, browser background work and extra asset checks
remain potential contributors to measure, not asserted causes. A production pair
must also be represented in later workload qualification.

Reconciliation recommendation: preserve Webmin's 192 MiB cap, 128 MiB high watermark, no-swap
policy, other service caps and 96 MiB reserve. The accepted 624 MiB startup budget
is 320 + 192 + 16 + 96; increasing Webmin by any amount changes that admission
budget and requires separate host review plus combined running-service/scan
qualification. Do not borrow reserve or count hypothetical recovered overhead.

Reused the existing Webmin diagnostic sampler rather than adding another runner.
Its samples now retain memory charge categories, effective limits/swap usage,
selected numeric PSS aggregates, parent PID and explicit unavailable/truncated
process evidence. Existing response-body/cookie/command-line/environment exclusions
and output/time bounds remain. Its live HTTP runner still emits diagnostic GETs;
it must not be mistaken for a passive browser observer. Future local attribution
must call the sampler without that request thread, correlate bounded safe browser
phases, capture unit and container/ancestor events before teardown, and verify
that observation is outside the Webmin service cgroup. Measurement overhead and
missing samples must remain visible. No such runtime diagnostic was executed here.

The next local qualification must first align the fixture with owner unit/drop-in
controls, preserve the existing browser workload/health checks and use one changed
factor per controlled comparison. A passing diagnostic control cannot replace
full browser, WebSocket, actual proxy-source/path, native account or Pi resource
acceptance. W-135 stays Open and W-134 stays Blocked until that evidence supports
an owner-governed correction; no deployment is sealed.

Validation: six focused diagnostic tests passed, including numeric-only memory
projection, omission reporting, disappearing processes, private-data exclusion and
real local-loopback HTTP/timeouts. Scoped pre-commit checks passed in both owners;
working-tree Gitleaks scans passed for Webmin and the monitoring repository, and
whitespace/table checks passed. Sessions 50530, 21555 and 12568 exited 0 and are
retired. No runtime fixture or live-target execution session was created.

## November 12 — W-135 aligned offline attribution in progress

Aaron requested alignment and phase-correlated memory capture. The new private
store is `/home/aaron/code/.local-evidence/uptime-kuma/webmin-memory-phases-b5u3vjvd/`.
One owned network-none fixture uses existing image
`14256f5f3c69b7fec79d8153ca54737d5b9df4c60af6a46faa57a791d7d5e9a2`.
Its Webmin unit comes from the pinned package's updateboot.pl producer; its
foundation drop-in is extracted unchanged from the owning YAML and hash-bound.
No handwritten unit or copied resource-policy subset is used. Synthetic account,
loopback fixture addresses, fixture CA and AMD64 limitations remain explicit.
The existing browser test now emits bounded safe monotonic phase markers. The
offline observer reuses sample() without its HTTP probe thread, samples Webmin
and visible ancestors, and stops the owned services on failure/deadline. It does
not retry the browser or change resource limits. Runtime evidence is diagnostic,
not a new production acceptance attempt or a deployment authorization.

### Aligned attribution result

The package-generated unit and unchanged owner drop-in passed effective checks:
MemoryHigh=128 MiB, MemoryMax=192 MiB, no swap, 128 tasks, one CPU,
KillMode=control-group, OOMPolicy=stop, 60/20-second startup/stop timeouts,
Restart=on-failure with two seconds, and three starts per five minutes. The native
unit also supplies PERLLIB and its own ExecStart/ExecReload. The generated unit,
effective property receipt, owner binding and exact executed source copies are
retained. Current installed Pi unit/drop-in identity is still not verified; the
fixture does not recreate its host-specific startup-authority state.

The one diagnostic collected 48 samples over 11.975 seconds (including a
five-second baseline), with a maximum observed sampling gap of 0.257 seconds.
The synthetic IPv4 browser workload exited 0: trusted TLS, rejected/accepted login,
eight assets, protected-page referrer checks, native WebSocket frames without
terminal input, and logout/old-session rejection passed. The Webmin service was
active before containment with NRestarts=0 and MemoryPeak=139042816 bytes
(132.6015625 MiB), below the unchanged 192 MiB cap. Its memory.events.local ended
with high=446 and max/oom/oom_kill/oom_group_kill=0. Visible system.slice/container
ancestors also showed no local hard-limit/OOM events. This is a diagnostic pass,
not production acceptance or proof that the historical OOM cause is fixed.

The highest sampled current charge, 138997760 bytes, coincided with trusted-referrer.
The sample included nine native/CGI-related processes and predominantly anonymous
memory; one process rollup was unavailable. Across the run there were no truncated
process inventories, but seven samples lacked at least one rollup. The observer
ran outside Webmin's service cgroup and peaked at 18604 KiB RSS. It is not free
observation overhead and is not added back to any admission threshold. Recorded
phase markers cover every browser stage, but assets and foreign-referrer completed
between memory samples. Cross-file reads are not an atomic allocation snapshot;
these data cannot attribute every byte or reconstruct the historical failure.

The run was shorter than the configured 30-second health interval and used one
Caddy process, synthetic authentication, fixture CA and AMD64. It does not qualify
sustained health-check overlap, a real proxy pair, IPv6 browser/each upstream path,
Pi resources or the existing operator account. Keep full acceptance pending and
preserve all earlier partial passes/failures. No cap increase or acceptance waiver
was selected. Fixture alignment plus instrumentation changed several conditions;
a single successful run is not a controlled proof of which change mattered.

Evidence files include `memory-phases.jsonl`, `browser-phases-ipv4.jsonl`,
`phase-summary.json`, `attribution-result.json`, `browser-expanded-ipv4.json`,
`generated-webmin.service`, `effective-unit.txt`, `source-hashes.json` and
`executed-sources/` in the private store above. Credentials/keys remain separate
private fixture inputs and are not included in source hashes or diagnostic output.
After collection, only the phase reader was hardened to read at most 16385 bytes
and accept known phase names; three neutral parser regressions cover that change.
The actual executed observer is preserved with its original hash; no workload was
repeated to validate the parser-only correction.

Containment stopped Webmin/Caddy. Native miniserv left failed/exit-code on stop,
with MainPID=0 and no restarts; that stop result is distinct from runtime OOM.
Caddy was inactive and no owned browser/node process remained. Container
webmin-memory-b5u3vjvd was removed. Sessions 57315 (launch), 48669 (preparation)
and 6121 (diagnostic) exited 0 and are retired. No live target was contacted,
no consumed deployment was replayed, and nothing was published or sealed.

Final validation: three phase-reader and six diagnostic regressions passed;
browser JavaScript syntax passed. Scoped owner pre-commit checks, whitespace
checks and working-tree Gitleaks scans passed. Test/hook sessions 42774 and 95731,
and final scan session 63230, exited 0 and are retired. The parser-only follow-up
has its own private qualification hash record; the executed sources remain intact.
No session or task-owned container remains active. Changes are uncommitted.

## Sustained paired-proxy resource qualification — November 12, 2026 (W-135)

Local scope only: extend the aligned fixture in place with two Caddy processes,
four sequential node/frontend-family browser checks (A forces IPv4 upstream,
B forces IPv6), then restore both upstreams on each proxy and run two concurrent
95-second authenticated browser/WebSocket workloads. Repeated protected HTTP
checks occur at 0/15/30/45/60/75/95 seconds. This spans three configured 30-second
health intervals; it does not instrument each successful health probe.
All addresses remain inside one network-none namespace; production source/path
acceptance is not represented by these fixture paths.

Reuse the pinned fixture image and package-generated unit with exact owner
foundation controls. No cap, reserve or restart-policy change. Observe every
250 ms with existing bounded cgroup/process sampler; retain phase markers,
visible ancestor and proxy charges, gaps and observer RSS. Stop/contain on failed
workload, hard-limit/OOM event, disappearing cgroup, 24 MiB evidence bound or
420-second deadline; do not rerun a failed workload. Preserve old evidence.

Private evidence: `.local-evidence/uptime-kuma/webmin-paired-resource-ioc4sknu/`.
Source copies/hashes, owner binding and scope are retained before launch.
Five neutral phase/matrix/containment tests and syntax checks passed. No live
contact or publication is authorized. Runtime qualification is not yet complete.

### Paired resource result: failed, contained

The exact source snapshot above ran once. Preparation exited 0 with the package
unit and owner controls verified. Observation exited 1 after 82.176 seconds with
318 samples; its stop reason was workload-failed. Node A/IPv4 completed trusted
TLS, rejected/accepted login, assets, referrer checks, native WebSocket and logout.
Node A/IPv6 reached the expected TLS endpoint, accepted login and eight assets,
then timed out after 60 seconds opening the protected referrer page. Both used
A's deliberately single IPv4 upstream; this is not evidence of an IPv6 backend
failure. Node B browser paths, restoring dual upstreams and the concurrent
95-second sustained phase were not executed.

Webmin was active with NRestarts=0 before containment. MemoryPeak was 169021440
bytes (161.19140625 MiB), and sampled current memory reached 168566784 bytes.
The unchanged MemoryHigh=128 MiB produced 12440 high events; max/oom/oom_kill/
oom_group_kill remained zero. During the failing phase, up to 13 sampled
processes waited in __mem_cgroup_handle_over_high. End-of-run memory pressure
reported full avg10=97.42%, with about 61.9 seconds cumulative full stalls.
This directly demonstrates severe high-limit reclaim/throttling in this run;
it does not identify each request's process or prove the earlier OOM's cause.

Both Caddy health checks timed out awaiting headers around observer seconds
37.7 and 67.7. Caddy subsequently returned HTTP 504 after a 60.003-second header
wait. Initial connection-refused health messages occurred about 25.3 seconds
before observation, while the fixture backend was starting; retain them separately
from the later loaded-service timeouts. Absence of hard-limit/OOM events is not
successful responsiveness or capacity acceptance. Do not relax browser/proxy
response deadlines or service controls to turn this result into a pass.

Sampling gap peaked at 0.2686 seconds; observer RSS peaked at 19368 KiB outside
the Webmin cgroup. Inventory exceeded the 16-process capture bound in 24 samples
(up to two omitted); seven samples lacked a process rollup. Attribution is
therefore incomplete. Visible ancestors had no local max/OOM events; container
peak was 874143744 bytes against its 1536 MiB limit. Chromium and both fixture
proxies are outside Webmin's cap. This AMD64 run does not qualify the Pi's combined
Kuma/foundation/scan reserve or actual proxy source selection.

Retained private files include source-hashes.json and executed-sources/,
foundation-dropin.conf and owner-binding.json, generated-webmin.service,
effective-unit.txt, fixture-mode.json, four validated Caddy configurations,
per-client results/phase markers, memory-phases.jsonl, phase-summary.json,
proxy-timing-summary.json, bounded private journals and attribution-result.json.
Synthetic credentials/keys remain separate, private and excluded from hashes.
No previous bundle, receipt or evidence file was changed.

Containment independently verified all three service MainPIDs=0, no Webmin/HTTPS
listeners and no node/chromium processes. The native Webmin stop left failed/
exit-code, distinct from its active/success state before containment. The first
container removal refused because its systemd PID 1 was still running; the owned
container was then stopped and removed successfully. No browser or service retry
occurred. Launch 45638 and preparation 50094 exited 0; observer 75806 exited 1;
all are retired. Cleanup commands completed synchronously. No live host contact,
publication or deployment sealing occurred.

Local validation: five neutral phase/matrix/stop-condition regressions and Python/
JavaScript syntax checks passed. All eleven executed source hashes match their
retained copies and current files. Owner checks and working-tree secret scans
passed. Record lint initially rejected two extra blank lines; those were removed
before the final check. Helper-based repository verification was unavailable from
the parent workspace (not a Git repository); focused checks provide the available
verification. This does not convert the failed browser workload into acceptance.
Changes remain local and uncommitted.

## Proposed durable fixture-evidence instruction (W-136)

Proposed location: `/home/aaron/code/AGENTS.md`, beside substantial-change and
validation guidance. This is proposed wording, not an installed global rule.
Keep one canonical workspace instruction; component runbooks and the maintained
change-control skill can reference its boundary rather than copy diverging rules.

> **Fixture evidence and target capacity**
>
> Use fixtures primarily to validate configuration correctness, application
> contracts, safety controls, recovery and reproducible defects. Identify the
> decision each test supports before building or extending it.
>
> Do not use a substitute fixture to qualify, accept or reject the capacity of a
> named deployment host. Do not expand or repeat fixture load tests to settle that
> question. Target capacity requires bounded measurements on the actual host with
> its intended workload, service controls, dependencies and co-resident services.
>
> Resource testing in fixtures remains appropriate when it directly answers the
> question under test: verifying resource-limit enforcement, detecting a leak or
> resource regression, comparing implementations under controlled conditions, or
> characterizing the actual disposable deployment platform being evaluated. State
> the workload, relevant equivalence/differences, metric, duration and decision in
> the existing work record. Limit conclusions to that tested system or comparison;
> never promote them to capacity acceptance of a different host.
>
> Stop fixture work when the stated correctness/defect question is answered or
> the fixture cannot resolve the remaining uncertainty. Repeat only for changed
> relevant inputs or a specific unresolved defect. A fixture capacity failure is
> risk evidence for target trial design, not an indefinite requirement for a
> fixture pass. Concrete correctness/security/recovery defects still require a
> safe resolution before using the affected path.
>
> Preserve failures and uncertainty. Prepare one bounded actual-target trial with
> unchanged accepted controls, explicit workload, observation, stop conditions and
> recovery. Obtain the applicable live authority before contact or mutation; do
> not weaken limits, omit failing functions or extend timeouts to manufacture a
> pass. Do not add a separate document or bespoke test framework for this rule.

Aaron's agreement to the actual-host direction is applied to this project:
PLAN.md now defines the trial, and Webmin's onboarding procedure no longer makes
a substitute-fixture resource pass a target-capacity prerequisite. Existing
correctness qualification and historical failures remain valid within their
limits. W-135 is neither erased nor marked target-capacity accepted.

## Actual-host qualification preparation (W-137)

The [target qualification plan](PLAN.md#target-qualification-boundary--november-12-2026)
specifies real Pi/proxy paths, one workstation browser, unchanged host controls,
a ten-minute measured workload with 30-second baseline and at least 95 seconds
of authenticated use, existing guarded scan integration, stop conditions and
owner recovery. No DNS change occurs in that trial. Private credentials remain
with Aaron; operator waiting outside the measured trial is not a deployment
failure. No root terminal is opened merely to satisfy a test.

Retained readiness has paths but not hashes of the actual Pi service unit and
all drop-ins, nor current route-selected proxy sources for Webmin. These are
needed for exact before-state, ingress and recovery bindings. The existing
Webmin collector now optionally hashes only selected unit paths, captures
non-secret effective controls, loads native modules using explicit Webmin library
paths, and reports only user/sudoenforce from an existing ama terminal ACL.
It does not expose unit bodies, environments, users databases or credentials.
Missing terminal ACL is an explicit observation, not permission to create one.
Installed-file drift and boot changes reject the capture.

Sixteen collector regressions passed, including rejected private/unexpected paths,
empty metadata, unchanged legacy collection, no raw stderr and unit-identity drift.
Launcher tests used a local SSH stub: exact three-target order, strict host pins,
stop on primary failure and exclusive-attempt replay rejection passed. This is
correctness qualification, not a capacity fixture. No test contacted a host.

### Exact read-only target-readiness bundle for review (W-137)

Prepared, locally qualified and unused; not authorized. One capture each, in order:
`ama@10.1.3.75`, `pi@10.1.0.53`, `pi@10.1.0.54`; stop on the first failure.
No browser, HTTP, load or scan runs. The selected Pi native hostname remains
`j2-svpi3bmf`; targets are bound through retained strict SSH host-key pins.
Proxy hostnames are reported for independent review. Each capture uses fresh
boot identity and checks continuity within that capture, never an old boot ID.

Bundle:
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-target-readiness-fe7cvab0/`

`INPUTS.SHA256SUMS` SHA-256:
`f269d075aea624082899b446b5c92ed451f44fbbfee4eaf47a17f6d216918c3c`

Frozen collector SHA-256:
`edbddd0b776c1d37a6732629f3d6586cfd487791db6061267a4de42ee191ea67`

Exact command after approval and independent manifest-digest verification:

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/webmin-target-readiness-fe7cvab0/run.sh
```

Five manifest-bound inputs: Pi collector, proxy read-only payload, retained host
pins, scope JSON and launcher. The launcher verifies inputs and exclusively
creates attempt/ before any SSH, preventing replay. Existing SSH credentials are
used without collection; remote payloads run from stdin without staging files.
No previous bundle or receipt is changed. An unsuccessful capture stops the
sequence; it does not authorize a replacement attempt or a capacity conclusion.

Pi scope: existing selected non-secret Webmin configuration/file identities;
installed Webmin version and architecture; stable installed service/drop-in
hashes and effective startup/dependency/resource properties; native IO::Pty and
Net::WebSocket::Server availability with explicit Webmin library paths; only
user/sudoenforce from the optional existing ama terminal ACL; port 10000 listeners,
eth0 addresses/routes and nftables rules. No full unit bodies, environment,
command lines, password/user databases, sessions, private keys or account changes.

Proxy scope: route lookups to each Pi family and local addresses, hostname/current
boot ID, accepted current-release path and manifest identity, Caddy service state,
and public certificate coverage/expiry for the approved Webmin browser name.
No probes to the backend or DNS, no certificate-worker execution, no release
staging/publication/reload, no failover and no access to private TLS keys.

Bounds: 115 seconds plus five seconds termination grace per SSH capture, remote
100-second deadline with five-second grace, eight seconds per diagnostic command,
256 KiB per selected file, 64 KiB retained command-output checks and 2 MiB file
limits for controller stdout/stderr. At most three sequential target captures;
no retry. Private receipts/transport output/status remain under attempt/.
Capture failures report bounded error metadata. These limits bound the inspection;
they are not application performance criteria or capacity qualification.

Excluded: all remote writes/staging, workload generation, credential collection,
package/configuration/firewall/account/DNS changes, service start/stop/reload,
restart/reboot, publication and the future guarded backend/Caddy deployment.
No recovery is needed for these reads. The mutation/trial scope remains unsealed
until these missing inputs have been reconciled and the exact recovery binding
and applicable browser capability are prepared. Reviewability is not live authority.

Authorization reason: homelab-server-configs/AGENTS.md, Definition and authorization,
requires: "A definition-only task must not contact a live target unless the user has
explicitly requested or authorized a read-only inspection." The earlier inspection
approvals are consumed; agreement to prepare the target trial does not authorize
these captures or the later mutation. This is one bounded readiness review, not a
new fixture requirement or an approval for each internal read command.

### Fleet readiness instruction clarification (W-137)

Aaron required the missing unit/source prerequisites to apply fleet-wide. Webmin's
CADDY_ONBOARDING.md now has one mandatory readiness section for every host:
installed FragmentPath/all DropInPaths identities and effective controls, plus
current route-selected sources from every Caddy node to every intended backend
family. It defines private evidence fields, ingress/recovery bindings, pre-mutation
rechecks and separate real-packet acceptance. OPERATIONS.md links that canonical
section. No values may be copied from the first host or another application's
allowlist as assumed acceptance. The sealed inspection inputs and approval state
remain unchanged; no live capture, harness-rule installation or publication occurred.

### W-136 installation and W-137 execution authorization

Aaron approved the exact proposed workspace rule and sealed read-only capture.
The rule is installed verbatim under Fixture evidence and target capacity in
/home/aaron/code/AGENTS.md. All five sealed input hashes and the reviewed manifest
digest matched; attempt/ was absent. One execution is authorized, Pi then both
proxies, stopping on failure. No mutation, browser load, retry or publication.

### W-137 read-only capture passed — November 12, 2026

The exact approved launcher ran once and exited 0. All three captures completed:
Pi first, then primary and secondary. Both proxies reported capture timestamps
19:49:53–19:49:54 UTC. All input hashes were verified before execution; receipts
and their SHA-256 index remain in the sealed bundle's private attempt/ directory
and receipt-hashes.json. Session 6287 is complete and retired. Approval is consumed;
no further inspection, mutation, browser load, retry or publication is authorized.

The Pi reports ARM64, Webmin 2.670, active/running and NRestarts=0, with only
127.0.0.1/[::1]:10000 listeners. Effective owner controls remain 128/192 MiB
high/max, no swap, 128 tasks, one CPU, control-group kill/stop-on-OOM, 60/20-second
startup/stop timeouts and on-failure restart at two seconds. Its startup-authority
dependency remains present; preserve it when adding the ingress dependency.
Installed file identities, root-owned mode 0644:

| Installed file | SHA-256 |
| --- | --- |
| /usr/lib/systemd/system/webmin.service | ca26388a569ef106439eec33a9ca29153caaeac63c06148a863a69196b496768 |
| /etc/systemd/system/webmin.service.d/10-fleet-foundation.conf | 2cf5ef73617a668b7f39bd8f75da0694735c9dfefa763661de3bd08a61c9071b |
| /etc/systemd/system/webmin.service.d/60-startup-authority.conf | 365cf8b8af7e55f2e22a78a7ba1bc5b234fb167c9832992b69808f49c5c16b7d |

Both native module loads passed. The optional /etc/webmin/xterm/ama.acl is absent;
this does not establish the effective terminal privilege or mean WebSockets are
unavailable. Resolve a safe existing-account capability before browser acceptance;
do not create an ACL/account or open a root terminal under this read-only approval.
Selected configuration retains collect_pkgs=0, referers_none=1 and the loopback
profile. Global referer remains absent, so the candidate's explicit referer=0 is
still a deliberate reviewed change, not an observed existing setting.

| Proxy | Destination family | Observed source | Interface |
| --- | --- | --- | --- |
| j1-svpihole0 (10.1.0.53) | IPv4 to 10.1.3.75 | 10.1.0.53 | eth0 |
| j1-svpihole0 (10.1.0.53) | IPv6 to fd36:5aa8:6971:1::75 | fd36:5aa8:6971:1::56 | eth0 |
| j1-svpihole00 (10.1.0.54) | IPv4 to 10.1.3.75 | 10.1.0.54 | eth0 |
| j1-svpihole00 (10.1.0.54) | IPv6 to fd36:5aa8:6971:1::75 | fd36:5aa8:6971:1::54 | eth0 |

Both route lookups report on-link paths with no gateway field. These are current
route selections, not completed HTTP or target-observed packet acceptance, and
do not establish post-failover selections. Both proxies are active with no restarts
and report the same accepted release 20261111T213048Z-71b7deb8-bc71-45d5-8f33-98270af79d3b,
manifest SHA-256 b972d15185960fc219d09c1c047cd5c2269be97f42e6cc5eef6a3b691aa7d52d.
Public leaf/fullchain hostname and expiry checks passed for the approved Webmin
name; the certificate expires January 19, 2027. This is certificate coverage,
not a new trusted-browser handshake. Per-node boot continuity, Pi file/service stability and unchanged proxy release
paths passed within the captures. No service, firewall, account, Caddy or DNS state was
changed; no host capacity or browser acceptance is claimed.

## Fleet model and actual-host trial preparation (W-137/W-138)

Aaron approved adding safe WebSocket acceptance to fleet onboarding and preparing
an actual-host trial. Preparation grants no live authority. CADDY_ONBOARDING.md
now requires the enabled feature, effective existing-account permissions, exact
safe action and side effects, expected connection/session/cleanup results and an
explicit applicability disposition before sealing. OPERATIONS.md links that one
canonical section. No account creation, permission broadening or root-terminal
probe is implicit in acceptance.

The fleet procedure also requires reusable discoveries to be incorporated into
the appropriate Webmin/Caddy/DNS owner instructions before the finding closes.
Host values, private evidence and attempt outcomes stay in the existing record.
This first deployment is the model; its success will not accept other hosts.

Local review of retained Webmin 2.670 source found xterm/shellserver.pl calls
proc::pty_process_exec at lines 88–89 before constructing its WebSocket listener.
The same source selects an execution identity and shell initialization earlier.
Thus sending no terminal input does not establish absence of side effects. Source:
foundation-prepare-20261110-bcvgim9k/extracted/webmin_2.670_all.deb/usr/share/webmin/.
This does not establish ama's effective live permissions or justify a new live
inspection. W-138 retains that gap; no not-applicable or successful check is claimed.

PLAN.md now binds preparation to the accepted installed unit identities, observed
per-node/family sources and Caddy parent, and distinguishes the active-loopback
recovery baseline from the old stopped installation diagnostic. It records ordered
restoration, controller-loss containment, Caddy partial-state handling and the
remaining exact backup/timer/child bindings. No new executable recovery path or
sealed operation is claimed. Existing profile/guard implementations are reused;
no fixture capacity workload, live contact or publication occurred.

Validation: focused Markdown/pre-commit checks cover the four changed documents;
working-tree Gitleaks found no leaks. An extra blank line found by Markdown lint
was corrected before the final check. No executable behavior changed and no
capacity test ran. The prior parent-workspace vexp completion check remains
unavailable (not a Git repository); direct repository checks are used instead.

## Native trial bindings and safe statistics method (W-137/W-138/W-139)

Aaron confirmed that existing ama access includes System Information and real-time
statistics graphs, without a new login or inspection. W-138 selects that feature
instead of xterm. Pinned Webmin 2.670 sources reviewed: authentic-theme/stats.cgi,
stats.pl, authentic-funcs.pl and extensions/stats/stats.src.js in the retained
foundation package. Native System Status access and session validation remain
required during the future trial. The collector can write cache/history and
register a loopback backend; those are declared workload effects. Its shutdown/
disable control can affect all clients, so test cleanup must not invoke it.
The method, ordinary settings preservation and cleanup distinction are now in
the shared fleet procedure and first-host PLAN.md. Actual browser acceptance is
still pending; no new native account capability was measured.

The backend implementation reuses the existing renderer/configuration producer
and native Ansible/systemd. proxy-trial.yaml stages all inputs first, snapshots
an active enabled loopback baseline, arms a 30-minute recovery timer, then starts
a bounded apply service. recover-proxy.py preserves exact file metadata and all
installed unit/drop-in/effective controls. It stops the apply service before
restoration; cancelled/restored states reject late apply. proxy-trial-restore.yaml
requires verified restored state before stopping the timer. No backend writes
remain as controller tasks after arming. This closes the delayed-controller
write race identified during local review.

The private prepared binding/rendered inputs are in
webmin-trial-preparation-h3qt9wvn/. Installed identities come from W-137's accepted
receipt, not source hashes. Proposed host storage, timer/service bounds and
backup paths are in PLAN.md. This is an unsealed backend component, not a complete
Caddy/browser/resource operation. No parent boolean gate is claimed to implement
those missing owner checks. No Caddy stream was defined or production inventory
changed. The selected trial restores loopback even on a passing measurement;
future permanent promotion and DNS are not implicit.

Native correctness qualification used the retained local image with networking
disabled and a tiny dummy HTTP service, real systemd/nftables and the actual
backend producer/recovery commands. It measures no Webmin/ARM64 host capacity and
runs no browser. The fixture deadline accelerates the recovery timer to 30 seconds;
production's reviewed proposal remains 1800 seconds. Earlier local failures are
preserved in webmin-trial-local-20261112/ and webmin-recovery-native-n_3fk6d9/.
The first stopped at its handwritten guard setup; the latter did not reach
terminal recovery. Their retained diagnostics do not conclusively attribute every
failure. The fixture now uses the actual guard renderer and preserves failure
state/controls/journal before cleanup. Transient-unit absence and the guard's
reverse ordering edge are explicit implementation/regression cases, not reasons
to weaken baseline identity or effective-control checks.

Final native qualification passed in webmin-recovery-native-kcsrdd5e/: real apply
and timed recovery restored exact loopback configuration/metadata/effective
controls and both HTTP listeners, removed only trial ingress, preserved an
unrelated nft table and rejected a late apply. The frozen native inputs match
current source. The dummy service does not establish Webmin behavior, Pi capacity,
real proxy paths or Caddy recovery. Owned-container cleanup exited 0.

Fourteen focused recovery regressions, Ansible syntax checking through the owner
private-temp wrapper, scoped owner pre-commit and Webmin working-tree Gitleaks
passed. qualification.json and sessions.json in the private preparation directory
retain hashes, result boundaries and terminal session records. No live targets,
browser workload, capacity fixture, Caddy publication or DNS change occurred.
All local execution sessions are complete and retired. The combined trial remains
unsealed pending its existing-owner integration; no live authorization is requested.

## Combined trial integration review (W-137/W-140/W-141)

The existing application outer selected the Kuma proposal directly; its transaction
accepted only a 20-prefixed fragment, and the authorization test required Kuma's
FQDN/probe. Those assumptions prevented reuse for the reviewed Webmin proposal.
The outer now binds one workspace-relative owner source, exact application basename
in the documented 20-79 range and SHA-256. Missing/duplicate fields, traversal,
symlinked files/ancestors, name mismatch and changed bytes reject before transport.
The payload is rehashed after copying. The transaction and definition checks use
that selected application; no new publisher or parallel deployment entrypoint was
introduced. The neutral operation/transaction pins are reconciled; the stream
remains clean/inactive and accepted production inventories are unchanged.

The actual offline owner fixture now includes Webmin primary-first activation
while preserving the existing Kuma fragment. It exercises the real outer,
serialized SSH substitute, publisher, finalizer, accepted deployed reconciler,
Caddy reload and dual-stack HTTPS. These are correctness/path tests in an isolated
network, not actual Pi capacity, real proxy-source or browser authentication tests.
The first run stopped because the old Kuma-addition fixture copied a production
baseline that now already includes Kuma. It did not retain its remote runner
readback before its assertion; that evidence gap is preserved. The fixture now
retains readback before asserting status, excludes the candidate only for modeled
Kuma additions, and retains accepted Kuma for the Webmin case.

Private integration records are under `webmin-trial-preparation-h3qt9wvn/`.
The failed offline run is `/tmp/caddy-application-qualification-i7oosdii/`;
`dbzetw3s` passed the intermediate source. Final source qualification is
`/tmp/caddy-application-qualification-2skzatjx/`: all ten cases and independent
retained-evidence verification passed, cleanup status 0. Result/log/source-graph
copies are retained under the private preparation directory. The fixtures measure
no target capacity, and no live host was contacted.

Two integration boundaries still prevent sealing. W-140: application_restore
only handles local activation failure; the current outer cleans payloads on
success and does not contain/restore a replicated temporary child as one paired
operation. A standalone symlink rollback can be undone by late replication.
The certificate repair rollback is not an application trial recovery path.
W-141: the existing scan include installs its guard, and its observer explicitly
reports scan-only acceptance. The trial needs the installed guard identity and
one observer covering the combined workload through the scan. Importing that
include unchanged or adding another sampler would not satisfy this requirement.
PLAN.md records the concrete owner sequence and recovery ordering; the reusable
Webmin procedure now carries these requirements for subsequent fleet hosts.

No combined parent command, Caddy successor or deployment authority is claimed.
All consumed readiness and deployment bundles remain unchanged. W-137/W-140 and
W-141 remain unfinished; backend correctness and Caddy source binding alone do
not qualify the combined trial.

Focused host application policy, payload rejection tests, shell syntax/ShellCheck,
canonical formatting and readonly/local collision policy passed. Scoped owner
pre-commit passed. The first record lint run found two added blank lines; those
were corrected before the final record check. Caddy working-tree Gitleaks reports
only the five unchanged historical outer-hash entries in HISTORY.md; no new
finding or suppression. Offline sessions 90857 (failed), 31793 and 63431 (passed)
are retired, with owned-container cleanup 0. Host and record check receipts remain
in the private preparation directory. No live, publication or browser workload
session was started.

## Paired restoration and scan component qualification (W-140/W-141/W-142)

The application owner now admits a temporary trial with fresh boot continuity,
prior outgoing inventories and retained payloads. Its existing primary-first path
activates the selected Webmin fragment alongside Kuma. Completion or timeout
cancels later exposure, stops publication/reconciliation on both nodes, waits for
receivers, restores B then A, checks inventories and only then resumes transport.
Incomplete recovery retains inputs and stopped transport for owner handling.
The finish signal is not an application receipt. Controller loss does not imply
automatic paired Caddy restoration; backend deadline recovery is independent.

The first native incomplete-transfer case found W-142: Bash conditional invocation
suppressed intermediate errexit failures inside candidate validation. Explicit
returns correct that defect. Preserve the failed run at
`/tmp/caddy-application-qualification-bd77yg5a/`. The exact corrected 16-case run at
`/tmp/caddy-application-qualification-dptr9r89/` passed with network disabled and
owned-container cleanup 0. Its result.json binds source hashes and accepted
reconciler bytes. Cases include lost exposure reply, missing secondary transfer,
failed restoration, incomplete candidate and rejection of late exposure.
This establishes recovery behavior, not host capacity.

The foundation observer now accepts a private reviewed service/cgroup profile.
One observer and the existing lock cover baseline, workload, list-only scan and
post-scan samples. The 224/192/96 MiB thresholds and caps remain unchanged; fresh
192 MiB admission is rechecked after baseline. It records service identity,
controls, memory events/pressure and observer cost with timestamps. Drift,
restarts, swap, hard-limit events, reserve loss or excessive sampling gaps reject.
Resource acceptance remains separate from browser/path acceptance.

The trial Ansible branch verifies the installed guard before and after, stages
source/profile by separate hashes outside the empty evidence directory, and does
not reinstall the guard or alter its schedule. Nineteen observer/guard tests pass,
including overlap exclusion, post-baseline rejection, bounded trial launch,
retained failure readings and cleanup failures. Two local Ansible rendering tests
pass for default/trial commands and the unchanged daily schedule. The initial
sandboxed rendering runs failed to start Ansible's local RPC; the local-only run
outside that restriction passed. No inventory target was contacted.

Permanent owner procedures now describe these interfaces and fleet reuse.
W-140/W-142 are resolved locally. W-141 remains in progress because its full closure
also requires the parent to join actual path/source and browser receipts, prove
scan overlap and stop owned browser load promptly on failure. Those W-137 bindings
remain before sealing; no new live scope or operator command is proposed.

Private qualification/session records are retained under
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-paired-scan-e5vz3x0a/`.
All consumed bundles, target controls and accepted inventories remain unchanged.

## November 16 crash-status reconciliation (W-137/W-141/W-143)

The interrupted preparation survived in the working tree and private directory
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-parent-integration-527pe9z6/`.
New uncommitted drafts include the combined parent, proxy-source/counter checks,
statistics-only browser client, workload supervisor and handoff helper. The
single observer now has workload readiness/cancellation gates. These are local
implementation drafts, not an accepted combined operation.

Retained `native-result.json` reports pass, exit 0 and container cleanup 0.
All five current packet-qualification inputs match `native-inputs.json`. Four
isolated source/family paths and both denied families passed; no browser workload
or target-capacity test ran. Preserve the earlier entrypoint-timeout failure.
`render-tests.log` records two passing local Ansible tests; `parent-flow.log`
records a passing test containing five synthetic-owner scenarios. However, the
current combined parent and workload supervisor no longer match the retained
`parent-flow-inputs.json`; that pass does not qualify their final revision.
The earlier syntax-check log likewise does not establish current-input acceptance.

W-143 remains In progress. Direct comparison with PLAN.md found concrete closure
work: the client gives six paths short checks and only two a sustained hold,
whereas the plan requires at least 95 seconds per reviewed path; logout checks
for the login page but does not demonstrate denial of the prior session. Resolve
these implementation gaps without silently changing acceptance. Also verify the
native System Information navigation and current-socket frame readiness: the
client requests `/sysinfo.cgi`, the pinned file is under `authentic-theme/`, and
frame counts currently span navigation. This is an unresolved contract review,
not proof that the native route fails.

The first-host draft explicitly has no seal/live authority, operator readiness
and readiness acceptance are false, and no final `INPUTS.SHA256SUMS` exists.
The Caddy operation remains inactive. Exact owner authorization coverage, final
input binding, affected qualification and permanent procedure reconciliation
remain before a deployment review. W-137/W-141/W-143 stay In progress; accepted
Kuma and the Partial Webmin-extension result are unchanged.

Retained terminal logs reconcile stale session entries 9202 and 90506. The final
native run associated with 80114 also has a terminal pass/cleanup receipt; no
matching test/trial processes were visible in this status check. No old session
was polled or command replayed. This review contacted no live target, launched
no browser or fixture, and performed no publication. Production state has not
been refreshed; accepted state remains based on the existing receipts.

## November 16 final combined local qualification (W-137/W-141/W-143)

The statistics client now follows the native System Information link, requires
its page marker, and counts only fresh frames from currently open statistics
sockets after navigation. Source review resolved the earlier path uncertainty:
MiniServ searches the active theme's preroot, which provides `/sysinfo.cgi`.
The native theme supplies the selected navigation and `sysinfo_host` marker;
its own statistics client performs activation without test-driven setting changes.

All six frontend paths now receive at least 95 seconds in three successive pairs;
the final A/IPv4 and B/IPv6 pair uses the reviewed longer hold for scan overlap.
No more than two owned clients run concurrently. Every path logs out and tests
the prior session cookie against the protected page before clearing the cookie
and closing its context. Cookies remain in memory and never enter receipts.
The parent rejects missing per-path duration/session denial and uses the same
single-observer token gate and conservative cross-clock overlap checks. The
existing 600-second observation, Caddy window and backend recovery bounds are
unchanged; insufficient time or missing overlap fails.

Evidence is retained under
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-contract-final-d1xkjc2_/`.
`INPUTS.json` binds the nine-group suite: browser contracts, workload verifier/
cleanup, profile, recovery, resource observer, schedule rendering, actual Ansible
parent control flow with synthetic owner adapters, parent syntax and YAML checks.
All passed. The browser cases cover stale frames, closed sockets, absent page
readiness, frame loss, insecure cookie, invalidation failure and launch failure,
as well as success. Parent cases cover success, path failure, workload failure,
Caddy failure and unverified cleanup with ordered restoration.

After adding the receipt-interface regression, only two test files changed;
`FINAL-INPUTS.json` and `final-recheck.json` bind their successful affected rechecks
and confirm unchanged implementation inputs. Eight workload tests now include
receipts emitted by the actual client logic through the synthetic browser adapter,
joined to the actual parent verifier with synthetic clock/scan samples. This is
contract qualification, not measured browser behavior, native service execution
or Pi capacity. Retained native packet-test inputs still match the current source;
no redundant packet or capacity fixture was run.

The installed workstation module/executable access check passed without launching
Chromium. First-host observer/profile hashes still match their draft bindings.
The fleet Webmin and foundation procedures document native navigation, six-path
duration, session rejection, readiness/cancellation, clock brackets and cleanup;
neutral hooks cover the new client and workload regressions. vexp verification
was unavailable because its session points at the non-repository workspace;
focused repository checks provide the validation recorded here.

W-141/W-143 are resolved for local implementation qualification. W-137 still needs
the Caddy owner operation/authorization coverage and complete parent input manifest
before sealing; the Caddy stream remains inactive and operator/readiness flags
remain false. Live permission, browser/real-path, resource and recovery acceptance
remain AC-013 work. No previous bundle or receipt was changed or replayed.

Final checks: Markdown, YAML and whitespace checks passed. Repository-wide
Gitleaks exited 1 with 18 findings; structured triage located every finding in
`.vexp/manifest.json`'s generated `file_hashes` map, which Git ignores. They are
index fingerprints, not source-file credentials; the hash algorithm is not
inferred. There were zero source-file findings. Retain both scanner runs and
`gitleaks-triage.json`; no suppressions or index changes were made. Qualification
session 78485 and scan sessions 40555/32503 are complete and retired. Final source
identities remain unchanged. No execution session is active.

## November 16 combined trial sealed for review (W-137/W-144/W-145)

One local candidate is prepared; execution approval is recorded below. The sole
Caddy stream is `defined`, operation `20261116-webmin-first-host-trial`, with
status `defined-unexecuted`. Production inventories and consumed bundles remain
unchanged. [PLAN.md](PLAN.md#first-host-combined-trial-candidate-november-16)
owns the combined scope, acceptance and recovery.

### Exact bundle, command and scope

Private review root:
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-combined-review-0ve83yjr`.

- Parent authorization manifest: `INPUTS.SHA256SUMS`, 236 regular files;
  SHA-256 `b15710ed9209ac6e47e0e796798e2c4956d0514d797f106394cf30857ee4ef8d`.
- Caddy owner authorization: current
  `Caddy/scripts/run-serving-health-deployment-outer.sh`, SHA-256
  `d7b1d9ca0e8464286138f7c4c9954153bb7678cbc964f3753fa4fcae7889b754`.
  Its operation, transaction, recipe, state and coverage graph pass the owner
  authorization gate against `caddy-qualification-final`.
- `launch.json` binds the existing Ansible parent invocation and explicit runtime
  environment; `inputs/` binds inventory, native hostname, reviewed installed
  unit/configuration identities, source addresses, rendered guard/profile,
  resource controls, browser destinations and single-observer commands.
- `INPUT-METADATA.json` binds relevant file modes, runtime symlinks and absent
  SSH configuration inputs. Both SSH paths recognize the accepted keys.
  Causal qualification evidence is revalidated by the existing owner gate.
- Password: ama's existing Webmin password, prompted only in the workstation
  terminal after approval. External file reference:
  `/run/user/1000/webmin-trial-credentials-88f88a41b1ac58e502e3.json`.
  Owner-private runtime parent, exclusive mode-0600 creation, no value in hashes
  or logs, and identity-checked removal after the parent exits. Existing SSH
  authentication remains external; no private key is read into the bundle.

**Consumed November 16, 2026 — do not rerun:** approval covered one execution of this exact combined trial,
including its bounded acceptance and both owner recovery paths. After explicit
approval, run this command in the workstation WSL/Ubuntu terminal when available
for the automated trial; keep it open until the parent exits. It does not open a
human-response countdown or require a browser on the Pi.

```bash
/usr/bin/python3 -I -B /home/aaron/code/.local-evidence/uptime-kuma/webmin-combined-review-0ve83yjr/operator.py --manifest-sha256 b15710ed9209ac6e47e0e796798e2c4956d0514d797f106394cf30857ee4ef8d --run-approved-once
```

The helper verifies inputs and owner readiness, prompts privately, then invokes
`Webmin/ansible/proxy-combined-trial.yaml` through the existing local-temp wrapper.
It adds no deployment/recovery implementation. `attempt.started` prevents replay;
retain that marker, `parent.log`, `parent.exit`, workload receipts and independent
owner outcomes even on failure. A preflight failure is not permission to retry.
`--verify-only` completed locally without credentials, target contact or Chromium.

Targets: ama on `10.1.3.75`, pi on `10.1.0.53` and `10.1.0.54`, and the reviewed
Caddy node/VIP frontend addresses. Mutation is confined to temporary guarded
Webmin exposure, one Caddy application candidate through primary-first managed
replication, one list-only scan and their owned runtime state. No DNS, reboot,
forced failover, account/ACL change, terminal, resource-limit change, permanent
browser promotion, unrelated route/radio change or Git publication.

Acceptance requires actual native statistics login/WebSocket/session checks on
all six paths, exact route/socket/guard evidence, paired browser/scan overlap,
unchanged caps and sampled reserve, and both independent recovery outcomes.
On success as well as failure, restore the paired Caddy baseline/outgoing
inventories and exact Webmin loopback baseline. Controller loss can require
manual Caddy recovery despite the independent backend timer. A passing trial
qualifies only this bounded workload and does not leave browser ingress enabled.

The exact bundle requirement is
[server policy](../../../homelab-server-configs/AGENTS.md#definition-and-authorization)
and [Caddy's owner authorization contract](../../../homelab-server-configs/Caddy/AGENTS.md#authorization-cadence).
The former readiness inspection is consumed. Aaron separately approved this exact
candidate for one attempt on November 16; that attempt is now failed-consumed.

### Local evidence and retained failures

`caddy-qualification-final/result.json` records 16 offline owner scenarios passed,
network disabled and owned-container cleanup status zero. The original final
fixture is `/tmp/caddy-application-qualification-61uz6gap`; its durable copy retains
bytes and symlinks, with copy ownership normalized through the Podman namespace.
`authorization-ready-final.log`, `evidence-negative-final.log`,
`caddy-host-corrected.log`, `parent-syntax-final.log`, `client-preflight-final.log`,
`operator-tests-final.log` and `sealed-preflight.log` retain the passing checks.
The helper's six local cases cover verification without credentials/contact,
success/failure cleanup, replay rejection, existing-file preservation and drift.
These checks establish contracts and bindings, not Pi capacity or native UI success.

W-145 was found by the actual authorization gate: the temporary restoration
success row incorrectly expected rejection despite status zero. The generator
now derives success from the existing expected exit status. Preserve the original
16-case run and contradictory authorization result. My first rebinding placed the
fixture hash in the wrapper field; the rerun stopped at the definition check
before scenarios. Both correct field hashes were then bound and the complete
suite passed. Retain that failed run at
`/tmp/caddy-application-qualification-wfgllro8` and the original complete copy at
`caddy-qualification`. The earlier failed evidence copy is retained separately;
no consumed evidence was edited and no production defect is inferred from these
local preparation failures.

The fleet onboarding procedure now records final owner/input binding, separate
SSH-path key checks and untimed private credential handoff. Local qualification
sessions 51724, 49798, 78362, 3783 and 52613 completed successfully and are retired;
65551 failed before scenarios and is retired. `sessions.json` retains prior IDs.
No execution session is active. RESULT.md remains Partial with AC-013 pending.

### November 16 approval and private operator handoff (W-146)

Aaron approved the exact bundle, command and scope at the review section above
for one attempt. `approval.json` records both authorization identities and the
conversation reference without changing any sealed input. Local verification
using the sealed helper passed again; `approved-preflight.log` retains the result.
No attempt marker, parent result, browser workload or target contact exists.
Session 80351 completed with exit zero and is retired.

Run the approved command above in the workstation WSL/Ubuntu terminal, enter
ama's existing Webmin password only at its private prompt, and keep the terminal
open until completion. This operator launch supplies readiness for the automated
trial. Report only the terminal outcome; do not share the password or raw browser
contents. The one attempt includes both owner recovery paths and remains separate
from any permanent browser promotion or publication. If it stops or fails, retain
its evidence and do not repeat the command.

### November 16 trial failed and recovered (W-146/W-147/W-148)

The operator executed the approved command once. The parent exited 2; its Caddy
child exited 1. The original approval and one-attempt marker remain preserved.
No replay, extra live inspection or new workload ran during reconciliation.

Actual Pi admission accepted hostname, boot capture, installed controls and service
cgroups. Temporary backend apply completed. Both proxies reached Webmin over IPv4
and IPv6 with the expected route/socket sources and increasing target allow
counters. Both unlisted-workstation paths were denied with increasing family drop
counters. Those retained path results establish this trial's backend connectivity,
not native browser or combined capacity acceptance.

Caddy prepared, finalized and reconciled the primary candidate. Its first
application IPv4 probe, HTTPS port 443 on Node A for the Webmin name's
`session_login.cgi`, returned curl 28 after 5001 ms with zero bytes received and
HTTP 000. The expected HTTP status was 200. Readback succeeded. The exact stage is
known; the underlying timeout cause is not established. No transport exposure
command published the candidate to the secondary. The parent's readiness wait
reported that the Caddy owner had already ended; this is the consequence, not a
second independent timeout.

The existing recovery path contained the candidate and restored both Caddy nodes.
Decoded readbacks passed their byte-count and SHA-256 checks; each contains
restored/resumed receipts and identical original, restored and resumed outgoing
inventories. Both existing serving-family checks passed. The parent separately
ran Webmin restore, read its private state, passed `phase == restored`, then
stopped the recovery timer. The raw backend state remains in the host's retained
private trial directory; the local parent log records the completed assertions.
No further host contact was made to retrieve it.

The browser and scan were never launched, so ama credentials and actual browser
permissions were not tested. The private credential file is absent after helper
cleanup. Workload receipts are absent; `parent-owner-outcomes.json` has null
workload/finish results and a completed Caddy child. No active session remains.

Private evidence remains beneath
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-combined-review-0ve83yjr`:
`parent.log`, `parent.exit`, `inputs/evidence/`, `caddy-live-evidence/`,
`decoded-caddy-readbacks.json` and `terminal-summary.json`. The Caddy evidence was
copied unchanged from `/tmp/caddy-ssh-evidence-serving_health.2759y0`. Before any
lifecycle edit, all 236 manifest inputs were hash-verified and retained under
`executed-inputs/`, including original coverage and source identities. The
original manifest, approval, marker and qualification evidence remain intact.

Caddy now records `terminal-pending` / `failed-consumed`, clears the deployable
and coverage registries, and retains the exact executed operation/recipe/runtime
sources. Its sanitized terminal result and planned archive tag are in the owner
history. Deployment-window, successor and lifecycle policy checks passed. No
commit, tag or push occurred. W-147 owns local timeout diagnosis and W-148 owns
archive preparation; neither grants a retry or accepts AC-013.

### November 16 retained timeout reconciliation (W-147)

Local source/receipt comparison narrows what the failed trial proves. The direct
backend collector requested `/` over HTTP with the approved Host and forwarded
HTTPS header, requiring status 200 and the password form. The four requests took
about 1.74–1.82 seconds. The first Caddy request instead used trusted HTTPS on
Node A and requested `/session_login.cgi`. It had a three-second connect limit
and five-second total limit; the retained failure reports 5001 ms, zero received
bytes, curl 28 and HTTP 000. Direct backend success does not establish this
frontend TLS/request path or this different application endpoint.

The fragment's active health check also uses `/session_login.cgi`, with its own
three-second timeout; the upstream response-header limit is 60 seconds. These
are distinct controls, not proof that changing a deadline would solve the issue.
The retained evidence does not distinguish frontend connection/TLS delay,
backend selection/health state, or application response delay. It has no curl
phase timing, correlated Caddy request/error logs, backend request logs or
contemporaneous resource samples. Authentication and host capacity were not
exercised. Do not attribute the failure to either, reproduce speculative load,
or lengthen limits to manufacture acceptance.

W-147 remains open for the unknown cause. Before any future trial, the owner
procedure should align the backend and proxy probe path and retain bounded,
credential-safe transport phase timings, selected endpoint/status and correlated
proxy/backend diagnostics at failure, before restoration. This is a preparation
requirement for a separately reviewed change, not authority for contact now.
The consumed sources and receipts remain unchanged. No additional fixture or
live operation ran for this diagnosis.

### November 16 terminal archive prepared locally (W-148/W-149)

Private review root:
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-terminal-archive-review-oq66q1zm`.
It contains `files.txt`, `FILES.SHA256SUMS`, `files/`, `archive.patch`,
`diff-stat.txt`, `review.json`, exact commit/tag messages and `review-command.sh`.
The temporary index leaves the normal Git index empty. This is a historical
failed-attempt archive, not an accepted deployment or a successor.

- Owner repository: `Racerx323/homelab-server-configs`, branch `main`.
- Base commit: `3a27837f2a7dce023fc77154aff65aae7863106c`.
- Candidate tree: `5cf239d64909a26c632012bf0ca49407e8e3c252`.
- Exact selected paths: 61 files; `files.txt` SHA-256
  `d94a6bc3e3f6de41b7698147c5c06d49e53d96e912217a32c231db5ff6bbaa47`.
- File manifest SHA-256:
  `cb3d4967e4d5c94aa827b5e84ad18e44944271a747d8730e3f295748d727ffc9`.
- Patch SHA-256:
  `c8e3c1d7889c555ffa47f0ed28df555eb1300aa8a52e57d844919bb3cc2d0907`.
- Planned annotated tag:
  `caddy-webmin-first-host-trial-terminal-2026-11-16`.

The selection includes the consumed Caddy/Webmin/foundation implementation,
required hooks/instructions and sanitized terminal lifecycle records. It excludes
raw private receipts, credentials, the monitoring change record, both unrelated
inventory edits and the untracked `oom` file. Excluded-file hashes are retained;
no staging, commit, tag or network publication occurred. All 236 original inputs
remain separately preserved, including pre-terminal operation coverage.

The prepared command would verify the destination identity/visibility, unchanged
remote/local base, absent tag, exact selected bytes and candidate tree; then make
one commit, one annotated tag and an atomic push, followed by remote readback.
Its command and message hashes are in `review.json`. Do not run it under the
consumed trial approval. Separate exact archive approval is required by the Caddy
owner lifecycle; destination visibility has not been queried during local work.

Validation is explicit: source/snapshot hashes and core terminal lifecycle checks
pass. The real workspace documentation policy passes. The wider host-only
`current-repository-policies` run exited 1 because its documentation self-test
copies only Caddy into `/tmp`, leaving the linked sibling DNS owner document
absent (W-149). Preserve that failed check; this is not an all-green suite claim.
The initial default secret scan flagged five historical outer integrity hashes;
the same snapshot passed using the repository's existing exact-pin allowlist.
No new allowlist exception was added. The private publication helper's standalone
negated tag check was corrected to an explicit conditional after ShellCheck;
Bash syntax and ShellCheck then passed. No consumed source changed.

Session 78041 is retired with exit 1; its complete log is retained as
`webmin-combined-review-0ve83yjr/archive-owner-checks.log`. At this checkpoint W-149 remained unresolved; its subsequent disposition is
recorded below. The broader suite did not pass. No live work, retry, browser,
scan, permanent promotion or publication is authorized by this preparation.

### November 16 archive review and fixture disposition (W-148/W-149)

Aaron directed that no time be spent repairing the documentation fixture for
this deployment. W-149 is Deferred to the Caddy test owner, with this ledger as
its follow-up destination. The actual workspace documentation check passed;
the self-test's incomplete temporary repository layout does not explain the
production timeout or establish production acceptance. Retain its failure, but
remove fixture repair as a prerequisite to archiving this failed attempt. No
fixture, production implementation or test configuration was changed.

Local review rechecked all 61 selected source/snapshot hashes, file-list and
patch hashes, publication-command and message hashes, unchanged base commit,
empty normal index and exact temporary-index tree. All match the prepared
archive above. Scope, planned tag and excluded files remain unchanged. W-148 is
ready for separate archive authorization with the W-149 limitation disclosed;
this is not a claim that the broader test suite passed. Mandatory publication
hooks remain enabled; any hook rejection must be reported, not bypassed.

The exact publication command is retained in the private review root's
`review-command.sh`, SHA-256
`8b4a2fb0073b3c6af4b028ba20c5253ef0eb6becc3c15c33d4229527cd683d0a`.
Approval would cover only its one commit, annotated tag and atomic push of the
reviewed historical archive, plus destination/ref verification. It would not
cover neutral cleanup, source correction, a successor or live host work.
Caddy's [archive rule](../../../homelab-server-configs/Caddy/AGENTS.md#scope-and-archive)
requires preserving executed artifacts in an annotated pushed tag before removal;
the current request explicitly grants no publication authority. No commit, tag,
push, target contact, browser workload or retry occurred.

### November 16 approved terminal archive published (W-148)

Aaron approved the exact archive, command and scope for one commit, annotated
tag and push. The approved command exited 0 with mandatory hooks enabled; all
applicable hooks passed. The destination was verified as the public repository
`Racerx323/homelab-server-configs`. No private evidence was published.

- Commit: `66d8ae5bbaea05587bd30d2be01f2682b3d5066c`.
- Annotated tag: `caddy-webmin-first-host-trial-terminal-2026-11-16`.
- Tag object: `675e17873510f395f27bc32f193f7a27646186fb`.
- Committed tree matches approved tree `5cf239d64909a26c632012bf0ca49407e8e3c252`;
  its parent matches the reviewed base. Remote main and peeled tag both resolve
  to the commit above; the remote tag object matches locally.

Private `publication-approval.json`, `publication.log`, `publication.exit` and
`publication-result.json` in the archive review root retain authorization,
complete hook/push output and verification. Session 59826 is retired, exit 0.
The normal index is empty and excluded inventory edits/`oom` hashes are unchanged.
This record update remains local in the monitoring repository, outside the
approved owner archive. W-149's separately observed fixture failure is still
Deferred; passing publication hooks do not erase it.

W-148 is resolved. The stream remains terminal-pending until separately scoped
local cleanup; no consumed operation data was removed. W-147 and AC-013 remain
open. Publication approval is consumed; no further publication, cleanup, live
contact, retry or production promotion occurred.

### November 16 remaining-source publication authorization

Aaron requested committing and pushing all remaining changes. Scope review found
three owner repositories: monitoring documentation/change records, the server
inventory's retained accepted state, and DNS records/procedure/admission source
and tests. The empty untracked server `oom` file is excluded and remains untouched;
private evidence remains outside Git. This authorization covers source publication
only, with mandatory hooks and destination/ref verification. It does not authorize
Caddy neutral cleanup, target contact, retry or deployment. Exact selected paths,
base commits, destination visibility and command results are retained in
`.local-evidence/uptime-kuma/remaining-publication-nuxtpfm8`.

### November 16 neutral Caddy cleanup (W-150)

The published annotated archive and retained remote-verification receipt were
checked locally. Executed operation, recipe, outer runner and terminal-result
bytes matched the tag before editing. No remote query or live host contact was
needed. The archive and all private execution evidence remain unchanged.

The current operation is inactive (`action: none`), with current transaction and
state hashes. The outer runner's operation hash is rebound. The recipe is empty
apart from its header; the terminal manifest and lifecycle registration are
removed. The stream is `clean`, retains the latest archive tag, and has no
successor or coverage. Operation/recipe lifecycle classifications are restored
to workstation-only. The neutral transaction and accepted production/state
manifests retain their previous hashes; no runtime behavior was changed.

Private evidence: `.local-evidence/uptime-kuma/webmin-neutral-cleanup-tqg49dry`.
`cleanup.json` records archive provenance and protected hashes; `checks.json`
and individual logs record eight passing checks: deployment-window, successor,
lifecycle and actual-workspace documentation policies, Bash syntax, ShellCheck,
canonical shell formatting and whitespace. W-149's deferred fixture was not run.
Session 38621 exited 0 and is retired. Changes remain local and uncommitted.

W-147 diagnostic preparation is next; no new operation, retry, browser workload,
scan, deployment or publication is authorized. AC-013 remains pending.

### November 16 bounded diagnostic correction locally qualified (W-151)

The existing Webmin backend probe now requests `/session_login.cgi`, matching
Caddy's reviewed probe. It records the request start epoch, connect/header elapsed
times and fixed failure phase without retaining the body or exception message.
Its source/endpoint checks and timeout settings are unchanged.

Caddy retains the original HTTP status receipt plus numeric curl connection,
TLS, first-byte and total times and remote endpoint, including on failure. Start
and timing files use `.tsv` names carried by the existing readback. Before the
restoration trap runs, a failed application probe captures at most 32 Caddy
journal entries since its start, with a three-second command bound and 64 KiB
input bound. Only numeric timestamps and fixed categories survive filtering;
raw messages, headers, cookies and URLs are not retained. The original curl
failure remains authoritative even if diagnostic collection fails. No deadline
was increased and no probe retry was added.

The existing parent records one fixed numeric Webmin/Kuma cgroup snapshot before
native backend restoration, with a three-second command limit. This happens
AFTER the Caddy owner completes, so it is labelled and timestamped as later
resource evidence, not a simultaneous failure sample or capacity acceptance.
Missing evidence cannot suppress backend recovery. The fleet onboarding guide
now documents these repeatable diagnostic requirements and evidence limitations.

Local qualification decision: prove request alignment, safe evidence and failure/
recovery contracts, not named-host capacity. Existing tests were extended rather
than adding another framework. Shell probe cases cover success, curl 28, HTTP
failure, unavailable journal and private-text exclusion. Webmin tests cover
matching path, timeout phase, credential-safe output and connection cleanup.
The parent passes six scenarios, including failure of the added snapshot while
restoration still completes. Its original failures remain preserved.

Private evidence root:
`.local-evidence/uptime-kuma/webmin-diagnostic-local-it_tu3qy`.
`source-hashes.json` pins the changed source; `final-checks.json`,
`http-outside.log`, `parent-final.log` and `gitleaks.log` retain passing checks.
Shell collision policy, syntax, ShellCheck, canonical formatting, YAML,
neutral successor/window policy, documentation and whitespace checks pass.
The changed-file secret scan passed with existing owner configuration. The
vexp completion helper reported unavailable because its session root is not a
Git repository; it supplied no verification. Direct focused checks were used.

Initial HTTP and parent tests could not use local socket/worker facilities in
the filesystem sandbox. Those failed results remain retained; the same suites
passed outside the sandbox using localhost only. Sessions 69695, 29741, 58248
and 93051 are complete and retired. W-149's deferred fixture was not repaired or
rerun. Consumed bundles and archive remain untouched. The operation remains
inactive with current neutral hashes; no successor is defined or sealed.

W-147's historical timeout cause is still unknown. This correction improves the
next authorized attempt's evidence; it does not prove production behavior. No
live target contact, browser load, scan, retry, promotion or publication occurred.

### November 16 bounded diagnostic successor sealed for review (W-152/W-153)

This is a new diagnostic operation, `20261116-webmin-proxy-diagnostic`, using
existing Webmin parent and primary-first Caddy owner entrypoints. The published
failed attempt and every consumed input/receipt remain unchanged. W-147's
historical cause is unconfirmed. W-149 fixture repair remains Deferred.

Private bundle:
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-diagnostic-review-eb_83at5`.

- Parent manifest SHA-256 (230 input files):
  `9ddd690a5663a49f7c783464ab1c062388797038572ad19b8fd39684f5693637`.
- Exact Caddy outer SHA-256:
  `c51b010aacc2c2a2ca3d79a273a041cd85c61ad2ce7eaa250914a9928d56ffcc`.
- `review.json` records the command/scope; `launch.json` and
  `INPUT-METADATA.json` bind invocation, SSH inputs, file modes and symlinks.
- The operator helper requires no credential or browser runtime. It verifies the
  manifest and owner authorization gate, creates one exclusive `attempt.started`
  marker, then invokes the existing parent with private logs. Replays fail.

#### Exact bundle, command and scope for one diagnostic attempt

```bash
/usr/bin/python3 -I -B /home/aaron/code/.local-evidence/uptime-kuma/webmin-diagnostic-review-eb_83at5/operator.py --manifest-sha256 9ddd690a5663a49f7c783464ab1c062388797038572ad19b8fd39684f5693637 --run-approved-once
```

Requested authority: one temporary diagnostic on ama@10.1.3.75 and the existing
pi@10.1.0.53/10.1.0.54 Caddy pair. Admit current boot continuity and exact installed
configurations/controls. Temporarily apply the same guarded Webmin profile;
verify the four direct login paths with route/socket/counter evidence and the
two workstation denial paths. Activate and verify the selected Caddy fragment
on the primary, expose through managed replication only after acceptance, and
verify the same release on the secondary and reviewed shared endpoints.

On probe failure, retain bounded safe timing/journal evidence before Caddy's
restoration. On readiness success, the diagnostic-only parent sends finish
immediately. Retain the later numeric backend snapshot, verify paired Caddy
restoration/outgoing inventories and exact native Webmin loopback restoration,
then stop the owned recovery timer. Evidence failure cannot bypass recovery or
replace the original operation failure. Review both owner receipts even on
nonzero exit. Controller loss can require manual Caddy recovery; independent
backend recovery remains armed at 1800 seconds. The Caddy exposure safety bound
remains 660 seconds; it is not a request to wait that long after readiness.

No password, login, browser, WebSocket workload, scan, DNS, reboot, forced
failover, resource-limit change, unrelated route change, permanent promotion,
Git commit/tag/push or additional attempt is included. A passing diagnostic does
not accept AC-013. This candidate does not authorize itself: explicit approval
of this exact bundle/command/scope is required by the
[Caddy authorization rule](../../../homelab-server-configs/Caddy/AGENTS.md#authorization-cadence)
and the current no-live-work boundary. No operator attendance window is needed.

#### Local qualification and preparation findings

The existing offline Podman suite passed all 16 activation/replication/recovery
cases with network disabled and cleanup status zero. This validates the changed
owner path; no capacity conclusion is drawn. The original fixture remains at
`/tmp/caddy-application-qualification-krcbdzgb`; a durable namespace-safe copy is
under `caddy-qualification/`. The exact current owner graph passed
`--authorization-ready`, and `operator.py --verify-only` passed without contact.
Eight localhost parent scenarios include diagnostic success/failure with no
workload, unavailable snapshot evidence and unchanged recovery ordering. The
private helper tests cover verification-only, success, failure, replay and drift.
Playbook syntax, YAML, shell/collision/format, lifecycle and documentation checks
passed. No new platform fixture or W-149 repair was added.

Preparation corrected two local binding omissions before sealing: a defined
stream cannot retain an archive tag in its active registry field, and operation/
recipe lifecycle rows must be `defined-unexecuted`. The prior archive remains in
HISTORY and its published tag. Initial gate failures are retained; corrected gates
pass. The secret scan reported only the generated nonsecret correlation token in
two parent/resource bindings; its exact equality and purpose are recorded in
`secret-scan-disposition.json`. No credential value or new source allowlist was
introduced. The original parent test log was renamed `parent-tests.log` so the
future operation's exclusive `parent.log` remains absent.

Sessions 84643 (offline owner suite), 26559 (parent tests) and 70031 (evidence copy)
completed successfully and are retired. `sessions.json` retains their state.
No attempt marker exists; no target contact, browser, scan or publication occurred.

### November 16 diagnostic failed; owner restoration verified (W-153–W-156)

Aaron approved the exact bundle, command and scope at the review above for one
attempt. The operator verified the sealed inputs, recorded `approval.json` and
created its exclusive attempt marker. Parent session 32715 exited 2; the Caddy
child exited 1. Both are complete. This approval is consumed.

Private evidence remains under
`.local-evidence/uptime-kuma/webmin-diagnostic-review-eb_83at5`. All 230 manifest
inputs were verified and copied to `executed-inputs/` before terminal metadata
edits. `caddy-execution/` preserves the original controller evidence from
`/tmp/caddy-ssh-evidence-serving_health.P8GYpY`; three readback streams were decoded
only after verifying every recorded byte count and SHA-256. `terminal-summary.json`
records the observations; raw logs remain private.

The four direct `/session_login.cgi` probes passed with HTTP 200, matching route,
socket source and target guard counters. Total times were 2.36–2.54 seconds.
Both workstation denial checks passed. The first primary IPv4 HTTPS request
then failed with curl 28, HTTP 000 and zero response bytes. TCP connected in
0.000118 seconds, TLS completed at 0.052676 seconds, and no first byte arrived
before the 5.002007-second total. This narrows the current failure to after TLS;
it does not identify the upstream cause. Managed replication exposure, secondary
application acceptance, browser and scan workloads never started.

The bounded Caddy journal capture succeeded but retained 32 entries classified
`other`; it does not establish a request failure cause. The subsequent Pi snapshot,
after Caddy recovery and before backend restoration, reports Webmin peak
201326592 bytes (192 MiB), oom 3 and oom_kill 1. These counters lack a preceding
baseline or event timestamp. They cannot establish that the kill happened during
this request, caused this timeout or explains W-147. Kuma's snapshot reports
zero OOM events. No host-capacity acceptance follows.

Both Caddy restore/resume commands and readbacks passed, including the original
outbound inventories and existing dual-stack serving checks. The parent restored
Webmin, passed its exact restored-state assertion and stopped the owned timer.
This proves the scoped restoration checks, not all later monitor health.

Aaron supplied an Apprise alert first observed at `2026-11-16T17:53:23Z`, during
the Caddy child's recovery window (child ended at 17:53:24 UTC). It reports
`caddy-sync-health.service` failed, `lsyncd=unknown`, Caddy active and no VIP
movement. The owner resumes transport and checks baseline state, but does not
retain a subsequent successful replication-health cycle. A transient recovery
interaction is possible, not established. W-154 remains open; no suggested live
status/journal commands, reset-failed or restart were run.

Caddy is `terminal-pending` / `failed-consumed`; the operation, recipe and
implementation remain byte-identical to execution. The terminal manifest and
history retain sanitized outcomes/hashes, and successor/coverage registries are
cleared. Planned tag: `caddy-webmin-proxy-diagnostic-terminal-2026-11-16`.
Archive review/publication is separate. AC-013 remains pending, W-149 remains
Deferred, and no retry, live inspection, promotion or publication is authorized.

Terminal reconciliation checks passed: deployment-window, lifecycle, actual-workspace
documentation policy, terminal YAML, Markdown and whitespace. W-149 was not run.
The original operation, recipe, transaction and outer runner match their preserved
executed copies. No source behavior was changed after execution.

### November 16 retained-evidence reconciliation (W-154/W-155/W-157)

No target contact occurred. The existing recovery implementation deliberately
stops `caddy-lsyncd.service`, then restores both nodes and resumes transport.
It does not stop `caddy-sync-health.timer`. The health worker rejects either an
inactive sender or an invalid `/run/caddy-lsyncd/status` snapshot. The reported
11:53:23 AM CST alert falls within this recovery window. This establishes a
plausible monitor/recovery interaction, not the exact failed predicate or later
recovery. No health-worker journal or completed post-resume cycle was retained.
W-154 remains Open; the alert must not be dismissed as harmless or resolved.

The notifier's `is-active` expression appends `unknown` after nonzero exit, then
rejects the combined string. A pure local scalar reproduction maps `inactive`
with exit 3 to `unknown`. No systemctl, notification or network command was run.
Its `active -> failed` and no-VIP-movement text are static labels, not independent
transition measurements. W-157 records this information-loss defect separately;
no consumed source was changed. Current source explains the possible path but
does not establish which code or state produced the reported live event.

W-155's local evidence review is complete. Direct login probes were sequential;
the activated fragment defines health checks for both addresses every 30 seconds,
with a three-second health timeout, alongside proxied requests. Their actual
concurrency was not captured. TCP/TLS client timings exclude a client-side
connection/handshake timeout for this request, but do not measure the upstream
connection. The 32-entry journal projection contains only `other` categories;
raw messages cannot be reconstructed. The later OOM counters lack a preceding
baseline and event timestamp. None proves the current or historical root cause.
W-147 and AC-013 remain unresolved. No timeout increase, limit change or fixture
load test is justified by this evidence. If further live work is proposed later,
its missing evidence is the health-worker result after resume and request-window
upstream/Webmin timing with timestamped resource events, using existing owners.

Private `local-reconciliation.json` records source hashes, the scalar reproduction
and limitations beside the original diagnostic receipts.

### November 16 diagnostic terminal archive prepared (W-156)

The exact 12 changed Caddy/Webmin files are retained under
`.local-evidence/uptime-kuma/webmin-diagnostic-archive-review-650k0rmk/files/`.
`files.txt` enumerates scope; `FILES.SHA256SUMS`, `archive.patch`, commit/tag messages
and `review.json` bind the candidate. A separate temporary Git index produced the
reviewed tree; the normal index remains empty. No commit, tag or push occurred.
The executed operation, recipe, transaction and outer runner match the preserved
230-input bundle. Terminal metadata adds the local reconciliation limitations;
raw/private evidence and monitoring change records are excluded from this archive.

- Base commit: `c88c77b29b9c62c194545a421e37eaf6ad845d05`.
- Candidate tree: `63a1562bfc9b485bdb8e84a7da1707e5c579af4c`.
- File-manifest SHA-256: `f277c26d4f881c849f965e8c6b884d74e9e9d0ae3e985577840b059ef7d4aac6`.
- Patch SHA-256: `6c8f4c63a6c47f8ec5bfe64c7f2a25b7493989c10cbb45d78714498e51d69460`.
- Planned annotated tag: `caddy-webmin-proxy-diagnostic-terminal-2026-11-16`.
- Command SHA-256: `d7bc9fd7849f39f309ce88bfa2f18686858af9661e1942b2a70e501ee04060bf`.

#### Exact terminal archive command and scope for separate approval

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/webmin-diagnostic-archive-review-650k0rmk/review-command.sh
```

Requested scope: one commit of the exact 12-file tree, one annotated tag and one
atomic push to `Racerx323/homelab-server-configs` main plus that tag. The command
checks base/remote identity, remote visibility, absence of the tag, source hashes
and candidate tree before publication. Mandatory hooks remain enabled; changed
inputs or hook rejection stop progression. Remote branch/tag readback follows.
No live host work, cleanup of consumed inputs, successor, retry or promotion is
included. The repository's [archive rule](../../../homelab-server-configs/Caddy/AGENTS.md#scope-and-archive)
requires an annotated pushed terminal archive before consumed operation removal;
the current request grants preparation only, so publication needs explicit approval.

Nine focused checks passed: deployment window, lifecycle, actual-workspace owner
documentation, terminal YAML, history Markdown, whitespace, command Bash syntax,
ShellCheck and snapshot Gitleaks with the existing owner configuration. W-149's
known documentation fixture was not run or repaired. This is archive validation,
not production or browser acceptance. All checks completed; no session is active.

### November 16 archive publication stopped at commit hook (W-158)

Aaron approved the exact archive command at WORK.md:7485 for one commit, annotated
tag and push. Destination verification confirmed the intended GitHub repository.
The command staged the exact 12-file tree, then the mandatory test-lifecycle hook
rejected one extra generated file:
`Caddy/tests/__pycache__/application-onboarding-regression.cpython-312.pyc`.
No tracked source or inventory entry was missing. No commit, tag or push ran.

The generated bytecode is preserved privately as `blocking-generated-bytecode.pyc`
in the archive review root, then removed from the test directory. The unchanged
inventory check passes. The reviewed base, every source hash and candidate tree
still match; all 12 reviewed files remain staged. This is not W-149's deferred
fixture problem. No source behavior, fixture or inventory policy was changed.
`publication.log`, `publication.exit`, `publication-result.json` and the retired
session record retain the failed attempt. Session 36583 exited 1.

#### Exact archive publication continuation for separate approval

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/webmin-diagnostic-archive-review-650k0rmk/continue-publication.sh
```

Command SHA-256: `9f7a551ea8cf25b49bc9596a30f2acee90ac9673584dc7221fab80e8a1897a43`.

Scope remains the exact 12-file tree, one commit, annotated tag and atomic push
specified above. The continuation checks the already-staged tree instead of
requiring an empty index; it also requires no unstaged changes. All destination,
base, input, tag-absence, tree and mandatory-hook checks remain. Bash syntax and
ShellCheck pass. This command has not run. The approved scope explicitly said
hook rejection stops progression; separate approval is needed to continue.
No host work, replay, neutral cleanup or additional files are included.

### November 16 reported CI failures reconciled (W-159)

Both reported runs failed in `Caddy current-production contracts` / `Repository
policies`: run 43913820717 for c88c77b and run 43913190025 for 66d8ae5. GitHub job
logs are retained as `ci-job-133462505168.log` and `ci-job-133460271387.log` in the
archive review root. The initial `gh run view --log-failed` returned empty output;
the actual job logs were retrieved through the read-only jobs API.

Both report the same broken relative link from `Caddy/docs/APPLICATION_ONBOARDING.md`
to the DNS owner's `Unbound/docs/host-record-deployment.md`. The workflow does
check out the sibling DNS repository, but pins commit
`9ae13d0b03a4cec4124d411dd86b273462370129`, which lacks that file. Local Git object
inspection confirms the published DNS commit
`2ce710544c96479da2d79ab058a023646dd33c92` contains it. Updating that immutable
dependency requires checking the other DNS inputs consumed by these CI profiles;
file existence alone does not qualify the replacement pin.

This is not the generated-bytecode publication-hook issue (W-158), and not exactly
W-149's isolated self-test, which omits the sibling tree altogether. That deferred
self-test can remain a separate failure after the stale CI pin is corrected.
Neither failure establishes a production fault or explains the HTTPS timeout.
The staged archive, publication continuation and source files remain unchanged.
No workflow rerun, target contact or publication occurred. W-159 tracks the CI
correction separately; archive publication authority remains pending.

### November 16 diagnostic terminal archive published (W-156/W-158)

Aaron approved the prepared publication continuation. The staged tree, all source
and command hashes, base commit and destination were rechecked. The exact command
exited 0 with mandatory hooks enabled. The original failed attempt remains intact.

- Commit: `4e6b3d5a016e03d4ee2101d9fe745f7d63702de7`.
- Annotated tag: `caddy-webmin-proxy-diagnostic-terminal-2026-11-16`.
- Tag object: `37cfe4773890eccf826c9667d7e9c3d46d313898`.
- Tree: `63a1562bfc9b485bdb8e84a7da1707e5c579af4c`, exactly as reviewed.
- Destination: verified public repository `Racerx323/homelab-server-configs`.

Atomic push completed; remote main and peeled tag match the commit, and the remote
tag object matches locally. Server worktree and normal index are clean. Private
`continuation-approval.json`, `continuation-publication.log`, exit/result and
session records retain the evidence in the existing archive review directory.
Session 56626 exited 0 and is retired. No further execution session is active.

This publication preserves the consumed diagnostic; it does not resolve W-154,
W-147, W-157 or AC-013. W-159's stale CI dependency pin remains unchanged; passing
local hooks is not a claim that GitHub CI is green. Caddy remains terminal-pending
until local neutral reconciliation. No host contact, replay, cleanup, promotion
or additional publication occurred. This monitoring-record update remains local.

### November 16 DNS CI pin correction and qualification limits (W-159/W-160)

Aaron approved fixing and qualifying the dependency pin. The sole server-repository
change is `.github/workflows/validation.yml`: DNS revision 9ae13d0 is replaced
with published `2ce710544c96479da2d79ab058a023646dd33c92`. Workflow YAML, actionlint
and whitespace checks pass. No commit, push, workflow dispatch or live contact ran.

Private evidence: `.local-evidence/uptime-kuma/caddy-dns-pin-review-yilym96l`.
Local detached checkouts of server commit 4e6b3d5 and the exact old/new DNS commits
reproduce the original document failure with the old pin and pass the same
`operator-documentation-policy.sh --check` with the new pin. These checkouts use
committed files, not the working DNS tree. All three CI host profiles ran with
`--phase host --container never`; no capacity or container workload was used.

- Repository policies still fails inside W-149's isolated documentation self-test,
  whose temporary tree lacks the DNS sibling. The real checkout check now passes.
- Serving-health passes tracking lifecycle checks, then fails at the accepted-zone
  hash comparison (W-160). All other serving manifest hashes match. The remaining
  installation production-path and durable Apprise queue regressions were run
  separately and pass; this does not turn the failed profile green.
- Synchronization passes completely.

The earliest published commit adding the DNS procedure already changes the zone
source; selecting an older document-bearing commit does not preserve the old
accepted-zone hash. Do not change a production accepted identity merely to fit
new source. W-160 requires retained DNS acceptance/source reconciliation. W-149
remains explicitly deferred; this narrow pin approval did not repair that fixture
or disable its check. W-159's pin fix is implemented and its original symptom is
qualified, but end-to-end CI qualification remains incomplete.

Sessions 73312 (three profiles) and 5291 (remaining serving tests) completed and
are retired. Profile exit codes and logs remain retained, including both failures.
No consumed diagnostic input, Caddy lifecycle state or production file was changed.

### November 16 CI ownership reconciliation completed locally (W-149/W-159/W-160/W-161)

Aaron requested resolving the remaining CI scope/ownership. This authorizes the
local correction of W-149's test layout for this CI task; its earlier deferral
for archive preparation remains historical. The fixture now uses a private parent
containing sibling server/DNS directories and copies the real DNS owner document.
It explicitly removes that document and proves rejection before restoring it;
all prior negative tests remain. No fake document or disabled link check is used.

W-160 was stale Caddy bookkeeping, not proof of DNS drift. The November 12 DNS
terminal summary's complete evidence hash index verifies unchanged. Both node
apply outputs identify installed hash
`2df1be44a9ea39a35df1e75db16d72a4138b4ab3048fdc7bcf58bd7ff1a959dc`; the paired final
gate accepted. The published source at DNS 2ce7105 has hash
`4659dde5e93786ab144cb5a4f31b40de99faece7500303fcbde9ac65968158d9`, with the same
directives in preserved repository order as already reconciled under W-124.
Caddy's accepted-live registry, production inventory and serving contract now cite
the actual DNS-owner deployment. Source and deployed hashes remain separate;
serving validation compares each to the corresponding inventory field. This is
reconciliation of retained acceptance, not a new live observation or deployment.

The first local profile rerun correctly rejected the old state-hash binding.
To avoid rewriting a consumed operation, its operation/recipe/transaction/outer/
terminal bytes were checked against the published annotated diagnostic archive
at commit `4e6b3d5a016e03d4ee2101d9fe745f7d63702de7`. Local neutral cleanup then
removed the current terminal record, emptied the consumed recipe, inactivated
the operation and restored clean lifecycle classifications. State/outer/registry
hashes now bind the reconciled inventories. The archive and original receipts
remain unchanged; no runtime transaction behavior changed or successor exists.

Evidence is retained in
`.local-evidence/uptime-kuma/caddy-ci-reconciliation-p355i4oc`, including initial
failed profiles, final input hashes and final logs. The exact DNS checkout is
2ce7105; server inputs are the archived commit plus the recorded local changes.
All three CI host profiles pass with containers disabled: repository policies,
serving-health contracts and synchronization. Separate negative cases reject
wrong source and wrong installed zone hashes. Shell collision policy, Bash syntax,
ShellCheck, canonical formatting, workflow actionlint/YAML, Markdown and whitespace
checks pass. No host-capacity fixture or live contact was used.

Sessions 80284 (initial rerun) and 56823 (final profiles) completed and are retired;
individual failed profile statuses remain in their logs. Final negative/static
checks completed synchronously. Changes remain local and uncommitted. Hosted CI
has not run on them; publication remains separate. W-154/W-147/W-157 and AC-013
are unaffected and still unresolved.

### November 16 reconciliation publication review (W-162)

Reviewed scope: 15 paths in `homelab-server-configs` and three existing records in
`homelab-monitoring-observability` (PLAN, WORK, RESULT). Server changes cover the
pinned DNS dependency, documentation fixture layout, evidence-backed DNS inventory
identities, typed source/installed-hash validation and completed neutral cleanup.
The transaction implementation and production configurations are unchanged. The
monitoring records preserve the diagnostic attempt, archive publication, CI
findings, owner decisions and remaining acceptance gaps.

Private review: `.local-evidence/uptime-kuma/caddy-ci-publication-review-qj7dvmm0`.
Every server input still matches the final qualification hash list; no reason to
repeat unchanged profiles was found. The three host profiles and negative cases
remain passing evidence, not a hosted-CI result. Bases are server 4e6b3d5 and
monitoring 14cd5bd. Local remotes point to the corresponding Racerx323 repositories;
remote identity/visibility/ref verification remains part of authorized publication.

The server snapshot secret scan passes using existing owner configuration. The
monitoring scan reports one generic-api-key match on the documented parent
manifest digest `9ddd690a5663a49f7c783464ab1c062388797038572ad19b8fd39684f5693637`.
It was verified against the retained manifest bytes; it is not a credential.
The finding and disposition are preserved, with no suppression or policy change.
No raw private evidence, unrelated repository changes or `oom` file is selected.

Ready scope for a future explicit publication request: one ordinary commit and
push per owner repository, mandatory hooks enabled, then remote-ref and relevant
CI verification. No new tag is needed: the diagnostic terminal archive is already
published. This review does not authorize those writes, deployment, retries,
notification sends or changes to pending Webmin acceptance. No code changed
within this review; only this local record was updated. No sessions are active.

### November 16 approved reconciliation publication (W-162)

Aaron approved commit and push of all reviewed changes. Scope remains the 15
server paths and PLAN/WORK/RESULT monitoring records. Both origin destinations
were verified as the corresponding public Racerx323 repositories. Server inputs
still match local qualification; mandatory commit hooks remain enabled. No new
tag or live operation is included. Publication and hosted-CI results follow.

The reported Repository validation run 43926049277 for archived commit 4e6b3d5
failed on the same missing DNS owner-document link; that commit predates the
reviewed correction. This adds no new implementation defect.

Server publication completed at `722bc45a9f85bb3a50eb4d47fe33f9852562c7e0`;
remote main matches and the worktree is clean. Mandatory commit hooks passed.
Repository validation run 43933039649 passed, including all three Caddy profiles;
CodeQL workflow run 43933039034 passed. W-149/W-159/W-160 now have hosted
validation as well as local qualification. W-161 neutral cleanup is published.

This monitoring publication includes only PLAN, WORK and RESULT, with mandatory
hooks. Its resulting commit/ref and hosted-CI receipts are retained under
`.local-evidence/uptime-kuma/caddy-ci-publication-review-qj7dvmm0`; this record
does not predeclare their success. No deployment or new tag is included.

The monitoring commit hook initially rejected the previously reviewed manifest
digest as a generic API key because its adjacent label contained “nonsecret
input”. The label was clarified; the digest and consumed bundle are unchanged.
No scanner suppression or hook bypass was added.

### November 16 post-publication owner reconciliation (W-163)

Publication receipts confirm server 722bc45 and monitoring 7da98d0, matching
remote refs and passing repository validation/CodeQL. Current local work began
from clean worktrees. Publication did not change installed services or resolve
the retained operational uncertainty.

W-154 belongs to Caddy recovery/monitor acceptance. Current
`application_trial_resume` starts transport/reconciliation and validates existing
serving paths, but does not establish a completed later replication-health cycle.
Containment stops the sender while its health timer remains eligible to run. The
retained health-worker source hash matches current source. This supports a possible
interaction, not attribution of the November 16 alert. Do not silence the monitor
or mark the alert resolved on this basis. A future read-only scope should retain
the health unit result/journal, sender/status-snapshot state and completed natural
post-resume cycle, with installed identities and fresh operation continuity.
Historical journal retention may limit attribution even if current health passes.
No such inspection is defined, sealed or authorized here.

W-147 belongs to Webmin and Caddy request-path diagnosis. The retained successful
direct requests and failed primary HTTPS request do not establish equivalent
concurrency. Client handshake timing does not time the upstream connection; the
later cumulative OOM counters have no request-window baseline. The missing
evidence cannot be recovered by another fixture or by relabeling those counters.
A future target diagnostic needs request-correlated upstream/Webmin timing and
before/after resource-event evidence, retained before restoration. Keep current
timeouts, caps, reserve and recovery. Do not restart browser/scan qualification
until the failed basic proxy path is understood or a demonstrated correction is
qualified. AC-013 remains pending.

W-157 is a confirmed local notifier defect, independent of those unknown causes.
The existing `is-active` fallback concatenates valid nonactive stdout with
`unknown`, then rejects the combined string. Correct the existing notifier to
preserve bounded observed state and exit status separately. Report unknown on
missing/unsafe output; do not convert a failed command into a healthy result.
Replace static transition and VIP-movement assertions with explicitly unmeasured
context. Qualify active, inactive, failed, empty/error and malformed-output cases
through existing notification tests using a local capturing enqueue substitute;
no real notification send or service command is needed. Installed rollout and
inventory acceptance remain separately governed. No executable was edited or
notifier/test rerun was needed for this reconciliation; the retained scalar
reproduction remains the defect evidence.

This reconciliation stops repeated diagnosis from unchanged evidence. The next
local implementation is W-157; W-154 requires separately authorized observation,
and W-147 remains an unresolved target failure. No new operation, publication,
network contact or active execution session exists.

### November 16 notifier correction and qualification (W-157)

The existing Caddy notifier now retains bounded state values separately from the
exit status of each systemctl query. Nonactive states no longer concatenate with
`unknown`. Missing, malformed or multi-line states become unknown while their
query status remains visible. Unit-result query status is also retained. Prior
transition and VIP movement are explicitly unobserved; timing describes notification
observation rather than asserting the first occurrence.

The existing durable notification regression invokes the real producer with local
systemctl/logger substitutes and captures enqueue arguments. Active, inactive,
failed, empty/error, malformed, inconsistent active/nonzero and multi-line/error
cases pass. No real notification or service command ran. Source-candidate hashes
were updated in owner manifests; accepted installed identities were preserved.
Serving-health source validation now respects that existing identity distinction
for this notifier. No operation or successor was registered.

Local evidence: `.local-evidence/uptime-kuma/notifier-w157-local`. Durable Apprise,
current serving-health and repository-policy host profiles all passed; Bash syntax,
ShellCheck, canonical formatting and readonly/local collision checks passed.
These tests settle reporting correctness, not target health or capacity. Vexp
verification was unavailable because its session root was not a Git repository;
owner checks supplied validation. Session 17370 exited 0 and is retired.

### W-164 exact read-only inspection scope for review

Bundle: `.local-evidence/uptime-kuma/replication-health-review-qj3k31du`.
`INPUTS.SHA256SUMS` SHA-256:
`3c78548d4afb0cdda516e63cdd67b0009e5cb3a4aafc84f0ea99d50b5fe733f2`.
The manifest binds `inspect.sh`, `run.sh` and the retained known-hosts file.

Command, only after separate authorization:

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/replication-health-review-qj3k31du/run.sh
```

One SSH capture as `pi` on Node A `10.1.0.53`, using existing strict SSH host-key
verification and expected native hostname `j1-svpihole0`. Capture a fresh boot ID
at admission and require continuity throughout. Read installed health-worker and
notifier hashes, health service/timer definitions, selected Caddy/replication unit
properties and bounded status-file metadata/header. Observe three snapshots at
0/75/150 seconds without triggering a worker. Read at most 200 journal records
from November 16 17:50–18:00 UTC and 100 recent records for the health worker,
sender and reconciler. Preserve complete bounded output privately. Remote limit
220 seconds; controller limit 240 seconds plus five-second kill grace; output
file limit 4 MiB. An exclusive attempt directory prevents accidental replay.

Exclude Node B, the Pi/Webmin host, browser or scan workloads, notification sends,
configuration writes, reloads, starts, restarts, reset-failed, timer changes, DNS,
promotion and publication. Only local evidence files are written. Stop on wrong
host, changed boot, transport/command failure or bound exhaustion; retain status
and stderr. No recovery is needed for this read-only scope. SSH/sudo may create
normal audit records.

Capture success is not health acceptance. Independently review installed identity
and definition drift, sender state/restarts, snapshot freshness, health result
and a completed natural invocation after admission. Compare invocation and exit
timestamps across snapshots; an old successful result is insufficient. Missing
cycles/journal coverage or inconsistent state leave W-154 unresolved. A currently
healthy cycle does not prove the historical failure cause. Do not adopt observed
drift as accepted state. No timeout or policy relaxation follows from absent
evidence. Local Bash syntax and ShellCheck pass for both scripts; the collector
was not run and no fixture health result is claimed.

Repository `AGENTS.md` requires explicit authority for live inspection. This
prepared scope is reviewable but not authorized. No successor trial is proposed.

Working-tree secret scans: monitoring passed; server reported 18 matches confined
to the unselected `.vexp/manifest.json` index metadata, with none in changed
files. Raw redacted findings are retained under the W-157 evidence directory;
no global server scan pass or metadata disposition is claimed. No index metadata
is included in this change. Scan session 59441 completed and is retired.

### November 16 approved read-only Node A capture (W-164/W-154)

Aaron approved the exact W-164 scope. Manifest and input hashes passed before the
exclusive attempt began. Session 69890 exited 0; stderr is empty. Approval is
consumed. No service command other than scoped reads ran, and no worker was
triggered manually. All evidence remains under
`.local-evidence/uptime-kuma/replication-health-review-qj3k31du/attempt`;
`review-result.json` binds retained evidence hashes and the independent review.

The hostname matched `j1-svpihole0`, boot continuity passed, installed health-worker
and notifier hashes matched their accepted identities, and health service/timer
definitions exactly matched repository source with no drop-ins. The locally
corrected notifier is not installed.

Historical journal evidence now identifies the failing branch: at November 16
17:53:23.458 UTC the worker reported the sender was not active and stable and
exited 1. Systemd recorded the sender started at 17:53:23.911 UTC, approximately
0.45 seconds later; sender startup synchronization finished at 17:53:26.176.
The next scheduled health cycle completed successfully at 17:54:26.674 UTC.
This confirms the recovery/health-check overlap underlying the reported alert.
It does not prove a specific individual predicate within sender validation or
explain the Webmin request timeout.

Observation ran from 19:09:41 to 19:12:11 UTC (13:09:41–13:12:11 CST). Two new
natural cycles completed at 19:10:39 and 19:11:51 UTC with distinct invocation IDs,
advancing exit timestamps, Result=success and ExecMainStatus=0. Sender PID 870438
remained active/running with NRestarts=0; Caddy stayed active/running and the
health timer/reconcile path stayed active/waiting. The oneshot health worker's
inactive/dead state between successful cycles is expected. W-154 is resolved
for alert diagnosis and observed subsequent monitor health.

The status report remained unchanged at its 17:53:36 timestamp through all three
snapshots. The installed worker validates file safety/structure, not age; passing
cycles cannot establish fresh replication data or a new successful transfer.
Do not infer stalled replication from the unchanged file alone. W-165 tracks
this acceptance limitation alongside the demonstrated recovery/monitor overlap
for local owner reconciliation. Node B and the Pi were not contacted.

W-147 and AC-013 remain unresolved. The capture grants no corrective rollout,
retry, new inspection, promotion or publication authority. No recovery was needed
for this read-only operation. All execution sessions are complete and retired.

### November 16 recovery/monitor boundary reconciliation (W-165)

The existing recovery has two different outcomes: restoring the accepted release
and transport, then demonstrating that the scheduled monitor has accepted that
resumed state. W-164 proves that these can be separated by a transient check
failure. The shared onboarding procedure now states the future acceptance
boundary explicitly; the current executable still lacks that post-resume wait.
W-166 tracks the required integration rather than claiming it is implemented.

Keep timer/failure reporting active. Retain containment-window failures and their
chronology; do not mask the signal. A future bounded owner operation must retain
pre-resume invocation/exit baselines and require a successful natural invocation
starting after transport resume on each affected node, with unchanged boot,
stable sender PID/restarts and existing restoration checks. Fit the observation
within the approved total recovery deadline. Missing/failed cycles remain an
acceptance failure even if configuration restoration passed; preserve those
distinct results and avoid additional starts, rollback or forced checks merely
to obtain green status. Actual restoration failure retains existing containment.

Repository package intent is Lsyncd 2.2.3-1. Upstream release-2.2.3 `lsyncd.lua`
lines 4067–4166 (`StatusFile`) and 4332–4404 (`runner.cycle`) show throttled status
writes from the event loop, not a guaranteed heartbeat. Source reference:
`https://raw.githubusercontent.com/lsyncd/lsyncd/release-2.2.3/lsyncd.lua`.
The November 16 capture did not identify the installed package/binary version;
this source review explains why mtime alone is not a sound health requirement,
not proof of every detail of that installed build. No fixture or host retry is
needed to establish the scope distinction.

Consequently, the unchanged report is neither proof of stopped replication nor
proof of a recent successful transfer. Do not add a freshness threshold or touch
the file. Continue using actual release/receipt verification for transfer
acceptance. W-154 stays resolved on its observed monitor results; W-147 remains
independent and unexplained. No service policy or executable changed this turn.

W-166 local qualification should exercise existing recovery entrypoints with
controlled monitor results, not model Pi capacity or add another deployment
framework. Once that boundary is implemented, future W-147 preparation still
needs request-window upstream/Webmin timing and resource-event deltas under
unchanged caps/timeouts. Neither preparation nor these records authorizes live
work. Consumed bundles and W-164 receipts remain unchanged.

### November 16 W-166 implementation qualification in progress

The existing transaction now records pre-resume health identity and a per-node
monotonic resume cutoff, then observes a completed successful natural cycle within
150 seconds of resume. The outer resumes both nodes before observation; monitor
failure preserves restored service, attempts both readbacks and returns incomplete
acceptance without replaying restoration. No new owner operation is defined.

Host contract tests passed fresh success, failed/missing cycles, stale success,
boot change, sender restart, inactive timer, late completion and command error.
The actual pair-coordinator function test proves monitor failure still reads both
nodes and performs containment only once. Repository policies pass.

The first offline integrated run preserved at
`/tmp/caddy-application-qualification-811vv63f` passed all ten ordinary cases but
failed trial-success: its systemctl timer substitute returned status zero with
empty output. The real observer correctly rejected empty state. The adapter was
corrected to return the native active-state text; no production check was weakened.
A changed-input rerun is in progress. This fixture corrects a command contract,
not host capacity. Initial runner session 85478 exited 1; owner-container cleanup
completed. Sessions 12776 and 48042 exited 0. No live work occurred.

### November 16 W-166 final local qualification

Source changes remain in the existing transaction, outer runner and application
regression. Resume retains the old invocation/exit timestamp, then records
monotonic resume time and sender PID/restart baseline. A new trial-monitor phase
requires a different completed invocation starting after resume, success/exit 0,
unchanged boot, active timer and stable active/running sender. Completion must
fall within 150 seconds of that node's resume. The second node's deadline is
not renewed when the coordinator reaches it. Each systemctl query is capped at
five seconds; failed queries and the last samples retain stdout/stderr/status.

Both transports resume before either observation. Regardless of monitor failure,
the coordinator attempts the other node and both readbacks, reports restoration
passed/monitor incomplete and returns 125 without recontaining or replaying
restoration. A failure of restoration itself still follows existing containment.
No health worker is manually invoked; no timer, failure-reporting or status-file
age policy changed. Parent limits remain 1200 seconds for the child and 900
seconds for terminal waiting; the next exact candidate must account for all
phases and these anchored observation windows within those bounds. This record
does not claim a future candidate's budget has been sealed.

The corrected offline run `/tmp/caddy-application-qualification-jzljxxus` passed
all 16 application cases using the actual producer/recovery entrypoints, native
Caddy and controlled SSH/systemd scheduling substitutes. Network was disabled;
image identity and inputs are retained in `result.json`. Nine focused observer
cases plus the real pair-coordinator failure case pass on the host. The initial
failed fixture remains at `/tmp/caddy-application-qualification-811vv63f`; its
empty active-state output was corrected without weakening the production check.
No fixture measurement is used to accept Pi capacity.

Repository-policy profile, definition/payload checks, Bash/ShellCheck, canonical
formatting, readonly/local collision checks, Markdown and whitespace pass. Clean
stream/successor policy passes after refreshing the inactive operation's
transaction hash and outer bindings. Local source identities and logs are in
`.local-evidence/uptime-kuma/notifier-w157-local`, including
`w166-final-inputs.json`. Consumed archives and accepted installed identities are
unchanged. No new operation is defined.

Sessions 12776, 48042, 69234 and corrected native session 15663 exited 0; initial
native session 85478 exited 1. Both owned qualification containers were removed
and all sessions are retired. W-166 is locally resolved. W-147/AC-013 still need
separately reviewed target evidence; no further inspection or retry is authorized.

### November 16 W-167 diagnostic preparation and qualification

The existing Caddy route probe now generates a separate random request ID per
address-family request and retains it with client timing. The proposed Webmin
fragment logs only marked requests, removes request/response headers and user
identity before encoding, and appends native upstream address, duration and
header-latency fields. The existing bounded journal projection retains only
matching request IDs, numeric timing/status and address-shaped upstream values;
unavailable metrics remain null. Other entries retain only safe categories.
No global debug logging, body logging, private login or Webmin code patch is used.

The existing Webmin collector now supports a root-private, exclusive-create
observation in the trial directory: one baseline, one-second samples, a 300-second
maximum and a one-MiB output bound. Samples retain epoch/monotonic time, boot and
cgroup identity, numeric memory files and interval event-counter deltas. Replaced
cgroups, changed boot, missing/malformed counters or decreasing counters are not
reported as comparable. A delta identifies an interval, not the request that
caused it. The parent starts it only for diagnostic-only work before Caddy and
requires a usable baseline; it stops/collects the observer and continues native
restoration even when collection fails. Independent resource status is retained.
Existing service limits, request deadlines and parent recovery limits are unchanged.

Focused qualification used the actual offline Caddy binary and local HTTP server:
marked success and client cancellation produced correlated access records,
ordinary requests were omitted, upstream timing was populated on success and
credential canaries were excluded. Counter increment/reset/identity, private
file, stop/deadline and no-replay cases pass. The actual parent Ansible flow passes
all eight isolated owner-adapter scenarios; this proves sequencing, not live
SSH/recovery or Pi capacity. Actual probe/journal projection and W-166 observer
contract tests pass, as do the application-onboarding host profile, clean-stream
policy, shell syntax/lint/format and readonly/local collision checks.

Evidence is under `.local-evidence/uptime-kuma/diagnostic-w167-local`.
An initial HTTP test could not open sandbox sockets; the Ansible sandbox run
could not start its local RPC server. Native qualification first found malformed
fixture global-option syntax, then a readiness failure with no startup log. The
fixture now validates adaptation explicitly and reports child exit/log evidence;
the focused native case and final complete ten-test run passed. These local
failures do not explain the historical production timeout. No target-capacity
fixture was run. All owned containers exited and were removed.

W-168 is a sealing prerequisite, not a reason to retry: transport keepalives are
not a whole-command deadline, and cross-host timestamps need measured uncertainty.
The new sampler cannot cover requests after its cutoff. Retain W-166's natural
monitor observation inside the existing parent budget; do not manufacture a
budget by adding timeout constants or use fixture elapsed time as a target bound.
The clean inactive operation hashes were refreshed; installed identities and all
consumed bundles remain unchanged. No successor or live command is proposed.

Final local checks: ten diagnostic tests passed in the offline native Caddy image;
six backend-profile tests and all eight parent-flow scenarios passed. Markdown and
whitespace checks pass. The source-only secrets scan passes with the existing
repository configuration; an initial default-config scan reported five unchanged
historical hash lines in Caddy/HISTORY.md, with no new credential finding. No
allowlist was changed. Source hashes and bounded logs are retained in
`diagnostic-w167-local/source-inputs.json`. All local execution sessions ended.

### November 16 W-168 aggregate deadline and correlation qualification

The existing Caddy runner selects diagnostic bounds only from the hash-bound
`application_diagnostic_seconds=240` input, together with the existing trial
backstop. The parent requires that selection before backend mutation. One
240-second forward deadline starts before transport; recovery changes phase but
keeps the original aggregate cutoff at 840 seconds. Remote process groups and
local SSH are separately bounded, and uploads use the same remaining-time gate.
Ordinary calls have a 90-second cap, monitor calls 170; the remaining phase time
can reduce either cap, with 20 seconds reserved for termination and transport.
Expired forward work cannot borrow recovery time or renew the deadline.

W-166 containment/restoration, both-node resume, natural monitor observation and
readback remain in the existing recovery path. A timeout alone does not prove a
systemd job stopped or a remote mutation ended. Missing recovery evidence or an
exhausted reserve remains incomplete/manual intervention. No replay, monitor
suppression or service-limit change was added. Parent child timeout stays 1200
seconds; the terminal setting is 900 polling retries, not a precise wall-clock
timer. The 840-second owner budget avoids treating that retry count as a bound.

Clock capture reuses the existing handoff helper with three exact reviewed SSH
prefixes in a private, manifest-bound diagnostic specification. Each fixed
read-only query has a five-second limit. Requests and target samples use Linux
boottime, as do clock replies; controller round-trip bounds are retained before
sampling and after collection. This avoids mixing CLOCK_MONOTONIC with
/proc/uptime after a host has suspended. Historical boot IDs are not prerequisites.

The Caddy transaction appends every probe's ID, node, boot and start/end times to
its existing evidence. The handoff helper checks encoded readback lengths and
SHA-256 values, rejects changed duplicate IDs, and joins the retained request
index to sampled event intervals. It rejects missing brackets, boot changes,
excessive measured uncertainty, sample gaps/resets and requests outside sampler
coverage. Output is an estimated envelope of measured pre/post offsets, with
intervening drift explicitly unobserved; possible event overlap is not causal
attribution. Failed clock/correlation checks retain failure information and still
run mandatory backend restoration. Private fetched sample files are mode 0600.

Qualification is retained under
`.local-evidence/uptime-kuma/diagnostic-w168-local`. Real timeout and remote-shell
serialization tests cover a responsive stalled command, expired forward and
recovery budgets, recovery reserve availability and bounded uploads. Existing
probe and monitor contracts pass. Eleven handoff/workload tests cover clock
capture, uncertainty, missing/out-of-window/reset evidence and readback tampering.
Two focused collector tests pass. The real Ansible block/always/final acceptance
flow passes eleven isolated scenarios, including pre-clock, post-clock and
correlation failures; these do not become accepted after successful restoration.

The offline owner suite at `/tmp/caddy-application-qualification-zdrouy9o`
passes all 16 scenarios with actual native Caddy/release machinery; diagnostic
bounds are selected for its trial cases. Image identity, source hashes and
cleanup are in its result.json. The actual retained native readbacks also pass
the handoff parser: successful paired requests and a failed primary request are
indexed and deduplicated from hash-verified producer output. No fixture result
is used as Pi capacity acceptance. Shell lint/format, collision policy, owner
profile and clean inactive-stream checks pass. Neutral source pins are updated;
consumed inputs, accepted installed hashes and previous evidence are preserved.

All local processes and owned containers completed; execution sessions are
retired. W-167/W-168 are locally resolved. W-147 attribution and AC-013 still
require a separately prepared and authorized actual-host diagnostic. No new
operation is defined or sealed, and no live work or publication occurred.

Final W-168 documentation/whitespace and configured source-only secrets checks
passed. Exact changed-source and qualification-log hashes are retained in
`diagnostic-w168-local/source-inputs.json`. Vexp completion verification was
unavailable from the non-repository parent workspace; the owner qualification
above supplies the executable checks. No execution sessions remain active.

### November 16 W-169 timing-diagnostic candidate sealed for review

Operation `20261116-webmin-proxy-timing-diagnostic` is defined and unexecuted.
It uses the existing Webmin parent and Caddy primary-first owner, with the current
W-167/W-168 sources and W-166 recovery observation. The archived prior diagnostic
and every consumed input/receipt remain unchanged. W-147's cause is unconfirmed;
AC-013 remains pending. W-154 is resolved and W-157 is not installed.

Private review directory:
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-diagnostic-review-oyi4vl5g`.

- Parent manifest SHA-256 (236 inputs):
  `63f873cb63bacacfd2c5d05d2585ff6483b8476ff8eacbe21291d05c989123d7`.
- Caddy outer SHA-256:
  `c5dbd379752cc1d1f4721c1dad5db079201022dbabd62f5f6c397e62e9e7321f`.
- `INPUTS.SHA256SUMS`, `INPUT-METADATA.json` and `launch.json` bind exact inputs,
  permissions, runtime links, SSH settings and command/environment. Private
  `sealed-inputs/` retains their reviewed bytes; drift stops launch.
- `review.json` describes the scope. No `attempt.started`, live evidence or
  approval record exists. The helper creates its exclusive attempt marker only
  for an explicitly authorized execution; replays fail.

#### Exact bundle, command and scope for one timing-diagnostic attempt

```bash
/usr/bin/python3 -I -B /home/aaron/code/.local-evidence/uptime-kuma/webmin-diagnostic-review-oyi4vl5g/operator.py --manifest-sha256 63f873cb63bacacfd2c5d05d2585ff6483b8476ff8eacbe21291d05c989123d7 --run-approved-once
```

Requested authority covers ama@10.1.3.75 and pi@10.1.0.53/10.1.0.54, through the
existing parent. Admit current boot continuity and the exact retained native
hostname, configurations, installed units/drop-ins, service limits and Caddy
release/tool identities. Recheck real route/socket sources against the guarded
allowlist. Temporarily expose the same Webmin profile; verify four direct
`/session_login.cgi` paths and dual-stack workstation denial. Preserve the
existing account, application data, Kuma service and unrelated routes/TLS.

Capture fixed, bounded read-only clocks on all three hosts before sampling.
Start one 300-second numeric Pi sampler, then stage the exact Caddy payload and
activate/verify the proposed Webmin fragment on the primary. Only primary
acceptance permits managed replication to the secondary; verify that node and
shared paths through the owner. Mark each request, retain upstream/client timing,
request indices and bounded safe failure logs before recovery. On successful
readiness the diagnostic parent sends finish immediately; it starts no browser
or scan. Post-operation clocks and resource coverage remain independently checked.
Requests outside retained coverage, missing deltas or excessive clock uncertainty
cannot pass; event overlap is not proof that a request caused an OOM.

Caddy forward work has one 240-second budget. Restoration, both-node resume,
fresh natural monitor-cycle acceptance and readback use the remaining aggregate
840-second owner budget, without renewal. The existing 1200-second child limit,
900 polling retries, 660-second exposure backstop and independent 1800-second
backend recovery timer are unchanged. Native Webmin loopback restoration runs
even when Caddy or correlation fails. Review both owner receipts on any exit.
Exhausted recovery time or missing proof is incomplete/manual intervention;
a timeout does not establish remote quiescence. Controller loss may require
manual Caddy recovery. These bounds do not promise recovery under every stall.

No password/login, browser/WebSocket workload, needrestart scan, account/ACL
change, DNS, reboot, forced failover, resource-limit change, notifier installation,
synthetic notification, unrelated route/radio change, permanent promotion,
commit/tag/push or extra attempt is included. Existing natural monitoring may
emit its own alerts. A passing diagnostic does not accept AC-013 or host capacity.
No operator attendance window is required. Execute only after explicit approval
of this exact bundle, command and scope under the
[Caddy authorization rule](../../../homelab-server-configs/Caddy/AGENTS.md#authorization-cadence).

#### Local qualification and retained limitations

The exact defined graph passed all 16 native offline Caddy owner cases, including
primary-first success/failure, restoration, budgeted trial transport and natural
monitor observation. Its original evidence remains at
`/tmp/caddy-application-qualification-_x_tn8ne`; the byte-preserving private copy
is `caddy-qualification/`, with native cleanup status zero. Authorization-ready
verification rederived decisions from that retained producer evidence.

W-168 parent/resource/clock input hashes remain unchanged; their existing eleven
parent scenarios, eleven helper/workload cases and focused collector/timeout
checks are reused through `reused-qualification.json`, rather than repeated to
claim host capacity. Current rendered profile bytes match the owner renderer and
retained baseline. Definition, lifecycle/window, syntax, shell formatting,
operator verification/replay/drift tests and the sealed no-contact preflight pass.
No runtime implementation was changed during candidate preparation.

Preparation retained local tooling failures: an incorrect lifecycle-test
filename, corrected to the existing owner policy; and ordinary access to
namespace-owned fixture directories, resolved by a scoped `podman unshare`
byte-preserving copy. The final collision check also rejected an unsupported
flag; it passed with explicit source paths. None contacted a target or reran a consumed
operation. Whole-working-tree scans found only 22 generated `.vexp` file-hash
values; the separate candidate source scan found its two identical nonsecret
correlation-token bindings. Exact dispositions are retained privately; no
credential finding or new allowlist was introduced.

All local sessions are complete and retired. No target contact, browser load,
scan, live attempt or publication occurred. The candidate is sealed for review,
not authorized. Changes remain uncommitted.

Final candidate Markdown/whitespace, owner documentation and collision checks
pass; sealed verify-only passed again with no target contact. Vexp completion
verification remains unavailable from the non-repository parent workspace; the
actual owner gates above provide qualification. All session IDs are retired.

### November 16 W-170 execution failed; recovery and subsequent monitor health verified

Aaron approved the exact W-169 command once. The operator verified the seal and
created one attempt marker; parent exit 2 and Caddy exit 1 are retained beneath
`webmin-diagnostic-review-oyi4vl5g`. Session 11496 is complete and retired. No
browser, scan, password, DNS, permanent promotion or publication was attempted.

All four direct backend login-page/source/counter checks passed with HTTP 200 in
2.304–2.369 seconds, followed by both workstation-denial checks. The primary
Caddy IPv4 request completed TCP in 0.000120 seconds and TLS in 0.048945 seconds,
but received no first byte before its unchanged 5.001341-second client timeout
(curl 28, client status 000). The marked Caddy access record reports 499 after
4.954312 seconds and the expected IPv4 backend; upstream latency/duration fields
are absent. This records cancellation, not a demonstrated backend root cause.
The proposed release was not exposed to the secondary for acceptance.

Both Caddy original selections/outbound inventories were independently verified
restored through hash-checked readbacks. Both nodes resumed, then each completed
a distinct successful natural health-monitor invocation within its 150-second
window: 66.719 seconds after Node A resume and 40.997 seconds after Node B resume.
Timers were active; sender PIDs/restart counts were stable. The Caddy child ended
in 84.614 seconds. Native Webmin restoration and restored-state assertion passed;
its independent recovery timer was stopped only afterward.

Aaron's new replication notification at **2026-11-16 21:15:23 UTC** falls during
this operation. W-172 records the alert and the later independently accepted
health above. Its exact failing predicate was not captured. The installed
notifier still has W-157's known reporting defect: its transition/VIP assertions
and unknown sender label do not establish those facts. No reset, restart, fresh
inspection or alert-suppression action followed.

#### Original correlation failure and separate local reconstruction

The Pi sampler exited normally after 96 seconds, retaining 96 readings plus a
terminal record. Pre/post clock capture passed. The parent correlation failed
with `owner_evidence_directory`: the owner emits that discovery marker after
`run_live`, so its nonzero exit bypasses the marker. W-171 tracks this actual
failed-path producer/consumer gap. Successful restoration did not turn it into
passing diagnostic acceptance.

Local reconciliation independently associated
`/tmp/caddy-ssh-evidence-serving_health.MvuUlJ` with this attempt through its exact
payload recipe/fragment/publisher hashes and the target revision present in the
parent log. `owner-evidence-binding.json` records that association. All three
readback streams were decoded with filename, byte-length and SHA-256 validation;
the original directory was copied to private `owner-execution/`.

The recovered request index and the unchanged clock/resource verifier produced
`supplemental-local-coverage.json`, without any target contact or synthetic log
marker. The original failed receipt remains unchanged. The supplementary
estimated request interval has 0.422 seconds of clock uncertainty. Possibly
overlapping Webmin intervals contain 2,083 memory.high increments and zero
observed memory.max, oom or oom_kill increments. Later samples show unavailable/
reset Webmin counters around 21:15:31–33 UTC. Those gaps cannot identify an OOM
or establish causation. W-147 remains unresolved; retained evidence now supports
local review of pressure and the active proxy/health-request pattern before
proposing further live diagnosis. No capacity limit was weakened.

The exact 236 reviewed input bytes were verified before terminal registry
updates. Their snapshots, original/supplemental receipts and safe summary are
retained privately. The operation, recipe and executed implementations remain
unchanged; terminal registry/coverage changes prevent reuse. Caddy is
`terminal-pending` with planned archive
`caddy-webmin-proxy-timing-diagnostic-terminal-2026-11-16`. W-173 owns its separate
archive review; no commit, tag or push is authorized. W-147/AC-013 remain pending.

### November 16 narrowed request diagnosis agreed (W-174)

Aaron approved the narrow diagnostic recommendation and asked whether address
families should be checked serially. Diagnostic requests will be sequential,
starting with primary Node A and the Pi's IPv4 address. A later IPv6 comparison
requires an explicit reason and scope; a passing IPv4 request does not establish
IPv6 or fleet acceptance. No custom production health scheduler is selected.

Caddy's official reverse_proxy documentation (retrieved through Context7,
/caddyserver/website on November 16) describes background active checks and
per-handler results; it documents no address-family serialization control.
This does not establish the installed worker's exact concurrency or explain the
historical timeout. Existing configured dual-address checks are a plausible
source of overlapping work, requiring target evidence. The new candidate uses
one upstream for isolation; any pass applies only to that changed diagnostic
configuration and cannot establish that removing IPv6 fixed the original fault.

The accepted diagnostic design is in PLAN.md. Existing raw evidence and executed
sources remain unchanged. The consumed stream must be archived before editing
its owner entrypoints. No additional fixture load campaign is needed: qualify
only request equivalence, bounded safe evidence, failure handoff and recovery.
The private archive preparation first stopped on the expected terminal stream
metadata difference; no source edit or commit occurred. Final preparation
explicitly distinguishes terminal metadata from 18 unchanged executed sources.

### November 16 W-173 terminal archive prepared for review

The exact 23 changed Caddy/Webmin files are copied under
`.local-evidence/uptime-kuma/webmin-timing-archive-review-fs4xr71p/files/`.
`files.txt`, `FILES.SHA256SUMS`, `archive.patch` and `review.json` bind this scope.
A private temporary Git index produced the reviewed tree; the normal index is
unchanged. Eighteen changed executed sources match the consumed seal. The other
five files are history, onboarding documentation, lifecycle/stream metadata and
the sanitized terminal result. The archive includes the locally qualified W-157
notifier correction as source only; it is not an installation or acceptance claim.
Monitoring records, raw private evidence and the ignored `oom` file are excluded.

- Base commit: `722bc45a9f85bb3a50eb4d47fe33f9852562c7e0`.
- Candidate tree: `c2a09075fed6b01a9f132b3d01739cffd15cbf1e`.
- File-manifest SHA-256: `5e70c44607ffef9720c36d5ee296a1b0d15114ab73cce0601e3cb754de82f2f1`.
- Patch SHA-256: `aec70bb417c4472d69d254776a80f1e245fcb1e7873d6b70451248dc7e47ba61`.
- Command SHA-256: `ddcce8728e54c40c167aa5ed2d77af1f2e2071693a168462df9316ed81e811f9`.
- Planned annotated tag: `caddy-webmin-proxy-timing-diagnostic-terminal-2026-11-16`.

#### Exact archive command and scope for separate approval

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/webmin-timing-archive-review-fs4xr71p/review-command.sh
```

Requested authority: one commit of the exact 23-file tree, one annotated tag,
and one atomic push of main plus that tag to `Racerx323/homelab-server-configs`.
The reused publication command checks destination/visibility, base, remote ref,
tag absence, file hashes and candidate tree; mandatory commit hooks remain
active. Changed inputs or hook rejection stop publication. Remote ref readback
follows. No host contact, source cleanup, successor execution or promotion is
included. Aaron's approval to pursue the diagnostic does not include publication.

[Caddy's archive rule](../../../homelab-server-configs/Caddy/docs/DEPLOYMENT_LIFECYCLE.md#close-an-operation)
requires the terminal commit and pushed annotated tag before consumed inputs are
removed. This is the remaining prerequisite to in-place diagnostic implementation,
not a request to repeat the broad fixture trial.

Eight focused archive checks passed: deployment window, lifecycle, successor
policy, whitespace, command syntax, ShellCheck, history Markdown and snapshot
Gitleaks. Evidence is in `qualification.json` and adjacent logs. No commit, tag,
push, live contact or browser/scan workload ran; no execution session is active.

### November 16 W-173 terminal archive published and verified

Aaron approved the exact WORK.md:8357 command for one commit, annotated tag and
push. All six reviewed artifact/message hashes, all 23 source hashes, the base
and empty normal index matched before execution. The command ran once with
mandatory hooks enabled and exited 0. Destination verification confirmed the
public `Racerx323/homelab-server-configs` repository.

- Commit: `a6491d0795e4493e000f3afe81be09d01514fffd`.
- Tree: `c2a09075fed6b01a9f132b3d01739cffd15cbf1e` (the reviewed tree).
- Annotated tag: `caddy-webmin-proxy-timing-diagnostic-terminal-2026-11-16`.
- Tag object: `cdebcef29aca82194f0aaf10842f9a769551ee5b`.

Atomic push succeeded. Remote main, tag object and peeled tag were independently
compared with local identities; all match. The server repository worktree is
clean. All applicable commit hooks passed. This establishes publication and local
hook validation, not a new target or hosted-CI acceptance result.

Private `webmin-timing-archive-review-fs4xr71p/publication-result.json` records
identities and verification; `publication.log`, `publication.exit`,
`publication-attempt.json` and `publication-session.json` retain execution.
Session 89810 is retired with exit 0 and its complete log consumed. No live target
contact, cleanup, successor, diagnostic retry or promotion occurred. Monitoring
record updates remain local and were excluded from this approved publication.

### November 16 local neutral cleanup and narrow-path implementation

The published W-173 tag resolves to the reviewed terminal commit. W-175 removes
only its consumed operation/recipe bindings and terminal manifest, retains the
archive tag, and refreshes the neutral transaction/operation pins. The stream is
clean and operation inactive. All executed bytes remain in the archive/private
seal. No new operation is registered.

W-171 is corrected in place: the outer reports its mode-0700 evidence directory
before payload construction or live dispatch. The actual bottom dispatch was
exercised with execution outcomes 0, 28 and 125; the directory is retained and the
original status is unchanged. These are failure-handoff tests, not target tests.

W-174's existing coordinator now supports explicit `primary-ipv4` diagnostic
scope. It skips secondary upload/admission/readiness, restores after a primary
pass or failure, and never publishes/exposes the candidate. Primary recovery
retains its existing containment, restoration, natural monitor and readback
steps; no secondary recovery is invoked. The transaction's application probe
uses IPv4 only. The proposed Webmin fragment selects one IPv4 upstream while
retaining health-check interval/timeout and service resource limits.

The existing parent binds the same scope before target work, permits only the
selected primary IPv4 path, captures clocks on the Pi and primary only, and starts
the resource collector before the direct request. It skips ready/finish/browser/
scan handling for this mode and still waits for Caddy completion before native
backend restoration. Direct/proxy request construction aligns public Host,
forwarded identity, user agent and encoding; this is not proof of received headers.

Focused checks caught and corrected a secondary-readiness call before the new
success stop boundary. Additional local test corrections fixed a missing test
payload context, an overly broad string substitution and an incorrect expected
success for the deliberately failing primary scenario. An initial clean-state
check rejected the neutral registry sentinel and stale outer pins; both were
corrected. The collision checker requires file arguments, not `--check`; the
correct invocation passed. None of these checks contacted a target.

Final qualification: owner payload/scope tests (including nonzero handoff and
IPv4-only probes), unchanged paired monitor/deadline cases, the two primary parent
success/failure cases, the existing eleven parent cases, twelve workload/clock
unit tests, native local HTTP/Caddy diagnostic tests, application-onboarding
host-only profile, neutral lifecycle/window/successor checks, Bash/ShellCheck,
readonly/local collision policy, Ansible syntax, YAML, Markdown and whitespace
checks pass. The initial parent run's sole failure was its incorrect expectation
for primary failure; that case was corrected and rerun with the primary success
case. No new load fixture or capacity acceptance was performed. vexp completion
verification was unavailable from the parent workspace (`not a git repository`);
owner checks are the verification evidence.

Private qualification evidence is under
`.local-evidence/uptime-kuma/primary-diagnostic-local-20261116/`; source hashes and
session dispositions are retained there. Sessions 88538, 73204, 16461, 59913,
60824 and 98190 are retired. The first parent wrapper exited 0 while retaining
parent-test failure 1 and HTTP-test success 0; the later primary rerun passed.

W-174 is not complete: W-176 must supply backend-native request evidence and
coverage for both requests before any candidate is sealed. Current request
correlation still indexes the Caddy probe; moving sampling earlier does not by
itself add direct-request correlation or prove health-probe overlap. Preserve
that limitation and the historical unknown cause. W-147/AC-013 remain unresolved,
W-157 remains source-only, and no live action, replay or publication occurred.

### November 16 W-176 bounded backend-interface evidence

Webmin's retained native source supports selected headers in its completed-request
access log, but that does not prove arrival for a stalled request. Its debug path
can include submitted data. Neither was enabled. The existing collector instead
uses a Linux packet socket in its existing process, on `eth0`, filtering the exact
reviewed primary IPv4/backend port pair before parsing. No vendor source, Webmin
log settings, service limits or recovery deadlines change. This is interface
observation, not instrumentation of Webmin's CGI execution.

The collector retains no packet files, bodies, cookies, authorization fields or
arbitrary header values. It stores matches against reviewed header constants (or
`unexpected`), a random request marker, native kernel timestamps, response status
and FIN/reset events. Header assembly is bounded to 8 KiB per stream, 64 connections
and 512 records; capture shares the existing 300-second observer. The receive
queue is bounded. TCP gaps/reordering, fragments, capture drops, invalid timestamps,
excess delivery lag, limits and incomplete receipts reject completeness. This is
not a general TCP analyzer: unsupported traffic stays an explicit evidence gap.
A FIN/reset records a connection ending, not successful delivery of a full HTTP
body. An absent response stays unknown; no causal attribution is inferred.

The direct request now carries its own marker and primary boot/boottime interval.
The temporary Caddy health probe has a fixed non-secret marker. The parent fetches
private wire evidence alongside resource samples before backend restoration.
Correlation requires both direct and proxied request identities, covers both
client intervals and the marked backend events, and retains possible health-probe
overlap. Missing wire/direct receipts cannot produce an accepted coverage receipt.
Recovery remains independent of diagnostic success.

Qualification decisions: test protocol parsing/privacy and the native capture
API, not target capacity. Twelve HTTP/collector tests passed in cached image
`14256f5f3c69` with `--network none`, including the actual collector loop, Linux
packet timestamps, seeded-secret exclusion, private file modes, shutdown and
native Caddy HTTP handling. Fourteen correlation/workload tests passed, including
both-request coverage and missing/out-of-window rejection. The two actual Ansible
primary parent success/failure cases passed with local owner adapters. Syntax
qualification, strict YAML, Markdown and whitespace checks passed. No load,
browser, scan or homelab contact occurred.

Earlier local attempts are retained: sandbox restrictions blocked loopback HTTP
and Ansible RPC before those cases could execute; the same bounded tests passed
outside that sandbox. A test's Python temporary suffix occasionally violated the
production evidence-directory grammar; it now uses the production `mktemp`
grammar. An import-edit indentation error was corrected before the final run.
These failures supply no evidence about the Pi or historical timeout.

Private logs and source hashes are retained under
`.local-evidence/uptime-kuma/backend-wire-local-20261116/`. Sessions 48522, 46808,
47980, 81566, 92283 and 21036 are retired; 47980 failed at local Ansible RPC startup,
while the scoped rerun passed. W-176 is locally resolved at the stated network
boundary. W-174 still needs exact owner/input bindings and a reviewed seal; no
new live authority exists. W-147 and AC-013 remain unresolved.

### November 16 W-177 routine upload correction and W-178 exact review

Aaron directed removal of duplicate application uploads during routine onboarding.
The primary receives the recipe, application fragment and publisher. The secondary
receives only the control recipe for expected hashes, admission and recovery; its
application files arrive through managed replication after primary verification.
The transaction rejects a fragment or publisher in secondary staging. No installed
publisher, finalizer, reconciler or notifier was changed. The permanent Caddy
onboarding procedure records this transfer boundary.

The diagnostic uses the existing owner path but excludes secondary staging,
admission, activation, observation and recovery. Its exact targets are
`ama@10.1.3.75` and `pi@10.1.0.53`, with existing strict host-key checks and fresh
operation boot continuity. Only the primary IPv4 source/backend path is probed.
The temporary backend profile preserves its existing guard and resource controls;
its recovery restores the exact loopback configuration.

Qualification:

- All 18 actual offline Caddy owner cases passed, including routine replication,
  paired trial restoration, and primary-only success/failure without secondary
  SSH or exposure. The secondary archive contains only the control recipe.
- Current graph evidence and nine stale/tampered/missing-evidence rejection cases
  passed. Focused host owner checks, shell syntax/ShellCheck/format and readonly
  collision checks passed. The initial host inventory check found a local Python
  import cache; removing that generated cache restored the check without a source
  or policy exemption.
- All seven W-176 qualification hashes remain unchanged. Its native HTTP/privacy,
  parent recovery and resource coverage evidence is reused explicitly. The exact
  private inventory/variables pass Ansible syntax-only checking; operator failure,
  one-use and drift tests pass. No host capacity conclusion follows.
- Local evidence copying encountered rootless fixture permissions, then existing
  symlinks on completion. The source evidence remained unchanged; namespace-aware
  copying completed the missing directories, all 36 selection links matched, and
  complete evidence verification passed. No test or target was replayed for this.
- vexp verification was unavailable from the parent workspace (`not a git
  repository`); the owner checks above provide the mechanical qualification.

Private review root:
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-primary-review-9m4pjnr5`.
`caddy-qualification/result.json` records passed and owned-container cleanup 0.
`reused-qualification.json`, `host-qualification-final.log`,
`evidence-verification-final.log`, `ansible-syntax.log`, `operator-tests.log` and
`sealed-preflight.log` retain the local results. The predecessor bundles and
published W-173 archive remain unchanged.

#### W-178 exact bundle, command and scope for review

Operation: `20261116-webmin-primary-ipv4-diagnostic`.

- Parent manifest: `78664fe65680404a1df264aa39fd275282e8ac31dde4b880d77f1879f339c84a` (241 inputs).
- Caddy outer authorization identity: `f1d56c0ebcc9b5a7b4fe119ef86881a3c79af3d4d56c9b36f2e6b8c989535e27`.
- `review.json` binds the manifest, targets, exclusions and command;
  `sealed-inputs-index.json` retains the reviewed bytes. Private file modes,
  runtime symlinks, SSH configuration absences and the existing local agent socket
  binding are checked. `--verify-only` passed without creating `attempt.started`.

Requested authority is **one diagnostic attempt**, including temporary backend
exposure and primary route activation, equivalent marked `/session_login.cgi`
requests, bounded timing/resource/backend-interface observation, and mandatory
primary plus Webmin restoration. It stops before replication on either outcome.
The backend observer records safe received-header comparisons, response status,
connection-close/reset and marked health-probe overlap; it does not prove internal
CGI execution or successful HTTP-body completion. Missing/out-of-window/dropped
capture remains incomplete, not a fabricated explanation of W-147.

Forward work is bounded to 240 seconds. Recovery, natural monitor acceptance and
readback share the aggregate 840-second cutoff. The resource/interface sampler
remains 300 seconds, child limit 1200 seconds and independent backend recovery
timer 1800 seconds. Existing service limits, reserve, guards, TLS and unrelated
routes are preserved. There is no secondary contact, replication progression,
DNS, authentication/browser/WebSocket workload, needrestart scan, reboot, failover,
notifier installation, permanent promotion, publication or replay.

After separate approval, run this once from the workstation WSL/Ubuntu terminal;
no password prompt or timed human acceptance is part of this diagnostic:

```bash
/usr/bin/python3 -I -B /home/aaron/code/.local-evidence/uptime-kuma/webmin-primary-review-9m4pjnr5/operator.py --manifest-sha256 78664fe65680404a1df264aa39fd275282e8ac31dde4b880d77f1879f339c84a --run-approved-once
```

The repository's [exact-bundle authorization rule](../../../homelab-server-configs/AGENTS.md)
and [Caddy authorization cadence](../../../homelab-server-configs/Caddy/AGENTS.md)
require approval before this live command. The operation is defined and sealed,
not executed or authorized. W-147 and AC-013 remain unresolved; W-157 is uninstalled.
All local sessions (89659, 29998, 75385, 78098, 76783 and 39473) are complete and
retired; session 26925 was already absent on resume and its retained payload log
passed. No execution session is active.

### November 16 W-179 approved diagnostic: direct HTTP 401 before Caddy

Aaron approved W-178's exact bundle/command/scope for one attempt. The unchanged
241-input manifest and owner authorization checks passed. `approval.json` records
that approval, and the exclusive `attempt.started` marker consumed it. Parent
session 44658 exited 2; it is complete and retired.

The direct request from `10.1.0.53` to `10.1.3.75:10000/session_login.cgi`, using
the selected Webmin hostname and proxy headers, returned HTTP 401 in 0.0513 seconds.
Connection setup took about 2.2 ms and the client header interval about 30.3 ms.
The expected allow counter rose from 0 to 9. The direct gate requires HTTP 200
and login-page content; it stopped before launching the Caddy outer runner.
This was a fast HTTP response, not a reproduced HTTPS timeout.

The backend interface retained the matching request marker and expected Host,
forwarded host/protocol/source and other reviewed headers. It observed response
first bytes, HTTP 401 and FIN closure; its terminal record reports no issues and
zero kernel drops. No health-probe request was recorded. This does not prove CGI
execution or complete body delivery, and cannot establish what caused the prior
proxied timeout. No response body or authentication challenge was retained.

The resource observer exited 0 and retained 33 samples, with stable Webmin cgroup
identity and zero high/max/OOM/OOM-kill counters throughout. Observed current memory
peaked at 58,740,736 bytes. This bounded failed request is not service capacity
acceptance. The complete direct/proxy coverage check is unavailable: no proxy
request or `caddy.stdout` was produced, and the checker reported FileNotFoundError.
W-180 tracks that outcome distinction alongside the response-contract review.

Recovery and scope:

- Owned proxy probe storage was removed. The diagnostic observer stopped and its
  interface/resource receipts were fetched before backend recovery.
- Exact Webmin loopback restoration returned success; its terminal-state assertion
  passed before the independent recovery timer was disarmed.
- Caddy child launch/recovery was skipped because the direct prerequisite failed.
  There was no Caddy publication, route activation, replication, secondary contact,
  browser/scan workload, DNS change or permanent promotion.
- The parent approval is consumed. The Caddy stream still describes a defined,
  **unexecuted child**, not an executed Caddy terminal operation. Preserve that
  distinction; it grants no right to invoke the child separately or replay the
  consumed parent. No terminal archive publication is requested by this result.

Evidence remains under the W-178 private review root. `execution-summary.json`,
`RECEIPTS.SHA256SUMS`, `parent.log`, `parent.exit`, `inputs/evidence/backend-path-a-ipv4.json`,
`backend-wire.jsonl`, `backend-resource-samples.jsonl`, clock receipts and
`parent-owner-outcomes.json` bind the observations and recovery to the unchanged
sealed inputs. W-147/AC-013 remain unresolved and W-157 remains uninstalled.
Next work is local contract reconciliation, not another live trial.

### November 16 W-180 login-page contract reconciliation

The pinned Webmin 2.670 request handler provides a concrete explanation for the
new direct-401 result: `miniserv-lib.pl` lines 509–516 disable session mode when
User-Agent matches `/webmin/i`. Its HTTP-authentication branch returns 401 with a
Basic challenge. Both diagnostic clients send `homelab-webmin-diagnostic`, and the
wire observer expects that same string. This is a client contract defect, not a
reason to weaken the login-page acceptance gate or change Webmin authentication.

One bounded experiment used the existing cached image
`14256f5f3c69b7fec79d8153ca54737d5b9df4c60af6a46faa57a791d7d5e9a2`, native Webmin
2.670 and `--network=none`. With the same server, path and other request headers,
only User-Agent changed:

| User-Agent | HTTP | Basic challenge | Login form |
| --- | --- | --- | --- |
| `homelab-webmin-diagnostic` | 401 | Yes | No |
| `homelab-proxy-diagnostic` | 200 | No | Yes |
| `homelab-webmin-diagnostic` | 401 | Yes | No |

The native library SHA-256 was
`41efb90b14725a01f623a524c7bfec74dec17bf52b4ff369ee33fd69396e252d`.
The process exited and its exact owned container was removed. This experiment
settles the pinned authentication-selection defect; no broader fixture load,
paired-proxy run or capacity test is needed. It does not prove the historical
HTTPS timeout's cause. The live attempt retained no challenge/body or live handler
hash, so the production observation is consistent with this demonstrated mechanism,
not an independent proof of every server-side branch.

The reconciled contract keeps unauthenticated `/session_login.cgi`, trusted proxy
HTTPS, existing limits and HTTP-200/login-form acceptance. Use one neutral header
in the direct client, Caddy probe and observer. Do not add credentials, accept 401
as browser readiness, change server session policy or lengthen timeouts. Any
configured `agents_nosession` pattern also belongs in request-contract review.
The permanent Webmin fleet procedure now records this requirement and the need
for a native handler check rather than a generic HTTP-200 substitute.

The follow-on coverage error is separate: the direct gate stopped before the
Caddy child existed, so `caddy.stdout` was absent. Future reporting should label
that proxy request not run while preserving the original rejection and recovery;
there is no evidence of another transport failure.

Private evidence: `/home/aaron/code/.local-evidence/uptime-kuma/login-contract-w180`.
`comparison.json` records the native results without bodies/cookies/credentials;
`compare.py`, extracted vendor source, `cleanup.json` and `reconciliation.json`
retain provenance. `user-agent-correction.patch` changes only the three header
sites and passes `git apply --check`. It is not applied or sealed; W-181 tracks
integration and owner binding refresh. Consumed bundles/receipts remain intact.
Context7's official Webmin proxy guide confirms the existing hostname/referrer
settings, but does not specify this User-Agent behavior; pinned native source and
execution provide the evidence. Documentation lint and diff checks pass.
No live contact, retry or publication occurred. Session 91415 exited 0 and is
retired; no execution session is active.

### November 16 W-181 integration and neutral owner reconciliation

Applied the reviewed three-site User-Agent patch: the direct client, Caddy curl
probe and received-header comparison now agree on `homelab-proxy-diagnostic`.
The HTTP-200/login-page requirement is unchanged; the focused regression includes
an HTTP-401 response and confirms rejection without retaining private body text.
W-180's native header-only comparison remains the evidence for the server contract.
No additional native load fixture was needed for this literal header correction.

The parent invokes direct/proxy coverage only after a Caddy job was launched.
If the direct prerequisite stops it first, it retains `coverage_accepted: false`,
`proxy_request: not-run`, `reason: caddy-not-started` in the comparison receipt and
owner outcomes. It still collects available evidence, preserves the original
failure and restores the backend; a skipped comparison cannot satisfy completion.

W-179 never launched the Caddy child. Its unexecuted definition and recipe were
withdrawn locally, successor/coverage registrations cleared, and the existing
neutral transaction/operation/outer hashes refreshed. The stream is clean, the
operation inactive, and W-173's last published archive tag remains the boundary.
This does not reclassify W-179 as a successful operation or authorize reuse. All
241 preserved input copies match their sealed-input index; the consumed parent,
one-attempt marker, approvals and live receipts remain in their original private
root. No executed Caddy operation was removed without its required archive.

Local qualification at the recorded source hashes:

- Existing actual Ansible parent flow passed primary success, primary Caddy failure
  and the added direct-path rejection case. The latter proves no Caddy/coverage
  invocation, explicit not-run receipts, and final backend restoration.
- Focused client and segmented wire/privacy tests passed. The client test checks
  neutral header agreement with the owner probe and still rejects 401.
- Caddy application-onboarding host profile, neutral successor/lifecycle/window
  policies, shell collision/format checks, YAML lint and diff checks passed.
- vexp verification remains unavailable from this parent workspace; owner checks
  provide the scoped verification. No full paired fixture or capacity run was used.

Evidence: `/home/aaron/code/.local-evidence/uptime-kuma/user-agent-integration-w181`.
`source-sha256.json` binds changed implementation, tests and neutral owner inputs;
`w181-parent.log`, `w181-http.log` and `w181-owner-final.log` retain test results.
The old candidate's source/evidence bindings are intentionally obsolete; no new
manifest, operator command, operation or authorization has been created.

Any future candidate must bind the current client, parent, observer, neutral
owner path and its new operation-specific qualification. Preserve the same
primary/IPv4 scope, guards, deadlines and recovery. Do not reuse W-178's manifest,
old owner qualification or consumed approval. Actual target response and the
historical HTTPS timeout remain unresolved under W-147/AC-013. W-157 remains
uninstalled; no target contact or publication occurred.

### November 16 W-182 corrected primary/Pi diagnostic preparation

Prepared one new definition from W-181's corrected sources. Direct and proxied
login-page requests and wire comparison share the neutral User-Agent; the
HTTP-200/login requirement is unchanged. The parent records pre-Caddy comparison
as not run and still restores the backend. No other runtime behavior was changed
for this candidate. The owner graph, recipe and parent paths are newly bound;
W-178's consumed manifest and approval are not reused.

Local qualification:

- All 18 current owner execution/recovery cases passed in the network-disabled
  container, including primary-only success/failure without secondary contact or
  replication exposure. Owned-container cleanup passed.
- Current graph verification and all nine stale/tampered/missing-evidence
  rejection cases passed; the owner authorization-ready check passed.
- Focused host application-onboarding checks, shell syntax/ShellCheck/format,
  exact Ansible syntax-only inputs and operator one-use/failure/drift tests passed.
- W-181's four unchanged Webmin source/test hashes reuse its focused parent and
  HTTP/wire qualification. Three unchanged earlier observer/workload/proposal
  hashes reuse W-176 evidence. W-180's native header-only comparison is retained;
  no new capacity/load fixture was run and no target capacity claim follows.
- All 241 preserved W-178 input copies still match their retained index.
  Namespace-aware copying preserved the completed owner's evidence without
  replaying tests. Current runtime symlinks, private modes and SSH input absences
  were checked during sealing. The local agent socket exists; live admission
  must still independently establish readiness and fresh boot continuity.

Private evidence and exact reviewed input copies:
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-primary-review-6u01j43s`.
`reused-qualification.json` identifies reused evidence and its unchanged hashes;
`caddy-qualification/result.json`, `owner-host.log`, `evidence-rejection.log`,
`authorization-ready.log`, `ansible-syntax.log`, `operator-test.log` and
`sealed-preflight.log` retain the current qualification. No `attempt.started`
exists. vexp remains unavailable from the parent workspace; current owner
validation provides the scoped verification.

#### W-182 exact bundle, command and scope for review

Operation: `20261116-webmin-primary-login-diagnostic`.

- Parent manifest: `323cb347b16f1279d2b36756e26c732a435d67ec2bb4f5143778ab244fd65c81` (241 inputs).
- Caddy outer authorization identity: `2a2d7df7c6464fed9f9b8cf16a83dc574e1e93594e72e90eddb81fa64b40bfaf`.
- Targets: `ama@10.1.3.75` and primary `pi@10.1.0.53` only.
- `review.json` records the command and scope; `sealed-inputs-index.json` retains
  the exact reviewed bytes. Local `--verify-only` passed without live contact.

Requested authority is **one diagnostic attempt**: temporarily apply the guarded
Webmin profile, run the primary-to-Pi IPv4 login-page prerequisite, activate the
primary-only temporary Caddy route if it passes, compare the equivalent marked
proxied request, retain bounded timing/interface/resource evidence, then restore
both owners regardless of the request result. No replication exposure occurs.
The observer reports received-header comparisons, response/close events and
health-probe overlap at the backend network boundary, not internal CGI completion
or successful full-body delivery. Missing, dropped or out-of-window evidence
cannot establish a complete comparison or explain the historical timeout.

Forward work remains bounded to 240 seconds; recovery, natural primary monitor
acceptance and readback share the 840-second aggregate cutoff. The sampler remains
300 seconds, child limit 1200 seconds, and independent backend recovery timer
1800 seconds. Existing caps, reserve, guards, TLS and unrelated routes remain.
No secondary contact, replication progression, DNS, credentials/authentication,
browser/WebSocket workload, scan, reboot, failover, notifier installation,
permanent promotion, publication or replay is included.

After separate approval, this exact command permits one attempt; no private login
or timed human check is required:

```bash
/usr/bin/python3 -I -B /home/aaron/code/.local-evidence/uptime-kuma/webmin-primary-review-6u01j43s/operator.py --manifest-sha256 323cb347b16f1279d2b36756e26c732a435d67ec2bb4f5143778ab244fd65c81 --run-approved-once
```

The [repository authorization rule](../../../homelab-server-configs/AGENTS.md)
and [Caddy authorization cadence](../../../homelab-server-configs/Caddy/AGENTS.md)
require exact-bundle approval before live execution. This candidate is sealed,
unexecuted and not authorized. W-147/AC-013 remain unresolved; W-157 is not
installed. Local sessions 88684, 68038, 13025, 9652 and 89469 exited 0 and are
retired; syntax and operator checks also completed. No execution session is active.

### November 16 W-183 approved primary/Pi diagnostic result

Aaron approved W-182's exact bundle and scope for one attempt. Input verification
passed, approval was retained privately, and the existing operator launched once
as session 78547. Parent exit 2, Caddy exit 1, primary curl exit 28. Approval is
consumed. The 241 sealed input copies, approval, attempt marker and complete logs
remain in `webmin-primary-review-6u01j43s`; no replay was performed.

Observed request boundary:

- Direct primary-to-Pi IPv4 `/session_login.cgi` returned HTTP 200/login content
  in 2.475 seconds. The neutral User-Agent correction reached the target.
- Primary HTTPS completed TLS in 0.051 seconds but received no first byte before
  the 5.002-second timeout. The backend capture contains that request's exact
  marker and the same eight recorded header values as the direct request.
- The proxied flow reached the Pi interface but has no captured response bytes
  or response headers. Its request-side FIN followed about five seconds later;
  a backend-side FIN was observed later. This locates the observed stall beyond
  successful TLS and backend delivery, not inside a specific CGI function.
- Marked health requests were also captured. Their presence does not establish
  that they caused memory growth or the request failure.

Actual Webmin resource evidence changes the next investigation. The original
cgroup reached a sampled 201,134,080 bytes (191.82 MiB) under its unchanged
201,326,592-byte cap. Its counters rose to `high=5519`, `max=60`, `oom=3` and
`oom_kill=1`. High events began during the proxied request; the OOM kill occurred
later than the client timeout. The cgroup was then unavailable in two samples
and reappeared with a different identity. Do not infer healthy execution from the
new cgroup's zero counters or the later pre-restoration snapshot. These are
actual-target observations, not fixture capacity acceptance. The triggering
activity and exact timeout cause remain unconfirmed under W-147.

The observer exited 0 and retained 78 resource samples plus its stop record and
47 wire records. The wire terminal record reports no capture issues or kernel
drops. Nevertheless the aggregate checker rejected `backend_wire_headers_incomplete`:
its per-flow rule requires a request-header record even for unmarked flows with
only a close event. Both marked foreground request-header records are present.
W-184 tracks this local evidence-contract gap. Preserve the failed aggregate
receipt; manual observations above do not convert it into accepted correlation.

Recovery and scope:

- Primary selection/outbound restoration and independent readback passed.
  The natural replication-monitor completion, success status and boot continuity
  checks passed; the notifier was not replaced.
- Exact Webmin loopback restoration and the native terminal-state assertion
  passed before the independent recovery timer was stopped.
- No secondary SSH/transfer/activation, replication exposure, credentials,
  browser/WebSocket workload, scan, DNS, reboot or promotion occurred.

Private evidence: `execution-summary.json`, `RECEIPTS.SHA256SUMS`,
`inputs/evidence/backend-path-a-ipv4.json`, `backend-wire.jsonl`,
`backend-resource-samples.jsonl`, `diagnostic-coverage.json`, the complete parent
log and copied `caddy-live-evidence` tree. Decoded readback files were verified
against their retained byte lengths and SHA-256 values. `resource-summary.json`
keeps cgroup identities separate. No new target query was used for this review.

The Caddy stream is now terminal-pending with failed-consumed result. Exact
executed runtime/operation/recipe bytes remain; successor and coverage registries
are cleared. The planned archive tag is
`caddy-webmin-primary-login-diagnostic-terminal-2026-11-16` (unpublished).
W-185 requires separate archive preparation and publication approval. W-147 and
AC-013 remain unresolved, W-157 uninstalled. No further live work is authorized.

Terminal local checks: deployment-window and successor terminal policies pass;
Markdown and diff checks pass. The full application-onboarding host profile stops
at `coverage_sha256`: its definition check expects the still-executed operation's
coverage hash to match the now-cleared terminal coverage registry. Preserve the
operation and failed test; do not rebind a consumed input to manufacture a pass.
W-185 archive preparation must account for this terminal-state qualification
boundary. This local test result changes neither restored host state nor the
observed HTTP failure. Session 11365 exited 1; 54534 exited 0; both are retired.

### November 16 W-186 all-changes publication

Aaron authorized committing and pushing all changes. Workspace inventory found
changes in two repositories only: server configurations and this tracking record.
Both destinations were verified as public repositories owned by Racerx323; both
local main branches matched their fetched remotes before publication. Private
raw evidence and generated indexes are excluded.

Server commit `bda63a46f88620f177d01e527644625b5eb27ab2` publishes 20 changed files,
including the consumed primary/Pi diagnostic. Its annotated tag
`caddy-webmin-primary-login-diagnostic-terminal-2026-11-16` and main branch were
pushed atomically and remote-verified, including the tag object's peeled commit.
W-185 is complete. The deployment stream remains terminal-pending; no neutral
cleanup, live retry or source installation was performed.

Publication qualification:

- All three current Caddy CI profiles passed locally against the exact pinned
  DNS checkout. Server pre-commit hooks and the staged-tree secret scan passed.
- Initial YAML lint rejected valid indentless sequences in the consumed operation.
  A small repository lint entrypoint permits consistent sequence indentation only
  for that exact operation path. All other YAML retains its existing rules;
  malformed YAML still fails. The executed bytes and their hashes are unchanged.
- Whole-tree secret scans flagged ignored generated index metadata and two
  integrity hashes in this ledger. Both ledger hashes were independently verified
  against preserved outer-runner bytes and narrowly allowlisted. No credential
  was found in the publication scope; raw private evidence stays outside Git.
- The previously recorded application-onboarding profile failure on the cleared
  terminal coverage registry remains preserved. It is distinct from the three
  passing current-production CI profiles. No consumed operation was rebound and
  no failed live acceptance was converted to success.

This monitoring commit includes the plan, work ledger, result and the two exact
non-secret hash exclusions. Final monitoring remote verification and GitHub CI
receipts are retained in the private review at
`/home/aaron/code/.local-evidence/uptime-kuma/publication-w186-h4166g95`.
Publication does not resolve W-147/W-184 or AC-013 and does not install W-157.

### November 17 W-187 retained evidence reconciliation

This review used only the consumed W-183 bundle. All 71 entries in its
`RECEIPTS.SHA256SUMS` still match. The current handoff checker matches the sealed
copy and reproduces `backend_wire_headers_incomplete` on the original wire file.
No receipt or consumed runtime input was rewritten. Local derived analysis is in
`/home/aaron/code/.local-evidence/uptime-kuma/reconciliation-w187/retained-analysis.json`.
It is an analysis record, not replacement acceptance.

W-147 timeline, from the backend's retained timestamps:

| Observation | Relation to the proxied request arriving at the Pi |
| --- | --- |
| Direct login request returns 200 in 2.475 seconds | Completed about 23 seconds earlier |
| Eight marked health requests arrive in 1.624 seconds | Start 1.806 seconds before it; all arrive before it |
| Proxied request arrives with matching foreground headers | Time zero; no response-first-byte or response-header event captured |
| First positive memory.high sample | About 2.870 seconds later; counter increases from 0 to 9 |
| Client-side FIN; Caddy logs marked request status 499 | About 4.951 seconds later; curl reports timeout, HTTP 000 |
| First positive memory.max sample | About 25.005 seconds later |
| First positive OOM/kill sample | About 26.008 seconds later; OOM 3, kill 1 |

Counters are sampled, not exact event timestamps. The existing before/after
clock-envelope calculation independently places the first high-event interval
inside the client's request interval and the first OOM/kill interval after it,
including clock uncertainty. Therefore an OOM kill is not established as the
initiating event for this timeout. Pressure during the request is established;
its contribution to response latency is not quantified. Peak sampled usage was
191.82 MiB under the unchanged 192 MiB cap. The original cgroup, two unavailable
samples and replacement cgroup remain separate; later zero counters do not
clear the original OOM evidence.

The eight health flows have no captured response bytes. Six client FINs occur
almost immediately; two occur about three seconds after their request headers.
Backend FINs appear later, clustered near the first positive OOM sample. These
are network observations, not proof of eight concurrently executing CGI workers.
The health requests also differ from the foreground header contract: retained
User-Agent/Accept-Encoding values are classified as unexpected, with original
values intentionally not stored. The two foreground header sets still match.
Do not infer the health requests' exact values, authentication mode or outcome.

The fragment specifies a 30-second health interval, yet eight requests arrived
within 1.624 seconds during primary preparation/activation. This makes startup
probe generation the next narrow owner-path question. Retained source contains
validation/finalization/reconciliation steps, but these receipts do not identify
which process generated each connection. A causal claim about validation,
health-check concurrency, a Webmin worker or a leak would exceed this evidence.
The sanitized journal retains two timeout categories and the marked 499 record;
it has no worker attribution or upstream-duration value. No new fixture load
can settle this target question. Do not increase caps/timeouts, serialize health
checks or remove checks merely to obtain a pass.

W-184 reconciliation and future correction boundary:

- Flows 3 and 5 contain only request/response FIN records, with no first-byte or
  header events in either direction. The collector creates these flows on a
  captured inbound SYN and reports no issues or drops. They are connections with
  no observed payload, not incomplete copies of either marked HTTP request.
- Retain them explicitly in a separate connection classification. Do not invent
  an HTTP request, health marker, successful response or CGI completion for them.
- Preserve rejection for any first-byte event without complete request headers,
  response data without an attributable request, unexpected events, duplicate or
  missing required markers, capture issues/drops and failed clock/resource coverage.
  An empty/headerless flow must not become a general bypass.
- Qualify only this parsing contract using the retained close-only example and
  minimal negative cases in the existing tests. No additional capacity fixture
  or target attempt is needed to settle W-184. Source implementation is pending.

The original aggregate receipt remains failed; manually established facts above
do not certify its downstream gates. Both owner restorations and primary natural
monitor acceptance remain as recorded in W-183. AC-013 and W-147 stay open;
W-157 remains uninstalled. W-185's published archive remains intact and Caddy is
still terminal-pending; neutral cleanup has not run. This local review provides
no live, replay, promotion or publication authority.

### November 17 W-188 neutral cleanup and W-184 correction

Verified the annotated W-185 tag resolves to `bda63a4` and matches the retained
remote publication receipt. Before cleanup, the current operation, recipe,
terminal manifest and outer runner matched their archived bytes. Reset the
operation to inactive, remove its consumed recipe/terminal data from the current
branch, retain the archive tag, and refresh only the outer operation hash.
Lifecycle rows now classify the neutral inputs as workstation-only. No successor
is registered. Archive and private sealed copies remain unchanged.

The existing Webmin handoff now retains valid close-only flows separately as
`no-observed-payload`. It does not turn them into health checks or HTTP successes.
Their event times must remain inside resource coverage. Partial request headers,
response data without a request, unknown events, duplicate closes/markers,
missing required markers and capture issues/drops still reject. This is a small
parser correction in place, not a new observer or orchestration layer.

Qualification:

- All 14 existing workload tests pass, with added FIN/reset classification,
  partial/unknown event, malformed close, duplicate-header and out-of-window-close
  cases. Existing missing-marker, capture-loss and clock/resource cases remain.
- The corrected full correlation path processes byte-identical copies of W-183's
  captured wire/resource/clock data and hash-verified readback envelopes. Both
  foreground requests and eight health requests remain; flows 3/5 are classified
  separately. Derived coverage passes and explicitly retains `causal_attribution:
  false`. All 71 original receipt hashes still match. The original failed receipt
  is unchanged; this is local reanalysis, not retrospective live acceptance.
- The current Caddy repository-policy host profile, neutral window/successor
  policies, documentation policy, YAML/Markdown checks, ShellCheck, canonical
  shell formatting and readonly/local collision policy pass. The vexp completion
  helper remains unavailable from the parent workspace (`not a git repository`);
  repository checks supply verification instead.

Private qualification and source hashes are in
`/home/aaron/code/.local-evidence/uptime-kuma/classification-w184/`.
`verify-retained.py` exercises the actual corrected handoff against copies and
writes a separate source-hash-named derived receipt. No live socket, target SSH,
browser, scan or capacity fixture was used. All temporary analysis copies were
removed. W-184/W-188 are resolved locally; source is uncommitted and uninstalled.

### November 17 W-189 startup health-request source trace

The actual primary path calls publisher preparation, the installed finalizer,
then the installed reconciler before serving checks. Source trace:

| Stage | Request-generating opportunity |
| --- | --- |
| Publisher `publish-release-v2.sh:190` | Validates the complete candidate before preparing it |
| Finalizer `finalize-incoming-release-v2.sh:249,267` | Validates before and after setting completion/locked modes |
| Installed reconciler `reconcile-release-v2.sh:498` | Validates candidate before selection |
| Installed reconciler line 577 / Caddy service reload | Loads/provisions the selected configuration |

The finalizer source matches its accepted installed hash. The current reconciler
source differs from the installed identity; the installed hash instead matches
Git commit `d131b9da63ad92abaa7c9901d2f76998ca6f2508`, and the validation/reload
calls above were checked in that exact historical source. This is identity-based
source reconstruction, not a new installed-state observation.

Caddy's command documentation states that validation provisions modules. The
pinned 2.11.4 upstream source confirms `Handler.Provision` launches the active
health checker (`reverseproxy.go:421`); `activeHealthChecker` checks immediately
before waiting for the interval (`healthchecks.go:283`). Thus a 30-second interval
does not impose a 30-second delay on first probes or serialize separate validation
processes. Repeated validation and reload provide a concrete mechanism for the
observed startup burst. Upstream file identities and references are retained in
`classification-w184/upstream-provenance.json`.

This trace does not assign all eight captured health connections to specific
processes, prove how many Webmin workers executed, or prove memory/timeout
causation. Do not equate the validation call count with the packet count. Keep
W-147 open. The next owner decision should address pre-activation validation
probe traffic while preserving full configuration validation and the activated
service's health checks, before selecting a single-factor target comparison.
No validation removal, health-policy change, timeout/cap increase or new target
comparison has been selected or authorized.

Fleet Caddy and Webmin onboarding instructions now require startup validation/
reload probe load to be considered, and document the close-only evidence boundary.
No new live operation is sealed. AC-013 remains pending, W-157 uninstalled and
restoration results unchanged. All local sessions are complete and retired.

### November 17 W-190 Caddy owner review: validation probe containment

The owner contract requires full candidate validation before activation and
independent receiver validation. Preserve those checks. The correction should
change the validation subprocess's network access, while keeping its exact
configuration, module provisioning, TLS/key inputs, environment and result checks.
It should leave runtime reload and the activated service's health checks in their
normal network context. This separates validation side effects from serving
health without weakening either validation or application acceptance.

Proposed implementation boundary, pending W-191 qualification:

- Reuse a small shared Caddy validation entrypoint at the publisher, finalizer
  and reconciler validation calls. Keep finalizer validation both before and
  after locking/completion; its integrity boundary is not redundant work to remove.
- Use a short-lived native network namespace for the validator process only,
  with no external interfaces/routes, namespace persistence, host firewall edits
  or new service lifecycle. Existing root callers can create a network namespace;
  the unprivileged `caddy-sync` finalizer needs a qualified unprivileged namespace
  mechanism. `unshare` is a candidate mechanism, not an established host capability.
- Preserve caller authority and required filesystem access. A current-user mapping
  must not be assumed equivalent merely because its numeric UID/GID matches:
  supplementary groups, TLS access and the reconciler's `NoNewPrivileges=true`
  context need focused proof. Do not add sudo rights, setuid/capability helpers,
  account/group changes or relax unit controls to make the proposal work.
- If namespace creation, identity/access checks or validation fails, stop before
  progression with bounded expected/observed diagnostics and original status.
  Never fall back to networked validation. Preserve current request/parent deadlines
  and direct signal handling; no persistent helper or new recovery orchestration.
- Apply the same rule to any provisioning validation used in a recovery path;
  keep actual reload, rollback, transport and serving-health checks outside the
  validator's namespace. Bind changed helper/tool identities through the existing
  owner inventory and separately reviewed deployment procedure.

Changing only the controller or publisher would leave installed finalizer and
reconciler validation unchanged. A production correction therefore needs an
explicit owner-managed tool update and its recovery, beyond the earlier
application-fragment-only trial. Qualifying a repository helper does not establish
that any installed caller uses it. Account for that scope before a live review.

This proposal targets IPv4/IPv6 backend traffic. A network namespace does not
isolate filesystem Unix sockets or prove that every module is offline-compatible.
The current release uses local TLS material and fixed backend addresses; any
module that requires external access to provision must fail explicitly and return
for owner review. Do not strip health configuration, substitute backend addresses,
or waive validation failures. No assertion about either proxy's namespace support
or current permissions follows from this local review.

Alternatives rejected for this correction: replacing validation with adaptation,
removing active checks during validation, lengthening intervals/timeouts, raising
Webmin's cap, serializing only foreground address-family probes, or isolating the
whole Caddy/reconciliation service. These either change the tested configuration,
miss immediate startup probes, change the capacity question, or exceed the needed
process boundary. A new privileged validation service would add machinery and
privilege not justified by this review.

Focused local qualification, using the existing test environment only:

1. Exercise the actual pinned Caddy validator and proposed entrypoint under root
   and the existing unprivileged-finalizer permission model, including the
   reconciler's restrictions. Prove required TLS/config access remains and that
   no new authority is granted. Unavailable host-equivalence remains a prerequisite
   for separately authorized admission, not a reason to weaken local checks.
2. Use an instrumented disposable HTTP endpoint to show validation sends no
   external IPv4/IPv6 requests. The unchanged valid configuration must still
   provision successfully; malformed configuration, unreadable/bad TLS inputs
   and isolation failure must reject. This tests containment/configuration,
   not the Pi's capacity. Do not add load-duration or memory benchmarks.
3. Start the same configuration normally within that disposable test environment
   and verify its configured active checks still reach the endpoint. Exercise
   child failure, deadline and termination through existing entrypoints; retain
   status and cleanup without adding an orchestration layer.

Stop local testing when those decisions are settled. Only then prepare a
separately reviewed primary/Pi comparison with this one changed factor, unchanged
health policy/caps/deadlines and the already qualified request/resource capture
and restoration. A pass would support this factor's relevance, not conclusively
attribute every historical failure. No such operation is defined or authorized.

Permanent Caddy instructions now explicitly place `validate` and `adapt --validate`
examples inside network-disabled local qualification; a temporary directory alone
never authorized backend contact. Vendor reference: Caddy CLI provisioning semantics
and util-linux 2.38.1 `unshare(1)` namespace/mapping semantics were reviewed. The
latter is a mechanism reference, not a claim about installed utility versions.
No executable correction, namespace experiment, target inspection, live workload
or publication occurred in this review. W-147/AC-013 stay open; W-191 owns the next
local implementation and qualification.

Review validation: focused Markdown, Caddy operator-documentation policy and
Git whitespace checks pass. No behavioral test or target-capacity claim was added.

### November 17 W-191 validation isolation implementation and qualification

The shared preparation-only helper is
`homelab-server-configs/Caddy/scripts/validate-caddy-isolated.sh`; its lifecycle is
`future-task`, not node-installable. Root uses native `unshare --net`, retaining its
original user namespace and receiver-file access authority. Unprivileged callers
use `--user --map-current-user --net`. Both directly exec the exact Caddy validator
with the supplied config and inherited environment. There is no fork, privilege
helper, config rewriting or networked fallback. Publisher/finalizer/reconciler
calls and installed inventories remain unchanged because qualification is partial.

The focused `Caddy/tests/validation-network-isolation.py` runs actual Caddy 2.11.4
in existing image `8ab253f9450c`, with `--pull never --network none`, a read-only
source mount and unchanged default capabilities/security policy. Only disposable
container accounts/files are created. This tests containment and permissions, not
Pi capacity. The caddy-sync fixture has a supplementary caddy-tls group and reads
a root-owned group-readable private key. With NoNewPrivileges enabled:

- Full exact-config validation passes and sends zero requests to instrumented
  IPv4/IPv6 endpoints outside the validation namespace.
- An unknown proxy option, invalid TLS key and root-only unreadable key reject.
- The unchanged config running normally reaches both health endpoints; its owned
  runtime process group is terminated and the container is removed.
- Root's network-only isolation fails closed with status 1 and Operation not
  permitted. Mapping root into a new user namespace succeeds but cannot read a
  receiver-owned 0640 input that the original root can read. This is a permission
  regression, not an acceptable workaround.

The final qualification exits **2 (partial)**, deliberately not success. Root
namespace capability is unavailable in this unchanged local container; this is
not evidence about either target's capability. No capabilities, privilege, kernel
settings, permissions or service controls were added to get a pass.
NoNewPrivileges is tested; the complete reconciler service sandbox, root success,
full owner call paths, deadline/termination integration and real release/module
inputs remain unqualified. W-191 is blocked pending a local qualification approach
that preserves the approved authority constraints. Do not integrate this helper
or prepare a target comparison from the partial result.

Evidence is private under
`/home/aaron/code/.local-evidence/uptime-kuma/validation-isolation-w191/`.
The first test exposed an invalid negative test: a trailing Caddyfile token was
accepted as another site. Its failed log is retained. The corrected test uses an
unknown reverse-proxy subdirective; the final run also retains the root permission
regression. This fixture correction establishes configuration rejection only.
No live contact, workload, retry, promotion or publication occurred. All commands
ended synchronously; all owned containers were removed. W-147/AC-013 remain open,
W-157 is uninstalled, and consumed operation evidence remains untouched.

Local structural validation passes: Bash syntax, ShellCheck, canonical shfmt,
multifile-grep and readonly-local collision policy; Caddy deployment lifecycle,
test inventory, neutral successor and operator documentation policies; focused
Markdown and Git whitespace checks. The private `qualification.json` binds final
helper/test hashes, exact offline command, log hash and exit 2. These checks do not
clear the root-success or owner-integration blocker.

### November 17 W-192 narrower preparation and W-193 harness review

Aaron agreed to stop fixture expansion and prepare a small primary-host
capability/validation check. This supersedes W-191's earlier requirement to
resolve root isolation inside the local container before any target-check
preparation. The retained failure remains valid evidence about that container;
it neither proves nor disproves namespace support on the primary. Root's
user-namespace permission regression remains a real reason to reject that
workaround. The helper stays preparation-only and unintegrated.

PLAN.md now owns the bounded scope: primary only, existing caller authority,
namespace-first execution, full validation without activation, native service
restrictions, explicit deadlines and owned temporary-process cleanup. Execution
must first be bound to exact commands/inputs for separate authorization. This
review does not define a Webmin comparison or authorize running the check.

The existing workspace `AGENTS.md`, section "Fixture evidence and target
capacity", already says to stop when the fixture cannot resolve the remaining
uncertainty. The agent failed to apply that instruction; absence of a rule was
not the cause. Its detailed examples emphasize capacity. Proposed addition
within that existing section (not installed):

> Apply this stopping rule to platform compatibility as well as capacity. A
> fixture's different privileges, kernel capabilities, filesystem permissions or
> service sandbox are evidence limits, not automatically deployment defects or
> requirements to repair the fixture. Once applicable correctness and safety
> questions are settled, move the remaining environment-specific question to the
> smallest separately authorized check in the intended environment. Do not extend
> fixture fidelity or add orchestration solely to make a substitute reproduce that
> environment. Concrete correctness, security and recovery defects remain blockers.

No executable, fixture, workspace instruction, production inventory or live state
was changed in this reassessment. Existing results and consumed attempts are
preserved. Only the change-record scope, next action and result were reconciled.

### November 17 W-193 approved harness clarification installed

Aaron approved the recorded wording. Added it unchanged to workspace
`/home/aaron/code/AGENTS.md` within "Fixture evidence and target capacity". The
rule now explicitly covers platform privilege, kernel, filesystem and service
sandbox differences. Existing safety blockers and separate live authorization
remain intact. W-193 is resolved; W-192 preparation and all deployment states
are unchanged. No executable, fixture or live work occurred; nothing was published.

Validation: installed paragraph matches the approved text exactly; whitespace
checks pass.

### W-192 exact primary-host capability/validation bundle for review

Bundle:
`/home/aaron/code/.local-evidence/uptime-kuma/validation-capability-review-2jben2ib`.
Twelve inputs bind the runner, remote script and embedded namespace child,
reviewed plan, scope, retained known-hosts file, accepted owner inventories,
installed-file expectations and preparation-only helper reference.

`INPUTS.SHA256SUMS` SHA-256:
`c777734467943e0e2bef901e55b4ffbde6c9f18dc8432744ac1503694ee2dc89`.
Runner SHA-256:
`1737c3be2e6db5358f1011c0eb3ffffed71019e93fd3fc3239a4ea12d374e045`.

Exact command, **only after separate one-attempt authorization**:

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/validation-capability-review-2jben2ib/run.sh --run-approved-once
```

Scope: one SSH session as pi to primary `10.1.0.53`, expected native hostname
`j1-svpihole0`, strict retained host-key verification and existing sudo authority.
Fresh boot continuity, accepted release/payload, installed owner tools/environment
and reconciler unit are checked before transient work. The accepted Caddy version
is 2.11.4; executable hash is freshly admitted, matched to the running service
executable and required unchanged. No historical binary hash is invented.

The check creates one private `/run/caddy-validation-capability.<nonce>` directory
and at most six sequential validation-only transient units named from that owned
directory, context and phase. Root publisher, caddy-sync finalizer and root
reconciler contexts each prove isolated networking and required file access
first. No validation runs unless all three prechecks pass. Each then performs
one full validation of the unchanged accepted release, in that order. Namespace
creation failure, file-access failure, inventory drift or validation failure stops
progression; there is no retry, networked fallback or privilege change.

All transient processes make production files read-only and use private temporary
logs. Reconciler NoNewPrivileges, PrivateTmp, ProtectHome, ProtectSystem and UMask
are checked against installed effective values and preserved; its production
write exceptions are intentionally withheld. Required configuration/TLS inputs
are read in place, never copied into the bundle. Only fixed validator diagnostic
classes and status are returned, not arbitrary configuration/key/error content.
This establishes read-only mechanism compatibility only, not full owner-call-path
qualification. Existing publisher/finalizer/reconciler and serving entrypoints
are never executed.

Bounds: 10-second prechecks and 30-second validation runtimes, eight-second
transient startup limit and three-second stop limit; remote supervision is
240 seconds plus 30 seconds for termination, with a 295-second controller limit
and five-second kill margin. Native KillMode=control-group, no restart and
automatic transient collection bound children independently of SSH. Cleanup
stops only units claimed by this check, removes its owned directory, and checks
release integrity, executable identity, serving PID and boot continuity. A cleanup
failure is exit 125; missing final evidence is unknown, never acceptance. A lost
connection may leave the owned directory or incomplete readback; do not replay
the attempt to resolve that uncertainty.

No secondary or Pi contact, backend HTTP requests, existing service transitions,
release publication, replication changes, DNS, notifications, authentication,
browser/scan load, permanent installation or source publication is included.
Transient unit/process creation and temporary files are explicitly included, so
this is a non-activating check, not a strictly read-only inspection. The Caddy
release stream stays clean/inactive; no deployment successor is registered.

Local qualification: Bash syntax for each script, ShellCheck and explicit
canonical-style shfmt checks pass. Embedded child bytes match the sealed child;
source review checks the primary-only transport and absence of existing service
start/reload/restart commands. `run.sh --check` verifies all twelve inputs without
SSH or creating an attempt. No fixture or container was run. The single-use
`attempt` directory is absent; no execution session exists.

Upon approval, the runner creates that directory before its sole SSH call and
retains private stdout, stderr and exit status there. Authorization is consumed
by that attempt, including an admission/connection failure. A successful result
permits local owner-integration preparation only; any primary/Pi comparison
requires a separately reviewed operation.

### November 17 W-192 execution failed at admission; W-194 opened

Aaron approved the exact bundle, command and scope at the review above for one
primary-only capability check. The unchanged runner verified all twelve inputs,
created its one-use attempt directory and made its sole SSH connection. The
command completed synchronously with exit 1; no session remains active.

Hostname, fresh boot capture, accepted release/payload and all five installed
file identities passed. The assertion at sealed `inspect.sh:60` then failed:
its expected version pattern is `v2.11.4` followed by a space and suffix. The
actual version output and the `timeout 5 /usr/bin/caddy version` command status
were not retained separately. The receipt proves failure of that compound
assertion, not an installed-version change, command timeout or namespace failure.
W-194 tracks this evidence gap and local prerequisite reconciliation.

No temporary directory/unit creation, namespace check or full validation was
reached. The exit trap reported cleanup/continuity status 0: boot, accepted
release link, manifest identity and payload integrity remained valid. Binary
hash and serving PID admission had not run, so their conditional exit checks
were skipped; effective unit properties and service-active checks also were not
reached. Do not describe these unperformed checks as passing. No existing
service transition, secondary/Pi contact or configuration change was requested.

Private evidence remains under the unchanged bundle's `attempt/` directory;
`execution-summary.json` records the limited result, and `EXECUTION.SHA256SUMS`
binds it and the three raw receipts. The sealed inputs and input manifest remain
unchanged. Approval is consumed. W-191 remains partially qualified/unintegrated;
no target isolation capability or Webmin acceptance is established. Reconcile
locally before defining any separately authorized successor; no retry, further
inspection, rollout or publication is authorized.

### November 17 W-194 version-admission reconciliation and local correction

The retained owner `Caddy/manifests/reproducibility-production.yaml` records the
August 24 package inventory's Caddy version as 2.11.4. W-191's local container
returned a version plus module checksum. Neither establishes the primary's
November 17 CLI output. The failed receipt contains no output or independent
version-command status; local analysis cannot recover either value.

Pinned upstream `caddyserver/caddy` v2.11.4 `caddy.go`, function `Version()`,
initializes the full version to the module version and adds a space/checksum
only when the module sum is nonempty. A build suffix is optional. The prepared
check incorrectly made that suffix mandatory. A separate scalar reproduction
also shows that its command substitution discards a nonzero command status:
matching stdout can pass even when the version command fails. These are proven
admission defects, not proof of the historical target failure's cause.

Private `version-admission-w194/version-admission.patch` changes only the version
admission block of the consumed `inspect.sh` for future use. It preserves the
five-second timeout and exact v2.11.4 requirement, accepts the bare version or
existing space-delimited build suffix, requires successful command exit, and
rejects empty, oversized, multiline or control-character output. The report
retains expected version, command status, observed length and an escaped prefix
bounded to 256 bytes under the C locale. It does not bypass binary/serving-process,
configuration, host or service checks. No installed identity is changed.

Twelve scalar cases passed: bare/suffixed exact version, wrong version, lookalike
prefix, empty output, failed command with matching output, timeout, failed bare
version, multiline/control output, oversized output and unknown version. The
unchanged old gate reproduced rejection of a bare version and acceptance of a
failed command with matching text. The patch was applied only to a disposable
local copy for full-script Bash syntax, ShellCheck and canonical-style shfmt
checks; that copy was removed. No Caddy process, namespace, container, systemd,
SSH or homelab workload was invoked. This is admission-contract qualification,
not target capability evidence or a substitute capacity test.

Private evidence: `/home/aaron/code/.local-evidence/uptime-kuma/version-admission-w194/`
contains the patch, scalar gate, qualification results, provenance and hashes.
The consumed bundle's input and execution checksums still pass. W-194 local
reconciliation is resolved; historical attribution remains unknown. No successor
is defined or sealed, and no retry, fresh inspection, rollout or publication is
authorized. All local commands ended; no execution session remains active.

### W-195 exact primary-only capability successor for review

Bundle:
`/home/aaron/code/.local-evidence/uptime-kuma/validation-capability-review-26haozu7`.
Fourteen inputs bind the corrected collector, unchanged runner/namespace child,
current reviewed plan and owner inputs, scope, W-194 patch and qualification.

`INPUTS.SHA256SUMS` SHA-256:
`d7fc9c4454eea84f010b547ca8aef491dbcaeac2a9438890d189b0d91b633813`.
Runner SHA-256:
`1737c3be2e6db5358f1011c0eb3ffffed71019e93fd3fc3239a4ea12d374e045`.
Collector SHA-256:
`d736fb1e3e528ae32a200349ef5cbd824aab435b431d39768891a8311ba8478b`.

Exact command, **only after separate one-attempt authorization**:

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/validation-capability-review-26haozu7/run.sh --run-approved-once
```

This is a new, unexecuted successor to the consumed W-192 attempt, not a replay.
Its sole executable change is W-194's version block: C locale, independent command
status, bounded escaped observed output and exact v2.11.4 with optional build
suffix. Failed commands and malformed output stop admission. Historical failure
attribution remains unknown. Owner inventories and the proposed helper reference
match current local source; no installed-state change is inferred from that match.

Scope remains the [W-192 primary-host capability plan](PLAN.md#primary-host-validation-capability-check-w-192-prepared-scope)
and its detailed earlier review. One SSH session as `pi` to `10.1.0.53`, native
hostname `j1-svpihole0`, strict retained host keys and existing sudo authority.
Admit fresh boot, exact accepted release/payload and installed owner identities,
version, binary/serving-process identity, effective service controls and health.
Then at most six sequential, temporary validation-only units: namespace/access
checks for root publisher, caddy-sync finalizer and restricted root reconciler,
followed by full validation in those contexts only if every precheck passes.
No real publisher/finalizer/reconciler entrypoint executes. No privilege additions
or networked fallback. Production inputs stay read-only; reconciler write
exceptions are withheld, so a pass proves mechanism compatibility only.

Bounds remain 10 seconds per namespace/access check, 30 seconds per validation,
eight-second unit startup and three-second stop limits; 240-second remote
supervision plus 30-second termination margin; 295-second controller supervision
plus five-second kill margin. Owned transient names derive from the single private
`/run/caddy-validation-capability.<nonce>` directory. Cleanup stops only owned
units, removes that directory and checks admitted boot/release/binary/PID
continuity. Cleanup failure is exit 125; missing evidence is unknown, not success.
Admission failure still consumes this attempt. No retry or additional inspection
is included, including after connection loss.

No secondary/Pi contact, backend HTTP, replication or release changes, existing
service transitions, DNS, notifications, authentication/browser/scan workloads,
installation, deployment or source publication is authorized by this review.
Temporary process/unit/file creation is part of the proposed scope; this is a
non-activating capability check, not strictly read-only inspection. The Caddy
release stream remains clean/inactive, with no deployment successor.

Local qualification passed all twelve cases against the version block extracted
from this exact collector, Bash syntax/ShellCheck/canonical-style shfmt for the
four shell inputs, embedded-child equality, unchanged runner/transport/deadlines,
current owner-input equality and `run.sh --check`. No fixture/container or target
command ran. The attempt directory is absent. Both predecessor input and receipt
manifests still verify; consumed bytes remain unchanged. All local checks ended;
no execution session is active. No commit, push or live authority is requested
beyond the exact one-attempt capability scope above.

### November 17 W-195 execution stopped on observed version mismatch

Aaron approved the exact fourteen-input successor for one primary-only capability
check. Inputs verified unchanged; its single-use runner made one SSH connection
and completed synchronously with exit 1. No execution session is active.

Host, fresh boot capture, accepted release/payload and all five installed owner
file identities passed. The corrected version report retained command status 0,
55 bytes of output and version `v2.11.9`, with its module checksum in the private
receipt. The exact `v2.11.4` requirement failed at sealed `inspect.sh:67`. This
attempt's failure is an observed version mismatch, not a suffix/parser failure,
timeout or namespace failure. It does not recover the earlier attempt's lost
output, establish upgrade timing, or identify the running Caddy process version.

No namespace, temporary directory/unit or validation phase started. The exit
trap passed boot continuity, release-link/manifest identity and payload checks.
Binary hash and serving PID admission had not run; their conditional exit checks
were skipped. Effective service controls and active-state checks were also not
reached. No existing service transition or configuration change was requested.

Private `validation-capability-review-26haozu7/attempt/` retains raw stdout,
stderr and status. `execution-summary.json` records the limited result and
`EXECUTION.SHA256SUMS` binds all four receipts. Input hashes remain unchanged;
the original consumed capability bundle is also preserved. W-196 requires local
owner-baseline reconciliation before another candidate. The observed executable
version is not an accepted inventory update or proof of capability compatibility.
Do not replace the expected pin merely to obtain admission. W-191 remains partial
and unintegrated; W-147/AC-013 remain open and W-157 is not installed. Approval
is consumed; no further inspection, retry, rollout or publication is authorized.

### November 17 W-196 operator-confirmed production version reconciliation

Aaron confirmed Caddy was updated on production hosts and requested the current
production version in inventory. Updated owner `reproducibility-production.yaml`
to 2.11.9 with explicit provenance: Aaron's fleet confirmation plus W-195's Node A
CLI/status evidence. Node B and package version are operator-confirmed; no fresh
paired capture or running-process identity is claimed. The August 24 full-package
digest/equality are retained as historical fields, with current complete-package
hash/equality unknown. Other retained observations are not silently refreshed.

Updated the dependent current-live-state manifest hash, owner history and
reproducibility documentation, and the future capability prerequisite in PLAN.md.
No runtime file, installed tool hash, accepted release identity or consumed bundle
was changed. W-196 baseline reconciliation is resolved; capability/owner integration
remain pending. A successor must bind the revised inputs and retain fresh binary,
serving-process, configuration, health and continuity checks. No new operation,
live inspection, retry, rollout or publication is authorized by this inventory edit.

Validation: YAML, Markdown, whitespace, deployment lifecycle and accepted-live
hash policies pass. The first neutral-successor check exposed the expected stale
state hash after inventory edits; refreshed the inactive specification/registry
state bindings and outer specification pin. The neutral-successor policy and
outer Bash syntax then passed. No operation was activated or runtime behavior
changed; the runner edit changes only its inactive-specification identity.

### W-197 exact primary-only capability bundle for review

Bundle:
`/home/aaron/code/.local-evidence/uptime-kuma/validation-capability-review-upci2q6g`.
Fourteen inputs bind current owner inventories and PLAN.md, runner, collector,
namespace child, retained host keys, installed-file expectations, helper reference,
scope, minimal version-baseline patch and local qualification.

`INPUTS.SHA256SUMS` SHA-256:
`68f2f8ec7282893dfa4adb0ee5cdf83b2126ee88b37293b4bbcc0aac4ce90c16`.
Collector SHA-256:
`3fc6375b396e255ef4fbd239bdbff10796b572782be2bda70c2079b465de4832`.
Runner SHA-256:
`1737c3be2e6db5358f1011c0eb3ffffed71019e93fd3fc3239a4ea12d374e045`.

Exact command, **only after separate one-attempt authorization**:

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/validation-capability-review-upci2q6g/run.sh --run-approved-once
```

The executable delta from consumed W-195 is exactly three version literals:
2.11.4 becomes 2.11.9 in expected-output reporting and exact version admission.
W-196 supplies owner confirmation and retained primary CLI evidence. Admission
still requires command success, bounded safe output and the exact version token;
build suffix remains optional. This does not pre-accept the running process,
namespace capability or installed service controls. Current state/inventory hashes
and plan are refreshed; accepted installed-tool/release identities are unchanged.

Scope: one SSH session as `pi` to primary `10.1.0.53`, native hostname
`j1-svpihole0`, using retained strict host keys and existing sudo authority.
Fresh boot continuity, accepted release/payload, five installed owner-file hashes,
version, executable/running-process identity, effective unit properties and service
health gate progression. At most six sequential temporary units first check
namespace isolation and file access for root publisher, caddy-sync finalizer and
restricted root reconciler, then validate the exact accepted configuration once
per context only after every precheck passes. No real owner entrypoint executes.
No privilege addition, networked fallback or production write is allowed.
Reconciler write exceptions remain withheld; success supports read-only mechanism
compatibility and local owner-integration preparation only.

Bounds and cleanup are unchanged: 10-second prechecks, 30-second validation,
eight-second unit startup and three-second stop limits; remote supervision
240 seconds plus 30 seconds for termination, controller 295 seconds plus five
seconds for termination. One private `/run/caddy-validation-capability.<nonce>`
directory owns transient-unit names. Cleanup stops only owned units, removes that
directory and verifies admitted boot/release/binary/PID continuity. Cleanup failure
exits 125. Missing or skipped checks are unknown, not success. The attempt directory
is created before the sole SSH call; connection or admission failure consumes
authority. There is no retry or follow-up inspection within this scope.

Excluded: secondary/Pi contact, backend HTTP, release publication, replication
changes, existing-service transitions, DNS, notifications, login/browser/scan
workloads, installation, rollout and source publication. Temporary files/processes
and validation units are included, so this is a non-activating check, not strictly
read-only inspection. The Caddy deployment stream stays clean/inactive.

Local checks pass on the exact candidate: twelve extracted version-gate cases
(including rejection of the previous version, command failure, timeout and unsafe
output), Bash syntax, ShellCheck and canonical-style shfmt for all shell inputs,
embedded-child identity, exact executable-delta review and `run.sh --check`.
Both consumed input and execution manifests still verify unchanged. No fixture,
container or target workload ran; the new attempt directory is absent. No target
capability result is claimed. All local commands completed; no session is active.

### November 17 W-197 primary-host capability check passed

Aaron approved the exact fourteen-input bundle for one primary-only capability
check. Input integrity passed; one SSH session ran the sealed collector. Session
84010 completed with exit 0 and is retired. No other execution session is active.

Admission passed hostname, fresh boot capture, accepted release/payload and all
five installed owner-file identities. Caddy reported v2.11.9 with status 0. Its
on-disk binary hash matched the serving process executable. Effective reconciler
properties, required node environment and serving/replication service state
passed. The private receipt retains binary, namespace and account identities.

All three namespace/access prechecks passed before validation: root publisher,
caddy-sync finalizer with existing caddy-tls group access, and restricted root
reconciler. Root retained its user namespace; finalizer used current-user mapping.
Every child had a distinct network namespace, no external interface and no routes,
and could read the required accepted configuration/TLS files with payload hashes
intact. Each context then completed full validation with status 0. Fixed diagnostic
classes included network-unreachable and valid-configuration messages. The retained
report does not attribute individual unreachable requests; namespace isolation and
successful validation establish the scoped result without external routing.

All six temporary units completed and were collected. The owned scratch directory
was removed; final cleanup and boot/release/binary/serving-PID continuity passed.
No production files were written or existing services transitioned. No secondary,
Pi, backend HTTP, DNS, replication mutation, browser or scan workload was included.

This resolves W-192/W-197's bounded capability question on the actual primary.
It does not qualify writable reconciler execution, complete owner-call-path or
deadline integration, future builds, or Webmin capacity/timeout causation. The
proposed helper remains uninstalled and unintegrated. W-191 continues with local
integration preparation under the existing owner path, preserving validation,
normal runtime health checks, privileges and fail-closed behavior.

Private evidence remains in `validation-capability-review-upci2q6g/attempt/`;
`execution-summary.json` and `EXECUTION.SHA256SUMS` bind the observed scope and
raw receipts. Both earlier failed capability bundles remain unchanged. Approval
is consumed. No additional inspection, retry, rollout, primary/Pi comparison or
publication is authorized. W-147/AC-013 remain open; W-157 is not installed.

### November 17 W-198 local caller integration qualified; W-199 remains

The existing publisher, finalizer and reconciler each replace their one direct
validation invocation with `/usr/local/libexec/validate-caddy-isolated.sh` and the
same absolute Caddyfile path. Existing CADDY_CONFIG_ROOT/node environment, error
handling and reload/runtime-health code remain unchanged. The helper uses the
namespace flags qualified by W-197; only its preparation comment was reconciled.
No new wrapper, transaction or test framework was added. Its future-task lifecycle
remains explicit: the helper is not installed and callers must not be deployed
without their separately governed helper delivery and prior-state recovery.

The existing isolation test now has a host-only `--caller-contracts` mode, invoked
by the existing receiver/finalization regression. It extracts the real three
caller boundaries and uses a private stand-in only for the fixed helper executable.
Twelve cases verify one exact path argument (including spaces), expected inherited
configuration/node environment, success, validation failure, timeout exit status,
missing-helper failure and finalizer temporary-error cleanup. Publisher/reconciler
retain their existing normalized failure status; finalizer retains validator status.
This does not execute complete release transactions or prove process termination.

The current-synchronization host profile passed, including its registered host
regressions/policies. Canonical formatting, ShellCheck/Bash syntax, readonly-local
collision, lifecycle, accepted-hash, neutral-successor, documentation, YAML and
whitespace checks passed. The container-only candidate-drain branch explicitly
reported deferred; no container or native validation was launched. W-197 supplies
actual-target mechanism evidence; root fixture repair was not reopened. vexp
completion verification was unavailable from the parent non-Git workspace; it
provided no verification claim. Repository checks are the local evidence.

Production/runtime manifests refresh only repository-source hashes. Deployed
hashes and accepted release identities remain unchanged. Neutral state/specification
bindings are refreshed with the operation inactive. The shared onboarding guide
records the fixed root:root:0755 helper requirement, util-linux dependency,
installation-before-caller ordering and recovery prerequisite. No caller-only
rollout is safe; W-199 owns exact delivery, restoration and deadline integration
within the existing owner machinery before a controlled target comparison.

Private `caller-integration-w198/qualification.json` binds source hashes and the
host log. Session 53896 exited 0 and is retired. Changes are uncommitted; consumed
bundles and receipts are untouched. W-191 remains in progress, W-147/AC-013 open
and W-157 uninstalled. No live contact, retry, operation sealing or publication
occurred or is authorized by this local work.

### November 17 W-199 owner delivery/restoration bindings prepared

Local source review identifies the minimum primary payload addition: the isolation
helper, finalizer and reconciler. The publisher already runs from the primary
payload; its installed copy does not need replacement. Finalizer and reconciler
currently execute installed files. PLAN.md records the four exact source hashes,
the two accepted installed hashes, helper path/mode, required prior-state capture
and recovery ordering. Accepted inventories and all consumed inputs remain unchanged.

The installed reconciler's retained source differs from the candidate in the
validation invocation and a self-test directory label only; the label change is
not production execution. The future trial must keep full validation and runtime
health settings, installed unit restrictions and privileges. Tool payloads remain
primary-only; no secondary delivery or release replication is added.

A concrete integration gap was found: publisher validation requires the helper
before it can produce a candidate ID, while the existing outer failure branch
requires application-target.tsv to enter trial restoration. Installation cannot
be inserted there without a tool-only recovery branch. The prepared contract
requires verified backups and independently recorded file changes, restoration
without a target ID, phase-specific candidate versus baseline identity checks,
and restoration before service resume. It forbids synthesizing a target ID or
claiming no mutation from absent output. Existing 240-second forward and
840-second aggregate limits cover these steps; neither is extended.

The shared onboarding guide records this reusable requirement. No new installer,
operation specification, test framework or fixture was introduced. W-199 remains
in progress until the existing payload/transaction/outer implement and qualify
these prepared bindings. Source review is not execution qualification. W-197's
read-only capability and W-198's caller tests remain scoped evidence; W-147's
historical timeout and AC-013 remain unresolved. W-157 is not installed.

Qualification for this preparation: all four source hashes and both accepted
installed hashes match the current files/owner manifest. Markdown lint, owner
documentation policy, neutral successor policy and whitespace checks pass. No
executable source changed this turn, so no runtime/fixture test was added or
repeated. Changes remain uncommitted; no live contact, retry, sealing, rollout or
publication occurred. All commands completed synchronously; no session is active.

### November 17 W-199 delivery and pre-release recovery locally qualified

The existing outer payload builder now accepts a hash-bound primary-only validation
trial option and verifies all three added tool sources. It includes the helper,
finalizer and reconciler with the staged publisher on Node A. The secondary control
archive still contains only the recipe; diagnostic dispatch never contacts Node B.
The inactive recipe remains empty and no successor is registered.

The existing transaction admits the original caller hashes and absent helper,
rejecting symlinks, hard links, unsafe metadata and unsupported ACLs/xattrs. It
retains checked originals and metadata under its protected payload before mutation,
then stops sender/reconciler activity and waits for receiver inactivity. The helper
is installed first at root:root:0755; caller replacements preserve their original
permissions/ownership. Candidate hashes are verified. Python 3 is declared as an
existing dependency; the trial does not install packages or alter service units.

An explicit empty application-target.tsv is written before tool installation.
On a failed primary phase, the outer accepts that empty receipt only for the bound
primary diagnostic; missing/malformed receipts still stop. Recovery restores
callers before removing the helper, then verifies the unchanged baseline release,
prepared and sync inventories before resuming. A new unexplained prepared release
or changed installed file prevents acceptance; backups remain retained. Absence
and an empty prepared directory are equivalent. Failure before the backup-ready
marker causes no service transition. Later release failure retains the existing
release restoration before tool restoration. Failed restoration prevents resume.

All transfer, installation and recovery calls remain inside the existing forward
and aggregate deadlines and remote process-group bounds. No new timer, service,
transaction framework or fixture-capacity test was introduced. Future live inputs
must bind these sources and the metadata/dependency admission; local tests do not
prove writable systemd execution, actual completion time or target capacity.

The application-onboarding host profile passes. Its existing regression now runs
fifteen real-filesystem cases through the extracted current payload/transaction
functions: full install/restore, publisher failure before a release ID, each partial
replacement, interruption, backup failure, unexpected helper, tampered payload,
failed restore, foreign caller/prepared state, unsupported xattrs, later request
failure and absent prepared directory. Privileged paths/ownership are mapped to a
private local directory; service control/process lookup are stand-ins. Existing
primary-only dispatch now also rejects an empty target without opt-in and recovers
it with opt-in. Probe, monitor and aggregate budget contracts continue to pass.

Bash syntax, ShellCheck, canonical formatting, readonly/local collision, accepted
hash/neutral successor/test-lifecycle policies, owner documentation policy, YAML,
Markdown and whitespace checks pass. A dependency-list indentation mistake was
caught by YAML validation and corrected before completion. No target or container
was contacted. Neutral transaction/specification hashes were refreshed; accepted
production hashes, consumed bundles and the notifier installation state are unchanged.

Private evidence: `validator-delivery-w199/host.log`, `host.status` and
`qualification.json` under the existing private evidence root. Session 23150 exited
0; static-check session 31934 exited 1 for the corrected YAML error. Earlier local
sessions 54747, 57932, 32405 and 14983 completed and are retired. No session remains
active. Changes are uncommitted; no publication or live authority follows.

### November 17 W-200 primary/Pi candidate prepared; sealing withheld

Prepared the private draft at
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-isolation-candidate-xbe0nu5s`.
The proposed owner recipe binds current publisher, fragment, helper, finalizer and
reconciler hashes, original installed caller hashes, and the accepted release.
It explicitly selects `validation_tools_trial=primary` with primary/IPv4 scope.
The parent inputs use a fresh workload token and operation paths. They retain the
accepted Webmin controls, guarded profile, source address, owner restoration and
240/840-second Caddy budgets. No old approval, agent socket or execution receipt
was copied as current authority. W-197 remains capability evidence only; future
live admission must independently revalidate the retained baselines.

Current source functions constructed the exact proposed primary payload and checked
its recipe/hash bindings locally. The secondary archive contains control metadata
only; there is no secondary execution in the proposed scope. Parent profile/token/
path checks and Ansible syntax passed without target contact. Session 96719 exited
0 and is retired. The candidate has no operator launcher, live input manifest or
execution command; its PREPARATION.SHA256SUMS identifies drafting artifacts only.
`review.json` states prepared-unsealed and records the exclusions and blocker.

Sealing review found a specific qualification gap. The current owner gate requires
execution coverage tied to the exact current source graph. The retained W-182
whole-path receipts correctly fail current verification with `stale or incomplete
graph`; they were not modified. More importantly, the existing whole-path suite's
recipe setup does not select W-199's validation-tool option. Running that unchanged
suite would not exercise the new installation/recovery path. Fifteen W-199 file/
recovery tests remain valid focused evidence, not complete owner execution coverage.

Resolve this through the existing owner qualification for the actual primary-only
branch, with expected/observed delivery, dispatch, pre-ID failure and restoration
results. Do not reopen target-kernel capability or capacity fixtures: W-197 already
settled the read-only mechanism on the primary, and target writable execution is
an explicit trial question. No evidence hash rewrite, synthetic success receipt,
coverage waiver or broad fixture rerun was used to obtain authorization readiness.

Caddy remains clean/inactive and its neutral policy check passes. No operation was
registered or sealed, no container or target was contacted, and no publication
occurred. Consumed attempts and accepted hashes remain unchanged. W-200 stays in
progress; W-191/W-147/AC-013 remain open and W-157 remains uninstalled.

### November 17 W-200 primary-only owner coverage completed locally

The existing application qualification now enables `validation_tools_trial=primary`
for its primary-only cases and binds current helper/finalizer/reconciler hashes.
Its focused launcher runs three cases through the real payload builder, serialized
SSH substitute, complete owner transaction, readback and restoration: successful
primary HTTPS, failed HTTP acceptance, and an injected finalizer-install rename
failure after helper installation but before any release ID. All three pass.
Independent checks require actual helper/caller identities at validation dispatch,
the empty target receipt for the installation failure, restored caller/publisher
bytes and modes, helper/stage removal, baseline release selection and no secondary
command or exposure. The failure is injected at the actual fixed-PATH rename,
not by pre-writing a transaction result.

The disposable offline fixture substitutes transport, service scheduling and only
the unavailable namespace primitive. Exact delivered helper/callers and native
Caddy validation/HTTPS execute. This does not prove isolation, real writable service
restrictions, runtime timing or Pi capacity; W-197's actual-host capability evidence
remains separately scoped. No root-isolation or load fixture was repeated.

Private retained evidence is `w200-primary-tools-qualified` beneath the existing
Uptime Kuma evidence root: `result.json`, `primary-tools-summary.json`, raw case
receipts, `host.log` and `verifier-negative-tests.json`. The current graph and raw
effects verify again after preservation. Four private-copy mutations (stale graph,
missing option, altered restored caller and missing dispatch) reject; the restored
control passes. The application-onboarding host profile, neutral successor policy,
test lifecycle and whitespace checks pass.

Earlier runs remain at `/tmp/caddy-application-qualification-t4v_o6z2`,
`/tmp/caddy-application-qualification-99lr4akt` and
`/tmp/caddy-application-qualification-05x1aj23`. They exposed only test-adapter
integration gaps: non-root finalizer dispatch and fixed-PATH fault injection.
Those runs are not relabeled. Final run
`/tmp/caddy-application-qualification-rvcuqk_z` passed and its container cleanup
returned zero. Sessions 47561, 6211 and 92116 exited 1; 2515 and host-check session
27272 exited 0. All are retired.

The new focused summary deliberately cannot pass the full authorization gate;
no old receipt was relabeled or gate waived. Exact candidate/authorization coverage
bindings still need reconciliation before sealing. W-200 remains in progress for
that boundary. No production executable changed in this step, no helper/caller
was installed, and no target contact, successor registration, sealing or publication
occurred. W-191/W-147/AC-013 remain open; W-157 is not installed.

### November 17 W-200 exact candidate authorization bindings reconciled

The existing owner gate had required paired onboarding evidence for a diagnostic
that cannot expose or contact the secondary. It now selects the explicit
`primary-validation-diagnostic` profile only when the definition binds the single
primary, exact Webmin fragment/login request, validation-tool hashes and existing
240/660-second recipe limits. Unknown profiles, broadened targets, missing tool
delivery, changed family, budget or helper identity reject. Paired onboarding keeps
its full case set. This is proportional coverage selection under the approved
primary-only scope, not a waiver of recovery or identity checks.

The private review at `webmin-isolation-candidate-xbe0nu5s` now retains an exact
owner projection under `owner-workspace`, its graph in `OWNER-CANDIDATE.SHA256SUMS`,
and fresh execution in `owner-authorization-evidence`. Three complete owner cases
pass: successful request, failed HTTP acceptance and partial install before a
release ID. The existing `--authorization-ready` gate passes against those exact
bytes after private preservation. It rejects nine evidence mutations, including
stale graph, changed status, missing option/dispatch/decision/readback, changed
restored caller and symlinked evidence. Six separate profile/recipe mutations
reject. Earlier focused and consumed receipts are unchanged; no summary was renamed
or relabeled as current authorization evidence.

The parent now points to the private owner projection and its accepted local
qualification evidence. Its primary/Pi inventory, diagnostic-only flags, original
limits, fresh token/paths, fixed recovery and exclusions are unchanged. The live
input-manifest path remains uncreated, operator readiness remains false by default,
and no live launcher is present. `owner-binding-review.json` records exact owner
and parent hashes; `authorization-ready.log` records the owner gate. Local gate
success is preparation evidence, not user authorization or writable target acceptance.

The first private-projection run failed because the non-root fixture adapter could
not read owner-private source. The adapter now forwards that caller's commands to
the native validator/rename programs without opening private directories or adding
privileges. That failed evidence remains at
`/tmp/caddy-application-qualification-2sgsdz8v`; session 82676 exited 1. The corrected
run `/tmp/caddy-application-qualification-uewq4fzd` exited 0 (session 88716), all
owned-container cleanup passed, and its evidence was preserved. Copy session 31654
exited 0. No namespace/capacity fixture was added or used to accept the target.

Parent syntax, current host qualification, shell syntax/lint/formatting/collision,
neutral owner policy, documentation and whitespace checks are recorded in the
private review. The main stream and accepted installed identities remain unchanged.
Only the review projection is defined; no main operation was registered and no
live bundle was sealed. W-200 remains in progress for sealing and separate live
review. W-191/W-147/AC-013 remain open; W-157 remains uninstalled.

### November 17 W-200 sealed primary/Pi diagnostic — approval required

The exact qualified owner definition is registered locally as
`20261117-webmin-isolated-validation-diagnostic`. The main stream is now defined;
accepted installed identities are unchanged. The frozen private owner projection,
parent inputs and qualification receipts are the execution inputs. No live authority
is implied by registration or a passing authorization-readiness gate.

The final lifecycle check caught the predecessor archive tag in the new defined
stream row. That field is now neutral in both main and the private projection;
the published archive and historical record remain preserved. No executable or
qualification graph changed. The final manifest was regenerated before review.

**Exact bundle and command for one attempt:**

- Private review: `/home/aaron/code/.local-evidence/uptime-kuma/webmin-isolation-candidate-xbe0nu5s`.
- Manifest: `INPUTS.SHA256SUMS`, 260 regular inputs.
- Manifest SHA-256: `1688b2b2cb8191151013debd757eb1ee3d4a29f69a1d725b54e6fc6d396fde7a`.
- `scope.json`, `launch.json`, parent inputs, owner sources, raw qualification
  evidence and non-secret execution dependencies are bound. `sealed-inputs-index.json`
  and private copies retain the input bytes. Existing SSH-agent credentials remain
  external; no password or key material is collected.

```bash
/usr/bin/python3 -I -B /home/aaron/code/.local-evidence/uptime-kuma/webmin-isolation-candidate-xbe0nu5s/operator.py --manifest-sha256 1688b2b2cb8191151013debd757eb1ee3d4a29f69a1d725b54e6fc6d396fde7a --run-approved-once
```

**Targets and temporary changes:** only `ama@10.1.3.75` and `pi@10.1.0.53`.
Temporarily apply the guarded Webmin backend profile and primary route. Deliver the
isolated validator helper before its finalizer/reconciler callers, after preserving
verified originals; keep the publisher payload-local. Stop before replication.
Compare marked direct/proxy IPv4 login-page requests using the neutral User-Agent
and unchanged HTTP-200/login requirement. Retain received headers, boundary timing,
health-probe overlap, clock uncertainty and bounded resource deltas. Boundary events
do not establish internal CGI execution or full response-body completion.

**Stop and recovery:** fail closed on identity/configuration drift, failed isolation
or file access, request/evidence failure or deadline. Restore both owners regardless
of request outcome, including failures before a release ID exists. Restore original
callers before removing the helper, then verify release/selection, loopback backend
and primary natural monitor acceptance. Preserve incomplete recovery as a failure;
no automatic replay. Forward work remains 240 seconds; recovery/monitor/readback
share the 840-second aggregate cutoff, within the 1200-second child bound. The
sampler remains 300 seconds and independent backend recovery 1800 seconds. Resource
limits, normal runtime health checks and existing privileges remain unchanged.

**Excluded:** secondary contact/exposure, replication progression, DNS, private
login/browser/WebSocket/graphs, scans, reboot/failover, privilege additions,
networked validation fallback, notifier installation, permanent promotion and
publication. No private operator password or timed browser check is required.

**Local qualification:** final sealed `--verify-only` passes without target contact;
exact owner authorization readiness, deployment-window and lifecycle checks pass.
The unchanged launcher's local tests cover success/failure, non-consuming preflight,
replay rejection and drift rejection. Existing fresh three-case owner execution,
nine evidence negatives and six scope/recipe negatives remain bound; no fixture
expansion or capacity/root-isolation repetition occurred. Private logs retain the
checks. No attempt marker exists and all commands completed synchronously.

W-200 preparation is complete for review. W-191 writable delivery, W-147 timeout
attribution and AC-013 remain unaccepted. Approval must explicitly cover this bundle,
command and scope for one attempt; no live contact or publication occurred.

### November 17 W-200 approved attempt stopped before Caddy (W-201)

Aaron approved the exact bundle and scope at the preceding review section for one
primary/Pi diagnostic attempt. The launcher verified the sealed 260-input manifest
and exact owner authorization gate, created its exclusive attempt marker and ran
once. Session 94634 completed with parent exit 2; it is retired. The original
manifest, inputs, attempt marker, parent.log and parent.exit remain unchanged in
`webmin-isolation-candidate-xbe0nu5s`. Approval is consumed; do not replay.

Pi host/service-control admission passed. The parent staged the guarded backend,
saved the baseline, armed independent recovery and applied the temporary backend
profile. Pre-operation clock capture then returned FileNotFoundError. The configured
controller output directory `inputs/evidence` is absent. Later writes of the
pre-restoration snapshot and final parent-owner outcomes explicitly failed because
that directory does not exist. Source inspection confirms clock capture writes its
receipt there; the historical remote clock values were not retained. Do not infer
successful clock results from the error alone.

The parent continued mandatory backend recovery: native restore returned success,
private state read succeeded, the assertion requiring phase `restored` passed and
only then was the recovery timer stopped. This is recovery evidence in the retained
Ansible log, not a separately persisted recovery receipt. The final owner-outcomes
write failed and later combined terminal/boot checks were not reached. No further
inspection was performed to fill that evidence gap.

Caddy's child was never launched. Its definition remains unexecuted; no primary
tool installation, route publication, request comparison, sampler, browser or scan
workload ran. Clock capture may have contacted the primary within approved scope;
this is not a claim of zero primary contact. No Caddy restoration was needed and
no monitor-cycle acceptance was performed in this attempt. W-191 remains pending,
W-147 has no new request evidence, AC-013 remains pending and W-157 is not installed.

W-201 owns the local output-directory admission and receipt-persistence correction.
Reconcile the unexecuted child/parent lifecycle before any separately reviewed
successor. Do not broaden fixtures, create the missing directory and replay, or
change the consumed bundle. No publication or further live action is authorized.

### November 17 W-201 controller evidence admission corrected locally

The parent had no storage admission before native backend preparation. Its existing
flow test supplied an already-created temporary directory and substituted clock
capture, so it did not exercise the missing-output-directory boundary. The frozen
attempt's missing directory explains the repeated receipt-persistence failures;
its unretained remote clock results remain unknown.

The existing handoff helper now admits a prepared absolute controller-owned
mode-0700 directory, rejecting missing, file, symlinked and non-private paths.
It exercises the existing exclusive JSON receipt writer and private readback in
a disposable child, then removes only that probe. The parent calls admission after
manifest verification and before its first target command. It neither creates nor
repairs an operation directory at runtime. The fleet onboarding procedure now
requires preparing that private output directory before sealing. Later disk or
permission failure is still possible; the original parent log remains fallback
evidence and mandatory native recovery is unchanged.

The real localhost Ansible admission task passed six cases (missing, file,
symlink, public mode, read-only mode and valid private storage). Negative cases
stop before a simulated target step. The actual writer's injected error propagates
and its disposable probe is cleaned up. Three existing primary-only parent cases
and the original clock-before-failure scenario pass after including admission;
recovery runs and terminal outcome receipts persist. These tests check controller
storage/sequencing only, not target capacity, namespace capability or HTTPS.

Private `w201-controller-storage` retains source hashes, test logs and qualification
summary. Initial sandbox runs 39558/36071 exited 1 because Ansible's local RPC
server could not start; they are not acceptance evidence. Localhost-only rerun
23287 and clock-failure run 54516 exited 0 outside that restriction. The vexp
completion helper was unavailable from the parent workspace; focused owner tests
and whitespace checks were used. All sessions are retired.

All 260 consumed input hashes still match their original manifest. The Caddy
child never launched and its existing definition is preserved, not marked as an
executed terminal operation or reused as new authority. Future source/binding
reconciliation must precede a new seal and review; this change does not authorize
replay. W-201 is locally resolved. W-147/AC-013 remain pending, W-157 remains
uninstalled, and no live contact or publication occurred.

### November 17 W-202 parent successor and unexecuted child reconciliation

The failed parent never launched its Caddy child. Retain the same single
`20261117-webmin-isolated-validation-diagnostic` definition; it is unexecuted,
not a consumed Caddy terminal operation. No Caddy terminal tag or second stream
is created. The failed parent, its exclusive attempt marker, original 260 inputs
and recovery log remain unchanged. Its approval cannot authorize this successor.

The Caddy recipe, operation, transaction, runner and complete qualification graph
match the previously qualified bytes. The actual owner gate passes against the
original `webmin-isolation-candidate-xbe0nu5s/owner-authorization-evidence` with its
provenance intact. That evidence is hash-bound in the new manifest; it is not
relabeled as fresh execution. W-201 changed the parent/handoff and their tests,
not the child graph, so no owner fixture, capacity or root-isolation rerun was
needed. Future target admission still revalidates current state independently.

The new private parent has fresh paths/token and prepared controller-owned 0700
`inputs/evidence`. Its frozen source includes W-201. The exact parent tasks before
first target contact ran locally: seven passed, zero changes, one non-applicable
browser task skipped. This exercised scope binding, actual Caddy authorization,
manifest verification and real storage receipt writer/readback. Full parent syntax,
owner window/lifecycle policies and sealed launcher preflight pass. Session 98073
exited 0; no target task, SSH, container, browser or service operation ran.

**Exact W-202 bundle, command and scope — separate live approval required:**

- Private review: `/home/aaron/code/.local-evidence/uptime-kuma/webmin-storage-review-jbd4aw5t`.
- Manifest: `INPUTS.SHA256SUMS`, 263 regular inputs.
- SHA-256: `3c7a91105fcdb02f551dc15fd2b65c3227dd3592fe6b689c16a56d1667e2b88c`.
- Exact frozen inputs, metadata, original owner evidence and W-201 qualification
  are bound; private sealed copies retain their bytes. Credentials remain external
  through the existing agent. No new password or browser attendance is required.

```bash
/usr/bin/python3 -I -B /home/aaron/code/.local-evidence/uptime-kuma/webmin-storage-review-jbd4aw5t/operator.py --manifest-sha256 3c7a91105fcdb02f551dc15fd2b65c3227dd3592fe6b689c16a56d1667e2b88c --run-approved-once
```

One attempt on `ama@10.1.3.75` and `pi@10.1.0.53` only. After controller storage
admission and target identity/configuration checks, temporarily apply the guarded
Webmin backend profile. Preserve original primary callers, install the isolated
validator helper before finalizer/reconciler, and keep the publisher payload-local.
Temporarily activate the primary route and compare equivalent marked direct/proxy
IPv4 login-page requests with the neutral User-Agent and unchanged HTTP-200/login
contract. Retain bounded received headers, network-boundary timing, health-probe
overlap, clock uncertainty and resource deltas; do not infer CGI execution,
full-body completion or timeout causation from boundary observations alone.

Stop on drift, failed isolation/access, failed request/evidence or deadline.
Restore both owners regardless of comparison outcome, including pre-release-ID
failure. Restore callers before removing the helper; verify original selection,
backend loopback and primary natural monitor acceptance. Report incomplete recovery
without replay. Forward work remains 240 seconds; recovery/observation/readback
share the aggregate 840-second cutoff, within the 1200-second child bound. Sampler
300 seconds and independent backend recovery 1800 seconds remain unchanged, as do
resource caps, existing privileges and normal runtime health checks.

No secondary contact/exposure, replication progression, DNS, authentication,
browser/WebSocket/graphs, scan, reboot/failover, privilege additions, networked
validation fallback, notifier installation, permanent promotion or publication.
The new attempt marker is absent, output directory empty and all original consumed
hashes still match. W-191 writable execution, W-147 attribution and AC-013 remain
unaccepted. This is a prepared review, not live authorization.

### November 17 W-202 execution — timeout with retained timing (W-203/W-204)

Aaron approved the exact 263-input bundle for one primary/Pi attempt. Launcher
admission and W-201 storage admission passed. Session 51564 ended with parent exit
2 and child exit 1; all execution sessions are retired. Approval is consumed.
Evidence is retained in `webmin-storage-review-jbd4aw5t`: parent.log/exit,
inputs/evidence, copied caddy-evidence and TERMINAL-EVIDENCE.SHA256SUMS.

Backend preparation, clock captures, actual route/source and denial checks passed.
The Caddy child installed its bound validation tools and activated its unexposed
primary candidate. The marked HTTPS request completed TLS in 0.048183 seconds,
then timed out after 5.001715 seconds with no client response (HTTP 000, curl 28).
The direct request returned HTTP 200 with first bytes about 2.307 seconds after
arrival. The proxied request reached the backend interface; its first response
bytes were observed about 7.491 seconds after arrival, after client closure. No
complete proxy response headers/status were captured. This narrows the observed
stall to delayed backend response; it does not explain why Webmin responded late
or establish CGI/full-body completion.

Clock/resource/wire correlation passed. Two health connections were recorded.
Webmin's sampled memory.current peak was 115.28125 MiB; its retained memory.events
high/max/oom/oom_kill counters remained zero, as did Kuma's. These observations
apply to this finite interval; they neither prove host capacity nor exclude all
resource effects. The result does not support treating validation isolation alone
as a demonstrated remedy for W-147. Detailed causal reconciliation remains W-203.

Primary containment, release/tool restoration, resume, disposition and readback
all returned zero. The validation-restored receipt is present. A natural monitor
cycle started after resume and completed successfully (ExecMainStatus 0); sender
PID/restart continuity passed. Native backend restore and the restored-phase
assertion passed, then its recovery timer was stopped. Parent-owner-outcomes.json
persisted successfully. Final parent acceptance rejected the nonzero Caddy result;
it did not falsely accept application success. No browser or scan workload ran.

The Caddy stream is now failed-consumed/terminal-pending with its exact executed
operation retained and deployable/coverage registries cleared. Planned tag:
`caddy-webmin-isolated-validation-terminal-2026-11-17`. W-204 owns separate archive
preparation/publication review; no commit, tag, push or cleanup occurred. Prior
consumed attempts remain preserved. W-147/AC-013 remain unresolved and W-157 is not
installed. No fresh inspection, retry, permanent promotion or publication is
authorized by this consumed approval.

### November 17 W-203 retained timing reconciliation

The two marked foreground requests have identical retained expected headers and
the same login path. Direct first payload arrived after 2.306852 seconds and HTTP
200 headers were captured. Two distinct health flows arrived about 0.177 seconds
before the proxied foreground request. Their first backend payload arrived about
7.513/7.517 seconds later; the proxied first payload arrived after 7.491 seconds.
Health clients closed after about three seconds and the foreground connection
closed after about five. These are same-interface kernel timestamps; controller
clock uncertainty is not subtracted from these local intervals.

The wire observer emits first-byte only for new TCP payload, not ACK/FIN alone.
It reported no capture issues or kernel drops. Nevertheless no complete response
headers/status or response-close was captured for the three delayed flows. Do not
call them successful HTTP responses or proof of completed CGI work. The two health
flows carry the diagnostic health marker but their process origins are not
individually proven. Their User-Agent and Accept-Encoding differ from the foreground
contract; the safe recorder retains only `unexpected`, not raw values. These fields
must not be assumed equivalent when attributing latency.

This single comparison demonstrates delayed backend-side payload after client
cancellation with overlapping health requests. It does not establish serialization,
CPU pressure, name lookup, Perl/CGI behavior or another internal cause. Memory event
counters remained zero across the sampled interval; the earlier pressure/OOM attempt
is preserved, not generalized to this attempt. W-191 isolation was exercised but
is not a demonstrated timeout remedy. No timeout or cap is changed.

`w203-reconciliation.json` retains derived intervals and limits beside original
receipts. W-203 retained-evidence reconciliation is resolved; W-147 remains open.
A next owner review should focus on simultaneous health/foreground request handling
and the health request contract, rather than another broad deployment qualification.
No new diagnostic is defined or authorized. W-204 archive preparation is separate.

### November 17 W-204 terminal archive prepared for publication review

The exact 32-file owner archive is prepared locally in
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-isolation-archive-review-si8xkvku`.
It includes pending Caddy 2.11.9 inventory reconciliation, isolated validator/caller
implementation and qualification, the executed recipe/operation, W-201 parent
storage correction, owner documentation and terminal lifecycle metadata. The
review's files.txt is the complete path list; archive.patch is the exact diff.
Twenty-seven files match bound executed source bytes; the remaining five are
history/reproducibility documentation or terminal registries/result. Raw evidence,
monitoring change records and other repositories are excluded.

**Exact W-204 archive command and scope — separate publication approval required:**

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/webmin-isolation-archive-review-si8xkvku/review-command.sh
```

- Repository/destination: `Racerx323/homelab-server-configs`, origin main only.
  The command verifies owner/repository/visibility and unchanged remote main before
  committing; no remote was contacted during this preparation.
- Base commit: `bda63a46f88620f177d01e527644625b5eb27ab2`.
- Exact candidate tree: `fc61097b68e0899d92a55d5bcb752e75c9dbb646`.
- Tag: `caddy-webmin-isolated-validation-terminal-2026-11-17` (annotated).
- File manifest SHA-256: `4c605d4c7f483c5da90980c49394675cb83b66652d9fcb9b0da702c57766dea4`.
- Patch SHA-256: `66404c6fab43b2ffeac5c21d18e8b4d5311f4165dd0bdab9f2095f83f80c2faf`.
- Command SHA-256: `4127a9c6c2305ea9beed010c08b57c43933904125eb664e85beb2031319fd943`.
- Commit/tag messages and their identities are retained in review.json; the
  temporary candidate index leaves the repository's existing index unchanged.

Authorize one commit, one annotated tag and one atomic push of those two refs.
The command checks the original index/base, exact source file hashes and candidate
tree, refuses existing local/remote tag or changed remote base, runs normal commit
hooks, checks the resulting tree, and reads remote refs after the push. A changed
input/hook-mutated tree stops for reconciliation; it does not silently rebind this
review. Approval does not include any live host operation, terminal cleanup,
private evidence publication, additional repository commit or retry.

Local checks pass: terminal window/successor/lifecycle, Bash syntax, ShellCheck,
whitespace and the repository-configured Gitleaks scan. The initial unconfigured
scan flagged five historical integrity pins in HISTORY.md; the existing owner
allowlist handles them. Both logs are preserved; no scanner policy was changed.
Existing W-200 exact child qualification and W-201 parent tests retain their
original scope/provenance. No broader fixture run was needed for this archive.

No commit/tag/push was performed. W-204 remains in progress until separately
approved publication and remote verification. Executed definitions/inputs remain
present; cleanup must follow that archive boundary. W-147/AC-013 stay unresolved,
W-157 remains uninstalled and no new live authority exists.

### November 17 W-205 publication stop and corrected continuation

Aaron approved the exact W-204 command. It ran once and stopped in the normal
`accepted-live-hash-policy` commit hook: `lifecycle_complete=false`. The terminal
result was missing from the lifecycle registry and the consumed operation still
had its earlier defined-unexecuted classification. No commit, annotated tag or
push occurred. Session 13640 exited 1 and is retired. The original review,
publication log and stopped-before-commit receipt remain unchanged.

The local correction changes only `Caddy/manifests/manifest-lifecycle.tsv` from
the approved archive: classify the operation and terminal result as
failed-consumed/non-deployable. No runtime input, executed operation or receipt
was edited. The main index still holds the original candidate; the corrected
candidate uses an explicit temporary index, not a repository in evidence storage.

**Exact W-205 publication continuation — separate approval required:**

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/webmin-archive-continuation-s06pi9x8/review-command.sh
```

- Same 32 paths, messages, repository and scope as W-204: one commit, one annotated
  tag and one atomic push to `Racerx323/homelab-server-configs` main/tag.
- Base: `bda63a46f88620f177d01e527644625b5eb27ab2`.
- Expected initial index: `fc61097b68e0899d92a55d5bcb752e75c9dbb646`.
- Corrected tree: `bec2abdf0d95e16648e6b22cc35e307b9e62b9db`.
- Annotated tag: `caddy-webmin-isolated-validation-terminal-2026-11-17`.
- File manifest SHA-256: `9f9d66b9e68cc59593c5ad88b735e79df29e37d9f9f4e23a148d1c644366c1ae`.
- Patch SHA-256: `287b3e422d97ab04aa66522ff97587fb588ef0e919ab6b4935af17235340a386`.
- Command SHA-256: `386874c9af6ab38312003eb2ca4e1f0e90c998a58bef5df312773e0618b94c46`.

The review directory contains the exact snapshots, path list, diff, message hashes
and command. It checks destination/base/tag absence, file identities and staged
and committed trees, runs normal hooks, pushes atomically and reads remote refs.
The original W-204 approval is consumed; this changed tree is not authorized.
No private evidence, monitoring records or workspace instructions are included.
No live action, terminal cleanup or replay is included.

Qualification passed: accepted-live-hash, deployment-lifecycle and successor
policies; command Bash syntax/ShellCheck; whitespace; repository-configured
Gitleaks. No fixture expansion was needed. W-204 remains pending publication.

### November 17 W-206 evidence storage Git discovery and correction

The uptime-kuma evidence root itself is not a repository. VS Code discovered
nested repositories: the W-200 qualification snapshot and its W-202 copy each
contained an unborn Git index with 71 uncommitted entries and no remote. Earlier
qualification/publication worktrees and upstream checkouts added more Git roots.
These were preparation artifacts, not unsynced evidence intended for publication.
Creating Git metadata there violated the intended evidence-only role.

Twelve discovered `.git` directories/pointer files across `.local-evidence` were
reversibly moved to
`/home/aaron/code/.local-git-metadata-archive/2026-11-17-evidence-cleanup/`.
`relocations.json` maps originals to retained metadata; `verification.json`
records that all twelve former roots are no longer Git repositories. Source,
logs and receipts remain in place. All 260/263 file hashes in both consumed
input manifests still match. External worktree registrations were preserved;
no prune or evidence deletion was performed. Historical Git-dependent checks
are not rerunnable in place and must not be replayed as consumed operations.

The scan could not enter 100 protected synthetic fixture directories; no
permission changes or exhaustive privileged scan was performed. VS Code may
retain cached entries until refresh/reload. Workspace AGENTS.md now prohibits
Git initialization, cloning, worktree creation or copied Git metadata under
`.local-evidence`, and directs Git-dependent qualification to outside workspaces
or an explicit temporary index. This rule and ledger update remain local.

### November 17 W-207 publication launcher correction

Aaron approved W-205's exact continuation. Session 48594 ran once and exited 1
before staging, commit, tag or push. The launcher mistakenly expected the final
candidate tree at the initial-index gate; review.json and the approved scope
correctly specified the original staged tree. Sequential string replacement
during preparation caused this defect. The empty log is retained; local source
inspection and unchanged index establish the mismatch. No hook or commit ran.

The corrected launcher changes only its first index assertion. The archive's
32 paths, source hashes, base, final tree, messages, tag and destination are
unchanged. Original launcher/review and failed execution receipt are preserved.
Local checks verify the actual initial index/base, all 32 source hashes, distinct
pre/post-staging assertions, Bash syntax and ShellCheck. No Git repository was
created in evidence storage.

**Exact W-207 corrected command and unchanged W-205 publication scope — approval required:**

```bash
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/webmin-archive-continuation-s06pi9x8/review-command-v2.sh
```

Command SHA-256: `367ebccb7a47872519d46fa3955082e65bd83a522b426ba282ab8339a33b678a`.
Initial index: `fc61097b68e0899d92a55d5bcb752e75c9dbb646`.
Final candidate tree: `bec2abdf0d95e16648e6b22cc35e307b9e62b9db`.
All other identities and boundaries are those in W-205 above, retained in
review.json and command-v2-review.json. Authorize one execution for one commit,
one annotated tag and one atomic push to the same verified owner repository,
with normal hooks and remote-ref readback. No live host work, cleanup, monitoring
publication or private evidence publication is included. W-205 execution approval
is consumed; the corrected command is not yet authorized.

### November 17 W-207 publication completed; W-204/W-205 resolved

Aaron approved the corrected command above. Its exact SHA-256 and review
identities were verified before one execution. Normal commit hooks passed;
commit `49867222c7a55957471d2a8a15038eeb649693f7` has the approved base parent and
exact tree `bec2abdf0d95e16648e6b22cc35e307b9e62b9db`.
Annotated tag `caddy-webmin-isolated-validation-terminal-2026-11-17` has object
`5734d995a561b0102d0e7062211a7e8e5b553372` and peels to that commit. Atomic push
completed; remote main, tag object and peeled commit match local identities.
The server repository worktree/index are clean. Remote CI was not checked.

The private review retains publication-v2.log, publication-v2-result.json and
publication-v2-session.json. Session 37873 exited 0 and is retired. Both earlier
publication failures are preserved. No monitoring change record or private
evidence was included. This local ledger/result update remains uncommitted.

W-204/W-205/W-207 are resolved. Terminal cleanup has not run; the consumed
operation remains present and must not be replayed. W-147/AC-013 remain pending,
W-157 is uninstalled, and publication grants no target/retry/promotion authority.

### November 17 W-208 Git metadata archive retired

Aaron authorized history inspection, worktree-registration reconciliation and
removal of `.local-git-metadata-archive`. Three server worktree HEADs are ancestors
of main. Two synthetic baseline commits and two Webmin review commits were absent
from their recorded remote branches. Preserved all locally present objects,
including unreachable objects, in inert packs with refs and staged patches at
`/home/aaron/code/.local-evidence/git-metadata-retirement-2026-11-17`.
Pack checksums/indexes and exact object sets verified before deletion. The Webmin
clone was partial/promisor: missing upstream objects were not fetched, and this
is preservation of local objects, not a claim of complete upstream history.

Removed the three exact stale registrations from the server repository; four
Webmin registrations disappeared with their retired metadata. Evidence/source
worktrees remain untouched. Server refs and worktree/index status compare equal
before/after. Deleted `/home/aaron/code/.local-git-metadata-archive` and verified
its absence. Recovery artifacts contain no `.git` and are not a repository.
`result.json`, relocation mapping and SHA256SUMS.json retain the audit. Local
session 85779 exited 0; no session remains active. No publication or host work.

### November 17 W-209 retirement directory audit and deletion

Aaron requested an audit for deletion and reconciliation of anything needed into
its repository home. Read-only remote verification confirms the three Webmin fork
branch heads recorded in the owner publication document. Their fdisk, smart-status
and system-status module trees exactly match the final combined review branch;
combined changes touch no other modules. The two combined commits therefore add
no implementation absent from the published branches. All locally present Webmin
commits are reachable from the retained refs after reconstructing the partial
clone's missing-parent boundaries for local analysis; no extra abandoned Webmin
commit was found. No fetch, push, merge or production change occurred.

The two Codebase Memory commits contain identical eight-line synthetic watcher
fixtures. The two unborn qualification indexes contain identical blob sets: 68
blobs remain in the retained source snapshots; the remaining three are an obsolete
operation hash, a superseded regression-test version and generated Python bytecode.
The three saved server worktree commits are already in main. Two indexes match
retained worktree files; the third matches its original committed HEAD, while its
later worktree edits remain in the original source snapshot. No staged-only work
requires migration.

Recorded source reconciliation in Webmin/docs/DISK_DISCOVERY_UPSTREAM_PUBLICATION.md.
Deleted `.local-evidence/git-metadata-retirement-2026-11-17` and the task-owned
`/tmp/webmin-reconcile-np4lqfpi` analysis repository. No replacement archive or
repository was created in evidence storage. Original source snapshots, consumed
bundles and diagnostic receipts remain untouched. These documentation updates
are local/uncommitted; no publication authority was used.

### November 17 W-210 local neutral cleanup; W-211 qualification limit

Verified annotated archive tag and exact commit 4986722 against the retained
remote-verification receipt, then compared consumed operation, recipe and terminal
result bytes against that commit before cleanup. Reused the existing inactive
operation format, rebound current transaction/state/production and outer-operation
hashes, cleared the recipe, removed the archived terminal-result working file,
updated lifecycle classification and set the stream clean while retaining its
archive tag. Successor remains none and coverage remains header-only. No neutral
implementation or accepted deployed identity was reverted. The unrelated Webmin
publication documentation edit was preserved.

Window, successor, accepted-live and lifecycle policies pass. Current-tree
operator-documentation check passes. Outer-runner Bash syntax, ShellCheck,
canonical formatting, readonly/local collision and whitespace checks pass.
The current-repository-policies host profile passes its preceding regressions,
then fails its documentation self-test: the temporary copy lacks the Webmin
onboarding document linked from Caddy. W-211 tracks that fixture-only gap; no
fixture repair or load test was undertaken. Initial local command/profile/schema
errors were corrected and their logs retained, not reported as acceptance.

Logs and result are in `.local-evidence/uptime-kuma/neutral-cleanup-w210/`.
Sessions 70714 (profile exit 1) and 64355 (shell checks exit 0) are retired.
Cleanup changes remain uncommitted. No live contact, replay, new candidate,
installation or publication occurred. W-147 and AC-013 remain open; W-157 is
not installed. The failed diagnostic archive and private consumed receipts remain.

### November 17 W-212 retained request-contract review

Sources: W-202 backend-wire.jsonl and backend-path-a-ipv4.json under the consumed
webmin-storage-review-jbd4aw5t/inputs/evidence directory; its existing
w203-reconciliation.json; archived 4986722 request implementation/proposal and
unchanged corresponding current request code. No original receipt was modified.

| Contract | Direct foreground | Proxied foreground | Marked health flows |
| --- | --- | --- | --- |
| Request | GET /session_login.cgi | Same | Same configured method/path |
| Host | Approved Webmin name | Same retained value | Same retained value |
| User-Agent | homelab-proxy-diagnostic | Same retained value | Recorded unexpected; raw value unavailable |
| Accept-Encoding | identity | Same retained value | Recorded unexpected; raw value unavailable |
| Forwarded/Accept headers | Explicit HTTPS, host, source and Accept */* | Retained map matches direct | Absent from retained health map |
| Connection | close | close | close |
| Client bound | Python socket timeout 5 seconds per blocking operation | curl max-time 5 seconds overall | Configured health timeout 3 seconds |
| Acceptance | HTTP 200 plus bounded body containing login password field | HTTP 200; body discarded | Configured HTTP 200; no login-form assertion |

Thus path and foreground headers match, but the three producers do not have
identical deadline or response-body contracts. The direct Python timeout is not
an overall five-second request deadline. The proxy transport's 60-second header
timeout also does not extend the five-second curl deadline. These distinctions
are not explanations of the failure and are not a proposal to increase limits.
The health marker containing the word webmin is not its User-Agent; no retained
raw health User-Agent establishes the earlier authentication-selection defect.

Observed: direct first backend payload at 2.307 seconds, accepted HTTP 200/login;
two health flows start about 177 ms before the proxied foreground. Their first
payloads arrive at 7.517/7.513 seconds; foreground first payload at 7.491 seconds.
Health clients close near three seconds and foreground near five. No complete
HTTP response/status was captured for the delayed flows. These are network-boundary
observations, not proof of internal CGI execution, serialization or completion.
Zero sampled memory-high/max/OOM events do not establish absence of CPU, I/O,
name-lookup or internal waits. Individual health process origins remain unassigned.

The primary proposal already has one IPv4 upstream. Serializing IPv4/IPv6 probe
loops would not remove the two health flows observed in this single-family run.
Do not infer independent capacity from two addresses of the same Webmin process.
Do not equate the configured 30-second health interval with request serialization.

Owner review recommendation, not an execution definition: use the existing native
backend path to compare one foreground-contract request with a bounded overlapping
batch using the identical method/path/headers and response criteria. Vary only
concurrency; do not simultaneously normalize health headers, increase deadlines,
raise caps or change authentication. This tests whether equivalent concurrent
requests can reproduce delay on the actual host; it would not prove the historical
health-request cause or accept production proxy onboarding. No Caddy route
publication, secondary, DNS, browser or scan is needed for that question. Existing
backend exposure/guard, measurement and restoration still require explicit scope
and live approval; no current backend reachability is assumed.

If the owner instead chooses to investigate differing health headers, treat it
as a separate factor with a fixed concurrency level. Do not fabricate the missing
raw header values or collect cookies/credentials/bodies to recover them. Use a
small allowlisted safe header contract. Stop after a decisive bounded result;
no further capacity fixture or broad deployment rehearsal is justified by this
review. No candidate, command, acceptance waiver or live authority was created.
W-211 remains independently open. W-147/AC-013 remain unresolved.

### November 17 W-213 backend concurrency comparison review

The proposed question is narrow: does overlapping identical unauthenticated
login-page work change this actual Webmin backend's response under its existing
service controls? It does not test Caddy forwarding, original health-header
behavior, browser acceptance or sustained capacity.

Owner-path review: `Webmin/ansible/proxy-trial.yaml` and
`proxy-trial-restore.yaml` already snapshot, temporarily apply and restore the
native backend with an independent recovery timer. They are include tasks, not
standalone execution authority. The existing `proxy-combined-trial.yaml` requires
a Caddy argv, recipe, authorization-ready successor and Caddy recovery. Do not
run it with a fake/no-op Caddy action or register a Caddy successor solely for
this comparison. Preparation should reuse the native tasks and existing probe/
observation components in a narrowly scoped Webmin entrypoint, without a new
transaction framework. Existing 1800-second fallback recovery and its verified
restoration/disarm ordering remain; this is not permission for 1800 seconds of
load. Backend apply limits and all service caps remain unchanged.

Proposed test boundaries for local preparation:

- Only the primary as HTTP client and the Pi as backend, IPv4. Retained source
  address is 10.1.0.53 and backend 10.1.3.75:10000; fresh admission must confirm
  route-selected source, SSH/hostname identity, boot continuity, installed units,
  limits, configuration and guard before temporary access. Historical captures
  are not current readiness. Reuse owner-approved ingress restrictions; any
  proposed narrowing must be explicit and qualified, never silently broadened.
- Fixed GET /session_login.cgi, approved Host, neutral User-Agent,
  Accept-Encoding identity, Accept */*, HTTPS forwarded contract and connection
  close. Only correlation IDs and concurrency differ. No authentication,
  cookies, login credentials or stored response bodies. Evaluate HTTP 200 and
  the existing bounded login-form predicate in memory, recording only outcomes.
- One baseline request; after completed/healthy settling, one batch of three
  simultaneous requests. At most one final single-request control if the batch
  finishes and resource/health/cleanup gates permit it. Five requests maximum;
  no automatic retry. Record actual backend arrival overlap rather than infer
  it from client thread launch. Three requests approximate the observed count,
  not the historical header mixture or exact 177 ms lead.
- Every request uses the same five-second total wall-clock deadline, including
  body inspection. This must be implemented consistently: the existing direct
  helper's five-second socket timeout is per blocking operation and is not a
  total deadline. Do not extend limits to obtain HTTP 200. Record connection,
  first-header/body timing, final status and timeout stage; distinguish slow
  valid responses from client failures and failed login-form predicates.
- Reuse bounded resource observation covering all phases, unchanged service
  controls and the existing reserve/pressure stop rules. Abort on OOM, service
  restart, resource/health stop conditions, loss of required evidence or lost
  continuity. Do not launch a phase while earlier request work is outstanding.
  Client socket closure alone does not prove CGI work stopped. Preparation must
  provide a bounded, non-secret backend quiescence check; if it cannot establish
  completion safely, stop and restore rather than launch the final control.
- Use a short explicit aggregate forward deadline inside the previously accepted
  240-second ceiling; reserve bounded recovery separately. No opportunistic
  extension for settling. Prove cancellation/owned-client cleanup, exact backend
  loopback/guard restoration and terminal readback before disarming recovery.
  The final single control is optional evidence, never a reason to bypass a stop.
- No Caddy publication, validation-tool installation, health-policy edit,
  secondary contact, DNS, scan, browser/graphs, package change, cap change or
  persistent access promotion. Existing background fleet work is not suppressed;
  record relevant overlap and classify a confounded result honestly.

Interpretation agreed within this review, not production acceptance:

| Observation | Supported conclusion / next boundary |
| --- | --- |
| Baseline fails | Concurrency comparison not established; stop, retain failure and restore. |
| Baseline succeeds; overlapping batch degrades or times out | Equivalent concurrent workload reproduces a backend symptom in this run; historical Caddy/health causation still unproven. |
| Batch and eligible final single succeed | No reproduced symptom under this count/contract/run; concurrency is not ruled out generally. |
| Final single degrades despite safe settling | Possible state/order effect; no simple concurrency attribution. |
| Overlap, quiescence or resource evidence missing | Inconclusive, not a passing comparison; stop and restore as applicable. |

Review is complete. Local implementation should test request/deadline/cancellation
and restoration correctness only; no substitute-host capacity or elaborate
fixture expansion. Any exposed correctness/recovery defect remains a blocker.
No executable scope, command, successor or live authority is defined by this
review. W-211 is independent; W-147 and AC-013 remain unresolved. No tools contacted
either target, launched a workload or published changes.

### November 17 W-211 published CI failure confirmed

Repository validation run 44173741545 for exact commit 49867222c7a55957471d2a8a15038eeb649693f7
failed in Caddy current-production contracts / Repository policies. Its log reports
operator_documentation_policy_failure=relative_link_broken for the temporary
self-test copy of APPLICATION_ONBOARDING.md linking to
../../Webmin/docs/CADDY_ONBOARDING.md. This matches W-211's local failure.
The self-test copies Caddy and the DNS dependency but omits this Webmin document;
the real file exists and the current-tree check passes. This is a fixture-copy
defect, not evidence of a deployed Caddy/Webmin outage. The accepted DNS pin is
not the reported cause. The complete failed-job log is retained in
neutral-cleanup-w210/ci-44173741545-failed.log. No test rerun, code edit, live
contact or publication occurred. W-211 remains open for the small dependency-copy
correction and focused positive/missing-dependency qualification.

### November 17 W-214 backend-only implementation checkpoint

Prepared `Webmin/ansible/backend-comparison.yaml` and its phase include using
existing native apply/restore tasks, with `Webmin/scripts/compare-backend.py`
reusing the current probe and observer. No Caddy operation is registered.
The draft's unconditional first task refuses execution locally; it is not a
live command or a deployable candidate.

The helper limits each request to five seconds across blocking stages and
reaps its owned worker processes. The fixed phase list is one, three, one;
any failed phase prevents the next. Resource gates preserve explicit service
limits, boot/cgroup/process identity, the 96 MiB reserve and zero increases in
high/max/OOM events. Backend quiescence conservatively requires the original
single Webmin process and no outstanding connections for two samples; socket
closure alone is insufficient. Unexpected persistent child activity stops the
comparison rather than being accepted as harmless. The sampler's optional
callback leaves existing callers unchanged.

Qualification: seven focused tests passed (actual local worker deadlines and
cleanup; resource/continuity rejection; quiescence; observed overlap; fixed
scope and execution refusal). Fifteen existing workload tests passed. Ansible
syntax passed with a writable controller temporary directory; the initial
sandbox-only home temporary-directory failure is retained. Syntax checking used
localhost inventory and made no host connection. No fixture capacity tests or
containers were used. vexp completion verification was unavailable from the
parent workspace (not a repository); it is not a passing qualification.

Remaining correctness work before sealing:

- Bind an aggregate forward/recovery supervisor; the declared 240/840-second
  values and per-command timeouts do not establish an aggregate bound.
- Qualify independent recovery and client-directory cleanup on all failure paths,
  including a snapshot cancelled before mutation and failed evidence retrieval.
- Require terminal observer completion, resource interval coverage, header
  equivalence and overlapping-traffic disposition. Current per-phase wire checks
  demonstrate arrivals/overlap only and cannot accept the final capture.
- Resolve stop propagation: a sampled resource stop blocks subsequent phases,
  but an in-flight batch can continue to its five-second request deadline. Do not
  describe this as immediate cancellation.

These are implementation/control gaps, not Pi capacity findings. The parent
remains disabled until resolved; no approval is requested for an incomplete
operation. W-211 is separate and unchanged. Existing consumed evidence and Caddy
neutral bindings remain untouched. Local sessions completed; no live execution.

Private qualification logs and exact source hashes: `.local-evidence/uptime-kuma/backend-comparison-local-h1u9lgzd/`. This directory contains inert evidence only, no Git metadata.

### November 17 W-211 documentation self-test correction

The existing self-test now copies Webmin/docs/CADDY_ONBOARDING.md into its
temporary repository. The negative case removes that file, requires the specific
relative_link_broken failure, restores it and requires a passing check. This fixes
the omitted fixture dependency without weakening current-tree link validation.

The self-test, current-repository-policies host profile, canonical shell format,
readonly/local collision policy and whitespace check passed. No container or
live host was used. The failed published run remains historical evidence; remote
CI has not rerun because this fix is uncommitted and unpublished.

Source SHA-256: `a94a7ef40ada227b5002de619c9aa517e218e56438ca3c334472c35f79d24668`.
Profile log: `.local-evidence/uptime-kuma/backend-comparison-local-h1u9lgzd/w211-repository-policies.log`.
Local sessions 4700 and 24049 completed with exit 0 and are retired. W-214 and
Webmin production acceptance are unchanged.

### November 17 W-214 deadline, recovery and terminal evidence qualified

The backend-only parent now uses `compare-backend.py run` to supervise two
invocations of the same playbook: forward work, then recovery regardless of
forward failure, timeout or controller interrupt. Forward has a 240-second
aggregate controller budget; recovery, evidence retrieval and readback share
840 seconds. Process-group termination is inside those budgets. Zero command
statuses alone cannot accept a run: the controller also requires the terminal
restoration, cleanup and evidence receipt. Fresh private output storage and an
exclusive start marker prevent reuse of this entrypoint's consumed output.
Direct playbook invocation omits supervision and is not the candidate launcher.

The recovery play reads the persisted admission boot identities. Primary stop
failure cannot prevent backend restoration when the backend's own identity is
still valid. Restoration is attempted before fetching or interpreting evidence;
failed restoration does not disarm the independent timer. The shared native
restore path now verifies unchanged files, controls, absent ingress and loopback
before accepting cancellation of a snapshot that never mutated the host. Both
hosts' boot continuity is checked again after restoration. No historical boot
identity is imposed on a new admission.

Client stop latching plus an exclusive lock waits for owned workers and rejects
late dispatch. The private primary directory remains with that latch; retained
files are not running workload. The observer records its process identity and
completion, and recovery verifies it has exited. Final evidence requires clean
terminal records, no drops, matching request headers/markers, observed overlap,
same-host clock/resource coverage, reserve/control/process continuity and final
quiescence. Missing or confounded evidence fails acceptance after restoration.
The observer covers the selected primary/backend interface; it does not prove
absence of every possible background task or internal CGI completion. Native
owner loopback readbacks are separate from the maximum five comparison requests.

A resource stop blocks subsequent phases. Requests already launched remain
bounded by five seconds; no instantaneous cross-host cancellation is claimed.
Controller cutoff or loss of transport is a failed/unverified operation, not
proof that remote recovery finished. Preserve the existing independent native
fallback and require manual reconciliation if restoration cannot be verified.
The 1800-second fallback remains a contingency, not an extension of the 840-second
controller acceptance budget. Service caps and the 96 MiB reserve are unchanged.

Qualification on the final implementation:

- Thirteen comparison tests pass: real local worker deadlines and stop/late-start
  handling; forward failure/timeout and independent recovery timeout; terminal
  evidence rejection; fixed scope; five actual localhost Ansible recovery cases.
- The Ansible cases cover success, client-stop failure, restore failure, invalid
  evidence and verified pre-mutation cancellation. Their native service boundary
  is explicitly substituted; the owner task graph and evidence/error handling
  execute locally. This does not establish writable target recovery.
- Fifteen native recovery tests and fifteen existing workload tests pass.
- Ansible syntax, Python parsing, host current-repository-policies, hook
  configuration and whitespace checks pass. The new focused pre-commit hook
  selects these comparison checks for relevant changes. The existing Webmin
  README records the diagnostic's launcher and limits, without making it a
  mandatory fleet-onboarding gate.

Earlier local failures are retained: the restricted sandbox prevented Ansible's
RPC startup; the first native-control substitution did not intercept the fully
qualified timer module and hit an absent local unit. No service changed. The
corrected tests substitute that one task explicitly and passed. The old recovery
test's expectation of zero commands was updated to require the new read-only
baseline checks while still excluding a restart. No capacity fixtures or
production hosts were used. vexp completion verification remained unavailable
from the parent workspace and is not counted as a pass.

Private final logs and exact source identities: `.local-evidence/uptime-kuma/backend-comparison-w214-jzp28qwm/`.

All local sessions completed and are retired (final comparison 58683 and host
policy 10305 exited 0). Previous consumed bundles remain unchanged. The Caddy
stream is still clean/inactive; no successor or live bundle was registered or
sealed. W-211 remains locally resolved. W-147/AC-013 still require actual target
evidence under separately reviewed authority; W-157 remains uninstalled.

### November 17 W-215 exact backend-only comparison review

Prepared bundle: `/home/aaron/code/.local-evidence/uptime-kuma/webmin-backend-review-2k86wh8y/`.
`INPUTS.SHA256SUMS` binds 33 frozen inputs, including the launcher, supervisor,
native owner tasks/helpers, inventory, host keys, installed baseline, limits,
rendered profile, runtime references and operation scope. Its SHA-256 is:

`f366744efeccddf5886e27956b1f6cd2cf7944d7a5c105fe633fb6191c98dd29`

This candidate uses the existing backend-only supervisor. It defines no Caddy
operation and does not invoke the combined Caddy parent. Retained W-202 inputs
supply the accepted installed Webmin file/control identities and service limits;
current owner sources are frozen separately. Historical boot IDs are not reused.
Live admission must revalidate the baseline and capture fresh continuity IDs.
Primary native hostname comes from the Caddy owner's deployment inventory;
Pi native hostname is `j2-svpi3bmf`, matching the retained installed binding.
SSH uses the retained host keys with strict checking and disables ambient SSH
configuration. Authentication uses existing external SSH credentials; none are
copied or hashed into this bundle.

Explicit narrowing from the previous profile: only 10.1.0.53 can reach the Pi's
IPv4 backend. IPv4/IPv6 loopback remain; the non-loopback IPv6 listener and all
other proxy allow rules are absent. Remaining managed Webmin settings are
unchanged. Source comparison proves only listener/allow-list/rule removal;
this is local configuration qualification, not target firewall acceptance.
A read-only `ip route get` assertion now runs before temporary exposure and
requires the reviewed primary source; each request also checks selected route
and connected endpoints. The exact installed unit/drop-ins, configuration hashes
and controls are checked by the native snapshot before apply.

**Exact command for separate one-attempt authorization:**

```sh
/usr/bin/python3 -I -B /home/aaron/code/.local-evidence/uptime-kuma/webmin-backend-review-2k86wh8y/operator.py --manifest-sha256 f366744efeccddf5886e27956b1f6cd2cf7944d7a5c105fe633fb6191c98dd29 --run-approved-once
```

Targets and permitted mutations if approved:

- `pi@10.1.0.53` / `j1-svpihole0`: identity/route/boot reads, private client-file
  staging and bounded unauthenticated HTTP requests. No primary service change.
- `ama@10.1.3.75` / `j2-svpi3bmf`: existing privileged native owner snapshot,
  independent recovery timer, temporary restricted Webmin profile/guard and
  service restart, bounded resource/wire observation, exact loopback restoration
  and readback before timer disarm. No package or service-limit changes.
- Comparison: one request, three concurrent identical requests, then at most one
  conditional single control. Maximum five, no retries; each has a five-second
  total deadline. Fixed GET `/session_login.cgi`, approved Host and neutral
  User-Agent; no authentication, cookies or retained response bodies. Native
  owner loopback readbacks are additional, separately bounded recovery checks.

Forward work has a 240-second aggregate controller budget; recovery and final
retrieval/readback share 840 seconds. The independent native fallback stays at
1800 seconds with its existing bounded service timeout; it is a contingency,
not permission to extend workload or claim controller acceptance. Resource
controls remain Webmin high/max 128/192 MiB, Kuma 256/320 MiB, zero swap and
96 MiB available reserve. Stop on limit drift, new high/max/OOM events, lost
process/boot identity, missing evidence or failed quiescence. Already dispatched
requests may run to their five-second deadline; no instantaneous cancellation
claim. The final single control runs only if prior request, health and quiescence
checks succeed.

Recovery runs independently after forward failure. Primary stop failure or
observer failure cannot skip Pi restoration when its own continuity is valid.
Verify client stop latch/worker cleanup, observer exit, original files/controls,
loopback and guard restoration, then disarm the timer. Retain the primary private
client directory and stop latch to reject delayed dispatch; it is evidence, not
running workload. A controller cutoff, transport loss or changed boot leaves
restoration unverified and requires owner reconciliation; no retry or assumed
rollback. Terminal evidence cannot override a failed restoration.

Qualification: all 13 frozen comparison tests pass, including existing local
worker/deadline tests and five localhost Ansible recovery cases. Four actual
localhost assertions exercise the pre-exposure route expression with accepted
`prefsrc`/`src`, wrong source and missing source. Exact-inventory syntax, Python
parsing, frozen/current source equality, unchanged-profile/narrowing checks,
wrong-manifest rejection, private modes and secret scan pass. W-214 native
recovery/workload results remain applicable to unchanged source identities.
Logs are under the bundle's `qualification/`; no substitute capacity fixture
was run. The launcher was run only with local verification; its one-attempt
marker is absent and prepared output is empty. The evidence directory contains
no Git metadata. Local sessions 60340 and 63572 exited 0 and are retired.

Acceptance is limited to this request comparison, complete resource/wire coverage,
cleanup and restoration. A reproduced symptom is not historical Caddy causation;
a pass is not sustained Pi capacity or AC-013 browser acceptance. No Caddy
publication/validation/reload, secondary contact, DNS, login/browser/graphs, scan
launch, notifier installation, permanent promotion or Git publication is included.
Existing fleet background work is not suppressed; confounding evidence fails
comparison acceptance. W-147/AC-013 remain open; W-157 remains uninstalled.

Authorization: **not granted**. Repository policy requires explicit approval of
this exact bundle, command and scope before any target contact. Prepared local
checks do not consume live authority. All prior bundles and receipts remain intact.

W-215 final scan disposition: the sealed candidate and monitoring working-tree
scans found no leaks. The broad server working-tree scan exited 1 on 18 entries
in untracked `.vexp/manifest.json`; every match is a hexadecimal file-index
identity keyed by an existing source path, not a credential value. Those entries
are outside the frozen bundle. The redacted report and classification are retained
under `qualification/`; no scanner exclusion or production control was changed.
Both scans and the diagnostic report scan completed; sessions 47986 and 50120
are retired. Final local verification still finds the bundle unconsumed and
Caddy clean/inactive. No live operation or publication occurred.

### November 17 W-216 approved backend-only execution

Aaron approved W-215’s exact bundle, command and scope for one attempt. Frozen
input verification passed immediately before launch. Authority covers only the
reviewed primary/Pi comparison and its recovery; no Caddy or publication action.
The execution receipt is retained beside the unchanged sealed inputs.

### November 17 W-216 terminal outcome and W-217 follow-up

The approved command ran once and exited 1. Session 3274 is complete and retired.
Its sealed 33-input manifest and every input still match the approved hashes.
Private evidence remains in `webmin-backend-review-2k86wh8y/`; the terminal summary
and `TERMINAL-EVIDENCE.SHA256SUMS` bind the retained logs and receipts. Approval
is consumed. No replay, new live inspection or publication is authorized.

Primary hostname/source-route and both admission boot reads passed. The native
owner checked the accepted installed baseline, armed recovery and applied the
temporary primary-only backend profile. The initial quiescence gate then exited
1 after 10.645403 seconds with `backend_not_quiescent`. Observation and comparison
requests never started; this is not another measured HTTP timeout or evidence
of concurrency causation. Native owner loopback checks did run within their scope.

The gate requires an original singleton Webmin process, an unchanged process
set and no active port-10000 connections for two samples. Its failure path does
not preserve the observed values, so retained evidence cannot distinguish an
initial child process, subsequent process activity or connected sockets. Do not
attribute this rejection to host capacity or a particular background service.

Recovery independently checked boot continuity, latched primary client stop,
restored the exact original native configuration and controls, verified loopback
and guard restoration, then stopped the recovery timer. The fetched native state
is `restored`; recovery-result records restoration_verified=true,
restoration_failed=false and client cleanup rc=0. The observer never started;
there was no observer workload to join. Final boot continuity assertions passed.

The final evidence analyzer returned FileNotFoundError because resource/wire
and phase records were never produced. This made the recovery play exit 2 at
its comparison-evidence assertion, not at restoration. Forward also exited 2;
neither aggregate controller budget expired. Overall acceptance remains false.
Preserve this distinction rather than report recovery failure or a successful
comparison. W-217 tracks the missing gate detail and explicit not-started outcome.

No Caddy action, secondary contact, DNS, browser/login, scan, package/cap change
or publication occurred. Caddy remains clean/inactive without an operation.
W-147 and AC-013 remain unresolved; W-157 remains uninstalled. Further work is
local reconciliation only until another separately reviewed scope is approved.

### November 17 W-218 diagnostic reset after Aaron's review

Aaron rejected the repeated cycle of complex tests that fail without useful
observations. The audit reviewed the current comparison/gate/client code, W-202
request evidence, accepted service controls and extracted native Webmin 2.670
source. It made no live contact and did not launch another server/load fixture.

**What is established:**

- The last attempt did not reproduce an HTTP problem. Its gate stopped before
  observation or comparison requests. Restoration was verified.
- `compare-backend.py` requires the initial Webmin process list to contain exactly
  one member. That baseline never changes. A stable two-process idle state fails;
  even settling to one process cannot satisfy this predicate. The health check
  also treats disappearance of any initial child as failure. This is not a valid
  general Webmin-idleness contract.
- Native 2.670 `miniserv.pl` lines 573–606 starts a persistent log-clearing child
  when logclear is enabled; lines 335–348 supports an external-authentication
  child. `--nofork` does not prohibit those children or request handlers. The
  current target's logclear setting/process roles were not captured in W-216;
  do not claim this particular child caused its rejection.
- The gate saves its baseline only on success, throws a bare code on failure,
  and starts observation afterward. Therefore its own rejection removes the
  evidence needed to explain it. Terminal evaluation then assumes samples exist,
  producing the secondary FileNotFoundError. The tests used a singleton process
  model and did not establish validity of that model for Webmin.
- Worker exceptions can also collapse detail to an exception class. Adding more
  acceptance gates cannot repair missing measurement at the failing boundary.

Pure local calls to the existing predicate reproduced both false cases, without
starting processes or contacting a host. Exact source hash/results are retained
in `webmin-diagnostic-audit-z_e3a94h/findings.json`. Consumed inputs are unchanged.

**What the actual HTTP evidence says:** W-202's direct request returned HTTP 200
with the login predicate and first payload at about 2.307 seconds. Two overlapping
health flows and the foreground request produced first payloads at about
7.517/7.513/7.491 seconds. The five-second foreground deadline expired first.
No sampled memory high/max/OOM events occurred in that run. Earlier pressure/OOM
observations belong to a different run and do not establish this run's cause.
The retained Webmin control is CPUQuotaPerSecUSec=1s, a one-CPU aggregate ceiling.
Approximately threefold elapsed time under three requests makes shared CPU work
or contention a concrete leading hypothesis. CPU usage/throttling, I/O waits and
handler attribution were not collected; it remains unproven. Serialisation,
lookup or other waits remain alternatives. Do not increase timeouts/caps or
change health policy merely to make acceptance pass.

Vendor documentation review via Context7 confirmed the dedicated-hostname recipe
uses referers, redirect_ssl and redirect_host. The prepared settings supply those
keys, with the approved name and redirect_port=443. The vendor nginx example uses
an HTTPS backend; the local owner contract deliberately uses guarded LAN HTTP.
That transport distinction is explicit and is not evidence of the observed delay.
Configuration review cannot establish current live browser acceptance.

**Replace the default next step:** use the Pi's existing loopback listener to
measure native server work. No Caddy release/replication, temporary LAN exposure,
profile change, restart or restoration transaction is needed merely to ask whether
concurrent login-page rendering is slow. Prepare a transparent bounded native
request/sampling command, with one single request and only an eligible controlled
concurrent batch. Preserve deadlines, caps, reserve and explicit stop conditions;
no authentication, bodies, cookies or command-line/environment collection.
Collect request outcomes alongside numeric CPU usage/throttling, memory events,
process identities/roles and waits before, during and after requests, including
failure. Distinguish an expected persistent helper from owned request activity;
do not require one process or claim that socket closure proves CGI completion.
Do not launch another phase when earlier request work is unresolved.

This is a materially narrower proposed measurement, not yet an executable scope
or authorization. Loopback changes the peer/network path: reproducing delay there
supports a backend workload problem; a pass does not exonerate Caddy, remote-peer
handling or health-request headers. If it fails to reproduce, select the next
measurement from those results rather than rebuild the full deployment trial.
No fixture may settle actual Pi capacity. Test only a concrete measurement defect,
not an ever-growing simulated production system.

Every diagnostic failure must retain bounded expected/observed values and phase
status before exit; unavailable data must say why. Keep request outcome, evidence
completeness and restoration as separate outcomes. This audit changes the planned
preparation approach, not resource policy or live authority. W-217 remains open
but repairing its entire superseded comparison path is not a prerequisite to a
smaller diagnostic. W-147/AC-013 remain unresolved. No source deployment,
publication, new test bundle or live retry occurred.

### November 17 W-219 proposed durable instruction

Aaron asked how to prevent fixture engineering and assumption-driven gates while
keeping tests minimal. The workspace already limits fixture capacity/platform
claims, but does not explicitly require the gate's premise to be established.
Proposed addition beside that existing rule in `/home/aaron/code/AGENTS.md`:

> **Evidence before gates; smallest sufficient tests**
>
> Before adding a diagnostic gate or test, state its question, the documented,
> observed or user-approved contract it relies on, and the result that changes
> the next action. Use the existing work record; create no new checklist.
> An unverified premise is something to measure, not a blocking assertion.
>
> Prefer an existing native command and the smallest path that can distinguish
> the plausible causes. Add a helper only for a missing measurement or safety
> boundary; do not recreate a deployment to diagnose one request.
>
> Start with one representative success and the relevant failure. Add cases only
> for distinct safety boundaries, a demonstrated defect or changed behavior.
> Preserve required repository checks. A test that agrees with its own mock
> proves implementation behavior, not the mock's fidelity to the target.
>
> Before live use, verify that failure retains bounded safe expected/observed
> values, phase, timing and command status. Emit observations before assertions.
> Distinguish not-run, failed measurement and failed cleanup. Do not replay an
> unexplained failure with the same measurement blind spot.
>
> Stop when the stated question is answered. Remaining target uncertainty belongs
> in the smallest authorized target observation, not expanded fixtures. Keep
> established safety controls and authority boundaries; minimal tests do not mean
> weaker acceptance or an arbitrary test-count cap.

This is a reviewable proposal, not an installed instruction. No AGENTS.md change
or personal-memory update was made. Existing fixture/authorization rules remain.

### November 17 W-220 exact Pi loopback measurement for review

Prepared private bundle:
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-loopback-review-zyhou1lc/`.
Six frozen inputs: current diagnostic source, its test source/provenance, retained
SSH host keys, selected scope and the direct SSH launcher. No Git metadata.
`INPUTS.SHA256SUMS` SHA-256:

`5187d43c89ffb4f82ebc4025da4d9b4b26be96e0a075cca076e761e1f9677de8`

**Exact command for separate one-attempt approval:**

```sh
/bin/bash /home/aaron/code/.local-evidence/uptime-kuma/webmin-loopback-review-zyhou1lc/operator.sh 5187d43c89ffb4f82ebc4025da4d9b4b26be96e0a075cca076e761e1f9677de8 --run-approved-once
```

One SSH connection to `ama@10.1.3.75`, strict retained host keys, expected native
hostname `j2-svpi3bmf`. Source is streamed to privileged Python stdin through
noninteractive sudo. No host file installation, Ansible, service restart, profile
change, firewall change, Caddy/primary/secondary contact, DNS, browser/login,
scan, package operation, cap change, publication or retry is included. SSH/sudo
and Webmin may produce their normal access logs. Credentials remain external.

Request contract: GET `http://127.0.0.1:10000/session_login.cgi`, approved browser
Host and forwarded headers, neutral User-Agent, connection close, no credentials,
cookies, redirects or retries. Native curl discards the body and reports HTTP
status, connection, first-byte and total-transfer timing. It does not assert the
login form. One request, then only if healthy/settled and successful, three
concurrently launched clients: four maximum, each five seconds total. No final
recovery-control request. Loopback peer differs from prior remote traffic;
concurrent client launch is not packet-level proof of backend arrival overlap.

The script takes a baseline and emits samples before checking prerequisites.
It checks exact hostname, existing Webmin/Kuma memory limits, one-CPU Webmin
quota, boot and main-process continuity, 96 MiB reserve and zero new memory
high/max/OOM events. It observes process PID/parent/state/start ticks/CPU ticks,
wait channels, cgroup CPU usage/throttling/pressure, memory/I/O pressure and
counters, available memory and sampler CPU. It skips expensive PSS rollups for
this capture. No process command lines/environments, raw configuration, response
headers, bodies or credentials are captured. Process roles are observed
attributes, not guessed labels.

There is no singleton requirement: established helper processes are allowed,
normal child exit is allowed, and a process that disappears during sampling is
explicit rather than automatically a service failure. Only the original main
process must survive. Before another batch, require no connected port-10000
sockets or newly observed processes for two samples within ten seconds. This
conservative observation is not proof of absence of all background work or
internal CGI completion; new background activity may stop further work, but its
observed PID/socket differences are retained. No existing work is suppressed.

Sampling is nominally half-second while clients run and one second during
settling. The stream includes phase and elapsed time, actual sampling gaps and
observer CPU so overhead remains visible. Missing CPU counters, relevant process
evidence or controls stop progression; all collected observations remain. Final
readback and terminal output are independent of HTTP success. A failed single
request prevents the three-client batch. Resource stops kill/reap only owned
curl clients; Webmin itself is never killed or restarted by this diagnostic.
Client closure does not prove server-side work ended. Outstanding activity is
recorded as unresolved and prevents success; it needs owner review, not an
unapproved recovery action.

Bounds: Python alarm 45 seconds, remote timeout 50 seconds plus two-second kill
grace, controller SSH timeout 65 seconds plus three-second kill grace. Each curl
has a five-second deadline and a six-second supervisor check. These bounds apply
to diagnostic/client lifetime, not Webmin handler lifetime. No automatic retry or
fallback. Controller output records the SSH/timeout exit and separate stderr;
missing terminal output/transport loss remains unverified. Nothing in this scope
authorizes raising caps, extending request acceptance, or restarting a service.

Qualification is limited to measurement and safety behavior. Six focused tests
passed: actual local HTTP/curl timeout and output privacy; the coordinator with
a two-process baseline, normal child exit and resource-stop/no-next-batch;
existing sampler privacy/disappeared-process cases; existing HTTP status and
slow-header reporting. Proc/cgroup readings in the coordinator case are explicitly
substituted. The endpoint is not Webmin and cannot qualify Pi capacity or predict
its result. The final source and test hashes match the frozen copies. Shell syntax,
ShellCheck, explicit shell formatting, Python parsing, local manifest verification,
wrong-hash/invalid-argument rejection and whitespace checks pass. No target was
contacted. The existing superseded comparison and all consumed bundles are intact.
Local sessions 73540, 23717 and 91029 completed with exit 0 and are retired.

Private logs: `qualification/` within the bundle. Earlier local format checking
reported only shell whitespace; it was corrected before the final seal. An
inapplicable shell-format invocation on Python failed without editing the file
and is not a qualification result. No new host/capacity fixture was built.

Interpretation: observed CPU usage/throttling and process waits can support or
weaken the backend-contention hypothesis; they cannot alone assign every wait's
cause. A slow loopback request reproduces a backend symptom in this run. A pass
leaves remote-peer handling, proxy behavior and health-header differences open.
Neither outcome is sustained-capacity or AC-013 browser acceptance. W-147 remains
unresolved. W-157 is uninstalled; Caddy is clean/inactive. W-217's old comparison
path is preserved, not repaired/resealed as a prerequisite to this measurement.

Authorization: **not granted**. This request approved local preparation and the
loopback direction, not execution. Repository policy requires approval of this
exact bundle, command and scope before the one attempt. Output remains empty;
no attempt marker exists. No publication is authorized.

Final privacy scans found no leaks in the six-input bundle or Webmin owner tree.
The full change-record scan flagged two unchanged historical Caddy outer
authorization identities (lines 8621 and 8853, both present in HEAD); it is not
a clean whole-ledger scan. No historical evidence was altered or suppressed.

### November 17 W-220 authorization and execution

Aaron explicitly approved the exact W-220 Pi-only bundle, command and scope for
one attempt, and installation of W-219. The approved instruction is now installed
in workspace AGENTS.md verbatim from the proposal. No publication is authorized.
Execution will consume the existing one-attempt marker; no replay is permitted.

### November 17 W-221 actual Pi loopback result

Aaron's annotation approved the exact W-220 scope and W-219 installation.
Automatic review initially rejected process creation using the older preparation-only
boundary. The same unchanged command was resubmitted with the latest explicit
approval reference and permitted. There was one actual attempt, session 8728,
exit 1; it is retired. No retry occurred. All six sealed inputs remain unchanged.

Evidence: private W-220 bundle `output/observation.jsonl`, `ssh.stderr` (empty),
`exit.status` and derived `derived-summary.json`. Thirty-five records include
27 samples and a terminal result. One request returned HTTP 200: first byte
2.282220s, total 2.338846s. Three concurrently launched curl clients each exited
28 at 5.0027s with no response headers. Settling completed before the explicit
request-outcome rejection; final readback recorded clients reaped, no unresolved
backend activity, no service change and no recovery attempt. Boot/main-process
and accepted controls passed the scoped readback. No additional target contact
was used to analyze these receipts.

The accepted CPU quota was 100000/100000 microseconds (one CPU). From the first
overlap sample through final settling, Webmin used 8.879368 CPU seconds over
about 10.27 elapsed seconds; 88 of 91 accounting periods were throttled and the
throttled-time counter rose by 17.352628 seconds. This counter is not equivalent
to request wall-clock delay. Workers were sampled running, with other processes
waiting in do_wait, poll or sleep. No new memory-high/max/OOM events occurred.
The observer used about 0.407 CPU seconds between baseline and final sample;
its contribution is measured, not presumed absent.

This reproduces a backend-only concurrency symptom without Caddy or ingress
changes and supports CPU-quota contention as a contributor. It does not prove
causation for historical proxy failures or quantify the effect of changing quota.
W-222 owns the next local policy/design decision; no repeated test, limit change,
service restart or broader workload is authorized. AC-013 remains pending.

### November 17 W-222 owner review and proposed decision

Source ownership: `homelab-server-configs/foundation/ansible/prepare.yaml:37`
sets Webmin CPUQuota=100% alongside MemoryHigh=128M, MemoryMax=192M and swap=0.
The accepted W-221 capture independently observed cpu.max=100000 100000. This
is an installed fleet control, not evidence of a vendor-required ceiling.
Systemd's resource-control manual defines quota relative to one CPU, with values
above 100% permitting more CPU time; this is a ceiling, not reserved capacity.
Reference: <https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html#CPUQuota=>

The current Webmin Caddy proposal uses one IPv4 upstream and active GETs to
/session_login.cgi every 30 seconds, with a three-second deadline. It is a
proposal, not accepted Webmin production configuration. W-221's single request
used 2.34 seconds and the three-client batch exceeded five seconds without
Caddy. The three-second probe deadline has little margin against this one solo
sample; it is not a latency distribution or proof that health requests have
identical cost/headers. Serial address-family checks cannot prevent overlap with
foreground traffic or another proxy. Removing duplicate validation probes alone
also cannot explain away this measured backend-only symptom.

Recommended decision for Aaron's review: permit preparation of one temporary,
single-factor actual-Pi comparison at CPUQuota=200%, returning to the admitted
100% ceiling at the end. Two CPU equivalents is a bounded experimental setting,
not an accepted permanent budget or a guarantee of five-second responses.
Do not remove CPU limits, substitute CPUWeight, raise memory caps, lengthen
request deadlines or alter the health contract in the same comparison. Preserve
the existing listener, request headers/path, one-plus-three request pattern,
resource stop conditions and co-resident Kuma observation. Reuse W-221's native
measurement; do not build another Caddy/ingress transaction or capacity fixture.

Preparation must bind the effective unit and ancestor CPU restrictions, exact
runtime-property restoration and independent cleanup on controller loss. A changed
quota must be verified before workload, and original effective quota restored and
verified even on failure. Native runtime controls are preferred; no persistent
fleet-default change or restart is proposed. These are preparation requirements,
not a new executable or authority. Local checks should cover only the changed
quota/restoration boundary; existing measurement checks need no expansion.

Decision after the comparison: lower throttling plus successful unchanged requests
would support a host-specific CPU-policy correction, still subject to combined
workload/browser acceptance. Continued delay despite effective extra CPU would
leave the hypothesis insufficient; inspect the retained process/wait evidence,
not another identical retry. A memory/resource stop rejects that candidate and
requires owner review. If temporary CPU-policy relaxation is declined, explicitly
revisit responsiveness/concurrency requirements rather than silently weakening
acceptance or claiming that serialized probes make browser capacity adequate.

The shared health-check design also needs a lower-cost readiness contract before
fleet promotion. No replacement URI/status is selected without native evidence;
a static response alone must not be presented as authenticated application health.
Keep that design decision separate from this causal comparison so only one factor
changes. No production definition, script, limit, Caddy fragment or installed
instruction changed in this review. W-222 remains In progress pending Aaron's
policy decision; W-147/AC-013 remain unresolved. No live contact or publication.

### November 17 W-223 exact temporary CPU comparison for review

Aaron approved local preparation of W-222's proposal. W-222 is resolved as a
preparation decision, not acceptance of a permanent two-CPU budget. The original
W-220 bundle, observations and all earlier consumed inputs remain unchanged.

Private bundle:
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-quota-review-fmxfd6af`.
Nine inputs: two owner scripts, their two test sources for provenance, retained
SSH keys, native staging/collection commands, controller launcher and scope.
`INPUTS.json` SHA-256:
`bef1667075f5673a8fb9e7362a9b1840db394cfdd439f188c8109f31e9c9835a`.

**Exact command for separate one-attempt authorization:**

```sh
/usr/bin/python3 -I -B /home/aaron/code/.local-evidence/uptime-kuma/webmin-quota-review-fmxfd6af/operator.py bef1667075f5673a8fb9e7362a9b1840db394cfdd439f188c8109f31e9c9835a --run-approved-once
```

Targets: only `ama@10.1.3.75`, strict retained SSH host keys, native hostname
`j2-svpi3bmf`, noninteractive existing sudo. At most two SSH commands: one stages
and runs the single comparison; one collects retained receipts and cleans up
owned temporary files if restoration and unit inactivity are verified. No
Caddy/proxy/secondary/DNS contact or configuration, browser/login, needrestart
scan, package change, service restart, permanent budget change or publication.

Temporary mutation: root-private `/run/webmin-quota-7917ee636b1a8df5` holds two
scripts and receipts. A native transient service of that name runs the workload.
Admission retains boot, main PID, cgroup identity, unit/drop-in hashes and current
CPU/memory limits, ancestor CPU ceilings and effective CPUs. It requires the
accepted 100000/100000 quota, unchanged Webmin memory limits, at least two usable
CPUs and no observed ancestor ceiling below two CPUs. These last checks establish
that the proposed change can actually permit two CPU equivalents; failure emits
observed values and makes no quota change. Existing runtime CPUQuota drop-in
bytes and owner/group/mode (or absence) are saved privately before native launch.

The worker rechecks admission, applies only `CPUQuota=200%` through
`systemctl set-property --runtime webmin.service`, and calls the existing
loopback measurement with an expected two-CPU ceiling. The fixed request path,
headers, single-plus-conditional-three workload, five-second client deadlines,
45-second observer alarm, memory limits, 96 MiB reserve, resource-event stops,
process checks and client cleanup are unchanged. Only expected CPU ratio varies.
No new performance fixture was built.

Recovery: the transient unit has a 60-second runtime limit, control-group process
cleanup and a 20-second stop budget. Its ExecStopPost runs independently of SSH,
including worker failure/termination. Restoration is separately bounded to 18
seconds plus two-second kill grace. It first lowers the effective quota to 100%,
then restores the saved runtime CPUQuota drop-in bytes/uid/gid/mode or removes the
new file and newly created empty directory. `systemctl daemon-reload` reconciles
that restored configuration; no restart is requested. Final readback requires
original boot, cgroup, main PID, unit-file hashes and resource controls. A restore
failure is retained as `restored:false`; HTTP failure is not confused with it.
Do not call worker/restore phases directly or reset a failed operation.

The first controller SSH command is bounded to 120 seconds. On a nonzero result,
collection waits until at least 115 seconds from launch before its one bounded
20-second read/cleanup command; no workload retry. Receipts and bounded native
stderr are collected privately. Cleanup removes only the reviewed root-owned
regular files after restoration and an inactive/failed unit with MainPID=0 are
verified. Unexpected files or unverified recovery keep the directory for review.
Transport loss or host failure never implies restoration passed. A reboot loses
runtime overrides; this is not permission to reboot or a substitute for readback.
The operation may run daemon-reload and leave evidence under /run on failure;
these are explicit scope, not hidden cleanup side effects.

Qualification: four focused cases cover the native recovery/deadline argument
binding, exact file restoration for prior-present/prior-absent override, retained
restore failure, and worker admission-before-change. The existing localhost HTTP
measurement test passes one-CPU success, resource stop/no-next-batch and the new
two-CPU expected-limit branch. A first launch hit the filesystem sandbox's socket
restriction before serving; the unchanged localhost-only test passed outside it
(session 71845, exit 0, retired). Source/frozen-copy equality, Python parsing,
manifest admission/wrong-hash rejection and whitespace checks pass. Private
bundle and Webmin working-tree secret scans pass. No actual systemd activation,
Pi quota write or target restoration is claimed by these local checks. Existing
vexp completion was unavailable at the parent non-repository workspace; it was
not replayed unchanged. `qualification/results.json` binds these limited results.

Interpretation remains W-222's: success with lower throttling supports a targeted
CPU-policy correction but is not fleet capacity or browser acceptance. Continued
latency or resource stops require review of the actual retained measurements,
not another identical run or an extended timeout. Caddy health-contract redesign
is separate. W-147/AC-013 remain open; W-157 is not installed.

Authorization: **not granted**. The current approval covers preparation only.
No attempt marker exists; output is empty. No live contact, mutation, retry or
publication occurred. Source changes are uncommitted; all local sessions retired.

### November 17 W-224 approved quota comparison execution

Aaron explicitly approved the exact W-223 bundle, command and scope linked at
line 11295 for one attempt. Manifest verification passed locally; this approval
covers the single Pi comparison and its bounded recovery/receipt collection.
No other live operation or publication is authorized.

W-224 terminal outcome: **Passed comparison; original policy restored.** The
approved command executed once, session 49206, exit 0. Bootstrap and collection
both exited 0; their stderr files are empty. Approval is consumed. The exact
nine sealed inputs remain unchanged. No other target was contacted.

Private evidence is W-223 bundle `output/bootstrap.stdout`, `collect.stdout`,
`exit-status.json` and `derived-summary.json`. The controller retained the native
measurement and restoration receipts before removing the owned target directory.
The transient unit was inactive with MainPID=0; remote cleanup was confirmed.

Observed request results (same path/headers and five-second bounds as W-221):

- Single: HTTP 200, first byte 2.290212s, total 2.327324s.
- Concurrent three: HTTP 200, first bytes 3.763899-3.787239s, total
  3.831959-3.852697s. Each client exited 0.
- Measurement completed; clients reaped and backend activity settled.

All samples showed cpu.max=200000 100000. During overlap through final settling,
Webmin used 7.891471 CPU seconds in about 5.183 elapsed seconds; 38 of 41 periods
were throttled and throttled_usec increased 3.671466s. W-221's corresponding
interval was about 10.27s with 8.879368 CPU seconds and 17.352628s throttled time.
These are differently sized phase intervals, not normalized throttle rates or
request-wall-time decomposition. Throttling was reduced in cumulative duration,
not eliminated. Sampled memory peaked at 120909824 bytes; new memory high/max/OOM
events were zero, minimum available memory was 454684 KiB. Observer CPU increased
about 0.327s. These observations do not accept sustained or authenticated-browser
capacity.

Native ExecStopPost restoration passed: cpu.max=100000 100000, original Webmin
memory controls, same boot/cgroup/main PID, same installed unit/drop-in hashes
and original runtime CPUQuota override state. No Webmin restart occurred.
`daemon-reload` reconciled the restored runtime configuration within the approved
scope. The inner observer's `service_changed:false` describes that read-only
observer only; the enclosing operation did temporarily change and then restore
the quota. No permanent CPU-policy or Caddy configuration change remains.

Interpretation: the deliberate quota change preserved the request contract and
changed the concurrent outcome from three timeouts to three HTTP-200 responses,
while solo timing stayed about 2.33s. This is strong actual-host evidence that
the one-CPU ceiling contributed to the tested concurrency delay. Background load
was not controlled in a randomized experiment; it does not prove every historical
proxy failure had the same cause. W-147 retains that distinction. W-225 now owns
the corrective policy/health-contract decision; repeating this diagnostic or
expanding fixtures is not the next step. AC-013 still requires browser acceptance.
No permanent promotion, retry, further inspection or publication is authorized.

### November 17 W-225 concrete CPU and health-contract proposal

This is a local owner review, not approval to implement permanent policy or run
another workload. W-224's original 100% baseline remains restored. The selected
correction below requires Aaron's agreement before implementation/preparation.

| Owner | Proposed correction | Preserved boundary |
| --- | --- | --- |
| Foundation/Webmin | Explicit selected-host CPUQuota=200% for j2-svpi3bmf, owned by the existing foundation profile/host selection. | Do not replace the fleet-wide 100% default or edit installed controls outside the owner path. MemoryHigh=128M, MemoryMax=192M, swap=0, tasks, stop/start controls and reserve stay unchanged. |
| Caddy/Webmin | Keep GET /session_login.cgi and exact HTTP 200; make the health headers explicit: Host and X-Forwarded-Host = webmin-j2-svpi3bmf.local.theama.co, X-Forwarded-Proto=https, User-Agent=homelab-proxy-diagnostic, Accept=*/*, Accept-Encoding=identity, Connection=close. | No credentials, cookies, fabricated X-Forwarded-For identity, redirect-following, authentication bypass or new synthetic health endpoint. Preserve a safe health marker; it is not an auth identity. |
| Caddy | Change this selected route's health_timeout from 3s to 5s. | Keep health_interval=30s, health_fails=3, health_passes=1 and active checks. Foreground five-second acceptance stays fixed; transport timeouts are not changed. |
| Acceptance | Use actual paired-proxy/browser acceptance with existing memory/scan/resource protections after local configuration checks. | No repeated identical loopback experiment, capacity fixture, new orchestration layer, permanent promotion before acceptance, or inferred acceptance from the short CPU comparison. |

Why five seconds: it aligns health responsiveness with the existing unchanged
foreground criterion, which the 200% comparison actually met. It is an explicitly
proposed health-policy revision, not a retrospective pass for any failed run or
permission to lengthen client deadlines. The 3.83-3.85s measurements are not a
percentile or proof that every health/browser request fits five seconds.

Contract audit: the current proposed Caddy fragment has a health Host and marker,
but no explicit neutral User-Agent or forwarded-protocol headers. The successful
loopback client supplied those headers plus X-Forwarded-For, and contacted a
loopback peer. Caddy's active checks have their own health_headers configuration;
do not assume foreground header_up settings make these requests identical.
W-180's retained native test established a User-Agent-sensitive Webmin session
branch. Reuse its neutral User-Agent, rather than repeating that experiment.
Do not fabricate a client source header to force equality; preserve and document
the health request's intentional no-user context.

The earlier top-of-ledger wording calling the three-second health deadline
'incompatible' overstated what was measured. It is shorter than the observed
concurrent foreground timings; the existing health request's exact behavior was
not measured by W-224. That is a design concern, not a newly proven health failure.
The header proposal removes avoidable request ambiguity without claiming every
request has equal cost. Vendor reference consulted: Caddy reverse_proxy active
health-check documentation, particularly health_headers, health_timeout and
health_follow_redirects:
<https://caddyserver.com/docs/caddyfile/directives/reverse_proxy#active-health-checks>

Topology/load: the current fragment is explicitly a primary/IPv4 diagnostic,
not the final dual-stack candidate. Preserve the accepted paired-proxy and
backend-family acceptance requirement. Two address families reach one Webmin
process; do not count them as independent application capacity. Paired health
checks and browser traffic may create more overlap than W-224's three clients.
Do not promise serial checks merely by listing addresses in order, and do not
add a health-check scheduler to manufacture that promise. Retain normal runtime
health checks; the approved validation-isolation work remains a separate owner
installation boundary and is not assumed deployed by this review.

Smallest implementation qualification: check selected-host scoping/default
preservation and adapted health header/timeout values in existing owner tests.
Use retained W-180 contract evidence; no new Webmin load fixture. Reconcile exact
owner inputs and recovery before a single actual browser/onboarding operation.
That operation must observe the combined real workload and stop on existing
resource/acceptance failures; it must not silently remove a family, disable
health checks or raise limits again. No implementation, candidate seal, live
contact, retry, permanent promotion or publication occurred in this review.
W-225 stays In progress pending Aaron's policy decision; AC-013 remains pending.

### November 17 W-225 approval and W-226 local implementation

Aaron approved the proposed policy for local implementation and preparation.
The existing Webmin owner now provides the explicit selected-host CPU profile,
staging and recovery described in its CADDY_ONBOARDING.md. Foundation's 100%
default is unchanged. The proposed route has explicit health headers and a
five-second health timeout; foreground and memory limits are unchanged.

Focused checks: all 20 tests in Webmin/tests/test_proxy_recovery.py pass,
including selected-host/default boundaries, payload/preexisting-file rejection,
apply/restore ordering and changed-file containment. These use temporary files
and injected native-command responses; they do not accept target execution.
The existing offline Caddy image (v2.11.4, network disabled) adapted the proposal;
JSON assertions verified the exact headers, GET/login path, HTTP 200, 5s timeout,
30s interval and 3/1 thresholds. This is configuration syntax/contract evidence,
not full production 2.11.9 validation or capacity evidence. Local adaptation
artifacts: /tmp/webmin-policy-jbdtux49. No Webmin workload was run. Ansible
syntax validation of the changed trial include, both repository diff whitespace
checks and a redacted Webmin working-tree secret scan also passed.

Preparation boundary: the current Caddy fragment is still primary/IPv4 diagnostic
scope. A final browser candidate must bind paired/dual-stack behavior, the new
profile and changed helper inputs, current predecessor identities and existing
combined workload/recovery before sealing. No operation was registered or sealed.
Consumed bundles remain unchanged; W-224 is still the latest actual-host result.
W-147 historical attribution and AC-013 remain unresolved. No live action,
publication or permanent promotion occurred.

### November 17 W-227 paired browser bindings; W-228 owner-path gap

Local draft: `/home/aaron/code/.local-evidence/uptime-kuma/webmin-browser-candidate-fgkrltok`.
It has fresh workload tokens, private controller/target paths, four backend source
paths, six browser endpoints, selected CPU profile and exact prior Webmin control
identities. The predecessor binding comes from the retained restored W-202 inputs;
old captures are not a fresh observation of the hosts. Readiness/operator flags
remain false. No old receipt, launcher or attempt marker was copied. The proposed
recipe binds current publisher/helper/caller/fragment hashes and the accepted
release predecessor. SOURCE-INPUTS.SHA256SUMS is a preparation snapshot, not a
closed authorization graph; it must be refreshed for subsequent source changes.

The Webmin owner proposal now includes both IPv4 and IPv6 upstreams with W-225's
explicit health contract. Local checks passed: four-path/six-path and common-token
bindings, unchanged observation/scan windows, browser source/module preflight
without launching a browser, and combined parent Ansible syntax. Offline Caddy
2.11.4 adaptation checked both upstream addresses and exact health headers,
5s/30s timeout/interval, 200 status and 3/1 failure/pass thresholds. This does not
claim production 2.11.9 validation, UI acceptance or capacity. No Webmin load
fixture or target measurement was run.

W-228 is executable, not hypothetical: the current publisher unconditionally
calls `/usr/local/libexec/validate-caddy-isolated.sh`. The outer payload guard
requires application_diagnostic_scope=primary-ipv4 and diagnostic_seconds=240;
the transaction also requires node-a for validation tools, while the paired
secondary receives the same control recipe. Empty release-ID restoration is
likewise restricted to the primary diagnostic. The actual local payload guard
was invoked alone against the proposed paired recipe and returned 1 at that
scope requirement. No outer transaction or transport was executed.

This draft cannot be sealed merely by updating hashes. PLAN.md records the
bounded correction needed in the existing owner path: primary-only tools,
secondary replication with unchanged installed callers, and explicit pre-ID
versus post-exposure recovery. Do not bypass the guard, omit the helper, infer
secondary isolation capability or rebuild capacity fixtures. W-227 remains
In progress and W-228 Open. The main Caddy stream remains clean/inactive; window
and successor checks pass. The vexp completion helper is unavailable from the
parent workspace (not a Git repository); it supplied no acceptance evidence.
No live operation, DNS change, publication or permanent promotion is authorized.

Final local checks: both repository whitespace checks and the Webmin working-tree
secret scan passed. The private draft scan reported four instances of its freshly
generated workload coordination token; all were verified against that same field,
not an account credential. They remain private; no scanner exception was added.
The draft has no Git metadata. No execution sessions remain active.

### November 17 W-228 paired delivery/recovery contract reconciled locally

The existing owner payload and transaction now accept a paired 660-second browser
trial with `validation_tools_trial=primary` and no diagnostic fields. Diagnostic
scope/seconds must still occur together and retain their prior limits. Only Node A
receives validation tools. Node B accepts control metadata, rejects tool/application
payload directories and retains its installed callers; replication delivers the
application. This does not qualify isolated validation on Node B.

An independently read explicit empty target receipt permits primary tool recovery
before a release ID exists, followed by cleanup of both staged payloads. Secondary
admission has not changed services or releases. Missing/unreadable receipts still
fail closed. After an ID exists, paired B-before-A restoration and natural monitor
acceptance remain in force. No browser, memory, CPU or recovery deadlines changed.

Qualification is retained at
`/home/aaron/code/.local-evidence/uptime-kuma/w228-owner-contract-ebm_uead`:

- Existing validation-tools tests: 18 local file/payload/recovery cases pass,
  including paired success, pre-ID publisher failure and post-ID request failure.
  Secondary control-only acceptance rejects unexpected tool directories and an
  incomplete diagnostic binding.
- Existing outer dispatch tests cover paired pre-ID cleanup without secondary
  restoration/exposure, and post-ID B-before-A restoration with both monitor checks.
- Full host-only application-onboarding profile passed (session 47013, exit 0).
  Canonical shell formatting, readonly/local collisions, multi-file grep policy
  and current-tree operator documentation checks pass.

These checks exercise local source boundaries with substituted service/transport
results. They do not establish target recovery, secondary capability, browser
capacity or a complete current candidate authorization graph. W-227 retains that
exact candidate qualification before sealing. Neutral operation/outer source hashes
are reconciled; action remains none and status inactive. Permanent owner procedures
now describe this distinction. Earlier draft rejection and consumed evidence remain
unchanged; a separate W-228 source snapshot records the new preparation revision.
No live target, browser, container workload or publication was performed.

### November 17 W-227 exact paired candidate qualified; sealing remains

Private review remains
`/home/aaron/code/.local-evidence/uptime-kuma/webmin-browser-candidate-fgkrltok`.
Its `owner-workspace` is a plain-file review projection, not a Git checkout. The
main Caddy stream remains clean/inactive. The private paired operation binds both
proxies, current recipe/source hashes and primary-only temporary validation tools.
The parent binds that owner path/evidence, four proxy-to-backend paths, six browser
paths and the selected Pi CPU profile. Readiness/operator flags remain false; no
INPUTS.SHA256SUMS or live launcher exists.

W-229 reconciles a concrete qualification mismatch: existing paired cases omitted
tool delivery and seeded a source finalizer on the secondary. They now select the
paired recipe without diagnostic-only fields, deliver candidate tools only to A,
and independently verify both restored tool identities and the secondary's lack
of tool mutation. Accepted finalizer bytes came from local Git commit d048013;
accepted reconciler bytes came from d131b9d. Both match the accepted owner hashes.
Generic non-trial cases model an installed validator; they do not prove the trial
installation. Namespace substitution remains explicit and adds no capacity or
isolation claim. No substitute Webmin browser/load fixture was run.

Fresh execution of all 19 required owner cases passed in the existing offline
container, retained at `owner-authorization-evidence` (source run
`/tmp/caddy-application-qualification-c1i5s_iz`, session 52887 exit 0).
Owned-container cleanup passed. The actual authorization gate accepts the current
private graph and rejects nine altered-evidence cases. Initial gate checks exposed
missing private lifecycle metadata and absent Git context; both were reconciled
without changing tested runtime inputs or creating Git metadata in evidence.
The gate reads executable-mode metadata from the real owner's index through
explicit GIT_DIR/GIT_WORK_TREE; content identities still come from the private
graph. Parent environment retains those bindings. Earlier failed gate logs remain.

The actual payload builder accepts the exact candidate recipe; secondary archive
contains only the recipe. `exact-payload-check/receipt.json` records that result
and parent/browser/resource bindings: 600-second observation, scan after 400,
660-second owner exposure, original 1800-second native recovery and unchanged
memory limits. Syntax passed with the actual candidate vars/inventory, without
connecting to hosts. Parent paired/primary recovery-flow tests passed. The one
admission-test failure (session 76734) was W-230: umask 077 changed its intended
0755 test input to 0700. Explicit chmod fixes the test input; admission-only
session 28710 passed. Production privacy checks were not weakened.

The current host onboarding profile passed (session 34776); neutral stream,
owner policy, current documentation and whitespace checks pass. Webmin's working
scan passed. Caddy's scan reports five existing published authorization digests
in HISTORY.md; private inputs report four occurrences of the same fresh workload
coordination token. These findings were inspected, remain recorded, and add no
scanner exceptions or account credentials. The vexp helper remains unavailable
from the parent workspace and supplied no acceptance evidence.

`owner-binding-review.json` records exact owner and parent identities;
`authorization-ready-final.log` and `authorization-evidence-rejections.log` retain
the gate results. Earlier source snapshots and consumed attempts are preserved.
W-227 is qualified for sealing, not live-authorized or accepted on the Pi. AC-013,
actual browser/permission/resource acceptance and W-147 attribution remain open.
All execution sessions are retired; no live contact or publication occurred.

### November 17 W-231 source publication

Aaron authorized committing and pushing all changes. The reviewed scope is 31
server-repository paths and the three monitoring change records. Both destinations
are verified Racerx323 repositories. Private candidate inputs, tokens, receipts
and raw logs remain outside Git. Publication does not seal W-227 or authorize
installation, browser workloads or target contact. Required commit-hook results
and remote receipts are retained in
`/home/aaron/code/.local-evidence/uptime-kuma/publication-w231`.

Server commit `2a19a36bbaf5ed2f24a25a687cf3c11954fe0ab8` is pushed and
remote-verified on main. All required hooks passed after removing two duplicate
blank lines in Webmin documentation; no behavioral checks were weakened. The
initial failed-hook logs remain retained. Hosted validation run 44208718982 and
Push on main run 44208717459 are in progress. The monitoring records are next.
