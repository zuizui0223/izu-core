"""Build a broad, predeclared public-image cohort manifest.

This script intentionally relaxes the earlier three-regime *taxon* gate.  The
later analysis treats each transition separately, so a taxon with Oshima and
no-Bombus images can inform the second transition even when mainland images are
absent.  Functional group labels are read from the existing audited
classification table; taxa outside `specialist_bee` and `generalist_open` are
not silently recoded.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

OUTPUT_FIELDS = (
    "taxon", "analysis_group", "functional_group", "group_confidence", "n_islands", "total_occ",
    "selection_rank", "role", "trait_layer", "selection_boundary",
)


def clean(value: object) -> str:
    return str(value or "").strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--classification", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-specialists", type=int, default=12)
    parser.add_argument("--max-generalists", type=int, default=12)
    parser.add_argument("--min-islands", type=int, default=3)
    parser.add_argument("--min-total-occ", type=int, default=10)
    return parser.parse_args()


def select(rows: list[dict[str, str]], group: str, max_taxa: int, min_islands: int, min_total_occ: int) -> list[dict[str, str]]:
    eligible = [
        row for row in rows
        if clean(row["functional_group"]) == group
        and clean(row["confidence"]) in {"high", "medium"}
        and int(clean(row["n_islands"])) >= min_islands
        and int(clean(row["total_occ"])) >= min_total_occ
    ]
    eligible.sort(key=lambda row: (-int(row["n_islands"]), -int(row["total_occ"]), clean(row["name"])))
    return eligible[:max_taxa]


def main() -> None:
    args = parse_args()
    if args.max_specialists <= 0 or args.max_generalists <= 0:
        raise SystemExit("max cohort sizes must be positive")
    with args.classification.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"name", "functional_group", "confidence", "n_islands", "total_occ"}
    if not rows or not required.issubset(rows[0]):
        raise SystemExit("classification table is empty or missing required columns")
    specialist = select(rows, "specialist_bee", args.max_specialists, args.min_islands, args.min_total_occ)
    generalist = select(rows, "generalist_open", args.max_generalists, args.min_islands, args.min_total_occ)
    output: list[dict[str, object]] = []
    boundary = (
        "Selection uses existing functional-group labels and occurrence coverage only. It does not establish that a photographed flower is open, "
        "that an image feature is a floral trait, or that a taxon experiences a measured pollinator regime."
    )
    for analysis_group, selected in (("specialist", specialist), ("generalist", generalist)):
        for rank, row in enumerate(selected, start=1):
            output.append({
                "taxon": clean(row["name"]), "analysis_group": analysis_group,
                "functional_group": clean(row["functional_group"]), "group_confidence": clean(row["confidence"]),
                "n_islands": clean(row["n_islands"]), "total_occ": clean(row["total_occ"]),
                "selection_rank": rank,
                "role": "positive_pattern_test" if analysis_group == "specialist" else "negative_control_pattern_test",
                "trait_layer": "exploratory_scale_free_public_image_signature",
                "selection_boundary": boundary,
            })
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader(); writer.writerows(output)
    print(f"wrote {len(specialist)} specialist and {len(generalist)} generalist taxa to {args.out}")


if __name__ == "__main__":
    main()
