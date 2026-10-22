# Munin fleet component

This directory owns Munin configuration for the fleet. Application repositories
may specify desired measurements and host requirements, but must not keep a
second deployable copy of a Munin plugin, plugin setting, or master entry.

## Layout and selection

- `node/plugins/<app>/`: custom plugin source. Source is not enabled by its
  presence in this directory.
- `node/plugin-conf.d/`: plugin user, group, and environment settings.
- `node/profiles/`: explicit plugin selections and their settings. A profile is
  a definition, not a host assignment.
- `master/`: master-side registration and accepted native configuration;
  acceptance remains specific to the reviewed hosts and operations.
- `tests/`: repository-only checks for profile completeness and plugin output.

Host inventory selects a profile explicitly; this component defines what that
profile installs. Do not infer selection from a hostname or copy every plugin
onto every node. The Caddy profile is a deferred candidate. There is no
accepted base profile. The j2-svntp1 runtime and bounded expanded master
collection are accepted; delivery remains open. Inventory now selects `ntp`
for `j2-svntp1`; that desired assignment does not deploy it. The
[NTP candidate](node/profiles/ntp/README.md) now has an explicit metric/privilege
selection and locally qualified installer payload. No hosts are selected here.

When a deployment workflow is approved, it should install custom plugin source
as executable files under `/usr/local/munin/lib/plugins`, link only the selected
names into `/etc/munin/plugins`, install the selected settings into
`/etc/munin/plugin-conf.d`, and register approved nodes in the master's
`/etc/munin/munin.conf`. Package-provided plugins remain package-owned. Record
exact host/profile selection and installed-file readback in inventory and
operation evidence; do not treat this candidate layout as an installer.

Before activating a profile, review `munin-node-configure --suggest`, test each
selected plugin with `munin-run <name> config` and `munin-run <name>`, confirm
the node's master allowlist and TCP 4949 reachability, then confirm the approved
master polls the node. Verify privilege and file access for each plugin. Caddy
specifically needs an on-host metrics endpoint and certificate read access;
these have not been live-validated for Munin. Install and rollback one node at a
time, with master registration only after node validation.

The [NTP dependency/profile review](docs/ntp-monitoring-review.md) carries the
OBS-02/OBS-07 prerequisites. The candidate selection and installer controls have
local qualification and an inventory assignment; the approved node bundle, master setup,
job-success producers and target polling/alerts remain separate gates.

The operator requires j2-svntp1 to match every applicable generic system statistic
from j2-svpi4mf alongside its NTP readers. The
[expanded-profile requirements](docs/ntp-generic-statistics.md) cover reference
comparison, target capability mapping and coordinated expected-set deployment.
The expanded selection is now deployed through the approved coordinated stages;
the later expanded observation accepted scheduled collection and all selected
dual-stack graph families; producer and alert gates remain separate.
The [coordinated expansion draft](docs/ntp-generic-deployment.md) defines the
isolated native qualification and ordered master/node/restoration stages.
Native v2 qualification now passes all 33 proposed instances, including both NFS
readers; concurrent full workloads took at most 15.50 seconds within 25 seconds.
Expanded settings and exact-set transport candidates are prepared. Guarded update
and recovery pass nine native cases. All three approved v2 stages committed and
reconciled the canonical mirrors. The node now selects 29 generic plugins plus
four NTP readers; final master transport requires all 33. Both source-bound warm
protocol families and existing HTTPS passed. The subsequent observation accepted
three expanded scheduled cycles, 280 fresh RRDs and all 120 verified HTTPS checks.
Independent producer, canonical source-attribution and alert gates remain open.

The [expanded observations](docs/ntp-expanded-observation.md) executed and accepted
all selected graph families and three genuine post-expansion cycles. Both
maintenance records remain absent; alerts stay disabled.

Run `bash Munin/tests/validate-scaffold.sh` for local repository validation.

Separate reviews cover [node installation](docs/ntp-node-installation-review.md)
and [master/dashboard acceptance](docs/ntp-master-acceptance-review.md).
The network/DNS owners accepted static master IPv4/ULA and both names October 21.
Sampled native Apache HTTPS also passed both literals. Node listeners and
independent TCP, expanded scheduled collection and fresh graphs are accepted;
canonical TCP source attribution and delivered alerts remain separate gates.
The [reconciled handoff](docs/ntp-monitoring-review.md#separate-stage-handoff) names
the sealed node/producer stages and [resolved master design](master/ntp-design.md).
Native master parser/activation/recovery qualification and commissioning are
accepted. Genuine producer records, native limits/transitions and downstream
delivery remain open.

The approved producer installation passed October 21. Following initial node
containment, the separately approved classifier correction/start passed at
13:04:08 CDT: all nine plugin paths, literal listeners, independent IPv4/IPv6 TCP
and NTP continuity. Munin-node is enabled/running; consumed stages cannot replay.
Later commissioning and expanded observations accepted master activation,
scheduled collection and fresh graphs. Genuine producer records, canonical
source attribution and delivered alerts remain open.
