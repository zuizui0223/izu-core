from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave7 import build_strengthening_audit as build_wave7_audit

ROOT = Path(__file__).resolve().parents[1]
SECOND_WAVE = ROOT / "data/design/chapter2_systematic_second_wave_search_gate_20260903.csv"
THIRD_WAVE = ROOT / "data/design/chapter2_systematic_third_wave_search_gate_20260903.csv"
WAVE8 = ROOT / "data/design/chapter2_systematic_source_strengthening_wave8_20260905.csv"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_pre_promotion_20260905.json"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave8_audit_20260905.json"

EXPECTED_TARGETS = {
    "Christmas Island",
    "Solomon Islands",
    "Palau",
    "Comoros and Mayotte",
    "Cayman Islands",
    "Chatham Islands",
    "Norfolk Island",
}
CLEARED_TARGETS = {
    "Christmas Island",
    "Solomon Islands",
    "Palau",
    "Comoros and Mayotte",
}
OPEN_TARGETS = EXPECTED_TARGETS - CLEARED_TARGETS
EXPECTED_MANUSCRIPT_ENTRIES = 39
EXPECTED_MANUSCRIPT_LABELS = 34


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_strengthening_audit() -> dict:
    base = build_wave7_audit()
    second = _read_rows(SECOND_WAVE)
    third = _read_rows(THIRD_WAVE)
    rows = _read_rows(WAVE8)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if base["source_work_state_after_wave7"]["targets_requiring_additional_source_work"] != 30:
        raise RuntimeError("wave 8 must start from the 30-target post-wave-7 source-work state")
    if len(rows) != len(EXPECTED_TARGETS):
        raise RuntimeError(f"source-strengthening wave 8 changed: expected {len(EXPECTED_TARGETS)} rows, got {len(rows)}")

    ids = [row["strengthening_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate source-strengthening wave-8 IDs")
    targets = [row["geographic_target"] for row in rows]
    if len(targets) != len(set(targets)) or set(targets) != EXPECTED_TARGETS:
        raise RuntimeError(f"unexpected wave-8 target set: {sorted(set(targets))}")
    if any(row["full_chapter2_contract"] != "fail" for row in rows):
        raise RuntimeError("source strengthening must not silently create a full Chapter 2 contract")
    if any(row["further_source_work_after"].lower() not in {"true", "false"} for row in rows):
        raise RuntimeError("further_source_work_after must be true/false")
    if any(row["global_confrontation_candidate_after"].lower() not in {"true", "false"} for row in rows):
        raise RuntimeError("global_confrontation_candidate_after must be true/false")

    prior_by_id = {row["gate_id"]: row for row in second + third}
    for row in rows:
        prior = prior_by_id.get(row["prior_gate_id"])
        if prior is None or prior["geographic_target"] != row["geographic_target"]:
            raise RuntimeError(f"source-strengthening prior gate mismatch for {row['geographic_target']}")

    by_target = {row["geographic_target"]: row for row in rows}
    for target in CLEARED_TARGETS:
        row = by_target[target]
        if row["further_source_work_after"].lower() != "false":
            raise RuntimeError(f"{target} should be cleared from source work")
        if row["global_confrontation_candidate_after"].lower() != "true":
            raise RuntimeError(f"{target} should remain a breadth candidate after source strengthening")

    for target in OPEN_TARGETS:
        row = by_target[target]
        if row["further_source_work_after"].lower() != "true":
            raise RuntimeError(f"{target} should remain open for source work")
        if row["global_confrontation_candidate_after"].lower() != "false":
            raise RuntimeError(f"{target} must not be promoted while the local mechanism/source gap remains")

    if by_target["Christmas Island"]["source_reference"] != "10.1186/s40462-022-00315-8":
        raise RuntimeError("Christmas Island must retain the verified flying-fox pollen-vector article")
    if by_target["Solomon Islands"]["source_reference"] != "10.2307/2388592":
        raise RuntimeError("Solomon Islands must retain the direct Heliconia bat-pollination article")
    if by_target["Palau"]["dedup_decision"] != "hold_overlap_unresolved_pacific_multi_system":
        raise RuntimeError("Palau promotion must remain held on unresolved Pacific overlap")
    if by_target["Solomon Islands"]["dedup_decision"] != "hold_overlap_unresolved_pacific_multi_system":
        raise RuntimeError("Solomon promotion must remain held on unresolved Pacific overlap")
    if by_target["Comoros and Mayotte"]["dedup_decision"] != "eligible_new_group_with_effectiveness_caveat":
        raise RuntimeError("Comoros/Mayotte must retain the explicit effectiveness caveat")

    breadth = manifest["world_breadth_extension"]
    manuscript_entries = breadth["combined_descriptive_research_entries_before_cross_layer_deduplication"]
    manuscript_labels = breadth["combined_exact_overlap_labels_before_higher_level_archipelago_deduplication"]
    if manuscript_entries != EXPECTED_MANUSCRIPT_ENTRIES or manuscript_labels != EXPECTED_MANUSCRIPT_LABELS:
        raise RuntimeError(
            f"manuscript-facing breadth moved unexpectedly: expected {EXPECTED_MANUSCRIPT_ENTRIES}/{EXPECTED_MANUSCRIPT_LABELS}, "
            f"got {manuscript_entries}/{manuscript_labels}"
        )
    if manifest["claim_ceiling"]["formal_external_prediction"] != "not_evaluable":
        raise RuntimeError("formal external prediction boundary changed unexpectedly")
    if manifest["claim_ceiling"]["external_full_contracts"] != "0_of_25":
        raise RuntimeError("frozen full-contract boundary changed unexpectedly")

    cleared = sorted(target for target in targets if by_target[target]["further_source_work_after"].lower() == "false")
    unresolved = sorted(target for target in targets if by_target[target]["further_source_work_after"].lower() == "true")
    candidates = sorted(target for target in targets if by_target[target]["global_confrontation_candidate_after"].lower() == "true")
    decision_counts = Counter(row["dedup_decision"] for row in rows)
    verification_counts = Counter(row["source_verification"] for row in rows)
    remaining = base["source_work_state_after_wave7"]["targets_requiring_additional_source_work"] - len(cleared)

    return {
        "schema_version": "1.0",
        "status": "systematic_source_strengthening_wave8",
        "effective_search_targets": base["effective_search_targets"],
        "first_pass_search_complete": base["first_pass_search_complete"],
        "starting_source_work_targets": base["source_work_state_after_wave7"]["targets_requiring_additional_source_work"],
        "wave8": {
            "reviewed_targets": len(rows),
            "target_names": sorted(targets),
            "cleared_from_source_work": len(cleared),
            "cleared_target_names": cleared,
            "remain_open_after_review": len(unresolved),
            "open_target_names": unresolved,
            "global_confrontation_candidates_after_review": len(candidates),
            "candidate_target_names": candidates,
            "decision_counts": dict(sorted(decision_counts.items())),
            "source_verification_counts": dict(sorted(verification_counts.items())),
            "full_chapter2_contract_passes": 0,
        },
        "source_work_state_after_wave8": {
            "targets_requiring_additional_source_work": remaining,
            "resolved_targets": cleared,
            "open_targets": unresolved,
            "christmas_source_state": "direct_source_native_pollen_vector_and_movement_evidence",
            "solomon_source_state": "direct_bat_pollination_plus_self_incompatibility_experiment",
            "palau_source_state": "direct_field_pollinator_observations_reject_simple_lost_pollinator_hypothesis",
            "comoros_source_state": "broad_archipelago_flower_interaction_plus_mayotte_direct_reproduction_effectiveness_unmeasured_broadly",
            "cayman_source_state": "regional_obligate_mutualism_without_cayman_local_pollination_effectiveness",
            "chatham_source_state": "geography_covered_process_locality_unrecovered",
            "norfolk_source_state": "taxonomic_reproductive_wording_conflict_pollination_mechanism_unresolved",
        },
        "manuscript_boundary": {
            "source_backed_research_entries": manuscript_entries,
            "exact_geographic_labels": manuscript_labels,
            "changed_by_wave8": False,
            "formal_external_prediction": manifest["claim_ceiling"]["formal_external_prediction"],
            "frozen_full_contracts": manifest["claim_ceiling"]["external_full_contracts"],
        },
        "full_contract_result": {
            "systematic_extension_creates_full_contract": False,
            "source_strengthening_wave8_passes": 0,
        },
        "claim_boundary": (
            "Wave 8 strengthens source quality without altering the frozen 25-entry identifiability audit or the current "
            "manuscript-facing source-backed breadth of 39 research entries / 34 exact labels. Christmas Island, Solomon Islands, "
            "Palau and Comoros/Mayotte are cleared from source work with their promotion/effectiveness caveats preserved; Cayman, "
            "Chatham and Norfolk remain open. Formal external prediction remains not_evaluable."
        ),
    }


def write_strengthening_audit(output: Path = DEFAULT_OUTPUT) -> Path:
    payload = build_strengthening_audit()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_strengthening_audit())
