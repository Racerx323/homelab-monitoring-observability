#!/usr/bin/env python3
"""Prepare an append-only Pi boot correction locally; never contact a target."""

import argparse
import hashlib
from pathlib import Path


def render(original, expected_sha256):
    if hashlib.sha256(original).hexdigest() != expected_sha256:
        raise ValueError("original boot file differs from the reviewed baseline")
    if not original or len(original) > 16384:
        raise ValueError("invalid boot file size")
    original.decode("ascii")
    ending = b"\r\n" if original.endswith(b"\r\n") else b"\n" if original.endswith(b"\n") else b""
    line = original[:-len(ending)] if ending else original
    if any(value < 32 and value != 9 for value in line) or b"\x7f" in line or b"#" in line:
        raise ValueError("expected one plain kernel command line")
    tokens = line.split()
    if sum(token.startswith(b"root=") for token in tokens) != 1:
        raise ValueError("expected exactly one root argument")
    for token in tokens:
        if token.startswith(b"cgroup_disable=") and b"memory" in token.split(b"=", 1)[1].split(b","):
            raise ValueError("stored memory-disable argument requires separate review")
        if token.startswith(b"cgroup_memory=") or (
            token.startswith(b"cgroup_enable=") and b"memory" in token.split(b"=", 1)[1].split(b",")
        ):
            raise ValueError("existing memory override requires reconciliation")
    return line + b" cgroup_enable=memory" + ending


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--expected-sha256", required=True)
    args = parser.parse_args()
    if args.source.is_symlink() or not args.source.is_file():
        parser.error("source must be a regular file, not a symlink")
    result = render(args.source.read_bytes(), args.expected_sha256)
    with args.destination.open("xb") as stream:
        args.destination.chmod(0o600)
        stream.write(result)
    print(hashlib.sha256(result).hexdigest())


if __name__ == "__main__":
    main()
