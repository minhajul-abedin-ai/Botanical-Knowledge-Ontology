"""Offline tests for environment provenance capture."""
import importlib.util
from pathlib import Path
from unittest.mock import patch

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "capture_dependencies.py"
spec = importlib.util.spec_from_file_location("capture_dependencies", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_capture_records_all_direct_dependencies():
    with patch.object(module.importlib.metadata, "version", side_effect=lambda name: f"{name}-test"):
        data = module.capture()
    assert data["packages"] == {
        "rdflib": "rdflib-test",
        "networkx": "networkx-test",
        "matplotlib": "matplotlib-test",
        "pytest": "pytest-test",
    }
    assert data["python_version"]


def test_missing_dependency_fails_closed():
    with patch.object(
        module.importlib.metadata,
        "version",
        side_effect=module.importlib.metadata.PackageNotFoundError("rdflib"),
    ):
        with pytest.raises(RuntimeError, match="Required dependency not installed: rdflib"):
            module.capture()


def test_cli_emits_valid_json_with_installed_versions():
    """Exercise the actual command, not just the imported capture function."""
    import json
    import subprocess
    import sys

    completed = subprocess.run(
        [sys.executable, str(MODULE_PATH)],
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )
    assert completed.stderr == ""
    payload = json.loads(completed.stdout)
    assert payload["python_version"] == module.platform.python_version()
    assert payload["python_implementation"] == module.platform.python_implementation()
    assert set(payload["packages"]) == set(module.DIRECT_DEPENDENCIES)
    for name in module.DIRECT_DEPENDENCIES:
        assert payload["packages"][name] == module.importlib.metadata.version(name)


def test_cli_main_missing_dependency_returns_error_without_json(capsys):
    """A failed capture must not emit misleading JSON to stdout."""
    with patch.object(module, "capture", side_effect=RuntimeError("Required dependency not installed: rdflib")):
        status = module.main()
    output = capsys.readouterr()
    assert status == 1
    assert output.out == ""
    assert "Required dependency not installed: rdflib" in output.err
