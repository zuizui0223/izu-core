from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import dataclass
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


@dataclass(frozen=True)
class LineageTemplate:
    trait: float
    pollinator_dependency: float
    assurance_ceiling: float
    assurance_responsiveness: float
    trait_adjustment: float


@dataclass
class LineageState:
    template: LineageTemplate
    trait: float
    assurance: float = 0.08
    reproduction: float = 0.0
    best_match: float = 0.0


@dataclass
class Pollinator:
    trait: float
    breadth: float
    introduced: bool


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return min(hi, max(lo, x))


def scenarios() -> tuple[Scenario, Scenario]:
    return (
        Scenario("mainland_like", 9, 0.28, 0.015, 0.22, 0.35, 0.05),
        Scenario("oceanic_island", 4, 0.12, 0.055, 0.16, 0.58, 0.22),
    )


def make_lineages(rng: random.Random, n: int) -> list[LineageTemplate]:
    return [
        LineageTemplate(
            trait=clamp(rng.gauss(0.5, 0.18)),
            pollinator_dependency=rng.uniform(0.35, 0.95),
            assurance_ceiling=rng.uniform(0.10, 0.90),
            assurance_responsiveness=rng.uniform(0.004, 0.035),
            trait_adjustment=rng.uniform(0.01, 0.055),
        )
        for _ in range(n)
    ]


def make_pollinator(rng: random.Random, s: Scenario) -> Pollinator:
    broad = rng.random() < s.generalist_fraction
    return Pollinator(
        trait=clamp(rng.gauss(0.5, s.trait_dispersion)),
        breadth=0.42 if broad else 0.16,
        introduced=rng.random() < s.replacement_fraction,
    )


def encounter_score(lineage: LineageState, pollinator: Pollinator) -> float:
    mismatch = abs(lineage.trait - pollinator.trait)
    match = math.exp(-((mismatch / max(pollinator.breadth, 1e-6)) ** 2))
    return clamp(match * (0.82 if pollinator.introduced else 1.0))


def fixed_budget_pollination(scores: list[float], saturation: float) -> float:
    if not scores:
        return 0.0
    # Richness changes the mix of partners, but not total visitation opportunity.
    # The mean service score is therefore converted through a saturating response.
    mean_service = sum(scores) / len(scores)
    return clamp(1.0 - math.exp(-saturation * mean_service))


def run_scenario(
    templates: list[LineageTemplate],
    s: Scenario,
    seed: int,
    steps: int,
    saturation: float,
) -> list[LineageState]:
    rng = random.Random(seed)
    lineages = [LineageState(template=t, trait=t.trait) for t in templates]
    pollinators = [make_pollinator(rng, s) for _ in range(s.n_pollinator_types)]

    for _ in range(steps):
        pollinators = [p for p in pollinators if rng.random() >= s.partner_loss]
        if rng.random() < s.partner_arrival:
            pollinators.append(make_pollinator(rng, s))

        for lin in lineages:
            scores = [encounter_score(lin, p) for p in pollinators]
            pollination = fixed_budget_pollination(scores, saturation)

            d = lin.template.pollinator_dependency
            autonomous = lin.template.assurance_ceiling * lin.assurance
            pollinator_route = d * pollination
            assurance_route = (1.0 - d) * autonomous
            lin.reproduction = clamp(1.0 - (1.0 - pollinator_route) * (1.0 - assurance_route))

            if pollinators and pollination < 0.45:
                best = max(pollinators, key=lambda p: encounter_score(lin, p))
                lin.trait = clamp(lin.trait + lin.template.trait_adjustment * (best.trait - lin.trait))
            if lin.reproduction < 0.50:
                lin.assurance = min(
                    lin.template.assurance_ceiling,
                    lin.assurance + lin.template.assurance_responsiveness,
                )

    # Observation-only extension for held-out validation; does not change dynamics.
    for lin in lineages:
        scores = [encounter_score(lin, p) for p in pollinators]
        lin.best_match = max(scores) if scores else 0.0
    return lineages


def paired_run(seed: int, saturation: float, n_lineages: int = 16, steps: int = 120) -> dict:
    templates = make_lineages(random.Random(seed), n_lineages)
    mainland, oceanic = scenarios()
    m = run_scenario(templates, mainland, seed + 100_000, steps, saturation)
    o = run_scenario(templates, oceanic, seed + 200_000, steps, saturation)
    deltas = [oo.reproduction - mm.reproduction for mm, oo in zip(m, o)]
    match_deltas = [oo.best_match - mm.best_match for mm, oo in zip(m, o)]
    eps = 1e-9
    return {
        "positive": sum(d > eps for d in deltas),
        "negative": sum(d < -eps for d in deltas),
        "near_zero": sum(abs(d) <= eps for d in deltas),
        "mean_delta": sum(deltas) / len(deltas),
        "mean_mainland_reproduction": sum(x.reproduction for x in m) / len(m),
        "mean_oceanic_reproduction": sum(x.reproduction for x in o) / len(o),
        "best_match_lower": sum(d < -eps for d in match_deltas),
        "best_match_higher": sum(d > eps for d in match_deltas),
        "best_match_equal": sum(abs(d) <= eps for d in match_deltas),
        "mean_best_match_delta": sum(match_deltas) / len(match_deltas),
    }


def summarize(rows: list[dict]) -> dict:
    positive = sum(r["positive"] for r in rows)
    negative = sum(r["negative"] for r in rows)
    zero = sum(r["near_zero"] for r in rows)
    total = positive + negative + zero
    mixed = sum(r["positive"] > 0 and r["negative"] > 0 for r in rows)
    return {
        "n_lineage_contrasts": total,
        "positive_lineage_responses": positive,
        "negative_lineage_responses": negative,
        "near_zero_lineage_responses": zero,
        "positive_fraction": positive / total,
        "negative_fraction": negative / total,
        "mixed_sign_runs": mixed,
        "mean_delta": sum(r["mean_delta"] for r in rows) / len(rows),
        "mean_mainland_reproduction": sum(r["mean_mainland_reproduction"] for r in rows) / len(rows),
        "mean_oceanic_reproduction": sum(r["mean_oceanic_reproduction"] for r in rows) / len(rows),
        "best_match_lower": sum(r["best_match_lower"] for r in rows),
        "best_match_higher": sum(r["best_match_higher"] for r in rows),
        "best_match_equal": sum(r["best_match_equal"] for r in rows),
        "mean_best_match_delta": sum(r["mean_best_match_delta"] for r in rows) / len(rows),
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--replicates", type=int, default=120)
    p.add_argument("--lineages", type=int, default=16)
    p.add_argument("--steps", type=int, default=120)
    p.add_argument("--seed", type=int, default=20260819)
    p.add_argument("--out", type=Path, default=Path("data/results/constraint_mechanism_abm_v4_fixed_visit_budget.json"))
    args = p.parse_args()

    envelope = {}
    for saturation in (1.0, 1.5, 2.0, 2.5, 3.0):
        rows = [paired_run(args.seed + i, saturation, args.lineages, args.steps) for i in range(args.replicates)]
        envelope[str(saturation)] = summarize(rows)

    payload = {
        "model": "constraint_mechanism_abm_v4_fixed_visit_budget",
        "status": "structural_correction_mechanistic_test_not_empirical_evidence",
        "structural_change": "Pollinator richness no longer acts as visitation frequency. A fixed total visit budget is distributed across partner types via mean effective service and a saturating response.",
        "saturation_envelope": envelope,
        "claim_boundary": "The saturation values form a mechanism sensitivity envelope, not fitted empirical parameters. Izu outcomes are not used to select a preferred value."
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
