import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "data/design/system_agnostic_multi_system_validation_gate.json"
CORRECTION = ROOT / "data/results/guaiacum_propagation_state_correction.json"


def load():
    return json.loads(GATE.read_text(encoding="utf-8"))


def test_programme_is_not_blocked_by_campanula_or_issue91():
    data = load()
    rule = data["programme_rule"]
    assert rule["campanula_is_one_anchor_not_centre"] is True
    assert rule["issue91_can_progress_in_parallel"] is True
    assert rule["programme_can_progress_without_issue91_field_rows"] is True
    assert rule["no_single_focal_taxon_can_block_programme"] is True
    assert rule["no_retuning_to_any_one_system"] is True
    assert rule["axis_specific_reproductive_responses_must_not_be_collapsed_into_one_buffer_label"] is True


def test_validation_spans_propagation_buffering_branching_decoupling_and_falsification():
    data = load()
    targets = {row["system_id"]: row["target_state"] for row in data["qualitative_validation_targets"]}
    assert len(targets) == 6
    assert targets["ogasawara_psychotria_homalosperma"] == "propagates_same_direction"
    assert targets["hawaii_lobelioids_2026"] == "buffered_or_resilient"
    assert targets["izu_multi_taxon_hiraiwa"] == "branches_downstream"
    assert targets["dominica_heliconia"] == "counterdirectional_to_frozen_signed_position_prediction"
    assert targets["california_channel_islands_nicotiana_glauca"] == "buffered_or_alternative_mechanism"
    assert targets["puerto_rico_mona_guaiacum"] == "reproductive_axes_decouple"


def test_network_context_buffering_is_a_synthetic_capability_not_empirical_mapping():
    data = load()
    buffered = data["existing_abm_state"]["synthetic_buffering_state"]
    assert buffered["network_context_sign_rescue_replicated"] is True
    assert buffered["result"] == "data/results/network_context_buffering_capability_robustness_frozen.json"
    assert "can also worsen" in buffered["interpretation"]
    assert "empirically identifies" in data["claim_boundary"]


def test_guaiacum_correction_is_explicit_and_not_whole_reproduction_buffering():
    data = load()
    row = next(row for row in data["qualitative_validation_targets"] if row["system_id"] == "puerto_rico_mona_guaiacum")
    correction = json.loads(CORRECTION.read_text(encoding="utf-8"))
    assert row["correction"] == "data/results/guaiacum_propagation_state_correction.json"
    assert correction["corrected_propagation_state"] == "reproductive_axes_decouple"
    assert correction["buffer_candidate_status"].startswith("remove_from_reproductive_buffer_portfolio")
    assert "Mona" in correction["corrected_observed_pattern"]
    assert "open reproductive performance differs" in correction["boundary"]


def test_existing_abm_failures_are_preserved_not_retuned():
    data = load()
    failures = data["existing_abm_state"]["protected_failures"]
    assert "v12_dominica_signed_position_prediction_failed_declared_direction" in failures
    assert "partner_effectiveness_not_sufficient_to_generate_total_branching" in failures
    assert "dependency_heterogeneity_not_required_for_branch_generation" in failures
    assert "assurance_sign_buffering_not_replicated_in_independent_v14_block" in failures
    assert data["programme_rule"]["failed_system_prediction_is_retained_as_a_result"] is True


def test_validation_is_qualitative_not_a_fake_pooled_effect():
    data = load()
    assert data["success_is_not"] == "matching every system numerically"
    assert "pooled effect-size model" in data["claim_boundary"]
    assert "does not claim" in data["claim_boundary"]
