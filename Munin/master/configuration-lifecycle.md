# Munin master configuration lifecycle

Munin is a repository-managed production service. The accepted configuration
on svmf is the initial known-good baseline. Its exact bytes are mirrored in
[configs/munin.conf](configs/munin.conf); keep them synchronized after every
accepted change to `/etc/munin/munin.conf`. Preserve existing production host
names and their RRD history. Do not substitute a cleaned-up approximation.

## Baseline import and drift checks

An approved read-only `master-baseline` capture exports the exact config into
owner-private evidence. It pins the previously accepted production SHA-256;
unexpected drift stops export for review. The controller's exclusive receipt,
successful capture, target/spec identity and returned file hash must all match.
No credentials or raw include files are imported into the repository.

Use the [baseline synchronizer](../scripts/sync_master_baseline.py) after that
capture succeeds. It performs no target contact. `check` compares repository
bytes and exits 2 on drift. `import` first scans the exact payload privately
with Gitleaks, rejects destination symlinks and concurrent repository changes,
then atomically replaces the baseline and verifies its bytes.

```bash
python3 -I -B Munin/scripts/sync_master_baseline.py check \
    --directory APPROVED_CAPTURE --sha256 APPROVED_ARCHIVE_SHA256
python3 -I -B Munin/scripts/sync_master_baseline.py import \
    --directory APPROVED_CAPTURE --sha256 APPROVED_ARCHIVE_SHA256
```

Retain the capture timestamp and checksum in operation evidence/history. A local
check proves agreement with that capture, not current live state indefinitely.
No background target access or automatic production overwrite is introduced.

## Reviewed changes and acceptance

Keep deployment candidates separate from the accepted mirror. Pin both the
current production hash and candidate bytes in each sealed operation. Stop on
drift before mutation. Preserve unrelated node sections, native scheduler,
Apache service policy and actual success/submission records.

After successful deployment, require exact installed readback against candidate
bytes, then update the canonical repository mirror from that accepted readback.
After accepted restoration, retain the restored baseline instead. An operation
is not reconciled until the accepted production and repository hashes agree.
Repository changes do not authorize deployment; a live result does not authorize
unreviewed edits. Never reseal or modify consumed execution inputs.

## Cache and commissioning candidates

Keep cache policy separate from baseline synchronization. The proposed cache
resolution is direct-RRD operation, using Munin's native empty socket default.
The [candidate renderer](../scripts/qualify_master.py) removes only the reviewed
stale socket directive, preserves unrelated bytes and keeps new contacts `none`.
Do not install a cache daemon to satisfy a stale configuration entry.

Validate that candidate with installed native parser/update/graph code, qualify
actual CGI refresh and node restart/restoration, then seal deployment. Importing
production does not deploy this candidate. Exact message approvals, genuine
scheduled records, native scheduled polling/fresh graphs and delivered alerts
remain independent acceptance gates.
