"""Run source-level uncertainty sweeps with the ordinal island-order proxy."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from statistics import mean

from channel_id.island_multichannel import load_guide_order_constraints
from channel_id.island_source_level import load_source_level_evidence
from channel_id.source_level_isolation_order_diagnostics import isolation_order_sensitivity
from channel_id.source_level_sensitivity import (
    default_sensitivity_settings,
    factorial_sensitivity_settings,
    run_source_level_sensitivity,
)

FIELDNAMES = (
    "setting_id", "seed", "scenario", "rank", "log_marginal_compatibility",
    "max_importance_weight", "importance_effective_sample_size",
    "importance_ess_fraction", "draws", "included_channels", "warning",
)


def _warning(ess: float, fraction: float) -> str | None:
    if ess < 10.0:
        return "importance_ess_lt_10"
    if fraction < 0.01:
        return "importance_ess_lt_1_percent"
    return None


def _rerank(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, int], list[dict[str, object]]] = {}
    for row in rows:
        groups.setdefault((str(row["setting_id"]), int(row["seed"])), []).append(row)
    ranked: list[dict[str, object]] = []
    for key in sorted(groups):
        for rank, row in enumerate(sorted(groups[key], key=lambda item: float(item["log_marginal_compatibility"]), reverse=True), start=1):
            ranked.append({**row, "rank": rank})
    return ranked


def _summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    by_scenario: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        by_scenario.setdefault(str(row["scenario"]), []).append(row)
    summary = []
    for scenario, values in by_scenario.items():
        ess = sorted(float(row["importance_effective_sample_size"]) for row in values)
        summary.append({
            "scenario": scenario,
            "cells": len(values),
            "rank_one_count": sum(int(row["rank"]) == 1 for row in values),
            "rank_one_fraction": mean(int(row["rank"]) == 1 for row in values),
            "mean_rank": mean(int(row["rank"]) for row in values),
            "min_ess": min(ess),
            "median_ess": ess[len(ess) // 2],
            "warning_cells": sum(row["warning"] is not None for row in values),
        })
    return sorted(summary, key=lambda row: (-float(row["rank_one_fraction"]), float(row["mean_rank"])))


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
    base = run_source_level_sensitivity(
        evidence, constraints, settings=settings, seeds=tuple(args.seeds), draws=args.draws
    )
    ordinal = isolation_order_sensitivity(
        evidence,
        island_summary_path=args.island_summary,
        guide_constraints=constraints,
        settings=settings,
        seeds=tuple(args.seeds),
        draws=args.draws,
    )
    rows = [
        {
            "setting_id": result.setting_id,
            "seed": result.seed,
            "scenario": result.scenario.value,
            "log_marginal_compatibility": result.log_marginal_compatibility,
            "max_importance_weight": result.max_importance_weight,
            "importance_effective_sample_size": result.importance_effective_sample_size,
            "importance_ess_fraction": result.importance_ess_fraction,
            "draws": result.draws,
            "included_channels": [channel.value for channel in result.included_channels],
            "warning": result.warning,
        }
        for result in base
    ]
    rows.extend({
        "setting_id": result.setting_id,
        "seed": result.seed,
        "scenario": result.scenario,
        "log_marginal_compatibility": result.log_marginal_compatibility,
        "max_importance_weight": result.max_importance_weight,
        "importance_effective_sample_size": result.importance_effective_sample_size,
        "importance_ess_fraction": result.importance_ess_fraction,
        "draws": result.draws,
        "included_channels": [channel.value for channel in result.included_channels],
        "warning": result.warning,
    } for result in ordinal)
    ranked = _rerank(rows)
    summary = _summary(ranked)

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in ranked:
            writer.writerow({
                **row,
                "included_channels": ";".join(row["included_channels"]),
                "warning": row["warning"] or "",
            })
    payload = {
        "schema_version": 2,
        "draws": args.draws,
        "seeds": list(args.seeds),
        "setting_count": len(settings),
        "factorial": args.factorial,
        "candidate_scenarios": sorted({str(row["scenario"]) for row in ranked}),
        "boundary": (
            "Five-candidate source-level compatibility sweep. The ordinal island-order candidate uses a fixed proxy scaffold; it is not a distance, history, or causal-isolation estimate. ESS diagnoses Monte Carlo integration quality."
        ),
        "rank_summary": summary,
        "results": ranked,
    }
    args.output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Source-level sensitivity and Monte Carlo diagnostics", "", payload["boundary"], "",
        "## Rank stability", "",
        "| scenario | rank-one cells | cells | rank-one fraction | mean rank | minimum ESS | median ESS | warning cells |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary:
        lines.append(
            f"| {row['scenario']} | {row['rank_one_count']} | {row['cells']} | {row['rank_one_fraction']:.3f} | "
            f"{row['mean_rank']:.3f} | {row['min_ess']:.2f} | {row['median_ess']:.2f} | {row['warning_cells']} |"
        )
    lines.extend((
        "", "## Diagnostics rule", "",
        "Low ESS does not favor another scenario. It means that the corresponding prior-Monte-Carlo integral is poorly resolved and its score must not be interpreted as numerically stable without more or adapted sampling.",
        "", "See the CSV for every setting × seed × scenario cell.",
    ))
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
