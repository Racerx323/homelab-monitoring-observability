#!/usr/bin/env python3
"""Qualify an explicit image in isolated local containers; never contact a host."""

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True, help="Immutable native-platform image reference")
    parser.add_argument("--evidence-root", required=True, type=Path)
    args = parser.parse_args()
    if "@sha256:" not in args.image or len(args.image.rsplit("@sha256:", 1)[1]) != 64:
        parser.error("use an immutable SHA-256 image reference")
    if not args.evidence_root.is_dir() or args.evidence_root.is_symlink():
        parser.error("evidence root must be an existing task-owned real directory")
    os.umask(0o077)
    root = Path(tempfile.mkdtemp(prefix="runtime-smoke-", dir=args.evidence_root))
    identity = root.name
    names = []
    checks = {}
    invocation = 0

    def run(arguments, *, input_text=None, timeout=60, required=True):
        nonlocal invocation
        invocation += 1
        result = subprocess.run(arguments, input=input_text, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=timeout)
        (root / f"{invocation:02d}-stdout.log").write_text(result.stdout[:1048576])
        (root / f"{invocation:02d}-stderr.log").write_text(result.stderr[:1048576])
        if len(result.stdout) > 1048576 or len(result.stderr) > 1048576:
            raise RuntimeError("command output exceeded the retained evidence bound")
        if required and result.returncode:
            raise RuntimeError(f"command {invocation} failed with status {result.returncode}")
        return result

    def podman(*arguments, **kwargs):
        return run(["podman", *arguments], **kwargs)

    def start(name, data):
        data.mkdir(exist_ok=True)
        # A timed-out launch can still create a container that needs cleanup.
        names.append(name)
        podman("run", "--detach", "--name", name,
               "--label", "homelab.uptime-kuma.smoke=" + identity,
               "--network", "none", "--pull", "never",
               "--read-only", "--tmpfs", "/tmp:rw,nosuid,nodev,size=64m",
               "--cap-drop", "all", "--security-opt", "no-new-privileges",
               "--memory", "320m", "--memory-swap", "320m", "--pids-limit", "256",
               "--cpus", "2", "--volume", str(data) + ":/app/data:U",
               "--env", "UPTIME_KUMA_DB_TYPE=sqlite",
               "--env", "UPTIME_KUMA_HOST=127.0.0.1",
               "--env", "TZ=America/Chicago", args.image, timeout=90)

    def ready(name):
        program = (
            'const fs = require("node:fs");\n'
            '(async () => { const r = await fetch("http://127.0.0.1:3001/");\n'
            'if (!r.ok || !fs.existsSync("/app/data/kuma.db")) process.exit(2);\n'
            'console.log(JSON.stringify({status:r.status,uid:process.getuid(),'
            'version:require("/app/package.json").version,'
            'databaseBytes:fs.statSync("/app/data/kuma.db").size}));\n'
            '})().catch(() => process.exit(3));\n'
        )
        deadline = time.monotonic() + 90
        while True:
            result = podman("exec", "-i", name, "node", input_text=program,
                            timeout=10, required=False)
            if result.returncode == 0:
                observation = json.loads(result.stdout)
                if observation["uid"] == 0 or observation["databaseBytes"] == 0:
                    raise RuntimeError("non-root/database acceptance failed")
                return observation
            if time.monotonic() >= deadline:
                raise RuntimeError("application did not become ready within 90 seconds")
            time.sleep(3)

    outcome = {"image": args.image, "checks": checks, "evidence": str(root),
               "test_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "scope": "Local native image, no network or published ports; no ARM64 target, systemd, firewall, TLS or account acceptance."}
    try:
        podman("pull", args.image, timeout=240)
        source = identity + "-source"
        data = root / "data"
        start(source, data)
        checks["initial_start"] = ready(source)
        checks["idle_stats"] = json.loads(podman("stats", "--no-stream", "--format", "json", source).stdout)
        podman("exec", source, "node", "-e",
               'require("node:fs").writeFileSync("/app/data/.smoke-marker", "persisted")')
        podman("stop", "--time", "30", source)
        archive = root / "data.tar"
        podman("unshare", "tar", "-C", str(data), "-cf", str(archive), ".")
        podman("start", source)
        checks["restart"] = ready(source)
        marker = 'if(require("node:fs").readFileSync("/app/data/.smoke-marker","utf8")!=="persisted")process.exit(1)'
        podman("exec", source, "node", "-e", marker)
        checks["restart_persistence"] = True
        podman("stop", "--time", "30", source)
        restored = root / "restored"
        restored.mkdir()
        podman("unshare", "tar", "-C", str(restored), "-xf", str(archive))
        restore_name = identity + "-restore"
        start(restore_name, restored)
        checks["restored_start"] = ready(restore_name)
        podman("exec", restore_name, "node", "-e", marker)
        checks["restored_persistence"] = True
        outcome["verdict"] = "passed"
    except Exception as error:
        outcome["verdict"] = "failed"
        outcome["error"] = str(error)
        raise
    finally:
        cleanup_errors = []
        for name in reversed(names):
            try:
                exists = podman("container", "exists", name, required=False)
                if exists.returncode == 1:
                    continue
                if exists.returncode:
                    raise RuntimeError("could not determine whether container exists")
                podman("logs", name, required=False)
                info = json.loads(podman("inspect", name).stdout)[0]
                if info["Config"]["Labels"].get("homelab.uptime-kuma.smoke") != identity:
                    raise RuntimeError("refusing cleanup without the task label")
                podman("rm", "--force", name)
            except Exception as error:
                cleanup_errors.append({"container": name, "error": str(error)})
        outcome["owned_containers_removed"] = not cleanup_errors
        if cleanup_errors:
            outcome["cleanup_errors"] = cleanup_errors
            outcome["verdict"] = "failed"
        (root / "result.json").write_text(json.dumps(outcome, indent=2) + "\n")
        print(json.dumps(outcome, indent=2))
    if outcome["verdict"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
