# Initial Uptime Kuma installation

Install the service on `j2-svpi3bmf` with persistent local storage, a private administrator, the fleet host foundation and a dual-stack HTTPS dashboard. The installation scope ends at an operable empty service. The [installation procedure](../../uptime-kuma/docs/OPERATIONS.md#initial-installation) is the entry point for another host.

## Acceptance criteria

| ID | Required observed outcome | Verification method and evidence required |
| --- | --- | --- |
| AC-001 | Target identity, Debian 13 ARM64, supplied network addresses and adequate resources are verified. | Bounded host baseline and reviewed resource/storage budget; discrepancies resolved explicitly. |
| AC-002 | One agreed architecture and a reproducible, immutable runtime definition exist. | Architecture review, pinned upstream release and ARM64 digest, local parser/policy tests; no mutable-tag-only deployment. |
| AC-003 | The service uses local persistent data with correct ownership and a suitable filesystem. | Target mount/ownership observations, service write/read check and persistence after restart; no NFS data directory. |
| AC-004 | The internal dashboard works at `https://uptime.local.theama.co` over both intended address families. | Owning DNS/Caddy validation, trusted TLS, HTTP and WebSocket/application checks from the intended client path. |
| AC-005 | Initial administration is safely established and protected. | Controlled bootstrap, authenticated dashboard, unauthenticated access behavior and absence of public setup exposure; no secrets in tracked artifacts. |
| AC-006 | Startup and recovery work within a measured resource budget on this Pi. | Actual systemd/Quadlet acceptance, bounded restart/reboot test where approved, memory/storage observations and absence of OOM/restart loops. |
| AC-007 | Backup and restore are documented and qualified without corrupting the active database. | Consistent full data-directory backup and isolated restore check; limitations and off-node backup destination explicit. |
| AC-008 | Existing services, network policy and unrelated configuration are preserved. | Before/after comparison limited to affected state, conflict checks and rollback/residue verification. |
| AC-009 | No Uptime Kuma monitors/alerts, synthetic test notifications or unattended application upgrades are activated. | Configuration review and target application/service observations; later scope remains separate. |
| AC-010 | The deployment is operable and all findings have a durable disposition. | Permanent operations/architecture references, reconciled ledger and criterion-by-criterion result; no unsupported claim of live acceptance. |
| AC-011 | Retain fleet needrestart, msmtp and watchdog coverage. | Verify the scheduled scan, Mailrise default and vendor watchdog policy. |
| AC-012 | Host notifications use existing fleet Mailrise/Apprise, with Mailrise selected by default in msmtp. | Inspect effective account/aliases and consumer invocation; qualify SMTP greeting/QUIT without sending. Preserve Mailgun for explicit external email. Real test messages and downstream delivery require separately reviewed content; do not claim receipt from configuration or SMTP connectivity. |

## Recovery

Before changing boot or network settings, preserve the original boot file off-node, confirm console access and use the network owner’s checkpoint. If the host does not return, recover the original configuration from the console. Preserve existing data and keep startup contained after failed bootstrap or backend promotion. Restore data only after qualifying an isolated restore. The Caddy and DNS owners govern withdrawal or reversal of their respective changes.

See the [accepted result](RESULT.md) for the delivered configuration and remaining operational limits.
