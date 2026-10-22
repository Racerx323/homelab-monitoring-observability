# Native master configuration review

Reviewed October 21, 2026. Canonical repository baseline:
[master/configs/munin.conf](../master/configs/munin.conf).
Production path: `/etc/munin/munin.conf` on svmf. Recommendations outside the
accepted commissioning scope remain proposals.

## Production correspondence

Commissioning committed at **15:34:46 CDT on October 21**. The accepted production
candidate and canonical repository mirror match byte-for-byte at SHA-256
`eefe2d3f0cfa59f65ee76b06e53e8e4ef911e9f6fa169ff8f6140d9e61c11851`.
The guarded synchronizer privately scanned exact bytes and imported atomically.
Production names, unrelated sections, comments and historical graph identities
remain preserved. The initial 14:15:51 baseline and frozen archives remain
historical evidence; do not reimport them over the accepted successor.

The [commissioning outcome](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-master-commissioning-20261021-v1/outcome.md)
records consumed approval, successful native parser/CLI/protocol checks and
independent verified HTTPS before and after on both literals. The stale cache
socket directive is removed; native direct-RRD defaults are active. One canonical
j2 registration and transport overrides/plugin are installed with contacts none.
Munin-node restarted and verified native CGI descendants refreshed; Apache
identity stayed unchanged. Commissioning alone did not accept scheduled collection or fresh j2 graphs.
The later [master observation](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-master-observation-20261021-v1/outcome.md)
accepts three native cycles, fresh RRD updates and verified dual-family serving.
Maintenance records, source attribution, limits/transitions and delivered alerts
remain open.

The [configuration lifecycle](../master/configuration-lifecycle.md) requires
matching readback/repository synchronization after every accepted change or
restoration. This equality is tied to the accepted operation, not indefinite
live state. No additional tuning was applied.

## Findings and recommendations

| Item | Assessment | Proposed action |
| --- | --- | --- |
| Baseline synchronization | Exact production bytes imported and hash-verified | Preserve production identities; reject drift and synchronize the mirror after accepted deployment/restoration |
| j2 registration | Canonical IPv4 entry and dual-family transport installed | Observe genuine native scheduled data and both transport fields |
| Alert contacts | Baseline contact examples are commented; earlier inspection found no active contacts | Commission with explicit `contacts none` for the new j2 series and transport graph; activate only scoped contacts after parser/limits qualification and exact-message approval |
| Cache transport | Stale socket directive removed; native direct-RRD operation commissioned | Observe fresh j2 graphs; retain qualified restoration and existing history |
| `munin_cgi_graph_jobs 6` | Comment names `max_cgi_graph_jobs`; the fetched 2.0.73 CGI entry point does not directly consume either key | All three graph-job keys parse in installed code. Actual FastCGI process controls remain unqualified; do not rename the key or claim it caps Apache workers |
| `graph_strategy cgi`, `html_strategy cgi` | Consistent with the accepted Apache CGI serving arrangement | Preserve; verify current CGI paths, access, cache permissions and new graph freshness during master acceptance |
| `graph_period minute` | Global graph display choice affects rate presentation | Prefer default seconds unless per-minute units are intentional; verify plugin labels and overrides before proposing a change. It does not change the five-minute polling schedule |
| `max_processes 16`, fetch deadlines 180/240 seconds | No evidence of a capacity or timeout fault in retained observations | Preserve initially; tune from measured cycle duration, CPU/memory and failures, keeping collection within the native five-minute cycle |
| Includes and permissions | Configured include directory requires effective native expansion/inheritance checks | Pin actual files and owners/modes; inspect native include rules and keep unprivileged parsing distinct from update/limits execution |
| Example comments | Long stock examples obscure the four active node sections | After reconciling bytes, shorten comments in a separate repository cleanup; avoid a whole-file replacement during j2 activation |

No additional tuning change, daemon replacement, web-server change or node rename
is justified by the current evidence. Stale-cache removal is accepted; preserve
the synchronized successor and existing production paths/services.

## Qualification and activation boundary

The [acceptance review](ntp-master-acceptance-review.md) remains the deployment
gate. The new read-only `master-config` mode in the NTP-owned readiness controller
pins this baseline, the contact example and the monitoring-owned
[qualification helper](../scripts/qualify_master.py). It compares actual bytes,
exports only safe directive differences, and exercises the installed native
parser as munin on in-memory current/repository/commissioning/example streams.
It captures fixed native source, supported reload metadata and socket metadata.
No update, limits, plugin, contact, restart, reload or production write occurs.

Parsing each supplied stream does not prove native include filtering or effective
contact inheritance; those remain explicit unknowns until installed source and
parser results are reviewed. The read-only parsing results alone were not an
installer or restoration proof. The accepted preserving merge retains identities, inserts
only the transport overrides and j2 section, and uses `contacts none`; the
upstream 2.0.73 limits implementation explicitly skips that contact name.

The guarded [commissioning workflow](ntp-master-deployment.md) now passes nine
isolated native Bookworm cases, including actual node restart, CGI refresh,
conditional restoration, foreign-drift preservation, worker/controller loss and
rejected HTTPS acceptance. Native text/unit hashes match the production capture.
The [sealed review](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-master-commissioning-20261021-v1/review.md)
was executed successfully; see the accepted outcome above. New contacts remain
none. The accepted mirror is synchronized after commit/readback;
the later three-cycle/graph observation passed within its captured scope.
Actual maintenance records, source attribution, limits/transitions and exact
previewed delivery remain separate gates.

## Sources and limits

The installed Debian Munin 2.0.73-1 code remains authoritative. Context7 supplied
the upstream configuration/rrdcached/Apache CGI references. The review also
retrieved version-pinned upstream `2.0.73` Config, GraphOld, HTMLOld, Update,
LimitsOld and CGI graph sources into private evidence, with hashes retained.
Upstream source explains behavior; it does not prove Debian byte equality.

- [Munin configuration reference](https://github.com/munin-monitoring/munin/blob/2.0.73/doc/reference/munin.conf.rst)
- [Native parser](https://github.com/munin-monitoring/munin/blob/2.0.73/master/lib/Munin/Master/Config.pm)
- [Limits/contact implementation](https://github.com/munin-monitoring/munin/blob/2.0.73/master/lib/Munin/Master/LimitsOld.pm)
- [CGI graph implementation](https://github.com/munin-monitoring/munin/blob/2.0.73/master/_bin/munin-cgi-graph.in)
- [rrdcached integration](https://github.com/munin-monitoring/munin/blob/master/doc/master/rrdcached.rst)

The read-only parsing and source review preceded accepted production
commissioning. Live activation and existing-dashboard continuity are accepted;
production restoration was not needed. Conditional restoration passed isolated
native qualification. Scheduled collection, fresh j2 graphs, limits/transitions,
delivery and extended monitoring remain open. Native CGI refresh preserves
Apache identity and signals only verified descendants through pidfds.
