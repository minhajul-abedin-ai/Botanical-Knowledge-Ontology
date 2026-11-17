# Reproducing the recorded dependency environment

The project declares **compatible ranges** in `requirements.txt`:

| Direct dependency | Allowed range | Observed in CI on 17 Nov 2026 |
| --- | --- | --- |
| rdflib | >=7.0,<8 | 7.6.0 |
| networkx | >=3.0,<4 | 3.6.1 |
| matplotlib | >=3.8,<4 | 3.11.2 |
| pytest | >=8.0,<9 | 8.4.2 |

The observed versions came from [GitHub Actions run 44006232297](https://github.com/minhajul-abedin-ai/Botanical-Knowledge-Ontology/actions/runs/44006232297), which recorded CPython 3.11.18. These are **observations**, not a tested lockfile.

## Clean-environment verification

Use a fresh Python 3.11 environment (the commands below assume a POSIX shell):

```sh
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
python src/build_ontology.py
python src/validate_ontology.py
python -m pytest -q
python scripts/capture_dependencies.py > dependency-environment.json
python -m json.tool dependency-environment.json >/dev/null
```

To *attempt* a direct-version replay of the recorded CI environment, start in a **different fresh** Python 3.11 virtual environment and install the observed direct versions:

```sh
python -m pip install 'rdflib==7.6.0' 'networkx==3.6.1' 'matplotlib==3.11.2' 'pytest==8.4.2'
python -m pip check
python src/build_ontology.py
python src/validate_ontology.py
python -m pytest -q
python scripts/capture_dependencies.py > dependency-environment.json
```

Compare the resulting JSON against the `dependency-environment` artifact attached to the referenced CI run. The artifact expires according to GitHub's retention policy.

## Interpretation and limitations

- `pip check` tests whether installed package requirements conflict; it does not validate ontology semantics or freeze transitive dependencies.
- Pinning four direct packages does **not** pin their transitive dependencies, the Python patch version, operating system, or package indexes. A different solver result may change outputs.
- A successful replay requires executing the commands and recording the result; this document does **not** claim the replay has been performed.
- For stronger reproducibility, evaluate a generated, reviewed, hash-checked lock/constraints file in a separate change, with cross-platform compatibility considered before enforcing it.
- Keep generated `dependency-environment.json` local or in CI artifacts rather than committing machine-specific environment metadata.
