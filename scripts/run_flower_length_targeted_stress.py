"""Run high-precision tempered-SMC stress tests for one declared flower set."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.flower_length_comparability import build_flower_length_sets
from channel_id.island_multichannel import load_guide_order_constraints
from channel_id.island_source_level import load_source_level_evidence
from channel_id.source_level_tempered_smc import (
    TemperedSMCConfig,
    bridge_order_deltas,
    run_tempered_smc_comparison,
    summarize_tempered_smc,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--set-id", required=True)
    parser.add_argument("--island-summary", type=Path, default=Path("data/inoue_literature_island_traits.csv"))
    parser.add_argument("--outcrossing", type=Path, default=Path("data/two_breakpoint_evidence/inoue1990_outcrossing.csv"))
    parser.add_argument("--bagging", type=Path, default=Path("data/two_breakpoint_evidence/inoue1988_bagging.csv"))
    parser.add_argument("--flower", type=Path, default=Path("data/two_breakpoint_evidence/inoue1995_flower_length.csv"))
    parser.add_argument("--guide-constraints", type=Path, default=Path("data/guide_direction_constraints.csv"))
    parser.add_argument("--particles", type=int, default=750)
    parser.add_argument("--target-ess-fraction", type=float, default=0.70)
    parser.add_argument("--rejuvenation-steps", type=int, default=1)
    parser.add_argument("--seeds", type=int, nargs="+", default=tuple(range(20260710, 20260718)))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    evidence = load_source_level_evidence(
        island_summary_path=args.island_summary,
        outcrossing_path=args.outcrossing,
        bagging_path=args.bagging,
        flower_path=args.flower,
    )
    selected = next((row for row in build_flower_length_sets(evidence, args.flower) if row.set_id == args.set_id), None)
    if selected is None:
        raise SystemExit(f"unknown flower set: {args.set_id}")
    constraints = load_guide_order_constraints(args.guide_constraints)
    config = TemperedSMCConfig(
        particles=args.particles,
        target_ess_fraction=args.target_ess_fraction,
        rejuvenation_steps=args.rejuvenation_steps,
    )
    results = run_tempered_smc_comparison(
        selected.evidence,
        island_summary_path=args.island_summary,
        guide_constraints=constraints,
        config=config,
        seeds=tuple(args.seeds),
    )
    summary = summarize_tempered_smc(results)
    deltas = bridge_order_deltas(results)
    positive = sum(bool(row["order_higher"]) for row in deltas)
    payload = {
        "schema_version": 1,
        "set_id": selected.set_id,
        "description": selected.description,
        "retained_labels": list(selected.retained_labels),
        "excluded_labels": list(selected.excluded_labels),
        "config": {
            "particles": config.particles,
            "target_ess_fraction": config.target_ess_fraction,
            "rejuvenation_steps": config.rejuvenation_steps,
            "seeds": list(args.seeds),
        },
        "rank_summary": list(summary),
        "bridge_order_deltas": list(deltas),
        "order_higher_count": positive,
        "order_higher_fraction": positive / len(deltas),
        "boundary": (
            "Targeted numerical replication for a predeclared flower-row leverage set. "
            "It tests Monte Carlo stability after removing one source row; it does not "
            "turn that row into a causal mechanism or estimate unreported experiment effects."
        ),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Targeted flower-row leverage stress test", "", payload["boundary"], "",
        f"- set: `{selected.set_id}`",
        f"- retained rows: {', '.join(selected.retained_labels)}",
        f"- excluded rows: {', '.join(selected.excluded_labels)}",
        f"- order higher than bridge: {positive}/{len(deltas)} ({payload['order_higher_fraction']:.3f})",
        "", "| seed | order minus bridge | order higher |", "|---:|---:|---|",
    ]
    for row in deltas:
        lines.append(f"| {row['seed']} | {float(row['order_minus_bridge']):.3f} | {str(row['order_higher']).lower()} |")
    lines.extend((
        "", "## Candidate rank summary", "",
        "| scenario | mean compatibility | SD | rank-one fraction | mean rank | min incremental ESS |", "|---|---:|---:|---:|---:|---:|",
    ))
    for row in summary:
        lines.append(
            f"| {row['scenario']} | {float(row['mean_log_marginal_compatibility']):.3f} | "
            f"{float(row['sd_log_marginal_compatibility']):.3f} | {float(row['rank_one_fraction']):.3f} | "
            f"{float(row['mean_rank']):.3f} | {float(row['minimum_incremental_ess']):.1f} |"
        )
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
