from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "data/design/chapter2_global_master_manuscript_value_review_20260906.csv"
SMALL = ROOT / "data/results/chapter2_small_island_supplement_audit_20260906.json"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
DEFAULT_OUT = ROOT / "data/results/chapter2_global_master_manuscript_value_review_audit_20260906.json"

PROMOTED = {
    "surtsey_honckenya_2014",
    "tiritiri_hihi_2022",
    "gulf_california_cardon",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def audit() -> dict:
    rows = read_csv(REVIEW)
    small = json.loads(SMALL.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if not small["precondition"]["large_island_saturation_met"]:
        raise RuntimeError("manuscript-value review opened before large-island saturation")
    if small["supplement"]["reviewed_systems"] != 8:
        raise RuntimeError("manuscript-value review opened before small-island supplement completion")
    if len(rows) != 13:
        raise RuntimeError(f"expected 13 value-review candidates, observed {len(rows)}")
    ids = [row["candidate_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("candidate_id values must be unique")

    promoted = {row["candidate_id"] for row in rows if row["decision"] == "promote_final_synthesis"}
    if promoted != PROMOTED:
        raise RuntimeError(f"final-synthesis promotion set changed: {sorted(promoted)}")
    if any(row["candidate_id"] in PROMOTED and row["new_response_or_process_state"] in {"", "none"} for row in rows):
        raise RuntimeError("a promoted candidate lacks a distinct process/response role")

    breadth = manifest["world_breadth_extension"]
    claims = manifest["claim_ceiling"]
    boundary = (
        breadth["combined_descriptive_research_entries_before_cross_layer_deduplication"],
        breadth["combined_exact_overlap_labels_before_higher_level_archipelago_deduplication"],
        breadth["formal_identifiability_research_entries"],
        claims["external_full_contracts"],
        claims["formal_external_prediction"],
    )
    if boundary != (42, 37, 25, "0_of_25", "not_evaluable"):
        raise RuntimeError(f"value review silently mutated manuscript boundaries: {boundary}")

    return {
        "schema_version": "1.0",
        "status": "pass",
        "candidate_systems": len(rows),
        "decision_counts": dict(sorted(Counter(row["decision"] for row in rows).items())),
        "promote_final_synthesis_ids": sorted(promoted),
        "promotion_logic": {
            "surtsey_honckenya_2014": "dated empty-island colonization plus persistent breeding-system response",
            "tiritiri_hihi_2022": "direct documented pollinator reintroduction plus direct functional test and compensatory-community result",
            "gulf_california_cardon": "historical/ploidy alternative mechanism that bounds current-pollinator causality",
        },
        "historical_bottleneck": {
            "direct_partner_loss_closed": False,
            "direct_partner_arrival_present_in_small_island_supplement": True,
            "full_source_transition_realization_response_contracts": 0,
            "status": "partially_moved_not_closed",
        },
        "active_manuscript_boundary": {
            "descriptive_research_entries": 42,
            "exact_geographic_labels": 37,
            "formal_identifiability_research_entries": 25,
            "formal_full_contracts": "0_of_25",
            "formal_external_prediction": "not_evaluable",
            "mutated_by_value_review": False,
        },
        "izu_transition_gate": {
            "large_island_saturation_met": True,
            "small_island_supplement_complete": True,
            "separate_manuscript_value_review_complete": True,
            "ready_for_final_izu_mechanistic_zoom": True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    payload = audit()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
