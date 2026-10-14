"""Read-only historical t0 prediction diagnostics, no new biological histories."""
import copy
import json
from pathlib import Path

import numpy as np
import pytest

from scripts.audit_chapter2_initial_clock_transfer_20261013 import (
    CLASSES, MODEL_NAMES, LAMBDAS, ingest, features, feature_matrix,
    train_multinomial, predict, proper_score, run, leave_one_context_out, blob_sha,
    RAW_FEATURE_GIT_BLOB, EXPECTED_INPUT_GIT_BLOB,
)
from scripts.audit_chapter2_initial_clock_identifiability_20261013 import (
    EXPECTED_SOURCE_COMMIT, EXPECTED_PRODUCER_SHA,
)


def fixture():
    # Purpose-built synthetic fixture; never represented as an original genomic readout.
    cats={k:0 for k in CLASSES}
    summ={'status':'ALL2304_RAW_GENOTYPE_AND_ORDER_TRACES_ADMITTED',
          'cases':2304,'updates':460800,'execution_commit':EXPECTED_SOURCE_COMMIT,
          'producer_sha256':EXPECTED_PRODUCER_SHA,'cells':[]}
    t0={'status':'ALL2304_ORIGINAL_INITIAL_FEATURES_ADMITTED','original_starts':2304,
        'founder_contexts':18,'replicated_t0_invariance_verified':True,
        'execution':{'conclusion':'success','no_biological_simulation':True},
        'original_raw_t0_feature_rows':[]}
    for block in ('main','confirmation'):
        for ctx in range(9):
            supply=(0.,.03125,.03125,.125,.125,.5,.5,1.,1.)[ctx]
            comp=('empty','matched','separated','matched','separated','matched','separated','matched','separated')[ctx]
            n=[15,20,10,75,1,7] if ctx%2 else [20,40,20,45,1,2]
            assert sum(n)==128
            counts=dict(zip(CLASSES,n))
            summ['cells'].append({'block':block,'context':ctx,'supply':supply,'composition':comp,
                                  'starts':128,'categories':counts,'D':(n[0]-n[1])/128})
            t0['original_raw_t0_feature_rows'].append({'block':block,'context':ctx,
               'supply':supply,'composition':comp,'starts':128,'time0_only':{
                'I_variance_allelic_proxy':0.00476 if block=='main' else 0.0063,
                'I_variance_expressed':0.0026 if block=='main' else 0.0092,
                'A_variance_expressed':0.0,'A_variance_allelic_proxy':0.001953125,
                'A_expected_F1_Mendelian_variance_no_mutation':0.001953125,
                't0_expected_I_response':(ctx-3.)*0.0003,
                't0_expected_A_response':0.0,'founder_mean_I':0.52,
                'founder_mean_A':0.5}})
    return summ,t0


def test_all_six_outcomes_and_source_genotype_cells():
    summ,t0=fixture(); rows=ingest(summ,t0)
    assert len(rows)==18
    assert len({(r['block'],r['context']) for r in rows})==18
    assert all(r['counts'].sum()==128 for r in rows)
    assert MODEL_NAMES==('prevalence','ecology','genetic_access','ecology_genetics','ecology_genetics_quadratic','ecology_genetics_price')


def test_affected_t0_or_duplicated_cells_fail_closed():
    summ,t0=fixture()
    broken=copy.deepcopy(t0)
    broken['original_raw_t0_feature_rows'][0]['time0_only']['t0_expected_A_response']=0.1
    with pytest.raises(ValueError,match='assurance response'):ingest(summ,broken)
    broken=copy.deepcopy(t0)
    broken['original_raw_t0_feature_rows'][0]=broken['original_raw_t0_feature_rows'][1]
    with pytest.raises(ValueError,match='Repeated'):ingest(summ,broken)
    broken=copy.deepcopy(t0)
    broken['original_raw_t0_feature_rows'][0]['supply']=0.999
    with pytest.raises(ValueError,match='context drift'):ingest(summ,broken)
    broken=copy.deepcopy(summ)
    broken['cells'][0]['categories']['neither']+=1
    with pytest.raises(ValueError):ingest(broken,t0)


def test_only_time_zero_features_change_predictors():
    summ,t0=fixture(); rows=ingest(summ,t0)
    r=rows[0];eco=features(r,'ecology');price=features(r,'ecology_genetics_price')
    assert eco.shape==(4,)
    assert price.shape==(6,)
    assert price[-1]==r['f']['t0_expected_I_response']/0.05
    rr=copy.deepcopy(r);rr['counts']=np.array([128,0,0,0,0,0])
    for model in MODEL_NAMES:
        np.testing.assert_array_equal(features(r,model),features(rr,model))


