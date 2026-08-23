import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "data/design/system_agnostic_multi_system_validation_gate.json"


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


def test_validation_spans_multiple_observed_state_classes():
    data = load()
    targets = {row["system_id"]: row["target_state"] for row in data["qualitative_validation_targets"]}
    assert len(targets) == 6
    assert targets["ogasawara_psychotria_homalosperma"] == "propagates_same_direction"
    assert targets["hawaii_lobelioids_2026"] == "buffered_or_resilient"
    assert targets["izu_multi_taxon_hiraiwa"] == "branches_downstream"
    assert targets["dominica_heliconia"] == "counterdirectional_to_frozen_signed_position_prediction"
    assert targets["california_channel_islands_nicotiana_glauca"] == "buffered_or_alternative_mechanism"
    assert targets["puerto_rico_mona_guaiacum"] == "buffered_or_resilient"


def test_existing_abm_failures_are_preserved_not_retuned():
    data = load()
    failures = data["existing_abm_state"]["protected_failures"]
    assert "v12_dominica_signed_position_prediction_failed_declared_direction" in failures
    assert "partner_effectiveness_not_sufficient_to_generate_total_branching" in failures
    assert "dependency_heterogeneity_not_required_for_branch_generation" in failures
    assert data["programme_rule"]["failed_system_prediction_is_retained_as_a_result"] is True


def test_validation_is_qualitative_not_a_fake_pooled_effect():
    data = load()
    assert data["success_is_not"] == "matching every system numerically"
    assert "pooled effect-size model" in data["claim_boundary"]
    assert "does not claim that the ABM mechanism is empirically identified" in data["claim_boundary"]
