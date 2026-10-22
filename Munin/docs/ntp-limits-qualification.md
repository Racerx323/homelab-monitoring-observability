# Native limits and contact qualification — October 22, 2026

## Corrected repository candidate

The correction now passes 28 native cases in the same pinned, network-disabled
image. That qualification changed no production source/configuration or contacts. The
original 14 cases below remain historical characterization; the corrected run
adds full-precision boundaries, unknown health fields, actual contact-candidate
inheritance and exclusion of generic/unrelated-host/unselected-master graphs.

The node reader now emits `selected_offset_ok` and `selected_jitter_ok` in
`ntp_health`, with full-precision inclusive ±5 ms and 0–1 ms comparisons.
Native limits evaluate their `1:1` critical ranges. Existing timing values,
names and seconds units remain unchanged; their incorrect native critical
directives are removed. Failed queries expose both flags as `U`. Two health
RRD fields are added; the 33-plugin selection and graph identities are preserved.

The contact candidate and helper now share exactly eight NTP graph origins,
plus master transport. Global and j2-host contacts default to `none`. Actual
native evaluation produced eight separately captured NTP messages and one
master-transport message, while df, unrelated hosts and unselected master
graphs produced no contact invocation. Captured messages passed the real helper's
validation without SMTP/status calls. No generic alert scope was added.

The [correction manifest](../node/profiles/ntp/timing-health.candidate-manifest.json)
pins repository artifacts and accepted baseline hashes. The guarded reader
update/recovery now passes 17 native transaction cases; separate node correction
and master acceptance reviews are recorded in the
[deployment procedure](ntp-timing-deployment.md). The approved node correction
committed and reconciled October 22 at 11:35:57 CDT. Separate master acceptance
passed at 11:54:45: three genuine post-commit cycles, twelve fresh health/timing
RRDs and ten verified dual-stack HTTPS resources including both day graphs.
Both new flags are 1; historical unknowns remain preserved. Contact activation
and exact-message delivery tests remain later reviews. Keep contacts disabled.

## Result

The installed native 2.0.73 limits implementation was exercised in the existing
local Bookworm image, with networking disabled, a read-only image/repository and
private temporary state. Four Config/Utils/LimitsOld module hashes matched the
accepted October 21 master source capture. This is local native-engine
qualification. The subsequent approved master capture at 10:28:57 CDT on
October 22 confirmed the same four native module hashes and protected
contacts-none configuration. The defects below remain applicable.

All 14 characterization cases passed with real native parsing, state files,
limits evaluation and child contact processes. Synthetic samples were confined
to the container. The contact command only captured stdin locally; the candidate
helper parsed those actual native messages without delivery or status writes.
Production contacts remain disabled. No production target was contacted.

| Behavior | Native result |
| --- | --- |
| Healthy, warning, critical and recovery | Correct state transitions and fixed six-field expansion |
| Repeated healthy/warning/unknown | No repeat notification without a transition |
| Inherited `unknown_limit 0` and stale samples | Immediate unknown; a sample older than 600 seconds becomes unknown |
| `contacts none` | No contact process/message |
| `max_messages 1` with two simultaneous graphs | Two separate EOF-delimited contact processes/messages |
| 4 ms jitter with critical `0:0.001` seconds | **Incorrectly healthy for the intended policy** |
| Offset exactly ±5 ms with critical `-0.005:0.005` seconds | **Incorrectly critical for the intended inclusive boundary** |
| Candidate helper given a `df` alert | Rejected despite the candidate host-wide contact assignment |

## Original findings

These findings describe the preceding candidate and deployed reader. The
repository correction above addresses them; the node reader is now deployed,
with scheduled master-field acceptance also passed.

The native evaluator formats each value with `sprintf("%.2f", value)` before
comparing limits. It turns 0.004 seconds into 0.00 and ±0.005 into ±0.01.
The current second-based timing thresholds cannot enforce the intended
5 ms offset and 1 ms jitter policy. This affects limits evaluation; it does not
invalidate the recorded raw timing measurements or earlier transport evidence.
Do not activate contacts on the strength of the existing seconds thresholds.

Recommended correction: preserve existing timing series/units and add explicit
offset/jitter threshold-health fields computed from full-precision values in
the node reader, exposing unknown input as `U` and healthy/unhealthy as 1/0.
Their native critical range can then be `1:1`. Retire the misleading native
critical directives on the second-based series. This requires a separate
coordinated node/master correction, field-count qualification and guarded
deployment review; no production payload was changed here.

The candidate assigns `contacts ntp_mailrise` to the entire expanded host, while
the helper accepts only the original 16 graph identities. Generic alerts such
as `df` would fail validation. Nested multigraphs also require explicit identity
handling: the native evaluator's plugin variable names the local service node.
Do not solve this by accepting arbitrary strings or only adding device names.
Before activation, choose an explicit reviewed graph scope. The smallest scope
keeps host contacts `none` and assigns the contact only to reviewed NTP graphs
and master transport. Broader generic alerts require an exact graph-identity
mapping and matching helper validation, including multigraph qualification.
Neither option was activated or silently selected here.

## Maintenance observation

The separately approved read-only master review executed once at 10:28:57 CDT
on October 22. All four maintenance RRDs are present and fresh. Both evidence
fields equal 1 and both numeric age series agree with the sealed real producer
completion epochs. Six finite 300-second samples per field, native cycles at
10:10/10:15/10:20 CDT and all ten verified dual-stack HTTPS requests passed,
including both maintenance PNGs. Protected continuity, the four native module
hashes and the empty effective include directory passed. Contacts stayed disabled.

Accept bounded master consumption and serving of the genuine maintenance fields.
Consolidation does not identify an individual raw fetch. No job, update/limits,
contact or plugin was invoked, and no service/configuration change occurred.
The [outcome](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-master-maintenance-observation-20261022-v1/outcome.md)
retains scope and evidence. The receipt is consumed; do not replay it. Corrected
alert behavior, downstream delivery and continued recurrence remain open.

## Retained qualification

The repository-owned [native test](../tests/test_limits_native.py) is explicitly
container-only. It imports installed package modules, creates only fresh test
state and uses the existing contact helper's parsing path without calling its
delivery function. No archived executable implementation is imported.

Private evidence is retained under
`munin-limits-preparation-20261022-v1`: pinned image/source/input invocation,
native stdout/stderr/status, offline test logs, and the maintenance sealing
record. The native result characterizes the defects above; it does not certify
the current alert design or downstream delivery. Exact-message delivery tests
remain separate later gates after the blockers are corrected.
