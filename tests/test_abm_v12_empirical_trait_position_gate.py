import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data" / "design" / "abm_v12_empirical_trait_position_gate.json"


def load_gate():
    return json.loads(DESIGN.read_text(encoding="utf-8"))


def test_signed_position_is_the_preferred_empirical_construct():
    gate = load_gate()
    mapping = gate["empirical_mapping_principle"]
    assert mapping["target_construct"] == "signed initial plant position relative to the pollinator functional environment"
    assert "plant_matching_trait_mm" in mapping["preferred_direct_form"]
    assert "pollinator_functional_center_mm" in mapping["preferred_direct_form"]
    forbidden = " ".join(mapping["forbidden_substitutions"]).lower()
    assert "tm_sp_z" in forbidden
    assert "fdq" in forbidden


def test_izu_direct_signed_test_remains_blocked_without_source_native_traits_and_weights():
    gate = load_gate()
    route = next(item for item in gate["evidence_routes"] if item["id"] == "izu_signed_functional_position")
    assert route["decision"] == "blocked_for_direct_signed_position_test"
    assert route["pollinator_trait_available"] is False
    assert route["current_numeric_proboscis_coverage"] == "0/209 current named pollinator taxa"
    assert len(route["reopen_conditions"]) == 3


def test_southwest_pacific_is_consistency_not_causal_confirmation():
    gate = load_gate()
    route = next(item for item in gate["evidence_routes"] if item["id"] == "southwest_pacific_starting_state")
    assert route["role"] == "independent_preexisting_external_consistency"
    assert route["causal_confirmation"] is False
    assert route["measurement_error_gate"]["mainland_log_size_reliability_estimated_from_source"] is False
    assert route["measurement_error_gate"]["cluster_interval_entirely_negative_requires_reliability_gt"] > 0.9


def test_issue91_is_not_promoted_to_cross_lineage_validation():
    gate = load_gate()
    route = next(item for item in gate["evidence_routes"] if item["id"] == "issue91_campanula_direct_field")
    assert "single Campanula lineage" in route["limitation_for_v12"]
    assert "cross-lineage" in route["limitation_for_v12"]


def test_current_inference_keeps_empirical_causation_open():
    gate = load_gate()
    unsupported = " ".join(gate["current_inference"]["not_yet_supported"]).lower()
    assert "caused" in unsupported
    assert "reproductive dependency is empirically irrelevant" in unsupported
