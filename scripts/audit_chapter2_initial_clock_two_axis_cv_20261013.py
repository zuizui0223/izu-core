"""Retrospective source-bound 9x5 double-held-out six-class outcome predictions.

Every prediction is for one ecological context left out entirely AND seed histories
held out across all nine contexts, within each of the original two founder blocks.
The nine-context pairing for each (founder, replicate) is never split between
training and evaluation. It is a two-axis held-out diagnostic on previously
observed conditions, NOT independent model/system confirmation or a complete
access+selection first-passage clock.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import json
from pathlib import Path
import numpy as np

from scripts.audit_chapter2_initial_clock_identifiability_20261013 import (
    CLASSES, EXPECTED_INPUT_GIT_BLOB,
)
from scripts.audit_chapter2_initial_clock_transfer_20261013 import (
    RAW_FEATURE_GIT_BLOB, LAMBDAS, MODEL_NAMES, blob_sha, ingest,
    feature_matrix as original_feature_matrix, features as original_features,
    train_multinomial, predict, proper_score,
)
from scripts.audit_chapter2_initial_clock_paired_cv_20261013 import (
    validate_clusters, paired_delta, bootstrap,
)

FOLDS = 5
N_CONTEXTS = 9
N_HISTORY_BLOCKS = 256
# Deliberately adversarial, POST-HOC control feature sets. They are not
# preregistered, equal-complexity causal estimators or biological interactions.
FLEX_NAMES = (
    'ecology_genetics_quadratic_full',          # 2 ecological curvature columns
    'ecology_genetics_variance_supply',         # 1 G_I × log(supply) column
    'ecology_genetics_variance_composition',    # 1 G_I × composition column
    'ecology_genetics_quadratic_var_supply',    # 3 additional flexible columns
)
ALL_MODELS = MODEL_NAMES + FLEX_NAMES


def model_matrix(rows,model,train_idx,test_idx):
    if model in MODEL_NAMES:
        return original_feature_matrix(rows,model,train_idx,test_idx)
    if model not in FLEX_NAMES:
        raise ValueError('Unregistered exploratory feature family')
    matrix=[]
    for row in rows:
        base=original_features(row,'ecology_genetics')
        log_s=np.log1p(16*float(row['supply']))
        sep=float(row['composition']=='separated')
        variance=float(row['f']['I_variance_allelic_proxy'])
        if model=='ecology_genetics_quadratic_full':
            added=[log_s**2,sep*log_s**2]
        elif model=='ecology_genetics_variance_supply':
            added=[variance*log_s]
        elif model=='ecology_genetics_variance_composition':
            added=[variance*sep]
        else:
            added=[log_s**2,sep*log_s**2,variance*log_s]
        matrix.append(np.concatenate((base,added)))
    matrix=np.stack(matrix)
    mean=matrix[train_idx].mean(axis=0)
    sd=matrix[train_idx].std(axis=0)
    sd=np.where(sd>1e-12,sd,1.0)
    expand=lambda ids:np.column_stack((np.ones(len(ids)),(matrix[ids]-mean)/sd))
    return expand(train_idx),expand(test_idx)


def double_heldout_predictions(rows, histories, regularization):
    """Explicitly excludes both held-out ecological profile and random history.

    Only training outcomes from the 8 other contexts x remaining 4 seed folds are
    used to fit, scale, and tune *nothing*. All models have exactly the same split.
    """
    if len(rows)!=18 or regularization<=0:
        raise ValueError('Original 18 input rows / positive fixed penalty required')
    keys={(r['block'],r['context']):j for j,r in enumerate(rows)}
    if len(keys)!=18 or set(keys)!={(b,c) for b in ('main','confirmation') for c in range(9)}:
        raise ValueError('Incomplete ecological/founder panel')
    if len(histories)!=N_HISTORY_BLOCKS:
        raise ValueError('Incomplete paired random-stream clusters')
    outputs={m:{} for m in ALL_MODELS}
    trace=[]
    for held_context in range(N_CONTEXTS):
        train_index=[j for j,r in enumerate(rows) if r['context']!=held_context]
        test_index=[keys[block,held_context] for block in ('main','confirmation')]
        for held_fold in range(FOLDS):
            counts=np.zeros((18,6),dtype=np.int64)
            for (block,rep),seq in histories.items():
                if rep%FOLDS==held_fold:
                    continue
                for c,y in enumerate(seq):
                    if c!=held_context:
                        counts[keys[block,c],y]+=1
            ntrain=counts[train_index].sum(axis=1)
            if len(train_index)!=16 or np.any(ntrain<=0) or len(test_index)!=2 or np.any(counts[test_index]):
                raise ValueError('Double-held-out training closure failure')
            row={'held_context':held_context,'seed_fold':held_fold,
                 'train_starts':int(counts.sum()),
                 'test_starts':sum(rep%FOLDS==held_fold for block,rep in histories)}
            # Weight the 16 distinct profiles equally, irrespective of fold size.
            ytrain=counts[train_index]/ntrain[:,None]*128
            for m in ALL_MODELS:
                Xtrain,Xtest=model_matrix(rows,m,train_index,test_index)
                B=train_multinomial(Xtrain,ytrain,regularization)
                pp=predict(Xtest,B)
                for block,j in [('main',0),('confirmation',1)]:
                    for rep in range(128):
                        if rep%FOLDS==held_fold:
                            key=(block,rep,held_context)
                            if key in outputs[m]:
                                raise ValueError('Duplicate held-out case')
                            outputs[m][key]=pp[j]
            trace.append(row)
    for m in ALL_MODELS:
        if len(outputs[m])!=2304:
            raise ValueError('Missing predictions for '+m)
        if set(outputs[m])!={(b,r,c) for b in ('main','confirmation') for r in range(128) for c in range(9)}:
            raise ValueError('Incomplete original outcome-key inventory')
    if len(trace)!=45:
        raise ValueError('Expected nine contexts x five seed folds')
    return outputs,trace


def scored_outcomes(histories, preds):
    out={}
    contexts={}
    for model in ALL_MODELS:
        p=[];ys=[]
        for block in ('main','confirmation'):
            for rep in range(128):
                for ctx,y in enumerate(histories[block,rep]):
                    p.append(preds[model][block,rep,ctx]);ys.append(y)
        arr=np.array(p);y=np.array(ys,dtype=int)
        counts=np.zeros_like(arr);counts[np.arange(len(y)),y]=1
        out[model]=proper_score(arr,counts)
        contexts[model]=[]
        for ctx in range(9):
            pp=np.array([preds[model][b,r,ctx] for b in ('main','confirmation') for r in range(128)])
            yy=np.array([histories[b,r][ctx] for b in ('main','confirmation') for r in range(128)])
            one=np.zeros_like(pp);one[np.arange(256),yy]=1
            contexts[model].append({'context':ctx,**proper_score(pp,one)})
    return out,contexts


def evaluate(summary,features,paired):
    rows=ingest(summary,features)
    histories=validate_clusters(paired,rows)
    output=[]
    for lam in LAMBDAS:
        preds,trace=double_heldout_predictions(rows,histories,lam)
        scores,by_context=scored_outcomes(histories,preds)
        contrasts={}
        comparisons=(
            ('price_over_ecology_genetics','ecology_genetics','ecology_genetics_price'),
            ('price_over_equal_complexity_quadratic','ecology_genetics_quadratic','ecology_genetics_price'),
            ('price_over_ecology_only','ecology','ecology_genetics_price'),
            ('price_over_two_ecological_curvatures','ecology_genetics_quadratic_full','ecology_genetics_price'),
            ('price_over_variance_supply_interaction','ecology_genetics_variance_supply','ecology_genetics_price'),
            ('price_over_fully_flexible_null','ecology_genetics_quadratic_var_supply','ecology_genetics_price'),
        )
        for comparison_index,(k,base,more) in enumerate(comparisons):
            within,mean=paired_delta(histories,preds,base,more)
            delta={'log_loss_reduction':float(mean[0]),'brier_reduction':float(mean[1]),
                   'conditional_seed_cluster_interval':bootstrap(within,bootstrap_count=10000,
                      seed=2026101315+comparison_index)}
            if max(abs(delta['log_loss_reduction']-(scores[base]['log_loss']-scores[more]['log_loss'])),
                   abs(delta['brier_reduction']-(scores[base]['brier']-scores[more]['brier'])))>1e-12:
                raise ValueError('Paired log-score closure error')
            contrasts[k]=delta
        output.append({'lambda':lam,'scores':scores,'per_context':by_context,
                       'comparisons':contrasts,'folds':trace})
    return {'schema':'chapter2_initial_clock_ecology_and_seed_double_holdout_exploratory_v1',
            'status':'DOUBLE_HELDOUT_RETROSPECTIVE_2304_CASE_256_HISTORY_READONLY',
            'cases':2304,'seed_clusters':256,'ecological_contexts':9,'founder_blocks':2,
            'model_names':list(ALL_MODELS),'lambda_grid':list(LAMBDAS),
            'crossvalidation': 'For (ecological context c, random seed fold f), fit only other 8 contexts and histories rep%5 != f; predict original c/f cell.',
            'results':output,
            'source':{'input_compact_git_blob':EXPECTED_INPUT_GIT_BLOB,
                      'raw_t0_features_git_blob':RAW_FEATURE_GIT_BLOB,
                      'provider_archive_originals_authenticated_by_paired_events':True},
            'limits':['Retrospective re-use of exposed original synthetic outcomes; hyperparameters/features not preregistered.',
                      'Held-out ecological context shares model-family/functional definitions with training; not natural/external generality.',
                      'Flexible biological/ecological controls chosen after initial comparisons; comparisons are adversarial exploratory sensitivity and model dimensions differ.',
                      'Original 256 paired random streams represent stochastic replicates, not 256 independent island ecological systems.',
                      'The t0 A selection response and A segregation potential do not vary by context; no identified access-delay response clock.',
                      'Conditional paired bootstrap treats fold-fitted predictions as fixed, not a new trial nor parameter-refitting confidence interval.',
                      'All six outcomes and source constraints preserved, no biological reruns.']}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ('compact','t0','paired','out'):
        ap.add_argument('--'+key,type=Path,required=True)
    args=ap.parse_args()
    if args.out.exists():raise ValueError('Existing output must not be overwritten')
    raw=args.compact.read_bytes();fraw=args.t0.read_bytes()
    if blob_sha(raw)!=EXPECTED_INPUT_GIT_BLOB or blob_sha(fraw)!=RAW_FEATURE_GIT_BLOB:
        raise ValueError('Admitted compact/t0 git blobs have drifted')
    paired_raw=args.paired.read_bytes()
    paired_blob='afab849d2f0036d07d28beb1441644f9ca2808cb'
    if blob_sha(paired_raw)!=paired_blob:
        raise ValueError('Original paired event identity differs')
    result=evaluate(json.loads(raw),json.loads(fraw),json.loads(paired_raw))
    result['source']['original_paired_git_blob']=paired_blob
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('x',encoding='utf-8',newline='\n') as output:
        output.write(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':result['status'],'n':result['cases'],
                      'lambda_015_scores':result['results'][1]['scores'],
                      'lambda_015_comp':result['results'][1]['comparisons']},indent=2))
if __name__=='__main__':main()