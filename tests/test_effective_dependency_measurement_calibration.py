import math

from channel_id.effective_dependency_measurement_calibration import build_svd_recount_calibration


def _row(calibration_id, svd_id, recount_id, counter_id, conspecific, blinded="yes"):
    return {
        "calibration_id": calibration_id,
        "svd_id": svd_id,
        "recount_id": recount_id,
        "counter_id": counter_id,
        "blinded_to_original": blinded,
        "total_pollen_grains": str(conspecific),
        "conspecific_pollen_grains": str(conspecific),
        "heterospecific_pollen_grains": "0",
        "unclassified_pollen_grains": "0",
    }


def test_three_samples_with_recounts_estimate_technical_repeatability_only():
    rows = (
        _row("c1", "s1", "r1", "A", 10),
        _row("c2", "s1", "r2", "B", 11),
        _row("c3", "s2", "r1", "A", 30),
        _row("c4", "s2", "r2", "B", 29),
        _row("c5", "s3", "r1", "A", 50),
        _row("c6", "s3", "r2", "B", 51),
    )
    result = build_svd_recount_calibration(rows)
    rep = result["conspecific_pollen_count_repeatability"]
    assert rep["status"] == "estimable"
    assert rep["distinct_svd_samples"] == 3
    assert rep["technical_recounts"] == 6
    assert rep["technical_recount_repeatability"] > 0.99
    assert math.isclose(result["blinded_recount_fraction"], 1.0)
    assert result["distinct_counters"] == ["A", "B"]
    assert result["direct_dependency_reliability_identified"] is False


def test_too_few_recounted_samples_does_not_invent_repeatability():
    rows = (
        _row("c1", "s1", "r1", "A", 10),
        _row("c2", "s1", "r2", "B", 12),
        _row("c3", "s2", "r1", "A", 20),
        _row("c4", "s2", "r2", "B", 22),
    )
    result = build_svd_recount_calibration(rows)
    assert result["conspecific_pollen_count_repeatability"]["status"] == "not_estimable"
    assert result["direct_dependency_reliability_identified"] is False


def test_recount_partition_must_sum():
    row = _row("c1", "s1", "r1", "A", 10)
    row["total_pollen_grains"] = "11"
    try:
        build_svd_recount_calibration((row,))
    except ValueError as error:
        assert "partition does not sum" in str(error)
    else:
        raise AssertionError("expected invalid pollen partition to fail")
