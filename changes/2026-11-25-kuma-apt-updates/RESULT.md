# Kuma Pi unattended APT updates

**Accepted November 26, 2026.** The [work ledger](WORK.md) records the W-004 installation, first scheduled update, notification receipt, camera-package review and operator-approved reboot.

| Criterion | Result | Evidence |
| --- | --- | --- |
| AC-001 | Pass | Verified Pi admission, off-node populated backup and three-package installation. |
| AC-002 | Pass | Read back four allowed release identities, manual reboot policy and mail settings. Native dry run passed. |
| AC-003 | Pass | Both timers enabled and waiting on the accepted daily calendars. Dashboard recovered. |
| AC-004 | Pass | First scheduled transaction succeeded and the operator received the report. Following a manual reboot, all 22 monitors produced fresh UP heartbeats and the list-only restart scan was clean. |

Four camera updates require a library replacement and remain outside the automatic transaction. Review that package change separately if needed.
