"""Detect RDFLib upgrades that change persisted fingerprint digest values.

These are compatibility canaries from RDFLib 7.5.0, not a claim that RDFLib
promises version-independent digests. A failure requires investigation before
comparing fingerprints persisted by different deployments.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "src" / "graph_fingerprint.py"


@pytest.mark.parametrize(
    ("turtle", "expected_digest"),
    [
        (
            '<urn:r> <urn:p> _:a, _:b . _:a <urn:p> _:b . _:b <urn:p> _:a .',
            "140019511831678940013272293025807993045829448515198258166051200257339832473348",
        ),
        (
            '<urn:r> <urn:p> _:a, _:b . _:a <urn:q> "x" . _:b <urn:q> "x" .',
            "318407736385603807689907793525089077723667411733002168093865379262206124458845",
        ),
    ],
    ids=["symmetric-cycle", "indistinguishable-twins"],
)
def test_fingerprint_digest_compatibility_canary(tmp_path: Path, turtle: str, expected_digest: str):
    ontology = tmp_path / "fixture.ttl"
    ontology.write_text(turtle + "\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(ontology)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["triple_count"] == 4
    assert payload["digest"] == expected_digest
