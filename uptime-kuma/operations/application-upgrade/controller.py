"""Workstation entry point invoked by the local Ansible playbook."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import time
import uuid

import yaml

from release import candidate, version
from upgrade import digest, pages

HERE = Path(__file__).resolve().parent
MANIFEST = HERE.parents[1] / "manifests/deployment.yaml"
PI = "ama@10.1.3.75"
SVMF = "pi@10.1.3.83"
WRITER = ["sudo", "-nu", "kuma-backup"]
ROOT = ["sudo", "-n"]
FILES = ["release.py", "upgrade.py", "store_backup.py", "controller.py"]


def pins():
    config = yaml.safe_load(MANIFEST.read_text())["application"]
    return {key: config[key] for key in ("release", "image", "local_image_id")}


def sources():
    files = {name: digest(HERE / name) for name in FILES}
    files["nightly_receiver"] = digest(HERE.parent / "nightly-backup/receive.py")
    files["playbook"] = digest(HERE.parents[1] / "ansible/application-upgrade.yaml")
    return files


def ssh(host, args):
    return ["ssh", "-oBatchMode=yes", "-oStrictHostKeyChecking=yes", "-oConnectTimeout=8",
            "-oServerAliveInterval=10", "-oServerAliveCountMax=3", host, shlex.join(map(str, args))]


def call(host, args, data=None, timeout=45):
    return subprocess.run(ssh(host, args), input=data, stdout=subprocess.PIPE, check=True,
                          timeout=timeout).stdout


def put(host, identity, path, data):
    call(host, [*identity, "dd", f"of={path}", "status=none", "conv=excl"], data)


def read_event(root, name):
    raw = call(PI, [*ROOT, "sh", "-c", 'if test -f "$1"; then cat "$1"; fi', "read", root / name])
    return json.loads(raw) if raw else None


def handoff(root, remote, ident, record):
    with subprocess.Popen(ssh(PI, [*ROOT, "cat", root / "data.tar"]), stdout=subprocess.PIPE) as source:
        try:
            sink = subprocess.run(ssh(SVMF, [*WRITER, "python3", "-B", remote / "store_backup.py",
                                             ident, json.dumps(record)]), stdin=source.stdout,
                                  stdout=subprocess.PIPE, timeout=480, check=True)
        finally:
            source.stdout.close()
        if source.wait(timeout=10) or json.loads(sink.stdout)["sha256"] != record["sha256"]:
            raise ValueError("transfer or restore failed")
    put(PI, ROOT, root / "backup-verified", record["sha256"].encode())


def reconcile(old, new):
    original = MANIFEST.read_text()
    if pins() != old:
        raise ValueError("accepted manifest changed during upgrade; reconcile accepted receipt manually")
    updated = original
    for key in old:
        updated, count = re.subn(rf"(?m)^  {key}: {re.escape(old[key])}$", f"  {key}: {new[key]}", updated)
        if count != 1:
            raise ValueError(f"cannot reconcile manifest {key}")
    tmp = MANIFEST.with_suffix(".yaml.upgrade")
    with tmp.open("x") as output:
        output.write(updated)
    os.chmod(tmp, MANIFEST.stat().st_mode & 0o777)
    tmp.replace(MANIFEST)


def apply(path, approved):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != approved:
        raise ValueError("candidate checksum differs")
    spec = json.loads(raw)
    if spec["sources"] != sources() or spec["old"] != pins():
        raise ValueError("workstation inputs changed since preparation")
    ident = uuid.UUID(hex=spec["run"]).hex
    root = Path("/var/backups") / ("kuma-upgrade-" + ident)
    remote = Path("/var/backups/uptime-kuma") / (".work-" + ident)
    receipt = path.with_suffix(".receipt.json")
    with receipt.open("x") as out:
        json.dump({"state": "admitting", "pi": str(root)}, out)
    # The backup writer's directory is private. Check the estimate before downtime.
    size = int(call(PI, [*ROOT, "du", "-sb", "/var/lib/uptime-kuma/data"]).split()[0])
    free = int(call(SVMF, [*WRITER, "df", "-B1", "--output=avail", remote.parent]).splitlines()[-1])
    if free < 2 * size + 128 * 2**20:
        raise ValueError("insufficient svmf space")
    receiver = call(SVMF, [*WRITER, "sha256sum", "/usr/local/libexec/uptime-kuma-backup/receive.py"])
    if receiver.split()[0].decode() != spec["sources"]["nightly_receiver"]:
        raise ValueError("installed backup receiver differs from the reviewed revision")
    call(PI, [*ROOT, "mkdir", "-m700", root])
    call(SVMF, [*WRITER, "mkdir", "-m700", remote])
    started = False
    try:
        for name in ("upgrade.py", "release.py"):
            put(PI, ROOT, root / name, (HERE / name).read_bytes())
        for name in ("upgrade.py", "release.py", "store_backup.py"):
            put(SVMF, WRITER, remote / name, (HERE / name).read_bytes())
        put(PI, ROOT, root / "candidate.json", raw)
        unit = "kuma-upgrade-" + ident
        call(PI, [*ROOT, "systemd-run", "--unit", unit, "--property=UMask=0077",
                  "/usr/bin/python3", "-B", root / "upgrade.py", root])
        started = True
        sent = set()
        problem = None
        while True:
            result = read_event(root, "result")
            if result:
                result.update(run=ident, candidate_sha256=approved, old=spec["old"], new=spec["new"],
                              backup=f"upgrade-{ident}.tar" if "backup-ready" in sent else None,
                              workstation_failure=problem)
                receipt.write_text(json.dumps(result, indent=2) + "\n")
                if result["state"] == "restored":
                    pages(result)
                if result["state"] != "accepted":
                    raise RuntimeError(f"{result} (Pi evidence {root})")
                reconcile(spec["old"], spec["new"])
                print(f"Accepted {spec['new']['release']}; receipt {receipt}")
                break
            if call(PI, [*ROOT, "systemctl", "show", "-p", "ActiveState", "--value", unit]).strip() not in (
                    b"active", b"activating", b"deactivating"):
                if read_event(root, "result"):
                    continue
                raise RuntimeError(f"worker terminated without a receipt; inspect {root}")
            if not problem:
                try:
                    for event in ("backup-ready", "candidate-ready"):
                        if event in sent:
                            continue
                        record = read_event(root, event)
                        if record is None:
                            continue
                        if event == "backup-ready":
                            handoff(root, remote, ident, record)
                        else:
                            pages(record)
                            put(PI, ROOT, root / "client-verified", b"ok")
                        sent.add(event)
                except Exception as error:
                    problem = str(error)
                    print(f"Requesting recovery: {problem}", file=sys.stderr)
                    put(PI, ROOT, root / "abort", b"abort")
            time.sleep(3)
    finally:
        for name in ("upgrade.py", "release.py", "store_backup.py"):
            call(SVMF, [*WRITER, "rm", "-f", remote / name])
        call(SVMF, [*WRITER, "rmdir", remote])
        if started:
            print(f"Pi terminal evidence: {root}/result")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["prepare", "apply"])
    parser.add_argument("file", type=Path)
    parser.add_argument("selection")
    args = parser.parse_args()
    os.umask(0o077)
    if args.mode == "prepare":
        old = pins()
        if version(args.selection) <= version(old["release"]):
            parser.error("select a newer stable release")
        spec = {"run": uuid.uuid4().hex, "old": old, "new": candidate(args.selection), "sources": sources()}
        with args.file.open("x") as out:
            json.dump(spec, out, indent=2)
        print(json.dumps(spec, indent=2), digest(args.file))
    else:
        apply(args.file, args.selection)
