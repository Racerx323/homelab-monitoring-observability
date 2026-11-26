#!/usr/bin/python3
"""Discover stable Kuma ARM64 images and notify through the fleet Apprise API."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import time
from urllib.request import Request, urlopen

REPO = "louislam/uptime-kuma"
REGISTRY = f"https://registry-1.docker.io/v2/{REPO}/manifests/"
DIGEST = r"sha256:[0-9a-f]{64}"
STATE = Path("/var/lib/kuma-release-check/last.json")


def request(url, headers=None, data=None):
    with urlopen(Request(url, data=data, headers=headers or {}), timeout=20) as response:
        body = response.read(2_000_001)
        if len(body) > 2_000_000:
            raise ValueError("release API response exceeds limit")
        return response.status, body


def version(value):
    if not re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", value):
        raise ValueError("expected a stable three-component version")
    return tuple(map(int, value.split(".")))


def candidate(release):
    import hashlib
    version(release)
    token = json.loads(request("https://auth.docker.io/token?service=registry.docker.io"
                               f"&scope=repository:{REPO}:pull")[1])["token"]
    headers = {"Authorization": f"Bearer {token}", "Accept": ", ".join([
        "application/vnd.oci.image.index.v1+json", "application/vnd.docker.distribution.manifest.list.v2+json",
        "application/vnd.oci.image.manifest.v1+json", "application/vnd.docker.distribution.manifest.v2+json"])}
    index = json.loads(request(REGISTRY + release + "-slim-rootless", headers)[1])
    matches = [m["digest"] for m in index["manifests"] if m["platform"]["os"] == "linux"
               and m["platform"]["architecture"] == "arm64" and m["platform"].get("variant", "v8") == "v8"]
    if len(matches) != 1 or not re.fullmatch(DIGEST, matches[0]):
        raise ValueError("release has no unique linux/arm64 image")
    body = request(REGISTRY + matches[0], headers)[1]
    if "sha256:" + hashlib.sha256(body).hexdigest() != matches[0]:
        raise ValueError("registry manifest digest mismatch")
    local_id = json.loads(body)["config"]["digest"]
    if not re.fullmatch(DIGEST, local_id):
        raise ValueError("invalid image config digest")
    return {"release": release, "image": f"docker.io/{REPO}@{matches[0]}", "local_image_id": local_id}


def installed():
    return subprocess.check_output(["podman", "exec", "uptime-kuma", "node", "-p",
                                    "require('/app/package.json').version"], timeout=15, text=True).strip()


def check(dry, confirmation=False):
    current = installed()
    info = json.loads(request(f"https://api.github.com/repos/{REPO}/releases/latest")[1])
    latest = info["tag_name"].removeprefix("v")
    if info["prerelease"] or info["draft"]:
        raise ValueError("upstream latest release is not stable")
    order = version(latest)
    if order < version(current) and not confirmation:
        print("installed version is newer")
        return
    image = candidate(latest)
    same = order == version(current)
    key = [current, latest, image["image"]]
    prior = json.loads(STATE.read_text()) if STATE.exists() else {}
    reshaped = prior.get("key", [])[:2] == key[:2] and prior.get("key") != key
    if same and installed_id() == image["local_image_id"] and not reshaped and not confirmation:
        print("current")
        return
    now = int(time.time())
    if confirmation:
        title = "[Uptime Kuma] Release checker delivery test"
        action = "Confirm receipt at your notification destinations."
    elif same or reshaped:
        title = "[Uptime Kuma] Release image changed"
        action = "Review the changed ARM64 image digest in the checker journal before approving an upgrade."
    else:
        title = "[Uptime Kuma] Update available"
        action = "Review the release notes before scheduling the upgrade."
    if not confirmation and prior.get("key") == key and now - prior["sent"] < 518400:
        print("already notified")
        return
    print(title, current, latest, image["image"], flush=True)
    if dry:
        return
    body = (
        "Summary\n\n"
        "- Host: j2-svpi3bmf\n"
        f"- Installed version: {current}\n"
        f"- Latest stable version: {latest}\n\n"
        f"Next step\n\n- {action}"
    )
    body += f"\n\nRelease notes\n{info['html_url']}"
    message = {"type": "info", "format": "text", "title": title, "body": body}
    status, _ = request("http://10.1.3.83:8000/notify/apprise", {"Content-Type": "application/json"},
                        json.dumps(message).encode())
    if status != 200:
        raise RuntimeError(f"Apprise returned HTTP {status}")
    if not confirmation:
        temp = STATE.with_suffix(".new")
        temp.write_text(json.dumps({"key": key, "sent": now}))
        os.replace(temp, STATE)


def installed_id():
    return "sha256:" + subprocess.check_output(["podman", "inspect", "--format", "{{.Image}}",
                                                "uptime-kuma"], text=True, timeout=15).strip().removeprefix("sha256:")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--prepare", metavar="VERSION")
    modes.add_argument("--dry-run", action="store_true")
    modes.add_argument("--confirm-delivery", action="store_true")
    args = parser.parse_args()
    if args.prepare:
        print(json.dumps(candidate(args.prepare)))
    else:
        check(args.dry_run, args.confirm_delivery)
