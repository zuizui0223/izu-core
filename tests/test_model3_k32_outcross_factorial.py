"""Full 2^3 Model3 outcross factor intervention fidelity and nonadditivity checks."""
import numpy as np
import pytest

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import genotype_counts_to_canonical_state
from scripts.model3_island.reproduction import reproduce
from scripts.run_model3_k32_outcross_ablation import (
    SOURCE, ARMS, reweighted_outcross, step_with_intervention,
)
from scripts.run_model3_k32_outcross_factorial import (
    FACTOR_NAMES, FACT_METRICS, MASK_LABELS, SINGLE_ARM,
    combine_outcross_factors, step_with_mask, factorial_terms, run_factorial,
)


@pytest.mark.parametrize("budget",[3.,8.])
def test_all_8_masks_conserve_ledger_census_support_and_exact_one_factor_baseline(budget):
    first,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=budget)
    s=genotype_counts_to_canonical_state(first,grid,0,32)
    ledger=reproduce(s,vis,cfg)
    for mask in range(8):
        alt=combine_outcross_factors(ledger,mask)
        assert alt.shape==ledger.outcross.shape
        assert np.all(alt>=0) and np.all(np.diag(alt)==0)
        assert np.all((ledger.outcross>0)|(alt<=1e-12))
        assert alt.sum()==pytest.approx(ledger.outcross.sum(),abs=1e-10)
        if mask in SINGLE_ARM:
            np.testing.assert_allclose(
                alt,reweighted_outcross(ledger,SINGLE_ARM[mask]),
                atol=1e-12,rtol=0)
        elif mask==0:
            np.testing.assert_array_equal(alt,ledger.outcross)


def test_source_mask_exact_canonical_replay_and_single_masks_match_previous_code():
    first,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    for mask,arm in [(0,SOURCE),(1,ARMS[1]),(2,ARMS[2]),(4,ARMS[3])]:
        seen=step_with_mask(first,grid,vis,cfg,np.random.default_rng(883),0,mask)
        expected=step_with_intervention(
            first,grid,vis,cfg,np.random.default_rng(883),0,arm)
        np.testing.assert_array_equal(seen,expected)


def test_mobius_contrasts_telescoping_and_interactions():
    # f(S)=5 +2 E +3 R -M +7 ER -4 RM +6 ERM
    d={i:np.array([5+2*(bool(i&1))+3*(bool(i&2))-
                    (bool(i&4))+7*(bool(i&1) and bool(i&2))-
                    4*(bool(i&2) and bool(i&4))+
                    6*(i==7)],float)
       for i in range(8)}
    t=factorial_terms(d)
    assert t[0][0]==pytest.approx(5.)
    for key,val in [(1,2.),(2,3.),(4,-1.),(3,7.),(5,0.),(6,-4.),(7,6.)]:
        assert t[key][0]==pytest.approx(val)
    assert sum(t[k][0] for k in range(1,8))==pytest.approx(d[7][0]-d[0][0])
    with pytest.raises(ValueError):
        factorial_terms({0:np.array([1.]),7:np.array([2.])})


def test_recruitment_after_absorption_cannot_resurrect_source_allele():
    first,grid,vis,cfg=fixed_support_problem(capacity=32,ovule_budget=8.)
    extinct=np.zeros_like(first)
    for mask in range(8):
        np.testing.assert_array_equal(
            step_with_mask(extinct,grid,vis,cfg,np.random.default_rng(7),0,mask),
            extinct)
    with pytest.raises(ValueError):
        step_with_mask(first,grid,vis,cfg,np.random.default_rng(7),0,8)


@pytest.mark.parametrize("budget",[3.,8.])
def test_eight_year_factorial_source_scope_and_all_interaction_identities(budget):
    r=run_factorial(budget=budget,draws=16,seed=420261017)
    c=r["conditions"]
    assert r["status"]=="SOURCE_EXACT_K32_OLD_HISTORY_FULL_2x2x2_FACTORIAL"
    assert (c["K"],c["mutation_rate"],c["generations"],c["ovule_budget"])==(32,0,8,budget)
    assert c["old_visitor_history"]==26110601
    assert c["independent_visitor_histories"]==1
    assert c["canonical_source_biology_modified"] is False
    assert c["prospective_confirmatory_cohorts_used"] is False
    assert c["self_seed_intensity_and_total_outcross_seed_intensity_preserved_at_each_current_parent"] is True
    assert len(r["years"])==8 and len(FACTOR_NAMES)==3
    assert r["masks"]=={str(i):MASK_LABELS[i] for i in range(8)}
    for year in r["years"].values():
        assert len(year["arms"])==8
        for arm in year["arms"].values():
            assert arm["n_survivors"]+arm["n_extinct"]==16
            assert 0<=arm["mean_lost_alleles_all"]<=6
        for metric in FACT_METRICS:
            row=year["metrics"][metric]
            assert row["max_additivity_identity_error"]<1e-10
            total=row["all_three_minus_original"]["mean"]
            singles=row["sum_of_three_single_factor_effects"]["mean"]
            interactions=row["aggregate_pairwise_and_three_way_interaction"]["mean"]
            assert singles+interactions==pytest.approx(total,abs=1e-12)
            assert row["aggregate_pairwise_and_three_way_interaction"]["demographic_mc_se"] is not None
            assert sum(x["mean"] for x in row["factorial_components"].values())==pytest.approx(total,abs=1e-12)


def test_disallowed_budget_guard():
    with pytest.raises(ValueError):
        run_factorial(budget=4.,draws=16)
    with pytest.raises(ValueError):
        run_factorial(budget=8.,draws=8)
