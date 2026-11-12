#!/usr/bin/env bash
set -Eeuo pipefail
set +x

kuma_test_repository=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
readonly kuma_test_repository
cd -- "$kuma_test_repository"

python3 uptime-kuma/tests/test-memory-controller.py
python3 uptime-kuma/tests/test-restore-archive.py
python3 uptime-kuma/tests/test-backend-contract.py
python3 uptime-kuma/tests/test-network.py
python3 uptime-kuma/tests/test-network-diagnostic.py
python3 uptime-kuma/tests/test-startup-permit.py
python3 uptime-kuma/tests/test-admission-evidence.py
python3 ../homelab-server-configs/foundation/tests/test-observe-needrestart.py
python3 ../homelab-server-configs/foundation/tests/test-guarded-schedule.py
/bin/bash ../homelab-server-configs/tests/repository/run-with-ansible-local-temp.sh \
    ansible-playbook --syntax-check -i uptime-kuma/ansible/inventory.yaml \
    uptime-kuma/ansible/initial-deployment.yaml
/bin/bash ../homelab-server-configs/tests/repository/run-with-ansible-local-temp.sh \
    ansible-playbook --syntax-check -i uptime-kuma/operations/network-diagnostic-inventory.yaml \
    uptime-kuma/ansible/diagnose-network.yaml
/bin/bash ../homelab-server-configs/tests/repository/run-with-ansible-local-temp.sh \
    ansible-playbook --syntax-check -i uptime-kuma/operations/network-diagnostic-inventory.yaml \
    uptime-kuma/ansible/correct-loopback.yaml
/bin/bash ../homelab-server-configs/tests/repository/run-with-ansible-local-temp.sh \
    ansible-playbook --syntax-check -i uptime-kuma/ansible/inventory.yaml \
    uptime-kuma/ansible/remaining-deployment.yaml
/bin/bash ../homelab-server-configs/tests/repository/run-with-ansible-local-temp.sh \
    ansible-playbook --syntax-check -i uptime-kuma/ansible/inventory.yaml \
    uptime-kuma/ansible/measure-capacity.yaml
shfmt -d -i 4 -ci \
    uptime-kuma/scripts/probe-backend.sh uptime-kuma/tests/check.sh
shellcheck uptime-kuma/scripts/probe-backend.sh uptime-kuma/tests/check.sh
/bin/bash ../homelab-server-configs/Caddy/tests/check-shell-readonly-local-collisions-v2.sh \
    uptime-kuma/scripts/probe-backend.sh uptime-kuma/tests/check.sh
