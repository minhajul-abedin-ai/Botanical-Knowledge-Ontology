"""Protect the documented fingerprint JSON contract against accidental format changes."""
import json
import re
from pathlib import Path

from rdflib import Graph
from rdflib.compare import to_isomorphic

from src.graph_fingerprint import fingerprint


def test_fingerprint_json_schema_and_decimal_digest(tmp_path: Path):
    ontology = tmp_path / "sample.ttl"
    ontology.write_text('<urn:subject> <urn:predicate> "value" .\n', encoding="utf-8")

    payload = fingerprint(ontology)
    assert set(payload) == {"algorithm", "triple_count", "digest"}
    assert payload["algorithm"] == "rdflib-isomorphic-sha256"
    assert type(payload["triple_count"]) is int
    assert payload["triple_count"] == 1
    assert type(payload["digest"]) is str
    assert re.fullmatch(r"(?:0|[1-9][0-9]*)", payload["digest"])

    graph = Graph()
    graph.parse(ontology, format="turtle")
    assert payload["digest"] == str(to_isomorphic(graph).graph_digest())
    assert json.loads(json.dumps(payload)) == payload
