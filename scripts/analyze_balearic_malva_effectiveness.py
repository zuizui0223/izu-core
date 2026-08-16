#!/usr/bin/env python3
"""Analyze source-native Malva arborea pollination effectiveness data."""
from __future__ import annotations
import argparse, csv, json, math
from collections import defaultdict
from pathlib import Path

TREATMENTS={
    "TC":"control_open",
    "TA":"autogamy_all_pollinators_excluded",
    "TEA":"bird_exclusion_insects_and_lizards_allowed",
    "TEL":"lizard_exclusion_insects_and_birds_allowed",
}


def read_csv(path: Path):
    raw=path.read_bytes()
    for enc in ("utf-8-sig","latin-1"):
        try: text=raw.decode(enc); break
        except UnicodeDecodeError: continue
    return list(csv.DictReader(text.splitlines()))


def num(value):
    text=str(value or "").strip().replace(",",".")
    if not text or text.upper()=="NA": return None
    return float(text)


def mean(values):
    vals=[v for v in values if v is not None]
    return sum(vals)/len(vals) if vals else None


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--data-dir",type=Path,default=Path("artifacts/balearic_malva_effectiveness/files")); ap.add_argument("--out",type=Path,default=Path("artifacts/balearic_malva_effectiveness/analysis/summary.json")); args=ap.parse_args()
    fruit=read_csv(args.data_dir/"Fruit and seed set.csv")
    fvr=read_csv(args.data_dir/"FVR.csv")

    visitor={}
    for group in sorted({row["class"] for row in fvr}):
        rows=[r for r in fvr if r["class"]==group]
        visitor[group]={
            "n_event_rows":len(rows),
            "visits":sum(num(r["n_visits"]) or 0 for r in rows),
            "flowers_contacted":sum(num(r["n_flower_contacted"]) or 0 for r in rows),
            "mean_standardized_flower_contact":mean(num(r["n_flower_contacted_std"]) for r in rows),
            "mean_standardized_FVR":mean(num(r["FVR_std"]) for r in rows),
        }

    treatments={}
    for code,label in TREATMENTS.items():
        rows=[r for r in fruit if r["treatment"]==code]
        buds=sum(int(num(r["n_buds"]) or 0) for r in rows); fruits=sum(int(num(r["n_fruits"]) or 0) for r in rows)
        treatments[label]={
            "source_code":code,
            "n_rows":len(rows),
            "n_individuals":len({r["ID"] for r in rows}),
            "buds":buds,
            "fruits":fruits,
            "weighted_fruit_set":fruits/buds if buds else None,
            "mean_row_fruit_set":mean(num(r["fruit_set"]) for r in rows),
            "mean_seed_count":mean(num(r["n_seeds"]) for r in rows),
            "n_seed_count_observed":sum(num(r["n_seeds"]) is not None for r in rows),
            "mean_seed_length":mean(num(r["seed_length"]) for r in rows),
            "n_seed_length_observed":sum(num(r["seed_length"]) is not None for r in rows),
        }

    control=treatments["control_open"]["weighted_fruit_set"]
    auto=treatments["autogamy_all_pollinators_excluded"]["weighted_fruit_set"]
    report={
        "schema_version":"1.0",
        "source_id":"robles_et_al_2024_malva_arborea_pollination_effectiveness",
        "article_doi":"10.1093/aobpla/plae010",
        "dataset_doi":"10.6084/m9.figshare.25204958",
        "study_system":"Cabrera Grand, Balearic Islands",
        "focal_plant":"Malva arborea",
        "scale":{"visitor_event_rows":len(fvr),"treatment_rows":len(fruit),"treatment_codes":sorted(TREATMENTS)},
        "quantitative_component":{"source_definition":"number of visits and number of flowers contacted; source article compares insects, birds and lizards","by_visitor_class":visitor},
        "qualitative_component":{"source_treatment_mapping":TREATMENTS,"by_treatment":treatments},
        "reproductive_assurance_context":{
            "autogamy_weighted_fruit_set":auto,
            "control_weighted_fruit_set":control,
            "autogamy_to_control_ratio":auto/control if control else None,
            "reading":"Autogamy produces substantial fruit set in this island population but does not match the open-control weighted fruit set; reproductive assurance is present but incomplete on this observed outcome."
        },
        "source_level_result":"The primary article reports insects as the most frequent visitors, with birds and lizards less frequent; control flowers generally had higher qualitative fitness than exclusion treatments, and autogamy demonstrates self-pollination capacity.",
        "claim_boundary":"Contemporary one-population pollination-effectiveness evidence. Raw standardized visitation/contact variables and exclusion-treatment outcomes are retained separately. The autogamy treatment is direct reproductive-assurance evidence for Malva arborea on Cabrera, but it is not numerically transported to the Izu dependency estimand."
    }
    args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2,ensure_ascii=False))

if __name__=="__main__": main()
