"""Synthetic only: historic K-at-B48 pathway reduction and frozen-status controls."""
from pathlib import Path
import numpy as np
import pytest

from scripts.chapter2_k_fixedB48_posthoc_pathways import (
    EXPECTED_SHAPE, history_order_channel, _nonnegative, SEED, METRICS
)
from scripts.chapter2_k_fixedB48_prehistory import prospective_biological_design


def test_registered_independent_source_unit_and_history_weighting():
    d=prospective_biological_design()
    grid=np.zeros(EXPECTED_SHAPE,dtype=float)
    grid[:32,:,:,0,:,:,:,0,0]=1.0
    x=history_order_channel(grid,d)
    assert x.shape==(64,2,2)
    np.testing.assert_allclose(x[:32,0,0],np.ones(32),atol=1e-12)
    np.testing.assert_allclose(x[:32,0,1],np.zeros(32),atol=1e-12)
    np.testing.assert_allclose(x[32:],np.zeros((32,2,2)),atol=1e-12)


def test_history_cells_cannot_be_mistaken_for_independent_future_replicates():
    d=prospective_biological_design()
    with pytest.raises(AssertionError,match="complete"):
        history_order_channel(np.zeros((114688,2)),d)


def test_valid_channels_and_bootstrap_are_explicitly_exploratory():
    assert SEED==2026100973
    assert "restricted_persistence_updates" in METRICS
    assert "cumulative_self_recruits" in METRICS
    source=Path("scripts/chapter2_k_fixedB48_posthoc_pathways.py").read_text()
    assert "POST_OUTCOME_EXPLORATORY_SOURCE_ADMITTED_CHANNEL_AUDIT" in source
    assert "Cumulative recruits depend on survival duration" in source
    assert "ORIGINAL_VERDICT = \"supported_controlled_demographic_K_moderation_at_fixed_B48\"" in source


@pytest.mark.parametrize("bad",[-1,float("nan"),float("inf"),True,None,"0"])
def test_invalid_biological_channel_fails_closed(bad):
    with pytest.raises(AssertionError):
        _nonnegative(bad,"synthetic test")
