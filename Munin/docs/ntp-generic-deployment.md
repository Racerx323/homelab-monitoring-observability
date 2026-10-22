# Coordinated generic-statistics expansion

Updated October 21, 2026. **All three approved v2 stages committed, accepted
and repository-reconciled.** The node now selects 29 generic plugins plus four
NTP readers; final master transport requires exactly that expanded set.

Compatibility v1 stopped before publication and is consumed. The
[metadata inspection](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-transport-metadata-20261021-v1/outcome.md)
confirmed the accepted hash, root:root ownership and mode 0755; only link count
2 differed from the expected 1. The original installer retains a hard-link
publication proof. The corrected preflight pins the inspected inode and requires
the exact commissioning proof to share its hash/inode/owner/mode and two-link
count before publication. This inspection did not read the proof itself;
deployment must verify it or stop.

Atomic replacement detaches only the live pathname and preserves the historical
proof. New and restored source files have one link. Recovery restores original
bytes, ownership and mode without rejoining the historical proof inode. A
changed proof holds recovery. No chmod/chown repair of the existing file or
historical cleanup is proposed. The main configuration mirror remains unchanged.

The [comparison](ntp-generic-comparison.md) maps all 33 reference graph groups;
the [candidate](../node/profiles/ntp/generic-parity.candidate.json) retains four
NTP readers and proposes 29 generic instances. The accepted node profile/settings and canonical master transport now mirror
the expanded production selection.

Native target qualification v2 is accepted: all 33 plugin instances (including
both NFS clients) and all 33 reference generic graph groups are represented.
Individual native work took 13.14 seconds; concurrent full workloads took
15.50/15.33/15.33 seconds within 25 seconds. Diskstats warm state/readback passed
after the genuine interval. Generic output was numeric; only the existing two
pending maintenance-job ages were unknown. Production daemon and both-family
direct TCP acceptance passed. Subsequent expanded observations accepted three
genuine cycles, all 280 selected RRDs and all 120 verified HTTPS responses. The
[candidate manifest](../node/profiles/ntp/generic-expansion.candidate-manifest.json)
binds expanded settings and separate compatible/final transport candidates to
the accepted capture. Guarded update/restoration is now implemented and locally
qualified. All three successors executed in order and are consumed; no replay. Node warm
full-protocol passes took 7.92/8.06 seconds after the genuine 305-second interval.
Finalization passed both expanded protocol families and existing dual-stack
HTTPS before/after. These checks do not accept expanded scheduled cycles/graphs.
Those separate [expanded observations](ntp-expanded-observation.md) have now
accepted the three genuine cycles and every selected graph family, including
device-specific diskstats. Producer/source-attribution/alert gates remain open.

## Sealed execution order

The operator confirmed the repository main-config stanza move was intentional
for readability, without changing operational directives. Preserve its layout.
Production keeps its pinned accepted bytes; byte-for-byte equality is not
claimed. This presentation difference does not block the expanded observations.
No main-config write is part of those reviews.

All three v2 reviews below were approved and executed successfully. Retain them
as immutable provenance; they authorize no replay or additional observation.

1. **Master compatibility:**
   [review](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-generic-compatible-20261021-v2/review.md)
   and [SHA-256](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-generic-compatible-20261021-v2/sealing.json:1).
2. **Node expansion:**
   [review](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-generic-node-20261021-v2/review.md)
   and [SHA-256](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-generic-node-20261021-v2/sealing.json:1).
3. **Master finalization:**
   [review](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-generic-expanded-20261021-v2/review.md)
   and [SHA-256](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-generic-expanded-20261021-v2/sealing.json:1).

Each bundle freezes `scripts/deploy_generic.py`, `scripts/update_generic.py`,
`scripts/probe_generic.py`, current repository dependencies and native/offline
qualification inputs. They reuse the existing transaction runner's exclusive
lock, detached apply worker and independent recovery timer. No implementation is
imported from an executed archive; prior archives supply data/provenance only.
Each later stage requires its predecessor's accepted/reconciled local result
and committed root-private transaction receipt on the appropriate host. Both
must match the predecessor's sealed digest. Approval may cover all three exact
bundles, but execution remains strictly ordered and stops on failure/uncertainty.

