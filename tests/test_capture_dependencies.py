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
