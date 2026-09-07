from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from statistics import mean

from scripts.run_chapter2_conditional_why_diagnostics import (
    classify_matrix,
    realization_class_counts,
    two_way_decomposition,
)
from scripts.run_response_geometry_parameter_robustness import (
    BASE,
    TRAIT_GRID,
    endpoint_on_trajectory,
    pollinator_trajectory,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_realized_richness_matching_freeze_20260907.json"
MODEL = ROOT / "scripts/run_response_geometry_parameter_robustness.py"
DIAGNOSTICS = ROOT / "scripts/run_chapter2_conditional_why_diagnostics.py"
OUT = ROOT / "data/results/chapter2_realized_richness_matching_frozen_20260907.json"


def git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def _expected_blob(value: str) -> str:
    if not value.startswith("blob:"):
        raise ValueError(f"expected blob identity, got {value!r}")
    return value.split(":", 1)[1]


def verify_design(design: dict) -> None:
    if design.get("status") != "fixed_before_execution":
        raise ValueError("realized-richness sensitivity was not frozen before execution")
    identities = design["source_identity"]
    observed = {
        "scripts/run_response_geometry_parameter_robustness.py": git_blob_sha(MODEL),
        "scripts/run_chapter2_conditional_why_diagnostics.py": git_blob_sha(DIAGNOSTICS),
    }
    failed = [
        path
        for path, blob in observed.items()
        if blob != _expected_blob(identities[path])
    ]
    if failed:
        raise RuntimeError(f"source identity changed after sensitivity freeze: {failed}")
    baseline = design["baseline"]
    if int(baseline["steps"]) != BASE.steps:
        raise RuntimeError("frozen step count does not match BASE")
    if int(baseline["trait_grid_points"]) != len(TRAIT_GRID):
        raise RuntimeError("frozen trait-grid size does not match BASE")


def _subsample(snapshot: tuple, target: int, rng: random.Random) -> tuple:
    if target < 0 or target > len(snapshot):
        raise ValueError("invalid richness target")
    if target == len(snapshot):
        return snapshot
    if target == 0:
        return ()
    indices = sorted(rng.sample(range(len(snapshot)), target))
    return tuple(snapshot[index] for index in indices)


def match_trajectories(
    mainland: tuple[tuple, ...],
    island: tuple[tuple, ...],
    *,
    matching_seed: int,
    replicate_index: int,
    design: dict,
) -> tuple[tuple[tuple, ...], tuple[tuple, ...], dict]:
    if len(mainland) != len(island):
        raise RuntimeError("trajectory lengths differ before richness matching")
    rng_design = design["matching_rng"]
    stride = int(rng_design["replicate_stride"])
    mainland_rng = random.Random(
        int(matching_seed) + int(replicate_index) * stride + int(rng_design["mainland_offset"])
    )
    island_rng = random.Random(
        int(matching_seed) + int(replicate_index) * stride + int(rng_design["island_offset"])
    )

    matched_mainland: list[tuple] = []
    matched_island: list[tuple] = []
    targets: list[int] = []
    original_gaps: list[int] = []
    original_mainland: list[int] = []
    original_island: list[int] = []
    unequal_after = 0

    for mainland_snapshot, island_snapshot in zip(mainland, island):
        mainland_n = len(mainland_snapshot)
        island_n = len(island_snapshot)
        target = min(mainland_n, island_n)
        mainland_matched = _subsample(mainland_snapshot, target, mainland_rng)
        island_matched = _subsample(island_snapshot, target, island_rng)
        if len(mainland_matched) != len(island_matched):
            unequal_after += 1
        matched_mainland.append(mainland_matched)
        matched_island.append(island_matched)
        targets.append(target)
        original_gaps.append(abs(mainland_n - island_n))
        original_mainland.append(mainland_n)
        original_island.append(island_n)

    return (
        tuple(matched_mainland),
        tuple(matched_island),
        {
            "snapshots": len(targets),
            "unequal_after_matching": unequal_after,
            "target_richness_values": targets,
            "original_absolute_richness_gaps": original_gaps,
            "original_mainland_richness_values": original_mainland,
            "original_island_richness_values": original_island,
        },
    )


def matched_response_matrix(*, matching_seed: int, design: dict) -> tuple[list[list[float]], dict]:
    baseline = design["baseline"]
    community_seed = int(baseline["community_seed"])
    replicates = int(baseline["matched_community_realizations"])
    matrix: list[list[float]] = [[] for _ in TRAIT_GRID]

    target_values: list[int] = []
    original_gaps: list[int] = []
    original_mainland_values: list[int] = []
    original_island_values: list[int] = []
    unequal_after = 0

    for rep in range(replicates):
        run_seed = community_seed + rep * 10_000
        mainland = pollinator_trajectory(BASE.mainland, run_seed + 100_000, BASE)
        island = pollinator_trajectory(BASE.island, run_seed + 200_000, BASE)
        matched_mainland, matched_island, audit = match_trajectories(
            mainland,
            island,
            matching_seed=matching_seed,
            replicate_index=rep,
            design=design,
        )
        unequal_after += int(audit["unequal_after_matching"])
        target_values.extend(audit["target_richness_values"])
        original_gaps.extend(audit["original_absolute_richness_gaps"])
        original_mainland_values.extend(audit["original_mainland_richness_values"])
        original_island_values.extend(audit["original_island_richness_values"])

        for index, trait in enumerate(TRAIT_GRID):
            _, mainland_service = endpoint_on_trajectory(trait, matched_mainland, BASE)
            _, island_service = endpoint_on_trajectory(trait, matched_island, BASE)
            matrix[index].append(island_service - mainland_service)

    if not target_values:
        raise RuntimeError("no matched snapshots were produced")
    total_snapshots = len(target_values)
    richness_audit = {
        "trajectory_pairs": replicates,
        "steps_per_pair": BASE.steps,
        "total_snapshot_pairs": total_snapshots,
        "unequal_after_matching": unequal_after,
        "all_snapshot_pairs_equal_realized_richness": unequal_after == 0,
        "target_richness": {
            "mean": mean(target_values),
            "min": min(target_values),
            "max": max(target_values),
            "zero_snapshot_pairs": sum(value == 0 for value in target_values),
            "zero_snapshot_fraction": sum(value == 0 for value in target_values) / total_snapshots,
        },
        "before_matching": {
            "mean_mainland_richness": mean(original_mainland_values),
            "mean_island_richness": mean(original_island_values),
            "mean_absolute_richness_gap": mean(original_gaps),
            "snapshot_pairs_with_nonzero_gap": sum(value > 0 for value in original_gaps),
            "fraction_with_nonzero_gap": sum(value > 0 for value in original_gaps) / total_snapshots,
        },
    }
    return matrix, richness_audit


def summarize_seed(*, matching_seed: int, design: dict) -> dict:
    matrix, richness = matched_response_matrix(matching_seed=matching_seed, design=design)
    decomposition = two_way_decomposition(matrix)
    fractions = decomposition["sum_of_squares_fraction"]
    return {
        "matching_seed": int(matching_seed),
        "mean_geometry_classification": classify_matrix(matrix),
        "realization_class_counts": realization_class_counts(matrix),
        "sum_of_squares_fraction": {
            "starting_position": float(fractions["starting_position"]),
            "community_realization": float(fractions["community_realization"]),
            "starting_position_by_community_nonadditivity": float(
                fractions["starting_position_by_community_nonadditivity"]
            ),
        },
        "additive_sign_mismatch_cells": int(decomposition["additive_sign_mismatch_cells"]),
        "additive_sign_mismatch_fraction": float(decomposition["additive_sign_mismatch_fraction"]),
        "richness_audit": richness,
    }


def build() -> dict:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    verify_design(design)
    seeds = [int(value) for value in design["matching_rng"]["seeds"]]
    primary_seed = int(design["matching_rng"]["primary_seed"])
    if primary_seed not in seeds:
        raise RuntimeError("primary matching seed is not in prespecified seed ensemble")

    rows = [summarize_seed(matching_seed=seed, design=design) for seed in seeds]
    primary = next(row for row in rows if row["matching_seed"] == primary_seed)

    hard_control_valid = all(
        row["richness_audit"]["all_snapshot_pairs_equal_realized_richness"] for row in rows
    )
    primary_mixed = primary["mean_geometry_classification"] == "mixed_mean_geometry"
    ensemble_mixed = all(row["mean_geometry_classification"] == "mixed_mean_geometry" for row in rows)
    individual_mixed = all(row["realization_class_counts"]["mixed_sign"] > 0 for row in rows)
    relational_nonadditivity = all(
        row["sum_of_squares_fraction"]["starting_position_by_community_nonadditivity"] > 0
        for row in rows
    )
    conditions = {
        "hard_control_valid": hard_control_valid,
        "primary_mixed_geometry": primary_mixed,
        "ensemble_mixed_geometry": ensemble_mixed,
        "individual_mixed_realizations": individual_mixed,
        "relational_nonadditivity": relational_nonadditivity,
    }
    if all(conditions.values()):
        decision = "scientific_blocker_cleared_realized_richness_difference_not_required"
    elif hard_control_valid and primary_mixed:
        decision = "partial_clear_narrow_robustness_wording_before_submission"
    else:
        decision = "blocker_failed_reframe_before_author_metadata"

    def values(path: tuple[str, ...]) -> list[float]:
        output = []
        for row in rows:
            value = row
            for key in path:
                value = value[key]
            output.append(float(value))
        return output

    mixed_counts = [row["realization_class_counts"]["mixed_sign"] for row in rows]
    return {
        "schema_version": "1.0",
        "analysis": "chapter2_realized_richness_matching_sensitivity",
        "status": "frozen_complete_20260907",
        "design": design,
        "method": (
            "Original BASE mainland-like and island-like trajectories are generated unchanged. At every step, each pair is hard-matched "
            "to min(realized mainland richness, realized island richness). Only the larger snapshot is uniformly subsampled without replacement, "
            "using response-blind prespecified matching seeds. The matched trajectory, not the original trajectory, is then supplied to trait "
            "adjustment and endpoint service."
        ),
        "rows": rows,
        "primary": primary,
        "ensemble_summary": {
            "matching_seeds": seeds,
            "mean_geometry_classifications": [row["mean_geometry_classification"] for row in rows],
            "mixed_realization_count_range": [min(mixed_counts), max(mixed_counts)],
            "starting_position_fraction_range": [
                min(values(("sum_of_squares_fraction", "starting_position"))),
                max(values(("sum_of_squares_fraction", "starting_position"))),
            ],
            "community_realization_fraction_range": [
                min(values(("sum_of_squares_fraction", "community_realization"))),
                max(values(("sum_of_squares_fraction", "community_realization"))),
            ],
            "nonadditivity_fraction_range": [
                min(values(("sum_of_squares_fraction", "starting_position_by_community_nonadditivity"))),
                max(values(("sum_of_squares_fraction", "starting_position_by_community_nonadditivity"))),
            ],
            "zero_target_snapshot_fraction_range": [
                min(values(("richness_audit", "target_richness", "zero_snapshot_fraction"))),
                max(values(("richness_audit", "target_richness", "zero_snapshot_fraction"))),
            ],
        },
        "decision_gate": {
            "conditions": conditions,
            "decision": decision,
        },
        "claim_boundary": design["claim_boundary"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "decision": payload["decision_gate"],
        "primary": {
            "classification": payload["primary"]["mean_geometry_classification"],
            "counts": payload["primary"]["realization_class_counts"],
            "fractions": payload["primary"]["sum_of_squares_fraction"],
            "richness": payload["primary"]["richness_audit"],
        },
        "ensemble": payload["ensemble_summary"],
    }, indent=2))


if __name__ == "__main__":
    main()
