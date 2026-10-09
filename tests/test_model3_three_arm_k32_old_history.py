"""Pinned K32 old-history three-arm Model 3 comparison tests."""
import numpy as np
import pytest

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.run_model3_three_arm_k32_old_history import (
    compare,
    canonical_conditional_kernel,
    deterministic_expected_step,
    deterministic_integerize,
)


def test_expectation_integerization_preserves_counts_and_impossible_support():
    out = deterministic_integerize(np.array([0., .18, .17, .65]), 32)
    assert out.dtype.kind in "iu"
    assert out.tolist()[0] == 0
    assert int(out.sum()) == 32
    np.testing.assert_array_equal(
        out, deterministic_integerize(np.array([0., .18, .17, .65]), 32)
    )
    assert deterministic_integerize(np.array([1., 0.]), 0).sum() == 0
    with pytest.raises(ValueError):
        deterministic_integerize(np.array([-.1, 1.1]), 32)


def test_det_expected_step_uses_source_ledger_and_exact_inheritance():
    initial, grid, visitors, cfg = fixed_support_problem(
        capacity=32, ovule_budget=8.
    )
    # This unit test uses the pre-existing engineered visitors. Main
    # executable comparison uses ONLY archived visitor history 26110601.
    intensity, q = canonical_conditional_kernel(
        initial, grid, visitors, cfg, 0
    )
    assert intensity > 0
    assert len(q) == 27
    assert q.sum() == pytest.approx(1., abs=1e-12)
    a, risk_a = deterministic_expected_step(
        initial, grid, visitors, cfg, 0
    )
    b, risk_b = deterministic_expected_step(
        initial, grid, visitors, cfg, 0
    )
    np.testing.assert_array_equal(a, b)
    assert risk_a == risk_b
    assert int(a.sum()) <= 32
    assert 0 <= risk_a <= 1


@pytest.mark.parametrize("budget", [3., 8.])
def test_old_history_no_mutation_eight_update_comparison_is_labeled(budget):
    result = compare(draws=32, budget=budget)
    assert result["status"].startswith("EXPLORATORY_OLD_HISTORY")
    assert result["evidence_type"] == "simulated_engineering_only_not_observed_island_data"
    c = result["conditions"]
    assert c["K"] == 32 and c["mutation_rate"] == 0.
    assert c["generations"] == 8
    assert c["source_visitor_history_seed"] == 26110601
    assert c["n_independent_visitor_histories"] == 1
    assert c["new_confirmatory_histories"] == 0
    assert c["confirmatory_37110801_37110864_used"] is False
    assert result["numerical_integrity"]["canonical_biology_modified"] is False
    assert len(result["trajectories"]["deterministic"]) == 8
    for key in ("exact_finite_markov", "projected_gaussian"):
        arm = result["arms"][key]
        assert arm["n_draws"] == 32
        assert arm["invalid_censuses"] == 0
        assert 0 <= arm["extinction_probability"] <= 1
        assert 0 <= arm["mean_genotype_classes_unconditional"] <= 27
        assert len(arm["initial_genotype_indices"]) == 4
        if arm["n_occupied"] > 0:
            assert len(arm["occupied_trait_mean"]) == 3
    det = result["arms"]["deterministic_expected_integer_plug_in"]
    assert det["n_draws"] == 0
    assert det["not_a_sampling_probability"] is True
    assert det["mean_census"] <= 32
    assert result["numerical_integrity"]["standalone_sde_or_spde_validated"] is False
