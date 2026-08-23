import json
from pathlib import Path

from scripts.audit_buffer_mechanism_abm_admission import assess_candidate


ROOT = Path(__file__).resolve().parents[1]
INTERFACE = json.loads((ROOT / "data/design/buffer_mechanism_abm_admission_interface.json").read_text(encoding="utf-8"))


def candidate(**overrides):
    row = {
        "system_id": "test_island_system",
        "candidate_mechanism": "autonomous_reproductive_assurance",
        "upstream_functional_change_source_locked": True,
        "propagation_step_directly_measured": True,
        "downstream_reproductive_response_directly_measured": True,
        "candidate_filter_directly_measured": True,
        "matched_transition_or_prospectively_matched_units": True,
        "sampling_hierarchy_locked": True,
        "source_native_units_locked": True,
        "alternative_filters_recorded": True,
        "mapping_to_abm_component_predeclared": True,
        "mapping_frozen_before_target_outcome_test": True,
        "target_outcome_used_to_choose_parameter_values": False,
        "predeclared_test_result": None,
    }
    row.update(overrides)
    return row


def test_hawaii_like_cross_time_candidate_stays_candidate_only():
    result = assess_candidate(
        candidate(matched_transition_or_prospectively_matched_units=False),
        INTERFACE,
    )
    assert result["state"] == "candidate_only_no_abm_admission"
    assert result["mapping_ready"] is False
    assert result["empirically_admitted"] is False


def test_complete_preoutcome_mapping_is_only_ready_to_test():
    result = assess_candidate(candidate(), INTERFACE)
    assert result["state"] == "mapping_ready_for_heldout_test"
    assert result["mapping_ready"] is True
    assert result["empirically_admitted"] is False


def test_failed_predeclared_test_is_retained_as_failure():
    result = assess_candidate(candidate(predeclared_test_result="fail"), INTERFACE)
    assert result["state"] == "failed_predeclared_test_no_admission"
    assert result["mapping_ready"] is True
    assert result["empirically_admitted"] is False
    assert "cannot be rescued" in result["reasons"][0]


def test_passing_predeclared_test_is_the_only_empirical_admission_route():
    result = assess_candidate(candidate(predeclared_test_result="pass"), INTERFACE)
    assert result["state"] == "empirically_supported_mechanism_admission"
    assert result["empirically_admitted"] is True


def test_target_outcome_parameter_selection_is_invalid_not_model_rescue():
    result = assess_candidate(
        candidate(target_outcome_used_to_choose_parameter_values=True, predeclared_test_result="pass"),
        INTERFACE,
    )
    assert result["state"] == "invalid_posthoc_mapping_no_admission"
    assert result["empirically_admitted"] is False


def test_new_resource_component_cannot_be_admitted_without_same_rules():
    result = assess_candidate(
        candidate(candidate_mechanism="resource_or_demographic_compensation"),
        INTERFACE,
    )
    assert result["state"] == "mapping_ready_for_heldout_test"
    assert result["new_component_required_if_admitted"] is True
    assert result["empirically_admitted"] is False
