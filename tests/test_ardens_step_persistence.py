from dataclasses import replace
from pathlib import Path
import random

import pytest

from channel_id.ardens_step_persistence_smc import run_six_candidate_comparison, summarize_six_candidate_comparison
from channel_id.island_multichannel import EvidenceChannel
from channel_id.island_source_level import load_source_level_evidence
from channel_id.source_level_ardens_step_persistence import (
    ARDENS_STEP_PERSISTENCE_SCENARIO,
    ArdensStepState,
    compare_ardens_step_persistence,
    draw_ardens_step_persistence_parameters,
    load_ardens_step_states,
    predict_ardens_step_persistence,
)
from channel_id.source_level_tempered_smc import TemperedSMCConfig

ROOT = Path(__file__).parents[1]
SUMMARY = ROOT / "data" / "inoue_literature_island_traits.csv"
STAGES = ROOT / "data" / "ardens_step_persistence_stages.csv"


def evidence():
    return load_source_level_evidence(
        island_summary_path=SUMMARY,
        outcrossing_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1990_outcrossing.csv",
        bagging_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1988_bagging.csv",
        flower_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1995_flower_length.csv",
    )


def test_declared_stage_scaffold_marks_bridge_and_post_bridge_without_using_outcomes() -> None:
    states = load_ardens_step_states(STAGES, evidence().islands)

    assert states["Honshu"] == ArdensStepState(0, 0)
    assert states["Oshima"] == ArdensStepState(1, 0)
    assert states["Toshima"] == ArdensStepState(1, 1)
    assert states["Hachijo"] == ArdensStepState(1, 1)


def test_strict_persistence_keeps_flower_equal_across_same_stage_when_environment_equal() -> None:
    rows = evidence().islands
    oshima = next(row for row in rows if row.island_id == "Oshima")
    hachijo = next(row for row in rows if row.island_id == "Hachijo")
    draw = draw_ardens_step_persistence_parameters(3, random.Random(41))
    zero_environment = (0.0, 0.0, 0.0)

    bridge = predict_ardens_step_persistence(oshima, draw, zero_environment, ArdensStepState(1, 0))
    downstream = predict_ardens_step_persistence(hachijo, draw, zero_environment, ArdensStepState(1, 1))
    altered_pollinators = replace(hachijo, bombus_diversus=1.0, bombus_ardens=1.0, halictid_pollinator=0.0, megachilid_pollinator=0.0)
    same_downstream = predict_ardens_step_persistence(altered_pollinators, draw, zero_environment, ArdensStepState(1, 1))

    assert bridge.expected_flower_length_mm == downstream.expected_flower_length_mm
    assert downstream.assurance > bridge.assurance
    assert downstream.expected_outcrossing < bridge.expected_outcrossing
    assert same_downstream == downstream


def test_step_source_level_comparison_is_reproducible_and_keeps_source_rows() -> None:
    rows = evidence()
    channels = (EvidenceChannel.OUTCROSSING, EvidenceChannel.BAGGING, EvidenceChannel.FLOWER)
    first = compare_ardens_step_persistence(rows, stage_scaffold_path=STAGES, draws=180, seed=31, included_channels=channels)
    second = compare_ardens_step_persistence(rows, stage_scaffold_path=STAGES, draws=180, seed=31, included_channels=channels)

    assert first == second
    assert first.scenario == ARDENS_STEP_PERSISTENCE_SCENARIO
    assert first.included_channels == channels
    assert first.n_outcrossing_rows == 17
    assert first.n_bagging_rows == 7
    assert first.n_flower_rows == 6


def test_six_candidate_smc_includes_step_candidate_with_stable_small_screen() -> None:
    rows = evidence()
    config = TemperedSMCConfig(particles=30, target_ess_fraction=0.70, rejuvenation_steps=1)
    results = run_six_candidate_comparison(
        rows,
        island_summary_path=SUMMARY,
        stage_scaffold_path=STAGES,
        config=config,
        seeds=(57,),
        included_channels=(EvidenceChannel.OUTCROSSING, EvidenceChannel.BAGGING, EvidenceChannel.FLOWER),
    )
    summary = summarize_six_candidate_comparison(results)

    assert len(results) == 6
    assert {row.scenario for row in results} >= {ARDENS_STEP_PERSISTENCE_SCENARIO, "isolation_order", "ardens_bridge_loss"}
    assert any(row["scenario"] == ARDENS_STEP_PERSISTENCE_SCENARIO for row in summary)
    assert all(row.min_incremental_ess >= 0.70 * config.particles - 1e-4 for row in results)


def test_invalid_step_scaffold_is_rejected(tmp_path: Path) -> None:
    broken = tmp_path / "broken_stages.csv"
    broken.write_text(
        "island_id,bridge_flower_stage,post_bridge_reproductive_stage\nHonshu,0,0\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="step scaffold missing"):
        load_ardens_step_states(broken, evidence().islands)
