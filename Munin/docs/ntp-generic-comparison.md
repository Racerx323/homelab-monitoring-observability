# j2-svntp1 generic statistics comparison

The approved read-only inventories completed October 21, 2026 at 16:30 CDT.
Both captures passed with unchanged continuity; all four verified HTTPS index
requests passed. Their one-use receipts are consumed. No plugin, autoconfiguration,
sensor/device command, service change or install was executed. The reference
node itself was not contacted; this comparison uses its current master pages
and retained native RRD metadata.

## Observed selection

Both address families expose the same 33 generic top-level reference graphs,
matching the native reference RRD inventory. j2-svntp1 currently enables five
generic plugins and the four custom NTP readers. Its 16 top-level graphs comprise
five generic and eleven NTP multigraphs. Generic parity maps to **29 package
plugin instances: 24 additions**, retaining the four NTP readers. The resulting
candidate has 33 plugin instances before any explicit capability dispositions.

The complete, machine-readable
[candidate selection](../node/profiles/ntp/generic-parity.candidate.json) is
retained as review provenance. The canonical profile and settings now mirror
the accepted expanded deployment.
All needed package template names are present among the target's 182 installed
core plugin names; munin-node and munin-plugins-core are both 2.0.76-5. Presence
and version alone do not qualify unused source bytes or runtime dependencies.

| Measurements | Proposed package plugin instances | Target qualification |
| --- | --- | --- |
| Existing CPU/load/memory/process count/uptime | cpu, load, memory, processes, uptime | Preserve current accepted fields and identity |
| Temperature and CPU frequency | acpi, cpuspeed | thermal_zone0 exists; verify actual readable thermal/cpufreq counters |
| Filesystem usage and inodes | df, df_inode | Native mount discovery and access; preserve NTP-specific available-space views |
| Disk I/O, latency, throughput and utilization | diskstats | One multigraph plugin supplies four overview graphs and device children; qualify state and actual device discovery |
| Interface traffic and errors | if_eth0, if_wlan0, if_err_eth0, if_err_wlan0 | Both interface names exist; monitoring must not enable Wi-Fi or alter link policy |
| Network counters and TCP connections | fw_packets, netstat | netstat supplies both netstat graphs; verify net-tools and effective read permissions |
| Entropy, forks, interrupts and IRQs | entropy, forks, interrupts, irqstats | Counter availability and per-plugin runtime/access |
| Open files/inodes, priorities and threads | open_files, open_inodes, proc_pri, threads | Native counters/process visibility and bounded runtime |
| Swap, logged-in users and VM state | swap, users, vmstat | Verify native counters, who and vmstat; zero activity is valid |
| NFS client statistics | nfs_client, nfs4_client | Conditional on actual /proc/net/rpc/nfs proc3/proc4 capability; currently unknown, not silently excluded |
| NTP source/timing, storage, statistics and jobs | ntp_health, ntp_storage, ntp_statistics, ntp_jobs | Retain all four current custom readers and their graph identities |

## Device and source findings

The target exposes eth0/wlan0, mmcblk0 with partitions, zram0, loop devices,
thermal_zone0 and three hwmon entries. These are capability names, not proof
that every sensor is readable or supported. Do not copy reference sda names;
use actual target diskstats discovery and explicitly review device selection.
Some reference overview/device series are historical and stale.

The 33 initially unmatched RRD filenames resolve to diskstats device-child
series under its four graph families. They were retained as gaps by the capture,
then mapped offline using the exact package source; none was silently discarded.
They are field series, not 33 additional required plugin instances.

The approved cached munin-plugins-core package was hash-verified and inspected
as data only. The diskstats plugin uses Munin plugin-state storage and saves
state during collection; its live qualification cannot be described as a pure
read-only counter probe. It supports unprivileged counters; root is optional for
device-mapper naming. The `if_` plugin can need extra privilege/tools for link-speed
discovery. fw_packets documents root but actually reads IP counters from
/proc/net/snmp; it does not query or modify firewall rules. Resolve effective
access before granting privilege. NFS plugins require the respective proc3/proc4
lines. netstat emits both observed TCP graph families and depends on its command.
These are source findings, not live execution acceptance.

