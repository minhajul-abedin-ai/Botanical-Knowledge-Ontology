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


def test_blank_node_renaming_and_triple_reordering_preserve_digest(tmp_path: Path):
    a = tmp_path / "named-a.ttl"
    b = tmp_path / "named-b.ttl"
    a.write_text('''@prefix ex: <https://example.org/> .
ex:root ex:child _:first .
_:first ex:value "one" ; ex:next _:second .
_:second ex:value "two" .
''')
    b.write_text('''@prefix other: <https://example.org/> .
_:beta other:value "two" .
_:alpha other:next _:beta .
_:alpha other:value "one" .
other:root other:child _:alpha .
''')
    assert fingerprint(a) == fingerprint(b)
    assert fingerprint(a)["triple_count"] == 4


def test_blank_node_edge_change_changes_digest(tmp_path: Path):
    a = tmp_path / "edge-a.ttl"
    b = tmp_path / "edge-b.ttl"
    a.write_text('''@prefix ex: <https://example.org/> .
ex:root ex:child _:a .
_:a ex:value "one" ; ex:next _:b .
_:b ex:value "two" .
''')
    b.write_text('''@prefix ex: <https://example.org/> .
ex:root ex:child _:a .
_:a ex:value "one" ; ex:next _:a .
_:b ex:value "two" .
''')
    assert fingerprint(a)["digest"] != fingerprint(b)["digest"]
