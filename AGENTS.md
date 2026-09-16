# Repository instructions

This repository owns fleet Munin configuration. Read `README.md` and
`Munin/README.md` before changing Munin artifacts. It is a scaffold; no current
profile is accepted for live deployment.

- Inventory explicitly selects host profiles; this repository defines their
  node plugins, settings, and master entries. Do not infer selection from a
  hostname or install every available plugin.
- Keep plugin source distinct from `/etc/munin/plugins` links. Changes to a
  candidate profile do not select hosts or authorize deployment.
- Keep application-specific Munin configuration here. Application repositories
  may state requirements and link to this component, not maintain competing
  deployable copies.
- Treat Caddy files as deferred candidates. Confirm current Caddy contracts,
  privilege, data output, and polling before proposing activation.
- A repository-only request permits local edits and checks, not host access,
  master mutation, package installation, or restart. Obtain one scoped approval
  for each live node or master stage. That approval may cover its exact
  preflight, change, readback, polling, and rollback path; it does not authorize
  another stage. Do not require command-by-command approval within that scope.
  Apply node changes one node at a time. Keep operation evidence separate from
  architecture docs. Define a hash-bound deployment bundle only when a live
  installer and its approval workflow exist.
- Check changed shell files with `bash -n`, ShellCheck, and
  `shfmt -d -i 4 -ci`. Keep executable plugin and test entry points executable
  in both the working tree and Git index. Do not run bare `shfmt -w`; format
  only intended files with the same pinned flags. Test success and failure
  paths when changing plugin parsing or validation. Do not impose
  `set -Eeuo pipefail` on existing plugins without testing their error paths.
- Keep validation proportionate: run `bash Munin/tests/validate-scaffold.sh`
  for plugin, settings, or profile changes and the relevant pre-commit hooks
  for changed file types. Documentation-only edits need focused Markdown and
  Git checks. Add fixture-backed tests when changing plugin behavior. Do not
  call a `config` output test a live node or master acceptance test.
- The pre-commit Gitleaks hook scans staged content. It does not scan untracked
  or unstaged artifacts, even under `pre-commit run --all-files`. Before
  reviewing new local artifacts or requesting deployment, run a separate
  working-tree scan with `gitleaks detect --source . --no-git --redact
  --no-banner`.
- Do not upload private infrastructure files to optional third-party review
  services without authorization.
