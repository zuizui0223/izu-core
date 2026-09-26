"""Matched conditional trajectories; histories are generated outside this runner."""
import numpy as np

from .density import density_step, project_state
from .reproduction import reproduce
from .population import advance,resident_seed_control,subset
from .randomness import stream, STREAM_IDS


def simulate(config, history, founders, *, replicate: int, grid, check_budget=None,
             projection_mode='grid',immigration_mode='source') -> dict:
    if projection_mode not in ('grid','continuous') or immigration_mode not in ('source','resident_matched'):
        raise ValueError('unknown numerical or immigration intervention')
    if len(history.visitors)!=config.years or history.event_order!=config.event_order:
        raise ValueError('history length or order differs from configuration')
    if len(founders.ids)>config.capacity or (founders.birth_years>0).any():
        raise ValueError('invalid founders')
    state,counts=project_state(founders,grid)
    initial=state.alleles.copy()
    initial_origins=np.unique(founders.allele_origin)
    streams={name:stream(replicate,name,0) for name in STREAM_IDS}
    t=config.years
    population=np.zeros(t+1,dtype=int)
    trait_mean=np.full((t+1,3),np.nan)
    trait_variance=np.full((t+1,3),np.nan)
    allele_count=np.zeros((t+1,3),dtype=int)
    heterozygosity=np.full((t+1,3),np.nan)
    ancestry=np.full(t+1,np.nan)
    density_mass=np.zeros(t+1)
    density_traits=np.full((t+1,3),np.nan)
    density_trait_variance=np.full((t+1,3),np.nan)
    density_counts=np.zeros((t+1,len(counts)))
    states=[]
    reproductive=np.zeros((t,6))
    density_reproductive=np.zeros((t,6))
    demographic=np.zeros((t,8),dtype=np.int64)
    undefined=np.zeros(t,dtype=bool)
    control_rng=stream(replicate,'source_genotypes',0)
    demographic_keys=('survivors','resident_potential','immigrant_candidates','immigrant_settled',
                      'resident_recruits','immigrant_recruits','parent_age_sum','parent_contributions')
    def record(year):
        states.append(state)
        density_counts[year]=counts
        population[year]=len(state.ids)
        if len(state.ids):
            traits=state.alleles.mean(axis=2)
            trait_mean[year]=traits.mean(axis=0)
            trait_variance[year]=traits.var(axis=0)
            allele_count[year]=[len(np.unique(state.alleles[:,k])) for k in range(3)]
            heterozygosity[year]=(state.alleles[:,:,0]!=state.alleles[:,:,1]).mean(axis=0)
            ancestry[year]=np.isin(state.allele_origin,initial_origins).mean()
        density_mass[year]=counts.sum()
        if counts.sum()>0:
            density_traits[year]=counts @ grid.genotypes.mean(axis=2)/counts.sum()
            density_trait_variance[year]=counts @ (grid.genotypes.mean(axis=2)-density_traits[year])**2/counts.sum()
    def totals(ledger):
        return [ledger.ovules.sum(),ledger.outcross.sum(),ledger.self_raw.sum(),
                ledger.self_viable.sum(),ledger.exported.sum(),ledger.delivered.sum()]
    record(0)
    first_extinction=-1
    recolonizations=0
    for year in range(t):
        if check_budget is not None:
            check_budget()
        old_n=len(state.ids)
        immigrants=history.seed_candidates[year]
        if immigration_mode=='resident_matched' and len(immigrants.ids):
            matched,reason=resident_seed_control(state,immigrants,control_rng)
            if reason is not None:
                # No invented resident genotype after extinction. The contrast is
                # non-evaluable from this point, flagged and retained for auditing.
                undefined[year]=True
                immigrants=subset(immigrants,np.empty(0,dtype=int))
            else:
                immigrants=matched
        if projection_mode=='grid':
            immigrants,_=project_state(immigrants,grid)
        ledger=reproduce(state,history.visitors[year],config)
        counts,density_ledger=density_step(counts,grid,history.visitors[year],immigrants,config)
        reproductive[year]=totals(ledger)
        density_reproductive[year]=totals(density_ledger)
        state,info=advance(state,ledger,immigrants,config,streams,year=year)
        if projection_mode=='grid':
            state,_=project_state(state,grid)
        demographic[year]=[info[key] for key in demographic_keys]
        if old_n and not len(state.ids) and first_extinction<0:
            first_extinction=year+1
        if not old_n and len(state.ids):
            # Initial establishment in an initially empty island is not recolonization.
            recolonizations+=int(first_extinction>=0)
        record(year+1)
    return dict(population=population,trait_mean=trait_mean,trait_variance=trait_variance,
        allele_count=allele_count,heterozygosity=heterozygosity,founder_ancestry=ancestry,
        density_mass=density_mass,density_traits=density_traits,reproductive=reproductive,
        density_counts=density_counts,density_trait_variance=density_trait_variance,
        density_reproductive=density_reproductive,demographic=demographic,
        projection_mode=projection_mode,immigration_mode=immigration_mode,
        resident_control_undefined=undefined,
        visitor_count=np.array([len(v.ids) for v in history.visitors]),
        initial_genotypes=initial,final_genotypes=state.alleles,final_allele_origin=state.allele_origin,
        final_ids=state.ids,final_birth_years=state.birth_years,final_density_counts=counts,
        final_mutation_flags=state.mutation_flags,
        state_offsets=np.r_[0,np.cumsum(population)],
        state_alleles=np.concatenate([s.alleles for s in states]),
        state_allele_origin=np.concatenate([s.allele_origin for s in states]),
        state_mutation_flags=np.concatenate([s.mutation_flags for s in states]),
        state_ids=np.concatenate([s.ids for s in states]),
        state_birth_years=np.concatenate([s.birth_years for s in states]),
        extinction_year=first_extinction,recolonizations=recolonizations,
        demographic_keys=np.array(demographic_keys),
        reproductive_keys=np.array(['ovules','outcross','self_raw','self_viable','exported','delivered']))
