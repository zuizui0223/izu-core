from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPRODUCE = ROOT / "REPRODUCE.md"
SCIENTIFIC_GATE = ROOT / ".github/workflows/chapter2-scientific-gate.yml"
FULL_PRODUCTION = ROOT / ".github/workflows/model3_ch2_bridge_production.yml"


def _collapse_shell_continuations(text: str) -> str:
    return re.sub(r"\\\n[ \t]*", " ", text)


def _pytest_targets(text: str) -> set[str]:
    collapsed = _collapse_shell_continuations(text)
    targets: set[str] = set()
    for line in collapsed.splitlines():
        stripped = line.strip()
        if not stripped.startswith("pytest -q "):
            continue
        for token in stripped.split():
            if token.startswith("tests/"):
                targets.add(token.split("::", 1)[0])
    return targets


def test_documented_pytest_targets_exist() -> None:
    targets = _pytest_targets(REPRODUCE.read_text(encoding="utf-8"))
    assert targets
    for target in targets:
        assert (ROOT / target).is_file(), f"REPRODUCE.md points to missing pytest target: {target}"


def test_fast_reviewer_path_is_covered_by_scientific_gate() -> None:
    documented = _pytest_targets(REPRODUCE.read_text(encoding="utf-8"))
    workflow = _pytest_targets(SCIENTIFIC_GATE.read_text(encoding="utf-8"))
    assert documented <= workflow
    for required in {
        "tests/test_chapter2_branch_identifiability_boundary.py",
        "tests/test_chapter2_independent_unit_reporting.py",
        "tests/test_repository_artifact_budget.py",
        "tests/test_workflow_trigger_policy.py",
    }:
        assert required in documented


def test_full_model3_production_remains_manual_only() -> None:
    assert FULL_PRODUCTION.is_file()
    text = FULL_PRODUCTION.read_text(encoding="utf-8")
    assert "workflow_dispatch" in text
    assert "pull_request" not in text
    assert "schedule:" not in text
