import json
from pathlib import Path

from scripts.audit_frozen_abm_state_separability import build

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "data/results/frozen_abm_state_separability_frozen.json"


def test_separability_regenerates_exactly():
    assert build() == json.loads(FROZEN.read_text(encoding="utf-8"))


def test_mixed_sign_is_specific_but_insensitive():
    result = build()["diagnostics"]["mixed_sign_branching_as_trait_heterogeneity_diagnostic"]
    assert result["specificity"] == 1.0
    assert result["sensitivity"] < 0.5
    assert result["false_positive_rate"] == 0.0
    assert result["false_negative_rate"] > 0.5


def test_same_direction_is_not_identifying():
    result = build()["diagnostics"]["same_direction_as_trait_uniformity_diagnostic"]
    assert result["sensitivity"] == 1.0
    assert result["false_positive_rate"] > 0.5
    assert result["specificity"] < 0.5


def test_strong_buffer_and_attenuation_have_different_diagnostic_value():
    diagnostics = build()["diagnostics"]
    sign = diagnostics["sign_rescue_as_network_context_vs_assurance_diagnostic"]
    attenuation = diagnostics["magnitude_attenuation_as_assurance_vs_network_context_diagnostic"]
    assert sign["specificity_against_assurance"] == 1.0
    assert sign["network_context_sensitivity"] < 0.2
    assert attenuation["assurance_sensitivity"] > 0.95
    assert attenuation["network_context_false_positive_rate"] > 0.88
    assert attenuation["specificity_against_network_context"] < 0.12


def test_assurance_state_does_not_cross_to_sign_buffering_across_saturations():
    states = build()["transition_boundaries"]["assurance_across_saturations_1_2_3"]["by_saturation"]
    assert set(states) == {"1.0", "2.0", "3.0"}
    assert all(row["sign_rescue_fraction"] == 0.0 for row in states.values())
    assert all(row["magnitude_attenuation_fraction"] > 0.94 for row in states.values())
