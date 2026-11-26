"""Kuma Pi worker. Runs independently of the workstation during the stop window."""
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from urllib.parse import quote
from urllib.request import urlopen

from release import installed, installed_id, version

UNIT = "uptime-kuma.service"
QUAD = Path("/etc/containers/systemd/uptime-kuma.container")
DATA = Path("/var/lib/uptime-kuma/data")
FQDN = "https://uptime.local.theama.co"


def run(*args, timeout=180):
    return subprocess.check_output(args, text=True, timeout=timeout).strip()


def db_open(data):
    return sqlite3.connect((data / "kuma.db").as_uri() + "?mode=ro", uri=True)


def inventory(data):
    with db_open(data) as db:
        db.execute("BEGIN")
        queries = {
            "monitor": "SELECT id,name,type,active FROM monitor ORDER BY id",
            "pages": "SELECT id,slug,title,published FROM status_page ORDER BY id",
            "groups": 'SELECT id,status_page_id,name,weight FROM "group" ORDER BY id',
            "membership": "SELECT group_id,monitor_id,weight FROM monitor_group ORDER BY group_id,monitor_id",
            "assignments": "SELECT monitor_id,notification_id FROM monitor_notification ORDER BY 1,2",
        }
        return {name: db.execute(sql).fetchall() for name, sql in queries.items()}


def signature(rows):
    return hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def emit(root, name, record):
    tmp = root / (name + ".tmp")
    tmp.write_text(json.dumps(record))
    tmp.replace(root / name)


def pages(rows, origin=FQDN):
    with urlopen(origin + "/dashboard", timeout=10) as response:
        if response.status != 200:
            raise ValueError("dashboard unavailable")
    for _, slug, _, published in rows["pages"]:
        if published:
            path = quote(slug, safe="")
            with urlopen(f"{origin}/status/{path}", timeout=10) as response:
                if response.status != 200:
                    raise ValueError("status page unavailable")
            with urlopen(f"{origin}/api/status-page/{path}", timeout=10) as response:
                if json.load(response)["config"]["slug"] != slug:
                    raise ValueError("status page identity mismatch")


def monitors(data):
    with db_open(data) as db:
        rows = db.execute("SELECT id,type,interval,retry_interval,maxretries,timeout FROM monitor WHERE active=1")
        result = {}
        for ident, kind, interval, retry, retries, timeout in rows:
            if kind in ("push", "group"):
                raise ValueError(f"monitor {ident} ({kind}) requires a reviewed freshness criterion")
            result[ident] = int(interval) + (int(retries or 0) + 1) * (int(timeout or 0) + int(retry or interval)) + 30
        return result


def verify(expected, rows, started, since):
    for attempt in range(61):
        try:
            if installed() == expected["release"] and installed_id() == expected["local_image_id"]:
                with urlopen("http://127.0.0.1:3001/dashboard", timeout=3) as response:
                    if response.status == 200:
                        break
        except (subprocess.SubprocessError, OSError):
            pass
        time.sleep(3)
    else:
        raise RuntimeError("running image or application version failed verification")
    if signature(inventory(DATA)) != signature(rows):
        raise ValueError("monitor, status page or assignment inventory differs")
    pages(rows, "http://127.0.0.1:3001")
    pending = monitors(DATA)
    down = []
    while pending:
        with db_open(DATA) as db:
            for ident, budget in list(pending.items()):
                beat = db.execute("SELECT status FROM heartbeat WHERE monitor_id=? AND time>=? "
                                  "AND status IN (0,1) ORDER BY id DESC LIMIT 1", (ident, since)).fetchone()
                if beat:
                    del pending[ident]
                    if beat[0] == 0:
                        down.append(ident)
                elif time.monotonic() - started > budget:
                    raise TimeoutError(f"monitor {ident} has no fresh completed heartbeat")
        if pending:
            time.sleep(3)
    return {"pages": rows["pages"], "down": down, "inventory_sha256": signature(rows)}


def start_check(expected, rows):
    started = time.monotonic()
    since = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    run("systemctl", "start", UNIT, timeout=210)
    return verify(expected, rows, started, since)


def wait_ack(root, name, timeout=600):
    limit = time.monotonic() + timeout
    while time.monotonic() < limit:
        if (root / "abort").exists():
            raise RuntimeError("workstation reported failure")
        if (root / name).exists():
            return
        time.sleep(1)
    raise TimeoutError(f"waiting for {name}")


def stopped():
    run("systemctl", "stop", UNIT)
    state = run("systemctl", "show", "-p", "ActiveState", "--value", UNIT)
    running = run("podman", "ps", "--filter", "name=^uptime-kuma$", "--format", "{{.Names}}")
    if state not in {"inactive", "failed"} or running:
        raise RuntimeError("Kuma did not stop")


def switch(root, candidate_bytes):
    with tempfile.NamedTemporaryFile(dir=QUAD.parent, prefix="." + root.name, delete=False) as output:
        stage = Path(output.name)
    try:
        shutil.copy2(QUAD, stage)
        stage.write_bytes(candidate_bytes)
        os.replace(stage, QUAD)
    finally:
        stage.unlink(missing_ok=True)
    run("systemctl", "daemon-reload")


