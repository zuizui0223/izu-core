"""Statewise equal TOTAL pollen: exact negative control, not natural mediation."""
import json
import numpy as np
import pytest

from scripts.audit_chapter2_q3q4_statewise_pollen_equalized_20261011 import (
    STATUS, FRACTIONS, POLICIES, VISITOR_ARMS, SETTINGS, BUDGETS,
    source_equalized, transition, longrun, audit,
)
from scripts.audit_chapter2_q3q4_functional_mismatch_20261011 import (
    states, source, reproductive_source,
)


@pytest.mark.parametrize("frac",FRACTIONS)
@pytest.mark.parametrize("policy",POLICIES)
def test_all_164_living_source_genotypes_equalize_pollen(frac,policy):
    # Do not merely match the founding heterozygote N8 source!
    # Each subsequent census and genotype class must be checked separately.
    for counts in states()[1:]:
        x=source_equalized(counts,"delayed_control",6.,frac,policy)
        assert x["source_census"]==sum(counts)
        assert 0<=x["effectiveness_multiplier"]<=1+1e-12
        assert x["matched_pollen"]>=0
        assert np.isfinite(x["viable_seed_difference"])
        assert x["paternal_q_L1"]>=0
        mu,q=x["shifted4"]
        native_mu,native_q,*_=reproductive_source(
            counts,"delayed_control",6.,frac,policy
        )
        assert mu==pytest.approx(native_mu,abs=1e-11)
        np.testing.assert_allclose(q,native_q,rtol=0,atol=1e-12)
    # The N1/no-outcross 0/0 edge case must not produce NaNs.
    for s in ((1,0,0),(0,1,0),(0,0,1)):
        z=source_equalized(s,"delayed_control",6.,frac,policy)
        assert z["matched_pollen"]==0
        assert z["effectiveness_multiplier"]==1


def test_founder_genomes_first_generation_recruitment_matched_exactly():
    for frac in FRACTIONS:
        for policy in POLICIES:
            x=source_equalized((0,8,0),"delayed_control",6.,frac,policy)
            a=x["shifted4"];b=x["original4_statewise_equal_delivery"]
            assert a[0]==pytest.approx(b[0],abs=1e-11)
            np.testing.assert_allclose(a[1],[.25,.5,.25],atol=1e-12)
            np.testing.assert_allclose(a[1],b[1],atol=1e-12)
            assert abs(x["viable_seed_difference"])<1e-11


@pytest.mark.parametrize("frac",FRACTIONS)
def test_80_year_statewise_equalized_census_kernel_is_stochastic(frac):
    Tshift=transition("delayed_control",6.,frac,"native","shifted4")
    Tequal=transition(
        "delayed_control",6.,frac,"native","original4_statewise_equal_delivery"
    )
    assert Tshift.shape==Tequal.shape==(165,165)
    for T in (Tshift,Tequal):
        assert T[0,0]==1
        assert np.isfinite(T).all()
        assert np.all(T>=0)
        np.testing.assert_allclose(T.sum(axis=1),1.,atol=1e-12,rtol=0)
        result=longrun(T)
        assert 0 < result["P80_occupied"] < 1
        assert 0<=result["P80_low_allele_fixed_and_occupied"]<=result["P80_occupied"]
    # Original shifted arm remains IDENTICAL to merged #468 source model,
    # not a reimplementation with another demographic transition law.
    assert longrun(Tshift)["P80_occupied"]==pytest.approx(
        longrun(transition(
            "delayed_control",6.,frac,"native","shifted4"
        ))["P80_occupied"],abs=1e-13
    )


def test_complete_science_contract_for_source_counterfactual():
    from scripts.audit_chapter2_q3q4_statewise_pollen_equalized_20261011 import SETTINGS,BUDGETS
    assert len(FRACTIONS)*len(SETTINGS)*len(BUDGETS)==24
    assert "NOT a biologically realizable" in " ".join(
        audit()["limitations"]
    )
    d=audit()
    assert d["status"]==STATUS
    assert d["n_source_settings"]==24
    assert d["n_independent_biological_histories"]==0
    assert d["n_visitor_types_each_arm"]==4
    assert d["states_per_operator"]==165
    assert len(d["results"])==24
    for row in d["results"]:
        assert abs(row["founder_seed_difference"])<1e-11
        assert row["founder_total_pollen_equalized"]>=0
        assert 0<=row["founder_effectiveness_multiplier"]<=1
        assert set(row["full_arms"])=={
            p+"|"+v for p in POLICIES for v in VISITOR_ARMS
        }
        assert np.isfinite(row["P80_native_shift_minus_equalized"])
    json.dumps(d,allow_nan=False)


def test_unknown_or_external_conditions_fail_closed():
    with pytest.raises(ValueError):
        source_equalized((0,8,0),"delayed_control",6.,0.,"native")
    with pytest.raises(ValueError):
        source_equalized((0,8,0),"invented",6.,.25,"native")
    with pytest.raises(ValueError):
        transition("delayed_control",6.,.25,"native","invented")
