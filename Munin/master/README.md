# Munin master

This component owns native svmf polling, limits and contact candidates. The
[j2 design](ntp-design.md) selects one canonical IPv4 metric series and a
master-local plugin that verifies both literal families during the existing
five-minute Munin schedule. Installation and three captured scheduled cycles
are accepted; longer observation and remaining health gates stay open.

The canonical baseline is [configs/munin.conf](configs/munin.conf), targeting
production `/etc/munin/munin.conf`. The [configuration review](../docs/master-config-review.md)
records accepted commissioning at 15:34:46 CDT on October 21; the canonical
mirror matches accepted production bytes. The stale cache directive is removed,
one canonical j2 entry and the transport plugin are installed, and contacts
remain none. The guarded [deployment workflow](../docs/ntp-master-deployment.md)
committed after dual-family transport and independent HTTPS acceptance.
The [master observation outcome](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-master-observation-20261021-v1/outcome.md)
accepts three scheduled cycles, fresh RRD updates and all 40 verified dual-family
HTTPS checks. Both maintenance records remain absent (evidence=0, ages unknown);
mail is also unknown. The [observation procedure](../docs/ntp-observation.md)
retains provenance and freshness rules. Maintenance completion, actual canonical
source attribution, limits/delivery, client coverage and persistence remain open.

The [configuration lifecycle](configuration-lifecycle.md) requires an exact
production import and matching readback after every accepted deployment or
restoration. Keep the accepted mirror separate from future candidates. The
[synchronizer](../scripts/sync_master_baseline.py) imports verified private
captures after scanning their exact bytes and reports drift without target access.

[Registration/contact configuration](configs/j2-svntp1.conf.example) and
[plugin privileges](configs/ntp-transport.plugin-conf.example) are merge inputs,
not complete replacements for `/etc/munin/munin.conf` or existing node settings.
Keep unrelated hosts and contacts. The existing Apache vhost remains the serving
authority. Installation requires a separate sealed master operation after the
[node and producer stages](../docs/ntp-monitoring-review.md#separate-stage-handoff).

The [transport plugin](plugins/ntp_transport_j2) runs as munin. The
[fixed Mailrise contact](../scripts/ntp_mailrise.py) submits only through the
observed loopback endpoint; exact test messages require separate approval.
Missing genuine job records remain faults. Local tests do not prove scheduled
polling, fresh graphs, limits evaluation or downstream alert delivery.