The [native qualification](/home/aaron/code/.local-evidence/homelab-ntp/current/munin-generic-update-qualification-20261021-v4/qualification.json)
passes nine actual isolated Munin/systemd cases: node and master commit,
ordinary node restoration, SIGKILL after node file publication, controller loss
after master preparation, foreign node link, foreign master file and preflight
drift and foreign commissioning-proof drift. Master cases start from real
two-link source/proof layouts and verify the retained proof remains separate
after publication/restoration. Real independent timers restored the uncommitted states; a delayed guard
did not undo a commit. Master source publication was visible through the
already-running native daemon without restart. Foreign bytes/inodes were held.
Cases use actual Trixie 2.0.76 package bytes and the native Bookworm master image,
networking disabled and workspace read-only. The native master source marker
tests publication visibility; they do not fabricate NTP data or accept production
timing/routing. Timer tests use 20 seconds; sealed production guards use 600.

Node restart preflight pins the package unit, the accepted original startup guard
and empty permit, and rejects extra effective drop-ins. Master changes replace
only the existing transport source; its settings, running daemon, main config,
Apache and CGI are preserved. After committed readback, the controller privately
scans and conditionally synchronizes the transport mirror, or the node settings
and expanded profile. Repository drift is held without undoing a production
commit. The original first installer remains consumed; no replay is introduced.

## Native qualification first

`scripts/qualify_generic.py` prepares a separate, one-use, hash-bound node
qualification. It reuses the repository's bounded SSH, protected reads and
continuity checks. Executed archives supply baseline data and provenance only;
runtime implementations come from repository sources, frozen into the new bundle.
No target contact occurs during sealing/checking.

Approved v1 contact verified pinned bytes and dependency presence/module loads,
then stopped before staging because the protected reader rejected /proc/net's
normal self/net alias. Its receipt is consumed. The corrected v2 reads the
current worker PID's concrete procfs path while preserving symlink rejection.
V2 executed successfully with a consumed receipt. No dependency installation,
production selection change, service restart or restoration was performed.

The review explicitly permits isolated staging and native plugin-state writes;
it is not labeled read-only. Native package source hashes, dependencies, NFS
proc3/proc4 markers, effective generic munin:munin identities, individual output,
305-second diskstats warm-up, three concurrent full workloads and subsequent
state readback are captured. Only the two established NTP readers retain root.
NFS without native capability is withheld with an explicit finding; software,
NFS and Wi-Fi are not enabled merely to produce graphs.

Every plugin receives isolated native state overrides. Config/fetch use actual
installed munin-run with an alternate service directory and settings; interface
symlink names preserve the native instance suffix. State is retained under the
operation's own directory. Existing default state directories must already
exist because native munin-run checks them before environment overrides.

Local native testing uses the actual approved 2.0.76-5 package bytes in a
disposable Trixie container with networking disabled. It checks native instance
naming, unprivileged diskstats, state isolation, concurrent atomic writes and
readback. It does not accept target hardware, privileges under the live daemon,
the target's 300-second samples, actual network polling or recovery.

Review every config/fetch field, unknown value, device selection and duration.
Record diskstats' empty first fetch as an explicit cold start; require complete
values after warm-up. Interface self-referencing CDEF expressions scale raw
counters and must retain those fetch requirements in the transport successor;
the existing checker incorrectly treats every CDEF as a computed-only field.
Require genuine readable native state after concurrent runs. Distinguish zero
activity from unsupported data. Do not silently discard NFS, thermal/frequency,
inactive interface or device measurements: document the native result and any
equivalent before finalizing the profile. A successful capture is not acceptance.

The 25-second native workload limit estimates the current transport budget;
the live daemon sandbox, TCP framing, master scheduling and actual IPv4/IPv6
source attribution remain deployment acceptance checks. Do not enlarge the
production deadline solely to make a local test pass.

## Bound deployment inputs

