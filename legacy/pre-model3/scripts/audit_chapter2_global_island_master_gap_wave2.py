from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WAVE1 = ROOT / "data/design/chapter2_global_island_master_gap_wave1_20260906.csv"
WAVE2 = ROOT / "data/design/chapter2_global_island_master_gap_wave2_20260906.csv"
PRIORITY = ROOT / "data/design/chapter2_global_island_master_priority_systems_20260906.csv"
UNIVERSE = ROOT / "data/design/chapter2_systematic_island_universe_v1_20260903.csv"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
DEFAULT_OUT = ROOT / "data/results/chapter2_global_island_master_gap_wave2_audit_20260906.json"

MASTER_PROVENANCE = {
    "source_repository": "zuizui0223/island",
    "source_commit": "f1462cd1aa76b2703bc2df159996a4ab65510a25",
    "source_path": "legacy/v1/artifacts/data_global_islands/global_islands_over20km2.csv",
    "source_blob": "42f31df81db250ebfe46b35ebce6cb1c52b19fc9",
    "area_threshold_km2": 20,
    "candidate_island_polygons": 4663,
}

EXPECTED_PROMOTION_QUEUE = {
    "channel_islands_nicotiana_2004",
    "chiloe_embothrium_2006",
    "newfoundland_menyanthes_1998",
    "tierra_fuego_fuchsia_1998",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_wave2(row: dict[str, str]) -> dict[str, str]:
    out = dict(row)
    out["source_verification"] = row["source_status"]
    return out


def audit() -> dict:
    wave1 = read_csv(WAVE1)
    wave2 = [normalize_wave2(row) for row in read_csv(WAVE2)]
    priority = read_csv(PRIORITY)
    universe = read_csv(UNIVERSE)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    combined = wave1 + wave2

    if len(wave1) != 8 or len(wave2) != 12 or len(combined) != 20:
        raise RuntimeError("global-master wave sizes changed")
    ids = [row["system_id"] for row in combined]
    if len(ids) != len(set(ids)):
        raise RuntimeError("global-master system IDs must be unique across waves")

    existing_targets = {row["geographic_target"].casefold() for row in universe}
    for row in combined:
        if row["full_chapter2_contract"] != "fail":
            raise RuntimeError(f"unverified full contract in master-gap waves: {row['system_id']}")
        if row["geographic_system"] == "Izu Islands":
            raise RuntimeError("Izu must remain the final focal zoom")
        if row["geographic_system"].casefold() in existing_targets:
            raise RuntimeError(f"master-gap system already appears verbatim in 111 frame: {row['geographic_system']}")

    if len(priority) != 20:
        raise RuntimeError("first master-gap priority tranche must contain 20 systems")
    if any(row["represented_in_111"] != "false" for row in priority):
        raise RuntimeError("priority tranche contains a system marked represented in 111")
    if sum(row["wave_status"] == "searched_wave1" for row in priority) != 8:
        raise RuntimeError("wave1 priority count changed")
    if sum(row["wave_status"] == "searched_wave2" for row in priority) != 12:
        raise RuntimeError("wave2 priority count changed")
    if any(row["wave_status"] == "next_wave" for row in priority):
        raise RuntimeError("first 20-system geography gap tranche is not fully reviewed")

    promotion_queue = {row["system_id"] for row in combined if row["manuscript_value_decision"] == "promote_next_review"}
    if promotion_queue != EXPECTED_PROMOTION_QUEUE:
        raise RuntimeError(f"promotion-review queue changed: {sorted(promotion_queue)}")

    breadth = manifest["world_breadth_extension"]
    claims = manifest["claim_ceiling"]
    expected_boundary = (42, 37, 25, "0_of_25", "not_evaluable")
    observed_boundary = (
        breadth["combined_descriptive_research_entries_before_cross_layer_deduplication"],
        breadth["combined_exact_overlap_labels_before_higher_level_archipelago_deduplication"],
        breadth["formal_identifiability_research_entries"],
        claims["external_full_contracts"],
        claims["formal_external_prediction"],
    )
    if observed_boundary != expected_boundary:
        raise RuntimeError(f"active/frozen manuscript boundary changed: {observed_boundary}")

    direct_fields = (
        "direct_source_state",
        "direct_partner_loss",
        "direct_partner_arrival_replacement",
        "direct_realized_community_shift",
        "direct_local_filtering",
        "direct_assurance_breeding",
        "direct_plant_response",
    )
    direct_counts = {field: sum(row[field] == "direct" for row in combined) for field in direct_fields}
    if direct_counts["direct_partner_loss"] != 0 or direct_counts["direct_partner_arrival_replacement"] != 0:
        raise RuntimeError("master-gap waves must not manufacture direct historical turnover measurements")

    return {
        "schema_version": "1.0",
        "status": "pass",
        "master_provenance": MASTER_PROVENANCE,
        "search_frame_boundary": {
            "prior_named_target_frame": 111,
            "prior_frame_is_world_census": False,
            "independent_master_candidate_island_polygons_ge_20km2": 4663,
            "individual_polygons_treated_as_independent_ecological_systems": False,
            "first_master_gap_tranche_geographic_systems": 20,
            "first_master_gap_tranche_reviewed": 20,
        },
        "wave1": {
            "systems": 8,
            "primary_verified": 8,
        },
        "wave2": {
            "systems": 12,
            "source_status_counts": dict(sorted(Counter(row["source_verification"] for row in wave2).items())),
            "decision_counts": dict(sorted(Counter(row["manuscript_value_decision"] for row in wave2).items())),
            "full_contract_passes": 0,
        },
        "combined_20_system_review": {
            "systems": 20,
            "primary_verified_sources": sum(row["source_verification"] == "primary_article_verified" for row in combined),
            "promotion_review_queue": sorted(promotion_queue),
            "direct_measurement_counts": direct_counts,
            "full_contract_passes": 0,
            "transition_coordinate_result": "no direct partner-loss or partner-arrival/replacement series recovered",
        },
        "active_manuscript_boundary": {
            "descriptive_research_entries": 42,
            "exact_geographic_labels": 37,
            "formal_identifiability_research_entries": 25,
            "formal_full_contracts": "0_of_25",
            "formal_external_prediction": "not_evaluable",
            "mutated_by_master_gap_review": False,
        },
        "scientific_readout": (
            "Geography-independent expansion recovers additional direct outcome, breeding, community and local-filtering evidence, "
            "including strong falsification cases, but the historical transition coordinates remain the limiting measurements."
        ),
        "next_step": "expand the master-gap queue beyond the first 20 systems, then separately review promotion value; defer Izu until world confrontation stabilizes",
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
