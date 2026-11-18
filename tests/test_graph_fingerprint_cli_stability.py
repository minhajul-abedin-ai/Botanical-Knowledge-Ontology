"""End-to-end stability checks for the RDF fingerprint JSON CLI."""

import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "src" / "graph_fingerprint.py"


def _fingerprint_cli(path: Path) -> dict:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_cli_digest_ignores_blank_node_ids_prefixes_and_triple_order(tmp_path: Path):
    first = tmp_path / "first.ttl"
    second = tmp_path / "second.ttl"
    first.write_text(
        '@prefix ex: <https://example.org/> .\n'
        'ex:root ex:child _:left .\n'
        '_:left ex:value "one" ; ex:next _:right .\n'
        '_:right ex:value "two" .\n',
        encoding="utf-8",
    )
    second.write_text(
        '@prefix other: <https://example.org/> .\n'
        '_:renamedB other:value "two" .\n'
        '_:renamedA other:next _:renamedB .\n'
        '_:renamedA other:value "one" .\n'
        'other:root other:child _:renamedA .\n',
        encoding="utf-8",
    )
    a = _fingerprint_cli(first)
    b = _fingerprint_cli(second)
    assert a == b
    assert a["triple_count"] == 4


def test_cli_digest_changes_for_nonisomorphic_graph_with_same_triple_count(tmp_path: Path):
    first = tmp_path / "linked.ttl"
    second = tmp_path / "self-loop.ttl"
    first.write_text(
        '<urn:root> <urn:child> _:a .\n'
        '_:a <urn:next> _:b .\n'
        '_:b <urn:value> "two" .\n',
        encoding="utf-8",
    )
    second.write_text(
        '<urn:root> <urn:child> _:a .\n'
        '_:a <urn:next> _:a .\n'
        '_:b <urn:value> "two" .\n',
        encoding="utf-8",
    )
    a = _fingerprint_cli(first)
    b = _fingerprint_cli(second)
    assert a["triple_count"] == b["triple_count"] == 3
    assert a["digest"] != b["digest"]
