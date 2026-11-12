# Uptime Kuma

This repository owns the Uptime Kuma application and file store for `j2-svpi3bmf`. The internal dashboard name
`uptime.local.theama.co` is agreed. Service foundation and the guarded dual-stack
backend were accepted November 11, 2026; the Caddy route and private HTTPS application acceptance are accepted, while DNS
remains pending. Monitors and alerts remain unconfigured.

- [Governing architecture](docs/ARCHITECTURE.md)
- [Repeatable operating procedures](docs/OPERATIONS.md)
- [Initial deployment plan](../changes/2026-11-09-uptime-kuma/PLAN.md)
- [Current work and findings](../changes/2026-11-09-uptime-kuma/WORK.md)

The architecture holds enduring design, the change record holds this transition,
and the operating procedure holds repeatable administration. The host foundation includes fleet-managed needrestart, Webmin, msmtp and
watchdog coverage. Notifications use shared fleet Apprise API/Mailrise; Uptime
Kuma monitors and alert activation remain later work. Earlier installation operations are consumed. Use the change ledger for the
current exact operation and approval state; definitions alone grant no live authority.

`ansible/diagnose-network.yaml` defines a bounded per-family diagnostic of an
existing contained installation. It saves observations before shutdown and leaves
persistent start guards requiring an ephemeral permit, so generated units cannot
start unattended afterward. See the [operating procedure](docs/OPERATIONS.md)
for its evidence and containment boundaries. No diagnostic is live-approved by
this README.

The proposed IPv6 loopback correction uses the owner systemd socket/proxy
[templates](ansible/templates/uptime-kuma-loopback.socket.j2) and the existing
bounded observation/containment lifecycle through
[correct-loopback.yaml](ansible/correct-loopback.yaml). The current ledger binds
any live authority; previous diagnostics cannot be replayed.

The [remaining-deployment coordinator](ansible/remaining-deployment.yaml) resumes
an installed, corrected and contained baseline. It imports the existing service
acceptance tasks, preserves guard files, and bounds startup across one reboot
and controller loss. Its status and exact authorization remain in the ledger.
