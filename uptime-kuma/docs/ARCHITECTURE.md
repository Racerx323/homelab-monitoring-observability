# Uptime Kuma architecture

Status: service foundation and guarded backend accepted November 11, 2026.
The dashboard name and service-first scope are agreed; DNS/Caddy and final HTTPS
onboarding remain pending. Current findings and execution status belong in the
[work ledger](../../changes/2026-11-09-uptime-kuma/WORK.md).

## Purpose and boundaries

Provide a self-hosted availability-monitoring service with an internal dashboard
at **`https://uptime.local.theama.co`**, through the existing Caddy service.
Initial deployment establishes the service, persistent state and operating
procedures. The host also requires fleet-managed needrestart, Webmin, msmtp and watchdog
coverage. Monitor selection and Uptime Kuma notification activation are later work.

This service complements existing monitoring; it does not replace Munin or
change another component's health, HA, alerting or update policy. It does not
monitor its own host independently of that host, and a single Pi is not an HA
monitoring service.

## Host and resources

The service runs on Raspberry Pi 3B+ `j2-svpi3bmf`, using Debian 13 ARM64,
Ethernet `eth0`, 1 GB physical RAM and a 32 GB raw microSD card. The intended
host addresses are `10.1.3.75/22` and `fd36:5aa8:6971:1::75/64`.
Management identity is distinct from the dashboard alias.

Preserve DHCP IPv4, Router Advertisement routing, global IPv6, resolver policy,
existing services and radio-block policy. Network ownership remains with
`homelab-network`; the application installer must not silently allocate or
replace a LAN address. A missing intended address blocks final backend exposure.

Proposed initial container budget: 256 MiB memory pressure threshold, 320 MiB
hard memory limit, no container swap, at most two CPU cores of aggregate time,
and 256 tasks. These are starting limits for the service foundation, not a claim
about supported monitor count. Require a working memory cgroup controller and
native target enforcement before accepting those limits. Any required boot
correction and reboot must be part of the approved maintenance operation.

Use the upstream slim image without embedded Chromium or MariaDB. Do not build
Node.js dependencies on the Pi. Use SQLite on local ext4 storage; no external
database, browser engine, Docker daemon, runtime socket mount or container
auto-update service is required.

## Runtime and state

Proposed runtime: system-managed Podman Quadlet, with the application running as
the image's non-root `node` user inside an isolated network namespace. Rootful
Podman is the service manager's runtime; this does not make the application
process root. Keep the container runtime socket unexposed.

Use one component-owned dual-stack bridge network. Let the native runtime
allocate private container subnets, reject conflicts with observed host routes,
and record the resulting network during acceptance. These are local container
networks, not new LAN/VLAN allocations. Do not use host networking.

Pin the release and ARM64 registry digest in the deployment definition. Prepare
the image and exact runtime packages in the reviewed offline bundle. Keep the
registry manifest identity, local immutable image configuration ID and archive
checksum distinct. Load only the approved archive and run its configuration ID;
ordinary startup must not fetch an image. Use the runtime's supported nftables
driver explicitly on this dedicated host, preserving any pre-existing policy
through a stop-and-review preflight. Keep the root filesystem read-only, provide bounded temporary storage,
drop capabilities and disallow privilege escalation, subject to runtime
qualification. If the supported image requires a writable path, document and
bound that path rather than making the whole filesystem writable by default.

Persist the complete `/app/data` tree in one component-owned local directory.
Verify actual runtime UID/GID ownership; do not infer container ownership from
the SSH account. Preserve any pre-existing data and refuse an unreviewed
installation over it. Bound container log storage separately from application
data. Monitor/data retention is decided when monitors are introduced.

## Fleet host foundation and notifications

Use the component owners' definitions instead of creating application-local
copies of fleet configuration. Installing Kuma does not establish host readiness.

| Requirement | Configuration authority | Required disposition |
| --- | --- | --- |
| needrestart | [Needrestart](../../../homelab-server-configs/Needrestart/README.md) | Install package and owner script/cron policy; qualify Debian 13 and Pi 3B+ kernel reporting before enabling daily 05:30 execution. No Pi 5 kernel filter by inference. |
| Webmin | [Webmin](../../../homelab-server-configs/Webmin/README.md) | Install and configure host administration through an owner-reviewed Debian 13 ARM64 package and management-access policy. Select the proposed SSH-loopback profile and existing sudo/PAM account; the USB drive-polling trial is not selected. |
| msmtp | [Fleet mail owner](../../../homelab-dns/msmtp/docs/FLEET_AUDIT_STANDARDIZATION_PROMPT.md) | Install msmtp and the sendmail-compatible frontend. Resolve consumer account selection explicitly; preserve unrelated accounts and aliases. |
| watchdog | [Fleet watchdog policy](../../../homelab-server-configs/watchdog/docs/FLEET-POLICY.md) | Discover hardware and current device owner; prefer qualified systemd manager coverage. A Debian watchdog daemon is an exception requiring exclusive ownership, not an automatic additional package. |
| Notification transport | [Apprise API and Mailrise](../../../homelab-notification/apprise-api/README.md) | Consume the existing shared services; do not deploy duplicate notification servers on this Pi. |

