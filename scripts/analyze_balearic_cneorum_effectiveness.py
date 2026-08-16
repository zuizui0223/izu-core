#!/usr/bin/env python3
"""Analyze source-native Cneorum tricoccon pollination/exclusion data.

Pollination census, flower-selection interactions, exclusion outcomes, breeding
rows and seed-dispersal/germination rows remain distinct source channels. The
main lizard-exclusion contrast follows the source-defined Control (open) versus
Insects (lizards excluded; insect pollination retained) labels. The additional
raw `Lizards` label is reported but not assigned a biological exclusion mapping
unless separately source-locked.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


def read_semicolon(path: Path) -> list[dict[str, str]]:
    raw = path.read_bytes()
    text = None
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        raise ValueError(f"cannot decode {path}")
    return list(csv.DictReader(text.splitlines(), delimiter=";"))


def number(value):
    text = str(value or "").strip().replace(",", ".")
    if not text or text.upper() == "NA":
        return None
    try:
        return float(text)
    except ValueError:
        return None


def mean(values):
    vals = [float(v) for v in values if v is not None]
    return sum(vals) / len(vals) if vals else None


def group_plant_means(rows, treatment):
    selected = [r for r in rows if r["Type"] == "Ex" and r["Treatment"] == treatment]
    plants = defaultdict(list)
    for row in selected:
        plants[row["Plant.ID"]].append(row)
    plant_fruit = []
    plant_seed = []
    for rr in plants.values():
        plant_fruit.append(mean(number(r["Mature fruits "]) for r in rr))
        plant_seed.append(mean(number(r["Seeds"]) for r in rr))
    return {
        "n_flower_rows": len(selected),
        "n_plants": len(plants),
        "weighted_flower_fruit_set": mean(number(r["Mature fruits "]) for r in selected),
        "weighted_seeds_per_flower": mean(number(r["Seeds"]) for r in selected),
        "mean_plant_fruit_set": mean(plant_fruit),
        "mean_plant_seeds_per_flower": mean(plant_seed),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("artifacts/balearic_cneorum_effectiveness/files"))
    parser.add_argument("--out", type=Path, default=Path("artifacts/balearic_cneorum_effectiveness/analysis/summary.json"))
    args = parser.parse_args()

    census = read_semicolon(args.data_dir / "Pollination_censues_2015_16.csv")
    selection = read_semicolon(args.data_dir / "Flower_selection_database_15_16.csv")
    exclusion = read_semicolon(args.data_dir / "Exclusions.csv")
    germination = read_semicolon(args.data_dir / "Germination_15_16.csv")
    dispersal = read_semicolon(args.data_dir / "Seed_dispersal_censuses.csv")

    census_minutes = sum(number(r["CensusTime"]) or 0 for r in census)
    lizard_visits = sum(number(r["TLvisits"]) or 0 for r in census)
    insect_visits = sum(number(r["Ivisits"]) or 0 for r in census)
    lizard_flowers = sum(number(r["TTflowers"]) or 0 for r in census)
    insect_flowers = sum(number(r["ITflowers"]) or 0 for r in census)

    selection_groups = {}
    for label in sorted({r["Pollinator"] for r in selection}):
        rr = [r for r in selection if r["Pollinator"] == label]
        total = sum(number(r["TF"]) or 0 for r in rr)
        herm = sum(number(r["HF"]) or 0 for r in rr)
        selection_groups[label] = {
            "interaction_rows": len(rr),
            "total_flowers_contacted": total,
            "mean_flowers_contacted_per_interaction": total / len(rr) if rr else None,
            "hermaphrodite_flowers_contacted": herm,
            "hermaphrodite_fraction_of_contacted_flowers": herm / total if total else None,
        }

    exclusion_summary = {label: group_plant_means(exclusion, label) for label in ("Control", "Insects", "Lizards")}
    control = exclusion_summary["Control"]
    insects = exclusion_summary["Insects"]
    main_contrast = {
        "source_mapping": "Control=open pollination; Insects=lizards excluded while insect pollination remains, as defined by the primary article's lizard-exclusion experiment.",
        "insects_only_to_open_weighted_fruit_set_ratio": insects["weighted_flower_fruit_set"] / control["weighted_flower_fruit_set"],
        "insects_only_to_open_weighted_seed_ratio": insects["weighted_seeds_per_flower"] / control["weighted_seeds_per_flower"],
        "open_minus_insects_only_mean_plant_fruit_set": control["mean_plant_fruit_set"] - insects["mean_plant_fruit_set"],
        "open_minus_insects_only_mean_plant_seeds_per_flower": control["mean_plant_seeds_per_flower"] - insects["mean_plant_seeds_per_flower"],
        "reading": "Excluding lizards while retaining insect pollination lowers both fruit-set and seed-per-flower summaries in the source-native experiment, consistent with an additional lizard pollination contribution."
    }

    germination_values = [number(r["Germination"]) for r in germination]
    germination_values = [v for v in germination_values if v is not None]

    report = {
        "schema_version": "1.0",
        "source_id": "fuster_traveset_2020_cneorum_tricoccon_double_mutualism",
        "article_doi": "10.1111/oik.06659",
        "dataset_doi": "10.5061/dryad.2ngf1vhj1",
        "study_system": "Cneorum tricoccon x Podarcis lilfordi, Balearic Islands",
        "scale": {
            "pollination_census_rows": len(census),
            "pollination_census_plants": len({r["ID"] for r in census}),
            "pollination_census_hours": census_minutes / 60.0,
            "flower_selection_interactions": len(selection),
            "exclusion_all_rows": len(exclusion),
            "exclusion_pollination_rows": sum(r["Type"] == "Ex" for r in exclusion),
            "breeding_rows_kept_separate": sum(r["Type"] == "Br" for r in exclusion),
            "germination_rows": len(germination),
            "seed_dispersal_census_rows": len(dispersal),
        },
        "pollination_census": {
            "lizard_visits": int(lizard_visits),
            "insect_visits": int(insect_visits),
            "lizard_flowers_contacted": int(lizard_flowers),
            "insect_flowers_contacted": int(insect_flowers),
            "lizard_visits_per_census_hour": lizard_visits / (census_minutes / 60.0),
            "insect_visits_per_census_hour": insect_visits / (census_minutes / 60.0),
            "lizard_flowers_contacted_per_visit": lizard_flowers / lizard_visits if lizard_visits else None,
            "insect_flowers_contacted_per_visit": insect_flowers / insect_visits if insect_visits else None,
        },
        "flower_selection_interactions": selection_groups,
        "pollination_exclusion": {
            "by_source_label": exclusion_summary,
            "main_control_vs_insects_only_contrast": main_contrast,
            "additional_lizards_label_boundary": "The raw Type=Ex treatment label `Lizards` is summarized numerically but is not assigned an exclusion meaning here because that mapping is not needed for the source-defined Control-versus-Insects lizard-exclusion contrast and has not been separately source-locked."
        },
        "separate_seed_dispersal_context": {
            "germination_rows": len(germination),
            "rows_with_binary_germination": len(germination_values),
            "germinated": int(sum(v == 1 for v in germination_values)),
            "observed_germination_fraction": sum(v == 1 for v in germination_values) / len(germination_values) if germination_values else None,
            "seed_dispersal_census_rows": len(dispersal),
            "reading": "These rows concern the second mutualistic function and are not mixed into the pollination-effectiveness contrast."
        },
        "source_level_result": "The primary article concludes that Podarcis lilfordi is a legitimate pollinator of Cneorum tricoccon; lizards contacted more flowers and selected more hermaphrodite flowers than insects, and lizard access increased fruit and seed set relative to insect-only pollination.",
        "analysis_unit_boundary": "Census sessions and flower-level exclusion rows are repeated observations, not independent island replicates. Plant-level exclusion means are therefore reported separately from flower-weighted summaries; Control and Insects are separate treatment groups, not treated as paired plants.",
        "claim_boundary": "This is contemporary within-system pollination-effectiveness evidence. Pollination and seed-dispersal functions remain separate. This distinct Balearic plant experiment is not a distinct archipelago from Malva arborea and does not establish historical floral evolution or a universal island dependency coefficient."
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
