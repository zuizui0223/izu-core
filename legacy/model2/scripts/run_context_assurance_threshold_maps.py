from __future__ import annotations

import argparse
import dataclasses
import importlib.util
import json
import random
import sys
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
V4_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v4_fixed_visit_budget.py"
V9_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v9_local_plant_opportunity.py"
V10_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v10_effective_service_dependency.py"
OUT = ROOT / "data/results/context_assurance_threshold_maps.json"

SATURATIONS = (1.0, 2.0, 3.0)
SUPPORT_STRENGTHS = (0.0, 0.10, 0.25, 0.40, 0.50, 0.60, 0.75)
ASSURANCE_MULTIPLIERS = (0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0)
QUALITY_STRENGTH = 1.0
EPS = 1e-12


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sign(value: float) -> int:
    if value > EPS:
        return 1
    if value < -EPS:
        return -1
    return 0


def disable_assurance(templates: list) -> list:
    return [
        dataclasses.replace(template, assurance_ceiling=0.0, assurance_responsiveness=0.0)
        for template in templates
    ]


def scale_assurance(templates: list, multiplier: float) -> list:
    if multiplier < 0:
        raise ValueError("assurance multiplier must be nonnegative")
    return [
        dataclasses.replace(
            template,
            assurance_ceiling=min(1.0, float(template.assurance_ceiling) * multiplier),
            assurance_responsiveness=min(1.0, float(template.assurance_responsiveness) * multiplier),
        )
        for template in templates
    ]


def delta(island: dict, mainland: dict, name: str, field: str) -> float:
    return float(island[name][field]) - float(mainland[name][field])


def opportunities(v4, v9, run_seed: int, saturation: float, n_lineages: int, steps: int):
    mainland, _, _ = v9.run_weighted_network(
        0.0,
        run_seed,
        saturation,
        support_seed=run_seed + 31_000_000,
        support_strength=0.0,
        weight_seed=run_seed + 41_000_000,
        weight_strength=0.0,
        n_lineages=n_lineages,
        steps=steps,
    )
    island, _, _ = v9.run_weighted_network(
        1.0,
        run_seed,
        saturation,
        support_seed=run_seed + 31_000_000,
        support_strength=0.0,
        weight_seed=run_seed + 41_000_000,
        weight_strength=0.0,
        n_lineages=n_lineages,
        steps=steps,
    )
    return mainland, island


def simulate_pair(v10, v9, mainland_opportunity, island_opportunity, templates: list, *, saturation: float, support_strength: float, contexts: int, context_seed: int):
    common = dict(
        templates=templates,
        v9=v9,
        saturation=saturation,
        support_strength=support_strength,
        contexts=contexts,
        context_seed=context_seed,
        quality_strength=QUALITY_STRENGTH,
    )
    mainland = v10.simulate_endpoint(
        mainland_opportunity,
        quality_stream_offset=1_000_000,
        **common,
    )
    island = v10.simulate_endpoint(
        island_opportunity,
        quality_stream_offset=2_000_000,
        **common,
    )
    return mainland, island


