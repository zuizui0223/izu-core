from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Scenario:
    name: str
    n_pollinator_types: int
    partner_arrival: float
    partner_loss: float
    trait_dispersion: float
    generalist_fraction: float
    replacement_fraction: float
    selfing_capacity: float


@dataclass
class Plant:
    trait: float
    assurance: float
    reproduction: float = 0.0


@dataclass
class Pollinator:
    trait: float
    breadth: float
    introduced: bool


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return min(hi, max(lo, x))


def make_pollinators(rng: random.Random, s: Scenario) -> list[Pollinator]:
    pollinators: list[Pollinator] = []
    for _ in range(s.n_pollinator_types):
        trait = clamp(rng.gauss(0.5, s.trait_dispersion))
        broad = rng.random() < s.generalist_fraction
        breadth = 0.42 if broad else 0.16
        introduced = rng.random() < s.replacement_fraction
        pollinators.append(Pollinator(trait=trait, breadth=breadth, introduced=introduced))
    return pollinators


def encounter_score(plant: Plant, pollinator: Pollinator) -> float:
    mismatch = abs(plant.trait - pollinator.trait)
    match = math.exp(-((mismatch / max(pollinator.breadth, 1e-6)) ** 2))
    replacement_penalty = 0.82 if pollinator.introduced else 1.0
    return clamp(match * replacement_penalty)


def step(
    rng: random.Random,
    plants: list[Plant],
    pollinators: list[Pollinator],
    s: Scenario,
) -> tuple[list[Plant], list[Pollinator]]:
    # geography/opportunity layer: partners are lost and occasionally replaced/arrive
    survivors = [p for p in pollinators if rng.random() >= s.partner_loss]
    if rng.random() < s.partner_arrival:
        broad = rng.random() < s.generalist_fraction
        survivors.append(
            Pollinator(
                trait=clamp(rng.gauss(0.5, s.trait_dispersion)),
                breadth=0.42 if broad else 0.16,
                introduced=rng.random() < s.replacement_fraction,
            )
        )
    pollinators = survivors

    for plant in plants:
        if pollinators:
            scores = [encounter_score(plant, p) for p in pollinators]
            pollination = 1.0 - math.prod(1.0 - min(0.65, 0.22 * x) for x in scores)
        else:
            pollination = 0.0

        autonomous = s.selfing_capacity * plant.assurance
        plant.reproduction = clamp(pollination + (1.0 - pollination) * autonomous)

        # weak adaptive response: change trait toward the best current partner only when
        # pollination is poor; otherwise retain phenotype. Assurance can also rise.
        if pollinators and pollination < 0.45:
            best = max(pollinators, key=lambda p: encounter_score(plant, p))
            plant.trait = clamp(plant.trait + 0.035 * (best.trait - plant.trait))
        if plant.reproduction < 0.45:
            plant.assurance = clamp(plant.assurance + 0.018)

    return plants, pollinators


def architecture_label(pollinators: list[Pollinator], plants: list[Plant]) -> str:
    if not pollinators:
        return "assurance_dominated"
    broad = sum(p.breadth >= 0.4 for p in pollinators) / len(pollinators)
    introduced = sum(p.introduced for p in pollinators) / len(pollinators)
    if introduced >= 0.5:
        return "novel_partner_replacement"
    if broad >= 0.5:
        return "complementary_or_redundant_generalism"
    # concentration proxy: most plants share the same best-matching partner
    best_ids = []
    for plant in plants:
        scores = [encounter_score(plant, p) for p in pollinators]
        best_ids.append(max(range(len(scores)), key=scores.__getitem__))
    top_share = max(best_ids.count(i) for i in set(best_ids)) / len(best_ids)
    return "concentrated_dependency" if top_share >= 0.6 else "species_specific_mosaic"


def run_one(s: Scenario, seed: int, steps: int = 120, n_plants: int = 80) -> dict:
    rng = random.Random(seed)
    plants = [Plant(trait=clamp(rng.gauss(0.5, 0.18)), assurance=0.08) for _ in range(n_plants)]
    pollinators = make_pollinators(rng, s)

    for _ in range(steps):
        plants, pollinators = step(rng, plants, pollinators, s)

    mean_reproduction = sum(p.reproduction for p in plants) / len(plants)
    mean_assurance = sum(p.assurance for p in plants) / len(plants)
    trait_sd = math.sqrt(sum((p.trait - sum(x.trait for x in plants) / len(plants)) ** 2 for p in plants) / len(plants))
    return {
        "scenario": s.name,
        "seed": seed,
        "n_pollinators_final": len(pollinators),
        "mean_reproduction": mean_reproduction,
        "mean_assurance": mean_assurance,
        "plant_trait_sd": trait_sd,
        "architecture": architecture_label(pollinators, plants),
    }


def summarize(rows: list[dict]) -> dict:
    by_scenario: dict[str, list[dict]] = {}
    for row in rows:
        by_scenario.setdefault(row["scenario"], []).append(row)

    out = {}
    for name, xs in by_scenario.items():
        arch_counts: dict[str, int] = {}
        for x in xs:
            arch_counts[x["architecture"]] = arch_counts.get(x["architecture"], 0) + 1
        out[name] = {
            "n_runs": len(xs),
            "mean_reproduction": sum(x["mean_reproduction"] for x in xs) / len(xs),
            "mean_assurance": sum(x["mean_assurance"] for x in xs) / len(xs),
            "mean_final_pollinator_types": sum(x["n_pollinators_final"] for x in xs) / len(xs),
            "architecture_counts": arch_counts,
        }
    return out


def default_scenarios() -> list[Scenario]:
    return [
        Scenario("mainland_like", 9, 0.28, 0.015, 0.22, 0.35, 0.05, 0.20),
        Scenario("continental_island", 7, 0.20, 0.025, 0.20, 0.42, 0.08, 0.24),
        Scenario("oceanic_island", 4, 0.12, 0.055, 0.16, 0.58, 0.22, 0.30),
    ]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--replicates", type=int, default=200)
    p.add_argument("--steps", type=int, default=120)
    p.add_argument("--seed", type=int, default=20260818)
    p.add_argument("--out", type=Path, default=Path("data/results/constraint_mechanism_abm_v1.json"))
    args = p.parse_args()

    rows = []
    for si, scenario in enumerate(default_scenarios()):
        for r in range(args.replicates):
            rows.append(run_one(scenario, seed=args.seed + si * 100000 + r, steps=args.steps))

    payload = {
        "model": "constraint_mechanism_abm_v1",
        "status": "mechanistic_hypothesis_test_not_empirical_evidence",
        "scenarios": [asdict(s) for s in default_scenarios()],
        "summary": summarize(rows),
        "claim_boundary": (
            "This ABM asks whether constrained partner opportunity alone can generate multiple stable interaction architectures "
            "while preserving reproduction. It must not be used to estimate empirical prevalence or to upgrade any island pathway gate."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
