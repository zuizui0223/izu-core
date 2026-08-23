import json
from pathlib import Path


FROZEN = Path("data/results/constraint_mechanism_abm_v14b_assurance_buffering_robustness_frozen.json")


def load_result():
    return json.loads(FROZEN.read_text(encoding="utf-8"))


def test_large_independent_block_has_no_sign_rescue_and_broad_magnitude_attenuation():
    result = load_result()
    assert result["configuration"]["replicates"] == 40
    assert result["overall"]["lineage_contrasts"] == 2880
    assert result["overall"]["service_decline_lineages"] == 2015
    assert result["overall"]["assurance_sign_rescues"] == 0
    assert result["overall"]["assurance_magnitude_rescues"] == 1932
    assert result["robustness"]["magnitude_rescue_fraction"] > 0.95
    assert result["robustness"]["sign_level_replication"] is False


def test_large_block_changes_no_empirical_admission_or_model_threshold():
    result = load_result()
    assert result["configuration"]["parameter_changes_from_v14"] is False
    assert result["configuration"]["threshold_changes_from_v14"] is False
    assert result["upstream_service_identical_between_assurance_ablations"] is True
    assert result["upstream_service_mismatch_count"] == 0
    assert result["empirical_mechanism_admission_changed"] is False
    assert result["hawaii_assurance_candidate_state"] == "candidate_only_no_abm_admission"
