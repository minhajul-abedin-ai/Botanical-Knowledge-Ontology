# Grounded query evidence for neuro-symbolic prototypes

This is a **portfolio extension**, not a reproduction of an evaluated LLM or a claim of scientific validation. The ontology itself is a reconstruction; see [assignment traceability](ASSIGNMENT_TRACEABILITY.md) before relying on its assertions.

The exporter executes a local SPARQL `SELECT` query and emits JSON containing column names, stringified result rows, a row-limit flag, and an explicit provenance warning. It makes **no LLM API calls**, introduces **no external datasets**, and does not claim that an answer is factually true outside the reconstructed graph.

## Reproduce

Install the repository's existing dependencies:

```bash
python -m pip install -r requirements.txt
python src/export_query_evidence.py queries/YOUR_EXISTING_QUERY.sparql --max-rows 20
python -m pytest -q tests/test_query_evidence.py
```

Replace `YOUR_EXISTING_QUERY.sparql` with a real query filename in the repository's `queries/` directory. For a standalone test, save the following to `/tmp/botanical-select.sparql`:

```sparql
SELECT ?subject ?predicate ?object WHERE {
  ?subject ?predicate ?object .
} LIMIT 3
```

Then run `python src/export_query_evidence.py /tmp/botanical-select.sparql`.

## Safe use

Treat the JSON as *retrieved evidence*, not a validated answer. A downstream language model should cite the returned graph statements, distinguish absent evidence from negative facts, and explicitly abstain when the graph lacks support. The output is capped at 100 rows and flags truncation. Only run **trusted local query files**; this script is not a sandbox for arbitrary SPARQL workloads.

## Verification scope

Unit tests use a tiny synthetic RDF graph, not the reconstructed botanical dataset. Passing tests verify output formatting, ordering, truncation and non-SELECT rejection, **not** ontology accuracy, reasoning completeness, LLM grounding quality or external crop/nutrition facts.
