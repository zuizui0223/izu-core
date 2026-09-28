from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/preregistered_global_oceanic_network_sample_v1.json"
DORE = ROOT / "data/results/dore2021_oceanic_island_candidate_summary.json"
IZU = ROOT / "config/hiraiwa_ushimaru_figshare_source.json"
YONGXING = ROOT / "config/wanshan_yongxing_dryad_source.json"
OUT = ROOT / "data/results/global_oceanic_validation_release_gate_v1.json"


def build_gate() -> dict:
    design = json.loads(DESIGN.read_text())
    dore = json.loads(DORE.read_text())
    izu = json.loads(IZU.read_text())
    yongxing = json.loads(YONGXING.read_text())

    strata = []
    for row in dore["admitted_candidate_systems_pending_final_geology_and_matrix_gate"]:
        systems = []
        for system in row["systems"]:
            detail = dore["candidate_system_details"][system]
            systems.append({
                "system": system,
                "source_family": "Dore_global_compilation",
                "independence_state": "independent_source_system_candidate",
                "sampling_effort_state": "source_numeric_sampling_effort_complete" if detail["sampling_effort_complete"] else "sampling_effort_incomplete",
                "matrix_state": "source_database_traceability_present_but_byte_level_matrix_gate_pending",
                "geography_state": "source_labeled_oceanic_candidate_pending_common_global_island_attribute_lock",
                "final_admission": False,
            })
        strata.append({
            "stratum": row["stratum"],
            "systems": systems,
            "candidate_two_system_requirement_met": len(systems) >= 2,
            "fully_admitted_two_system_requirement_met": False,
        })

    yctx = yongxing["source_reported_site_context"]["Yongxing"]
    nw_systems = [
        {
            "system": "Izu archipelago",
            "source_family": izu["source_id"],
            "independence_state": "independent_multi_island_sampling_program",
            "matrix_state": "source_native_figshare_interaction_tables_retrievable_by_existing_acquisition_workflow",
            "sampling_effort_state": "standardized_site_x_season_sampling_block_proxy; numeric observation hours not exposed in current archived table",
            "geography_state": "source_native island distance_and_area columns available for five Izu islands; common global-island attribute lock still required for cross-source fit",
            "final_admission": False,
        },
        {
            "system": "Yongxing / Xisha",
            "source_family": yongxing["source_id"],
            "independence_state": "independent_oceanic_coral_island_sampling_program",
            "matrix_state": "source_native_weighted_visitation_matrix_acquired_and_reanalysed",
            "sampling_effort_state": "visitation_rate_standardized_by_flowers_observed_and_censuses",
            "geography_state": {
                "origin": yctx["island_origin"],
                "distance_to_source_km": yctx["distance_to_source_km"],
                "area_km2": yctx["area_km2"],
                "source_reference": yctx["source_reference"],
                "common_global_island_attribute_lock_required": True,
            },
            "final_admission": False,
        },
    ]
    strata.append({
        "stratum": "NW / western Pacific",
        "systems": nw_systems,
        "candidate_two_system_requirement_met": True,
        "fully_admitted_two_system_requirement_met": False,
    })

    candidate_strata = sum(x["candidate_two_system_requirement_met"] for x in strata)
    admitted_strata = sum(x["fully_admitted_two_system_requirement_met"] for x in strata)
    minimum = 4
    return {
        "schema_version": "1.0",
        "analysis": "preregistered_global_oceanic_validation_release_gate",
        "selection_phase": "outcome_blind_candidate_freeze_before_named_system_ABM_fit",
        "preregistered_minimum_strata_required": minimum,
        "candidate_strata_with_two_independent_systems": candidate_strata,
        "fully_admitted_strata_with_two_independent_systems": admitted_strata,
        "candidate_geographic_minimum_met": candidate_strata >= minimum,
        "balanced_global_quantitative_fit_released": admitted_strata >= minimum,
        "candidate_sample_frozen": candidate_strata >= minimum,
        "frozen_candidate_strata": strata,
        "common_geography_source_gate": {
            "dataset": "Weigelt, Jetz & Kreft 2013 global island physical/bioclimatic data",
            "doi": "10.5061/dryad.fv94v",
            "required_fields": ["distance_to_mainland", "area", "elevation"],
            "rule": "Use one common island-attribute definition across frozen systems; do not substitute study sampling area for island area.",
        },
        "fit_release_blockers": [
            "Byte/source-native matrix trace must be completed for the three Dore candidate strata rather than relying on database-availability flags alone.",
            "Oceanic-island geology/name matching must be locked to the common island-attribute source for every frozen system.",
            "Izu cross-source effort treatment must remain a declared standardized sampling-block proxy; raw visit totals must not be pooled as if observation hours were known.",
        ],
        "next_gate": "Acquire and name-match the common Weigelt global island attribute table, complete byte-level matrix traceability for frozen systems, then run leave-one-system-out ABM predictions without changing the frozen system list or selecting a saturation value post hoc.",
        "forbidden_post_freeze_actions": design["forbidden_selection_criteria"] + [
            "replace a frozen system because its ABM fit is poor",
            "use held-out network outcomes to choose the distance-to-constraint mapping",
        ],
        "claim_boundary": "Four geographic strata are now available at the outcome-blind candidate level, so the candidate list can be frozen. This does not release the quantitative global ABM fit: final matrix/geology/effort gates remain explicit and no named-system ABM fit has been inspected for candidate selection.",
    }


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(build_gate(), indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
