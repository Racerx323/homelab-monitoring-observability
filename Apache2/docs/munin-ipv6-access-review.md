# Munin Apache IPv6 access review

Updated October 20, 2026 after approved deployment and sampled acceptance.

## Observed baseline

The approved `svmf-apache-qualification-20261020-v1` capture inspected the
enabled vhost on `svmf.local.theama.co`. Its bytes matched the supplied file,
SHA-256 `6896785bfd538f136a4ba25c8ce5aac7a0cd9918cd81717f32d4482d66eeb40e`.
Apache owns TCP 80/443 and its service identity stayed unchanged during capture.
Parsing disk files does not establish exactly which bytes the daemon loaded.

Verified HTTPS root and sampled HTML returned 200 through IPv4 and IPv6.
`/munin/` returned 403 through both. `/static/style-new.css` returned IPv4 200
and IPv6 403. Four `Require ip` lists cover private IPv4 ranges and IPv6 loopback,
with no ULA client range. The stylesheet result is consistent with that omission;
no full authorization trace or graph request was performed.

The subsequent approved `svmf-graph-qualification-20261020-v1` completed eight
verified HTTPS GETs. Domain/node HTML returned 200 on both families. The sampled
stylesheet and daily graph returned IPv4 200 and IPv6 403. IPv4 returned a valid
PNG with the expected content type at
`/munin-cgi/munin-cgi-graph/J1-SVMF/J1-SVMF/apache_accesses-day.png`.
TLS verification passed throughout. Its receipt is consumed; graph freshness
remains unproven. No Apache change was performed by either diagnostic.

## Accepted minimal configuration

The [candidate vhost](../configs/001-munin.theama.co-ssl.conf) adds only
`fd36:5aa8:6971:1::/64` to each of the four existing IP lists: core static files,
generated web files, `/munin/` and graph CGI. This is the LAN prefix supplied by
the operator and contains the observed management-client ULA. It deliberately
does not authorize every ULA prefix or all IPv6 clients. Prefix membership does
not establish a dedicated management subnet; approving deployment must explicitly
accept access from this LAN /64.

Existing IPv4 and loopback rules, TLS, CGI handlers and rewrites retain their
current configuration. The CGI directory's existing `Require all granted` remains;
this patch does not establish a uniform dashboard-wide access policy. Do not
attribute the IPv4 `/munin/` failure to the missing ULA rule. Use the already
working root `/` as the candidate canonical dashboard landing page rather than
adding unrelated path rewrites to this change.

Apache supports IPv6 CIDRs in `Require ip`. Directory and URL sections may merge
differently, so acceptance must test HTML, stylesheet and actual graph requests
after the complete configuration is parsed. A four-line ACL review alone cannot
prove runtime access or deny behavior. Refer to the official Apache 2.4
`mod_authz_host` and configuration-sections documentation for these semantics.

## Qualified deployment review

Targeted graph-path inspection is complete. Reuse the retained exact URLs and
both-family results; do not repeat discovery or replay the consumed receipt.
Preserve both completed captures as the baseline for deployment qualification.

The [Apache-owned transaction](acl-deployment.md) now has eight passing offline
contracts and eight native Apache 2.4.68/FastCGI/systemd transaction scenarios.
Commit passed; missing confirmation, worker loss, rejected health, failed
configuration test and failed reload restored the original. Foreign drift held
without overwrite, and preflight drift stopped before replacement. An additional
real-parser check rejected invalid configuration and failed graceful reload,
preserved dual-stack root serving and then reloaded the restored valid file.

Sealed `svmf-apache-acl-20261020-v1`, archive SHA-256
`23aafda870c8cf1dc9863c48c5402ed8aa8306a06838c5d081f40760e0800941`,
pins the expected original hash, candidate, target/boot/service identity, included
files, public trust and host key. Its detached worker preserves actual protected
owner/group/mode, backups, atomic replacement, full configuration tests and the
qualified graceful reload. An independent recovery timer covers worker loss;
exact dual-stack HTML/CSS/PNG proof is required before commit. See the runbook
for restore-versus-hold behavior and post-commit readback limits.

The native fixtures are Debian 12 amd64 with synthetic certificates/content;
production preflight subsequently qualified the installed reload command and
unchanged identities before writing. The exact-hash-approved live transaction
committed and final verified HTTPS HTML/CSS/PNG passed through both original
families. The accepted target hash is
`555551c423e879d6b0ea5706807f5bb7a02c6238293e7509527ecf6d2004091f`,
root:root 0644, with original backup/state retained. No restoration was needed;
the consumed operation must not replay. Its guard's later no-op is unobserved.

Every-client access, graph freshness, future static ULA and DNS AAAA acceptance
remain open. Update and requalify the network wrapper's HTTPS health contract,
then seal a successor static-network bundle. DNS and Munin monitoring follow
their own approved stages.
