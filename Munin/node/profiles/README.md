# Node profiles

The Caddy profile contains a `plugins.list` with one custom plugin name per line.
The NTP candidate uses `profile.json` to distinguish package-provided plugins,
custom plugins and root-only readers. Each has a README describing prerequisites
and status. A custom plugin
name must match both a source filename under `node/plugins/<app>/` and a stanza
in the associated `node/plugin-conf.d/<profile>.conf`. An installer must
reject a missing, duplicate, or unapproved plugin, and must use a separate
inventory selection rather than selecting profiles automatically.

`caddy-ha` remains deferred. [ntp](ntp/README.md) is a locally qualified candidate,
selected for j2-svntp1 in server inventory, with no accepted live installation
or approved installation bundle. `base` remains
reserved. Profile existence never selects a host or authorizes deployment.
