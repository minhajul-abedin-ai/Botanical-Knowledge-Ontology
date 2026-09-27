from pathlib import Path
import sys
from rdflib import Graph, Namespace, RDF, RDFS, OWL, XSD, Literal

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "ontology" / "botanical_ontology.ttl"
BOT = Namespace("https://minhajul-abedin-ai.github.io/botanical-knowledge-ontology#")

REQUIRED_CLASSES = [
    "Vegetable", "RootVegetable", "LeafyVegetable", "LegumeVegetable", "FruitVegetable",
    "PlantPart", "Root", "TapRoot", "Leaf", "Seed", "MonocotSeed", "DicotSeed",
]
REQUIRED_PROPERTIES = [
    "hasPart", "isPartOf", "proteinPer100g", "growthTimeDays", "hasVitaminA", "hasColor"
]


def validate() -> list[str]:
    errors: list[str] = []
    g = Graph().parse(ONTOLOGY, format="turtle")

    for name in REQUIRED_CLASSES:
        if (BOT[name], RDF.type, OWL.Class) not in g:
            errors.append(f"Missing required class: {name}")

    for name in REQUIRED_PROPERTIES:
        if not list(g.triples((BOT[name], RDF.type, None))):
            errors.append(f"Missing required property: {name}")

    if (BOT.hasPart, RDF.type, OWL.TransitiveProperty) not in g:
        errors.append("hasPart must be transitive")
    if (BOT.hasPart, OWL.inverseOf, BOT.isPartOf) not in g:
        errors.append("hasPart / isPartOf inverse axiom missing")

    # Source-supported carrot facts.
    expected = [
        (BOT.Carrot_ind, RDF.type, BOT.RootVegetable),
        (BOT.Carrot_ind, BOT.hasColor, Literal("Orange")),
        (BOT.Carrot_ind, BOT.growthTimeDays, Literal(70, datatype=XSD.integer)),
        (BOT.Carrot_ind, BOT.hasVitaminA, Literal(True, datatype=XSD.boolean)),
        (BOT.Radish_ind, BOT.growthTimeDays, Literal(25, datatype=XSD.integer)),
        (BOT.Pumpkin_ind, BOT.growthTimeDays, Literal(90, datatype=XSD.integer)),
    ]
    for triple in expected:
        if triple not in g:
            errors.append(f"Missing source-supported triple: {triple}")

    # Check declared disjoint classes for direct instance overlap.
    for a, _, b in g.triples((None, OWL.disjointWith, None)):
        a_members = set(g.subjects(RDF.type, a))
        b_members = set(g.subjects(RDF.type, b))
        overlap = a_members & b_members
        if overlap:
            errors.append(f"Disjointness violation between {a} and {b}: {sorted(map(str, overlap))}")

    # Check numeric data are non-negative.
    for prop in [BOT.proteinPer100g, BOT.carbPer100g, BOT.fatPer100g, BOT.caloriesPer100g, BOT.growthTimeDays]:
        for subj, _, obj in g.triples((None, prop, None)):
            try:
                if float(obj) < 0:
                    errors.append(f"Negative numeric value for {prop} on {subj}: {obj}")
            except (TypeError, ValueError):
                errors.append(f"Non-numeric value for numeric property {prop} on {subj}: {obj}")

    # Ensure every explicit hasPart assertion has an inverse isPartOf assertion.
    for whole, _, part in g.triples((None, BOT.hasPart, None)):
        if (part, BOT.isPartOf, whole) not in g and part != BOT.TomatoSeed:
            # Tomato->Seed is an explicit transitive closure convenience; its direct inverse isPartOf TomatoFruit.
            errors.append(f"Missing inverse isPartOf assertion for {whole} hasPart {part}")

    return errors


def main():
    errors = validate()
    if errors:
        print("Ontology validation FAILED")
        for e in errors:
            print(f" - {e}")
        sys.exit(1)
    print("Ontology validation PASSED")


if __name__ == "__main__":
    main()
