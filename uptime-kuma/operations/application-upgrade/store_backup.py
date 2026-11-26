"""Receive an upgrade snapshot as the existing svmf writer; keep daily rotation separate."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import sys
import tempfile

from upgrade import inventory, signature


def receive(directory, run_id, expected, source, restore):
    if not re.fullmatch("[0-9a-f]{32}", run_id):
        raise ValueError("invalid run ID")
    final = directory / f"upgrade-{run_id}.tar"
    with (directory / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if shutil.disk_usage(directory).free < 2 * expected["size"] + 128 * 2**20:
            raise ValueError("insufficient receiver space")
        with tempfile.TemporaryDirectory(dir=directory) as tmp:
            archive = Path(tmp) / "data.tar"
            with archive.open("xb") as out:
                shutil.copyfileobj(source, out)
                out.flush()
                os.fsync(out.fileno())
            with archive.open("rb") as reader:
                checksum = hashlib.file_digest(reader, "sha256").hexdigest()
            if archive.stat().st_size != expected["size"] or checksum != expected["sha256"]:
                raise ValueError("off-node archive mismatch")
            scratch = Path(tmp) / "scratch"
            scratch.mkdir()
            restore(archive, scratch)
            if signature(inventory(scratch / "data")) != expected["inventory"]:
                raise ValueError("restored inventory differs")
            os.link(archive, final)
            fd = os.open(directory, os.O_DIRECTORY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
    return {"archive": final.name, "sha256": checksum}


if __name__ == "__main__":
    os.umask(0o077)
    nightly = runpy.run_path("/usr/local/libexec/uptime-kuma-backup/receive.py")
    print(json.dumps(receive(nightly["DEST"], sys.argv[1], json.loads(sys.argv[2]),
                             sys.stdin.buffer, nightly["check_restore"])))
