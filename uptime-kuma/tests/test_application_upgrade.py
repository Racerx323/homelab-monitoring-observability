import importlib.util
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "operations/application-upgrade"))
import release
import store_backup
import upgrade

spec = importlib.util.spec_from_file_location("nightly", HERE / "operations/nightly-backup/receive.py")
nightly = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nightly)


class ReleaseChecks(unittest.TestCase):
    def test_discovery_and_delivery(self):
        with tempfile.TemporaryDirectory() as work:
            state = Path(work) / "last.json"
            info = {"prerelease": False, "draft": False, "tag_name": "2.5.10", "html_url": "notes"}
            image = {"local_image_id": "image", "image": "digest"}
            calls = []

            def request(url, *args):
                if args:
                    calls.append(args)
                    return (503 if len(calls) == 1 else 200), b""
                return 200, json.dumps(info).encode()

            with patch.object(release, "installed", return_value="2.5.9"), patch.object(release, "installed_id", return_value="image"), \
                    patch.object(release, "STATE", state), patch.object(release, "request", side_effect=request), \
                    patch.object(release, "candidate", return_value=image):
                release.check(True)
                self.assertFalse(state.exists())
                with self.assertRaises(RuntimeError):
                    release.check(False)
                self.assertFalse(state.exists())
                release.check(False)
                release.check(False)
                self.assertEqual(len(calls), 2)
                update = json.loads(calls[-1][1])
                self.assertEqual(update["format"], "text")
                self.assertIn("\n\nNext step\n\n- ", update["body"])
                self.assertIn("\n\nRelease notes\nnotes", update["body"])
                release.check(False, confirmation=True)
                confirmation = json.loads(calls[-1][1])
                self.assertIn("delivery test", confirmation["title"])
                self.assertIn("- Installed version: 2.5.9\n- Latest stable version: 2.5.10", confirmation["body"])
                self.assertTrue(confirmation["body"].endswith("\n\nRelease notes\nnotes"))
                self.assertNotIn("digest", confirmation["body"])
                info["tag_name"] = "2.5.9"
                release.check(False)
                info["prerelease"] = True
                with self.assertRaises(ValueError):
                    release.check(False)
                self.assertEqual(len(calls), 3)

    def test_missing_arm64(self):
        responses = [(200, b'{"token":"example"}'), (200, b'{"manifests":[]}')]
        with patch.object(release, "request", side_effect=responses), self.assertRaisesRegex(ValueError, "arm64"):
            release.candidate("2.5.10")


def populate(data):
    data.mkdir()
    with sqlite3.connect(data / "kuma.db") as db:
        db.executescript("""
            CREATE TABLE monitor(id,name,type,active,interval,retry_interval,maxretries,timeout);
            INSERT INTO monitor VALUES(1,'DNS','dns',1,1,1,0,1),(2,'paused','http',0,1,1,0,1);
            CREATE TABLE status_page(id,slug,title,published);
            INSERT INTO status_page VALUES(1,'one','The fleet',1),(2,'empty','Empty',0);
            CREATE TABLE "group"(id,status_page_id,name,weight);
            INSERT INTO "group" VALUES(3,1,'services',100);
            CREATE TABLE monitor_group(group_id,monitor_id,weight);
            INSERT INTO monitor_group VALUES(3,1,8);
            CREATE TABLE notification(id);
            INSERT INTO notification VALUES(4);
            CREATE TABLE monitor_notification(monitor_id,notification_id);
            INSERT INTO monitor_notification VALUES(1,4);
            CREATE TABLE heartbeat(id,monitor_id,time,status);
            INSERT INTO heartbeat VALUES(1,1,'2000-01-01 00:00:00',1);
        """)


