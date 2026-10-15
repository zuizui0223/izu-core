"""Post-outcome original-archive visitor-state partitioning guards."""
import numpy as np
import pytest

from scripts.audit_chapter2_far_early_visitor_states_20261015 import (
    BOOTSTRAPS, SETTINGS, TERMS, expected_shards, partition_pair,
    interval, correlation,
)


def fixture_case(positive=False):
    n = 200
    visitors = np.r_[np.zeros(100, dtype=int), np.ones(100, dtype=int)]
    effects = np.zeros(n)
    if positive:
        effects[49] = .03
        effects[149] = .02
    means = np.r_[.5, .5 + np.cumsum(effects)]
    return {
        "n_visitors": visitors,
        "mean_I": means,
        "mean_A_expressed": np.full(n + 1, .5),
        "realized_delta_I": effects,
        "weighted_parental_Price_I": effects,
        "recruit_transmission_residual_I": np.zeros(n),
        "survivor_sampling_I": np.zeros(n),
    }


def test_original_shards_have_immutable_archive_hashes():
    shards = expected_shards()
    assert len(shards) == 4
    assert len(set(shards)) == 4
    assert all(len(d) == 64 for d in shards)


def test_visitor_partition_preserves_source_i_change_and_weights():
    f, e = fixture_case(), fixture_case(positive=True)
    got = partition_pair(e, f)
    assert got["zero_visitor_years"] == 100
    assert got["present_visitor_years"] == 100
    assert got["terminal_I_EminusF"] == pytest.approx(.05)
    assert got["absent_realized_delta_I"] == pytest.approx(.03)
    assert got["present_realized_delta_I"] == pytest.approx(.02)
    assert got["absent_weighted_parental_Price_I"] == pytest.approx(.03)
    assert got["present_recruit_transmission_residual_I"] == 0
    assert got["annual_absent_minus_present_EF"] == pytest.approx(.0001)


def test_reject_unpaired_exposure_or_undocumented_response():
    f,e=fixture_case(),fixture_case(positive=True)
    e["n_visitors"][5] = 1
    with pytest.raises(AssertionError):
        partition_pair(e,f)
    e=fixture_case(positive=True)
    e["realized_delta_I"][9] += .1
    with pytest.raises(AssertionError):
        partition_pair(e,f)


def test_history_cluster_units_not_plants_or_years():
    assert BOOTSTRAPS == 4096
    assert len(SETTINGS) == 4
    assert len(TERMS) == 4
    result = interval(np.full(64, .125), seed=7)
    assert result["n_histories"] == 64
    assert result["mean"] == pytest.approx(.125)
    assert result["history_bootstrap95_descriptive"] == pytest.approx([.125, .125])
    with pytest.raises(AssertionError):
        interval(np.full(65, .125), seed=7)


def test_rank_correlation_reproducibility():
    x=np.arange(64, dtype=float)
    y=np.arange(64, dtype=float)[::-1]
    result=correlation(x,y,seed=12)
    assert result["n_histories"] == 64
    assert result["rho"] == pytest.approx(-1)
    assert result["history_bootstrap95_descriptive"] == pytest.approx([-1,-1])
