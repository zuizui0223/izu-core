"""Fail-closed tests for double-heldout ecological and random-stream evaluation."""
import copy
import json
from pathlib import Path

import numpy as np
import pytest

from scripts.audit_chapter2_initial_clock_transfer_20261013 import ingest
from scripts.audit_chapter2_initial_clock_paired_cv_20261013 import validate_clusters
from scripts.audit_chapter2_initial_clock_two_axis_cv_20261013 import (
    model_matrix, double_heldout_predictions, scored_outcomes, evaluate, ALL_MODELS,
)


def actual_sources():
    compact=Path('data/results/ecological_order_boundary_20261013.json')
    t0=Path('data/results/chapter2_initial_clock_t0_raw_20261013.json')
    events=Path('data/results/chapter2_initial_clock_paired_events_20261013.json')
    if not all(x.is_file() for x in (compact,t0,events)):
        pytest.skip('Full pinned original source checkout not present in isolated tester')
    summary=json.loads(compact.read_text())
    features=json.loads(t0.read_text())
    paired=json.loads(events.read_text())
    rows=ingest(summary,features)
    groups=validate_clusters(paired,rows)
    return summary,features,paired,rows,groups


def test_flexible_controls_are_t0_only_and_train_scaled():
    # No observed outcomes enter this matrix: missing class field is intentional.
    rows=[]
    for block in ('main','confirmation'):
        for ctx in range(9):
            supply=(0.,.03125,.03125,.125,.125,.5,.5,1.,1.)[ctx]
            composition=('empty','matched','separated','matched','separated',
                         'matched','separated','matched','separated')[ctx]
            rows.append({'block':block,'context':ctx,'supply':supply,'composition':composition,
                         'f':{'I_variance_allelic_proxy':.0063 if block=='main' else .0047,
                              't0_expected_I_response':0.0}})
    train=[i for i in range(18) if i not in (0,9)]
    test=[0,9]
    for name in ALL_MODELS:
        # Original feature sets need fuller feature ledger; flexible controls only.
        if name not in ('ecology_genetics_quadratic_full',
                        'ecology_genetics_variance_supply',
                        'ecology_genetics_variance_composition',
                        'ecology_genetics_quadratic_var_supply'):
            continue
        tr,te=model_matrix(rows,name,train,test)
        assert tr.shape[0]==16 and te.shape[0]==2
        assert tr.shape[1]==te.shape[1]
        assert np.isfinite(tr).all() and np.isfinite(te).all()
        np.testing.assert_allclose(tr[:,0],1)
        np.testing.assert_allclose(te[:,0],1)
        np.testing.assert_allclose(tr[:,1:].mean(axis=0),0,atol=1e-12)
    with pytest.raises(ValueError,match='Unregistered'):
        model_matrix(rows,'unregistered_t0_model',train,test)


def test_full_case_unseen_seed_and_unseen_context_prediction():
    _,_,_,rows,history=actual_sources()
    out,folds=double_heldout_predictions(rows,history,0.15)
    assert len(folds)==45
    assert sum(f['test_starts'] for f in folds)==2304
    assert sum(f['train_starts'] for f in folds)==sum(16*(128-sum(r%5==k for r in range(128))) for k in range(5))*9
    assert all(f['train_starts']>0 for f in folds)
    for m in ALL_MODELS:
        assert len(out[m])==2304
        for probability in out[m].values():
            assert probability.shape==(6,)
            assert np.isfinite(probability).all() and (probability>0).all()
            assert abs(probability.sum()-1)<1e-12
    score,_=scored_outcomes(history,out)
    assert score['ecology_genetics_price']['n']==2304
    assert score['ecology_genetics_price']['argmax_accuracy']<.6


def test_test_label_cannot_perturb_own_pair_or_unseen_context_fit():
    _,_,_,rows,history=actual_sources()
    prior,_=double_heldout_predictions(rows,history,.15)
    changed=copy.deepcopy(history)
    changed['main',0][0]=(changed['main',0][0]+1)%6
    after,_=double_heldout_predictions(rows,changed,.15)
    for name in ALL_MODELS:
        # Seed 0 is held out for *all* nine contexts, independent of its label.
        for ctx in range(9):
            np.testing.assert_array_equal(prior[name]['main',0,ctx],after[name]['main',0,ctx])
        # Ecological context 0 is entirely absent from the fit of its own labels.
        for block in ('main','confirmation'):
            for rep in range(128):
                np.testing.assert_array_equal(prior[name][block,rep,0],after[name][block,rep,0])


def test_original_two_axis_results_and_stronger_null_scope():
    summary,t0,pair,_,_=actual_sources()
    result=evaluate(summary,t0,pair)
    assert result['status']=='DOUBLE_HELDOUT_RETROSPECTIVE_2304_CASE_256_HISTORY_READONLY'
    assert len(result['results'])==3
    main=result['results'][1]
    assert main['lambda']==.15
    assert main['scores']['ecology_genetics_price']['n']==2304
    assert abs(main['scores']['ecology_genetics_price']['log_loss']-1.4216902260569377)<1e-7
    assert abs(main['scores']['ecology_genetics_quadratic']['log_loss']-1.4438958712809464)<1e-7
    assert abs(main['scores']['ecology_genetics_quadratic_var_supply']['log_loss']-1.4165933752581907)<1e-7
    assert main['comparisons']['price_over_equal_complexity_quadratic']['log_loss_reduction']>0
    assert main['comparisons']['price_over_fully_flexible_null']['log_loss_reduction']<0
    assert all(len(r['folds'])==45 for r in result['results'])