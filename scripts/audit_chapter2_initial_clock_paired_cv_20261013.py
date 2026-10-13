"""Paired-seed blocked 5-fold exploratory six-class t0 prediction check.

Each founder-specific biological replicate is a 9-context paired cluster.
All nine contexts for a single (founder,replicate) are held out together.
Predictions rely only on initial biological state and static visitor ecology.
Bootstrap draws clusters within founder blocks, conditional on the five
trained models; it is NOT a confidence interval for ecological-site generality.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_initial_clock_identifiability_20261013 import CLASSES
from scripts.audit_chapter2_initial_clock_transfer_20261013 import (
    RAW_FEATURE_GIT_BLOB,EXPECTED_INPUT_GIT_BLOB,LAMBDAS,MODEL_NAMES,
    ingest,feature_matrix,train_multinomial,predict,proper_score,blob_sha,
)

SEED=2026101301
B=10000
PAIRED_EVENTS_GIT_BLOB = "afab849d2f0036d07d28beb1441644f9ca2808cb"


def validate_clusters(pair:dict,rows:list[dict]):
    if (pair.get('status')!='ALL2304_CASE_HASHES_AND_256_PAIRED_CLUSTERS_VERIFIED' or
        pair.get('case_count')!=2304 or pair.get('clusters')!=256 or
        pair.get('random_streams_reused_across_contexts') is not True or
        pair.get('no_new_biological_histories') is not True or
        pair.get('original_source_compact_git_blob')!=EXPECTED_INPUT_GIT_BLOB):
        raise ValueError('Original seed-cluster source identity not admitted')
    label_map=pair.get('categories')
    expected=dict(zip(('A','I','T','a','i','N'),CLASSES))
    if label_map != expected or pair.get('context_order')!=list(range(9)):
        raise ValueError('Original category encoding/context order mismatch')
    observed={}
    if not isinstance(pair.get('data'),list) or len(pair['data'])!=256:
        raise ValueError('Paired original cluster cardinality mismatch')
    for row in pair['data']:
        k=(row.get('block'),row.get('replicate'))
        if k in observed or k[0] not in ('main','confirmation') or type(k[1]) is not int or not 0<=k[1]<128:
            raise ValueError('Repeated/outside original cluster')
        seq=row.get('sequence')
        if not isinstance(seq,str) or len(seq)!=9 or any(c not in expected for c in seq):
            raise ValueError('Truncated/unknown six-way original outcomes')
        observed[k]=[CLASSES.index(expected[c]) for c in seq]
    if len(observed)!=256 or set(observed)!={(b,i) for b in ('main','confirmation') for i in range(128)}:
        raise ValueError('Missing paired stream or founder')
    # Independently compare each of the 18 source cell category distributions.
    for cell in rows:
        counts=np.bincount([observed[(cell['block'],r)][cell['context']] for r in range(128)],minlength=6)
        if not np.array_equal(counts,cell['counts']):
            raise ValueError('Original paired event counts fail source summary')
    return observed


def out_of_fold_predictions(rows,cluster_labels,lam):
    indices={(r['block'],r['context']):i for i,r in enumerate(rows)}
    features_idx=list(range(18))
    X={m:feature_matrix(rows,m,features_idx,features_idx)[0] for m in MODEL_NAMES}
    predictions={m:{} for m in MODEL_NAMES}
    fold_models=[]
    for k in range(5):
        train_counts=np.zeros((18,6));test_counts=np.zeros((18,6))
        for (block,rep),seq in cluster_labels.items():
            target = test_counts if rep%5==k else train_counts
            for ctx,y in enumerate(seq):target[indices[block,ctx],y]+=1
        # 128 biological streams PER source cell, divided into five folds.
        ntrain=train_counts.sum(axis=1);ntest=test_counts.sum(axis=1)
        if not np.all(ntrain>0) or not np.all(ntest>0):raise ValueError('Empty seed fold')
        yscaled=(train_counts/ntrain[:,None])*128  # all 18 profiles weight one each
        fold={'fold':k,'heldout_clusters':int(ntest.sum()/9),'heldout_cases':int(ntest.sum())}
        for m in MODEL_NAMES:
            beta=train_multinomial(X[m],yscaled,lam)
            phat=predict(X[m],beta)
            fold[m]=proper_score(phat,test_counts)
            for (block,rep),seq in cluster_labels.items():
                if rep%5==k:
                    for ctx in range(9):predictions[m][(block,rep,ctx)]=phat[indices[block,ctx]]
        fold_models.append(fold)
    if any(len(v)!=2304 for v in predictions.values()):raise ValueError('Incomplete out-of-fold predictions')
    return predictions, fold_models


def paired_delta(cluster_labels, preds, base, enriched):
    results={}
    for block in ('main','confirmation'):
        a=np.zeros((128,2))
        for rep in range(128):
            for ctx in range(9):
                y=cluster_labels[block,rep][ctx]
                pb=preds[base][block,rep,ctx]
                pe=preds[enriched][block,rep,ctx]
                if min(pb[y],pe[y])<=0:raise ValueError('Nonpositive conditional probability')
                a[rep,0]+=(np.log(pe[y])-np.log(pb[y]))/9
                a[rep,1]+=((np.sum(pb*pb)-2*pb[y])-(np.sum(pe*pe)-2*pe[y]))/9
        results[block]=a
    diffs=np.concatenate([results['main'],results['confirmation']])
    return results, diffs.mean(axis=0)


def bootstrap(history_deltas, bootstrap_count=B, seed=SEED):
    # Resample both founder blocks separately and retain the 9-context pairing.
    rng=np.random.default_rng(seed)
    a=history_deltas['main'];b=history_deltas['confirmation']
    if a.shape!=(128,2) or b.shape!=(128,2):raise ValueError('Original paired cluster shape changed')
    draws=np.empty((bootstrap_count,2))
    for z in range(bootstrap_count):
        draws[z]=(a[rng.integers(128,size=128)].mean(axis=0)+
                  b[rng.integers(128,size=128)].mean(axis=0))/2
    lo,hi=np.quantile(draws,[0.025,0.975],axis=0)
    return {'replicates':bootstrap_count,'unit':'founder-specific replicate/visitor random-stream cluster (all nine ecological contexts stay together)',
            'sampling':'paired within each of two source founders, fitted 5-fold predictions treated as fixed',
            'bootstrap_seed':seed,'log_loss_reduction_95_percentile':[float(lo[0]),float(hi[0])],
            'brier_reduction_95_percentile':[float(lo[1]),float(hi[1])]}


def run(summary, features, paired):
    rows=ingest(summary,features)
    history=validate_clusters(paired,rows)
    allres=[]
    for lam in LAMBDAS:
        preds,folds=out_of_fold_predictions(rows,history,lam)
        scores={}
        for model in MODEL_NAMES:
            p=[];cnt=[]
            # All labels scored under predictions trained without the seed-cluster.
            for row in rows:
                for rep in range(128):
                    obs=np.zeros(6);obs[history[row['block'],rep][row['context']]]=1
                    p.append(preds[model][row['block'],rep,row['context']]);cnt.append(obs)
            scores[model]=proper_score(np.array(p),np.array(cnt))
        blocks,delta=paired_delta(history,preds,'ecology_genetics','ecology_genetics_price')
        ci=bootstrap(blocks)
        blocks_eco,delta_eco=paired_delta(history,preds,'ecology','ecology_genetics_price')
        ci_eco=bootstrap(blocks_eco,seed=SEED+1)
        blocks_quad,delta_quad=paired_delta(history,preds,'ecology_genetics_quadratic','ecology_genetics_price')
        ci_quad=bootstrap(blocks_quad,seed=SEED+2)
        ll_check=scores['ecology_genetics']['log_loss']-scores['ecology_genetics_price']['log_loss']
        brier_check=scores['ecology_genetics']['brier']-scores['ecology_genetics_price']['brier']
        if max(abs(ll_check-delta[0]),abs(brier_check-delta[1]))>1e-12:
            raise ValueError('Original all-start paired score does not close')
        allres.append({'lambda':lam,'five_fold_out_of_history_scores':scores,'folds':folds,
                       'controlled_add_source_Price_vs_ecology_genetics':{'log_loss_reduction':float(delta[0]),
                         'brier_reduction':float(delta[1]),'confidence_exploratory_conditional':ci},
                       'full_vs_ecology_only':{'log_loss_reduction':float(delta_eco[0]),
                         'brier_reduction':float(delta_eco[1]),'confidence_exploratory_conditional':ci_eco},
                       'full_vs_equal_complexity_quadratic':{'log_loss_reduction':float(delta_quad[0]),
                         'brier_reduction':float(delta_quad[1]),'confidence_exploratory_conditional':ci_quad}})
    return {'schema':'chapter2_initial_clock_seed_blocked_cv_exploratory_v1',
            'status':'COMPLETED_RETROSPECTIVE_256_CLUSTER_PAIRED_FOLD_PROPER_SCORES_NOT_PROSPECTIVE_CONFIRMATION',
            'cases':2304,'independent_stochastic_stream_clusters':256,
            'ecological_contexts_per_cluster':9,'genotypic_founder_blocks':2,
            'six_original_categories':list(CLASSES),'paired_seed_fold_rule':'replicate % 5; all nine contexts and matching founder held out together',
            'models':list(MODEL_NAMES),'lambda_sensitivity':list(LAMBDAS),
            'original_source_bio':'fixed ecological Model3, no new evolutionary trajectories',
            'cohort_scope':'Single biological model and two founder genetic states; reused stochastic streams across contexts.',
            'selection_direction_inference':'initial full-parent Price I response, not an A-vs-I first-passage prediction',
            'initial_assurance_genetic_access':'constant A heterozygosity, expressed variance0, expected t0 selection0, F1 segregation proxy constant',
            'results':allres,
            'inference_limitations':['Post-hoc selected model features, exploratory tests only.','Paired cluster bootstrap conditions on fold-fitted probabilities, ignoring refit variability.',
              'History seeds are independent stochastic inputs but share fixed ecology and only two genotypes; no ecological cross-system generality.',
              'Cannot identify access-delay A selection or a two-trait causal response-clock ratio from constant A source accessibility.',
              'Not a natural-order persistence result or field-validated evolutionary equation.']}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--compact',type=Path,required=True)
    p.add_argument('--t0',type=Path,required=True)
    p.add_argument('--paired',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    if a.out.exists():raise ValueError('Refuse overwrite of existing readout')
    if blob_sha(a.compact.read_bytes())!=EXPECTED_INPUT_GIT_BLOB or blob_sha(a.t0.read_bytes())!=RAW_FEATURE_GIT_BLOB:
        raise ValueError('Source-bound compact and original-genotype t0 identity')
    paired_raw = a.paired.read_bytes()
    if blob_sha(paired_raw) != PAIRED_EVENTS_GIT_BLOB:
        raise ValueError('Source-bound paired event identity differs')
    result=run(json.loads(a.compact.read_bytes()),json.loads(a.t0.read_bytes()),json.loads(paired_raw))
    result['source']={'original_compact_sha':EXPECTED_INPUT_GIT_BLOB,'original_t0_sha':RAW_FEATURE_GIT_BLOB,
                      'original_paired_git_blob': PAIRED_EVENTS_GIT_BLOB,
                      'source_paired_case_status':'ALL2304_CASE_HASHES_AND_256_PAIRED_CLUSTERS_VERIFIED'}
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open("x", encoding="utf-8", newline="\n") as output:
        output.write(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':result['status'],'n_history_clusters':256,
                      'main':result['results'][1]['controlled_add_source_Price_vs_ecology_genetics'],
                      'scores':result['results'][1]['five_fold_out_of_history_scores']},indent=2))

if __name__=='__main__':main()
