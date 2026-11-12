#!/usr/bin/env python3
"""Read bounded service observations on the Kuma host; emit no credentials."""

import argparse
import json
from pathlib import Path
import sqlite3
import subprocess
from urllib.parse import quote
from urllib.request import ProxyHandler, build_opener


def command(*argv):
    result = subprocess.run(argv, capture_output=True, text=True, timeout=10)
    if result.returncode:
        raise RuntimeError(f"{argv[0]} returned {result.returncode}")
    if len(result.stdout) > 262144 or len(result.stderr) > 16384:
        raise RuntimeError("observation output exceeded its bound")
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-directory", required=True, type=Path)
    parser.add_argument("--port", required=True, type=int)
    parser.add_argument("--connection-uuid", required=True)
    args = parser.parse_args()
    properties = dict(line.split("=", 1) for line in command(
        "systemctl", "show", "uptime-kuma.service", "--property=ActiveState,SubState,ControlGroup,NRestarts"
    ).splitlines())
    group = (Path("/sys/fs/cgroup") / properties["ControlGroup"].lstrip("/")).resolve()
    if not group.is_relative_to("/sys/fs/cgroup/system.slice"):
        raise RuntimeError("unexpected service cgroup")
    limits = {name: (group / name).read_text().strip() for name in (
        "memory.max", "memory.high", "memory.current", "memory.swap.max", "cpu.max", "pids.max")}
    memory_events = {key: int(value) for key, value in
                     (line.split() for line in (group / "memory.events").read_text().splitlines())}
    container = json.loads(command("podman", "inspect", "uptime-kuma"))[0]
    image = json.loads(command("podman", "image", "inspect", container["Image"]))[0]
    filesystem = json.loads(command("findmnt", "--json", "--target", str(args.data_directory),
                                    "--output", "TARGET,FSTYPE,OPTIONS"))["filesystems"][0]
    radios = json.loads(command("/usr/sbin/rfkill", "--json"))["rfkilldevices"]
    network = {
        "addresses": json.loads(command("ip", "--json", "address", "show", "dev", "eth0"))[0]["addr_info"],
        "ipv4_default": json.loads(command("ip", "-4", "--json", "route", "show", "default")),
        "ipv6_default": json.loads(command("ip", "-6", "--json", "route", "show", "default")),
        "active_connections": command("nmcli", "--terse", "--fields", "UUID,DEVICE",
                                      "connection", "show", "--active").splitlines(),
        "methods": command("nmcli", "--get-values", "ipv4.method,ipv6.method",
                           "connection", "show", args.connection_uuid).splitlines(),
        "persistent_ipv6": command("nmcli", "--escape", "no", "--get-values", "ipv6.addresses",
                                   "connection", "show", args.connection_uuid).strip(),
        "ipv6_forwarding": Path("/proc/sys/net/ipv6/conf/all/forwarding").read_text().strip(),
        "kernel_accept_ra": Path("/proc/sys/net/ipv6/conf/eth0/accept_ra").read_text().strip(),
    }
    opener = build_opener(ProxyHandler({}))
    http = {}
    for address in ("127.0.0.1", "[::1]"):
        with opener.open(f"http://{address}:{args.port}/", timeout=5) as response:
            http[address] = response.status
    database = args.data_directory / "kuma.db"
    if database.is_symlink() or not database.is_file():
        raise RuntimeError("database must be a regular file")
    with sqlite3.connect("file:" + quote(str(database)) + "?mode=ro", uri=True, timeout=5) as connection:
        counts = {name: connection.execute('SELECT COUNT(*) FROM "' + name + '"').fetchone()[0]
                  for name in ("user", "monitor", "notification")}
        counts["active_users"] = connection.execute('SELECT COUNT(*) FROM "user" WHERE active = 1').fetchone()[0]
        auth = connection.execute("SELECT value FROM setting WHERE key = 'disableAuth'").fetchone()
    loopback_proxy = {}
    for role in ('socket', 'service'):
        loopback_proxy[role] = dict(line.split('=', 1) for line in command(
            'systemctl', 'show', 'uptime-kuma-loopback.' + role,
            '--property=ActiveState,MainPID,MemoryMax,MemorySwapMax,MemoryPeak,Listen').splitlines())
    observation = {
        "unit": properties, "limits": limits, "memory_events": memory_events,
        "loopback_proxy": loopback_proxy,
        "architecture": image["Architecture"], "image_digest": image.get("Digest"),
        "image_id": "sha256:" + image["Id"].removeprefix("sha256:"),
        "uid": int(command("podman", "exec", "uptime-kuma", "id", "-u").strip()),
        "release": command("podman", "exec", "uptime-kuma", "node", "-p",
                           'require("/app/package.json").version').strip(),
        "read_only_root": container["HostConfig"]["ReadonlyRootfs"],
        "mounts": [{key: mount.get(key) for key in ("Source", "Destination", "RW")}
                   for mount in container["Mounts"]],
        "port_bindings": container["HostConfig"]["PortBindings"],
        "networks": sorted(container["NetworkSettings"]["Networks"]),
        "filesystem": filesystem, "radio": radios, "network": network, "http": http, "counts": counts,
        "authentication_disabled": bool(json.loads(auth[0])) if auth and isinstance(auth[0], str)
        else bool(auth[0]) if auth else False,
    }
    print(json.dumps(observation, sort_keys=True))


if __name__ == "__main__":
    main()
