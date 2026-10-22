# Guarded native master commissioning

This stage installs the accepted j2 polling design with new contacts disabled.
It does not close scheduled collection, fresh j2 graphs, limit transitions or
delivery. The [design](../master/ntp-design.md) owns those requirements;
the [acceptance review](ntp-master-acceptance-review.md) retains the open gates.

## Inputs and approved scope

The [sealer/controller](../scripts/deploy_ntp_master.py) requires the successful
exact-production baseline retrieval, accepted Apache TLS provenance and a passing
native qualification manifest for every closed executable input. It pins current
production/repository config bytes, host/boot, complete package inventory,
NetworkManager/Apache/cron identity, installed native source and Apache vhost.
Keep the [accepted mirror](../master/configs/munin.conf) unchanged during preparation.

The [installer/restorer](../scripts/install_ntp_master.py) adds one transport
plugin, its root-owned settings and plugin link, and the preserving main-config
candidate. Effective include files, preexisting authored destinations, unsafe
ancestry or drift fail before live config changes. Preserve unrelated plugins,
existing node config, scheduler, RRDs, records and host/network/DNS/Apache policy.

The candidate removes only the stale cache socket directive, inserts transport
overrides into the existing master section and registers j2 once over IPv4.
Both new contact scopes are explicitly `none`. No contact command/helper,
success record, schedule or package is activated/created. The transport plugin
enforces munin:munin, checks all nine remote plugins over both explicit source-
bound families, and has a 25-second internal budget with a 60-second native limit.
Native config/fetch must require IPv4=1 and IPv6=1; absent mail evidence stays U.

## Activation, independent commit and CGI refresh

An exclusive root-private stage holds frozen sources and an immutable archive.
A detached systemd worker has a 300-second runtime cap; an independent 600-second
timer is armed first. The worker saves verified backups and durable publication
inode proofs before touching live names. It validates native parsing as munin,
restarts only the existing Munin-node, then exercises both installed CLI and real
served config/fetch. The explicit node name from its greeting is used for lists;
an unqualified `list` can select a different default host.

Long-running CGI programs load config before accepting requests. Refresh only
native HTML/graph CGI descendants of the accepted Apache master: validate exact
script, www-data UID, process start identity and ancestry; signal TERM through
pidfds and prove the old workers exited. Apache itself is neither restarted nor
reloaded. No kill-by-name or SIGKILL fallback is allowed. If no persistent native
CGI exists, subsequent ordinary CGI requests read current configuration normally.

The worker stops at `prepared`. The controller verifies existing HTML, CSS and
a real existing PNG over each master literal, with the approved hostname, CA and
leaf identity, before and after preparation. Only a successful independent check
permits commit under the same lock and disarms recovery. Existing graph checks
accept serving continuity; they do not establish new j2 freshness.

Worker/controller loss cannot commit. The independent timer restores an
uncommitted operation. This transient guard covers current-boot worker/controller
loss; reboot or power loss requires a fresh inspection and recovery review.

## Conditional restoration and evidence

Restore the main file only when its bytes and publication inode match the
authored candidate and its private backup matches the accepted baseline.
Remove only source/settings/link entries with proven authored identities.
Revalidate native parsing, restart the original node when needed, recycle only
native CGI workers and prove the original protocol/plugin set and protected
identities. Unrelated files and foreign drift are never overwritten. A mismatch
holds restoration with explicit errors; it is not reported as restored.

Keep private backups, source proofs, stage state and newly created empty source
directories. Never delete RRD/history or real success/submission records. A later
guard is a no-op for committed/restored state; committed rollback is a separate
review. An uncertain outcome permits one same-bundle read-only inspection within
expiry, not apply replay or blind retry.

After committed production readback, update the repository mirror only when it
still equals the approved baseline or already matches the candidate. Scan exact
bytes privately and verify the atomic import. Concurrent repository edits are
held rather than overwritten; production commitment and repository reconciliation
remain distinct results. The [configuration lifecycle](../master/configuration-lifecycle.md)
requires their agreement before reconciliation is complete.

## Qualification

Run offline tests with the scaffold check. Native validation is opt-in:

```bash
python3 -I -B Munin/tests/run_master_native.py \
    --evidence /absolute/private/new-evidence-directory \
    --cases success configured-failure prepared-failure foreign-config \
    foreign-link preflight-drift worker-loss controller-loss health-reject
```

Run this Podman wrapper outside the filesystem sandbox. It uses the recorded local
Bookworm image, network=none, isolated systemd, read-only source mounts and one
private evidence directory per case. Every invocation records image identity,
arguments, input hashes, complete log and terminal status. Changed mounted inputs
invalidate the result. Failed containers and logs remain for diagnosis.

Native setup runs real Munin 2.0.73, Apache/FastCGI, an actual local cache and one
ordinary native cycle to establish a genuine baseline. The fixture cache only
provides baseline access; production installs no cache daemon. Isolated remote
transport values are explicitly zero/U and never called production success.
Real native CGI responses, process identities, file/link publication, service
restart, existing RRD preservation and timed recovery exercise the actual path.
This qualification does not replace required live IPv4=1/IPv6=1 acceptance.
