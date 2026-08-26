from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import dataclass, replace
from pathlib import Path
from statistics import mean

OUT = Path("data/results/response_geometry_parameter_robustness.json")
EPS = 1e-9
TRAIT_GRID = tuple(i / 20 for i in range(21))


@dataclass(frozen=True)
class Scenario:
    n_pollinator_types: int
    partner_arrival: float
    partner_loss: float
    trait_dispersion: float
    generalist_fraction: float
    replacement_fraction: float


@dataclass(frozen=True)
class GeometryConfig:
    mainland: Scenario
    island: Scenario
    generalist_breadth: float = 0.42
    specialist_breadth: float = 0.16
    replacement_penalty: float = 0.82
    saturation: float = 2.0
    trait_adjustment: float = 0.03
    steps: int = 120


@dataclass(frozen=True)
class Pollinator:
    trait: float
    breadth: float
    introduced: bool


BASE = GeometryConfig(
    mainland=Scenario(9, 0.28, 0.015, 0.22, 0.35, 0.05),
    island=Scenario(4, 0.12, 0.055, 0.16, 0.58, 0.22),
)

SWEEPS = {
    "trait_dispersion_multiplier": (0.5, 1.0, 1.5),
    "generalist_fraction_shift": (-0.20, 0.0, 0.20),
    "replacement_fraction_shift": (-0.15, 0.0, 0.15),
    "partner_loss_multiplier": (0.5, 1.0, 1.5),
    "partner_arrival_multiplier": (0.5, 1.0, 1.5),
    "saturation": (1.0, 2.0, 3.0),
    "trait_adjustment": (0.0, 0.03, 0.06),
    "generalist_breadth": (0.30, 0.42, 0.54),
    "specialist_breadth": (0.10, 0.16, 0.22),
    "replacement_penalty": (0.65, 0.82, 1.0),
}


def clamp(x: float) -> float:
    return min(1.0, max(0.0, x))


def make_pollinator(rng: random.Random, scenario: Scenario, cfg: GeometryConfig) -> Pollinator:
    generalist = rng.random() < scenario.generalist_fraction
    return Pollinator(
        trait=clamp(rng.gauss(0.5, scenario.trait_dispersion)),
        breadth=cfg.generalist_breadth if generalist else cfg.specialist_breadth,
        introduced=rng.random() < scenario.replacement_fraction,
    )


def encounter(trait: float, pollinator: Pollinator, cfg: GeometryConfig) -> float:
    mismatch = abs(trait - pollinator.trait)
    match = math.exp(-((mismatch / max(pollinator.breadth, 1e-6)) ** 2))
    return clamp(match * (cfg.replacement_penalty if pollinator.introduced else 1.0))


def service(trait: float, pollinators: list[Pollinator], cfg: GeometryConfig) -> float:
    if not pollinators:
        return 0.0
    mean_match = mean(encounter(trait, p, cfg) for p in pollinators)
    return clamp(1.0 - math.exp(-cfg.saturation * mean_match))


def endpoint(initial_trait: float, scenario: Scenario, seed: int, cfg: GeometryConfig) -> tuple[float, float]:
    rng = random.Random(seed)
    trait = initial_trait
    pollinators = [make_pollinator(rng, scenario, cfg) for _ in range(scenario.n_pollinator_types)]
    for _ in range(cfg.steps):
        pollinators = [p for p in pollinators if rng.random() >= scenario.partner_loss]
        if rng.random() < scenario.partner_arrival:
            pollinators.append(make_pollinator(rng, scenario, cfg))
        current_service = service(trait, pollinators, cfg)
        if pollinators and current_service < 0.45 and cfg.trait_adjustment > 0.0:
            best = max(pollinators, key=lambda p: encounter(trait, p, cfg))
            trait = clamp(trait + cfg.trait_adjustment * (best.trait - trait))
    return trait, service(trait, pollinators, cfg)


def sign(x: float) -> int:
    if x > EPS:
        return 1
    if x < -EPS:
        return -1
    return 0


def summarize_trait(initial_trait: float, cfg: GeometryConfig, replicates: int, seed: int) -> dict:
    deltas = []
    endpoint_trait_deltas = []
    for rep in range(replicates):
        run_seed = seed + rep * 10_000
        mt, ms = endpoint(initial_trait, cfg.mainland, run_seed + 100_000, cfg)
        it, iserv = endpoint(initial_trait, cfg.island, run_seed + 200_000, cfg)
        deltas.append(iserv - ms)
        endpoint_trait_deltas.append(it - mt)
    positive = sum(d > EPS for d in deltas)
    negative = sum(d < -EPS for d in deltas)
    return {
        "initial_trait": initial_trait,
        "mean_delta_service": mean(deltas),
        "mean_delta_endpoint_trait": mean(endpoint_trait_deltas),
        "positive_replicates": positive,
        "negative_replicates": negative,
        "near_zero_replicates": replicates - positive - negative,
        "positive_fraction": positive / replicates,
        "negative_fraction": negative / replicates,
        "mean_sign": sign(mean(deltas)),
    }


