from __future__ import annotations

import argparse
import dataclasses
import importlib.util
import json
import random
import sys
from itertools import product
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
V4_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v4_fixed_visit_budget.py"
V9_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v9_local_plant_opportunity.py"
V10_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v10_effective_service_dependency.py"
OUT = ROOT / "data/results/constraint_mechanism_abm_v11_factorial_branching.json"
SATURATIONS = (1.0, 2.0, 3.0)
SUPPORT_ON_STRENGTH = 0.5
DEPENDENCY_COMMON_VALUE = 0.65  # midpoint of the frozen v4 U(0.35, 0.95) range
EPS = 1e-12
FACTORS = ("local_support", "dependency_heterogeneity", "assurance_responsiveness", "partner_effectiveness")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def config_id(config: dict[str, bool]) -> str:
    return "__".join(f"{name}_{'on' if config[name] else 'off'}" for name in FACTORS)


def all_configs() -> tuple[dict[str, bool], ...]:
    return tuple(
        dict(zip(FACTORS, values))
        for values in product((False, True), repeat=len(FACTORS))
    )


def modified_templates(base_templates: list, config: dict[str, bool]) -> list:
    result = []
    for template in base_templates:
        changes = {}
        if not config["dependency_heterogeneity"]:
            changes["pollinator_dependency"] = DEPENDENCY_COMMON_VALUE
        if not config["assurance_responsiveness"]:
            changes["assurance_responsiveness"] = 0.0
        result.append(dataclasses.replace(template, **changes))
    return result


def sign(value: float) -> int:
    if value > EPS:
        return 1
    if value < -EPS:
        return -1
    return 0


def branching_balance(positive: int, negative: int) -> float:
    n = positive + negative
    return 0.0 if n == 0 else 2.0 * min(positive, negative) / n


