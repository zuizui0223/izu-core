"""Check broad review scope without pretending AST parsing proves correctness."""
from __future__ import annotations

from scripts.audit_chapter2_repository_wide_static_20261016 import scan_source


def test_every_nonlegacy_script_and_test_is_python_parseable():
    result = scan_source()
    assert result["scanned_python_files"] >= 1000
    assert result["by_kind"]["scripts"] >= 590
    assert result["by_kind"]["tests"] >= 470
    # Data/results may contain historical snapshots. Parser errors, if any,
    # must not be silently excluded from the source census.
    assert result["syntax_failures"] == []
    assert result["scanned_lines"] > 40000
    assert "all functions" in result["methodological_limits"][0]
    assert set(result["risk_counts"]) == {
        "dynamic_code", "unseeded_numpy_rng", "pickle_input",
        "yaml_unsafe_load", "broad_exception_swallowed",
        "destructive_shell", "archive_extraction",
    }


def test_static_flags_mean_risks_not_assumed_defects(tmp_path):
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    source = scripts / "sample.py"
    source.write_text(
        "import numpy as np\n"
        "def f():\n"
        "    x=np.random.default_rng()\n"
        "    try: x=eval('1 + 1')\n"
        "    except Exception: pass\n"
        "    return x\n", encoding="utf-8")
    report = scan_source(tmp_path)
    assert report["by_kind"]["scripts"] == 1
    assert report["risk_counts"]["dynamic_code"] == 1
    assert report["risk_counts"]["unseeded_numpy_rng"] == 1
    assert report["risk_counts"]["broad_exception_swallowed"] == 1
    assert not report["syntax_failures"]
    assert report["risk_examples"]["dynamic_code"][0]["file"] == "scripts/sample.py"
