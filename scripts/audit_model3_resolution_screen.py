"""Cheap analytical mutation-resolution screen, NOT a full evolution benchmark."""
import hashlib
import json
from pathlib import Path
import numpy as np
from scripts.model3_island.density import birth_mutation_matrix

ROOT=Path(__file__).resolve().parents[1]
COUNTS=(9,13,17,25,33,49,65,97,129)


def exact_decay(modes,rate,sd,scheme):
    modes=np.asarray(modes,dtype=float)
    exponent=(modes*np.pi*sd)**2/2
    if scheme=='jump':return 1-rate+rate*np.exp(-exponent)
    if scheme=='heat_fv':return np.exp(-rate*exponent)
    raise ValueError('unknown scheme')


def memory_floor(n):
    genotypes=(n*(n+1)//2)**3
    pairs=n**6
    size=genotypes*(6*8+8)+pairs*(8+4)
    return dict(nodes=n,genotypes=genotypes,gamete_pairs=pairs,
        bytes_lower_bound=size,gib_lower_bound=size/2**30)


def assess(n,scheme,horizons=(1,200,1000)):
    x=np.linspace(0,1,n);u=.01;sd=.05
    kernel=birth_mutation_matrix(x,u,sd,scheme)
    primary=np.arange(1,9)
    extra=np.array([m for m in [16,32] if m<=n-1],dtype=int)
    modes=np.r_[primary,extra]
    basis=np.cos(x[:,None]*(modes*np.pi)[None,:])
    eigen=exact_decay(modes,u,sd,scheme)
    rows=[]
    for t in horizons:
        numerical=np.linalg.matrix_power(kernel,t)@basis
        expected=basis*(eigen**t)[None,:]
        error=np.abs(numerical-expected)
        rows.append(dict(birth_events=int(t),primary_max_error=float(error[:,:8].max()),
            modes=[dict(mode=int(m),max_error=float(error[:,i].max()),
                worst_start=float(x[np.argmax(error[:,i])])) for i,m in enumerate(modes)]))
    reference=u*sd**2
    variance=float(kernel[n//2]@((x-.5)**2))
    relative=abs(variance/reference-1)
    maximum=max(r['primary_max_error'] for r in rows)
    return dict(nodes=n,scheme=scheme,spacing=1/(n-1),spacing_over_mutation_sd=1/(n-1)/sd,
        central_variance=variance,variance_reference=reference,variance_relative_error=relative,
        primary_max_error=maximum,screen_pass=bool(relative<.01 and maximum<.01),
        row_mass_max_error=float(np.max(abs(kernel.sum(axis=1)-1))),horizons=rows)


def audit():
    rows=[assess(n,scheme) for n in COUNTS for scheme in ['jump','heat_fv']]
    sources=[Path(__file__),ROOT/'scripts/model3_island/density.py',
        ROOT/'scripts/model3_island/birth_diffusion.py',
        ROOT/'docs/superpowers/plans/2026-10-04-model3-resolution-screen.md']
    minimum={s:next((r['nodes'] for r in rows if r['scheme']==s and r['screen_pass']),None)
        for s in ['jump','heat_fv']}
    return dict(rows=rows,minimum_screened_pass=minimum,memory=[memory_floor(n) for n in COUNTS],
        source_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        exact_reference='Reflecting cosine eigenmodes: jump 1-u+u*exp(-(m*pi*sd)^2/2); heat exp(-u*(m*pi*sd)^2/2)',
        thresholds=dict(primary_modes=list(range(1,9)),horizons=[1,200,1000],max_absolute_mode_error=.01,max_relative_central_variance_error=.01),
        scope='Operator-only engineering screen. First passing candidate is not a minimum required full-model grid. No selection, mating, inheritance or ecological feedback. Does not prove ecological trajectory accuracy or jump-heat equivalence.')


if __name__=='__main__':
    result=audit()
    path=ROOT/'data/results/model3_resolution_screen_20261004.json'
    path.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps(dict(minimum_screened_pass=result['minimum_screened_pass'],
        rows=[{k:r[k] for k in ['nodes','scheme','primary_max_error','variance_relative_error','screen_pass']} for r in result['rows']]),indent=2))
