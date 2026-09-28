"""Exogenous seed/visitor arrival histories and exposure-order interventions."""
from dataclasses import replace
import numpy as np

from .types import Config, History, PlantState, VisitorState
from .randomness import stream


def reach_probability(distance: float, scale: float, kernel: str) -> float:
    if not np.isfinite([distance,scale]).all() or distance<0 or scale<=0:
        raise ValueError('distance must be nonnegative and scale positive')
    if kernel=='exponential':
        return float(np.exp(-distance/scale))
    if kernel=='heavy_tail':
        return float((1+distance/scale)**-2)
    raise ValueError('unknown reach kernel')


def reflect_unit(values):
    """Reflect steps at 0 and 1 rather than accumulating mass by clipping."""
    values=np.asarray(values,dtype=float)
    if not np.isfinite(values).all():
        raise ValueError('reflection requires finite values')
    return 1-np.abs(np.mod(values,2)-1)


def make_history(config: Config, *, seed: int, inherited_visitors=None) -> History:
    # Explicit ID namespace, distinct across histories and from low-ID residents.
    # Bound is a storage constraint, not a limit on random generator capability.
    if isinstance(seed,(bool,np.bool_)) or not isinstance(seed,(int,np.integer)) or not 0<=seed<2**31-1:
        raise ValueError('history seed must be an integer in [0,2**31-1)')
    block=(int(seed)+1)*2**32
    seeds_next=block
    visitors_next=block
    if config.background_resources==0 and (config.initial_visitors or
            config.visitor_arrival.supply*config.visitor_arrival.establishment>0):
        raise ValueError('visitor establishment requires declared background resources')
    visitor_rng=stream(seed,'visitor_arrivals',0)
    initial_rng=stream(seed,'visitor_initial',0)
    loss_rng=stream(seed,'visitor_loss',0)
    settlement_rng=stream(seed,'visitor_settlement',0)
    seed_rng=stream(seed,'seed_arrivals',0)
    allele_rng=stream(seed,'source_genotypes',0)
    if config.island_history=='separation':
        if not isinstance(inherited_visitors,VisitorState) or len(inherited_visitors.ids)!=config.initial_visitors:
            raise ValueError('separation requires an explicit inherited visitor state')
        visitors=inherited_visitors
        if len(visitors.ids):
            visitors_next=max(visitors_next,int(visitors.ids.max())+1)
    else:
        if inherited_visitors is not None:
            raise ValueError('founding cannot silently inherit a separation community')
        count=config.initial_visitors
        visitors=VisitorState(ids=np.arange(visitors_next,visitors_next+count,dtype=np.int64),
            optima=initial_rng.uniform(size=count),breadths=np.full(count,config.visitor_breadth),
            effectiveness=np.full(count,config.visitor_effectiveness))
        visitors_next+=count
    seed_rate=config.seed_arrival.supply*reach_probability(config.seed_arrival.distance,
                        config.seed_arrival.scale,config.seed_arrival.kernel)
    visitor_rate=config.visitor_arrival.supply*reach_probability(config.visitor_arrival.distance,
                        config.visitor_arrival.scale,config.visitor_arrival.kernel)
    visitor_path=[]; seed_path=[]
    for year in range(config.years):
        visitor_path.append(visitors)
        count=int(seed_rng.poisson(seed_rate))
        if seeds_next+count>=block+2**32:
            raise ValueError('seed ID namespace exhausted')
        ids=np.arange(seeds_next,seeds_next+count,dtype=np.int64)
        alleles=reflect_unit(np.asarray(config.source_allele_means)[None,:,None]
                            +allele_rng.normal(0,config.source_allele_sd,(count,3,2)))
        seed_path.append(PlantState(alleles=alleles,allele_origin=np.broadcast_to(ids[:,None,None],alleles.shape),
            mutation_flags=np.zeros(alleles.shape,dtype=bool),ids=ids,birth_years=np.full(count,year+1,dtype=np.int64)))
        seeds_next+=count
        # Seed establishment is applied by population.advance, never twice.
        survived=loss_rng.random(len(visitors.ids))>=-np.expm1(-config.visitor_arrival.loss_hazard)
        arrivals=int(visitor_rng.poisson(visitor_rate))
        optima=visitor_rng.uniform(size=arrivals)
        settled=settlement_rng.random(arrivals)<config.visitor_arrival.establishment
        if visitors_next+arrivals>np.iinfo(np.int64).max:
            raise ValueError('visitor ID namespace exhausted')
        new_ids=np.arange(visitors_next,visitors_next+arrivals,dtype=np.int64)[settled]
        visitors_next+=arrivals
        visitors=VisitorState(ids=np.concatenate([visitors.ids[survived],new_ids]),
            optima=np.concatenate([visitors.optima[survived],optima[settled]]),
            breadths=np.concatenate([visitors.breadths[survived],np.full(len(new_ids),config.visitor_breadth)]),
            effectiveness=np.concatenate([visitors.effectiveness[survived],np.full(len(new_ids),config.visitor_effectiveness)]))
    return History(tuple(visitor_path),tuple(seed_path),config.event_order,config.island_history,0)


def permute_exposure(history: History, order: np.ndarray, recovery: History) -> History:
    order=np.asarray(order)
    n=len(history.visitors)
    if order.shape!=(n,) or order.dtype.kind not in 'iu' or not np.array_equal(np.sort(order),np.arange(n)):
        raise ValueError('order must be an exact permutation of exposure indices')
    if history.event_order!=recovery.event_order:
        raise ValueError('history event orders disagree')
    old_ids={int(i) for p in history.seed_candidates for i in p.ids}
    new_ids={int(i) for p in recovery.seed_candidates for i in p.ids}
    if old_ids & new_ids:
        raise ValueError('recovery must use distinct seed individual IDs')
    recovery_seeds=tuple(replace(p,birth_years=p.birth_years+n) for p in recovery.seed_candidates)
    # Seed arrival timing is held fixed while only visitor chronology changes.
    return History(tuple(history.visitors[int(i)] for i in order)+recovery.visitors,
                   history.seed_candidates+recovery_seeds,history.event_order,'controlled',0)
