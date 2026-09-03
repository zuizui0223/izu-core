from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIVERSE = ROOT / "data/design/chapter2_systematic_island_universe_v1_20260903.csv"
FIRST_WAVE_GATE = ROOT / "data/design/chapter2_systematic_first_wave_source_gate_20260903.csv"
FIRST_WAVE_DEDUP = ROOT / "data/design/chapter2_systematic_first_wave_dedup_review_20260903.csv"
SECOND_WAVE_GATE = ROOT / "data/design/chapter2_systematic_second_wave_search_gate_20260903.csv"
SECOND_WAVE_DEDUP = ROOT / "data/design/chapter2_systematic_second_wave_dedup_review_20260903.csv"
SOURCE_NATIVE_CORRECTIONS = ROOT / "data/design/chapter2_systematic_source_native_overlap_corrections_20260903.csv"
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

SECOND_WAVE_OUTCOMES = {
    "source_found_trait_only",
    "initial_search_inconclusive",
    "source_found_direct_exact_subtarget",
    "source_found_direct",
    "source_insufficient_hypothesis_only",
    "source_insufficient_ecology_only",
    "source_found_direct_historical",
    "source_found_authoritative_grey",
    "resolved_by_subtarget_gates",
}

CORRECTION_ACTIONS = {"confirm_current36_coverage", "add_source_native_target"}


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_audit() -> dict:
    rows = _read_rows(UNIVERSE)
    gates = _read_rows(FIRST_WAVE_GATE)
    dedup = _read_rows(FIRST_WAVE_DEDUP)
    second = _read_rows(SECOND_WAVE_GATE)
    second_dedup = _read_rows(SECOND_WAVE_DEDUP)
    corrections = _read_rows(SOURCE_NATIVE_CORRECTIONS)

    if len(rows) != 110:
        raise RuntimeError(f"seed systematic island universe changed: expected 110 rows, got {len(rows)}")
    if len(gates) != 7:
        raise RuntimeError(f"first-wave source gate changed: expected 7 rows, got {len(gates)}")
    if len(dedup) != 7:
        raise RuntimeError(f"first-wave dedup review changed: expected 7 rows, got {len(dedup)}")
    if len(second) != 19:
        raise RuntimeError(f"second-wave search gate changed: expected 19 rows, got {len(second)}")
    if len(second_dedup) != 5:
        raise RuntimeError(f"second-wave dedup review changed: expected 5 rows, got {len(second_dedup)}")
    if len(corrections) != 10:
        raise RuntimeError(f"source-native correction ledger changed: expected 10 rows, got {len(corrections)}")

    keys = [(row["macroregion"], row["geographic_target"]) for row in rows]
    if len(keys) != len(set(keys)):
        raise RuntimeError("duplicate macroregion + geographic_target rows in systematic island universe")

    statuses = {row["coverage_status"] for row in rows}
    unknown = statuses - ALLOWED_STATUS
    if unknown:
        raise RuntimeError(f"unknown coverage statuses: {sorted(unknown)}")
    if any(not row["seed_source"].strip() for row in rows):
        raise RuntimeError("every seed target must carry a seed source or explicit systematic-target marker")
    if any(row["full_chapter2_contract"] != "fail" for row in gates + second):
        raise RuntimeError("systematic source gates must not silently create a full Chapter 2 contract")

    target_names = {row["geographic_target"] for row in rows}
    row_by_target = {row["geographic_target"]: row for row in rows}

    correction_ids = [row["correction_id"] for row in corrections]
    if len(correction_ids) != len(set(correction_ids)):
        raise RuntimeError("duplicate source-native correction IDs")
    correction_actions = {row["action"] for row in corrections}
    if correction_actions - CORRECTION_ACTIONS:
        raise RuntimeError(f"unexpected correction actions: {sorted(correction_actions - CORRECTION_ACTIONS)}")
    added_targets = [row for row in corrections if row["action"] == "add_source_native_target"]
    if len(added_targets) != 1:
        raise RuntimeError("source-native corrections must add exactly one missing target in this audit version")
    if added_targets[0]["geographic_target"] in target_names:
        raise RuntimeError("source-native added target already exists in seed universe")
    confirmed_existing = [row for row in corrections if row["action"] == "confirm_current36_coverage"]
    missing_correction_targets = sorted(row["geographic_target"] for row in confirmed_existing if row["geographic_target"] not in target_names)
    if missing_correction_targets:
        raise RuntimeError(f"source-native correction targets missing from seed universe: {missing_correction_targets}")

    effective_target_names = target_names | {row["geographic_target"] for row in added_targets}
    effective_target_rows = len(effective_target_names)

    gate_targets = [row["geographic_target"] for row in gates]
    second_targets = [row["geographic_target"] for row in second]
    if len(gate_targets) != len(set(gate_targets)):
        raise RuntimeError("duplicate first-wave geographic targets")
    if len(second_targets) != len(set(second_targets)):
        raise RuntimeError("duplicate second-wave geographic targets")
    if set(gate_targets) & set(second_targets):
        raise RuntimeError("first- and second-wave target sets overlap")
    missing_wave_targets = sorted((set(gate_targets) | set(second_targets)) - effective_target_names)
    if missing_wave_targets:
        raise RuntimeError(f"systematic-wave targets missing from effective universe: {missing_wave_targets}")

    gate_ids = {row["gate_id"] for row in gates}
    dedup_ids = {row["gate_id"] for row in dedup}
    if gate_ids != dedup_ids:
        raise RuntimeError("first-wave source gate and dedup review IDs do not match")

    gate_decisions = Counter(row["global_confrontation_admission"] for row in gates)
    if set(gate_decisions) != {"eligible_for_breadth_after_dedup_review", "retain_search_record_not_confrontation"}:
        raise RuntimeError(f"unexpected first-wave admission decisions: {sorted(gate_decisions)}")

    promotion_decisions = Counter(row["promotion_decision"] for row in dedup)
    expected_promotions = {"eligible_new_group", "eligible_shared_new_group", "eligible_existing_group", "do_not_promote"}
    if set(promotion_decisions) != expected_promotions:
        raise RuntimeError(f"unexpected first-wave promotion decisions: {sorted(promotion_decisions)}")

    second_outcomes = Counter(row["search_outcome"] for row in second)
    if set(second_outcomes) - SECOND_WAVE_OUTCOMES:
        raise RuntimeError(f"unexpected second-wave outcomes: {sorted(set(second_outcomes) - SECOND_WAVE_OUTCOMES)}")
    if any(row["further_source_work"].lower() not in {"true", "false"} for row in second):
        raise RuntimeError("second-wave further_source_work must be true/false")
    if any(row["global_confrontation_candidate"].lower() not in {"true", "false"} for row in second):
        raise RuntimeError("second-wave global_confrontation_candidate must be true/false")

    second_candidates = {row["gate_id"] for row in second if row["global_confrontation_candidate"].lower() == "true"}
    second_dedup_ids = {row["gate_id"] for row in second_dedup}
    if second_candidates != second_dedup_ids:
        raise RuntimeError("second-wave dedup rows must exactly match second-wave confrontation candidates")
    second_dedup_decisions = Counter(row["promotion_decision"] for row in second_dedup)
    if set(second_dedup_decisions) != {"eligible_new_group", "eligible_existing_group", "hold_overlap_unresolved"}:
        raise RuntimeError(f"unexpected second-wave dedup decisions: {sorted(second_dedup_decisions)}")

    status_counts = Counter(row["coverage_status"] for row in rows)
    region_counts = Counter(row["macroregion"] for row in rows)
    priority_counts = Counter(row["search_priority"] for row in rows)
    for row in added_targets:
        region_counts[row["macroregion"]] += 1
        priority_counts["covered"] += 1

    base_covered_targets = {row["geographic_target"] for row in rows if row["coverage_status"] in RESOLVED_OR_INDEXED}
    correction_covered_targets = {row["geographic_target"] for row in corrections}
    prior_covered_targets = base_covered_targets | correction_covered_targets

    reviewed_after_first = prior_covered_targets | set(gate_targets)
    reviewed_after_second = reviewed_after_first | set(second_targets)
    if not reviewed_after_second <= effective_target_names:
        raise RuntimeError("reviewed target set escaped effective universe")

    never_reviewed_or_covered_targets = effective_target_names - reviewed_after_second
    target_not_yet_names = {row["geographic_target"] for row in rows if row["coverage_status"] == "target_not_yet_source_gated"}
    source_found_names = {row["geographic_target"] for row in rows if row["coverage_status"] == "source_found_needs_ledger_gate"}
    nested_names = {row["geographic_target"] for row in rows if row["coverage_status"] == "nested_target_needs_specific_gate"}

    directly_not_yet_after_second = target_not_yet_names - reviewed_after_second
    source_found_needing_gate_after_second = source_found_names - reviewed_after_second
    nested_after_second = nested_names - reviewed_after_second

    second_further_work_targets = {row["geographic_target"] for row in second if row["further_source_work"].lower() == "true"}
    additional_source_work_targets = never_reviewed_or_covered_targets | second_further_work_targets

    eligible_dedup_rows = [row for row in dedup if row["promotion_decision"] != "do_not_promote"]
    first_candidate_groups = {row["proposed_higher_level_group"] for row in eligible_dedup_rows}
    first_confirmed_new_groups = {
        row["proposed_higher_level_group"]
        for row in eligible_dedup_rows
        if row["overlap_with_current36"].lower() == "false"
    }

    second_confirmed_new_groups = {
        row["proposed_higher_level_group"] for row in second_dedup if row["promotion_decision"] == "eligible_new_group"
    }
    second_overlap_unresolved = {
        row["proposed_higher_level_group"] for row in second_dedup if row["promotion_decision"] == "hold_overlap_unresolved"
    }

    return {
        "schema_version": "1.4",
        "status": "systematic_search_universe_v1_through_second_wave_with_source_native_overlap_correction",
        "scope": (
            "Named archipelagos, island groups and selected large/sentinel islands relevant to terrestrial flowering-plant "
            "pollination, breeding systems, reproductive assurance or plant-pollinator networks. The effective target count "
            "can increase when source-native multi-archipelago datasets reveal a missing named target. It is not a claim about "
            "the total number of island systems on Earth."
        ),
        "seed_target_rows": len(rows),
        "effective_target_rows_after_source_native_recovery": effective_target_rows,
        "macroregions": len(region_counts),
        "macroregion_counts": dict(sorted(region_counts.items())),
        "seed_coverage_status_counts": dict(sorted(status_counts.items())),
        "effective_priority_counts": dict(sorted(priority_counts.items())),
        "source_native_overlap_corrections": {
            "rows": len(corrections),
            "current36_source_native_targets_confirmed": len(correction_covered_targets),
            "new_search_targets_added": len(added_targets),
            "added_target_names": sorted(row["geographic_target"] for row in added_targets),
            "source_reference": "10.1093/aob/mcaf005",
        },
        "first_wave_source_gate": {
            "gated_targets": len(gates),
            "eligible_for_breadth_after_dedup_review": gate_decisions["eligible_for_breadth_after_dedup_review"],
            "retain_search_record_not_confrontation": gate_decisions["retain_search_record_not_confrontation"],
            "full_chapter2_contract_passes": 0,
        },
        "first_wave_dedup_review": {
            "rows": len(dedup),
            "eligible_research_entries": len(eligible_dedup_rows),
            "eligible_higher_level_groups": len(first_candidate_groups),
            "confirmed_new_higher_level_groups_relative_to_current36": len(first_confirmed_new_groups),
            "promotion_decision_counts": dict(sorted(promotion_decisions.items())),
            "current36_changed_by_this_audit": False,
        },
        "second_wave_search_gate": {
            "reviewed_targets": len(second),
            "search_outcome_counts": dict(sorted(second_outcomes.items())),
            "global_confrontation_candidates_before_dedup": len(second_candidates),
            "candidate_targets_before_dedup": sorted(row["geographic_target"] for row in second if row["global_confrontation_candidate"].lower() == "true"),
            "full_chapter2_contract_passes": 0,
            "targets_requiring_stronger_or_broader_source": len(second_further_work_targets),
        },
        "second_wave_dedup_review": {
            "rows": len(second_dedup),
            "confirmed_new_higher_level_groups": len(second_confirmed_new_groups),
            "confirmed_new_group_names": sorted(second_confirmed_new_groups),
            "existing_current36_groups": second_dedup_decisions["eligible_existing_group"],
            "overlap_unresolved_groups": len(second_overlap_unresolved),
            "overlap_unresolved_group_names": sorted(second_overlap_unresolved),
            "promotion_decision_counts": dict(sorted(second_dedup_decisions.items())),
            "current36_changed_by_this_audit": False,
        },
        "coverage_after_second_wave": {
            "targets_with_documented_search_or_prior_coverage": len(reviewed_after_second),
            "targets_never_yet_directly_reviewed_or_prior_covered": len(never_reviewed_or_covered_targets),
            "targets_requiring_additional_source_work": len(additional_source_work_targets),
            "directly_not_yet_source_gated": len(directly_not_yet_after_second),
            "source_found_needing_ledger_gate": len(source_found_needing_gate_after_second),
            "nested_targets_needing_specific_gate": len(nested_after_second),
        },
        "claim_boundary": (
            "Do not add the effective systematic-search target count to the frozen 25-entry identifiability denominator or "
            "automatically to the current 36-entry descriptive confrontation. A documented search, source gate, breadth "
            "candidacy, or source-native overlap correction is not promotion. Search-inconclusive targets remain coverage "
            "gaps, not biological absences."
        ),
    }


def write_audit(output: Path = DEFAULT_OUTPUT) -> Path:
    payload = build_audit()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_audit())
