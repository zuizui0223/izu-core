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
OUT = ROOT / "data/results/abm_assurance_buffer_capability.json"
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
    """Remove the already-declared assurance route without changing dependency or upstream state."""
    return [
        dataclasses.replace(template, assurance_ceiling=0.0, assurance_responsiveness=0.0)
        for template in templates
    ]


def matched_configuration(
    *,
    seed: int,
    saturation: float,
    support_strength: float,
    contexts: int,
    n_lineages: int,
    steps: int,
) -> dict:
    v4 = load_module(V4_SCRIPT, f"assurance_v4_{seed}_{saturation}_{support_strength}")
    v9 = load_module(V9_SCRIPT, f"assurance_v9_{seed}_{saturation}_{support_strength}")
    v10 = load_module(V10_SCRIPT, f"assurance_v10_{seed}_{saturation}_{support_strength}")

    templates_on = v4.make_lineages(random.Random(seed), n_lineages)
    templates_off = assurance_off_templates(templates_on)

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
        v9=v9,
        saturation=saturation,
        support_strength=support_strength,
        contexts=contexts,
        context_seed=seed + 51_000_000,
        quality_strength=v10.QUALITY_STRENGTH,
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

    lineage_rows = []
    upstream_identical = True
    for index in range(n_lineages):
        name = f"lineage_{index + 1}"
        service_mainland_on = mainland_on[name]["mean_effective_service"]
        service_island_on = island_on[name]["mean_effective_service"]
        service_mainland_off = mainland_off[name]["mean_effective_service"]
        service_island_off = island_off[name]["mean_effective_service"]
        if (
            abs(service_mainland_on - service_mainland_off) > EPS
            or abs(service_island_on - service_island_off) > EPS
        ):
            upstream_identical = False

        service_delta = service_island_on - service_mainland_on
        reproduction_delta_on = (
            island_on[name]["mean_reproduction"] - mainland_on[name]["mean_reproduction"]
        )
        reproduction_delta_off = (
            island_off[name]["mean_reproduction"] - mainland_off[name]["mean_reproduction"]
        )
        eligible = service_delta < -EPS and reproduction_delta_off < -EPS
        attenuation = reproduction_delta_on - reproduction_delta_off if eligible else None
        partially_attenuated = bool(eligible and attenuation is not None and attenuation > EPS)
        fully_sign_buffered = bool(eligible and reproduction_delta_on >= -EPS)
        overcompensated = bool(eligible and reproduction_delta_on > EPS)
        worsened = bool(eligible and attenuation is not None and attenuation < -EPS)

        lineage_rows.append(
            {
                "lineage": name,
                "service_delta_island_minus_mainland": service_delta,
                "reproduction_delta_assurance_on": reproduction_delta_on,
                "reproduction_delta_assurance_off": reproduction_delta_off,
                "eligible_service_loss_with_off_decline": eligible,
                "assurance_attenuation": attenuation,
                "partially_attenuated": partially_attenuated,
                "fully_sign_buffered": fully_sign_buffered,
                "overcompensated": overcompensated,
                "worsened_by_assurance": worsened,
                "dependency": mainland_on[name]["dependency"],
                "final_assurance_mainland": mainland_on[name]["final_assurance"],
                "final_assurance_island": island_on[name]["final_assurance"],
            }
        )

    return {
        "seed": seed,
        "saturation": saturation,
        "support_strength": support_strength,
        "upstream_service_identical_between_assurance_ablations": upstream_identical,
        "lineages": lineage_rows,
    }


