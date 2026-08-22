from __future__ import annotations

import argparse
import importlib.util
import json
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

from channel_id.external_archipelago_network import WeightedNetwork

ROOT = Path(__file__).resolve().parents[1]
V4_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v4_fixed_visit_budget.py"
V9_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v9_local_plant_opportunity.py"
OUT = ROOT / "data/results/constraint_mechanism_abm_v10_effective_service_dependency.json"
SATURATIONS = (1.0, 2.0, 3.0)
SUPPORT_STRENGTHS = (0.25, 0.5, 0.75)
WEIGHT_STRENGTH = 0.5
QUALITY_STRENGTH = 1.0
QUALITY_HALF_RANGE = 0.8  # recovers the v3 [0.2, 1.8] broad probe at strength=1
EPS = 1e-12


@dataclass
class ResponseState:
    assurance: float = 0.08
    reproduction_sum: float = 0.0
    service_sum: float = 0.0
    opportunity_sum: float = 0.0
    contexts: int = 0


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def clamp(value: float) -> float:
    return min(1.0, max(0.0, value))


def quality_multipliers(
    pollinator_names: tuple[str, ...], *, seed: int, quality_strength: float
) -> tuple[float, ...]:
    if not 0.0 <= quality_strength <= 1.0:
        raise ValueError("quality_strength must be in [0,1]")
    if quality_strength == 0.0:
        return tuple(1.0 for _ in pollinator_names)
    rng = random.Random(seed)
    return tuple(
        1.0 + quality_strength * rng.uniform(-QUALITY_HALF_RANGE, QUALITY_HALF_RANGE)
        for _ in pollinator_names
    )


def plant_rows(network: WeightedNetwork | None) -> dict[str, tuple[float, ...]]:
    if network is None:
        return {}
    return {name: row for name, row in zip(network.plant_names, network.matrix)}


def row_service(
    row: tuple[float, ...] | None,
    multipliers: tuple[float, ...],
    *, saturation: float,
) -> tuple[float, float]:
    if row is None:
        return 0.0, 0.0
    if len(row) != len(multipliers):
        raise ValueError("row and multiplier lengths differ")
    opportunity = sum(row)
    effective_score = sum(weight * quality for weight, quality in zip(row, multipliers))
    service = clamp(1.0 - math.exp(-saturation * effective_score))
    return opportunity, service


def reproductive_output(template, state: ResponseState, service: float) -> float:
    dependency = float(template.pollinator_dependency)
    autonomous = float(template.assurance_ceiling) * state.assurance
    pollinator_route = dependency * service
    assurance_route = (1.0 - dependency) * autonomous
    reproduction = clamp(1.0 - (1.0 - pollinator_route) * (1.0 - assurance_route))
    if reproduction < 0.50:
        state.assurance = min(
            float(template.assurance_ceiling),
            state.assurance + float(template.assurance_responsiveness),
        )
    return reproduction


def simulate_endpoint(
    opportunity: WeightedNetwork,
    templates: list,
    *,
    v9,
    saturation: float,
    support_strength: float,
    contexts: int,
    context_seed: int,
    quality_strength: float,
    quality_stream_offset: int,
) -> dict[str, dict[str, float]]:
    states = [ResponseState() for _ in templates]
    for context in range(contexts):
        support_seed = context_seed + context * 1009
        weight_seed = context_seed + context * 1013 + 17_000_000
        realized, _audit = v9.realize_local_context(
            opportunity,
            support_seed=support_seed,
            support_strength=support_strength,
            weight_seed=weight_seed,
            weight_strength=WEIGHT_STRENGTH,
        )
        rows = plant_rows(realized)
        names = tuple() if realized is None else realized.pollinator_names
        quality = quality_multipliers(
            names,
            seed=context_seed + quality_stream_offset + context * 1021,
            quality_strength=quality_strength,
        )
        for index, template in enumerate(templates):
            name = f"lineage_{index + 1}"
            row = rows.get(name)
            opportunity_score, service = row_service(row, quality, saturation=saturation)
            reproduction = reproductive_output(template, states[index], service)
            states[index].opportunity_sum += opportunity_score
            states[index].service_sum += service
            states[index].reproduction_sum += reproduction
            states[index].contexts += 1

    result: dict[str, dict[str, float]] = {}
    for index, state in enumerate(states):
        denom = max(1, state.contexts)
        result[f"lineage_{index + 1}"] = {
            "mean_opportunity": state.opportunity_sum / denom,
            "mean_effective_service": state.service_sum / denom,
            "mean_reproduction": state.reproduction_sum / denom,
            "final_assurance": state.assurance,
            "dependency": float(templates[index].pollinator_dependency),
        }
    return result


def direction_counts(values: list[float]) -> dict[str, int]:
    return {
        "lower": sum(value < -EPS for value in values),
        "higher": sum(value > EPS for value in values),
        "equal": sum(abs(value) <= EPS for value in values),
    }


