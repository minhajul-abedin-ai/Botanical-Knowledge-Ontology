from pathlib import Path
import sys
from rdflib import Graph, Namespace, RDF, OWL, XSD, Literal

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from validate_ontology import validate

BOT = Namespace("https://minhajul-abedin-ai.github.io/botanical-knowledge-ontology#")
ONTOLOGY = ROOT / "ontology" / "botanical_ontology.ttl"


def graph():
    return Graph().parse(ONTOLOGY, format="turtle")


def test_validation_passes():
    assert validate() == []


def test_source_supported_carrot_facts():
    g = graph()
    assert (BOT.Carrot_ind, RDF.type, BOT.RootVegetable) in g
    assert (BOT.Carrot_ind, BOT.hasColor, Literal("Orange")) in g
    assert (BOT.Carrot_ind, BOT.growthTimeDays, Literal(70, datatype=XSD.integer)) in g
    assert (BOT.Carrot_ind, BOT.hasVitaminA, Literal(True, datatype=XSD.boolean)) in g


def test_disjointness_axioms_present():
    g = graph()
    assert (BOT.RootVegetable, OWL.disjointWith, BOT.LeafyVegetable) in g
    assert (BOT.MonocotSeed, OWL.disjointWith, BOT.DicotSeed) in g


def test_assignment_query_examples_are_represented():
    g = graph()
    fast = set(g.subjects(RDF.type, BOT.FastGrowingCrop))
    assert BOT.Bean_ind in fast
    assert BOT.Beetroot_ind in fast
    assert BOT.Spinach_ind in fast
    assert (BOT.Spinach_ind, RDF.type, BOT.HighProteinCrop) in g


def test_transitive_demo_fact_is_available():
    g = graph()
    assert (BOT.Tomato_ind, BOT.hasPart, BOT.TomatoSeed) in g
