"""8×8 original visitor by parental-genotype-state cross source guards."""
import numpy as np
import pytest

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_k32_pathwise_selection_drift import allele_frequency_basis
from scripts.audit_model3_k32_state_visitor_cross import (
    STAT_KEYS,exact_original_crossed_direction,
    symmetrized_endpoint_attribution,run_state_visitor_cross,
)
from scripts.run_model3_three_arm_k32_old_history import canonical_conditional_kernel


def test_twenty_four_cell_endpoint_sign_attribution_and_interaction_identity():
    x=np.zeros((8,8,3),float)
    for t in range(8):
        for v in range(8):
            x[t,v]=np.array([
                -0.05+0.015*t/7+0.01*v/7+0.03*t*v/49,
                +0.01-0.02*t/7,
                -0.03+0.01*v/7,
            ])
    r=symmetrized_endpoint_attribution(x)
    assert r["actual_diagonal_late_minus_early"]==pytest.approx([.055,-.02,.01])
    assert r["symmetrized_state_contribution"]==pytest.approx([.03,-.02,0.])
    assert r["symmetrized_visitor_contribution"]==pytest.approx([.025,0.,.01])
    assert r["state_visitor_difference_in_differences"]==pytest.approx([.03,0.,0.])
    assert r["numerical_identity_max_abs_error"]<1e-12
    with pytest.raises(ValueError):
        symmetrized_endpoint_attribution(np.zeros((7,8,3)))


@pytest.mark.parametrize("budget",[3.,8.])
def test_fixed_parent_original_ledger_equals_full_exact_genotype_offspring_mean(budget):
    first,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=budget)
    r=exact_original_crossed_direction(first,grid,vis,cfg,0)
    assert r["status"]=="MATCHED_MARGINALS"
    assert r["source_canonical_biology_edited"] is False
    _,q=canonical_conditional_kernel(first,grid,vis,cfg,0)
    basis=allele_frequency_basis(grid)
    np.testing.assert_allclose(
        np.asarray(r["expected_next_allele_frequency"]),q@basis,
        atol=1e-12,rtol=0)
    np.testing.assert_allclose(
        np.asarray(r["parent_allele_frequency"])+
        np.asarray(r["expected_allele_direction"]),
        np.asarray(r["expected_next_allele_frequency"]),
        atol=1e-12,rtol=0)
    np.testing.assert_allclose(
        np.asarray(r["viable_self_seed_allele_direction"])+
        np.asarray(r["outcross_paternal_allele_direction"])+
        np.asarray(r["outcross_maternal_allele_direction"]),
        np.asarray(r["expected_allele_direction"]),
        atol=1e-12,rtol=0)
    assert exact_original_crossed_direction(
        np.zeros_like(first),grid,vis,cfg,0)=={"status":"EXTINCT_PARENT"}


@pytest.mark.parametrize("budget",[3.,8.])
def test_cross_one_old_visitor_history_with_same_surviving_parent_cohort(budget):
    result=run_state_visitor_cross(budget=budget,draws=16,seed=420261017)
    assert result["status"]=="K32_ORIGINAL_MODEL3_OLD_HISTORY_STATE_VISITOR_CROSS_VERIFIED"
    c=result["conditions"]
    assert (c["K"],c["mutation_rate"],c["generations"],c["budget"])==(32,0,8,budget)
    assert c["old_visitor_history"]==26110601
    assert c["n_independent_visitor_histories"]==1
    assert c["n_nested_demographic_draws"]==16
    assert c["source_biological_reproduction_changed"] is False
    assert c["visitor_swap_is_non_autonomous_one_step_counterfactual"] is True
    assert c["prospective_confirmatory_history_used"] is False
    assert c["source_parent_survival_cohort_common_across_years"] is True
    assert c["conditioned_on_occupation_at_start_of_year8"] is True
    assert len(result["full_8x8_same_cohort"])==8
    for t in range(1,9):
        assert len(result["full_8x8_same_cohort"][str(t)])==8
        for v in range(1,9):
            cell=result["full_8x8_same_cohort"][str(t)][str(v)]
            assert set(cell)==set(STAT_KEYS)
            for key in STAT_KEYS:
                assert cell[key]["n"]==c["n_alive_parent_year7"]
            np.testing.assert_allclose(
                cell["expected_allele_direction"]["mean"],
                sum((np.asarray(cell[k]["mean"]) for k in STAT_KEYS[1:]),
                    np.zeros(3)),atol=1e-12,rtol=0)
        diagonal=result["full_8x8_same_cohort"][str(t)][str(t)]
        np.testing.assert_allclose(
            result["observed_diagonal_expected_direction_by_original_parent_year"][t-1],
            diagonal["expected_allele_direction"]["mean"],
            atol=1e-12,rtol=0)
    endpoint=result["early_late_same_cohort_order_symmetrized"]
    np.testing.assert_allclose(
        np.asarray(endpoint["symmetrized_state_contribution"])+
        endpoint["symmetrized_visitor_contribution"],
        endpoint["actual_diagonal_late_minus_early"],atol=1e-12,rtol=0)
    assert endpoint["numerical_identity_max_abs_error"]<1e-12
    assert result["balanced_8x8_effects"]["max_double_centering_error"]<1e-12
    for x in result["early_late_same_cohort_demographic_mc_se"].values():
        assert x["n"]==c["n_alive_parent_year7"]


def test_rejects_unapproved_histories_budgets_and_draw_counts():
    with pytest.raises(ValueError):
        run_state_visitor_cross(budget=4.,draws=16)
    with pytest.raises(ValueError):
        run_state_visitor_cross(budget=8.,draws=8)
