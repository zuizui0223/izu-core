"""Allele-state transplant identity, experiment size, and frozen-failure guards."""
import json
from pathlib import Path
import numpy as np

from scripts.run_chapter2_island_genetic_state_transplant import (
    crossed_state, load_pilot, rank_order
)
from scripts.run_chapter2_island_genetic_state_transplant_independent16 import (
    load_frozen,
)
from scripts.run_chapter2_assurance_generality import founders

ROOT=Path(__file__).resolve().parents[1]


def test_pilot_and_independent_randomization_contracts_are_disjoint():
    d,src=load_pilot()
    assert len(d['history_seeds'])==4
    assert d['n_postshock_trajectories']==512
    protocol,n,source=load_frozen()
    assert len(n['history_seeds'])==16
    assert n['n_postshock_trajectories']==2048
    assert not set(d['history_seeds']).intersection(n['history_seeds'])
    assert set(d['four_settings'])==set(source['settings'])
    assert protocol['expected_genetic_factorial_states']==512
    assert protocol['bootstrap']['unit']=='independent_visitor_history'


def test_native_alleles_and_provenance_are_bitwise_identical():
    _,source=load_pilot()
    state=founders(source)
    # Reorder the founder sample to make a synthetic n=8 recipient.
    from scripts.model3_island.population import subset
    recipient=subset(state,np.arange(8))
    donor=subset(state,np.arange(8,16))
    native=crossed_state(recipient,recipient,recipient)
    for name in ('alleles','allele_origin','mutation_flags','ids','birth_years'):
        assert np.array_equal(getattr(native,name),getattr(recipient,name))
    crossed=crossed_state(recipient,donor,recipient)
    assert np.array_equal(crossed.alleles[:,0,:],recipient.alleles[:,0,:])
    assert np.array_equal(crossed.alleles[:,2,:],recipient.alleles[:,2,:])
    assert np.array_equal(
        crossed.alleles[rank_order(recipient,1),1,:],
        donor.alleles[rank_order(donor,1),1,:]
    )
    assert np.array_equal(
        crossed.allele_origin[rank_order(recipient,1),1,:],
        donor.allele_origin[rank_order(donor,1),1,:]
    )


def test_exploratory_pilot_is_descriptive_and_independent16_gate_failed():
    exploratory=json.loads((
        ROOT/'data/results/chapter2_island_genetic_state_transplant_pilot_20261008.json'
    ).read_text(encoding='utf-8'))
    independent=json.loads((
        ROOT/'data/results/chapter2_island_genetic_state_transplant_independent16_20261008.json'
    ).read_text(encoding='utf-8'))
    assert exploratory['status'].startswith('completed_exploratory')
    assert exploratory['independent_visitor_histories']==4
    assert independent['genetic_factorial_states']==512
    assert independent['poststress_trajectories']==2048
    assert independent['independent_visitor_histories']==16
    assert independent['frozen_primary']['passed'] is False
    assert independent['frozen_primary']['mean']>0
    lo,hi=independent['frozen_primary']['bootstrap95']
    assert lo<0<hi
    assert len(independent['secondary_by_setting_and_background'])==8
    assert len(independent['provenance']['raw_sha256'])==64
    assert independent['provenance']['github_actions_replay'] is False


def test_independent16_positive_secondary_cannot_override_global_failure():
    r=json.loads((
        ROOT/'data/results/chapter2_island_genetic_state_transplant_independent16_20261008.json'
    ).read_text(encoding='utf-8'))
    records={(x['setting'],x['recipient_background']):x
             for x in r['secondary_by_setting_and_background']}
    for setting in ('delayed_control','prior_selfing','pollen_discount'):
        for background in ('near','far'):
            assert records[(setting,background)]['terminal_occupancy'][
                'assurance_effect']['bootstrap95'][0]>0
    # Under direct assurance cost the transplant survival benefit is weak.
    assert records['assurance_cost','near']['terminal_occupancy'][
        'assurance_effect']['bootstrap95'][0]==0
    assert r['frozen_primary']['passed'] is False
