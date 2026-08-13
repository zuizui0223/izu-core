import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/cross_archipelago_morphology/hetherington_2019_measurement_consistency_validation.json"


def load_result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_source_locked_repeat_measurements_are_recorded_exactly():
    result = load_result()
    lock = result["source_lock"]
    assert lock["handle"] == "1807/96116"
    assert lock["sha256"] == "15e0f48f0bb48e8516e848bafc73b89e1a7c2303e558e4fae84ee18a8cf5f453"
    repeats = result["within_individual_repeat_regressions"]
    assert [row["r_squared"] for row in repeats] == [0.94, 0.88, 0.93]
    assert [row["slope"] for row in repeats] == [0.97, 0.82, 0.88]


def test_equal_error_proxy_cannot_be_promoted_to_observed_reliability():
    result = load_result()
    thresholds = result["southwest_pacific_eiv_reference_thresholds"]
    assessment = result["estimand_assessment"]
    state = result["admission_state"]
    assert thresholds["all_three_equal_error_proxies_exceed_island_cluster_threshold"] is True
    assert assessment["sqrt_r_squared_is_admissible_reliability_without_extra_assumptions"] is False
    assert assessment["assumptions_supported_by_source"] is False
    assert state["external_empirical_measurement_consistency_source_recovered"] is True
    assert state["empirical_reliability_coefficient_identified"] is False
    assert state["southwest_pacific_eiv_gate_opened"] is False
    assert state["hendriks_eiv_gate_opened"] is False
    assert state["formal_cross_system_admission_opened"] is False
