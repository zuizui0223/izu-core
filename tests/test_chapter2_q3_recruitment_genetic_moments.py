"""No-history exact Q3 inheritance/recruitment accounting regression tests."""
from dataclasses import replace
import json
import math
from pathlib import Path

import numpy as np
import pytest
from scipy.stats import poisson

from scripts.audit_chapter2_q3_recruitment_genetic_moments import (
    CAPACITIES, B, BUDGET, STATUS, plants, visitors, config,
    offspring_count_probabilities, one_generation_moments, run_all
)
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.expectation import capped_poisson_mean
from scripts.model3_island.population import inherit


def test_original_parentage_and_poisson_count_law_are_preserved():
    p = plants(np.full((8, 2), .35))
    for k in CAPACITIES:
        row = one_generation_moments(p, k)
        mu = row["original_source_viable_seed_mean"]
        assert mu == pytest.approx(8.994424151193341, abs=1e-7)
        probs = offspring_count_probabilities(mu, k)
        assert probs.shape == (k+1,)
        assert probs.sum() == pytest.approx(1)
        assert probs[0] == pytest.approx(math.exp(-mu))
        assert probs[-1] == pytest.approx(poisson.sf(k-1, mu))
        assert row["E_next_census"] == pytest.approx(capped_poisson_mean(mu, k))
        assert row["P_next_occupied"] == pytest.approx(1-math.exp(-mu))
        assert row["independent_genetic_histories"] == 0
        assert row["original_parent_selfing_share_by_expected_viable_seeds"] > 0
        assert row["original_parent_selfing_share_by_expected_viable_seeds"] < 1


def test_equal_visible_phenotypes_can_have_different_heritable_variance():
    homo = plants(np.full((8, 2), .35))
    hidden = plants(np.tile(np.array([.2, .5]), (8, 1)))
    for k in CAPACITIES:
        a = one_generation_moments(homo, k)
        b = one_generation_moments(hidden, k)
        assert a["original_source_viable_seed_mean"] == pytest.approx(
            b["original_source_viable_seed_mean"], abs=1e-12
        )
        assert a["E_next_census"] == pytest.approx(b["E_next_census"], abs=1e-12)
        assert a["P_next_occupied"] == pytest.approx(b["P_next_occupied"], abs=1e-12)
        ai = a["results_by_trait"]["investment"]
        bi = b["results_by_trait"]["investment"]
        assert ai["single_child_variance"] == pytest.approx(0,abs=1e-14)
        assert bi["parent_pair_lottery_single_child_variance"] == pytest.approx(0,abs=1e-14)
        assert bi["mendelian_single_child_variance"] == pytest.approx(.01125,abs=1e-13)
        assert bi["expected_child_mean_shift_conditional_on_occupancy"] == pytest.approx(0,abs=1e-14)
        assert bi["mean_trait_variance_conditional_on_occupancy"] == pytest.approx(
            .01125 * b["E_inverse_recruits_given_occupied"], abs=1e-12
        )
        assert bi["mean_trait_variance_conditional_on_occupancy"] > ai["mean_trait_variance_conditional_on_occupancy"]


def test_carrying_capacity_modulates_genetic_realization_variance_not_expected_mean():
    hidden = plants(np.tile(np.array([.2, .5]), (8, 1)))
    a = one_generation_moments(hidden, 8)
    b = one_generation_moments(hidden, 48)
    assert a["P_next_occupied"] == pytest.approx(b["P_next_occupied"],abs=1e-13)
    assert a["E_next_census"] < b["E_next_census"]
    assert a["E_inverse_recruits_given_occupied"] > b["E_inverse_recruits_given_occupied"]
    assert a["E_inverse_recruits_given_occupied"] == pytest.approx(.145689595636,abs=1e-7)
    assert b["E_inverse_recruits_given_occupied"] == pytest.approx(.1278507039,abs=1e-7)
    assert a["results_by_trait"]["investment"]["expected_child_mean_conditional_on_occupancy"] == pytest.approx(
        b["results_by_trait"]["investment"]["expected_child_mean_conditional_on_occupancy"]
    )
    assert a["results_by_trait"]["investment"]["mean_trait_variance_conditional_on_occupancy"] > (
        b["results_by_trait"]["investment"]["mean_trait_variance_conditional_on_occupancy"]
    )


