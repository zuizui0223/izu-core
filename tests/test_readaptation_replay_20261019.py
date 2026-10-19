import copy

import pytest

from scripts.readaptation_contract_20261019 import load_contract,seed_for
from scripts.readaptation_replay_20261019 import replay_cohort,replay_future


@pytest.mark.parametrize('policy',['fixed','evolving'])
def test_cohort_native_replay_and_altered_probability(policy):
    from test_readaptation_transfer_20261019 import synthetic_donor,synthetic_config,empty_visitors,streams
    from scripts.readaptation_transfer_20261019 import make_cohort,STATE_FIELDS
    c=load_contract(); key=[0,0,policy,0]; seed=seed_for(c,'cohort',key)
    donor=synthetic_donor(); config=synthetic_config(policy); visitors=empty_visitors()
    child,receipt=make_cohort(donor,config,visitors,streams(seed),key)
    saved={name:getattr(child,name) for name in STATE_FIELDS}
    saved.update(receipt=receipt,stream_key=seed)
    result=replay_cohort(saved,donor,config,visitors,c,key)
    assert result['independent_biological_implementation'] is False
    assert result['status']=='PASS_SAME_IMPLEMENTATION_REPLAY'
    broken=copy.deepcopy(saved)
    broken['receipt']['expected_viable_production']+=.01
    with pytest.raises(ValueError,match='replay'):
        replay_cohort(broken,donor,config,visitors,c,key)


def test_future_byte_replay_and_altered_assay():
    from test_readaptation_futures_20261019 import fixture
    from scripts.readaptation_futures_20261019 import run_future
    c=load_contract(); key=[0,0,'fixed',0,0,.5,0]
    state,config,visitors=fixture()
    saved=run_future(state,config,visitors,seed_for(c,'future',key),80)
    result=replay_future(saved,state,config,visitors,c,key)
    assert result['updates']==80
    assert result['independent_biological_implementation'] is False
    broken=copy.deepcopy(saved)
    broken['assays']['0']['maternal_outcross'][0]+=.02
    broken['assays']['0']['genetic_return'][0]+=.01
    broken['assays']['0']['mean_genetic_return']+=.01/len(state.ids)
    with pytest.raises(ValueError,match='replay'):
        replay_future(broken,state,config,visitors,c,key)


def test_replay_rejects_wrong_stream_instead_of_adopting_it():
    from test_readaptation_futures_20261019 import fixture
    from scripts.readaptation_futures_20261019 import run_future
    c=load_contract(); key=[0,0,'fixed',0,0,.5,0]
    state,config,visitors=fixture(0)
    saved=run_future(state,config,visitors,1,80)
    with pytest.raises(ValueError,match='stream'):
        replay_future(saved,state,config,visitors,c,key)
