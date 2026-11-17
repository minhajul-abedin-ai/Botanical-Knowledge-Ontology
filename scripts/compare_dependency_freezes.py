"""Compare pip freeze --all inventories without depending on package order.

Usage: python scripts/compare_dependency_freezes.py standard.txt replay.txt
Exit status 0 means identical normalized package records; 1 means a difference
or malformed input. This compares versions, not wheel hashes or build outputs.
"""
import argparse
import re
from pathlib import Path

RECORD = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)==([^\s]+)$")


def parse_freeze(text):
    packages = {}
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = RECORD.fullmatch(line)
        if not match:
            raise ValueError(f"line {number}: unsupported freeze record: {line!r}")
        name, version = match.groups()
        key = re.sub(r"[-_.]+", "-", name).lower()
        if key in packages:
            raise ValueError(f"line {number}: duplicate distribution: {key}")
        packages[key] = version
    if not packages:
        raise ValueError("no installed distributions found")
    return packages


def compare(left, right):
    a, b = parse_freeze(left), parse_freeze(right)
    return [(name, a.get(name), b.get(name)) for name in sorted(a.keys() | b.keys())
            if a.get(name) != b.get(name)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("standard", type=Path)
    parser.add_argument("replay", type=Path)
    args = parser.parse_args()
    try:
        differences = compare(args.standard.read_text(encoding="utf-8"),
                              args.replay.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Cannot compare inventories: {exc}\n")
    if differences:
        for name, left, right in differences:
            print(f"{name}: standard={left or '<missing>'}, replay={right or '<missing>'}")
        return 1
    print("Installed distribution names and versions match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
