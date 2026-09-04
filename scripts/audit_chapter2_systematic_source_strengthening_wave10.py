from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave9 import build_strengthening_audit as build_wave9_audit

ROOT = Path(__file__).resolve().parents[1]
SECOND_WAVE = ROOT / "data/design/chapter2_systematic_second_wave_search_gate_20260903.csv"
THIRD_WAVE = ROOT / "data/design/chapter2_systematic_third_wave_search_gate_20260903.csv"
WAVE10 = ROOT / "data/design/chapter2_systematic_source_strengthening_wave10_20260905.csv"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave10_audit_20260905.json"

EXPECTED_TARGETS = {
    "Ascension Island",
    "Bioko",
    "Chatham Islands",
    "Dalmatian Islands",
    "Marshall Islands",
    "Nauru",
    "Norfolk Island",
    "Selvagens",
    "Tristan da Cunha",
    "Turks and Caicos",
}
EXPECTED_RESOLUTION_COUNTS = {
    "terminal_authoritative_conflict": 1,
    "terminal_geography_covered_process_gap": 1,
    "terminal_primary_source_explicit_unknown": 1,
    "terminal_source_gap": 7,
}
EXPECTED_MANUSCRIPT_ENTRIES = 39
EXPECTED_MANUSCRIPT_LABELS = 34


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_strengthening_audit() -> dict:
    base = build_wave9_audit()
    second = _read_rows(SECOND_WAVE)
    third = _read_rows(THIRD_WAVE)
    rows = _read_rows(WAVE10)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if base["source_work_state_after_wave9"]["targets_requiring_additional_source_work"] != 19:
        raise RuntimeError("wave 10 must start from the 19-target post-wave-9 source-work state")
    if not base["terminal_gap_rule"]["enabled"] or not base["terminal_gap_rule"]["reopen_if_new_source_found"]:
        raise RuntimeError("wave 10 requires the wave-9 terminal-gap rule and reopen contract")
    if len(rows) != len(EXPECTED_TARGETS):
        raise RuntimeError(f"source-strengthening wave 10 changed: expected {len(EXPECTED_TARGETS)} rows, got {len(rows)}")

    ids = [row["strengthening_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate source-strengthening wave-10 IDs")
    targets = [row["geographic_target"] for row in rows]
    if len(targets) != len(set(targets)) or set(targets) != EXPECTED_TARGETS:
        raise RuntimeError(f"unexpected wave-10 target set: {sorted(set(targets))}")
    if any(row["full_chapter2_contract"] != "fail" for row in rows):
        raise RuntimeError("wave 10 must not silently create a full Chapter 2 contract")
    if any(row["further_source_work_after"].lower() != "false" for row in rows):
        raise RuntimeError("wave 10 terminally completes all ten reviewed targets")
    if any(row["global_confrontation_candidate_after"].lower() != "false" for row in rows):
        raise RuntimeError("wave 10 terminal completions must not become confrontation candidates")

    prior_by_id = {row["gate_id"]: row for row in second + third}
    for row in rows:
        prior = prior_by_id.get(row["prior_gate_id"])
        if prior is None or prior["geographic_target"] != row["geographic_target"]:
            raise RuntimeError(f"source-strengthening prior gate mismatch for {row['geographic_target']}")
        if not row["dedup_decision"].startswith("terminal_"):
            raise RuntimeError(f"wave-10 target {row['geographic_target']} must carry an explicit terminal decision")

    by_target = {row["geographic_target"]: row for row in rows}
    if by_target["Turks and Caicos"]["source_reference"] != "10.1017/S0030605311000251":
        raise RuntimeError("Turks and Caicos must retain the primary source explicitly reporting unknown pollination")
    if by_target["Turks and Caicos"]["resolution_class"] != "terminal_primary_source_explicit_unknown":
        raise RuntimeError("Turks and Caicos must close as a primary-study explicit knowledge gap")
    if by_target["Norfolk Island"]["resolution_class"] != "terminal_authoritative_conflict":
        raise RuntimeError("Norfolk must preserve the authoritative mechanism conflict")
    if by_target["Chatham Islands"]["resolution_class"] != "terminal_geography_covered_process_gap":
        raise RuntimeError("Chatham must preserve geography-covered/process-unrecovered separation")

    resolution_counts = Counter(row["resolution_class"] for row in rows)
    if dict(sorted(resolution_counts.items())) != EXPECTED_RESOLUTION_COUNTS:
        raise RuntimeError(f"unexpected wave-10 resolution counts: {dict(sorted(resolution_counts.items()))}")
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

    remaining = base["source_work_state_after_wave9"]["targets_requiring_additional_source_work"] - len(rows)

    return {
        "schema_version": "1.0",
        "status": "systematic_source_strengthening_wave10_terminal_review_completion",
        "effective_search_targets": base["effective_search_targets"],
        "first_pass_search_complete": base["first_pass_search_complete"],
        "starting_source_work_targets": base["source_work_state_after_wave9"]["targets_requiring_additional_source_work"],
        "terminal_gap_rule": base["terminal_gap_rule"],
        "wave10": {
            "reviewed_targets": len(rows),
            "target_names": sorted(targets),
            "closed_from_active_source_work": len(rows),
            "global_confrontation_candidates_after_review": 0,
            "candidate_target_names": [],
            "resolution_class_counts": dict(sorted(resolution_counts.items())),
            "decision_counts": dict(sorted(decision_counts.items())),
            "source_verification_counts": dict(sorted(verification_counts.items())),
            "full_chapter2_contract_passes": 0,
        },
        "source_work_state_after_wave10": {
            "targets_requiring_additional_source_work": remaining,
            "closed_targets": sorted(targets),
            "terminal_source_gap_targets": sorted(
                row["geographic_target"] for row in rows if row["resolution_class"] == "terminal_source_gap"
            ),
            "terminal_special_state_targets": sorted(
                row["geographic_target"] for row in rows if row["resolution_class"] != "terminal_source_gap"
            ),
            "norfolk_source_state": "authoritative_reproductive_wording_conflict_pollination_mechanism_unresolved",
            "turks_source_state": "primary_article_explicitly_reports_pollination_unknown",
            "chatham_source_state": "geography_already_covered_local_pollination_process_unrecovered",
        },
        "manuscript_boundary": {
            "source_backed_research_entries": manuscript_entries,
            "exact_geographic_labels": manuscript_labels,
            "changed_by_wave10": False,
            "formal_external_prediction": claims["formal_external_prediction"],
            "frozen_full_contracts": claims["external_full_contracts"],
        },
        "full_contract_result": {
            "systematic_extension_creates_full_contract": False,
            "source_strengthening_wave10_passes": 0,
        },
        "claim_boundary": (
            "Wave 10 terminally completes ten repeatedly searched targets without converting source gaps, authoritative conflicts, "
            "or an explicit primary-study unknown into biological absence. No wave-10 target becomes a global-confrontation candidate. "
            "The active source-work queue falls from 19 to 9; manuscript-facing breadth remains 39 research entries / 34 exact labels, "
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
