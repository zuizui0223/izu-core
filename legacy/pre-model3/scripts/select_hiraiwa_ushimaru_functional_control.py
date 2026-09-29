#!/usr/bin/env python3
"""Select a prospective high-functional-generality phenotype control.

Selection uses only source-defined pollen-target membership, realized plant
functional generality, and geographic coverage. It does not use the sign of a
floral morphology, corrected trait-matching, pollen-receipt, or breeding-system
response. The selected plant is therefore a prospective control candidate for
future phenotype/breeding comparisons, not retrospective confirmation of a null.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


MIN_SITES = 6
MIN_FG_ROWS = 5


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("artifacts/hiraiwa_ushimaru_figshare/files"))
    parser.add_argument("--out-dir", type=Path, default=Path("artifacts/hiraiwa_ushimaru_figshare/functional_control"))
    args = parser.parse_args()

    pollen = load_csv(args.data_dir / "data_pollen.csv")
    plants = load_csv(args.data_dir / "data_sp_plant.csv")
    target_species = {row["plant"].strip() for row in pollen}

    fg: dict[str, list[float]] = defaultdict(list)
    sites: dict[str, set[int]] = defaultdict(set)
    for row in plants:
        plant = row["plant"].strip()
        if plant not in target_species:
            continue
        raw = str(row.get("FG_Pla_sp_z") or "").strip()
        if not raw or raw.upper() == "NA":
            continue
        fg[plant].append(float(raw))
        sites[plant].add(int(row["siteid"]))

    ranking = []
    for plant in sorted(target_species):
        values = fg.get(plant, [])
        n_sites = len(sites.get(plant, set()))
        ranking.append({
            "plant": plant,
            "mean_functional_generality_z": None if not values else sum(values) / len(values),
            "n_functional_generality_rows": len(values),
            "n_sites_with_functional_generality": n_sites,
            "coverage_eligible": len(values) >= MIN_FG_ROWS and n_sites >= MIN_SITES,
        })
    ranking.sort(
        key=lambda row: (
            not bool(row["coverage_eligible"]),
            -(float(row["mean_functional_generality_z"]) if row["mean_functional_generality_z"] is not None else -1e9),
        )
    )
    eligible = [row for row in ranking if row["coverage_eligible"]]
    if not eligible:
        raise ValueError("no pollen-target species passes the prospective control coverage gate")
    selected = eligible[0]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    with (args.out_dir / "ranking.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ranking[0]))
        writer.writeheader(); writer.writerows(ranking)

    report = {
        "selection_target": "prospective phenotype/breeding negative-control candidate",
        "source_defined_universe": "10 dominant outcrossing insect-pollinated plants selected by the source study for pollen-receipt measurements",
        "selection_variables": [
            "mean source-native FG_Pla_sp_z",
            "at least 6 of 8 sites with functional-generality observations",
            "at least 5 functional-generality rows"
        ],
        "variables_not_used_for_selection": [
            "corrected trait-matching contrast",
            "pollen-receipt contrast",
            "floral morphology response",
            "breeding-system response"
        ],
        "selected": selected,
        "n_coverage_eligible_species": len(eligible),
        "ranking": ranking,
        "claim_boundary": (
            "High realized functional generality is not pollinator effectiveness, selfing capacity, or proof of "
            "ecological independence. The selected plant is prospectively locked only as a high-interaction-breadth "
            "control candidate for future phenotype/breeding tests."
        ),
    }
    (args.out_dir / "summary.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
