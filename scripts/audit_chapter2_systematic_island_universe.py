from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIVERSE = ROOT / "data/design/chapter2_systematic_island_universe_v1_20260903.csv"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_systematic_island_universe_audit_v1_20260903.json"

ALLOWED_STATUS = {
    "source_verified_current",
    "source_gated_current",
    "umbrella_source_verified",
    "umbrella_source_covered",
    "umbrella_network_indexed",
    "source_found_needs_ledger_gate",
    "nested_target_needs_specific_gate",
    "target_not_yet_source_gated",
}

RESOLVED_OR_INDEXED = {
    "source_verified_current",
    "source_gated_current",
    "umbrella_source_verified",
    "umbrella_source_covered",
    "umbrella_network_indexed",
}


def _rows() -> list[dict[str, str]]:
    with UNIVERSE.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_audit() -> dict:
    rows = _rows()
    if len(rows) != 110:
        raise RuntimeError(f"systematic island universe changed: expected 110 rows, got {len(rows)}")

    keys = [(row["macroregion"], row["geographic_target"]) for row in rows]
    if len(keys) != len(set(keys)):
        raise RuntimeError("duplicate macroregion + geographic_target rows in systematic island universe")

    statuses = {row["coverage_status"] for row in rows}
    unknown = statuses - ALLOWED_STATUS
    if unknown:
        raise RuntimeError(f"unknown coverage statuses: {sorted(unknown)}")

    if any(not row["seed_source"].strip() for row in rows):
        raise RuntimeError("every target must carry a seed source or explicit systematic-target marker")

    status_counts = Counter(row["coverage_status"] for row in rows)
    region_counts = Counter(row["macroregion"] for row in rows)
    priority_counts = Counter(row["search_priority"] for row in rows)
    resolved = sum(row["coverage_status"] in RESOLVED_OR_INDEXED for row in rows)

    return {
        "schema_version": "1.0",
        "status": "systematic_search_universe_v1",
        "scope": (
            "Named archipelagos, island groups and selected large/sentinel islands relevant to terrestrial "
            "flowering-plant pollination, breeding systems, reproductive assurance or plant-pollinator networks. "
            "This is a reproducible search universe, not a claim that 110 is the number of island systems on Earth."
        ),
        "target_rows": len(rows),
        "macroregions": len(region_counts),
        "macroregion_counts": dict(sorted(region_counts.items())),
        "coverage_status_counts": dict(sorted(status_counts.items())),
        "priority_counts": dict(sorted(priority_counts.items())),
        "resolved_or_umbrella_indexed_targets": resolved,
        "targets_requiring_further_source_work": len(rows) - resolved,
        "directly_not_yet_source_gated": status_counts["target_not_yet_source_gated"],
        "source_found_needing_ledger_gate": status_counts["source_found_needs_ledger_gate"],
        "nested_targets_needing_specific_gate": status_counts["nested_target_needs_specific_gate"],
        "claim_boundary": (
            "Do not add these 110 targets to the frozen 25-entry identifiability denominator or the current "
            "36-entry descriptive confrontation. A target is promoted only after source verification and explicit "
            "overlap/de-duplication review."
        ),
    }


def write_audit(output: Path = DEFAULT_OUTPUT) -> Path:
    payload = build_audit()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_audit())
