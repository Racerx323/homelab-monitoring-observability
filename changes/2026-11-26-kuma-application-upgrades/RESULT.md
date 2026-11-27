# Uptime Kuma application upgrade result

**Accepted, November 26, 2026.** The approved workstation playbook upgraded the Pi from 2.5.9 to 2.5.12 in one attempt. The application version and running image matched the [deployment manifest](../../uptime-kuma/manifests/deployment.yaml).

| Criterion | Outcome |
| --- | --- |
| AC-001 | Pass. The Pi discovered the newer stable ARM64 release. Aaron confirmed the labeled Apprise message on email, Discord and Pushover. Deduplication and delivery-failure handling passed locally. |
| AC-002 | Pass. The fresh pre-upgrade archive on svmf passed checksum, isolated SQLite restore and monitoring inventory comparison before the image switch. |
| AC-003 | Pass. The monitor and status-page inventories matched, including memberships and alert assignments. All enabled polling monitors supplied fresh completed heartbeats, with none recorded down. The workstation verified the HTTPS dashboard and published page `one`. |
| AC-004 | Not applicable to this live run. Acceptance passed. Conditional restoration of the matching image and data was exercised in local qualification. |

The private candidate, terminal receipt and Ansible log are in `application-upgrade.7YSNGMrA` under the Kuma evidence directory. The corresponding svmf archive is `/var/backups/uptime-kuma/upgrade-a6245ade292b4d28a0f70894fa16b96f.tar`. It was retained through the first successful post-upgrade nightly restore.

On November 27 the svmf timer triggered at 02:30:46 CST. At 02:31:12 the receiver published the fresh 9,021,440-byte `2026-11-27.tar` after isolated SQLite restore and integrity checks. The receipt counted 22 monitors, one status page, six groups, 22 group memberships and 21 notification assignments. The pre-upgrade archive was still present at verification. Aaron then authorized deletion. The Pi and svmf archives matched the verified backup checksum before removal. Readback confirmed removal of both upgrade archives and the Pi’s saved predecessor Quadlet. The November 27 daily archive remained present on svmf.
