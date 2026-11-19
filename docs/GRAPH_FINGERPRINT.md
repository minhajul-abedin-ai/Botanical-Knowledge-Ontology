# Reproducible ontology fingerprint

After installing `pip install -r requirements.txt` and generating the ontology with `python src/build_ontology.py`, run:

```bash
python src/graph_fingerprint.py ontology/botanical_ontology.ttl
python -m pytest -q tests/test_graph_fingerprint.py
```

The CLI prints JSON containing a triple count and an RDF graph isomorphism digest. Unlike hashing raw Turtle bytes, the digest is unaffected by whitespace, prefix aliases or blank-node identifiers. A changed digest signals a structural graph change; it does **not** prove factual correctness, source provenance, or semantic equivalence under OWL reasoning. The digest is calculated using rdflib's default SHA-256 hash; compare outputs with the same rdflib version for maximum reproducibility.

This is a reproducibility aid for the **portfolio reconstruction**, not evidence that the original coursework ontology file has been recovered. See [assignment traceability](ASSIGNMENT_TRACEABILITY.md).

## Relative IRIs and file location

RDFLib resolves relative IRIs in Turtle against a base IRI. When parsing a local file without an explicit base, that base can depend on the file's location. Consequently, two byte-identical Turtle files containing relative IRIs (for example, `<subject> <predicate> <object> .`) in different directories may resolve to different absolute IRIs and produce **different** graph digests. This is expected RDF parsing behavior, not a hash collision or a failure of blank-node canonicalization.

For location-independent comparisons, use absolute IRIs throughout the input, or ensure that the RDF parser uses a consistent, explicitly specified base IRI before fingerprinting. The current `fingerprint(path)` helper does not expose a base-IRI override; do not assume moving relative-IRI files preserves their digest.
