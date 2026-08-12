import json
from pathlib import Path

from scripts.analyze_hendriks_2019_flower_area import (
    EXPECTED_ISLAND_COUNTS,
    analyze,
    attach_island_mapping,
    read_island_mapping,
    read_pairs,
)
from scripts.compare_json_numeric_tolerant import assert_json_close


ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "data/source_tables/hendriks_2019_flower_area_table_b9_reconstructed.csv"
MAPPING = ROOT / "data/source_tables/hendriks_2019_flower_area_island_mapping.csv"
SOURCE = ROOT / "data/source_tables/hendriks_2019_flower_area_table_b9_source.json"
SUMMARY = ROOT / "data/results/hendriks_2019/flower_area_reconstruction_summary.json"


def mapped_rows():
    return attach_island_mapping(read_pairs(TABLE), read_island_mapping(MAPPING))


def test_reconstruction_has_all_35_positive_pairs():
    rows = read_pairs(TABLE)
    assert len(rows) == 35
    assert [row["pair_id"] for row in rows] == list(range(1, 36))
    assert all(row["island_flower_area_cm2"] > 0 for row in rows)
    assert all(row["mainland_flower_area_cm2"] > 0 for row in rows)


def test_appendix_island_mapping_matches_table_a14_exactly():
    mapping = read_island_mapping(MAPPING)
    counts = {}
    for row in mapping.values():
        group = row["island_group"]
        counts[group] = counts.get(group, 0) + 1
    assert counts == EXPECTED_ISLAND_COUNTS
    assert len(counts) == 9
    assert sum(counts.values()) == 35


def test_rounded_table_reproduces_reported_direct_ols_slope():
    result = analyze(mapped_rows(), bootstrap_repetitions=2000, seed=20260811)
    direct = result["reconstructed_models"]["direct_log_island_on_log_mainland_ols"]
    ratio = result["reconstructed_models"][
        "log_island_mainland_ratio_on_log_mainland_ols"
    ]
    assert abs(direct["slope"] - 0.58) < 0.01
    assert abs(ratio["slope"] - (-0.39)) < 0.03
    assert direct["slope"] < 1.0


def test_island_cluster_resampling_preserves_ols_but_not_sma_isometry_exclusion():
    result = analyze(mapped_rows(), bootstrap_repetitions=5000, seed=20260811)
    cluster = result["island_cluster_bootstrap"]
    assert cluster["n_clusters"] == 9
    assert cluster["ols_slope_percentiles"]["p97_5"] < 1.0
    assert cluster["sma_slope_percentiles"]["p2_5"] < 1.0
    assert cluster["sma_slope_percentiles"]["p97_5"] > 1.0
    leave_one = result["leave_one_island"]
    assert leave_one["all_leave_one_island_ols_below_isometry"] is True
    assert leave_one["all_leave_one_island_sma_below_isometry"] is True


def test_symmetric_axis_sensitivity_keeps_formal_admission_closed():
    result = analyze(mapped_rows(), bootstrap_repetitions=5000, seed=20260811)
    sensitivity = result["measurement_error_sensitivity"]
    assert sensitivity["sma_point_slope"] < 1.0
    assert sensitivity["pair_sma_bootstrap_interval"][0] < 1.0
    assert sensitivity["pair_sma_bootstrap_interval"][1] > 1.0
    assert sensitivity["pair_sma_bootstrap_interval_excludes_isometry"] is False
    assert sensitivity["island_cluster_sma_bootstrap_interval"][0] < 1.0
    assert sensitivity["island_cluster_sma_bootstrap_interval"][1] > 1.0
    assert sensitivity["island_cluster_sma_bootstrap_interval_excludes_isometry"] is False
    assert result["effect_registry_eligible"] is False


def test_checked_summary_is_deterministically_regenerable():
    expected = json.loads(SUMMARY.read_text(encoding="utf-8"))
    observed = analyze(mapped_rows(), bootstrap_repetitions=20000, seed=20260811)
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    observed["source_id"] = source["source_id"]
    observed["source_retrieval_state"] = source["retrieval_state"]
    # Python/libm versions can differ at the final floating-point bit.  The
    # scientific result and all categorical gates must remain exact, while
    # numeric values are compared at a tolerance far below reported precision.
    assert_json_close(observed, expected, atol=1e-12)


def test_source_provenance_keeps_formal_admission_closed():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert source["source_reported_pair_count"] == 35
    assert source["reconstructed_numeric_pair_count"] == 35
    assert source["institutional_record_recovered"] is True
    assert source["institutional_identifier"] == "10.26686/wgtn.17136800"
    assert source["island_group_mapping"]["frequency_vector_matches_table_a14"] is True
    assert source["raw_pdf_checksum_locked"] is False
    assert source["stable_institutional_download_recovered"] is False
    assert summary["island_group_structure"]["matches_appendix_a14"] is True
    assert summary["formal_cross_system_fit_ready"] is False
    assert summary["effect_registry_eligible"] is False
