"""Raw arithmetic/inheritance audit. Imports neither model nor producer.

Single-future admission only; full allocation/archive admission remains separate.
Reproductive probabilities and assay biology require native replay, not this audit.
"""
import hashlib
import json

import numpy as np


FIELDS=('alleles','allele_origin','mutation_flags','ids','birth_years')


def require(condition,message):
    if not condition:
        raise ValueError(message)


def raw_state_digest(d,t):
    digest=hashlib.sha256()
    start,end=d['state_offsets'][t:t+2]
    for name in FIELDS:
        a=np.ascontiguousarray(d['state_'+name][start:end])
        header=json.dumps([name,a.shape,a.dtype.str],sort_keys=True,
                          separators=(',',':'),allow_nan=False).encode()
        digest.update(header); digest.update(a.tobytes())
    return digest.hexdigest()


def _assay(a,n):
    require(a['population']==n and a['occupied']==bool(n)
            and a['reference_competitors']==47,'assay population/context')
    names=('maternal_outcross','paternal_outcross','viable_self','genetic_return')
    v=[np.asarray(a[k],dtype=float) for k in names]
    require(all(x.shape==(n,) and np.isfinite(x).all() and (x>=0).all() for x in v),
            'assay component shape or value')
    require(np.allclose(.5*v[0]+.5*v[1]+v[2],v[3],rtol=0,atol=1e-12),'assay return')
    if n:
        require(np.isclose(a['mean_genetic_return'],v[3].mean(),rtol=0,atol=1e-12),'assay mean')
    else:
        require(a['mean_genetic_return'] is None,'empty assay must be undefined')
    return a['mean_genetic_return']


def audit_future(d):
    require(d['schema']=='readaptation_future_v1' and d['horizon']==80,'future schema/horizon')
    pop=np.asarray(d['population'])
    require(pop.shape==(81,) and pop.dtype.kind in 'iu' and ((pop>=0)&(pop<=48)).all(),
            'population inventory')
    offsets=np.asarray(d['state_offsets'])
    require(offsets.dtype.kind in 'iu' and np.array_equal(offsets,np.r_[0,np.cumsum(pop)]),'state offsets')
    total=int(pop.sum())
    for name in FIELDS:
        a=np.asarray(d['state_'+name])
        shape=(total,3,2) if name in FIELDS[:3] else (total,)
        kind='f' if name=='alleles' else 'b' if name=='mutation_flags' else 'iu'
        require(a.shape==shape and a.dtype.kind in kind,'raw state shape/type')
    alleles=d['state_alleles']; origins=d['state_allele_origin']; flags=d['state_mutation_flags']
    require(np.isfinite(alleles).all() and ((alleles>=0)&(alleles<=1)).all(),'allele range')
    require(len(d['state_sha256'])==81,'missing census digest')
    parent_offsets=np.asarray(d['parentage_offsets'])
    require(parent_offsets.dtype.kind in 'iu' and
            np.array_equal(parent_offsets,np.r_[0,np.cumsum(pop[1:])]),'parent offsets')
    parents=np.asarray(d['parentage'])
    require(parents.shape==(int(pop[1:].sum()),3) and parents.dtype.kind in 'iu','parent inventory')
    means=np.full((81,3),np.nan)
    variances=means.copy(); lows=means.copy(); highs=means.copy()
    for t in range(81):
        lo,hi=offsets[t:t+2]
        require(raw_state_digest(d,t)==d['state_sha256'][t],'state digest mismatch')
        ids=d['state_ids'][lo:hi]
        require(len(set(ids))==len(ids),'duplicate individual IDs')
        require(np.all(d['state_birth_years'][lo:hi]==t),'birth census mismatch')
        if pop[t]:
            traits=alleles[lo:hi].mean(axis=2)
            means[t]=traits.mean(axis=0); variances[t]=traits.var(axis=0)
            lows[t]=alleles[lo:hi].min(axis=(0,2)); highs[t]=alleles[lo:hi].max(axis=(0,2))
        if t:
            p=parents[parent_offsets[t-1]:parent_offsets[t]]
            require(np.array_equal(p[:,0],ids),'child IDs mismatch')
            oldlo,oldhi=offsets[t-1:t+1]
            lookup={int(v):oldlo+i for i,v in enumerate(d['state_ids'][oldlo:oldhi])}
            for i,row in enumerate(p):
                for side,parent_id in enumerate(row[1:]):
                    require(int(parent_id) in lookup,'missing parent')
                    parent=lookup[int(parent_id)]
                    for locus in range(3):
                        require(any(alleles[lo+i,locus,side]==alleles[parent,locus,k]
                                    and origins[lo+i,locus,side]==origins[parent,locus,k]
                                    and flags[lo+i,locus,side]==flags[parent,locus,k]
                                    for k in range(2)),'inheritance mismatch')
    for key,expected in [('trait_mean',means),('trait_variance',variances),
                         ('allele_min',lows),('allele_max',highs)]:
        observed=np.asarray(d[key])
        require(observed.shape==expected.shape and np.allclose(observed,expected,rtol=0,
                atol=1e-12,equal_nan=True),'trait summary mismatch')
    absent=np.flatnonzero(pop==0)
    extinction=int(absent[0]) if len(absent) else None
    require(d['first_extinction']==extinction,'extinction time mismatch')
    require(extinction is None or not pop[extinction:].any(),'reappearance without immigration')
    first=_assay(d['assays']['0'],int(pop[0]))
    last=_assay(d['assays']['80'],int(pop[-1]))
    return dict(status='PASS_RAW_STATE_ARITHMETIC',initial_population=int(pop[0]),
                final_population=int(pop[-1]),occupied=bool(pop[-1]),first_extinction=extinction,
                change=(means[-1]-means[0]).tolist() if pop[0] and pop[-1] else None,
                assay_change=last-first if first is not None and last is not None else None,
                limitation='No allocation admission or biological probability replay')
