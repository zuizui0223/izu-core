import json
import random
from pathlib import Path

import pytest

from channel_id.dependency_fdq_design_simulation import (
    Scenario,
    _select_coverage_rows,
    load_design_config,
    run_design_simulation,
    simulate_replicate,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data" / "design" / "dependency_fdq_design_scenarios.json"
RESULT = ROOT / "data" / "results" / "dependency_fdq_design_simulation.json"


def test_config_explicitly_marks_all_dependency_support_as_synthetic():
    data = load_design_config(CONFIG)
    assert data["synthetic_dependency_values"] is True
    assert data["empirical_structure_anchor"]["community_sites"] == 8
    assert data["empirical_structure_anchor"]["community_seasons"] == 5
    assert data["empirical_structure_anchor"]["proxy_moderation_eligible_taxa"] == 9
    assert data["empirical_structure_anchor"]["proxy_moderation_rows"] == 105
    assert data["empirical_structure_anchor"]["resolved_high_dependency_bombus_endpoints"] == 0
    assert "does not provide true dependency values" in data["empirical_structure_anchor"]["anchor_boundary"]


def test_sparse_coverage_retains_every_taxon_and_site_season_cluster():
    scenario = Scenario(
        scenario_id="coverage-test",
        dependency_values=(0.1, 0.3, 0.5, 0.7),
        sites=4,
        seasons=3,
        dependency_reliability=0.8,
        coverage_fraction=0.5,
        description="test",
    )
    rows = _select_coverage_rows(scenario, random.Random(11))
    assert len(rows) == scenario.target_rows
    assert {taxon for taxon, _, _ in rows} == set(range(scenario.taxa))
    assert {(site, season) for _, site, season in rows} == {
        (site, season)
        for site in range(scenario.sites)
        for season in range(scenario.seasons)
    }


def test_one_replicate_is_finite_and_uses_clustered_interaction_fit():
    scenario = Scenario(
        scenario_id="fit-test",
        dependency_values=(0.05, 0.35, 0.65, 0.95),
        sites=4,
        seasons=3,
        dependency_reliability=0.85,
        coverage_fraction=0.75,
        description="test",
    )
    settings = {
        "fdq_main_effect": 0.8,
        "cluster_shock_sd": 0.35,
        "observation_error_sd": 0.8,
        "fdq_site_sd": 0.8,
        "fdq_season_sd": 0.45,
        "fdq_residual_sd": 0.65,
        "taxon_intercept_sd": 0.55,
        "site_intercept_sd": 0.45,
        "season_intercept_sd": 0.25,
    }
    result = simulate_replicate(scenario, 0.4, random.Random(20260810), settings)
    assert result.interaction_se > 0
    assert abs(result.interaction_t) < 100


def test_checked_result_prioritizes_dependency_span_over_more_rows_alone():
    report = json.loads(RESULT.read_text(encoding="utf-8"))
    results = {row["scenario_id"]: row for row in report["scenario_results"]}

    def detect(scenario_id: str, effect: float = 0.4) -> float:
        rows = results[scenario_id]["effect_results"]
        row = next(
            item
            for item in rows
            if item["declared_synthetic_interaction"] == effect
        )
        return row["calibrated_detection_probability"]

    assert detect("direct_add_high_endpoint") > detect("direct_narrow_9")
    assert detect("direct_full_span_10") > detect("survivor_proxy_more_seasons")
    assert detect("direct_full_span_16") > detect("direct_narrow_16")
    assert all(
        row["claim_boundary"] == report["claim_boundary"]
        or "synthetic" in row["claim_boundary"].lower()
        for row in report["scenario_results"]
    )


def test_invalid_config_cannot_hide_empirical_status(tmp_path: Path):
    data = load_design_config(CONFIG)
    data["synthetic_dependency_values"] = False
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="synthetic_dependency_values"):
        load_design_config(path)


def test_small_run_is_deterministic():
    data = load_design_config(CONFIG)
    data["simulation"]["null_calibration_replicates"] = 12
    data["simulation"]["null_validation_replicates"] = 12
    data["simulation"]["effect_replicates"] = 16
    data["scenarios"] = data["scenarios"][:1]
    data["design_contrasts"] = []
    first = run_design_simulation(data)
    second = run_design_simulation(data)
    assert first == second
