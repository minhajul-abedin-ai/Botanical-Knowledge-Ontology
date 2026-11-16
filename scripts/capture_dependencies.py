"""Capture installed dependency versions without modifying the environment.

Run after installing requirements: python scripts/capture_dependencies.py
Output is JSON on stdout, suitable for saving as a CI artifact.
"""
import importlib.metadata
import json
import platform
import sys

DIRECT_DEPENDENCIES = ("rdflib", "networkx", "matplotlib", "pytest")


def capture():
    packages = {}
    for name in DIRECT_DEPENDENCIES:
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError as exc:
            raise RuntimeError(f"Required dependency not installed: {name}") from exc
    return {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "packages": packages,
    }


def main():
    try:
        result = capture()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
