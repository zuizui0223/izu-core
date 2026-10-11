"""Exactly trace full-joint Mendelian allele direction to parental marginals."""
import numpy as np
import pytest

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import genotype_counts_to_canonical_state
from scripts.model3_island.reproduction import reproduce
from scripts.run_model3_k32_outcross_factorial import (
    MASK_LABELS,combine_outcross_factors,
)
from scripts.audit_model3_k32_parental_marginal_direction import (
    LOCI, exact_parent_marginal_contributions,
    same_parent_factorial_marginals,run_parental_marginals,
)


@pytest.mark.parametrize("budget",[3.,8.])
def test_parental_mean_exactly_equals_full_mendelian_genotype_kernel(budget):
    first,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=budget)
    state=genotype_counts_to_canonical_state(first,grid,0,32)
    ledger=reproduce(state,vis,cfg)
    for mask in range(8):
        alt=combine_outcross_factors(ledger,mask)
        r=exact_parent_marginal_contributions(
            state,ledger,alt,grid,check_child_genotype_law=True)
        assert r["status"]=="MATCHED_MARGINALS"
        q=np.asarray(r["expected_next_allele_frequency"])
        p=np.asarray(r["parent_allele_frequency"])
        direction=np.asarray(r["expected_allele_direction"])
        assert len(q)==3
        np.testing.assert_allclose(p+direction,q,atol=1e-12)
        np.testing.assert_allclose(
            direction,
            np.asarray(r["viable_self_seed_allele_direction"])+
            np.asarray(r["outcross_paternal_allele_direction"])+
            np.asarray(r["outcross_maternal_allele_direction"]),
            atol=1e-12,rtol=0)


def test_only_maternal_paternal_marginals_change_at_same_parents():
    first,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    result=same_parent_factorial_marginals(first,grid,vis,cfg,0)
    assert result["status"]=="EXACT_PARENTAL_MARGINALS"
    assert set(result["same_parent_intervention_contrasts"])==set(range(1,8))
    found_change=False
    for mask,contrast in result["same_parent_intervention_contrasts"].items():
        assert MASK_LABELS[mask]
        assert contrast["max_identity_error"]<1e-12
        np.testing.assert_allclose(contrast["self_component_contrast"],0.,atol=1e-12)
        np.testing.assert_allclose(
            contrast["source_parent_allele_direction_difference"],
            np.asarray(contrast["outcross_father_marginal_contrast"])+
            contrast["outcross_mother_marginal_contrast"],atol=1e-12)
        found_change |= bool(np.max(np.abs(
            contrast["source_parent_allele_direction_difference"]))>1e-12)
    assert found_change


def test_absorbing_parent_extinction_is_not_fake_allele_frequency():
    first,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    zero=np.zeros_like(first)
    assert same_parent_factorial_marginals(zero,grid,vis,cfg,0)=={
        "status":"EXTINCT_PARENT"}


@pytest.mark.parametrize("budget",[3.,8.])
def test_original_old_history_3_locus_parental_direction_for_8_years(budget):
    r=run_parental_marginals(budget=budget,draws=16,seed=420261017)
    assert r["status"]=="K32_EXACT_SAME_PARENT_MATERNAL_PATERNAL_PRICE_IDENTITY"
    c=r["conditions"]
    assert c["K"]==32 and c["mutation_rate"]==0
    assert c["old_visitor_history"]==26110601
    assert c["independent_visitor_histories"]==1
    assert c["locus_order"]==list(LOCI)
    assert c["canonical_original_Model3_biology_modified"] is False
    assert c["prospective_confirmatory_histories_used"] is False
    assert c["same_original_parental_genotype_state_across_all_masks"] is True
    assert c["no_autonomous_alternative_population_forecast"] is True
    assert len(r["years"])==8
    for row in r["years"].values():
        assert row["n_surviving_original_parent_states"]>0
        src=row["source_marginals"]
        expected=np.asarray(src["expected_allele_direction"]["mean"])
        terms=sum((
            np.asarray(src[k]["mean"]) for k in
            ("self_seed_contribution","outcross_father_contribution",
             "outcross_mother_contribution")
        ),np.zeros(3))
        np.testing.assert_allclose(expected,terms,atol=1e-12,rtol=0)
        for mask in range(1,8):
            contrast=row["factorial_contrasts_on_identical_parent_state"][str(mask)]
            np.testing.assert_allclose(
                contrast["counterfactual_minus_source_expected_allele_direction"]["mean"],
                np.asarray(contrast["outcross_father_marginal_contribution"]["mean"])+
                contrast["outcross_mother_marginal_contribution"]["mean"],
                atol=1e-12,rtol=0)
            assert contrast["self_contribution_zero_exactly"] is True


def test_source_history_scope_rejects_unsupported_budgets_or_draws():
    with pytest.raises(ValueError):
        run_parental_marginals(budget=4.,draws=16)
    with pytest.raises(ValueError):
        run_parental_marginals(budget=8.,draws=8)
