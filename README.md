# Homelab monitoring and observability

This repository is the configuration owner for the fleet Munin deployment. It is
currently a scaffold, not an installable monitoring stack. There is no Compose
deployment, Prometheus, Grafana, or Alertmanager configuration here.

The [Munin component](Munin/README.md) contains node plugin source, plugin
settings, candidate profiles, and the master-configuration contract. The
`Apache2/` directory is an empty placeholder; it has no deployment contract.

No repository file currently selects a host or authorizes a live Munin change.
