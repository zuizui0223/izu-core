"""Dynamic-support finite genotype measure process for frozen Model 3.

The state is the empirical joint diploid genotype measure, storing unique
three-locus genotypes and integer multiplicities. Mutation creates NEW support
points with exact floating-point reflected-Gaussian allele values; genotypes
are never snapped to a grid. The transition uses canonical reproduce() and
inherit() without consulting a reference ABM trajectory after initialization.

This is a *discrete-time finite measure-valued Markov process*, not an SDE,
SPDE, approximate diffusion, or an independent ecological biological model.
Restricted to annual complete replacement, no seed immigration. Because it
does not retain founder ancestry and mutation provenance, it MUST NOT be used
for pedigree/ancestry readouts or migration/survival experiments.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from scripts.model3_island.population import inherit
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import Config, PlantState, VisitorState, mutation_trait_mask


@dataclass(frozen=True)
class GenotypeMeasure:
    """Integer atomic measure on [0,1]^(3x2), modulo allele-copy exchange."""
    genotypes: np.ndarray  # (G,3,2), sorted within each diploid locus
    counts: np.ndarray     # (G,), exact integer multiplicity

    def __post_init__(self):
        g=np.asarray(self.genotypes,dtype=np.float64)
        c=np.asarray(self.counts)
        if (g.ndim!=3 or g.shape[1:]!=(3,2) or c.shape!=(len(g),)
                or c.dtype.kind not in "iu" or (c<=0).any()
                or not np.isfinite(g).all() or (g<0).any() or (g>1).any()):
            raise ValueError("invalid bounded joint diploid genotype measure")
        if len(g):
            if not np.array_equal(g,np.sort(g,axis=2)):
                raise ValueError("each locus must use canonical allele order")
            flattened=g.reshape(len(g),6)
            if len(np.unique(flattened,axis=0))!=len(g):
                raise ValueError("duplicate genotype classes must be combined")
        g=g.copy()
        c=c.astype(np.int64,copy=True)
        g.setflags(write=False)
        c.setflags(write=False)
        object.__setattr__(self,"genotypes",g)
        object.__setattr__(self,"counts",c)

    @property
    def census(self) -> int:
        return int(self.counts.sum())

    @classmethod
    def from_plant_state(cls,state:PlantState) -> "GenotypeMeasure":
        if not isinstance(state,PlantState):
            raise TypeError("expected Model3 PlantState")
        alleles=np.sort(state.alleles,axis=2)
        if not len(alleles):
            return cls(np.empty((0,3,2),dtype=float),
                       np.empty((0,),dtype=np.int64))
        distinct,multiplicities=np.unique(
            alleles.reshape(len(alleles),6),axis=0,return_counts=True
        )
        return cls(distinct.reshape(-1,3,2),multiplicities)

    def to_plant_state(self, *, year:int, capacity:int)->PlantState:
        """Expand copies into distinct individuals for canonical pollen exclusion."""
        if (type(year) is not int or year<0 or
                type(capacity) is not int or capacity<1 or self.census>capacity):
            raise ValueError("invalid year/capacity for finite measure")
        alleles=np.repeat(self.genotypes,self.counts,axis=0)
        n=len(alleles)
        return PlantState(
            alleles=alleles,
            allele_origin=np.zeros((n,3,2),dtype=np.int64),
            mutation_flags=np.zeros((n,3,2),dtype=bool),
            ids=year*capacity+np.arange(n,dtype=np.int64),
            birth_years=np.full(n,year,dtype=np.int64),
        )


def measure_step(
    measure:GenotypeMeasure,
    visitors:VisitorState,
    config:Config,
    streams:dict,
    *,
    year:int,
    mutation_traits=(True,True,True),
)-> GenotypeMeasure:
    """One independent, exact-law finite-genotype transition with birth mutation.

    This repeats the original *probability law*, not the arbitrary order of
    individual IDs or pedigree labels. Each genotype copy remains an individual
    for pollen self-exclusion. The separate canonical RNG streams allow a
    one-step pathwise audit from the identical expanded starting state.
    """
    mutation_traits=mutation_trait_mask(mutation_traits)
    if not isinstance(measure,GenotypeMeasure) or not isinstance(config,Config):
        raise TypeError("canonical measure and config required")
    if (config.survival!=0 or config.seed_arrival.supply!=0):
        raise ValueError(
            "dynamic genotype measure requires complete adult turnover and "
            "zero seed immigration"
        )
    if not isinstance(visitors,VisitorState) or type(year) is not int or year<0:
        raise ValueError("canonical visitor state and valid time required")
    for key in ("recruitment","parents","segregation","mutation"):
        if key not in streams or not isinstance(streams[key],np.random.Generator):
            raise ValueError("missing canonical random stream: "+key)
    # No plants and no external immigrants: extinction is absorbing.
    if measure.census==0:
        return measure
    state=measure.to_plant_state(year=year,capacity=config.capacity)
    ledger=reproduce(state,visitors,config)
    parents=ledger.outcross.copy()
    parents[np.diag_indices(len(state.ids))]+=ledger.self_viable
    intensity=float(parents.sum())
    if not np.isfinite(intensity) or intensity<0:
        raise ArithmeticError("invalid canonical reproduction intensity")
    retained=min(int(streams["recruitment"].poisson(intensity)),config.capacity)
    if retained:
        if intensity<=0:
            raise ArithmeticError("recruited offspring with zero parents")
        indices=streams["parents"].choice(
            len(state.ids)**2,size=retained,p=parents.ravel()/intensity
        )
        fathers,mothers=np.unravel_index(indices,parents.shape)
    else:
        fathers=mothers=np.empty((0,),dtype=np.int64)
    children=inherit(
        state,mothers,fathers,config,
        segregation_rng=streams["segregation"],
        mutation_rng=streams["mutation"],
        year=year+1,mutation_traits=mutation_traits,
    )
    return GenotypeMeasure.from_plant_state(children)
