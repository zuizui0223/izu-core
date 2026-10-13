"""Exploratory, context-held-out six-class initial-response prediction audit.

Predictors are t0 source genotypes, ecology and original t0 full-parent Price
response only. No future state (including stochastic replicate ID) enters model
features. The 2,304 outcomes are *aggregates* of shared-seed context panels:
leave-one-context-out evaluates contextual interpolation/extrapolation, NOT an
independent-seed test or a prospectively verified two-trait evolutionary clock.
The assurance F1 segregation variance is constant in this cohort, and the t0
assurance Price response is exactly zero. No assurance response-time estimator
is claimed. Do not pool the 2,304 entries as independent ecological histories.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp

from scripts.audit_chapter2_initial_clock_identifiability_20261013 import (
    CLASSES, EXPECTED_INPUT_GIT_BLOB, admit,
)

RAW_FEATURE_GIT_BLOB = 'ac6cf64f7c190a03d9c6a5a74105fdea75c719cd'
LAMBDAS = (0.025, 0.15, 0.6)  # exploratory sensitivity; primary display is 0.15
MODEL_NAMES = ('prevalence', 'ecology', 'genetic_access',
               'ecology_genetics', 'ecology_genetics_quadratic', 'ecology_genetics_price')
CUTOFF = 0.05


def blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def ingest(summary: dict, features: dict) -> list[dict]:
    """Fail closed against altered ecological labels, source states and use of later predictors."""
    rows = admit(summary)
    if features.get('status') != 'ALL2304_ORIGINAL_INITIAL_FEATURES_ADMITTED' or (
        features.get('original_starts') != 2304 or features.get('founder_contexts') != 18 or
        not features.get('replicated_t0_invariance_verified') or
        features.get('execution', {}).get('conclusion') != 'success' or
        features.get('execution', {}).get('no_biological_simulation') is not True
    ):
        raise ValueError('Raw t0 feature audit did not pass source admission')
    feat_rows = features.get('original_raw_t0_feature_rows')
    if not isinstance(feat_rows, list) or len(feat_rows) != 18:
        raise ValueError('Expected exactly 18 source-only features')
    by_key = {}
    for row in feat_rows:
        if not isinstance(row, dict):
            raise ValueError('Invalid original feature entry')
        key = (row.get('block'), row.get('context'))
        if key in by_key:
            raise ValueError('Repeated feature cell')
        by_key[key] = row
    out = []
    for c in rows:
        key = (c['block'], c['context'])
        raw = by_key.pop(key, None)
        if raw is None:
            raise ValueError('Unmatched original t0 cell')
        f = raw.get('time0_only')
        if not isinstance(f, dict):
            raise ValueError('Missing raw-feature-only certificate')
        required = ('I_variance_allelic_proxy', 'I_variance_expressed',
                    'A_variance_expressed', 'A_variance_allelic_proxy',
                    'A_expected_F1_Mendelian_variance_no_mutation',
                    't0_expected_I_response', 't0_expected_A_response',
                    'founder_mean_I', 'founder_mean_A')
        if not all(type(f.get(k)) in (int, float) and math.isfinite(f[k]) for k in required):
            raise ValueError('Invalid t0 numeric feature')
        if f['A_variance_expressed'] != 0 or f['t0_expected_A_response'] != 0:
            raise ValueError('Impossible nonzero t0 assurance response')
        if abs(f['A_expected_F1_Mendelian_variance_no_mutation']-0.001953125)>1e-14:
            raise ValueError('Mendelian access changed')
        if f['founder_mean_A'] != 0.5:
            raise ValueError('Assurance founder value drift')
        if f['I_variance_allelic_proxy'] <= 0 or f['I_variance_expressed'] <= 0:
            raise ValueError('Nonpositive original I variance')
        if raw.get('starts') != 128 or raw.get('supply') is None:
            raise ValueError('Raw feature/exposure pairing unavailable')
        context = c['context']
        # Original context table is authoritative, not an after-the-fact annotation.
        supply = (0., .03125, .03125, .125, .125, .5, .5, 1., 1.)[context]
        composition = ('empty','matched','separated','matched','separated',
                       'matched','separated','matched','separated')[context]
        if raw.get('supply') != supply or raw.get('composition') != composition:
            raise ValueError('Original t0 ecological context drift')
        obs = np.asarray([c['categories'][k] for k in CLASSES], dtype=np.float64)
        if obs.sum()!=128:
            raise ValueError('Original six-event partition corrupted')
        out.append(dict(block=c['block'], context=context, supply=supply,
                        composition=composition, f={k:float(f[k]) for k in required},
                        counts=obs))
    if by_key:
        raise ValueError('Unexpected extra source genotype cell')
    return out


def features(row: dict, model: str) -> np.ndarray:
    """Only pre-outcome ecological context, founders and exact t0 source response.

    t0 genetic A variance is common to every condition, hence does not
    identify an A access-time effect. Adding it would duplicate the intercept.
    """
    if model not in MODEL_NAMES:
        raise ValueError('Unknown read-only predictor family')
    if model == 'prevalence':
        return np.empty(0, dtype=float)
    s = float(row['supply'])
    sep = float(row['composition']=='separated')
    occupied = float(s > 0)
    log_s = math.log1p(16 * s)
    eco = np.array([log_s, occupied, sep, sep*log_s], dtype=float)
    genetic = np.array([row['f']['I_variance_allelic_proxy']], dtype=float)
    # Signed exact t0 Price response per original reproductive update, divided
    # by 0.05 solely to make its size interpretable as a first-step response ratio.
    # This is NOT a fitted t0 beta or a predicted A/I first passage.
    price = np.array([row['f']['t0_expected_I_response']/CUTOFF], dtype=float)
    if model == 'ecology':return eco
    if model == 'genetic_access':return genetic
    if model == 'ecology_genetics':return np.concatenate([eco,genetic])
    if model == 'ecology_genetics_quadratic':
        return np.concatenate([eco,genetic,np.array([log_s*log_s])])
    return np.concatenate([eco,genetic,price])


def feature_matrix(rows: list[dict], model: str, train_idx: list[int], test_idx: list[int]):
    mat = np.vstack([features(row,model) for row in rows]) if model != 'prevalence' else np.empty((len(rows), 0))
    if mat.shape[1] == 0:
        return np.ones((len(train_idx),1)),np.ones((len(test_idx),1))
    avg = mat[train_idx].mean(axis=0)
    scale = mat[train_idx].std(axis=0)
    scale = np.where(scale > 1e-12, scale, 1.0)
    # No imputation, scaling, or encoding using heldout context outcomes.
    def expand(ind):return np.column_stack([np.ones(len(ind)),(mat[ind]-avg)/scale])
    return expand(train_idx), expand(test_idx)


def train_multinomial(X:np.ndarray, Y:np.ndarray, regularization:float) -> np.ndarray:
    """Weighted aggregate multinomial logit, 5 logits plus reference class.

    Per-cell counts are divided by 128, preventing nested replicates from
    falsely weakening the fixed L2 regularizer. L-BFGS with analytic gradient.
    """
    if regularization <= 0 or X.ndim!=2 or Y.shape!=(len(X),6):
        raise ValueError('Invalid aggregate fit')
    yy = Y/128
    n = len(yy)
    q = X.shape[1]
    totals = yy.sum(axis=0) + 0.5 # finite intercept at rare event classes
    init = np.zeros((q,5))
    init[0] = np.log(totals[:5]/totals[5])
    def objective(p):
        B=p.reshape(q,5)
        logits=np.column_stack([X@B,np.zeros(n)])
        lse=logsumexp(logits,axis=1)
        logp=logits-lse[:,None]
        p6=np.exp(logp)
        loss=(lse*yy.sum(axis=1)-(yy*logits).sum(axis=1)).mean()
        grad=X.T@(p6[:,:5]*yy.sum(axis=1)[:,None]-yy[:,:5])/n
        penalty=0.5*regularization*np.square(B[1:]).sum()
        grad[1:]+=regularization*B[1:]
        return float(loss+penalty), (grad.ravel())
    result=minimize(objective,init.ravel(),jac=True,method='L-BFGS-B',
                    options={'maxiter':1500,'ftol':1e-13,'gtol':1e-9})
    if not result.success and np.max(np.abs(result.jac))>1e-6:
        raise ValueError(f'Multinomial fit did not converge: {result.message}')
    return result.x.reshape(q,5)


def predict(X:np.ndarray, B:np.ndarray) -> np.ndarray:
    logits=np.column_stack([X@B,np.zeros(len(X))]);z=np.exp(logits-logsumexp(logits,axis=1)[:,None])
    if z.shape != (len(X),6) or np.any(z<=0) or not np.allclose(z.sum(axis=1),1,atol=1e-12):
        raise ValueError('Invalid predictive probabilities')
    return z


def proper_score(probs:np.ndarray, counts:np.ndarray):
    if probs.shape!=counts.shape or probs.shape[-1]!=6:
        raise ValueError('Predictive score requires six classes')
    # Aggregated counts are exact sufficient statistics for scoring a constant
    # probability prediction within a unique t0 founder/context cell.
    n=counts.sum()
    logloss = -float(np.sum(counts*np.log(np.clip(probs,1e-200,1))))/n
    brier = float(np.sum((probs*probs).sum(axis=1)*counts.sum(axis=1)
                 -2*np.sum(probs*counts,axis=1)+counts.sum(axis=1)).sum())/n
    top=np.argmax(probs,axis=1)
    correct=sum(counts[i,k] for i,k in enumerate(top))
    return {'log_loss':logloss,'brier':brier,'argmax_accuracy':float(correct/n),
            'correct':int(correct),'n':int(n)}


def leave_one_context_out(rows:list[dict], lam:float):
    if len(rows)!=18 or len({(r['block'],r['context']) for r in rows})!=18:
        raise ValueError('Expected original 18 distinct profiles')
    raw=np.vstack([r['counts'] for r in rows]);pred={m:np.empty((18,6)) for m in MODEL_NAMES}
    folds=[]
    for ctx in range(9):
        test=[i for i,r in enumerate(rows) if r['context']==ctx]
        train=[i for i,r in enumerate(rows) if r['context']!=ctx]
        if len(test)!=2 or len(train)!=16 or len({r['block'] for r in (rows[i] for i in test)})!=2:
            raise ValueError('Must hold out BOTH founders at the same ecological context')
        fold={'context':ctx,'heldout_profile_keys':[rows[i]['block'] for i in test]}
        for model in MODEL_NAMES:
            xt, xv=feature_matrix(rows,model,train,test)
            beta=train_multinomial(xt,raw[train],lam)
            pred[model][test] = predict(xv,beta)
            fold[model]=proper_score(pred[model][test],raw[test])
        folds.append(fold)
    performance={m:proper_score(p,raw) for m,p in pred.items()}
    base=performance['ecology_genetics']
    flexible=performance['ecology_genetics_quadratic']
    price=performance['ecology_genetics_price']
    return dict(lambda_value=lam,model_scores=performance,
                delta_add_t0_price_vs_ecology_genetics={
                    'log_loss_reduction':base['log_loss']-price['log_loss'],
                    'brier_reduction':base['brier']-price['brier'],
                    'argmax_accuracy_change':price['argmax_accuracy']-base['argmax_accuracy']},
                delta_add_t0_price_vs_equal_complexity_quadratic={
                    'log_loss_reduction':flexible['log_loss']-price['log_loss'],
                    'brier_reduction':flexible['brier']-price['brier'],
                    'argmax_accuracy_change':price['argmax_accuracy']-flexible['argmax_accuracy']},
                fold_results=folds)


def run(summary:dict, raw_features:dict) -> dict:
    rows=ingest(summary,raw_features)
    prediction_results=[leave_one_context_out(rows,lam) for lam in LAMBDAS]
    return dict(
        schema='chapter2_initial_clock_leave_context_out_exploratory_v1',
        status='EXPLORATORY_CONTEXT_HELD_OUT_AGGREGATE_PROPER_SCORE_NOT_GENETIC_CLOCK_CONFIRMED',
        cohorts={'cells':18,'founder_blocks':2,'ecological_contexts':9,
                 'repeats_per_cell':128,'case_observations':2304,
                 'independent_initial_conditions':18,
                 'reused_seeds_across_contexts':True},
        outcome_categories=list(CLASSES),
        score_direction='Lower log-loss and Brier are better; every original outcome retained.',
        feature_contract={'shared_A_F1_Mendelian_variance':0.001953125,
                          't0_A_selection_response':0.0,
                          't0_A_clock_estimable':False,
                          't0_I_price_response':True,
                          'selection_mediator_causal_tested':False},
        holdout='All 128 replicates from BOTH founders for one ecological context held out per fold; seeds across contexts are reused, so folds are not independent visitor histories.',
        regularization={'main_lambda':0.15,'sensitivity_lambdas':list(LAMBDAS),'aggregation':'counts per 128, L2 on slopes'},
        results=prediction_results,
        inferential_limits=[
            'Exploratory post-outcome model family choices, not preregistered.',
            'Aggregated category counts do not provide paired seed-level covariance; no confidence interval/p value is available.',
            'Only two fixed founder genotype profiles and constant A F1 variance; cannot identify access-width effect or a two-trait first passage clock.',
            'Heldout ecological contexts share replicate random numbers with train contexts: contextual transfer, not new independent-history validation.',
            'A shared founder/context can show different stochastic outcomes with identical initial predictors.',
            'No genetically unique response onset, mutation effect, natural sequence persistence mediator or natural species calibration.',
        ]
    )


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--compact',type=Path,required=True)
    p.add_argument('--t0',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    if a.out.exists():raise ValueError('Output overwrite forbidden')
    sc=a.compact.read_bytes();rr=a.t0.read_bytes()
    if blob_sha(sc)!=EXPECTED_INPUT_GIT_BLOB or blob_sha(rr)!=RAW_FEATURE_GIT_BLOB:
        raise ValueError('Historical compact or original source t0 blob changed')
    result=run(json.loads(sc),json.loads(rr))
    result['source']={'compact_git_blob':EXPECTED_INPUT_GIT_BLOB,'t0_git_blob':RAW_FEATURE_GIT_BLOB,
                      'raw_history_sha256':'819741aa4a9f5bc1aaf2dadddbd56b79d158fc9295d07fc3bffe362693fc056a',
                      'no_new_biological_trajectories':True}
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open("x", encoding="utf-8", newline="\n") as output:
        output.write(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':result['status'],'main_lambda':0.15,
                      'main_scores':result['results'][1]['model_scores'],
                      'sensitivity':[{ 'lambda':x['lambda_value'],
                          'delta':x['delta_add_t0_price_vs_ecology_genetics']} for x in result['results']]},indent=2))

if __name__=='__main__':main()
