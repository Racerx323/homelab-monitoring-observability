# Uptime Kuma application lifecycle

Prepare a repeatable upgrade for the installed ARM64 service and a weekly release alert. Each release requires one approval covering its backup, upgrade, acceptance and conditional rollback. The checker has separate installation and delivery acceptance.

| ID | Acceptance |
| --- | --- |
| AC-001 | Detect a newer stable release with a matching ARM64 image, deduplicate successful fleet Apprise notifications and retry failed delivery. |
| AC-002 | Admit the exact candidate and installed predecessor, preserve an off-node isolated restore and compare populated monitors and status pages before switching. |
| AC-003 | Verify the running image, application version, pages, memberships and fresh completed polling heartbeats. |
| AC-004 | On failure restore the prior Quadlet and matching data. Verify predecessor identity, inventory, pages and heartbeats. |

Keep private archives on the Pi and svmf. Use the [operations guide](../../uptime-kuma/docs/OPERATIONS.md#application-release-checks-and-upgrades) for commands.
