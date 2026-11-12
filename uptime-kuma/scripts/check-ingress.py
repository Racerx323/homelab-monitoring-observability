#!/usr/bin/env python3
"""Probe the actual guard from an unapproved container source; publish no port."""

import argparse
import ipaddress
import json
import subprocess
import uuid


def denied_counters(raw):
    result = {}
    for item in json.loads(raw)["nftables"]:
        rule = item.get("rule", {})
        name = rule.get("comment")
        if name in ("deny-v4", "deny-v6"):
            if name in result:
                raise ValueError("duplicate guard counter")
            result[name] = next(int(expr["counter"]["packets"]) for expr in rule["expr"] if "counter" in expr)
    if set(result) != {"deny-v4", "deny-v6"}:
        raise ValueError("missing native guard counters")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True)
    parser.add_argument("--ipv4", required=True)
    parser.add_argument("--ipv6", required=True)
    parser.add_argument("--port", required=True, type=int)
    args = parser.parse_args()
    if ipaddress.ip_address(args.ipv4).version != 4 or ipaddress.ip_address(args.ipv6).version != 6:
        parser.error("expected the reviewed backend addresses")
    identity = uuid.uuid4().hex
    name = "kuma-ingress-" + identity[:12]
    result = {"accepted": False}

    def run(*argv, required=True, timeout=30):
        process = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        if len(process.stdout) > 65536 or len(process.stderr) > 8192:
            raise ValueError("probe output exceeded its bound")
        if required and process.returncode:
            raise RuntimeError(f"{argv[0]} exited {process.returncode}: {process.stderr[:1000]}")
        return process

    def counters():
        return denied_counters(run("nft", "--json", "list", "table", "inet", "uptime_kuma").stdout)

    program = "const cfg=" + json.dumps({"ipv4": args.ipv4, "ipv6": args.ipv6, "port": args.port}) + ";" + r'''
const net=require('node:net');
async function probe(address){
 const ssh=await new Promise(resolve=>{
  const s=net.createConnection({host:address,port:22});s.setTimeout(3000);
  s.on('connect',()=>{s.destroy();resolve(true)});
  s.on('error',()=>resolve(false));s.on('timeout',()=>{s.destroy();resolve(false)});
 });
 let denied=false;
 try{await fetch(`http://${address.includes(':')?'['+address+']':address}:${cfg.port}/`,{signal:AbortSignal.timeout(3000)})}
 catch(e){denied=e.name==='TimeoutError'||e.name==='AbortError'}
 return {ssh_reachable:ssh,http_timed_out:denied};
}
(async()=>{console.log(JSON.stringify({ipv4:await probe(cfg.ipv4),ipv6:await probe(cfg.ipv6)}));process.exit(0)})().catch(()=>process.exit(3));
'''
    try:
        result["before"] = counters()
        client = run("podman", "run", "--rm", "--timeout", "45", "--name", name,
                     "--label", "homelab.uptime-kuma.ingress=" + identity,
                     "--network", "uptime-kuma", "--pull", "never", "--read-only",
                     "--user", "1000:1000", "--cap-drop", "all", "--security-opt", "no-new-privileges",
                     "--memory", "64m", "--memory-swap", "64m", "--pids-limit", "32", "--cpus", "1",
                     "--entrypoint", "node", args.image, "-e", program, timeout=45)
        result["client"] = json.loads(client.stdout)
        result["after"] = counters()
        for family, counter in (("ipv4", "deny-v4"), ("ipv6", "deny-v6")):
            if (result["client"][family] != {"ssh_reachable": True, "http_timed_out": True}
                    or result["after"][counter] <= result["before"][counter]):
                raise RuntimeError("denial/management-path/counter observations disagree for " + family)
        result["accepted"] = True
    except Exception as error:
        result["error"] = str(error)[:2000]
    finally:
        try:
            exists = run("podman", "container", "exists", name, required=False)
            if exists.returncode == 0:
                info = json.loads(run("podman", "inspect", name).stdout)[0]
                if info["Config"]["Labels"].get("homelab.uptime-kuma.ingress") != identity:
                    raise RuntimeError("refusing cleanup without the exact task label")
                run("podman", "rm", "--force", name)
            elif exists.returncode != 1:
                raise RuntimeError("container cleanup state unknown")
            result["container_removed"] = True
        except Exception as error:
            result["accepted"] = False
            result["cleanup_error"] = str(error)[:1000]
        print(json.dumps(result))
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
