import json
from dataclasses import replace
from types import SimpleNamespace

import numpy as np
import pytest

from scripts.model3_island.types import Config, PlantState, VisitorState
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.reproduction import reproduce
from scripts.readaptation_contract_20261019 import ROOT, load_contract
from scripts.readaptation_transfer_20261019 import (
    make_cohort, destination_states, destination_activity, cohort_digest,
)


def synthetic_donor(n=2):
    a=np.full((n,3,2),.2)
    if n>1:
        a[1]=.8
    return PlantState(a,np.arange(n*6).reshape(n,3,2),np.zeros((n,3,2),bool),
                      np.arange(n)+500,np.full(n,80,dtype=int))


def synthetic_config(policy='evolving'):
    c=json.loads((ROOT/'data/design/model3_island_v2.json').read_text())['base_config']
    c.update(assurance_mode=policy,assurance_cost=.5,survival=0,mutation_rate=0,
             activity_mode='fixed',years=80)
    c['visitor_arrival']['supply']=0
    return Config.from_dict(c)


def streams(seed=88):
    return {key:stream(seed,key,0) for key in STREAM_IDS}


def empty_visitors():
    return VisitorState(np.array([],dtype=int),np.array([]),np.array([]),np.array([]))


@pytest.mark.parametrize('n,ovules',[(0,8),(2,0)])
def test_absent_or_seedless_donor_is_retained(n,ovules):
    cohort,receipt=make_cohort(synthetic_donor(n),replace(synthetic_config(),ovule_budget=ovules),
                              empty_visitors(),streams(),[0,0,'evolving',0])
    assert len(cohort.ids)==0
    assert receipt['transferred']==0 and receipt['source_production']==0
    assert receipt['allocated'] is True
    assert cohort.alleles.shape==(0,3,2)


def test_actual_kernel_preserves_diploid_origins_and_entry_clock():
    donor=synthetic_donor()
    a,receipt=make_cohort(donor,synthetic_config(),empty_visitors(),streams(),[0,0,'evolving',0])
    b,again=make_cohort(donor,synthetic_config(),empty_visitors(),streams(),[0,0,'evolving',0])
    assert 0<len(a.ids)<=12
    assert cohort_digest(a)==cohort_digest(b)==receipt['cohort_sha256']
    assert receipt==again
    assert (a.birth_years==0).all()
    assert np.array_equal(a.ids,np.arange(len(a.ids)))
    assert set(a.allele_origin.ravel())<=set(donor.allele_origin.ravel())
    assert set(a.alleles.ravel())<=set(donor.alleles.ravel())
    assert (donor.birth_years==80).all()


def test_raw_cohort_audit_verifies_donor_parentage():
    import copy
    from scripts.audit_readaptation_raw_20261019 import audit_cohort
    donor=synthetic_donor()
    child,receipt=make_cohort(donor,synthetic_config(),empty_visitors(),streams(),[0,0,'evolving',0])
    fields=('alleles','allele_origin','mutation_flags','ids','birth_years')
    source={name:getattr(donor,name) for name in fields}
    offspring={name:getattr(child,name) for name in fields}
    assert audit_cohort(source,offspring,receipt)['transferred']==len(child.ids)
    broken=copy.deepcopy(receipt)
    broken['mother_source_ids'][0]=999999
    with pytest.raises(ValueError):
        audit_cohort(source,offspring,broken)
    broken=copy.deepcopy(receipt); broken['source_production']=0
    with pytest.raises(ValueError):
        audit_cohort(source,offspring,broken)


def test_parent_orientation_and_small_seed_supply(monkeypatch):
    # Independent fixture: only father 1 / mother 0 is possible.
    monkeypatch.setattr('scripts.readaptation_transfer_20261019.reproduce',
                        lambda *args:SimpleNamespace(outcross=np.array([[0.,0.],[10.,0.]]),
                                                     self_viable=np.zeros(2)))
    class ThreeSeeds:
        def poisson(self, total):
            assert total==10
            return 3
    rs=streams(); rs['recruitment']=ThreeSeeds()
    c,r=make_cohort(synthetic_donor(),synthetic_config(),empty_visitors(),rs,[0,0,'evolving',0])
    assert len(c.ids)==3 and r['source_production']==3
    assert np.all(c.alleles[:,:,0]==.2)  # maternal transmission
    assert np.all(c.alleles[:,:,1]==.8)  # paternal transmission
    assert r['mother_source_ids']==[500]*3
    assert r['father_source_ids']==[501]*3
    assert r['parent_probability_matrix']==[[0.,0.],[1.,0.]]


def test_native_fixed_policy_controls_seed_production_not_hidden_A():
    donor=synthetic_donor()
    cfg=synthetic_config('fixed')
    _,r=make_cohort(donor,cfg,empty_visitors(),streams(),[0,0,'fixed',0])
    expected=reproduce(donor,empty_visitors(),cfg).self_viable.sum()
    hidden=reproduce(donor,empty_visitors(),replace(cfg,assurance_mode='evolving')).self_viable.sum()
    assert r['expected_viable_production']==pytest.approx(expected)
    assert expected!=pytest.approx(hidden)
    assert r['donor_assurance_mode']=='fixed'


def test_five_destinations_preserve_cohort_and_visitor_id_invariance():
    contract=load_contract()
    destinations=destination_states(contract)
    assert list(destinations)==['none','a0_m0','a0_m1','a1_m0','a1_m1']
    donor=synthetic_donor(); before=cohort_digest(donor)
    for key,v in destinations.items():
        assert len(v.ids)==(0 if key=='none' else 6)
        cfg=replace(synthetic_config(),activity=destination_activity(key,contract))
        r=reproduce(donor,v,cfg)
        changed=reproduce(donor,replace(v,ids=v.ids+1000),cfg)
        assert np.array_equal(r.delivered,changed.delivered)
        assert cohort_digest(donor)==before
    assert destination_activity('a0_m1',contract)==.25
    assert destination_activity('a1_m0',contract)==1
    assert np.all(destinations['a0_m0'].optima==.5)
    assert np.all(destinations['a0_m1'].optima==.7)
    with pytest.raises(ValueError):
        destination_activity('a99_m0',contract)


def test_changed_alleles_change_cohort_identity():
    donor=synthetic_donor()
    changed=replace(donor,alleles=donor.alleles+.01)
    assert cohort_digest(donor)!=cohort_digest(changed)


def test_high_production_is_capped_after_the_source_draw():
    cfg=replace(synthetic_config(),ovule_budget=1000)
    cohort,receipt=make_cohort(synthetic_donor(),cfg,empty_visitors(),streams(),
                              [0,0,'evolving',0])
    assert receipt['source_production']>12
    assert receipt['transferred']==len(cohort.ids)==12
