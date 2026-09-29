#!/usr/bin/env python3
"""Summarize evidence architecture across island systems without pooling effects.

This analysis operates on evidence/admission state only. It must not be interpreted
as a biological effect-direction analysis: a direct cell means that a response axis
has source-locked/direct evidence in that system, not that the response changed in
a common direction.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

DEFAULT_AXES = (
    "pollinator_functional_environment",
    "floral_morphology",
    "mating_and_reproductive_assurance",
    "visual_signal",
    "pollinator_effectiveness",
    "interaction_network",
    "reproductive_outcome",
)

EXACT_MISSING = {
    "not_registered",
    "not_primary_axis_in_registered_panels",
    "not_registered_as_controlled_dependency",
    "direct_current_six_channel_field_bundle_missing",
    "raw_treatment_outcome_table_missing",
}
PARTIAL_MARKERS = (
    "context",
    "blocked",
    "not_common_estimand",
    "cross_year",
)


def classify_cell(status: str) -> str:
    value = status.strip().lower()
    if (
        value in EXACT_MISSING
        or value.startswith("missing_")
        or value.startswith("matched_per_visit_pollen_function_missing")
        or value.startswith("not_harmonized")
    ):
        return "missing"
    if value.startswith("partial_"):
        return "partial"
    if "missing" in value:
        return "partial"
    if value.startswith("source_locked"):
        return "partial" if "cross_year" in value else "direct"
    if any(marker in value for marker in PARTIAL_MARKERS):
        return "partial"
    return "direct"


def analyze(matrix: dict) -> dict:
    systems = matrix["systems"]
    axes = tuple(matrix.get("response_axes", DEFAULT_AXES))
    if set(axes) != set(DEFAULT_AXES):
        raise ValueError("response-axis matrix does not match the current seven-axis registry")

    by_axis = {axis: Counter() for axis in axes}
    profiles = []
    direct_sets: dict[str, set[str]] = {}

    for system in systems:
        sid = system["system_id"]
        classes = {axis: classify_cell(system["axes"][axis]) for axis in axes}
        for axis, cls in classes.items():
            by_axis[axis][cls] += 1
        direct = {axis for axis, cls in classes.items() if cls == "direct"}
        direct_sets[sid] = direct
        profiles.append(
            {
                "system_id": sid,
                "direct_axes": sorted(direct),
                "partial_axes": sorted(axis for axis, cls in classes.items() if cls == "partial"),
                "missing_axes": sorted(axis for axis, cls in classes.items() if cls == "missing"),
                "n_direct": len(direct),
                "n_partial": sum(cls == "partial" for cls in classes.values()),
                "n_missing": sum(cls == "missing" for cls in classes.values()),
            }
        )

    pair_counts = []
    for a, b in itertools.combinations(axes, 2):
        members = sorted(sid for sid, direct in direct_sets.items() if {a, b}.issubset(direct))
        pair_counts.append({"axes": [a, b], "n_systems": len(members), "systems": members})
    pair_counts.sort(key=lambda row: (-row["n_systems"], row["axes"]))

    triple_counts = []
    for combo in itertools.combinations(axes, 3):
        members = sorted(sid for sid, direct in direct_sets.items() if set(combo).issubset(direct))
        if members:
            triple_counts.append({"axes": list(combo), "n_systems": len(members), "systems": members})
    triple_counts.sort(key=lambda row: (-row["n_systems"], row["axes"]))

    axis_summary = {
        axis: {
            "direct_systems": by_axis[axis]["direct"],
            "partial_systems": by_axis[axis]["partial"],
            "missing_systems": by_axis[axis]["missing"],
        }
        for axis in axes
    }
    direct_backbone = [axis for axis in axes if axis_summary[axis]["direct_systems"] >= 4]

    return {
        "schema_version": "1.1",
        "analysis_type": "evidence_architecture_not_effect_direction",
        "n_systems": len(systems),
        "axis_summary": axis_summary,
        "system_profiles": sorted(profiles, key=lambda row: row["system_id"]),
        "direct_backbone_axes_at_least_four_systems": direct_backbone,
        "top_direct_axis_pairs": pair_counts[:10],
        "top_direct_axis_triples": triple_counts[:10],
        "key_findings": {
            "visual_signal_direct_systems": axis_summary["visual_signal"]["direct_systems"],
            "visual_signal_is_active_but_empirically_empty_in_current_matrix": axis_summary["visual_signal"]["direct_systems"] == 0,
            "pollinator_functional_environment_direct_systems": axis_summary["pollinator_functional_environment"]["direct_systems"],
            "strongest_three_axis_direct_backbone": triple_counts[0] if triple_counts else None,
            "interpretation": "The current matrix supports repeated evidence modules including a pollinator-functional-environment / floral-morphology / interaction-network backbone, but comparable biological directions and propagation states remain a second source-locked layer. Evidence presence alone must not be read as common effect direction.",
        },
        "claim_boundary": "Counts describe source-locked/direct evidence coverage only. They are not independent effect counts, do not imply common response direction, and do not license pooling noncommensurate estimands.",
    }


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    source = root / "data" / "design" / "island_system_response_axis_matrix.json"
    output = root / "data" / "results" / "island_response_evidence_architecture.json"
    matrix = json.loads(source.read_text(encoding="utf-8"))
    result = analyze(matrix)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
