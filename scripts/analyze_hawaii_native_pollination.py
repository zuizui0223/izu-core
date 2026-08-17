#!/usr/bin/env python3
"""Summarize the source-native Hawaii native-plant flower-visitation workbook.

The Dryad package contains visitation observations but not the manual flower-
treatment table described in the article. This analysis therefore quantifies
only the raw visitation/handling surface and keeps the published bagging result
as source-level context rather than reconstructing unpublished treatment rows.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import openpyxl

SHEETS = {
    "ARGGLA": ("Argemone glauca", "Common"),
    "BIDMEN": ("Bidens menziesii", "Common"),
    "DUBLIN": ("Dubautia linearis", "Common"),
    "HAPHAP": ("Haplostachys haplostachya", "T&E"),
    "SIDFAL": ("Sida fallax", "Common"),
    "SILLAN": ("Silene lanceolata", "T&E"),
    "STEANG": ("Stenogyne angustifolia", "T&E"),
    "TETARE": ("Tetramolopium arenarium", "T&E"),
}
MISSING_VISITOR_LABELS = {"", "N", "NONE", "UNKNOWN", "?", "N/A", "NA"}


def clean(value: object) -> str:
    return str(value or "").strip()


def yes(value: object) -> bool:
    return clean(value).upper().startswith("Y")


def workbook_rows(worksheet) -> list[dict[str, object]]:
    values = list(worksheet.iter_rows(values_only=True))
    headers = [clean(value) for value in values[0]]
    output = []
    for row in values[1:]:
        if not any(value is not None for value in row):
            continue
        output.append(dict(zip(headers, row)))
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path("artifacts/hawaii_native_pollination")
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("artifacts/hawaii_native_pollination/analysis/summary.json"),
    )
    args = parser.parse_args()

    workbook_path = args.root / "files" / "Pollination_visitation_obs_for_dryad.xlsx"
    readme_path = args.root / "files" / "README_for_Pollination_visitation_obs_for_dryad.docx"
    workbook = openpyxl.load_workbook(workbook_path, read_only=True, data_only=True)

    per_plant: dict[str, object] = {}
    all_focal_labels: Counter[str] = Counter()
    total_raw_rows = 0
    total_sessions = 0
    total_focal_events = 0
    total_flowers_probed = 0.0

    for sheet, (taxon, status) in SHEETS.items():
        rows = workbook_rows(workbook[sheet])
        total_raw_rows += len(rows)
        sessions = {
            (
                clean(row.get("Site")),
                clean(row.get("Date")),
                clean(row.get("Start Time")),
                clean(row.get("Observer")),
            )
            for row in rows
            if clean(row.get("Site"))
            and row.get("Date") is not None
            and row.get("Start Time") is not None
        }
        focal_rows = []
        labels: Counter[str] = Counter()
        flowers_probed = 0.0
        for row in rows:
            label = clean(row.get("Focal individual visitor Spp")).upper()
            if label in MISSING_VISITOR_LABELS:
                continue
            focal_rows.append(row)
            labels[label] += 1
            all_focal_labels[label] += 1
            value = row.get("# flowers probed from top")
            if isinstance(value, (int, float)):
                flowers_probed += float(value)

        record = {
            "sheet": sheet,
            "taxon": taxon,
            "source_status": status,
            "raw_rows": len(rows),
            "observation_sessions": len(sessions),
            "focal_visitor_event_rows": len(focal_rows),
            "unique_raw_focal_visitor_labels": len(labels),
            "flowers_probed_in_focal_rows": flowers_probed,
            "nectar_foraging_yes_rows": sum(yes(row.get("Nectar foraging?")) for row in focal_rows),
            "pollen_collecting_yes_rows": sum(yes(row.get("Pollen collecting?")) for row in focal_rows),
            "pollen_visible_on_body_yes_rows": sum(yes(row.get("Pollen visible on body?")) for row in focal_rows),
            "nectar_robbed_flower_count": sum(
                float(row.get("# flowers nectar robbed") or 0)
                for row in focal_rows
                if isinstance(row.get("# flowers nectar robbed"), (int, float))
            ),
            "top_raw_focal_visitor_labels": [
                {"label": label, "event_rows": count}
                for label, count in labels.most_common(10)
            ],
        }
        per_plant[taxon] = record
        total_sessions += len(sessions)
        total_focal_events += len(focal_rows)
        total_flowers_probed += flowers_probed

    workbook.close()
    report = {
        "schema_version": "1.0",
        "source_id": "aslan_etal_2019_hawaii_native_pollination",
        "article_doi": "10.1002/ajb2.1233",
        "dataset_doi": "10.5061/dryad.tm575v4",
        "source_files": {
            "visitation_workbook": {
                "bytes": workbook_path.stat().st_size,
                "sha256": hashlib.sha256(workbook_path.read_bytes()).hexdigest(),
            },
            "readme": {
                "bytes": readme_path.stat().st_size,
                "sha256": hashlib.sha256(readme_path.read_bytes()).hexdigest(),
            },
        },
        "raw_visitation_scale": {
            "focal_plant_sheets": len(SHEETS),
            "raw_rows": total_raw_rows,
            "observation_sessions": total_sessions,
            "focal_visitor_event_rows": total_focal_events,
            "unique_raw_focal_visitor_labels": len(all_focal_labels),
            "flowers_probed_in_focal_rows": total_flowers_probed,
            "top_raw_focal_visitor_labels": [
                {"label": label, "event_rows": count}
                for label, count in all_focal_labels.most_common(15)
            ],
        },
        "by_plant": per_plant,
        "source_reported_context": {
            "flower_observation_hours": 576.36,
            "reported_non_native_share_of_visits": 0.85,
            "reported_endangered_focal_species": 4,
            "reported_species_with_significant_seed_set_reduction_under_bagging": 6,
            "reading": (
                "These values are article-level source conclusions. The recovered Dryad package contains "
                "raw visitation observations and keys, not the manual flower-treatment table, so species-level "
                "bagging effect sizes are not reconstructed here."
            ),
        },
        "scientific_gain": (
            "Eight native Hawaii plants now contribute source-native visitation/handling rows in one independent "
            "island ecosystem. The raw panel includes large among-plant differences in observed visitor-event depth, "
            "while the article independently reports pollinator dependence for six focal species."
        ),
        "analysis_unit_boundary": (
            "Workbook rows and focal visitor events are repeated observations, not independent plants, studies or "
            "island systems. Raw visitor labels are retained as recorded and may include spelling/synonym variants; "
            "they are not automatically collapsed into species richness."
        ),
        "claim_boundary": (
            "The raw dataset supports visitation and handling summaries only. The published bagging result is retained "
            "as source-level dependency context, not converted into unobserved raw treatment values. Non-native visitor "
            "dominance does not demonstrate equal effectiveness, and contemporary dependence does not establish "
            "historical floral evolution."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
