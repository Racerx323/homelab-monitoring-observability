# NTP package and plugin qualification

Reviewed October 20, 2026. This qualifies retained package bytes and local fixtures;
it authorizes no host contact, installation, plugin selection or service change.
The [prerequisite review](ntp-monitoring-review.md) owns the proposed metrics and
remaining node/master acceptance requirements.

## Package integrity and maintainer behavior

All 15 packages selected by the accepted no-recommends simulation are already
cached. Their exact version, architecture, size and SHA-256 match the existing
installation manifest. The narrowed [package review manifest](../../../homelab-ntp/ntpsec/configs/munin-package-review.json)
records the complete selection, including munin-common, munin-node and
munin-plugins-core 2.0.76-5. No download or installation was needed for review.
The retained archive inspection found maintainer scripts only in those three
Munin packages; six scripts pass shell syntax checks. Trigger/conffile inputs
were retained separately. Dependency packages in this selection add no maintainer
scripts of their own; that does not waive ordinary dpkg/package trigger handling.

The important package effects are:

- munin-common creates the system munin account if absent and requests tmpfiles.
- munin-node changes its log/config-directory permissions, runs
  `munin-node-configure --shell`, executes the resulting shell to create automatic
  plugin links, and requests init/systemd enable/start or restart. Its Perl-major
  upgrade trigger can request restart. Service suppression alone does not prevent
  plugin execution or selection.
- The default node configuration binds `host *` with loopback-only allow rules;
  default plugin settings include root-running rules for unrelated applications.
  Replace or restrict the effective selection/settings before reviewed startup.
- Node purge removes dangling links/logs; plugin-core purge removes plugin-state
  files. Purge is not the proposed recovery action for an installation failure.

Before sealing installation, include both an autoconfiguration boundary and
first-start controls. A private PATH shim for the exact unqualified
`munin-node-configure` call was tested against the packaged init_plugins function
with only temp/log paths rewritten: it produced no plugin commands and cleaned
its temporary files. This proves the function-level guard, not the full dpkg
transaction. The later installer must pin these script bytes, control PATH,
validate the complete hook/first-start/recovery path, restrict service exposure
and restore normal tooling after configuration. A service mask alone is
insufficient because the package calls helper unmask/enable logic.

## Real-package first-start and recovery qualification

Five fresh, network-isolated systemd containers passed on October 20, 2026,
using [the fixture](../tests/test_ntp_install_systemd.py) and the exact verified
Architecture-all Munin 2.0.76-5 archives. The [image definition](../tests/Containerfile.ntp-install)
provides an amd64 Debian Trixie dependency environment. Private evidence retains
the image identity, source digest, complete commands, package output, protocol
checks and per-case results under munin-install-qualification-20261020-v1.

| Scenario | Observed result |
| --- | --- |
| Success | Real dpkg install completed; private PATH shim suppressed autoconfiguration; restricted config survived; policy and systemd condition blocked premature starts. Explicit permit enabled loopback-only config/fetch for load; cleanup stopped the listener |
| Partial dpkg failure | A real invalid-archive error after common-package installation left the fixture contained and non-serving |
| Configuration failure | Failure after package installation remained non-serving with the startup guard retained |
| Failure after first start | Recovery stopped the real daemon and removed its permit; no listener remained |
| Foreign policy edit | Recovery preserved the foreign policy bytes and reported held; guard retained, permit absent, no listener |

Each case preserved the unrelated dummy service's PID, invocation and restart
count. The pre-existing policy fixture's unrelated-service result was delegated
unchanged; normal recovery restored its exact bytes. Completed containers are
stopped and retained. No production host was contacted and no message was sent.

This closes the isolated package-hook/first-start/recovery mechanics check.
It does not qualify ARM64 native dependencies, the real NTP service, production
IPv4/IPv6 binding, selected profile privileges or the complete future installer.
The fixture is container-only and is not a production installer. The eventual
installer must use these qualified controls, reject foreign/symlink inputs,
preserve the real node's accepted state, and pass its own recovery tests before
sealing. Do not infer target acceptance from the dummy-service continuity check.

