# Generic statistics parity for j2-svntp1

The operator requires j2-svntp1 to expose every applicable generic system
statistic provided by j2-svpi4mf, alongside all four NTP-specific readers.
The accepted expanded profile selects 29 generic package plugin instances plus
four NTP readers. Dependency/NFS/privilege/runtime qualification, coordinated
deployment and expanded scheduled RRD/graph observations are complete; the
canonical profile and settings mirror that deployment. The original five-plugin
baseline is historical, not the current accepted selection.

The [observed comparison](ntp-generic-comparison.md) retains the initial inventory
and mapping rationale; [deployment](ntp-generic-deployment.md) and
[expanded observations](ntp-expanded-observation.md) retain acceptance. Broader
client/access coverage, source persistence and sustained operation follow the
[NTP observation contract](../../../homelab-ntp/ntpsec/docs/PRODUCTION-OBSERVATION-CONTRACT.md#coverage-and-persistence-reconciliation).
Preserve accepted device mappings rather than rediscovering parity from stale RRDs.

## Establish the actual baseline

Use separate read-only inventories through the
[observation controller](../scripts/review_ntp_observation.py) with
`seal --generic-profile --kind node` and `seal --generic-profile --kind master`.
The standard accepted commissioning/producer/corrected-node inputs still apply;
each inventory requires its own exact-hash execution approval.

The master inventory reads the reference and target's existing native RRD
names/mtimes and verified HTTPS index links. It contacts svmf only. It does not
connect to the reference host or execute any reference plugin. Historical RRDs
must be checked against current page links and recent activity; they are not
proof of the currently enabled plugin set. Missing/unsupported layout or stale
reference evidence needs a scoped follow-up rather than invented parity.

The node inventory reads installed plugin links/source hashes, available package
plugin names, safe privilege/timeout selectors and installed Munin versions.
It lists network, block, thermal and hwmon capability names without reading
devices or sensors. It exports no environment values and runs no plugins,
autoconfiguration, suggestions, SMART commands, service changes or installs.

## Expanded profile and deployment requirements

Build an explicit graph-by-graph comparison from the inventories. Classify each
reference graph as a generic system/hardware measurement or reference-only
application measurement. Include every applicable generic measurement, not just
a predefined shortlist. Map interface/disk/sensor instances to actual target
names. Record every unsupported capability and proposed equivalent for review;
do not silently omit a requested measurement or copy a foreign device name.

Keep ntp_health, ntp_storage, ntp_statistics and ntp_jobs, their accepted data
identities and genuine maintenance evidence. Review each added plugin's actual
package source, dependencies, privileges, bounded runtime and failure behavior.
Use ordinary unprivileged counters where supported; justify additional privilege
or device access per plugin. Package presence is not qualification or permission
to enable every installed plugin. Keep application-specific statistics scoped
to applications that actually run on j2-svntp1.

The current installer and master transport plugin enforce the exact nine-plugin
set. Enabling additional node links alone makes the master transport check
fail. Prepare a coordinated continuation that updates selection/settings,
guarded node readback and the master's expected set, with a reviewed transition
and ownership-safe restoration. Preserve both explicit transport families and
all NTP checks. Measure complete config/fetch runtime for the expanded set; do
not blindly remove the 25-second protocol budget or relax validation to accept
arbitrary plugins. Keep the accepted main master configuration synchronized.

After approved deployment, accept actual scheduled collection, each new generic
graph and existing NTP graphs over both dashboard families. Existing nine-plugin
observations remain historical evidence; they do not accept the expanded set.
Genuine maintenance completion, source attribution, limits/delivery, sustained
statistics retention/growth, persistence and later separate-host ntpviz retain
their own open gates. Do not let profile expansion hide those follow-ups.