def paired_configuration(
    *,
    seed: int,
    saturation: float,
    support_strength: float,
    contexts: int,
    n_lineages: int,
    steps: int,
) -> dict:
    v4 = load_module(V4_SCRIPT, f"abm_v10_v4_{seed}_{saturation}")
    v9 = load_module(V9_SCRIPT, f"abm_v10_v9_{seed}_{saturation}_{support_strength}")
    templates = v4.make_lineages(random.Random(seed), n_lineages)

    mainland_opportunity, _, _ = v9.run_weighted_network(
        0.0,
        seed,
        saturation,
        support_seed=seed + 31_000_000,
        support_strength=0.0,
        weight_seed=seed + 41_000_000,
        weight_strength=0.0,
        n_lineages=n_lineages,
        steps=steps,
    )
    island_opportunity, _, _ = v9.run_weighted_network(
        1.0,
        seed,
        saturation,
        support_seed=seed + 31_000_000,
        support_strength=0.0,
        weight_seed=seed + 41_000_000,
        weight_strength=0.0,
        n_lineages=n_lineages,
        steps=steps,
    )

    common = dict(
        templates=templates,
        v9=v9,
        saturation=saturation,
        support_strength=support_strength,
        contexts=contexts,
        context_seed=seed + 51_000_000,
    )
    mainland_off = simulate_endpoint(
        mainland_opportunity,
        quality_strength=0.0,
        quality_stream_offset=1_000_000,
        **common,
    )
    island_off = simulate_endpoint(
        island_opportunity,
        quality_strength=0.0,
        quality_stream_offset=2_000_000,
        **common,
    )
    mainland_on = simulate_endpoint(
        mainland_opportunity,
        quality_strength=QUALITY_STRENGTH,
        quality_stream_offset=1_000_000,
        **common,
    )
    island_on = simulate_endpoint(
        island_opportunity,
        quality_strength=QUALITY_STRENGTH,
        quality_stream_offset=2_000_000,
        **common,
    )

    names = [f"lineage_{index + 1}" for index in range(n_lineages)]
    opportunity_delta = [
        island_off[name]["mean_opportunity"] - mainland_off[name]["mean_opportunity"]
        for name in names
    ]
    reproduction_delta_off = [
        island_off[name]["mean_reproduction"] - mainland_off[name]["mean_reproduction"]
        for name in names
    ]
    reproduction_delta_on = [
        island_on[name]["mean_reproduction"] - mainland_on[name]["mean_reproduction"]
        for name in names
    ]
    sign_flips = sum(
        (left < -EPS and right > EPS) or (left > EPS and right < -EPS)
        for left, right in zip(reproduction_delta_off, reproduction_delta_on)
    )
    quality_changed = sum(abs(left - right) > 1e-9 for left, right in zip(reproduction_delta_off, reproduction_delta_on))

    return {
        "seed": seed,
        "saturation": saturation,
        "support_strength": support_strength,
        "opportunity_direction": direction_counts(opportunity_delta),
        "reproduction_direction_quality_off": direction_counts(reproduction_delta_off),
        "reproduction_direction_quality_on": direction_counts(reproduction_delta_on),
        "quality_induced_response_sign_flips": sign_flips,
        "quality_changed_reproductive_contrast": quality_changed,
        "mean_opportunity_delta": mean(opportunity_delta),
        "mean_reproduction_delta_quality_off": mean(reproduction_delta_off),
        "mean_reproduction_delta_quality_on": mean(reproduction_delta_on),
        "upstream_identical_between_quality_ablations": all(
            abs(mainland_off[name]["mean_opportunity"] - mainland_on[name]["mean_opportunity"]) <= EPS
            and abs(island_off[name]["mean_opportunity"] - island_on[name]["mean_opportunity"]) <= EPS
            for name in names
        ),
    }


