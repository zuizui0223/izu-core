"""Invariant checks for source-aware secondary-colonisation exploratory pilot.

A small crossed-source smoke test, NOT a new confirmatory experiment.
"""
import json

import numpy as np
import pytest

from scripts.secondary_colonization_pilot_20261020 import (
    ANCESTRY_LIMIT, CHECKPOINTS, DESTINATIONS, DISTANCES, STATUS,
    ancestry_summary, configuration, destination_future, make_founders,
    reference_residents, run_experiment, source_allele_mask, visitors_for,
)
from scripts.model3_island.population import subset


def test_baseline_and_operator_freeze():
    for policy in ("fixed", "evolving"):
        cfg = configuration(policy)
        assert cfg.capacity == 48 and cfg.ovule_budget == 8
        assert cfg.mutation_rate == 0
        assert cfg.seed_arrival.supply == 0
        assert cfg.visitor_arrival.supply == 0
        assert cfg.assurance_cost == .5
        assert cfg.fixed_assurance == .5
    resident = reference_residents()
    assert len(resident.ids) == 40
    assert not source_allele_mask(resident).any()
    founders = make_founders(202610201, 0)
    assert source_allele_mask(founders).all()
    assert founders.allele_origin.max() < ANCESTRY_LIMIT


def test_empty_cohort_occupied_destination_is_not_colonisation():
    founders = make_founders(202610201, 0)
    empty = subset(founders, slice(0, 0))
    full, sparse = visitors_for(202610211)
    result = destination_future(
        empty, full, sparse, "mainland_like_resident", 0.,
        arrival_seed=5551, future_seed=5552, founder_mean_I=.5,
    )
    assert result["settled_seeds"] == 0
    assert result["source_lineage_present_at_horizon"] is False
    assert result["first_source_allele_absence"] == 0
    assert result["initial"]["population"] == 40
    assert result["final"]["source_carriers"] == 0
    assert result["entry_common_context_return"] is None
    # The resident community exists independently of colonist arrival.
    assert result["final"]["population"] > 0


def test_arrival_kernel_boundaries_and_unknown_distance():
    founders = make_founders(202610201, 0)
    cohort = subset(founders, slice(0, 8))
    full, sparse = visitors_for(202610211)
    near = destination_future(
        cohort, full, sparse, "mainland_like_vacant", 0.,
        arrival_seed=801, future_seed=811, founder_mean_I=.5,
    )
    far = destination_future(
        cohort, full, sparse, "mainland_like_vacant", 1.5,
        arrival_seed=801, future_seed=811, founder_mean_I=.5,
    )
    assert near["arrival_probability_per_seed"] == .8
    assert far["arrival_probability_per_seed"] == pytest.approx(.8 * np.exp(-1.5))
    assert far["settled_seeds"] <= near["settled_seeds"]
    with pytest.raises(ValueError, match="distance"):
        destination_future(
            cohort, full, sparse, "mainland_like_vacant", 3.,
            801, 811, .5,
        )


def test_bounded_source_cross_and_allele_no_reappearance():
    result = run_experiment(
        founder_seeds=(202610201,), visitor_seeds=(202610211,),
        repeats=1,
    )
    assert result["status"] == STATUS
    assert len(result["sources"]) == 1 + 2 * len(CHECKPOINTS)
    assert len(result["summary"]) == len(result["sources"]) * len(DESTINATIONS) * len(DISTANCES)
    assert result["future_paths"] == len(result["paths"]) == 30
    assert result["sources"][0]["historical_A_policy"] == "ancestral"
    assert result["sources"][0]["donor_alive"]
    assert any(row["source_lineage_present_at_horizon"] for row in result["paths"])
    assert result["source_sha256"]
    for row in result["paths"]:
        censuses = row["censuses"]
        assert len(censuses) == 21
        assert all(0 <= c["source_carriers"] <= c["population"] <= 48 for c in censuses)
        assert row["initial"] == censuses[0] and row["final"] == censuses[-1]
        assert row["settled_seeds"] <= row["source_seed_production"]["cohort_size"] <= 8
        if row["destination"] == "mainland_like_resident":
            assert row["initial"]["population"] == 40 + row["settled_seeds"]
        else:
            assert row["initial"]["population"] == row["settled_seeds"]
        zero_seen = False
        last_max = None
        for census in censuses:
            if zero_seen:
                assert census["source_allele_copies"] == 0
            if census["source_allele_copies"] == 0:
                zero_seen = True
            maximum = census["source_I_max"]
            if maximum is not None:
                if last_max is not None:
                    assert maximum <= last_max + 1e-12
                last_max = maximum
        if not row["settled_seeds"]:
            assert row["source_lineage_present_at_horizon"] is False
        if row["first_source_allele_absence"] is None:
            assert row["final"]["source_allele_copies"] > 0
    assert len(json.dumps(result, sort_keys=True)) > 1000


def test_source_pilot_repeatability_reuses_same_locked_streams():
    # Same independently seeded design must produce bitwise-identical readouts
    # across reruns; the rerun is technical verification, not another N.
    kwargs = dict(
        founder_seeds=(202610201,), visitor_seeds=(202610211,), repeats=1
    )
    a = run_experiment(**kwargs)
    b = run_experiment(**kwargs)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
