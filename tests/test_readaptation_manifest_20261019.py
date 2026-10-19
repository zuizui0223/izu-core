import copy
import hashlib
import itertools
import json

import pytest

from scripts.readaptation_contract_20261019 import load_contract,canonical
from scripts.audit_readaptation_raw_20261019 import admit_manifest, audit_archive, _audit_files


def manifest():
    c=load_contract()
    cohorts=list(itertools.product(c['founder_indices'],c['visitor_indices'],
                                   c['donor_policies'],range(c['cohort_draws'])))
    keys=[(*k,d,.5,r) for k in cohorts for d in range(5) for r in range(32)]
    m=dict(format='readaptation_manifest_v1',contract_sha256=hashlib.sha256(canonical(c)).hexdigest(),
           cohorts=[dict(key=list(k),cohort_sha256='0'*64) for k in cohorts],
           futures=[dict(key=list(k),file=f'future-{i}.npz',sha256='0'*64,bytes=100)
                    for i,k in enumerate(keys)])
    return c,m


def test_full_inventory_and_cohort_mapping():
    c,m=manifest()
    keys,cohorts=admit_manifest(m,c)
    assert len(keys)==10240 and len(cohorts)==64


@pytest.mark.parametrize('damage',['missing','duplicate','cohort','contract','path','alias'])
def test_inventory_admission_fails_before_file_reads(damage):
    c,m=manifest()
    if damage=='missing': m['futures'].pop()
    elif damage=='duplicate': m['futures'].append(copy.deepcopy(m['futures'][0]))
    elif damage=='cohort': m['cohorts'].pop()
    elif damage=='contract': m['contract_sha256']='f'*64
    elif damage=='path': m['futures'][0]['file']='../elsewhere.npz'
    else: m['futures'][1]['file']=m['futures'][0]['file']
    with pytest.raises(ValueError):
        admit_manifest(m,c)


def test_public_archive_rejects_changed_contract_before_reading(tmp_path):
    c,_=manifest(); c['future_repeats']=1
    with pytest.raises(ValueError,match='contract'):
        audit_archive(tmp_path,c)


def test_streaming_archive_integration_on_empty_synthetic_fixture(tmp_path):
    # Reduced allocation only exercises the internal reader; the public gate
    # rejects this test contract. No scientific source or future is simulated.
    from test_readaptation_futures_20261019 import fixture
    from scripts.readaptation_futures_20261019 import run_future
    from scripts.readaptation_storage_20261019 import save_future
    from scripts.readaptation_contract_20261019 import seed_for, ROOT
    from scripts.readaptation_transfer_20261019 import cohort_digest
    c=load_contract()
    c.update(founder_indices=[0],visitor_indices=[0],donor_policies=['fixed'],
             cohort_draws=1,activity=[.25],optima=[[.5]*6])
    base=json.loads((ROOT/'data/design/model3_island_v2.json').read_text())['base_config']
    state,config,visitors=fixture(0)
    raw=run_future(state,config,visitors,1,80)
    receipts=[]
    for destination in range(2):
        for repeat in range(32):
            key=[0,0,'fixed',0,destination,.5,repeat]
            d=copy.deepcopy(raw)
            d['stream_key']=seed_for(c,'future',key)
            if destination:
                d['config']['activity']=.25
                d['visitors']=dict(ids=list(range(6)),optima=[.5]*6,breadths=[.2]*6,effectiveness=[1.]*6)
            receipts.append(save_future(tmp_path/f'future-{destination}-{repeat}.npz',key,d))
    m=dict(format='readaptation_manifest_v1',contract_sha256=hashlib.sha256(canonical(c)).hexdigest(),
           cohorts=[dict(key=[0,0,'fixed',0],cohort_sha256=cohort_digest(state))],futures=receipts)
    result=_audit_files(tmp_path,m,c,base)
    assert result['allocated']==64 and result['cohorts']==1
    assert result['source_admission'] is False
    assert result['biological_replay'] is False
    assert all(g['occupancy']['count']==0 for g in result['groups'])
    # An extra orphan file is not silently omitted from the inventory.
    (tmp_path/'orphan.npz').write_bytes(b'orphan')
    with pytest.raises(ValueError,match='file inventory'):
        _audit_files(tmp_path,m,c,base)