def summarize(rows: list[dict], n_lineages: int) -> dict:
    total_contrasts = len(rows) * n_lineages
    upstream_lower = sum(row["opportunity_direction"]["lower"] for row in rows)
    off_positive = sum(row["reproduction_direction_quality_off"]["higher"] for row in rows)
    off_negative = sum(row["reproduction_direction_quality_off"]["lower"] for row in rows)
    on_positive = sum(row["reproduction_direction_quality_on"]["higher"] for row in rows)
    on_negative = sum(row["reproduction_direction_quality_on"]["lower"] for row in rows)
    mixed_off = sum(
        row["reproduction_direction_quality_off"]["higher"] > 0
        and row["reproduction_direction_quality_off"]["lower"] > 0
        for row in rows
    )
    mixed_on = sum(
        row["reproduction_direction_quality_on"]["higher"] > 0
        and row["reproduction_direction_quality_on"]["lower"] > 0
        for row in rows
    )
    sign_flips = sum(row["quality_induced_response_sign_flips"] for row in rows)
    quality_changed = sum(row["quality_changed_reproductive_contrast"] for row in rows)
    invariants = all(row["upstream_identical_between_quality_ablations"] for row in rows)

    if not invariants:
        decision = "v10_invalid_quality_layer_changes_upstream_opportunity"
    elif sign_flips == 0:
        decision = "v10_quality_layer_changes_magnitude_but_not_response_branch_identity"
    elif on_positive > off_positive or mixed_on > mixed_off:
        decision = "v10_partner_effectiveness_interacts_with_v9_to_broaden_downstream_branching"
    else:
        decision = "v10_partner_effectiveness_changes_branch_identity_without_broadening_positive_tail"

    return {
        "configuration_count": len(rows),
        "lineage_contrast_count": total_contrasts,
        "upstream_oceanic_lower_fraction": upstream_lower / total_contrasts,
        "quality_off_positive_responses": off_positive,
        "quality_off_negative_responses": off_negative,
        "quality_on_positive_responses": on_positive,
        "quality_on_negative_responses": on_negative,
        "mixed_sign_configurations_quality_off": mixed_off,
        "mixed_sign_configurations_quality_on": mixed_on,
        "quality_induced_response_sign_flips": sign_flips,
        "quality_changed_reproductive_contrasts": quality_changed,
        "upstream_identical_between_quality_ablations": invariants,
        "decision": decision,
    }


def build(
    *,
    replicates: int = 6,
    contexts: int = 6,
    n_lineages: int = 24,
    steps: int = 120,
    seed: int = 20260822,
) -> dict:
    rows = []
    for saturation in SATURATIONS:
        for support_strength in SUPPORT_STRENGTHS:
            for replicate in range(replicates):
                rows.append(
                    paired_configuration(
                        seed=seed + replicate,
                        saturation=saturation,
                        support_strength=support_strength,
                        contexts=contexts,
                        n_lineages=n_lineages,
                        steps=steps,
                    )
                )
    summary = summarize(rows, n_lineages)
    return {
        "analysis": "constraint_mechanism_abm_v10_effective_service_dependency",
        "status": "synthetic_joint_mechanism_retest_after_v4_to_v9_structural_corrections",
        "scientific_question": (
            "After fixed visit budget and explicit local plant/pollinator/pair support are in place, "
            "does geography-independent partner effectiveness interact with lineage dependency/assurance "
            "to alter downstream reproductive branch identity without changing upstream opportunity?"
        ),
        "history": {
            "v3_decision": "partner_service_quality_heterogeneity_alone_is_insufficient",
            "why_retest_is_admissible": (
                "v3 preceded the fixed-visit-budget correction and local support hierarchy. v10 does not tune v3; "
                "it reuses the broad v3 quality probe as an ablation on the later v9 structure."
            ),
        },
        "mechanism": {
            "upstream_network": "unchanged v9 local plant opportunity -> pollinator support -> pair support -> v5 weight realization",
            "partner_effectiveness": "multiplicative quality on existing positive pair weights only; distribution is geography-independent and never creates links",
            "quality_probe": "1 + U(-0.8,0.8), recovering the frozen v3 0.2-1.8 broad probe at strength 1",
            "visit_budget": "v4 fixed-budget identity retained; row weights enter one saturating service transform rather than accumulating visit frequency with richness",
            "plant_filter": "v4 lineage pollinator_dependency, assurance_ceiling and assurance_responsiveness",
            "assurance_update": "same v4 rule: increase assurance only when reproduction < 0.5, capped by lineage ceiling",
        },
        "design": {
            "saturation_envelope": list(SATURATIONS),
            "support_strengths": list(SUPPORT_STRENGTHS),
            "weight_strength": WEIGHT_STRENGTH,
            "quality_strength": QUALITY_STRENGTH,
            "replicates_per_setting": replicates,
            "local_contexts_per_endpoint": contexts,
            "lineages_per_run": n_lineages,
            "evolution_steps": steps,
            "seed": seed,
            "empirical_inputs_loaded": [],
            "izu_target_frequencies_loaded": False,
            "external_target_values_loaded": False,
        },
        "predeclared_interpretation": {
            "upstream_common_constraint": "descriptive only: report the fraction of lineages with lower oceanic opportunity; do not fit it to Izu 8/8",
            "downstream_branching": "report positive and negative reproductive contrasts under quality-off and quality-on",
            "quality_discrimination": "a sign flip under matched upstream networks shows partner effectiveness changes branch identity; positive-tail expansion is stronger evidence but is not required for implementation validity",
            "scientific_falsification_is_not_ci_failure": True,
        },
        "summary": summary,
        "rows": rows,
        "claim_boundary": (
            "v10 is synthetic mechanism evidence, not empirical causal identification. It cannot use the known Izu 4/4 pollen split as a target, "
            "does not identify historical Bombus loss, and does not make visitor-network weights equivalent to SVD or reproductive dependency. "
            "A later independent island validation must freeze compatible effective-service and reproductive outcomes before inspection."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=6)
    parser.add_argument("--contexts", type=int, default=6)
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
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
