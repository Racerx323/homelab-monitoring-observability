# Read-only scheduled-record and graph observation

Use separate reviews for the NTP node's actual maintenance records and the
native master's scheduled collection and dashboard. The
[controller](../scripts/review_ntp_observation.py) seals each against accepted
producer installation, corrected node runtime and committed master commissioning.
The [collector](../scripts/observe_ntp.py) reads existing evidence; it does not
run a job, plugin, update, limits process or packet capture. Do not replay an
accepted installer or use a pre-install inventory pin.

## Node and producer evidence

Validate the two independent private completion records and correlate their
epochs with matching cron/logrotate events. Each must follow the actual producer
installation, name the correct job, indicate success and be no older than
172800 seconds. A global logrotate timer timestamp alone does not establish
execution of the NTP rule. Missing records remain faults. Reporting's 05:30
America/Chicago schedule can legitimately mean its first post-install scheduled
record does not yet exist. This observation never invokes it or sends mail.

Record provenance separately from freshness and downstream delivery. If journal
records are unavailable, rotated or insufficient, keep scheduled provenance open
rather than calling a syntactically valid timestamp proof of scheduled execution.

## Three native cycles and graph freshness

The master capture is retrospective, bounded to existing evidence. Review the
latest three eligible completed post-commissioning runs in consecutive
five-minute slots. Require matching native cron events, completed j2 and master
workers and global completion within 240 seconds of each start, with no fault
or intervening start. Starts must be within 60 seconds of their cron boundary;
an eligible start is at least 240 seconds old. Do not bridge a failed/missing
slot, silently restart a window or infer acceptance from elapsed time.

Inspect native last-update timestamps and 300-second AVERAGE samples for the
same three cycles, across the 16 j2 graphs and master transport graph. Check
every collected field, not only an aggregate timestamp. Require both transport
fields to show successful collection; absent mail evidence remains unknown.
RRD consolidation is not an exact raw fetch. Unknown job ages, data gaps,
missing graphs or stale RRDs remain visible and unaccepted.

Verify HTML/CSS and the actual day PNGs over both explicit master addresses with
hostname, CA and leaf verification. Ordinary CGI requests may refresh native
caches. A rendered PNG or changed image hash is insufficient: require recent
underlying RRD updates and samples. Capture time, sample times and HTTPS results
must be reviewed together. No manual Munin collection is allowed to make a graph
look current. Missing cron journal attribution or unsupported log/RRD layout is
a finding requiring a later scoped review; do not expand paths during execution.

The captures do not attribute the actual canonical TCP connection's source.
Keep that design obligation open until directly evidenced. Three cycles also
do not close limits/transitions, delivery, longer statistics-growth/storage
budget observation, persistence, OBS-09 or required later separate-host ntpviz.

## Preparation and execution

Run offline contracts through the normal scaffold validation. Seal one `node`
and one `master` review with accepted operation directories as data inputs:

```bash
python3 -I -B Munin/scripts/review_ntp_observation.py seal \
    --kind node \
    --commissioning ACCEPTED_MASTER \
    --producers ACCEPTED_PRODUCERS \
    --node ACCEPTED_CORRECTED_NODE \
    --output PRIVATE_NEW_OPERATION
```

Repeat preparation with `--kind master` and a distinct output directory. The
archive includes the exact controller, collector, transport helper, TLS probe,
tests, host key, trust data, specification and review. Check the frozen archive
locally before requesting its exact-hash execution approval:

```bash
python3 -I -B DIRECTORY/runner.py check \
    --directory DIRECTORY --sha256 APPROVED_SHA256
python3 -I -B DIRECTORY/runner.py execute \
    --directory DIRECTORY --sha256 APPROVED_SHA256
```

Execution consumes one receipt before target contact and retains private raw
capture and HTTPS observations. A complete capture is not automatic readiness
acceptance. No recovery is included because the inspection authors no production
state. A failed, partial or inconclusive capture needs a new separately approved
review for additional contact. Keep raw evidence private and record accepted
findings/open gates in the readiness checklist and deployment history.
