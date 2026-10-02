import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_trait_accessibility_pilot_20261002.json"
RESULT = ROOT / "data/results/chapter2_trait_accessibility_pilot_20261002.json"


def test_frozen_trait_accessibility_pilot_receipt() -> None:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    result = json.loads(RESULT.read_text(encoding="utf-8"))

    assert design["status"] == "prospective_pilot_frozen_before_execution"
    assert design["operator"]["operator_changes_allowed"] is False
    assert design["operator"]["mutation_rate"] == 0.0

    assert result["status"] == "complete_trait_accessibility_pilot"
    assert result["standing_variation_filter_supported"] is True
    assert result["contrasts"]["access_variation_effect_deterministic"] > 0
    assert result["contrasts"]["investment_variation_effect_deterministic"] > 0
    assert result["contrasts"]["access_variation_effect_finite_abm"] > 0
    assert result["contrasts"]["investment_variation_effect_finite_abm"] > 0
