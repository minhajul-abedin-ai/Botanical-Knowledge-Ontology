"""Evidence grounding regression tests for direct RDF assertion Q&A."""
from pathlib import Path
import sys
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from grounded_answers import answer

def graph():
    return Graph().parse(ROOT / "ontology" / "botanical_ontology.ttl", format="turtle")

def test_carrot_growth_evidence():
    result = answer(graph(), "How many days does carrot grow?")
    assert result["status"] == "grounded"
    assert "70" in result["answer"]
    assert any(item["predicate"].endswith("#growthTimeDays") and item["object"] == "70" for item in result["evidence"])

def test_carrot_color_and_vitamin_a():
    result = answer(graph(), "What colour is carrot and does it have vitamin A?")
    assert result["status"] == "grounded"
    assert len(result["evidence"]) == 2
    assert "Orange" in result["answer"]
    assert "true" in result["answer"]

def test_missing_fact_does_not_hallucinate():
    result = answer(graph(), "What colour is radish?")
    assert result["status"] == "unknown"
    assert result["evidence"] == []
    assert "unknown" in result["answer"]

def test_unknown_crop_is_unsupported():
    result = answer(graph(), "How many days does banana grow?")
    assert result["status"] == "unsupported"
    assert result["evidence"] == []

def test_multiple_crops_unsupported():
    result = answer(graph(), "How many days does carrot and radish grow?")
    assert result["status"] == "unsupported"
    assert result["evidence"] == []

def test_word_boundary_prevents_substring_match():
    result = answer(graph(), "How many days does scarrot grow?")
    assert result["status"] == "unsupported"

def test_unrelated_question_unsupported():
    result = answer(graph(), "What is the price of carrot?")
    assert result["status"] == "unsupported"
    assert result["evidence"] == []
