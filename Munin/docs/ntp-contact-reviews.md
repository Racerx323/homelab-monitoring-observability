# Gated NTP contact activation and exact-message delivery

Activation v3 executed once and committed with repository reconciliation and
twelve passing verified HTTPS checks. Gated notifications are enabled for the
reviewed nine graph origins. The proof-preserving successor leaves the retained
commissioning proof untouched and retains strict checks for all other authored
files. Sixteen native contact cases and 28 limits cases qualified the final inputs.

The exact problem test was attempted once and recorded SMTP `450 failed to send
notification`. Aaron nevertheless supplied the exact downstream Apprise problem
message. Preserve both the failed submission status and confirmed delivery;
never retry the consumed send. The recorded operator confirmation then allowed
the separately approved recovery test, whose SMTP submission/status passed.
Aaron supplied the exact recovery notification too. Both confirmations bind
the exact archive/message/consumed receipt; no delivery was inferred from SMTP.

Aaron also supplied an automatic CRITICAL `J1-SVMF/ntp_transport_j2` notification
for field `mail`, followed by the automatic transport OK notification with no
warning, critical or unknown fields. Both downstream arrivals are explicitly
operator-confirmed. Native sample attribution and the SMTP discrepancy's cause
remain unverified; no additional target inspection or send occurred.
The approved [mail/limits/status observation](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-contact-mail-observation-20261022-v1/outcome.md)
completed once at 15:07:04 CDT. Protected committed inputs/services and empty
includes passed. Native mail sample is 1 at 15:05:13, matching RRD lastupdate;
limits state is ok. Three genuine completed cycles began at 14:50:02, 14:55:01
and 15:00:01. Status is successful and stable, last attempted at 14:50:15; the
schema has no message identity. Optional suppression state is absent. The RRD
retains earlier zero/recovery/later-one AVERAGE intervals, not raw fetches.

Aaron's Apprise logs establish initial partial delivery: Discord and Mailgun
reported success, Pushover had a connection error and the API returned 424.
Later requests reported success for all three services with HTTP 200. Preserve
the SMTP 450 result separately from confirmed delivery. The underlying Pushover
connection cause and exact later per-message mapping remain unproven.

Bounded native mail/current-state observation is accepted. No retry, forced
collection, limits/contact invocation, HTTP or target mutation occurred. The
observation receipt is consumed; further target reads need a separate scope.

## Consumed execution stages

1. [Activation v3 outcome](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-contacts-activate-20261022-v3/outcome.md).
2. [Problem v2 outcome](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-contacts-problem-20261022-v2/outcome.md).
3. [Recovery v2 outcome](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-contacts-recovery-20261022-v2/outcome.md).

All three approved one-use stages are consumed. Do not replay them. Original
activation v2 and its metadata diagnostic remain historical consumed operations.
No post-commit restoration, status editing or new target inspection is implied.

## Dedicated transaction and first-send boundary

The [sealer/controller](../scripts/review_ntp_contacts.py) freezes all sources,
qualification, accepted observation provenance, target/boot/service/file pins,
both before configs, candidate, TLS material and message inputs. The
[installer/restorer](../scripts/install_ntp_contacts.py) is dedicated to contacts.
It reuses repository launch/lock/timer mechanics; the consumed commissioning
installer and its contact-forbidden scope are never selected or replayed.

