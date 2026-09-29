from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave6 import build_strengthening_audit as build_wave6_audit

ROOT = Path(__file__).resolve().parents[1]
THIRD_WAVE = ROOT / "data/design/chapter2_systematic_third_wave_search_gate_20260903.csv"
WAVE7 = ROOT / "data/design/chapter2_systematic_source_strengthening_wave7_20260904.csv"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave7_audit_20260904.json"

EXPECTED_TARGETS = {
    "Austral Islands",
    "Tuamotu Archipelago",
    "Gambier Islands",
    "Wallis and Futuna",
    "Niue",
    "Kiribati / Gilbert Islands",
    "Tuvalu",
}
CLEARED_TARGETS = {"Austral Islands", "Tuamotu Archipelago"}
OPEN_TARGETS = EXPECTED_TARGETS - CLEARED_TARGETS


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_strengthening_audit() -> dict:
    base = build_wave6_audit()
    third = _read_rows(THIRD_WAVE)
    rows = _read_rows(WAVE7)

    if base["source_work_state_after_wave6"]["targets_requiring_additional_source_work"] != 32:
        raise RuntimeError("wave 7 must start from the 32-target post-wave-6 source-work state")
    if len(rows) != len(EXPECTED_TARGETS):
        raise RuntimeError(f"source-strengthening wave 7 changed: expected {len(EXPECTED_TARGETS)} rows, got {len(rows)}")

    ids = [row["strengthening_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate source-strengthening wave-7 IDs")
    targets = [row["geographic_target"] for row in rows]
    if len(targets) != len(set(targets)) or set(targets) != EXPECTED_TARGETS:
        raise RuntimeError(f"unexpected wave-7 target set: {sorted(set(targets))}")
    if any(row["full_chapter2_contract"] != "fail" for row in rows):
        raise RuntimeError("source strengthening must not silently create a full Chapter 2 contract")
    if any(row["further_source_work_after"].lower() not in {"true", "false"} for row in rows):
        raise RuntimeError("further_source_work_after must be true/false")
    if any(row["global_confrontation_candidate_after"].lower() not in {"true", "false"} for row in rows):
        raise RuntimeError("global_confrontation_candidate_after must be true/false")

    prior_by_id = {row["gate_id"]: row for row in third}
    for row in rows:
        prior = prior_by_id.get(row["prior_gate_id"])
        if prior is None or prior["geographic_target"] != row["geographic_target"]:
            raise RuntimeError(f"source-strengthening prior gate mismatch for {row['geographic_target']}")

    by_target = {row["geographic_target"]: row for row in rows}
    for target in CLEARED_TARGETS:
        row = by_target[target]
        if row["further_source_work_after"].lower() != "false":
            raise RuntimeError(f"{target} should be cleared from source work")
        if row["global_confrontation_candidate_after"].lower() != "false":
            raise RuntimeError(f"{target} should not create a new confrontation entry from the same French Polynesia paper")
        if row["dedup_decision"] != "resolve_existing_french_polynesia_source_no_new_entry":
            raise RuntimeError(f"{target} must resolve inside the existing French Polynesia source layer")

    for target in OPEN_TARGETS:
        if by_target[target]["further_source_work_after"].lower() != "true":
            raise RuntimeError(f"{target} should remain open for source work")

    for target in {"Austral Islands", "Tuamotu Archipelago"}:
        if by_target[target]["source_reference"] != "10.1098/rsbl.2011.0771":
            raise RuntimeError(f"{target} must retain the 17-island specialized-mutualist survey anchor")

    gambier = by_target["Gambier Islands"]
    if gambier["source_reference"] != "10.1098/rspb.2013.0361":
        raise RuntimeError("Gambier must retain the southeastern Polynesian co-radiation anchor")
    if gambier["dedup_decision"] != "hold_local_pollination_directness":
        raise RuntimeError("Gambier must remain open on local pollination directness")

    wallis = by_target["Wallis and Futuna"]
    if wallis["source_reference"] != "10.1098/rspb.2013.0361":
        raise RuntimeError("Wallis must retain the co-radiation sampling anchor")
    if wallis["dedup_decision"] != "hold_local_pollination_directness":
        raise RuntimeError("Wallis/Futuna must remain open on local pollination directness")

    cleared = sorted(target for target in targets if by_target[target]["further_source_work_after"].lower() == "false")
    unresolved = sorted(target for target in targets if by_target[target]["further_source_work_after"].lower() == "true")
    candidates = sorted(target for target in targets if by_target[target]["global_confrontation_candidate_after"].lower() == "true")
    decision_counts = Counter(row["dedup_decision"] for row in rows)
    verification_counts = Counter(row["source_verification"] for row in rows)
    remaining = base["source_work_state_after_wave6"]["targets_requiring_additional_source_work"] - len(cleared)

    return {
        "schema_version": "1.0",
        "status": "systematic_source_strengthening_wave7",
        "effective_search_targets": base["effective_search_targets"],
        "first_pass_search_complete": base["first_pass_search_complete"],
        "starting_source_work_targets": base["source_work_state_after_wave6"]["targets_requiring_additional_source_work"],
        "wave7": {
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
        "source_work_state_after_wave7": {
            "targets_requiring_additional_source_work": remaining,
            "resolved_targets": cleared,
            "open_targets": unresolved,
            "austral_source_state": "native_specialized_mutualist_presence_existing_french_polynesia_source",
            "tuamotu_source_state": "native_specialized_mutualist_presence_existing_french_polynesia_source",
            "gambier_source_state": "host_phylogeography_without_explicit_local_pollination_effectiveness",
            "wallis_source_state": "host_sampling_without_explicit_local_pollinator_pair",
        },
        "full_contract_result": {
            "systematic_extension_creates_full_contract": False,
            "source_strengthening_wave7_passes": 0,
        },
        "claim_boundary": (
            "Austral and Tuamotu are cleared using source-native specialized-mutualist evidence already contained in the existing "
            "French Polynesia research layer; they are not split into new research entries. Gambier, Wallis/Futuna, Niue, Kiribati "
            "and Tuvalu remain open. The frozen 25-entry audit, current 36-entry confrontation and formal prediction boundary are unchanged."
        ),
    }


def write_strengthening_audit(output: Path = DEFAULT_OUTPUT) -> Path:
    payload = build_strengthening_audit()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_strengthening_audit())
