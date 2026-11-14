from pathlib import Path
from src.graph_fingerprint import fingerprint


def test_isomorphic_blank_nodes_have_same_fingerprint(tmp_path: Path):
    a = tmp_path / "a.ttl"
    b = tmp_path / "b.ttl"
    a.write_text('@prefix ex: <https://example.org/> . ex:x ex:p [ ex:q "v" ] .')
    b.write_text('@prefix e: <https://example.org/> . e:x e:p [ e:q "v" ] .')
    assert fingerprint(a) == fingerprint(b)
    assert fingerprint(a)["triple_count"] == 2


def test_changed_literal_changes_digest(tmp_path: Path):
    a = tmp_path / "a.ttl"
    b = tmp_path / "b.ttl"
    a.write_text('<urn:s> <urn:p> "before" .')
    b.write_text('<urn:s> <urn:p> "after" .')
    assert fingerprint(a)["digest"] != fingerprint(b)["digest"]
