import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_global_strict_extension_preserves_exact_five_gate_contract():
    registry = load("data/design/global_strict_network_context_mapping_registry.json")
    assert registry["required_gates"] == [
        "matched_transition_unit",
        "repeated_local_context_support",
        "visitor_specific_rate",
        "visitor_specific_direct_effectiveness",
        "reproductive_outcome",
    ]
    assert len(registry["systems"]) == 7
    assert "Only exact 'admitted' passes" in registry["admission_rule"]


def test_zero_of_twelve_mapping_readiness_is_preserved():
    result = load("data/results/global_strict_network_context_mapping_readiness_frozen.json")
    parent = load("data/results/network_context_mapping_readiness_frozen.json")
    assert parent["systems_screened"] == 5
    assert parent["mapping_ready_count"] == 0
    assert result["new_strict_systems_screened"] == 7
    assert result["mapping_ready_count"] == 0
    assert result["combined_with_parent"]["combined_systems_screened"] == 12
    assert result["combined_with_parent"]["combined_mapping_ready_count"] == 0


def test_closest_new_candidates_stop_at_same_context_effectiveness():
    result = load("data/results/global_strict_network_context_mapping_readiness_frozen.json")
    rows = {row["system_id"]: row for row in result["rows"]}
    for system_id in ["seychelles_ant_disruption", "canary_teide_honeybee_network"]:
        row = rows[system_id]
        assert row["n_admitted_required_gates"] == 4
        assert row["missing_required_gates"] == ["visitor_specific_direct_effectiveness"]
        assert row["network_context_mapping_ready"] is False
        assert row["named_source_search_state"] == "closed_without_same_context_Ek"
    assert result["closest_new_missing_gate"] == "visitor_specific_direct_effectiveness"


def test_seychelles_does_not_transport_pooled_qlc_into_ant_contexts():
    diag = load("data/design/seychelles_network_context_effectiveness_linkage_diagnostic.json")
    assert diag["repo_evidence"]["visitor_specific_single_visit_outcomes_available"] is True
    assert diag["repo_evidence"]["ant_disturbed_vs_undisturbed_visit_rate_available"] is True
    assert diag["repo_evidence"]["same_context_Ek_link_demonstrated"] is False
    assert diag["decision"] == "do_not_admit_visitor_specific_direct_effectiveness_for_ant_context_mapping"


def test_canary_does_not_transport_effectiveness_across_years_or_designs():
    diag = load("data/design/canary_teide_network_context_effectiveness_linkage_diagnostic.json")
    assert diag["primary_study_readout"]["visitor_specific_visit_frequency"] is True
    assert diag["primary_study_readout"]["five_plant_reproductive_response"] is True
    assert diag["primary_study_readout"]["single_visit_pollen_deposition_or_reproductive_effectiveness"] is False
    assert diag["older_teide_evidence"]["transport_as_Ek_allowed"] is False
    assert diag["decision"] == "do_not_admit_visitor_specific_direct_effectiveness_for_teide_2007_2009_mapping"


def test_next_gate_stops_unrestricted_retrospective_searching():
    result = load("data/results/global_strict_network_context_mapping_readiness_frozen.json")
    assert result["decision"].startswith("zero_of_twelve_mapping_ready")
    assert result["combined_with_parent"]["parent_named_source_search_state"] == "closed_without_Ek"
    assert "Stop unrestricted retrospective searching" in result["next_gate"]
    assert "prospective measurement" in result["next_gate"]