The shared SMTP endpoint is `mailrise.local.theama.co:8025`. The mail owner
includes an unauthenticated, TLS-off Mailrise account for the restricted LAN;
that policy requires endpoint/access qualification. Aaron selected Mailrise as the default: the owner template now selects
`account default: apprise`, with root and unmatched local-recipient aliases using
`notify@mailrise.xyz`. Mailgun remains available through explicit account
selection. An alias alone does not choose an account; verify root-run
needrestart/cron and other consumers against effective configuration before
enabling jobs. Preserve authenticated
account secrets externally; do not collect them for this application.

The needrestart owner schedule distinguishes direct `notify@mailrise.xyz`
notifications from cron failures to `notify.failure@mailrise.xyz`. These existing
consumer contracts do not select a Uptime Kuma alert recipient or configuration
key. Apprise credentials and notification URLs remain external secret inputs.
No synthetic email, test alert or downstream delivery is part of local validation.

Watchdog policy currently proposes 60-second runtime and 120-second reboot
settings for qualification; these are not accepted values for this Pi. Preserve
an existing owner and vendor policy during discovery, never open the device as a
probe, and do not introduce load/ping/temperature reset triggers. Configuration
adoption and real watchdog-expiry recovery proof remain separate claims.

Include all resident foundation processes in the Pi's measured resource budget.
The combined initial budget caps Kuma at 320 MiB, Webmin at 192 MiB and the
needrestart scan at 96 MiB, plus a 16 MiB native loopback proxy. Require at least
624 MiB available before starting the stopped services; admit each scan separately
using the staged policy below, preserving the 96 MiB observed reserve. This is an initial service-only
budget, not monitor-load capacity proof. The earlier standalone Kuma startup
observation does not qualify the combined workload on 1 GB RAM. Acceptance must preserve SSH, automatic networking and
radio blocks while verifying the foundation alongside the running application.

## Client and backend paths

Clients resolve the dashboard alias to the existing Proxy VIPs, not directly to
the Kuma host. The intended service A/AAAA records use the currently accepted
Proxy identities: `10.1.0.56` and `fd36:5aa8:6971:1::56`.
Canonical Proxy PTR ownership is unchanged.

Caddy terminates internal HTTPS with the existing trust model and forwards
HTTP/WebSocket traffic to the Kuma backend on TCP 3001. Preserve certificate
validation; never work around trust errors by disabling it. Use a separate
application fragment through Caddy's immutable-release process.

Proposed dashboard client allowlist: the supplied LAN IPv4 network
`10.1.0.0/22` and ULA network `fd36:5aa8:6971:1::/64`. Additional client networks
require an explicit access decision; do not assume VPN or public access.

Publish backend ports only on the approved host IPv4, permanent ULA and loopback
addresses. A component-owned host firewall guard admits backend traffic from
the enumerated Caddy source addresses and local administration, rejecting other
remote access to TCP 3001. Include the shared Proxy ULA in the reviewed source
set because the active node currently selects it for this backend; do not add
proxy routing changes merely to force a different source identity. Both node
permanent identities remain allowed for standby and role changes.
Enforce the guard before container startup and
test the actual published-port/DNAT path; an INPUT-only rule is insufficient for
a bridged container. Never flush the whole host ruleset.

The backend's HTTP transport is confined to this approved internal path. Caddy
owns client TLS and source-network restriction; Uptime Kuma owns application
authentication. Verify HTTP, WebSocket, authentication and each intended address
family independently; a successful root-page request alone is insufficient.

The prepared Caddy health contract is GET `/dashboard` with exact status 200.
The administrator-bearing application redirects `/`; do not use that redirect
as a failed backend health check. HTTP health does not establish authentication
or WebSocket acceptance. The proposed single application uses two backend
addresses, with passive exclusion disabled and HTTP keepalive off; deployment
remains subject to the Caddy owner's onboarding review.

