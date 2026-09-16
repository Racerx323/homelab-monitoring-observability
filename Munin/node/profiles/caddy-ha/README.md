# Caddy HA candidate profile

Status: deferred; no host has opted in. This profile is retained because the
source now matches the Caddy component's service names, listener addresses,
certificate path, sync paths, and loopback metrics endpoint. Obsolete VRRP
state-file, IPv4 peer, and failure-marker probes were removed; VIP ownership is
measured directly instead.

`plugins.list` is the complete selection. Its settings are in
`../../plugin-conf.d/caddy-ha.conf`. The scripts remain uninstalled. Before
acceptance, confirm the metrics schema and permissions on each Caddy node,
review the root-running sync plugin for least privilege, test with
`munin-run`, then verify polling on the master. Caddy deployment completion does
not imply Munin deployment completion.