After qualification, render one exact selected profile and settings, recording
every capability disposition. Preserve existing graph/field names, the canonical
host and RRD history. Pin the existing production selection, settings, daemon
configuration, custom reader sources and master transport bytes before mutation.
Include all new source bytes, tests, backups, recovery commands, file ownership,
expected sets, acceptance commands and expiry in the respective sealed stages.

Use a guarded continuation for the existing node. The original installer and
correction/start approvals are consumed and cannot be replayed. Do not run
munin-node-configure to enable unrelated plugins. Package templates remain
package-owned; the continuation owns only its explicit new links and settings.

## Ordered transactions and restoration

1. **Master compatibility stage.** Install a reviewed transport successor that
   accepts exactly either the current nine-name set or the complete qualified
   expanded set. Reject partial sets, arbitrary supersets and missing NTP
   readers. Preserve full per-plugin config/fetch validation, both source-bound
   family checks and the measured deadline. Accept the old set before proceeding.
   Restore owned transport bytes on failure; leave the node unchanged. No master
   service restart, CGI refresh or main configuration change is submitted.
2. **Node expansion stage.** Back up and prove ownership of the current selection
   and settings, arm independent bounded recovery, then stop only munin-node for
   its finite update. Add only qualified links/settings; leave NTP/GPS, network,
   schedules and package state untouched. Validate native readers and privilege
   settings, restart munin-node, then accept its exact expanded list and complete
   config/fetch via the master over both families. Check NTP continuity before
   disarming recovery. An outage or failed sample must remain visible in evidence.
   On failure restore only owned additions/settings and restart/accept the old
   selection; the compatible master can still validate that old set.
   Diskstats' native state filename includes the connecting collector's source
   address. A local CLI fetch warms a different state file. Seed genuine native
   samples from the approved master over both source-bound families, allow a
   real 305-second interval, and validate complete warm protocol output before
   committing. Do not copy isolated qualification state into production or treat
   cold empty output as accepted transport. Size the node recovery/commit window
   to include this interval and measured polling time; the original installer's
   immediate health check is insufficient. Genuine scheduled samples remain a
   later acceptance gate even when these direct native reads pass.
3. **Master finalization stage.** Only after node expansion acceptance, narrow
   the transport successor to exactly the expanded set. Confirm source-bound
   checks and native master parsing before accepting. Its recovery baseline is
   the compatible old-or-expanded transport, which can validate the expanded
   node; restoring the original nine-only transport would break collection.
4. **Scheduled acceptance.** Observe three genuine collection cycles, fresh
   canonical RRD updates and every applicable new graph plus all NTP graphs over
   both HTTPS families. Review warmed diskstats device/overview samples and
   actual concurrent canonical/transport behavior. Do not fabricate runs or
   records. Reconcile accepted production configuration bytes to their repository
   mirrors; record authored paths, recovery state and remaining gates.

Each live target/stage requires its own exact hash-bound approval. Cross-host
atomicity is not assumed. If interrupted between stages, retain the last accepted
compatible state and document the exact resume point. Never restore a file whose
current bytes no longer match the transaction's authored bytes; hold for review.
Independent recovery must have qualified success/failure paths before sealing.
Existing native recovery machinery should be reused where its ownership and
deadline contracts cover this continuation.

## Remaining acceptance

Keep contacts disabled throughout these stages. Genuine maintenance-job records,
canonical TCP source attribution, native limits/contact transitions and downstream
delivery, client coverage, sustained storage growth/budget, persistence and final
observation remain separate requirements in the NTP readiness checklist. The
mandatory separate-host private ntpviz dashboard remains after j2 completion and
before the next NTPsec installation; its host is still undecided.

## Expanded observation reviews

Both approved node/producer and native-master observations executed successfully.
The [observation procedure](ntp-expanded-observation.md) covers all 56 accepted
j2 graph names plus master transport, genuine post-expansion cycles and fresh
RRDs/dual-stack graphs. Alerts remain disabled and no additional deployment is
included. Both receipts are consumed; later captures require new exact-hash approval.
