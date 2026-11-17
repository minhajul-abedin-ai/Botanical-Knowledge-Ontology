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

## Comparing CI dependency artifacts

The [successful two-job run 44119473142](https://github.com/minhajul-abedin-ai/Botanical-Knowledge-Ontology/actions/runs/44119473142) on 17 November 2026 produced a standard `dependency-environment` artifact and an isolated `clean-replay-dependency-environment` artifact. Both jobs ran with pip 26.3; an independent comparison reported identical JSON manifests and all 19 `pip freeze --all` package records. This is **installed-version equality for that run**, not a hash-locked build or a guarantee about future dependency resolution.

To independently repeat the comparison, download **both ZIP artifacts from the same workflow run** using the GitHub Actions artifacts page. Extract each ZIP into a different directory:

```sh
mkdir -p /tmp/ontology-standard /tmp/ontology-replay
unzip -q dependency-environment.zip -d /tmp/ontology-standard
unzip -q clean-replay-dependency-environment.zip -d /tmp/ontology-replay
python - <<'PY'
import json
from pathlib import Path

standard = Path("/tmp/ontology-standard")
replay = Path("/tmp/ontology-replay")
a = json.loads((standard / "dependency-environment.json").read_text(encoding="utf-8"))
b = json.loads((replay / "replay-dependency-environment.json").read_text(encoding="utf-8"))
assert a == b, f"Environment JSON differs: {a!r} != {b!r}"

def records(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines and len(lines) == len(set(lines)), "Empty or duplicate freeze records"
    return sorted(lines)

left = records(standard / "dependency-freeze.txt")
right = records(replay / "replay-dependency-freeze.txt")
assert left == right, "Installed package inventories differ"
print(f"JSON manifests match; {len(left)} installed package records match")
PY
```

The ZIP filenames in the commands are examples: rename the downloaded files accordingly. A failed assertion is evidence of a difference, not proof of which environment is correct. Compare package names and versions before proposing any pin changes. The artifacts have a 14-day retention policy and may expire; use a newer successful run if necessary.

## Interpretation and limitations

- `pip check` tests whether installed package requirements conflict; it does not validate ontology semantics or freeze transitive dependencies.
- Pinning four direct packages does **not** pin their transitive dependencies, the Python patch version, operating system, or package indexes. A different solver result may change outputs.
- The clean-replay job has run successfully in CI (see run 44119473142), but this document does **not** claim an independently executed local replay.
- For stronger reproducibility, evaluate a generated, reviewed, hash-checked lock/constraints file in a separate change, with cross-platform compatibility considered before enforcing it.
- Keep generated `dependency-environment.json` local or in CI artifacts rather than committing machine-specific environment metadata.
