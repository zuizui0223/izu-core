from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WAVE = ROOT / "data/design/chapter2_global_island_master_gap_wave1_20260906.csv"
PRIORITY = ROOT / "data/design/chapter2_global_island_master_priority_systems_wave1_snapshot_20260906.csv"
UNIVERSE = ROOT / "data/design/chapter2_systematic_island_universe_v1_20260903.csv"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
DEFAULT_OUT = ROOT / "data/results/chapter2_global_island_master_gap_wave1_audit_20260906.json"

MASTER_PROVENANCE = {
    "source_repository": "zuizui0223/island",
    "source_commit": "f1462cd1aa76b2703bc2df159996a4ab65510a25",
    "source_path": "legacy/v1/artifacts/data_global_islands/global_islands_over20km2.csv",
    "source_blob": "42f31df81db250ebfe46b35ebce6cb1c52b19fc9",
    "source_lineage": "Global Islands v3 / WCMC-USGS-derived historical artifact",
    "area_threshold_km2": 20,
    "candidate_island_polygons": 4663,
}

REQUIRED_WAVE1 = {
    "channel_islands_nicotiana_2004",
    "chiloe_embothrium_2006",
    "newfoundland_menyanthes_1998",
    "svalbard_saxifraga_2001",
    "hainan_impatiens_2014",
    "borneo_goniothalamus_2016",
    "sulawesi_coffee_2003",
    "new_guinea_fig_wasp_2012",
}

PROMOTE_NEXT = {
    "channel_islands_nicotiana_2004",
    "chiloe_embothrium_2006",
    "newfoundland_menyanthes_1998",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def audit() -> dict:
    wave = read_csv(WAVE)
    priority = read_csv(PRIORITY)
    universe = read_csv(UNIVERSE)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    ids = {row["system_id"] for row in wave}
    if ids != REQUIRED_WAVE1:
        raise RuntimeError(f"wave1 membership changed: {sorted(ids)}")
    if len(wave) != len(ids):
        raise RuntimeError("wave1 system_id values must be unique")

    existing_targets = {row["geographic_target"].casefold() for row in universe}
    for row in wave:
        if row["geographic_system"].casefold() in existing_targets:
            raise RuntimeError(f"wave1 system already appears verbatim in 111 frame: {row['geographic_system']}")
        if row["full_chapter2_contract"] != "fail":
            raise RuntimeError(f"unverified full contract in wave1: {row['system_id']}")
        if row["source_verification"] != "primary_article_verified":
            raise RuntimeError(f"wave1 source is not primary-verified: {row['system_id']}")
        if row["geographic_system"] == "Izu Islands":
            raise RuntimeError("Izu must remain the final zoom, not enter the global gap wave")

    promoted = {row["system_id"] for row in wave if row["manuscript_value_decision"] == "promote_next_review"}
    if promoted != PROMOTE_NEXT:
        raise RuntimeError(f"wave1 promotion-review queue changed: {sorted(promoted)}")

    priority_rows = {row["geographic_system"]: row for row in priority}
    for system in ("Borneo", "New Guinea", "Newfoundland", "Hokkaido", "Tierra del Fuego", "Spitsbergen / Svalbard", "Hainan", "Sulawesi"):
        if system not in priority_rows:
            raise RuntimeError(f"major geography missing from master-gap queue: {system}")
        if priority_rows[system]["represented_in_111"] != "false":
            raise RuntimeError(f"major gap was silently marked represented: {system}")

    breadth = manifest["world_breadth_extension"]
    claims = manifest["claim_ceiling"]
    if breadth["combined_descriptive_research_entries_before_cross_layer_deduplication"] != 42:
        raise RuntimeError("global-master gap review must not mutate active 42-entry descriptive breadth")
    if breadth["combined_exact_overlap_labels_before_higher_level_archipelago_deduplication"] != 37:
        raise RuntimeError("global-master gap review must not mutate active 37-label descriptive breadth")
    if breadth["formal_identifiability_research_entries"] != 25:
        raise RuntimeError("frozen identifiability denominator changed")
    if claims["external_full_contracts"] != "0_of_25" or claims["formal_external_prediction"] != "not_evaluable":
        raise RuntimeError("formal external-inference boundary changed")

    decisions = Counter(row["manuscript_value_decision"] for row in wave)
    falsification = Counter(row["falsification_value"] for row in wave)
    source_dimensions = {
        field: sum(row[field] == "direct" for row in wave)
        for field in (
            "direct_source_state",
            "direct_partner_loss",
            "direct_partner_arrival_replacement",
            "direct_realized_community_shift",
            "direct_local_filtering",
            "direct_assurance_breeding",
            "direct_plant_response",
        )
    }

    return {
        "schema_version": "1.0",
        "status": "pass",
        "master_provenance": MASTER_PROVENANCE,
        "search_frame_boundary": {
            "prior_named_target_frame": 111,
            "prior_frame_is_world_census": False,
            "independent_master_candidate_island_polygons_ge_20km2": 4663,
            "individual_polygons_treated_as_independent_ecological_systems": False,
        },
        "priority_queue": {
            "documented_omitted_geographic_systems": len(priority),
            "searched_wave1": sum(row["wave_status"] == "searched_wave1" for row in priority),
            "next_wave": sum(row["wave_status"] == "next_wave" for row in priority),
        },
        "wave1": {
            "systems": len(wave),
            "primary_verified": sum(row["source_verification"] == "primary_article_verified" for row in wave),
            "decision_counts": dict(sorted(decisions.items())),
            "falsification_value_counts": dict(sorted(falsification.items())),
            "direct_measurement_counts": source_dimensions,
            "full_contract_passes": 0,
            "promotion_review_queue": sorted(promoted),
        },
        "active_manuscript_boundary": {
            "descriptive_research_entries": 42,
            "exact_geographic_labels": 37,
            "formal_identifiability_research_entries": 25,
            "formal_full_contracts": "0_of_25",
            "formal_external_prediction": "not_evaluable",
            "mutated_by_wave1": False,
        },
        "next_step": "continue master-driven gap waves before any Izu zoom; promotion requires a separate value review",
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
