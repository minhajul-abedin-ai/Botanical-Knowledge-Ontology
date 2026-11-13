import sys
from pathlib import Path

import pytest
from rdflib import Graph, Literal, Namespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from export_query_evidence import evidence_for_query

EX = Namespace("https://example.org/")
QUERY = """PREFIX ex: <https://example.org/>
SELECT ?plant ?days WHERE { ?plant ex:growthDays ?days } ORDER BY ?days"""


def sample():
    graph = Graph()
    graph.add((EX.carrot, EX.growthDays, Literal(70)))
    graph.add((EX.radish, EX.growthDays, Literal(25)))
    return graph


def test_select_results():
    output = evidence_for_query(sample(), QUERY)
    assert [row["days"] for row in output["rows"]] == ["25", "70"]
    assert not output["truncated"]


def test_row_limit():
    output = evidence_for_query(sample(), QUERY, max_rows=1)
    assert len(output["rows"]) == 1
    assert output["truncated"]


@pytest.mark.parametrize("limit", [0, 101])
def test_invalid_limits(limit):
    with pytest.raises(ValueError):
        evidence_for_query(sample(), QUERY, max_rows=limit)


def test_reject_non_select():
    with pytest.raises(ValueError):
        evidence_for_query(sample(), "CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o }")
