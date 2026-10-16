"""Compact shard axis admission; no simulations or historical output changes."""
import json
import numpy as np
import pytest
from scripts.audit_chapter2_finite_history_signal import _load,PAIRS

@pytest.fixture
def shards(tmp_path):
    arms=[arm for pair in PAIRS.values() for arm in pair]
    for shard in range(16):
        values={}
        for arm in arms:
            value=2. if arm in {pair[1] for pair in PAIRS.values()} else 1.
            for mode in ('individual','density'):values[arm+'|'+mode]=np.full((3,8,8),value).tolist()
        doc=dict(status='complete_verified_shard_export',history_seeds=list(range(shard*8,(shard+1)*8)),starts=[.2,.5,.8],demographic_seeds=list(range(8)),arms=arms,values=values)
        (tmp_path/f'shard-{shard:02d}.json').write_text(json.dumps(doc))
    return tmp_path

def test_complete_shards_keep_far_minus_near_orientation(shards):
    h,s,d,values=_load(shards)
    assert len(h)==128 and s==[.2,.5,.8] and d==list(range(8))
    for near,far in PAIRS.values():np.testing.assert_array_equal(values[far+'|individual']-values[near+'|individual'],np.ones((3,128,8)))

@pytest.mark.parametrize('field',['starts','demographic_seeds','arms'])
def test_reordered_axis_rejected(shards,field):
    p=shards/'shard-01.json';doc=json.loads(p.read_text());doc[field].reverse();p.write_text(json.dumps(doc))
    with pytest.raises(ValueError,match='axes'):_load(shards)

@pytest.mark.parametrize('mutation',['missing','extra'])
def test_tensor_inventory_rejected(shards,mutation):
    p=shards/'shard-01.json';doc=json.loads(p.read_text())
    if mutation=='missing':doc['values'].pop('near|individual')
    else:doc['values']['unknown|individual']=doc['values']['near|individual']
    p.write_text(json.dumps(doc))
    with pytest.raises(ValueError,match='tensor'):_load(shards)
