"""Run a five-candidate source-level profile search including island order."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from channel_id.island_multichannel import load_guide_order_constraints
from channel_id.island_source_level import load_source_level_evidence
from channel_id.source_level_isolation_order_diagnostics import profile_isolation_order
from channel_id.source_level_profile import ProfileSearchConfig, profile_source_level_scenarios


def _serialize_base(result) -> dict[str, object]:
    return {
        "scenario": result.scenario.value,
        "best_log_likelihood": result.best_log_likelihood,
        "terminal_elite_mean_log_likelihood": result.terminal_elite_mean_log_likelihood,
        "channel_log_likelihood": {
            "outcrossing": result.best_outcrossing_log_likelihood,
            "bagging": result.best_bagging_log_likelihood,
            "flower": result.best_flower_log_likelihood,
            "guide_order": result.best_guide_log_likelihood,
        },
        "best_draw": asdict(result.best_draw),
    }


def _serialize_order(result) -> dict[str, object]:
    return {
        "scenario": result.scenario,
        "best_log_likelihood": result.best_log_likelihood,
        "terminal_elite_mean_log_likelihood": result.terminal_elite_mean_log_likelihood,
        "channel_log_likelihood": {
            "outcrossing": result.best_outcrossing_log_likelihood,
            "bagging": result.best_bagging_log_likelihood,
            "flower": result.best_flower_log_likelihood,
            "guide_order": result.best_guide_log_likelihood,
        },
        "best_draw": asdict(result.best_draw),
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
    base = profile_source_level_scenarios(evidence, constraints, config=config, seed=args.seed)
    order = profile_isolation_order(
        evidence,
        island_summary_path=args.island_summary,
        guide_constraints=constraints,
        population_size=config.population_size,
        iterations=config.iterations,
        elite_fraction=config.elite_fraction,
        prior_refresh_fraction=config.prior_refresh_fraction,
        initial_temperature=config.initial_temperature,
        final_temperature=config.final_temperature,
        seed=args.seed,
    )
    rows = sorted([*(_serialize_base(result) for result in base), _serialize_order(order)], key=lambda row: float(row["best_log_likelihood"]), reverse=True)
    for index, row in enumerate(rows, start=1):
        row["profile_rank"] = index
    payload = {
        "schema_version": 2,
        "seed": args.seed,
        "config": asdict(config),
        "candidate_scenarios": [row["scenario"] for row in rows],
        "boundary": "Five-candidate profile search. isolation_order is a fixed ordinal proxy, not a historical reconstruction or causal-isolation estimate. This optimizer is not a posterior probability or marginal-evidence ranking.",
        "results": rows,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Source-level profile compatibility", "", payload["boundary"], "",
        "| rank | scenario | best log likelihood | terminal elite mean | outcrossing | bagging | flower | guide order |",
        "|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        channel = row["channel_log_likelihood"]
        lines.append(
            f"| {row['profile_rank']} | {row['scenario']} | {float(row['best_log_likelihood']):.3f} | {float(row['terminal_elite_mean_log_likelihood']):.3f} | {float(channel['outcrossing']):.3f} | {float(channel['bagging']):.3f} | {float(channel['flower']):.3f} | {float(channel['guide_order']):.3f} |"
        )
    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