def build(*, replicates: int = 4, contexts: int = 4, n_lineages: int = 24, steps: int = 120, seed: int = 20260826) -> dict:
    v4 = load_module(V4_SCRIPT, "threshold_map_v4")
    v9 = load_module(V9_SCRIPT, "threshold_map_v9")
    v10 = load_module(V10_SCRIPT, "threshold_map_v10")

    context_counts = {str(value): {"sign_changes": 0, "negative_to_nonnegative": 0, "positive_to_nonpositive": 0, "lineage_contrasts": 0} for value in SUPPORT_STRENGTHS}
    assurance_counts = {str(value): {"eligible_baseline_declines": 0, "sign_rescues": 0, "magnitude_improvements": 0} for value in ASSURANCE_MULTIPLIERS}
    context_first_thresholds = []
    assurance_first_thresholds = []
    service_mismatches_across_assurance = 0

    for saturation in SATURATIONS:
        for replicate in range(replicates):
            run_seed = seed + replicate + int(saturation * 10_000)
            base_templates = v4.make_lineages(random.Random(run_seed), n_lineages)
            no_assurance = disable_assurance(base_templates)
            mainland_opportunity, island_opportunity = opportunities(v4, v9, run_seed, saturation, n_lineages, steps)
            context_seed = run_seed + 51_000_000
            names = [f"lineage_{i + 1}" for i in range(n_lineages)]

            context_outputs = {}
            for support_strength in SUPPORT_STRENGTHS:
                context_outputs[support_strength] = simulate_pair(
                    v10,
                    v9,
                    mainland_opportunity,
                    island_opportunity,
                    no_assurance,
                    saturation=saturation,
                    support_strength=support_strength,
                    contexts=contexts,
                    context_seed=context_seed,
                )
            baseline_mainland, baseline_island = context_outputs[0.0]
            for name in names:
                baseline_delta = delta(baseline_island, baseline_mainland, name, "mean_reproduction")
                baseline_sign = sign(baseline_delta)
                first_context = None
                for support_strength in SUPPORT_STRENGTHS:
                    mainland, island = context_outputs[support_strength]
                    current_delta = delta(island, mainland, name, "mean_reproduction")
                    current_sign = sign(current_delta)
                    cell = context_counts[str(support_strength)]
                    cell["lineage_contrasts"] += 1
                    changed = current_sign != baseline_sign
                    cell["sign_changes"] += int(changed)
                    cell["negative_to_nonnegative"] += int(baseline_sign < 0 and current_sign >= 0)
                    cell["positive_to_nonpositive"] += int(baseline_sign > 0 and current_sign <= 0)
                    if changed and first_context is None and support_strength > 0:
                        first_context = support_strength
                if first_context is not None:
                    context_first_thresholds.append(first_context)

            assurance_outputs = {}
            for multiplier in ASSURANCE_MULTIPLIERS:
                templates = scale_assurance(base_templates, multiplier)
                assurance_outputs[multiplier] = simulate_pair(
                    v10,
                    v9,
                    mainland_opportunity,
                    island_opportunity,
                    templates,
                    saturation=saturation,
                    support_strength=0.50,
                    contexts=contexts,
                    context_seed=context_seed,
                )
            zero_mainland, zero_island = assurance_outputs[0.0]
            for name in names:
                baseline_reproduction = delta(zero_island, zero_mainland, name, "mean_reproduction")
                baseline_service = delta(zero_island, zero_mainland, name, "mean_effective_service")
                eligible = baseline_service < -EPS and baseline_reproduction < -EPS
                first_assurance = None
                for multiplier in ASSURANCE_MULTIPLIERS:
                    mainland, island = assurance_outputs[multiplier]
                    current_reproduction = delta(island, mainland, name, "mean_reproduction")
                    current_service = delta(island, mainland, name, "mean_effective_service")
                    if abs(current_service - baseline_service) > EPS:
                        service_mismatches_across_assurance += 1
                    cell = assurance_counts[str(multiplier)]
                    cell["eligible_baseline_declines"] += int(eligible)
                    cell["sign_rescues"] += int(eligible and current_reproduction >= -EPS)
                    cell["magnitude_improvements"] += int(eligible and current_reproduction > baseline_reproduction + EPS)
                    if eligible and current_reproduction >= -EPS and first_assurance is None and multiplier > 0:
                        first_assurance = multiplier
                if first_assurance is not None:
                    assurance_first_thresholds.append(first_assurance)

    for cell in context_counts.values():
        n = cell["lineage_contrasts"]
        cell["sign_change_fraction"] = cell["sign_changes"] / n if n else None
    for cell in assurance_counts.values():
        n = cell["eligible_baseline_declines"]
        cell["sign_rescue_fraction"] = cell["sign_rescues"] / n if n else None
        cell["magnitude_improvement_fraction"] = cell["magnitude_improvements"] / n if n else None

    return {
        "analysis": "context_assurance_threshold_maps",
        "status": "scientific_reassessment_gate_phase3",
        "context_map": {
            "semantic_definition": "support_strength is local availability / interaction filtering stress, not beneficial support",
            "support_strengths": list(SUPPORT_STRENGTHS),
            "by_strength": context_counts,
            "lineages_with_any_sign_change": len(context_first_thresholds),
            "median_first_sign_change_strength": median(context_first_thresholds) if context_first_thresholds else None,
        },
        "assurance_map": {
            "assurance_multipliers": list(ASSURANCE_MULTIPLIERS),
            "by_multiplier": assurance_counts,
            "lineages_with_any_sign_rescue": len(assurance_first_thresholds),
            "median_first_sign_rescue_multiplier": median(assurance_first_thresholds) if assurance_first_thresholds else None,
            "upstream_service_mismatch_count": service_mismatches_across_assurance,
            "upstream_service_identical_across_assurance_multipliers": service_mismatches_across_assurance == 0,
        },
        "design": {
            "saturations": list(SATURATIONS),
            "replicates_per_saturation": replicates,
            "contexts": contexts,
            "lineages": n_lineages,
            "steps": steps,
            "common_seed_ensemble_across_threshold_values": True,
            "empirical_inputs_loaded": [],
        },
        "interpretation_rule": "Context thresholds quantify when stronger local filtering changes response sign rather than merely magnitude. Assurance thresholds quantify how far the existing compensating route must be amplified before a service-decline lineage crosses the reproduction sign boundary.",
        "claim_boundary": "These thresholds are synthetic model properties, not empirical ecological thresholds. Support strength is filtering stress, and assurance multipliers are sensitivity probes rather than fitted biological values.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=4)
    parser.add_argument("--contexts", type=int, default=4)
    parser.add_argument("--lineages", type=int, default=24)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--seed", type=int, default=20260826)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build(replicates=args.replicates, contexts=args.contexts, n_lineages=args.lineages, steps=args.steps, seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({
        "context_median_first_sign_change_strength": payload["context_map"]["median_first_sign_change_strength"],
        "assurance_median_first_sign_rescue_multiplier": payload["assurance_map"]["median_first_sign_rescue_multiplier"],
        "assurance_service_identical": payload["assurance_map"]["upstream_service_identical_across_assurance_multipliers"],
    }, indent=2))


if __name__ == "__main__":
    main()