def evaluate_config(
    *,
    config: dict[str, bool],
    base_templates: list,
    mainland_opportunity,
    island_opportunity,
    v9,
    v10,
    saturation: float,
    contexts: int,
    context_seed: int,
) -> list[float]:
    templates = modified_templates(base_templates, config)
    support_strength = SUPPORT_ON_STRENGTH if config["local_support"] else 0.0
    quality_strength = v10.QUALITY_STRENGTH if config["partner_effectiveness"] else 0.0
    common = dict(
        templates=templates,
        v9=v9,
        saturation=saturation,
        support_strength=support_strength,
        contexts=contexts,
        context_seed=context_seed,
        quality_strength=quality_strength,
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
    names = [f"lineage_{index + 1}" for index in range(len(templates))]
    return [
        island[name]["mean_reproduction"] - mainland[name]["mean_reproduction"]
        for name in names
    ]


def summarize_config(values: list[float], mixed_runs: int, run_count: int) -> dict:
    positive = sum(value > EPS for value in values)
    negative = sum(value < -EPS for value in values)
    equal = len(values) - positive - negative
    return {
        "lineage_contrasts": len(values),
        "positive": positive,
        "negative": negative,
        "equal": equal,
        "positive_fraction_nonzero": positive / (positive + negative) if positive + negative else None,
        "branching_balance": branching_balance(positive, negative),
        "mixed_sign_runs": mixed_runs,
        "mixed_sign_run_fraction": mixed_runs / run_count if run_count else None,
        "mean_oceanic_minus_mainland_reproduction": mean(values) if values else None,
        "mean_absolute_reproductive_contrast": mean(abs(value) for value in values) if values else None,
    }


def build(
    *,
    replicates: int = 4,
    contexts: int = 4,
    n_lineages: int = 24,
    steps: int = 120,
    seed: int = 20260822,
) -> dict:
    v4 = load_module(V4_SCRIPT, "abm_v11_v4")
    v9 = load_module(V9_SCRIPT, "abm_v11_v9")
    v10 = load_module(V10_SCRIPT, "abm_v11_v10")
    configs = all_configs()
    ids = {config_id(config): config for config in configs}
    contrast_values: dict[str, list[float]] = {key: [] for key in ids}
    contrast_signs: dict[str, dict[tuple[float, int, int], int]] = {key: {} for key in ids}
    mixed_runs: dict[str, int] = {key: 0 for key in ids}
    run_count = 0

    for saturation in SATURATIONS:
        for replicate in range(replicates):
            run_seed = seed + replicate + int(saturation * 10_000)
            base_templates = v4.make_lineages(random.Random(run_seed), n_lineages)
            mainland_opportunity, _, _ = v9.run_weighted_network(
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
            island_opportunity, _, _ = v9.run_weighted_network(
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
            context_seed = run_seed + 51_000_000
            for key, config in ids.items():
                values = evaluate_config(
                    config=config,
                    base_templates=base_templates,
                    mainland_opportunity=mainland_opportunity,
                    island_opportunity=island_opportunity,
                    v9=v9,
                    v10=v10,
                    saturation=saturation,
                    contexts=contexts,
                    context_seed=context_seed,
                )
                contrast_values[key].extend(values)
                signs = [sign(value) for value in values]
                if 1 in signs and -1 in signs:
                    mixed_runs[key] += 1
                for lineage_index, value_sign in enumerate(signs):
                    contrast_signs[key][(saturation, replicate, lineage_index)] = value_sign
            run_count += 1

    summaries = {
        key: {
            "factors": config,
            **summarize_config(contrast_values[key], mixed_runs[key], run_count),
        }
        for key, config in ids.items()
    }
    full_config = {name: True for name in FACTORS}
    full_id = config_id(full_config)
    full = summaries[full_id]

    drop_one = {}
    for factor in FACTORS:
        config = dict(full_config)
        config[factor] = False
        key = config_id(config)
        dropped = summaries[key]
        paired_keys = sorted(contrast_signs[full_id])
        sign_flips = sum(
            contrast_signs[full_id][pair_key] != contrast_signs[key][pair_key]
            for pair_key in paired_keys
        )
        drop_one[factor] = {
            "ablated_config": key,
            "branching_balance_full": full["branching_balance"],
            "branching_balance_ablated": dropped["branching_balance"],
            "branching_balance_loss": full["branching_balance"] - dropped["branching_balance"],
            "mixed_sign_run_fraction_full": full["mixed_sign_run_fraction"],
            "mixed_sign_run_fraction_ablated": dropped["mixed_sign_run_fraction"],
            "mixed_sign_run_fraction_loss": full["mixed_sign_run_fraction"] - dropped["mixed_sign_run_fraction"],
            "positive_full": full["positive"],
            "positive_ablated": dropped["positive"],
            "negative_full": full["negative"],
            "negative_ablated": dropped["negative"],
            "paired_branch_sign_changes": sign_flips,
            "paired_branch_sign_change_fraction": sign_flips / len(paired_keys) if paired_keys else None,
        }

    ranked = sorted(
        FACTORS,
        key=lambda factor: (
            drop_one[factor]["branching_balance_loss"],
            drop_one[factor]["mixed_sign_run_fraction_loss"],
            drop_one[factor]["paired_branch_sign_change_fraction"],
        ),
        reverse=True,
    )

    return {
        "analysis": "constraint_mechanism_abm_v11_factorial_branching_causes",
        "status": "synthetic_matched_factorial_ablation_after_v10",
        "scientific_question": (
            "Conditional on the frozen v4 island-scale opportunity generator, which downstream components are necessary or influential for mixed reproductive response branching?"
        ),
        "factors": {
            "local_support": {
                "on": f"v9 local plant/pollinator/pair support at generic strength {SUPPORT_ON_STRENGTH}",
                "off": "support_strength=0; support fixed while inherited within-support weight variation remains",
            },
            "dependency_heterogeneity": {
                "on": "frozen v4 lineage-specific U(0.35,0.95)",
                "off": f"all lineages set to frozen-range midpoint {DEPENDENCY_COMMON_VALUE}",
            },
            "assurance_responsiveness": {
                "on": "frozen v4 lineage-specific responsiveness",
                "off": "responsiveness set to zero; baseline assurance and assurance ceilings retained",
            },
            "partner_effectiveness": {
                "on": "v10 frozen geography-independent [0.2,1.8] broad quality probe",
                "off": "all quality multipliers equal one",
            },
        },
        "scope_boundary": (
            "Dependency and assurance ablations operate on the downstream translation stage while the v4 island-scale opportunity network is held fixed. "
            "They therefore test conditional downstream necessity/influence, not full eco-evolutionary necessity including feedback during upstream network evolution."
        ),
        "design": {
            "factorial_configurations": len(configs),
            "saturation_envelope": list(SATURATIONS),
            "replicates_per_saturation": replicates,
            "local_contexts_per_endpoint": contexts,
            "lineages_per_run": n_lineages,
            "evolution_steps": steps,
            "paired_runs_per_config": run_count,
            "lineage_contrasts_per_config": run_count * n_lineages,
            "empirical_inputs_loaded": [],
            "izu_target_frequencies_loaded": False,
            "external_target_values_loaded": False,
        },
        "full_model_config": full_id,
        "full_model_summary": full,
        "drop_one_ablation": drop_one,
        "factor_ranking_by_branching_balance_loss": ranked,
        "all_configurations": summaries,
        "interpretation_rule": (
            "A large positive branching-balance loss after dropping a factor indicates that the factor helps sustain two-sided reproductive branching under matched upstream states. "
            "A near-zero or negative loss means that factor is not necessary for aggregate branching under this conditional model, even if paired branch identities change."
        ),
        "claim_boundary": (
            "This is a synthetic causal-structure diagnostic, not empirical mediation. No known Izu response frequency is fit. "
            "A factor can be important in nature even if it is non-necessary in this model; empirical confirmation requires compatible joint island data."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=4)
    parser.add_argument("--contexts", type=int, default=4)
    parser.add_argument("--lineages", type=int, default=24)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--seed", type=int, default=20260822)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build(
        replicates=args.replicates,
        contexts=args.contexts,
        n_lineages=args.lineages,
        steps=args.steps,
        seed=args.seed,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({
        "full_model": payload["full_model_summary"],
        "drop_one": payload["drop_one_ablation"],
        "ranking": payload["factor_ranking_by_branching_balance_loss"],
    }, indent=2))


if __name__ == "__main__":
    main()
