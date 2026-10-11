"""Exact, no-new-history Model 3 clonal census Markov baseline."""
import json

import numpy as np
import pytest
from scipy.stats import poisson

from scripts.audit_chapter2_exact_clonal_demographic_null import (
    STATUS, HORIZONS, CAPACITIES, BUDGETS, clone_state,
    source_viable_mu, fixed_config, run_all, static_visitors, transition,
)
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.population import inherit


def test_original_source_ledger_reproduces_known_N8_fixedB48_reference():
    mu8 = source_viable_mu(8, 8, 6.0)
    assert mu8 == pytest.approx(8.994424151193341, abs=1e-10)
    assert mu8 == pytest.approx(source_viable_mu(8, 48, 6.0), abs=1e-11)
    s = clone_state(8)
    v = static_visitors()
    cfg = fixed_config(8, 6.0)
    ledger = reproduce_kb(s, v, cfg, background_denominator_capacity=48)
    assert cfg.survival == 0
    assert cfg.mutation_rate == 0
    assert cfg.seed_arrival.supply == 0
    assert ledger.self_viable.sum() + ledger.outcross.sum() == pytest.approx(mu8)
    assert np.all(s.alleles[:, :, :] == s.alleles[0])


def test_original_diploid_reproduction_is_genetically_closed_under_clones():
    source = clone_state(8)
    cfg = fixed_config(8, 6.0)
    child = inherit(
        source, np.array([0, 1, 2, 3], dtype=np.int64),
        np.array([4, 5, 6, 7], dtype=np.int64), cfg,
        segregation_rng=np.random.default_rng(2),
        mutation_rng=np.random.default_rng(3),
        year=1,
    )
    np.testing.assert_allclose(child.alleles, source.alleles[:4], atol=0, rtol=0)
    assert np.array_equal(child.mutation_flags, np.zeros((4, 3, 2), dtype=bool))


def test_transition_probabilities_and_K_capped_poisson_tail():
    for K in CAPACITIES:
        matrix, mu = transition(K, 6.0)
        assert matrix.shape == (K + 1, K + 1)
        assert len(mu) == K
        assert matrix[0, 0] == 1
        assert matrix[0, 1:].sum() == 0
        assert np.allclose(matrix.sum(axis=1), 1.0, atol=1e-12, rtol=0)
        assert matrix[8, 0] == pytest.approx(poisson.pmf(0, mu[8]))
        assert matrix[8, K] == pytest.approx(poisson.sf(K - 1, mu[8]))
        assert np.all(matrix >= 0)


def test_exact_80_update_results_are_model_demographic_only():
    result = run_all()
    assert result["status"] == STATUS
    assert result["n_evaluated_conditions"] == 6
    assert result["new_stochastic_histories"] == 0
    assert result["new_genetic_trajectories"] == 0
    assert result["is_confirmatory_evolution_test"] is False
    assert result["horizons"] == list(HORIZONS)
    lookup = {(x["K"], x["budget"]): x for x in result["results"]}
    assert set(lookup) == {(k,b) for k in CAPACITIES for b in BUDGETS}
    expected = {
        (8, 4.5): 3.939919057671659e-9,
        (8, 6.0): 0.030242646454152422,
        (8, 8.0): 0.9027478995381906,
        (48, 4.5): 0.015275228625207138,
        (48, 6.0): 0.828719233465605,
        (48, 8.0): 0.9981845515652196,
    }
    for key, reference in expected.items():
        v = lookup[key]["moments"]
        assert v["0"]["p_occupied"] == 1
        assert v["80"]["p_occupied"] == pytest.approx(reference, abs=2e-8, rel=0)
        assert v["20"]["p_occupied"] >= v["80"]["p_occupied"]
        assert 0 <= v["80"]["p_at_N6_to_N9_unconditional"] <= v["80"]["p_occupied"]
        assert v["80"]["expected_census_unconditional"] >= v["80"]["p_occupied"]
    # No genotype or visitor turnover: a demographic non-selection baseline.
    assert lookup[(8, 6.0)]["moments"]["80"]["p_occupied"] < 0.05
    assert lookup[(48, 6.0)]["moments"]["80"]["p_occupied"] > 0.8
    # Historical #452's monomorphic SOURCE conflict window is N=6..9.
    # Its persistence under a no-evolution density Markov process differs
    # dramatically between K8 and K48; these are NOT selection trajectories.
    k8 = lookup[(8, 6.0)]["moments"]["80"]
    k48 = lookup[(48, 6.0)]["moments"]["80"]
    assert k8["p_at_N6_to_N9_unconditional"] == pytest.approx(
        0.017158342418196575, abs=1e-9
    )
    assert k48["p_at_N6_to_N9_unconditional"] == pytest.approx(
        1.9291598825843511e-7, abs=1e-10
    )
    assert 0.5 < k8["p_at_N6_to_N9_unconditional"] / k8["p_occupied"] < 0.65
    assert k48["p_at_N6_to_N9_unconditional"] / k48["p_occupied"] < 1e-6
    assert "NOT a genetic" in result["interpretation"]
    json.dumps(result, allow_nan=False)


def test_reject_unregistered_census_and_resource_grid():
    with pytest.raises(ValueError):
        clone_state(0)
    with pytest.raises(ValueError):
        source_viable_mu(9, 8, 6.0)
    with pytest.raises(ValueError):
        fixed_config(7, 6.0)
    with pytest.raises(ValueError):
        fixed_config(8, 6.1)
