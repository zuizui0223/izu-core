import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_syndrome_causal_knockout_20261002.json"
RESULT = ROOT / "data/results/chapter2_syndrome_causal_knockout_20261002.json"


def test_frozen_syndrome_causal_knockout_receipt() -> None:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    result = json.loads(RESULT.read_text(encoding="utf-8"))

    assert design["status"] == "prospective_frozen_before_execution"
    assert design["operator"]["operator_changes_allowed"] is False
    assert design["operator"]["new_trait_axes_allowed"] is False

    assert result["status"] == "complete_prospective_stage_A_causal_knockout"
    assert result["route_A"]["supported"] is True
    assert result["route_B"]["supported"] is True

    key = {
        (r["activity"], r["fixed_assurance"], r["investment_cost"]): r
        for r in result["route_A"]["key_rows"]
    }
    assert key[(0.05, 0.5, 0.5)]["fixed_total_gradient"] < 0
    assert key[(0.05, 0.0, 0.5)]["fixed_total_gradient"] > 0
    assert key[(0.05, 0.5, 0.0)]["fixed_total_gradient"] > 0
    assert key[(0.05, 0.0, 0.5)]["abm_terminal_occupancy"] == 0.0
    assert key[(0.05, 0.5, 0.5)]["abm_terminal_occupancy"] == 1.0

    contrasts = result["route_B"]["left_minus_right_same_count"]
    assert any(r["fixed_gradient_sign_change"] for r in contrasts)
