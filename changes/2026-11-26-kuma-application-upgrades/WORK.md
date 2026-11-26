# Application upgrade work ledger

**Next action:** Retain the upgrade backup through the rollback window. Review cleanup after a later successful nightly restore. See [result](RESULT.md).

[PLAN.md](PLAN.md) owns acceptance and recovery. This ledger owns status and next actions. Record live outcomes in RESULT.md when available.

| ID | State | Work and closure |
| --- | --- | --- |
| W-001 | Resolved | Implemented discovery, notification, isolated restore, upgrade and recovery. Six offline tests passed against a populated database with simulated service and transport boundaries. Public registry lookup of 2.5.9 matched both accepted image digests. Both playbooks passed syntax checks. |
| W-002 | Resolved | November 26 approved installation completed once. All three installed files matched reviewed hashes. Discovery passed and Apprise returned HTTP 200 for the labeled confirmation. Timer enabled and active; next trigger November 30 at 09:25:53 CST. Aaron confirmed receipt on email, Discord and Pushover. Private receipt directory `release-check-jCeN9U2m`. |
| W-003 | Resolved | Aaron approved one attempt. The playbook accepted 2.5.12 and reconciled the manifest. |
| W-004 | Resolved | Discord showed the original confirmation as a dense block. The local revision uses fleet plain-text sections and bullets, keeps the digest in the journal and places the release URL on a separate line for Discord previews, including delivery tests. November 26: six tests passed, the approved revision was installed and its hash verified, and Apprise accepted one labeled confirmation. Timer active and enabled. Aaron confirmed delivery to email, Discord and Pushover. The supplied Discord receipt shows the section headings, version bullets and GitHub release preview. Private receipt: `check-format-dlM8tipq`. |

## W-003 release review and candidate

[2.5.10](https://github.com/louislam/uptime-kuma/releases/tag/2.5.10) updates Node.js in the container and fixes the embedded MariaDB password reset. [2.5.11](https://github.com/louislam/uptime-kuma/releases/tag/2.5.11) updates dependencies and fixes an admin-only remote-code-execution issue. [2.5.12](https://github.com/louislam/uptime-kuma/releases/tag/2.5.12) sandboxes JSONata and updates dependencies. The [tag comparison](https://github.com/louislam/uptime-kuma/compare/2.5.9...2.5.12) includes no database migration files; the database shutdown change is conditional on embedded MariaDB. No intermediate release or manual SQLite migration is prescribed. The reported fleet DNS, HTTPS, NTP, host and notification checks retain the usual post-start heartbeat verification.

Workstation preparation passed for Linux ARM64 slim-rootless. Review candidate `application-upgrade.7YSNGMrA/candidate.json` in private Kuma evidence, SHA-256 `ff88670bc6894c45e7ad8ced67fc7ac11544aaca750887e4dde4078db5a038b8`. The image digest matches the delivered alert. One live attempt would stop Kuma for the backup, verify the populated off-node restore on svmf, switch the image on the Pi and check the running version, monitor heartbeats and published pages. Failure after switching restores the matching image and data. The [upgrade procedure](../../uptime-kuma/docs/OPERATIONS.md#prepare-an-application-upgrade) defines the apply command and prerequisites. The single approval was consumed. The controller exited 0 with an accepted receipt.
