"""Export bounded, traceable SPARQL SELECT evidence for downstream LLM workflows."""
import argparse
import json
from pathlib import Path

from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]


def evidence_for_query(graph: Graph, query_text: str, *, max_rows: int = 20) -> dict:
    if max_rows < 1 or max_rows > 100:
        raise ValueError("max_rows must be between 1 and 100")
    result = graph.query(query_text)
    if result.type != "SELECT":
        raise ValueError("Only read-only SPARQL SELECT queries are supported")
    columns = [str(v) for v in result.vars]
    rows = []
    truncated = False
    for row in result:
        if len(rows) >= max_rows:
            truncated = True
            break
        rows.append({key: str(value) if value is not None else None
                     for key, value in zip(columns, row)})
    return {
        "source": "reconstructed botanical ontology (not independently verified)",
        "columns": columns,
        "rows": rows,
        "truncated": truncated,
        "warning": "Query output is ontology evidence, not external scientific validation.",
    }


def main():
    parser = argparse.ArgumentParser(description="Export ontology SELECT evidence as JSON")
    parser.add_argument("query", type=Path, help="Trusted local SPARQL SELECT query file")
    parser.add_argument("--ontology", type=Path,
                        default=ROOT / "ontology" / "botanical_ontology.ttl")
    parser.add_argument("--max-rows", type=int, default=20)
    args = parser.parse_args()
    graph = Graph()
    graph.parse(args.ontology, format="turtle")
    print(json.dumps(evidence_for_query(
        graph, args.query.read_text(encoding="utf-8"), max_rows=args.max_rows
    ), indent=2))


if __name__ == "__main__":
    main()
