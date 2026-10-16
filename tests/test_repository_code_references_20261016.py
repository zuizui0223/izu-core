"""Safe code cleanup map: referenced and unreferenced scripts are never deleted."""
from __future__ import annotations

from pathlib import Path

from scripts.audit_repository_code_references_20261016 import audit


def _fixture(root: Path):
    content = {
        "scripts/__init__.py": "",
        "scripts/foo.py": "from .bar import run\n",
        "scripts/bar.py": "def run(): return 1\n",
        "scripts/duplicate.py": "def run(): return 1\n",
        "scripts/unreferenced.py": "print('may be called externally')\n",
        "scripts/run_chapter2_assurance_generality.py": "pass\n",
        "tests/test_foo.py": "import scripts.foo\n",
        ".github/workflows/ci.yml": "run: python -m scripts.foo\n",
        "README.md": "see scripts/bar.py\n",
        "legacy/model2/old.py": "pass\n",
    }
    for filename, text in content.items():
        path = root / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def test_static_references_and_frozen_code_are_distinct(tmp_path):
    _fixture(tmp_path)
    report = audit(tmp_path)
    paths = {r["path"]: r for r in report["scripts"]}
    assert report["inventory"]["scripts_python"] == 6
    assert report["inventory"]["workflows"] == 1
    assert report["inventory"]["legacy_files"] == 1
    assert "tests/test_foo.py" in paths["scripts/foo.py"]["references_examples"]
    assert paths["scripts/foo.py"]["category"] == "workflow_reference_check_before_edit"
    assert "scripts/foo.py" in paths["scripts/bar.py"]["references_examples"]
    assert paths["scripts/run_chapter2_assurance_generality.py"]["category"] == "frozen_model_or_producer_protect"
    assert paths["scripts/unreferenced.py"]["category"] == "unresolved_do_not_delete"
    assert ["scripts/bar.py", "scripts/duplicate.py"] in report["duplicate_byte_identical_groups"]
    assert report["parse_errors"] == []


def test_damaged_python_is_reported_not_silently_skipped(tmp_path):
    _fixture(tmp_path)
    (tmp_path / "scripts" / "foo.py").write_text("def broken(:\n", encoding="utf-8")
    result = audit(tmp_path)
    assert len(result["parse_errors"]) == 1
    assert result["parse_errors"][0]["path"] == "scripts/foo.py"


def test_reference_absence_is_never_deletion_approval(tmp_path):
    _fixture(tmp_path)
    result = audit(tmp_path)
    assert "No detected reference does not mean unused" in result["limits"][0]
    unknown = next(x for x in result["scripts"] if x["path"] == "scripts/unreferenced.py")
    assert "do_not_delete" in unknown["category"]


def test_full_repository_reports_research_provenance_and_legacy_without_deleting():
    repo = Path(__file__).resolve().parents[1]
    result = audit(repo)
    assert result["inventory"]["scripts_python"] >= 590
    assert result["inventory"]["tests_python"] >= 470
    assert result["inventory"]["legacy_files"] >= 1000
    assert result["inventory"]["workflows"] >= 35
    assert result["parse_errors"] == []
    protected = {row["path"] for row in result["scripts"]
                 if row["category"] == "frozen_model_or_producer_protect"}
    assert "scripts/model3_island/reproduction.py" in protected
    assert "scripts/model3_island/population.py" in protected
    assert "scripts/run_chapter2_assurance_generality.py" in protected
    assert "scripts/run_chapter2_q1_fresh_founders_20261016.py" in protected
    assert "scripts/run_chapter2_island_demographic_independent32.py" in protected
