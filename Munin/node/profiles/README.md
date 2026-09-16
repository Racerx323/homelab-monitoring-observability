# Node profiles

Each profile directory contains a `plugins.list` with one custom plugin name
per line and a `README.md` describing its prerequisites and status. The plugin
name must match both a source filename under `node/plugins/<app>/` and a stanza
in the associated `node/plugin-conf.d/<profile>.conf`. A future installer must
reject a missing, duplicate, or unapproved plugin, and must use a separate
inventory selection rather than selecting profiles automatically.

`caddy-ha` is a deferred candidate. `base` and `ntp` are reserved concepts, not
deployable profiles: package-provided baseline plugins and NTP-specific metrics
have not yet been selected or validated. Do not create empty selection lists to
make them appear implemented.
