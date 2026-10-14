"""Original-operator pilot input inventory gates: NO biological trajectories."""
import hashlib
import json
from pathlib import Path
import re

import numpy as np
import pytest

from scripts.register_chapter2_clock_factorial_pilot_20261013 import (
    source_admit, manifest, hidden_genome, seed, checksum, git_blob,
    CONTEXTS, FOUNDERS, WIDTHS, I_HIDDEN, REPEATS, PILOT_SALT,
    PILOT_PROTOCOL_GIT_BLOB, ORIGINAL_SALT, TECHNICAL_SALT,
)

ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/'data/design/chapter2_clock_factorial_pilot_registered_inputs_20261013.json'
PROTOCOL=ROOT/'data/design/chapter2_clock_factorial_pilot_protocol_20261013.json'


def test_existing_frozen_protocol_and_registered_manifest():
    assert git_blob(PROTOCOL.read_bytes())==PILOT_PROTOCOL_GIT_BLOB
    recorded=json.loads(RECORD.read_text('utf8'))
    assert recorded['pilot_protocol_git_blob']==PILOT_PROTOCOL_GIT_BLOB
    assert recorded['schema']=='chapter2_clock_factorial_pilot_exact_case_registration_v1'
    assert recorded['status']=='FROZEN_INPUT_INVENTORY_ONLY_DO_NOT_DISPATCH'
    assert recorded['n_cases']==1536 and recorded['n_updates_if_executed']==307200
    assert recorded['cluster_count']==128 and recorded['cases_per_cluster']==12
    assert recorded['new_biological_histories']==0 and recorded['not_a_biological_readout']
    assert len(recorded['source_configs'])==6 and len(recorded['genetic_treatments'])==8
    assert len(recorded['pilot_case_keys'])==1536
    assert len(recorded['rng_clusters'])==128


def test_paired_seed_stream_and_all_12_treatments_are_registered_once():
    document=json.loads(RECORD.read_text('utf8'))
    groups={}
    names=set()
    seeds=set()
    streams={(r['block'],r['replicate']):r['master'] for r in document['rng_clusters']}
    assert len(streams)==128
    for key in document['pilot_case_keys']:
        parsed=re.fullmatch(r'(main|confirmation)_c([034])_w(24|40)_i([01])_r(\d{3})',key)
        assert parsed,key
        block,context,w,h,rep=parsed.groups()
        context=int(context);w=int(w)/512;h=float(h);rep=int(rep)
        cluster=(block,rep)
        groups.setdefault(cluster,[]).append((context,w,h,key))
        assert key not in names
        names.add(key)
        assert streams[cluster]==str(seed(PILOT_SALT,block,rep))
        seeds.add(streams[cluster])
    assert len(names)==1536 and len(groups)==128 and len(seeds)==128
    for (block,rep),rows in groups.items():
        assert len(rows)==12
        assert {(c,w,h) for c,w,h,_ in rows} == {
            (ctx,w,h) for ctx in CONTEXTS for w in WIDTHS for h in I_HIDDEN}
        assert int(streams[block,rep])!=seed(TECHNICAL_SALT,block,rep)
        original_seed=int.from_bytes(hashlib.sha256((ORIGINAL_SALT+'\0'+block+'\0'+str(rep)+'\0'+'0').encode()).digest()[:16],'big')
        assert int(streams[block,rep])!=original_seed


def test_original_exact_same_expressed_genotypes_and_source_commit():
    record=json.loads(RECORD.read_text('utf8'))
    assert record['original_source_execution_commit']=='328548612e93469fcc8663f24548530a57399b9a'
    assert record['seed_salt']==PILOT_SALT
    assert len(record['original_source_git_blobs'])==5
    expected={
        ('main',.046875,0.):'0ee1d65d8dd8adb604bbd68bc8e322dcaadd13de5df10e2adb72994d09084092',
        ('main',.046875,1.):'4da49d080c1033932b78d44e5b0804406ddc48896e0789d3ec211c2c5c39b96b',
        ('main',.078125,0.):'6e1406b39e603d6cb92d638e39f5ba2313e37b72bb275c27210425b603a649fd',
        ('main',.078125,1.):'e89ea3b09158d5429c29effce466750be198b53a47a5c0fd0da8179db792fdad',
        ('confirmation',.046875,0.):'307b150451a3a89c29c2c104ac5bbf8bf6ffd3070a09e2ca3e171134738e8829',
        ('confirmation',.046875,1.):'8ab836651b21bb69460667749eb2e67492c7f43d52b9613310241c0ff3029106',
        ('confirmation',.078125,0.):'bf1a563c02cd7d5940a6792686d054b70670c93d6c55da64d89211f294d52f05',
        ('confirmation',.078125,1.):'54a173e049d06f07c5f996de697485745f3f0ad7b3a0abf0b06b210b161f1141',
    }
    found={}
    for row in record['genetic_treatments']:
        key=(row['block'],row['A_width'],row['I_hidden_homolog'])
        assert row['t0_expressed_sha256']==row['source_t0_expressed_sha256']
        found[key]=row['genotype_sha256']
    assert found==expected


def test_genome_transform_preserves_each_adult_phenotype_and_support():
    a=np.zeros((48,3,2),dtype=float)
    a[:,0,:]=.5
    a[:,1,0]=np.repeat([.25,.5,.75,.625],12)
    a[:,1,1]=np.repeat([.75,.5,.25,.375],12)
    a[:,2,:]=[.4375,.5625]
    reference=a.mean(axis=2)
    for w in WIDTHS:
        for h in I_HIDDEN:
            changed=hidden_genome(a,w,h)
            assert np.array_equal(changed.mean(axis=2),reference)
            assert np.array_equal(changed[:,0,:],a[:,0,:])
            if h==0:
                assert np.array_equal(changed[:,1,0],changed[:,1,1])
    with pytest.raises(ValueError,match='Unsupported'):
        hidden_genome(a,.07,0.)


def test_bad_source_zip_rejected_before_any_biological_simulation(tmp_path):
    paths={c:tmp_path/f'c{c}.zip' for c in CONTEXTS}
    for path in paths.values():path.write_bytes(b'not a frozen source')
    with pytest.raises(ValueError,match='SHA drift'):
        source_admit(paths)
    with pytest.raises(ValueError,match='All and only'):
        source_admit({0:paths[0]})


def test_design_mismatch_and_wrong_checksum_not_admitted(monkeypatch):
    from scripts import register_chapter2_clock_factorial_pilot_20261013 as generator
    design=json.loads(PROTOCOL.read_text('utf8'))
    design['pilot']['salt']='tampered-salt'
    with pytest.raises(ValueError,match='Pilot salt'):
        manifest({},design,PROTOCOL.read_bytes())
    assert checksum(b'')==hashlib.sha256(b'').hexdigest()
