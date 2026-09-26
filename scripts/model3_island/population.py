"""Finite inheritance, ancestry, mutation and arrival-aware recruitment."""
from dataclasses import replace
import numpy as np

from .types import PlantState, _integer
from .history import reflect_unit


def subset(state, index):
    return PlantState(**{name:getattr(state,name)[index] for name in
        ('alleles','allele_origin','mutation_flags','ids','birth_years')})


def concatenate(states):
    return PlantState(**{name:np.concatenate([getattr(s,name) for s in states],axis=0)
        for name in ('alleles','allele_origin','mutation_flags','ids','birth_years')})


def inherit(state, mothers, fathers, config, *, segregation_rng, mutation_rng, year: int) -> PlantState:
    _integer(year,'birth year',1)
    mothers=np.asarray(mothers); fathers=np.asarray(fathers)
    n=len(mothers) if mothers.ndim==1 else -1
    if (mothers.ndim!=1 or fathers.shape!=mothers.shape or mothers.dtype.kind not in 'iu'
            or fathers.dtype.kind not in 'iu' or n>config.capacity
            or (mothers<0).any() or (fathers<0).any()
            or (mothers>=len(state.ids)).any() or (fathers>=len(state.ids)).any()):
        raise ValueError('invalid parental indices or retained offspring count')
    if year*config.capacity+n>=2**32:
        raise ValueError('resident offspring ID namespace exhausted')
    maternal=segregation_rng.integers(0,2,size=(n,3))
    paternal=segregation_rng.integers(0,2,size=(n,3))
    loci=np.arange(3)[None,:]
    def transmit(array):
        return np.stack([array[mothers[:,None],loci,maternal],
                         array[fathers[:,None],loci,paternal]],axis=-1)
    alleles=transmit(state.alleles)
    origins=transmit(state.allele_origin)
    flags=transmit(state.mutation_flags)
    if config.mutation_rate and config.mutation_sd:
        mutations=mutation_rng.random(alleles.shape)<config.mutation_rate
        # Fixed-capacity assurance is an intervention, not an evolving third trait.
        if config.assurance_mode=='fixed':
            mutations[:,2,:]=False
        steps=mutation_rng.normal(0,config.mutation_sd,alleles.shape)
        alleles[mutations]=reflect_unit(alleles[mutations]+steps[mutations])
        flags=flags|mutations
    ids=np.arange(year*config.capacity,year*config.capacity+n,dtype=np.int64)
    return PlantState(alleles,origins,flags,ids,np.full(n,year,dtype=np.int64))


def advance(state, ledger, seed_candidates, config, streams, *, year: int):
    _integer(year,'year')
    n=len(state.ids)
    if n>config.capacity or len(ledger.ovules)!=n:
        raise ValueError('population/ledger dimensions inconsistent with capacity')
    if (state.birth_years>year).any() or (seed_candidates.birth_years!=year+1).any():
        raise ValueError('resident ages or seed arrival years inconsistent')
    if np.intersect1d(state.ids,seed_candidates.ids).size:
        raise ValueError('seed candidate IDs must differ from resident IDs')
    parents=ledger.outcross.copy()
    parents[np.diag_indices(n)]+=ledger.self_viable
    total=float(parents.sum())
    if not np.isfinite(total):
        raise ValueError('nonfinite expected reproduction')
    keep=streams['survival'].random(n)<config.survival
    adults=subset(state,keep)
    resident_potential=int(streams['recruitment'].poisson(total))
    settled=streams['seed_settlement'].random(len(seed_candidates.ids))<config.seed_arrival.establishment
    immigrants=subset(seed_candidates,settled)
    immigrant_potential=len(immigrants.ids)
    vacancies=config.capacity-len(adults.ids)
    retained=min(vacancies,resident_potential+immigrant_potential)
    if immigrant_potential and resident_potential and retained:
        resident_count=int(streams['recruitment'].hypergeometric(resident_potential,immigrant_potential,retained))
    else:
        resident_count=min(resident_potential,retained)
    immigrant_count=retained-resident_count
    if resident_count:
        choices=streams['parents'].choice(n*n,size=resident_count,p=parents.ravel()/total)
        fathers,mothers=np.unravel_index(choices,parents.shape)
    else:
        fathers=mothers=np.empty(0,dtype=int)
    children=inherit(state,mothers,fathers,config,segregation_rng=streams['segregation'],
                     mutation_rng=streams['mutation'],year=year+1)
    immigrant_indices=streams['recruitment'].choice(immigrant_potential,size=immigrant_count,replace=False)
    incoming=subset(immigrants,immigrant_indices)
    result=concatenate([adults,children,incoming])
    # Parent age at offspring census; migrants are excluded from this estimate.
    ages=np.stack([year+1-state.birth_years[mothers],year+1-state.birth_years[fathers]],axis=1)
    info=dict(survivors=len(adults.ids),resident_potential=resident_potential,
              immigrant_candidates=len(seed_candidates.ids),immigrant_settled=immigrant_potential,
              resident_recruits=resident_count,immigrant_recruits=immigrant_count,
              parent_age_sum=int(ages.sum()),parent_contributions=int(ages.size))
    return result,info


def resident_seed_control(state, seed_candidates, rng):
    """Counterfactual genotype-matched immigration, keeping immigrant genealogy.

    External origin IDs are retained even when resident genotypes are copied.
    This is a diagnostic intervention, not actual resident descent.
    """
    if not len(state.ids):
        return None,'no_resident_genotype_distribution'
    sampled=rng.integers(0,len(state.ids),size=len(seed_candidates.ids))
    return replace(seed_candidates,alleles=state.alleles[sampled],
                   mutation_flags=state.mutation_flags[sampled]),None
