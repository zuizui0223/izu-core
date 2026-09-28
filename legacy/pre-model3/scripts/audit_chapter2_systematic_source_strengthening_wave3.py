from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave2 import build_strengthening_audit as build_wave2_audit

ROOT = Path(__file__).resolve().parents[1]
SECOND_WAVE = ROOT / "data/design/chapter2_systematic_second_wave_search_gate_20260903.csv"
THIRD_WAVE = ROOT / "data/design/chapter2_systematic_third_wave_search_gate_20260903.csv"
WAVE3 = ROOT / "data/design/chapter2_systematic_source_strengthening_wave3_20260904.csv"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave3_audit_20260904.json"

EXPECTED_TARGETS = {
    "Comoros and Mayotte",
    "Cayman Islands",
    "Virgin Islands",
    "Guadeloupe",
    "Marquesas Islands",
    "Chatham Islands",
    "Pitcairn Islands",
}
CLEARED_TARGETS = {
    "Virgin Islands",
    "Guadeloupe",
    "Marquesas Islands",
    "Pitcairn Islands",
}
OPEN_TARGETS = EXPECTED_TARGETS - CLEARED_TARGETS


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_strengthening_audit() -> dict:
    base = build_wave2_audit()
    second = _read_rows(SECOND_WAVE)
    third = _read_rows(THIRD_WAVE)
    rows = _read_rows(WAVE3)

    if base["source_work_state_after_wave2"]["targets_requiring_additional_source_work"] != 43:
        raise RuntimeError("wave 3 must start from the 43-target post-wave-2 source-work state")
    if len(rows) != len(EXPECTED_TARGETS):
        raise RuntimeError(f"source-strengthening wave 3 changed: expected {len(EXPECTED_TARGETS)} rows, got {len(rows)}")

    ids = [row["strengthening_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate source-strengthening wave-3 IDs")
    targets = [row["geographic_target"] for row in rows]
    if len(targets) != len(set(targets)) or set(targets) != EXPECTED_TARGETS:
        raise RuntimeError(f"unexpected wave-3 target set: {sorted(set(targets))}")
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

    if by_target["Virgin Islands"]["source_reference"] != "10.1017/S0030605320001234":
        raise RuntimeError("Virgin Islands must be anchored to the Vachellia pollinator-dependency study")
    if by_target["Guadeloupe"]["source_reference"] != "10.5772/64674":
        raise RuntimeError("Guadeloupe must be anchored to the Vanilla autogamy study")
    if by_target["Marquesas Islands"]["source_reference"] != "10.1098/rsbl.2011.0771":
        raise RuntimeError("Marquesas must be anchored to the Glochidion-Epicephala survey")
    if by_target["Pitcairn Islands"]["dedup_decision"] != "retain_direct_search_record_not_promote":
        raise RuntimeError("Pitcairn direct observation must not be auto-promoted")
    if by_target["Comoros and Mayotte"]["dedup_decision"] != "eligible_new_group_with_subtarget_limit":
        raise RuntimeError("Comoros/Mayotte must preserve the subtarget-coverage limit")

    cleared = sorted(target for target in targets if by_target[target]["further_source_work_after"].lower() == "false")
    unresolved = sorted(target for target in targets if by_target[target]["further_source_work_after"].lower() == "true")
    candidates = sorted(target for target in targets if by_target[target]["global_confrontation_candidate_after"].lower() == "true")
    cleared_candidates = sorted(target for target in cleared if by_target[target]["global_confrontation_candidate_after"].lower() == "true")
    decision_counts = Counter(row["dedup_decision"] for row in rows)
    verification_counts = Counter(row["source_verification"] for row in rows)
    remaining = base["source_work_state_after_wave2"]["targets_requiring_additional_source_work"] - len(cleared)

    return {
        "schema_version": "1.0",
        "status": "systematic_source_strengthening_wave3",
        "effective_search_targets": base["effective_search_targets"],
        "first_pass_search_complete": base["first_pass_search_complete"],
        "starting_source_work_targets": base["source_work_state_after_wave2"]["targets_requiring_additional_source_work"],
        "wave3": {
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
        "source_work_state_after_wave3": {
            "targets_requiring_additional_source_work": remaining,
            "resolved_targets": cleared,
            "open_targets": unresolved,
            "comoros_scope_state": "mayotte_direct_broad_comoros_incomplete",
            "cayman_source_state": "pollinator_association_without_direct_local_plant_pollination",
            "chatham_source_state": "geography_covered_process_locality_incomplete",
        },
        "full_contract_result": {
            "systematic_extension_creates_full_contract": False,
            "source_strengthening_wave3_passes": 0,
        },
        "claim_boundary": (
            "Source strengthening changes evidence quality, not the frozen 25-entry identifiability denominator, the current "
            "36-entry descriptive confrontation, or formal prediction readiness. Direct search resolution is distinct from "
            "manuscript promotion: Pitcairn is cleared as a search record but not promoted; Comoros/Mayotte remains open at the "
            "broad-archipelago level despite strong Mayotte evidence."
        ),
    }


def write_strengthening_audit(output: Path = DEFAULT_OUTPUT) -> Path:
    payload = build_strengthening_audit()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_strengthening_audit())
