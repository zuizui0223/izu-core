import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/results/cross_archipelago_morphology/empirical_reliability_identifiability.json"


def load_state():
    return json.loads(PATH.read_text(encoding="utf-8"))


def test_current_source_native_materials_do_not_identify_reliability():
    state = load_state()
    assert state["status"] == "empirical_reliability_unidentifiable_from_current_source_native_materials"
    consequence = state["current_consequence"]
    assert consequence["eiv_sensitivity_envelope_completed"] is True
    assert consequence["empirical_reliability_identified"] is False
    assert consequence["formal_cross_system_admission_opened"] is False
    assert consequence["issue_96_complete"] is False


def test_southwest_pacific_thresholds_are_not_relabelled_as_observed_reliability():
    swp = load_state()["southwest_pacific"]
    thresholds = swp["existing_classical_x_error_thresholds"]
    assert thresholds["point_direction_requires_reliability_above"] == 0.8490052881072877
    assert thresholds["island_cluster_interval_wholly_below_isometry_requires_reliability_above"] == 0.9258005353502381
    forbidden = set(swp["not_valid_reliability_substitutes"])
    assert "trait min/max range" in forbidden
    assert "source-method category" in forbidden
    assert "an assumed reliability selected to preserve below-isometry direction" in forbidden


def test_unidentifiability_result_remains_open_to_external_validation_recovery():
    state = load_state()
    assert state["next_search_targets"]
    assert "does not prove" in state["claim_boundary"].lower()
