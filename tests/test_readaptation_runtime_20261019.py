import json

import pytest

from scripts.readaptation_runtime_20261019 import resource_gate, complete_future, ResourceStop
from scripts.readaptation_contract_20261019 import ROOT,load_contract,seed_for
from scripts.readaptation_transfer_20261019 import cohort_digest


@pytest.mark.parametrize('memory,disk,used',[(2**30-1,20*2**30,0),
                                          (2**30,10*2**30-1,0),
                                          (2**30,20*2**30,8*2**30)])
def test_resource_shortage_stops_without_work(tmp_path,monkeypatch,memory,disk,used):
    monkeypatch.setattr('scripts.readaptation_runtime_20261019.measure_resources',
                        lambda p:dict(available_memory=memory,free_disk=disk))
    with pytest.raises(ResourceStop):
        resource_gate(tmp_path,used)
    assert not list(tmp_path.iterdir())


def test_checkpoint_resume_never_reexecutes_completed_future(tmp_path,monkeypatch):
    from test_readaptation_futures_20261019 import fixture
    from scripts.readaptation_futures_20261019 import run_future
    monkeypatch.setattr('scripts.readaptation_runtime_20261019.measure_resources',
                        lambda p:dict(available_memory=2*2**30,free_disk=20*2**30))
    state,config,visitors=fixture(0)
    contract=load_contract(); key=[0,0,'fixed',0,0,.5,0]
    base=json.loads((ROOT/'data/design/model3_island_v2.json').read_text())['base_config']
    path=tmp_path/'future-0.npz'; calls=[]
    def produce():
        calls.append(1)
        return run_future(state,config,visitors,seed_for(contract,'future',key),80)
    first=complete_future(path,key,contract,base,cohort_digest(state),0,produce)
    assert first['state']=='created' and len(calls)==1
    second=complete_future(path,key,contract,base,cohort_digest(state),first['added_bytes'],produce,
                           receipt=first['receipt'])
    assert second['state']=='resumed' and second['added_bytes']==0 and len(calls)==1
    # Crash after atomic file publication but before a manifest write.
    recovered=complete_future(path,key,contract,base,cohort_digest(state),first['added_bytes'],produce)
    assert recovered['state']=='recovered' and len(calls)==1
    assert recovered['receipt']==first['receipt']
    path.write_bytes(b'corrupted')
    with pytest.raises(ValueError):
        complete_future(path,key,contract,base,cohort_digest(state),first['added_bytes'],produce,
                        receipt=first['receipt'])
    assert len(calls)==1 and path.read_bytes()==b'corrupted'


def test_missing_receipted_checkpoint_is_not_silently_rerun(tmp_path):
    with pytest.raises(ValueError,match='missing'):
        complete_future(tmp_path/'missing.npz',[],{}, {},'0'*64,0,
                        lambda:pytest.fail('must not rerun'),receipt={'file':'missing.npz'})
