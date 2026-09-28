import json
from pathlib import Path

RESULT = Path("data/results/network_context_rescue_discriminator_frozen.json")
PRIORITY = Path("data/design/network_context_empirical_measurement_priority.json")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_frozen_result_exactly_nests_parent_classes():
    result = load(RESULT)
    assert result["parent_nesting"]["exact_nesting_passes"] is True
    assert result["class_counts"] == {
        "sign_rescue": 16,
        "attenuation_only": 69,
        "worsening": 11,
        "other_no_material_change": 0,
    }
    assert result["configuration"]["new_parameter_count"] == 0
    assert result["configuration"]["empirical_targets_loaded"] == []


def test_active_context_and_partner_retention_are_predeclared_measurement_priorities():
    result = load(RESULT)
    rescue = result["class_descriptor_means"]["sign_rescue"]
    attenuation = result["class_descriptor_means"]["attenuation_only"]
    worsening = result["class_descriptor_means"]["worsening"]
    assert rescue["support_on_island_minus_mainland_active_context_fraction"] == 0.0
    assert attenuation["support_on_island_minus_mainland_active_context_fraction"] < -0.4
    assert worsening["support_on_island_minus_mainland_active_context_fraction"] < -0.4
    assert rescue["support_on_island_minus_mainland_mean_positive_partner_count"] > attenuation["support_on_island_minus_mainland_mean_positive_partner_count"]
    assert rescue["support_on_island_minus_mainland_mean_positive_partner_count"] > worsening["support_on_island_minus_mainland_mean_positive_partner_count"]

    priority = load(PRIORITY)
    assert priority["priorities"][0]["measurement"] == "repeated_local_active_context_fraction"
    assert priority["priorities"][1]["measurement"] == "repeated_positive_partner_count"
    assert priority["priorities"][2]["measurement"] == "visitor_specific_direct_effectiveness"


def test_initial_trait_is_not_promoted_as_rescue_cause_from_this_diagnostic():
    result = load(RESULT)
    contrast = result["predeclared_mean_contrasts"]["sign_rescue_minus_attenuation_only"]
    assert abs(contrast["initial_lineage_trait"]) < 0.01
    priority = load(PRIORITY)
    assert priority["priorities"][4]["measurement"] == "plant_functional_position_and_dependency_as_modifiers"
    assert "do not require them to explain network rescue" in priority["priorities"][4]["definition"]


def test_dominance_is_not_reinterpreted_post_hoc():
    result = load(RESULT)
    assert "zero coding" in result["caution"]
    priority = load(PRIORITY)
    assert "treat repeated active-context fraction as a causal buffer coefficient" in priority["forbidden"]