def transaction(root, old, new):
    if installed() != old["release"] or installed_id() != old["local_image_id"]:
        raise ValueError("predecessor drift")
    if version(new["release"]) <= version(old["release"]):
        raise ValueError("candidate must be newer")
    original = QUAD.read_bytes()
    before = ("Image=" + old["local_image_id"]).encode()
    lines = original.splitlines()
    if [line for line in lines if line.startswith(b"Image=")] != [before] or b"Pull=never" not in lines:
        raise ValueError("Quadlet predecessor or pull policy differs")
    if run("hostname", "-s") != "j2-svpi3bmf" or run("uname", "-m") != "aarch64":
        raise ValueError("wrong host or architecture")
    for guard in ("uptime-kuma-firewall.service", "uptime-kuma-startup-permit.service"):
        if guard not in run("systemctl", "show", "-p", "Requires", "--value", UNIT).split():
            raise ValueError(f"missing dependency {guard}")
    run("systemctl", "is-active", UNIT, "uptime-kuma-firewall.service")
    run("podman", "image", "exists", old["local_image_id"])
    retained_size = int(run("podman", "image", "inspect", "--format", "{{.Size}}", old["local_image_id"]))
    graph_root = Path(run("podman", "info", "--format", "{{.Store.GraphRoot}}"))
    if shutil.disk_usage(graph_root).free < 2 * retained_size + 128 * 2**20:
        raise ValueError("insufficient Podman staging space")
    run("podman", "pull", "--platform", "linux/arm64", new["image"], timeout=900)
    image = json.loads(run("podman", "image", "inspect", new["image"]))[0]
    if image["Architecture"] != "arm64" or image["Id"].removeprefix("sha256:") != new["local_image_id"][7:]:
        raise ValueError("staged image identity mismatch")
    rows = inventory(DATA)
    monitors(DATA)
    pages(rows, "http://127.0.0.1:3001")
    size = int(run("du", "-sb", DATA).split()[0])
    if min(shutil.disk_usage(p).free for p in (root, DATA.parent)) < size * 3 + 128 * 2**20:
        raise ValueError("insufficient Pi backup or recovery space")
    if run("systemctl", "show", "-p", "NRestarts", "--value", UNIT) != "0":
        raise ValueError("recent automatic restarts; review before upgrade")
    active_us = int(run("systemctl", "show", "-p", "ActiveEnterTimestampMonotonic", "--value", UNIT))
    if time.clock_gettime(time.CLOCK_MONOTONIC) - active_us / 1e6 < 300:
        raise ValueError("wait for five minutes of stable service before upgrade")
    (root / "prior.container").write_bytes(original)
    archive = root / "data.tar"
    changed = False
    try:
        stopped()
        rows = inventory(DATA)
        run("tar", "--numeric-owner", "--acls", "--xattrs", "-C", DATA.parent, "-cf", archive, "data", timeout=600)
        checksum = digest(archive)
        emit(root, "backup-ready", {"sha256": checksum, "inventory": signature(rows), "size": archive.stat().st_size})
        wait_ack(root, "backup-verified")
        if (root / "backup-verified").read_text().strip() != checksum:
            raise ValueError("off-node checksum acknowledgement differs")
        if QUAD.read_bytes() != original:
            raise ValueError("Quadlet changed during the backup")
        changed = True
        switch(root, original.replace(before, ("Image=" + new["local_image_id"]).encode(), 1))
        result = start_check(new, rows)
        emit(root, "candidate-ready", result)
        wait_ack(root, "client-verified", 120)
        emit(root, "result", {"state": "accepted", **result})
    except Exception as failure:
        try:
            if changed:
                stopped()
                if digest(archive) != checksum:
                    raise ValueError("rollback archive digest changed")
                scratch = DATA.parent / (root.name + "-restore")
                scratch.mkdir(mode=0o700)
                run("tar", "--acls", "--xattrs", "--numeric-owner", "-C", scratch, "-xf", archive, timeout=600)
                if signature(inventory(scratch / "data")) != signature(rows):
                    raise ValueError("rollback inventory mismatch")
                DATA.rename(DATA.parent / (root.name + "-failed-data"))
                (scratch / "data").rename(DATA)
                scratch.rmdir()
                switch(root, original)
            evidence = start_check(old, rows)
            emit(root, "result", {"state": "restored", "reason": str(failure), **evidence})
        except Exception as recovery:
            emit(root, "result", {"state": "recovery-failed", "reason": str(failure), "recovery": str(recovery)})
        raise


if __name__ == "__main__":
    os.umask(0o077)
    root = Path(sys.argv[1])
    try:
        with open("/run/lock/uptime-kuma-backup.lock", "a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            spec = json.loads((root / "candidate.json").read_text())
            transaction(root, spec["old"], spec["new"])
    except Exception as error:
        if not (root / "result").exists():
            emit(root, "result", {"state": "preflight-failed", "reason": str(error)})
        raise
