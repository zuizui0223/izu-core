#!/usr/bin/env python3
"""Summarize community-level seasonal Oshima-versus-post network responses.

The five seasons are repeated temporal observations of the same geographic
units. They are used only to describe temporal consistency and never promoted to
five independent boundary replications.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


POST_SITES = {"niijima", "kozu", "miyake", "hachijo"}
METRICS = ("FDQ", "TM_z", "FG_Pol_z", "FG_Pla_z", "richness")


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("artifacts/hiraiwa_ushimaru_figshare/files/data_main.csv"))
    parser.add_argument("--out", type=Path, default=Path("artifacts/hiraiwa_ushimaru_figshare/community_response/summary.json"))
    args = parser.parse_args()

    with args.data.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    seasons = sorted({int(row["season"]) for row in rows})
    if seasons != [1, 2, 3, 4, 5]:
        raise ValueError(f"unexpected seasons: {seasons}")

    output = {}
    for metric in METRICS:
        seasonal = []
        for season in seasons:
            oshima_rows = [row for row in rows if row["site"] == "oshima" and int(row["season"]) == season]
            if len(oshima_rows) != 1:
                raise ValueError(f"season {season}: expected one Oshima row")
            post = [
                float(row[metric]) for row in rows
                if row["site"] in POST_SITES and int(row["season"]) == season and row[metric] not in {"", "NA"}
            ]
            if len(post) != 4:
                raise ValueError(f"season {season} metric {metric}: expected four post-site values")
            oshima = float(oshima_rows[0][metric])
            post_mean = mean(post)
            seasonal.append({
                "season": season,
                "oshima": oshima,
                "post_mean": post_mean,
                "delta_post_minus_oshima": post_mean - oshima,
                "n_post_sites": len(post),
            })
        deltas = [row["delta_post_minus_oshima"] for row in seasonal]
        output[metric] = {
            "seasonal": seasonal,
            "mean_delta": mean(deltas),
            "n_lower_post_seasons": sum(value < 0 for value in deltas),
            "n_higher_post_seasons": sum(value > 0 for value in deltas),
        }

    report = {
        "source_dataset": "10.6084/m9.figshare.25025000.v1",
        "contrast": "same-season Oshima value versus mean of Niijima, Kozu, Miyake and Hachijo",
        "temporal_repeats": 5,
        "independent_oshima_bridge_sites": 1,
        "metrics": output,
        "reading": (
            "Community corrected trait matching is lower post-Oshima in four of five seasons and has a negative "
            "mean contrast, whereas plant and pollinator functional generality are directionally mixed or often "
            "higher post-Oshima. Functional diversity and richness also vary across seasons. The contemporary "
            "community pattern is therefore matching-focused rather than a synchronous decline in all network channels."
        ),
        "claim_boundary": (
            "The five seasons are repeated observations of one Oshima geographic unit and four post sites, not five "
            "independent boundary experiments. These summaries are descriptive contemporary network context and do not "
            "identify a causal pollinator-regime boundary effect or historical floral evolution."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