def summarize(rows: list[dict]) -> dict:
    lineages = [lineage for row in rows for lineage in row["lineages"]]
    eligible = [row for row in lineages if row["eligible_service_loss_with_off_decline"]]
    attenuated = [row for row in eligible if row["partially_attenuated"]]
    full = [row for row in eligible if row["fully_sign_buffered"]]
    over = [row for row in eligible if row["overcompensated"]]
    worsened = [row for row in eligible if row["worsened_by_assurance"]]
    invariants = all(row["upstream_service_identical_between_assurance_ablations"] for row in rows)

    if not invariants:
        decision = "invalid_assurance_ablation_changed_upstream_service"
    elif full:
        decision = "existing_assurance_route_can_generate_full_sign_buffering_without_new_parameter"
    elif attenuated:
        decision = "existing_assurance_route_can_attenuate_reproductive_propagation_without_full_sign_buffering"
    else:
        decision = "existing_assurance_route_does_not_generate_buffering_under_frozen_envelope"

    attenuation_values = [row["assurance_attenuation"] for row in eligible if row["assurance_attenuation"] is not None]
    return {
        "configuration_count": len(rows),
        "lineage_contrast_count": len(lineages),
        "eligible_service_loss_with_off_decline": len(eligible),
        "assurance_attenuated_count": len(attenuated),
        "assurance_attenuated_fraction_of_eligible": len(attenuated) / len(eligible) if eligible else None,
        "full_sign_buffer_count": len(full),
        "full_sign_buffer_fraction_of_eligible": len(full) / len(eligible) if eligible else None,
        "overcompensated_count": len(over),
        "worsened_by_assurance_count": len(worsened),
        "mean_assurance_attenuation_among_eligible": mean(attenuation_values) if attenuation_values else None,
        "upstream_service_identical_between_assurance_ablations": invariants,
        "decision": decision,
    }


def build(
    *,
    replicates: int = 6,
    contexts: int = 6,
    n_lineages: int = 24,
    steps: int = 120,
    seed: int = 20260823,
) -> dict:
    rows = []
    for saturation in SATURATIONS:
        for support_strength in SUPPORT_STRENGTHS:
            for replicate in range(replicates):
                rows.append(
                    matched_configuration(
                        seed=seed + replicate,
                        saturation=saturation,
                        support_strength=support_strength,
                        contexts=contexts,
                        n_lineages=n_lineages,
                        steps=steps,
                    )
                )
    summary = summarize(rows)
    return {
        "analysis": "abm_assurance_buffer_capability",
        "status": "synthetic_matched_existing_assurance_route_ablation",
        "scientific_question": (
            "Can the already-declared v10 assurance route attenuate or fully buffer a reproductive decline under matched service loss, without adding a new parameter or using any empirical target value?"
        ),
        "design": {
            "saturation_envelope": list(SATURATIONS),
            "support_strengths": list(SUPPORT_STRENGTHS),
            "replicates_per_setting": replicates,
            "local_contexts_per_endpoint": contexts,
            "lineages_per_run": n_lineages,
            "evolution_steps": steps,
            "seed": seed,
            "partner_effectiveness_strength": 1.0,
            "assurance_on": "frozen v4 lineage assurance_ceiling and assurance_responsiveness",
            "assurance_off": "same templates with assurance_ceiling=0 and assurance_responsiveness=0",
            "empirical_inputs_loaded": [],
            "empirical_target_values_loaded": False,
        },
        "threshold_free_interpretation": {
            "eligible": "island-minus-mainland service < 0 and assurance-OFF reproduction < 0",
            "partial_attenuation": "assurance-ON reproductive contrast > matched assurance-OFF contrast",
            "full_sign_buffer": "assurance-OFF reproductive contrast < 0 but assurance-ON contrast >= 0",
            "note": "EPS=1e-12 is numerical sign tolerance only, not a biological effect-size threshold",
        },
        "summary": summary,
        "rows": rows,
        "claim_boundary": (
            "This is a synthetic capability test of an already-existing ABM route. A positive capability result does not admit autonomous assurance as the empirical explanation for Hawaiʻi, Nicotiana, Guaiacum, Campanula, or any other system. Empirical admission remains governed by the frozen buffer-mechanism admission interface and requires matched source-native evidence plus a predeclared held-out or prospective test."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=6)
    parser.add_argument("--contexts", type=int, default=6)
    parser.add_argument("--lineages", type=int, default=24)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--seed", type=int, default=20260823)
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
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
