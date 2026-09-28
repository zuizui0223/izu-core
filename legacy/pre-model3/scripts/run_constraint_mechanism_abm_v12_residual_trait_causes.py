from __future__ import annotations

import argparse
import dataclasses
import importlib.util
import json
import math
import random
import sys
from itertools import product
from pathlib import Path
from statistics import mean

from channel_id.external_archipelago_network import WeightedNetwork

ROOT = Path(__file__).resolve().parents[1]
V4_CORE = ROOT / "scripts/run_constraint_mechanism_abm_v4_fixed_visit_budget.py"
GRADIENT = ROOT / "scripts/run_abm_v4_global_continuous_isolation_gradient.py"
V11_FROZEN = ROOT / "data/results/constraint_mechanism_abm_v11_factorial_summary_frozen.json"
OUT = ROOT / "data/results/constraint_mechanism_abm_v12_residual_trait_causes.json"
SATURATIONS = (1.0, 2.0, 3.0)
FACTORS = ("initial_trait_heterogeneity", "trait_adjustment_heterogeneity", "assurance_ceiling_heterogeneity")
COMMON_TRAIT = 0.5
COMMON_TRAIT_ADJUSTMENT = (0.01 + 0.055) / 2.0
COMMON_ASSURANCE_CEILING = 0.5
COMMON_DEPENDENCY = 0.65
FIXED_ASSURANCE_RESPONSIVENESS = 0.0
INITIAL_ASSURANCE = 0.08
EPS = 1e-12


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def all_configs() -> tuple[dict[str, bool], ...]:
    return tuple(dict(zip(FACTORS, values)) for values in product((False, True), repeat=3))


def config_id(config: dict[str, bool]) -> str:
    return "__".join(f"{name}_{'on' if config[name] else 'off'}" for name in FACTORS)


def transform_templates(base_templates: list, config: dict[str, bool]) -> list:
    transformed = []
    for template in base_templates:
        transformed.append(
            dataclasses.replace(
                template,
                trait=template.trait if config["initial_trait_heterogeneity"] else COMMON_TRAIT,
                pollinator_dependency=COMMON_DEPENDENCY,
                assurance_ceiling=(
                    template.assurance_ceiling
                    if config["assurance_ceiling_heterogeneity"]
                    else COMMON_ASSURANCE_CEILING
                ),
                assurance_responsiveness=FIXED_ASSURANCE_RESPONSIVENESS,
                trait_adjustment=(
                    template.trait_adjustment
                    if config["trait_adjustment_heterogeneity"]
                    else COMMON_TRAIT_ADJUSTMENT
                ),
            )
        )
    return transformed


def run_weighted_network_with_templates(
    *,
    v4,
    gradient,
    templates: list,
    isolation_index: float,
    seed: int,
    saturation: float,
    steps: int,
) -> WeightedNetwork:
    scenario = gradient.scenario_at(v4, isolation_index)
    rng = random.Random(seed + 100_000)
    lineages = [v4.LineageState(template=t, trait=t.trait) for t in templates]
    pollinators = [v4.make_pollinator(rng, scenario) for _ in range(scenario.n_pollinator_types)]

    for _ in range(steps):
        pollinators = [p for p in pollinators if rng.random() >= scenario.partner_loss]
        if rng.random() < scenario.partner_arrival:
            pollinators.append(v4.make_pollinator(rng, scenario))
        for lineage in lineages:
            scores = [v4.encounter_score(lineage, pollinator) for pollinator in pollinators]
            pollination = v4.fixed_budget_pollination(scores, saturation)
            dependency = lineage.template.pollinator_dependency
            autonomous = lineage.template.assurance_ceiling * lineage.assurance
            lineage.reproduction = v4.clamp(
                1.0
                - (1.0 - dependency * pollination)
                * (1.0 - (1.0 - dependency) * autonomous)
            )
            if pollinators and pollination < 0.45:
                best = max(pollinators, key=lambda pollinator: v4.encounter_score(lineage, pollinator))
                lineage.trait = v4.clamp(
                    lineage.trait
                    + lineage.template.trait_adjustment * (best.trait - lineage.trait)
                )
            # assurance_responsiveness is frozen at zero in v12, so no state update can occur.

    names = [f"lineage_{index + 1}" for index in range(len(lineages))]
    if not pollinators:
        return WeightedNetwork.from_rows(names, ["no_pollinator"], [[0.0] for _ in lineages])
    denominator = float(len(pollinators))
    matrix = []
    for lineage in lineages:
        scores = [v4.encounter_score(lineage, pollinator) for pollinator in pollinators]
        matrix.append([score / denominator for score in scores])
    return WeightedNetwork.from_rows(
        names,
        [f"pollinator_{index + 1}" for index in range(len(pollinators))],
        matrix,
    )


