from __future__ import annotations

import argparse
import dataclasses
import importlib.util
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
V4_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v4_fixed_visit_budget.py"
V9_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v9_local_plant_opportunity.py"
V10_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v10_effective_service_dependency.py"
PARENT_RESULT = ROOT / "data/results/network_context_buffering_capability_robustness_frozen.json"
DEFAULT_OUT = ROOT / "data/results/network_context_rescue_discriminator.json"
SATURATIONS = (1.0, 2.0, 3.0)
REPLICATES = 4
CONTEXTS = 4
LINEAGES = 24
STEPS = 120
SUPPORT_OFF = 0.0
SUPPORT_ON = 0.5
SEED_BLOCK = 90260824
EPS = 1e-12
DESCRIPTORS = (
    "initial_lineage_trait",
    "pollinator_dependency",
    "global_opportunity_delta",
    "support_off_effective_service_delta",
    "support_on_island_minus_mainland_active_context_fraction",
    "support_on_island_minus_mainland_mean_positive_partner_count",
    "support_on_island_minus_mainland_mean_row_shannon",
    "support_on_island_minus_mainland_mean_dominant_partner_share",
)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def disable_assurance(templates: list) -> list:
    return [
        dataclasses.replace(template, assurance_ceiling=0.0, assurance_responsiveness=0.0)
        for template in templates
    ]


def row_sums(network) -> dict[str, float]:
    return {name: float(sum(row)) for name, row in zip(network.plant_names, network.matrix)}


def row_structure(row: tuple[float, ...] | None) -> tuple[float, float, float, float]:
    if row is None:
        return 0.0, 0.0, 0.0, 0.0
    positive = [float(value) for value in row if value > EPS]
    if not positive:
        return 0.0, 0.0, 0.0, 0.0
    total = sum(positive)
    proportions = [value / total for value in positive]
    shannon = -sum(p * math.log(p) for p in proportions if p > 0.0)
    dominant = max(proportions)
    return 1.0, float(len(positive)), shannon, dominant


def local_structure_by_lineage(
    *,
    opportunity,
    v9,
    v10,
    context_seed: int,
    contexts: int,
    n_lineages: int,
) -> dict[str, dict[str, float]]:
    accum: dict[str, dict[str, list[float]]] = {
        f"lineage_{index + 1}": {
            "active": [],
            "partner_count": [],
            "shannon": [],
            "dominant_share": [],
        }
        for index in range(n_lineages)
    }
    for context in range(contexts):
        support_seed = context_seed + context * 1009
        weight_seed = context_seed + context * 1013 + 17_000_000
        realized, _audit = v9.realize_local_context(
            opportunity,
            support_seed=support_seed,
            support_strength=SUPPORT_ON,
            weight_seed=weight_seed,
            weight_strength=v10.WEIGHT_STRENGTH,
        )
        row_map = {} if realized is None else {
            name: tuple(float(value) for value in row)
            for name, row in zip(realized.plant_names, realized.matrix)
        }
        for name, values in accum.items():
            active, count, shannon, dominant = row_structure(row_map.get(name))
            values["active"].append(active)
            values["partner_count"].append(count)
            values["shannon"].append(shannon)
            values["dominant_share"].append(dominant)
    return {
        name: {
            "active_context_fraction": mean(values["active"]),
            "mean_positive_partner_count": mean(values["partner_count"]),
            "mean_row_shannon": mean(values["shannon"]),
            "mean_dominant_partner_share": mean(values["dominant_share"]),
        }
        for name, values in accum.items()
    }


def classify(reproduction_off: float, reproduction_on: float) -> str:
    if reproduction_on >= -EPS:
        return "sign_rescue"
    if reproduction_on > reproduction_off + EPS:
        return "attenuation_only"
    if reproduction_on < reproduction_off - EPS:
        return "worsening"
    return "other_no_material_change"


