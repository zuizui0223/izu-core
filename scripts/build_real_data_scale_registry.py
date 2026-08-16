#!/usr/bin/env python3
"""Build an auditable registry of the current source-native real-data panels.

Scale dimensions are deliberately kept separate. Raw rows, plants, sites,
site-month networks, flowers, treatment units and independent archipelagos are
not summed into one pseudo sample size.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "data/results/real_data_scale_registry.json")
    args = parser.parse_args()

    hiraiwa = load("data/predictive_meta/hiraiwa_ushimaru_matching_to_pollen.json")
    sey_eff = load("data/results/seychelles_pollination_effectiveness_summary.json")
    sey_net = load("data/results/seychelles_restoration_network_summary.json")
    gal = load("data/results/galapagos_bird_insect_effectiveness_summary.json")
    malva = load("data/results/balearic_malva_effectiveness_summary.json")
    lotus = load("data/results/canary_lotus_effectiveness_summary.json")
    cneorum = load("data/results/balearic_cneorum_effectiveness_summary.json")

    panels = [
        {
            "panel_id": "izu_hiraiwa_ushimaru_2024",
            "archipelago_cluster": "izu",
            "study_id": "hiraiwa_ushimaru_2024",
            "plant_taxa": hiraiwa["fixed_effect_subsets"]["all_eight_sites"]["n_plants"],
            "scale": {
                "plant_site_season_cells": hiraiwa["fixed_effect_subsets"]["all_eight_sites"]["n_cells"],
                "sites": hiraiwa["fixed_effect_subsets"]["all_eight_sites"]["n_sites"],
                "seasons": hiraiwa["fixed_effect_subsets"]["all_eight_sites"]["n_seasons"],
            },
            "channels": ["trait_matching", "pollen_receipt"],
            "direct_exclusion": False,
            "single_visit_outcome": False,
            "pollen_transport": False,
            "breeding_or_autogamy": False,
            "network_structure": True,
            "independence_note": "Plant x site x season cells are repeated observational units inside one Izu system; taxa are not independent boundary experiments.",
        },
        {
            "panel_id": "seychelles_fuster_2020_effectiveness",
            "archipelago_cluster": "seychelles",
            "study_id": "fuster_kaiser_bunbury_traveset_2020",
            "plant_taxa": sey_eff["scale"]["plant_species"],
            "scale": {
                "raw_rows": sey_eff["scale"]["raw_rows"],
                "visual_census_hours": sey_eff["scale"]["visual_census_hours"],
                "single_visit_exclusion_rows": sey_eff["scale"]["single_visit_exclusion_rows"],
                "breeding_treatment_rows": sey_eff["scale"]["breeding_treatment_rows"],
            },
            "channels": ["visitation", "flower_contact", "single_visit_reproductive_outcome", "breeding_treatment"],
            "direct_exclusion": True,
            "single_visit_outcome": True,
            "pollen_transport": False,
            "breeding_or_autogamy": True,
            "network_structure": False,
            "independence_note": "Three plants are one Seychelles study system, not three independent archipelagos.",
        },
        {
            "panel_id": "seychelles_kaiser_bunbury_2017_restoration",
            "archipelago_cluster": "seychelles",
            "study_id": "kaiser_bunbury_et_al_2017",
            "plant_taxa": None,
            "scale": {
                "site_month_network_rows": sey_net["scale"]["network_rows"],
                "sites": sey_net["scale"]["sites"],
                "months": sey_net["scale"]["months"],
                "restored_sites": sey_net["scale"]["treatment_sites"]["Restored"],
                "unrestored_sites": sey_net["scale"]["treatment_sites"]["Unrestored"],
                "reported_observation_hours": sey_net["source_contract_context"]["reported_observation_hours"],
                "reported_pollinator_visits": sey_net["source_contract_context"]["reported_pollinator_visits"],
                "reported_unique_links": sey_net["source_contract_context"]["reported_unique_links"],
            },
            "channels": ["visitation", "network_size", "nestedness", "connectance", "restoration_response"],
            "direct_exclusion": False,
            "single_visit_outcome": False,
            "pollen_transport": False,
            "breeding_or_autogamy": False,
            "network_structure": True,
            "independence_note": "The 64 rows are repeated 8 sites x 8 months; site is the treatment-level unit. This is the same Seychelles archipelago cluster as the three-plant panel.",
        },
        {
            "panel_id": "galapagos_hervias_parejo_2018_effectiveness",
            "archipelago_cluster": "galapagos",
            "study_id": "hervias_parejo_traveset_2018",
            "plant_taxa": gal["scale"]["census_species"],
            "scale": {
                "census_rows": gal["scale"]["census_rows"],
                "fitness_species_with_raw_data": gal["scale"]["fitness_species_with_nonempty_raw_sheet"],
                "fitness_raw_rows": gal["scale"]["fitness_raw_rows"],
                "id_treatment_units": gal["scale"]["id_treatment_units"],
            },
            "channels": ["bird_insect_visitation", "fruit_set", "seed_set", "fruit_traits", "seedling_emergence"],
            "direct_exclusion": True,
            "single_visit_outcome": False,
            "pollen_transport": False,
            "breeding_or_autogamy": False,
            "network_structure": False,
            "independence_note": "Four plant taxa belong to one Galapagos study system; Cordia lutea has census but no nonempty raw fitness sheet.",
        },
        {
            "panel_id": "balearic_malva_2024_effectiveness",
            "archipelago_cluster": "balearic",
            "study_id": "robles_et_al_2024",
            "plant_taxa": 1,
            "scale": {
                "visitor_event_rows": malva["scale"]["visitor_event_rows"],
                "treatment_rows": malva["scale"]["treatment_rows"],
                "open_treatment_individuals": malva["qualitative_component"]["by_treatment"]["control_open"]["n_individuals"],
                "autogamy_treatment_individuals": malva["qualitative_component"]["by_treatment"]["autogamy_all_pollinators_excluded"]["n_individuals"],
            },
            "channels": ["visitation", "flower_contact", "autogamy", "pollinator_exclusion", "fruit_set", "seed_traits"],
            "direct_exclusion": True,
            "single_visit_outcome": False,
            "pollen_transport": False,
            "breeding_or_autogamy": True,
            "network_structure": False,
            "independence_note": "One Cabrera population; separate experiment from Cneorum but same Balearic archipelago cluster.",
        },
        {
            "panel_id": "canary_lotus_2024_effectiveness",
            "archipelago_cluster": "canary",
            "study_id": "gonzalez_castro_siverio_2024",
            "plant_taxa": 1,
            "scale": {
                "exclusion_flower_rows": lotus["scale"]["exclusion_flower_rows"],
                "exclusion_plants": lotus["scale"]["exclusion_plants"],
                "lizards_assayed_for_pollen": lotus["scale"]["lizards_assayed_for_pollen"],
                "reproductive_success_plants": lotus["scale"]["reproductive_success_plants"],
                "reproductive_success_sites": lotus["scale"]["reproductive_success_sites"],
            },
            "channels": ["visit_legitimacy", "pollen_carriage", "visitor_exclusion", "fruit_set", "plant_level_visitation_reproduction"],
            "direct_exclusion": True,
            "single_visit_outcome": False,
            "pollen_transport": True,
            "breeding_or_autogamy": False,
            "network_structure": False,
            "independence_note": "One endemic plant on Tenerife; independent Canary archipelago context.",
        },
        {
            "panel_id": "balearic_cneorum_2020_effectiveness",
            "archipelago_cluster": "balearic",
            "study_id": "fuster_traveset_2020_cneorum",
            "plant_taxa": 1,
            "scale": {
                "pollination_census_rows": cneorum["scale"]["pollination_census_rows"],
                "pollination_census_plants": cneorum["scale"]["pollination_census_plants"],
                "pollination_census_hours": cneorum["scale"]["pollination_census_hours"],
                "flower_selection_interactions": cneorum["scale"]["flower_selection_interactions"],
                "pollination_exclusion_rows": cneorum["scale"]["exclusion_pollination_rows"],
                "breeding_rows": cneorum["scale"]["breeding_rows_kept_separate"],
                "germination_rows_separate_channel": cneorum["scale"]["germination_rows"],
            },
            "channels": ["pollination_census", "flower_selection", "lizard_exclusion", "fruit_set", "seed_set", "breeding", "germination_separate"],
            "direct_exclusion": True,
            "single_visit_outcome": False,
            "pollen_transport": False,
            "breeding_or_autogamy": True,
            "network_structure": False,
            "independence_note": "Distinct plant experiment from Malva but the same Balearic archipelago cluster; pollination and seed-dispersal channels remain separate.",
        },
    ]

    archipelagos = sorted({panel["archipelago_cluster"] for panel in panels})
    quantitative_plant_taxa = sum(panel["plant_taxa"] or 0 for panel in panels)
    summary = {
        "schema_version": "1.0",
        "scope": "Source-native quantitative real-data panels with machine-readable scale in the current repository. Historical focal Campanula source summaries and qualitative-only external evidence are not converted into raw-row counts here.",
        "counts": {
            "study_panels": len(panels),
            "independent_archipelago_clusters": len(archipelagos),
            "archipelago_clusters": archipelagos,
            "plant_taxa_slots_across_panels": quantitative_plant_taxa,
            "panels_with_direct_exclusion": sum(panel["direct_exclusion"] for panel in panels),
            "panels_with_single_visit_outcome": sum(panel["single_visit_outcome"] for panel in panels),
            "panels_with_direct_pollen_transport": sum(panel["pollen_transport"] for panel in panels),
            "panels_with_breeding_or_autogamy": sum(panel["breeding_or_autogamy"] for panel in panels),
            "panels_with_network_structure": sum(panel["network_structure"] for panel in panels),
        },
        "panels": panels,
        "counting_rules": [
            "Study panels are not independent archipelagos.",
            "Repeated months, flowers, fruits, visitor events and plant x site x season cells are not promoted to independent evolutionary replicates.",
            "Plant taxa slots are panel memberships, not a deduplicated phylogenetic sample size and not an inferential n.",
            "Different channel row counts are retained separately instead of summed into one pseudo sample size.",
            "Direct exclusion, single-visit outcomes, pollen transport, breeding/autogamy and network structure are distinct evidence depths."
        ],
        "claim_boundary": "The registry documents real-data scale and channel depth only. More rows within one experiment improve estimation inside that experiment but do not substitute for additional independent systems."
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary["counts"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
