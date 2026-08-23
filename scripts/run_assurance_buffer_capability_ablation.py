from __future__ import annotations

import argparse
import dataclasses
import importlib.util
import json
import random
import sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
V4_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v4_fixed_visit_budget.py"
V9_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v9_local_plant_opportunity.py"
V10_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v10_effective_service_dependency.py"
DEFAULT_OUT = ROOT / "data/results/assurance_buffer_capability_ablation.json"
SATURATIONS = (1.0, 2.0, 3.0)
SUPPORT_STRENGTHS = (0.25, 0.5, 0.75)
EPS = 1e-12


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def assurance_off_templates(templates: list) -> list:
    return [
        dataclasses.replace(
            template,
            assurance_ceiling=0.0,
            assurance_responsiveness=0.0,
        )
        for template in templates
    ]


def sign(value: float) -> int:
    if value > EPS:
        return 1
    if value < -EPS:
        return -1
    return 0


def build(
    *,
    replicates: int = 4,
    contexts: int = 4,
    n_lineages: int = 24,
    steps: int = 120,
    seed: int = 20260823,
) -> dict:
    v4 = load_module(V4_SCRIPT, "assurance_buffer_v4")
    v9 = load_module(V9_SCRIPT, "assurance_buffer_v9")
    v10 = load_module(V10_SCRIPT, "assurance_buffer_v10")

    rows: list[dict[str, float | int | bool]] = []
    upstream_identical = True

    for saturation in SATURATIONS:
        for support_strength in SUPPORT_STRENGTHS:
            for replicate in range(replicates):
                run_seed = seed + replicate + int(saturation * 10_000) + int(support_strength * 100_000)
                templates_on = v4.make_lineages(random.Random(run_seed), n_lineages)
                templates_off = assurance_off_templates(templates_on)

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

                common = dict(
                    v9=v9,
                    saturation=saturation,
                    support_strength=support_strength,
                    contexts=contexts,
                    context_seed=run_seed + 51_000_000,
                    quality_strength=v10.QUALITY_STRENGTH,
                )

                mainland_off = v10.simulate_endpoint(
                    mainland_opportunity,
                    templates_off,
                    quality_stream_offset=1_000_000,
                    **common,
                )
                island_off = v10.simulate_endpoint(
                    island_opportunity,
                    templates_off,
                    quality_stream_offset=2_000_000,
                    **common,
                )
                mainland_on = v10.simulate_endpoint(
                    mainland_opportunity,
                    templates_on,
                    quality_stream_offset=1_000_000,
                    **common,
                )
                island_on = v10.simulate_endpoint(
                    island_opportunity,
                    templates_on,
                    quality_stream_offset=2_000_000,
                    **common,
                )

                for lineage_index in range(n_lineages):
                    name = f"lineage_{lineage_index + 1}"
                    service_delta_off = (
                        island_off[name]["mean_effective_service"]
                        - mainland_off[name]["mean_effective_service"]
                    )
                    service_delta_on = (
                        island_on[name]["mean_effective_service"]
                        - mainland_on[name]["mean_effective_service"]
                    )
                    if abs(service_delta_off - service_delta_on) > EPS:
                        upstream_identical = False

                    reproduction_delta_off = (
                        island_off[name]["mean_reproduction"]
                        - mainland_off[name]["mean_reproduction"]
                    )
                    reproduction_delta_on = (
                        island_on[name]["mean_reproduction"]
                        - mainland_on[name]["mean_reproduction"]
                    )

                    service_loss = service_delta_off < -EPS
                    off_reproductive_loss = reproduction_delta_off < -EPS
                    assurance_improves_delta = reproduction_delta_on > reproduction_delta_off + EPS
                    partial_buffer = (
                        service_loss
                        and off_reproductive_loss
                        and assurance_improves_delta
                        and reproduction_delta_on < -EPS
                    )
                    full_sign_buffer = (
                        service_loss
                        and off_reproductive_loss
                        and reproduction_delta_on >= -EPS
                    )

                    rows.append(
                        {
                            "saturation": saturation,
                            "support_strength": support_strength,
                            "replicate": replicate,
                            "lineage_index": lineage_index,
                            "service_delta": service_delta_off,
                            "reproduction_delta_assurance_off": reproduction_delta_off,
                            "reproduction_delta_assurance_on": reproduction_delta_on,
                            "assurance_effect_on_reproductive_delta": reproduction_delta_on - reproduction_delta_off,
                            "service_loss": service_loss,
                            "off_reproductive_loss": off_reproductive_loss,
                            "assurance_improves_delta": assurance_improves_delta,
                            "partial_buffer": partial_buffer,
                            "full_sign_buffer": full_sign_buffer,
                            "sign_flip_off_to_on": sign(reproduction_delta_off) != sign(reproduction_delta_on),
                        }
                    )

    service_loss_rows = [row for row in rows if row["service_loss"]]
    off_loss_rows = [row for row in service_loss_rows if row["off_reproductive_loss"]]
    partial = [row for row in off_loss_rows if row["partial_buffer"]]
    full = [row for row in off_loss_rows if row["full_sign_buffer"]]
    improved = [row for row in service_loss_rows if row["assurance_improves_delta"]]
    sign_flips = [row for row in rows if row["sign_flip_off_to_on"]]

    if full:
        decision = "existing_assurance_route_has_synthetic_partial_and_full_sign_buffering_capability"
    elif partial:
        decision = "existing_assurance_route_has_synthetic_partial_buffering_capability_without_full_sign_rescue"
    else:
        decision = "existing_assurance_route_does_not_generate_threshold_free_buffering_in_declared_envelope"

    return {
        "analysis": "assurance_buffer_capability_ablation",
        "status": "synthetic_model_capability_test_not_empirical_mechanism_admission",
        "scientific_question": (
            "With the existing frozen network, partner-effectiveness, dependency and trait-position structure held fixed, can the already-implemented reproductive-assurance route attenuate or fully rescue reproductive decline when effective service declines?"
        ),
        "design": {
            "saturations": list(SATURATIONS),
            "support_strengths": list(SUPPORT_STRENGTHS),
            "replicates_per_cell": replicates,
            "contexts_per_endpoint": contexts,
            "lineages_per_run": n_lineages,
            "evolution_steps": steps,
            "paired_lineage_contrasts": len(rows),
            "empirical_targets_loaded": [],
            "hawaii_outcomes_loaded": False,
            "campanula_outcomes_loaded": False,
            "new_buffer_parameter_added": False,
        },
        "ablation": {
            "assurance_on": "retain frozen v4 assurance_ceiling and assurance_responsiveness with v10 baseline assurance state",
            "assurance_off": "set assurance_ceiling=0 and assurance_responsiveness=0 for the same lineage templates",
            "all_other_components": "identical paired opportunity networks, local-support realization, partner quality streams, dependency, trait position and trait adjustment",
            "upstream_effective_service_identical_between_assurance_arms": upstream_identical,
        },
        "threshold_free_state_definitions": {
            "service_loss": "effective_service_island - effective_service_mainland < 0",
            "partial_buffer": "service loss and reproductive loss without assurance; assurance makes the reproductive contrast less negative but it remains below 0",
            "full_sign_buffer": "service loss and reproductive loss without assurance; with assurance the reproductive contrast reaches or exceeds 0",
            "epsilon_only_for_floating_point_sign": EPS,
        },
        "summary": {
            "paired_lineage_contrasts": len(rows),
            "service_loss_cases": len(service_loss_rows),
            "service_loss_cases_with_off_reproductive_loss": len(off_loss_rows),
            "service_loss_cases_where_assurance_improves_reproductive_delta": len(improved),
            "partial_buffer_cases": len(partial),
            "full_sign_buffer_cases": len(full),
            "assurance_induced_reproductive_sign_changes_all_cases": len(sign_flips),
            "mean_assurance_effect_on_reproductive_delta_among_service_loss_cases": (
                mean(float(row["assurance_effect_on_reproductive_delta"]) for row in service_loss_rows)
                if service_loss_rows
                else None
            ),
            "mean_assurance_effect_on_reproductive_delta_among_off_loss_cases": (
                mean(float(row["assurance_effect_on_reproductive_delta"]) for row in off_loss_rows)
                if off_loss_rows
                else None
            ),
        },
        "decision": decision,
        "claim_boundary": (
            "A positive result establishes only that the existing synthetic assurance route has the mathematical capacity to attenuate or rescue reproductive decline under matched service loss. It does not identify assurance as the empirical buffer in Hawaiʻi, Nicotiana, Guaiacum, Izu or any other island system. Empirical mechanism admission remains governed by data/design/buffer_mechanism_abm_admission_interface.json."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=4)
    parser.add_argument("--contexts", type=int, default=4)
    parser.add_argument("--lineages", type=int, default=24)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--seed", type=int, default=20260823)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    result = build(
        replicates=args.replicates,
        contexts=args.contexts,
        n_lineages=args.lineages,
        steps=args.steps,
        seed=args.seed,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"decision": result["decision"], "summary": result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
