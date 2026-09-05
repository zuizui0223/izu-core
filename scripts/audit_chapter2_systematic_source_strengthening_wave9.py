from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from scripts.audit_chapter2_systematic_source_strengthening_wave8 import build_strengthening_audit as build_wave8_audit

ROOT = Path(__file__).resolve().parents[1]
THIRD_WAVE = ROOT / "data/design/chapter2_systematic_third_wave_search_gate_20260903.csv"
WAVE9 = ROOT / "data/design/chapter2_systematic_source_strengthening_wave9_20260905.csv"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave9_audit_20260905.json"

EXPECTED_TARGETS = {
    "ABC Islands",
    "Bermuda",
    "Chagos Archipelago",
    "Cocos (Keeling) Islands",
    "Desventuradas Islands",
    "Lakshadweep",
    "Maldives",
}
EXPECTED_TERMINAL_GAPS = {
    "Bermuda",
    "Chagos Archipelago",
    "Cocos (Keeling) Islands",
    "Desventuradas Islands",
    "Lakshadweep",
}
EXPECTED_CANDIDATES = {"ABC Islands", "Maldives"}
EXPECTED_RESOLUTION_CLASSES = {
    "terminal_partial_subtarget_evidence",
    "terminal_source_gap",
    "direct_source_resolved",
}
EXPECTED_MANUSCRIPT_ENTRIES = 39
EXPECTED_MANUSCRIPT_LABELS = 34


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_strengthening_audit() -> dict:
    base = build_wave8_audit()
    third = _read_rows(THIRD_WAVE)
    rows = _read_rows(WAVE9)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if base["source_work_state_after_wave8"]["targets_requiring_additional_source_work"] != 26:
        raise RuntimeError("wave 9 must start from the 26-target post-wave-8 source-work state")
    if len(rows) != len(EXPECTED_TARGETS):
        raise RuntimeError(f"source-strengthening wave 9 changed: expected {len(EXPECTED_TARGETS)} rows, got {len(rows)}")

    ids = [row["strengthening_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate source-strengthening wave-9 IDs")
    targets = [row["geographic_target"] for row in rows]
    if len(targets) != len(set(targets)) or set(targets) != EXPECTED_TARGETS:
        raise RuntimeError(f"unexpected wave-9 target set: {sorted(set(targets))}")
    if any(row["full_chapter2_contract"] != "fail" for row in rows):
        raise RuntimeError("source strengthening must not silently create a full Chapter 2 contract")
    if any(row["further_source_work_after"].lower() != "false" for row in rows):
        raise RuntimeError("wave 9 closes all seven targets from active source work, whether by evidence or terminal gap")

    resolution_classes = {row["resolution_class"] for row in rows}
    if resolution_classes - EXPECTED_RESOLUTION_CLASSES:
        raise RuntimeError(f"unexpected wave-9 resolution classes: {sorted(resolution_classes - EXPECTED_RESOLUTION_CLASSES)}")

    prior_by_id = {row["gate_id"]: row for row in third}
    for row in rows:
        prior = prior_by_id.get(row["prior_gate_id"])
        if prior is None or prior["geographic_target"] != row["geographic_target"]:
            raise RuntimeError(f"source-strengthening prior gate mismatch for {row['geographic_target']}")

    by_target = {row["geographic_target"]: row for row in rows}
    terminal_gap_targets = {
        row["geographic_target"] for row in rows if row["resolution_class"] == "terminal_source_gap"
    }
    if terminal_gap_targets != EXPECTED_TERMINAL_GAPS:
        raise RuntimeError(f"unexpected terminal source-gap set: {sorted(terminal_gap_targets)}")

    candidates = {
        row["geographic_target"] for row in rows if row["global_confrontation_candidate_after"].lower() == "true"
    }
    if candidates != EXPECTED_CANDIDATES:
        raise RuntimeError(f"unexpected wave-9 candidate set: {sorted(candidates)}")

    if by_target["Maldives"]["source_reference"] != "10.3897/BDJ.10.e85107":
        raise RuntimeError("Maldives must retain the verified multi-island flower-visitor article")
    if by_target["Maldives"]["resolution_class"] != "direct_source_resolved":
        raise RuntimeError("Maldives must resolve through direct source evidence")
    if by_target["ABC Islands"]["resolution_class"] != "terminal_partial_subtarget_evidence":
        raise RuntimeError("ABC must close with an explicit subtarget limit, not broad generalization")
    if by_target["ABC Islands"]["global_confrontation_candidate_after"].lower() != "true":
        raise RuntimeError("ABC should retain the Curaçao-limited breadth candidacy")

    for target in EXPECTED_TERMINAL_GAPS:
        row = by_target[target]
        if row["global_confrontation_candidate_after"].lower() != "false":
            raise RuntimeError(f"terminal source-gap target {target} must not become a confrontation candidate")
        if not row["dedup_decision"].startswith("terminal_"):
            raise RuntimeError(f"terminal source-gap target {target} must carry an explicit terminal decision")

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

    decision_counts = Counter(row["dedup_decision"] for row in rows)
    verification_counts = Counter(row["source_verification"] for row in rows)
    resolution_counts = Counter(row["resolution_class"] for row in rows)
    closed_targets = sorted(targets)
    candidate_names = sorted(candidates)
    remaining = base["source_work_state_after_wave8"]["targets_requiring_additional_source_work"] - len(closed_targets)

    return {
        "schema_version": "1.0",
        "status": "systematic_source_strengthening_wave9_with_terminal_gap_rule",
        "effective_search_targets": base["effective_search_targets"],
        "first_pass_search_complete": base["first_pass_search_complete"],
        "starting_source_work_targets": base["source_work_state_after_wave8"]["targets_requiring_additional_source_work"],
        "terminal_gap_rule": {
            "enabled": True,
            "definition": (
                "After repeated target-specific searches, a geography may leave active source work as a documented terminal source gap "
                "when no qualifying local primary process source is recovered. This is a literature/source state, not evidence of biological absence."
            ),
            "reopen_if_new_source_found": True,
        },
        "wave9": {
            "reviewed_targets": len(rows),
            "target_names": closed_targets,
            "closed_from_active_source_work": len(closed_targets),
            "terminal_source_gap_targets": len(terminal_gap_targets),
            "terminal_source_gap_names": sorted(terminal_gap_targets),
            "direct_or_partial_evidence_resolutions": len(rows) - len(terminal_gap_targets),
            "global_confrontation_candidates_after_review": len(candidates),
            "candidate_target_names": candidate_names,
            "resolution_class_counts": dict(sorted(resolution_counts.items())),
            "decision_counts": dict(sorted(decision_counts.items())),
            "source_verification_counts": dict(sorted(verification_counts.items())),
            "full_chapter2_contract_passes": 0,
        },
        "source_work_state_after_wave9": {
            "targets_requiring_additional_source_work": remaining,
            "closed_targets": closed_targets,
            "maldives_source_state": "direct_multiisland_flower_visitor_assemblage_with_land_use_contrast_effectiveness_unmeasured",
            "abc_source_state": "curacao_direct_bonaire_authoritative_broad_abc_generalization_blocked",
            "terminal_gap_targets": sorted(terminal_gap_targets),
        },
        "manuscript_boundary": {
            "source_backed_research_entries": manuscript_entries,
            "exact_geographic_labels": manuscript_labels,
            "changed_by_wave9": False,
            "formal_external_prediction": manifest["claim_ceiling"]["formal_external_prediction"],
            "frozen_full_contracts": manifest["claim_ceiling"]["external_full_contracts"],
        },
        "full_contract_result": {
            "systematic_extension_creates_full_contract": False,
            "source_strengthening_wave9_passes": 0,
        },
        "claim_boundary": (
            "Wave 9 introduces a terminal source-gap state so exhaustive review can finish without treating unrecovered literature as biological absence. "
            "Seven targets leave active source work, reducing the queue from 26 to 19; only ABC (Curaçao-limited) and Maldives remain breadth candidates. "
            "The frozen 25-entry identifiability audit and manuscript-facing 39-entry / 34-label breadth remain unchanged, and formal prediction remains not_evaluable."
        ),
    }


def write_strengthening_audit(output: Path = DEFAULT_OUTPUT) -> Path:
    payload = build_strengthening_audit()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_strengthening_audit())