Only native master `pi@10.1.3.83`, strict alias `svmf.local.theama.co`, is targeted.
Keep global and j2-host defaults `contacts none`; select only the eight explicit
NTP graphs and master transport in the [design](../master/ntp-design.md#contact-and-delivery-failure).
Preserve the operator's repository stanza placement. Its directives equal the
accepted production baseline despite different bytes; reconciliation pins its
separate before hash and rejects concurrent local edits.

Install helper and [gate](../scripts/ntp_contact_gate.py) root:root 0755 under
`/usr/local/libexec`. Provision `/var/lib/munin/ntp-alerts` as munin:munin 0700,
and the root-owned gate directory and 0644 lock. Reject preexisting authored
destinations, unsafe ancestry/metadata, shared files and nonempty effective
includes. Do not preseed success. No package, collection, limits, job, cron,
Apache, Munin-node, NTP-node, networking or RRD action is performed.

The gate starts disabled. Real native calls before enable exit 75 without SMTP
or a success record, preserve suppression evidence, and prevent commit. They
are not silently accepted, queued, retried or backfilled. An exclusive gate lock
orders suppression detection and commit. The controller requires installed
native parsing and six verified HTTPS continuity requests before and after
preparation. Genuine scheduled use remains a separate acceptance gate.

Commit first persists a durable committed decision, then publishes the
config/helper/gate-hash-bound enable marker. Marker publication is the first
possible automatic send. A lost committer after the decision but before enable
leaves contacts disabled and the stage held for inspection; the guard neither
undoes nor completes a committed decision. A message submitted after enable
cannot be recalled. Ordinary calls validate current pinned inputs under a shared
lock and hold it through SMTP/status recording. No schedule is stopped to make
this boundary work.

## Recovery and uncertainty

An exclusive stage lock, durable publication inode intents and independent
600-second current-boot systemd recovery protect the uncommitted operation.
Known rejection restores only matching authored main/helper/gate bytes and empty
directories. Preserve actual submission/suppression records and foreign changes;
foreign drift holds recovery. Recovery handles interrupted no-clobber publication
and does not repeat restoration. Keep backups, proofs and all RRDs.

Controller/worker loss before durable commit recovers independently. This is not
power-loss/reboot recovery. Uncertain outcomes use the approved same-bundle
read-only inspection once within expiry, never apply replay. Committed rollback
or a partially completed commit needs a new inspected continuation review.

## One-use exact sender and receipt confirmation

Each send requires accepted, committed and repository-reconciled activation,
matching remote worker token, installed helper/gate/config and protected
continuity. Consume and fsync the local receipt before target contact and a
root-private remote receipt before the SMTP attempt. Drop permanently to the
native munin UID/GID; hold the gate lock so native submissions cannot race the
test status write. Send exactly the reviewed `.eml` bytes to the fixed envelope,
through `127.0.0.1:8025` only, ten-second timeout, one attempt, no retry.

Problem recipient is `notify.failure@mailrise.xyz`; recovery recipient is
`notify@mailrise.xyz`; sender is `munin@local.theama.co`. No Proton Mail,
sendmail, alternate route or production fault is used. Record only the actual
helper submission result as 0600 after the attempt. Status-write failure cannot
justify another send. SMTP timeout or lost transport leaves submission uncertain
and receipts consumed even if the receiver obtained the message.

SMTP acceptance proves submission only. Aaron must explicitly confirm each
actual downstream receipt. Only after that direct confirmation may the local
`confirm-delivery` action record the operator's words, exact archive/message
hashes and consumed-receipt hash. It sends nothing. Recovery execution checks
that bound problem confirmation before target contact; no elapsed time,
controller completion or inferred success can create it. Recovery's own receipt
confirmation remains necessary to accept both routes.

## Qualification and remaining gates

Thirteen real native systemd cases pass against final input hashes: success,
idempotent restoration, known rejection, worker/controller loss, foreign
config/helper/state preservation, early preflight drift, loss after the commit
decision, ambiguous SMTP acknowledgement, interrupted publication and actual
pre-commit suppression. All seven protected native modules match production
provenance. The 28 actual native limits cases also pass with the gated candidate.
The full scaffold suite includes focused closed-scope, payload and confirmation
checks. Loopback qualification captures real SMTP wire bytes in isolated
containers; it does not claim production Mailrise or downstream delivery.

The predecessor metadata rejection and read-only diagnosis remain retained.
Successor activation and both controlled tests are now executed; both exact
messages have explicit downstream confirmations. Bounded native mail recovery and scheduled collection are now accepted. The
underlying Pushover connection cause, sustained storage budget, client/source
persistence, coverage and final observation remain open.
The NTP readiness checklist records the current read-only follow-up gate.
