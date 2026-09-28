"""Run profile-compatibility optimization for source-level island scenarios."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from channel_id.island_multichannel import load_guide_order_constraints
from channel_id.island_source_level import load_source_level_evidence
from channel_id.source_level_profile import ProfileSearchConfig, profile_source_level_scenarios


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--island-summary", type=Path, default=Path("data/inoue_literature_island_traits.csv"))
    parser.add_argument("--outcrossing", type=Path, default=Path("data/two_breakpoint_evidence/inoue1990_outcrossing.csv"))
    parser.add_argument("--bagging", type=Path, default=Path("data/two_breakpoint_evidence/inoue1988_bagging.csv"))
    parser.add_argument("--flower", type=Path, default=Path("data/two_breakpoint_evidence/inoue1995_flower_length.csv"))
    parser.add_argument("--guide-constraints", type=Path, default=Path("data/guide_direction_constraints.csv"))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--population-size", type=int, default=600)
    parser.add_argument("--iterations", type=int, default=16)
    parser.add_argument("--seed", type=int, default=20260702)
    args = parser.parse_args()

    evidence = load_source_level_evidence(
        island_summary_path=args.island_summary,
        outcrossing_path=args.outcrossing,
        bagging_path=args.bagging,
        flower_path=args.flower,
    )
    constraints = load_guide_order_constraints(args.guide_constraints)
    config = ProfileSearchConfig(population_size=args.population_size, iterations=args.iterations)
    results = profile_source_level_scenarios(evidence, constraints, config=config, seed=args.seed)

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "seed": args.seed,
        "config": asdict(config),
        "boundary": results[0].boundary,
        "results": [
            {
                "scenario": result.scenario.value,
                "profile_rank": result.profile_rank,
                "best_log_likelihood": result.best_log_likelihood,
                "channel_log_likelihood": {
                    "outcrossing": result.best_outcrossing_log_likelihood,
                    "bagging": result.best_bagging_log_likelihood,
                    "flower": result.best_flower_log_likelihood,
                    "guide_order": result.best_guide_log_likelihood,
                },
                "terminal_elite_mean_log_likelihood": result.terminal_elite_mean_log_likelihood,
                "best_draw": asdict(result.best_draw),
            }
            for result in results
        ],
    }
    args.output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Source-level profile compatibility",
        "",
        results[0].boundary,
        "",
        "## Ranking by best compatible parameter region",
        "",
        "| rank | scenario | best log likelihood | terminal elite mean | outcrossing | bagging | flower | guide order |",
        "|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for result in results:
        lines.append(
            f"| {result.profile_rank} | {result.scenario.value} | {result.best_log_likelihood:.3f} | "
            f"{result.terminal_elite_mean_log_likelihood:.3f} | {result.best_outcrossing_log_likelihood:.3f} | "
            f"{result.best_bagging_log_likelihood:.3f} | {result.best_flower_log_likelihood:.3f} | "
            f"{result.best_guide_log_likelihood:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This report asks which restricted model can get closest to all retained observations inside the declared parameter bounds. It is intentionally not a posterior probability or a marginal-evidence ranking. Compare it with the source-level sensitivity report: a scenario can have a sharp profile fit but low prior-volume compatibility, or vice versa.",
        ]
    )
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
