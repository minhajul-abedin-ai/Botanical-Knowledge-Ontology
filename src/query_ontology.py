from pathlib import Path
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "ontology" / "botanical_ontology.ttl"
QUERY_DIR = ROOT / "queries"


def load_graph() -> Graph:
    g = Graph()
    g.parse(ONTOLOGY, format="turtle")
    return g


def run_query(g: Graph, path: Path):
    print(f"\n=== {path.name} ===")
    result = g.query(path.read_text(encoding="utf-8"))
    rows = list(result)
    if not rows:
        print("(no results)")
        return
    headers = [str(v) for v in result.vars]
    print(" | ".join(headers))
    print("-" * max(20, len(" | ".join(headers))))
    for row in rows:
        print(" | ".join(str(value) for value in row))


def main():
    g = load_graph()
    for path in sorted(QUERY_DIR.glob("*.sparql")):
        run_query(g, path)


if __name__ == "__main__":
    main()
