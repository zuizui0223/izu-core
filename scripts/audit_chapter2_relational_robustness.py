from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import replace
from pathlib import Path

from scripts.run_chapter2_conditional_why_diagnostics import (
    response_matrix,
    realization_class_counts,
    two_way_decomposition,
)
from scripts.run_response_geometry_parameter_robustness import BASE

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_relational_robustness_audit_freeze_20260831.json"
LEDGER = ROOT / "data/design/chapter2_external_prediction_admission_ledger_20260828.csv"
OUT = ROOT / "data/results/chapter2_relational_robustness_audit_frozen_20260831.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summarize_matrix(cfg, *, seed: int, replicates: int = 96) -> dict:
    matrix = response_matrix(cfg, replicates, seed)
    decomposition = two_way_decomposition(matrix)
    fractions = decomposition["sum_of_squares_fraction"]
    ranked = sorted(
        (
            ("starting_position", float(fractions["starting_position"])),
            ("community_realization", float(fractions["community_realization"])),
            (
                "starting_position_by_community_nonadditivity",
                float(fractions["starting_position_by_community_nonadditivity"]),
            ),
        ),
        key=lambda item: (-item[1], item[0]),
    )
    return {
        "realization_class_counts": realization_class_counts(matrix),
        "sum_of_squares_fraction": fractions,
        "component_ranking": [name for name, _ in ranked],
        "largest_component": ranked[0][0],
        "additive_sign_mismatch_cells": decomposition["additive_sign_mismatch_cells"],
        "additive_sign_mismatch_fraction": decomposition["additive_sign_mismatch_fraction"],
        "interpretation_boundary": (
            "Conditional on each shared pollinator-community trajectory, every starting-position x community cell is deterministic. "
            "The residual sum of squares is therefore the non-additive starting-position-by-community-realization component of this "
            "fixed response matrix, not a mixture with within-cell simulation noise. The sampled community trajectories remain a "
            "finite synthetic ensemble, so numerical variance shares are ensemble-specific design diagnostics rather than population parameters."
        ),
    }


def direct_measurement_counts() -> dict[str, int]:
    columns = json.loads(DESIGN.read_text(encoding="utf-8"))["external_measurement_asymmetry"]["columns"]
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return {
        column: sum(row[column] == "direct_measurement" for row in rows)
        for column in columns
    }


