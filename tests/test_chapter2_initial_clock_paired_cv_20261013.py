"""Tests of paired original case integrity and six-class prediction evaluation."""
import copy
import json
from pathlib import Path

import numpy as np
import pytest

from scripts.audit_chapter2_initial_clock_paired_cv_20261013 import (
    validate_clusters, out_of_fold_predictions, paired_delta, bootstrap,
    run, SEED,
)
from scripts.audit_chapter2_initial_clock_transfer_20261013 import ingest,MODEL_NAMES
from scripts.audit_chapter2_initial_clock_identifiability_20261013 import (
    EXPECTED_INPUT_GIT_BLOB,
)


def canonical_if_present():
    pa=Path('data/results/ecological_order_boundary_20261013.json')
    pb=Path('data/results/chapter2_initial_clock_t0_raw_20261013.json')
    pc=Path('data/results/chapter2_initial_clock_paired_events_20261013.json')
    if not (pa.exists() and pb.exists() and pc.exists()):
        pytest.skip('Original three source files not staged in isolated test checkout')
    return json.loads(pa.read_text()),json.loads(pb.read_text()),json.loads(pc.read_text())


def test_real_all_start_seed_members_and_counts():
    summary,features,paired=canonical_if_present()
    rows=ingest(summary,features)
    events=validate_clusters(paired,rows)
    assert len(events)==256
    assert len({k for k in events if k[0]=='main'})==128
    assert all(len(v)==9 for v in events.values())
    assert paired['original_source_compact_git_blob']==EXPECTED_INPUT_GIT_BLOB
    assert len(paired['provider_receipts'])==9
    assert paired['case_count']==2304


def test_corrupt_paired_stream_or_context_rejected():
    summary,features,paired=canonical_if_present()
    rows=ingest(summary,features)
    wrong=copy.deepcopy(paired)
    wrong['data'][0]['sequence']='AAAAAAAAN' # deliberately different original 9 events
    with pytest.raises(ValueError,match='counts'):validate_clusters(wrong,rows)
    wrong=copy.deepcopy(paired)
    wrong['data'][0]=wrong['data'][1]
    with pytest.raises(ValueError,match='Repeated'):validate_clusters(wrong,rows)
    wrong=copy.deepcopy(paired)
    wrong['data'][0]['sequence']='NNNNNNNN?' # illegal category
    with pytest.raises(ValueError,match='Truncated'):validate_clusters(wrong,rows)


def test_seed_group_cv_does_not_split_nine_contexts():
    summary,features,paired=canonical_if_present()
    rows=ingest(summary,features)
    events=validate_clusters(paired,rows)
    preds,folds=out_of_fold_predictions(rows,events,0.15)
    assert len(folds)==5 and sum(f['heldout_clusters'] for f in folds)==256
    assert sum(f['heldout_cases'] for f in folds)==2304
    assert all(f['heldout_cases']==f['heldout_clusters']*9 for f in folds)
    for model in MODEL_NAMES:
        assert len(preds[model])==2304
        for (block,rep,context),prediction in preds[model].items():
            assert (block,rep) in events and 0<=context<9
            assert prediction.shape==(6,) and abs(prediction.sum()-1)<1e-12


def test_manual_one_seed_label_change_does_not_enter_own_fold_training():
    summary,features,paired=canonical_if_present()
    rows=ingest(summary,features)
    events=validate_clusters(paired,rows)
    original,folds=out_of_fold_predictions(rows,events,0.15)
    changed=copy.deepcopy(events)
    y=changed['main',0][0]
    changed['main',0][0]=(y+1)%6
    alternative,_=out_of_fold_predictions(rows,changed,0.15)
    for model in MODEL_NAMES:
        # Training held out rep=0 along with all other rep%5==0 histories.
        np.testing.assert_allclose(original[model]['main',0,0],
                                   alternative[model]['main',0,0],atol=1e-12)


def test_fixed_predicted_pairstream_bootstrap_and_strong_scope():
    summary,features,paired=canonical_if_present()
    rows=ingest(summary,features)
    events=validate_clusters(paired,rows)
    preds,_=out_of_fold_predictions(rows,events,0.15)
    clusters,delta=paired_delta(events,preds,'ecology_genetics','ecology_genetics_price')
    assert clusters['main'].shape==(128,2) and clusters['confirmation'].shape==(128,2)
    b1=bootstrap(clusters,bootstrap_count=120,seed=SEED)
    b2=bootstrap(clusters,bootstrap_count=120,seed=SEED)
    assert b1==b2
    assert delta[0]>0


def test_original_script_expected_all_256_history_results():
    summary,features,paired=canonical_if_present()
    result=run(summary,features,paired)
    assert len(result['results'])==3
    main=result['results'][1]
    assert main['lambda']==0.15
    score=main['five_fold_out_of_history_scores']
    np.testing.assert_allclose(score['ecology_genetics_price']['log_loss'],
                               1.318750,atol=2e-5)
    np.testing.assert_allclose(main['controlled_add_source_Price_vs_ecology_genetics']['log_loss_reduction'],
                               0.04593164651328621,atol=1e-8)
    np.testing.assert_allclose(main['full_vs_equal_complexity_quadratic']['log_loss_reduction'],
                               0.011869523390381411,atol=1e-8)
    ci=main['controlled_add_source_Price_vs_ecology_genetics']['confidence_exploratory_conditional']
    assert ci['replicates']==10000
    assert ci['log_loss_reduction_95_percentile'][0]>0
    assert result['independent_stochastic_stream_clusters']==256