"""Real original typed Model3 birth/ancestry/mutation/advance technical checks.

No prospective cohort or historical scientific comparison is initiated by pytest.
"""
from __future__ import annotations
import copy
from pathlib import Path
import sys

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1] if (ROOT.parents[1]/'scripts/model3_island').exists() else ROOT
if str(REPOSITORY) not in sys.path:
    sys.path.insert(0,str(REPOSITORY))

from scripts.audit_chapter2_clock_native_birth_technical_20261013 import (
    TECHNICAL_UPDATES, TECHNICAL_REPEATS, FOUNDER_BLOCKS, CONTEXTS,
    A_HALF_WIDTHS, I_HOMOLOG_SCALE, FROZEN_SOURCE_GIT_BLOBS, MUTATION_MASK,
    audit, decode_array, source_fixture, ledger_reference, load_original_source,
    initial_state, visitor_and_config, technical_case, technical_seed,
    compare_child_genetics, streams, FIXTURE_PATH,
)


def test_exact_original_source_biology_and_complete_t0_typed_fixture():
    modules=load_original_source()
    f=source_fixture()
    reference=ledger_reference()
    assert set(reference)=={(b,c) for b in FOUNDER_BLOCKS for c in CONTEXTS}
    assert len(FROZEN_SOURCE_GIT_BLOBS)==5
    for block in FOUNDER_BLOCKS:
        original=f['original_founders'][block]['source_state_arrays']
        ids=decode_array(original['ids'])
        assert ids.shape==(48,) and ids.dtype.kind=='i'
        for w in A_HALF_WIDTHS:
            for h in I_HOMOLOG_SCALE:
                state,summary=initial_state(f,block,w,h,modules)
                assert state.alleles.shape==(48,3,2)
                assert summary['I_individual_expressed_traits_all_preserved']
                assert np.array_equal(state.alleles[:,2,:],np.tile([.5-w,.5+w],(48,1)))
                assert np.array_equal(state.alleles[:,1,:].mean(axis=1),
                                      decode_array(original['alleles'])[:,1,:].mean(axis=1))


def test_technical_stream_is_nested_paired_but_disjoint_from_original_history():
    assert len({technical_seed(b,r) for b in FOUNDER_BLOCKS for r in TECHNICAL_REPEATS})==4
    assert MUTATION_MASK==(False,False,True)
    assert TECHNICAL_UPDATES==3
    for block in FOUNDER_BLOCKS:
        assert technical_seed(block,0)!=technical_seed(block,1)
        assert technical_seed(block,0)>0


def test_native_original_48_technical_paths_and_independent_birth_only_replay():
    # Total 2 founder * 2 technical streams * 3 contexts * 4 genotype states.
    result=audit()
    assert result['status']=='ORIGINAL_SOURCE_48_TECHNICAL_FIXTURES_REPLAYED_NOT_BIOLOGICAL_COHORT'
    assert result['technical_cases']==48
    assert result['technical_updates']==144
    assert result['native_replay_checks']==144
    assert result['new_pilot_cases']==0
    assert len(result['cases'])==48
    assert len({(x['block'],x['context'],x['A_width'],x['I_homolog_scale'],x['technical_repeat']) for x in result['cases']})==48
    for case in result['cases']:
        assert len(case['rows'])==3
        assert len({r['update'] for r in case['rows']})==3
        assert all(r['birth_only_replay_exact'] and r['original_parent_pairs_valid'] for r in case['rows'])
        assert all(0 <= r['next_n']<=48 and r['birth_A_mutated_homologs']>=0 for r in case['rows'])
        assert case['seed_master']==str(technical_seed(case['block'],case['technical_repeat']))
    for block in FOUNDER_BLOCKS:
        for repeat in TECHNICAL_REPEATS:
            group=[x for x in result['cases'] if x['block']==block and x['technical_repeat']==repeat]
            assert len(group)==12
            assert len({x['seed_master'] for x in group})==1
            assert len({x['initial_state_sha256'] for x in group})==4
            assert all(x['rows'][0]['source_n']==48 for x in group)


def test_native_birth_rejects_inconsistent_recorded_parent_identity():
    modules=load_original_source();f=source_fixture()
    state,_=initial_state(f,'main',A_HALF_WIDTHS[0],I_HOMOLOG_SCALE[0],modules)
    cfg,vis,_=visitor_and_config(f,'main',0,modules)
    pop=modules['population'];repro=modules['reproduction'];rng=streams('main',0,modules)
    empty=pop.subset(state,np.empty(0,dtype=int))
    ledger=repro.reproduce(state,vis,cfg)
    segreg=copy.deepcopy(rng['segregation']);mut=copy.deepcopy(rng['mutation'])
    child,info=pop.advance(state,ledger,empty,cfg,rng,year=0,mutation_traits=MUTATION_MASK)
    tampered=dict(info)
    tampered['parentage']=np.asarray(info['parentage']).copy()
    assert len(child.ids)>0
    tampered['parentage'][0,1]=999999999
    with pytest.raises(ValueError,match='parentage points to unregistered source'):
        compare_child_genetics(state,child,tampered,modules,cfg,segreg,mut,0)


def test_source_fixture_modification_or_array_bytes_fail_closed(tmp_path):
    original=FIXTURE_PATH.read_bytes()
    p=tmp_path/'fixture.json'
    p.write_bytes(original+b' ')
    with pytest.raises(ValueError,match='Git blob drift'):
        source_fixture(p)
    f=source_fixture()
    item=copy.deepcopy(f['original_founders']['main']['source_state_arrays']['alleles'])
    item['data_b64']=item['data_b64'][:-4]+'AAAA'
    with pytest.raises(ValueError,match='field array changed'):
        decode_array(item)


def test_source_mutation_package_drift_rejected(monkeypatch):
    from scripts import audit_chapter2_clock_native_birth_technical_20261013 as technical
    monkeypatch.setitem(technical.FROZEN_SOURCE_GIT_BLOBS,'population.py','0'*40)
    with pytest.raises(ValueError,match='original model source Git blob mismatch|Original model source Git blob mismatch'):
        technical.load_original_source()