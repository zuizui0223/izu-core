"""Source-conformity and non-promotion checks for three-way old-history assay."""
import numpy as np
import pytest

from scripts.compare_model3_three_k32_old_history import (
    _parent_projection, _last_step_descriptors, _allele_loss, compare_three,
    FIXED_K, FIXED_YEARS, OLD_HISTORY,
)
from scripts.audit_model3_projected_gaussian_genotypes import fixed_support_problem
from scripts.audit_model3_stochastic_bridge import capped_poisson_distribution


def test_parent_projection_is_explicit_and_conserves_integer_census():
    floats=np.array([2.7,1.2,.1,0.])
    projected,error=_parent_projection(floats,32)
    np.testing.assert_array_equal(projected,[3,1,0,0])
    assert error==pytest.approx(.6)
    assert projected.dtype.kind in "iu"
    assert int(projected.sum())==4
    with pytest.raises(ValueError):
        _parent_projection(np.array([float("nan")]),32)
    with pytest.raises(ValueError):
        _parent_projection(np.array([-1.,2.]),32)


def test_conditional_last_step_formula_keeps_extinction_separate():
    q=np.array([.02,.98])
    pn=capped_poisson_distribution(.8,32)
    r=_last_step_descriptors(q,pn,occupancy_prob=.4)
    assert r["expected_genotype_classes_given_occupied"]>=1
    assert 0<=r["expected_genotype_simpson_given_occupied"]<=1
    assert len(r["genotype_absence_including_extinction"])==2
    assert r["genotype_absence_including_extinction"][0]>.6
    assert _last_step_descriptors(None,pn,occupancy_prob=.4) is None


def test_true_allele_loss_not_confused_with_genotype_class_absence():
    first,grid,_,_=fixed_support_problem(capacity=32,ovule_budget=8.)
    assert _allele_loss(first,grid)==0
    single=np.zeros_like(first)
    single[np.flatnonzero(first)[0]]=1
    assert _allele_loss(single,grid)>=1
    assert _allele_loss(np.zeros_like(first),grid)==6



def test_source_kernel_agrees_with_existing_three_arm_code_at_same_old_history():
    """Independent comparison implementations must not silently change biology."""
    from dataclasses import replace
    from scripts.compare_model3_three_k32_old_history import _kernel
    from scripts.run_model3_three_arm_k32_old_history import canonical_conditional_kernel
    from scripts.run_chapter2_assurance_generality import (
        DEFAULT_DESIGN, config as source_config, load_design,
    )
    from scripts.run_model3_persistent_isolation import exposure
    first,grid,_,_=fixed_support_problem(capacity=32,ovule_budget=8.)
    d=load_design(DEFAULT_DESIGN)
    source=source_config(d,"prior_selfing",0.,"evolving")
    cfg=replace(source,capacity=32,survival=0.,mutation_rate=0.,
                ovule_budget=8.,seed_arrival=replace(source.seed_arrival,supply=0.))
    visitors=exposure(26110601,"near").visitors
    x,q=_kernel(first,grid,visitors[0],cfg,0)
    y,p=canonical_conditional_kernel(first,grid,visitors[0],cfg,0)
    assert x==pytest.approx(y,rel=0,abs=1e-12)
    np.testing.assert_allclose(q,p,rtol=0,atol=1e-12)

def test_three_way_comparison_fixed_old_history_and_nonpromotion():
    r=compare_three(draws=16,seed=5213,budget=8.)
    c=r["conditions"]
    assert c["capacity"]==FIXED_K==32
    assert c["generations"]==FIXED_YEARS==8
    assert c["mutation_rate"]==0
    assert c["old_visitor_history"]==OLD_HISTORY==26110601
    assert c["new_visitor_histories_sampled"]==0
    assert c["confirmatory_cohorts_accessed"] is False
    assert c["independent_visitor_histories"]==1
    assert c["genotype_classes"]==27
    assert c["reproductive_setting"]=="prior_selfing"
    assert r["evidence_type"].startswith("synthetic_")
    assert r["canonical_biology_modified"] is False
    assert r["numerical_precision"]["finite_markov_integer_mass_error"]==0
    assert r["numerical_precision"]["gaussian_projected_integer_mass_error"]==0
    det=r["arms"]["deterministic_conditional_expectation"]
    assert len(det["trajectory"])==8
    assert len(det["projected_parent_l1_by_year"])==8
    for name in ("exact_finite_Markov","projected_Gaussian"):
        a=r["arms"][name]
        assert 0<=a["probability_extinct"]<=1
        assert 0<=a["mean_genotype_classes"]<=32
        assert 0<=a["mean_allele_types_lost"]<=6
        assert len(a["founder_genotype_indices"])==4
        if a["n_occupied"]:
            assert len(a["trait_mean_given_occupied"])==3
    assert set(r["errors_relative_to_exact_Markov_Monte_Carlo"]) >= {
        "deterministic_extinction_abs","gaussian_extinction_abs",
        "gaussian_allele_loss_abs",
    }


def test_rejects_unplanned_horizon_and_small_sample():
    with pytest.raises(ValueError):
        compare_three(draws=16,years=7)
    with pytest.raises(ValueError):
        compare_three(draws=8)
