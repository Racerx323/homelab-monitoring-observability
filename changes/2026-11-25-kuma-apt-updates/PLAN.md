# Kuma Pi unattended APT updates

Install native unattended updates on j2-svpi3bmf. The signed sources in debian.sources and raspi.sources cover Debian trixie, trixie-updates, trixie-security and Raspberry Pi Foundation trixie for arm64 and armhf. Aaron selected daily maintenance and manual reboots. Keep the existing package holds, signing keys, fleet mail, guarded 05:30 needrestart scan and pinned Kuma image.

| Acceptance | Evidence |
| --- | --- |
| AC-001 | Verify a recent off-node backup, Pi identity, APT health, space, dashboard and reviewed installation transaction. |
| AC-002 | Read back all four allowed releases, reporting and manual-reboot policy. Run the native dry run before resuming timers. |
| AC-003 | Verify enabled, active timers and next refresh at 03:15 and upgrade at 03:30 America/Chicago. Verify dashboard recovery. |
| AC-004 | Read the first natural trigger, APT service result and updater log. Record package disposition, reboot requirement, dashboard availability and fresh monitor heartbeats. Confirm delivery if a report was generated. After a no-op, check the first actual transaction separately. |

Use the [Pi-only playbook](../../uptime-kuma/ansible/apt-updates.yaml). An installation failure withdraws the new settings, checks that periodic upgrading is off and restores the original timers. Preserve installed packages and logs. If a package transaction is active, allow it to finish. Package-specific recovery and host reboot are separate operations.
