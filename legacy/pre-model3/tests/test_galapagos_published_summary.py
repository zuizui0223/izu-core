import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "analyze_galapagos_published_summary.py"
SPEC = importlib.util.spec_from_file_location("galapagos_published", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_exact_sign_flip_pvalue_is_two_sided_and_deterministic():
    assert MODULE.exact_sign_flip_pvalue([1.0, 1.0]) == pytest.approx(0.5)
    assert MODULE.exact_sign_flip_pvalue([0.0, 0.0]) is None


def test_pearson_and_interval_guards():
    assert MODULE.pearson([1, 2, 3], [2, 4, 6]) == pytest.approx(1.0)
    assert MODULE.pearson([1, 1, 1], [2, 3, 4]) is None
    assert MODULE.interval_coverage(0.10, 0.12, 0.03)
    assert not MODULE.interval_coverage(0.10, 0.15, 0.03)


def test_checked_table_reproduces_article_level_69_percent_association():
    rows = MODULE.load_table(
        ROOT / "data/source_tables/galapagos_nnakenyi_2019_tables_1_2.csv"
    )
    summary, diagnostics = MODULE.analyse(rows)
    model = summary["model_comparison"]

    assert summary["n_islands"] == 10
    assert len(diagnostics) == 10
    assert model["observed_vs_ais_r_squared"] == pytest.approx(
        0.6861986091364222
    )
    assert model["published_69_percent_reproduced"] is True
    assert model["observed_vs_null_r_squared"] == pytest.approx(
        0.6246667031025713
    )
    assert model["ais_mean_absolute_error"] == pytest.approx(0.0268)
    assert model["null_mean_absolute_error"] == pytest.approx(0.0367)
    assert model["n_islands_where_ais_has_lower_absolute_error"] == 4
    assert model["n_ais_intervals_covering_observed"] == 6
    assert model["n_null_intervals_covering_observed"] == 6
    assert model[
        "exact_paired_sign_flip_pvalue_for_mean_absolute_error_improvement"
    ] == pytest.approx(0.572265625)


def test_published_summary_never_opens_raw_network_or_cross_system_claims():
    rows = MODULE.load_table(
        ROOT / "data/source_tables/galapagos_nnakenyi_2019_tables_1_2.csv"
    )
    summary, _ = MODULE.analyse(rows)
    assert summary["raw_dryad_network_source_recovered"] is False
    assert summary["effect_registry_eligible"] is False
    assert summary["cross_system_model_eligible"] is False
    assert "No raw plant-pollinator edges" in summary["claim_boundary"]


def test_descriptive_covariate_rows_have_leave_one_island_ranges():
    rows = MODULE.load_table(
        ROOT / "data/source_tables/galapagos_nnakenyi_2019_tables_1_2.csv"
    )
    summary, _ = MODULE.analyse(rows)
    records = {
        row["predictor"]: row
        for row in summary["observed_nestedness_covariate_correlations"]
    }
    assert records["weighted_connectance"]["pearson_r"] == pytest.approx(
        -0.7365939909353626
    )
    assert records["age_ma"]["leave_one_island_r_min"] < 0
    assert records["age_ma"]["leave_one_island_r_max"] > 0
    assert all(
        record["status"] == "descriptive_fixed_published_table_values"
        for record in records.values()
    )
