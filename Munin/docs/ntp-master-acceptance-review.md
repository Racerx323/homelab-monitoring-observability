# Munin master and dual-stack acceptance review

Reconciled October 21, 2026. Master networking, DNS and sampled Apache transport
are accepted. Producer hooks are installed; genuine maintenance records remain
unaccepted. The separate [classifier correction/start](ntp-node-installation-review.md)
passed node runtime acceptance at 13:04:08 CDT, including all nine plugin paths
and independent IPv4/IPv6 TCP. Guarded master commissioning committed at
15:34:46 CDT. The [outcome](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-master-commissioning-20261021-v1/outcome.md)
records successful CLI/native transport values, independent dual-family HTTPS,
commit, disarmed recovery timer and exact repository reconciliation. Receipt
consumed; no replay. Contacts remain none. The [master observation](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-master-observation-20261021-v1/outcome.md)
completed October 21 at 16:00 CDT: three scheduled cycles at 15:45/15:50/15:55,
current RRD updates and all 40 dual-family HTTPS checks passed. Both maintenance
records remain absent; evidence=0, job ages and master mail unknown. No contacts
were activated. Actual canonical source attribution, maintenance completion,
limits/transitions, delivered alerts, client refresh/coverage and persistence
remain open. Both observation receipts are consumed; do not replay them. The
[observation procedure](ntp-observation.md) separates capture, sampled collection
and serving acceptance from overall readiness.
Target native master: `pi@10.1.3.83`, established
host-key alias `svmf.local.theama.co`, configuration `/etc/munin/munin.conf`.

## Accepted addresses and serving baseline

