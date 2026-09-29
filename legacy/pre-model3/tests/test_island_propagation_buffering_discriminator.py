import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/island_propagation_buffering_discriminator_v1.json"
CORRECTION = ROOT / "data/results/guaiacum_propagation_state_correction.json"
MAINLINE = ROOT / "data/design/active_development_mainline.json"


def load():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def correction():
    return json.loads(CORRECTION.read_text(encoding="utf-8"))


def case(case_id):
    return next(row for row in load()["cases"] if row["case_id"] == case_id)


def discrimination(name):
    return next(row for row in load()["cross_case_discriminations"] if row["hypothesis"] == name)


def test_current_case_vocabulary_uses_correction_overlay_for_guaiacum():
    data = load()
    historical_states = {row["case_id"]: row["propagation_state"] for row in data["cases"]}
    assert historical_states["ogasawara_psychotria_homalosperma"] == "propagates_same_direction"
    assert historical_states["hawaii_lobelioids_2026"] == "buffered_or_resilient"
    assert historical_states["izu_hiraiwa_and_campanula_anchor"] == "branches_downstream"
    assert historical_states["california_channel_islands_nicotiana_glauca"] == "buffered_or_alternative_mechanism"
    # v1 is retained as historical evidence; current Guaiacum state is explicitly superseded.
    assert historical_states["puerto_rico_mona_guaiacum"] == "buffered_or_resilient"
    assert correction()["corrected_propagation_state"] == "reproductive_axes_decouple"
    assert correction()["supersedes"]["old_propagation_state"] == "buffered_or_resilient"


def test_autonomous_assurance_is_not_promoted_to_universal_buffer():
    d = discrimination("autonomous_reproductive_assurance_is_the_universal_buffer")
    assert d["decision"] == "rejected_as_universal"
    guaiacum = case("puerto_rico_mona_guaiacum")
    assurance = guaiacum["candidate_filters"]["autonomous_reproductive_assurance"]
    assert assurance["evidence_state"] == "argues_against_universal_assurance_buffer"
    assert "pollen vector is required" in assurance["evidence"]
    assert correction()["buffer_candidate_status"].startswith("remove_from_reproductive_buffer_portfolio")


def test_ogasawara_and_hawaii_remain_propagation_and_buffer_boundary_references():
    ogasawara = case("ogasawara_psychotria_homalosperma")
    hawaii = case("hawaii_lobelioids_2026")
    assert ogasawara["candidate_filters"]["physical_access_or_functional_matching"]["evidence_state"] == "direct_support_for_propagation"
    assert hawaii["candidate_filters"]["physical_access_or_functional_matching"]["evidence_state"] == "direct_upstream_effect_not_sufficient_for_reproductive_collapse"
    assert hawaii["candidate_filters"]["direct_reproductive_dependency"]["evidence_state"] == "missing"


def test_nicotiana_keeps_establishment_filter_live_when_current_service_deficit_is_absent():
    nicotiana = case("california_channel_islands_nicotiana_glauca")
    assert nicotiana["candidate_filters"]["colonization_or_establishment_filtering"]["evidence_state"] == "live_source_supported_alternative"
    assert nicotiana["candidate_filters"]["partner_effectiveness_or_service_redundancy"]["evidence_state"] == "current_service_adequate"
    d = discrimination("current_pollinator_service_deficit_is_required_for_island_trait_or_assurance_difference")
    assert d["decision"] == "rejected_as_universal"


def test_guaiacum_current_reading_separates_breeding_index_from_realized_reproduction():
    c = correction()
    assert c["corrected_propagation_state"] == "reproductive_axes_decouple"
    assert "self/outcross seed-set index is similar" in c["corrected_observed_pattern"]
    assert "open reproductive performance is not equivalently maintained" in c["corrected_observed_pattern"]
    assert "Mona" in " ".join(c["source_native_facts_requiring_correction"]["realized_reproductive_performance"])


def test_no_single_common_buffer_is_claimed_and_issue91_is_not_programme_blocker():
    d = discrimination("one_common_buffering_mechanism_is_already_identified")
    assert d["decision"] == "not_supported"
    mainline = json.loads(MAINLINE.read_text(encoding="utf-8"))
    assert mainline["protected_scientific_state"]["mechanism_decomposition"]["empirically_identified_universal_buffer"] is False
    assert mainline["protected_scientific_state"]["issue91_prediction_freeze"]["programme_blocker"] is False
    assert mainline["protected_scientific_state"]["buffer_mechanism_admission"]["candidate_count"] == 2


def test_current_next_gate_is_network_service_mapping_not_hidden_cause():
    mainline = json.loads(MAINLINE.read_text(encoding="utf-8"))
    assert mainline["protected_scientific_state"]["buffer_mechanism_admission"]["mapping_ready_count"] == 0
    assert mainline["protected_scientific_state"]["buffer_mechanism_admission"]["empirically_admitted_count"] == 0
    assert mainline["comparison_contract"]["network_context_empirical_prediction_freeze"] == "data/design/network_context_empirical_prediction_freeze.json"
    assert "visitor_assemblage_difference_as_service_redundancy_without_per_visit_effectiveness" in mainline["not_mainline"]
