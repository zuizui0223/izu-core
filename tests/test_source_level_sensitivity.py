from pathlib import Path

import pytest

from channel_id.island_source_level import load_source_level_evidence
from channel_id.source_level_sensitivity import (
    SensitivitySetting,
    importance_effective_sample_size,
    rank_summary,
    run_source_level_sensitivity,
)


ROOT = Path(__file__).parents[1]


def evidence():
    return load_source_level_evidence(
        island_summary_path=ROOT / "data" / "inoue_literature_island_traits.csv",
        outcrossing_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1990_outcrossing.csv",
        bagging_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1988_bagging.csv",
        flower_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1995_flower_length.csv",
    )


def test_importance_effective_sample_size_matches_simple_cases() -> None:
    assert importance_effective_sample_size((0.5, 0.5)) == pytest.approx(2.0)
    assert importance_effective_sample_size((1.0, 0.0, 0.0)) == pytest.approx(1.0)
    with pytest.raises(ValueError, match="positive"):
        importance_effective_sample_size((0.0, 0.0))


def test_sensitivity_is_deterministic_and_ranks_each_cell() -> None:
    settings = (SensitivitySetting("central", 0.70, 8.0, 3.5),)
    first = run_source_level_sensitivity(evidence(), settings=settings, seeds=(19,), draws=100)
    second = run_source_level_sensitivity(evidence(), settings=settings, seeds=(19,), draws=100)

    assert first == second
    assert sorted(row.rank for row in first) == [1, 2, 3, 4]
    assert all(0.0 < row.importance_effective_sample_size <= 100.0 for row in first)
    assert all(0.0 < row.importance_ess_fraction <= 1.0 for row in first)


def test_rank_summary_has_all_scenarios() -> None:
    settings = (SensitivitySetting("central", 0.70, 8.0, 3.5),)
    summary = rank_summary(run_source_level_sensitivity(evidence(), settings=settings, seeds=(23,), draws=80))

    assert len(summary) == 4
    assert sum(row["rank_one_count"] for row in summary) == 1
