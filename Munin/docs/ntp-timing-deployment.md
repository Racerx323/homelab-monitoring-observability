# Guarded timing-health reader correction

This rollout replaces one node reader and then observes genuine master
collection. It does not install the contact helper or activate any contact.
The [correction manifest](../node/profiles/ntp/timing-health.candidate-manifest.json)
owns the fields and future explicit contact scope. The approved node v2 stage
committed and reconciled the corrected reader at 11:35:57 CDT on October 22.
Separate master scheduled-field/graph acceptance passed at 11:54:45 CDT.

## Node correction and companion checks

The repository's existing generic transaction now has a closed `timing` role.
It uses the same authenticated archive, root launcher, detached worker,
operation lock, inode-based publication intents and independent systemd guard.
It atomically replaces only `/usr/local/munin/lib/plugins/ntp_metrics.py`, mode
0644 root:root. Exactly 33 links and all node settings remain unchanged.
Only munin-node stops/starts; its accepted unit, drop-ins and permit are pinned.
No NTP/GPS, package, network, cron, master configuration or contact change occurs.

This review includes the companion master for source-bound protocol and existing
HTTPS continuity checks. Both IPv4 and IPv6 must fetch the complete current
selection before mutation. After publication, both flags must equal 1, declare
native critical 1:1, and preserve the raw seconds graph without the incorrect
native timing critical directives. Two complete post-publication fetches have
a genuine 305-second separation. A known rejection restores matching authored
bytes; uncertain transport leaves the independent 600-second guard armed.
Foreign drift holds recovery without overwriting it. A completed restoration
is idempotent: a later guard does not restart the node again.

The master native update code requests service configuration during ordinary
collection. The correction therefore needs no forced master update, manual RRD
creation or limits invocation. Existing RRD history remains intact. Warm probes
do not prove new scheduled RRD/graph freshness; the next review owns that gate.

## Separate master acceptance

The master-only read-only review requires the node controller's accepted,
committed and repository-reconciled result for the exact sealed archive.
Its derived runtime context records the actual commit completion epoch and is
hash-bound to the capture separately from the immutable sealed specification.
Later observation reviews can reuse the accepted commit without replaying the
node mutation. No additional node contact is included in this review.

Run only after three consecutive eligible native post-commit cycles exist,
allowing the usual 240-second eligibility margin. The collector does not wait
or trigger a collection. It reads twelve exact GAUGE RRDs: eight ntp_health
fields and four unchanged ntp_timing fields. Both new flags must be 1 in fresh
post-commit samples. Pre-creation unknown history remains visible and is not
treated as a successful post-commit sample. Existing native cron/update evidence
must support all three cycles; missing/intervening failures cannot be skipped.

Ten fixed verified HTTPS requests cover root/CSS/index and both day PNGs over
both master families. Require field freshness as well as valid served PNGs.
Main configuration remains pinned to accepted contacts-none bytes, native
module hashes remain pinned and effective includes must stay empty. No parser,
update, limits, contact, plugin, job or state-deserialization command is invoked.

The approved capture accepted native 11:40/11:45/11:50 CDT cycles, all twelve
fresh RRDs with three finite post-commit samples each, and ten verified
dual-stack HTTPS resources including both day graphs. Both corrected timing
flags are 1. Historical pre-creation unknowns remain visible. Protected
continuity, contacts-none configuration, native modules and empty effective
includes passed. Private node/master outcomes retain the evidence bindings.

## Qualification and approval order

Native recovery qualification covers the original nine transaction cases plus
eight reader-correction cases: commit, restoration, worker/controller loss,
foreign file/link/settings preservation and early preflight rejection. Real
systemd guards and Munin-node serving run in isolated network-disabled
containers. The transaction reader baseline is synthetic test data; this
qualification does not claim GPS/time accuracy. The real reader's timing and
contact semantics separately passed the 28 native limits cases.

The approved node v2 review committed and reconciled; its receipt is consumed.
A superseded, unexecuted v1 proposal remains private. Both complete post-change
dual-stack probes passed across all 33 plugins with the required 305-second
gap, and all twelve before/after HTTPS continuity requests passed. Recovery
was disarmed on commit. The separately approved master review also executed
once after sufficient genuine scheduled cycles. Do not replay either review.

- **Node reader correction and companion checks, v2:**
  [review](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-generic-timing-20261022-v2/review.md)
  / [SHA-256](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-generic-timing-20261022-v2/sealing.json:1).
- **Master-only corrected-field acceptance:**
  [review](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-timing-master-acceptance-20261022-v1/review.md)
  / [SHA-256](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-timing-master-acceptance-20261022-v1/sealing.json:1).

Each has its own hash and one-use receipt. Do not replay consumed operations or
infer acceptance from elapsed time. Keep backups and raw captures private.

On accepted node commit the repository candidate must still match the sealed
reader; reconciliation rejects foreign local edits. The later master result
closes only corrected collection/serving. Contact activation and exact-message
problem/recovery delivery remain later approvals. Sustained storage budget,
client coverage, persistence and final observation remain open.
