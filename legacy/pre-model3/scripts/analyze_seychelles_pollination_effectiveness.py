#!/usr/bin/env python3
"""Summarize source-native Seychelles pollination-effectiveness data.

This script deliberately keeps four observational/experimental layers separate:
1) visual-census visitation quantity,
2) per-visit flower-contact behavior,
3) single-visit reproductive outcomes from exclusion experiments, and
4) breeding-system treatment outcomes.

It does not recreate the paper's final QNC x QLC index unless all source-native
subcomponent definitions are explicitly reproduced.  The goal is a transparent,
source-native expansion of the empirical evidence base without inventing a
cross-system causal estimand.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

PLANTS = {
    "Polyscias crassa": {
        "census": "P._crassa_census.csv",
        "contact": "P._crassa_flw_touched.csv",
        "fruit": "P._crassa_fruitset.csv",
        "minutes": "Census Time (min)",
        "flowers": "Flw observed",
        "visit_columns": {"Sunbird": "Sunbird", "Phelsuma": "Phelsuma", "Mabuya": "Mabuya", "Insects": "Insect"},
        "ant_column": "Ants",
        "contact_group": "Pollinator",
        "contact_prop": "Propflwtouched",
        "exclusion_group": "Treatment",
        "breeding_group": "Treatment",
        "green_fruit": "Green fruit",
        "mature_fruit": "Mature fruit",
        "seeds": "Fruit seeds",
    },
    "Syzygium wrightii": {
        "census": "S._wrightii_census.csv",
        "contact": "S._wrightii_flwtouched.csv",
        "fruit": "S._wrightii_fruitset.csv",
        "minutes": "Census Time (min)",
        "flowers": "Flw observed",
        "visit_columns": {"Sunbird": "Sunbird", "Phelsuma": "Phelsuma", "Mabuya": "Mabuya", "Insects": "Insect"},
        "ant_column": "Ants",
        "contact_group": "Pollinator",
        "contact_prop": "Propflwtouched",
        "exclusion_group": "Treatment1",
        "breeding_group": "Treatment1",
        "green_fruit": "Gree0 fruit",
        "mature_fruit": "Mature fruit",
        "seeds": "Fruit seeds",
    },
    "Thespesia populnea": {
        "census": "T._populnea_census.csv",
        "contact": "T._populnea_flw_touched.csv",
        "fruit": "T._populnea_fruitset.csv",
        "minutes": "Census Time",
        "flowers": "FlwObs",
        "visit_columns": {"Insects": "Insects", "Sunbird": "Sunbird", "Fody": "Fody", "Skink": "Skink"},
        "ant_column": None,
        "contact_group": "Pollinator",
        "contact_prop": "PropFlwtouched",
        "exclusion_group": "Treatment",
        "breeding_group": "Treatment",
        "green_fruit": None,
        "mature_fruit": "Fruiting",
        "seeds": "Total seeds",
    },
}

TREATMENT_MAP = {
    "Thespesia populnea": {
        "exclusion": {"B": "Birds", "In": "Insects", "R": "Reptiles"},
        "breeding": {"Aut": "Auto", "C": "Control", "G": "Geitonogamy", "X": "Xenogamy"},
    },
    "Polyscias crassa": {"exclusion": {}, "breeding": {}},
    "Syzygium wrightii": {"exclusion": {}, "breeding": {}},
}

PUBLISHED_HEADLINE = {
    "Thespesia populnea": "flying insects",
    "Polyscias crassa": "Phelsuma geckos",
    "Syzygium wrightii": "sunbirds",
}


def decode_csv(path: Path) -> list[dict[str, str]]:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
        encoding = "utf-8-sig"
    except UnicodeDecodeError:
        text = raw.decode("latin-1")
        encoding = "latin-1"
    rows = list(csv.DictReader(text.splitlines(), delimiter=";"))
    if not rows:
        raise ValueError(f"empty source table: {path}")
    for row in rows:
        row["__encoding__"] = encoding
    return rows


def clean(value: object) -> str:
    return str(value or "").strip()


def number(value: object) -> float | None:
    text = clean(value).replace(",", ".")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def binary(value: object) -> int | None:
    text = clean(value).lower()
    if text in {"y", "yes", "1", "1.0", "true"}:
        return 1
    if text in {"n", "no", "0", "0.0", "false"}:
        return 0
    return None


def wilson(successes: int, n: int, z: float = 1.959963984540054) -> list[float] | None:
    if n <= 0:
        return None
    p = successes / n
    denom = 1.0 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return [max(0.0, center - half), min(1.0, center + half)]


def binary_summary(values: Iterable[int | None]) -> dict[str, object]:
    observed = [int(value) for value in values if value is not None]
    n = len(observed)
    successes = sum(observed)
    return {
        "n_observed": n,
        "successes": successes,
        "proportion": successes / n if n else None,
        "wilson_95": wilson(successes, n),
    }


def numeric_summary(values: Iterable[float | None]) -> dict[str, object]:
    observed = [float(value) for value in values if value is not None]
    if not observed:
        return {"n_observed": 0, "mean": None, "min": None, "max": None}
    return {
        "n_observed": len(observed),
        "mean": sum(observed) / len(observed),
        "min": min(observed),
        "max": max(observed),
    }


def census_summary(rows: list[dict[str, str]], spec: dict[str, object]) -> dict[str, object]:
    minutes_col = str(spec["minutes"])
    flower_col = str(spec["flowers"])
    visit_columns = dict(spec["visit_columns"])
    total_minutes = sum(number(row.get(minutes_col)) or 0.0 for row in rows)
    flower_hours = sum(
        (number(row.get(minutes_col)) or 0.0) / 60.0 * (number(row.get(flower_col)) or 0.0)
        for row in rows
    )
    guilds = {}
    for label, column in visit_columns.items():
        visits = sum(number(row.get(column)) or 0.0 for row in rows)
        guilds[label] = {
            "visits": visits,
            "visits_per_flower_hour": visits / flower_hours if flower_hours else None,
        }
    out: dict[str, object] = {
        "n_censuses": len(rows),
        "total_observation_minutes": total_minutes,
        "total_observation_hours": total_minutes / 60.0,
        "flower_hours": flower_hours,
        "guilds": guilds,
    }
    ant_col = spec.get("ant_column")
    if ant_col:
        disturbed = []
        undisturbed = []
        for row in rows:
            minutes = number(row.get(minutes_col)) or 0.0
            ants = number(row.get(str(ant_col))) or 0.0
            ants_per_30 = ants * 30.0 / minutes if minutes > 0 else ants
            (disturbed if ants_per_30 > 6.0 else undisturbed).append(row)
        def rate(subset: list[dict[str, str]]) -> dict[str, object]:
            denom = sum(
                (number(row.get(minutes_col)) or 0.0) / 60.0 * (number(row.get(flower_col)) or 0.0)
                for row in subset
            )
            visits = sum(
                sum(number(row.get(column)) or 0.0 for column in visit_columns.values())
                for row in subset
            )
            return {
                "n_censuses": len(subset),
                "flower_hours": denom,
                "non_ant_pollinator_visits": visits,
                "visits_per_flower_hour": visits / denom if denom else None,
            }
        d = rate(disturbed); u = rate(undisturbed)
        d_rate = d["visits_per_flower_hour"]; u_rate = u["visits_per_flower_hour"]
        out["ant_disturbance"] = {
            "definition": ">6 ants per standardized 30 min census, matching the primary article",
            "disturbed": d,
            "undisturbed": u,
            "disturbed_to_undisturbed_rate_ratio": d_rate / u_rate if d_rate is not None and u_rate else None,
            "descriptive_only": True,
        }
    return out


def contact_summary(rows: list[dict[str, str]], spec: dict[str, object]) -> dict[str, object]:
    group_col = str(spec["contact_group"])
    prop_col = str(spec["contact_prop"])
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        label = clean(row.get(group_col)) or "unlabeled"
        grouped[label].append(row)
    output = {}
    for label, subset in sorted(grouped.items()):
        output[label] = {
            "n_visit_rows": len(subset),
            "flowers_touched": numeric_summary(number(row.get("Flw touched")) for row in subset),
            "proportion_flowers_touched": numeric_summary(number(row.get(prop_col)) for row in subset),
        }
    return {"n_visit_rows": len(rows), "by_source_pollinator_group": output}


def fruit_binary(row: dict[str, str], column: str | None) -> int | None:
    if not column:
        return None
    return binary(row.get(column))


def treatment_summary(
    rows: list[dict[str, str]],
    *,
    group_col: str,
    mapping: dict[str, str],
    green_col: str | None,
    mature_col: str | None,
    seed_col: str,
) -> dict[str, object]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        raw = clean(row.get(group_col)) or "unlabeled"
        grouped[mapping.get(raw, raw)].append(row)
    output = {}
    for label, subset in sorted(grouped.items()):
        seed_values = [number(row.get(seed_col)) for row in subset]
        output[label] = {
            "n_rows": len(subset),
            "green_fruit": binary_summary(fruit_binary(row, green_col) for row in subset) if green_col else None,
            "mature_or_recorded_fruit": binary_summary(fruit_binary(row, mature_col) for row in subset) if mature_col else None,
            "seed_count": numeric_summary(seed_values),
            "seed_positive": binary_summary(None if value is None else int(value > 0) for value in seed_values),
            "source_pollinator_labels": dict(Counter(clean(row.get("Pollinator")) or "none" for row in subset)),
        }
    return output


def fruitset_summary(rows: list[dict[str, str]], plant: str, spec: dict[str, object]) -> dict[str, object]:
    exclusion = [row for row in rows if clean(row.get("Experiment")) == "Exclusion"]
    breeding = [row for row in rows if clean(row.get("Experiment")) == "Breeding"]
    maps = TREATMENT_MAP[plant]
    exclusion_summary = treatment_summary(
        exclusion,
        group_col=str(spec["exclusion_group"]),
        mapping=maps["exclusion"],
        green_col=spec.get("green_fruit"),
        mature_col=spec.get("mature_fruit"),
        seed_col=str(spec["seeds"]),
    )
    breeding_summary = treatment_summary(
        breeding,
        group_col=str(spec["breeding_group"]),
        mapping=maps["breeding"],
        green_col=spec.get("green_fruit"),
        mature_col=spec.get("mature_fruit"),
        seed_col=str(spec["seeds"]),
    )
    return {
        "n_rows": len(rows),
        "single_visit_exclusion_n": len(exclusion),
        "breeding_treatment_n": len(breeding),
        "single_visit_quality": exclusion_summary,
        "breeding_treatments": breeding_summary,
        "source_labeled_auto_treatment_present": "Auto" in breeding_summary,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("artifacts/seychelles_pollination_effectiveness/files"))
    parser.add_argument("--out", type=Path, default=Path("artifacts/seychelles_pollination_effectiveness/analysis/summary.json"))
    args = parser.parse_args()

    result: dict[str, object] = {
        "schema_version": "1.0",
        "source_id": "fuster_et_al_2020_seychelles_pollination_effectiveness",
        "article_doi": "10.1002/ajb2.1499",
        "dataset_doi": "10.6084/m9.figshare.12029580.v2",
        "study_system": "Mahe, Seychelles",
        "plants": {},
    }
    total_rows = 0
    total_census_hours = 0.0
    total_exclusion = 0
    total_breeding = 0
    for plant, spec in PLANTS.items():
        census_rows = decode_csv(args.data_dir / str(spec["census"]))
        contact_rows = decode_csv(args.data_dir / str(spec["contact"]))
        fruit_rows = decode_csv(args.data_dir / str(spec["fruit"]))
        census = census_summary(census_rows, spec)
        fruit = fruitset_summary(fruit_rows, plant, spec)
        plant_result = {
            "source_rows": {
                "census": len(census_rows),
                "flower_contact": len(contact_rows),
                "pollination_and_breeding": len(fruit_rows),
            },
            "census_quantity": census,
            "flower_contact_behavior": contact_summary(contact_rows, spec),
            "reproductive_experiments": fruit,
            "published_overall_effectiveness_headline": PUBLISHED_HEADLINE[plant],
            "headline_scope": "Primary-article conclusion; this script reports source-native components separately rather than reconstructing the published composite QNC x QLC index.",
        }
        result["plants"][plant] = plant_result
        total_rows += len(census_rows) + len(contact_rows) + len(fruit_rows)
        total_census_hours += float(census["total_observation_hours"])
        total_exclusion += int(fruit["single_visit_exclusion_n"])
        total_breeding += int(fruit["breeding_treatment_n"])

    result["scale"] = {
        "plant_species": len(PLANTS),
        "source_csv_files": len(PLANTS) * 3,
        "raw_rows": total_rows,
        "visual_census_hours": total_census_hours,
        "single_visit_exclusion_rows": total_exclusion,
        "breeding_treatment_rows": total_breeding,
    }
    result["cross_plant_reading"] = (
        "The three plants share the same island landscape but differ in which visitor guild the primary article identifies as most effective. "
        "This is direct evidence against treating visitor identity, interaction frequency, or vertebrate-versus-insect status as a universal proxy for reproductive effectiveness across island plants."
    )
    result["claim_boundary"] = (
        "This is source-native contemporary pollination-function evidence. Visitation quantity, flower contact, single-visit fruit/seed outcomes, and breeding treatments remain separate channels. "
        "The rows are not independent archipelagos, the analysis does not identify historical floral evolution, and the source-labeled Auto treatment is not transported into the Izu dependency estimand without a prespecified compatibility review."
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result["scale"], indent=2))
    for plant, values in result["plants"].items():
        ant = values["census_quantity"].get("ant_disturbance")
        print(plant, "single_visit=", values["reproductive_experiments"]["single_visit_exclusion_n"], "breeding=", values["reproductive_experiments"]["breeding_treatment_n"])
        if ant:
            print("  ant disturbed/undisturbed visit-rate ratio=", ant["disturbed_to_undisturbed_rate_ratio"])


if __name__ == "__main__":
    main()
