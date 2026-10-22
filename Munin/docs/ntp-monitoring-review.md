# NTP monitoring dependency and profile review

Reconciled October 21, 2026. Inventory selects the qualified NTP profile for
j2-svntp1. Genuine producers were installed and accepted; the node installation
initially failed health acceptance and was contained; the separately approved
classifier correction/start passed node runtime acceptance at 13:04:08 CDT.
Master registration remains
undeployed. Outcomes do not establish scheduled jobs, polling or delivery. October 20 node/master inspections
remain retained observations, not a fresh package/service baseline.

The inventory master is the single `svmf` host, also in the notification group.
Munin runs natively there; Apprise API and Mailrise run as Podman containers on
the same host. The former monitoring/notification host records were placeholders,
not separate hosts or intended FQDNs. Container privilege/ownership is not inferred.

## Current desired state and separate reviews

Inventory explicitly selects `ntp` for j2-svntp1. The master is the shared
native Munin/Apache host svmf; Apprise/Mailrise remain Podman services there.

### Accepted prerequisites — October 21, 2026

| Owner stage | Accepted result | Evidence and limit |
| --- | --- | --- |
| Network | Static master 10.1.3.83/22 and fd36:5aa8:6971:1::83/64; actual .83/::83 NTP route sources, RA global/default route and original generated ULA retained | [Committed 09:58:00 CDT](/home/aaron/code/.local-evidence/homelab-network/current/svmf-static-network-20261021-v1/outcome.md), archive 935f60fd1dab11fa3a209efb98be40b3657143c2b9148065a8640db0ac160b8e; physical reboot/renewal persistence unobserved |
| DNS | munin/svmf A .83, AAAA ::83 and canonical IPv4/IPv6 PTR to svmf; node/loopback/VIP family answers and paired DNS/Caddy health passed | [Accepted 10:12:30 CDT](/home/aaron/code/.local-evidence/homelab-dns/current/munin-svmf-dns-deployment-20261021-v1/outcome.md), archive 81d6544c533baa2592c9e63c093f2be2f403400309ffc244fb0561840a827e30; client cache/FQDN SSH refresh unaccepted |
| Dashboard transport | Native Apache, verified HTTPS for munin.local.theama.co on 443; HTML, /static/style-new.css and sampled CGI PNG passed both intended literals | Network terminal checks above; [vhost authority](../../Apache2/configs/001-munin.theama.co-ssl.conf); sampled graph does not prove freshness or j2 metrics |

These consumed operations require no replay. The old generated ULA is retained
for existing consumers, but is excluded from new node allowlists. The exact
poller identities are .83/32 and ::83/128. DNS cluster Caddy is separate from
svmf's native Apache. Do not reopen network assignment or Apache ACL deployment
as a missing prerequisite; recheck current state within each new approved stage.

### Separate stage handoff

| Review | Reconciled readiness | Still needed before execution |
| --- | --- | --- |
| [Node installation](ntp-node-installation-review.md) | Inventory/profile and master network/DNS accepted; installer payload locally qualified | v3 initially contained; separate classifier correction/start accepted all nine installed paths, literal listeners, independent IPv4/IPv6 TCP and NTP continuity. Receipt consumed; master polling remains separate |
| [Job-success recording](../../../homelab-ntp/ntpsec/docs/monitoring-job-success-review.md) | Genuine hooks/helper installed and accepted at 12:02:25 CDT | Execution consumed; observe each actual scheduled completion independently; no jobs or synthetic records were invoked |
| [Master acceptance](ntp-master-acceptance-review.md) | Commissioning and exact repository reconciliation accepted; contacts none | October 21 16:00 observation accepts three scheduled cycles, fresh RRD updates and all 40 dual-family HTTPS requests. Both maintenance records absent (0/U), mail U; actual canonical source attribution, limits/transitions, delivered alerts, client coverage and persistence remain open |

Node and producer preparation can proceed independently. Node acceptance may
retain the expected missing-record faults; it must not fabricate success or
suppress the jobs plugin. Final master health/alert acceptance depends on both
accepted stages and actual scheduled job completion. Dashboard access, TCP 4949
listeners and intended-family scheduled polling each need their own evidence.

Both corrected v2 read-only inspections completed October 21 with exit 0 and
sealed continuity: [node/producer outcome](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-node-producer-readiness-20261021-v2/outcome.md) at 10:51:48 CDT,
[native-master outcome](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-native-master-readiness-20261021-v2/outcome.md) at 10:51:32 CDT. Receipts are
consumed. Failed v1 attempts and the tested bootstrap correction remain retained.
No target mutation, plugin/job/limits invocation, CGI/HTTPS/DNS query or message.

Node: ARM64/701 package records; exact 15-version cached simulation, zero
upgrades/removals, no account/unit/listener/config or preexisting policy/installer
paths. NTP config/retention rule/reporter hashes match repository sources. Both
success records remain missing. Source routes and capacity floors passed this
sample; scheduled rule success, sustained growth and alerting are unaccepted.
Master: Munin 2.0.73-1, no j2 entry/active contacts in inspected config, five-minute
cron/recent limits activity and unchanged accepted Apache vhost. Captured
INET6/MultiHomed/address excerpts do not prove scheduled polling over both families.

