"""Bounded JOINT endpoint method calibration; no Model3 biological histories.

Six fresh statistical scenarios, including four-binary-arm +/-2 survival
contrasts and dependence between genetic and survival outcomes. Artificial
DGPs are not fitted Model3 distributions; no new biological power claim.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.stats import beta, t
from scripts.q3_joint_inference_20261019 import ph_statistics

ROOT=Path(__file__).resolve().parents[1]
PLAN=ROOT/'docs/protocols/CHAPTER2_JOINT_OC_EXTENSION_FROZEN_20261019.json'


def marginal(mu,variance,support,tails=None):
    values=np.asarray(support,dtype=float)
    if not np.isfinite([mu,variance]).all() or variance<0:
        raise ValueError('invalid moments')
    second=variance+mu*mu
    if len(values)==3 and values.tolist()==[-1.,0.,1.]:
        p=np.array([(second-mu)/2,1-second,(second+mu)/2])
    elif len(values)==5 and values.tolist()==[-2.,-1.,0.,1.,2.] and tails is not None:
        left,right=map(float,tails)
        residual_second=second-4*(left+right)
        residual_mean=mu-2*(right-left)
        pm=(residual_second-residual_mean)/2
        pp=(residual_second+residual_mean)/2
        p=np.array([left,pm,1-left-right-pm-pp,pp,right])
    else: raise ValueError('unsupported support')
    if not np.isfinite(p).all() or min(p)<-1e-12 or abs(p.sum()-1)>1e-12:
        raise ValueError('impossible finite-support moments')
    return np.maximum(p,0)/np.maximum(p,0).sum()


def decode_survival(s):
    """Budget B8,B4.5, policy F,E: valid binary realization of each contrast."""
    s=np.asarray(s)
    if not np.isin(s,[-2,-1,0,1,2]).all(): raise ValueError('bad survival contrast')
    table=np.array([[[0,1],[1,0]],[[1,1],[1,0]],[[1,1],[1,1]],
                    [[1,1],[0,1]],[[1,0],[0,1]]],dtype=np.int8)
    return table[(s+2).astype(int)]


def sample_pair(rng,scenario,batch):
    n=scenario['n']
    shapes=((batch,n,1),(batch,1,n),(batch,n,n))
    uniforms=[rng.random(shape) for shape in shapes]
    selector=rng.random((batch,n,n))
    pair=[]
    for e,support in enumerate(([-1,0,1],[-2,-1,0,1,2])):
        vf,vv,vr=scenario['components'][e];total=vf+vv+vr
        a=np.sqrt(vf/total);b=np.sqrt(vv/total)
        if a+b>1+1e-12: raise ValueError('selector weights impossible')
        p=marginal(scenario['mu'][e],total,support,
                   scenario['S_tail_mass'] if e else None)
        cdf=np.cumsum(p);cdf[-1]=1.
        sources=[np.asarray(support,dtype=np.int8)[np.searchsorted(cdf,
            np.minimum(1-u,np.nextafter(1.,0.)) if e and scenario['coupling']=='opposed' else u,side='right')]
                 for u in uniforms]
        pair.append(np.where(selector<a,sources[0],
                      np.where(selector<a+b,sources[1],sources[2])))
    return np.stack(pair,axis=-1)


def decide_counts(mean,variance,truth,*,critical):
    mean=np.asarray(mean);variance=np.asarray(variance);truth=np.asarray(truth)
    half=critical*np.sqrt(np.maximum(variance,0));valid=variance>0
    pos=valid & (mean-half>0);neg=valid & (mean+half<0)
    null=truth==0
    reject=(pos|neg)&null
    covered=valid & (abs(mean-truth)<=half)
    return dict(positive_each=pos.sum(axis=0).astype(int).tolist(),
        rejected_each=(pos|neg).sum(axis=0).astype(int).tolist(),
        joint_positive=int(pos.all(axis=1).sum()),
        joint_negative=int(neg.all(axis=1).sum()),
        false_reject_any_true_null=int(reject.any(axis=1).sum()),
        simultaneous_coverage=int(covered.all(axis=1).sum()),
        degenerate_each=(~valid).sum(axis=0).astype(int).tolist())


def mc_interval(k,n,alpha):
    return [0. if k==0 else float(beta.ppf(alpha/2,k,n-k+1)),
            1. if k==n else float(beta.ppf(1-alpha/2,k+1,n-k))]


def run(scenario,plan,out):
    sid=scenario['id'];total=plan['replications_per_scenario'];n=scenario['n']
    key=int.from_bytes(hashlib.sha256(sid.encode()).digest()[:8],'big')
    rng=np.random.default_rng(np.random.SeedSequence([20261019,106,key]))
    means=[];variances=[]
    for start in range(0,total,plan['batch_size']):
        x=sample_pair(rng,scenario,min(plan['batch_size'],total-start))
        m,v=ph_statistics(x);means.append(m);variances.append(v)
    means=np.concatenate(means);variances=np.concatenate(variances)
    critical=float(t.ppf(1-.025/2,n-1))
    counts=decide_counts(means,variances,scenario['mu'],critical=critical)
    alpha=plan['MC_simultaneous_alpha_per_interval']
    corr=float(np.corrcoef(means.T)[0,1])
    record=dict(scenario=scenario,replications=total,counts=counts,
        mean_estimates=means.mean(axis=0).tolist(),mean_correlation=corr,
        empirical_variance_of_mean=means.var(axis=0).tolist(),
        known_variance_of_mean=[a/n+b/n+c/n**2 for a,b,c in scenario['components']],
        joint_positive_rate=counts['joint_positive']/total,
        joint_positive_MC_interval=mc_interval(counts['joint_positive'],total,alpha),
        familywise_false_rejection_rate=counts['false_reject_any_true_null']/total,
        familywise_false_rejection_MC_interval=mc_interval(
            counts['false_reject_any_true_null'],total,alpha),
        stats_file=sid+'.npz',Model3_histories=0,confirmation_authorized=False)
    out.mkdir(parents=True,exist_ok=True)
    with (out/(sid+'.npz')).open('xb') as f:
        np.savez_compressed(f,mean=means,variance=variances)
    with (out/(sid+'.json')).open('x') as f:
        json.dump(record,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:record[k] for k in ('scenario','joint_positive_rate',
        'joint_positive_MC_interval','familywise_false_rejection_rate',
        'familywise_false_rejection_MC_interval','mean_correlation')},sort_keys=True),flush=True)
    return record


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--plan-sha',required=True);p.add_argument('--scenario',required=True)
    a=p.parse_args();raw=PLAN.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=a.plan_sha:p.error('frozen plan changed')
    plan=json.loads(raw)
    chosen=[s for s in plan['scenarios'] if s['id']==a.scenario]
    if len(chosen)!=1:p.error('unplanned scenario')
    run(chosen[0],plan,a.out)

if __name__=='__main__':main()
