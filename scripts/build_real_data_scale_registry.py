#!/usr/bin/env python3
"""Build the current source-native real-data scale registry without pseudoreplication."""
from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out",type=Path,default=ROOT/"data/results/real_data_scale_registry.json")
    args=ap.parse_args()
    h=load("data/predictive_meta/hiraiwa_ushimaru_matching_to_pollen.json")
    se=load("data/results/seychelles_pollination_effectiveness_summary.json")
    sn=load("data/results/seychelles_restoration_network_summary.json")
    g=load("data/results/galapagos_bird_insect_effectiveness_summary.json")
    m=load("data/results/balearic_malva_effectiveness_summary.json")
    l=load("data/results/canary_lotus_effectiveness_summary.json")
    c=load("data/results/balearic_cneorum_effectiveness_summary.json")
    hi=load("data/results/hawaii_native_pollination_summary.json")
    d=load("data/results/dominica_heliconia_selection_summary.json")

    panels=[
      {"panel_id":"izu_hiraiwa_2024","cluster":"izu","plant_taxa_slots":h["fixed_effect_subsets"]["all_eight_sites"]["n_plants"],"scale":{"plant_site_season_cells":h["fixed_effect_subsets"]["all_eight_sites"]["n_cells"],"sites":8,"seasons":5},"depth":["network_structure","trait_matching","pollen_receipt"],"note":"Repeated plant×site×season cells inside one Izu system."},
      {"panel_id":"seychelles_fuster_2020","cluster":"seychelles","plant_taxa_slots":se["scale"]["plant_species"],"scale":{"raw_rows":se["scale"]["raw_rows"],"visual_census_hours":se["scale"]["visual_census_hours"],"single_visit_rows":se["scale"]["single_visit_exclusion_rows"],"breeding_rows":se["scale"]["breeding_treatment_rows"]},"depth":["visitation","contact","single_visit_reproductive_outcome","breeding"],"note":"Three plants in one Seychelles study."},
      {"panel_id":"seychelles_restoration_2017","cluster":"seychelles","plant_taxa_slots":0,"scale":{"site_month_networks":sn["scale"]["network_rows"],"sites":sn["scale"]["sites"],"months":sn["scale"]["months"],"reported_hours":sn["source_contract_context"]["reported_observation_hours"],"reported_visits":sn["source_contract_context"]["reported_pollinator_visits"]},"depth":["network_structure","visitation","restoration_response"],"note":"64 repeated site×month networks; site is treatment-level unit."},
      {"panel_id":"galapagos_effectiveness_2018","cluster":"galapagos","plant_taxa_slots":g["scale"]["census_species"],"scale":{"census_rows":g["scale"]["census_rows"],"fitness_raw_rows":g["scale"]["fitness_raw_rows"],"id_treatment_units":g["scale"]["id_treatment_units"]},"depth":["visitation","fruit_seed_outcomes","fitness_treatments"],"note":"Four focal plants in one Galapagos study."},
      {"panel_id":"balearic_malva_2024","cluster":"balearic","plant_taxa_slots":1,"scale":{"visitor_event_rows":m["scale"]["visitor_event_rows"],"treatment_rows":m["scale"]["treatment_rows"]},"depth":["visitation","contact","autogamy","pollinator_exclusion","fruit_seed_outcomes"],"note":"One Cabrera population."},
      {"panel_id":"canary_lotus_2024","cluster":"canary","plant_taxa_slots":1,"scale":{"exclusion_flower_rows":l["scale"]["exclusion_flower_rows"],"lizards_assayed_for_pollen":l["scale"]["lizards_assayed_for_pollen"],"reproductive_success_plants":l["scale"]["reproductive_success_plants"]},"depth":["visit_legitimacy","pollen_transport","pollinator_exclusion","fruit_set","plant_level_reproduction"],"note":"One Tenerife endemic plant."},
      {"panel_id":"balearic_cneorum_2020","cluster":"balearic","plant_taxa_slots":1,"scale":{"pollination_census_rows":c["scale"]["pollination_census_rows"],"pollination_exclusion_rows":c["scale"]["exclusion_pollination_rows"],"breeding_rows":c["scale"]["breeding_rows_kept_separate"]},"depth":["pollination_census","flower_selection","pollinator_exclusion","fruit_seed_outcomes","breeding"],"note":"Distinct Balearic plant experiment; same cluster as Malva."},
      {"panel_id":"hawaii_native_pollination_2019","cluster":"hawaii","plant_taxa_slots":hi["raw_visitation_scale"]["focal_plant_sheets"],"scale":{"raw_rows":hi["raw_visitation_scale"]["raw_rows"],"observation_sessions":hi["raw_visitation_scale"]["observation_sessions"],"focal_visitor_event_rows":hi["raw_visitation_scale"]["focal_visitor_event_rows"],"flowers_probed":hi["raw_visitation_scale"]["flowers_probed_in_focal_rows"],"reported_observation_hours":hi["source_reported_context"]["flower_observation_hours"]},"depth":["visitation","handling","article_level_bagging_context"],"note":"Eight native plants in one Hawaii ecosystem; raw Dryad lacks treatment table."},
      {"panel_id":"dominica_heliconia_2019","cluster":"lesser_antilles","plant_taxa_slots":1,"scale":{"plant_rows":d["scale"]["plant_rows"],"bird_measurement_rows":d["scale"]["bird_measurement_rows"],"nectar_visit_rows":d["scale"]["nectar_visit_rows"],"post_hurricane_visitor_plant_rows":d["scale"]["post_hurricane_visitor_plant_rows"]},"depth":["floral_morphology","seed_output","visitation","pollinator_morphology","natural_selection_context"],"note":"One Dominica before/after hurricane natural-disturbance system."},
    ]
    clusters=sorted({p["cluster"] for p in panels})
    all_depths=[depth for p in panels for depth in p["depth"]]
    counts={
      "study_panels":len(panels),
      "independent_archipelago_clusters":len(clusters),
      "archipelago_clusters":clusters,
      "plant_taxa_slots_across_panels":sum(p["plant_taxa_slots"] for p in panels),
      "panels_with_pollinator_exclusion_or_bagging_raw":sum(any(x in p["depth"] for x in ["pollinator_exclusion","single_visit_reproductive_outcome"]) for p in panels),
      "panels_with_single_visit_reproductive_outcome":sum("single_visit_reproductive_outcome" in p["depth"] for p in panels),
      "panels_with_direct_pollen_transport":sum("pollen_transport" in p["depth"] for p in panels),
      "panels_with_breeding_or_autogamy_raw":sum(any(x in p["depth"] for x in ["breeding","autogamy"]) for p in panels),
      "panels_with_network_structure":sum("network_structure" in p["depth"] for p in panels),
      "panels_with_source_native_seed_or_fruit_outcomes":sum(any(x in p["depth"] for x in ["fruit_seed_outcomes","fruit_set","seed_output","single_visit_reproductive_outcome"]) for p in panels),
      "panels_with_article_level_dependency_context_only":sum("article_level_bagging_context" in p["depth"] for p in panels),
    }
    report={
      "schema_version":"2.0",
      "scope":"Current source-native quantitative panels in izu-core. Historical focal summaries, qualitative-only evidence and source-blocked candidate systems are not converted into raw-row counts.",
      "counts":counts,
      "panels":panels,
      "counting_rules":[
        "Study panels are not independent archipelagos.",
        "Repeated months, flowers, fruits, visitor events, plant rows and plant×site×season cells are not promoted to independent evolutionary replicates.",
        "Plant-taxa slots are panel memberships, not a deduplicated phylogenetic sample size and not an inferential n.",
        "Different channel row counts remain separate instead of being summed into one pseudo sample size.",
        "Article-level dependency context without source-native treatment rows is counted separately from raw exclusion/breeding evidence."
      ],
      "claim_boundary":"The registry documents real-data scale and evidence depth. More rows inside one experiment improve within-system estimation but do not substitute for additional independent systems."
    }
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(counts,indent=2,ensure_ascii=False))

if __name__=="__main__": main()
