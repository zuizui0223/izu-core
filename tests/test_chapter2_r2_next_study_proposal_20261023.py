"""Fail-closed boundaries on future independent R2 biological experiment."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs/protocols/CHAPTER2_R2_HISTORY_POLLEN_STATE_NEXT_STUDY_PROPOSAL_20261023.json"


def test_design_is_pending_without_claimed_registration_or_authorization():
    p = json.loads(PROTOCOL.read_text(encoding="utf8"))
    assert p["schema"] == "chapter2_r2_independent_history_service_identification_design_proposal_v1"
    assert p["status"] == "DESIGN_ONLY_NOT_AUTHORIZED_NOT_PREREGISTERED"
    assert p["existing_evidence"]["r1_r5_manuscript_claims_unchanged"]
    assert p["existing_evidence"]["registered_confirm160_G_S_unchanged"]
    assert p["existing_evidence"]["fresh_founder_r2_four_setting_status"] == "INCONCLUSIVE"
    assert p["existing_evidence"]["old_384_outcomes_will_not_be_reused_for_new_confirmation"]
    assert p["existing_evidence"]["old_pollen_protocol_sha256"] == (
        "87af92484af9988181b4f3bed6760d39325de70cca8c0b4e1cec19c47b8c9849"
    )
    assert all(value is False for value in p["run_gate"].values())


def test_no_fake_matched_pollen_or_false_isolation_of_genetic_history():
    p = json.loads(PROTOCOL.read_text(encoding="utf8"))
    assert p["design"]["native_futures"]["actual_per_mother_q_measured_not_assumed_matched"]
    assert p["design"]["static_counterfactual"]["separate_from_native_evolutionary_futures"]
    assert p["design"]["static_counterfactual"]["no_allele_transmission_or_population_updates"]
    assert p["design"]["static_counterfactual"]["never_impute_total_export_or_activity_match_as_per_mother_q_equality"]
    assert p["design"]["optional_A_state_intervention"]["status"] == "NOT_SPECIFIED_NOT_AUTHORIZED"
    assert p["independent_sampling"]["source_axes_disjoint_from_older_exposed_campaigns"]
    assert p["independent_sampling"]["founder_visitors_crossed"]
    assert p["independent_sampling"]["sample_size_power_and_precision_contract"] is None
    assert p["independent_sampling"]["registered_minimum_biologically_meaningful_A_change"] is None
    assert p["independent_sampling"]["future_founder_source_count"] is None


def test_immutable_explicit_source_capture_and_scientific_failure_gates():
    p = json.loads(PROTOCOL.read_text(encoding="utf8"))
    fields = "\n".join(p["required_start_and_each_update_capture"])
    for fragment in ("diploid alleles", "allele origins", "visitor optima",
                     "per-recipient q", "maternal", "paternal",
                     "random stream pairing", "extinction"):
        assert fragment in fields
    limits = " ".join(p["failure_and_interpretation_boundaries"]).lower()
    assert "source history" in limits
    assert "not call exact zero" in limits
    assert "not launch future biology" in limits
    assert "author signoff" in limits
    assert not p["run_gate"]["should_dispatch_actions"]
