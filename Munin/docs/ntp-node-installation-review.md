# j2-svntp1 Munin node installation review

Reconciled October 21, 2026. The approved
[correction/start outcome](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-node-correction-start-20261021-v1/outcome.md)
passed at 13:04:08 CDT: all nine installed plugin config/fetch paths before/after
startup, exact literal listeners, independent IPv4/IPv6 TCP and NTP continuity.
Munin-node is enabled/running. Only the classifier changed; no packages, jobs,
master activation or messages. Missing genuine records remain explicit faults.
Node runtime acceptance does not establish master polling, graphs or delivery.

The initial v3 installation failed on a classifier false negative and was
contained. The read-only selection inspection confirmed stable selected
SHM(2)/PPS matching the accepted configuration. Original apply/inspect and
correction/start receipts are consumed. Preserve their immutable archives,
original state, separate resume state, backups and guard; do not replay them.
Inventory selects `ntp` with `node_runtime_accepted`; master acceptance and real
scheduled producer completions remain separate. Next qualify native master
merge/parser/activation and restoration before sealing its execution review.

The sections below retain the original installation contract; the executed
continuation replaced only the classifier and conditionally restored only its
authored change on failure, as defined in its frozen review.

## Inputs and preflight

Use the locally qualified [actual installer](../scripts/install_ntp_node.py)
and [profile](../node/profiles/ntp/README.md). A production outer bundle must pin
the executable, complete closed profile artifact set, explicit inventory selection,
all 15 verified package archives, transport/helpers, spec and recovery commands.
The CLI spec digest alone is not authorization. Do not invoke it directly from
this document or execute an amd64 fixture against production.

The [accepted prerequisites](ntp-monitoring-review.md#accepted-prerequisites--october-21-2026)
fix master sources .83/::83 and both names. The
[approved v2 capture](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-node-producer-readiness-20261021-v2/outcome.md) completed October 21 at
10:51:48 CDT with 701 ARM64 package records, matching 15-version cached simulation,
accepted NTP service continuity and protected-file hashes. No Munin account,
unit/listener/config, policy-rc.d or installer paths exist. Both directions' route
lookups select the reviewed source identities; packet/firewall/protocol acceptance
remains part of restricted installation and separate master checks. The actual
statistics directives and producer metadata are captured. Keep cached package
age/version reconciliation and source/hash/identity preflight in the outer bundle;
stop on drift instead of silently refreshing. Do not classify a pre-install
missing listener as a firewall failure. No package was installed by readiness.

## Configuration and mutation boundary

Bind TCP 4949 explicitly on `10.1.0.51` and `fd36:5aa8:6971:1::51`.
Allow only master source `10.1.3.83/32` and `fd36:5aa8:6971:1::83/128`,
with no additional loopback allowlist in this candidate. The old generated master ULA
is not the desired allowlist identity. Prove actual post-change route sources
before installing; reject broader LAN allowlists. Separate network-owned policy
changes if current firewall rules do not permit these exact flows.

Install only the selected packages, five packaged plugins, four custom readers
and reviewed privilege settings. Preserve the guarded first start, scoped package
autoconfiguration suppression, final source/settings/link readback and durable
recovery controls exercised in qualification. No NTP/GPSD changes, purge,
unrelated restart, master registration, scheduler change or notification send.

## Acceptance and recovery

Prove both literal listeners, independent TCP connections and real Munin protocol
config/fetches. Exercise all nine plugins under their installed identities;
validate source-built ntpq parsing/units, selected PPS/reach/leap fields, bounded
runtime, available-byte/inode floors and metadata-only statistics freshness.
Keep missing job-success records faulted until the producer stage is accepted.
Successful config/fetch with evidence=0 and age=U accepts reader behavior only;
it does not accept maintenance health. A missing record alone must not be
misclassified as installer recovery failure or bypassed with synthetic records.
Require unchanged package expectations, protected files and time-service identity.
Master-origin polling is accepted in the separate master stage after node health.

Recovery removes the authored start permit, stops/disables only munin-node and
restores only the matching authored policy wrapper. Packages and the start guard
remain installed. Retain durable state/backups. Foreign policy/guard drift holds;
foreign config is preserved while the service is contained. Verify closed
listeners, disabled/inactive unit and NTP continuity. Failed or interrupted
recovery needs inspection and a separately approved continuation.

## Executed bundle boundaries and continuation gate

The v2 readiness receipt is consumed. The
[outer controller](../../../homelab-ntp/ntpsec/scripts/run-munin-stage.py) seals
exact ARM64 packages, unchanged qualified installer/profile bytes, inventory
selection, source/settings/guard acceptance, independent family TCP checks and
authored containment. Focused tests cover dispatch success, failure recovery,
early identity rejection, actual stdin bootstrap and one-use/tamper boundaries.
The retained actual-installer container qualification was not rerun unchanged.

The producer bundle was accepted first; node package installation followed.
The old 701-package pin cannot authorize a new install. These stages ran neither
real job. Missing records remain faults until genuine
scheduled completion. The failed one-use outer archive and its inspection are consumed; neither can
be replayed. A new continuation requires fresh state and exact-hash approval. Follow its conditional
recovery and read-only inspection scope. Master protocol, scheduled collection,
fresh graphs and alerts remain under the [master design](../master/ntp-design.md).
No local or readiness result accepts production installation or master polling.
