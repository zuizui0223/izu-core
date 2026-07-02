"""Run source-level uncertainty and Monte Carlo robustness sweeps.

The default nine-setting design varies the three likelihood-scale assumptions
one at a time and jointly at conservative/precise corners. Use `--factorial`
for the full 27-setting grid.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from channel_id.island_multichannel import load_guide_order_constraints
from channel_id.island_source_level import load_source_level_evidence
from channel_id.source_level_sensitivity import (
    default_sensitivity_settings,
    factorial_sensitivity_settings,
    rank_summary,
    run_source_level_sensitivity,
)


FIELDNAMES = (
    "setting_id",
    "seed",
    "scenario",
    "rank",
    "log_marginal_compatibility",
    "max_importance_weight",
    "importance_effective_sample_size",
    "importance_ess_fraction",
    "draws",
    "included_channels",
    "warning",
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--island-summary", type=Path, default=Path("data/inoue_literature_island_traits.csv"))
    parser.add_argument("--outcrossing", type=Path, default=Path("data/two_breakpoint_evidence/inoue1990_outcrossing.csv"))
    parser.add_argument("--bagging", type=Path, default=Path("data/two_breakpoint_evidence/inoue1988_bagging.csv"))
    parser.add_argument("--flower", type=Path, default=Path("data/two_breakpoint_evidence/inoue1995_flower_length.csv"))
    parser.add_argument("--guide-constraints", type=Path, default=Path("data/guide_direction_constraints.csv"))
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--draws", type=int, default=3_000)
    parser.add_argument("--seeds", type=int, nargs="+", default=(20260702, 20260703, 20260704))
    parser.add_argument("--factorial", action="store_true")
    args = parser.parse_args()

    evidence = load_source_level_evidence(
        island_summary_path=args.island_summary,
        outcrossing_path=args.outcrossing,
        bagging_path=args.bagging,
        flower_path=args.flower,
    )
    constraints = load_guide_order_constraints(args.guide_constraints)
    settings = factorial_sensitivity_settings() if args.factorial else default_sensitivity_settings()
    results = run_source_level_sensitivity(
        evidence,
        constraints,
        settings=settings,
        seeds=tuple(args.seeds),
        draws=args.draws,
    )
    summary = rank_summary(results)

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for result in results:
            writer.writerow(
                {
                    "setting_id": result.setting_id,
                    "seed": result.seed,
                    "scenario": result.scenario.value,
                    "rank": result.rank,
                    "log_marginal_compatibility": result.log_marginal_compatibility,
                    "max_importance_weight": result.max_importance_weight,
                    "importance_effective_sample_size": result.importance_effective_sample_size,
                    "importance_ess_fraction": result.importance_ess_fraction,
                    "draws": result.draws,
                    "included_channels": ";".join(channel.value for channel in result.included_channels),
                    "warning": result.warning or "",
                }
            )
    payload = {
        "schema_version": 1,
        "draws": args.draws,
        "seeds": list(args.seeds),
        "setting_count": len(settings),
        "factorial": args.factorial,
        "boundary": (
            "Scenario compatibility sweep over declared observation-scale assumptions. "
            "ESS diagnoses Monte Carlo integration quality; low ESS means posterior "
            "expectations and rankings require more/adapted draws before interpretation."
        ),
        "rank_summary": summary,
        "results": [
            {
                "setting_id": result.setting_id,
                "seed": result.seed,
                "scenario": result.scenario.value,
                "rank": result.rank,
                "log_marginal_compatibility": result.log_marginal_compatibility,
                "max_importance_weight": result.max_importance_weight,
                "importance_effective_sample_size": result.importance_effective_sample_size,
                "importance_ess_fraction": result.importance_ess_fraction,
                "draws": result.draws,
                "warning": result.warning,
            }
            for result in results
        ],
    }
    args.output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Source-level sensitivity and Monte Carlo diagnostics",
        "",
        payload["boundary"],
        "",
        "## Rank stability",
        "",
        "| scenario | rank-one cells | cells | rank-one fraction | mean rank | minimum ESS | median ESS | warning cells |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary:
        lines.append(
            f"| {row['scenario']} | {row['rank_one_count']} | {row['cells']} | "
            f"{row['rank_one_fraction']:.3f} | {row['mean_rank']:.3f} | "
            f"{row['min_ess']:.2f} | {row['median_ess']:.2f} | {row['warning_cells']} |"
        )
    lines.extend(
        [
            "",
            "## Diagnostics rule",
            "",
            "A low ESS does not favor another biological scenario. It says the prior Monte Carlo integral is poorly resolved for that scenario/setting, so the corresponding compatibility score must not be interpreted as numerically stable without more or adapted sampling.",
            "",
            "See the CSV for each setting × seed × scenario cell.",
        ]
    )
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
