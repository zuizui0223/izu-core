"""Independent exact 2-locus one-offspring distribution under old Model3 returns."""
import inspect

import numpy as np
import pytest

from scripts.model3_island import reproduction, types
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    original_fixture, original_context
)
from scripts.audit_chapter2_balanced_cocarriage_20261014 import (
    balanced_source, balanced_cocarriage
)
from scripts.audit_chapter2_full_F1_joint_distribution_20261014 import (
    LEVELS, TOL, one_offspring_joint_distribution, total_variation,
    technical_report
)


def independent_bincount_joint(state,ledger):
    """Separate vectorized flat-bin accumulator, summing all 16 A/I copies."""
    parent=ledger.outcross.copy()
    np.fill_diagonal(parent,np.diag(parent)+ledger.self_viable)
    parent/=parent.sum()
    original=state.alleles
    result=np.zeros(LEVELS*LEVELS,dtype=float)
    weight=parent.ravel()/16
    for aF in (0,1):
        for aM in (0,1):
            Abin=np.rint((original[:,2,aF,None]+original[None,:,2,aM])*16).astype(int)
            for iF in (0,1):
                for iM in (0,1):
                    Ibin=np.rint((original[:,1,iF,None]+original[None,:,1,iM])*16).astype(int)
                    result+=np.bincount((Abin*LEVELS+Ibin).ravel(),
                                        weights=weight,minlength=LEVELS*LEVELS)
    return result.reshape((LEVELS,LEVELS))


@pytest.mark.parametrize("pool,context,m",[
    (0,0,0),(0,0,12),(0,3,0),(0,3,12),
    (7,4,3),(7,4,6),(8,3,0),(8,3,12),(8,4,12),(15,3,0),(15,3,12),
])
def test_exact_two_locus_distribution_against_independent_bincount(pool,context,m):
    base=balanced_source(pool)
    s=balanced_cocarriage(base,pool,m)
    fixture=original_fixture()
    cfg,v=original_context(fixture,"main",context)
    led=reproduction.reproduce(s,v,cfg)
    actual=one_offspring_joint_distribution(s,led)
    independent=independent_bincount_joint(s,led)
    assert actual.shape==(33,33)
    assert np.isfinite(actual).all()
    assert np.min(actual)>=0
    assert abs(actual.sum()-1)<TOL
    assert np.max(abs(actual-independent))<TOL
    assert abs(total_variation(actual,independent))<TOL


def test_all_source_192_conditions_match_entire_marginals_but_not_joint():
    r=technical_report()
    assert r["source_profiles"]==16
    assert r["conditional_first_offspring_distributions"]==192
    assert r["future_biological_histories"]==0
    assert r["actual_offspring_births"]==0
    assert r["long_run_evolution_order"]=="NOT_MEASURED"
    assert r["Q4_population_persistence"]=="NOT_MEASURED"
    assert len(r["context_summary"])==3
    for row in r["rows"]:
        assert row["all_marginal_F1_distributions_matched"]
        assert row["A_marginal_max_absolute_bin_difference_from_m0"]<1e-12
        assert row["I_marginal_max_absolute_bin_difference_from_m0"]<1e-12
        if row["co_carriers_m"]==0:
            assert row["joint_A_I_total_variation_from_m0"]==0
        else:
            assert row["joint_A_I_total_variation_from_m0"]>1e-8
    for x in r["context_summary"]:
        assert x["sources_with_nonzero_m12_vs_m0_joint_change"]==16
        assert 0 < x["min_m12_vs_m0_joint_total_variation"] <= x["max_m12_vs_m0_joint_total_variation"] <= 1
        # Descriptive SOURCE-LOCKED regression values independently recomputed
        # after the original exploratory run; NOT prospective acceptance limits.
        frozen = {
            0: (0.030801658703423565, 0.08365511485973845),
            3: (0.026796926775215973, 0.10463431991308235),
            4: (0.030697583670462505, 0.08924802069701840),
        }
        lower, upper = frozen[x["visitor_context"]]
        assert abs(x["min_m12_vs_m0_joint_total_variation"]-lower) < 1e-12
        assert abs(x["max_m12_vs_m0_joint_total_variation"]-upper) < 1e-12
        assert x["max_single_trait_distribution_bin_error_across_m"]<1e-12
    assert sum(x["n_sources_with_nonmonotone_TV_across_m3_m6_m12"]
               for x in r["context_summary"])>0


def test_incompatible_locus_grid_and_invalid_joint_probability_rejected():
    original=balanced_source(0)
    changed=balanced_cocarriage(original,0,6)
    c,vis=original_context(original_fixture(),"main",3)
    led=reproduction.reproduce(changed,vis,c)
    a=changed.alleles.copy()
    a[0,2,:]=(.49,.51)
    altered=types.PlantState(
        alleles=a,allele_origin=changed.allele_origin,
        mutation_flags=changed.mutation_flags,
        ids=changed.ids,birth_years=changed.birth_years)
    with pytest.raises(ValueError,match="sixteenth-grid"):
        one_offspring_joint_distribution(altered,led)
    bad=np.zeros((33,33))
    with pytest.raises(ValueError,match="Inadmissible"):
        total_variation(bad,bad)


def test_the_joint_audit_is_analytic_and_never_calls_a_biological_future():
    from scripts import audit_chapter2_full_F1_joint_distribution_20261014 as module
    text=inspect.getsource(module)
    assert "population.advance(" not in text
    assert "population.inherit(" not in text
    assert "model_history(" not in text
    assert "simulate(" not in text
