#!/usr/bin/env python3
"""Open an actual backup in a contained instance; never operate the source service."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time


def extract_backup(source, destination):
    with tarfile.open(source, "r:") as archive:
        members, total = [], 0
        for member in archive:
            total += member.size
            if len(members) >= 10000 or total > 67108864:
                raise ValueError("backup exceeds the initial-deployment extraction budget")
            members.append(member)
        archive.extractall(destination, members=members, filter="data")
    data = destination / "data"
    if (data.is_symlink() or not data.is_dir() or (data / "kuma.db").is_symlink()
            or not (data / "kuma.db").is_file()):
        raise ValueError("expected a real data directory and database")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--archive-sha256", required=True)
    parser.add_argument("--work-root", type=Path, required=True)
    parser.add_argument("--expected-active-users", type=int, required=True)
    parser.add_argument("--expected-release", required=True)
    parser.add_argument("--memory", required=True)
    parser.add_argument("--timezone", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"(?:docker\.io/louislam/uptime-kuma@)?sha256:[a-f0-9]{64}", args.image):
        parser.error("use the approved immutable upstream image")
    if args.archive.is_symlink() or not args.archive.is_file() or args.archive.stat().st_size > 67108864:
        parser.error("initial-deployment archive must be a regular file of at most 64 MiB")
    if (args.work_root.is_symlink() or not args.work_root.is_dir()
            or args.work_root.resolve() != args.work_root
            or args.work_root.stat().st_mode & 0o777 != 0o700
            or args.work_root.stat().st_uid != os.geteuid()):
        parser.error("work root must be a real, private directory owned by this process user")
    with args.archive.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != args.archive_sha256:
        parser.error("archive differs from the captured source backup identity")
    os.umask(0o077)
    work = Path(tempfile.mkdtemp(prefix="restore-", dir=args.work_root))
    extracted = work / "extracted"
    extracted.mkdir()
    name = "kuma-" + work.name
    label = "homelab.uptime-kuma.restore"
    outcome = {"image": args.image, "archive_sha256": digest, "commands": [],
               "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "verdict": "failed", "scope": "Isolated backup restore; source availability is checked separately"}
    attempted = False

    def run(argv, *, timeout=30, required=True, input_text=None):
        result = subprocess.run(argv, input=input_text, capture_output=True, text=True, timeout=timeout)
        outcome["commands"].append({"argv": argv, "status": result.returncode})
        if len(result.stdout) > 262144 or len(result.stderr) > 16384:
            raise RuntimeError("command output exceeded its bound")
        if required and result.returncode:
            raise RuntimeError(f"{argv[0]} returned {result.returncode}: {result.stderr[:1000]}")
        return result

    def podman(*argv, **kwargs):
        return run(["podman", *argv], **kwargs)

    try:
        data = extract_backup(args.archive, extracted)
        attempted = True
        podman("run", "--detach", "--timeout", "300", "--name", name, "--label", label + "=" + work.name,
               "--network", "none", "--pull", "never", "--read-only", "--user", "1000:1000",
               "--tmpfs", "/tmp:rw,nosuid,nodev,size=64m", "--cap-drop", "all",
               "--security-opt", "no-new-privileges", "--memory", args.memory,
               "--memory-swap", args.memory, "--pids-limit", "256", "--cpus", "2",
               "--volume", str(data) + ":/app/data:U", "--env", "UPTIME_KUMA_DB_TYPE=sqlite",
               "--env", "UPTIME_KUMA_HOST=127.0.0.1", "--env", "TZ=" + args.timezone,
               args.image, timeout=90)
        program = ('(async()=>{const r=await fetch("http://127.0.0.1:3001/");'
                   'if(!r.ok)process.exit(2);console.log(JSON.stringify({status:r.status,'
                   'uid:process.getuid(),release:require("/app/package.json").version}));'
                   '})().catch(()=>process.exit(3));')
        deadline = time.monotonic() + 180
        while True:
            ready = podman("exec", name, "node", "-e", program, required=False, timeout=10)
            if ready.returncode == 0:
                break
            if time.monotonic() >= deadline:
                raise RuntimeError("restored application did not become ready")
            time.sleep(3)
        outcome["application"] = json.loads(ready.stdout)
        if outcome["application"] != {"status": 200, "uid": 1000, "release": args.expected_release}:
            raise RuntimeError("restored application identity or HTTP result differs")
        # Stop before inspecting restored SQLite state; never read credential fields.
        podman("stop", "--time", "30", name, timeout=45)
        sql = '''import json,sqlite3,sys
from urllib.parse import quote
with sqlite3.connect('file:'+quote(sys.argv[1])+'?mode=ro',uri=True) as c:
 auth=c.execute("SELECT value FROM setting WHERE key='disableAuth'").fetchone()
 print(json.dumps({'active_users':c.execute('SELECT COUNT(*) FROM user WHERE active=1').fetchone()[0],
 'monitors':c.execute('SELECT COUNT(*) FROM monitor').fetchone()[0],
 'notifications':c.execute('SELECT COUNT(*) FROM notification').fetchone()[0],
 'authentication_disabled':bool(json.loads(auth[0])) if auth and isinstance(auth[0],str) else bool(auth[0]) if auth else False}))
'''
        prefix = ["podman", "unshare"] if os.geteuid() != 0 else []
        counts = run([*prefix, sys.executable, "-c", sql, str(data / "kuma.db")])
        outcome["counts"] = json.loads(counts.stdout)
        if outcome["counts"] != {"active_users": args.expected_active_users, "monitors": 0,
                                  "notifications": 0, "authentication_disabled": False}:
            raise RuntimeError("restored account/monitor/notification counts differ")
        outcome["verdict"] = "passed"
    except Exception as error:
        outcome["error"] = str(error)[:2000]
    finally:
        cleanup_errors = []
        try:
            if attempted:
                exists = podman("container", "exists", name, required=False)
                if exists.returncode == 0:
                    info = json.loads(podman("inspect", name).stdout)[0]
                    if info["Config"]["Labels"].get(label) != work.name:
                        raise RuntimeError("refusing cleanup without the exact task label")
                    podman("rm", "--force", name, timeout=45)
                elif exists.returncode != 1:
                    raise RuntimeError("could not determine container cleanup state")
            outcome["container_removed"] = True
            if extracted.is_symlink() or extracted.resolve() != work / "extracted":
                raise RuntimeError("refusing cleanup of an unexpected extraction path")
            if os.geteuid() == 0:
                shutil.rmtree(extracted)
            else:
                run(["podman", "unshare", "rm", "-rf", "--", str(extracted)])
            outcome["extracted_data_removed"] = True
        except Exception as error:
            cleanup_errors.append(str(error)[:1000])
        if cleanup_errors:
            outcome["verdict"] = "failed"
            outcome["cleanup_errors"] = cleanup_errors
        (work / "receipt.json").write_text(json.dumps(outcome, indent=2) + "\n")
        print(json.dumps({"verdict": outcome["verdict"], "receipt": str(work / "receipt.json"),
                          "cleanup_errors": cleanup_errors, "error": outcome.get("error")}))
    return 0 if outcome["verdict"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
