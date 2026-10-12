"""Explicit diagnostic parent sampler; unchanged biological ledger retained."""
from dataclasses import dataclass
import numpy as np

POLICY='A_mean_equal_uniform_parents'


def equal_parent_weights(outcross,self_viable):
    o=np.asarray(outcross,dtype=float);s=np.asarray(self_viable,dtype=float)
    if (s.ndim!=1 or o.shape!=(len(s),len(s)) or not np.isfinite(o).all()
            or not np.isfinite(s).all() or (o<0).any() or (s<0).any()
            or np.any(np.diag(o)!=0)):
        raise ValueError('invalid native outcross/self returns')
    n=len(s);total_o=float(o.sum());total_s=float(s.sum())
    if not n:
        return np.empty((0,0))
    if n==1 and total_o!=0:raise ValueError('singleton outcross impossible')
    weights=np.zeros((n,n))
    if n>1:
        weights[:]=total_o/(n*(n-1));np.fill_diagonal(weights,0.)
    np.fill_diagonal(weights,total_s/n)
    np.testing.assert_allclose(weights.sum(),total_o+total_s,atol=1e-12,rtol=1e-12)
    np.testing.assert_allclose(np.trace(weights),total_s,atol=1e-12,rtol=1e-12)
    np.testing.assert_allclose(weights.sum(0)+weights.sum(1),np.full(n,2*(total_o+total_s)/n),atol=1e-12,rtol=1e-12)
    return weights


@dataclass(frozen=True)
class SamplingLedger:
    """Only fields consumed by native advance, not a pollen/ovule ledger."""
    outcross: np.ndarray
    self_viable: np.ndarray
    ovules: np.ndarray


def sampling_ledger(native):
    p=equal_parent_weights(native.outcross,native.self_viable)
    s=np.diag(p).copy();o=p.copy();np.fill_diagonal(o,0.)
    return SamplingLedger(o,s,native.ovules.copy())


def tasks():
    from scripts import persistence_expression_mechanism_20261012 as old
    return [dict(block=b,replicate=r,origin=o,target=t,policy=POLICY)
            for b in old.BLOCKS for r in range(512) for o in old.ORIGINS for t in old.TARGETS]


def analyze(occupied,*,bootstrap_count=19999):
    import math
    from scripts import persistence_expression_mechanism_20261012 as old
    x=np.asarray(occupied,float)
    if x.shape!=(2,512,2,3,2) or not np.isfinite(x).all() or not np.isin(x,[0.,1.]).all():
        raise ValueError('complete paired all-start occupancy required')
    if type(bootstrap_count) is not int or bootstrap_count<1:raise ValueError('invalid bootstrap count')
    d=x[...,0]-x[...,1];means=d.mean(axis=(0,1));primary=[]
    radius=4*math.sqrt(math.log(2*4/.05)/(2*1024))
    for j,target in enumerate(old.TARGETS):
        for k,name in enumerate(('controlled_future_parent_selection','residual_reference_contrast')):
            paired=d[:,:,j,k]-d[:,:,j,k+1]
            rng=np.random.default_rng(2026101307+len(primary));draws=np.zeros(bootstrap_count)
            for block in paired:
                draws+=block[rng.integers(0,512,size=(bootstrap_count,512))].mean(1)/2
            lo,hi=np.quantile(draws,[.025/4,1-.025/4]);estimate=float(paired.mean())
            primary.append(dict(target=target,contrast=name,estimate=estimate,
                simultaneous_bootstrap_interval=[float(lo),float(hi)],
                distribution_free_interval=[max(-2.,estimate-radius),min(2.,estimate+radius)],
                block_estimates=paired.mean(1).tolist(),
                decision='positive' if lo>0 else 'negative' if hi<0 else 'unresolved'))
    error=max(abs(primary[2*j]['estimate']+primary[2*j+1]['estimate']-(means[j,0]-means[j,2])) for j in range(2))
    if error>1e-12:raise ArithmeticError('controlled partition does not close')
    return dict(primary=primary,primary_family=4,bootstrap_count=bootstrap_count,
        policy_order=['A_mean_equal_native',POLICY,'original_A_fixed'],
        policy_route_differences=means.tolist(),block_policy_route_differences=d.mean(1).tolist(),
        occupied_counts=x.sum(axis=(0,1)).astype(int).tolist(),partition_closure_error=error,
        inference='All-locus controlled parent weighting contrast; no pure assurance-selection or natural-order mediation.')
