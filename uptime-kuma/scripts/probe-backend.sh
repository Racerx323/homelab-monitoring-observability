#!/usr/bin/env bash
set -Eeuo pipefail

[[ $# -eq 3 ]] || exit 64

curl --noproxy '*' --ipv4 --fail --silent --show-error \
    --connect-timeout 3 --max-time 10 --output /dev/null \
    --write-out '{"family":"ipv4","path":"/dashboard","status":%{http_code},"source":"%{local_ip}","backend":"%{remote_ip}"}\n' \
    "http://$1:$3/dashboard"
curl --noproxy '*' --ipv6 --fail --silent --show-error \
    --connect-timeout 3 --max-time 10 --output /dev/null \
    --write-out '{"family":"ipv6","path":"/dashboard","status":%{http_code},"source":"%{local_ip}","backend":"%{remote_ip}"}\n' \
    "http://[$2]:$3/dashboard"
