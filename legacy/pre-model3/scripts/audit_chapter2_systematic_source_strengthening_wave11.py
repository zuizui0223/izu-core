from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave10 import build_strengthening_audit as build_wave10_audit

ROOT = Path(__file__).resolve().parents[1]
SECOND_WAVE = ROOT / "data/design/chapter2_systematic_second_wave_search_gate_20260903.csv"
THIRD_WAVE = ROOT / "data/design/chapter2_systematic_third_wave_search_gate_20260903.csv"
WAVE11 = ROOT / "data/design/chapter2_systematic_source_strengthening_wave11_20260905.csv"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_pre_promotion_20260905.json"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave11_audit_20260905.json"

EXPECTED_TARGETS = {
    "São Tomé and Príncipe",
    "Tonga",
    "Cayman Islands",
    "Kiribati / Gilbert Islands",
    "Niue",
    "Wallis and Futuna",
    "Tuvalu",
    "Tokelau",
    "Gambier Islands",
}
EXPECTED_TERMINAL_GAPS = {
    "São Tomé and Príncipe",
    "Tonga",
    "Kiribati / Gilbert Islands",
    "Niue",
    "Tuvalu",
    "Tokelau",
}
EXPECTED_SPECIAL_STATES = {
    "Cayman Islands": "terminal_local_pollinator_association_effectiveness_unrecovered",
    "Wallis and Futuna": "terminal_host_phylogeography_pollinator_pairing_unrecovered",
    "Gambier Islands": "terminal_indirect_local_mutualism_trace",
}
EXPECTED_MANUSCRIPT_ENTRIES = 39
EXPECTED_MANUSCRIPT_LABELS = 34


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_strengthening_audit() -> dict:
    base = build_wave10_audit()
    second = _read_rows(SECOND_WAVE)
    third = _read_rows(THIRD_WAVE)
    rows = _read_rows(WAVE11)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if base["source_work_state_after_wave10"]["targets_requiring_additional_source_work"] != 9:
        raise RuntimeError("wave 11 must start from the 9-target post-wave-10 source-work state")
    if not base["terminal_gap_rule"]["enabled"] or not base["terminal_gap_rule"]["reopen_if_new_source_found"]:
        raise RuntimeError("wave 11 requires the terminal-gap rule and reopen contract")
    if len(rows) != len(EXPECTED_TARGETS):
        raise RuntimeError(f"source-strengthening wave 11 changed: expected {len(EXPECTED_TARGETS)} rows, got {len(rows)}")

    ids = [row["strengthening_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate source-strengthening wave-11 IDs")
    targets = [row["geographic_target"] for row in rows]
    if len(targets) != len(set(targets)) or set(targets) != EXPECTED_TARGETS:
        raise RuntimeError(f"unexpected wave-11 target set: {sorted(set(targets))}")
    if any(row["full_chapter2_contract"] != "fail" for row in rows):
        raise RuntimeError("wave 11 must not silently create a full Chapter 2 contract")
    if any(row["further_source_work_after"].lower() != "false" for row in rows):
        raise RuntimeError("wave 11 completes all remaining active source work")
    if any(row["global_confrontation_candidate_after"].lower() != "false" for row in rows):
        raise RuntimeError("wave 11 terminal completions must not silently add confrontation candidates")

    prior_by_id = {row["gate_id"]: row for row in second + third}
    for row in rows:
        prior = prior_by_id.get(row["prior_gate_id"])
        if prior is None or prior["geographic_target"] != row["geographic_target"]:
            raise RuntimeError(f"source-strengthening prior gate mismatch for {row['geographic_target']}")
        if not row["resolution_class"].startswith("terminal_"):
            raise RuntimeError(f"wave-11 target {row['geographic_target']} must carry a terminal resolution class")
        if not row["dedup_decision"].startswith("terminal_"):
            raise RuntimeError(f"wave-11 target {row['geographic_target']} must carry an explicit terminal decision")

    by_target = {row["geographic_target"]: row for row in rows}
    terminal_gap_targets = {
        row["geographic_target"] for row in rows if row["resolution_class"] == "terminal_source_gap"
    }
    if terminal_gap_targets != EXPECTED_TERMINAL_GAPS:
        raise RuntimeError(f"unexpected final terminal-source-gap set: {sorted(terminal_gap_targets)}")
    for target, expected_state in EXPECTED_SPECIAL_STATES.items():
        if by_target[target]["resolution_class"] != expected_state:
            raise RuntimeError(f"unexpected special terminal state for {target}")

    if by_target["Cayman Islands"]["source_reference"] != "10.11646/zootaxa.3970.1.1; 10.3389/fpls.2021.639368":
        raise RuntimeError("Cayman must retain the regional Zamia-Rhopalotria association anchors")
    if by_target["Wallis and Futuna"]["source_reference"] != "10.1098/rspb.2013.0361":
        raise RuntimeError("Wallis must retain the Glochidion-Epicephala co-radiation anchor")
    if by_target["Gambier Islands"]["source_reference"] != "10.1098/rspb.2013.0361":
        raise RuntimeError("Gambier must retain the Mangareva Phyllanthus-Epicephala anchor")

    resolution_counts = Counter(row["resolution_class"] for row in rows)
    decision_counts = Counter(row["dedup_decision"] for row in rows)
    verification_counts = Counter(row["source_verification"] for row in rows)

    breadth = manifest["world_breadth_extension"]
    manuscript_entries = breadth["combined_descriptive_research_entries_before_cross_layer_deduplication"]
    manuscript_labels = breadth["combined_exact_overlap_labels_before_higher_level_archipelago_deduplication"]
    if manuscript_entries != EXPECTED_MANUSCRIPT_ENTRIES or manuscript_labels != EXPECTED_MANUSCRIPT_LABELS:
        raise RuntimeError(
            f"manuscript-facing breadth moved unexpectedly: expected {EXPECTED_MANUSCRIPT_ENTRIES}/{EXPECTED_MANUSCRIPT_LABELS}, "
            f"got {manuscript_entries}/{manuscript_labels}"
        )
    claims = manifest["claim_ceiling"]
    if claims["formal_external_prediction"] != "not_evaluable" or claims["external_full_contracts"] != "0_of_25":
        raise RuntimeError("frozen prediction/full-contract boundary changed unexpectedly")

    remaining = base["source_work_state_after_wave10"]["targets_requiring_additional_source_work"] - len(rows)
    if remaining != 0:
        raise RuntimeError(f"wave 11 should close the active source-work queue, got {remaining}")

    return {
        "schema_version": "1.0",
        "status": "systematic_source_review_complete_wave11",
        "effective_search_targets": base["effective_search_targets"],
        "first_pass_search_complete": base["first_pass_search_complete"],
        "starting_source_work_targets": base["source_work_state_after_wave10"]["targets_requiring_additional_source_work"],
        "terminal_gap_rule": base["terminal_gap_rule"],
        "wave11": {
            "reviewed_targets": len(rows),
            "target_names": sorted(targets),
            "closed_from_active_source_work": len(rows),
            "terminal_source_gap_targets": len(terminal_gap_targets),
            "terminal_source_gap_names": sorted(terminal_gap_targets),
            "special_terminal_state_targets": len(EXPECTED_SPECIAL_STATES),
            "special_terminal_state_names": sorted(EXPECTED_SPECIAL_STATES),
            "global_confrontation_candidates_after_review": 0,
            "candidate_target_names": [],
            "resolution_class_counts": dict(sorted(resolution_counts.items())),
            "decision_counts": dict(sorted(decision_counts.items())),
            "source_verification_counts": dict(sorted(verification_counts.items())),
            "full_chapter2_contract_passes": 0,
        },
        "source_work_state_after_wave11": {
            "targets_requiring_additional_source_work": 0,
            "source_review_complete_under_current_protocol": True,
            "closed_targets": sorted(targets),
            "terminal_source_gap_targets": sorted(terminal_gap_targets),
            "special_terminal_states": dict(sorted(EXPECTED_SPECIAL_STATES.items())),
            "reopen_if_new_source_found": True,
        },
        "manuscript_boundary": {
            "source_backed_research_entries": manuscript_entries,
            "exact_geographic_labels": manuscript_labels,
            "changed_by_wave11": False,
            "formal_external_prediction": claims["formal_external_prediction"],
            "frozen_full_contracts": claims["external_full_contracts"],
        },
        "full_contract_result": {
            "systematic_extension_creates_full_contract": False,
            "source_strengthening_wave11_passes": 0,
        },
        "claim_boundary": (
            "Wave 11 closes the final nine active source-work targets under the documented terminal-review protocol. "
            "The active source-work queue reaches zero, but terminal source gaps and bounded/indirect evidence states remain "
            "reopenable and are not biological absences or new confrontation cases. The current 111-target search frame is review-complete, "
            "not a census of every island or every possible paper. Manuscript-facing breadth remains 39 research entries / 34 exact labels, "
            "the frozen 25-entry identifiability audit remains unchanged, and formal external prediction remains not_evaluable."
        ),
    }


def write_strengthening_audit(output: Path = DEFAULT_OUTPUT) -> Path:
    payload = build_strengthening_audit()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_strengthening_audit())
