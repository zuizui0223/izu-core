from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "data/results/chapter2_global_master_manuscript_value_review_audit_20260906.json"
SMALL = ROOT / "data/results/chapter2_small_island_supplement_audit_20260906.json"
BOUNDARY = ROOT / "data/design/hiraiwa_ushimaru_boundary_identifiability.json"
FDQ = ROOT / "data/predictive_meta/hiraiwa_ushimaru_continuous_functional_exposure.json"
MATCH_POLLEN = ROOT / "data/predictive_meta/hiraiwa_ushimaru_matching_to_pollen.json"
CROSS = ROOT / "data/predictive_meta/hiraiwa_ushimaru_cross_channel_concordance.json"
SIGNED = ROOT / "data/results/izu_signed_position_structural_audit_frozen_20260827.json"
PROBOSCIS = ROOT / "data/design/izu_pollinator_proboscis_recovery_status.json"
FIELD = ROOT / "data/design/effective_pollinator_dependency_field_readiness.json"
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
DEFAULT_OUT = ROOT / "data/results/chapter2_izu_final_mechanistic_zoom_audit_20260906.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def audit() -> dict:
    world = load(WORLD)
    small = load(SMALL)
    boundary = load(BOUNDARY)
    fdq = load(FDQ)
    match_pollen = load(MATCH_POLLEN)
    cross = load(CROSS)
    signed = load(SIGNED)
    proboscis = load(PROBOSCIS)
    field = load(FIELD)
    manifest = load(MANIFEST)

    if not world["izu_transition_gate"]["ready_for_final_izu_mechanistic_zoom"]:
        raise RuntimeError("Izu zoom opened before the preregistered world-confrontation gate closed")
    if small["bottleneck_update"]["status"] != "partially_moved_not_closed":
        raise RuntimeError("small-island bottleneck state changed before Izu zoom")

    if boundary["second_boundary_independent_site_replication"] != {
        "pre_boundary_oshima_like_sites": 1,
        "post_boundary_sites": 4,
    }:
        raise RuntimeError("Izu second-boundary geographic replication changed")
    if boundary["identifiability"]["causal_second_boundary_effect_identifiable_from_this_dataset_alone"]:
        raise RuntimeError("Izu boundary was silently promoted to a causal experiment")

    fdq_izu = fdq["fixed_effect_subsets"]["izu_five_islands"]
    fdq_post = fdq["fixed_effect_subsets"]["post_oshima_four_islands"]
    if fdq_izu["fdq_coefficient"] <= 0 or fdq_post["fdq_coefficient"] <= 0:
        raise RuntimeError("Izu FDQ-to-matching direction changed")
    if not fdq["leave_one_site_sensitivity"]["izu_five_islands"]["all_positive"]:
        raise RuntimeError("Izu FDQ-to-matching leave-one-island sign robustness changed")
    if not fdq["leave_one_site_sensitivity"]["post_oshima_four_islands"]["all_positive"]:
        raise RuntimeError("post-Oshima FDQ-to-matching leave-one-island sign robustness changed")

    pollen_izu = match_pollen["fixed_effect_subsets"]["izu_five_islands"]
    pollen_post = match_pollen["fixed_effect_subsets"]["post_oshima_four_islands"]
    if pollen_izu["tm_coefficient"] <= 0 or pollen_post["tm_coefficient"] <= 0:
        raise RuntimeError("average Izu matching-to-pollen direction changed")
    if match_pollen["leave_one_site_sensitivity"]["izu_five_islands"]["all_positive"]:
        raise RuntimeError("Izu matching-to-pollen was silently promoted to island-robust")
    if match_pollen["leave_one_site_sensitivity"]["post_oshima_four_islands"]["all_positive"]:
        raise RuntimeError("post-Oshima matching-to-pollen was silently promoted to island-robust")

    directions = cross["directions"]
    if directions["corrected_trait_matching"] != {"lower_post": 8, "higher_post": 0}:
        raise RuntimeError("cross-channel corrected-matching direction changed")
    if directions["tube_morphology"] != {"shorter_post": 3, "longer_post": 4, "equal": 1}:
        raise RuntimeError("cross-channel tube response changed")
    if directions["pollen_receipt"] != {"lower_post": 4, "higher_post": 4}:
        raise RuntimeError("cross-channel pollen branching changed")

    if signed["raw_matching"]["slope"] <= 0 or not signed["raw_matching"]["all_five_leave_one_island_slopes_positive"]:
        raise RuntimeError("raw signed-position relation changed")
    if signed["null_corrected_matching"]["supported"]:
        raise RuntimeError("background-corrected signed-position target was silently promoted")
    if signed["decision"]["historical_bombus_causation_identified"]:
        raise RuntimeError("historical Bombus causation was silently promoted")

    current_traits = proboscis["current_trait_coverage"]
    if (current_traits["current_named_pollinator_taxa"], current_traits["exact_source_native_numeric_proboscis_mm_recovered"]) != (209, 202):
        raise RuntimeError("Izu proboscis recovery state changed")
    fdq_readiness = field["functional_exposure_readiness"]
    if fdq_readiness["historical_trait_recovery"]["recovered_numeric_proboscis_taxa"] != 202:
        raise RuntimeError("field readiness is stale relative to recovered Izu source traits")
    if field["status"] != "implementation_ready_field_data_missing":
        raise RuntimeError("final Izu audit expects the field implementation to be ready while empirical linked rows remain missing")
    if field["prospective_design_simulation"]["empirical_structure_anchor"]["exact_population_dependency_measurements"] != 0:
        raise RuntimeError("exact population dependency data appeared without a new field admission audit")

    breadth = manifest["world_breadth_extension"]
    claims = manifest["claim_ceiling"]
    boundary_state = (
        breadth["combined_descriptive_research_entries_before_cross_layer_deduplication"],
        breadth["combined_exact_overlap_labels_before_higher_level_archipelago_deduplication"],
        breadth["formal_identifiability_research_entries"],
        claims["external_full_contracts"],
        claims["formal_external_prediction"],
    )
    if boundary_state != (42, 37, 25, "0_of_25", "not_evaluable"):
        raise RuntimeError(f"Izu zoom silently changed manuscript/inference denominators: {boundary_state}")

    return {
        "schema_version": "1.0",
        "status": "pass",
        "entry_gate": {
            "large_island_saturation_met": True,
            "small_island_supplement_complete": True,
            "post_saturation_value_review_complete": True,
            "final_izu_zoom_allowed": True,
        },
        "world_to_izu_bottleneck": {
            "world_after_small_islands": "historical partner arrival can be recovered in special small-island histories, but a matched source-state -> transition -> realized community -> plant-response contract remains unclosed",
            "izu_current_role": "resolves contemporary functional realization and downstream response branching, not the historical transition coordinate",
            "same_core_bottleneck_persists": True,
        },
        "izu_current_evidence": {
            "historical_proboscis_species_level_recovery": "202_of_209_current_named_taxa",
            "exact_site_level_fdq_reconstruction_complete": False,
            "current_functional_exposure_to_matching": {
                "supported": True,
                "izu5_fdq_coefficient": fdq_izu["fdq_coefficient"],
                "post4_fdq_coefficient": fdq_post["fdq_coefficient"],
                "all_izu5_leave_one_island_coefficients_positive": True,
                "all_post4_leave_one_island_coefficients_positive": True,
            },
            "matching_to_pollen": {
                "average_direction_positive": True,
                "izu5_tm_coefficient": pollen_izu["tm_coefficient"],
                "post4_tm_coefficient": pollen_post["tm_coefficient"],
                "leave_one_island_sign_stable": False,
            },
            "response_branching": {
                "shared_targets": cross["n_shared_targets"],
                "corrected_matching_lower": 8,
                "tube_shorter": 3,
                "tube_longer": 4,
                "tube_equal": 1,
                "pollen_lower": 4,
                "pollen_higher": 4,
                "full_matching_lower_tube_shorter_pollen_lower": cross["concordance"]["matching_lower_tube_shorter_pollen_lower_n"],
            },
            "signed_position": {
                "raw_slope": signed["raw_matching"]["slope"],
                "raw_ci95": signed["raw_matching"]["ci95"],
                "raw_all_leave_one_island_positive": True,
                "null_corrected_supported": False,
                "exact_island_center_order_uniquely_identified": False,
            },
            "second_boundary_replication": {
                "oshima_bridge_sites": 1,
                "post_boundary_sites": 4,
                "causal_boundary_effect_identifiable": False,
            },
        },
        "still_missing_in_izu": {
            "direct_historical_partner_loss": False,
            "direct_historical_partner_arrival_replacement_in_same_focal_transition": False,
            "direct_effective_dependency_same_tagged_populations": False,
            "matched_single_visit_pollen_to_mature_seed_chain": False,
            "independent_bridge_state_geographic_replication": False,
            "temporal_pre_post_transition_with_matched_plant_response": False,
            "field_data_status": field["status"],
        },
        "final_mechanistic_resolution": {
            "resolved_now": [
                "continuous contemporary pollinator functional structure predicts corrected trait matching within Izu and within the post-Oshima subset",
                "translation from matching to pollen receipt is weaker and network-state conditional",
                "a shared decline in corrected matching branches into shorter, longer or unchanged tubes and higher or lower pollen receipt",
                "the precise island-center geometry and historical Bombus-causation reading are not identified",
            ],
            "single_highest_value_next_measurement": "a tagged-population transition panel linking visitor identity/proboscis and zero-visit effort to SVD, open/bagged/outcross reproduction and mature seed, repeated across a true transition or independently replicated bridge-state exposure",
            "do_not_spend_next_effort_on": [
                "more cross-sectional island examples after the preregistered world saturation condition",
                "more synthetic parameter tuning as the main line",
                "more species or seasons at the single Oshima bridge site while calling them independent boundary replicates",
                "inferring effective dependency from floral morphology or visitor-group labels",
            ],
        },
        "claim_boundary": {
            "historical_bombus_causation_identified": False,
            "causal_oshima_post_boundary_identified": False,
            "formal_external_prediction_reopened": False,
            "full_world_contracts": "0_of_25_frozen_formal_audit",
            "active_descriptive_breadth_mutated": False,
        },
        "decision": "world_confrontation_saturated_and_izu_contemporary_mechanism_resolved_as_far_as_existing_data_allow; next empirical gain requires linked transition/dependency field data rather than further cross-sectional expansion",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    payload = audit()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