def reproduction_from_row(row: tuple[float, ...], *, saturation: float, assurance_ceiling: float) -> float:
    # v5 weight realization is deliberately removed here. Under quality=1 its row-sum
    # conservation makes it algebraically invisible to the v10 service transform.
    opportunity = sum(row)
    service = 1.0 - math.exp(-saturation * opportunity)
    autonomous = assurance_ceiling * INITIAL_ASSURANCE
    pollinator_route = COMMON_DEPENDENCY * service
    assurance_route = (1.0 - COMMON_DEPENDENCY) * autonomous
    return 1.0 - (1.0 - pollinator_route) * (1.0 - assurance_route)


def paired_deltas(
    *,
    v4,
    gradient,
    templates: list,
    seed: int,
    saturation: float,
    steps: int,
) -> list[float]:
    mainland = run_weighted_network_with_templates(
        v4=v4,
        gradient=gradient,
        templates=templates,
        isolation_index=0.0,
        seed=seed,
        saturation=saturation,
        steps=steps,
    )
    oceanic = run_weighted_network_with_templates(
        v4=v4,
        gradient=gradient,
        templates=templates,
        isolation_index=1.0,
        seed=seed,
        saturation=saturation,
        steps=steps,
    )
    if mainland.plant_names != oceanic.plant_names:
        raise RuntimeError("paired opportunity networks lost lineage identity")
    deltas = []
    for index, template in enumerate(templates):
        m = reproduction_from_row(
            mainland.matrix[index],
            saturation=saturation,
            assurance_ceiling=template.assurance_ceiling,
        )
        o = reproduction_from_row(
            oceanic.matrix[index],
            saturation=saturation,
            assurance_ceiling=template.assurance_ceiling,
        )
        deltas.append(o - m)
    return deltas


def sign(value: float) -> int:
    if value > EPS:
        return 1
    if value < -EPS:
        return -1
    return 0


def within_run_balance(values: list[float]) -> float:
    positive = sum(value > EPS for value in values)
    negative = sum(value < -EPS for value in values)
    n = positive + negative
    return 0.0 if n == 0 else 2.0 * min(positive, negative) / n


def summarize(values: list[float], run_values: list[list[float]]) -> dict:
    positive = sum(value > EPS for value in values)
    negative = sum(value < -EPS for value in values)
    equal = len(values) - positive - negative
    mixed = sum(
        any(value > EPS for value in run) and any(value < -EPS for value in run)
        for run in run_values
    )
    return {
        "lineage_contrasts": len(values),
        "positive": positive,
        "negative": negative,
        "equal": equal,
        "aggregate_branching_balance": (
            0.0 if positive + negative == 0 else 2.0 * min(positive, negative) / (positive + negative)
        ),
        "mixed_sign_runs": mixed,
        "mixed_sign_run_fraction": mixed / len(run_values) if run_values else None,
        "mean_within_run_branching_balance": mean(within_run_balance(run) for run in run_values),
        "mean_oceanic_minus_mainland_reproduction": mean(values) if values else None,
    }


