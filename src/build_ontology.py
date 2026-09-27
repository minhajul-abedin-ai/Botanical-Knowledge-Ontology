from pathlib import Path
from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL, XSD
from rdflib.namespace import DCTERMS

BASE = Namespace("https://minhajul-abedin-ai.github.io/botanical-knowledge-ontology#")


def add_class(g: Graph, name: str, parent: str | None = None, label: str | None = None, comment: str | None = None):
    uri = BASE[name]
    g.add((uri, RDF.type, OWL.Class))
    g.add((uri, RDFS.label, Literal(label or name)))
    if parent:
        g.add((uri, RDFS.subClassOf, BASE[parent]))
    if comment:
        g.add((uri, RDFS.comment, Literal(comment)))
    return uri


def add_object_property(g: Graph, name: str, domain=None, range_=None, *, transitive=False):
    uri = BASE[name]
    g.add((uri, RDF.type, OWL.ObjectProperty))
    g.add((uri, RDFS.label, Literal(name)))
    if transitive:
        g.add((uri, RDF.type, OWL.TransitiveProperty))
    if domain:
        g.add((uri, RDFS.domain, BASE[domain]))
    if range_:
        g.add((uri, RDFS.range, BASE[range_]))
    return uri


def add_data_property(g: Graph, name: str, datatype, domain="Vegetable"):
    uri = BASE[name]
    g.add((uri, RDF.type, OWL.DatatypeProperty))
    g.add((uri, RDFS.label, Literal(name)))
    g.add((uri, RDFS.domain, BASE[domain]))
    g.add((uri, RDFS.range, datatype))
    return uri


def add_individual(g: Graph, name: str, class_name: str, label: str | None = None):
    uri = BASE[name]
    g.add((uri, RDF.type, OWL.NamedIndividual))
    g.add((uri, RDF.type, BASE[class_name]))
    g.add((uri, RDFS.label, Literal(label or name)))
    return uri