## Actual installer and selected-profile qualification

The reusable [installer](../scripts/install_ntp_node.py), rather than a fixture
reimplementation, passed eleven fresh network-isolated systemd scenarios:
success, partial dpkg failure, guarded/configured/started failures, foreign
policy, foreign guard, foreign configuration, resumed CLI recovery,
pre-activation configuration drift and held CLI recovery. Held recovery returns
nonzero. Every scenario preserved the unrelated service's PID, invocation and
restart count. Packages remain installed but non-serving after containment;
foreign state is preserved rather than overwritten.

The success case proved both exact loopback listeners and real Munin protocol
fetches over IPv4 and IPv6. All nine selected plugins passed config/fetch under
their installed settings. An instrumented fixture ntpq proved the time query
ran as munin; root-private success records proved root-only reader access.
Missing records first reported evidence=0, then the synthetic fixture records
reported evidence=1. No live job result or notification is inferred from these
synthetic records.

The final source also checks exact pre-existing policy state, complete protected
files, running time-service identity, closed source/package sets, nonroot Munin
identity and final source/settings/link/guard readback before activation. It uses
literal per-address port entries and makes only its configuration directories
searchable. Original failed fixtures for packaged README handling, per-address
binding and directory permissions remain retained with their diagnosed fixes.

Private evidence is munin-production-installer-qualification-20261020-v1, with
release-inputs.json and release-* results. It uses an amd64 Trixie environment
and the three exact Architecture-all Munin archives. The production path requires
all 15 pinned packages and arm64; native ARM dependencies, actual NTP service
continuity, target parsing/runtime and external polling still need the approved
target stage. This qualifies the installer payload, not a production deployment.
The fixture's exact existing policy delegation was tested; production should
use the accepted policy absence unless a separate existing-policy review qualifies
otherwise. Inventory now selects ntp for j2-svntp1; no installation bundle or live
installation is accepted yet.

The [selected profile](../node/profiles/ntp/README.md) replaces the earlier reserved
NTP concept. Five package plugins and four custom readers are selected. Two
root-only metadata readers avoid broad ACL/sudo/raw-log grants. Maintenance
heartbeat producers are explicitly not deployed and remain an NTP-owned stage;
the reader reports that absence as a fault. Retain it in OBS-01/OBS-03/OBS-07.

## Earlier packaged-plugin smoke results

Exact sources were retained from the verified archives. Eight candidate plugins
had config and fetch modes exercised, for 16 successful local runs. df/df_inode
used a fixed df fixture; ntp_offset used a private ntpq peer fixture, preventing
network queries. Other baseline plugins read only the workstation's local system
counters; these are not Pi or live-node acceptance results. The first shell runs
failed because the extraction omitted packaged plugin.sh; after restoring that
exact helper, only the affected runs were repeated. Original diagnostics remain.

| Plugin | Static/local disposition | Required live qualification |
| --- | --- | --- |
| cpu, load, memory, uptime, processes | Config/fetch passed with packaged helpers; baseline candidates | Validate actual Pi output, least-privilege identity, bounded runtime and sensible load limits |
| df | Config/fetch passed; reports percentage used with default 92/98 limits | Map root/statistics mount and add an absolute available-byte measurement for the 10 GiB floor |
| df_inode | Config/fetch passed; default 92/98 limits do not implement the accepted 5 percent free-inode floor | Review a 95-percent-used critical ceiling against actual field semantics and configure recovery/alert behavior |
| ntp_offset | Config/fetch passed against a selected-PPS peer fixture; delay/offset/jitter units and millisecond-to-second cdefs checked | Pin /usr/local/bin tool resolution, selected-peer/missing-data behavior and local query permissions; this plugin alone does not prove reach/leap health |
| ntp_states | Defer: requires Net::DNS outside the selected set and performs resolver queries | Use an explicitly approved dependency/query scope or a reviewed local numeric-only alternative |
| ntp_kernel_err, ntp_kernel_pll_freq, ntp_kernel_pll_off | Defer: source compares ntpq version digits against legacy 4.2.7 and can select ntpdc for NTPsec 1.2.5 | Replace/qualify the query and parser before considering selection; do not install another time stack to satisfy the heuristic |

