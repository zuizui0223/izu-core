"""One bounded future, retaining raw states for independent readback.

Library only: no source loading, manifest execution or production entrypoint.
Production authorization and archive admission remain separate pending gates.
"""
from dataclasses import asdict

import numpy as np

from scripts.model3_island.population import advance, subset
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.reproduction import reproduce
from scripts.readaptation_assay_20261019 import assay_population
from scripts.readaptation_transfer_20261019 import STATE_FIELDS, cohort_digest


DEMOGRAPHIC_KEYS=('survivors','resident_potential','immigrant_candidates',
                  'immigrant_settled','resident_recruits','immigrant_recruits',
                  'parent_age_sum','parent_contributions',
                  'resident_selfed_recruits','resident_outcross_recruits')
REPRODUCTIVE_KEYS=('ovules','outcross','self_raw','self_viable','exported','delivered')


def run_future(cohort, config, visitors, stream_key, horizon):
    """Run exactly 80 updates, without projecting or editing inherited genotypes."""
    expected=dict(capacity=48,years=80,assurance_mode='evolving',assurance_cost=.5,
                  assurance_timing='delayed',pollen_discount=0,depression=.5,
                  survival=0,mutation_rate=0,ovule_budget=8,activity_mode='fixed')
    if any(getattr(config,k)!=v for k,v in expected.items()):
        raise ValueError('future configuration differs from bounded design')
    if type(horizon) is not int or horizon!=80:
        raise ValueError('future horizon must be 80')
    if config.seed_arrival.supply!=0 or config.visitor_arrival.supply!=0:
        raise ValueError('future requires no immigration or visitor arrivals')
    if len(cohort.ids)>12 or (cohort.birth_years!=0).any():
        raise ValueError('invalid entry cohort')
    if len(visitors.ids)==0:
        valid_destination=config.activity==0
    else:
        valid_destination=(len(visitors.ids)==6 and config.activity in (.25,1)
                           and (np.all(visitors.optima==.5) or np.all(visitors.optima==.7))
                           and np.all(visitors.breadths==.2)
                           and np.all(visitors.effectiveness==1))
    if not valid_destination:
        raise ValueError('destination differs from bounded design')
    streams={name:stream(stream_key,name,0) for name in STREAM_IDS}
    empty=subset(cohort,np.empty(0,dtype=int))
    state=cohort
    states=[state]
    parents=[]
    demographic=[]
    reproductive=[]
    for year in range(horizon):
        ledger=reproduce(state,visitors,config)
        reproductive.append([float(getattr(ledger,k).sum()) for k in REPRODUCTIVE_KEYS])
        state,info=advance(state,ledger,empty,config,streams,year=year)
        states.append(state)
        parents.append(info['parentage'])
        demographic.append([info[k] for k in DEMOGRAPHIC_KEYS])
    population=np.array([len(s.ids) for s in states],dtype=np.int64)
    mean=np.full((81,3),np.nan)
    variance=mean.copy()
    lower=mean.copy(); upper=mean.copy()
    for t,s in enumerate(states):
        if len(s.ids):
            traits=s.alleles.mean(axis=2)
            mean[t]=traits.mean(axis=0)
            variance[t]=traits.var(axis=0)
            lower[t]=s.alleles.min(axis=(0,2))
            upper[t]=s.alleles.max(axis=(0,2))
    empty_times=np.flatnonzero(population==0)
    result=dict(schema='readaptation_future_v1',stream_key=int(stream_key),
                config=asdict(config),
                visitors={k:getattr(visitors,k).tolist() for k in
                          ('ids','optima','breadths','effectiveness')},
                horizon=horizon,population=population,trait_mean=mean,
                trait_variance=variance,allele_min=lower,allele_max=upper,
                first_extinction=int(empty_times[0]) if len(empty_times) else None,
                state_offsets=np.r_[0,np.cumsum(population)],
                state_sha256=[cohort_digest(s) for s in states],
                parentage=np.concatenate(parents),
                parentage_offsets=np.r_[0,np.cumsum([len(p) for p in parents])],
                parentage_keys=['child_id','mother_id','father_id'],
                reproductive=np.asarray(reproductive),reproductive_keys=list(REPRODUCTIVE_KEYS),
                demographic=np.asarray(demographic,dtype=np.int64),
                demographic_keys=list(DEMOGRAPHIC_KEYS),
                assays={'0':assay_population(cohort,config,visitors),
                        '80':assay_population(state,config,visitors)})
    for name in STATE_FIELDS:
        result['state_'+name]=np.concatenate([getattr(s,name) for s in states])
    return result
