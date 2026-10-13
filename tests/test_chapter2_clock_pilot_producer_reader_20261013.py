"""Short, disjoint technical pilot producer/reader gate; NO 200-update cases."""
from __future__ import annotations
import io
import json
import zipfile
import hashlib
import numpy as np
import pytest

from scripts.run_chapter2_clock_factorial_pilot_20261013 import (
    load_input_inventory,job_cases,simulate,saved_events,
    FULL_HORIZON, TECH_HORIZON, produce,
)
from scripts.read_chapter2_clock_factorial_pilot_20261013 import (
    one_events, decode_case, admit,
)
from scripts.audit_chapter2_clock_native_birth_technical_20261013 import (
    load_original_source,source_fixture,
)


def test_six_shards_exactly256_original_cases_and_technical_salt_distinct():
    registry=load_input_inventory()
    full=[r for k in range(6) for r in job_cases(registry,k)]
    assert len(full)==1536
    assert {r['key'] for r in full}==set(registry['pilot_case_keys'])
    assert len({(r['block'],r['replicate']) for r in full})==128
    for shard in range(6):
        tasks=job_cases(registry,shard)
        tech=job_cases(registry,shard,technical=True)
        assert len(tasks)==256 and len(tech)==4
        assert all(r['replicate']==0 for r in tech)
        assert all(r['master']!=tasks[[z['key'] for z in tasks].index(r['key'])]['master'] for r in tech)
        assert {(r['width'],r['hidden']) for r in tech}=={(.046875,0.),(.046875,1.),(.078125,0.),(.078125,1.)}
    with pytest.raises(ValueError,match='shard'):
        job_cases(registry,6)


def six_class_fixture(A,I,extinction=None):
    means=np.empty((201,3),float);means[:]=[.5,.5,.5]
    if A is not None:means[A:,2]=.61
    if I is not None:means[I:,1]=.39
    pop=np.full(201,48,dtype=int)
    if extinction is not None:
        pop[extinction:]=0
        means[extinction:]=np.nan
    return means,pop


@pytest.mark.parametrize('A,I,expected',[
    (10,30,'assurance_first'),(30,10,'investment_first'),
    (10,12,'near_simultaneous'),(10,None,'assurance_only'),
    (None,10,'investment_only'),(None,None,'neither'),
])
def test_producer_and_independent_reader_retain_six_original_outcome_classes(A,I,expected):
    means,n=six_class_fixture(A,I)
    first=saved_events(means,n,.05);independent=one_events(means,n,.05)
    assert first==independent and first['category']==expected


def test_extinction_is_missing_not_zero_and_never_recolonizes():
    means,n=six_class_fixture(15,20,extinction=31)
    assert saved_events(means,n,.05)==one_events(means,n,.05)
    means[-1]=[0,0,0];n[-1]=48
    with pytest.raises(ValueError,match='Invalid recolonization'):
        saved_events(means,n,.05)


def test_native_birth_short_pilot_smoke_uses_original_model_but_new_seed():
    registry=load_input_inventory()
    fixture=source_fixture()
    modules=load_original_source()
    first=job_cases(registry,3,technical=True)[0]
    arrays,metadata,geometry=simulate(first,registry,fixture,modules,TECH_HORIZON)
    replay,other,other_geo=simulate(first,registry,fixture,modules,TECH_HORIZON)
    assert metadata==other and geometry==other_geo
    assert arrays.keys()==replay.keys()
    for k in arrays:np.testing.assert_array_equal(arrays[k],replay[k])
    assert arrays['population'].shape==(4,) and arrays['population'][0]==48
    assert arrays['means'].shape==(4,3) and arrays['returns'].shape==(3,8)
    assert arrays['sexual_selection'].shape==(3,3,3)
    assert arrays['parentage'].shape[1]==3
    assert metadata['mutation_traits']==[False,False,True]
    assert metadata['technical']
    assert FULL_HORIZON==200 and TECH_HORIZON==3


def test_invalid_output_is_refused_before_full_pilot(monkeypatch,tmp_path):
    path=tmp_path/'existing'
    path.mkdir()
    with pytest.raises(ValueError,match='original NumPy 2.2.6|output directory'):
        # Never run biological cases from this test, only verify fail-closed.
        produce(0,path,technical=False)


def test_registered_task_key_decoder_refuses_unregistered_levels():
    assert decode_case('main_c0_w24_i0_r000')['context']==0
    with pytest.raises(ValueError,match='Bad source-registered'):
        decode_case('main_c1_w24_i0_r000')
    with pytest.raises(ValueError,match='Bad source-registered'):
        decode_case('main_c0_w33_i0_r000')


@pytest.fixture(scope='module')
def source_technical_zip(tmp_path_factory):
    # Run only four original Model3 technical fixtures x3 updates, with a
    # separate technical RNG. Zero full 200-update pilot histories.
    root=tmp_path_factory.mktemp('native_pilot_technical')
    output=root/'technical-original'
    r=produce(0,output,technical=True)
    assert r['status']=='TECHNICAL_ONLY_CLOCK_FACTORIAL_SHARD'
    assert r['cases']==4 and r['updates']==12
    archive=root/'technical-provider.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for path in sorted(output.iterdir()):z.write(path,path.name)
    return archive


def test_independent_reader_reproduces_every_native_parent_and_allele_in_technical_provider(source_technical_zip):
    # Reader shares only original native operator, never imports the producer
    # or its event definitions. It sees all five copied birth fields.
    r=admit(0,source_technical_zip,technical=True)
    assert r['status']=='TECHNICAL_FOUR_CASES_ORIGINAL_BIRTHS_ADMITTED'
    assert r['technical_only'] and r['cases']==4 and r['updates']==12
    assert r['reproductive_checks']==12 and r['birth_parent_checks']==12
    assert r['source_field_checks']==4*4*5
    assert r['category_counts']=={name:0 for name in (
        'assurance_first','investment_first','near_simultaneous',
        'assurance_only','investment_only','neither')}
    assert r['new_biological_histories_generated_by_reader']==0


def test_rehashed_parentage_corruption_is_still_rejected_by_native_replay(source_technical_zip,tmp_path):
    with zipfile.ZipFile(source_technical_zip) as src:
        original={name:src.read(name) for name in src.namelist()}
    completion=json.loads(original['_COMPLETION.json'])
    key=completion['records'][0]['task']['key']+'.npz'
    with np.load(io.BytesIO(original[key]),allow_pickle=False) as saved:
        arrays={field:saved[field] for field in saved.files}
    assert len(arrays['parentage'])>0
    tampered=arrays['parentage'].copy()
    tampered[0,1]=99999999
    arrays['parentage']=tampered
    content=io.BytesIO()
    np.savez_compressed(content,**arrays)
    original[key]=content.getvalue()
    completion['records'][0]['case_sha256']=hashlib.sha256(original[key]).hexdigest()
    original['_COMPLETION.json']=(json.dumps(completion,indent=2)+'\n').encode()
    corrupted=tmp_path/'tampered-technical-original.zip'
    with zipfile.ZipFile(corrupted,'w',compression=zipfile.ZIP_DEFLATED) as dest:
        for name,body in original.items():dest.writestr(name,body)
    with pytest.raises(ValueError,match='Original recorded child/father/mother pair differs'):
        admit(0,corrupted,technical=True)