## Next stage and unchanged gates

Native qualification v2 completed successfully October 21, 2026: all 33 plugin
instances ran with unchanged NTP/Munin identities, protected bytes and production
selection. Both NFS proc3/proc4 counter sets are present; no plugin omission is
needed. Individual config/fetch took 13.14 seconds; three concurrent complete
workloads after a genuine 305-second wait took 15.50, 15.33 and 15.33 seconds,
within the existing 25-second budget. Every generic warm field was numeric.
Only the two previously pending NTP maintenance-job ages remained unknown.

Native diskstats state and readback passed as munin, mode 0600, with 51 numeric
fields for loop0/mmcblk0/zram0 and their four overview families. Temperature,
four CPU-frequency counters, interfaces and both NFS readers worked without new
root privileges. Ethernet speed metadata was readable; Wi-Fi speed metadata was
unavailable, while its traffic/error counters were valid zero values. Retain
that optional metadata limitation without escalating privilege or changing radio
policy. Keep the two established NTP root readers only.

The candidate now carries this native qualification and exact selection.
[Expanded settings](../node/plugin-conf.d/ntp-expanded.candidate.conf),
[compatible transport](../master/plugins/ntp_transport_j2.compatible.candidate),
[final expanded transport](../master/plugins/ntp_transport_j2.expanded.candidate)
and [artifact manifest](../node/profiles/ntp/generic-expansion.candidate-manifest.json)
are prepared separately from accepted production sources. Offline checks accept
the exact old/expanded sets, reject partial/superset selections and preserve raw
self-referencing CDEF fields. Both candidates also parsed every captured native
warm config/fetch frame offline. The subsequent approved v2 stages deployed the reviewed selection.

Guarded update/recovery now passes nine native cases; the three corrected ordered
[deployment reviews](ntp-generic-deployment.md#sealed-execution-order) executed
successfully and are accepted/committed/reconciled. They include genuine per-source diskstats warm-up
before commit. Native plugin qualification bypassed systemd-property
simulation; production runtime and direct source-bound IPv4/IPv6 polling passed
the guarded deployment. Scheduled expanded collection and RRD/graph freshness
were later accepted by the dedicated
[expanded observations](ntp-expanded-observation.md). Canonical source attribution
and producer/alert gates remain open.

### Retained v1 diagnosis

The approved native qualification v1 stopped before staging when its protected
reader rejected the normal /proc/net alias. All 71 pinned source/configuration
files, dependency-command files and native module loads passed; services and
production selection remained unchanged. No plugin config/fetch or state was
created. NFS capability was then unknown. Corrected v2 used the current worker
PID's concrete procfs path, retaining symlink rejection; its separate approved
execution passed. See the NTP readiness checkpoint for the current deployment.

The [coordinated deployment procedure](ntp-generic-deployment.md) defines native
qualification, exact old/expanded transport compatibility, node continuation,
restoration baselines and scheduled acceptance. Native state qualification is
accepted; all three v2 production stages are now committed/reconciled.

V2 supersedes that interrupted qualification; both receipts are consumed and
cannot replay. Native concurrent workloads accept the scoped state/runtime
findings, and actual source-bound IPv4/IPv6 deployment fetches passed. Canonical scheduled
collector source attribution remains a separate gate. Preserve generic munin identities and the two established
NTP root readers. No NFS or hardware activation is required for this selection.

All three guarded v2 stages executed in order. The accepted profile now selects
29 generic plugins plus four NTP readers, and final transport requires all 33.
Warm full-protocol passes took 7.92/8.06 seconds within 25 seconds per family.
Every receipt is consumed; do not replay an installer or mutate links alone.
The later expanded observation accepted scheduled collection and all selected
graphs over both dashboard families, preserving the canonical host and RRD history.

The expanded profile is deployed. Maintenance completion, actual canonical source
attribution, limits/delivery, client coverage, sustained growth, persistence and
later mandatory separate-host ntpviz remain independent open requirements.
