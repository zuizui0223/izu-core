from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "data/design/chapter2_manuscript_value_promotion_review_20260905.csv"
WAVE11 = ROOT / "data/results/chapter2_systematic_source_strengthening_wave11_audit_20260905.json"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_manuscript_value_promotion_review_audit_20260905.json"

EXPECTED_PROMOTIONS = {
    "wave5_crete",
    "wave5_trinidad_tobago",
    "wave5_iceland",
}


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_audit() -> dict:
    rows = _read_rows(REVIEW)
    wave11 = json.loads(WAVE11.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if len(rows) != 29:
        raise RuntimeError(f"promotion review changed: expected 29 candidates, got {len(rows)}")

    ids = [row["candidate_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("candidate IDs must be unique")
    if any(row["full_chapter2_contract"] != "fail" for row in rows):
        raise RuntimeError("promotion review must not manufacture a full Chapter 2 contract")

    promoted = {row["candidate_id"] for row in rows if row["promotion_decision"] == "promote_next_integration"}
    if promoted != EXPECTED_PROMOTIONS:
        raise RuntimeError(f"unexpected promotion shortlist: {sorted(promoted)}")

    promoted_rows = [row for row in rows if row["candidate_id"] in promoted]
    if any(row["geographic_increment"] != "new_exact_group" for row in promoted_rows):
        raise RuntimeError("promoted candidates must add a clean new exact geographic group")
    if any(row["falsification_value"] != "high" for row in promoted_rows):
        raise RuntimeError("promoted candidates must have high falsification/mechanistic value")
    if any(row["redundancy_risk"] != "low" for row in promoted_rows):
        raise RuntimeError("promoted candidates must have low redundancy risk")

    queue = wave11["source_work_state_after_wave11"]
    if queue["targets_requiring_additional_source_work"] != 0:
        raise RuntimeError("manuscript-value review must start only after the active source-work queue reaches zero")
    if not queue["source_review_complete_under_current_protocol"]:
        raise RuntimeError("systematic source review is not complete")

    breadth = manifest["world_breadth_extension"]
    if breadth["combined_descriptive_research_entries_before_cross_layer_deduplication"] != 39:
        raise RuntimeError("promotion review must not silently mutate active manuscript breadth")
    if breadth["combined_exact_overlap_labels_before_higher_level_archipelago_deduplication"] != 34:
        raise RuntimeError("promotion review must not silently mutate active exact-label breadth")
    if manifest["claim_ceiling"]["formal_external_prediction"] != "not_evaluable":
        raise RuntimeError("formal external prediction gate changed during promotion review")

    decision_counts = Counter(row["promotion_decision"] for row in rows)
    value_counts = Counter(row["falsification_value"] for row in rows)

    return {
        "schema_version": "1.0",
        "status": "manuscript_value_promotion_review_complete",
        "review_precondition": {
            "systematic_search_targets": wave11["effective_search_targets"],
            "source_work_queue": queue["targets_requiring_additional_source_work"],
            "source_review_complete_under_current_protocol": queue["source_review_complete_under_current_protocol"],
        },
        "candidate_review": {
            "reviewed_candidates": len(rows),
            "decision_counts": dict(sorted(decision_counts.items())),
            "falsification_value_counts": dict(sorted(value_counts.items())),
            "promote_next_integration_ids": sorted(promoted),
            "promote_next_integration_targets": [row["geographic_target"] for row in promoted_rows],
            "full_chapter2_contract_passes": 0,
        },
        "active_manuscript_boundary": {
            "source_backed_research_entries_before_integration": 39,
            "exact_geographic_labels_before_integration": 34,
            "changed_by_review_only": False,
            "formal_external_prediction": "not_evaluable",
            "frozen_full_contracts": "0_of_25",
        },
        "promotion_logic": {
            "Crete": "negative control: self-compatible does not equal autonomous reproductive assurance",
            "Trinidad and Tobago": "direct inter-island pollinator-diversity contrast linked to plant pollination biology",
            "Iceland": "distinct Arctic reproductive-assurance state with cleistogamy and predominant inbreeding",
            "held_high_value_cases": [
                "Solomon Islands",
                "Palau",
                "Cook Islands",
            ],
            "held_reason": "Pacific geographic de-duplication and/or provenance must be resolved before count-changing admission",
        },
        "next_step": "integrate the three shortlisted exact-group entries into the post-freeze breadth layer without reopening the frozen 25-entry audit",
        "claim_boundary": (
            "This review ranks source-resolved candidates by marginal manuscript value rather than by source availability alone. "
            "It shortlists Crete, Trinidad and Tobago, and Iceland for the next integration step because each adds a clean exact geography, "
            "high mechanistic or falsification value, and low redundancy. The review itself does not change the active 39-entry / 34-label breadth, "
            "does not alter the frozen 25-entry identifiability audit, and does not reopen formal external prediction."
        ),
    }


def write_audit(output: Path = DEFAULT_OUTPUT) -> Path:
    payload = build_audit()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_audit())
