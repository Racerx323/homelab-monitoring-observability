# Homelab monitoring and observability

This repository is the configuration owner for the fleet Munin deployment. It is
currently a scaffold, not an installable monitoring stack. There is no Compose
deployment, Prometheus, Grafana, or Alertmanager configuration here.

The [Munin component](Munin/README.md) contains node plugin source, plugin
settings, candidate profiles, and the master-configuration contract. The
`Apache2/` directory owns the supplied Munin vhost and its
[IPv6 access review](Apache2/docs/munin-ipv6-access-review.md). Its four ULA ACL
additions were deployed through an approved
[sealed Apache transaction](Apache2/docs/acl-deployment.md), with sampled
IPv4/IPv6 HTML/CSS/PNG acceptance. That consumed approval grants no further
live authority; static networking, DNS and fleet monitoring remain separate.

No repository file currently selects a host or authorizes a live Munin change.
