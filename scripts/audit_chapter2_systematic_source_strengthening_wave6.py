from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave5 import build_strengthening_audit as build_wave5_audit

ROOT = Path(__file__).resolve().parents[1]
SECOND_WAVE = ROOT / "data/design/chapter2_systematic_second_wave_search_gate_20260903.csv"
THIRD_WAVE = ROOT / "data/design/chapter2_systematic_third_wave_search_gate_20260903.csv"
WAVE6 = ROOT / "data/design/chapter2_systematic_source_strengthening_wave6_20260904.csv"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave6_audit_20260904.json"

EXPECTED_TARGETS = {
    "Saint Vincent and the Grenadines",
    "Faroe Islands",
    "Turks and Caicos",
    "Norfolk Island",
    "Cayman Islands",
    "Dalmatian Islands",
    "Bioko",
}
CLEARED_TARGETS = {"Saint Vincent and the Grenadines", "Faroe Islands"}
OPEN_TARGETS = EXPECTED_TARGETS - CLEARED_TARGETS


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_strengthening_audit() -> dict:
    base = build_wave5_audit()
    second = _read_rows(SECOND_WAVE)
    third = _read_rows(THIRD_WAVE)
    rows = _read_rows(WAVE6)

    if base["source_work_state_after_wave5"]["targets_requiring_additional_source_work"] != 34:
        raise RuntimeError("wave 6 must start from the 34-target post-wave-5 source-work state")
    if len(rows) != len(EXPECTED_TARGETS):
        raise RuntimeError(f"source-strengthening wave 6 changed: expected {len(EXPECTED_TARGETS)} rows, got {len(rows)}")

    ids = [row["strengthening_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate source-strengthening wave-6 IDs")
    targets = [row["geographic_target"] for row in rows]
    if len(targets) != len(set(targets)) or set(targets) != EXPECTED_TARGETS:
        raise RuntimeError(f"unexpected wave-6 target set: {sorted(set(targets))}")
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
        if by_target[target]["further_source_work_after"].lower() != "false":
            raise RuntimeError(f"{target} should be cleared from source work")
    for target in OPEN_TARGETS:
        if by_target[target]["further_source_work_after"].lower() != "true":
            raise RuntimeError(f"{target} should remain open for source work")

    st_vincent = by_target["Saint Vincent and the Grenadines"]
    if st_vincent["source_reference"] != "10.1017/S0021859600088055":
        raise RuntimeError("St Vincent must retain the direct passionfruit bagging-experiment anchor")
    if st_vincent["global_confrontation_candidate_after"].lower() != "false":
        raise RuntimeError("St Vincent crop evidence should not be promoted as a new manuscript breadth candidate")
    if st_vincent["dedup_decision"] != "retain_direct_crop_pollination_record_existing_caribbean_layer":
        raise RuntimeError("St Vincent must preserve crop and existing-Caribbean boundaries")

    faroe = by_target["Faroe Islands"]
    if "Hagerup O. 1951" not in faroe["source_reference"]:
        raise RuntimeError("Faroe must retain the Hagerup 1951 primary-monograph anchor")
    if faroe["global_confrontation_candidate_after"].lower() != "true":
        raise RuntimeError("Faroe should remain a historical breadth candidate")
    if faroe["dedup_decision"] != "eligible_new_group_historical_primary_with_mechanism_caveat":
        raise RuntimeError("Faroe must preserve the historical-mechanism caveat")

    turks = by_target["Turks and Caicos"]
    if turks["source_reference"] != "10.1017/S0030605311000251":
        raise RuntimeError("Turks and Caicos must retain the primary source explicitly documenting unknown pollination")
    if turks["dedup_decision"] != "hold_direct_pollination_unrecovered":
        raise RuntimeError("Turks and Caicos must remain a direct-pollination gap")

    norfolk = by_target["Norfolk Island"]
    if norfolk["source_verification"] != "authoritative_taxonomic_sex_system_resolved_pollination_mechanism_unresolved":
        raise RuntimeError("Norfolk must resolve the sex-system discrepancy without claiming pollination mechanism")
    if norfolk["dedup_decision"] != "hold_pollination_mechanism_unresolved":
        raise RuntimeError("Norfolk must remain open for pollination mechanism")

    cayman = by_target["Cayman Islands"]
    if cayman["dedup_decision"] != "hold_local_pollination_directness":
        raise RuntimeError("Cayman must remain on local-directness hold")

    cleared = sorted(target for target in targets if by_target[target]["further_source_work_after"].lower() == "false")
    unresolved = sorted(target for target in targets if by_target[target]["further_source_work_after"].lower() == "true")
    candidates = sorted(target for target in targets if by_target[target]["global_confrontation_candidate_after"].lower() == "true")
    cleared_candidates = sorted(target for target in cleared if by_target[target]["global_confrontation_candidate_after"].lower() == "true")
    decision_counts = Counter(row["dedup_decision"] for row in rows)
    verification_counts = Counter(row["source_verification"] for row in rows)
    remaining = base["source_work_state_after_wave5"]["targets_requiring_additional_source_work"] - len(cleared)

    return {
        "schema_version": "1.0",
        "status": "systematic_source_strengthening_wave6",
        "effective_search_targets": base["effective_search_targets"],
        "first_pass_search_complete": base["first_pass_search_complete"],
        "starting_source_work_targets": base["source_work_state_after_wave5"]["targets_requiring_additional_source_work"],
        "wave6": {
            "reviewed_targets": len(rows),
            "target_names": sorted(targets),
            "cleared_from_source_work": len(cleared),
            "cleared_target_names": cleared,
            "remain_open_after_review": len(unresolved),
            "open_target_names": unresolved,
            "global_confrontation_candidates_after_review": len(candidates),
            "candidate_target_names": candidates,
            "cleared_candidates": len(cleared_candidates),
            "cleared_candidate_names": cleared_candidates,
            "decision_counts": dict(sorted(decision_counts.items())),
            "source_verification_counts": dict(sorted(verification_counts.items())),
            "full_chapter2_contract_passes": 0,
        },
        "source_work_state_after_wave6": {
            "targets_requiring_additional_source_work": remaining,
            "resolved_targets": cleared,
            "open_targets": unresolved,
            "norfolk_source_state": "taxonomic_sex_system_resolved_pollination_mechanism_unresolved",
            "faroe_source_state": "historical_primary_pollination_monograph_with_later_mechanism_caveat",
            "turks_source_state": "primary_article_explicitly_reports_pollination_unknown",
            "cayman_source_state": "association_and_candidate_pollinators_without_direct_local_plant_pollination",
        },
        "full_contract_result": {
            "systematic_extension_creates_full_contract": False,
            "source_strengthening_wave6_passes": 0,
        },
        "claim_boundary": (
            "Source strengthening clears St Vincent as a direct crop-pollination record and the Faroe Islands as historical "
            "primary pollination evidence, while keeping later mechanism caveats explicit. It does not alter the frozen 25-entry "
            "identifiability audit, the current 36-entry descriptive confrontation, or formal prediction readiness. Turks and "
            "Caicos, Norfolk, Cayman, Dalmatian Islands and Bioko remain open source/process gaps."
        ),
    }


def write_strengthening_audit(output: Path = DEFAULT_OUTPUT) -> Path:
    payload = build_strengthening_audit()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_strengthening_audit())
