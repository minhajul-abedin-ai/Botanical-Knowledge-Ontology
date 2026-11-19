"""End-to-end CLI exit-code checks for the dependency inventory comparator."""
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "compare_dependency_freezes.py"


@pytest.mark.parametrize(
    ("standard", "replay", "expected_output"),
    [
        ("example==1.0\n", "example==2.0\n", "example: standard=1.0, replay=2.0"),
        ("example==1.0\nother==3.0\n", "example==1.0\n", "other: standard=3.0, replay=<missing>"),
        ("example==1.0\n", "example @ https://example.org/pkg.whl\n", "Cannot compare inventories:"),
    ],
)
def test_cli_rejects_mismatched_or_invalid_inventories(tmp_path, standard, replay, expected_output):
    left = tmp_path / "standard.txt"
    right = tmp_path / "replay.txt"
    left.write_text(standard, encoding="utf-8")
    right.write_text(replay, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(left), str(right)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert expected_output in result.stdout + result.stderr


def test_cli_accepts_equivalent_inventories(tmp_path):
    left = tmp_path / "standard.txt"
    right = tmp_path / "replay.txt"
    left.write_text("My_Pkg==1.2\npip==26.3\n", encoding="utf-8")
    right.write_text("PIP==26.3\nmy-pkg==1.2\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(left), str(right)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Installed distribution names and versions match" in result.stdout
