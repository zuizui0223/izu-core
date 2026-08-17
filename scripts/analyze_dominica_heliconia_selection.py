#!/usr/bin/env python3
"""Analyze the source-native Dominica Heliconia/hummingbird workbook.

The analysis is intentionally descriptive. It summarizes year-specific plant
traits, seed output and visitation, hummingbird culmen length by sex/period, and
the post-hurricane visitor-sex/corolla panel. It does not recreate the primary
paper's selection model or treat the hurricane as randomized.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import xlrd


def clean(value: object) -> str:
    return str(value or "").strip()


def number(value: object) -> float | None:
    if value in (None, ""):
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def mean(values) -> float | None:
    vals = [float(value) for value in values if value is not None]
    return sum(vals) / len(vals) if vals else None


def sample_sd(values) -> float | None:
    vals = [float(value) for value in values if value is not None]
    if len(vals) < 2:
        return None
    avg = sum(vals) / len(vals)
    return math.sqrt(sum((value - avg) ** 2 for value in vals) / (len(vals) - 1))


def pearson(x, y) -> float | None:
    pairs = [(float(a), float(b)) for a, b in zip(x, y) if a is not None and b is not None]
    if len(pairs) < 3:
        return None
    xx = [a for a, _ in pairs]
    yy = [b for _, b in pairs]
    xm = sum(xx) / len(xx)
    ym = sum(yy) / len(yy)
    den = math.sqrt(sum((a - xm) ** 2 for a in xx) * sum((b - ym) ** 2 for b in yy))
    return sum((a - xm) * (b - ym) for a, b in pairs) / den if den else None


def rows(sheet) -> list[dict[str, object]]:
    headers = [clean(value) for value in sheet.row_values(0)]
    return [dict(zip(headers, sheet.row_values(index))) for index in range(1, sheet.nrows)]


def summarize_year(rows_for_year: list[dict[str, object]]) -> dict[str, object]:
    metrics = {
        "corolla_length_mm": "Corolla_length",
        "inflorescences": "Inflorescences",
        "seeds_per_plant": "Seeds_per_Plant",
        "visits_per_hour_per_plant": "Visits_per_hour_per plant",
        "seeds_per_flower": "Seeds_per_Flower",
        "visits_per_hour_per_flower": "Visits_per_hour_per_flower",
    }
    output: dict[str, object] = {
        "n_plant_rows": len(rows_for_year),
        "sites": sorted({clean(row.get("Site")) for row in rows_for_year if clean(row.get("Site"))}),
        "populations": sorted({clean(row.get("Population")) for row in rows_for_year if clean(row.get("Population"))}),
    }
    for label, column in metrics.items():
        vals = [number(row.get(column)) for row in rows_for_year]
        output[label] = {
            "n_observed": sum(value is not None for value in vals),
            "mean": mean(vals),
            "sd": sample_sd(vals),
        }
    corolla = [number(row.get("Corolla_length")) for row in rows_for_year]
    output["raw_alignment"] = {
        "corolla_vs_seeds_per_plant_pearson": pearson(corolla, [number(row.get("Seeds_per_Plant")) for row in rows_for_year]),
        "corolla_vs_seeds_per_flower_pearson": pearson(corolla, [number(row.get("Seeds_per_Flower")) for row in rows_for_year]),
        "corolla_vs_visits_per_hour_per_plant_pearson": pearson(corolla, [number(row.get("Visits_per_hour_per plant")) for row in rows_for_year]),
        "corolla_vs_visits_per_hour_per_flower_pearson": pearson(corolla, [number(row.get("Visits_per_hour_per_flower")) for row in rows_for_year]),
    }
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--xls", type=Path, default=Path("artifacts/dominica_heliconia_selection/files/Temeles_and_Bishop_data.xls")
    )
    parser.add_argument(
        "--out", type=Path, default=Path("artifacts/dominica_heliconia_selection/analysis/summary.json")
    )
    args = parser.parse_args()

    book = xlrd.open_workbook(args.xls)
    plant_rows = rows(book.sheet_by_name("H_wagneriana data"))
    bird_rows = rows(book.sheet_by_name("A jugularis measurements"))
    nectar_rows = rows(book.sheet_by_name("Hummingbird visits and nectar"))
    post_rows = rows(book.sheet_by_name("Visits and plant traits"))

    years = sorted({int(number(row.get("Year"))) for row in plant_rows if number(row.get("Year")) is not None})
    by_year = {str(year): summarize_year([row for row in plant_rows if int(number(row.get("Year"))) == year]) for year in years}

    bird_groups: dict[str, object] = {}
    for period in sorted({clean(row.get("Period")) for row in bird_rows if clean(row.get("Period"))}):
        period_rows = [row for row in bird_rows if clean(row.get("Period")) == period]
        by_sex = {}
        for sex in sorted({clean(row.get("Sex")) for row in period_rows if clean(row.get("Sex"))}):
            selected = [row for row in period_rows if clean(row.get("Sex")) == sex]
            culmen = [number(row.get("Total_culmen length")) for row in selected]
            by_sex[sex] = {"n_birds": len(selected), "mean_culmen_mm": mean(culmen), "sd_culmen_mm": sample_sd(culmen)}
        bird_groups[period] = {"n_birds": len(period_rows), "by_sex": by_sex}

    post_by_visitor = {}
    for visitor in sorted({clean(row.get("Visitor")) for row in post_rows if clean(row.get("Visitor"))}):
        selected = [row for row in post_rows if clean(row.get("Visitor")) == visitor]
        corolla = [number(row.get("Corolla length (mm)")) for row in selected]
        infl = [number(row.get("# Inflorescences")) for row in selected]
        post_by_visitor[visitor] = {
            "n_rows": len(selected),
            "n_sites": len({clean(row.get("Site")) for row in selected if clean(row.get("Site"))}),
            "mean_corolla_length_mm": mean(corolla),
            "sd_corolla_length_mm": sample_sd(corolla),
            "mean_inflorescences": mean(infl),
        }

    nectar_by_visitor = {}
    for visitor in sorted({clean(row.get("Visitor")) for row in nectar_rows if clean(row.get("Visitor"))}):
        selected = [row for row in nectar_rows if clean(row.get("Visitor")) == visitor]
        corolla = [number(row.get("Corolla_Length")) for row in selected]
        volume = [number(row.get("Volume")) for row in selected]
        nectar_by_visitor[visitor] = {
            "n_rows": len(selected),
            "mean_corolla_length_mm": mean(corolla),
            "mean_source_volume": mean(volume),
            "corolla_vs_source_volume_pearson": pearson(corolla, volume),
        }

    report = {
        "schema_version": "1.0",
        "source_id": "temeles_bishop_2019_dominica_heliconia_hurricane_selection",
        "article_doi": "10.1111/btp.12634",
        "dataset_doi": "10.5061/dryad.245p3r0",
        "source_file": {
            "bytes": args.xls.stat().st_size,
            "sha256": hashlib.sha256(args.xls.read_bytes()).hexdigest(),
        },
        "scale": {
            "plant_rows": len(plant_rows),
            "plant_years": years,
            "bird_measurement_rows": len(bird_rows),
            "nectar_visit_rows": len(nectar_rows),
            "post_hurricane_visitor_plant_rows": len(post_rows),
        },
        "plant_response_by_year": by_year,
        "hummingbird_morphology_by_period_and_sex": bird_groups,
        "post_hurricane_visitor_x_plant_traits": post_by_visitor,
        "hummingbird_visit_x_source_volume": nectar_by_visitor,
        "source_level_selection_context": (
            "The primary article reports no directional selection on corolla length before Hurricane Maria and "
            "directional selection favoring shorter corollas after the hurricane as male A. jugularis became the "
            "dominant visitor. That source model conclusion is not reconstructed from the descriptive summaries here."
        ),
        "analysis_unit_boundary": (
            "Plant rows, captured/measured birds and visitor-labelled rows are different source-native units and are "
            "not pooled into one sample size. Pearson values are descriptive within-year alignments, not selection "
            "gradients or causal effects."
        ),
        "claim_boundary": (
            "This before/after hurricane study is observational natural-disturbance evidence. Seed output, visitation, "
            "bird morphology and corolla traits can be compared descriptively, but the analysis does not recreate the "
            "primary selection model, establish experimental reproductive dependency, or identify historical island "
            "colonization effects."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
