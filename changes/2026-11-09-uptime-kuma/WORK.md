# Work ledger: initial Uptime Kuma deployment

## Current position

- Status: Backend-completion executed once and passed. Kuma/Webmin are active;
  service foundation, guarded dual-stack backend, backup/restore, combined scans,
  daily needrestart schedule and permanent startup are accepted. Approval is consumed.
- Last updated: November 11, 2026 (America/Chicago).
- Next action: Reconcile the separately owned DNS candidate and its conditional
  approval/expiry before proposing DNS progression. W-106 private and passive
  application acceptance passed: both nodes and combined verification accepted.
  This observation approval is consumed. Aaron separately authorized repository
  commit/push; publication qualification is in progress under W-116. No DNS or
  further live work is authorized. W-020/W-076 and documentation/closeout remain open; W-096 is
  deferred. Session 34421 exited 0 and is retired. No execution sessions are active.

## Tasks and findings

| ID | Task or finding | Acceptance/scope link | State | Closure requirement | Resolution / evidence / follow-up |
| --- | --- | --- | --- | --- | --- |
| W-001 | Define initial functional scope. | AC-009 | Resolved | Explicit service/monitor/notification boundary. | Aaron chose service first; monitors and alerts follow later. No test alert is included. |
| W-002 | Fix the dashboard name and access path. | AC-004 | Resolved | User agrees to one internal HTTPS name. | Aaron approved `uptime.local.theama.co` through existing Caddy on November 9. This does not approve source publication or live reload. |
| W-003 | Establish SSH identity and read-only host baseline. | AC-001, AC-008 | Resolved | Confirm intended target and collect bounded, non-mutating resource/runtime/network observations. | Read-only SSH succeeded with strict existing host-key verification. Host/model/OS/ARM64 and IPv4 match; hostname reports `j2-svpi3bmf.local.theama.co`. About 745 MiB memory available and 24.65 GiB root free at observation. No Podman or Kuma account/path was found by the scoped checks. Findings W-013 through W-016 retain limitations. |
| W-004 | No governing architecture exists. | AC-002, AC-010 | In progress | Prepare one proposed permanent architecture, with rationale and unresolved choices explicit. | Permanent architecture and operations drafts now define the complete candidate. Live approval reviews this design; reconcile observed behavior at closeout. |
| W-005 | Qualify a pinned ARM64 image for the Pi 3B+ resource envelope. | AC-001, AC-002, AC-006 | Resolved | Verify upstream stable release, actual architecture manifest/digest and resource budget. | ARM64 registry digest, local configuration ID and offline archive identity are separately verified in the sealed manifest. runtime-smoke-pxk7g5w0 passed actual AMD64 startup/restart/restore under the proposed controls; about 115 MB initial memory is an observation, not ARM64 capacity proof. Actual Pi execution and resource acceptance remain pending.  The proposed IPv6 loopback proxy adds a 16 MiB cap: the isolated corrective gate is 528 MiB and the future combined-foundation floor is 720 MiB. Requalify on the Pi; do not infer combined capacity from the isolated diagnostic.  Actual isolated corrective trial passed: Kuma peak 117.73 MiB, proxy 2.04 MiB, no memory-high/max/OOM events. Preflight available 728,184 KiB (711.12 MiB) exceeded the 528 MiB isolated floor but was 9,096 KiB below the future 720 MiB combined floor. Reconcile admission/capacity locally before a remaining-deployment candidate; no combined acceptance is claimed. November 11: actual pinned ARM64 runtime passed both combined checkpoints and scan-time reserve/pressure checks under the user-approved staged admission policy. Initial-service workload only; later monitors/load need review. |
| W-006 | Define runtime ownership, local persistence and safe initial administration. | AC-003, AC-005, AC-008 | Resolved | Establish runtime/service identity, filesystem/ownership, backend restriction and bootstrap path without stored chat credentials. | Proposed Quadlet uses UID/GID 1000, protected local data, read-only rootfs and loopback-only bootstrap. Native observer checks actual mounts, ports, limits, user counts and authentication setting without reading credentials. Actual target acceptance and operator account creation remain pending. November 11: actual runtime/administrator, persistent data, mounts/identity, backup/restore, guarded backend and ingress-denial checks passed. One active user, authentication enabled, no monitors/notifications; no credentials collected. |
| W-007 | Prepare DNS and Caddy onboarding under their owners. | AC-004, AC-008 | In progress | Reuse current application onboarding and source ownership; qualify both address families and WebSockets. | DNS read-only baseline completed; append-only six-record proposal and application fragment remain outside accepted production configuration. Existing immutable local image 1bab90ae19f4d9091b9529336ef023ecce44f96cf2bad6016ce95dbc04c64156 passed Unbound 1.17.1 candidate checking and Caddy 2.11.4 adaptation for both node environments. native-config-gwfqkdh5 retains inputs/status. No target staging, TLS provisioning or live application/auth/WebSocket acceptance. Owner execution definitions remain to prepare; application authority now homelab-monitoring-observability. |
| W-008 | Prepare simple declarative deployment, acceptance and rollback. | AC-002, AC-006, AC-008 | In progress | Reuse repository automation conventions; validate real entrypoints and failure boundaries. | Complete native coordinator includes controller integrity checks, boot/address prerequisites, offline runtime, boot proof, private administrator pause, actual backup/restore and guarded backend promotion. Frozen controller-only preflight passed. Runtime failure retains guard/data and requires residue review; earlier accepted prerequisites may remain. Actual execution/recovery acceptance pending. |
| W-009 | Define and qualify consistent backup/restore and retention. | AC-003, AC-007 | Resolved | Full local-data backup method, isolated restore proof, storage policy and off-node destination explicit. | Production restore checker passed against actual stopped application data in restore-final-khncnm5o/restore-cnpz4fqz/receipt.json, including immutable configuration-ID execution, database/authentication counts and cleanup. First-deployment archive budget is 64 MiB/10,000 members with no monitors/notifications; future workloads need review. Live administrator-bearing backup and protected controller copy remain pending; no recurring backup service is claimed. November 10 administrator-completion actual ARM64 backup/off-node identity, isolated restore, cleanup and source recovery passed; protected 307200-byte controller archive retained. No recurring backup service is claimed. |
| W-010 | Qualify and seal the concrete operation. | AC-001 through AC-009 | Resolved | Local checks pass; remaining target checks, immutable inputs, exact command and complete scoped bundle are reviewable. | One expanded offline candidate is sealed; frozen controller and actual boot-input checks pass locally. Exact hash, graph, command, scope, target acceptance and recovery are recorded below. Aaron approved and executed this exact bundle November 10; terminal APT simulation failure retained below. Approval is consumed; no replay or changed-input retry is authorized. |
| W-011 | Execute the authorized operation and independently accept or recover. | AC-001 through AC-009 | In progress | Required observed criteria pass, or failed/partial outcome and recovery/residue are recorded honestly. | Partial installation accepted boot/address prerequisites and all 29 package pins; Webmin remains contained after failed HTTP acceptance. Kuma image/definitions/data were installed and started, but loopback observer connection timed out; native rescue and independent inspection confirm stopped services. Private administrator acceptance, startup reboot, backup/restore, guarded backend, schedule and final DNS/Caddy HTTPS remain pending. Consumed operations are preserved; only a newly authorized continuation may proceed.  Subsequent approved loopback correction passed actual Pi HTTP acceptance over every container/direct/published family path, then returned all four units to verified stopped/guarded state. Remaining criteria above are still pending. November 11 successor exited 0: service foundation, preserved reboot identity, administrator, fresh backup/restore, guarded backend, combined scans, schedule and permanent startup accepted. DNS/Caddy HTTPS still pending; this is service-stage acceptance, not project closeout. |
| W-012 | Reconcile permanent documentation and close the record. | AC-010 | Open | Operations and architecture are current; every finding has disposition; write criterion-linked RESULT.md. | Keep repeatable procedures and enduring design out of the change journal. |
| W-013 | Requested permanent ULA is not configured. | AC-001, AC-004, AC-008 | Resolved | Establish the network owner's persistent address design and review the exact correction before deployment. | Native NetworkManager checkpoint operation prepared by the network owner appends only the permanent ULA, preserves automatic methods/routes and verifies a fresh SSH connection before committing. Source is included in the sealed bundle. No address change has occurred. Accepted November 10 through native checkpoint/reapply, fresh SSH, DAD and preserved route checks; independently retained after the later failure. |
| W-014 | Memory cgroup controller is unavailable. | AC-001, AC-006 | Resolved | Verify kernel/boot cause; prepare and authorize any needed correction/reboot, then observe the actual controller and resource enforcement. | Exact original/proposed boot bytes and native reboot/recovery play are included in the sealed candidate. Actual memory-controller availability and resource enforcement must pass after authorized reboot. No boot change has occurred. Accepted November 10 after the first reboot: changed boot ID, exact stored boot bytes, memory controller present, radio softblocks retained. Later residue inspection confirms controller remains active. |
| W-015 | Radio-disable claim needs finer verification. | AC-001, AC-008 | Resolved | Distinguish interface/rfkill/firmware state from daemon state without changing either. | Both Wi-Fi and Bluetooth are soft-blocked by rfkill. Daemon activity did not mean enabled radios. Preserve this policy; no radio changes needed. |
| W-016 | The first collector did not resolve sbin-only swap tooling or the firmware boot mount. | AC-001 | Resolved | Read `/proc/swaps` or the absolute swapon path and inspect the actual firmware mount. | Absolute swapon and /proc/swaps identify unused zram swap; firmware is mounted separately at /boot/firmware on vfat. Initial PATH/mount limitations retained; no package repair needed. |
| W-017 | A bridged container's published port may bypass an INPUT-only firewall rule. | AC-005, AC-008 | Resolved | Qualify the guard against the actual DNAT/forwarding path, including allowed proxy sources, denied direct clients and unchanged SSH. | Final actual-Ansible-rendered guard passed packet-y9e7vocf: native IPv4/IPv6 DNAT/forwarding packets, all five allowed proxy sources, both denied sources, production counter parser, unchanged SSH/unrelated table, and removal recovery. Target Podman path still requires acceptance. November 11 actual Pi ingress trial accepted: both proxy nodes returned dashboard 200 over both families; unapproved source HTTP timed out, deny counters rose by 6 IPv4/3 IPv6, SSH remained reachable, and temporary client was removed. |
| W-018 | Caddy source selection and current release need target observation. | AC-004, AC-008 | Resolved | Inspect both proxies read-only; establish actual per-family routes to Kuma and current immutable-release identity before defining the final guard/onboarding operation. | Both inspections succeeded; Caddy/Keepalived are active and native release-hash checks pass on the same release. IPv4 selects node .53/.54; active-node IPv6 selects shared Proxy ULA ::56, standby selects ::54. Proposed guard explicitly allows observed Proxy ULA plus both permanent node ULAs, avoiding unnecessary proxy route changes. No reload or failover occurred. Private proxy0/proxy1 receipts retain the baseline. |
| W-019 | Recovery access for the required boot prerequisite was unknown. | AC-001, AC-006, AC-008 | Resolved | Identify an independent way to recover a Pi that fails to return after reboot. | Aaron confirmed physical device/microSD access and console KVM. Candidate must preserve the original boot file and distinguish manual recovery from verified remote recovery. This does not authorize reboot. |
| W-020 | A rootful dual-stack bridge may change IPv6 forwarding/RA behavior. | AC-004, AC-008 | In progress | Verify the target runtime's effects and preserve existing Router Advertisement routes and global IPv6 throughout installation and reboot. | Netavark enables global forwarding; this NetworkManager-managed host already uses kernel eth0 accept_ra=0 with automatic IPv6. No generic accept_ra=2 edit is proposed. Native observer requires preserved automatic methods, persistent ULA, global addresses and IPv6 default routes after runtime start and reboot. A separately timed periodic RA renewal has not been qualified. November 11 runtime/preflight again accepted required addresses and routes after startup and promotion. Separately timed RA renewal remains unqualified; no new live observation authorized. |
| W-021 | The local smoke helper could lose its failure receipt or leave a container after a launch timeout. | AC-002, AC-007, AC-008 | Resolved | Register attempted container names before launch, clean only matching task labels, preserve the original failure and always retain cleanup results. | Cleanup corrected; revised test records its own source hash. runtime-smoke-pxk7g5w0 passed startup, restart and restored-data checks; both task containers removed. No homelab target contacted. |
| W-022 | Native local Quadlet rejected the proposed LogOpt key. | AC-002, AC-006 | Resolved | Use a log-bound configuration accepted by the relevant generator and preserve the first failed parse. | Target 5.4.2 documentation supports LogOpt, but the older local generator does not. The equivalent native PodmanArgs log bound passes both; definitions-n44a_l_4 generated bootstrap and exposed services successfully. definitions-d22wf7ed preserves the first failed parse. |
| W-023 | Local packet fixture could not inspect PID 1's network namespace after entering a user namespace. | AC-002, AC-005 | Resolved | Compare against the caller's captured network namespace identity and rerun in disposable namespaces. | Caller now supplies its captured namespace identity, checked before any network setup. packet-gr102hne passed under isolated namespaces; no host firewall was touched. |
| W-024 | Local forwarded IPv6 packet test timed out for an allowed proxy source. | AC-004, AC-005 | Resolved | Establish whether the fixture path or candidate guard is responsible and retain the failing observation. | Initial packet-0vhme_n4 failure retained. packet-b946stla confirmed failure even without the guard and an unresolved backend neighbor. Fixture now waits for link-local DAD; packet-gr102hne passed both address families. Target acceptance is still required. |
| W-025 | Minimal runtime package simulation does not establish which firewall driver the installed Netavark will use. | AC-002, AC-004, AC-008 | Resolved | Explicitly qualify a supported driver and its complete package/configuration inputs before sealing the operation. | Explicit nftables driver is supported by the pinned containers-common/Netavark versions. All nine packages were downloaded and verified against target APT metadata; ARM64 OCI archive is acquired and separately hashed. Native offline APT simulation rejects upgrades/removals; target installed driver and port behavior remain pending. November 11 accepted pinned installed package/configuration identities and actual dual-stack runtime, published backend and denied-source packet behavior. No package/driver change was needed. |
| W-026 | Existing Pi memory-controller planner is specific to Nautobot's USB storage baseline. | AC-001, AC-006 | In progress | Prepare an exact append-only boot correction bound to this Pi's saved original bytes and recovery path. | MicroSD-specific planner preserves exact original bytes/line endings, rejects drift/conflicts and passed five regression tests. Native phase preserves on/off-node copies and verifies controller/file/boot identities; reachable recovery restores the original, otherwise stops for physical intervention. Definitions and frozen controller locally qualified; target reboot/recovery not executed. |
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
| W-076 | Radio-related daemons have resident processes despite the radio-disabled host requirement. | AC-001, AC-008 | Open | Review fleet ownership/dependencies locally before proposing any service change; preserve Ethernet/NetworkManager and do not infer radio state from daemon presence. | Attribution observed wpa_supplicant and bluetooth service cgroups/processes. Combined current charge about 7.03 MiB, anonymous charge about 1.51 MiB; neither total is guaranteed recoverable or sufficient for the prior admission deficit. Inspection did not re-read rfkill or dependency policy. No stop/disable action authorized.  Local owner review found no target-specific radio-service disable profile in the searched fleet/network sources. Nautobot Bluetooth masking belongs to a different host and grants no authority here; no wpa_supplicant removal rule was found. Dependencies remain unverified; no action proposed. |
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
| W-116 | Publish reviewed pending changes and reconcile reported CI failures. | Repository publication; AC-010 | In progress | Validate and secret-scan intended sources, commit/push to verified owner repositories and verify remote refs; preserve private evidence and deployment boundaries. | Aaron requested commit and push of all changes. Four owner repositories contain pending work. Latest server-config Caddy/Nautobot jobs passed; baseline secret scanning flags the exact archived runner SHA-256, independently verified and narrowly excepted. The older Nautobot failure is superseded by later passes. CodeQL startup failure has no jobs/annotations; the October 12 Webmin run has no available logs. No live change or retry is included. |

## Execution record

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
