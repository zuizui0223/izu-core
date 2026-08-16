#!/usr/bin/env python3
"""Analyze source-native Lotus maculatus effectiveness and dependence data."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import openpyxl


def rows(ws):
    values=list(ws.iter_rows(values_only=True))
    headers=[str(v).strip() for v in values[0]]
    return [dict(zip(headers,row)) for row in values[1:]]


def mean(values):
    vals=[float(v) for v in values if v is not None]
    return sum(vals)/len(vals) if vals else None


def pearson(x,y):
    xx=[float(v) for v in x]; yy=[float(v) for v in y]
    xm=sum(xx)/len(xx); ym=sum(yy)/len(yy)
    num=sum((a-xm)*(b-ym) for a,b in zip(xx,yy))
    den=math.sqrt(sum((a-xm)**2 for a in xx)*sum((b-ym)**2 for b in yy))
    return num/den if den else None


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--xlsx",type=Path,default=Path("artifacts/canary_lotus_effectiveness/files/Dataset_for_statistical_analyses.xlsx")); ap.add_argument("--out",type=Path,default=Path("artifacts/canary_lotus_effectiveness/analysis/summary.json")); args=ap.parse_args()
    wb=openpyxl.load_workbook(args.xlsx,read_only=True,data_only=True)

    exclusion=rows(wb["Visitor-exclusion experiment"])
    treatments={}
    for treatment in sorted({str(r["Treatment"]) for r in exclusion}):
        rr=[r for r in exclusion if str(r["Treatment"])==treatment]
        fruits=sum(int(r["Fruit"] or 0) for r in rr); seeds=sum(int(r["Number of seeds"] or 0) for r in rr)
        treatments[treatment]={"n_flower_rows":len(rr),"n_plants":len({r["Plant_ID"] for r in rr}),"fruits":fruits,"weighted_fruit_set":fruits/len(rr) if rr else None,"seeds":seeds,"mean_seeds_per_flower":seeds/len(rr) if rr else None}

    legitimacy=rows(wb["Legitimacy of flower visits"])
    visitors={}
    for r in legitimacy:
        legit=int(r["Legitimate visits"] or 0); illegit=int(r["Illegitimate visits"] or 0); total=legit+illegit
        visitors[str(r["Flower visitor"])]= {"legitimate":legit,"illegitimate":illegit,"total":total,"legitimate_fraction":legit/total if total else None}

    pollen=rows(wb["Pollen load by lizards"])
    grains=[int(r["Number of pollen grains"] or 0) for r in pollen]
    sorted_grains=sorted(grains)
    if len(grains)%2==0: median=(sorted_grains[len(grains)//2-1]+sorted_grains[len(grains)//2])/2
    else: median=sorted_grains[len(grains)//2]
    pollen_summary={"n_lizards":len(pollen),"positive_pollen_load":sum(v>0 for v in grains),"positive_fraction":sum(v>0 for v in grains)/len(grains),"total_pollen_grains":sum(grains),"mean_pollen_grains":sum(grains)/len(grains),"median_pollen_grains":median,"max_pollen_grains":max(grains)}

    plant=rows(wb["Visits and reproductive success"])
    fruit_sets=[float(r["Number of Fruits"])/float(r["Number Flowers"]) for r in plant]
    visit_fields={
        "Gallotia galloti":"Visits by Gallotia galloti",
        "Lasioglossum arctifrons":"Visits by Lasioglossum arctifrons",
        "Apis mellifera":"Visits by Apis mellifera",
    }
    visit_association={}
    for visitor,field in visit_fields.items():
        vals=[float(r[field] or 0) for r in plant]
        visit_association[visitor]={"total_visits":sum(vals),"pearson_with_plant_fruit_set":pearson(vals,fruit_sets)}
    total_flowers=sum(int(r["Number Flowers"] or 0) for r in plant); total_fruits=sum(int(r["Number of Fruits"] or 0) for r in plant)
    plant_summary={"n_plants":len(plant),"n_sites":len({r["Study site"] for r in plant}),"total_flowers":total_flowers,"total_fruits":total_fruits,"weighted_fruit_set":total_fruits/total_flowers,"mean_plant_fruit_set":mean(fruit_sets),"visit_association":visit_association}
    wb.close()

    report={
        "schema_version":"1.0",
        "source_id":"gonzalez_castro_siverio_2024_lotus_maculatus_effectiveness",
        "article_doi":"10.26786/1920-7603(2024)777",
        "dataset_doi":"10.6084/m9.figshare.25559724",
        "study_system":"Lotus maculatus, Tenerife, Canary Islands",
        "scale":{"exclusion_flower_rows":len(exclusion),"exclusion_plants":len({r['Plant_ID'] for r in exclusion}),"visitor_classes":len(visitors),"lizards_assayed_for_pollen":len(pollen),"reproductive_success_plants":len(plant),"reproductive_success_sites":len({r['Study site'] for r in plant})},
        "visitor_exclusion":{
            "by_treatment":treatments,
            "exclusion_to_control_fruit_set_ratio":treatments["Exclusion"]["weighted_fruit_set"]/treatments["Control"]["weighted_fruit_set"] if treatments["Control"]["weighted_fruit_set"] else None,
            "reading":"Bagging strongly suppresses observed fruit and seed production in this source-native experiment; this is direct reproductive-dependence evidence for the focal Tenerife population."
        },
        "visit_legitimacy":visitors,
        "lizard_pollen_load":pollen_summary,
        "plant_level_visitation_and_reproduction":plant_summary,
        "source_level_result":"The primary study identifies Gallotia galloti as the key pollination agent: lizard visits are legitimate, lizards carry Lotus pollen, and source analyses report plant reproductive success increasing with lizard visitation. Honeybees predominantly rob nectar and Lasioglossum mainly gathers pollen.",
        "analysis_boundary":"The Pearson values are descriptive plant-level alignment diagnostics without site adjustment or causal interpretation; the source's statistical conclusion is retained separately rather than reverse-engineered from a different model.",
        "claim_boundary":"This is contemporary one-island evidence linking handling legitimacy, pollen carriage and strong bagging response. It does not establish historical floral evolution or transport a universal dependency coefficient to Izu."
    }
    args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2,ensure_ascii=False))

if __name__=="__main__": main()
