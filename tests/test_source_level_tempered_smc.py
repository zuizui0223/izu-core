from pathlib import Path

import pytest

from channel_id.island_multichannel import EvidenceChannel
from channel_id.island_source_level import load_source_level_evidence
from channel_id.source_level_tempered_smc import (
    TemperedSMCConfig,
    choose_next_beta,
    effective_sample_size,
    run_tempered_smc_comparison,
    summarize_tempered_smc,
)

ROOT = Path(__file__).parents[1]
SUMMARY = ROOT / "data" / "inoue_literature_island_traits.csv"


def evidence():
    return load_source_level_evidence(
        island_summary_path=SUMMARY,
        outcrossing_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1990_outcrossing.csv",
        bagging_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1988_bagging.csv",
        flower_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1995_flower_length.csv",
    )


def test_choose_next_beta_controls_incremental_ess() -> None:
    values = (-10.0, -7.0, -2.0, 0.0, 4.0, 9.0)
    beta = choose_next_beta(values, 0.0, target_ess_fraction=0.70, bisection_steps=40)
    weights = [pow(2.718281828459045, beta * value) for value in values]

    assert 0.0 < beta <= 1.0
    assert effective_sample_size(weights) >= 0.70 * len(values) - 1e-3


def test_tempered_smc_is_deterministic_and_includes_all_five_candidates() -> None:
    config = TemperedSMCConfig(particles=50, target_ess_fraction=0.65, rejuvenation_steps=1, max_tempering_steps=80)
    channels = (EvidenceChannel.OUTCROSSING, EvidenceChannel.BAGGING, EvidenceChannel.FLOWER)
    first = run_tempered_smc_comparison(
        evidence(), island_summary_path=SUMMARY, config=config, seeds=(91,), included_channels=channels
    )
    second = run_tempered_smc_comparison(
        evidence(), island_summary_path=SUMMARY, config=config, seeds=(91,), included_channels=channels
    )

    assert first == second
    assert {row.scenario for row in first} == {
        "environment_only", "body_size_only", "small_bee_substitution",
        "ardens_bridge_loss", "isolation_order",
    }
    assert all(row.beta_schedule[0] == pytest.approx(0.0) for row in first)
    assert all(row.beta_schedule[-1] == pytest.approx(1.0) for row in first)
    assert all(row.min_incremental_ess >= 0.65 * config.particles - 1e-3 for row in first)
    assert all(row.included_channels == channels for row in first)


def test_tempered_summary_has_rank_diagnostics() -> None:
    config = TemperedSMCConfig(particles=40, target_ess_fraction=0.60, rejuvenation_steps=0, max_tempering_steps=80)
    results = run_tempered_smc_comparison(
        evidence(), island_summary_path=SUMMARY, config=config, seeds=(51, 52)
    )
    summary = summarize_tempered_smc(results)

    assert len(summary) == 5
    assert all(row["replicates"] == 2 for row in summary)
    assert sum(row["rank_one_count"] for row in summary) == 2
    assert all(row["minimum_incremental_ess"] >= 0.60 * config.particles - 1e-3 for row in summary)
