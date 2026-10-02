import json
from copy import deepcopy
from pathlib import Path

from scripts.run_chapter2_trait_accessibility_mutation_pleiotropy import run

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_trait_accessibility_mutation_pleiotropy_next_20261002.json"
FROZEN_RESULT = ROOT / "data/results/chapter2_trait_accessibility_mutation_pleiotropy_20261002.json"


def test_frozen_mutation_pleiotropy_failure_receipt() -> None:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    frozen = json.loads(FROZEN_RESULT.read_text(encoding="utf-8"))
    assert design["status"] == "prospective_frozen_before_execution"
    assert design["implementation_boundary"]["ecological_reproduction_rules_changed"] is False
    assert design["implementation_boundary"]["demographic_rules_changed"] is False
    assert frozen["status"] == "complete_prospective_failure_not_identified"
    assert frozen["n_trajectories"] == 288
    assert frozen["mutation_accessibility_supported"] is False
    assert frozen["context_dependent_pleiotropy_supported"] is False
    assert frozen["right_aligned_pleiotropy_facilitated"] is False
    assert frozen["left_antagonistic_pleiotropy_constrained"] is False
    assert frozen["mutation_accessibility_tests"]["right4"]["access_accessible_gap_shift_median"] == -16.0


def test_mutation_pleiotropy_runner_smoke() -> None:
    design = deepcopy(json.loads(DESIGN.read_text(encoding="utf-8")))
    design["baseline"]["years"] = 5
    design["baseline"]["founder_seeds"] = [77201]
    design["baseline"]["demographic_seeds"] = [301]
    result = run(design)
    assert result["n_trajectories"] == 18
    assert set(result["mutation_accessibility_tests"]) == {"left4", "right4"}
    assert set(result["pleiotropy_tests"]) == {"left4", "right4"}
