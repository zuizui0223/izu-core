import json
from copy import deepcopy
from pathlib import Path

from scripts.run_chapter2_mutation_input_calibration_sensitivity import run

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_mutation_input_calibration_sensitivity_20261002.json"
RESULT = ROOT / "data/results/chapter2_mutation_input_calibration_sensitivity_20261002.json"


def test_frozen_mutation_input_calibration_receipt() -> None:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert design["status"] == "prospective_frozen_before_execution"
    assert result["status"] == "complete_prospective_mutation_input_calibration_sensitivity"
    assert result["n_trajectories"] == 160
    assert result["decisions"]["standing_dominates_at_400"] is True
    assert result["decisions"]["standing_dominates_at_800"] is True
    assert result["decisions"]["ranking_reversal_at_400"] is False
    assert result["decisions"]["ranking_reversal_at_800"] is False
    assert result["headline_decision"] == "retain_standing_variation_dominates_with_finite_horizon_qualification"
    assert result["response_ratios"]["high_standing_over_low_mutation_anchor_y800"] < result["response_ratios"]["high_standing_over_low_mutation_anchor_y400"]


def test_mutation_input_calibration_runner_smoke() -> None:
    design = deepcopy(json.loads(DESIGN.read_text(encoding="utf-8")))
    design["baseline"]["founder_seeds"] = [77401]
    design["baseline"]["demographic_seeds"] = [601]
    design["baseline"]["visitor_histories"] = {"left4": [0.15, 0.25, 0.35, 0.45]}
    design["capacities"] = [48]
    design["mutation_input"]["low_standing_VM_over_VG0"] = [0.0, 0.01]
    design["mutation_input"]["high_reference_VM_over_VG0"] = [0.0]
    result = run(design)
    assert result["n_trajectories"] == 3
    assert result["headline_decision"] in {
        "retain_standing_variation_dominates_with_finite_horizon_qualification",
        "drop_standing_variation_dominance_claim",
    }
