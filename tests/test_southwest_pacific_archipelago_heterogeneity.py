import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "swp_archipelago_heterogeneity",
    ROOT / "scripts" / "analyze_southwest_pacific_archipelago_heterogeneity.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def row(pair, island, mainland, fm, fi, syndrome=1, family="Fam"):
    import math

    return {
        "Pair number": pair,
        "Island": island,
        "Mainland": mainland,
        "Family": family,
        "FM": fm,
        "FI": fi,
        "LR": math.log10(fi / fm),
        "Syndrome": syndrome,
    }


def test_only_source_coded_valid_animal_rows_enter_groups():
    rows = [
        row(1, "A", "NZ", 1, 1.2, syndrome=1),
        row(2, "A", "NZ", 2, 1.8, syndrome=0),
        row(3, "B", "AU", 3, 2.0, syndrome=1),
        {**row(4, "B", "AU", 4, 3.0, syndrome=1), "LR": None},
    ]
    groups = MODULE.island_groups(rows)
    assert set(groups) == {"A", "B"}
    assert [item["Pair number"] for item in groups["A"]] == [1]
    assert [item["Pair number"] for item in groups["B"]] == [3]


def test_predeclared_minimum_blocks_small_island_slope():
    rows = [
        row(index, "A", "NZ", float(index), float(index) * 0.9)
        for index in range(1, MODULE.MIN_SLOPE_PAIRS)
    ]
    record = MODULE.island_record(
        "A", rows, bootstrap_repetitions=200
    )
    assert record["n_animal_valid"] == MODULE.MIN_SLOPE_PAIRS - 1
    assert record["starting_value_slope_status"] == (
        "blocked_n_below_predeclared_minimum"
    )
    assert record["ols_slope"] is None
    assert record["cross_system_model_eligible"] == "no"
    assert record["causal_claim_allowed"] == "no"


def test_estimable_island_reports_slope_and_keeps_it_descriptive():
    # Larger mainland flowers shrink proportionally more on the island.
    rows = [
        row(index, "A", "NZ", fm, fi)
        for index, (fm, fi) in enumerate(
            [(1, 1.1), (2, 2.0), (4, 3.5), (8, 6.0), (16, 10.0)],
            start=1,
        )
    ]
    record = MODULE.island_record(
        "A", rows, bootstrap_repetitions=200
    )
    assert record["starting_value_slope_status"] == (
        "estimated_descriptive_within_archipelago"
    )
    assert record["ols_slope"] < 0
    assert record["event_bootstrap_ci_low"] is not None
    assert record["row_role"] == "within_archipelago_descriptive_sensitivity"


def test_summary_counts_direction_without_claiming_independent_effects():
    records = [
        {
            "starting_value_slope_status": "estimated_descriptive_within_archipelago",
            "ols_slope": -0.2,
            "mean_lr": -0.1,
        },
        {
            "starting_value_slope_status": "estimated_descriptive_within_archipelago",
            "ols_slope": 0.1,
            "mean_lr": 0.2,
        },
        {
            "starting_value_slope_status": "blocked_n_below_predeclared_minimum",
            "ols_slope": None,
            "mean_lr": 0.05,
        },
    ]
    summary = MODULE.summarize(records)
    assert summary["n_archipelagos_with_valid_animal_pairs"] == 3
    assert summary["n_archipelagos_with_estimable_slope"] == 2
    assert summary["n_estimated_negative_slopes"] == 1
    assert summary["n_estimated_positive_slopes"] == 1
    assert summary["estimated_slope_range"] == pytest.approx([-0.2, 0.1])
    assert "not effective-dependency measures" in summary["claim_boundary"].casefold()
    assert "not entered" in summary["claim_boundary"].casefold()
