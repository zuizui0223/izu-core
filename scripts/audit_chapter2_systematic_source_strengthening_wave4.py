from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave3 import build_strengthening_audit as build_wave3_audit

ROOT = Path(__file__).resolve().parents[1]
SECOND_WAVE = ROOT / "data/design/chapter2_systematic_second_wave_search_gate_20260903.csv"
WAVE4 = ROOT / "data/design/chapter2_systematic_source_strengthening_wave4_20260904.csv"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave4_audit_20260904.json"

EXPECTED_TARGETS = {
    "São Tomé and Príncipe",
    "Ascension Island",
    "Tristan da Cunha",
    "Palau",
    "Marshall Islands",
    "Solomon Islands",
    "Tonga",
    "Rapa Nui / Easter Island",
}
CLEARED_TARGETS = {"Rapa Nui / Easter Island"}
OPEN_TARGETS = EXPECTED_TARGETS - CLEARED_TARGETS


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_strengthening_audit() -> dict:
    base = build_wave3_audit()
    second = _read_rows(SECOND_WAVE)
    rows = _read_rows(WAVE4)

    if base["source_work_state_after_wave3"]["targets_requiring_additional_source_work"] != 39:
        raise RuntimeError("wave 4 must start from the 39-target post-wave-3 source-work state")
    if len(rows) != len(EXPECTED_TARGETS):
        raise RuntimeError(f"source-strengthening wave 4 changed: expected {len(EXPECTED_TARGETS)} rows, got {len(rows)}")

    ids = [row["strengthening_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate source-strengthening wave-4 IDs")
    targets = [row["geographic_target"] for row in rows]
    if len(targets) != len(set(targets)) or set(targets) != EXPECTED_TARGETS:
        raise RuntimeError(f"unexpected wave-4 target set: {sorted(set(targets))}")
    if any(row["full_chapter2_contract"] != "fail" for row in rows):
        raise RuntimeError("source strengthening must not silently create a full Chapter 2 contract")
    if any(row["further_source_work_after"].lower() not in {"true", "false"} for row in rows):
        raise RuntimeError("further_source_work_after must be true/false")
    if any(row["global_confrontation_candidate_after"].lower() not in {"true", "false"} for row in rows):
        raise RuntimeError("global_confrontation_candidate_after must be true/false")

    prior_by_id = {row["gate_id"]: row for row in second}
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

    rapa = by_target["Rapa Nui / Easter Island"]
    if "10.1371/journal.pone.0115548" not in rapa["source_reference"]:
        raise RuntimeError("Rapa Nui must retain the verified Sophora toromiro peer-reviewed anchor")
    if rapa["global_confrontation_candidate_after"].lower() != "false":
        raise RuntimeError("Rapa Nui ex-situ breeding-system evidence must not be promoted as an extant island transition")
    if rapa["dedup_decision"] != "retain_breeding_system_record_not_promote":
        raise RuntimeError("Rapa Nui must remain a breeding-system search record only")

    palau = by_target["Palau"]
    if palau["source_reference"] != "10.3897/phytokeys.58.5292":
        raise RuntimeError("Palau must retain the source explicitly documenting the pollination-observation gap")
    if palau["further_source_work_after"].lower() != "true":
        raise RuntimeError("Palau must remain open after source-gap verification")

    cleared = sorted(target for target in targets if by_target[target]["further_source_work_after"].lower() == "false")
    unresolved = sorted(target for target in targets if by_target[target]["further_source_work_after"].lower() == "true")
    candidates = sorted(target for target in targets if by_target[target]["global_confrontation_candidate_after"].lower() == "true")
    decision_counts = Counter(row["dedup_decision"] for row in rows)
    verification_counts = Counter(row["source_verification"] for row in rows)
    remaining = base["source_work_state_after_wave3"]["targets_requiring_additional_source_work"] - len(cleared)

    return {
        "schema_version": "1.0",
        "status": "systematic_source_strengthening_wave4",
        "effective_search_targets": base["effective_search_targets"],
        "first_pass_search_complete": base["first_pass_search_complete"],
        "starting_source_work_targets": base["source_work_state_after_wave3"]["targets_requiring_additional_source_work"],
        "wave4": {
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
        "source_work_state_after_wave4": {
            "targets_requiring_additional_source_work": remaining,
            "resolved_targets": cleared,
            "open_targets": unresolved,
            "rapa_nui_source_state": "ex_situ_self_pollination_and_controlled_breeding_record_not_extant_transition",
            "palau_source_state": "primary_article_explicitly_reports_no_published_pollination_observations",
        },
        "full_contract_result": {
            "systematic_extension_creates_full_contract": False,
            "source_strengthening_wave4_passes": 0,
        },
        "claim_boundary": (
            "Source strengthening can resolve breeding-system evidence without resolving extant island interaction mechanism. "
            "Rapa Nui is cleared only as an ex-situ breeding-system record; São Tomé, Ascension, Tristan, Palau, Marshall, "
            "Solomon and Tonga remain source gaps. The frozen 25-entry audit, current 36-entry confrontation and formal "
            "prediction readiness remain unchanged."
        ),
    }


def write_strengthening_audit(output: Path = DEFAULT_OUTPUT) -> Path:
    payload = build_strengthening_audit()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_strengthening_audit())
