#!/usr/bin/env python3
"""Observe one attended command and dashboard recovery. Never retry the command."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import time

DASHBOARD = "https://uptime.local.theama.co/dashboard"


def probe():
    response = subprocess.run(
        ["curl", "--noproxy", "*", "--max-time", "2", "-s", "-o", "/dev/null",
         "-w", "%{http_code}", DASHBOARD], capture_output=True, text=True)
    return response.stdout.strip(), response.returncode


def observe(command, log, *, recovery_seconds=180, interval=0.5):
    def record(**fields):
        print(json.dumps({"utc": datetime.now(timezone.utc).isoformat(), **fields}),
              file=log, flush=True)

    def available(phase):
        status, rc = probe()
        record(phase=phase, http=status, curl_exit=rc)
        return rc == 0 and status == "200"

    if not available("admission"):
        record(transfer="not started")
        return 1
    with subprocess.Popen(command) as child:
        while child.poll() is None:
            available("transfer")
            time.sleep(interval)
        record(transfer_exit=child.returncode)
        deadline = time.monotonic() + recovery_seconds
        while True:
            if available("post-transfer"):
                record(dashboard="available")
                return child.returncode or 0
            if time.monotonic() >= deadline:
                record(dashboard="recovery unverified")
                return child.returncode or 1
            time.sleep(interval)


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("receipt", type=Path)
    cli.add_argument("command", nargs="+")
    args = cli.parse_args()
    os.umask(0o077)
    with args.receipt.open("x") as output:
        raise SystemExit(observe(args.command, output))
