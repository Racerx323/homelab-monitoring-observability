#!/usr/bin/env python3
"""Qualify the rendered ingress guard in disposable namespaces, including DNAT."""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import threading
import time

from jinja2 import Environment, FileSystemLoader, StrictUndefined
import yaml


def run(*argv, data=None):
    result = subprocess.run(argv, input=data, capture_output=True, text=True, timeout=12)
    if result.returncode:
        raise RuntimeError(f"{argv[0]} exited {result.returncode}: {result.stderr[:4096]}")
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--guard", type=Path, required=True,
                        help="Exact rendered ingress.nft candidate")
    parser.add_argument("--host-netns", required=True,
                        help="Network namespace identity captured before unshare")
    args = parser.parse_args()
    if os.readlink("/proc/self/ns/net") == args.host_netns:
        parser.error("run under unshare --user --map-root-user --net")
    component = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("ingress_probe", component / "scripts/check-ingress.py")
    ingress = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ingress)
    manifest = yaml.safe_load((component / "manifests/deployment.yaml").read_text())
    env = Environment(loader=FileSystemLoader(component / "ansible/templates"),
                      undefined=StrictUndefined, keep_trailing_newline=True)
    rules = args.guard.read_text()
    if rules != env.get_template("ingress.nft.j2").render(**manifest):
        parser.error("guard differs from the current manifest/template render")
    host4, host6 = manifest["host"]["ipv4"], manifest["host"]["permanent_ula"]
    port = manifest["application"]["port"]
    allowed = manifest["proxy"]["backend_ipv4_sources"] + manifest["proxy"]["backend_ipv6_sources"]
    denied = ["10.1.3.83", "fd36:5aa8:6971:1::83"]
    children, listeners = [], []
    results = {}
    try:
        run("ip", "link", "set", "lo", "up")
        for role in ("client", "backend"):
            child = subprocess.Popen(["unshare", "--net", "sleep", "180"])
            children.append(child)
            for _ in range(100):
                if child.poll() is not None:
                    raise RuntimeError("child namespace exited")
                if os.readlink(f"/proc/{child.pid}/ns/net") != os.readlink("/proc/self/ns/net"):
                    break
                time.sleep(0.01)
            else:
                raise RuntimeError("child namespace was not created")
            ns = ["nsenter", "--target", str(child.pid), "--net"]
            run("ip", "link", "add", role + "h", "type", "veth", "peer", "name", role + "n")
            run("ip", "link", "set", role + "n", "netns", str(child.pid))
            run("ip", "link", "set", role + "h", "up")
            run(*ns, "ip", "link", "set", "lo", "up")
            run(*ns, "ip", "link", "set", role + "n", "up")
            host_addresses = [host4 + "/22", host6 + "/64"] if role == "client" else ["192.0.2.1/30", "fd00:abcd:75::1/64"]
            child_addresses = [a + ("/64" if ":" in a else "/22") for a in allowed + denied] if role == "client" else ["192.0.2.2/30", "fd00:abcd:75::2/64"]
            for addresses, prefix, interface in ((host_addresses, [], role + "h"), (child_addresses, ns, role + "n")):
                for address in addresses:
                    run(*prefix, "ip", "address", "add", address, "dev", interface,
                        *(["nodad"] if ":" in address else []))
            if role == "backend":
                run(*ns, "ip", "route", "add", "default", "via", "192.0.2.1")
                run(*ns, "ip", "-6", "route", "add", "default", "via", "fd00:abcd:75::1")
        client = ["nsenter", "--target", str(children[0].pid), "--net"]
        backend = ["nsenter", "--target", str(children[1].pid), "--net"]
        # Link-local DAD must finish before forwarded IPv6 can resolve peers.
        deadline = time.monotonic() + 5
        for prefix in ([], client, backend):
            while any("tentative" in address.get("flags", [])
                      or address.get("tentative", False)
                      for device in json.loads(run(*prefix, "ip", "-6", "-j", "address"))
                      for address in device["addr_info"]):
                if time.monotonic() >= deadline:
                    raise RuntimeError("fixture IPv6 duplicate-address detection did not settle")
                time.sleep(0.05)
        run("sysctl", "-qw", "net.ipv4.ip_forward=1", "net.ipv6.conf.all.forwarding=1")
        run("nft", "-f", "-", data=f"""table inet fixture_nat {{
 chain ports {{ type nat hook prerouting priority dstnat; policy accept;
  ip daddr {host4} tcp dport {port} dnat ip to 192.0.2.2:{port}
  ip6 daddr {host6} tcp dport {port} dnat ip6 to [fd00:abcd:75::2]:{port}
 }}
}}
table inet fixture_unrelated {{
 chain input {{ type filter hook input priority filter; policy accept;
 }}
}}
""")
        unrelated = run("nft", "-j", "list", "table", "inet", "fixture_unrelated")
        run("nft", "--check", "-f", "-", data=rules)
        run("nft", "-f", "-", data=rules)
        # Applying the candidate twice must preserve unrelated tables and ports.
        run("nft", "-f", "-", data=rules)
        assert run("nft", "-j", "list", "table", "inet", "fixture_unrelated") == unrelated

        server_code = """import socket,threading,time
def serve(family,address):
 s=socket.socket(family);s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
 if family==socket.AF_INET6:s.setsockopt(socket.IPPROTO_IPV6,socket.IPV6_V6ONLY,1)
 s.bind((address,3001));s.listen()
 def loop():
  while True:
   c,_=s.accept();c.sendall(b'backend');c.close()
 threading.Thread(target=loop,daemon=True).start()
serve(socket.AF_INET,'192.0.2.2');serve(socket.AF_INET6,'fd00:abcd:75::2')
print('ready',flush=True);time.sleep(150)
"""
        server = subprocess.Popen([*backend, sys.executable, "-c", server_code],
                                  stdout=subprocess.PIPE, text=True)
        children.append(server)
        assert server.stdout.readline().strip() == "ready"
        for family, address in ((socket.AF_INET, host4), (socket.AF_INET6, host6)):
            s = socket.socket(family)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if family == socket.AF_INET6:
                s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
            s.bind((address, 22)); s.listen(); listeners.append(s)
            def accept_connections(listener):
                while True:
                    try:
                        connection, _ = listener.accept()
                        connection.sendall(b"ssh-fixture"); connection.close()
                    except OSError:
                        return
            threading.Thread(target=accept_connections, args=(s,), daemon=True).start()
        probe_code = """import socket,sys
s=socket.socket(socket.AF_INET6 if ':' in sys.argv[1] else socket.AF_INET)
s.settimeout(.4);s.bind((sys.argv[1],0))
try:
 s.connect((sys.argv[2],int(sys.argv[3])));print(s.recv(32).decode())
except socket.timeout: print('dropped')
"""
        def probe(source, target_port):
            return run(*client, sys.executable, "-c", probe_code, source,
                       host6 if ":" in source else host4, str(target_port)).strip()
        for source in allowed + denied:
            observed = probe(source, port)
            if observed != ("backend" if source in allowed else "dropped"):
                print(json.dumps({"failure_source": source,
                                  "rules": run("nft", "-j", "list", "ruleset"),
                                  "host_routes": run("ip", "-6", "route"),
                                  "backend_routes": run(*backend, "ip", "-6", "route"),
                                  "host_neighbors": run("ip", "-6", "neighbor")}))
                run("nft", "delete", "table", "inet", "uptime_kuma")
                print(json.dumps({"without_guard": probe(source, port),
                                  "ssh_path": probe(source, 22)}))
            assert observed == ("backend" if source in allowed else "dropped"), (source, observed)
            assert probe(source, 22) == "ssh-fixture"
            results[source] = observed
        counts = ingress.denied_counters(run("nft", "--json", "list", "table", "inet", "uptime_kuma"))
        assert counts["deny-v4"] > 0 and counts["deny-v6"] > 0
        run("nft", "delete", "table", "inet", "uptime_kuma")
        for source in denied:
            assert probe(source, port) == "backend", "denial must be caused by the guard"
        print(json.dumps({"passed": True, "guard_sha256": hashlib.sha256(rules.encode()).hexdigest(),
                          "sources": results, "ssh_preserved": True, "dnat_both_families": True,
                          "unrelated_table_preserved": True,
                          "denied_counters": counts,
                          "scope": "Disposable local kernel namespaces, not target Podman acceptance"}))
    finally:
        for listener in listeners:
            listener.close()
        for child in reversed(children):
            if child.poll() is None:
                child.terminate()
            child.wait(timeout=5)


if __name__ == "__main__":
    main()
