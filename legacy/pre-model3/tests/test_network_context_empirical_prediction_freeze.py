import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREDICTIONS = ROOT / "data/design/network_context_empirical_prediction_freeze.json"
GUAIACUM = ROOT / "data/design/guaiacum_network_context_mapping_preflight.json"
CORRECTION = ROOT / "data/results/guaiacum_propagation_state_correction.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_network_context_predictions_require_rate_weighted_direct_service():
    data = load(PREDICTIONS)
    assert data["status"] == "predictions_frozen_before_any_network_context_empirical_mapping_or_parameter_selection"
    assert data["primary_empirical_estimand"].startswith("rate_weighted_effective_service")
    required = set(data["required_measurements"])
    assert "visitor-specific visit rate or abundance on the same effort scale" in required
    assert any("direct effectiveness" in row for row in required)
    assert data["parameter_rule"].startswith("The frozen synthetic support strength must not be tuned")


def test_guaiacum_is_axis_decoupling_reference_not_buffer_candidate():
    preflight = load(GUAIACUM)
    correction = load(CORRECTION)
    assert preflight["role"] == "network_context_service_mapping_reference_not_whole_reproduction_buffer_case"
    assert correction["corrected_propagation_state"] == "reproductive_axes_decouple"
    assert correction["buffer_candidate_status"].startswith("remove_from_reproductive_buffer_portfolio")
    assert preflight["mapping_to_abm"]["status"] == "not_mapping_ready"
    assert preflight["mapping_to_abm"]["support_strength_tuning_allowed"] is False


def test_guaiacum_mapping_does_not_invent_per_visit_effectiveness():
    data = load(GUAIACUM)
    mapping = data["primary_mapping"]
    assert mapping["total_effective_service"] == "S_total = sum_k(V_k * E_k)"
    assert "transported effectiveness from another species or unmatched population" in mapping["forbidden_substitutes"]
    identity = data["service_equivalence_identity"]
    assert "E_Mona / E_Guanica = V_Guanica / V_Mona" in identity["general_form"]
    assert "not a recovered per-visit-effectiveness estimate" in identity["boundary"]


def test_future_data_can_distinguish_service_mapping_from_downstream_filter():
    data = load(PREDICTIONS)
    signatures = data["decision_signatures"]
    assert any("rate-weighted total effective service is maintained" in row for row in signatures["supports_network_context_or_service_redundancy"])
    assert any("effective service is clearly lower" in row for row in signatures["weakens_network_context_as_sufficient_buffer"])
    assert any("effective service remains lower" in row for row in signatures["supports_downstream_filter_after_network_context"])
    assert "visitor composition differs but per-visit effectiveness is absent" in signatures["unresolved"]


def test_system_specific_predictions_keep_hawaii_nicotiana_and_ogasawara_distinct():
    data = load(PREDICTIONS)
    rows = {row["system_id"]: row for row in data["system_specific_frozen_predictions"]}
    assert rows["puerto_rico_mona_guaiacum"]["current_status"] == "prediction_frozen_mapping_not_ready"
    assert rows["hawaii_lobelioids_2026"]["current_status"] == "prediction_frozen_mapping_not_ready"
    assert rows["california_channel_islands_nicotiana_glauca"]["current_status"] == "prediction_frozen_mapping_not_ready"
    assert rows["ogasawara_psychotria_homalosperma"]["role"] == "propagation_reference"