The [accepted prerequisites](ntp-monitoring-review.md#accepted-prerequisites--october-21-2026)
record static `10.1.3.83` and `fd36:5aa8:6971:1::83`, actual NTP route sources,
both names' A/AAAA and canonical IPv4/IPv6 PTR to svmf. Preserve RA global/default
routing and the existing generated ULA for other consumers; use only .83/::83
for new node allowlists/polling. No replay of network or DNS deployment is needed.
Physical reboot/renewal persistence and external client refresh remain open.

Munin is served by native Apache, with the repository-owned
[vhost](../../Apache2/configs/001-munin.theama.co-ssl.conf) and accepted
[IPv6 ACL deployment](../../Apache2/docs/acl-deployment.md). Verified HTTPS on
443 for `munin.local.theama.co` passed through both intended literals after
static-network commit: `/`, `/static/style-new.css` and the sampled
`/munin-cgi/munin-cgi-graph/J1-SVMF/J1-SVMF/apache_accesses-day.png`.
DNS-node Caddy serves the separate linked proxy VIPs; it is not this dashboard's
web server. Current Apache needs a drift/readiness check, not rediscovery or a
new serving/binding change by default. Preserve its private ACL and verified TLS;
no HTTP downgrade, insecure verification or family fallback. The existing sample
proves transport, not freshness or a future j2 graph.

## Resolved polling and contact design

The [master design](../master/ntp-design.md) selects one canonical raw-metric
series over literal IPv4 and the unprivileged master-local `ntp_transport_j2`
plugin. During the existing five-minute cycle it fully configures/fetches all nine
plugins over both literals with explicit .83/::83 source binds. Its independent
health fields accept `U` as valid transport; canonical limits report data health.
No second scheduler or duplicate j2 series. Installation and immediate protocol
checks are accepted; native scheduled collection remains open.

Prove actual native canonical source .83 and both plugin source binds at live
acceptance. Neither dashboard access, a route lookup nor two manual probes
establishes scheduled collection. Preserve the existing master node series.

The fixed contact uses validated stdin, `max_messages 1` and loopback Mailrise
127.0.0.1:8025. Problems/unknowns and recoveries use the agreed routes. Private
atomic status and stderr expose submission failure; this is not delivery proof
or an independent monitor of a stopped master. The design defines profile limits,
`unknown_limit 0`, transition-only sends, private state and conditional recovery.
Validate these with the installed 2.0.73-1 parser/limits before activation; upstream
2.0.73 source supports the design but does not prove Debian byte equality.

## Fresh preflight and mutation boundary

The [approved native-master v2 readiness capture](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-native-master-readiness-20261021-v2/outcome.md)
completed October 21 at 10:51:32 CDT with exact host/boot/NetworkManager continuity.
It retains package/configuration/scheduler/source-documentation and Apache/data
metadata, correct static route sources and unchanged accepted vhost hash. No j2
entry or active contacts appear in inspected config. Five-minute cron and bounded
recent update/limits activity are observed, not polling/delivery acceptance.
No client DNS, CGI/HTTPS, protocol fetch, plugin/limits run or message occurred.
Recheck the captured hashes/identities during the future approved mutation;
unknown custom paths, client refresh and fresh j2 data remain explicit scope gaps.

The inventory-backed NTP node stage must pass first. Integrate the independent
[NTP producer stage](../../../homelab-ntp/ntpsec/docs/monitoring-job-success-review.md)
and genuine scheduled retention/reporting completions before final maintenance
health acceptance. Missing records remain explicit faults; never fabricate,
backdate or suppress them to obtain a green dashboard. Producer preparation and
node preparation may proceed independently.

Prepare only the j2 registration, qualified polling design and reviewed
limits/contacts. Preserve unrelated entries, native five-minute cadence, Apache
applications and Mailrise/Apprise containers. Include a serving change only if
fresh evidence establishes one is required, with exact bytes and rollback in
scope. Do not change host networking, DNS, Caddy or Keepalived here.

Master owns limit evaluation/delivery; Aaron is operator. Problem route is
`notify.failure@mailrise.xyz`; recovery/status route is `notify@mailrise.xyz`.
No secret destination URLs belong in the bundle. Define field units, the existing
10 GiB/5 percent available-inode floors, time-health limits, stale/unknown
behavior, delivery failure visibility and recovery semantics before activation.
The selected profile is the candidate source; local plugin limits alone do not
accept the complete alert chain.

## Acceptance, delivery and recovery

Require parser/configuration checks, real master-origin config/fetch with actual
source proof over both families, scheduled collection evidence for the qualified
family design, fresh stored metrics and usable j2 graph output through both
hostname-forced HTTPS families. The design proposes three consecutive native
five-minute cycles for commissioning; approve the interval/reset rules in the
later sealed review. The longer final observation interval remains unselected. Prove actual limits evaluation and handling of
unknown/stale data, node/collection failure, storage floors and job-record faults.
Retain existing qualification; do not build more HA fixtures or simulate DNS
failover. Any bounded alert exercise must preserve NTP, logs and real success
records and have its precise effects included in the approved stage.

Preview exact problem/recovery recipients, subjects, bodies and downstream
effects before approval for one send each. No message previews or delivery tests
are approved here. SMTP acceptance is not downstream receipt; obtain operator
delivery confirmation. Quiet successful needrestart and a recorded successful
job do not themselves prove delivery.

Bind master before/after bytes, helpers, dependencies, exact sequence, private
backups, acceptance and rollback in a later exact-hash bundle. Restore only
matching authored registration/limits/contact or necessary serving changes;
validate and use the installed supported activation path. Prove baseline
Apache, scheduler and unrelated-node health after recovery. Preserve foreign
drift; uncertain outcome requires inspection and a separately reviewed
continuation. Do not roll back accepted networking/DNS from this stage.

## Commissioning provenance and remaining acceptance

The canonical baseline is [master/configs/munin.conf](../master/configs/munin.conf).
The [exact production baseline outcome](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-master-baseline-20261021-v1/outcome.md)
completed at 14:15:51 CDT. Continuity passed and all five in-memory streams parsed
successfully as munin. The guarded importer privately scanned and atomically
imported the exact production bytes, then verified their hash. Production and
repository now match, including comments, whitespace and graph identities. The
receipt is consumed. The configuration lifecycle requires synchronized accepted
readback after every later deployment/restoration.

Native UpdateWorker falls back when the configured socket is unavailable;
GraphOld/CGI set the cache address without that check. With the captured missing
socket/service, commissioning removed only the stale cache directive and uses
native direct-RRD defaults. The installed parser and CGI continuity passed;
keep the synchronized accepted successor as the current baseline.
Installed include semantics are known; effective contact inheritance, limits
transitions and graph concurrency remain unaccepted. munin-node cannot reload;
CGI loads configuration before its persistent loop. The qualified
[workflow](ntp-master-deployment.md) restarts only Munin-node and refreshes verified
native CGI descendants using pidfd TERM; Apache identity remains unchanged. Commission new contacts as none. No service action, update,
limits/plugin execution, RRD write or message occurred during the retrieval.

Network/DNS and sampled Apache transport prerequisites are closed within their
accepted scope. The [read-only master readiness capture](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-native-master-readiness-20261021-v2/outcome.md)
has completed; its receipt is consumed. The polling/limit/contact/recovery design
is defined in the linked document and candidates. Native in-memory parsing and exact production mirroring now pass. The direct-RRD
cache candidate and exact merge/recovery passed isolated native qualification.
The committed commissioning stage keeps contacts none; required live transport
values and independent HTTPS passed before commit. Scheduled observation and separately
previewed message effects require later approval.
Node installation and genuine producer acceptance remain prerequisites to final
health. Scheduled collection, fresh dual-family dashboard and approved delivered
alerts still need their own evidence. Keep OBS-02/OBS-07 and remaining
client/persistence obligations visible; no new inspection replay or deployment
is authorized by this captured result.
