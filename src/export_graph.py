from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
from rdflib import Graph, Namespace, RDF, RDFS, OWL

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "ontology" / "botanical_ontology.ttl"
ASSETS = ROOT / "assets"
BOT = Namespace("https://minhajul-abedin-ai.github.io/botanical-knowledge-ontology#")


def short(uri):
    text = str(uri)
    return text.rsplit("#", 1)[-1]


def hierarchy_graph():
    g = Graph().parse(ONTOLOGY, format="turtle")
    nxg = nx.DiGraph()
    for child, _, parent in g.triples((None, RDFS.subClassOf, None)):
        if (child, RDF.type, OWL.Class) in g and (parent, RDF.type, OWL.Class) in g:
            nxg.add_edge(short(parent), short(child))
    focus = {
        "BotanicalEntity", "Vegetable", "RootVegetable", "LeafyVegetable", "LegumeVegetable", "FruitVegetable",
        "PlantPart", "Root", "TapRoot", "FibrousRoot", "Leaf", "SimpleLeaf", "CompoundLeaf", "Seed", "MonocotSeed", "DicotSeed",
        "Nutrient", "Macronutrient", "Micronutrient"
    }
    nxg = nxg.subgraph([n for n in nxg.nodes if n in focus]).copy()
    pos = nx.spring_layout(nxg, seed=42, k=1.2)
    plt.figure(figsize=(14, 9))
    nx.draw_networkx_nodes(nxg, pos, node_size=2600)
    nx.draw_networkx_edges(nxg, pos, arrows=True, arrowsize=18)
    nx.draw_networkx_labels(nxg, pos, font_size=9)
    plt.title("Botanical Ontology — Selected Class Hierarchy")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(ASSETS / "class_hierarchy.png", dpi=180, bbox_inches="tight")
    plt.close()


def architecture_graph():
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.axis("off")
    boxes = [
        (0.03, 0.61, 0.18, 0.22, "Academic assignment\nconcepts & examples"),
        (0.28, 0.61, 0.18, 0.22, "OWL/RDF ontology\nclasses, properties,\nindividuals"),
        (0.53, 0.61, 0.18, 0.22, "Reasoning &\nconsistency\nvalidation"),
        (0.78, 0.61, 0.18, 0.22, "SPARQL /\ncompetency\nqueries"),
        (0.28, 0.18, 0.18, 0.22, "Protégé +\nOWL 2 DL"),
        (0.53, 0.18, 0.18, 0.22, "Python / RDFLib\nreproducibility"),
        (0.78, 0.18, 0.18, 0.22, "Neuro-symbolic\nAI grounding\nconcept"),
    ]
    for x, y, w, h, text in boxes:
        rect = plt.Rectangle((x, y), w, h, fill=False, linewidth=2)
        ax.add_patch(rect)
        ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=12)
    arrows = [
        ((0.21,0.72),(0.28,0.72)), ((0.46,0.72),(0.53,0.72)), ((0.71,0.72),(0.78,0.72)),
        ((0.37,0.61),(0.37,0.40)), ((0.62,0.61),(0.62,0.40)), ((0.87,0.61),(0.87,0.40)),
        ((0.46,0.29),(0.53,0.29)), ((0.71,0.29),(0.78,0.29)),
    ]
    for start, end in arrows:
        ax.annotate("", xy=end, xytext=start, arrowprops=dict(arrowstyle="->", linewidth=2))
    ax.text(0.5, 0.94, "Botanical Knowledge Ontology — Portfolio Reconstruction Architecture", ha="center", fontsize=16, weight="bold")
    ax.text(0.5, 0.04, "Source-derived ontology concepts are separated from portfolio engineering additions in ASSIGNMENT_TRACEABILITY.md", ha="center", fontsize=10)
    plt.savefig(ASSETS / "project_architecture.png", dpi=180, bbox_inches="tight")
    plt.close()


def main():
    ASSETS.mkdir(exist_ok=True)
    hierarchy_graph()
    architecture_graph()
    print(f"Wrote diagrams to {ASSETS}")


if __name__ == "__main__":
    main()