def test_parental_lottery_and_mendelian_components_are_independently_nonzero():
    mu = np.array([.20,.25,.30,.35,.40,.45,.50,.55])
    state = plants(np.column_stack([mu-.02,mu+.02]))
    q = one_generation_moments(state,8)
    vals = q["results_by_trait"]["investment"]
    assert vals["parent_pair_lottery_single_child_variance"] > 0
    assert vals["mendelian_single_child_variance"] > 0
    assert vals["expected_child_mean_shift_conditional_on_occupancy"] < 0
    assert abs(vals["expected_child_mean_shift_conditional_on_occupancy"]) < (
        vals["mean_trait_sd_conditional_on_occupancy"]
    )
    assert vals["single_child_variance"] == pytest.approx(
        vals["parent_pair_lottery_single_child_variance"]
        +vals["mendelian_single_child_variance"],abs=1e-15
    )
    assert vals["unconditional_next_allele_copy_trait_sum"] == pytest.approx(
        2*q["E_next_census"]*vals["expected_child_mean_conditional_on_occupancy"]
    )


def test_parentage_matrix_orientation_matches_original_inherit():
    p=plants(np.column_stack([
        np.array([.20,.25,.30,.35,.40,.45,.50,.55])-.02,
        np.array([.20,.25,.30,.35,.40,.45,.50,.55])+.02
    ]))
    cfg=config(8)
    l=reproduce_kb(p,visitors(),cfg,background_denominator_capacity=B)
    mother=np.array([0,1,2,3],dtype=np.int64)
    father=np.array([4,5,6,7],dtype=np.int64)
    c=inherit(
        p,mother,father,cfg,
        segregation_rng=np.random.default_rng(7),
        mutation_rng=np.random.default_rng(8),
        year=1
    )
    for i in range(4):
        assert c.alleles[i,1,0] in p.alleles[mother[i],1,:]
        assert c.alleles[i,1,1] in p.alleles[father[i],1,:]
    assert l.outcross.shape == (8,8)
    assert np.all(np.diag(l.outcross)==0)


def test_reject_invalid_inputs_and_no_outcome_promotions():
    with pytest.raises(ValueError):
        plants(np.full((9,2),.35))
    with pytest.raises(ValueError):
        plants(np.full((8,2),1.2))
    with pytest.raises(ValueError):
        offspring_count_probabilities(float("nan"),8)
    with pytest.raises(ValueError):
        offspring_count_probabilities(1,-1)
    with pytest.raises(ValueError):
        one_generation_moments(plants(np.full((8,2),.35)),7)
    x=run_all()
    assert x["status"] == STATUS
    assert x["n_new_visitor_histories"] == 0
    assert x["n_new_evolutionary_trajectories"] == 0
    assert x["n_new_stochastic_demographic_paths"] == 0
    assert x["experimental_status"] == "POST_DISCOVERY_DETERMINISTIC_SOURCE_FIXTURE_ONLY"
    assert x["assumptions"]["trait_mean_if_extinct"] == "MISSING"
    assert len(x["results"]) == 3
    assert all(len(r["by_capacity"]) == 2 for r in x["results"])
    json.dumps(x,allow_nan=False)


def test_six_source_moments_match_independently_recomputed_archived_receipt():
    path = (Path(__file__).resolve().parents[1] /
            "data/results/chapter2_q3_exact_recruitment_genetic_moments_20261010.json")
    receipt = json.loads(path.read_text(encoding="utf-8"))
    assert receipt["status"] == "POSTDISCOVERY_DETERMINISTIC_SOURCE_MATHEMATICS_NO_NEW_BIOLOGICAL_HISTORY"
    assert receipt["n_independent_histories"] == 0
    assert receipt["n_stochastic_paths"] == 0
    outcome = run_all()
    computed = {(x["fixture"], y["K"]): y
                for x in outcome["results"] for y in x["by_capacity"]}
    assert len(computed) == len(receipt["outcomes"]) == 6
    for original in receipt["outcomes"]:
        actual = computed[(original["fixture"], original["K"])]
        trait = actual["results_by_trait"]["investment"]
        for key, got in [
            ("mu",actual["original_source_viable_seed_mean"]),
            ("p_next_occupied",actual["P_next_occupied"]),
            ("expected_next_N",actual["E_next_census"]),
            ("parent_mean",trait["founder_mean"]),
            ("expected_child_mean",trait["expected_child_mean_conditional_on_occupancy"]),
            ("expected_shift",trait["expected_child_mean_shift_conditional_on_occupancy"]),
            ("conditional_next_trait_sd",trait["mean_trait_sd_conditional_on_occupancy"]),
            ("parent_lottery_variance",trait["parent_pair_lottery_single_child_variance"]),
            ("mendelian_variance",trait["mendelian_single_child_variance"]),
        ]:
            assert got == pytest.approx(original[key], abs=1e-7,rel=0), (
                original["fixture"], original["K"], key
            )