def geometry(cfg: GeometryConfig, replicates: int, seed: int) -> dict:
    rows = [summarize_trait(t, cfg, replicates, seed + i * 1_000_000) for i, t in enumerate(TRAIT_GRID)]
    signs = [row["mean_sign"] for row in rows]
    sign_switches = sum(a != b for a, b in zip(signs, signs[1:]) if a != 0 and b != 0)
    mixed_geometry = 1 in signs and -1 in signs
    positive_traits = [row["initial_trait"] for row in rows if row["mean_sign"] > 0]
    negative_traits = [row["initial_trait"] for row in rows if row["mean_sign"] < 0]
    return {
        "mixed_sign_geometry": mixed_geometry,
        "sign_switch_count_across_trait_grid": sign_switches,
        "positive_trait_range": [min(positive_traits), max(positive_traits)] if positive_traits else None,
        "negative_trait_range": [min(negative_traits), max(negative_traits)] if negative_traits else None,
        "trait_rows": rows,
    }


def shifted_fraction(x: float, delta: float) -> float:
    return min(0.99, max(0.01, x + delta))


def scaled_probability(x: float, multiplier: float) -> float:
    return min(0.99, max(0.0, x * multiplier))


def apply_sweep(cfg: GeometryConfig, name: str, value: float) -> GeometryConfig:
    if name == "trait_dispersion_multiplier":
        return replace(cfg, mainland=replace(cfg.mainland, trait_dispersion=cfg.mainland.trait_dispersion * value), island=replace(cfg.island, trait_dispersion=cfg.island.trait_dispersion * value))
    if name == "generalist_fraction_shift":
        return replace(cfg, mainland=replace(cfg.mainland, generalist_fraction=shifted_fraction(cfg.mainland.generalist_fraction, value)), island=replace(cfg.island, generalist_fraction=shifted_fraction(cfg.island.generalist_fraction, value)))
    if name == "replacement_fraction_shift":
        return replace(cfg, mainland=replace(cfg.mainland, replacement_fraction=shifted_fraction(cfg.mainland.replacement_fraction, value)), island=replace(cfg.island, replacement_fraction=shifted_fraction(cfg.island.replacement_fraction, value)))
    if name == "partner_loss_multiplier":
        return replace(cfg, mainland=replace(cfg.mainland, partner_loss=scaled_probability(cfg.mainland.partner_loss, value)), island=replace(cfg.island, partner_loss=scaled_probability(cfg.island.partner_loss, value)))
    if name == "partner_arrival_multiplier":
        return replace(cfg, mainland=replace(cfg.mainland, partner_arrival=scaled_probability(cfg.mainland.partner_arrival, value)), island=replace(cfg.island, partner_arrival=scaled_probability(cfg.island.partner_arrival, value)))
    if name in {"saturation", "trait_adjustment", "generalist_breadth", "specialist_breadth", "replacement_penalty"}:
        return replace(cfg, **{name: value})
    raise KeyError(name)


def build(replicates: int = 24, seed: int = 20260826) -> dict:
    baseline = geometry(BASE, replicates, seed)
    sweeps = {}
    stable_mixed = 0
    total = 0
    for name, values in SWEEPS.items():
        rows = []
        for index, value in enumerate(values):
            cfg = apply_sweep(BASE, name, value)
            result = geometry(cfg, replicates, seed + 10_000_000 + total * 1_000_000 + index * 100_000)
            rows.append({"value": value, **result})
            stable_mixed += int(result["mixed_sign_geometry"])
            total += 1
        sweeps[name] = rows
    return {
        "analysis": "response_geometry_parameter_robustness",
        "status": "scientific_reassessment_gate_phase1",
        "question": "Across plant starting positions, when does the island-minus-mainland functional-service response change sign, and does that sign geometry persist under plausible perturbations of the declared model parameters?",
        "baseline": baseline,
        "parameter_sweeps": sweeps,
        "robustness_summary": {
            "one_factor_parameter_settings": total,
            "mixed_sign_geometry_settings": stable_mixed,
            "mixed_sign_geometry_fraction": stable_mixed / total if total else None,
        },
        "design": {
            "trait_grid": list(TRAIT_GRID),
            "replicates_per_trait_parameter_setting": replicates,
            "steps": BASE.steps,
            "sweeps": {name: list(values) for name, values in SWEEPS.items()},
            "baseline_scenario_source": "declared v4 mainland-like and oceanic-island parameterization",
            "empirical_inputs_loaded": [],
        },
        "claim_boundary": "This is a synthetic response-geometry and one-factor-at-a-time robustness map. It does not estimate natural prevalence, fit empirical island data, or establish that the synthetic trait coordinate equals one named floral trait. A stable mixed-sign region is evidence of model robustness only; failure of stability triggers conceptual reframing rather than retuning.",
        "next_gate": "If phase 1 retains interpretable mixed-sign regions, run a joint multi-parameter design around the transition surfaces and separately map local-context sign changes and assurance sign-rescue thresholds.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20260826)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build(args.replicates, args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload["robustness_summary"], indent=2))


if __name__ == "__main__":
    main()
