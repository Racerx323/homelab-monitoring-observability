# Munin fleet component

This directory owns Munin configuration for the fleet. Application repositories
may specify desired measurements and host requirements, but must not keep a
second deployable copy of a Munin plugin, plugin setting, or master entry.

## Layout and selection

- `node/plugins/<app>/`: custom plugin source. Source is not enabled by its
  presence in this directory.
- `node/plugin-conf.d/`: plugin user, group, and environment settings.
- `node/profiles/`: explicit plugin selections and their settings. A profile is
  a definition, not a host assignment.
- `master/`: master-side node registration contract; no fleet entries are
  accepted yet.
- `tests/`: repository-only checks for profile completeness and plugin output.

Host inventory selects a profile explicitly; this component defines what that
profile installs. Do not infer selection from a hostname or copy every plugin
onto every node. The Caddy profile is a deferred candidate. There is no
accepted base or NTP profile yet; those require a host/package and metrics
review before definition. No hosts are selected in this repository.

When a deployment workflow is approved, it should install custom plugin source
as executable files under `/usr/local/munin/lib/plugins`, link only the selected
names into `/etc/munin/plugins`, install the selected settings into
`/etc/munin/plugin-conf.d`, and register approved nodes in the master's
`/etc/munin/munin.conf`. Package-provided plugins remain package-owned. Record
exact host/profile selection and installed-file readback in inventory and
operation evidence; do not treat this candidate layout as an installer.

Before activating a profile, review `munin-node-configure --suggest`, test each
selected plugin with `munin-run <name> config` and `munin-run <name>`, confirm
the node's master allowlist and TCP 4949 reachability, then confirm the approved
master polls the node. Verify privilege and file access for each plugin. Caddy
specifically needs an on-host metrics endpoint and certificate read access;
these have not been live-validated for Munin. Install and rollback one node at a
time, with master registration only after node validation.

Run `bash Munin/tests/validate-scaffold.sh` for local repository validation.
