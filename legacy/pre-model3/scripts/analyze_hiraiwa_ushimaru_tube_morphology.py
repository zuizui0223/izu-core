#!/usr/bin/env python3
"""Extract source-native site-level corolla tube morphology contrasts.

Hiraiwa & Ushimaru (2024) report that five flowers per plant species were
measured at each site using digital callipers and the species × site mean
corolla tube length was used in their network analyses. The Figshare
``data_sp_plant.csv`` stores those means in ``tube``.

This audit deduplicates repeated seasonal rows within plant × site and compares
mainland-site means, Oshima, and post-Oshima Izu means. The source dataset does
not expose within-site SD/SE for tube length, so these values are numeric
directional morphology evidence, not A-grade inverse-variance effect sizes.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


SITE = {1: "hitachi", 2: "hitachinaka", 3: "tateyama", 4: "oshima", 5: "niijima", 6: "kozu", 7: "miyake", 8: "hachijo"}
MAINLAND = {1, 2, 3}
OSHIMA = 4
POST = {5, 6, 7, 8}
SOURCE_N_FLOWERS_PER_SPECIES_SITE = 5


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def deduplicate_tube(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    values: dict[tuple[str, int], set[float]] = defaultdict(set)
    for row in rows:
        raw = str(row.get("tube") or "").strip()
        if not raw or raw.upper() == "NA":
            continue
        plant = row["plant"].strip()
        siteid = int(row["siteid"])
        values[(plant, siteid)].add(float(raw))
    output = []
    for (plant, siteid), observed in sorted(values.items()):
        if len(observed) != 1:
            raise ValueError(f"tube value changes across seasonal rows for {plant} site {siteid}: {sorted(observed)}")
        output.append({
            "plant": plant,
            "siteid": siteid,
            "site": SITE[siteid],
            "tube_mean_mm": next(iter(observed)),
            "source_n_flowers": SOURCE_N_FLOWERS_PER_SPECIES_SITE,
            "within_site_uncertainty_available": "no",
        })
    return output


def contrasts(site_rows: list[dict[str, object]], *, minimum_post_sites: int = 2) -> list[dict[str, object]]:
    by_plant: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in site_rows:
        by_plant[str(row["plant"])].append(row)
    output = []
    for plant, rows in sorted(by_plant.items()):
        mainland = [float(row["tube_mean_mm"]) for row in rows if int(row["siteid"]) in MAINLAND]
        oshima = [float(row["tube_mean_mm"]) for row in rows if int(row["siteid"]) == OSHIMA]
        post_rows = [row for row in rows if int(row["siteid"]) in POST]
        post = [float(row["tube_mean_mm"]) for row in post_rows]
        post_sites = len({int(row["siteid"]) for row in post_rows})
        if len(oshima) != 1 or post_sites < minimum_post_sites:
            continue
        mainland_mean = mean(mainland) if mainland else None
        oshima_value = oshima[0]
        post_mean = mean(post)
        output.append({
            "plant": plant,
            "n_mainland_sites": len(mainland),
            "n_post_sites": post_sites,
            "mainland_mean_tube_mm": mainland_mean,
            "oshima_tube_mm": oshima_value,
            "post_mean_tube_mm": post_mean,
            "second_delta_mm": post_mean - oshima_value,
            "second_percent_change_from_oshima": 100.0 * (post_mean - oshima_value) / oshima_value if oshima_value else None,
            "second_direction": "shorter_post" if post_mean < oshima_value else ("longer_post" if post_mean > oshima_value else "equal"),
            "measurement_n_per_species_site": SOURCE_N_FLOWERS_PER_SPECIES_SITE,
            "within_site_uncertainty_available": "no",
            "numeric_evidence_grade": "B_plus_site_mean_without_variance",
        })
    return output


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("artifacts/hiraiwa_ushimaru_figshare/files/data_sp_plant.csv"))
    parser.add_argument("--pollen", type=Path, default=Path("artifacts/hiraiwa_ushimaru_figshare/files/data_pollen.csv"))
    parser.add_argument("--out-dir", type=Path, default=Path("artifacts/hiraiwa_ushimaru_figshare/tube_morphology"))
    args = parser.parse_args()

    raw = load_csv(args.data)
    pollen = load_csv(args.pollen)
    target_species = {row["plant"].strip() for row in pollen}
    site_rows = deduplicate_tube(raw)
    all_contrasts = contrasts(site_rows)
    target_contrasts = [row for row in all_contrasts if row["plant"] in target_species]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "site_tube_means.csv", site_rows)
    write_csv(args.out_dir / "tube_contrasts_all_network_plants.csv", all_contrasts)
    write_csv(args.out_dir / "tube_contrasts_pollen_targets.csv", target_contrasts)

    indexed = {str(row["plant"]): row for row in all_contrasts}
    focal = {name: indexed.get(name) for name in ("Campanula microdonta", "Farfugium japonicum")}
    shorter = [row["plant"] for row in target_contrasts if row["second_direction"] == "shorter_post"]
    longer = [row["plant"] for row in target_contrasts if row["second_direction"] == "longer_post"]
    equal = [row["plant"] for row in target_contrasts if row["second_direction"] == "equal"]
    report = {
        "source_dataset": "10.6084/m9.figshare.25025000.v1",
        "measurement_method": "digital calliper; source Methods state five flowers per plant species at each site; species x site mean stored as tube",
        "within_site_sd_se_available_in_archived_species_table": False,
        "numeric_evidence_grade": "B_plus_site_mean_without_variance",
        "pollen_target_species_direction": {
            "eligible": len(target_contrasts),
            "shorter_post": len(shorter),
            "longer_post": len(longer),
            "equal": len(equal),
            "shorter_post_species": shorter,
            "longer_post_species": longer,
            "equal_species": equal,
        },
        "focal_examples": focal,
        "claim_boundary": (
            "Site means are direct numeric floral morphology, but the archived table does not provide within-site "
            "variance. Do not compute inverse-variance effect sizes, equivalence, or A-grade quantitative holdout "
            "claims from these means. Contemporary site morphology also cannot establish historical selection."
        ),
    }
    (args.out_dir / "summary.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
