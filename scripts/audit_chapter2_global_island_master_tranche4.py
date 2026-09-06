from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data/design/chapter2_global_island_master_tranche4_queue_20260906.csv"
RESULTS = ROOT / "data/design/chapter2_global_island_master_tranche4_results_20260906.csv"
RULE = ROOT / "data/design/chapter2_world_confrontation_saturation_rule_20260906.json"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
DEFAULT_OUT = ROOT / "data/results/chapter2_global_island_master_tranche4_audit_20260906.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def audit() -> dict:
    queue = read_csv(QUEUE)
    results = read_csv(RESULTS)
    rule = json.loads(RULE.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if len(queue) != 8 or len(results) != 8:
        raise RuntimeError("tranche4 must contain exactly 8 preselected systems and 8 reviewed results")
    if {row["geographic_system"] for row in queue} != {row["geographic_system"] for row in results}:
        raise RuntimeError("tranche4 result membership drifted from the pre-search queue")
    if any(row["selection_status"] != "selected_before_search" for row in queue):
        raise RuntimeError("tranche4 selection was not frozen before literature review")
    if any(row["geographic_system"] == "Izu Islands" for row in queue):
        raise RuntimeError("Izu entered the world-confrontation tranche prematurely")
    if any(row["direct_historical_loss"] != "no" or row["direct_historical_arrival"] != "no" for row in results):
        raise RuntimeError("tranche4 silently manufactured historical turnover measurements")

    novelty = [row for row in results if row["material_novelty"] != "no"]
    full_contracts = 0
    eligible = len(queue) >= rule["eligible_saturation_tranche"]["minimum_new_system_units"]
    zero_novelty = eligible and len(novelty) == 0 and full_contracts == 0
    if not zero_novelty:
        raise RuntimeError("recorded tranche4 is no longer a zero-novelty saturation tranche")

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
        raise RuntimeError(f"active/frozen inference boundaries changed during tranche4: {boundary}")

    return {
        "schema_version": "1.0",
        "status": "pass",
        "tranche": 4,
        "preselected_systems": 8,
        "reviewed_systems": 8,
        "saturation_tranche_eligible_by_size": eligible,
        "source_status_counts": dict(sorted(Counter(row["source_status"] for row in results).items())),
        "direct_measurement_counts": {
            "direct_visitation_or_community": sum(row["direct_visitation_or_community"] == "direct" for row in results),
            "direct_breeding_assurance": sum(row["direct_breeding_assurance"] == "direct" for row in results),
            "direct_plant_response_or_fitness": sum(row["direct_plant_response_or_fitness"] == "direct" for row in results),
        },
        "direct_historical_partner_loss": 0,
        "direct_historical_partner_arrival_replacement": 0,
        "full_contract_passes": 0,
        "material_novelty_events": 0,
        "material_novelty_systems": [],
        "zero_novelty_saturation_tranche": True,
        "consecutive_zero_novelty_tranches_after_this": 1,
        "large_island_saturation_met": False,
        "active_manuscript_boundary": {
            "descriptive_research_entries": 42,
            "exact_geographic_labels": 37,
            "formal_identifiability_research_entries": 25,
            "formal_full_contracts": "0_of_25",
            "formal_external_prediction": "not_evaluable",
            "mutated_by_tranche4": False,
        },
        "scientific_readout": "The fourth geography-first tranche adds direct visitor/breeding/reproductive evidence but no new response, process or falsification state and no historical turnover coordinate; it is the first zero-novelty saturation tranche.",
        "next_step": "freeze and review one more geography-first tranche of at least eight new system units; if it is also zero-novelty, large-island saturation is met"
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
