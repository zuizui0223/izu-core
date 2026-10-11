"""Protect Q3→Q4 hidden-variance conclusions against allele value/identity conflation."""
import json

import numpy as np
import pytest

from scripts.audit_chapter2_q3q4_genetic_span_20261011 import (
    STATUS, K, B, SETTINGS, BUDGETS, ALLELE_HALF_WIDTHS,
    source_mu_and_q, neutral_p80, matrix, audit,
)


@pytest.mark.parametrize("setting",SETTINGS)
@pytest.mark.parametrize("width",ALLELE_HALF_WIDTHS)
def test_heterozygous_founders_match_their_expression_and_mendelian_identity(setting,width):
    a,qa=source_mu_and_q((0,8,0),width,setting,6.,"native")
    b,qb=source_mu_and_q((0,8,0),width,setting,6.,"fixed_expression")
    assert a == pytest.approx(b,abs=1e-12)
    np.testing.assert_allclose(qa,[.25,.5,.25],rtol=0,atol=1e-12)
    np.testing.assert_allclose(qb,qa,rtol=0,atol=1e-12)


def test_parent_genotype_class_not_allele_numeric_value_defines_transmission():
    for width in ALLELE_HALF_WIDTHS:
        mu,q=source_mu_and_q((0,8,0),width,"delayed_control",6.,"native")
        assert q[1] == pytest.approx(.5,abs=1e-12)
        _,low=source_mu_and_q((8,0,0),width,"delayed_control",6.,"native")
        _,high=source_mu_and_q((0,0,8),width,"delayed_control",6.,"native")
        np.testing.assert_allclose(low,[1,0,0],atol=1e-12)
        np.testing.assert_allclose(high,[0,0,1],atol=1e-12)
    # The previous exploration incorrectly tested allele == 0.5, which
    # silently recoded ALL new 0.30/0.40 alleles as low; here this is impossible.


def test_native_source_original_015_halfwidth_matches_frozen_q3q4():
    r=audit()
    assert r["status"] == STATUS
    assert r["new_stochastic_histories"] == 0
    assert r["independent_confirmatory_evidence"] is False
    assert r["n_source_cells"] == 48
    assert r["state_count"] == 165
    d={(x["setting"],x["ovule_budget"],x["founder_investment_allele_half_width"]):x
       for x in r["results"]}
    reference={
        "delayed_control":(-.0039708198486585,.030242646454152422),
        "prior_selfing":(-.0012237250278442,.0181851921),
        "pollen_discount":(-.0002227736810872,.0148241889),
        "assurance_cost":(-.0005318239237264,.0034364153),
    }
    for setting,(delta,reference_fixed) in reference.items():
        row=d[(setting,6.,.15)]
        assert row["P80_native_minus_fixed"] == pytest.approx(delta,abs=2e-10)
        assert row["P80_fixed_expression"] == pytest.approx(reference_fixed,abs=2e-10)
    assert d[("delayed_control",6.,.05)]["P80_native_minus_fixed"] == pytest.approx(
        -.00047302557,abs=2e-10
    )
    assert d[("prior_selfing",6.,.10)]["P80_native_minus_fixed"] == pytest.approx(
        -.00056293529,abs=2e-10
    )
    assert d[("pollen_discount",6.,.10)]["P80_native_minus_fixed"] == pytest.approx(
        -.00008348911,abs=2e-10
    )
    assert d[("assurance_cost",6.,.05)]["P80_native_minus_fixed"] == pytest.approx(
        -.00006494292,abs=2e-10
    )


def test_all_forty_eight_cells_and_finite_population_floor_are_reported():
    result=audit()
    lookup={(r["setting"],r["ovule_budget"],r["founder_investment_allele_half_width"]):r
            for r in result["results"]}
    assert set(lookup)=={(s,b,w) for s in SETTINGS for b in BUDGETS for w in ALLELE_HALF_WIDTHS}
    for setting in SETTINGS:
        for budget in BUDGETS:
            baseline=lookup[(setting,budget,0.)]
            assert baseline["P80_native_minus_fixed"] == 0.
            assert baseline["founder_allelic_variance"]==0.
            assert baseline["P80_fixed_expression"]==pytest.approx(neutral_p80(setting,budget),abs=1e-13)
            if budget in (6.,8.):
                effects=[lookup[(setting,budget,w)]["P80_native_minus_fixed"] for w in ALLELE_HALF_WIDTHS]
                assert effects[0]==0.
                assert effects[0]>effects[1]>effects[2]>effects[3]
            else:
                for w in ALLELE_HALF_WIDTHS:
                    assert abs(lookup[(setting,budget,w)]["P80_native_minus_fixed"])<2e-9
    assert "INVALID" in result["warning"]
    assert "not natural island" in result["scientific_limit"]
    json.dumps(result,allow_nan=False)


def test_fail_closed_parameters_and_mass_conservation():
    with pytest.raises(ValueError):
        source_mu_and_q((0,8,0),.12,"delayed_control",6.,"native")
    with pytest.raises(ValueError):
        source_mu_and_q((0,8,0),.1,"invented",6.,"native")
    with pytest.raises(ValueError):
        source_mu_and_q((0,8,0),.1,"delayed_control",5.0,"native")
    T=matrix(.05,"delayed_control",6.,"native")
    assert T.shape==(165,165)
    np.testing.assert_allclose(T.sum(axis=1),1.,atol=1e-12,rtol=0)
    assert T[0,0] == 1
