"""Synthetic checks of common-context genetic return, not scientific futures."""
import json
from dataclasses import replace
from types import SimpleNamespace

import numpy as np
import pytest

from scripts.model3_island.types import Config, PlantState, VisitorState
from scripts.readaptation_contract_20261019 import ROOT
from scripts.readaptation_transfer_20261019 import cohort_digest
from scripts.readaptation_assay_20261019 import assay_population


def fixture(n=2):
    alleles=np.full((n,3,2),.5)
    state=PlantState(alleles,np.zeros((n,3,2),dtype=int),
                     np.zeros((n,3,2),dtype=bool),np.arange(n),np.zeros(n,dtype=int))
    raw=json.loads((ROOT/'data/design/model3_island_v2.json').read_text())['base_config']
    raw.update(capacity=48,assurance_mode='evolving',assurance_cost=.5,
               assurance_timing='delayed',depression=.5,ovule_budget=8,
               investment_cost=0,activity_mode='fixed')
    visitors=VisitorState(np.empty(0,dtype=int),np.empty(0),np.empty(0),np.empty(0))
    return state,Config.from_dict(raw),visitors


def test_native_self_only_hand_calculation_and_repeatability():
    state,config,visitors=fixture()
    before=cohort_digest(state)
    result=assay_population(state,config,visitors)
    expected=8*np.exp(-.5*.5**2)*.5*(1-.5)
    assert result['mean_genetic_return']==pytest.approx(expected)
    assert result['maternal_outcross']==[0.,0.]
    assert result['paternal_outcross']==[0.,0.]
    assert result['viable_self']==pytest.approx([expected]*2)
    assert result==assay_population(state,config,visitors)
    assert result['mean_genetic_return']-assay_population(state,config,visitors)['mean_genetic_return']==0
    assert cohort_digest(state)==before


def test_full_paternal_return_and_fixed_reference_context(monkeypatch):
    state,config,visitors=fixture()
    calls=[]
    def ledger(context, observed_visitors, observed_config):
        assert len(context.ids)==48 and len(set(context.ids))==48
        assert np.all(context.alleles[1:]==.5)
        assert observed_visitors is visitors and observed_config is config
        calls.append(context.alleles[0].copy())
        outcross=np.zeros((48,48))
        outcross[1,0]=2  # mother focal
        outcross[0,1]=6  # father focal
        own=np.zeros(48); own[0]=3
        return SimpleNamespace(outcross=outcross,self_viable=own)
    monkeypatch.setattr('scripts.readaptation_assay_20261019.reproduce',ledger)
    result=assay_population(state,config,visitors)
    assert len(calls)==2
    assert result['genetic_return']==[7.,7.]
    assert result['maternal_outcross']==[2.,2.]
    assert result['paternal_outcross']==[6.,6.]


def test_empty_population_is_undefined_not_zero(monkeypatch):
    state,config,visitors=fixture(0)
    def forbidden(*args):
        raise AssertionError('empty population must not be assayed')
    monkeypatch.setattr('scripts.readaptation_assay_20261019.reproduce',forbidden)
    result=assay_population(state,config,visitors)
    assert result['occupied'] is False
    assert result['mean_genetic_return'] is None
    assert result['genetic_return']==[]
    json.dumps(result,allow_nan=False)


@pytest.mark.parametrize('change',[{'capacity':49},{'assurance_mode':'fixed'}])
def test_rejects_changed_assay_context(change):
    state,config,visitors=fixture()
    with pytest.raises(ValueError):
        assay_population(state,replace(config,**change),visitors)
