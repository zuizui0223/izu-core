"""Deterministic checks, no sampled populations or new evolutionary runs."""
from decimal import Decimal, localcontext
import itertools
import json
from pathlib import Path

import numpy as np
import pytest
from scipy.stats import poisson

from scripts.audit_chapter2_demographic_ceiling_20261018 import (
    birth_rate, transition, extinction_probability, replacement_interval,
    diagnose, SOURCE,
)


def test_source_derived_scalar_law_and_resource_scaling():
    for a, i, q in itertools.product((.25, .5, .75), (.375, .5, .625), (0., .2, 1.)):
        expected=8*np.exp(-.5*i*i-.5*a*a)*(q+.5*a*(1-q))
        assert birth_rate(8, i, a, q=q)==pytest.approx(expected, rel=1e-14)
        assert birth_rate(4.5, i, a, q=q)==pytest.approx(expected*4.5/8, rel=1e-14)
    assert birth_rate(8, .625, .5)==pytest.approx(1.4518443019048164)
    with pytest.raises(ValueError): birth_rate(8, .625, float('nan'))
    with pytest.raises(ValueError): birth_rate(8, .625, .5, q=1.1)


def test_kernel_absorbing_state_mass_and_independent_poisson_reference():
    p=transition(1.2, 4)
    np.testing.assert_allclose(p.sum(1),1,atol=1e-14)
    np.testing.assert_array_equal(p[0], [1,0,0,0,0])
    for n in range(1,5):
        np.testing.assert_allclose(p[n,:4],poisson.pmf(np.arange(4),1.2*n),rtol=1e-13)
        assert p[n,4]==pytest.approx(poisson.sf(3,1.2*n))
    # Larger current populations stochastically dominate smaller ones.
    assert np.all(np.diff(p.cumsum(1),axis=0)<=1e-13)
    with pytest.raises(ValueError): transition(1.2,0)


def test_finite_time_absorption_matches_all_tiny_paths_and_monotonicity():
    p=transition(.9,2)
    brute=sum(p[2,x]*p[x,y]*p[y,0] for x,y in itertools.product(range(3), repeat=2))
    assert extinction_probability(.9,2,3)==pytest.approx(brute)
    assert extinction_probability(.9,2,0)==0
    assert extinction_probability(.9,2,3,initial=0)==1
    assert extinction_probability(0,2,1)==1
    assert extinction_probability(1.5,4,10)<extinction_probability(.8,4,10)
    assert extinction_probability(.8,4,10)<extinction_probability(.8,4,20)
    with pytest.raises(ValueError): extinction_probability(.9,2,-1)


def test_80_update_fixed_A_bound_against_70_digit_decimal_recursion():
    # Independent probability arithmetic: Decimal exp, recursive Poisson PMF,
    # no scipy, random generator, inherited state or source review helper.
    with localcontext() as ctx:
        ctx.prec=70
        k=48
        rate=Decimal(2)*(-Decimal('0.3203125')).exp()
        kernel=[]
        for n in range(k+1):
            mu=rate*n
            pmf=[(-mu).exp()]
            for j in range(1,k): pmf.append(pmf[-1]*mu/j)
            kernel.append(pmf+[1-sum(pmf)])
        mass=[Decimal(0)]*(k+1);mass[k]=Decimal(1)
        for _ in range(80):
            mass=[sum(mass[n]*kernel[n][j] for n in range(k+1)) for j in range(k+1)]
        independent=float(mass[0])
    result=extinction_probability(birth_rate(8,.625,.5),48,80)
    assert result==pytest.approx(independent,rel=1e-10,abs=0)
    assert 1e-15<result<2e-15


def test_resource_window_separates_diagnostic_genotypes_across_all_allowed_I():
    lo,hi=replacement_interval(.375,.625,.5,.75)
    assert lo==pytest.approx(4.29474315626682)
    assert hi==pytest.approx(4.8627633220821895)
    assert lo<4.5<hi
    for i in np.linspace(.375,.625,51):
        assert birth_rate(4.5,i,.5)<1
        assert birth_rate(4.5,i,.75)>1
    with pytest.raises(ValueError): replacement_interval(.9,.1,.5,.75)
    with pytest.raises(ValueError): replacement_interval(.375,.625,.75,.5)


def test_diagnostic_guardrails_no_hidden_simulation_or_confirmation(monkeypatch):
    def forbidden(*a,**k): raise AssertionError('no RNG allowed')
    monkeypatch.setattr(np.random,'default_rng',forbidden)
    data=json.loads(SOURCE.read_text())
    x=diagnose(data)
    assert x['new_biological_histories']==0
    assert x['future_confirmation_authorized'] is False
    assert x['source_counts']['living_at_t80']==144
    assert x['fixed_arm_ceiling']['maximum_possible_positive_survival_policy_effect']<2e-15
    assert x['fixed_arm_ceiling']['upper_probability_extinction_by_t80']<2e-15
    assert x['post_pilot_resource_proposal']['status']=='PROPOSED_MECHANISTIC_COMPANION_NOT_REGISTERED_OR_EXECUTED'
    assert all(row['not_evolved_arm_effect_estimate'] for row in x['fixed_trait_45_update_reference_chains'])
    data['design']['no_mutation_all_three_loci']=False
    with pytest.raises(ValueError,match='closed'): diagnose(data)
