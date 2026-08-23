import json
from pathlib import Path

INITIAL = Path("data/results/constraint_mechanism_abm_v14_assurance_buffering_frozen.json")
ROBUST = Path("data/results/constraint_mechanism_abm_v14_assurance_buffering_robustness_frozen.json")
BROAD = Path("data/results/assurance_buffering_capability_ablation_frozen.json")


def test_initial_sign_rescue_is_preserved_not_erased():
    initial = json.loads(INITIAL.read_text(encoding="utf-8"))
    assert initial["overall"]["service_decline_lineages"] == 202
    assert initial["overall"]["assurance_sign_rescues"] == 1
    assert initial["overall"]["assurance_magnitude_rescues"] == 197


def test_independent_exact_design_block_does_not_replicate_sign_rescue():
    robust = json.loads(ROBUST.read_text(encoding="utf-8"))
    assert robust["upstream_service_identical_between_assurance_ablations"] is True
    assert robust["overall"]["service_decline_lineages"] == 216
    assert robust["overall"]["assurance_sign_rescues"] == 0
    assert robust["overall"]["assurance_magnitude_rescues"] == 207
    assert robust["initial_block_comparison"]["independent_sign_rescue_replicated"] is False
    assert robust["initial_block_comparison"]["magnitude_attenuation_replicated"] is True
    assert robust["decision"] == "assurance_magnitude_attenuation_is_robust_but_sign_level_buffering_is_not_replicated"


def test_broadened_support_envelope_also_has_no_sign_rescue():
    broad = json.loads(BROAD.read_text(encoding="utf-8"))
    summary = broad["summary"]
    assert summary["service_decline_and_assurance_off_reproduction_decline"] == 525
    assert summary["full_attenuation_count"] == 510
    assert summary["full_sign_rescue_count"] == 0
    assert broad["decision"] == "existing_assurance_route_attenuates_service_driven_reproductive_declines_without_sign_rescue"


def test_empirical_mechanism_admission_stays_closed():
    robust = json.loads(ROBUST.read_text(encoding="utf-8"))
    assert robust["empirical_mechanism_admission_changed"] is False
    assert robust["hawaii_assurance_candidate_state"] == "candidate_only_no_abm_admission"
    assert "does not validate or falsify autonomous assurance" in robust["claim_boundary"]
