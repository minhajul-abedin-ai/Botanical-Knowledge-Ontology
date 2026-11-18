"""Subprocess contract tests for the RDF fingerprint command-line interface."""

import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "src" / "graph_fingerprint.py"


def run_cli(path: Path):
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path)],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_emits_parseable_json_with_expected_fields(tmp_path: Path):
    ontology = tmp_path / "valid.ttl"
    ontology.write_text('<urn:s> <urn:p> "value" .', encoding="utf-8")
    result = run_cli(ontology)
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert set(payload) == {"algorithm", "digest", "triple_count"}
    assert payload["algorithm"] == "rdflib-isomorphic-sha256"
    assert payload["triple_count"] == 1
    assert isinstance(payload["digest"], str) and payload["digest"].isdigit()


def test_cli_missing_file_fails_without_json(tmp_path: Path):
    result = run_cli(tmp_path / "missing.ttl")
    assert result.returncode != 0
    assert result.stdout.strip() == ""
    assert result.stderr.strip()


def test_cli_invalid_turtle_fails_without_json(tmp_path: Path):
    ontology = tmp_path / "invalid.ttl"
    ontology.write_text("this is not valid Turtle !!!", encoding="utf-8")
    result = run_cli(ontology)
    assert result.returncode != 0
    assert result.stdout.strip() == ""
    assert result.stderr.strip()