def build_graph() -> Graph:
    g = Graph()
    g.bind("bot", BASE)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)
    g.bind("dcterms", DCTERMS)

    ontology = BASE["BotanicalKnowledgeOntology"]
    g.add((ontology, RDF.type, OWL.Ontology))
    g.add((ontology, DCTERMS.title, Literal("Botanical Knowledge Ontology")))
    g.add((ontology, DCTERMS.creator, Literal("Minhajul Abedin")))
    g.add((ontology, DCTERMS.description, Literal(
        "Portfolio reconstruction of a botanical knowledge-engineering assignment, extended with reproducible RDF/OWL tooling."
    )))
    g.add((ontology, OWL.versionInfo, Literal("1.0.0")))

    # Core taxonomy from the assignment.
    add_class(g, "BotanicalEntity")
    add_class(g, "Plant", "BotanicalEntity")
    add_class(g, "Vegetable", "BotanicalEntity")
    add_class(g, "RootVegetable", "Vegetable")
    add_class(g, "LeafyVegetable", "Vegetable")
    add_class(g, "LegumeVegetable", "Vegetable")
    add_class(g, "FruitVegetable", "Vegetable")
    add_class(g, "BulbVegetable", "Vegetable")
    add_class(g, "CruciferousVegetable", "Vegetable")

    add_class(g, "PlantPart", "BotanicalEntity")
    add_class(g, "Root", "PlantPart")
    add_class(g, "TapRoot", "Root")
    add_class(g, "FibrousRoot", "Root")
    add_class(g, "Stem", "PlantPart")
    add_class(g, "Leaf", "PlantPart")
    add_class(g, "SimpleLeaf", "Leaf")
    add_class(g, "CompoundLeaf", "Leaf")
    add_class(g, "Seed", "PlantPart")
    add_class(g, "MonocotSeed", "Seed")
    add_class(g, "DicotSeed", "Seed")
    add_class(g, "Fruit", "PlantPart")
    add_class(g, "Tuber", "PlantPart")
    add_class(g, "Flower", "PlantPart")
    add_class(g, "Pod", "PlantPart")

    add_class(g, "Nutrient", "BotanicalEntity")
    add_class(g, "Macronutrient", "Nutrient")
    add_class(g, "Protein", "Macronutrient")
    add_class(g, "Carbohydrate", "Macronutrient")
    add_class(g, "Fat", "Macronutrient")
    add_class(g, "Micronutrient", "Nutrient")
    add_class(g, "VitaminA", "Micronutrient")
    add_class(g, "VitaminC", "Micronutrient")
    add_class(g, "VitaminK", "Micronutrient")

    add_class(g, "GrowthHabit", "BotanicalEntity")
    add_class(g, "Cuisine", "BotanicalEntity")

    # Reconstruction helper classes. These preserve assignment-described query outcomes
    # where exact numeric source assertions were not included in the report.
    add_class(g, "FastGrowingCrop", "Vegetable", comment="Portfolio helper class for assignment-described fast-growing query results.")
    add_class(g, "HighProteinCrop", "Vegetable", comment="Portfolio helper class for assignment-described >2g protein query result.")
    add_class(g, "MaturesUnder120Days", "Vegetable", comment="Portfolio helper class for assignment-described biofortification scenario.")
    add_class(g, "VitaminARichCrop", "Vegetable")

    # Disjointness explicitly discussed in the report.
    g.add((BASE.RootVegetable, OWL.disjointWith, BASE.LeafyVegetable))
    g.add((BASE.MonocotSeed, OWL.disjointWith, BASE.DicotSeed))

    # Object properties.
    has_part = add_object_property(g, "hasPart", "BotanicalEntity", "PlantPart", transitive=True)
    is_part_of = add_object_property(g, "isPartOf", "PlantPart", "BotanicalEntity")
    g.add((has_part, OWL.inverseOf, is_part_of))
    g.add((is_part_of, OWL.inverseOf, has_part))
    add_object_property(g, "hasGrowthHabit", "Vegetable", "GrowthHabit")
    add_object_property(g, "hasFlower", "Vegetable", "Flower")
    add_object_property(g, "hasPod", "Vegetable", "Pod")
    add_object_property(g, "usedInCuisine", "Vegetable", "Cuisine")

    # Data properties from the report.
    add_data_property(g, "proteinPer100g", XSD.decimal)
    add_data_property(g, "carbPer100g", XSD.decimal)
    add_data_property(g, "fatPer100g", XSD.decimal)
    add_data_property(g, "caloriesPer100g", XSD.integer)
    add_data_property(g, "hasVitaminA", XSD.boolean)
    add_data_property(g, "hasVitaminC", XSD.boolean)
    add_data_property(g, "hasVitaminK", XSD.boolean)
    add_data_property(g, "growthTimeDays", XSD.integer)
    add_data_property(g, "hasOrigin", XSD.string)
    add_data_property(g, "hasColor", XSD.string)
    add_data_property(g, "hasTaste", XSD.string)

    # Individuals explicitly named or exemplified in the assignment.
    carrot = add_individual(g, "Carrot_ind", "RootVegetable", "Carrot")
    g.add((carrot, BASE.hasColor, Literal("Orange")))
    g.add((carrot, BASE.growthTimeDays, Literal(70, datatype=XSD.integer)))
    g.add((carrot, BASE.hasVitaminA, Literal(True, datatype=XSD.boolean)))
    g.add((carrot, RDF.type, BASE.VitaminARichCrop))
    g.add((carrot, RDF.type, BASE.MaturesUnder120Days))

    carrot_root = add_individual(g, "CarrotTapRoot", "TapRoot", "Carrot taproot")
    g.add((carrot, BASE.hasPart, carrot_root))
    g.add((carrot_root, BASE.isPartOf, carrot))

    spinach = add_individual(g, "Spinach_ind", "LeafyVegetable", "Spinach")
    g.add((spinach, RDF.type, BASE.HighProteinCrop))
    g.add((spinach, RDF.type, BASE.FastGrowingCrop))
    g.add((spinach, BASE.hasVitaminA, Literal(True, datatype=XSD.boolean)))
    spinach_leaf = add_individual(g, "SpinachLeaf", "Leaf", "Spinach leaf")
    g.add((spinach, BASE.hasPart, spinach_leaf))
    g.add((spinach_leaf, BASE.isPartOf, spinach))

    tomato = add_individual(g, "Tomato_ind", "FruitVegetable", "Tomato")
    tomato_fruit = add_individual(g, "TomatoFruit", "Fruit", "Tomato fruit")
    tomato_seed = add_individual(g, "TomatoSeed", "DicotSeed", "Tomato seed")
    g.add((tomato, BASE.hasPart, tomato_fruit))
    g.add((tomato_fruit, BASE.isPartOf, tomato))
    g.add((tomato_fruit, BASE.hasPart, tomato_seed))
    g.add((tomato_seed, BASE.isPartOf, tomato_fruit))
    # Explicit transitive closure fact for portability to tools without a reasoner.
    g.add((tomato, BASE.hasPart, tomato_seed))

    kale = add_individual(g, "Kale_ind", "LeafyVegetable", "Kale")
    lettuce = add_individual(g, "Lettuce_ind", "LeafyVegetable", "Lettuce")
    pea = add_individual(g, "Pea_ind", "LegumeVegetable", "Pea")
    bean = add_individual(g, "Bean_ind", "LegumeVegetable", "Bean")
    g.add((bean, RDF.type, BASE.FastGrowingCrop))
    beetroot = add_individual(g, "Beetroot_ind", "RootVegetable", "Beetroot")
    g.add((beetroot, RDF.type, BASE.FastGrowingCrop))

    sweet_potato = add_individual(g, "SweetPotato_ind", "RootVegetable", "Sweet potato")
    g.add((sweet_potato, BASE.hasVitaminA, Literal(True, datatype=XSD.boolean)))
    g.add((sweet_potato, RDF.type, BASE.VitaminARichCrop))
    g.add((sweet_potato, RDF.type, BASE.MaturesUnder120Days))

    radish = add_individual(g, "Radish_ind", "RootVegetable", "Radish")
    g.add((radish, BASE.growthTimeDays, Literal(25, datatype=XSD.integer)))
    g.add((radish, RDF.type, BASE.FastGrowingCrop))

    pumpkin = add_individual(g, "Pumpkin_ind", "FruitVegetable", "Pumpkin")
    g.add((pumpkin, BASE.growthTimeDays, Literal(90, datatype=XSD.integer)))
    g.add((pumpkin, RDF.type, BASE.MaturesUnder120Days))

    bell_pepper = add_individual(g, "BellPepper_ind", "FruitVegetable", "Bell pepper")

    # Culinary concept used only as a light demonstration of usedInCuisine.
    salad = add_individual(g, "Salad", "Cuisine", "Salad")
    g.add((spinach, BASE.usedInCuisine, salad))
    g.add((lettuce, BASE.usedInCuisine, salad))

    return g


def write_outputs(root: Path | None = None):
    root = root or Path(__file__).resolve().parents[1]
    out_dir = root / "ontology"
    out_dir.mkdir(parents=True, exist_ok=True)
    g = build_graph()
    g.serialize(out_dir / "botanical_ontology.ttl", format="turtle")
    g.serialize(out_dir / "botanical_ontology.owl", format="xml")
    g.serialize(out_dir / "botanical_ontology.jsonld", format="json-ld", indent=2)
    print(f"Wrote ontology with {len(g)} RDF triples to {out_dir}")


if __name__ == "__main__":
    write_outputs()