def test_fit_is_proper_distribution_and_regularized():
    X=np.array([[1.,-1.],[1.,1.],[1.,-1.],[1.,1.]])
    Y=np.array([[80,20,10,10,4,4],[20,80,10,10,4,4],
                [75,25,10,10,4,4],[25,75,10,10,4,4]],float)
    B=train_multinomial(X,Y,0.15)
    p=predict(X,B)
    assert p.shape==(4,6) and np.all(p>0)
    np.testing.assert_allclose(p.sum(axis=1),1,atol=1e-12)
    assert p[0,0]>p[1,0]
    assert proper_score(p,Y)['n']==512


def test_leave_both_founders_out_at_same_context_and_recompute():
    summ,t0=fixture();rows=ingest(summ,t0)
    result=leave_one_context_out(rows,0.15)
    assert len(result['fold_results'])==9
    assert all(f['heldout_profile_keys']==['main','confirmation'] for f in result['fold_results'])
    assert all(f[m]['n']==256 for f in result['fold_results'] for m in MODEL_NAMES)
    assert all(result['model_scores'][m]['n']==2304 for m in MODEL_NAMES)


def test_heldout_context_outcomes_never_train_that_context():
    summ,t0=fixture();rows=ingest(summ,t0)
    a=leave_one_context_out(rows,0.15)
    changed=copy.deepcopy(rows)
    for r in changed:
        if r['context']==3:
            r['counts']=np.array([128,0,0,0,0,0],dtype=float)
    b=leave_one_context_out(changed,0.15)
    # Folds for context 3 have unchanged learned coefficients but changed loss.
    # We can directly verify model predictions when other context responses change.
    train=[i for i,r in enumerate(rows) if r['context']!=3]
    test=[i for i,r in enumerate(rows) if r['context']==3]
    for model in MODEL_NAMES:
        X,Xtest=feature_matrix(rows,model,train,test)
        X2,Xtest2=feature_matrix(changed,model,train,test)
        np.testing.assert_array_equal(X,X2)
        np.testing.assert_array_equal(Xtest,Xtest2)
        B=train_multinomial(X,np.vstack([r['counts'] for r in rows])[train],0.15)
        B2=train_multinomial(X2,np.vstack([r['counts'] for r in changed])[train],0.15)
        np.testing.assert_allclose(predict(Xtest,B),predict(Xtest2,B2),atol=1e-12)
        assert b['fold_results'][3][model]['log_loss']!=a['fold_results'][3][model]['log_loss']


def test_reject_wrong_model_or_mutable_output_contract():
    summ,t0=fixture(); rows=ingest(summ,t0)
    with pytest.raises(ValueError,match='Unknown'):features(rows[0],'oracle')
    with pytest.raises(ValueError):train_multinomial(np.ones((2,2)),np.ones((2,6)),0.0)
    with pytest.raises(ValueError):proper_score(np.ones((2,2)),np.ones((2,6)))


def test_original_repository_sources_and_expected_main_result_if_present():
    p=Path('data/results/ecological_order_boundary_20261013.json')
    q=Path('data/results/chapter2_initial_clock_t0_raw_20261013.json')
    if not p.exists() or not q.exists():
        pytest.skip('Original source data not present in focused standalone test checkout')
    assert blob_sha(p.read_bytes())==EXPECTED_INPUT_GIT_BLOB
    assert blob_sha(q.read_bytes())==RAW_FEATURE_GIT_BLOB
    result=run(json.loads(p.read_text()),json.loads(q.read_text()))
    assert len(result['results'])==3
    r=result['results'][1]
    assert r['lambda_value']==0.15
    assert r['model_scores']['ecology_genetics']['n']==2304
    assert r['model_scores']['ecology_genetics_price']['n']==2304
    np.testing.assert_allclose(r['model_scores']['ecology_genetics_price']['log_loss'],
                               1.418974125934159,atol=1e-8)
    np.testing.assert_allclose(r['delta_add_t0_price_vs_ecology_genetics']['log_loss_reduction'],
                               0.057836215148768355,atol=1e-8)
    assert len(r['fold_results'])==9
    assert sum(f['ecology_genetics_price']['log_loss']<f['ecology_genetics']['log_loss'] for f in r['fold_results'])==7