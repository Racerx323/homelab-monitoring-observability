# Initial Uptime Kuma deployment result

**Accepted November 12, 2026.** The Pi runs Kuma 2.5.9 on ARM64 with one administrator and an internal HTTPS dashboard. On November 23, host-specific Webmin retirement completed. The Caddy withdrawal preserved Kuma HTTP 200 over IPv4 and IPv6 on both proxies and the VIP. The retirement filesystem review closed with Kuma healthy.

The deployment manifest pins the image index. On the accepted host the ARM64 registry digest was `sha256:6be4ea6135b22947b463966ce115cc7725b1254ec47e892d3633620854556d7f` and the image configuration ID was `sha256:315dfadc88ca9be7ba59515578363871bda93f7989a8e406f162acf36c9b0037`.

## Acceptance results

| Plan criterion | Status | Observed result and evidence |
| --- | --- | --- |
| AC-001 Identity, OS, addresses, resources | Pass | Accepted platform/preflight and ARM64 runtime; required IPv4/ULA, storage and staged admission passed. Radio softblocks are accepted with existing services retained. |
| AC-002 Architecture and immutable runtime | Pass | Permanent architecture reconciled with accepted definitions; runtime image identities above and pinned backend inputs recorded. |
| AC-003 Persistent local data | Pass | Runtime reports local ext4, `/var/lib/uptime-kuma/data` mounted at `/app/data`, UID 1000 and one persistent administrator; restore/source recovery accepted. |
| AC-004 Internal dual-stack dashboard | Pass | Private authentication/WebSocket and passive acceptance plus DNS and normal-name IPv4/IPv6 HTTPS 200. |
| AC-005 Safe administration | Pass | One active administrator, authentication enabled, protected bootstrap and private login checks accepted; no credentials in this record. |
| AC-006 Startup/recovery and budget | Pass | Accepted reboot checkpoint, permanent startup state, native limits, combined scan sampling and source recovery. Final sampled minima 554968/566808 KiB; no observed OOM events. Empty-monitor workload only. |
| AC-007 Backup/restore | Pass | Consistent administrator-bearing archive, protected on/off-node copies and isolated pinned ARM64 restore accepted. Recurring scheduling was outside this installation. |
| AC-008 Preserve services/network policy | Pass | Scoped service/configuration preservation, required addresses/routes and radio softblocks passed through reboot/promotion. Retain radio services and defer timed RA renewal to the network owner. Renewal remains untested; its residual risk is accepted for this initial deployment. |
| AC-009 Excluded workload/actions | Pass | Counts at installation acceptance were zero monitors and zero notifications; no synthetic messages or unattended application upgrade activation in accepted operations. |
| AC-010 Operability | Pass | Initial-scope closeout accepted. |
| AC-011 Fleet foundation | Pass | Retained needrestart, mail and watchdog foundation accepted. |
| AC-012 Fleet notification transport | Pass | Mailrise default and owner consumer configuration accepted; greeting/QUIT only. No downstream message-delivery claim or provisioned Mailgun secret. |

## Operating boundary

The measured workload had zero monitors and zero notifications. The administrator-bearing backup and isolated restore passed. The [active-monitoring result](../2026-11-23-uptime-kuma-active-monitoring/RESULT.md) records the subsequent acceptance of populated backups, monitoring and downstream alert delivery. The [network owner](../../../homelab-network/host-network/uptime-kuma/README.md#router-advertisement-renewal) tracks timed RA renewal. The [operations guide](../../uptime-kuma/docs/OPERATIONS.md) covers ongoing administration.
