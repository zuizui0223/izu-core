"""Run the direct-table, source-level Izu scenario comparison.

This is deliberately separate from `run_island_multichannel_analysis.py`.
It restores the already transcribed population/experiment rows rather than
replacing them with a single island midpoint, while still treating the result
as a partial-identification compatibility analysis.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.island_multichannel import EvidenceChannel, load_guide_order_constraints
from channel_id.island_source_level import (
    compare_source_level_scenarios,
    load_source_level_evidence,
    render_markdown,
)


def _as_json(results):
    return [
        {
            "scenario": result.scenario.value,
            "draws": result.draws,
            "log_marginal_compatibility": result.log_marginal_compatibility,
            "mean_log_likelihood": result.mean_log_likelihood,
            "channel_log_likelihood": {
                "outcrossing": result.mean_outcrossing_log_likelihood,
                "bagging": result.mean_bagging_log_likelihood,
                "flower": result.mean_flower_log_likelihood,
                "guide_order": result.mean_guide_log_likelihood,
            },
            "max_importance_weight": result.posterior_best_draw_fraction,
            "included_channels": [channel.value for channel in result.included_channels],
            "boundary": result.boundary,
        }
        for result in results
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--island-summary", type=Path, default=Path("data/inoue_literature_island_traits.csv"))
    parser.add_argument("--outcrossing", type=Path, default=Path("data/two_breakpoint_evidence/inoue1990_outcrossing.csv"))
    parser.add_argument("--bagging", type=Path, default=Path("data/two_breakpoint_evidence/inoue1988_bagging.csv"))
    parser.add_argument("--flower", type=Path, default=Path("data/two_breakpoint_evidence/inoue1995_flower_length.csv"))
    parser.add_argument("--guide-constraints", type=Path, default=Path("data/guide_direction_constraints.csv"))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--draws", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=20260702)
    args = parser.parse_args()

    evidence = load_source_level_evidence(
        island_summary_path=args.island_summary,
        outcrossing_path=args.outcrossing,
        bagging_path=args.bagging,
        flower_path=args.flower,
    )
    constraints = load_guide_order_constraints(args.guide_constraints)
    full = compare_source_level_scenarios(evidence, constraints, draws=args.draws, seed=args.seed)
    ablations = {}
    for omitted in EvidenceChannel:
        retained = tuple(channel for channel in EvidenceChannel if channel is not omitted)
        ablations[omitted.value] = _as_json(
            compare_source_level_scenarios(
                evidence,
                constraints,
                draws=args.draws,
                seed=args.seed,
                included_channels=retained,
            )
        )

    payload = {
        "schema_version": 1,
        "input_files": {
            "island_summary": str(args.island_summary),
            "outcrossing": str(args.outcrossing),
            "bagging": str(args.bagging),
            "flower": str(args.flower),
            "guide_constraints": str(args.guide_constraints),
        },
        "draws": args.draws,
        "seed": args.seed,
        "retained_rows": {
            "outcrossing": len(evidence.outcrossing),
            "bagging": len(evidence.bagging),
            "flower": len(evidence.flower),
            "guide_constraints": len(constraints),
        },
        "boundary": (
            "Direct-table source-level compatibility analysis. The likelihoods use "
            "reported summaries and conservative residual/overdispersion terms; "
            "they do not establish raw-individual sampling, pollinator effectiveness, "
            "or historical causality."
        ),
        "full_evidence": _as_json(full),
        "leave_one_channel_out": ablations,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    markdown = render_markdown(full)
    markdown += "\n## Channel ablation\n\n"
    markdown += "Each ranking omits one channel; rank reversals flag a conclusion that depends materially on the omitted evidence.\n\n"
    for omitted, ranking in ablations.items():
        markdown += f"### Omit `{omitted}`\n\n| rank | scenario | log marginal compatibility |\n|---:|---|---:|\n"
        for rank, row in enumerate(ranking, start=1):
            markdown += f"| {rank} | {row['scenario']} | {row['log_marginal_compatibility']:.3f} |\n"
        markdown += "\n"
    args.output_md.write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
