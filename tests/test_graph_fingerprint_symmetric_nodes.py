"""Regression tests for symmetric RDF blank-node canonicalization via the CLI."""

import json
import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "src" / "graph_fingerprint.py"


def _cli(path: Path) -> dict:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


@pytest.mark.parametrize(
    ("first", "second"),
    [
        (
            '<urn:r> <urn:p> _:a, _:b . _:a <urn:p> _:b . _:b <urn:p> _:a .',
            '_:y <urn:p> _:x . <urn:r> <urn:p> _:y, _:x . _:x <urn:p> _:y .',
        ),
        (
            '<urn:r> <urn:p> _:a, _:b . _:a <urn:q> "x" . _:b <urn:q> "x" .',
            '_:z <urn:q> "x" . <urn:r> <urn:p> _:z, _:w . _:w <urn:q> "x" .',
        ),
    ],
    ids=["symmetric-cycle", "indistinguishable-twins"],
)
def test_symmetric_blank_node_renaming_preserves_cli_digest(
    tmp_path: Path, first: str, second: str
):
    a = tmp_path / "first.ttl"
    b = tmp_path / "second.ttl"
    a.write_text(first + "\n", encoding="utf-8")
    b.write_text(second + "\n", encoding="utf-8")
    original = _cli(a)
    renamed = _cli(b)
    assert original == renamed
    assert original["triple_count"] == 4
