import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/constraint_mechanism_abm_v14_assurance_buffering_frozen.json"


def test_v14_frozen_result_keeps_synthetic_and_empirical_claims_separate():
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    overall = data["overall"]
    assert data["upstream_service_identical_between_assurance_ablations"] is True
    assert data["upstream_service_mismatch_count"] == 0
    assert overall["lineage_contrasts"] == 288
    assert overall["service_decline_lineages"] == 202
    assert overall["synthetic_buffering_assurance_on"] == 1
    assert overall["synthetic_buffering_assurance_off"] == 0
    assert overall["assurance_sign_rescues"] == 1
    assert overall["assurance_magnitude_rescues"] == 197
    assert data["decision"] == "existing_assurance_route_is_synthetically_sufficient_for_sign_level_buffering_in_frozen_model"
    assert data["empirical_mechanism_admission_changed"] is False
    assert data["hawaii_assurance_candidate_state"] == "candidate_only_no_abm_admission"


def test_sign_rescue_occurs_only_in_lowest_saturation_in_frozen_run():
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    assert data["by_saturation"]["1.0"]["assurance_sign_rescues"] == 1
    assert data["by_saturation"]["2.0"]["assurance_sign_rescues"] == 0
    assert data["by_saturation"]["3.0"]["assurance_sign_rescues"] == 0
    assert data["overall"]["service_decline_buffer_fraction_assurance_on"] == 1 / 202
