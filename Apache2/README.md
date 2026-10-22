# Munin Apache component

This component owns the [Munin vhost](configs/001-munin.theama.co-ssl.conf),
its [minimal IPv6 access proposal](docs/munin-ipv6-access-review.md) and the
[sealed deployment workflow](docs/acl-deployment.md). The four LAN ULA /64
additions were deployed and sampled dual-stack HTML/CSS/PNG access accepted
under `svmf-apache-acl-20261020-v1`. The consumed approval is not reusable.

[deploy_acl.py](scripts/deploy_acl.py) is the controller and detached target
transaction. [Offline contracts](tests/test_deploy_acl.py) test proof validation
and recovery boundaries. The [native fixture](tests/native_acl.py) uses real
Apache, FastCGI, SSH and systemd in a Podman container with external networking
disabled. Its synthetic certificate/content and loopback LAN addresses do not
establish production or every-client acceptance.

Before a live execution, qualify the current executable bytes, pin all inputs
into a new bundle and obtain approval for its exact SHA-256. Production Apache
changes, static host networking, DNS and Munin registration remain separate
stages. Do not replay consumed captures or installers.
