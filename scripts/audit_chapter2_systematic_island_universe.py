from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIVERSE = ROOT / "data/design/chapter2_systematic_island_universe_v1_20260903.csv"
FIRST_WAVE_GATE = ROOT / "data/design/chapter2_systematic_first_wave_source_gate_20260903.csv"
FIRST_WAVE_DEDUP = ROOT / "data/design/chapter2_systematic_first_wave_dedup_review_20260903.csv"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_systematic_island_universe_audit_v1_20260903.json"

ALLOWED_STATUS = {
    "source_verified_current",
    "source_gated_current",
    "umbrella_source_verified",
    "umbrella_source_covered",
    "umbrella_network_indexed",
    "source_found_needs_ledger_gate",
    "nested_target_needs_specific_gate",
    "target_not_yet_source_gated",
}

RESOLVED_OR_INDEXED = {
    "source_verified_current",
    "source_gated_current",
    "umbrella_source_verified",
    "umbrella_source_covered",
    "umbrella_network_indexed",
}


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_audit() -> dict:
    rows = _read_rows(UNIVERSE)
    gates = _read_rows(FIRST_WAVE_GATE)
    dedup = _read_rows(FIRST_WAVE_DEDUP)
    if len(rows) != 110:
        raise RuntimeError(f"systematic island universe changed: expected 110 rows, got {len(rows)}")
    if len(gates) != 7:
        raise RuntimeError(f"first-wave source gate changed: expected 7 rows, got {len(gates)}")
    if len(dedup) != 7:
        raise RuntimeError(f"first-wave dedup review changed: expected 7 rows, got {len(dedup)}")

    keys = [(row["macroregion"], row["geographic_target"]) for row in rows]
    if len(keys) != len(set(keys)):
        raise RuntimeError("duplicate macroregion + geographic_target rows in systematic island universe")

    statuses = {row["coverage_status"] for row in rows}
    unknown = statuses - ALLOWED_STATUS
    if unknown:
        raise RuntimeError(f"unknown coverage statuses: {sorted(unknown)}")

    if any(not row["seed_source"].strip() for row in rows):
        raise RuntimeError("every target must carry a seed source or explicit systematic-target marker")
    if any(row["full_chapter2_contract"] != "fail" for row in gates):
        raise RuntimeError("first-wave source gates must not silently create a full Chapter 2 contract")

    target_names = {row["geographic_target"] for row in rows}
    gate_targets = [row["geographic_target"] for row in gates]
    if len(gate_targets) != len(set(gate_targets)):
        raise RuntimeError("duplicate first-wave geographic targets")
    missing_gate_targets = sorted(set(gate_targets) - target_names)
    if missing_gate_targets:
        raise RuntimeError(f"first-wave targets missing from systematic universe: {missing_gate_targets}")

    gate_ids = {row["gate_id"] for row in gates}
    dedup_ids = {row["gate_id"] for row in dedup}
    if gate_ids != dedup_ids:
        raise RuntimeError("first-wave source gate and dedup review IDs do not match")

    gate_decisions = Counter(row["global_confrontation_admission"] for row in gates)
    if set(gate_decisions) != {
        "eligible_for_breadth_after_dedup_review",
        "retain_search_record_not_confrontation",
    }:
        raise RuntimeError(f"unexpected first-wave admission decisions: {sorted(gate_decisions)}")

    promotion_decisions = Counter(row["promotion_decision"] for row in dedup)
    expected_promotions = {
        "eligible_new_group",
        "eligible_shared_new_group",
        "eligible_existing_group",
        "do_not_promote",
    }
    if set(promotion_decisions) != expected_promotions:
        raise RuntimeError(f"unexpected first-wave promotion decisions: {sorted(promotion_decisions)}")

    status_counts = Counter(row["coverage_status"] for row in rows)
    region_counts = Counter(row["macroregion"] for row in rows)
    priority_counts = Counter(row["search_priority"] for row in rows)
    base_resolved = sum(row["coverage_status"] in RESOLVED_OR_INDEXED for row in rows)

    unresolved_gate_targets = {
        row["geographic_target"]
        for row in rows
        if row["coverage_status"] not in RESOLVED_OR_INDEXED and row["geographic_target"] in set(gate_targets)
    }
    resolved_after_first_wave = base_resolved + len(unresolved_gate_targets)

    gated_from_not_yet = sum(
        row["coverage_status"] == "target_not_yet_source_gated" and row["geographic_target"] in unresolved_gate_targets
        for row in rows
    )
    gated_from_source_found = sum(
        row["coverage_status"] == "source_found_needs_ledger_gate" and row["geographic_target"] in unresolved_gate_targets
        for row in rows
    )

    eligible_dedup_rows = [row for row in dedup if row["promotion_decision"] != "do_not_promote"]
    candidate_groups = {row["proposed_higher_level_group"] for row in eligible_dedup_rows}
    candidate_new_groups = {
        row["proposed_higher_level_group"]
        for row in eligible_dedup_rows
        if row["overlap_with_current36"].lower() == "false"
    }

    return {
        "schema_version": "1.2",
        "status": "systematic_search_universe_v1_with_first_wave_source_and_dedup_gate",
        "scope": (
            "Named archipelagos, island groups and selected large/sentinel islands relevant to terrestrial "
            "flowering-plant pollination, breeding systems, reproductive assurance or plant-pollinator networks. "
            "This is a reproducible search universe, not a claim that 110 is the number of island systems on Earth."
        ),
        "target_rows": len(rows),
        "macroregions": len(region_counts),
        "macroregion_counts": dict(sorted(region_counts.items())),
        "seed_coverage_status_counts": dict(sorted(status_counts.items())),
        "priority_counts": dict(sorted(priority_counts.items())),
        "first_wave_source_gate": {
            "gated_targets": len(gates),
            "eligible_for_breadth_after_dedup_review": gate_decisions["eligible_for_breadth_after_dedup_review"],
            "retain_search_record_not_confrontation": gate_decisions["retain_search_record_not_confrontation"],
            "full_chapter2_contract_passes": 0,
            "newly_source_resolved_targets": len(unresolved_gate_targets),
        },
        "first_wave_dedup_review": {
            "rows": len(dedup),
            "eligible_research_entries": len(eligible_dedup_rows),
            "eligible_higher_level_groups": len(candidate_groups),
            "potential_new_higher_level_groups_relative_to_current36": len(candidate_new_groups),
            "promotion_decision_counts": dict(sorted(promotion_decisions.items())),
            "current36_changed_by_this_audit": False,
        },
        "resolved_or_umbrella_indexed_targets_after_first_wave": resolved_after_first_wave,
        "targets_requiring_further_source_work_after_first_wave": len(rows) - resolved_after_first_wave,
        "directly_not_yet_source_gated_after_first_wave": status_counts["target_not_yet_source_gated"] - gated_from_not_yet,
        "source_found_needing_ledger_gate_after_first_wave": status_counts["source_found_needs_ledger_gate"] - gated_from_source_found,
        "nested_targets_needing_specific_gate": status_counts["nested_target_needs_specific_gate"],
        "claim_boundary": (
            "Do not add these 110 targets to the frozen 25-entry identifiability denominator or the current "
            "36-entry descriptive confrontation. First-wave eligibility is not promotion. Even after de-duplication, "
            "the current 36 changes only in a separate promotion step after explicit manuscript-value review."
        ),
    }


def write_audit(output: Path = DEFAULT_OUTPUT) -> Path:
    payload = build_audit()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_audit())
