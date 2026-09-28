from pathlib import Path

import pytest

from channel_id.island_multichannel import EvidenceChannel
from channel_id.island_source_level import (
    _beta_binomial_logpmf,
    compare_source_level_scenarios,
    load_source_level_evidence,
)


ROOT = Path(__file__).parents[1]


def load_evidence():
    return load_source_level_evidence(
        island_summary_path=ROOT / "data" / "inoue_literature_island_traits.csv",
        outcrossing_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1990_outcrossing.csv",
        bagging_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1988_bagging.csv",
        flower_path=ROOT / "data" / "two_breakpoint_evidence" / "inoue1995_flower_length.csv",
    )


def test_source_level_loader_retains_population_and_experiment_rows() -> None:
    evidence = load_evidence()

    assert len(evidence.outcrossing) == 17
    assert len(evidence.bagging) == 7
    assert len(evidence.flower) == 6
    assert sum(row.island_id == "Honshu" for row in evidence.outcrossing) == 7
    assert {row.population_id for row in evidence.outcrossing if row.island_id == "Oshima"} == {
        "oshima_1",
        "oshima_2",
    }


def test_bagging_beta_binomial_prefers_matching_probability() -> None:
    observed = _beta_binomial_logpmf(8, 9, 0.85, 8.0)
    mismatched = _beta_binomial_logpmf(8, 9, 0.15, 8.0)

    assert observed > mismatched


def test_source_level_comparison_is_deterministic_and_uses_requested_channels() -> None:
    evidence = load_evidence()
    channels = (EvidenceChannel.OUTCROSSING, EvidenceChannel.BAGGING, EvidenceChannel.FLOWER)
    first = compare_source_level_scenarios(evidence, draws=150, seed=17, included_channels=channels)
    second = compare_source_level_scenarios(evidence, draws=150, seed=17, included_channels=channels)

    assert first == second
    assert all(row.included_channels == channels for row in first)
    assert all(row.n_outcrossing_rows == 17 for row in first)
    assert all(row.n_bagging_rows == 7 for row in first)
    assert all(row.n_flower_rows == 6 for row in first)


def test_invalid_bagging_counts_fail() -> None:
    with pytest.raises(ValueError, match="invalid beta-binomial count"):
        _beta_binomial_logpmf(5, 4, 0.5, 8.0)
