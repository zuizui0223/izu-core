from dataclasses import replace
import numpy as np
import pytest
from scripts.run_model3_assurance_intervention import founders
from scripts.initial_assurance_mean_20261013 import equalize_mean, tasks, verify_clamp_identity, analyze,verify_mapping
import json
from scripts.run_initial_assurance_mean_20261013 import references,run_shard


def test_mean_shift_preserves_variance_covariance_and_provenance():
    s=founders();a=s.alleles.copy();a[:,2,:]+=.12
    s=replace(s,alleles=a);t,receipt=equalize_mean(s)
    assert t.alleles[:,:,].shape==s.alleles.shape
    assert abs(t.alleles[:,2].mean()-.5)<1e-12
    np.testing.assert_allclose(t.alleles[:,2].var(),s.alleles[:,2].var(),atol=1e-12,rtol=0)
    np.testing.assert_array_equal(t.alleles[:,:2],s.alleles[:,:2])
    for f in ('allele_origin','mutation_flags','ids','birth_years'):
        np.testing.assert_array_equal(getattr(t,f),getattr(s,f))
    assert receipt['max_covariance_error']<1e-12


def test_infeasible_shift_is_rejected_without_clipping():
    s=founders();a=s.alleles.copy();a[:,2,:]=1.;a[0,2,0]=0.
    with pytest.raises(ValueError,match='outside'):
        equalize_mean(replace(s,alleles=a))


def test_complete_4096_inventory_and_shared_seed_recipe():
    rows=tasks();assert len(rows)==4096
    from scripts.persistence_expression_mechanism_20261012 import future_seed,shard_for
    assert len({tuple(sorted(t.items())) for t in rows})==4096
    assert all(sum(shard_for(t)==i for t in rows)==256 for i in range(16))
    assert future_seed(rows[0])==future_seed(dict(rows[0],origin='I_access_first',policy='A_fixed'))


def test_clamp_identity_rejects_changed_MI_or_parentage_but_allows_hidden_A():
    n=4;shape=(n,3,2)
    x=dict(population=np.array([2,2]),parentage=np.array([[2,0,1],[3,1,0]]),diagnostics=np.ones((1,11)),
           offsets=np.array([0,2,4]),ids=np.arange(n),birth_years=np.array([0,0,1,1]),
           alleles=np.ones(shape)*.5,allele_origin=np.zeros(shape,int),mutation_flags=np.zeros(shape,bool))
    y={k:v.copy() for k,v in x.items()};y['alleles'][:,2]=.8
    verify_clamp_identity(x,y)
    y['alleles'][0,1,0]=.8
    with pytest.raises(AssertionError):verify_clamp_identity(x,y)
    y={k:v.copy() for k,v in x.items()};y['parentage'][0,1]=1
    with pytest.raises(AssertionError):verify_clamp_identity(x,y)


def test_partition_retains_extinction_and_all_four_contrasts():
    x=np.zeros((2,512,2,3,2));x[:,:256,:,0,0]=1;x[:,:128,:,1,0]=1
    r=analyze(x,bootstrap_count=31)
    assert len(r['primary'])==4
    assert r['primary'][0]['estimate']==.25 and r['primary'][1]['estimate']==.25
    assert r['partition_closure_error']==0.
    with pytest.raises(ValueError):analyze(x[:,:511],bootstrap_count=31)
    x[0,0,0,0,0]=np.nan
    with pytest.raises(ValueError):analyze(x,bootstrap_count=31)


def test_labels_without_reference_payload_cannot_admit(tmp_path):
    from scripts.initial_assurance_mean_20261013 import INPUT_SHA,PRIOR_SHA
    (tmp_path/'REFERENCE.json').write_text(json.dumps(dict(status='ALL8192_PRIOR_REFERENCES_ADMITTED',
        raw_zip_sha256=PRIOR_SHA,input_sha256=INPUT_SHA,cases=8192,files={},records=[])),encoding='utf-8')
    with pytest.raises(ValueError,match='inventory'):
        references(tmp_path)


def test_production_cannot_recompute_technical_cases_or_skip_clamp_gate(tmp_path):
    with pytest.raises(ValueError,match='technical'):
        run_shard('not-read','not-read',0,tmp_path/'out')


def test_mapping_numeric_receipt_uses_frozen_invariance_tolerance():
    _,mapping=equalize_mean(founders());other=dict(mapping)
    other['max_covariance_error']+=1e-17
    verify_mapping(other,mapping)
    other['shift']+=.001
    with pytest.raises(ValueError):verify_mapping(other,mapping)
