"""Deterministic, evidence-first crop question answering over local RDF assertions."""
import argparse
import json
import re
from pathlib import Path
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef

BOT = Namespace("https://minhajul-abedin-ai.github.io/botanical-knowledge-ontology#")
ROOT = Path(__file__).resolve().parents[1]

def _label(graph, subject):
    value = graph.value(subject, RDFS.label)
    return str(value) if value is not None else str(subject).rsplit("#", 1)[-1]

def _entities(graph):
    entities = {}
    subjects = set(graph.subjects(RDF.type, None)) | set(graph.subjects(RDFS.label, None))
    for subject in subjects:
        if isinstance(subject, URIRef) and str(subject).startswith(str(BOT)) and str(subject).endswith("_ind"):
            entities[_label(graph, subject).casefold()] = subject
    return entities

def answer(graph, question):
    """Answer only supported single-crop questions; never infer absent facts."""
    q = question.casefold().strip()
    matches = [(name, uri) for name, uri in _entities(graph).items()
               if re.search(r"(?<!\w)" + re.escape(name) + r"(?!\w)", q)]
    if len(matches) != 1:
        return {"status": "unsupported", "answer": "Name exactly one known crop.", "evidence": []}
    _, subject = matches[0]
    fields = []
    if any(word in q for word in ("grow", "matur", "days", "harvest")):
        fields.append((BOT.growthTimeDays, "growth time", "days"))
    if "color" in q or "colour" in q:
        fields.append((BOT.hasColor, "colour", ""))
    if "vitamin a" in q:
        fields.append((BOT.hasVitaminA, "vitamin A", ""))
    if not fields:
        return {"status": "unsupported", "answer": "Supported topics: growth days, colour, vitamin A.", "evidence": []}
    evidence, sentences = [], []
    for predicate, field, unit in fields:
        values = sorted(set(graph.objects(subject, predicate)), key=str)
        if not values:
            sentences.append(f"{field.capitalize()} for {_label(graph, subject)} is unknown in this graph.")
        for value in values:
            readable = str(value).lower() if isinstance(value, Literal) and isinstance(value.value, bool) else str(value)
            sentences.append(f"{_label(graph, subject)} {field}: {readable}{' ' + unit if unit else ''}.")
            evidence.append({"subject": str(subject), "predicate": str(predicate), "object": str(value)})
    return {"status": "grounded" if evidence else "unknown", "answer": " ".join(sentences),
            "evidence": evidence, "limitations": "Direct RDF assertions only; no OWL entailment or external validation."}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question")
    parser.add_argument("--ontology", type=Path, default=ROOT / "ontology" / "botanical_ontology.ttl")
    args = parser.parse_args()
    graph = Graph().parse(args.ontology, format="turtle")
    print(json.dumps(answer(graph, args.question), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
