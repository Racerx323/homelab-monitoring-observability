# Expanded Munin observations

Both approved observations executed October 21, 2026 with complete captures,
controller/SSH exit 0 and unchanged protected continuity. Expanded scheduled
collection, bounded RRD freshness and all dual-stack graph families are accepted.
Producer success, source attribution and alert gates remain open; contacts stay
disabled. Receipts are consumed and cannot replay.

## Observed outcome

Three genuine post-expansion cycles at 19:00/19:05/19:10 CDT passed the native
cron/update rule. All 56 j2 graph families plus master transport were covered:
280 fresh RRDs with no missing fields and 120 successful verified HTTPS requests,
including 114 day PNGs. df/df_inode each had six recent fields. Unknown samples
were limited to the two missing maintenance ages and disabled mail status.

Node/producer capture at 19:13:59 CDT found both success records absent. Retention's
next observed trigger is October 22 at 00:45:39 CDT; reporting is configured for
05:30 America/Chicago. Neither schedule proves execution. Use a newly approved
read-only follow-up after completion to inspect real records and provenance.
Master capture at 19:14:41 CDT establishes bounded freshness, not ongoing health.

Retained [node outcome](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-expanded-node-observation-20261021-v1/outcome.md)
and [master outcome](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-expanded-master-observation-20261021-v1/outcome.md)
record the independent acceptance conclusions and remaining gates.

## Consumed reviews

- **j2-svntp1 node/producer:**
  [review](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-expanded-node-observation-20261021-v1/review.md)
  / [SHA-256](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-expanded-node-observation-20261021-v1/sealing.json:1).
- **svmf native master:**
  [review](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-expanded-master-observation-20261021-v1/review.md)
  / [SHA-256](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-expanded-master-observation-20261021-v1/sealing.json:1).

Each uses strict host-key/hostname/boot and accepted protected file/service
pins, one fsynced local receipt, bounded private capture and no replay. Runtime
implementations come from repository sources frozen into each archive; previous
archives provide data/provenance only. No target staging, package action,
service or timer change, plugin/protocol invocation, maintenance job, RRD write,
limits transition or notification is included. Ordinary audit logs and native
HTTPS CGI/cache writes remain possible. Missing evidence stays explicit.

## Node and genuine producers

Verify the exact 33 root-owned plugin links and committed expanded settings,
without running plugins. Read only the two bounded root-private success records,
validate schema/job/status/completion/age and correlate existing scheduler
provenance. Missing records, rotated logs or timer activity alone do not prove
success. Keep NTP continuity, producer completion and delivered alerts separate;
never invoke a job or infer its result from elapsed time.

## Three expanded collection cycles

The eligibility cutoff is after the node and final-master controllers finished
accepted, committed and reconciled stages. Use the latest three eligible native
starts in consecutive 300-second slots; correlate actual munin cron events and
both node/global finishes, rejecting gaps, intervening starts and logged faults.
Do not reuse the earlier nine-plugin observation, skip failures, wait for cycles
or force an update. Insufficient evidence needs a later separately approved
capture. This does not accept the longer final observation interval.

## Complete graph and field coverage

The sealed inventory derives from accepted expanded protocol and native
qualification captures: 56 j2 graph names plus master transport, with 277 j2 data
fields at deployment and three transport fields. All 12 diskstats device
subgraphs and four overviews are included. Native dotted graph names map to
hyphenated RRD service names and nested CGI paths. No historical state file is
deserialized. Preserve the canonical host and all ordinary RRD history.

Read only direct native RRD files under the two fixed host directories, at most
512 directory entries each and 384 selected files total. Fixed fields/types are
sealed; missing fields cannot be replaced by arbitrary files. df/df_inode mount
membership is dynamic: each exact graph prefix permits up to 64 direct gauge
RRDs, retaining names, timestamps and stale history for review against six fields
per graph at deployment. Older isolated nine-field mount lists are not treated
as today's required membership. No unsupported graph is silently omitted.

Use only bounded rrdtool lastupdate and fetch AVERAGE at 300-second resolution,
with unknown/NaN retained as null. Review per-field freshness against the same
observation window; consolidated values do not attribute exact raw samples to
a particular scheduler invocation. Transport mail and absent maintenance ages
remain explicit unknowns until separately accepted.

The controller requests root/CSS/j2 index and all 57 day PNGs over both explicit
master literals: 120 HTTPS requests maximum, each hostname/CA/leaf verified and
bounded to 12 seconds/1 MiB. An aggregate 180-second budget allows at most one
in-flight request beyond the cutoff. Stop on first failure. A valid PNG/HTTP 200
proves serving, not fresh measurements; correlate every graph with RRD evidence.

## Configuration presentation and remaining gates

The operator intentionally moved the main-config j2 stanza for human readability
without changing operational directives. Preserve that repository layout.
Production's accepted byte hash remains pinned, so byte-for-byte equality is
not claimed. No main-config deployment or layout correction is part of these
observations; this documented presentation difference is not a functional fault.

Capture completion is not readiness acceptance. Keep canonical source-address
attribution, limits/transitions, delivered alerts, sustained growth/storage,
client coverage, persistence, final observation and the later separate-host
ntpviz requirement open. The
[readiness checklist](/home/aaron/code/homelab-ntp/ntpsec/docs/PRODUCTION-READINESS.md)
owns the current checkpoint; execution outcomes belong in NTP history.
