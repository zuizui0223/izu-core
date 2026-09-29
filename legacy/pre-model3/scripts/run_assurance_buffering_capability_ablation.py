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
OUT = ROOT / "data/results/assurance_buffering_capability_ablation.json"
SATURATIONS = (1.0, 2.0, 3.0)
SUPPORT_STRENGTHS = (0.25, 0.5, 0.75)
EPS = 1e-12
MODES = ("off", "baseline_only", "full_adaptive")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def transform_templates(base_templates: list, mode: str) -> list:
    if mode not in MODES:
        raise ValueError(f"unknown assurance mode: {mode}")
    transformed = []
    for template in base_templates:
        if mode == "off":
            transformed.append(
                dataclasses.replace(
                    template,
                    assurance_ceiling=0.0,
                    assurance_responsiveness=0.0,
                )
            )
        elif mode == "baseline_only":
            transformed.append(
                dataclasses.replace(template, assurance_responsiveness=0.0)
            )
        else:
            transformed.append(template)
    return transformed


def simulate_pair(
    *,
    v4,
    v9,
    v10,
    seed: int,
    saturation: float,
    support_strength: float,
    contexts: int,
    n_lineages: int,
    steps: int,
) -> list[dict[str, float | bool]]:
    base_templates = v4.make_lineages(random.Random(seed), n_lineages)
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

    outputs: dict[str, tuple[dict[str, dict[str, float]], dict[str, dict[str, float]]]] = {}
    for mode in MODES:
        templates = transform_templates(base_templates, mode)
        common = dict(
            templates=templates,
            v9=v9,
            saturation=saturation,
            support_strength=support_strength,
            contexts=contexts,
            context_seed=seed + 51_000_000,
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

    rows: list[dict[str, float | bool]] = []
    for index in range(n_lineages):
        name = f"lineage_{index + 1}"
        service_delta_by_mode = {}
        opportunity_delta_by_mode = {}
        reproduction_delta_by_mode = {}
        for mode in MODES:
            mainland, island = outputs[mode]
            service_delta_by_mode[mode] = (
                island[name]["mean_effective_service"]
                - mainland[name]["mean_effective_service"]
            )
            opportunity_delta_by_mode[mode] = (
                island[name]["mean_opportunity"] - mainland[name]["mean_opportunity"]
            )
            reproduction_delta_by_mode[mode] = (
                island[name]["mean_reproduction"] - mainland[name]["mean_reproduction"]
            )

        service_identical = max(service_delta_by_mode.values()) - min(service_delta_by_mode.values()) <= EPS
        opportunity_identical = max(opportunity_delta_by_mode.values()) - min(opportunity_delta_by_mode.values()) <= EPS
        off = reproduction_delta_by_mode["off"]
        baseline = reproduction_delta_by_mode["baseline_only"]
        full = reproduction_delta_by_mode["full_adaptive"]
        service = service_delta_by_mode["full_adaptive"]

        rows.append(
            {
                "service_delta": service,
                "opportunity_delta": opportunity_delta_by_mode["full_adaptive"],
                "reproduction_delta_assurance_off": off,
                "reproduction_delta_baseline_only": baseline,
                "reproduction_delta_full_adaptive": full,
                "service_identical_across_assurance_modes": service_identical,
                "opportunity_identical_across_assurance_modes": opportunity_identical,
                "service_declines": service < -EPS,
                "off_reproduction_declines": off < -EPS,
                "baseline_attenuates_decline": service < -EPS and off < -EPS and baseline > off + EPS,
                "full_attenuates_decline": service < -EPS and off < -EPS and full > off + EPS,
                "baseline_sign_rescue": service < -EPS and off < -EPS and baseline >= -EPS,
                "full_sign_rescue": service < -EPS and off < -EPS and full >= -EPS,
                "adaptive_additional_rescue": service < -EPS and baseline < -EPS and full >= -EPS,
                "full_worsens_decline": service < -EPS and off < -EPS and full < off - EPS,
                "baseline_gain": baseline - off,
                "adaptive_increment": full - baseline,
                "full_gain": full - off,
            }
        )
    return rows


def summarize(rows: list[dict[str, float | bool]]) -> dict[str, object]:
    service_decline = [row for row in rows if row["service_declines"]]
    off_decline = [row for row in service_decline if row["off_reproduction_declines"]]
    def count(field: str, source: list[dict[str, float | bool]]) -> int:
        return sum(bool(row[field]) for row in source)

    return {
        "lineage_contrasts": len(rows),
        "service_decline_contrasts": len(service_decline),
        "service_decline_and_assurance_off_reproduction_decline": len(off_decline),
        "service_and_opportunity_invariant_all_contrasts": all(
            bool(row["service_identical_across_assurance_modes"])
            and bool(row["opportunity_identical_across_assurance_modes"])
            for row in rows
        ),
        "baseline_attenuation_count": count("baseline_attenuates_decline", off_decline),
        "full_attenuation_count": count("full_attenuates_decline", off_decline),
        "baseline_sign_rescue_count": count("baseline_sign_rescue", off_decline),
        "full_sign_rescue_count": count("full_sign_rescue", off_decline),
        "adaptive_additional_rescue_count": count("adaptive_additional_rescue", off_decline),
        "full_worsening_count": count("full_worsens_decline", off_decline),
        "mean_baseline_gain_among_off_declines": mean(float(row["baseline_gain"]) for row in off_decline) if off_decline else None,
        "mean_adaptive_increment_among_off_declines": mean(float(row["adaptive_increment"]) for row in off_decline) if off_decline else None,
        "mean_full_gain_among_off_declines": mean(float(row["full_gain"]) for row in off_decline) if off_decline else None,
    }


def build(
    *,
    replicates: int = 4,
    contexts: int = 4,
    n_lineages: int = 24,
    steps: int = 120,
    seed: int = 20260823,
) -> dict[str, object]:
    v4 = load_module(V4_SCRIPT, "assurance_capability_v4")
    v9 = load_module(V9_SCRIPT, "assurance_capability_v9")
    v10 = load_module(V10_SCRIPT, "assurance_capability_v10")

    rows: list[dict[str, float | bool]] = []
    for saturation in SATURATIONS:
        for support_strength in SUPPORT_STRENGTHS:
            for replicate in range(replicates):
                run_seed = seed + replicate + int(saturation * 10_000) + int(support_strength * 100_000)
                rows.extend(
                    simulate_pair(
                        v4=v4,
                        v9=v9,
                        v10=v10,
                        seed=run_seed,
                        saturation=saturation,
                        support_strength=support_strength,
                        contexts=contexts,
                        n_lineages=n_lineages,
                        steps=steps,
                    )
                )

    summary = summarize(rows)
    if not summary["service_and_opportunity_invariant_all_contrasts"]:
        decision = "invalid_matched_ablation_upstream_changed_between_assurance_modes"
    elif int(summary["full_sign_rescue_count"]) > 0:
        decision = "existing_assurance_route_has_synthetic_sign_rescue_buffering_capability"
    elif int(summary["full_attenuation_count"]) > 0:
        decision = "existing_assurance_route_attenuates_service_driven_reproductive_declines_without_sign_rescue"
    else:
        decision = "existing_assurance_route_does_not_buffer_service_driven_reproductive_declines_in_declared_envelope"

    return {
        "analysis": "assurance_buffering_capability_ablation",
        "status": "synthetic_matched_capability_test_not_empirical_mechanism_admission",
        "question": "Can the already-implemented autonomous-assurance route attenuate or reverse reproductive decline under declining effective service without adding a new parameter?",
        "assurance_modes": {
            "off": "assurance_ceiling=0 and assurance_responsiveness=0",
            "baseline_only": "frozen lineage assurance_ceiling retained; responsiveness=0; initial assurance remains the existing v10 value",
            "full_adaptive": "frozen v4 assurance_ceiling and assurance_responsiveness retained",
        },
        "fixed_components": {
            "upstream_networks_matched_between_modes": True,
            "local_support": "frozen v9 mechanism",
            "partner_effectiveness": "frozen v10 quality mechanism at QUALITY_STRENGTH",
            "dependency_heterogeneity": "frozen v4 lineage distribution",
            "trait_position_and_adjustment": "frozen v4 lineage values",
            "empirical_targets_loaded": [],
            "hawaii_outcomes_loaded": False,
            "campanula_outcomes_loaded": False,
        },
        "design": {
            "saturations": list(SATURATIONS),
            "support_strengths": list(SUPPORT_STRENGTHS),
            "replicates_per_cell": replicates,
            "contexts_per_endpoint": contexts,
            "lineages_per_run": n_lineages,
            "evolution_steps": steps,
            "total_lineage_contrasts": len(rows),
            "buffer_definition": "Among matched contrasts with effective-service decline and reproductive decline when assurance is OFF, attenuation means a larger island-minus-mainland reproduction contrast with assurance ON; sign rescue means OFF < 0 and ON >= 0. No empirical tolerance or fitted biological threshold is used.",
        },
        "summary": summary,
        "decision": decision,
        "claim_boundary": "This test establishes model capability only. A synthetic assurance rescue does not show that assurance explains Hawaiʻi, Nicotiana, Guaiacum, Campanula, or any other empirical system. Empirical admission remains governed by data/design/buffer_mechanism_abm_admission_interface.json and requires a predeclared held-out/prospective test after matched source-native mapping.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=4)
    parser.add_argument("--contexts", type=int, default=4)
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
    print(json.dumps({"summary": payload["summary"], "decision": payload["decision"]}, indent=2))


if __name__ == "__main__":
    main()