def build(*, replicates: int = 4, n_lineages: int = 24, steps: int = 120, seed: int = 20260822) -> dict:
    v4 = load_module(V4_CORE, "abm_v12_v4")
    gradient = load_module(GRADIENT, "abm_v12_gradient")
    configs = all_configs()
    ids = {config_id(config): config for config in configs}
    flat_values: dict[str, list[float]] = {key: [] for key in ids}
    per_run_values: dict[str, list[list[float]]] = {key: [] for key in ids}
    signs: dict[str, dict[tuple[float, int, int], int]] = {key: {} for key in ids}

    for saturation in SATURATIONS:
        for replicate in range(replicates):
            run_seed = seed + replicate + int(saturation * 10_000)
            base_templates = v4.make_lineages(random.Random(run_seed), n_lineages)
            for key, config in ids.items():
                templates = transform_templates(base_templates, config)
                values = paired_deltas(
                    v4=v4,
                    gradient=gradient,
                    templates=templates,
                    seed=run_seed,
                    saturation=saturation,
                    steps=steps,
                )
                flat_values[key].extend(values)
                per_run_values[key].append(values)
                for lineage_index, value in enumerate(values):
                    signs[key][(saturation, replicate, lineage_index)] = sign(value)

    summaries = {
        key: {"factors": config, **summarize(flat_values[key], per_run_values[key])}
        for key, config in ids.items()
    }
    full_id = config_id({factor: True for factor in FACTORS})
    none_id = config_id({factor: False for factor in FACTORS})
    full = summaries[full_id]
    none = summaries[none_id]
    drop_one = {}
    for factor in FACTORS:
        config = {name: True for name in FACTORS}
        config[factor] = False
        key = config_id(config)
        dropped = summaries[key]
        paired_keys = signs[full_id]
        branch_changes = sum(signs[full_id][pair_key] != signs[key][pair_key] for pair_key in paired_keys)
        drop_one[factor] = {
            "ablated_config": key,
            "mixed_sign_run_fraction_full": full["mixed_sign_run_fraction"],
            "mixed_sign_run_fraction_ablated": dropped["mixed_sign_run_fraction"],
            "mixed_sign_run_fraction_loss": full["mixed_sign_run_fraction"] - dropped["mixed_sign_run_fraction"],
            "mean_within_run_branching_balance_full": full["mean_within_run_branching_balance"],
            "mean_within_run_branching_balance_ablated": dropped["mean_within_run_branching_balance"],
            "mean_within_run_branching_balance_loss": full["mean_within_run_branching_balance"] - dropped["mean_within_run_branching_balance"],
            "paired_branch_sign_changes": branch_changes,
            "paired_branch_sign_change_fraction": branch_changes / len(paired_keys),
        }

    v11_reference = json.loads(V11_FROZEN.read_text())
    v11_all_off = v11_reference["all_four_tested_downstream_factors_off"]
    nesting = {
        "expected_positive": v11_all_off["positive"],
        "observed_positive": full["positive"],
        "expected_negative": v11_all_off["negative"],
        "observed_negative": full["negative"],
        "expected_equal": v11_all_off["equal"],
        "observed_equal": full["equal"],
        "expected_mixed_sign_run_fraction": v11_all_off["mixed_sign_run_fraction"],
        "observed_mixed_sign_run_fraction": full["mixed_sign_run_fraction"],
    }
    nesting["exact_count_nesting_passes"] = (
        nesting["expected_positive"] == nesting["observed_positive"]
        and nesting["expected_negative"] == nesting["observed_negative"]
        and nesting["expected_equal"] == nesting["observed_equal"]
        and abs(nesting["expected_mixed_sign_run_fraction"] - nesting["observed_mixed_sign_run_fraction"]) <= EPS
    )

    collapse = none["mixed_sign_runs"] == 0 and none["mean_within_run_branching_balance"] <= EPS
    return {
        "analysis": "constraint_mechanism_abm_v12_residual_trait_causes",
        "status": "prospective_residual_source_ablation_after_v11",
        "scientific_question": (
            "After the four v11 downstream modifiers are fixed off, which retained lineage attributes generate within-environment two-sided reproductive branching?"
        ),
        "factors": {
            "initial_trait_heterogeneity": {
                "on": "frozen v4 lineage initial trait distribution",
                "off": f"all initial traits fixed at {COMMON_TRAIT}",
            },
            "trait_adjustment_heterogeneity": {
                "on": "frozen v4 lineage trait-adjustment distribution U(0.01,0.055)",
                "off": f"all adjustment rates fixed at midpoint {COMMON_TRAIT_ADJUSTMENT}",
            },
            "assurance_ceiling_heterogeneity": {
                "on": "frozen v4 lineage assurance-ceiling distribution U(0.10,0.90)",
                "off": f"all assurance ceilings fixed at midpoint {COMMON_ASSURANCE_CEILING}",
            },
        },
        "fixed_off_from_v11": {
            "local_support_variation": True,
            "dependency_heterogeneity": True,
            "assurance_responsiveness": True,
            "partner_effectiveness": True,
            "dependency_value": COMMON_DEPENDENCY,
            "assurance_responsiveness_value": FIXED_ASSURANCE_RESPONSIVENESS,
        },
        "analytical_reduction": (
            "v5 within-support weight variation is omitted because it conserves each plant row sum exactly; with partner quality fixed to one, the v10 service transform depends only on that row sum. It therefore cannot change reproduction in this residual gate."
        ),
        "design": {
            "factorial_configurations": len(configs),
            "saturation_envelope": list(SATURATIONS),
            "replicates_per_saturation": replicates,
            "lineages_per_run": n_lineages,
            "evolution_steps": steps,
            "runs_per_config": len(SATURATIONS) * replicates,
            "lineage_contrasts_per_config": len(SATURATIONS) * replicates * n_lineages,
            "empirical_inputs_loaded": [],
            "izu_target_frequencies_loaded": False,
            "external_target_values_loaded": False,
        },
        "v11_all_off_nesting": nesting,
        "full_residual_config": full_id,
        "full_residual_summary": full,
        "drop_one_ablation": drop_one,
        "all_residual_factors_off": {**none, "within_run_branching_collapsed": collapse},
        "all_configurations": summaries,
        "decision": (
            "v12_residual_lineage_factors_exhaust_within_run_branching_in_declared_model"
            if collapse and nesting["exact_count_nesting_passes"]
            else "v12_residual_branching_not_exhausted_or_nesting_failed"
        ),
        "claim_boundary": (
            "v12 identifies synthetic sources of lineage branching inside the declared model only. Initial trait and adjustment parameters are abstract standardized axes, not direct estimates of a particular floral trait. "
            "No Izu sign frequency is used as a target. Empirical causation still requires joint trait, effective-service and reproductive measurements across independent systems."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=4)
    parser.add_argument("--lineages", type=int, default=24)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--seed", type=int, default=20260822)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build(replicates=args.replicates, n_lineages=args.lineages, steps=args.steps, seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({
        "nesting": payload["v11_all_off_nesting"],
        "full": payload["full_residual_summary"],
        "drop_one": payload["drop_one_ablation"],
        "all_off": payload["all_residual_factors_off"],
        "decision": payload["decision"],
    }, indent=2))


if __name__ == "__main__":
    main()
