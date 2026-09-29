from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data/design/chapter2_small_island_supplement_queue_20260906.csv"
RESULTS = ROOT / "data/design/chapter2_small_island_supplement_results_20260906.csv"
TRANCHE5 = ROOT / "data/results/chapter2_global_island_master_tranche5_audit_20260906.json"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
DEFAULT_OUT = ROOT / "data/results/chapter2_small_island_supplement_audit_20260906.json"

EXPECTED_SYSTEMS = {
    "Surtsey",
    "Saba",
    "Tromelin",
    "Pitcairn Island",
    "Clipperton Island",
    "Wadjemup / Rottnest Island",
    "Tiritiri Matangi Island",
    "Udo Island",
}
EXPECTED_NOVELTY = {"Surtsey", "Tiritiri Matangi Island"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def audit() -> dict:
    queue = read_csv(QUEUE)
    results = read_csv(RESULTS)
    tranche5 = json.loads(TRANCHE5.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if not tranche5["large_island_saturation_met"]:
        raise RuntimeError("small-island supplement opened before the preregistered large-island saturation condition was met")
    if len(queue) != 8 or len(results) != 8:
        raise RuntimeError("small-island supplement must contain exactly eight preselected and eight reviewed systems")
    if {row["geographic_system"] for row in queue} != EXPECTED_SYSTEMS:
        raise RuntimeError("small-island queue membership changed")
    if {row["geographic_system"] for row in results} != EXPECTED_SYSTEMS:
        raise RuntimeError("small-island results drifted from the pre-search queue")
    if any(row["selection_status"] != "selected_before_pollination_search" for row in queue):
        raise RuntimeError("small-island geography was not frozen before pollination-source review")
    if any(float(row["approx_area_km2"]) >= 20 for row in queue):
        raise RuntimeError("small-island supplement contains a >=20 km2 system")

    novelty = {row["geographic_system"] for row in results if row["material_novelty"] != "no"}
    if novelty != EXPECTED_NOVELTY:
        raise RuntimeError(f"small-island novelty set changed: {sorted(novelty)}")

    direct_arrival = [row for row in results if row["direct_partner_arrival_replacement"] == "direct"]
    partial_arrival = [row for row in results if row["direct_partner_arrival_replacement"] == "partial"]
    direct_loss = [row for row in results if row["direct_partner_loss"] == "direct"]
    full = [row for row in results if row["full_chapter2_contract"] == "pass"]

    if [row["geographic_system"] for row in direct_arrival] != ["Tiritiri Matangi Island"]:
        raise RuntimeError("documented direct partner-arrival state changed")
    if [row["geographic_system"] for row in partial_arrival] != ["Surtsey"]:
        raise RuntimeError("partial historical-arrival state changed")
    if direct_loss:
        raise RuntimeError("small-island supplement unexpectedly contains a direct historical partner-loss trajectory")
    if full:
        raise RuntimeError("small-island supplement unexpectedly closes a full Chapter 2 contract")

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
        raise RuntimeError(f"active/frozen manuscript boundary changed during small-island review: {boundary}")

    evidence_counts = {
        field: sum(row[field] == "direct" for row in results)
        for field in (
            "direct_source_functional_state",
            "direct_partner_loss",
            "direct_partner_arrival_replacement",
            "direct_realized_community_shift",
            "direct_local_filtering",
            "direct_breeding_assurance",
            "direct_plant_response",
        )
    }

    return {
        "schema_version": "1.0",
        "status": "pass",
        "precondition": {
            "large_island_saturation_met": True,
            "large_island_zero_novelty_tranches": 2,
        },
        "supplement": {
            "preselected_systems": len(queue),
            "reviewed_systems": len(results),
            "source_status_counts": dict(sorted(Counter(row["source_status"] for row in results).items())),
            "direct_measurement_counts": evidence_counts,
            "partial_historical_partner_arrival_systems": [row["geographic_system"] for row in partial_arrival],
            "direct_historical_partner_arrival_systems": [row["geographic_system"] for row in direct_arrival],
            "direct_historical_partner_loss_systems": [],
            "material_novelty_systems": sorted(novelty),
            "full_contract_passes": 0,
        },
        "bottleneck_update": {
            "status": "partially_moved_not_closed",
            "before_small_islands": "new geography-first >=20 km2 waves repeatedly recovered current interaction, breeding and plant-response measurements but no direct historical partner arrival/loss coordinate",
            "after_small_islands": "a direct dated partner reintroduction is recovered for Tiritiri Matangi and Surtsey supplies an empty-island colonization history with partially bounded pollinator arrival, but neither system closes the matched source-state -> transition -> realization -> plant-response chain",
            "remaining_missing_link": "direct historical partner turnover linked to a matched pre-transition functional state and post-transition plant response in the same focal system",
            "formal_frozen_25_reopened": False,
        },
        "active_manuscript_boundary": {
            "descriptive_research_entries": 42,
            "exact_geographic_labels": 37,
            "formal_identifiability_research_entries": 25,
            "formal_full_contracts": "0_of_25",
            "formal_external_prediction": "not_evaluable",
            "mutated_by_small_island_supplement": False,
        },
        "next_step": "perform the preregistered manuscript-value review of the geography-first expansion, then move to the final Izu mechanistic-resolution zoom",
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
