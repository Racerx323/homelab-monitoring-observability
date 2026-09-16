#!/usr/bin/env bash
set -euo pipefail

munin_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
plugin_root=$munin_root/node/plugins/caddy
profile_root=$munin_root/node/profiles/caddy-ha
settings=$munin_root/node/plugin-conf.d/caddy-ha.conf

[[ -f "$settings" && -f "$profile_root/plugins.list" ]]

declare -A selected=()
while IFS= read -r plugin || [[ -n "$plugin" ]]; do
    [[ "$plugin" =~ ^[a-z][a-z0-9_]*$ ]]
    [[ ! -v selected[$plugin] ]]
    selected[$plugin]=1
    [[ -f "$plugin_root/$plugin" && -x "$plugin_root/$plugin" ]]
    [[ "$(grep -Fxc "[$plugin]" "$settings")" -eq 1 ]]
    bash -n "$plugin_root/$plugin"
    "$plugin_root/$plugin" config | grep -Fq 'graph_title '
done <"$profile_root/plugins.list"

[[ ${#selected[@]} -eq 4 ]]
for plugin in "$plugin_root"/*; do
    [[ -v selected[${plugin##*/}] ]]
done
[[ "$(grep -Ec '^\[[a-z][a-z0-9_]*\]$' "$settings")" -eq ${#selected[@]} ]]
if grep -Eq 'vrrp-state|NETWORK_INTERFACE|PEER_IPV4|caddy-ha-notify' \
    "$plugin_root"/*; then
    exit 1
fi
if "$plugin_root/caddy_health" config | grep -Fq 'master.label'; then
    exit 1
fi
if "$plugin_root/lsyncd_caddy" config | grep -Eq 'reachable.label|failures.label'; then
    exit 1
fi

metrics="file://$munin_root/tests/fixtures/caddy-metrics.prom"
output=$(metrics_url=$metrics "$plugin_root/caddy_requests")
for expected in \
    'requests.value 12' 'errors.value 1' 'responses_2xx.value 10' \
    'responses_3xx.value 0' 'responses_4xx.value 2' \
    'responses_5xx.value 0' 'latency_ms.value 50.000'; do
    grep -Fxq "$expected" <<<"$output"
done

failed_output=$(metrics_url=file:///nonexistent/munin-metrics.prom \
    "$plugin_root/caddy_requests")
grep -Fxq 'requests.value U' <<<"$failed_output"
grep -Fxq 'latency_ms.value U' <<<"$failed_output"

printf 'Munin scaffold validation passed\n'
