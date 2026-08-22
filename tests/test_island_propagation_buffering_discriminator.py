import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/island_propagation_buffering_discriminator_v1.json"


def load():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def case(case_id):
    return next(row for row in load()["cases"] if row["case_id"] == case_id)


def discrimination(name):
    return next(row for row in load()["cross_case_discriminations"] if row["hypothesis"] == name)


def test_five_cases_span_propagation_buffering_branching_and_alternative_mechanisms():
    data = load()
    states = {row["case_id"]: row["propagation_state"] for row in data["cases"]}
    assert len(states) == 5
    assert states["ogasawara_psychotria_homalosperma"] == "propagates_same_direction"
    assert states["hawaii_lobelioids_2026"] == "buffered_or_resilient"
    assert states["puerto_rico_mona_guaiacum"] == "buffered_or_resilient"
    assert states["izu_hiraiwa_and_campanula_anchor"] == "branches_downstream"
    assert states["california_channel_islands_nicotiana_glauca"] == "buffered_or_alternative_mechanism"


def test_autonomous_assurance_is_not_promoted_to_universal_buffer():
    d = discrimination("autonomous_reproductive_assurance_is_the_universal_buffer")
    assert d["decision"] == "rejected_as_universal"
    guaiacum = case("puerto_rico_mona_guaiacum")
    assurance = guaiacum["candidate_filters"]["autonomous_reproductive_assurance"]
    assert assurance["evidence_state"] == "argues_against_universal_assurance_buffer"
    assert "pollen vector is required" in assurance["evidence"]


def test_ogasawara_and_hawaii_form_propagation_vs_buffering_contrast_without_numeric_overclaim():
    ogasawara = case("ogasawara_psychotria_homalosperma")
    hawaii = case("hawaii_lobelioids_2026")
    assert ogasawara["candidate_filters"]["physical_access_or_functional_matching"]["evidence_state"] == "direct_support_for_propagation"
    assert "categorical rather than a numeric signed-position" in ogasawara["candidate_filters"]["physical_access_or_functional_matching"]["interpretation"]
    assert hawaii["candidate_filters"]["physical_access_or_functional_matching"]["evidence_state"] == "direct_upstream_effect_not_sufficient_for_reproductive_collapse"
    assert hawaii["candidate_filters"]["direct_reproductive_dependency"]["evidence_state"] == "missing"


def test_nicotiana_keeps_establishment_filter_live_when_current_service_deficit_is_absent():
    nicotiana = case("california_channel_islands_nicotiana_glauca")
    assert nicotiana["candidate_filters"]["colonization_or_establishment_filtering"]["evidence_state"] == "live_source_supported_alternative"
    assert nicotiana["candidate_filters"]["partner_effectiveness_or_service_redundancy"]["evidence_state"] == "current_service_adequate"
    d = discrimination("current_pollinator_service_deficit_is_required_for_island_trait_or_assurance_difference")
    assert d["decision"] == "rejected_as_universal"


def test_no_single_common_buffer_is_claimed():
    data = load()
    d = discrimination("one_common_buffering_mechanism_is_already_identified")
    assert d["decision"] == "not_supported"
    assert data["programme_decision"] == "reject_single_buffer_explanation_prioritize_matched_dependency_effectiveness_measurements"
    assert "No single tested downstream filter" in data["current_causal_reading"]["central_result"]


def test_issue91_is_ranked_first_and_still_empirical_data_missing():
    data = load()
    first = data["ranked_next_measurements"][0]
    assert first["rank"] == 1
    assert first["target"] == "Izu Issue #91 direct dependency/effective-service anchor"
    assert first["status"] == "implementation_ready_field_data_missing"
    assert "open/bagged-autonomous/supplemental-outcross" in first["measurement"]


def test_candidate_labels_are_not_converted_to_hidden_causes():
    data = load()
    assert "does not estimate causal effect sizes" in data["claim_boundary"]
    assert "remain hypotheses" in data["claim_boundary"]
