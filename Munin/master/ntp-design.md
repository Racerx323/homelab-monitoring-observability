# j2 polling and alert design

Prepared October 21, 2026 for native Munin 2.0.73-1 on svmf. This resolves the
polling/contact design; it does not activate it. The
[master acceptance review](../docs/ntp-master-acceptance-review.md) owns the live
mutation and acceptance gate. Node/producer prerequisites remain separate.

## Collection and identity

Register `[j2-svntp1]` once at literal `10.1.0.51:4949`, with `use_node_name yes`.
This is the canonical raw-data series. Preserve the native five-minute
munin-cron schedule. Require its actual IPv4 source to be `10.1.3.83` at live
acceptance; the accepted route lookup alone is insufficient.

Install [ntp_transport_j2](plugins/ntp_transport_j2) on the master's existing
Munin node, under its existing `J1-SVMF` series. It binds explicit sources and
collects complete protocol/configuration/value responses from all nine selected
plugins over each literal family every scheduled fetch:

| Family | Source | Target |
| --- | --- | --- |
| IPv4 | `10.1.3.83` | `10.1.0.51:4949` |
| IPv6 | `fd36:5aa8:6971:1::83` | `[fd36:5aa8:6971:1::51]:4949` |

The plugin checks the fixed greeting, multigraph capability, exact plugin set,
complete frames and every configured noncomputed field. Numeric values and `U`
are valid transport data; canonical metric limits separately own data health.
Each family has an independent 25-second total budget and a connection timeout
of three seconds. Both run concurrently, unprivileged. Refusal, timeout, changed
identity, missing fields or malformed responses set only that family's state to
zero. No DNS resolution, family fallback, duplicate j2 series or second scheduler.
Keep native plugin execution limits above this bounded total; verify installed
limits and actual runtime in master preflight before activation.

The accepted NTP profile retains cpu/load/memory/uptime/processes and the four
custom readers. Only `ntp_statistics` and `ntp_jobs` run as root on j2; the new
master plugin runs as munin:munin. It reads no raw NTP statistics, mail credentials
or root-only success records. The j2 reader exposes derived job evidence/age.

## Limits, unknown data and ownership

The master evaluates the selected profile's limits and owns notification. Aaron
is the operator. Preserve these explicit health meanings:

| Metric | Critical condition |
| --- | --- |
| Query, synchronization, PPS selection, collection status | State differs from 1 |
| Selected reach / stratum / leap | Outside 1–255 / 1–15 / 0–2 respectively |
| Selected offset / jitter | Outside ±0.005 seconds / above 0.001 seconds |
| Available filesystem bytes / inodes | Below 10 GiB / below 5 percent |
| Active loopstats/peerstats/clockstats freshness | Older than 3600 seconds |
| Protostats | Collection must work; quiet event log has no periodic age limit |
| Genuine retention/reporting evidence / age | Missing or invalid / older than 172800 seconds |
| Transport IPv4 / IPv6 | Full protocol check differs from 1 |
| Last alert submission | Last recorded SMTP attempt failed; absent/invalid status is unknown |

Statistics size and positive net growth are observational metrics, not an
invented storage cap. Existing storage floors apply; sustained growth/storage
budget acceptance remains OBS-02. Counter resets may make a DERIVE sample unknown.
Do not suppress that state or infer a job ran from a global timer timestamp.

Candidate `unknown_limit 0` removes the stock unknown-data grace and exposes
missing samples at the next limits evaluation. No `always_send`: send state
transitions and recoveries, not a message every healthy cycle. Validate inheritance
and transitions with the installed 2.0.73-1 parser/limits before activating
contacts. An unknown value is neither zero nor evidence of healthy data; cached
graphs must not conceal stale collection. An entire stopped master cannot report
its own outage: the operator must check scheduler/log/graph freshness through the
existing operational checks. This design adds no independent watchdog.

## Contact and delivery failure

The [candidate contact](configs/j2-svntp1.conf.example) invokes a fixed command
with no shell-expanded alert values. Six bounded ASCII fields go through stdin:
severity, host, graph, warning fields, critical fields and unknown fields. The
[helper](../scripts/ntp_mailrise.py) validates the fixed hosts/graph set and rejects
headers, extra separators and arbitrary arguments. `max_messages 1` is required:
Munin otherwise reuses its contact pipe and could concatenate messages before EOF.

| State | Recipient |
| --- | --- |
| WARNING, CRITICAL, UNKNOWN | `notify.failure@mailrise.xyz` |
| OK recovery | `notify@mailrise.xyz` |

