import json
from pathlib import Path

INITIAL = Path("data/results/network_context_buffering_capability_ablation_frozen.json")
ROBUST = Path("data/results/network_context_buffering_capability_robustness_frozen.json")


def test_initial_network_context_block_has_sparse_sign_rescue_and_bidirectionality():
    initial = json.loads(INITIAL.read_text(encoding="utf-8"))
    s = initial["summary"]
    assert s["global_decline_and_support_off_reproduction_decline"] == 89
    assert s["reproduction_sign_rescue_count"] == 2
    assert s["reproduction_magnitude_rescue_count"] == 52
    assert s["reproduction_worsening_count"] == 37
    assert initial["empirical_mechanism_admission_changed"] is False


def test_independent_block_replicates_network_context_sign_rescue():
    robust = json.loads(ROBUST.read_text(encoding="utf-8"))
    s = robust["independent_summary"]
    assert s["global_decline_and_support_off_reproduction_decline"] == 96
    assert s["reproduction_sign_rescue_count"] == 16
    assert s["reproduction_magnitude_rescue_count"] == 85
    assert s["reproduction_worsening_count"] == 11
    assert robust["initial_block_comparison"]["independent_sign_rescue_replicated"] is True
    assert robust["initial_block_comparison"]["magnitude_rescue_replicated"] is True
    assert robust["initial_block_comparison"]["worsening_also_present_in_both_blocks"] is True
    assert robust["decision"] == "network_context_sign_buffering_capability_replicates_but_route_is_bidirectional_and_context_dependent"


def test_network_context_capability_does_not_empirically_admit_guaiacum():
    robust = json.loads(ROBUST.read_text(encoding="utf-8"))
    assert robust["empirical_mechanism_admission_changed"] is False
    assert robust["guaiacum_service_redundancy_candidate_state"] == "candidate_only_no_abm_admission"
    assert "not empirical mechanism identification" in robust["claim_boundary"]
