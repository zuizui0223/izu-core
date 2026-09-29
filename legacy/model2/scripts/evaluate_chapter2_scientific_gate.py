from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_OUT = Path("data/results/chapter2_scientific_gate_decision.json")


def _joint_mixed_fraction(joint: dict) -> float:
    """Read the actual phase-2 contract while retaining compatibility with early test payloads."""
    if "class_fractions" in joint:
        return float(joint["class_fractions"].get("mixed_mean_geometry", 0.0))
    summary = joint.get("summary", {})
    return float(summary.get("mixed_mean_geometry_fraction", 0.0))


def assess(phase1: dict, joint: dict, thresholds: dict) -> dict:
    baseline = phase1["baseline"]
    context_map = thresholds["context_map"]
    assurance_map = thresholds["assurance_map"]

    mean_boundary = bool(baseline.get("mean_geometry_mixed_sign", baseline.get("mixed_sign_geometry", False)))
    realization_fraction = float(baseline.get("mixed_sign_realization_fraction", 0.0))
    joint_mixed_fraction = _joint_mixed_fraction(joint)
    context_any = int(context_map.get("lineages_with_any_sign_change", 0)) > 0
    assurance_service_safe = bool(assurance_map.get("upstream_service_identical_across_assurance_multipliers", False))
    assurance_any_rescue = int(assurance_map.get("lineages_with_any_sign_rescue", 0)) > 0

    if mean_boundary and joint_mixed_fraction >= 0.25:
        route = "research_article_candidate"
        headline = "conditional_response_geometry"
    elif realization_fraction >= 0.25 and joint_mixed_fraction > 0.0:
        route = "research_article_possible_but_branching_is_realization_contingent"
        headline = "starting_position_by_pollinator_realization_interaction"
    else:
        route = "conceptual_review_or_mini_review"
        headline = "three_layer_island_syndrome_decomposition"

    blockers = []
    if not assurance_service_safe:
        blockers.append("assurance_threshold_map_changes_upstream_service")
    if not context_any:
        blockers.append("no_local_context_sign_change_found")
    if route.startswith("research_article") and joint_mixed_fraction == 0.0:
        blockers.append("mixed_geometry_absent_from_joint_parameter_space")

    return {
        "analysis": "chapter2_scientific_gate_decision",
        "route": route,
        "headline": headline,
        "evidence": {
            "baseline_mean_sign_boundary": mean_boundary,
            "baseline_mixed_realization_fraction": realization_fraction,
            "joint_mixed_mean_geometry_fraction": joint_mixed_fraction,
            "local_context_changes_sign_for_some_lineages": context_any,
            "assurance_threshold_upstream_service_invariant": assurance_service_safe,
            "assurance_sign_rescue_exists_within_sensitivity_envelope": assurance_any_rescue,
            "median_context_first_sign_change_strength": context_map.get("median_first_sign_change_strength"),
            "median_assurance_first_sign_rescue_multiplier": assurance_map.get("median_first_sign_rescue_multiplier"),
        },
        "blocking_failures": blockers,
        "submission_ready": route.startswith("research_article") and not blockers,
        "claim_boundary": (
            "A Research Article route is supported only if mixed response geometry is not confined to one stochastic realization or a vanishingly narrow parameter corner. "
            "Design-space fractions are robustness descriptors, not ecological prevalence estimates. Context and assurance thresholds remain synthetic sensitivity properties."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase1", type=Path, required=True)
    parser.add_argument("--joint", type=Path, required=True)
    parser.add_argument("--thresholds", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    phase1 = json.loads(args.phase1.read_text(encoding="utf-8"))
    joint = json.loads(args.joint.read_text(encoding="utf-8"))
    thresholds = json.loads(args.thresholds.read_text(encoding="utf-8"))
    result = assess(phase1, joint, thresholds)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
