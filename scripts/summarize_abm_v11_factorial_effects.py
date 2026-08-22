from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/results/constraint_mechanism_abm_v11_factorial_branching.json"
OUT = ROOT / "data/results/constraint_mechanism_abm_v11_factorial_summary.json"
FACTORS = ("local_support", "dependency_heterogeneity", "assurance_responsiveness", "partner_effectiveness")


def config_id(config: dict[str, bool]) -> str:
    return "__".join(f"{name}_{'on' if config[name] else 'off'}" for name in FACTORS)


def build(source: dict) -> dict:
    configs = source["all_configurations"]
    all_off_id = config_id({name: False for name in FACTORS})
    all_on_id = source["full_model_config"]
    marginal = {}
    for factor in FACTORS:
        on_rows = [row for row in configs.values() if row["factors"][factor]]
        off_rows = [row for row in configs.values() if not row["factors"][factor]]
        marginal[factor] = {
            "mean_branching_balance_on": mean(row["branching_balance"] for row in on_rows),
            "mean_branching_balance_off": mean(row["branching_balance"] for row in off_rows),
            "mean_branching_balance_on_minus_off": mean(row["branching_balance"] for row in on_rows) - mean(row["branching_balance"] for row in off_rows),
            "mean_mixed_sign_run_fraction_on": mean(row["mixed_sign_run_fraction"] for row in on_rows),
            "mean_mixed_sign_run_fraction_off": mean(row["mixed_sign_run_fraction"] for row in off_rows),
            "mean_mixed_sign_run_fraction_on_minus_off": mean(row["mixed_sign_run_fraction"] for row in on_rows) - mean(row["mixed_sign_run_fraction"] for row in off_rows),
            "mean_positive_fraction_nonzero_on": mean(row["positive_fraction_nonzero"] for row in on_rows if row["positive_fraction_nonzero"] is not None),
            "mean_positive_fraction_nonzero_off": mean(row["positive_fraction_nonzero"] for row in off_rows if row["positive_fraction_nonzero"] is not None),
            "mean_reproductive_delta_on": mean(row["mean_oceanic_minus_mainland_reproduction"] for row in on_rows),
            "mean_reproductive_delta_off": mean(row["mean_oceanic_minus_mainland_reproduction"] for row in off_rows),
        }

    all_off = configs[all_off_id]
    all_on = configs[all_on_id]
    any_two_sided_all_off = all_off["positive"] > 0 and all_off["negative"] > 0
    if any_two_sided_all_off:
        residual = "two_sided_branching_persists_with_all_four_tested_downstream_factors_off"
    else:
        residual = "two_sided_branching_collapses_when_all_four_tested_downstream_factors_are_off"

    return {
        "analysis": "constraint_mechanism_abm_v11_factorial_effect_summary",
        "source_analysis": source["analysis"],
        "status": "post_run_descriptive_summary_of_predeclared_16_factorial_cells",
        "all_on": all_on,
        "all_off": all_off,
        "all_off_residual_branching_decision": residual,
        "marginal_factor_descriptives": marginal,
        "primary_drop_one_results": source["drop_one_ablation"],
        "interpretation_boundary": (
            "All 16 factorial cells were generated prospectively, but these marginal averages and the all-off headline are post-run descriptive summaries. "
            "They do not replace the frozen drop-one diagnostic and do not identify an empirical causal mechanism. If branching persists with all four downstream factors off, the residual source lies in the frozen upstream v4 opportunity/lineage state or in other retained lineage attributes, and requires a separate prospective ablation rather than retrospective tuning."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    source = json.loads(args.source.read_text())
    payload = build(source)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
