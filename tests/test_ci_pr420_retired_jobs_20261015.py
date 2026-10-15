"""Guard normal CI against reintroducing unreachable PR #420-only jobs.

This is workflow hygiene. Original K32 sources, frozen readouts, and original
Git/Actions provenance remain outside the current shared CI.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / ".github/workflows/ci.yml"
GATE = ROOT / ".github/workflows/chapter2-scientific-gate.yml"
PROVENANCE = ROOT / "docs/CI_PR420_RETIRED_JOB_PROVENANCE_20261015.md"


def test_general_matrix_is_only_active_ci_job():
    text = CI.read_text(encoding="utf-8")
    assert text.startswith("name: CI\n")
    jobs = text.split("jobs:\n", 1)[1]
    names = re.findall(r"^  ([a-zA-Z][\w-]*):\s*$", jobs, flags=re.MULTILINE)
    assert names == ["tests"]
    assert "python-version: ['3.10', '3.11', '3.12']" in jobs
    assert "python -m pip install -e '.[dev]'" in jobs
    assert "pytest -q --junitxml=" in jobs
    assert "test ${PIPESTATUS[0]} -eq 0" in jobs
    assert "Upload pytest reports on failure" in jobs
    assert "cancel-in-progress: true" in text


def test_closed_pr420_never_gates_current_workflows():
    ci_text = CI.read_text(encoding="utf-8")
    assert "github.event.pull_request.number == 420" not in ci_text
    assert "model3-k32-" not in ci_text
    assert "on:\n  push:\n    branches: [main]\n  pull_request:" in ci_text
    gate = GATE.read_text(encoding="utf-8")
    assert "name: Chapter 2 scientific gate" in gate
    assert "test_chapter2_unified_el_review_bundle_20261010.py" in gate


def test_historical_provenance_links_original_workflow_and_exact_20_jobs():
    doc = PROVENANCE.read_text(encoding="utf-8")
    original_jobs = set(re.findall(r"`(model3-k32-[a-z-]+)`", doc))
    assert len(original_jobs) == 20
    assert "ae91c6aaf66637b23db14067eb08d135cb9f4172" in doc
    assert "264ed7d7185d6c205b6f02c019dd15bddfee982b" in doc
    assert "PR #420" in doc
    assert "no original Model 3" in doc.lower() or "No original Model 3" in doc
