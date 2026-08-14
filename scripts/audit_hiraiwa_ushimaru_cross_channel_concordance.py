#!/usr/bin/env python3
"""Join source-defined Hiraiwa-Ushimaru response channels across the same plants.

This audit links the already generated source-native Oshima -> post-Oshima
contrasts for the authors' pollen-success target plants:

- corrected trait matching (community functional fit),
- floral tube morphology (species x site means), and
- open-pollinated pollen receipt.

The purpose is not to fit a cross-species causal model. It asks whether a
coherent decline in corrected trait matching propagates as a uniform floral or
pollen-response syndrome across the same source-defined plant set.

Species share island/site environments, tube means lack within-site uncertainty,
and pollen receipt is observational. Direction counts and rank correlations are
therefore descriptive concordance diagnostics only.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable, Mapping


def text(row: Mapping[str, object], field: str) -> str:
    return str(row.get(field, "") or "").strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def ranks(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    output = [0.0] * len(values)
    position = 0
    while position < len(indexed):
        end = position + 1
        while end < len(indexed) and indexed[end][1] == indexed[position][1]:
            end += 1
        mean_rank = (position + 1 + end) / 2.0
        for index, _value in indexed[position:end]:
            output[index] = mean_rank
        position = end
    return output


def pearson(x: list[float], y: list[float]) -> float | None:
    if len(x) != len(y) or len(x) < 2:
        return None
    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)
    numerator = sum((a - x_mean) * (b - y_mean) for a, b in zip(x, y))
    x_ss = sum((a - x_mean) ** 2 for a in x)
    y_ss = sum((b - y_mean) ** 2 for b in y)
    denominator = (x_ss * y_ss) ** 0.5
    return None if denominator <= 0 else numerator / denominator


def spearman(x: list[float], y: list[float]) -> float | None:
    return pearson(ranks(x), ranks(y))


def direction_counts(rows: Iterable[Mapping[str, object]], field: str) -> dict[str, object]:
    values = [text(row, field) for row in rows]
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return {
        "n": len(values),
        "counts": dict(sorted(counts.items())),
    }


def build_audit(
    matching_rows: list[dict[str, str]],
    pollen_rows: list[dict[str, str]],
    tube_rows: list[dict[str, str]],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    matching = {text(row, "plant"): row for row in matching_rows}
    pollen = {text(row, "plant"): row for row in pollen_rows}
    tube = {text(row, "plant"): row for row in tube_rows}

    plants = sorted(set(matching) & set(tube))
    if len(plants) != 8:
        raise ValueError(f"expected 8 source-defined shared matching/tube targets, got {len(plants)}")
    missing_pollen = sorted(set(plants) - set(pollen))
    if missing_pollen:
        raise ValueError("shared target missing pollen contrast: " + ", ".join(missing_pollen))

    rows: list[dict[str, object]] = []
    for plant in plants:
        tm = matching[plant]
        po = pollen[plant]
        tu = tube[plant]
        row = {
            "plant": plant,
            "matching_delta_post_minus_oshima": float(tm["second_delta_post_minus_oshima"]),
            "matching_direction": text(tm, "second_direction"),
            "tube_delta_mm_post_minus_oshima": float(tu["second_delta_mm"]),
            "tube_percent_change_from_oshima": (
                None if not text(tu, "second_percent_change_from_oshima")
                else float(tu["second_percent_change_from_oshima"])
            ),
            "tube_direction": text(tu, "second_direction"),
            "pollen_delta_post_minus_oshima": float(po["second_delta_post_minus_oshima"]),
            "pollen_direction": text(po, "second_direction"),
            "matching_lower_and_tube_shorter": (
                text(tm, "second_direction") == "lower_post"
                and text(tu, "second_direction") == "shorter_post"
            ),
            "matching_lower_and_pollen_lower": (
                text(tm, "second_direction") == "lower_post"
                and text(po, "second_direction") == "lower_post"
            ),
            "triple_lower_or_shorter": (
                text(tm, "second_direction") == "lower_post"
                and text(tu, "second_direction") == "shorter_post"
                and text(po, "second_direction") == "lower_post"
            ),
        }
        rows.append(row)

    matching_delta = [float(row["matching_delta_post_minus_oshima"]) for row in rows]
    tube_delta = [float(row["tube_delta_mm_post_minus_oshima"]) for row in rows]
    pollen_delta = [float(row["pollen_delta_post_minus_oshima"]) for row in rows]

    triple = [str(row["plant"]) for row in rows if bool(row["triple_lower_or_shorter"])]
    tube_short_pollen_high = [
        str(row["plant"])
        for row in rows
        if row["tube_direction"] == "shorter_post" and row["pollen_direction"] == "higher_post"
    ]
    nonshort_pollen_low = [
        str(row["plant"])
        for row in rows
        if row["tube_direction"] in {"longer_post", "equal"} and row["pollen_direction"] == "lower_post"
    ]

    summary = {
        "schema_version": "1.0",
        "source_dataset": "10.6084/m9.figshare.25025000.v1",
        "scope": "source-defined pollen-success target plants with matched trait-matching, tube-morphology and pollen-receipt Oshima-to-post contrasts",
        "n_shared_targets": len(rows),
        "directions": {
            "corrected_trait_matching": direction_counts(rows, "matching_direction"),
            "tube_morphology": direction_counts(rows, "tube_direction"),
            "pollen_receipt": direction_counts(rows, "pollen_direction"),
        },
        "concordance": {
            "matching_lower_and_tube_shorter_n": sum(bool(row["matching_lower_and_tube_shorter"]) for row in rows),
            "matching_lower_and_pollen_lower_n": sum(bool(row["matching_lower_and_pollen_lower"]) for row in rows),
            "matching_lower_tube_shorter_pollen_lower_n": len(triple),
            "matching_lower_tube_shorter_pollen_lower_plants": triple,
            "tube_shorter_but_pollen_higher_plants": tube_short_pollen_high,
            "tube_longer_or_equal_but_pollen_lower_plants": nonshort_pollen_low,
        },
        "descriptive_rank_alignment": {
            "matching_delta_vs_tube_delta_spearman": spearman(matching_delta, tube_delta),
            "matching_delta_vs_pollen_delta_spearman": spearman(matching_delta, pollen_delta),
            "tube_delta_vs_pollen_delta_spearman": spearman(tube_delta, pollen_delta),
            "inferential_p_values_allowed": False,
            "reason": "Eight species share island/site environments and are not independent experimental replications; rank correlations are descriptive only.",
        },
        "reading": (
            "All eight source-defined shared targets have lower corrected trait matching post-Oshima, but tube morphology and pollen receipt split across directions. "
            "Only a minority of plants show the full matching-lower / tube-shorter / pollen-lower pattern, so the contemporary functional change does not propagate as a uniform multichannel response syndrome."
        ),
        "claim_boundary": (
            "This is a within-source cross-channel concordance audit, not a cross-species causal regression. Species share environments, tube means lack within-site variance, and pollen receipt is open-pollinated observational function. "
            "Do not infer that matching decline caused tube evolution, that tube change caused pollen receipt, or that the eight species are independent boundary experiments."
        ),
    }
    return rows, summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    columns = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--artifact-dir",
        type=Path,
        default=Path("artifacts/hiraiwa_ushimaru_figshare"),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("artifacts/hiraiwa_ushimaru_figshare/cross_channel_concordance"),
    )
    args = parser.parse_args()

    rows, summary = build_audit(
        read_csv(args.artifact_dir / "species_response" / "trait_matching_contrasts_pollen_targets.csv"),
        read_csv(args.artifact_dir / "species_response" / "pollen_receipt_contrasts.csv"),
        read_csv(args.artifact_dir / "tube_morphology" / "tube_contrasts_pollen_targets.csv"),
    )
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "cross_channel_concordance.csv", rows)
    (args.out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
