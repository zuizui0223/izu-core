"""Build the U1 all-taxon search queue from a rebuilt U0 parent universe.

U1 is intentionally broader than the 156-species entomophilous pilot. It ranks
search effort only by geography and record availability, never by a presumed
pollination group or expected trait direction. This prevents early ecological
filtering from predetermining the literature synthesis.

Usage:
    python paper/build_u1_screening_queue.py \
        --u0 artifacts/u0_snapshot/u0_parent_universe.csv \
        --out artifacts/u0_snapshot/u1_screening_queue.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

HERE = Path(__file__).parent
PILOT = HERE / "izu_entomophilous_candidates.csv"
ISLANDS = ("Oshima", "Toshima", "Niijima", "Kozushima", "Miyake", "Hachijo")


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def priority(row: dict[str, str]) -> tuple[float, str]:
    """Geographic-only priority score; no trait or pollination assumptions."""
    n_islands = int(row["n_islands"])
    total_occ = int(row["total_occ"])
    boundary = row.get("Oshima_present") == "yes" and row.get("Toshima_present") == "yes"
    endpoint = row.get("Hachijo_present") == "yes"
    score = 100 * n_islands + 20 * int(boundary) + 10 * int(endpoint) + math.log1p(total_occ)
    reason = f"{n_islands}/6 islands"
    if boundary:
        reason += "; contains Oshima-Toshima boundary"
    if endpoint:
        reason += "; reaches Hachijo endpoint"
    reason += f"; {total_occ} GBIF occurrences in profile"
    return score, reason


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--u0", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--summary", type=Path, default=None)
    args = parser.parse_args()

    u0 = load_csv(args.u0)
    pilot_keys = {row["speciesKey"] for row in load_csv(PILOT)}
    queue: list[dict[str, object]] = []
    for row in u0:
        score, reason = priority(row)
        key = row["accepted_key"]
        queue.append({
            "queue_rank": 0,
            "u0_accepted_key": key,
            "accepted_name": row["accepted_name"],
            "family": row.get("family", ""),
            "taxonomic_status": row.get("taxonomic_status", ""),
            "n_islands": row["n_islands"],
            "total_occ": row["total_occ"],
            "Oshima_present": row.get("Oshima_present", ""),
            "Toshima_present": row.get("Toshima_present", ""),
            "Hachijo_present": row.get("Hachijo_present", ""),
            "boundary_coverage": "yes" if row.get("Oshima_present") == "yes" and row.get("Toshima_present") == "yes" else "no",
            "in_156_entomophilous_pilot": "yes" if key in pilot_keys else "no",
            "u1_priority_score": f"{score:.4f}",
            "priority_reason": reason,
            "required_search_lanes": "Japanese_literature|English_literature|synonym_registry|regional_flora|media_availability",
            "screening_status": "not_searched",
            "evidence_role": "U1_trait_search_universe",
            "boundary": "Occurrence coverage creates a search priority only; it is not a floral, pollination or evolutionary observation.",
        })
    queue.sort(key=lambda row: (-float(row["u1_priority_score"]), str(row["accepted_name"])))
    for rank, row in enumerate(queue, 1):
        row["queue_rank"] = rank

    args.out.parent.mkdir(parents=True, exist_ok=True)
    fields = list(queue[0]) if queue else ["queue_rank", "u0_accepted_key", "accepted_name"]
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(queue)
    summary_path = args.summary or args.out.with_suffix(".summary.json")
    summary = {
        "u1_taxa": len(queue),
        "u1_also_in_156_pilot": sum(row["in_156_entomophilous_pilot"] == "yes" for row in queue),
        "u1_not_in_156_pilot": sum(row["in_156_entomophilous_pilot"] == "no" for row in queue),
        "u1_with_Oshima_Toshima_boundary": sum(row["boundary_coverage"] == "yes" for row in queue),
        "rule": "No pollination, floral or expected-response filter was applied in U1 ranking.",
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
