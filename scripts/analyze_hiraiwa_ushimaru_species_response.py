#!/usr/bin/env python3
"""Summarize species-level functional responses in the Hiraiwa-Ushimaru data.

The analysis uses the archived 2024 Figshare tables. Repeated seasonal rows are
first aggregated within plant × site, so seasons are not counted as independent
islands. The focal descriptive contrast is the source-native Oshima site versus
the mean of post-Oshima Izu sites (Niijima, Kozu, Miyake, Hachijo).

This is a contemporary interaction-function audit, not a floral-evolution or
historical-causation analysis.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Iterable


SITE_ORDER = {
    1: "hitachi",
    2: "hitachinaka",
    3: "tateyama",
    4: "oshima",
    5: "niijima",
    6: "kozu",
    7: "miyake",
    8: "hachijo",
}
MAINLAND = {1, 2, 3}
OSHIMA = 4
POST_BOUNDARY = {5, 6, 7, 8}


def _float(value: object) -> float | None:
    text = str(value or "").strip()
    if not text or text.upper() == "NA":
        return None
    return float(text)


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    if not values:
        raise ValueError("mean requires at least one value")
    return sum(values) / len(values)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_main_site_order(main_rows: list[dict[str, str]]) -> None:
    season_one = [row["site"].strip() for row in main_rows if int(row["season"]) == 1]
    expected = [SITE_ORDER[index] for index in range(1, 9)]
    if season_one != expected:
        raise ValueError(f"unexpected site order in data_main.csv: {season_one}")


def infer_pollen_site_mapping(
    pollen_rows: list[dict[str, str]], main_rows: list[dict[str, str]],
) -> dict[str, str]:
    """Resolve pollen-table aliases by exact shared community metrics.

    data_pollen contains legacy site aliases. Each row also stores the matching
    community TM_z and FG_pla_z. We identify the data_main site whose seasonal
    community values match exactly across all available seasons. This avoids a
    manually guessed alias map.
    """
    main_index = {
        (row["site"].strip(), int(row["season"])): (
            float(row["TM_z"]), float(row["FG_Pla_z"])
        )
        for row in main_rows
    }
    aliases = sorted({row["site"].strip() for row in pollen_rows})
    output: dict[str, str] = {}
    for alias in aliases:
        observed = {}
        for row in pollen_rows:
            if row["site"].strip() != alias:
                continue
            key = int(row["season"])
            observed.setdefault(key, (float(row["TM_z"]), float(row["FG_pla_z"])))
        candidates = []
        for site in SITE_ORDER.values():
            if all(
                season in {key[1] for key in main_index if key[0] == site}
                and all(abs(a - b) < 1e-10 for a, b in zip(values, main_index[(site, season)]))
                for season, values in observed.items()
            ):
                candidates.append(site)
        if len(candidates) != 1:
            raise ValueError(f"cannot uniquely map pollen site alias {alias}: {candidates}")
        output[alias] = candidates[0]
    return output


def aggregate_plant_site(sp_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    buckets: dict[tuple[str, int], dict[str, list[float]]] = defaultdict(
        lambda: {"FG": [], "TM": [], "tube": []}
    )
    for row in sp_rows:
        plant = row["plant"].strip()
        siteid = int(row["siteid"])
        if siteid not in SITE_ORDER:
            raise ValueError(f"unknown siteid: {siteid}")
        for source, target in (("FG_Pla_sp_z", "FG"), ("TM_sp_z", "TM"), ("tube", "tube")):
            value = _float(row.get(source))
            if value is not None and math.isfinite(value):
                buckets[(plant, siteid)][target].append(value)
    output = []
    for (plant, siteid), values in sorted(buckets.items()):
        output.append({
            "plant": plant,
            "siteid": siteid,
            "site": SITE_ORDER[siteid],
            "FG": _mean(values["FG"]) if values["FG"] else None,
            "TM": _mean(values["TM"]) if values["TM"] else None,
            "tube": _mean(values["tube"]) if values["tube"] else None,
        })
    return output


def aggregate_pollen_site(
    pollen_rows: list[dict[str, str]], alias_map: dict[str, str],
) -> list[dict[str, object]]:
    siteid_by_name = {name: siteid for siteid, name in SITE_ORDER.items()}
    buckets: dict[tuple[str, int], list[float]] = defaultdict(list)
    for row in pollen_rows:
        alias = row["site"].strip()
        site = alias_map[alias]
        siteid = siteid_by_name[site]
        value = _float(row.get("pollen_z"))
        if value is not None and math.isfinite(value):
            buckets[(row["plant"].strip(), siteid)].append(value)
    return [
        {
            "plant": plant,
            "siteid": siteid,
            "site": SITE_ORDER[siteid],
            "pollen_z": _mean(values),
            "n_flowers": len(values),
        }
        for (plant, siteid), values in sorted(buckets.items())
    ]


def contrast(
    records: list[dict[str, object]], metric: str, *, minimum_post_sites: int = 2,
) -> list[dict[str, object]]:
    by_plant: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in records:
        if row.get(metric) is not None:
            by_plant[str(row["plant"])].append(row)
    output = []
    for plant, rows in sorted(by_plant.items()):
        mainland = [float(row[metric]) for row in rows if int(row["siteid"]) in MAINLAND]
        oshima = [float(row[metric]) for row in rows if int(row["siteid"]) == OSHIMA]
        post_rows = [row for row in rows if int(row["siteid"]) in POST_BOUNDARY]
        post = [float(row[metric]) for row in post_rows]
        if len(oshima) != 1 or len({int(row["siteid"]) for row in post_rows}) < minimum_post_sites:
            continue
        mainland_mean = _mean(mainland) if mainland else None
        oshima_value = oshima[0]
        post_mean = _mean(post)
        output.append({
            "plant": plant,
            "metric": metric,
            "n_mainland_sites": len(mainland),
            "n_post_sites": len({int(row["siteid"]) for row in post_rows}),
            "mainland_mean": mainland_mean,
            "oshima": oshima_value,
            "post_mean": post_mean,
            "first_delta_oshima_minus_mainland": (
                None if mainland_mean is None else oshima_value - mainland_mean
            ),
            "second_delta_post_minus_oshima": post_mean - oshima_value,
            "second_direction": "lower_post" if post_mean < oshima_value else (
                "higher_post" if post_mean > oshima_value else "equal"
            ),
        })
    return output


def direction_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    lower = [str(row["plant"]) for row in rows if row["second_direction"] == "lower_post"]
    higher = [str(row["plant"]) for row in rows if row["second_direction"] == "higher_post"]
    equal = [str(row["plant"]) for row in rows if row["second_direction"] == "equal"]
    return {
        "n_eligible_species": len(rows),
        "n_lower_post": len(lower),
        "n_higher_post": len(higher),
        "n_equal": len(equal),
        "lower_post_species": lower,
        "higher_post_species": higher,
        "equal_species": equal,
    }


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
    parser.add_argument("--data-dir", type=Path, default=Path("artifacts/hiraiwa_ushimaru_figshare/files"))
    parser.add_argument("--out-dir", type=Path, default=Path("artifacts/hiraiwa_ushimaru_figshare/species_response"))
    args = parser.parse_args()

    main_rows = load_csv(args.data_dir / "data_main.csv")
    sp_rows = load_csv(args.data_dir / "data_sp_plant.csv")
    pollen_rows = load_csv(args.data_dir / "data_pollen.csv")
    validate_main_site_order(main_rows)
    alias_map = infer_pollen_site_mapping(pollen_rows, main_rows)
    plant_site = aggregate_plant_site(sp_rows)
    pollen_site = aggregate_pollen_site(pollen_rows, alias_map)

    fg = contrast(plant_site, "FG")
    tm = contrast(plant_site, "TM")
    pollen = contrast(pollen_site, "pollen_z")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "plant_site_metrics.csv", plant_site)
    write_csv(args.out_dir / "pollen_site_metrics.csv", pollen_site)
    write_csv(args.out_dir / "functional_generality_contrasts.csv", fg)
    write_csv(args.out_dir / "trait_matching_contrasts.csv", tm)
    write_csv(args.out_dir / "pollen_receipt_contrasts.csv", pollen)

    report = {
        "source": "Hiraiwa & Ushimaru 2024 Figshare dataset 10.6084/m9.figshare.25025000.v1",
        "site_order": SITE_ORDER,
        "pollen_alias_map_inferred_from_exact_shared_metrics": alias_map,
        "aggregation_unit": "plant x site; seasons averaged within site before regime contrasts",
        "minimum_post_sites": 2,
        "functional_generality": direction_summary(fg),
        "trait_matching": direction_summary(tm),
        "pollen_receipt": direction_summary(pollen),
        "key_observation": (
            "Every plant species with both Oshima and at least two post-boundary site-level corrected "
            "trait-matching observations has a lower post-boundary mean than its Oshima value. Functional "
            "generality and pollen receipt do not show the same uniform direction."
        ),
        "claim_boundary": (
            "Species share the same site-level environment and are not independent experimental replicates. "
            "This is a contemporary ecological interaction-function pattern, not evidence that plant floral "
            "traits evolved at the boundary. Corrected trait matching is a network-derived response; pollen "
            "receipt is open-pollinated reproductive function and is not autonomous reproductive capacity."
        ),
    }
    (args.out_dir / "summary.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
