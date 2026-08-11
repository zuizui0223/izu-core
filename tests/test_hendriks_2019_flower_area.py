import json
from pathlib import Path

from scripts.analyze_hendriks_2019_flower_area import analyze, read_pairs


ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "data/source_tables/hendriks_2019_flower_area_table_b9_reconstructed.csv"
SOURCE = ROOT / "data/source_tables/hendriks_2019_flower_area_table_b9_source.json"
SUMMARY = ROOT / "data/results/hendriks_2019/flower_area_reconstruction_summary.json"


def test_reconstruction_has_all_35_positive_pairs():
    rows = read_pairs(TABLE)
    assert len(rows) == 35
    assert [row["pair_id"] for row in rows] == list(range(1, 36))
    assert all(row["island_flower_area_cm2"] > 0 for row in rows)
    assert all(row["mainland_flower_area_cm2"] > 0 for row in rows)


def test_rounded_table_reproduces_reported_direct_ols_slope():
    result = analyze(read_pairs(TABLE), bootstrap_repetitions=2000, seed=20260811)
    direct = result["reconstructed_models"]["direct_log_island_on_log_mainland_ols"]
    ratio = result["reconstructed_models"][
        "log_island_mainland_ratio_on_log_mainland_ols"
    ]
    assert abs(direct["slope"] - 0.58) < 0.01
    assert abs(ratio["slope"] - (-0.39)) < 0.03
    assert direct["slope"] < 1.0


def test_symmetric_axis_sensitivity_weakens_isometry_claim():
    result = analyze(read_pairs(TABLE), bootstrap_repetitions=5000, seed=20260811)
    sensitivity = result["measurement_error_sensitivity"]
    assert sensitivity["sma_point_slope"] < 1.0
    assert sensitivity["sma_bootstrap_interval"][0] < 1.0
    assert sensitivity["sma_bootstrap_interval"][1] > 1.0
    assert sensitivity["sma_bootstrap_interval_excludes_isometry"] is False
    assert result["effect_registry_eligible"] is False


def test_checked_summary_is_deterministically_regenerable():
    expected = json.loads(SUMMARY.read_text(encoding="utf-8"))
    observed = analyze(read_pairs(TABLE), bootstrap_repetitions=20000, seed=20260811)
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    observed["source_id"] = source["source_id"]
    observed["source_retrieval_state"] = source["retrieval_state"]
    assert observed == expected


def test_source_provenance_keeps_formal_admission_closed():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert source["source_reported_pair_count"] == 35
    assert source["reconstructed_numeric_pair_count"] == 35
    assert source["raw_pdf_checksum_locked"] is False
    assert source["stable_institutional_download_recovered"] is False
    assert summary["formal_cross_system_fit_ready"] is False
    assert summary["effect_registry_eligible"] is False