class UpgradeChecks(unittest.TestCase):
    def exercise(self, failure):
        with tempfile.TemporaryDirectory() as work:
            base = Path(work)
            data = base / "data"
            populate(data)
            root = base / "run"
            root.mkdir()
            offnode = base / "offnode"
            offnode.mkdir()
            quad = base / "kuma.container"
            old = {"release": "2.5.9", "local_image_id": "sha256:old"}
            new = {"release": "2.5.10", "local_image_id": "sha256:new", "image": "candidate"}
            quad.write_text("Image=sha256:old\nPull=never\n")
            initial = upgrade.inventory(data)
            active = []
            native = upgrade.run

            def run(*args, **kwargs):
                if args[0] in ("du", "tar"):
                    return native(*args, **kwargs)
                results = {"hostname": "j2-svpi3bmf", "uname": "aarch64"}
                if args[:2] == ("podman", "ps"):
                    return ""
                if "{{.Size}}" in args:
                    return "4096"
                if "{{.Store.GraphRoot}}" in args:
                    return str(base)
                if "inspect" in args:
                    return '[{"Architecture":"arm64","Id":"sha256:new"}]'
                if "Requires" in args:
                    return "uptime-kuma-firewall.service uptime-kuma-startup-permit.service"
                if "ActiveState" in args:
                    return "inactive"
                return results.get(args[0], "0")

            def handoff(where, event, timeout=600):
                if event == "backup-verified":
                    record = json.loads((root / "backup-ready").read_text())
                    if failure == "backup":
                        record["sha256"] = "wrong"
                    with (root / "data.tar").open("rb") as source:
                        store_backup.receive(offnode, "a" * 32, record, source, nightly.check_restore)
                    (where / event).write_text(record["sha256"])

            def start(image, rows):
                active.append(image)
                if image == new and failure == "candidate":
                    with sqlite3.connect(data / "kuma.db") as db:
                        db.execute("UPDATE monitor_group SET monitor_id=2")
                if upgrade.inventory(data) != rows:
                    raise ValueError("inventory changed")
                return {"down": []}

            with patch.multiple(upgrade, QUAD=quad, DATA=data), patch.object(upgrade, "installed", return_value=old["release"]), \
                    patch.object(upgrade, "installed_id", return_value=old["local_image_id"]), patch.object(upgrade, "run", side_effect=run), \
                    patch.object(upgrade, "pages"), patch.object(upgrade, "start_check", side_effect=start), \
                    patch.object(upgrade, "wait_ack", side_effect=handoff), patch("time.clock_gettime", return_value=600):
                if failure:
                    with self.assertRaises(ValueError):
                        upgrade.transaction(root, old, new)
                else:
                    upgrade.transaction(root, old, new)
            result = json.loads((root / "result").read_text())
            self.assertEqual(result["state"], "restored" if failure else "accepted")
            self.assertEqual(active[-1], old if failure else new)
            self.assertIn(active[-1]["local_image_id"], quad.read_text())
            self.assertEqual(upgrade.inventory(data), initial)
            self.assertEqual(bool(list(offnode.glob("upgrade-*.tar"))), failure != "backup")
            self.assertEqual((base / "run-failed-data").exists(), failure == "candidate")

    def test_success(self):
        self.exercise(None)

    def test_rejected_archive(self):
        self.exercise("backup")

    def test_candidate_failure(self):
        self.exercise("candidate")

    def test_stale_then_fresh_down(self):
        with tempfile.TemporaryDirectory() as work:
            data = Path(work) / "data"
            populate(data)
            with patch.object(upgrade, "DATA", data), patch.object(upgrade, "installed", return_value="v"), \
                    patch.object(upgrade, "installed_id", return_value="id"), patch.object(upgrade, "pages"), \
                    patch.object(upgrade, "urlopen") as response:
                response.return_value.__enter__.return_value.status = 200
                args = ({"release": "v", "local_image_id": "id"}, upgrade.inventory(data), -1000, "2026-01-01")
                with self.assertRaisesRegex(TimeoutError, "fresh"):
                    upgrade.verify(*args)
                with sqlite3.connect(data / "kuma.db") as db:
                    db.execute("INSERT INTO heartbeat VALUES(2,1,'2026-01-02',0)")
                self.assertEqual(upgrade.verify(*args)["down"], [1])


if __name__ == "__main__":
    unittest.main()