def build() -> dict:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    if design.get("status") != "fixed_before_execution":
        raise ValueError("relational robustness audit design is not frozen before execution")

    replicates = int(design["baseline"]["matched_community_realizations"])
    baseline_seed = int(design["baseline"]["seed"])

    horizon_rows = []
    for steps in design["structural_horizon"]["steps"]:
        cfg = replace(BASE, steps=int(steps))
        horizon_rows.append({"steps": int(steps), **summarize_matrix(cfg, seed=baseline_seed, replicates=replicates)})

    adjustment_rows = []
    for value in design["trait_adjustment_context"]["values"]:
        cfg = replace(BASE, trait_adjustment=float(value))
        adjustment_rows.append({
            "trait_adjustment": float(value),
            **summarize_matrix(cfg, seed=baseline_seed, replicates=replicates),
        })

    seed_rows = []
    for seed in design["seed_ensemble"]["values"]:
        seed_rows.append({"seed": int(seed), **summarize_matrix(BASE, seed=int(seed), replicates=replicates)})

    equal_cfg = replace(
        BASE,
        island=replace(BASE.island, n_pollinator_types=int(design["equal_richness"]["island_initial_pollinator_types"])),
    )
    equal_richness = summarize_matrix(equal_cfg, seed=baseline_seed, replicates=replicates)
    equal_richness["mainland_initial_pollinator_types"] = BASE.mainland.n_pollinator_types
    equal_richness["island_initial_pollinator_types"] = equal_cfg.island.n_pollinator_types
    equal_richness["boundary"] = (
        "Only initial pollinator richness is equalized. Loss, arrival, dispersion, generalist fraction and replacement fraction retain "
        "their baseline mainland-like versus island-like differences. A mixed result therefore shows that richness reduction is not "
        "necessary for mixed response geometry; it does not show that island-specific community reorganization is unnecessary."
    )

    direct_counts = direct_measurement_counts()
    ordered_direct_counts = sorted(direct_counts.items(), key=lambda item: (-item[1], item[0]))

    baseline = next(row for row in seed_rows if row["seed"] == baseline_seed)
    seed_community_values = [float(row["sum_of_squares_fraction"]["community_realization"]) for row in seed_rows]
    seed_starting_values = [float(row["sum_of_squares_fraction"]["starting_position"]) for row in seed_rows]
    seed_nonadd_values = [
        float(row["sum_of_squares_fraction"]["starting_position_by_community_nonadditivity"])
        for row in seed_rows
    ]

    zero_adjustment = next(row for row in adjustment_rows if row["trait_adjustment"] == 0.0)
    equal_mixed = int(equal_richness["realization_class_counts"]["mixed_sign"])

    return {
        "schema_version": "1.0",
        "analysis": "chapter2_relational_robustness_audit",
        "status": "frozen_complete_20260831",
        "input_identity": {
            "design_sha256": sha256(DESIGN),
            "audit_script_sha256": sha256(Path(__file__)),
            "ledger_sha256": sha256(LEDGER),
        },
        "baseline_frozen_reference": {
            "seed": baseline_seed,
            "steps": BASE.steps,
            "trait_adjustment": BASE.trait_adjustment,
            "sum_of_squares_fraction": baseline["sum_of_squares_fraction"],
            "realization_class_counts": baseline["realization_class_counts"],
        },
        "structural_horizon": horizon_rows,
        "trait_adjustment_context": adjustment_rows,
        "seed_ensemble": {
            "rows": seed_rows,
            "community_realization_fraction_range": [min(seed_community_values), max(seed_community_values)],
            "starting_position_fraction_range": [min(seed_starting_values), max(seed_starting_values)],
            "nonadditive_fraction_range": [min(seed_nonadd_values), max(seed_nonadd_values)],
            "baseline_seed_is_maximum_community_fraction_in_this_prespecified_ensemble": (
                float(baseline["sum_of_squares_fraction"]["community_realization"]) == max(seed_community_values)
            ),
            "boundary": (
                "The historical seed remains the frozen baseline and is not replaced. This ensemble is a sensitivity audit of finite-community "
                "realization magnitude, not a new population-level variance estimate."
            ),
        },
        "equal_initial_pollinator_richness": equal_richness,
        "external_measurement_asymmetry": {
            "research_entries": 25,
            "direct_measurement_counts": dict(ordered_direct_counts),
            "highest_direct_measurement_item": ordered_direct_counts[0][0],
            "lowest_direct_measurement_item": ordered_direct_counts[-1][0],
            "boundary": (
                "These are source-audited research-entry availability counts before geographic de-duplication, not independent-archipelago frequencies."
            ),
        },
        "interpretation_corrections": {
            "nonadditivity": (
                "The old frozen diagnostic wording that added 'cell-level simulation variation' is superseded for interpretation. "
                "Because each community trajectory is generated once and shared across starting positions, cells are deterministic conditional "
                "on trajectory; the residual is state-by-community nonadditivity in the fixed matrix."
            ),
            "starting_state": (
                "A small additive starting-position SS fraction is not evidence that starting state is biologically absent. At zero trait adjustment, "
                "mixed realization geometry remains evaluable while state dependence can appear primarily as state-by-community nonadditivity. "
                "Trait adjustment changes the additive/non-additive expression of state dependence rather than creating state dependence de novo."
            ),
            "headline": (
                "Use component ordering and relational state-versus-realized-community structure as the headline. Retain 80.17/17.64/2.18% only as "
                "the historically frozen baseline example, with the seed-ensemble range disclosed."
            ),
        },
        "claim_tests": {
            "mixed_geometry_at_zero_trait_adjustment": zero_adjustment["realization_class_counts"]["mixed_sign"] > 0,
            "equal_richness_mixed_geometry_present": equal_mixed > 0,
            "starting_position_never_largest_across_prespecified_seed_ensemble": all(
                row["largest_component"] != "starting_position" for row in seed_rows
            ),
            "starting_position_never_largest_across_structural_horizons": all(
                row["largest_component"] != "starting_position" for row in horizon_rows
            ),
        },
        "claim_boundary": (
            "This audit does not recalibrate the model, reopen external prediction, or estimate natural frequencies. It tests whether manuscript-level "
            "structural claims survive prespecified changes to seed ensemble, horizon, trait adjustment and initial richness while preserving the original "
            "frozen baseline as provenance."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "baseline": payload["baseline_frozen_reference"],
        "structural_horizon": [
            {
                "steps": row["steps"],
                "counts": row["realization_class_counts"],
                "fractions": row["sum_of_squares_fraction"],
                "largest_component": row["largest_component"],
            }
            for row in payload["structural_horizon"]
        ],
        "trait_adjustment_context": [
            {
                "trait_adjustment": row["trait_adjustment"],
                "counts": row["realization_class_counts"],
                "fractions": row["sum_of_squares_fraction"],
                "largest_component": row["largest_component"],
            }
            for row in payload["trait_adjustment_context"]
        ],
        "seed_ranges": {
            "community": payload["seed_ensemble"]["community_realization_fraction_range"],
            "starting": payload["seed_ensemble"]["starting_position_fraction_range"],
            "nonadditive": payload["seed_ensemble"]["nonadditive_fraction_range"],
            "baseline_max_community": payload["seed_ensemble"]["baseline_seed_is_maximum_community_fraction_in_this_prespecified_ensemble"],
        },
        "equal_richness": {
            "counts": payload["equal_initial_pollinator_richness"]["realization_class_counts"],
            "fractions": payload["equal_initial_pollinator_richness"]["sum_of_squares_fraction"],
            "largest_component": payload["equal_initial_pollinator_richness"]["largest_component"],
        },
        "direct_measurement_counts": payload["external_measurement_asymmetry"]["direct_measurement_counts"],
        "claim_tests": payload["claim_tests"],
    }, indent=2))


if __name__ == "__main__":
    main()
