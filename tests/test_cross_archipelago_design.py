import json
import random
from pathlib import Path

import pytest

from channel_id.cross_archipelago_design import (
    ReplicationScenario,
    run_replication_simulation,
    scenario_index,
    simulate_replicate,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data" / "design" / "cross_archipelago_replication_scenarios.json"


def test_equal_island_counts_make_naive_and_system_point_estimates_equal():
    scenario = ReplicationScenario(
        scenario_id="balanced",
        n_archipelagos=4,
        islands_per_archipelago=3,
        description="test",
    )
    result = simulate_replicate(
        scenario,
        population_mean=0.2,
        between_archipelago_sd=0.5,
        within_archipelago_sd=0.4,
        rng=random.Random(11),
    )
    assert result.naive_estimate == pytest.approx(result.system_estimate)
    assert result.naive_se > 0
    assert result.system_se > 0


def test_invalid_single_archipelago_design_is_rejected():
    scenario = ReplicationScenario(
        scenario_id="invalid",
        n_archipelagos=1,
        islands_per_archipelago=24,
        description="test",
    )
    with pytest.raises(ValueError, match="at least two"):
        simulate_replicate(
            scenario,
            population_mean=0,
            between_archipelago_sd=0.2,
            within_archipelago_sd=0.4,
            rng=random.Random(1),
        )


def test_small_report_is_deterministic_and_keeps_total_budget_fixed():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    config["simulation"]["replicates"] = 100
    config["simulation"]["population_means"] = [0.0]
    config["simulation"]["between_archipelago_sds"] = [0.2]
    first = run_replication_simulation(config)
    second = run_replication_simulation(config)
    assert first == second
    assert {row["total_island_units"] for row in first["scenario_results"]} == {24}
    assert first["analysis_status"] == "synthetic_cross_archipelago_operating_characteristics"


def test_between_system_heterogeneity_exposes_naive_pseudoreplication():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    config["simulation"]["replicates"] = 2500
    config["simulation"]["population_means"] = [0.0, 0.3]
    config["simulation"]["between_archipelago_sds"] = [0.5]
    report = run_replication_simulation(config)
    index = scenario_index(report)

    deep_null = index[("two_archipelagos_deep", 0.0, 0.5)]
    broad_null = index[("twelve_archipelagos", 0.0, 0.5)]
    deep_effect = index[("two_archipelagos_deep", 0.3, 0.5)]
    broad_effect = index[("twelve_archipelagos", 0.3, 0.5)]

    naive_deep_false_positive = (
        deep_null["naive_island_level"]["positive_detection_probability"]
        + deep_null["naive_island_level"]["negative_detection_probability"]
    )
    system_deep_false_positive = (
        deep_null["system_level"]["positive_detection_probability"]
        + deep_null["system_level"]["negative_detection_probability"]
    )
    assert naive_deep_false_positive > system_deep_false_positive
    assert deep_null["reported_se_ratio_naive_to_system"] < 1

    assert (
        broad_effect["system_level"]["positive_detection_probability"]
        > deep_effect["system_level"]["positive_detection_probability"]
    )
    assert (
        broad_null["system_level"]["coverage_of_population_mean"]
        > deep_null["naive_island_level"]["coverage_of_population_mean"]
    )


def test_claim_boundary_marks_all_effects_synthetic():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    config["simulation"]["replicates"] = 10
    report = run_replication_simulation(config)
    boundary = report["claim_boundary"].casefold()
    assert "synthetic" in boundary
    assert "does not estimate empirical" in boundary
    assert "causality" in boundary
