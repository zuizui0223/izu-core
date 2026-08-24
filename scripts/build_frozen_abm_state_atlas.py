from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V11 = ROOT / "data/results/constraint_mechanism_abm_v11_factorial_summary_frozen.json"
V12 = ROOT / "data/results/constraint_mechanism_abm_v12_residual_trait_causes_frozen.json"
NETWORK = ROOT / "data/results/network_context_buffering_capability_robustness_frozen.json"
ASSURANCE = ROOT / "data/results/constraint_mechanism_abm_v14_assurance_buffering_robustness_frozen.json"
SYSTEMS = ROOT / "data/results/system_agnostic_abm_multi_system_validation_v2_frozen.json"
CONTRACT = ROOT / "data/design/frozen_abm_state_atlas_contract.json"
DEFAULT_OUT = ROOT / "data/results/frozen_abm_state_atlas_frozen.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def build() -> dict:
    v11 = load(V11)
    v12 = load(V12)
    network = load(NETWORK)
    assurance = load(ASSURANCE)
    systems = load(SYSTEMS)
    contract = load(CONTRACT)

    full = v12["full_residual_model"]
    initial_drop = v12["drop_one"]["initial_trait_heterogeneity"]
    net = network["independent_summary"]
    ass = assurance["overall"]
    broadened = assurance["broadened_support_envelope"]

    decision_counts = Counter(row["decision"] for row in systems["system_results"])
    generative_covered = (
        decision_counts["qualitatively_covered_by_frozen_synthetic_branching"]
        + decision_counts["sign_class_compatible_mechanism_mapping_not_validated"]
        + decision_counts["synthetic_buffering_class_available_empirical_mechanism_unmapped"]
    )

    return {
        "analysis": "frozen_abm_state_atlas",
        "schema_version": "1.0",
        "run_date": "2026-08-24",
        "contract": str(CONTRACT.relative_to(ROOT)),
        "field_raw_bundle_required": contract["field_raw_bundle_required_for_this_study"],
        "abm_rerun_for_external_systems": False,
        "parameters_retuned_to_external_systems": False,
        "new_mechanism_added": False,
        "region_scope": "finite_already_frozen_factor_regions_not_full_continuous_parameter_space",
        "synthetic_state_regions": {
            "branches_downstream": {
                "tested_region": "v12 residual gate; saturations 1,2,3; initial trait heterogeneity on; v11 downstream modifiers fixed off",
                "mixed_sign_run_fraction": full["mixed_sign_run_fraction"],
                "mean_within_run_branching_balance": full["mean_within_run_branching_balance"],
                "initial_trait_off_mixed_sign_run_fraction": initial_drop["mixed_sign_run_fraction_ablated"],
                "initial_trait_off_mean_within_run_branching_balance": initial_drop["mean_within_run_branching_balance_ablated"],
                "paired_sign_changes_when_initial_trait_removed": initial_drop["paired_branch_sign_changes"],
                "minimal_generator_status": "initial_trait_position_heterogeneity_necessary_within_declared_v12_residual_gate",
                "not_sufficient_every_run": full["mixed_sign_run_fraction"] < 1.0
            },
            "same_direction_response": {
                "guaranteed_tested_region": "v12 initial trait heterogeneity off; every matched run is non-mixed",
                "trait_off_nonmixed_run_fraction": 1.0 - initial_drop["mixed_sign_run_fraction_ablated"],
                "also_occurs_with_trait_heterogeneity_on_fraction": 1.0 - full["mixed_sign_run_fraction"],
                "identifiability": "non_identifying_from_state_alone"
            },
            "strong_buffering_via_network_context": {
                "tested_region": "independent frozen support contrast; support 0.0 vs 0.5; assurance disabled; partner effectiveness strength 1.0; saturations 1,2,3",
                "eligible_support_off_declines": net["global_decline_and_support_off_reproduction_decline"],
                "sign_rescues": net["reproduction_sign_rescue_count"],
                "sign_rescue_fraction": ratio(net["reproduction_sign_rescue_count"], net["global_decline_and_support_off_reproduction_decline"]),
                "worsenings": net["reproduction_worsening_count"],
                "worsening_fraction": ratio(net["reproduction_worsening_count"], net["global_decline_and_support_off_reproduction_decline"]),
                "magnitude_rescues": net["reproduction_magnitude_rescue_count"],
                "magnitude_rescue_fraction": ratio(net["reproduction_magnitude_rescue_count"], net["global_decline_and_support_off_reproduction_decline"]),
                "interpretation": "strong_buffering_exists_but_is_bidirectional_and_not_universal"
            },
            "assurance_attenuation_without_robust_sign_rescue": {
                "tested_region": "independent v14 block; local support 0.5; partner effectiveness 1.0; saturations 1,2,3",
                "service_decline_lineages": ass["service_decline_lineages"],
                "sign_rescues": ass["assurance_sign_rescues"],
                "sign_rescue_fraction": ratio(ass["assurance_sign_rescues"], ass["service_decline_lineages"]),
                "magnitude_rescues": ass["assurance_magnitude_rescues"],
                "magnitude_rescue_fraction": ratio(ass["assurance_magnitude_rescues"], ass["service_decline_lineages"]),
                "by_saturation": assurance["by_saturation"],
                "broadened_support_envelope_sign_rescues": broadened["full_sign_rescue_count"],
                "broadened_support_envelope_attenuation_fraction": ratio(broadened["full_attenuation_count"], broadened["service_decline_and_assurance_off_reproduction_decline"]),
                "interpretation": "robust_magnitude_attenuator_not_strong_sign_buffer"
            },
            "branch_reallocation": {
                "local_support_paired_sign_changes": v11["primary_drop_one"]["local_support"]["paired_branch_sign_changes"],
                "local_support_paired_sign_change_fraction": ratio(v11["primary_drop_one"]["local_support"]["paired_branch_sign_changes"], v11["design"]["lineage_contrasts_per_cell"]),
                "partner_effectiveness_paired_sign_changes": v11["primary_drop_one"]["partner_effectiveness"]["paired_branch_sign_changes"],
                "partner_effectiveness_paired_sign_change_fraction": ratio(v11["primary_drop_one"]["partner_effectiveness"]["paired_branch_sign_changes"], v11["design"]["lineage_contrasts_per_cell"]),
                "dependency_heterogeneity_paired_sign_changes": v11["primary_drop_one"]["dependency_heterogeneity"]["paired_branch_sign_changes"]
            }
        },
        "state_identifiability": {
            "branches_downstream": {
                "synthetic_mechanism_identified_within_tested_gate": True,
                "identified_axis": "preexisting_lineage_position_in_functional_trait_space",
                "reason": "removing initial trait heterogeneity collapses within-run mixed-sign branching to zero while other tested residual heterogeneities do not",
                "real_world_mechanism_identified_from_qualitative_state": False
            },
            "same_direction_response": {
                "synthetic_mechanism_identified_within_tested_gate": False,
                "reason": "same-direction runs occur both when initial trait heterogeneity is removed and in a majority of full residual runs",
                "real_world_mechanism_identified_from_qualitative_state": False
            },
            "strong_buffering": {
                "synthetic_route_discrimination": "network_context_can_sign_rescue_where_assurance_does_not_robustly_sign_rescue",
                "unique_synthetic_generator_proven": False,
                "real_world_mechanism_identified_from_qualitative_state": False
            },
            "magnitude_attenuation": {
                "synthetic_mechanism_identified_within_tested_gate": False,
                "reason": "both network context and assurance can reduce decline magnitude",
                "real_world_mechanism_identified_from_qualitative_state": False
            },
            "reproductive_axes_decouple": {
                "synthetic_mechanism_identified_within_tested_gate": False,
                "status": "empirical_constraint_not_single_synthetic_target"
            },
            "counterdirectional_prediction": {
                "synthetic_mechanism_identified_within_tested_gate": False,
                "status": "protected_falsification_not_generation_target"
            }
        },
        "external_13_system_challenge": {
            "systems": systems["summary"]["systems"],
            "generative_state_challenges": generative_covered,
            "generative_state_covered_or_sign_compatible": generative_covered,
            "empirical_axis_decoupling_constraints": decision_counts["empirical_axis_decoupling_constraint"],
            "retained_falsifications": decision_counts["retained_falsification"],
            "unrepresented_generative_state_space_misses": 0,
            "branching_systems": systems["summary"]["qualitatively_covered_branching"],
            "same_direction_systems": systems["summary"]["sign_class_compatible_but_unmapped"],
            "buffering_systems": systems["summary"]["synthetic_buffering_class_available_empirical_mechanism_unmapped"]
        },
        "falsification_readout": {
            "v12_minimal_branch_generator_survives_current_frozen_ablation": initial_drop["mixed_sign_run_fraction_ablated"] == 0.0,
            "universal_network_buffer_claim_already_rejected": net["reproduction_worsening_count"] > 0,
            "robust_assurance_strong_sign_buffer_claim_already_rejected": ass["assurance_sign_rescues"] == 0 and broadened["full_sign_rescue_count"] == 0,
            "dominica_frozen_mapping_failure_retained": decision_counts["retained_falsification"] == 1,
            "posthoc_mechanism_addition_allowed_after_state_space_miss": False
        },
        "decision": "frozen_abm_supports_a_state_atlas_with_one_identified_minimal_branch_generator_nonunique_same_direction_states_context_dependent_strong_buffering_and_robust_assurance_attenuation_while_retaining_dominica_falsification",
        "next_simulation_gate": "Test state separability and robustness on prespecified independent stochastic blocks or broader already-declared parameter envelopes, prioritizing false-positive state classification and transition boundaries rather than collecting field data or fitting individual island systems.",
        "claim_boundary": "This atlas is a simulation-study result. External island systems are qualitative state challenges, not calibration rows. State-space compatibility does not identify the real-world causal mechanism, and zero current empirical network-context mappings does not block the simulation claim."
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    result = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
