# Kuma Pi APT maintenance ledger

**Next action:** Under W-003, reconcile the November 26 scheduled refresh and upgrade with the service results, updater log, package disposition, reboot requirement, dashboard and fresh monitor heartbeats. Confirm receipt if a report is generated.

[Plan and acceptance](PLAN.md) · [Operating procedure](../../uptime-kuma/docs/OPERATIONS.md#unattended-apt-updates)

| ID | State | Decision or closure condition |
| --- | --- | --- |
| W-001 | Resolved | November 25 read-only inspection verified both signed source files, four release identities, armhf foreign architecture, enabled stock timers, no installed updater, no reported holds, and list-only needrestart. The installed sendmail interface uses msmtp. |
| W-002 | Resolved | W-004 completed the installation after the first attempt stopped. Original scope: Install the three-package transaction, verify effective policy, dry run, schedules and HTTPS dashboard. The November 25 svmf backup passed its isolated restore. |
| W-003 | Open | Reconcile the first scheduled upgrade with AC-004. |
| W-004 | Resolved | Approved continuation completed once. AC-001 through AC-003 passed. |

The reviewed simulation installed unattended-upgrades, python3-dbus and python3-distro-info with zero removals or upgrades. The host reported 24 GiB free on root and 438 MiB on the boot filesystem. Admission conservatively requires 1 GiB and 128 MiB respectively. The two existing timer calendars have randomized delays; local drop-ins set the selected times with persistent catch-up. The approved maintenance scope includes normal change/error reports through the existing Mailrise route.

## W-002 installation review (consumed)

One attended first installation targets only j2-svpi3bmf. The launcher first reads today's backup metadata and restore journal on svmf and checks HTTPS from the workstation. It then runs Ansible with the admitted Pi host key and finishes with another HTTPS check. The playbook refreshes indexes and installs the reviewed three packages, tests the upgrade policy in dry-run mode and activates the two timer calendars. Persistent catch-up is enabled. Conditional recovery stops the timers, removes the new control files and restores the prior calendars after checking that automatic installation is off. Installed packages and private evidence remain available for review. No host reboot is requested.

From a private WSL shell, the exact command for one installation is:

```bash
cd /home/aaron/code/.local-evidence/uptime-kuma/apt-updates-HP39xohp &&
  echo 'de027b042e2bab088533cf0977afb6fe067d2db98029cfd1ee5d25ec48d389b4  INPUTS.sha256' | sha256sum -c - &&
  /bin/bash install
```

The private manifest binds the launcher, playbook, inventory, APT policy and known host key. Ansible syntax, YAML, Markdown, launcher syntax, ShellCheck, input readback and the working-tree secret scan passed. Aaron approved one attempt. See the execution result below.

## W-002 stopped before package installation

On November 25 the signed refresh completed. The retained simulation contained exactly the approved three packages, zero upgrades and zero removals. The admission expression required a comma after “to remove”; APT printed “and 40 not upgraded.” The shell exited before the installation command. The recovery task verified periodic upgrading was off and restarted both original timers. Readback found both timers and Kuma active, unattended-upgrades absent, and the fleet dashboard returning HTTP 200.

The original bundle and Pi evidence directory are retained. The source now checks the observed summary format and reports the summary on rejection. Local checks exercised the observed line and rejected changed install, upgrade and removal counts. W-004 carries the continuation. W-003 awaits successful installation.

## W-004 continuation for separate approval

One installation on j2-svpi3bmf uses the corrected APT simulation gate and a fresh root-private Pi evidence directory, `/var/backups/kuma-apt-before-w004`. Admission requires that directory to be absent. The launcher's only execution change from W-002 is the explicit Ansible state-directory override. The existing backup, HTTPS, host identity, package and timer checks run again. The permitted install set is unattended-upgrades, python3-dbus and python3-distro-info with zero upgrades or removals. Dry-run verification precedes timer activation. Conditional recovery restores the prior calendars and verifies that periodic upgrading is off before resuming the timers. Keep both attempts' evidence. W-003 covers the first natural run separately.

Exact command from WSL:

```bash
cd /home/aaron/code/.local-evidence/uptime-kuma/apt-updates-w004-532eSfJ8 &&
  echo 'eadf7711a3132b884c581abe91a8913df1ea1cc6cd96ed16d5a2e92deb91fa98  INPUTS.sha256' | sha256sum -c - &&
  /bin/bash install
```

The original manifest still verifies. The new manifest binds the corrected playbook, launcher, inventory, policy and known host key. Local launcher syntax, ShellCheck, Ansible syntax with the state override, repository YAML lint and manifest readback passed. Aaron approved one installation and conditional recovery.

## W-004 installation accepted, November 25

The manifest verified and the launcher exited 0. The backup and dashboard admission checks passed. The signed refresh, reviewed package installation, effective four-origin policy readback, unattended-upgrade dry run and hold comparison passed. Both timers were enabled and active. Their next elapses were November 26 at 03:15 CST for refresh and 03:30 CST for upgrades. Both loopback and workstation HTTPS dashboard checks returned 200. Conditional recovery was unused. The workstation receipt is `apt-updates-w004-532eSfJ8/run/install.log` under the private Kuma evidence root; the Pi retains the dry-run log in `/var/backups/kuma-apt-before-w004/`. AC-004 awaits natural execution.