Sender is `munin@local.theama.co`; subject is `Munin STATE: HOST/GRAPH`.
The body identifies state, host, graph, affected field names and operator.
Submit directly to the observed Mailrise endpoint `127.0.0.1:8025`, timeout ten
seconds, once. No host sendmail, secret URL lookup, retry or spool is introduced.
SMTP acceptance proves submission only. Preview exact problem/recovery messages
and obtain one-send approval for each; retain operator confirmation of downstream
receipt. This preparation sends nothing.

Provision `/var/lib/munin/ntp-alerts` as munin:munin 0700. The helper atomically
writes/fsyncs `status.json` as 0600 after an actual attempt; never preseed success.
Failure exits nonzero and writes stderr plus false submission state. The transport
plugin exposes the last attempt as `mail`; subsequent successful attempts replace
that state. It is not a delivery receipt or a heartbeat. A broken Mailrise cannot
reliably deliver its own failure alert: operator review of the private status,
limits logs and master graph remains the independent diagnostic path. A status
write failure is nonzero/stderr and must also be checked during acceptance.

## Activation, observation and recovery

Munin is a repository-managed service. Its canonical
[master baseline](configs/munin.conf) must match accepted production bytes;
the [configuration lifecycle](configuration-lifecycle.md) owns exact import,
drift rejection, separate candidates and reconciliation after deployment or
restoration. Preserve production graph identities. Do not overwrite accepted
production from an unreconciled repository copy.

Keep the accepted Apache configuration, network and DNS unchanged. The master
operation must pin current config/node settings and source/privilege paths,
merge a single j2 entry and the existing master-section overrides, install the
transport plugin/settings/link and private state, then validate the installed parser.
Install the contact helper only in a separately approved alert stage.
Do not paste the example as a replacement or create a duplicate master section.
Restart only Munin-node. Refresh persistent native HTML/graph CGI descendants
through pidfd TERM after checking exact script, UID, start identity and accepted
Apache ancestry; prove their exit without restarting/reloading Apache. The
[guarded workflow](../docs/ntp-master-deployment.md) qualifies activation and
conditional restoration using native services. Native master collection reads
its config on scheduled runs.

Start with contacts inactive. Prove both master-origin protocol paths, all nine
plugins' installed privileges and bounded runtime, then native scheduled canonical
data and both transport fields. Require fresh timestamps and usable j2 PNGs,
HTML and CSS through verified hostname-forced HTTPS over both families. Propose
three consecutive five-minute scheduled cycles for this bounded commissioning
gate; the later master review must explicitly approve the interval/reset rules.
This bounded commissioning gate does not replace OBS-09's longer final interval.

Accept each genuine scheduled retention/reporting record independently before
closing maintenance health; expected absence remains faulted. Contact activation
also requires exact-message approval and bounded effects for problem/recovery
exercises. Real logs, clocks, success records and NTP service remain untouched by
alert tests. Prove unknown/stale/family-loss visibility in the approved native
acceptance sequence; no further HA fixtures or synthetic production heartbeats.

Private backups and exact before/after hashes must cover only authored master
config, local plugin link/settings/helper and contact helper. On failed acceptance,
deactivate authored contacts first, restore only matching authored bytes/links,
validate and apply the qualified native activation path. Preserve foreign drift,
real status/records, RRDs and historical graph data. Prove unrelated hosts, Apache
and the five-minute scheduler remain healthy. Node containment and producer
restoration belong to their separate bundles. Unknown outcome holds for inspected,
separately reviewed recovery; it never permits a replay or rollback of accepted
networking/DNS.

## Evidence and local validation

The unchanged production node installer/profile retain their earlier actual
first-start/recovery qualification. New focused checks use the real reporter,
cleanup and atomic writer with isolated files/captured mail, protocol transcripts
and SMTP capture objects; they make no host connection or message submission.
Run `python3 -I -B Munin/tests/test_ntp_master.py` or the scaffold validation.
Local checks do not execute native master limits or establish live acceptance.

Version-specific upstream sources establish the design, not Debian byte equality:
[single-address INET6 client](https://github.com/munin-monitoring/munin/blob/2.0.73/master/lib/Munin/Master/Node.pm),
[unknown grace, contact expansion, transitions and pipe lifecycle](https://github.com/munin-monitoring/munin/blob/2.0.73/master/lib/Munin/Master/LimitsOld.pm),
and [configuration reference](https://github.com/munin-monitoring/munin/blob/2.0.73/doc/reference/munin.conf.rst).
The retained 2.0.73-1 readiness capture and later installed parser validation
remain authoritative for production. The public sources do not prove both-family
scheduled collection or message delivery on svmf.
