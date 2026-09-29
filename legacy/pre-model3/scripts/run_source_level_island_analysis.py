"""Run direct-table source-level Izu comparisons, including island-order proxy.

The ordinal `isolation_order` candidate shares the likelihood with the four
existing ecological scenarios but does not use pollinator availability.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from channel_id.island_multichannel import EvidenceChannel, load_guide_order_constraints
from channel_id.island_source_level import compare_source_level_scenarios, load_source_level_evidence
from channel_id.source_level_isolation_order import compare_isolation_order


def _base_json(results) -> list[dict[str, object]]:
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


def _order_json(result) -> dict[str, object]:
    return {
        "scenario": result.scenario,
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


def _combined_rows(evidence, constraints, summary_path: Path, *, draws: int, seed: int, channels: Iterable[EvidenceChannel]) -> list[dict[str, object]]:
    base = _base_json(compare_source_level_scenarios(
        evidence, constraints, draws=draws, seed=seed, included_channels=channels
    ))
    ordinal = _order_json(compare_isolation_order(
        evidence,
        island_summary_path=summary_path,
        guide_constraints=constraints,
        draws=draws,
        seed=seed,
        included_channels=channels,
    ))
    return sorted([*base, ordinal], key=lambda row: float(row["log_marginal_compatibility"]), reverse=True)


def _markdown(rows: list[dict[str, object]], ablations: dict[str, list[dict[str, object]]]) -> str:
    lines = [
        "# Source-level island multichannel compatibility analysis",
        "",
        "Direct-table source-level compatibility only. The ordinal island-order candidate uses a fixed region_order proxy, not distance, history, or causal isolation. All candidates retain reported-summary uncertainty and conservative residual terms; none establishes pollinator effectiveness or historical causality.",
        "",
        "## Scenario ranking",
        "",
        "| rank | scenario | log marginal compatibility | mean log likelihood | max importance weight |",
        "|---:|---|---:|---:|---:|",
    ]
    for rank, row in enumerate(rows, start=1):
        lines.append(
            f"| {rank} | {row['scenario']} | {float(row['log_marginal_compatibility']):.3f} | "
            f"{float(row['mean_log_likelihood']):.3f} | {float(row['max_importance_weight']):.4f} |"
        )
    lines.extend((
        "",
        "## Channel ablation",
        "",
        "Each ranking omits one channel. A rank reversal flags a conclusion that depends materially on the omitted evidence.",
    ))
    for omitted, ranking in ablations.items():
        lines.extend(("", f"### Omit `{omitted}`", "", "| rank | scenario | log marginal compatibility |", "|---:|---|---:|"))
        for rank, row in enumerate(ranking, start=1):
            lines.append(f"| {rank} | {row['scenario']} | {float(row['log_marginal_compatibility']):.3f} |")
    return "\n".join(lines) + "\n"


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
    channels = tuple(EvidenceChannel)
    full = _combined_rows(evidence, constraints, args.island_summary, draws=args.draws, seed=args.seed, channels=channels)
    ablations = {
        omitted.value: _combined_rows(
            evidence,
            constraints,
            args.island_summary,
            draws=args.draws,
            seed=args.seed,
            channels=tuple(channel for channel in EvidenceChannel if channel is not omitted),
        )
        for omitted in EvidenceChannel
    }
    payload = {
        "schema_version": 2,
        "input_files": {
            "island_summary": str(args.island_summary),
            "outcrossing": str(args.outcrossing),
            "bagging": str(args.bagging),
            "flower": str(args.flower),
            "guide_constraints": str(args.guide_constraints),
        },
        "draws": args.draws,
        "seed": args.seed,
        "candidate_scenarios": [row["scenario"] for row in full],
        "retained_rows": {
            "outcrossing": len(evidence.outcrossing),
            "bagging": len(evidence.bagging),
            "flower": len(evidence.flower),
            "guide_constraints": len(constraints),
            "region_order": len(evidence.islands),
        },
        "boundary": (
            "Direct-table source-level compatibility analysis. The ordinal island-order candidate uses a fixed proxy scaffold and does not establish geographic distance, dispersal history, or causal isolation."
        ),
        "full_evidence": full,
        "leave_one_channel_out": ablations,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.output_md.write_text(_markdown(full, ablations), encoding="utf-8")


if __name__ == "__main__":
    main()
