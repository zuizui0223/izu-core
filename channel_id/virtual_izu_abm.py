"""Minimal agent-based model for a synthetic Izu archipelago.

Plants are individual agents. Pollinators are island-level functional services.
The model is an identifiability experiment, not a reconstruction of real Izu history.
"""
from __future__ import annotations

import math
import random
from dataclasses import asdict, dataclass
from typing import Iterable

SCENARIOS = {
    "environment_only",
    "distance_only",
    "pollinator_regime",
    "environment_plus_pollinator",
    "small_bee_substitution",
}


@dataclass(frozen=True)
class Island:
    name: str
    position: float
    environment: float
    carrying_capacity: int
    large_bombus: float
    ardens: float
    small_bee: float
    generalist_service: float


@dataclass(frozen=True)
class Plant:
    lineage: int
    island: int
    specialization: float
    floral_match: float
    autonomous_selfing: float
    dispersal: float
    environmental_optimum: float
    inbreeding_depression: float


def default_islands() -> tuple[Island, ...]:
    """A declared synthetic scaffold: mainland, Oshima, and four southern islands."""
    return (
        Island("mainland", 0.0, 0.00, 500, 1.00, 0.00, 0.45, 0.70),
        Island("oshima", 1.0, 0.15, 350, 0.00, 0.85, 0.55, 0.65),
        Island("toshima", 2.0, 0.28, 180, 0.00, 0.00, 0.60, 0.62),
        Island("niijima", 3.0, 0.42, 220, 0.00, 0.00, 0.68, 0.60),
        Island("miyake", 4.0, 0.58, 260, 0.00, 0.00, 0.72, 0.58),
        Island("hachijo", 5.0, 0.75, 320, 0.00, 0.00, 0.78, 0.57),
    )


def generate_founders(n: int, *, seed: int = 1) -> list[Plant]:
    if n <= 0:
        raise ValueError("n must be positive")
    rng = random.Random(seed)
    return [
        Plant(
            lineage=i,
            island=0,
            specialization=rng.random(),
            floral_match=rng.random(),
            autonomous_selfing=rng.betavariate(1.5, 4.0),
            dispersal=rng.betavariate(2.0, 3.0),
            environmental_optimum=rng.random(),
            inbreeding_depression=rng.uniform(0.05, 0.65),
        )
        for i in range(n)
    ]


def _pollinator_service(island: Island, plant: Plant, scenario: str) -> float:
    if scenario in {"environment_only", "distance_only"}:
        return 0.75
    specialist_service = max(island.large_bombus, island.ardens)
    if scenario == "small_bee_substitution":
        specialist_service = max(specialist_service, island.small_bee * 0.9)
    service = (
        plant.specialization * specialist_service
        + (1.0 - plant.specialization) * island.generalist_service
    )
    match = math.exp(-3.0 * (plant.floral_match - specialist_service) ** 2)
    return max(0.0, min(1.0, service * (0.55 + 0.45 * match)))


def _environment_survival(island: Island, plant: Plant, scenario: str) -> float:
    if scenario == "pollinator_regime":
        return 0.82
    mismatch = abs(island.environment - plant.environmental_optimum)
    return max(0.05, math.exp(-2.7 * mismatch))


def _dispersal_target(plant: Plant, islands: tuple[Island, ...], rng: random.Random, scenario: str) -> int:
    if rng.random() > 0.06 * plant.dispersal:
        return plant.island
    candidates = [i for i in range(len(islands)) if i != plant.island]
    weights = []
    for i in candidates:
        distance = abs(islands[i].position - islands[plant.island].position)
        penalty = math.exp(-1.15 * distance)
        if scenario == "distance_only":
            penalty *= math.exp(-0.55 * islands[i].position)
        weights.append(penalty)
    return rng.choices(candidates, weights=weights, k=1)[0]


def _mutate(value: float, rng: random.Random, sd: float = 0.025) -> float:
    return max(0.0, min(1.0, rng.gauss(value, sd)))


def step(population: list[Plant], islands: tuple[Island, ...], *, scenario: str, rng: random.Random) -> list[Plant]:
    if scenario not in SCENARIOS:
        raise ValueError(f"unknown scenario: {scenario}")
    offspring: list[Plant] = []
    for plant in population:
        island = islands[plant.island]
        survival = _environment_survival(island, plant, scenario)
        pollination = _pollinator_service(island, plant, scenario)
        outcross = pollination
        selfed = plant.autonomous_selfing * (1.0 - pollination) * (1.0 - plant.inbreeding_depression)
        expected = 1.55 * survival * (outcross + selfed)
        births = int(expected) + (1 if rng.random() < expected % 1 else 0)
        for _ in range(births):
            target = _dispersal_target(plant, islands, rng, scenario)
            offspring.append(Plant(
                lineage=plant.lineage,
                island=target,
                specialization=_mutate(plant.specialization, rng),
                floral_match=_mutate(plant.floral_match, rng),
                autonomous_selfing=_mutate(plant.autonomous_selfing, rng),
                dispersal=_mutate(plant.dispersal, rng, 0.015),
                environmental_optimum=_mutate(plant.environmental_optimum, rng, 0.015),
                inbreeding_depression=plant.inbreeding_depression,
            ))
    capped: list[Plant] = []
    for island_id, island in enumerate(islands):
        residents = [p for p in offspring if p.island == island_id]
        if len(residents) > island.carrying_capacity:
            residents = rng.sample(residents, island.carrying_capacity)
        capped.extend(residents)
    return capped


def summarize(population: Iterable[Plant], islands: tuple[Island, ...]) -> dict[str, object]:
    plants = list(population)
    rows = []
    for island_id, island in enumerate(islands):
        residents = [p for p in plants if p.island == island_id]
        rows.append({
            "island": island.name,
            "n": len(residents),
            "n_lineages": len({p.lineage for p in residents}),
            "mean_specialization": sum(p.specialization for p in residents) / len(residents) if residents else None,
            "mean_autonomous_selfing": sum(p.autonomous_selfing for p in residents) / len(residents) if residents else None,
        })
    southern = [p for p in plants if p.island >= 2]
    return {
        "total_population": len(plants),
        "extant_lineages": len({p.lineage for p in plants}),
        "southern_lineages": len({p.lineage for p in southern}),
        "islands": rows,
    }


def run_abm(*, scenario: str, generations: int = 80, founders: int = 180, seed: int = 1) -> dict[str, object]:
    if generations <= 0:
        raise ValueError("generations must be positive")
    islands = default_islands()
    population = generate_founders(founders, seed=seed)
    rng = random.Random(seed + 991)
    trajectory = []
    for generation in range(generations + 1):
        if generation in {0, generations // 2, generations}:
            trajectory.append({"generation": generation, **summarize(population, islands)})
        if generation < generations:
            population = step(population, islands, scenario=scenario, rng=rng)
    return {
        "scenario": scenario,
        "generations": generations,
        "founders": founders,
        "seed": seed,
        "island_scaffold": [asdict(x) for x in islands],
        "trajectory": trajectory,
        "final": summarize(population, islands),
        "claim_boundary": (
            "Outputs describe behavior of a declared synthetic archipelago. "
            "They are not estimates of real island parameters or historical reconstruction."
        ),
    }
