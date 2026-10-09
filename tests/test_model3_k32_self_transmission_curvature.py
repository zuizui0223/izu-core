"""Exact Model3 viable self linear in assurance but allele numerator is curved."""
from dataclasses import replace

import numpy as np
import pytest

from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import genotype_counts_to_canonical_state
from scripts.audit_model3_k32_fixed_frequency_heterozygosity import (
    controlled_assurance_pairs,
)
from scripts.audit_model3_k32_self_transmission_curvature import (
    KEYS,exact_self_transmission_contrast,run_self_curvature,
)
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN,load_design,config as source_config,
)


def source_inputs(budget=8.):
    c,g,v,_=fixed_support_problem(capacity=32,ovule_budget=budget)
    src=source_config(load_design(DEFAULT_DESIGN),"prior_selfing",0.,"evolving")
    cfg=replace(src,capacity=32,survival=0.,mutation_rate=0.,
                ovule_budget=budget,
                seed_arrival=replace(src.seed_arrival,supply=0.))
    state=genotype_counts_to_canonical_state(c,g,0,32)
    assert cfg.assurance_cost==0 and cfg.investment_cost==.5
    return state,v,cfg


@pytest.mark.parametrize("operator,expected_curvature",[
    ("heterozygosity_up",-.25),("heterozygosity_down",+.25)])
def test_allele_numerator_curvature_without_seed_mass_curvature(operator,expected_curvature):
    state,vis,cfg=source_inputs()
    order=np.random.default_rng(501).permutation(len(state.ids))
    sham=controlled_assurance_pairs(state,"sham",order)
    edited=controlled_assurance_pairs(state,operator,order)
    assert edited is not None
    r=exact_self_transmission_contrast(sham,edited,vis,cfg)
    assert set(r)==set(KEYS)
    assert r["sum_of_self_dosage_products_delta"]==pytest.approx(expected_curvature,abs=1e-12)
    assert r["self_intensity_if_both_investments_equal_delta"]==pytest.approx(0.,abs=1e-12)
    assert r["raw_high_allele_self_numerator_delta"]==pytest.approx(
        r["intrinsic_dosage_numerator_at_mean_investment"]+
        r["investment_alignment_numerator"],abs=1e-11)
    assert r["self_direction_total_exact"]==pytest.approx(
        sum(r[k] for k in (
            "self_direction_intrinsic_numerator_over_old_total",
            "self_direction_investment_alignment_over_old_total",
            "self_direction_denominator_due_to_self_seed_mass",
            "self_direction_denominator_due_to_outcross_seed_mass")),
        abs=1e-12)
    assert r["self_viable_seed_intensity_delta"]+r["outcross_viable_seed_intensity_delta"]==pytest.approx(
        r["total_viable_seed_intensity_delta"],abs=1e-11)
    if expected_curvature<0:
        assert r["intrinsic_dosage_numerator_at_mean_investment"]<0
    else:
        assert r["intrinsic_dosage_numerator_at_mean_investment"]>0


def test_equal_investment_weights_self_seed_mass_does_not_change():
    state,vis,cfg=source_inputs()
    alleles=state.alleles.copy()
    alleles[:,1,:]=.25
    state=replace(state,alleles=alleles)
    order=np.random.default_rng(99).permutation(len(state.ids))
    sham=controlled_assurance_pairs(state,"sham",order)
    for operator in ("heterozygosity_up","heterozygosity_down"):
        edited=controlled_assurance_pairs(state,operator,order)
        assert edited is not None
        r=exact_self_transmission_contrast(sham,edited,vis,cfg)
        assert r["investment_alignment_numerator"]==pytest.approx(0.,abs=1e-12)
        assert r["self_viable_seed_intensity_delta"]==pytest.approx(0.,abs=1e-12)
        assert r["raw_high_allele_self_numerator_delta"]==pytest.approx(
            r["intrinsic_dosage_numerator_at_mean_investment"],abs=1e-12)


def test_forbids_false_nonzero_intrinsic_assurance_cost_claim():
    state,vis,cfg=source_inputs()
    order=np.arange(len(state.ids))
    sham=controlled_assurance_pairs(state,"sham",order)
    edited=controlled_assurance_pairs(state,"heterozygosity_up",order)
    assert edited is not None
    with pytest.raises(ValueError):
        exact_self_transmission_contrast(sham,edited,vis,
                                         replace(cfg,assurance_cost=.5))
    with pytest.raises(ValueError):
        exact_self_transmission_contrast(sham,edited,vis,
                                         replace(cfg,assurance_timing="delayed"))
    altered=sham.alleles.copy()
    altered[:,0,:]=.75
    with pytest.raises(ValueError):
        exact_self_transmission_contrast(sham,replace(edited,alleles=altered),
                                         vis,cfg)


@pytest.mark.parametrize("budget",[3.,8.])
def test_old_history_conditional_self_curvature_reconstruction(budget):
    d=run_self_curvature(budget=budget,draws=16,permutations=2,seed=420261017)
    assert d["status"]=="ORIGINAL_K32_EXACT_LINEAR_SELFING_DOSAGE_CURVATURE_AUDIT_VERIFIED"
    c=d["source_provenance"]
    assert (c["K"],c["mutation_rate"],c["generations"],c["budget"])==(32,0,8,budget)
    assert c["old_visitor_history"]==26110601
    assert c["n_independent_visitor_histories"]==1
    assert c["assurance_cost"]==0
    assert c["investment_cost"]==.5
    assert c["selfing_depression"]==.5
    assert c["source_self_seed_function_linear_in_assurance_a"] is True
    assert c["source_model3_reproductive_biology_modified"] is False
    assert c["prospective_confirmatory_histories_accessed"] is False
    assert set(d["source_parent_years"])=={"1","4","8"}
    for parent_year in d["source_parent_years"].values():
        for op in ("heterozygosity_up","heterozygosity_down"):
            result=parent_year[op]
            n=result["n_source_parent_paths_eligible"]
            assert 0<=n<=c["n_source_year8_parent_survivors"]
            for vv in ("1","8"):
                summary=result["visitors"][vv]
                assert summary["n_original_parent_paths"]==n
                assert summary["max_absolute_reconstruction_error"]<1e-10
                if n:
                    m=summary["means"]
                    assert m["self_intensity_if_both_investments_equal_delta"]==pytest.approx(0.,abs=1e-12)
                    expected= -.25 if op=="heterozygosity_up" else .25
                    assert m["sum_of_self_dosage_products_delta"]==pytest.approx(expected,abs=1e-12)


def test_rejects_other_budgets_or_small_cohort():
    with pytest.raises(ValueError):
        run_self_curvature(budget=4.,draws=16)
    with pytest.raises(ValueError):
        run_self_curvature(budget=8.,draws=8)
