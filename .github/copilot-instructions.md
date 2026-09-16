# Repository guidance

Follow [AGENTS.md](../AGENTS.md) and the [Munin component guide](../Munin/README.md).
The repository is a scaffold; Caddy plugins are deferred candidates, not a
deployed or selected profile. Inventory must explicitly select host profiles.

For Munin changes, run `bash Munin/tests/validate-scaffold.sh` and the relevant
pre-commit checks. Do not treat local validation as permission for host or
master changes.
