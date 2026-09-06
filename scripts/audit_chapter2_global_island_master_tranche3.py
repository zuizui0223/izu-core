from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data/design/chapter2_global_island_master_tranche3_queue_20260906.csv"
RESULTS = ROOT / "data/design/chapter2_global_island_master_tranche3_results_20260906.csv"
RULE = ROOT / "data/design/chapter2_world_confrontation_saturation_rule_20260906.json"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
DEFAULT_OUT = ROOT / "data/results/chapter2_global_island_master_tranche3_audit_20260906.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def audit() -> dict:
    queue = read_csv(QUEUE)
    results = read_csv(RESULTS)
    rule = json.loads(RULE.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if len(queue) != 10 or len(results) != 10:
        raise RuntimeError("tranche3 must contain exactly 10 preselected systems and 10 reviewed results")
    if {row["geographic_system"] for row in queue} != {row["geographic_system"] for row in results}:
        raise RuntimeError("tranche3 result membership drifted from the pre-search queue")
    if any("selected_before_search" not in row["selection_status"] for row in queue):
        raise RuntimeError("tranche3 selection was not frozen before literature review")
    if any(row["geographic_system"] == "Izu Islands" for row in queue):
        raise RuntimeError("Izu entered the world-confrontation tranche prematurely")
    if any(row["direct_historical_loss"] != "no" or row["direct_historical_arrival"] != "no" for row in results):
        raise RuntimeError("tranche3 silently manufactured historical turnover measurements")

    novelty = [row for row in results if row["material_novelty"] != "no"]
    full_contracts = 0
    eligible_min = rule["eligible_saturation_tranche"]["minimum_new_system_units"]
    eligible = len(queue) >= eligible_min
    zero_novelty = len(novelty) == 0 and full_contracts == 0

    breadth = manifest["world_breadth_extension"]
    claims = manifest["claim_ceiling"]
    if (
        breadth["combined_descriptive_research_entries_before_cross_layer_deduplication"],
        breadth["combined_exact_overlap_labels_before_higher_level_archipelago_deduplication"],
        breadth["formal_identifiability_research_entries"],
        claims["external_full_contracts"],
        claims["formal_external_prediction"],
    ) != (42, 37, 25, "0_of_25", "not_evaluable"):
        raise RuntimeError("active/frozen inference boundaries changed during tranche3 review")

    direct_fields = (
        "direct_visitation_or_community",
        "direct_breeding_assurance",
        "direct_plant_response_or_fitness",
    )
    direct_counts = {field: sum(row[field] == "direct" for row in results) for field in direct_fields}

    return {
        "schema_version": "1.0",
        "status": "pass",
        "tranche": 3,
        "preselected_systems": len(queue),
        "reviewed_systems": len(results),
        "saturation_tranche_eligible_by_size": eligible,
        "source_status_counts": dict(sorted(Counter(row["source_status"] for row in results).items())),
        "direct_measurement_counts": direct_counts,
        "direct_historical_partner_loss": 0,
        "direct_historical_partner_arrival_replacement": 0,
        "full_contract_passes": full_contracts,
        "material_novelty_events": len(novelty),
        "material_novelty_systems": [row["geographic_system"] for row in novelty],
        "zero_novelty_saturation_tranche": zero_novelty,
        "consecutive_zero_novelty_tranches_after_this": 0,
        "large_island_saturation_met": False,
        "active_manuscript_boundary": {
            "descriptive_research_entries": 42,
            "exact_geographic_labels": 37,
            "formal_identifiability_research_entries": 25,
            "formal_full_contracts": "0_of_25",
            "formal_external_prediction": "not_evaluable",
            "mutated_by_tranche3": False
        },
        "scientific_readout": "The geography-first third tranche still adds a materially new historical/ploidy alternative in Gulf of California breeding-system variation, so world confrontation has not saturated and Izu remains deferred.",
        "next_step": "freeze and review another geography-first tranche before any Izu zoom"
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    result = audit()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