The approved producer stage passed and node stage failed/was contained, in that
order. Their linked reviews now carry terminal outcomes; receipts are consumed.
The separate correction/start now accepts the enabled/running node. Do not replay
consumed stages or reuse the old package pin. The [master design](../master/ntp-design.md) resolves one canonical IPv4
series plus scheduled full-protocol checks over both source-bound families,
limits/unknowns, fixed Mailrise contacts and recovery. Native activation/recovery
qualification passed and commissioning committed with the repository reconciled.
Separate read-only observations completed at 16:00 CDT with consumed receipts.
Three scheduled cycles and fresh graph serving passed; genuine maintenance
completion and remaining source/limit/client/delivery gates stay open.
Contacts stay disabled; later delivery requires exact-message approval.
The [readiness checkpoint](../../../homelab-ntp/ntpsec/docs/PRODUCTION-READINESS.md#decision-and-next-action)
retains actual scheduled jobs, collection/graphs/delivery and longer observations.
No preparation or local test authorizes live execution.

## Observed prerequisites — October 20, 2026

The separately approved inspections completed without mutation. Cached node/core
candidates are Debian Trixie/main 2.0.76-5; a no-recommends simulation adds 15
packages with zero upgrades/removals and no competing time daemon. Exact archive
qualification and package-script review passed offline, with the limits recorded
in the linked qualification document. No node package was installed by these inspections.

The native master has Munin 2.0.73-1. Its captured main configuration contains no
j2-svntp1 node entry, active contact definitions or explicit limit overrides.
Default/plugin limits and external notification remain unknown. The cron file
has a */5 row. The later approved qualification identified munin-cron and daily
limits references, recent update/limits activity and both current route sources.
Those observations do not establish address persistence or alert delivery.
Do not infer a master upgrade from the version difference; qualify actual polling
and plugin behavior. Both detailed outcomes remain in private NTP operation
evidence and the NTP readiness checklist carries the remaining gates.

The [package/plugin qualification](ntp-package-qualification.md) records verified
archive bytes, maintainer-hook behavior, local fixtures and deferred plugins.
The [NTP candidate profile](../node/profiles/ntp/README.md) now defines the local
metric/privilege selection and installer contract. Its existence does not select
a live host or authorize deployment.

## Dependency review

Inspect the node's cached APT policy, candidate metadata, dependency graph and
`apt-get --simulate --no-install-recommends install munin-node munin-plugins-core`.
No refresh, download or installation is included. Record cache age, exact origin,
version, architecture, dependencies and any removals/upgrades. Cached data may be
stale; review source configuration and approved refresh separately if needed.
Reject a later installation plan that replaces the source-built time stack or
adds a competing time daemon. Do not select munin-plugins-extra without evidence
that a required metric needs it. Package installation scripts may enable services;
the eventual installation review must restrict first startup before exposure.

Inspect the master separately for its installed versions, actual configuration,
node definitions, scheduling, network source candidates and contact/limit presence.
Do not infer that native packages or the standard configuration path prove the
active deployment. If the master lives elsewhere or in a container, retain that
as a gap and scope its configuration inspection before registration.

## Proposed measurements and privilege

Selection is now explicit in the linked candidate: five package plugins run as
munin; fixed time/storage readers also run as munin; statistics metadata and
private job-success records use two fixed-scope root readers. The following
table retains the acceptance requirements. The candidate's unit and actual
installer tests do not replace Pi-native output or master collection acceptance.

| Measurement | Candidate implementation | Required qualification |
| --- | --- | --- |
| CPU, load, memory, uptime and process count | Selected package-provided baseline plugins, subject to package review | Confirm actual shipped names, useful output and minimal execution identity; do not enable every autoconfig suggestion |
| Root/statistics filesystem byte and inode usage | Package-provided df/df_inode candidates plus an absolute available-byte field if needed | Prove field units and mount mapping. Percentage-used output cannot enforce an absolute 10 GiB floor |
| Available bytes and inode fraction | A reviewed statvfs-based measurement if selected package plugins lack these fields | Use f_bavail and f_favail/f_files. Preserve the accepted 10 GiB and 5 percent free-inode floors; define warning/recovery behavior and prove master alert receipt |
| Time-source health, offset/jitter/reach/leap | Source-built NTPsec tools with an explicitly reviewed local query/plugin | Confirm installed command path, output parser, restrictions and permissions; do not assume distro ntpq compatibility or install another NTP stack |
| Four-stream statistics freshness and bounded growth | Metadata reader scoped to /var/log/ntpstats | Deduplicate hardlinked inodes, distinguish UTC rollover/reset, do not read raw records. Observe event-driven protostats without alerting merely because it is quiet |
| Retention and reporting scheduler health | Reviewed last-success/state evidence for the particular rule/job | A timer invocation does not establish rule execution; a quiet successful needrestart scan need not send mail. Missing/stale results need an owned alert path |

Read-only statistics access needs review of UID/GID/modes and plugin identity.
Prefer a narrowly scoped group/read grant if necessary; do not recursively change
file ownership, make raw logs public or run all plugins as root. Existing
root-owned protostats files require explicit consideration. No permission change
is authorized here.

The recorded minute-long sample proves some activity, not a representative growth
budget. Select sampling cadence/duration and account for at least 31 days plus
headroom under the NTP plan. Distinguish collection failures, counter resets,
rollover and low activity from a daemon fault.

## Master, access and alerts

### Historical ownership and address policy — October 20, 2026

The initial preserve-network decision below was superseded by the accepted
October 21 static deployment above; alert ownership remains current.

The original instruction was to preserve networking and verify its existing IPv4 DHCP
reservation and effective stable ULA policy before accepting permanent node
allowlists; no fixed-address conversion, renewal, profile activation or reboot
is authorized. Current route-source observations alone do not prove persistence.
The controller reservation and master-local policy inspections are separate
read-only stages. Missing reservation fields or unsupported APIs remain gaps.

svmf.local.theama.co owns Munin alert evaluation and delivery through Mailrise.
Aaron is the operator. Problems use `notify.failure@mailrise.xyz`; recovery/status
uses `notify@mailrise.xyz`. This is an approved ownership/routing decision, not
an installed contact configuration or delivery acceptance. Define per-metric
limits, unknown/stale-data handling, recovery criteria and delivery-failure
visibility before activating contacts. Preview exact recipient, subject and
body and obtain approval before each delivery test. No test is authorized by
this ownership decision.

### Address inspection outcome — October 20, 2026

The separately approved controller inspection verified an enabled existing IPv4
reservation matching the master MAC and observed IPv4 source. The master-local
capture again found the same IPv4/ULA route sources. Its profile uses
addr-gen-mode=default with no effective generation/stable-id override;
stable-id is unset and runtime temporary addressing is disabled. Root-owned
host-identity files are present as regular files; only metadata was inspected.

Upstream [IPv6 settings](https://networkmanager.dev/docs/api/latest/settings-ipv6.html)
map default without a global override to stable-privacy. The
[connection settings](https://networkmanager.dev/docs/api/latest/settings-connection.html)
derive the unset stable-id fallback from the connection UUID. These support a
conditional stable-generation interpretation, not acceptance of the installed
version's defaults, saved-profile state or observed renewal/reboot persistence.
That inspection left permanent ULA acceptance open; the October 21 static
deployment above now establishes the configured poller identity. No node
allowlist, master contact or polling was activated by these inspections.

The subsequent approved saved-profile inspection confirmed NetworkManager
1.42.4 and located the active UUID under `/run/NetworkManager/system-connections`.
Installed policy documentation was captured. There is no proof here of an
equivalent saved `/etc` profile. The first follow-up held at an overly narrow
filename/path check; the corrected read-only stage completed without mutation.
The subsequent approved network-owned same-UUID profile save passed: a protected
persistent `/etc` profile retains the effective configuration and both route
sources, with unchanged NetworkManager and host identity. Configured ULA policy
persistence is accepted. No activation, reapply, reload, renewal or reboot ran;
empirical source comparison remains at the next approved maintenance window.

Use the accepted static master sources above and revalidate actual route/source
selection in the new approved node/master stages before activation. Host interface addresses are
candidates, not proof of the address used to reach the node. Route lookup, approved
node queries and master polling require their own reviewed acceptance scope.
Do not authorize the whole management LAN merely because Webmin uses that scope.

Keep node identity, bind addresses, TCP port, intended families and the master's
node registration consistent. Validate each selected plugin's config and fetch
outputs only under a scope that authorizes plugin execution and its side effects.
Then prove intended-family polling and fresh data across an agreed interval.

Inspect whether the active master runs munin-limits and has applicable limits and
contacts. Do not export contact commands, credentials or URLs from configuration.
Set owner, cadence, stale/missing-data handling, destination and response procedure.
Notification tests require preview and approval of the exact recipient/content;
configuration presence and SMTP acceptance do not establish downstream delivery.

## Exit criteria for installation preparation

Before sealing installation, resolve exact package selection and provenance,
plugin names/versions/privileges, profile selection in inventory, restricted first
startup, node/master access, storage and failure alerts, polling cadence,
observation duration and rollback. Keep unresolved decisions visible in the NTP
readiness register under OBS-02/OBS-07. Node and master changes are separate stages.

The read-only node/master inspection reviews collect prerequisites only. They do
not execute plugins, poll nodes, send alerts or deploy this proposal.

## Reference documentation

- [Munin node configuration](https://github.com/munin-monitoring/munin/blob/master/doc/reference/munin-node.rst)
- [Master configuration](https://github.com/munin-monitoring/munin/blob/master/doc/reference/munin.conf.rst)
- [Plugin protocol and units](https://github.com/munin-monitoring/munin/blob/master/doc/reference/plugin.rst)
- [Limits and contacts](https://github.com/munin-monitoring/munin/blob/master/doc/reference/munin-limits.rst)

These references inform review; installed package files and actual deployment
configuration remain the authority for acceptance.
