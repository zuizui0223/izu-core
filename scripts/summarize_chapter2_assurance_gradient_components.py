"""Fixed-resident assurance effects on corrected investment-invasion components."""
from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import json

import numpy as np

from scripts.model3_island.selection import investment_invasion_terms
from scripts.run_chapter2_assurance_generality import config, load_design
from scripts.run_model3_persistent_isolation import exposure
from scripts.summarize_chapter2_assurance_generality import bootstrap_interval


COMPONENTS = [
    "gradient",
    "maternal_outcross_component",
    "paternal_export_component",
    "selfing_displacement_component",
    "ovule_allocation_cost_component",
]


def estimate(values: list[float], draws: int, seed: int) -> dict:
    x = np.asarray(values, dtype=float)
    return {
        "mean": float(x.mean()),
        "bootstrap95": bootstrap_interval(x.tolist(), draws, seed),
        "n_histories": int(len(x)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-design", type=Path, required=True)
    parser.add_argument("--diagnostic-design", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    source = load_design(args.source_design)
    diagnostic = json.loads(args.diagnostic_design.read_text(encoding="utf-8"))
    if diagnostic["status"] != "frozen_before_gradient_component_calculation":
        raise ValueError("diagnostic design is not frozen")

    histories = range(
        int(diagnostic["source_histories"]["first"]),
        int(diagnostic["source_histories"]["last"]) + 1,
    )
    if len(histories) != 64:
        raise ValueError("expected 64 visitor histories")

    resident = diagnostic["resident"]
    matching = float(resident["matching"])
    investment = float(resident["investment"])
    assurance_levels = [float(x) for x in resident["assurance_levels"]]
    low, _, high = assurance_levels
    draws = int(diagnostic["bootstrap"]["draws"])
    seed0 = int(diagnostic["bootstrap"]["seed"])

    rows = []
    max_identity_error = 0.0
    estimate_index = 0

    for setting in diagnostic["settings"]:
        cfg = config(source, setting, float(source["main_campaign"]["mutation_probability"]), "evolving")
        for snapshot in diagnostic["visitor_snapshots"]:
            per_history = {}
            for seed in histories:
                per_history[seed] = {}
                for arm in diagnostic["arms"]:
                    visitors = exposure(seed, arm).visitors[int(snapshot)]
                    per_history[seed][arm] = {}
                    for assurance in assurance_levels:
                        z = np.array([matching, investment, assurance], dtype=float)
                        terms = investment_invasion_terms(z, visitors, cfg)
                        vals = {name: float(np.asarray(terms[name])) for name in COMPONENTS}
                        identity = (
                            vals["maternal_outcross_component"]
                            + vals["paternal_export_component"]
                            + vals["selfing_displacement_component"]
                            + vals["ovule_allocation_cost_component"]
                        )
                        max_identity_error = max(max_identity_error, abs(vals["gradient"] - identity))
                        per_history[seed][arm][assurance] = vals

            level_summary = {}
            for arm in diagnostic["arms"]:
                level_summary[arm] = {}
                for assurance in assurance_levels:
                    level_summary[arm][str(assurance)] = {}
                    for component in COMPONENTS:
                        values = [per_history[s][arm][assurance][component] for s in histories]
                        level_summary[arm][str(assurance)][component] = estimate(
                            values, draws, seed0 + estimate_index
                        )
                        estimate_index += 1

            assurance_effect = {}
            raw_effect = {}
            for arm in diagnostic["arms"]:
                assurance_effect[arm] = {}
                raw_effect[arm] = {}
                for component in COMPONENTS:
                    values = [
                        per_history[s][arm][high][component] - per_history[s][arm][low][component]
                        for s in histories
                    ]
                    raw_effect[arm][component] = values
                    assurance_effect[arm][component] = estimate(
                        values, draws, seed0 + estimate_index
                    )
                    estimate_index += 1

            near_minus_far = {}
            for component in COMPONENTS:
                values = [
                    raw_effect["near"][component][j] - raw_effect["far"][component][j]
                    for j in range(len(histories))
                ]
                near_minus_far[component] = estimate(values, draws, seed0 + estimate_index)
                estimate_index += 1

            component_sum_values = []
            gradient_values = []
            for j in range(len(histories)):
                g = raw_effect["near"]["gradient"][j] - raw_effect["far"]["gradient"][j]
                cs = sum(
                    raw_effect["near"][name][j] - raw_effect["far"][name][j]
                    for name in COMPONENTS[1:]
                )
                gradient_values.append(g)
                component_sum_values.append(cs)
            component_identity_error = float(
                np.max(np.abs(np.asarray(gradient_values) - np.asarray(component_sum_values)))
            )
            max_identity_error = max(max_identity_error, component_identity_error)

            rows.append(
                {
                    "setting": setting,
                    "snapshot": int(snapshot),
                    "resident": {
                        "matching": matching,
                        "investment": investment,
                        "assurance_low": low,
                        "assurance_high": high,
                    },
                    "levels": level_summary,
                    "assurance_effect_high_minus_low": assurance_effect,
                    "near_minus_far_assurance_effect": near_minus_far,
                    "max_component_identity_error": component_identity_error,
                }
            )

    result = {
        "schema_version": "1.0",
        "date": "2026-10-06",
        "status": "complete_gradient_component_diagnostic",
        "source_design_sha256": hashlib.sha256(args.source_design.read_bytes()).hexdigest(),
        "diagnostic_design_sha256": hashlib.sha256(args.diagnostic_design.read_bytes()).hexdigest(),
        "independent_visitor_histories": 64,
        "rows": rows,
        "max_additive_identity_error": max_identity_error,
        "claim_boundary": diagnostic["reporting_rules"],
    }
    if args.out.exists():
        raise ValueError("preserve existing gradient-component diagnostic")
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
