"""Regression tests for strict environment inventory comparisons."""
import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "compare_dependency_freezes.py"
spec = importlib.util.spec_from_file_location("compare_dependency_freezes", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_equal_after_name_normalization_and_reordering():
    assert module.compare("My_Pkg==1.2\npip==26.3\n", "PIP==26.3\nmy-pkg==1.2\n") == []


def test_changed_and_missing_versions_reported():
    assert module.compare("a==1\nb==2\n", "a==3\nc==4\n") == [
        ("a", "1", "3"), ("b", "2", None), ("c", None, "4")
    ]


@pytest.mark.parametrize("content", ["", "# comment only", "a @ https://example.org", "a==1\na==2", "a==1\nA==2"])
def test_rejects_empty_unsupported_or_duplicate_records(content):
    with pytest.raises(ValueError):
        module.parse_freeze(content)


def test_ignores_comments_and_blank_lines():
    assert module.parse_freeze("# via pip\n\nfoo==1.0\n") == {"foo": "1.0"}
