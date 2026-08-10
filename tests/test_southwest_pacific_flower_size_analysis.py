import json
from pathlib import Path

import pytest

from scripts.analyze_southwest_pacific_flower_size import (
    bootstrap_slope,
    ordinary_least_squares,
    standard_major_axis,
)


ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = ROOT / "data/results/southwest_pacific_pairs"
SUMMARY_PATH = RESULT_DIR / "analysis_summary.json"


def load_summary():
    return json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))


def synthetic_rows():
    return [
        {"FM": 1.0, "LR": 0.30, "Island": "A", "Family": "F1"},
        {"FM": 2.0, "LR": 0.15, "Island": "A", "Family": "F1"},
        {"FM": 4.0, "LR": -0.05, "Island": "B", "Family": "F2"},
        {"FM": 8.0, "LR": -0.25, "Island": "B", "Family": "F2"},
        {"FM": 16.0, "LR": -0.40, "Island": "C", "Family": "F3"},
    ]


def test_ols_and_sma_are_distinct_estimators():
    rows = synthetic_rows()
    x = [0.0, 0.30103, 0.60206, 0.90309, 1.20412]
    y = [float(row["LR"]) for row in rows]
    ordinary = ordinary_least_squares(x, y)
    major_axis = standard_major_axis(x, y)
    assert ordinary["slope"] < 0
    assert major_axis["slope"] < 0
    assert abs(major_axis["slope"]) > abs(ordinary["slope"])


def test_bootstrap_is_deterministic_and_cluster_aware():
    rows = synthetic_rows()
    first = bootstrap_slope(
        rows,
        cluster="Island",
        repetitions=300,
        seed_label="fixed test",
    )
    second = bootstrap_slope(
        rows,
        cluster="Island",
        repetitions=300,
        seed_label="fixed test",
    )
    assert first == second
    assert first["repetitions_valid"] == 300
    assert first["ci_95"][1] < 0


def test_checked_source_analysis_preserves_counts_and_claim_boundaries():
    analysis = load_summary()
    source_lock = json.loads(
        (RESULT_DIR / "source_lock.json").read_text(encoding="utf-8")
    )
    assert analysis["status"] == "source_native_129_pair_analysis_complete"
    assert analysis["n_source_rows"] == 129
    assert source_lock["n_source_rows"] == 129
    assert source_lock["files"][
        "mcaf005_suppl_supplementary_data_s2.xlsx"
    ]["sha256"] == "452c6f83143eb17e8249faae9659386be7b162f93742c4e137921952a9b88677"

    integrity = analysis["source_integrity"]
    assert integrity["syndrome_counts"] == {
        "animal": 89,
        "wind": 39,
        "unresolved": 1,
    }
    assert integrity["valid_size_counts_by_syndrome"] == {
        "animal": 88,
        "wind": 38,
        "unresolved": 1,
    }
    assert integrity["invalid_or_missing_size_pair_numbers"] == [69, 77]
    assert integrity["unresolved_syndrome_pair_numbers"] == [54]
    assert integrity["formula_lr_log10_fi_over_fm_mismatch_pair_numbers"] == []
    assert integrity["source_count_discrepancy_retained"] is True
    assert analysis["effect_registry_eligible"] is False
    assert "does not identify pollinator dependency" in analysis["claim_boundary"]


def test_animal_starting_size_dependence_is_robust_but_wind_is_not():
    analysis = load_summary()
    animal = analysis["primary_models"]["animal_source_coded"]
    wind = analysis["primary_models"]["wind_source_coded"]

    assert animal["n"] == 88
    assert animal["ols_slope"] == pytest.approx(-0.15099471189271235)
    assert animal["island_ci_95"][1] < 0
    assert animal["family_ci_95"][1] < 0
    assert animal["leave_one_island_all_negative"] is True
    assert animal["coupling_slope"] == pytest.approx(0.8490052881072877)
    assert animal["coupling_island_ci_95"][1] < 1

    assert wind["n"] == 38
    assert wind["ols_slope"] == pytest.approx(-0.07611432484743032)
    assert wind["island_ci_95"][0] < 0
    assert wind["island_ci_95"][1] > 0
    assert wind["mean_fsLR"]["ci_95"][0] < 0 < wind["mean_fsLR"]["ci_95"][1]


def test_morphology_and_display_support_channel_heterogeneity():
    analysis = load_summary()
    fused = analysis["key_sensitivities"]["actinomorphic_fused_petals"]
    free = analysis["key_sensitivities"]["actinomorphic_free_petals"]
    zygomorphic = analysis["key_sensitivities"]["zygomorphic"]
    display = analysis["animal_floral_display"]

    assert fused["n"] == 30
    assert fused["ols_slope"] < 0
    assert fused["island_ci_95"][1] < 0
    assert free["n"] == 56
    assert free["ols_slope"] < 0
    assert free["island_ci_95"][1] < 0
    assert zygomorphic == {"status": "blocked_n_too_small", "n": 2}

    assert display["n"] == 79
    assert display["mean_LFR"]["ci_95"][0] < 0
    assert display["mean_LFR"]["ci_95"][1] > 0


def test_regression_method_audit_is_explicit_not_silent():
    analysis = load_summary()
    audit = analysis["regression_method_audit"]
    assert audit["reported_animal_slope_absolute_difference_from_ols"] < 0.002
    assert audit["reported_animal_slope_absolute_difference_from_sma"] > 0.3
    assert "not a correction of author intent" in audit["reading"]


def test_effect_rows_are_future_same_family_candidates_not_current_pooling():
    document = json.loads(
        (RESULT_DIR / "effect_rows.json").read_text(encoding="utf-8")
    )
    assert document["formal_cross_system_fit_ready"] is False
    assert len(document["effects"]) == 3
    assert all(effect["causal_claim_allowed"] is False for effect in document["effects"])
    assert all(
        effect["cross_system_model_eligible"] is True
        for effect in document["effects"]
    )
    assert len({effect["system_cluster"] for effect in document["effects"]}) == 1