Local IPv6 administration uses an IPv6-only systemd socket on ::1:3001,
forwarding through the installed systemd-socket-proxyd to 127.0.0.1:3001.
The application retains its dual-stack bridge and IPv6 listener; direct and
remote backend IPv6 are separate paths. Podman publishes IPv4 loopback and,
after authorized promotion, the explicit IPv4/ULA backends. It does not publish
::1 through container NAT. The socket is wanted by and stopped with the
application; the proxy is unprivileged, capped at 16 MiB/no swap/10% CPU/16 tasks.
It forwards TCP without terminating HTTP or WebSocket. During controlled recovery,
all four units require the same ephemeral permit. Releasing those temporary
recovery guards remains a later reviewed transition. This transport correction
passed bounded ARM64 target acceptance; the service remains stopped and guarded.
Full foundation, startup and backend/HTTPS acceptance remain in the work ledger.

## Initial administration

Start in a loopback-only bootstrap mode. Establish the first administrator
through an operator-owned SSH tunnel before exposing the backend to Caddy.
Keep authentication enabled. Do not place passwords, session tokens, recovery
codes or private keys in Git, logs, manifests or chat.

Normal dashboard exposure follows successful administrator setup and its
acceptance checks within the authorized operation. If operator interaction is
needed, retain the work position and keep the service contained until it is
complete. Do not publish an unclaimed setup page to the LAN or public internet.

## Lifecycle, backup and recovery

Systemd owns startup, bounded restart and shutdown. Require the firewall and
network dependencies to be ready; prevent unlimited restart loops. Reboot
persistence and resource enforcement require target acceptance. Preserve
management access throughout prerequisite and application changes.

Back up the complete local data directory consistently, using a controlled
service stop and protected off-node copy. Restart and verify the source service,
then prove restore with the pinned image in an isolated environment. Retain
actual pre-upgrade data before any future version migration. Upstream v2 JSON
export/import is not a database backup or recovery method.

Rollback restores only reviewed component changes and the saved original state.
Do not delete persistent data as routine rollback. A failure before mutation
performs cleanup only. If boot/network access cannot be recovered remotely,
report manual recovery and use the prearranged physical/recovery path; loss of
SSH is not proof that rollback or reboot succeeded.

The operating procedure owns exact deployment, administration, backup/restore,
upgrade and recovery commands. Accepted version identities and terminal results
belong in component records and change results, not in this architecture.

## Ownership and sources

- `homelab-monitoring-observability/uptime-kuma` owns this application and its procedures.
- Server inventory owns host membership and stable hardware facts.
- `homelab-network` owns permanent LAN addressing and network policy.
- `homelab-dns` owns authoritative service and management DNS records.
- `Caddy/` owns proxy fragments and the HA immutable-release lifecycle; see
  [application onboarding](../../../homelab-server-configs/Caddy/docs/APPLICATION_ONBOARDING.md).
