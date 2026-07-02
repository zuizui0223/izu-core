"""Run adaptive tempered SMC for the five source-level Izu candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.island_multichannel import load_guide_order_constraints
from channel_id.island_source_level import load_source_level_evidence
from channel_id.source_level_tempered_smc import (
    TemperedSMCConfig,
    bridge_order_deltas,
    run_tempered_smc_comparison,
    summarize_tempered_smc,
)


def _row(result) -> dict[str, object]:
    return {
        "scenario": result.scenario,
        "seed": result.seed,
        "particles": result.particles,
        "log_marginal_compatibility": result.log_marginal_compatibility,
        "stages": result.stages,
        "beta_schedule": list(result.beta_schedule),
        "min_incremental_ess": result.min_incremental_ess,
        "mean_incremental_ess": result.mean_incremental_ess,
        "mean_rejuvenation_acceptance": result.mean_rejuvenation_acceptance,
        "included_channels": [channel.value for channel in result.included_channels],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--island-summary", type=Path, default=Path("data/inoue_literature_island_traits.csv"))
    parser.add_argument("--outcrossing", type=Path, default=Path("data/two_breakpoint_evidence/inoue1990_outcrossing.csv"))
    parser.add_argument("--bagging", type=Path, default=Path("data/two_breakpoint_evidence/inoue1988_bagging.csv"))
    parser.add_argument("--flower", type=Path, default=Path("data/two_breakpoint_evidence/inoue1995_flower_length.csv"))
    parser.add_argument("--guide-constraints", type=Path, default=Path("data/guide_direction_constraints.csv"))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--particles", type=int, default=500)
    parser.add_argument("--target-ess-fraction", type=float, default=0.70)
    parser.add_argument("--rejuvenation-steps", type=int, default=1)
    parser.add_argument("--max-tempering-steps", type=int, default=80)
    parser.add_argument("--seeds", type=int, nargs="+", default=(20260702, 20260703, 20260704))
    args = parser.parse_args()

    evidence = load_source_level_evidence(
        island_summary_path=args.island_summary,
        outcrossing_path=args.outcrossing,
        bagging_path=args.bagging,
        flower_path=args.flower,
    )
    constraints = load_guide_order_constraints(args.guide_constraints)
    config = TemperedSMCConfig(
        particles=args.particles,
        target_ess_fraction=args.target_ess_fraction,
        rejuvenation_steps=args.rejuvenation_steps,
        max_tempering_steps=args.max_tempering_steps,
    )
    results = run_tempered_smc_comparison(
        evidence,
        island_summary_path=args.island_summary,
        guide_constraints=constraints,
        config=config,
        seeds=tuple(args.seeds),
    )
    summary = summarize_tempered_smc(results)
    deltas = bridge_order_deltas(results)
    payload = {
        "schema_version": 1,
        "config": {
            "particles": config.particles,
            "target_ess_fraction": config.target_ess_fraction,
            "rejuvenation_steps": config.rejuvenation_steps,
            "max_tempering_steps": config.max_tempering_steps,
        },
        "seeds": list(args.seeds),
        "retained_rows": {
            "outcrossing": len(evidence.outcrossing),
            "bagging": len(evidence.bagging),
            "flower": len(evidence.flower),
            "guide_constraints": len(constraints),
            "region_order": len(evidence.islands),
        },
        "boundary": (
            "Adaptive tempered SMC comparison over the five declared source-level candidates. "
            "All candidates start from their declared priors; the ordinal candidate uses fixed region_order as a proxy, not distance, history, or causal isolation."
        ),
        "rank_summary": summary,
        "bridge_order_deltas": deltas,
        "results": [_row(result) for result in results],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Adaptive tempered SMC: source-level Izu candidates", "", payload["boundary"], "",
        "## Replicate ranking", "",
        "| scenario | replicates | mean log compatibility | SD | rank-one fraction | mean rank | mean stages | min incremental ESS | mean incremental ESS | mean move acceptance |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary:
        lines.append(
            f"| {row['scenario']} | {row['replicates']} | {row['mean_log_marginal_compatibility']:.3f} | "
            f"{row['sd_log_marginal_compatibility']:.3f} | {row['rank_one_fraction']:.3f} | "
            f"{row['mean_rank']:.3f} | {row['mean_stages']:.1f} | {row['minimum_incremental_ess']:.1f} | "
            f"{row['mean_incremental_ess']:.1f} | {row['mean_rejuvenation_acceptance']:.3f} |"
        )
    lines.extend((
        "", "## Isolation-order minus bridge-loss per replicate", "",
        "| seed | order minus bridge | order higher |", "|---:|---:|---|",
    ))
    for row in deltas:
        lines.append(f"| {row['seed']} | {row['order_minus_bridge']:.3f} | {str(row['order_higher']).lower()} |")
    lines.extend((
        "", "## Reading the diagnostics", "",
        "The minimum incremental ESS is intentionally controlled by the target fraction at each temperature step. This is not equivalent to proof of full convergence: compare replicated log-compatibility estimates, stage counts, and resample-move acceptance before interpreting a difference between candidates.",
    ))
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
