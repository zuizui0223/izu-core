from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave4 import build_strengthening_audit as build_wave4_audit

ROOT = Path(__file__).resolve().parents[1]
THIRD_WAVE = ROOT / "data/design/chapter2_systematic_third_wave_search_gate_20260903.csv"
WAVE5 = ROOT / "data/design/chapter2_systematic_source_strengthening_wave5_20260904.csv"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave5_audit_20260904.json"

EXPECTED_TARGETS = {
    "Crete",
    "Philippines",
    "Trinidad and Tobago",
    "Iceland",
    "ABC Islands",
    "Bermuda",
    "Christmas Island",
}
CLEARED_TARGETS = {"Crete", "Philippines", "Trinidad and Tobago", "Iceland"}
OPEN_TARGETS = EXPECTED_TARGETS - CLEARED_TARGETS


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_strengthening_audit() -> dict:
    base = build_wave4_audit()
    third = _read_rows(THIRD_WAVE)
    rows = _read_rows(WAVE5)

    if base["source_work_state_after_wave4"]["targets_requiring_additional_source_work"] != 38:
        raise RuntimeError("wave 5 must start from the 38-target post-wave-4 source-work state")
    if len(rows) != len(EXPECTED_TARGETS):
        raise RuntimeError(f"source-strengthening wave 5 changed: expected {len(EXPECTED_TARGETS)} rows, got {len(rows)}")

    ids = [row["strengthening_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate source-strengthening wave-5 IDs")
    targets = [row["geographic_target"] for row in rows]
    if len(targets) != len(set(targets)) or set(targets) != EXPECTED_TARGETS:
        raise RuntimeError(f"unexpected wave-5 target set: {sorted(set(targets))}")
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
        if row["global_confrontation_candidate_after"].lower() != "true":
            raise RuntimeError(f"{target} should remain a breadth candidate")
        if row["dedup_decision"] != "eligible_new_group":
            raise RuntimeError(f"{target} should be marked as an eligible new geographic group")

    abc = by_target["ABC Islands"]
    if abc["further_source_work_after"].lower() != "true":
        raise RuntimeError("ABC Islands must remain open because direct evidence is Curacao-specific")
    if abc["global_confrontation_candidate_after"].lower() != "true":
        raise RuntimeError("ABC Islands should remain a breadth candidate with an explicit subtarget limit")
    if abc["dedup_decision"] != "eligible_new_group_with_subtarget_limit":
        raise RuntimeError("ABC Islands must preserve its subtarget-limited candidate status")

    for target in {"Bermuda", "Christmas Island"}:
        row = by_target[target]
        if row["further_source_work_after"].lower() != "true":
            raise RuntimeError(f"{target} should remain open for source work")
        if row["global_confrontation_candidate_after"].lower() != "false":
            raise RuntimeError(f"{target} must not be promoted without direct local process evidence")

    if by_target["Crete"]["source_reference"] != "10.1006/bijl.1996.0119":
        raise RuntimeError("Crete must retain the Cyclamen creticum controlled-pollination anchor")
    if by_target["Trinidad and Tobago"]["source_reference"] != "10.2307/1938966":
        raise RuntimeError("Trinidad and Tobago must retain the direct two-island hummingbird-pollination anchor")
    if "1523-0430" not in by_target["Iceland"]["source_reference"]:
        raise RuntimeError("Iceland must retain the Campanula uniflora breeding-system anchor")
    if "10.1007/s11284-010-0799-7" not in abc["source_reference"]:
        raise RuntimeError("ABC Islands must retain the Curacao cactus-pollination anchor")

    cleared = sorted(target for target in targets if by_target[target]["further_source_work_after"].lower() == "false")
    unresolved = sorted(target for target in targets if by_target[target]["further_source_work_after"].lower() == "true")
    candidates = sorted(target for target in targets if by_target[target]["global_confrontation_candidate_after"].lower() == "true")
    cleared_candidates = sorted(target for target in cleared if by_target[target]["global_confrontation_candidate_after"].lower() == "true")
    decision_counts = Counter(row["dedup_decision"] for row in rows)
    verification_counts = Counter(row["source_verification"] for row in rows)
    remaining = base["source_work_state_after_wave4"]["targets_requiring_additional_source_work"] - len(cleared)

    return {
        "schema_version": "1.0",
        "status": "systematic_source_strengthening_wave5",
        "effective_search_targets": base["effective_search_targets"],
        "first_pass_search_complete": base["first_pass_search_complete"],
        "starting_source_work_targets": base["source_work_state_after_wave4"]["targets_requiring_additional_source_work"],
        "wave5": {
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
        "source_work_state_after_wave5": {
            "targets_requiring_additional_source_work": remaining,
            "resolved_targets": cleared,
            "open_targets": unresolved,
            "abc_scope_state": "curacao_direct_broad_abc_incomplete",
            "bermuda_source_state": "self_seeding_claim_without_controlled_reproductive_experiment",
            "christmas_source_state": "pollinarium_morphology_without_local_pollination_observation",
        },
        "full_contract_result": {
            "systematic_extension_creates_full_contract": False,
            "source_strengthening_wave5_passes": 0,
        },
        "claim_boundary": (
            "Source strengthening resolves direct reproductive or pollination evidence for Crete, the Philippines, Trinidad and Tobago, "
            "and Iceland, but does not alter the frozen 25-entry identifiability audit, the current 36-entry descriptive confrontation, "
            "or formal prediction readiness. Curacao evidence is not generalized to the entire ABC archipelago; Bermuda and Christmas "
            "Island remain open because direct local process evidence is still insufficient."
        ),
    }


def write_strengthening_audit(output: Path = DEFAULT_OUTPUT) -> Path:
    payload = build_strengthening_audit()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_strengthening_audit())
