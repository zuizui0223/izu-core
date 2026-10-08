"""Exact finite-genotype Markov bridge for repeated Model 3 reproduction.

Restricted reference, not an SDE or SPDE. Keeps the same finite plant
reproduction and full joint diploid genotype frequencies at every step.
It replaces *only* individual parent choices and Mendelian segregation with
the algebraically identical child genotype mixture and multinomial sampling.
No mutation, adult carry-over or seed immigration is allowed.
"""
from __future__ import annotations

import numpy as np

from scripts.audit_model3_stochastic_bridge import (
    offspring_genotype_distribution, require_restricted_case,
)
from scripts.model3_island.density import GeneticGrid
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import Config, PlantState, VisitorState


def exact_markov_step(state: PlantState, visitor: VisitorState,
                      config: Config, grid: GeneticGrid,
                      rng: np.random.Generator, *, year: int) -> PlantState:
    """Draw same next-generation joint genotype law as canonical ABM.

    This is law-equivalent conditional on the current *complete genotype census*
    and visitor set, including individual pollen self-exclusion. Pedigree
    identities and mutation flags are not compared (both biologically
    disabled for this restricted assay).
    """
    if type(year) is not int or year < 0:
        raise ValueError("invalid reproductive year")
    if not isinstance(rng,np.random.Generator):
        raise TypeError("numpy Generator required")
    if not isinstance(config,Config) or (config.survival != 0
        or config.mutation_rate != 0 or config.seed_arrival.supply != 0):
        raise ValueError("restricted bridge permits no adult survival, mutation or immigration")
    n = len(state.ids)
    if n == 0:
        return PlantState(
            np.empty((0,3,2),dtype=float),
            np.empty((0,3,2),dtype=np.int64),
            np.empty((0,3,2),dtype=bool),
            np.empty(0,dtype=np.int64),
            np.empty(0,dtype=np.int64),
        )
    ledger = reproduce(state,visitor,config)
    require_restricted_case(state,ledger,config)
    parents = ledger.outcross.copy()
    parents[np.diag_indices(n)] += ledger.self_viable
    total = float(parents.sum())
    if total<=0:
        next_n=0
    else:
        next_n=min(config.capacity,int(rng.poisson(total)))
    if next_n:
        genotype_prob = offspring_genotype_distribution(state,parents/total,grid)
        offspring_counts = rng.multinomial(next_n,genotype_prob)
        genotypes = np.repeat(np.arange(len(genotype_prob)),offspring_counts)
        alleles = grid.genotypes[genotypes].copy()
    else:
        alleles = np.empty((0,3,2),dtype=float)
    birth = year+1
    return PlantState(
        alleles,
        np.zeros((next_n,3,2),dtype=np.int64),
        np.zeros((next_n,3,2),dtype=bool),
        birth*config.capacity+np.arange(next_n,dtype=np.int64),
        np.full(next_n,birth,dtype=np.int64),
    )
