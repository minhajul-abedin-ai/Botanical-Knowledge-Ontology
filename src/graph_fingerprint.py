"""Produce a stable structural fingerprint of an RDF graph (including blank nodes)."""
import argparse
import json
from pathlib import Path
from rdflib import Graph
from rdflib.compare import to_isomorphic


def fingerprint(path: Path) -> dict:
    graph = Graph()
    graph.parse(path, format="turtle")
    return {"algorithm": "rdflib-isomorphic-sha256", "triple_count": len(graph),
            "digest": str(to_isomorphic(graph).graph_digest())}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ontology", type=Path, help="Turtle RDF file")
    args = parser.parse_args()
    print(json.dumps(fingerprint(args.ontology), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
