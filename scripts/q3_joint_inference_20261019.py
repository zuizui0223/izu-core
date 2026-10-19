"""Candidate Q3 analysis: complete crossed backgrounds, four survival arms.

No biological runner. Pigeonhole conditional variance is exact; t-reference
confidence coverage is NOT exact or guaranteed for all array distributions.
"""
from __future__ import annotations
import numpy as np
from scipy.stats import t


def contrasts(genetic_loss, occupancy):
    """Policy order F,E; budget order B8,B4.5. Never drop extinct cases.

    Genetic inputs are FIRST genetic-loss-before-extinction indicators, not
    terminal zero-filled traits. Upstream genotype/event audit is mandatory.
    """
    g=np.asarray(genetic_loss); s=np.asarray(occupancy)
    if (g.ndim!=3 or g.shape[-1]!=2 or s.shape!=g.shape[:2]+(2,2)
        or not np.isin(g,[0,1]).all() or not np.isin(s,[0,1]).all()):
        raise ValueError('complete binary F x V x policy/budget arrays required')
    g=g.astype(float);s=s.astype(float)
    return np.stack((g[...,1]-g[...,0],
                     (s[...,1,1]-s[...,1,0])-(s[...,0,1]-s[...,0,0])),axis=-1)


def ph_statistics(x):
    """Input batch,F,V,endpoint; output means and conditional bootstrap variance."""
    x=np.asarray(x,dtype=float)
    if x.ndim!=4 or min(x.shape[1:3])<2 or not np.isfinite(x).all():
        raise ValueError('finite batch x F x V x endpoint array required')
    _,nf,nv,_=x.shape
    mean=x.mean(axis=(1,2))
    r=x.mean(axis=2)-mean[:,None,:]
    c=x.mean(axis=1)-mean[:,None,:]
    ssr=np.square(r).sum(axis=1);ssc=np.square(c).sum(axis=1)
    sst=np.maximum(np.square(x).sum(axis=(1,2))-nf*nv*mean**2,0.)
    sse=np.maximum(sst-nv*ssr-nf*ssc,0.)
    return mean, ssr/nf**2+ssc/nv**2+sse/(nf*nv)**2


def summarize(differences, *, margin=.10):
    """Two 97.5% marginal candidate intervals; not execution authorization."""
    d=np.asarray(differences,dtype=float)
    if (d.ndim!=3 or d.shape[-1]!=2 or min(d.shape[:2])<3
        or not np.isfinite(d).all() or np.any(abs(d[...,0])>1)
        or np.any(abs(d[...,1])>2) or not 0<float(margin)<=2):
        raise ValueError('invalid complete paired contrasts or margin')
    means,var=ph_statistics(d[None])
    critical=float(t.ppf(1-.025/2,min(d.shape[:2])-1))
    out=[]
    for k,name in enumerate(('genetic_loss','survival_interaction')):
        m=float(means[0,k]);v=float(var[0,k]);h=critical*np.sqrt(v)
        valid=v>0
        lo=m-h;hi=m+h
        out.append(dict(name=name,estimate=m,variance=v,
            interval=[float(lo),float(hi)] if valid else None,
            classification=('degenerate_unresolved' if not valid else
                'positive' if lo>0 else 'negative' if hi<0 else 'unresolved'),
            exceeds_positive_margin=bool(valid and lo>margin),
            within_equivalence_band=bool(valid and lo>=-margin and hi<=margin)))
    return dict(method='pigeonhole_variance_t_candidate',independent_axes=list(d.shape[:2]),
        familywise_alpha=.05,marginal_confidence=.975,df=min(d.shape[:2])-1,
        proposed_margin=margin,endpoints=out,
        joint_positive=all(x['classification']=='positive' for x in out),
        both_exceed_margin=all(x['exceeds_positive_margin'] for x in out),
        execution_authorized=False,
        scope='Conditional empirical variance; t intervals have no universal finite-sample guarantee.')
