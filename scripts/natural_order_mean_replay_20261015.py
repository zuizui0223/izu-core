"""Separately written consumer; reuses frozen native kernels, not producer trajectory."""
import hashlib
import json

import numpy as np

from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.types import PlantState
from scripts.model3_island.population import advance, subset
from scripts.model3_island.randomness import stream, STREAM_IDS

FIELDS = ('alleles', 'allele_origin', 'mutation_flags', 'ids', 'birth_years')


def independent_initial(state):
    copied = {f: getattr(state, f).copy() for f in FIELDS}
    before = state.alleles[:, 2, :]
    offset = .5 - float(before.mean())
    copied['alleles'][:, 2, :] = before + offset
    after = copied['alleles'][:, 2, :]
    if not np.isfinite(after).all() or (after < 0).any() or (after > 1).any():
        raise ValueError('independent mean mapping infeasible; clipping forbidden')
    candidate = PlantState(**copied)
    if abs(candidate.alleles[:, 2, :].mean()-.5) > 1e-12:
        raise ValueError('independent assigned mean mismatch')
    old = state.alleles.mean(2)
    new = candidate.alleles.mean(2)
    for col in range(3):
        for other in range(3):
            a = np.mean((old[:,col]-old[:,col].mean())*(old[:,other]-old[:,other].mean()))
            b = np.mean((new[:,col]-new[:,col].mean())*(new[:,other]-new[:,other].mean()))
            if abs(a-b)>1e-12:
                raise ValueError('independent covariance check')
    return candidate


def replay(initial, visitors, config, task, *, horizon=200):
    key = {'study': 'history', 'block': task['block'], 'replicate': task['replicate']}
    raw = ('resolution-v1-20261011:challenge'+json.dumps(key,sort_keys=True)).encode()
    master = int.from_bytes(hashlib.sha256(raw).digest()[:16], 'big')
    streams = {name: stream(master,name,0) for name in STREAM_IDS}
    state = independent_initial(initial)
    no_arrivals = subset(initial,np.array([],dtype=int))
    saved = {f: [] for f in FIELDS}
    sizes=[]; boundaries=[0]; trait_means=[]; diagnostics=[]; parents=[]
    for census in range(horizon+1):
        n=len(state.ids);sizes.append(n);boundaries.append(boundaries[-1]+n)
        trait_means.append(state.alleles.mean(axis=(0,2)) if n else np.full(3,np.nan))
        for f in FIELDS:saved[f].append(getattr(state,f).copy())
        if census==horizon:break
        ledger=reproduce_kb(state,visitors,config,background_denominator_capacity=48)
        state,info=advance(state,ledger,no_arrivals,config,streams,year=200+census,
                           mutation_traits=(False,True,True))
        parents.append(info['parentage'])
        diagnostics.append([ledger.maternal.sum(),ledger.outcross.sum(),ledger.self_raw.sum(),
            ledger.self_viable.sum(),ledger.ovules.sum(),ledger.exported.sum(),ledger.delivered.sum(),
            info['resident_potential'],info['resident_recruits'],info['resident_selfed_recruits'],
            info['resident_outcross_recruits']])
    result={f:np.concatenate(saved[f]) for f in FIELDS}
    result.update(population=np.array(sizes),offsets=np.array(boundaries),means=np.array(trait_means),
                  diagnostics=np.array(diagnostics),parentage=np.concatenate(parents))
    return result
