"""Pure synthetic tests for frozen algebra; never run new biological histories."""
import numpy as np
import pytest

from scripts.plan_chapter2_order_expression_identification import load_protocol
from scripts.chapter2_orthogonal_capacity_readout import (
    EXPECTED_SHAPE, history_order_effects, summarize_history_effects,
    validate_readout_contract,
)


def test_readout_preflight_is_plan_only():
    info = validate_readout_contract()
    assert info["status"] == "READOUT_ALGEBRA_PREFLIGHT_ONLY"
    assert info["expected_shape"] == list(EXPECTED_SHAPE)
    assert info["science_executed"] is False


def test_complete_binary_grid_preserves_visitor_history_pairing():
    design = load_protocol()
    grid = np.zeros(EXPECTED_SHAPE, dtype=np.uint8)
    # 3 valid arms, only some histories show order effect at the self-half gate.
    # Binary inputs, not simulated biological trajectories.
    grid[:32, :, :, 0, :, :, :, 0, 0] = 1
    grid[:32, :, :, 0, :, :, :, 0, 1] = 1
    grid[:32, :, :, 0, :, :, :, 1, 0] = 1
    grid[:32, :, :, 0, :, :, :, 2, 0] = 1
    got = history_order_effects(grid, design=design)
    assert got.shape == (64, 3, 2)
    assert got[0, 0, 0] == pytest.approx(1)
    assert got[0, 0, 1] == pytest.approx(1)
    assert got[0, 1, 0] == pytest.approx(1)
    assert got[0, 1, 1] == pytest.approx(0)
    assert np.array_equal(got[32:], np.zeros((32, 3, 2)))


def test_primary_capacity_moderation_uses_paired_cluster_contrasts():
    value = np.zeros((64, 3, 2), dtype=float)
    value[:, 0, 0] = 0.02
    value[:, 0, 1] = 0.01
    value[:, 1, 0] = 0.02
    value[:, 1, 1] = 0.018
    value[:, 2, 0] = 0.02
    value[:, 2, 1] = 0.015
    out = summarize_history_effects(value)
    primary = out["contrasts"]["primary_capacity_conditional_fixed_eight"]
    secondary = out["contrasts"]["secondary_founder_abundance_and_sampling"]
    assert primary["mean"] == pytest.approx(0.008)
    assert primary["history_bootstrap95"] == pytest.approx([0.008, 0.008])
    assert secondary["mean"] == pytest.approx(-0.003)
    assert out["primary_decision_if_and_only_if_complete_raw_archive_admitted"] == (
        "supported_conditional_capacity_moderation"
    )
    assert out["status"] == "ALGEBRA_ONLY_NOT_AN_ADMITTED_SCIENTIFIC_RESULT"


def test_null_primary_contrast_falls_into_rope():
    value = np.zeros((64, 3, 2))
    result = summarize_history_effects(value)
    assert result["primary_decision_if_and_only_if_complete_raw_archive_admitted"] == (
        "practically_equivalent_within_0p005"
    )


@pytest.mark.parametrize("shape", [(64, 3, 2), (172032, 2), (1, 3, 2)])
def test_future_cell_pseudoreplication_fails_closed(shape):
    with pytest.raises(ValueError):
        summarize_history_effects(np.ones(shape))


def test_missing_future_cell_or_nonbinary_occupancy_fails_closed():
    design = load_protocol()
    z = np.zeros(EXPECTED_SHAPE, dtype=float)
    z[0, 0, 0, 0, 0, 0, 0, 0, 0] = np.nan
    with pytest.raises(ValueError):
        history_order_effects(z, design=design)
    z[0, 0, 0, 0, 0, 0, 0, 0, 0] = 0.5
    with pytest.raises(ValueError, match="binary"):
        history_order_effects(z, design=design)


def test_bootstrap_seed_and_draws_cannot_be_modified():
    v = np.zeros((64, 3, 2))
    with pytest.raises(ValueError, match="Frozen"):
        summarize_history_effects(v, draws=100)
    with pytest.raises(ValueError, match="Frozen"):
        summarize_history_effects(v, seed=123)
