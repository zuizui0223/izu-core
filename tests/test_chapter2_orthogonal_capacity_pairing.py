"""Synthetic-only source-ID matching and common-seed regression checks."""
from __future__ import annotations

import numpy as np
import pytest

from scripts.model3_island.types import PlantState
from scripts.chapter2_orthogonal_capacity_pairing import (
    common_future_seed, common_future_streams, prepare_arms,
    select_fixed_eight, state_fingerprint,
)


def fake_state(n: int) -> PlantState:
    return PlantState(
        alleles=np.linspace(0.1, 0.9, n * 6).reshape(n, 3, 2)
        if n else np.empty((0, 3, 2), dtype=float),
        allele_origin=np.arange(n * 6, dtype=np.int64).reshape(n, 3, 2),
        mutation_flags=np.zeros((n, 3, 2), dtype=bool),
        ids=np.arange(100, 100 + n, dtype=np.int64),
        birth_years=np.zeros(n, dtype=np.int64),
    )


def test_identical_eight_diploid_genotypes_under_two_capacities():
    full = fake_state(12)
    selected = select_fixed_eight(
        full, visitor_history=39110901,
        demographic_repeat=39111901, setting_index=0,
    )
    assert len(selected.ids) == 8
    arms = prepare_arms(full, selected)
    a = arms["eight_founders_capacity8"]
    b = arms["eight_founders_capacity48"]
    c = arms["all_available_founders_capacity48"]
    assert (a.capacity, b.capacity, c.capacity) == (8, 48, 48)
    assert a.state is b.state
    assert state_fingerprint(a.state) == state_fingerprint(b.state)
    assert len(c.state.ids) == 12


@pytest.mark.parametrize("n", [0, 3, 8])
def test_missing_or_extinct_source_is_never_selected_away(n):
    full = fake_state(n)
    selected = select_fixed_eight(
        full, visitor_history=39110901,
        demographic_repeat=39111901, setting_index=0,
    )
    arms = prepare_arms(full, selected)
    assert len(arms["eight_founders_capacity8"].state.ids) == n
    assert len(arms["eight_founders_capacity48"].state.ids) == n
    assert len(arms["all_available_founders_capacity48"].state.ids) == n


def test_reject_mismatched_diploid_alleles_even_with_matching_ids():
    full = fake_state(8)
    bad_alleles = full.alleles.copy()
    bad_alleles[0, 0, 0] += 0.01
    bad = PlantState(
        alleles=bad_alleles, allele_origin=full.allele_origin,
        mutation_flags=full.mutation_flags, ids=full.ids,
        birth_years=full.birth_years,
    )
    with pytest.raises(AssertionError, match="genotype"):
        prepare_arms(full, bad)


def test_regime_and_gate_cannot_enter_shared_initial_stream_seeds():
    kwargs = dict(
        visitor_history=39110901, demographic_repeat=39111901,
        setting="delayed_control", future_visitor="near", budget=3.0,
    )
    a = common_future_streams(**kwargs)
    b = common_future_streams(**kwargs)
    assert np.array_equal(a["survival"].random(10), b["survival"].random(10))
    assert common_future_seed(**kwargs) != common_future_seed(
        **{**kwargs, "future_visitor": "far"}
    )
    assert common_future_seed(**kwargs) != common_future_seed(
        **{**kwargs, "visitor_history": 39110902}
    )
    with pytest.raises(TypeError):
        common_future_seed(**kwargs, regime="eight_founders_capacity8")
    with pytest.raises(TypeError):
        common_future_seed(**kwargs, gate="self_half")


def test_no_old_exposed_cohort_could_enter_new_streams():
    with pytest.raises(ValueError, match="prospective independent"):
        common_future_seed(
            visitor_history=38110901, demographic_repeat=39111901,
            setting="delayed_control", future_visitor="near", budget=3.0,
        )
