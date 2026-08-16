#!/usr/bin/env python3
"""Summarize source-native Galapagos bird/insect pollination-effectiveness data.

Treatment codes in the raw fitness sheets are intentionally retained as opaque
source codes unless their codebook is independently source-locked. Repeated
seed/fruit rows are aggregated within ID x treatment before plant-level
summaries, preventing pseudoreplication.
"""
from __future__ import annotations
import argparse, json, math
from collections import defaultdict
from pathlib import Path
import xlrd

FITNESS_SHEETS=("C. pyriformis","W. ovata","O. echios")


def num(value):
    return float(value) if isinstance(value,(int,float)) else None


def mean(values):
    vals=[v for v in values if v is not None and not math.isnan(v)]
    return sum(vals)/len(vals) if vals else None


def rows(sheet):
    headers=[str(v).strip() for v in sheet.row_values(0)]
    return headers,[dict(zip(headers,sheet.row_values(i))) for i in range(1,sheet.nrows)]


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--xls",type=Path,default=Path("artifacts/galapagos_bird_insect_effectiveness/files/Hervias_Parejo_and_Traveset_-_ajb_-_2018.xls")); ap.add_argument("--out",type=Path,default=Path("artifacts/galapagos_bird_insect_effectiveness/analysis/summary.json")); args=ap.parse_args()
    book=xlrd.open_workbook(args.xls)
    census=book.sheet_by_name("Census of flower visitors"); ch,cr=rows(census)
    by_species={}
    for plant in sorted({str(r["Species"]).strip() for r in cr}):
        pr=[r for r in cr if str(r["Species"]).strip()==plant]
        classes={}
        for cls in ("Birds","Insecta"):
            rr=[r for r in pr if str(r["Class"]).strip()==cls]
            classes[cls]={
                "n_rows":len(rr),
                "sum_visits_to_flower":sum(num(r.get("Nº visits to a flower")) or 0 for r in rr),
                "sum_visited_flowers":sum(num(r.get("Nº of visited flowers")) or 0 for r in rr),
                "mean_FVR":mean(num(r.get("FVR")) for r in rr),
                "bird_exclusion_yes_rows":sum(str(r.get("Flowers with bird exclusion treatment?") or "").strip()=="Yes" for r in rr),
                "bird_exclusion_no_rows":sum(str(r.get("Flowers with bird exclusion treatment?") or "").strip()=="No" for r in rr),
            }
        by_species[plant]={"n_census_rows":len(pr),"by_class":classes}

    fitness={}; raw_fitness_rows=0; total_units=0
    for sheet_name in FITNESS_SHEETS:
        sh=book.sheet_by_name(sheet_name); hdr,dat=rows(sh); raw_fitness_rows+=len(dat)
        units=defaultdict(list)
        for r in dat:
            units[(r["ID"],str(r["treatment"]).strip())].append(r)
        total_units+=len(units)
        by_treatment=defaultdict(list)
        for (ident,treatment),rr in units.items():
            # fields such as fruit_set/seed_set are repeated across seed-level rows;
            # continuous fruit/seed/germination fields are averaged within the unit.
            unit={
                "ID":ident,
                "fruit_set":mean(num(r.get("fruit_set")) for r in rr),
                "seed_set":mean(num(r.get("seed_set")) for r in rr),
                "fruit_length":mean(num(r.get("fruit_length")) for r in rr),
                "fruit_mass":mean(num(r.get("fruit_mass")) for r in rr),
                "perc_germination":mean(num(r.get("perc_germination")) for r in rr),
                "flowers":mean(num(r.get("flowers")) for r in rr),
                "fruits":mean(num(r.get("fruits")) for r in rr),
                "seeds":mean(num(r.get("seeds")) for r in rr),
                "raw_rows":len(rr),
            }
            by_treatment[treatment].append(unit)
        treatments={}
        for code,uu in sorted(by_treatment.items()):
            treatments[code]={
                "n_id_treatment_units":len(uu),
                "raw_rows":sum(u["raw_rows"] for u in uu),
                "mean_fruit_set":mean(u["fruit_set"] for u in uu),
                "mean_seed_set":mean(u["seed_set"] for u in uu),
                "mean_fruit_length":mean(u["fruit_length"] for u in uu),
                "mean_fruit_mass":mean(u["fruit_mass"] for u in uu),
                "mean_seedling_emergence_proportion":mean(u["perc_germination"] for u in uu),
            }
        fitness[sheet_name]={"n_raw_rows":len(dat),"n_unique_individuals":len({key[0] for key in units}),"n_id_treatment_units":len(units),"treatment_codes":treatments}

    report={
        "schema_version":"1.0",
        "source_id":"hervias_parejo_traveset_2018_galapagos_pollination_effectiveness",
        "article_doi":"10.1002/ajb2.1122",
        "dataset_doi":"10.6084/m9.figshare.6142373",
        "study_system":"Santa Cruz, Galapagos",
        "scale":{"census_species":len(by_species),"census_rows":len(cr),"fitness_species_with_nonempty_raw_sheet":len(fitness),"fitness_raw_rows":raw_fitness_rows,"id_treatment_units":total_units},
        "quantitative_component_by_plant":by_species,
        "qualitative_component_by_raw_treatment_code":fitness,
        "missing_raw_fitness_sheet":{"Cordia lutea":"The source workbook contains an empty C. lutea sheet; no fitness values are reconstructed."},
        "source_level_result":"The primary article reports that birds were quantitatively less important than insects, while qualitative fitness components improved when both birds and insects could visit flowers, indicating effective opportunistic bird pollination and more generalized systems than floral syndromes alone suggest.",
        "treatment_code_boundary":"Raw treatment codes A/C/E/NE are retained as opaque labels here because the code-to-exclusion mapping has not yet been source-locked from the supplement. Source-level experimental interpretation is not assigned to individual raw codes until that mapping is verified.",
        "claim_boundary":"Contemporary one-archipelago effectiveness evidence. Repeated fruit/seed rows are collapsed within ID x treatment. The four plant taxa are not four independent archipelagos, and these data do not identify historical floral evolution or direct Izu reproductive dependency."
    }
    args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2,ensure_ascii=False))

if __name__=="__main__": main()
