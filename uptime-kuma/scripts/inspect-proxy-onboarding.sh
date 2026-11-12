#!/usr/bin/env bash
# Read-only readiness; execution requires the exact scope recorded in WORK.md.
set -Eeuo pipefail
set +x
umask 077
export PATH=/usr/bin:/bin

if [[ $# != 1 || $1 != /home/aaron/code/.local-evidence/uptime-kuma/*/execution ]]; then
    printf 'Supply a new private uptime-kuma evidence directory ending in /execution.\n' >&2
    exit 2
fi
readonly inspection_output=$1
# Exclusive creation makes the reviewed evidence location single-use.
mkdir -m 0700 -- "$inspection_output"
readonly inspection_payload=$inspection_output/remote.sh
cat >"$inspection_payload" <<'REMOTE'
set -Eeuo pipefail
set +x
export PATH=/usr/bin:/bin
date -u +%FT%TZ
hostname
release=$(readlink -e /etc/caddy/current)
[[ $release == /etc/caddy/releases/* && -d $release ]]
printf 'release=%s\n' "$release"
sha256sum "$release/manifest.sha256"
for certificate in leaf.pem fullchain.pem; do
    cert_path=$release/tls/$certificate
    [[ -f $cert_path && ! -L $cert_path ]]
    printf 'certificate=%s\n' "$certificate"
    timeout 5 openssl x509 -in "$cert_path" -noout -subject -issuer -dates \
        -ext subjectAltName -fingerprint -sha256
    timeout 5 openssl x509 -in "$cert_path" -noout -checkhost uptime.local.theama.co
    timeout 5 openssl x509 -in "$cert_path" -noout -checkend 0
done
timeout 10 systemctl show caddy.service keepalived.service \
    caddy-pihole-web-health.service caddy-sync-health.service \
    caddy-cert-expiry.service caddy-apprise-worker.service \
    --property=Id,LoadState,ActiveState,SubState,Result,FragmentPath,TimeoutStartUSec
timeout 10 systemctl show caddy-pihole-web-health.timer caddy-sync-health.timer \
    caddy-cert-expiry.timer caddy-apprise-worker.timer \
    --property=Id,LoadState,ActiveState,SubState,TimersMonotonic,TimersCalendar,AccuracyUSec,RandomizedDelayUSec
test "$(readlink -e /etc/caddy/current)" = "$release"
date -u +%FT%TZ
REMOTE
chmod 0600 "$inspection_payload"
sha256sum "$0" "$inspection_payload" >"$inspection_output/inputs.sha256"
date -u +%FT%TZ >"$inspection_output/started-at"
for inspection_node in 53 54; do
    inspection_status=0
    timeout --signal=TERM --kill-after=5s 90s \
        ssh -T -o BatchMode=yes -o StrictHostKeyChecking=yes \
        -o ConnectTimeout=10 -o ConnectionAttempts=1 \
        -o ServerAliveInterval=10 -o ServerAliveCountMax=2 \
        "pi@10.1.0.$inspection_node" \
        'sudo -n timeout --signal=TERM --kill-after=5s 70s /bin/bash -s' \
        <"$inspection_payload" \
        >"$inspection_output/node-$inspection_node.stdout" \
        2>"$inspection_output/node-$inspection_node.stderr" || inspection_status=$?
    printf '%s\n' "$inspection_status" >"$inspection_output/node-$inspection_node.status"
    if ((inspection_status != 0)); then
        printf 'failed node=%s status=%s\n' "$inspection_node" "$inspection_status" \
            >"$inspection_output/outcome"
        exit "$inspection_status"
    fi
done
date -u +%FT%TZ >"$inspection_output/finished-at"
printf 'collection-complete; independent review required\n' >"$inspection_output/outcome"