def descriptor_means(rows: list[dict[str, object]]) -> dict[str, float | None]:
    if not rows:
        return {name: None for name in DESCRIPTORS}
    return {
        name: mean(float(row[name]) for row in rows)
        for name in DESCRIPTORS
    }


def mean_contrast(left: dict[str, float | None], right: dict[str, float | None]) -> dict[str, float | None]:
    result: dict[str, float | None] = {}
    for name in DESCRIPTORS:
        if left[name] is None or right[name] is None:
            result[name] = None
        else:
            result[name] = float(left[name]) - float(right[name])
    return result


def build(
    *,
    replicates: int = REPLICATES,
    contexts: int = CONTEXTS,
    n_lineages: int = LINEAGES,
    steps: int = STEPS,
    seed_block: int = SEED_BLOCK,
) -> dict[str, object]:
    v4 = load_module(V4_SCRIPT, "network_rescue_discriminator_v4")
    v9 = load_module(V9_SCRIPT, "network_rescue_discriminator_v9")
    v10 = load_module(V10_SCRIPT, "network_rescue_discriminator_v10")

    rows: list[dict[str, object]] = []
    total_lineage_contrasts = 0
    for saturation in SATURATIONS:
        for replicate in range(replicates):
            run_seed = seed_block + replicate + int(saturation * 10_000)
            templates = disable_assurance(v4.make_lineages(random.Random(run_seed), n_lineages))
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
            mainland_global = row_sums(mainland_opportunity)
            island_global = row_sums(island_opportunity)
            context_seed = run_seed + 51_000_000

            outputs = {}
            for mode, support_strength in (("off", SUPPORT_OFF), ("on", SUPPORT_ON)):
                common = dict(
                    templates=templates,
                    v9=v9,
                    saturation=saturation,
                    support_strength=support_strength,
                    contexts=contexts,
                    context_seed=context_seed,
                    quality_strength=v10.QUALITY_STRENGTH,
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
                outputs[mode] = mainland, island

            mainland_structure = local_structure_by_lineage(
                opportunity=mainland_opportunity,
                v9=v9,
                v10=v10,
                context_seed=context_seed,
                contexts=contexts,
                n_lineages=n_lineages,
            )
            island_structure = local_structure_by_lineage(
                opportunity=island_opportunity,
                v9=v9,
                v10=v10,
                context_seed=context_seed,
                contexts=contexts,
                n_lineages=n_lineages,
            )

            for index, template in enumerate(templates):
                total_lineage_contrasts += 1
                name = f"lineage_{index + 1}"
                global_delta = island_global[name] - mainland_global[name]
                mainland_off, island_off = outputs["off"]
                mainland_on, island_on = outputs["on"]
                service_off = (
                    island_off[name]["mean_effective_service"]
                    - mainland_off[name]["mean_effective_service"]
                )
                reproduction_off = (
                    island_off[name]["mean_reproduction"]
                    - mainland_off[name]["mean_reproduction"]
                )
                reproduction_on = (
                    island_on[name]["mean_reproduction"]
                    - mainland_on[name]["mean_reproduction"]
                )
                if not (global_delta < -EPS and reproduction_off < -EPS):
                    continue

                m = mainland_structure[name]
                i = island_structure[name]
                rows.append({
                    "saturation": saturation,
                    "replicate": replicate,
                    "lineage_index": index,
                    "class": classify(reproduction_off, reproduction_on),
                    "initial_lineage_trait": float(template.trait),
                    "pollinator_dependency": float(template.pollinator_dependency),
                    "global_opportunity_delta": global_delta,
                    "support_off_effective_service_delta": service_off,
                    "support_off_reproduction_delta": reproduction_off,
                    "support_on_reproduction_delta": reproduction_on,
                    "support_on_island_minus_mainland_active_context_fraction": (
                        i["active_context_fraction"] - m["active_context_fraction"]
                    ),
                    "support_on_island_minus_mainland_mean_positive_partner_count": (
                        i["mean_positive_partner_count"] - m["mean_positive_partner_count"]
                    ),
                    "support_on_island_minus_mainland_mean_row_shannon": (
                        i["mean_row_shannon"] - m["mean_row_shannon"]
                    ),
                    "support_on_island_minus_mainland_mean_dominant_partner_share": (
                        i["mean_dominant_partner_share"] - m["mean_dominant_partner_share"]
                    ),
                })

    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["class"])].append(row)
    class_order = ("sign_rescue", "attenuation_only", "worsening", "other_no_material_change")
    class_counts = {name: len(grouped.get(name, [])) for name in class_order}
    class_means = {name: descriptor_means(grouped.get(name, [])) for name in class_order}

    parent = json.loads(PARENT_RESULT.read_text(encoding="utf-8"))
    parent_summary = parent["overall"] if "overall" in parent else parent["summary"]
    expected_subset = int(parent_summary["global_decline_and_support_off_reproduction_decline"])
    expected_sign_rescues = int(parent_summary["reproduction_sign_rescue_count"])
    expected_worsening = int(parent_summary["reproduction_worsening_count"])
    expected_magnitude_rescues = int(parent_summary["reproduction_magnitude_rescue_count"])
    exact_nesting = (
        len(rows) == expected_subset
        and class_counts["sign_rescue"] == expected_sign_rescues
        and class_counts["worsening"] == expected_worsening
        and class_counts["sign_rescue"] + class_counts["attenuation_only"] == expected_magnitude_rescues
    )

    return {
        "analysis": "network_context_rescue_vs_worsening_discriminator",
        "status": "synthetic_descriptor_diagnostic_nested_in_frozen_network_context_robustness_block",
        "design": {
            "saturations": list(SATURATIONS),
            "replicates": replicates,
            "contexts": contexts,
            "lineages": n_lineages,
            "steps": steps,
            "support_off": SUPPORT_OFF,
            "support_on": SUPPORT_ON,
            "seed_block": seed_block,
            "total_lineage_contrasts": total_lineage_contrasts,
            "analysis_subset_contrasts": len(rows),
            "new_parameter_count": 0,
            "empirical_targets_loaded": [],
        },
        "predeclared_descriptors": list(DESCRIPTORS),
        "class_counts": class_counts,
        "class_descriptor_means": class_means,
        "predeclared_mean_contrasts": {
            "sign_rescue_minus_worsening": mean_contrast(
                class_means["sign_rescue"], class_means["worsening"]
            ),
            "sign_rescue_minus_attenuation_only": mean_contrast(
                class_means["sign_rescue"], class_means["attenuation_only"]
            ),
        },
        "parent_nesting": {
            "expected_analysis_subset": expected_subset,
            "observed_analysis_subset": len(rows),
            "expected_sign_rescues": expected_sign_rescues,
            "observed_sign_rescues": class_counts["sign_rescue"],
            "expected_worsening": expected_worsening,
            "observed_worsening": class_counts["worsening"],
            "expected_magnitude_rescues": expected_magnitude_rescues,
            "observed_magnitude_rescues": class_counts["sign_rescue"] + class_counts["attenuation_only"],
            "exact_nesting_passes": exact_nesting,
        },
        "decision": (
            "predeclared_network_descriptors_ready_for_empirical_priority_interpretation"
            if exact_nesting
            else "discriminator_failed_parent_nesting_do_not_interpret_descriptors"
        ),
        "claim_boundary": (
            "Class-specific descriptor differences are synthetic associations inside the frozen ABM, not causal effects and not empirical moderator estimates. The analysis may prioritize which network descriptors to measure, but no descriptor can be mapped to a real island system without source-native matched measurements and the existing admission gate."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    result = build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "class_counts": result["class_counts"],
        "parent_nesting": result["parent_nesting"],
        "mean_contrasts": result["predeclared_mean_contrasts"],
        "decision": result["decision"],
    }, indent=2))


if __name__ == "__main__":
    main()
