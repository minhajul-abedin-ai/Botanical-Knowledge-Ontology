# Reproducible ontology fingerprint

After installing `pip install -r requirements.txt` and generating the ontology with `python src/build_ontology.py`, run:

```bash
python src/graph_fingerprint.py ontology/botanical_ontology.ttl
python -m pytest -q tests/test_graph_fingerprint.py
```

The CLI prints JSON containing a triple count and an RDF graph isomorphism digest. Unlike hashing raw Turtle bytes, the digest is unaffected by whitespace, prefix aliases or blank-node identifiers. A changed digest signals a structural graph change; it does **not** prove factual correctness, source provenance, or semantic equivalence under OWL reasoning. The digest is calculated using rdflib's default SHA-256 hash; compare outputs with the same rdflib version for maximum reproducibility.

## Digest representation and compatibility

The JSON `digest` field is a **base-10 decimal string** of the non-negative integer returned by `rdflib.compare.to_isomorphic(graph).graph_digest()`. It is **not** a 64-character hexadecimal SHA-256 string. Its decimal length can vary, and no leading zero padding is applied. The `algorithm` field is `rdflib-isomorphic-sha256`; `triple_count` is the number of parsed RDF triples.

For reproducible comparisons, compare `algorithm`, `triple_count`, and `digest` together and record the RDFLib version. Do not interpret the decimal digest as hexadecimal or compare it directly with a conventional file SHA-256 checksum. Changing the digest's output encoding to hex would be a **breaking change** for stored JSON snapshots and downstream consumers, even if the underlying graph hash remained the same. This documentation preserves the existing output contract.

This is a reproducibility aid for the **portfolio reconstruction**, not evidence that the original coursework ontology file has been recovered. See [assignment traceability](ASSIGNMENT_TRACEABILITY.md).