- [Upstream installation](https://github.com/louislam/uptime-kuma)
  defines local persistent storage and the service port.
- [Upstream image variants](https://github.com/louislam/uptime-kuma/wiki/Docker-Tags)
  distinguish slim and non-root images and their feature limitations.
- [Upstream database migration notes](https://github.com/louislam/uptime-kuma/wiki/Migration-From-v1-To-v2)
  explain the data-directory backup requirement.
- [Podman Quadlet](https://docs.podman.io/en/v5.4.2/markdown/podman-systemd.unit.5.html)
  governs native unit and network behavior for the candidate target runtime.

## Proposed guarded steady-state startup

Keep the four existing Kuma permit guards. A shared native startup dependency
creates their ephemeral permit from protected owner state. While deployment is
pending, that state permits at most one changed boot ID within forty minutes.
Expired, missing, contained or backward-clock state denies startup. Webmin keeps
its own persistent configuration guard and also depends on this startup check.

A persistent systemd deadline timer provides controller-loss containment across
reboot. Failure stops Kuma, its network/socket/proxy, Webmin and owned temporary
restore/ingress containers; it removes startup permits and the notification
schedule while retaining application data, backups and configuration. After all
remaining service checks pass, accepted owner state permits ordinary future
startup. Existing guards are preserved; the pending timer is disabled. The
[startup helper](../scripts/startup-permit.py) enforces this narrow boundary;
Ansible remains the deployment coordinator.

A separately reviewed administrator-bearing continuation can renew contained
startup authority while retaining an already accepted reboot. It preserves the
exact predecessor state, requires the same boot identity and independently
verified protected operator acknowledgement and administrator configuration,
and permits no further pending reboot. Renewal is exclusive and cannot overwrite
its predecessor archive. It retains the same deadline, guards and remaining
acceptance requirements; it never creates an administrator or edits application
data to satisfy a precondition.

The approved staged admission policy starts the stopped services only with at
least 624 MiB available. Service caps remain Kuma 320 MiB, Webmin 192 MiB and
loopback proxy 16 MiB; the remaining allowance is a 96 MiB host reserve. Preserve
cumulative pressure counters, healthy requests, no max/OOM/OOM-kill events and no
increasing pressure counters during settled acceptance. Actual Pi acceptance is
required; local AMD64 fixtures establish only their exercised behavior.

### Meaning and limits of the admission budget

Use actual unadjusted Ansible-path observations and retain numeric evidence before
assertion. Existing host and orchestration use is already reflected in
MemAvailable. Never add back an estimated observer cost or file/cache charge,
average readings into a pass, or retry admission until a passing sample appears.

| Stage | Fresh available-memory requirement | Accounting |
| --- | --- | --- |
| Start stopped services; no scan | 624 MiB | 320 + 192 + 16 service caps + 96 reserve. |
| Launch scan observer alongside services | 224 MiB | 96 scan + 32 observer + 96 reserve; resident services are already included in the reading. |
| Start scan with observer resident | 192 MiB | Fresh additional check for 96 scan + 96 reserve; do not add observer usage back. |
| During scan | 96 MiB sampled reserve | Host and every visible finite ancestor allowance; missing required evidence fails. |
| Start isolated restore after source is stopped | 416 MiB | Replacement 320 MiB instance + 96 reserve. |
| Start ingress client; no scan | 160 MiB | 64 MiB client + 96 reserve. |

Transient stages are serialized; restore never runs beside the source and the
schedule is enabled last. The separate 32 MiB observer is active only for scans,
not concurrently with restore or ingress. Core service caps, no-swap controls,
required foundation components and radio/network policy remain unchanged.

This replaces the former 720 MiB simultaneous-cap admission model. It accepts
measured stage headroom rather than provisioning every service at its cap at once.
A service can grow after admission and a short spike can occur between samples.
MemoryHigh throttles/reclaims and MemoryMax limits consumption; neither establishes
an enforced host reserve. The sampled 96 MiB requirement therefore is not a hard
reservation or guarantee against OOM. Service-only acceptance does not qualify
future monitors/browser checks or other load. Review workload growth separately.
A container's host MemAvailable is not its parent cgroup allowance; qualify both.

### Admission and observed acceptance have different roles

The foundation owner installs one reusable guard/observer used by all three
combined acceptance checkpoints (before reboot, after reboot, after guarded
promotion) and the scheduled producer. Acceptance uses a list-only scan and
checks actual kernel reporting; the scheduled path retains the real producer,
including its notification children within the same 96 MiB/no-swap/one-CPU limit.

A common nonblocking lock and unused-unit checks reject overlap or stale unit
adoption. Before observer launch, preserve the 224 MiB reading. Once resident,
require 192 MiB before the scan. Sample at nominal 200 ms, rejecting gaps above
one second, reserve failure, scan limit/OOM events, missing active-scan samples,
invalid native peak/no-swap data, unsuccessful exit or cleanup failure. Retain
exact MemoryPeak before collecting the scan unit. Deployment failures enter the
existing application containment path; scheduled failures stop owned scan work,
leave applications alone and surface through cron's existing failure transport.

List-only acceptance retains its 90-second native scan start timeout and
120-second observer runtime. The scheduled producer retains its own five-minute
scan timeout and 30-second kill grace; an outer 420-second unit bound includes
notification completion, followed by five-second stop allowance. The scheduled
observer has a 440-second runtime, the guard a 455-second subprocess wait and the
cron command a 470-second outer bound plus five-second kill allowance. No new
retry or success claim is allowed after a refusal. Native deadlines still bound
processes if the controller disappears; unreachable cleanup is not proven cleanup.

The daily job remains at 05:30 and is installed only after required acceptance.
An insufficient-headroom run is skipped with nonzero status and a failure record,
not marked successful. The guard does not send synthetic tests. Cron failure
transport remains outside the producer cgroup as in the existing owner schedule;
it is host activity, not a separately reserved allocation. Owner qualification
uses local mail substitutes; live notification authority remains separately scoped.
Deployment records own observed outcomes and the current authorization state.
