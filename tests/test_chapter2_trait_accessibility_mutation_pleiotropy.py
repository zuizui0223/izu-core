import json
from pathlib import Path

from scripts.run_chapter2_trait_accessibility_mutation_pleiotropy import run

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_trait_accessibility_mutation_pleiotropy_next_20261002.json"
FROZEN_RESULT = ROOT / "data/results/chapter2_trait_accessibility_mutation_pleiotropy_20261002.json"


def test_prospectively_frozen_mutation_pleiotropy_failure_is_reproducible() -> None:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    frozen = json.loads(FROZEN_RESULT.read_text(encoding="utf-8"))
    assert design["status"] == "prospective_frozen_before_execution"
    assert design["implementation_boundary"]["ecological_reproduction_rules_changed"] is False
    assert design["implementation_boundary"]["demographic_rules_changed"] is False

    result = run(design)

    # The preregistered success criteria failed in the first prospective run.
    # This is now a frozen scientific result, not a gate to be relaxed.
    assert result["n_trajectories"] == 288
    assert result["mutation_accessibility_supported"] is False
    assert result["context_dependent_pleiotropy_supported"] is False
    assert result["right_aligned_pleiotropy_facilitated"] is False
    assert result["left_antagonistic_pleiotropy_constrained"] is False
    assert result["mutation_accessibility_tests"] == frozen["mutation_accessibility_tests"]
    assert result["pleiotropy_tests"] == frozen["pleiotropy_tests"]
