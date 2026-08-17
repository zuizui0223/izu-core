import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data" / "design"


def load(name: str):
    return json.loads((DESIGN / name).read_text(encoding="utf-8"))


def test_programme_unit_is_independent_island_system_not_izu():
    routing = load("active_development_mainline.json")
    assert routing["programme_scope"] == "comparative_island_pollination_response_programme"
    assert routing["programme_unit"] == "independent_island_system"
    contract = routing["comparison_contract"]
    assert contract["systems_are_parallel"] is True
    assert contract["izu_role"] == "calibration_and_mechanistic_anchor_system_not_programme_center"
    assert routing["workstreams"][1]["name"] == "island_system_response_matrix"
    assert routing["workstreams"][1]["priority"] == 1


def test_nectar_guide_is_active_comparative_axis_not_programme_wide_blocked():
    axes = load("island_comparative_response_axis_registry.json")
    routing = load("active_development_mainline.json")
    visual = next(axis for axis in axes["response_axes"] if axis["id"] == "visual_signal")
    assert "nectar_guide" in visual["examples"]
    assert axes["current_programme_boundaries"]["nectar_guide_axis_programme_status"] == (
        "active_comparative_axis_system_specific_evidence_required"
    )
    assert routing["protected_scientific_state"]["izu_visible_signal"] == (
        "currently_unmeasured_not_programme_wide_exclusion"
    )
    assert not any("nectar_guide" in item for item in routing["not_mainline"])


def test_system_matrix_treats_missing_as_missing_not_zero():
    matrix = load("island_system_response_axis_matrix.json")
    assert matrix["current_pattern"]["uniform_response_syndrome_supported"] is False
    assert matrix["current_pattern"]["response_heterogeneity_recurs"] is True
    izu = next(system for system in matrix["systems"] if system["system_id"] == "izu")
    assert izu["role"] == "calibration_and_mechanistic_anchor"
    assert izu["axes"]["visual_signal"] == "missing_current_measurement_not_zero"
    assert len(matrix["systems"]) >= 10
    for system in matrix["systems"]:
        assert set(system["axes"]) == set(matrix["response_axes"])


def test_complete_bridge_remains_closed_while_axis_comparison_is_open():
    routing = load("active_development_mainline.json")
    protected = routing["protected_scientific_state"]
    assert protected["external_mechanism_bridge_state"]["complete_systems"] == 0
    assert protected["formal_cross_system_fit_ready"] is False
    assert routing["comparison_contract"]["complete_mechanism_bridge_is_high_value_but_not_required_for_axis_level_comparison"] is True
