from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.state_separability import diagnostic_from_frequencies

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "data/results/frozen_abm_state_atlas_frozen.json"
DEFAULT_OUT = ROOT / "data/results/frozen_abm_state_separability_frozen.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build() -> dict:
    atlas = load(ATLAS)
    states = atlas["synthetic_state_regions"]

    branching = states["branches_downstream"]
    same = states["same_direction_response"]
    network = states["strong_buffering_via_network_context"]
    assurance = states["assurance_attenuation_without_robust_sign_rescue"]
    reallocation = states["branch_reallocation"]

    branching_diag = diagnostic_from_frequencies(
        state="mixed_sign_branching",
        mechanism_present="initial_trait_heterogeneity_on",
        mechanism_absent_or_alternative="initial_trait_heterogeneity_off",
        present_frequency=branching["mixed_sign_run_fraction"],
        absent_frequency=branching["initial_trait_off_mixed_sign_run_fraction"],
    )
    same_diag = diagnostic_from_frequencies(
        state="same_direction_response",
        mechanism_present="initial_trait_uniformity",
        mechanism_absent_or_alternative="initial_trait_heterogeneity_on",
        present_frequency=same["trait_off_nonmixed_run_fraction"],
        absent_frequency=same["also_occurs_with_trait_heterogeneity_on_fraction"],
    )
    sign_rescue_diag = diagnostic_from_frequencies(
        state="strong_sign_rescue",
        mechanism_present="network_context_support",
        mechanism_absent_or_alternative="autonomous_assurance_route",
        present_frequency=network["sign_rescue_fraction"],
        absent_frequency=assurance["sign_rescue_fraction"],
    )
    attenuation_diag = diagnostic_from_frequencies(
        state="magnitude_attenuation",
        mechanism_present="autonomous_assurance_route",
        mechanism_absent_or_alternative="network_context_support",
        present_frequency=assurance["magnitude_rescue_fraction"],
        absent_frequency=network["magnitude_rescue_fraction"],
    )

    local_reallocation_sensitivity = reallocation["local_support_paired_sign_change_fraction"]
    partner_reallocation_fpr = reallocation["partner_effectiveness_paired_sign_change_fraction"]

    by_saturation = {}
    for saturation, row in assurance["by_saturation"].items():
        n = row["service_decline_lineages"]
        by_saturation[saturation] = {
            "service_decline_lineages": n,
            "sign_rescue_fraction": row["assurance_sign_rescues"] / n if n else 0.0,
            "magnitude_attenuation_fraction": row["assurance_magnitude_rescues"] / n if n else 0.0,
            "state": "attenuation_without_sign_rescue"
        }

    return {
        "analysis": "frozen_abm_state_separability",
        "schema_version": "1.0",
        "run_date": "2026-08-24",
        "parent_atlas": str(ATLAS.relative_to(ROOT)),
        "external_targets_used_for_classifier_training": False,
        "new_simulation_parameters_selected_from_external_outcomes": False,
        "diagnostics": {
            "mixed_sign_branching_as_trait_heterogeneity_diagnostic": {
                "sensitivity": branching_diag["sensitivity"],
                "false_negative_rate": branching_diag["false_negative_rate"],
                "false_positive_rate": branching_diag["false_positive_rate"],
                "specificity": branching_diag["specificity"],
                "interpretation": "high_specificity_low_sensitivity_within_v12_residual_gate"
            },
            "same_direction_as_trait_uniformity_diagnostic": {
                "sensitivity": same_diag["sensitivity"],
                "false_negative_rate": same_diag["false_negative_rate"],
                "false_positive_rate": same_diag["false_positive_rate"],
                "specificity": same_diag["specificity"],
                "interpretation": "nonmixed_state_is_not_mechanistically_identifying"
            },
            "sign_rescue_as_network_context_vs_assurance_diagnostic": {
                "network_context_sensitivity": sign_rescue_diag["sensitivity"],
                "false_negative_rate_with_network_context": sign_rescue_diag["false_negative_rate"],
                "assurance_false_positive_rate": sign_rescue_diag["false_positive_rate"],
                "specificity_against_assurance": sign_rescue_diag["specificity"],
                "interpretation": "high_specificity_low_sensitivity_for_network_context_against_tested_assurance_route"
            },
            "magnitude_attenuation_as_assurance_vs_network_context_diagnostic": {
                "assurance_sensitivity": attenuation_diag["sensitivity"],
                "network_context_false_positive_rate": attenuation_diag["false_positive_rate"],
                "specificity_against_network_context": attenuation_diag["specificity"],
                "interpretation": "poorly_separable_because_both_routes_commonly_attenuate_declines"
            },
            "paired_sign_reallocation_as_local_support_vs_partner_effectiveness_diagnostic": {
                "local_support_sign_change_fraction": local_reallocation_sensitivity,
                "partner_effectiveness_sign_change_fraction": partner_reallocation_fpr,
                "difference": local_reallocation_sensitivity - partner_reallocation_fpr,
                "interpretation": "local_support_is_stronger_branch_allocator_under_direct_synthetic_intervention_but_passive_real_world_state_does_not_identify_it"
            }
        },
        "transition_boundaries": {
            "initial_trait_heterogeneity_on_to_off": {
                "from_mixed_sign_run_fraction": branching["mixed_sign_run_fraction"],
                "to_mixed_sign_run_fraction": branching["initial_trait_off_mixed_sign_run_fraction"],
                "boundary_readout": "within_run_branching_collapses_at_tested_trait_uniformity_intervention"
            },
            "assurance_across_saturations_1_2_3": {
                "by_saturation": by_saturation,
                "boundary_readout": "no_transition_to_strong_sign_buffering_detected_across_tested_saturations"
            },
            "network_context_support_off_to_on": {
                "sign_rescue_fraction": network["sign_rescue_fraction"],
                "worsening_fraction": network["worsening_fraction"],
                "boundary_readout": "support_transition_is_lineage_specific_and_bidirectional_not_monotonic"
            }
        },
        "observation_to_inference_rules": [
            {
                "observation": "mixed positive and negative lineage responses within one matched upstream run",
                "allowed_inference": "supports preexisting trait-position heterogeneity as the necessary tested v12 branch generator",
                "forbidden_inference": "does not identify the real-world trait axis or local-support mechanism"
            },
            {
                "observation": "all lineages respond in the same direction",
                "allowed_inference": "compatible with the frozen model",
                "forbidden_inference": "cannot infer trait uniformity because 58.3% of full heterogeneity-on runs are also nonmixed"
            },
            {
                "observation": "service decline becomes nonnegative reproduction under a context change",
                "allowed_inference": "network context has this synthetic capability whereas the tested assurance route lacks robust sign rescue",
                "forbidden_inference": "cannot infer that a real island is buffered by network context without a source-native mapping"
            },
            {
                "observation": "decline magnitude is reduced but sign remains negative",
                "allowed_inference": "compatible with multiple frozen routes",
                "forbidden_inference": "cannot distinguish assurance from network context from attenuation alone"
            },
            {
                "observation": "external state not represented by any predeclared frozen class",
                "allowed_inference": "record a state-space miss",
                "forbidden_inference": "do not add or retune a mechanism after seeing the miss"
            }
        ],
        "decision": "state_observations_are_asymmetrically_informative_mixed_sign_and_sign_rescue_are_specific_but_insensitive_while_same_direction_and_magnitude_attenuation_are_nonidentifying",
        "paper_level_consequence": "The simulation study should report state-space coverage and diagnostic asymmetry rather than claiming one-to-one inversion from observed island state to causal mechanism.",
        "next_gate": "Use these frozen observation-to-inference rules to construct the manuscript result/falsification table and, only if additional simulation is needed, prespecify independent stochastic blocks that target the low-sensitivity diagnostics without using external outcomes to select parameters.",
        "claim_boundary": "Sensitivity and false-positive rates are conditional frequencies inside different declared synthetic interventions, not population-level diagnostic accuracies for natural islands. They quantify model observability, not empirical causal inference."
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    payload = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
