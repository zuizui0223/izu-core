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


@dataclass
class Pollinator:
    trait: float
    breadth: float
    introduced: bool
    service_quality: float


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
        # Deliberately independent of native/introduced status and geography.
        # Novel partners can therefore be poor, average or highly effective.
        service_quality=rng.uniform(0.20, 1.80),
    )


def encounter_score(lineage: LineageState, pollinator: Pollinator) -> float:
    mismatch = abs(lineage.trait - pollinator.trait)
    match = math.exp(-((mismatch / max(pollinator.breadth, 1e-6)) ** 2))
    return max(0.0, min(2.5, match * pollinator.service_quality))


def run_scenario(templates: list[LineageTemplate], s: Scenario, seed: int, steps: int) -> list[LineageState]:
    rng = random.Random(seed)
    lineages = [LineageState(template=t, trait=t.trait) for t in templates]
    pollinators = [make_pollinator(rng, s) for _ in range(s.n_pollinator_types)]

    for _ in range(steps):
        pollinators = [p for p in pollinators if rng.random() >= s.partner_loss]
        if rng.random() < s.partner_arrival:
            pollinators.append(make_pollinator(rng, s))

        for lin in lineages:
            if pollinators:
                scores = [encounter_score(lin, p) for p in pollinators]
                pollination = 1.0 - math.prod(1.0 - min(0.90, 0.18 * x) for x in scores)
            else:
                pollination = 0.0

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
    return lineages


def paired_run(seed: int, n_lineages: int = 16, steps: int = 120) -> dict:
    templates = make_lineages(random.Random(seed), n_lineages)
    mainland, oceanic = scenarios()
    m = run_scenario(templates, mainland, seed + 100_000, steps)
    o = run_scenario(templates, oceanic, seed + 200_000, steps)
    deltas = [oo.reproduction - mm.reproduction for mm, oo in zip(m, o)]
    eps = 1e-9
    return {
        "seed": seed,
        "n_lineages": n_lineages,
        "positive": sum(d > eps for d in deltas),
        "negative": sum(d < -eps for d in deltas),
        "near_zero": sum(abs(d) <= eps for d in deltas),
        "mean_delta": sum(deltas) / len(deltas),
        "mean_mainland_reproduction": sum(x.reproduction for x in m) / len(m),
        "mean_oceanic_reproduction": sum(x.reproduction for x in o) / len(o),
    }


def summarize(rows: list[dict]) -> dict:
    positive = sum(r["positive"] for r in rows)
    negative = sum(r["negative"] for r in rows)
    zero = sum(r["near_zero"] for r in rows)
    total = positive + negative + zero
    mixed_runs = sum(r["positive"] > 0 and r["negative"] > 0 for r in rows)
    return {
        "n_paired_runs": len(rows),
        "n_lineage_contrasts": total,
        "positive_lineage_responses": positive,
        "negative_lineage_responses": negative,
        "near_zero_lineage_responses": zero,
        "positive_fraction": positive / total,
        "negative_fraction": negative / total,
        "mixed_sign_runs": mixed_runs,
        "mixed_sign_run_fraction": mixed_runs / len(rows),
        "mean_delta": sum(r["mean_delta"] for r in rows) / len(rows),
        "mean_mainland_reproduction": sum(r["mean_mainland_reproduction"] for r in rows) / len(rows),
        "mean_oceanic_reproduction": sum(r["mean_oceanic_reproduction"] for r in rows) / len(rows),
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--replicates", type=int, default=120)
    p.add_argument("--lineages", type=int, default=16)
    p.add_argument("--steps", type=int, default=120)
    p.add_argument("--seed", type=int, default=20260819)
    p.add_argument("--out", type=Path, default=Path("data/results/constraint_mechanism_abm_v3_service_quality.json"))
    args = p.parse_args()

    rows = [paired_run(args.seed + i, args.lineages, args.steps) for i in range(args.replicates)]
    summary = summarize(rows)
    payload = {
        "model": "constraint_mechanism_abm_v3_service_quality",
        "status": "mechanistic_hypothesis_test_not_empirical_evidence",
        "mechanism_added_relative_to_v2": "partner-level service quality heterogeneity independent of geography and introduced/native status; fixed introduced-partner penalty removed",
        "summary": summary,
        "falsification": {
            "both_response_signs_present": summary["positive_lineage_responses"] > 0 and summary["negative_lineage_responses"] > 0,
            "mixed_sign_runs_present": summary["mixed_sign_runs"] > 0,
        },
        "claim_boundary": "Synthetic mechanism test only. Service-quality range is a broad mechanism probe, not an empirical effect-size fit, and Izu response frequencies are not a calibration target."
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
