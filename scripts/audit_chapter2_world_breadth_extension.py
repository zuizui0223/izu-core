from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN_LEDGER = ROOT / "data/design/chapter2_external_prediction_admission_ledger_20260828.csv"
EXTENSION_LEDGER = ROOT / "data/design/chapter2_world_breadth_extension_20260902.csv"
SYNTHESIS_LEDGER = ROOT / "data/design/chapter2_world_breadth_synthesis_context_20260904.csv"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_world_breadth_extension_audit_20260903.json"

DIRECT_ARRIVAL_CLASSES = {
    "direct_recent_arrival",
    "direct_recent_arrival_phylogeographic",
    "direct_historical_arrival",
}


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_audit() -> dict:
    frozen = _read_rows(FROZEN_LEDGER)
    extension = _read_rows(EXTENSION_LEDGER)
    syntheses = _read_rows(SYNTHESIS_LEDGER)

    if len(frozen) != 25:
        raise RuntimeError(f"frozen identifiability ledger changed: expected 25 rows, got {len(frozen)}")
    if len(extension) != 14:
        raise RuntimeError(f"post-freeze breadth extension changed: expected 14 rows, got {len(extension)}")
    if len(syntheses) != 1:
        raise RuntimeError(f"breadth synthesis context changed: expected 1 row, got {len(syntheses)}")

    extension_ids = [row["extension_id"] for row in extension]
    if len(set(extension_ids)) != len(extension_ids):
        duplicates = sorted(key for key, count in Counter(extension_ids).items() if count > 1)
        raise RuntimeError(f"duplicate breadth-extension IDs: {duplicates}")
    if any(not row["source_reference"].strip() for row in extension):
        raise RuntimeError("every breadth-extension row must carry a source reference")
    if any(row["full_chapter2_contract"] != "fail" for row in extension):
        raise RuntimeError("breadth extension must not silently create a full Chapter 2 contract")
    if any(row["source_verification"] == "" for row in extension):
        raise RuntimeError("every breadth-extension row must carry a source-verification state")
    if any(row["novel_geographic_group_relative_to_frozen25"].lower() != "true" for row in extension):
        raise RuntimeError("extension contains a row not marked as a novel exact geographic group")

    frozen_groups = {row["geographic_overlap_group"] for row in frozen}
    extension_groups = {row["geographic_overlap_group"] for row in extension}
    if frozen_groups & extension_groups:
        raise RuntimeError(f"exact geographic overlap leaked into extension: {sorted(frozen_groups & extension_groups)}")

    synthesis = syntheses[0]
    synthesis_group_count = int(synthesis["source_native_island_group_count"])
    synthesis_species_count = int(synthesis["source_native_species_count"])
    if synthesis_group_count != 11 or synthesis_species_count != 321:
        raise RuntimeError("Southern Ocean synthesis context changed from source-verified 11 groups / 321 species")
    if not synthesis["formal_identifiability_denominator_effect"].startswith("none"):
        raise RuntimeError("multi-group synthesis must remain outside formal identifiability denominators")

    arrival_counts = Counter(row["arrival_evidence_class"] for row in extension)
    direct_arrival_rows = [row["extension_id"] for row in extension if row["arrival_evidence_class"] in DIRECT_ARRIVAL_CLASSES]

    return {
        "schema_version": "1.2",
        "status": "post_freeze_breadth_extension_source_verified",
        "frozen_identifiability_denominator": {
            "research_entries": len(frozen),
            "geographic_overlap_labels": len(frozen_groups),
            "formal_external_prediction_reopened": False,
            "frozen_25_recomputed": False,
        },
        "post_freeze_extension": {
            "research_entries": len(extension),
            "exact_geographic_groups": len(extension_groups),
            "geographic_groups": sorted(extension_groups),
            "arrival_evidence_class_counts": dict(sorted(arrival_counts.items())),
            "direct_or_historical_arrival_entries": len(direct_arrival_rows),
            "direct_or_historical_arrival_ids": direct_arrival_rows,
            "full_chapter2_contract_passes": 0,
        },
        "multi_group_breadth_context": {
            "research_syntheses": len(syntheses),
            "southern_ocean_source_native_island_groups": synthesis_group_count,
            "southern_ocean_flowering_plant_species": synthesis_species_count,
            "included_in_formal_or_exact_group_denominators": False,
        },
        "combined_descriptive_universe": {
            "research_entries_before_cross_layer_deduplication": len(frozen) + len(extension),
            "exact_overlap_labels_before_higher_level_archipelago_deduplication": len(frozen_groups) + len(extension_groups),
            "independent_archipelago_denominator_claimed": False,
        },
        "claim_boundary": (
            "The 14 post-freeze exact-group entries plus the separately tracked Southern Ocean synthesis broaden geographic and process coverage only. "
            "They do not alter the frozen 25-entry identifiability audit, its 0/25 full-contract result, "
            "or the not_evaluable formal external-prediction conclusion."
        ),
    }


def write_audit(output: Path = DEFAULT_OUTPUT) -> Path:
    payload = build_audit()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_audit())
