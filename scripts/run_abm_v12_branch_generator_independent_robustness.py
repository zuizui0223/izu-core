from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.run_constraint_mechanism_abm_v12_residual_trait_causes import build as build_v12

ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "data/design/abm_v12_branch_generator_independent_robustness_freeze.json"
DEFAULT_OUT = ROOT / "data/results/abm_v12_branch_generator_independent_robustness.json"


def load_freeze() -> dict:
    return json.loads(FREEZE.read_text(encoding="utf-8"))


def classify(result: dict) -> str:
    full = result["full_residual_summary"]
    initial = result["drop_one_ablation"]["initial_trait_heterogeneity"]
    adjustment = result["drop_one_ablation"]["trait_adjustment_heterogeneity"]
    assurance = result["drop_one_ablation"]["assurance_ceiling_heterogeneity"]

    if (
        initial["mixed_sign_run_fraction_ablated"] > 0.0
        or initial["mean_within_run_branching_balance_ablated"] > 0.0
    ):
        return "contradicted_minimal_generator"
    if full["mixed_sign_run_fraction"] == 0.0:
        return "inconclusive_no_branching_in_independent_block"
    if (
        adjustment["mixed_sign_run_fraction_ablated"] > 0.0
        or assurance["mixed_sign_run_fraction_ablated"] > 0.0
    ):
        return "replicated_minimal_generator"
    return "inconclusive_other_residual_ablations_also_collapse_branching"


def build() -> dict:
    freeze = load_freeze()
    raw = build_v12(
        replicates=freeze["replicates"],
        n_lineages=freeze["lineages"],
        steps=freeze["steps"],
        seed=freeze["independent_seed"],
    )
    full = raw["full_residual_summary"]
    drop = raw["drop_one_ablation"]
    payload = {
        "analysis": "abm_v12_branch_generator_independent_robustness",
        "schema_version": "1.0",
        "run_date": "2026-08-24",
        "freeze": str(FREEZE.relative_to(ROOT)),
        "seed": freeze["independent_seed"],
        "design": {
            "replicates": freeze["replicates"],
            "lineages": freeze["lineages"],
            "steps": freeze["steps"],
            "saturations": freeze["saturations"],
            "external_targets_loaded": False,
            "empirical_inputs_loaded": False,
        },
        "full_residual": {
            "positive": full["positive"],
            "negative": full["negative"],
            "equal": full["equal"],
            "mixed_sign_run_fraction": full["mixed_sign_run_fraction"],
            "mean_within_run_branching_balance": full["mean_within_run_branching_balance"],
        },
        "drop_one": {
            factor: {
                "mixed_sign_run_fraction": row["mixed_sign_run_fraction_ablated"],
                "mean_within_run_branching_balance": row["mean_within_run_branching_balance_ablated"],
                "paired_branch_sign_changes": row["paired_branch_sign_changes"],
                "paired_branch_sign_change_fraction": row["paired_branch_sign_change_fraction"],
            }
            for factor, row in drop.items()
        },
        "all_residual_factors_off": {
            "mixed_sign_run_fraction": raw["all_residual_factors_off"]["mixed_sign_run_fraction"],
            "mean_within_run_branching_balance": raw["all_residual_factors_off"]["mean_within_run_branching_balance"],
            "within_run_branching_collapsed": raw["all_residual_factors_off"]["within_run_branching_collapsed"],
        },
        "decision": classify(raw),
        "stop_rule_honored": True,
        "claim_boundary": "Independent stochastic replication inside the declared ABM only; no external system was used to select the seed or parameters."
    }
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    payload = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("BEGIN_V12_INDEPENDENT_RESULT")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print("END_V12_INDEPENDENT_RESULT")


if __name__ == "__main__":
    main()
