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
OUT = ROOT / "data/results/network_context_buffering_capability_ablation.json"
EPS = 1e-12
SATURATIONS = (1.0, 2.0, 3.0)
SUPPORT_OFF = 0.0
SUPPORT_ON = 0.5


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
    return {
        name: float(sum(row))
        for name, row in zip(network.plant_names, network.matrix)
    }


def simulate_pair(
    *,
    v4,
    v9,
    v10,
    seed: int,
    saturation: float,
    contexts: int,
    n_lineages: int,
    steps: int,
) -> list[dict[str, float | bool]]:
    templates = disable_assurance(v4.make_lineages(random.Random(seed), n_lineages))
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
    mainland_global = row_sums(mainland_opportunity)
    island_global = row_sums(island_opportunity)

    outputs = {}
    for mode, support_strength in (("off", SUPPORT_OFF), ("on", SUPPORT_ON)):
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

    rows = []
    for index in range(n_lineages):
        name = f"lineage_{index + 1}"
        global_delta = island_global[name] - mainland_global[name]
        service = {}
        reproduction = {}
        for mode in ("off", "on"):
            mainland, island = outputs[mode]
            service[mode] = island[name]["mean_effective_service"] - mainland[name]["mean_effective_service"]
            reproduction[mode] = island[name]["mean_reproduction"] - mainland[name]["mean_reproduction"]

        global_decline = global_delta < -EPS
        service_off_decline = service["off"] < -EPS
        reproduction_off_decline = reproduction["off"] < -EPS
        rows.append({
            "global_opportunity_delta": global_delta,
            "service_delta_support_off": service["off"],
            "service_delta_support_on": service["on"],
            "reproduction_delta_support_off": reproduction["off"],
            "reproduction_delta_support_on": reproduction["on"],
            "global_opportunity_declines": global_decline,
            "service_off_declines": service_off_decline,
            "reproduction_off_declines": reproduction_off_decline,
            "service_magnitude_rescue": global_decline and service_off_decline and service["on"] > service["off"] + EPS,
            "service_sign_rescue": global_decline and service_off_decline and service["on"] >= -EPS,
            "reproduction_magnitude_rescue": global_decline and reproduction_off_decline and reproduction["on"] > reproduction["off"] + EPS,
            "reproduction_sign_rescue": global_decline and reproduction_off_decline and reproduction["on"] >= -EPS,
            "service_worsening": global_decline and service_off_decline and service["on"] < service["off"] - EPS,
            "reproduction_worsening": global_decline and reproduction_off_decline and reproduction["on"] < reproduction["off"] - EPS,
            "service_gain": service["on"] - service["off"],
            "reproduction_gain": reproduction["on"] - reproduction["off"],
        })
    return rows


def summarize(rows: list[dict[str, float | bool]]) -> dict[str, object]:
    global_declines = [row for row in rows if row["global_opportunity_declines"]]
    service_declines = [row for row in global_declines if row["service_off_declines"]]
    reproduction_declines = [row for row in global_declines if row["reproduction_off_declines"]]

    def count(field: str, source: list[dict[str, float | bool]]) -> int:
        return sum(bool(row[field]) for row in source)

    return {
        "lineage_contrasts": len(rows),
        "global_opportunity_decline_contrasts": len(global_declines),
        "global_decline_and_support_off_service_decline": len(service_declines),
        "global_decline_and_support_off_reproduction_decline": len(reproduction_declines),
        "service_magnitude_rescue_count": count("service_magnitude_rescue", service_declines),
        "service_sign_rescue_count": count("service_sign_rescue", service_declines),
        "reproduction_magnitude_rescue_count": count("reproduction_magnitude_rescue", reproduction_declines),
        "reproduction_sign_rescue_count": count("reproduction_sign_rescue", reproduction_declines),
        "service_worsening_count": count("service_worsening", service_declines),
        "reproduction_worsening_count": count("reproduction_worsening", reproduction_declines),
        "mean_service_gain_among_support_off_declines": mean(float(row["service_gain"]) for row in service_declines) if service_declines else None,
        "mean_reproduction_gain_among_support_off_declines": mean(float(row["reproduction_gain"]) for row in reproduction_declines) if reproduction_declines else None,
    }


def build(
    *,
    replicates: int = 4,
    contexts: int = 4,
    n_lineages: int = 24,
    steps: int = 120,
    seed: int = 20260823,
) -> dict[str, object]:
    v4 = load_module(V4_SCRIPT, "network_buffer_v4")
    v9 = load_module(V9_SCRIPT, "network_buffer_v9")
    v10 = load_module(V10_SCRIPT, "network_buffer_v10")

    rows: list[dict[str, float | bool]] = []
    for saturation in SATURATIONS:
        for replicate in range(replicates):
            run_seed = seed + replicate + int(saturation * 10_000)
            rows.extend(
                simulate_pair(
                    v4=v4,
                    v9=v9,
                    v10=v10,
                    seed=run_seed,
                    saturation=saturation,
                    contexts=contexts,
                    n_lineages=n_lineages,
                    steps=steps,
                )
            )

    summary = summarize(rows)
    if int(summary["reproduction_sign_rescue_count"]) > 0:
        decision = "existing_local_support_route_has_synthetic_network_context_sign_buffering_capability"
    elif int(summary["service_sign_rescue_count"]) > 0:
        decision = "existing_local_support_route_can_rescue_effective_service_sign_without_reproductive_sign_rescue"
    elif int(summary["reproduction_magnitude_rescue_count"]) > 0 or int(summary["service_magnitude_rescue_count"]) > 0:
        decision = "existing_local_support_route_changes_buffering_magnitude_without_sign_rescue"
    else:
        decision = "existing_local_support_route_does_not_buffer_declining_global_opportunity_in_declared_envelope"

    return {
        "analysis": "network_context_buffering_capability_ablation",
        "status": "synthetic_matched_capability_test_not_empirical_mechanism_admission",
        "question": "Can the already-implemented local support/network-context route convert declining global opportunity into maintained effective service or reproduction when autonomous assurance is disabled?",
        "matched_ablation": {
            "support_off": SUPPORT_OFF,
            "support_on": SUPPORT_ON,
            "assurance_ceiling": 0.0,
            "assurance_responsiveness": 0.0,
            "partner_effectiveness_strength": "frozen v10 QUALITY_STRENGTH",
            "dependency_heterogeneity": "frozen v4 lineage distribution",
            "same_global_opportunity_networks_between_support_modes": True,
            "empirical_targets_loaded": [],
        },
        "design": {
            "saturations": list(SATURATIONS),
            "replicates_per_saturation": replicates,
            "contexts_per_endpoint": contexts,
            "lineages_per_run": n_lineages,
            "evolution_steps": steps,
            "lineage_contrasts": len(rows),
            "sign_rescue_definition": "For lineages with declining global opportunity and a negative support-OFF delta, support ON reaches a non-negative effective-service or reproductive delta. Only the zero directional boundary is used.",
        },
        "summary": summary,
        "decision": decision,
        "claim_boundary": "This is a synthetic capability test of an already-existing network-context route. A sign rescue would not empirically identify service redundancy in Guaiacum or any other island system. Empirical admission remains governed by the common buffer-mechanism interface and requires matched source-native evidence plus a predeclared held-out/prospective test."
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