The candidate now supplies absolute free bytes, available inode percentage,
metadata-only statistics freshness/growth and explicit job-success evidence
handling. Its fixed readers and settings are selected; sustained storage/growth,
actual job-success producers and master alert delivery remain unaccepted.

## Remaining master and installation gates

The approved master qualification completed October 20. Current IPv4/ULA routes
to the fixed node addresses both use eth0 and the observed master source addresses.
The active NetworkManager profile uses automatic IPv4/IPv6 methods with no
explicit addresses. Captured addresses are dynamic; no temporary flag appeared.
The later separately approved controller inspection verified the existing IPv4
reservation against the master MAC and route source. Master-local policy capture
found addr-gen-mode=default, unset stable-id and no effective generation/stable-id
override. The later saved-profile follow-up captured installed 1.42.4 policy
documentation and found the active profile in `/run`, not persistent `/etc`
storage. The subsequent approved same-UUID profile save passed native `/etc`
readback with unchanged effective settings, route sources and manager identity.
Configured ULA policy persistence is accepted; empirical renewal/reboot evidence
remains a checkpoint at the next approved maintenance window.
See the [address inspection outcome](ntp-monitoring-review.md#address-inspection-outcome--october-20-2026).
Do not infer either random rotation or proven cross-boot permanence.

Cron invokes munin-cron every five minutes and also references a daily limits job.
Known source markers and bounded update/limits log summaries show recent activity
with no ERROR/FATAL markers in the sampled data. This qualifies recent scheduler
activity, not delivery or polling of the unregistered node. Captured configuration
still has no active contacts or explicit limit overrides. The operator approved
master-owned alert evaluation/delivery and both routes in the
[ownership decision](ntp-monitoring-review.md#approved-ownership-and-address-policy--october-20-2026).
Contact configuration, stale/error handling and exact approved delivery tests
remain open.
No plugin, polling, job, notification or network change ran during inspection.

Before installation preparation, resolve permanent master identity, inventory
assignment, access scope, representative growth/storage budgeting and the alert
implementation. Local metric/privilege and installer recovery qualification are
complete with the limitations above. Target acceptance remains separate.
Retain these gates under OBS-02/OBS-07 in the NTP readiness checklist.

The later static-address decision supersedes preserving the automatic master
profile: desired master sources are `10.1.3.83` and `fd36:5aa8:6971:1::83`.
Network/DNS acceptance is a prerequisite to sealing the separate
[node](ntp-node-installation-review.md) and [master](ntp-master-acceptance-review.md)
stages. The dashboard must also respond over both families. The prior profile
save and eleven installer fixtures remain retained evidence of their exact scope.

## Reconciled handoff — October 21, 2026

The [current prerequisite record](ntp-monitoring-review.md#accepted-prerequisites--october-21-2026)
now closes static master identity and Munin/svmf DNS, with sampled native Apache
HTTPS on both intended literals. Earlier automatic-profile observations remain
historical. Inventory already selects ntp for j2-svntp1. No package/plugin or
installer runtime changed for this reconciliation; retain existing qualification
without rerunning its containers. Fresh ARM64 node/package/access readiness and
the outer production bundle remain open. Producer writes and native scheduled
dual-family master polling/limits/delivery are separate unfinished work; the
reconciled three reviews retain these gates rather than treating network/DNS
acceptance as complete monitoring acceptance.
