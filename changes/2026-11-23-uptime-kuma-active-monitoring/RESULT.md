# Active monitoring result

**Accepted November 25, 2026.** The [work ledger](WORK.md) records the observations, operator confirmations and private receipt locations.

| Criterion | Outcome | Evidence |
| --- | --- | --- |
| AC-001 | Pass | The stored inventory and published page agreed on eight service monitors, six host checks and the external heartbeat. Aaron accepted the public membership. |
| AC-002 | Pass | Across 13 samples during normal polling, all dashboard probes returned HTTP 200. Kuma recorded zero restarts or memory pressure events. This window establishes short-term headroom only. |
| AC-003 | Pass | Aaron received the controlled DOWN and UP notifications on Discord, email and Pushover. The independent heartbeat also delivered missed-check and recovery emails. |
| AC-004 | Pass | The operations guide records ownership and maintenance. The November 24 attended restore matched source rows. The November 25 scheduled restore matched the populated counts and the dashboard returned HTTP 200. |

The [operations guide](../../uptime-kuma/docs/OPERATIONS.md#nightly-populated-backup) covers the nightly off-node backup. Aaron deferred automated recurring notification-delivery tests and will repeat the delivery check after alert-route changes.
