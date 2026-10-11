"""Q3→Q4 original-ledger genomic effects vs demographic effects; source-only."""
import json

import numpy as np
import pytest

from scripts.audit_chapter2_q3q4_exact_genotype_factorial_20261011 import (
    K, B, BUDGETS, STATUS, states, source_ledgers,
    intensity_and_genotype_probabilities, transition, propagate, audit,
)
from scripts.audit_chapter2_exact_clonal_demographic_null import source_viable_mu


def test_165_genotype_census_states_and_original_source_reproduction():
    s = states()
    assert len(s) == 165 == len(set(s))
    assert all(sum(x) <= 8 for x in s)
    original, native, fixed = source_ledgers((0,8,0),6.)
    assert len(original.ids) == 8
    assert np.all(original.alleles[:,1,:] == [0.2,0.5])
    assert np.isclose(native.outcross.sum()+native.self_viable.sum(),
                      8.994424151193341,atol=1e-10)
    assert np.array_equal(native.maternal,fixed.maternal)
    for kind in ('native','fixed_expression'):
        mu,q = intensity_and_genotype_probabilities((0,8,0),6.,kind)
        assert mu == pytest.approx(8.994424151193341,abs=1e-10)
        np.testing.assert_allclose(q,[.25,.5,.25],atol=1e-12)


def test_exact_kernel_and_identical_first_generation_all_four_arms():
    for b in BUDGETS:
        row=None
        for intensity in ('native','fixed_expression'):
            for parents in ('native','fixed_expression'):
                T=transition(b,intensity,parents)
                assert T.shape == (165,165)
                np.testing.assert_allclose(T.sum(axis=1),1.,atol=1e-12,rtol=0)
                assert T[0,0] == 1 and T[0,1:].sum() == 0
                initial = states().index((0,K,0))
                if row is not None:
                    np.testing.assert_allclose(T[initial],row,atol=1e-13,rtol=0)
                row=T[initial].copy()


def test_fixed_mu_is_genotype_independent_census_lumpable():
    for n in range(1,9):
        ref=source_viable_mu(n,8,6.)
        mus=[
            intensity_and_genotype_probabilities(s,6.,'fixed_expression')[0]
            for s in states() if sum(s)==n
        ]
        np.testing.assert_allclose(mus,ref,atol=1e-10,rtol=0)


def test_full_factorial_exact_source_results_and_interaction_boundaries():
    o=audit()
    assert o['status'] == STATUS
    assert o['states'] == 165 and o['K'] == 8 and o['B'] == 48
    assert o['new_stochastic_histories'] == o['new_genetic_trajectories'] == 0
    assert o['independent_confirmation'] is False
    assert len(o['results']) == 3
    rows={r['ovule_budget']:r for r in o['results']}
    base=rows[6.]
    v=base['P80']
    assert v['native|native'] == pytest.approx(.026271826605491617,abs=2e-10)
    assert v['fixed_expression|fixed_expression'] == pytest.approx(.030242646454152422,abs=2e-10)
    assert v['native|fixed_expression'] == pytest.approx(.025887950753339297,abs=2e-10)
    assert v['fixed_expression|native'] == pytest.approx(v['fixed_expression|fixed_expression'],abs=1e-12)
    assert base['native_minus_fixed'] == pytest.approx(-.003970819848658484,abs=2e-10)
    assert base['source_mu_channel_at_fixed_parentage'] == pytest.approx(-.00435469570081087,abs=2e-10)
    assert base['source_parentage_channel_at_fixed_mu'] == pytest.approx(0,abs=1e-12)
    assert base['remaining_channel_interaction'] == pytest.approx(.00038387585215235,abs=2e-10)

    native=base['arms']['native|native']['80']
    neutral=base['arms']['fixed_expression|fixed_expression']['80']
    changed_parentage=base['arms']['fixed_expression|native']['80']
    assert native['P_fixed_low_given_occupied'] == pytest.approx(.62599,abs=1e-5)
    assert neutral['P_fixed_low_given_occupied'] == pytest.approx(
        neutral['P_fixed_high_given_occupied'],abs=1e-12
    )
    assert changed_parentage['P_fixed_low_given_occupied'] > .55
    assert abs(changed_parentage['P_occupied']-neutral['P_occupied'])<1e-12
    assert .000002 < native['P_segregating_given_occupied'] < .000004
    at8=rows[8.]
    assert at8['native_minus_fixed'] == pytest.approx(-.00870066736794317,abs=2e-10)
    assert at8['source_mu_channel_at_fixed_parentage'] < at8['native_minus_fixed']
    assert at8['remaining_channel_interaction'] > 0
    assert rows[4.5]['native_minus_fixed'] > 0
    assert 'NOT natural biological mediation' in o['scientific_limit']
    json.dumps(o,allow_nan=False)


def test_reject_unknown_channels_or_undisclosed_ovule_budget():
    with pytest.raises(ValueError):
        transition(6.,'mutate_genome','native')
    with pytest.raises(ValueError):
        transition(6.1,'native','native')
