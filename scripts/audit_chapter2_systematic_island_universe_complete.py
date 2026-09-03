from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from scripts.audit_chapter2_systematic_island_universe import RESOLVED_OR_INDEXED, build_audit as build_second_wave_audit

ROOT = Path(__file__).resolve().parents[1]
UNIVERSE = ROOT / "data/design/chapter2_systematic_island_universe_v1_20260903.csv"
FIRST_WAVE_GATE = ROOT / "data/design/chapter2_systematic_first_wave_source_gate_20260903.csv"
SECOND_WAVE_GATE = ROOT / "data/design/chapter2_systematic_second_wave_search_gate_20260903.csv"
THIRD_WAVE_GATE = ROOT / "data/design/chapter2_systematic_third_wave_search_gate_20260903.csv"
THIRD_WAVE_DEDUP = ROOT / "data/design/chapter2_systematic_third_wave_dedup_review_20260903.csv"
SOURCE_NATIVE_CORRECTIONS = ROOT / "data/design/chapter2_systematic_source_native_overlap_corrections_20260903.csv"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_systematic_island_universe_complete_audit_20260903.json"


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_complete_audit() -> dict:
    base = build_second_wave_audit()
    rows = _read_rows(UNIVERSE)
    first = _read_rows(FIRST_WAVE_GATE)
    second = _read_rows(SECOND_WAVE_GATE)
    third = _read_rows(THIRD_WAVE_GATE)
    third_dedup = _read_rows(THIRD_WAVE_DEDUP)
    corrections = _read_rows(SOURCE_NATIVE_CORRECTIONS)

    if len(third) != 42:
        raise RuntimeError(f"third-wave search gate changed: expected 42 rows, got {len(third)}")
    if len(third_dedup) != 7:
        raise RuntimeError(f"third-wave dedup review changed: expected 7 rows, got {len(third_dedup)}")
    if any(row["full_chapter2_contract"] != "fail" for row in third):
        raise RuntimeError("third-wave search must not silently create a full Chapter 2 contract")
    if any(row["further_source_work"].lower() not in {"true", "false"} for row in third):
        raise RuntimeError("third-wave further_source_work must be true/false")
    if any(row["global_confrontation_candidate"].lower() not in {"true", "false"} for row in third):
        raise RuntimeError("third-wave global_confrontation_candidate must be true/false")

    seed_targets = {row["geographic_target"] for row in rows}
    added_targets = {row["geographic_target"] for row in corrections if row["action"] == "add_source_native_target"}
    effective_targets = seed_targets | added_targets
    base_covered = {row["geographic_target"] for row in rows if row["coverage_status"] in RESOLVED_OR_INDEXED}
    correction_covered = {row["geographic_target"] for row in corrections}
    reviewed_before_third = base_covered | correction_covered | {row["geographic_target"] for row in first} | {row["geographic_target"] for row in second}
    expected_third_targets = effective_targets - reviewed_before_third
    third_targets = {row["geographic_target"] for row in third}

    if third_targets != expected_third_targets:
        missing = sorted(expected_third_targets - third_targets)
        extra = sorted(third_targets - expected_third_targets)
        raise RuntimeError(f"third wave must exactly close the remaining search frame; missing={missing}, extra={extra}")

    third_ids = [row["gate_id"] for row in third]
    if len(third_ids) != len(set(third_ids)):
        raise RuntimeError("duplicate third-wave gate IDs")
    third_candidates = {row["gate_id"] for row in third if row["global_confrontation_candidate"].lower() == "true"}
    third_dedup_ids = {row["gate_id"] for row in third_dedup}
    if third_candidates != third_dedup_ids:
        raise RuntimeError("third-wave dedup rows must exactly match third-wave confrontation candidates")

    third_dedup_decisions = Counter(row["promotion_decision"] for row in third_dedup)
    expected_decisions = {"eligible_new_group", "eligible_existing_group", "hold_source_verification"}
    if set(third_dedup_decisions) != expected_decisions:
        raise RuntimeError(f"unexpected third-wave dedup decisions: {sorted(third_dedup_decisions)}")

    third_outcomes = Counter(row["search_outcome"] for row in third)
    third_further_targets = {row["geographic_target"] for row in third if row["further_source_work"].lower() == "true"}
    second_further_targets = {row["geographic_target"] for row in second if row["further_source_work"].lower() == "true"}
    additional_source_work = second_further_targets | third_further_targets

    reviewed_after_third = reviewed_before_third | third_targets
    if reviewed_after_third != effective_targets:
        raise RuntimeError("systematic search frame not fully reviewed after third wave")

    confirmed_new_groups = {
        row["proposed_higher_level_group"] for row in third_dedup if row["promotion_decision"] == "eligible_new_group"
    }
    existing_groups = {
        row["proposed_higher_level_group"] for row in third_dedup if row["promotion_decision"] == "eligible_existing_group"
    }
    held_groups = {
        row["proposed_higher_level_group"] for row in third_dedup if row["promotion_decision"] == "hold_source_verification"
    }

    return {
        "schema_version": "1.0",
        "status": "systematic_search_frame_complete_first_pass",
        "second_wave_audit_schema": base["schema_version"],
        "effective_search_targets": len(effective_targets),
        "macroregions": base["macroregions"],
        "search_completion": {
            "targets_with_documented_search_or_prior_coverage": len(reviewed_after_third),
            "targets_never_reviewed_or_prior_covered": 0,
            "first_pass_search_complete": True,
            "targets_requiring_additional_source_work": len(additional_source_work),
            "directly_not_yet_source_gated": 0,
            "source_found_needing_ledger_gate": 0,
            "nested_targets_needing_specific_gate": 0,
        },
        "third_wave_search_gate": {
            "reviewed_targets": len(third),
            "search_outcome_counts": dict(sorted(third_outcomes.items())),
            "initial_search_inconclusive": third_outcomes["initial_search_inconclusive"],
            "global_confrontation_candidates_before_dedup": len(third_candidates),
            "candidate_targets_before_dedup": sorted(row["geographic_target"] for row in third if row["global_confrontation_candidate"].lower() == "true"),
            "targets_requiring_stronger_or_broader_source": len(third_further_targets),
            "full_chapter2_contract_passes": 0,
        },
        "third_wave_dedup_review": {
            "rows": len(third_dedup),
            "confirmed_new_higher_level_groups": len(confirmed_new_groups),
            "confirmed_new_group_names": sorted(confirmed_new_groups),
            "existing_current36_groups": len(existing_groups),
            "existing_group_names": sorted(existing_groups),
            "held_for_source_verification": len(held_groups),
            "held_group_names": sorted(held_groups),
            "promotion_decision_counts": dict(sorted(third_dedup_decisions.items())),
            "current36_changed_by_this_audit": False,
        },
        "full_contract_result": {
            "first_wave_passes": 0,
            "second_wave_passes": 0,
            "third_wave_passes": 0,
            "systematic_extension_creates_full_contract": False,
        },
        "claim_boundary": (
            "The current 111-target systematic search frame has completed one documented search/coverage pass, but this is not "
            "a census of all islands on Earth and not 111 independent tests. Forty-nine targets still need stronger or broader "
            "sources. The frozen 25-entry identifiability denominator and current 36-entry descriptive confrontation remain unchanged."
        ),
    }


def write_complete_audit(output: Path = DEFAULT_OUTPUT) -> Path:
    payload = build_complete_audit()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_complete_audit())
