from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from scripts.audit_chapter2_systematic_island_universe_complete import build_complete_audit

ROOT = Path(__file__).resolve().parents[1]
WAVE2 = ROOT / "data/design/chapter2_systematic_source_strengthening_wave2_20260904.csv"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_systematic_source_strengthening_wave2_audit_20260904.json"


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_strengthening_audit() -> dict:
    base = build_complete_audit()
    rows = _read_rows(WAVE2)

    if base["search_completion"]["targets_requiring_additional_source_work"] != 48:
        raise RuntimeError("wave 2 must start from the 48-target post-Andaman source-work state")
    if len(rows) != 2:
        raise RuntimeError(f"source-strengthening wave 2 changed: expected 2 rows, got {len(rows)}")

    ids = [row["strengthening_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate source-strengthening wave-2 IDs")
    targets = [row["geographic_target"] for row in rows]
    if len(targets) != len(set(targets)):
        raise RuntimeError("duplicate source-strengthening wave-2 targets")
    if any(row["full_chapter2_contract"] != "fail" for row in rows):
        raise RuntimeError("source strengthening must not silently create a full Chapter 2 contract")
    if any(row["further_source_work_after"].lower() not in {"true", "false"} for row in rows):
        raise RuntimeError("further_source_work_after must be true/false")
    if any(row["global_confrontation_candidate_after"].lower() not in {"true", "false"} for row in rows):
        raise RuntimeError("global_confrontation_candidate_after must be true/false")

    by_target = {row["geographic_target"]: row for row in rows}
    if set(by_target) != {"Tasmania", "Norfolk Island"}:
        raise RuntimeError("wave 2 must contain the prespecified Tasmania and Norfolk targets")

    tasmania = by_target["Tasmania"]
    if tasmania["source_verification"] != "primary_government_research_report":
        raise RuntimeError("Tasmania must be supported by the direct authored government research report")
    if tasmania["further_source_work_after"].lower() != "false":
        raise RuntimeError("Tasmania should be cleared from source-strengthening work")
    if tasmania["dedup_decision"] != "eligible_new_group":
        raise RuntimeError("Tasmania should be retained as a new geographic breadth candidate")

    norfolk = by_target["Norfolk Island"]
    if norfolk["source_verification"] != "authoritative_sources_conflict_unresolved":
        raise RuntimeError("Norfolk must preserve the unresolved authoritative-source conflict")
    if norfolk["further_source_work_after"].lower() != "true":
        raise RuntimeError("Norfolk source work must remain open")
    if norfolk["dedup_decision"] != "hold_mechanism_conflict":
        raise RuntimeError("Norfolk must remain on mechanism-conflict hold")

    cleared = [row["geographic_target"] for row in rows if row["further_source_work_after"].lower() == "false"]
    unresolved = [row["geographic_target"] for row in rows if row["further_source_work_after"].lower() == "true"]
    candidates = [row["geographic_target"] for row in rows if row["global_confrontation_candidate_after"].lower() == "true"]
    decision_counts = Counter(row["dedup_decision"] for row in rows)

    remaining = base["search_completion"]["targets_requiring_additional_source_work"] - len(cleared)

    return {
        "schema_version": "1.0",
        "status": "systematic_source_strengthening_wave2",
        "effective_search_targets": base["effective_search_targets"],
        "first_pass_search_complete": base["search_completion"]["first_pass_search_complete"],
        "starting_source_work_targets": base["search_completion"]["targets_requiring_additional_source_work"],
        "wave2": {
            "reviewed_targets": len(rows),
            "target_names": sorted(targets),
            "cleared_from_source_work": len(cleared),
            "cleared_target_names": sorted(cleared),
            "remain_open_after_review": len(unresolved),
            "open_target_names": sorted(unresolved),
            "new_global_confrontation_candidates": len(candidates),
            "candidate_target_names": sorted(candidates),
            "decision_counts": dict(sorted(decision_counts.items())),
            "full_chapter2_contract_passes": 0,
        },
        "source_work_state_after_wave2": {
            "targets_requiring_additional_source_work": remaining,
            "tasmania_source_state": "direct_original_field_and_pollination_experiment_in_authoritative_research_report",
            "norfolk_source_state": "authoritative_mechanism_conflict_unresolved",
        },
        "full_contract_result": {
            "systematic_extension_creates_full_contract": False,
            "source_strengthening_wave2_passes": 0,
        },
        "claim_boundary": (
            "Source strengthening changes evidence quality, not the frozen 25-entry identifiability denominator, the current "
            "36-entry descriptive confrontation, or formal prediction readiness. Tasmania is cleared for later breadth-value "
            "review; Norfolk remains unresolved because authoritative sources conflict on reproductive mechanism."
        ),
    }


def write_strengthening_audit(output: Path = DEFAULT_OUTPUT) -> Path:
    payload = build_strengthening_audit()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_strengthening_audit())
