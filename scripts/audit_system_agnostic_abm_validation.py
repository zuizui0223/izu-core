#!/usr/bin/env python3
"""Audit frozen ABM mechanism coverage against admitted island response states.

This is a strict validation harness, not a new ABM layer. It does not fit or
retune any parameter to an island system. It asks which qualitative state
classes are already demonstrated by frozen synthetic outputs, which empirical
predictions have failed, which observed cases constrain the mechanism without
being direct capability targets, and which empirical mechanism mappings remain
unresolved.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GATE = ROOT / "data/design/system_agnostic_multi_system_validation_gate.json"
V11 = ROOT / "data/results/constraint_mechanism_abm_v11_factorial_summary_frozen.json"
V12 = ROOT / "data/results/constraint_mechanism_abm_v12_residual_trait_causes_frozen.json"
HELICONIA = ROOT / "data/results/abm_v12_heliconia_signed_position_test_frozen.json"
DISCRIMINATOR = ROOT / "data/results/island_propagation_buffering_discriminator_v1.json"
NETWORK_BUFFER = ROOT / "data/results/network_context_buffering_capability_robustness_frozen.json"
ASSURANCE_BUFFER = ROOT / "data/results/constraint_mechanism_abm_v14_assurance_buffering_robustness_frozen.json"


def load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def build(gate_path: Path = DEFAULT_GATE) -> dict[str, Any]:
    gate = load(gate_path)
    v11 = load(V11)
    v12 = load(V12)
    heliconia = load(HELICONIA)
    discriminator = load(DISCRIMINATOR)
    network_buffer = load(NETWORK_BUFFER)
    assurance_buffer = load(ASSURANCE_BUFFER)

    full = v12["full_residual_model"]
    mixed_fraction = float(full["mixed_sign_run_fraction"])
    if not 0.0 < mixed_fraction < 1.0:
        raise ValueError("v12 frozen full residual model must contain both mixed and same-sign runs")

    initial_trait = v12["drop_one"]["initial_trait_heterogeneity"]
    local_support = v11["primary_drop_one"]["local_support"]
    effectiveness = v11["primary_drop_one"]["partner_effectiveness"]
    network_summary = network_buffer["independent_summary"]
    if int(network_summary["reproduction_sign_rescue_count"]) <= 0:
        raise ValueError("network-context robustness result must preserve replicated sign rescue")
    if network_buffer["initial_block_comparison"]["independent_sign_rescue_replicated"] is not True:
        raise ValueError("network-context sign rescue must be replicated before exposing a buffering class")

    capabilities = {
        "branches_downstream": {
            "status": "synthetically_demonstrated",
            "evidence": {
                "v12_mixed_sign_run_fraction": mixed_fraction,
                "v12_mean_within_run_branching_balance": full["mean_within_run_branching_balance"],
                "initial_trait_off_mixed_sign_run_fraction": initial_trait["mixed_sign_run_fraction_ablated"],
            },
            "interpretation": "The frozen ABM generates positive and negative lineage responses within the same environmental run, and this collapses when initial trait-position heterogeneity is removed.",
        },
        "same_direction_response": {
            "status": "synthetically_demonstrated_at_sign_class_only",
            "evidence": {
                "v12_nonmixed_run_fraction": 1.0 - mixed_fraction,
                "v12_pooled_positive": full["positive"],
                "v12_pooled_negative": full["negative"],
                "v12_pooled_equal": full["equal"],
            },
            "interpretation": "The frozen architecture can produce run-level same-sign response classes. This does not map a particular physical access mechanism such as Ogasawara into model parameters.",
        },
        "branch_reallocation": {
            "status": "synthetically_demonstrated",
            "evidence": {
                "local_support_paired_sign_changes": local_support["paired_branch_sign_changes"],
                "partner_effectiveness_paired_sign_changes": effectiveness["paired_branch_sign_changes"],
            },
            "interpretation": "Local support and partner effectiveness can change branch identity without being required to generate aggregate branching.",
        },
        "buffered_or_resilient": {
            "status": "synthetically_demonstrated_via_network_context_empirical_mapping_unresolved",
            "evidence": {
                "network_context_initial_sign_rescues": network_buffer["initial_block_comparison"]["initial_reproduction_sign_rescue_count"],
                "network_context_independent_sign_rescues": network_summary["reproduction_sign_rescue_count"],
                "network_context_independent_worsening": network_summary["reproduction_worsening_count"],
                "network_context_sign_rescue_replicated": network_buffer["initial_block_comparison"]["independent_sign_rescue_replicated"],
                "assurance_independent_sign_rescues": assurance_buffer["overall"]["assurance_sign_rescues"],
            },
            "interpretation": "A threshold-free sign-level buffering state is now a replicated synthetic capability of local support/network context, while the route remains bidirectional and no real island system is yet mapped to it. The autonomous-assurance route has robust magnitude attenuation but its sign rescue did not replicate.",
        },
        "reproductive_axes_decouple": {
            "status": "empirical_constraint_not_a_single_synthetic_capability_target",
            "interpretation": "An island system may show stability on one reproductive axis while realized reproductive performance changes on another. Such cases constrain the model architecture but must not be relabelled as whole-reproduction buffering.",
        },
        "counterdirectional_prediction": {
            "status": "empirical_falsification_retained_not_a_capability_target",
            "evidence": {
                "dominica_decision": heliconia.get("decision"),
                "dominica_primary_slope": heliconia.get("primary_result", {}).get("slope"),
            },
            "interpretation": "The frozen Dominica signed-position prediction failed its declared direction and must remain a failure rather than being counted as model flexibility.",
        },
    }

    cases_by_id = {row["case_id"]: row for row in discriminator["cases"]}
    system_results = []
    for target in gate["qualitative_validation_targets"]:
        system_id = target["system_id"]
        target_state = target["target_state"]
        if target_state == "branches_downstream":
            decision = "qualitatively_covered_by_frozen_synthetic_branching"
            limitation = "No system-specific numerical fit or causal identification is implied."
        elif target_state == "propagates_same_direction":
            decision = "sign_class_compatible_mechanism_mapping_not_validated"
            limitation = "The ABM can generate same-sign runs, but the Ogasawara physical-access mechanism has not been mapped prospectively into the frozen model."
        elif target_state in {"buffered_or_resilient", "buffered_or_alternative_mechanism"}:
            decision = "synthetic_buffering_class_available_empirical_mechanism_unmapped"
            limitation = "Network-context sign buffering is a replicated synthetic capability, but assigning it or any other buffer to this empirical system requires the common source-native admission interface."
        elif target_state == "reproductive_axes_decouple":
            decision = "empirical_axis_decoupling_constraint"
            limitation = "Do not collapse stability of a breeding-system index and decline of realized reproductive performance into one propagate/buffer label."
        elif target_state == "counterdirectional_to_frozen_signed_position_prediction":
            decision = "retained_falsification"
            limitation = "Retuning the signed-position mapping is forbidden."
        else:
            decision = "unclassified_target_state"
            limitation = "Target vocabulary is outside the frozen harness."

        empirical_case = cases_by_id.get(system_id)
        if system_id == "izu_multi_taxon_hiraiwa":
            empirical_case = cases_by_id.get("izu_hiraiwa_and_campanula_anchor")
        if system_id == "dominica_heliconia":
            empirical_case = None
        system_results.append({
            "system_id": system_id,
            "target_state": target_state,
            "decision": decision,
            "observed_chain": target["observed_chain"],
            "empirical_case_found_in_discriminator": empirical_case is not None,
            "limitation": limitation,
        })

    n_covered = sum(row["decision"] == "qualitatively_covered_by_frozen_synthetic_branching" for row in system_results)
    n_sign_compatible = sum(row["decision"] == "sign_class_compatible_mechanism_mapping_not_validated" for row in system_results)
    n_buffer_available = sum(row["decision"] == "synthetic_buffering_class_available_empirical_mechanism_unmapped" for row in system_results)
    n_axis_decoupling = sum(row["decision"] == "empirical_axis_decoupling_constraint" for row in system_results)
    n_falsifications = sum(row["decision"] == "retained_falsification" for row in system_results)

    return {
        "analysis": "system_agnostic_abm_multi_system_validation",
        "schema_version": "1.1",
        "status": "strict_harness_complete_after_network_context_buffering_replication_and_guaiacum_axis_correction",
        "input_gate": gate_path.relative_to(ROOT).as_posix(),
        "empirical_inputs_loaded_into_abm": False,
        "parameters_retuned_to_systems": False,
        "campanula_specific_tuning": False,
        "synthetic_state_capabilities": capabilities,
        "system_results": system_results,
        "summary": {
            "systems": len(system_results),
            "qualitatively_covered_branching": n_covered,
            "sign_class_compatible_but_unmapped": n_sign_compatible,
            "synthetic_buffering_class_available_empirical_mechanism_unmapped": n_buffer_available,
            "empirical_axis_decoupling_constraints": n_axis_decoupling,
            "retained_falsifications": n_falsifications,
        },
        "decision": "multi_state_synthetic_class_coverage_improved_network_context_buffering_replicated_two_buffer_cases_unmapped_one_axis_decoupling_constraint_dominica_failure_retained",
        "next_gate": "Use the frozen empirical network-context prediction contract and the common buffer-mechanism admission interface. Seek source-native visitor-specific rate x effectiveness or another matched support/service mapping before assigning local-support buffering to Hawaiʻi, Nicotiana, Guaiacum, or any real system.",
        "claim_boundary": "Qualitative state-class capability is weaker than empirical mechanism validation. Replicated synthetic network buffering does not identify the mechanism in any real island; Guaiacum constrains reproductive-axis separation rather than whole-reproduction buffering; Dominica remains a failed frozen prediction."
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate", type=Path, default=DEFAULT_GATE)
    parser.add_argument("--output", type=Path, default=ROOT / "data/results/system_agnostic_abm_multi_system_validation.json")
    args = parser.parse_args()
    result = build(args.gate)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
