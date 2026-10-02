"""Prospective inheritance extension for trait-specific mutation accessibility.

The ecological reproductive operator remains scripts.model3_island.reproduction.reproduce.
This sibling module replaces only the post-segregation mutation kernel and then
uses the same survival/recruitment logic as Model 3.
"""
from __future__ import annotations

import numpy as np

from scripts.model3_island.history import reflect_unit
from scripts.model3_island.population import concatenate, subset
from scripts.model3_island.types import PlantState, _integer


def inherit_trait_accessibility(
    state: PlantState,
    mothers,
    fathers,
    config,
    *,
    mutation_spec: dict,
    coupling: float,
    segregation_rng,
    mutation_rng,
    year: int,
) -> PlantState:
    _integer(year, "birth year", 1)
    mothers = np.asarray(mothers)
    fathers = np.asarray(fathers)
    n = len(mothers) if mothers.ndim == 1 else -1
    if (
        mothers.ndim != 1
        or fathers.shape != mothers.shape
        or mothers.dtype.kind not in "iu"
        or fathers.dtype.kind not in "iu"
        or n > config.capacity
        or (mothers < 0).any()
        or (fathers < 0).any()
        or (mothers >= len(state.ids)).any()
        or (fathers >= len(state.ids)).any()
    ):
        raise ValueError("invalid parental indices or retained offspring count")
    if year * config.capacity + n >= 2**32:
        raise ValueError("resident offspring ID namespace exhausted")
    if not 0 <= coupling <= 1:
        raise ValueError("coupling must be in [0,1]")

    mu_a = float(mutation_spec["mutation_rate_access"])
    mu_z = float(mutation_spec["mutation_rate_investment"])
    sd_a = float(mutation_spec["mutation_sd_access"])
    sd_z = float(mutation_spec["mutation_sd_investment"])
    for value, name in ((mu_a, "mutation_rate_access"), (mu_z, "mutation_rate_investment")):
        if not 0 <= value <= 1:
            raise ValueError(f"{name} must be in [0,1]")
    for value, name in ((sd_a, "mutation_sd_access"), (sd_z, "mutation_sd_investment")):
        if value < 0 or not np.isfinite(value):
            raise ValueError(f"invalid {name}")

    maternal = segregation_rng.integers(0, 2, size=(n, 3))
    paternal = segregation_rng.integers(0, 2, size=(n, 3))
    loci = np.arange(3)[None, :]

    def transmit(array):
        return np.stack(
            [
                array[mothers[:, None], loci, maternal],
                array[fathers[:, None], loci, paternal],
            ],
            axis=-1,
        )

    alleles = transmit(state.alleles)
    origins = transmit(state.allele_origin)
    flags = transmit(state.mutation_flags)

    # Pair access and investment mutations within each inherited homolog copy.
    # Marginal mutation probabilities remain exactly mu_a and mu_z.
    shared_rate = coupling * min(mu_a, mu_z)
    if shared_rate > 0:
        shared = mutation_rng.random((n, 2)) < shared_rate
    else:
        shared = np.zeros((n, 2), dtype=bool)

    remaining = ~shared
    denom = 1.0 - shared_rate
    access_residual_p = 0.0 if denom == 0 else (mu_a - shared_rate) / denom
    invest_residual_p = 0.0 if denom == 0 else (mu_z - shared_rate) / denom
    access_only = remaining & (mutation_rng.random((n, 2)) < access_residual_p)
    invest_only = remaining & (mutation_rng.random((n, 2)) < invest_residual_p)

    shared_z = mutation_rng.normal(size=(n, 2))
    access_z = mutation_rng.normal(size=(n, 2))
    invest_z = mutation_rng.normal(size=(n, 2))

    access_step = np.where(shared, shared_z * sd_a, 0.0)
    access_step += np.where(access_only, access_z * sd_a, 0.0)
    invest_step = np.where(shared, shared_z * sd_z, 0.0)
    invest_step += np.where(invest_only, invest_z * sd_z, 0.0)

    access_mut = shared | access_only
    invest_mut = shared | invest_only
    if access_mut.any():
        alleles[:, 0, :][access_mut] = reflect_unit(
            alleles[:, 0, :][access_mut] + access_step[access_mut]
        )
        flags[:, 0, :][access_mut] = True
    if invest_mut.any():
        alleles[:, 1, :][invest_mut] = reflect_unit(
            alleles[:, 1, :][invest_mut] + invest_step[invest_mut]
        )
        flags[:, 1, :][invest_mut] = True

    ids = np.arange(year * config.capacity, year * config.capacity + n, dtype=np.int64)
    return PlantState(
        alleles,
        origins,
        flags,
        ids,
        np.full(n, year, dtype=np.int64),
    )


def advance_trait_accessibility(
    state: PlantState,
    ledger,
    seed_candidates: PlantState,
    config,
    streams,
    *,
    mutation_spec: dict,
    coupling: float,
    year: int,
):
    """Model 3 demographic update with only the inheritance mutation kernel swapped."""
    _integer(year, "year")
    n = len(state.ids)
    if n > config.capacity or len(ledger.ovules) != n:
        raise ValueError("population/ledger dimensions inconsistent with capacity")
    if (state.birth_years > year).any() or (seed_candidates.birth_years != year + 1).any():
        raise ValueError("resident ages or seed arrival years inconsistent")
    if np.intersect1d(state.ids, seed_candidates.ids).size:
        raise ValueError("seed candidate IDs must differ from resident IDs")

    parents = ledger.outcross.copy()
    parents[np.diag_indices(n)] += ledger.self_viable
    total = float(parents.sum())
    if not np.isfinite(total):
        raise ValueError("nonfinite expected reproduction")

    keep = streams["survival"].random(n) < config.survival
    adults = subset(state, keep)
    resident_potential = int(streams["recruitment"].poisson(total))
    settled = streams["seed_settlement"].random(len(seed_candidates.ids)) < config.seed_arrival.establishment
    immigrants = subset(seed_candidates, settled)
    immigrant_potential = len(immigrants.ids)
    vacancies = config.capacity - len(adults.ids)
    retained = min(vacancies, resident_potential + immigrant_potential)

    if immigrant_potential and resident_potential and retained:
        resident_count = int(
            streams["recruitment"].hypergeometric(
                resident_potential, immigrant_potential, retained
            )
        )
    else:
        resident_count = min(resident_potential, retained)
    immigrant_count = retained - resident_count

    if resident_count:
        choices = streams["parents"].choice(
            n * n, size=resident_count, p=parents.ravel() / total
        )
        fathers, mothers = np.unravel_index(choices, parents.shape)
    else:
        fathers = mothers = np.empty(0, dtype=int)

    children = inherit_trait_accessibility(
        state,
        mothers,
        fathers,
        config,
        mutation_spec=mutation_spec,
        coupling=coupling,
        segregation_rng=streams["segregation"],
        mutation_rng=streams["mutation"],
        year=year + 1,
    )
    immigrant_indices = streams["recruitment"].choice(
        immigrant_potential, size=immigrant_count, replace=False
    )
    incoming = subset(immigrants, immigrant_indices)
    result = concatenate([adults, children, incoming])

    return result, {
        "resident_recruits": resident_count,
        "immigrant_recruits": immigrant_count,
        "selfed_recruits": int(np.sum(mothers == fathers)),
        "outcross_recruits": int(np.sum(mothers != fathers)),
    }
