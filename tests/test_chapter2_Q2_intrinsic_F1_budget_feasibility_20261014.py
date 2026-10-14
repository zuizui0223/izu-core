"""Check Model3 nonlinear first-offspring intrinsic potential without births."""
from dataclasses import replace
import numpy as np
import pytest

from scripts.model3_island import reproduction
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    original_fixture, original_context
)
from scripts.audit_chapter2_balanced_cocarriage_20261014 import (
    balanced_source, balanced_cocarriage
)
from scripts.audit_chapter2_full_F1_joint_distribution_20261014 import (
    one_offspring_joint_distribution
)
from scripts.audit_chapter2_Q2_intrinsic_F1_budget_feasibility_20261014 import (
    one_child_intrinsic_budget_distribution, technical_report
)


def direct_two_locus_first_child_ovule_expectation(state,ledger,cfg):
    """Independent sum over every parent-pair × sixteen diploid copy choices."""
    parent=ledger.outcross.copy()
    np.fill_diagonal(parent,np.diag(parent)+ledger.self_viable)
    parent/=parent.sum()
    expected_ovules=expected_no_pollen_self=0.0
    for father in range(48):
        for mother in range(48):
            weight=float(parent[father,mother])
            if weight == 0:
                continue
            for af in (0,1):
                for am in (0,1):
                    A=(state.alleles[father,2,af]+
                       state.alleles[mother,2,am])/2
                    for inf in (0,1):
                        for inm in (0,1):
                            I=(state.alleles[father,1,inf]+
                               state.alleles[mother,1,inm])/2
                            ovules=(cfg.ovule_budget *
                                    np.exp(-cfg.investment_cost*I**2 -
                                           cfg.assurance_cost*A**2))
                            w=weight/16
                            expected_ovules+=w*ovules
                            expected_no_pollen_self+=w*ovules*A*(1-cfg.depression)
    return expected_ovules,expected_no_pollen_self


@pytest.mark.parametrize("pool,context,m",[
    (0,0,0),(0,0,12),(3,3,0),(7,3,12),(9,4,3),(15,4,12)
])
def test_native_ovule_formula_matches_independent_copy_enumeration(pool,context,m):
    d=original_fixture()
    cfg,vis=original_context(d,"main",context)
    state=balanced_cocarriage(balanced_source(pool),pool,m)
    ledger=reproduction.reproduce(state,vis,cfg)
    joint=one_offspring_joint_distribution(state,ledger)
    actual=one_child_intrinsic_budget_distribution(joint,cfg)
    brute=direct_two_locus_first_child_ovule_expectation(state,ledger,cfg)
    assert abs(actual["conditional_expected_offspring_intrinsic_ovule_budget"]-
               brute[0])<2e-11
    assert abs(actual["conditional_expected_no_pollen_self_viable_potential"]-
               brute[1])<2e-11


def test_marginal_factor_match_does_not_force_joint_expected_cost_match():
    fixture=original_fixture()
    cfg,vis=original_context(fixture,"main",0)
    for pool in (0,1,3,7,15):
        b=balanced_source(pool)
        results=[]
        for m in (0,3,6,12):
            s=balanced_cocarriage(b,pool,m)
            led=reproduction.reproduce(s,vis,cfg)
            joint=one_offspring_joint_distribution(s,led)
            z=one_child_intrinsic_budget_distribution(joint,cfg)
            results.append(z)
        for key in ("expected_cost_A_factor","expected_cost_I_factor"):
            assert max(x[key] for x in results)-min(x[key] for x in results)<1e-12
        left,right=results[0],results[-1]
        delta_ovules=(right["conditional_expected_offspring_intrinsic_ovule_budget"]-
                      left["conditional_expected_offspring_intrinsic_ovule_budget"])
        delta_cov=(right["covariance_of_model3_ovule_cost_factors"]-
                   left["covariance_of_model3_ovule_cost_factors"])
        assert abs(delta_ovules-cfg.ovule_budget*delta_cov)<1e-11


def test_zero_one_cost_factors_prevent_joint_distribution_only_ovule_difference():
    fixture=original_fixture()
    cfg,vis=original_context(fixture,"main",0)
    pool=4
    base=balanced_source(pool)
    p={}
    for m in (0,12):
        s=balanced_cocarriage(base,pool,m)
        led=reproduction.reproduce(s,vis,cfg)
        p[m]=one_offspring_joint_distribution(s,led)
    for parameter in ("investment_cost","assurance_cost"):
        # Technical mathematical negative control: NOT an approved model change
        no_joint_interaction=replace(cfg,**{parameter:0.0})
        values=[one_child_intrinsic_budget_distribution(p[m],no_joint_interaction)
                ["conditional_expected_offspring_intrinsic_ovule_budget"]
                for m in (0,12)]
        assert abs(values[1]-values[0])<1e-12


def test_all_192_source_scope_biology_execution_stays_closed():
    r=technical_report()
    assert r["status"]=="T0_CONDITIONAL_FIRST_OFFSPRING_GENOTYPE_POTENTIAL_ONLY"
    assert r["same_original_Model3_ovule_formula"] is True
    assert r["original_native_population_updates"]==0
    assert r["actual_offspring_births"]==0
    assert r["biological_evolutionary_histories"]==0
    assert r["new_pollen_community_or_fitness_assay"] is False
    assert r["original_order_six_class_response"]=="NOT_MEASURED"
    assert r["population_persistence_Q4"]=="NOT_MEASURED"
    assert len(r["rows"])==192
    assert len(r["context_comparisons"])==3
    assert all(x["synthetic_sources"]==16 for x in r["context_comparisons"])
    for x in r["context_comparisons"]:
        assert abs(x["m12_minus_m0_expected_intrinsic_ovules_min"]-
                   8*x["m12_minus_m0_intrinsic_cost_covariance_min"])<1e-10
        assert abs(x["m12_minus_m0_expected_intrinsic_ovules_max"]-
                   8*x["m12_minus_m0_intrinsic_cost_covariance_max"])<1e-10


def test_bad_conditional_zygote_law_rejected():
    fixture=original_fixture()
    cfg,_=original_context(fixture,"main",0)
    with pytest.raises(ValueError,match="source"):
        one_child_intrinsic_budget_distribution(np.zeros((33,33)),cfg)


def test_original_source_native_intrinsic_ovule_difference_matches_independent_regression_snapshot():
    """Source-locked descriptive regression values, not a minimum effect rule."""
    report=technical_report()
    snapshot={
        0:(7.85439201678173e-07,9.536903924356466e-07),
        3:(6.602497197860657e-07,8.358121714735489e-07),
        4:(7.496123473060834e-07,9.232660431734985e-07),
    }
    assert len(report["context_comparisons"])==3
    for row in report["context_comparisons"]:
        lo,hi=snapshot[row["original_visitor_context"]]
        assert abs(row["m12_minus_m0_expected_intrinsic_ovules_min"]-lo)<1e-11
        assert abs(row["m12_minus_m0_expected_intrinsic_ovules_max"]-hi)<1e-11
        assert row["m12_minus_m0_expected_intrinsic_ovules_positive_count"]==16
        assert row["m12_minus_m0_expected_intrinsic_ovules_negative_count"]==0
        # Deliberately small on the ORIGINAL source scale; not a proven
        # long-term fitness benefit or a source-cluster effect size.
        assert 0<row["m12_minus_m0_expected_intrinsic_ovules_max"]<1e-5
