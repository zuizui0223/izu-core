from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V12 = ROOT / "data/results/constraint_mechanism_abm_v12_residual_trait_causes_frozen.json"
ATLAS = ROOT / "data/results/frozen_abm_state_atlas_frozen.json"
SEPARABILITY = ROOT / "data/results/frozen_abm_state_separability_frozen.json"
SYSTEMS = ROOT / "data/results/system_agnostic_abm_multi_system_validation_v2_frozen.json"
DEFAULT_OUT = ROOT / "data/results/simulation_manuscript_figure_data_frozen.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build() -> dict:
    v12 = load(V12)
    atlas = load(ATLAS)
    separability = load(SEPARABILITY)
    systems = load(SYSTEMS)

    full = v12["full_residual_model"]
    drop = v12["drop_one"]
    routes = atlas["synthetic_state_regions"]
    diagnostics = separability["diagnostics"]

    fig2 = [
        {
            "configuration": "full_residual",
            "mixed_sign_run_fraction": full["mixed_sign_run_fraction"],
            "mean_within_run_branching_balance": full["mean_within_run_branching_balance"],
            "paired_sign_changes_vs_full": 0
        },
        {
            "configuration": "initial_trait_heterogeneity_off",
            "mixed_sign_run_fraction": drop["initial_trait_heterogeneity"]["mixed_sign_run_fraction_ablated"],
            "mean_within_run_branching_balance": drop["initial_trait_heterogeneity"]["mean_within_run_branching_balance_ablated"],
            "paired_sign_changes_vs_full": drop["initial_trait_heterogeneity"]["paired_branch_sign_changes"]
        },
        {
            "configuration": "trait_adjustment_heterogeneity_off",
            "mixed_sign_run_fraction": drop["trait_adjustment_heterogeneity"]["mixed_sign_run_fraction_ablated"],
            "mean_within_run_branching_balance": drop["trait_adjustment_heterogeneity"]["mean_within_run_branching_balance_ablated"],
            "paired_sign_changes_vs_full": drop["trait_adjustment_heterogeneity"]["paired_branch_sign_changes"]
        },
        {
            "configuration": "assurance_ceiling_heterogeneity_off",
            "mixed_sign_run_fraction": drop["assurance_ceiling_heterogeneity"]["mixed_sign_run_fraction_ablated"],
            "mean_within_run_branching_balance": drop["assurance_ceiling_heterogeneity"]["mean_within_run_branching_balance_ablated"],
            "paired_sign_changes_vs_full": drop["assurance_ceiling_heterogeneity"]["paired_branch_sign_changes"]
        }
    ]

    network = routes["strong_buffering_via_network_context"]
    assurance = routes["assurance_attenuation_without_robust_sign_rescue"]
    reallocation = routes["branch_reallocation"]
    fig3 = {
        "branch_reallocation": [
            {
                "route": "local_support",
                "paired_sign_change_fraction": reallocation["local_support_paired_sign_change_fraction"]
            },
            {
                "route": "partner_effectiveness",
                "paired_sign_change_fraction": reallocation["partner_effectiveness_paired_sign_change_fraction"]
            },
            {
                "route": "dependency_heterogeneity",
                "paired_sign_change_fraction": 0.0
            }
        ],
        "buffering_and_attenuation": [
            {
                "route": "network_context",
                "sign_rescue_fraction": network["sign_rescue_fraction"],
                "magnitude_attenuation_fraction": network["magnitude_rescue_fraction"],
                "worsening_fraction": network["worsening_fraction"]
            },
            {
                "route": "autonomous_assurance",
                "sign_rescue_fraction": assurance["sign_rescue_fraction"],
                "magnitude_attenuation_fraction": assurance["magnitude_rescue_fraction"],
                "worsening_fraction": None
            }
        ],
        "assurance_by_saturation": [
            {
                "saturation": float(saturation),
                "service_decline_lineages": row["service_decline_lineages"],
                "sign_rescue_fraction": row["assurance_sign_rescues"] / row["service_decline_lineages"],
                "magnitude_attenuation_fraction": row["assurance_magnitude_rescues"] / row["service_decline_lineages"]
            }
            for saturation, row in assurance["by_saturation"].items()
        ]
    }

    fig4_systems = [
        {
            "system_id": row["system_id"],
            "target_state": row["target_state"],
            "decision": row["decision"],
            "generation": row["generation"],
            "mechanism_identified": row.get("mechanism_identified")
        }
        for row in systems["system_results"]
    ]

    fig4_diagnostics = [
        {
            "diagnostic": "mixed_sign_branching_for_trait_heterogeneity",
            "sensitivity": diagnostics["mixed_sign_branching_as_trait_heterogeneity_diagnostic"]["sensitivity"],
            "false_positive_rate": diagnostics["mixed_sign_branching_as_trait_heterogeneity_diagnostic"]["false_positive_rate"],
            "specificity": diagnostics["mixed_sign_branching_as_trait_heterogeneity_diagnostic"]["specificity"]
        },
        {
            "diagnostic": "same_direction_for_trait_uniformity",
            "sensitivity": diagnostics["same_direction_as_trait_uniformity_diagnostic"]["sensitivity"],
            "false_positive_rate": diagnostics["same_direction_as_trait_uniformity_diagnostic"]["false_positive_rate"],
            "specificity": diagnostics["same_direction_as_trait_uniformity_diagnostic"]["specificity"]
        },
        {
            "diagnostic": "sign_rescue_for_network_context_vs_assurance",
            "sensitivity": diagnostics["sign_rescue_as_network_context_vs_assurance_diagnostic"]["network_context_sensitivity"],
            "false_positive_rate": diagnostics["sign_rescue_as_network_context_vs_assurance_diagnostic"]["assurance_false_positive_rate"],
            "specificity": diagnostics["sign_rescue_as_network_context_vs_assurance_diagnostic"]["specificity_against_assurance"]
        },
        {
            "diagnostic": "magnitude_attenuation_for_assurance_vs_network_context",
            "sensitivity": diagnostics["magnitude_attenuation_as_assurance_vs_network_context_diagnostic"]["assurance_sensitivity"],
            "false_positive_rate": diagnostics["magnitude_attenuation_as_assurance_vs_network_context_diagnostic"]["network_context_false_positive_rate"],
            "specificity": diagnostics["magnitude_attenuation_as_assurance_vs_network_context_diagnostic"]["specificity_against_network_context"]
        }
    ]

    return {
        "analysis": "simulation_manuscript_figure_data",
        "schema_version": "1.0",
        "run_date": "2026-08-24",
        "fig2_minimal_branch_generator": fig2,
        "fig3_branch_allocation_buffering_attenuation": fig3,
        "fig4_external_state_and_identifiability": {
            "systems": fig4_systems,
            "diagnostics": fig4_diagnostics,
            "retained_falsification_system": "dominica_heliconia"
        },
        "source_only_from_frozen_results": True,
        "external_systems_used_for_parameter_fitting": False,
        "claim_boundary": "These are plotting tables derived from frozen results. They do not add simulations, fit parameters, or turn qualitative external systems into calibration data."
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
