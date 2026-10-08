"""Engineering only: source-equivalence and conservation for opt-in payoff.

All live visitor histories used here are OLD published test histories; none of
the prospectively frozen 37110801-37110864 new cohort is ever sampled.
"""
from dataclasses import fields
import numpy as np
import pytest

from scripts.model3_island.reproduction import reproduce
from scripts.chapter2_order_expression_payoff import (
    reproduce_with_order_expression,
)
from scripts.model3_island.types import Ledger
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config, founders, load_design,
)
from scripts.run_model3_persistent_isolation import exposure


@pytest.mark.parametrize("setting", [
    "delayed_control", "prior_selfing", "pollen_discount", "assurance_cost",
])
@pytest.mark.parametrize("environment", ["near", "far"])
@pytest.mark.parametrize("mode", ["fixed", "evolving"])
def test_zero_expression_is_exactly_canonical_across_frozen_biology(
    setting, environment, mode
):
    design = load_design(DEFAULT_DESIGN)
    state = founders(design)
    visitor = exposure(26110601, environment).visitors[0]
    cfg = config(design, setting, 0.01, mode)
    reference = reproduce(state, visitor, cfg)
    candidate = reproduce_with_order_expression(state, visitor, cfg)
    assert isinstance(candidate, Ledger)
    for field in fields(Ledger):
        np.testing.assert_array_equal(
            getattr(candidate, field.name),
            getattr(reference, field.name),
        )


@pytest.mark.parametrize("setting", [
    "delayed_control", "prior_selfing", "pollen_discount", "assurance_cost",
])
def test_positive_order_expression_preserves_genomes_and_reproductive_ledger(setting):
    design = load_design(DEFAULT_DESIGN)
    state = founders(design)
    visitor = exposure(26110601, "near").visitors[0]
    cfg = config(design, setting, 0.01, "evolving")
    original = (
        state.alleles.tobytes(), state.allele_origin.tobytes(),
        state.mutation_flags.tobytes(), state.ids.tobytes(),
    )
    result = reproduce_with_order_expression(
        state, visitor, cfg, assurance_shift=0.45, investment_shift=-0.45,
    )
    normal = reproduce(state, visitor, cfg)
    assert len(result.ovules) == len(state.ids)
    np.testing.assert_allclose(result.outcross.sum(axis=0) + result.self_viable,
                               result.maternal, atol=1e-10)
    np.testing.assert_allclose(result.outcross.sum(axis=1) + result.self_viable,
                               result.paternal, atol=1e-10)
    np.testing.assert_allclose(result.delivered.sum(axis=1) + result.lost,
                               result.exported, atol=1e-10)
    assert np.all(np.diag(result.outcross) == 0)
    assert np.all(np.diag(result.delivered) == 0)
    assert not np.array_equal(result.maternal, normal.maternal)
    assert original == (
        state.alleles.tobytes(), state.allele_origin.tobytes(),
        state.mutation_flags.tobytes(), state.ids.tobytes(),
    )


def test_nonzero_a_shift_disallowed_in_fixed_assurance_arm():
    design = load_design(DEFAULT_DESIGN)
    state = founders(design)
    visitor = exposure(26110601, "near").visitors[0]
    cfg = config(design, "prior_selfing", 0.01, "fixed")
    with pytest.raises(ValueError, match="requires evolving A"):
        reproduce_with_order_expression(state, visitor, cfg, assurance_shift=0.45)


def test_empty_visitor_zero_pollen_and_safe_selfing():
    design = load_design(DEFAULT_DESIGN)
    state = founders(design)
    history = exposure(26110601, "near")
    v = history.visitors[0]
    from scripts.model3_island.types import VisitorState
    none = VisitorState(
        ids=np.empty(0, dtype=int), optima=np.empty(0),
        breadths=np.empty(0), effectiveness=np.empty(0),
    )
    cfg = config(design, "prior_selfing", 0.01, "evolving")
    result = reproduce_with_order_expression(
        state, none, cfg, assurance_shift=0.45, investment_shift=-0.45
    )
    assert np.all(result.outcross == 0)
    assert np.all(result.exported == 0)
    assert np.all(result.maternal == result.self_viable)
