from pathlib import Path
from types import SimpleNamespace
import hashlib
import importlib.util
import json

import numpy as np
import pytest

SRC=Path(__file__).resolve().parents[1]/'scripts'/'audit_chapter2_clock_t0_reproduction_equivalence_20261013.py'
spec=importlib.util.spec_from_file_location('clock_t0_original',SRC)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


def test_source_reproduction_module_is_exact_biological_version():
    import scripts.model3_island.reproduction as reproduction
    assert m.git_blob_digest(Path(reproduction.__file__))==m.ORIGINAL_NATIVE_REPRO_GIT_BLOB


def test_source_original_birthfree_reproduction_bitwise_invariant_under_hidden_genotypes():
    import scripts.model3_island.reproduction as reproduction
    from scripts.audit_chapter2_clock_factorial_feasibility_20261013 import transform
    a=np.full((48,3,2),.5,dtype=float)
    a[:,1,:]=np.tile([[.375,.625],[.375,.375],[.625,.625],[.5,.5]],(12,1))
    a[:,2,:]=[.4375,.5625]
    state=SimpleNamespace(ids=np.arange(48),alleles=a)
    cfg=SimpleNamespace(capacity=48,assurance_mode='evolving',fixed_assurance=.5,
         ovule_budget=8,investment_cost=.5,assurance_cost=.5,pollen_budget=20,
         pollen_discount=0.,activity=.05,activity_mode='count_scaled',
         reference_visitor_count=4,background_ratio=1.,
         assurance_timing='delayed',pollen_scale=1.,depression=.5)
    vis=SimpleNamespace(ids=np.arange(4),optima=np.full(4,.5),breadths=np.full(4,.2),effectiveness=np.ones(4))
    reference=m.source_ledger(reproduction,state,vis,cfg)
    fingerprint=m.checksum_ledger(reference)
    for width in (.046875,.078125):
        for scale in (0.,1.):
            new,_=transform(a,width,scale)
            after=m.source_ledger(reproduction,SimpleNamespace(ids=state.ids,alleles=new),vis,cfg)
            assert m.checksum_ledger(after)==fingerprint
            for key in m.SOURCE_FIELDS:np.testing.assert_array_equal(after[key],reference[key])


def test_original_readout_admitted_and_all_six_reference_states_in_git():
    p=Path(__file__).resolve().parents[1]/'data/results/chapter2_clock_t0_reproduction_equivalence_20261013.json'
    d=json.loads(p.read_bytes())
    assert d['status']=='SIX_ORIGINAL_SOURCE_STATES_TWENTY_FOUR_GENOTYPE_CONTRAST_LEDGERS_EXACT'
    assert d['original_reproduction_git_blob']==m.ORIGINAL_NATIVE_REPRO_GIT_BLOB
    assert d['genotype_adjusted_fixed_state_ledger_calls']==24
    assert d['original_source_reference_ledger_calls']==6
    assert d['population_advance_called'] is False and d['new_biological_histories']==0
    assert len(d['records'])==24
    assert len({(q['block'],q['original_context']) for q in d['records']})==6
    assert all(q['source_original_ledger_sha256']==q['source_new_ledger_sha256'] for q in d['records'])
    assert d['max_recorded_total_error']<1e-12
    assert {r['context'] for r in d['original_provider_receipts']}=={0,3,4}


def test_changed_original_shard_bytes_rejected(tmp_path):
    for k in (0,3,4):(tmp_path/f'{k}.zip').write_bytes(b'corrupt')
    with pytest.raises(ValueError,match='SHA'):
        m.check({k:tmp_path/f'{k}.zip' for k in (0,3,4)})
