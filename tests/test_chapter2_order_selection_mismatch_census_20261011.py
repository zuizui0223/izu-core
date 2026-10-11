"""Full parental W local gradient sign: density versus functional mismatch."""
import json
import numpy as np
import pytest

from scripts.audit_chapter2_order_selection_mismatch_census_20261011 import (
    STATUS, N_VALUES, TIMINGS, ASSURANCE_COSTS, FRACTIONS, STEPS,
    plants, source_config, visitor_state, genetic_return, perturb,
    gradient, audit
)


def test_native_original_48_genome_clones_and_four_functional_visitors():
    for n in N_VALUES:
        pop=plants(n)
        assert pop.alleles.shape==(n,3,2)
        np.testing.assert_allclose(pop.alleles[:,0,:],.2)
        np.testing.assert_allclose(pop.alleles[:,1,:],.35)
        np.testing.assert_allclose(pop.alleles[:,2,:],.35)
    for fraction in FRACTIONS:
        v=visitor_state(fraction)
        assert len(v.ids)==4
        np.testing.assert_allclose(v.breadths,.18)
        np.testing.assert_allclose(v.effectiveness,1.)
    with pytest.raises(ValueError):
        visitor_state(.17)


@pytest.mark.parametrize("timing",TIMINGS)
@pytest.mark.parametrize("cost",ASSURANCE_COSTS)
def test_investment_source_gradient_sign_depends_on_census_and_matching(timing,cost):
    # The historically interesting result is NOT "assurance always first";
    # N8 can already have both assurance upselection and investment downselection.
    for n in N_VALUES:
        start=gradient(n,timing,cost,0.,"investment",.0025)
        end=gradient(n,timing,cost,1.,"investment",.0025)
        assert end < -.30
        if n==8:assert start< -.03
        else:assert start>.10
        assurance_start=gradient(n,timing,cost,0.,"assurance",.0025)
        assurance_end=gradient(n,timing,cost,1.,"assurance",.0025)
        assert assurance_start>.8
        assert assurance_end>.8
    for n in (24,48):
        assert gradient(n,timing,cost,.25,"investment",.0025)>.03
        assert gradient(n,timing,cost,.5,"investment",.0025)<-.15


def test_original_male_female_selfing_consistency_and_numeric_reference():
    n=48; cfg=source_config("delayed",0.)
    w=genetic_return(plants(n),visitor_state(0.),cfg)
    assert w["group_seed"]>0
    assert w["W"] == pytest.approx(
        .5*(w["F"]+w["P"])+w["S"],abs=1e-12
    )
    assert gradient(48,"delayed",0.,0.,"investment",.0025)==pytest.approx(
        .5840,abs=.0005
    )
    assert gradient(48,"delayed",0.,.5,"investment",.0025)==pytest.approx(
        -.1933,abs=.0005
    )
    assert gradient(8,"delayed",0.,0.,"investment",.0025)==pytest.approx(
        -.063174,abs=.0004
    )
    assert gradient(48,"delayed",.5,0.,"assurance",.0025)==pytest.approx(
        1.1934,abs=.0005
    )


def test_all_60_finite_source_cells_and_factorial_claim_boundary():
    r=audit()
    assert r["status"]==STATUS
    assert r["n_cells"]==len(N_VALUES)*len(TIMINGS)*len(ASSURANCE_COSTS)*len(FRACTIONS)==60
    assert r["n_independent_natural_islands"]==0
    assert r["n_new_evolutionary_histories"]==0
    assert len(r["by_source_factorial"])==len(N_VALUES)*len(TIMINGS)*len(ASSURANCE_COSTS)
    assert all(row["visitor_functional_types"]==4 for row in r["rows"])
    assert all(row["focal_selection"]["assurance"]["status"]=="positive" for row in r["rows"])
    assert all(row["focal_selection"]["investment"]["status"] in ("positive","negative","near_zero")
               for row in r["rows"])
    for f in r["by_source_factorial"]:
        if f["n_adults"]==8:
            assert f["investment_sign_path"]==["negative"]*5
            assert f["positive_to_negative_between_tested_steps"] is False
        else:
            assert f["positive_to_negative_between_tested_steps"] is True
            assert f["first_analysed_mismatch_step_with_negative_investment_gradient"]==.5
    assert "NOT separate islands" in " ".join(r["notes"])
    json.dumps(r,allow_nan=False)


def test_source_gradient_refinement_and_invalid_settings():
    for n in N_VALUES:
        for trait in ("investment","assurance"):
            a=gradient(n,"delayed",.5,.25,trait,.005)
            b=gradient(n,"delayed",.5,.25,trait,.0025)
            assert abs(a-b)<.02
    with pytest.raises(ValueError):plants(9)
    with pytest.raises(ValueError):source_config("invented",0.)
    with pytest.raises(ValueError):source_config("prior",.2)
    with pytest.raises(ValueError):gradient(48,"delayed",0.,0.,"investment",.02)
    with pytest.raises(ValueError):perturb(plants(8),"foo",.005)
