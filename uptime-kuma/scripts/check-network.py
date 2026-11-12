#!/usr/bin/env python3
"""Reject container subnets that overlap another host interface's routes."""

import argparse
import ipaddress
import json
import subprocess


def conflicts(network, routes):
    if network["driver"] != "bridge" or not network["ipv6_enabled"]:
        raise ValueError("expected the dedicated dual-stack bridge")
    subnets = [ipaddress.ip_network(item["subnet"]) for item in network["subnets"]]
    if {subnet.version for subnet in subnets} != {4, 6}:
        raise ValueError("expected both address families")
    found = []
    for route in routes:
        if route.get("dev") == network["network_interface"] or route.get("dst", "default") == "default":
            continue
        prefix = ipaddress.ip_network(route["dst"], strict=False)
        if prefix.prefixlen and any(prefix.version == subnet.version and prefix.overlaps(subnet) for subnet in subnets):
            found.append({"route": str(prefix), "device": route.get("dev")})
    return found


def command(*argv):
    result = subprocess.run(argv, capture_output=True, text=True, check=True, timeout=15)
    if len(result.stdout) > 65536 or len(result.stderr) > 4096:
        raise ValueError("network observation exceeded its bound")
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--network", required=True)
    args = parser.parse_args()
    network = command("podman", "network", "inspect", args.network)[0]
    routes = command("ip", "-4", "--json", "route", "show", "table", "all")
    routes += command("ip", "-6", "--json", "route", "show", "table", "all")
    found = conflicts(network, routes)
    print(json.dumps({"network": network["name"], "subnets": network["subnets"], "conflicts": found}))
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
