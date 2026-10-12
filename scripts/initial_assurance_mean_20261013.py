"""Frozen initial-mean intervention; import the existing future operator unchanged."""
from dataclasses import replace
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from scripts import persistence_expression_mechanism_20261012 as old

INPUT_SHA='51a07a843a087059af3d67ad113f5d849644f5b03739a6df986d506bd636648f'
PRIOR_SHA='2f91cf5aca524e61a0c4edff841d269a135267bddd0bc6b7d699efe484eed09e'
OPERATOR_SHA='da8be50f183732f4bafc0cd3f8e5760514911859a96134a3ba61fdf5e2e32d0d'
POLICY='A_mean_equal_native'
TOL=1e-12


def source_gate():
    if old.digest(Path(old.__file__).read_text(encoding='utf-8').encode())!=OPERATOR_SHA:
        raise ValueError('frozen future operator drift')


def equalize_mean(state):
    if len(state.ids)==0:raise ValueError('occupied initial state required')
    aa=state.alleles.copy();before=aa[:,2,:].copy();mean=float(before.mean());shift=.5-mean
    aa[:,2,:]=before+shift
    if (aa[:,2,:]<0).any() or (aa[:,2,:]>1).any():raise ValueError('mean mapping outside unit interval; no clipping')
    after=aa[:,2,:];x=state.alleles.mean(2);y=aa.mean(2)
    xc=x-x.mean(0);yc=y-y.mean(0)
    cov_error=float(np.max(abs(xc.T@xc/len(x)-yc.T@yc/len(y))))
    var_error=max(abs(float(before.var()-after.var())),abs(float(x[:,2].var()-y[:,2].var())))
    mean_error=abs(float(after.mean())-.5)
    if max(cov_error,var_error,mean_error)>TOL:raise ValueError('initial invariance failed')
    treated=replace(state,alleles=aa)
    np.testing.assert_array_equal(treated.alleles[:,:2,:],state.alleles[:,:2,:])
    for f in old.FIELDS[1:]:np.testing.assert_array_equal(getattr(treated,f),getattr(state,f))
    return treated,dict(original_mean=mean,shift=shift,assigned_mean=float(after.mean()),
                        max_covariance_error=cov_error,max_variance_error=var_error,max_mean_error=mean_error)


def tasks():
    return [dict(block=b,replicate=r,origin=o,target=t,policy=POLICY)
            for b in old.BLOCKS for r in range(512) for o in old.ORIGINS for t in old.TARGETS]


def verify_mapping(actual,expected):
    if set(actual)!=set(expected):raise ValueError('mapping summary fields differ')
    for k,v in actual.items():
        if type(v) not in (int,float) or not np.isfinite(v) or abs(v-expected[k])>TOL:
            raise ValueError('mapping quantitative summary differs')
        if k.startswith('max_') and not 0<=v<=TOL:raise ValueError('mapping invariance failed')


def verify_clamp_identity(actual,reference):
    for f in ('population','offsets','parentage','ids','birth_years'):
        np.testing.assert_array_equal(actual[f],reference[f])
    for f in ('alleles','allele_origin','mutation_flags'):
        np.testing.assert_array_equal(actual[f][:,:2,:],reference[f][:,:2,:])
    np.testing.assert_allclose(actual['diagnostics'],reference['diagnostics'],atol=TOL,rtol=0)


def analyze(occupied,*,bootstrap_count=19999):
    x=np.asarray(occupied,float)
    if x.shape!=(2,512,2,3,2) or not np.isfinite(x).all() or not np.isin(x,[0.,1.]).all():
        raise ValueError('complete paired all-start occupancy required')
    if type(bootstrap_count) is not int or bootstrap_count<1:raise ValueError('invalid bootstrap count')
    d=x[...,0]-x[...,1];means=d.mean(axis=(0,1));primary=[]
    radius=4*math.sqrt(math.log(2*4/.05)/(2*1024))
    for j,target in enumerate(old.TARGETS):
        for k,name in enumerate(('initial_mean_component','residual_lifelong_expression')):
            paired=d[:,:,j,k]-d[:,:,j,k+1]
            rng=np.random.default_rng(2026101301+len(primary));draws=np.zeros(bootstrap_count)
            for block in paired:
                draws+=block[rng.integers(0,512,size=(bootstrap_count,512))].mean(1)/2
            lo,hi=np.quantile(draws,[.025/4,1-.025/4]);estimate=float(paired.mean())
            primary.append(dict(target=target,contrast=name,estimate=estimate,
                simultaneous_bootstrap_interval=[float(lo),float(hi)],
                distribution_free_interval=[max(-2.,estimate-radius),min(2.,estimate+radius)],
                block_estimates=paired.mean(1).tolist(),
                decision='positive' if lo>0 else 'negative' if hi<0 else 'unresolved'))
    error=max(abs(primary[2*j]['estimate']+primary[2*j+1]['estimate']-(means[j,0]-means[j,2])) for j in range(2))
    if error>TOL:raise ArithmeticError('controlled partition does not close')
    return dict(primary=primary,primary_family=4,bootstrap_count=bootstrap_count,
                policy_order=['original_native',POLICY,'original_A_fixed'],
                policy_route_differences=means.tolist(),block_policy_route_differences=d.mean(1).tolist(),
                occupied_counts=x.sum(axis=(0,1)).astype(int).tolist(),partition_closure_error=error,
                inference='Post-discovery model/cohort-conditional uncertainty; not independent confirmation or natural-order mediation.')
