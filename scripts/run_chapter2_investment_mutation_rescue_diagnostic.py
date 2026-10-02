"""Prospective diagnostic of why investment mutation accessibility failed.

This experiment does not alter the frozen failed Stage C. It separately tests
whether investment response is limited by standing variation, de novo mutation
supply, or finite-population establishment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from pathlib import Path

import numpy as np

from scripts.run_chapter2_trait_accessibility_mutation_pleiotropy import (
    _founders,
    _simulate_one,
    _visitors,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/design/chapter2_investment_mutation_rescue_diagnostic_20261002.json"


def _canonical_bytes(document: dict) -> bytes:
    return (json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _mean(values):
    x = np.asarray(values, dtype=float)
    return float(x.mean()) if len(x) else None


def run(design: dict) -> dict:
    if design["status"] != "prospective_diagnostic_frozen_before_execution":
        raise ValueError("design must be frozen before execution")

    rows = []
    baseline = design["baseline"]
    for capacity in design["factors"]["capacity"]:
        for standing_name, standing_sd in design["factors"]["standing_sd_investment"].items():
            for mutation_name, mutation_spec in design["factors"]["investment_mutation"].items():
                local = {
                    "baseline": {
                        "capacity": int(capacity),
                        "years": int(baseline["years"]),
                        "survival": float(baseline["survival"]),
                        "activity": float(baseline["activity"]),
                        "fixed_assurance": float(baseline["fixed_assurance"]),
                        "investment_cost": float(baseline["investment_cost"]),
                        "founder_mean_access": float(baseline["founder_mean_access"]),
                        "founder_mean_investment": float(baseline["founder_mean_investment"]),
                        "standing_sd_access": float(baseline["standing_sd_access"]),
                        "standing_sd_investment": float(standing_sd),
                    },
                    "threshold_definition": {
                        "magnitude": 0.05,
                        "sustained_years": 20,
                    },
                }
                for founder_seed in baseline["founder_seeds"]:
                    founders = _founders(local, int(founder_seed))
                    for demographic_seed in baseline["demographic_seeds"]:
                        master = int(
                            np.random.SeedSequence(
                                [int(founder_seed), int(demographic_seed)]
                            ).generate_state(1)[0]
                        )
                        for history_name, optima in baseline["visitor_histories"].items():
                            result = _simulate_one(
                                local,
                                founders=founders,
                                visitors=_visitors(optima),
                                mutation_spec=mutation_spec,
                                coupling=float(design["pleiotropy"]),
                                master_seed=master,
                            )
                            rows.append({
                                "capacity": int(capacity),
                                "standing_regime": standing_name,
                                "standing_sd_investment": float(standing_sd),
                                "mutation_regime": mutation_name,
                                "visitor_history": history_name,
                                "founder_seed": int(founder_seed),
                                "demographic_seed": int(demographic_seed),
                                "terminal_access_change": result["terminal_access_change"],
                                "terminal_investment_change": result["terminal_investment_change"],
                                "terminal_occupancy": result["terminal_occupancy"],
                            })

    def cell(capacity, standing, mutation, history):
        return [
            r for r in rows
            if r["capacity"] == capacity
            and r["standing_regime"] == standing
            and r["mutation_regime"] == mutation
            and r["visitor_history"] == history
        ]

    cell_summary = []
    for capacity in design["factors"]["capacity"]:
        for standing in design["factors"]["standing_sd_investment"]:
            for mutation in design["factors"]["investment_mutation"]:
                for history in baseline["visitor_histories"]:
                    x = cell(capacity, standing, mutation, history)
                    cell_summary.append({
                        "capacity": int(capacity),
                        "standing_regime": standing,
                        "mutation_regime": mutation,
                        "visitor_history": history,
                        "n": len(x),
                        "mean_abs_investment_change": _mean([
                            abs(r["terminal_investment_change"])
                            for r in x if r["terminal_investment_change"] is not None
                        ]),
                        "mean_signed_investment_change": _mean([
                            r["terminal_investment_change"]
                            for r in x if r["terminal_investment_change"] is not None
                        ]),
                        "mean_abs_access_change": _mean([
                            abs(r["terminal_access_change"])
                            for r in x if r["terminal_access_change"] is not None
                        ]),
                        "terminal_occupancy": _mean([r["terminal_occupancy"] for r in x]),
                    })

    def summary(capacity, standing, mutation, history):
        return next(
            r for r in cell_summary
            if r["capacity"] == capacity
            and r["standing_regime"] == standing
            and r["mutation_regime"] == mutation
            and r["visitor_history"] == history
        )

    standing_effects = []
    mutation_effects = []
    capacity_mutation_effects = {int(c): [] for c in design["factors"]["capacity"]}
    for capacity in design["factors"]["capacity"]:
        for history in baseline["visitor_histories"]:
            low_equal = summary(capacity, "low", "equal_baseline", history)
            high_equal = summary(capacity, "high", "equal_baseline", history)
            low_mut = summary(capacity, "low", "investment_accessible", history)
            standing_effects.append(
                high_equal["mean_abs_investment_change"]
                - low_equal["mean_abs_investment_change"]
            )
            rescue = (
                low_mut["mean_abs_investment_change"]
                - low_equal["mean_abs_investment_change"]
            )
            mutation_effects.append(rescue)
            capacity_mutation_effects[int(capacity)].append(rescue)

    contrasts = {
        "standing_variation_effect": float(np.mean(standing_effects)),
        "mutation_rescue_effect": float(np.mean(mutation_effects)),
        "mutation_rescue_by_capacity": {
            str(c): float(np.mean(v)) for c, v in capacity_mutation_effects.items()
        },
    }
    caps = sorted(int(x) for x in design["factors"]["capacity"])
    contrasts["capacity_modulation_of_mutation_rescue"] = (
        contrasts["mutation_rescue_by_capacity"][str(caps[-1])]
        - contrasts["mutation_rescue_by_capacity"][str(caps[0])]
    )

    decisions = {
        "standing_variation_bottleneck": contrasts["standing_variation_effect"] > 0,
        "de_novo_mutation_rescue": contrasts["mutation_rescue_effect"] > 0,
        "finite_establishment_bottleneck": contrasts["capacity_modulation_of_mutation_rescue"] > 0,
    }

    return {
        "status": "complete_investment_mutation_rescue_diagnostic",
        "design_sha256": hashlib.sha256(_canonical_bytes(design)).hexdigest(),
        "n_trajectories": len(rows),
        "cell_summary": cell_summary,
        "contrasts": contrasts,
        "decisions": decisions,
        "claim_boundary": design["claim_boundary"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--design", default=str(DEFAULT_DESIGN))
    parser.add_argument("--out")
    args = parser.parse_args()
    design = json.loads(Path(args.design).read_text(encoding="utf-8"))
    result = run(design)
    encoded = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.out:
        path = Path(args.out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
