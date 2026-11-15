# Reproducible ontology fingerprint

After installing `pip install -r requirements.txt` and generating the ontology with `python src/build_ontology.py`, run:

```bash
python src/graph_fingerprint.py ontology/botanical_ontology.ttl
python -m pytest -q tests/test_graph_fingerprint.py
```

The CLI prints JSON containing a triple count and an RDF graph isomorphism digest. Unlike hashing raw Turtle bytes, the digest is unaffected by whitespace, prefix aliases or blank-node identifiers. A changed digest signals a structural graph change; it does **not** prove factual correctness, source provenance, or semantic equivalence under OWL reasoning. The digest is calculated using rdflib's default SHA-256 hash; compare outputs with the same rdflib version for maximum reproducibility.

This is a reproducibility aid for the **portfolio reconstruction**, not evidence that the original coursework ontology file has been recovered. See [assignment traceability](ASSIGNMENT_TRACEABILITY.md).
