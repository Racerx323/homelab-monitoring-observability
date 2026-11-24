#!/usr/bin/python3
"""Pull one daily snapshot. Publish and prune only after an isolated SQLite restore."""
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import stat
import subprocess
import tarfile
import tempfile

DEST = Path("/var/backups/uptime-kuma")
SSH = ["/usr/bin/ssh", "-F", "/etc/uptime-kuma-backup/ssh_config", "kuma-backup-source"]


def check_restore(archive, directory):
    # Restore all regular files in private scratch. Never start monitor workers.
    with tarfile.open(archive, "r:") as tar:
        for member in tar:
            path = Path(member.name)
            if (path.parts[:1] != ("data",) or ".." in path.parts
                    or not (member.isfile() or member.isdir())):
                raise ValueError("unexpected archive member")
            # Scratch needs contents only. Never apply archive ownership or permissions.
            target = directory / path
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True, mode=0o700)
            else:
                target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
                with tar.extractfile(member) as source, target.open("xb") as output:
                    shutil.copyfileobj(source, output)
    database = directory / "data/kuma.db"
    with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as db:
        if db.execute("pragma integrity_check").fetchall() != [("ok",)]:
            raise ValueError("restored SQLite integrity check failed")
        counts = {}
        for table in ("monitor", "status_page", "group", "monitor_group", "monitor_notification"):
            counts[table] = db.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0]
        if not all(counts.values()):
            raise ValueError(f"expected populated monitoring configuration, observed {counts}")
        for table, links in (("group", (("status_page_id", "status_page"),)),
                             ("monitor_group", (("monitor_id", "monitor"), ("group_id", "group"))),
                             ("monitor_notification", (("monitor_id", "monitor"), ("notification_id", "notification")))):
            for column, parent in links:
                if db.execute(f'SELECT 1 FROM "{table}" c LEFT JOIN "{parent}" p ON p.id=c.{column} WHERE c.{column} IS NOT NULL AND p.id IS NULL LIMIT 1').fetchone():
                    raise ValueError(f"orphaned {table}.{column}")
    return counts


def receive(dest, command, day):
    mode = dest.lstat()
    if dest.resolve() != dest or not stat.S_ISDIR(mode.st_mode) or mode.st_uid != os.getuid() or stat.S_IMODE(mode.st_mode) != 0o700:
        raise ValueError("expected a private directory owned by the writer")
    with (dest / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        final = dest / f"{day.isoformat()}.tar"
        if final.exists():
            return
        with tempfile.TemporaryDirectory(dir=dest, prefix=".incoming-") as tmp:
            root = Path(tmp)
            archive = root / "snapshot.tar"
            with subprocess.Popen(command, stdout=subprocess.PIPE) as proc:
                try:
                    header = proc.stdout.readline(80)
                    if not re.fullmatch(rb"[a-f0-9]{64}  data\.tar\n", header):
                        raise ValueError("missing source archive checksum")
                    with archive.open("xb") as out:
                        shutil.copyfileobj(proc.stdout, out)
                        out.flush()
                        os.fsync(out.fileno())
                finally:
                    proc.stdout.close()
                if proc.wait() != 0:
                    raise RuntimeError("source export or SSH transfer failed")
            with archive.open("rb") as stream:
                if hashlib.file_digest(stream, "sha256").hexdigest().encode() != header[:64]:
                    raise ValueError("received archive checksum differs")
            restore = root / "restore"
            restore.mkdir()
            counts = check_restore(archive, restore)
            os.rename(archive, final)
            directory_fd = os.open(dest, os.O_DIRECTORY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
            print(json.dumps({"archive": final.name, "restored_counts": counts}))
        daily = sorted(p for p in dest.iterdir() if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.tar", p.name) and p.is_file() and not p.is_symlink())
        for old in daily[:-7]:
            old.unlink()


if __name__ == "__main__":
    os.umask(0o077)
    receive(DEST, SSH, datetime.date.today())
