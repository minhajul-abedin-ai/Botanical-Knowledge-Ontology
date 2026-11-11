# Evidence-grounded crop question answering

This experimental feature extends the repository's **portfolio reconstruction** of a botanical knowledge-engineering assignment. It is **not** a deployed LLM, a clinical/nutrition reference, or evidence that an original coursework artefact was recovered.

## Reproduce

```bash
python -m pip install -r requirements.txt
python src/grounded_answers.py "How many days does carrot grow?"
python src/grounded_answers.py "What colour is carrot and does it have vitamin A?"
python src/grounded_answers.py "What colour is radish?"
pytest -q tests/test_grounded_answers.py
```

The first two questions return direct RDF triple evidence. The last returns **unknown**, because the ontology does not assert a colour for radish.

## Scope and method

- The question matcher recognizes exactly one named crop using its `rdfs:label` and word boundaries.
- Supported relations: `growthTimeDays`, `hasColor`, and `hasVitaminA`.
- Answers include subject/predicate/object identifiers for each asserted value.
- Missing facts are explicitly marked unknown; unsupported or multi-crop questions are rejected.
- No model weights, retrieval from external sources, ontology entailment, or generated botanical facts are involved.
- The source RDF assertions are an illustrative reconstruction and should not be treated as verified agronomic measurements.

## Reproducibility

Inputs are the checked-in Turtle ontology and question string; outputs are deterministic JSON. Dependency `rdflib` is declared in `requirements.txt`. GitHub Actions runs the `pytest` suite on push and pull requests.

## Future research direction

A future neuro-symbolic LLM layer could propose a structured relation and crop identifier, but should validate them against the ontology and attach triple provenance before rendering any answer. Evaluate unsupported-query abstention and entity ambiguity on an independently labelled benchmark; **no such benchmark or accuracy result is claimed here**.
