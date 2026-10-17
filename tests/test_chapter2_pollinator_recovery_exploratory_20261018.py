"""Boundaries for the deliberately small, non-confirmatory visitor-return Model3 pilot."""
from dataclasses import replace

import numpy as np
import pytest

from scripts.explore_chapter2_pollinator_recovery_20261018 import (
    CHECKPOINTS, EXTIRPATION, FUTURE_REPLICATES, configuration,
    empty_plants, execute_micro_pilot, investment_mean, make_founders,
    make_visitors, seeded, support_bound,
)


def test_micro_pilot_is_not_mislabeled_as_no_selfing():
    fixed = configuration("fixed")
    evolving = configuration("evolving")
    assert fixed.assurance_mode == "fixed"
    assert fixed.fixed_assurance == .5
    assert fixed.depression == evolving.depression == .5
    assert fixed.mutation_rate == evolving.mutation_rate == 0
    assert fixed.seed_arrival.supply == 0
    assert EXTIRPATION == 35
    assert CHECKPOINTS == (10, 30, 45)


def test_upper_support_is_sufficient_not_equivalent_to_recovery():
    x = make_founders(181001)
    a = x.alleles.copy()
    a[:, 1, :] = .375
    unreachable = replace(x, alleles=a)
    assert support_bound(unreachable, .5) is True
    a[:, 1, :] = .625
    reachable_in_principle = replace(x, alleles=a)
    assert support_bound(reachable_in_principle, .5) is False
    assert support_bound(empty_plants(7), .5) is None


def test_crossed_seed_namespace_and_visitor_treatments():
    assert seeded(1, 0, 0) == seeded(1, 0, 0)
    assert seeded(1, 0, 0) != seeded(1, 0, 1)
    assert seeded(2, 0, 0, 10, 0, 0) != seeded(2, 0, 0, 10, 1, 0)
    full, sparse = make_visitors(182001)
    assert len(full.ids) == 6 and len(sparse.ids) == 1
    assert np.array_equal(sparse.optima, full.optima[:1])


def test_exploratory_one_crossed_cell_executes_and_replays_exactly():
    args = dict(founder_ids=(181001,), visitor_ids=(182001,),
                checkpoints=(10,), future_replicates=1)
    a = execute_micro_pilot(**args)
    b = execute_micro_pilot(**args)
    assert a == b
    assert a["status"] == "EXPLORATORY_PILOT_ONLY_NO_CONFIRMATORY_CLAIM"
    assert a["independent_crossed_blocks"] == 1
    assert a["future_trajectories"] == 6
    assert len(a["by_arm"]) == 6
    assert all(x["conditional_stream_paths"] == 1 for x in a["by_arm"])
    assert all(x["target_founder_mean_I"] == investment_mean(make_founders(181001))
               for x in a["paths"])
    assert all(x["historical_occupied"] or not x["high_I_sustained_and_occupied_final"]
               for x in a["paths"])
    assert any(x["future_assurance_policy"] == "freeze_at_attained_A" for x in a["paths"])
    assert set(x["historical_assurance_policy"] for x in a["paths"]) == {"fixed", "evolving"}
    assert all(x["regained_if_declined"] is None or x["declined_by_0p05_at_checkpoint"]
               for x in a["paths"])
    assert all(x["relative_focal_gradient_after_restoration"] is None or
               np.isfinite(x["relative_focal_gradient_after_restoration"])
               for x in a["paths"])


def test_future_simulation_budgets_must_not_expand():
    with pytest.raises(ValueError, match="only predeclared"):
        execute_micro_pilot(founder_ids=(181001,), visitor_ids=(182001,),
                            checkpoints=(10,), future_replicates=FUTURE_REPLICATES + 1)
    with pytest.raises(ValueError, match="only prespecified"):
        execute_micro_pilot(founder_ids=(181001,), visitor_ids=(182001,),
                            checkpoints=(12,), future_replicates=1)
