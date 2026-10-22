# NTP node profile

[profile.json](profile.json) selects 29 package plugins and four custom NTP
readers. Inventory selects this profile for j2-svntp1. The approved coordinated
v2 deployment committed and reconciled this profile and its settings mirror;
full source-bound IPv4/IPv6 config/fetch passed after the 305-second warm-up.
Only ntp_statistics/jobs retain root; all generic readers run as munin:munin.

The [generic comparison](../../../docs/ntp-generic-comparison.md) and
[expansion requirements](../../../docs/ntp-generic-statistics.md) define parity
with j2-svpi4mf. All 29 generic instances, including both proven NFS readers,
are selected alongside the four existing NTP readers. The separately retained
[generic-parity candidate](generic-parity.candidate.json) records the reviewed
selection; the canonical profile above is the accepted deployed mirror.

All three [deployment stages](../../../docs/ntp-generic-deployment.md#sealed-execution-order)
are accepted, committed and reconciled; their consumed receipts cannot replay.
Compatibility v1 stopped before publication on its two-link baseline. Corrected
v2 verified and preserved the historical commissioning proof. The original
[installation review](../../../docs/ntp-node-installation-review.md) remains
historical provenance. Three expanded scheduled cycles, fresh RRDs and all
selected dual-stack graphs are now accepted. Actual maintenance records,
canonical source attribution and alerts remain separate open gates.

| Selection | Execution identity | Inputs and behavior |
| --- | --- | --- |
| cpu, load, memory, uptime, processes | munin:munin | Exact reviewed munin-plugins-core 2.0.76-5 sources; ordinary local counters |
| ntp_health | munin:munin | Fixed `/usr/local/bin/ntpq`, numeric queries to 127.0.0.1, eight-second timeout; leap/stratum/selection/reach and system/selected-peer offset/jitter |
| ntp_storage | munin:munin | statvfs of root and statistics paths; available bytes and available inode percentage |
| ntp_statistics | root:root | Bounded metadata scan of the fixed statistics directory; no raw statistics reads or writes |
| ntp_jobs | root:root | Two fixed root-private success records; no scan, report, cleanup, SMTP or notification is executed |

The root readers accept only config/fetch arguments. Their paths cannot be
selected through plugin arguments or environment variables. The shared Python
module and entry points must be root-owned and unwritable by the plugin users.
No broad directory ACL, ownership change, setuid helper or sudo grant is needed.
Root is used only for directory metadata and private success-record access;
the source-built NTP tools and ordinary system plugins remain unprivileged.

## Fields and limits

Available-byte critical limits preserve the approved 10 GiB floor. Available
inodes use f_favail/f_files and the approved 5 percent floor, rather than total
free blocks/inodes reserved for root. Root and statistics may share a filesystem;
their gauges are separate views, not capacities to add together.

Selected-source critical timing limits are signed offset within 5 ms and jitter
within 1 ms, matching the NTP plan. Missing queries, unsynchronized state, lost
PPS selection and zero reach have explicit fault fields. Values from ntpq are
converted from milliseconds to seconds; the plugin does not claim absolute UTC
accuracy. Live source-built-tool parsing and local query permission still need
target acceptance.

Statistics storage deduplicates hardlinked inodes. Positive net growth is a
DERIVE field with minimum zero: deletion/rollover decreases are omitted rather
than graphed as negative generation. It is not a representative daily-growth
budget; retain the plan's separate 31-day-plus-headroom measurement requirement.
Newest-mtime age has a candidate one-hour critical limit for loopstats,
peerstats and clockstats. Event-driven protostats age has no quiet-time limit.
Missing/invalid data is unknown or an explicit collection fault, never zero age.
Confirm these freshness limits in the installation review against actual cadence.

The master must evaluate missing/unknown data and prove problem/recovery delivery;
plugin limits alone do not close the alert chain. Polling cadence is five minutes.
No final host observation duration is invented by this profile.

## Maintenance success records

The selected reader expects these fixed records:

- `/var/lib/ntpstats-retention/last-success.json`, job `retention`.
- `/var/lib/needrestart-reporting/last-success.json`, job `reporting`.

Each is a root-owned regular file, mode 0600, at most 4096 bytes, beneath
non-symlink directories. Schema 1 contains job, status `success` and a finite
completed_epoch. It must be atomically written only after the actual job succeeds.
The candidate staleness ceiling is 48 hours. Missing, malformed or inaccessible
records produce evidence=0 and age=U; future-dated records are rejected.

**The installed jobs do not yet produce these records.** A separate NTP-owned
maintenance/reporting stage must add post-success recording while preserving
locking, quiet scans and failure-mail behavior. Do not fabricate records, infer
rule execution from global logrotate success, or infer a needrestart run from
mail delivery. Keep this dependency in OBS-01/OBS-03/OBS-07 until accepted.
This profile exposes the existing evidence gap instead of reporting it healthy.

## Qualification and installation

Offline tests cover malformed/missing time data, units, available-space counters,
metadata-only scans, hardlink deduplication, rollover, future timestamps,
unknown/event-driven data, private heartbeat handling and the privilege selection.
The actual installer and selected plugins are also exercised in isolated
systemd containers; see [qualification](../../../docs/ntp-package-qualification.md).

The installer [source](../../../scripts/install_ntp_node.py) guards package
autoconfiguration and first start, installs only this selection, validates
source/settings/link readback before activation, and requires literal listeners.
Its production spec requires exact host/boot, running time-service identity,
protected-file and package-inventory hashes, all 15 pinned archives, profile
artifacts and an explicit pre-existing-policy hash or verified absence.
Only the isolated fixture may use amd64 and the three Architecture-all packages.

Do not invoke the source directly on production. A later operation must bind
this executable, spec, package bytes, profile, host assignment and every helper
into an approved bundle. Node installation and master registration remain
separate stages. The CLI's spec digest is not itself user authorization.

Recovery removes an authored permit, stops/disables the node and restores only
the matching authored policy wrapper. It leaves packages and the guard installed;
it never purges packages, restarts NTP or rewrites its configuration. Foreign
policy/guard changes hold recovery; foreign configuration is preserved while
the service is contained. Held CLI recovery exits nonzero. Durable root-private
state supports a newly approved recovery command after interruption; expose only
sanitized outcomes, not its stored policy backup. Inspect before continuation.

The PPS-selection classifier recognizes the accepted selected local SHM unit 2
(`SHM(2)` or numeric `127.127.28.2`, refid `.PPS.`, peer stratum 0 and type `l`)
under normal selected tally, as well as native `o` PPS-driver peers. A network
refid of PPS, wrong SHM unit or different refid is insufficient. This corrects
the observed false negative from requiring `o` for GPSD SHM. The correction/start
review is separate; updating source does not restart or accept a node.
