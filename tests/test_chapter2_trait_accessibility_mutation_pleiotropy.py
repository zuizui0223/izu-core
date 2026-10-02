import json
import warnings
from pathlib import Path

from scripts.run_chapter2_trait_accessibility_mutation_pleiotropy import run

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_trait_accessibility_mutation_pleiotropy_next_20261002.json"


def test_prospectively_frozen_mutation_pleiotropy_extension() -> None:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    assert design["status"] == "prospective_frozen_before_execution"
    assert design["implementation_boundary"]["ecological_reproduction_rules_changed"] is False
    assert design["implementation_boundary"]["demographic_rules_changed"] is False

    result = run(design)

    # Prospectively frozen scientific predictions. Failure is a scientific
    # result; do not weaken these assertions after inspecting the outcome.
    compact = {
        "mutation_accessibility_tests": result["mutation_accessibility_tests"],
        "mutation_accessibility_supported": result["mutation_accessibility_supported"],
        "pleiotropy_tests": result["pleiotropy_tests"],
        "right_aligned_pleiotropy_facilitated": result["right_aligned_pleiotropy_facilitated"],
        "left_antagonistic_pleiotropy_constrained": result["left_antagonistic_pleiotropy_constrained"],
        "context_dependent_pleiotropy_supported": result["context_dependent_pleiotropy_supported"],
        "cell_summary": result["cell_summary"],
    }
    warnings.warn("MUT_PLEIO_NUMERIC " + json.dumps(compact, sort_keys=True))
    assert result["n_trajectories"] == 288
    assert result["mutation_accessibility_supported"] is True
    assert result["context_dependent_pleiotropy_supported"] is True
