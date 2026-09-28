"""Screen flower-length comparability and row leverage with tempered SMC.

This is a declared data-comparability sensitivity, not a new evolutionary model.
It reruns the same five candidates after excluding only rows that lack a
within-experiment retained reference or that are deliberately tested for leverage.
"""

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


def _find(rows: tuple[dict[str, object], ...], scenario: str) -> dict[str, object]:
    for row in rows:
        if str(row["scenario"]) == scenario:
            return row
    raise ValueError(f"missing scenario {scenario!r}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--island-summary", type=Path, default=Path("data/inoue_literature_island_traits.csv"))
    parser.add_argument("--outcrossing", type=Path, default=Path("data/two_breakpoint_evidence/inoue1990_outcrossing.csv"))
    parser.add_argument("--bagging", type=Path, default=Path("data/two_breakpoint_evidence/inoue1988_bagging.csv"))
    parser.add_argument("--flower", type=Path, default=Path("data/two_breakpoint_evidence/inoue1995_flower_length.csv"))
    parser.add_argument("--guide-constraints", type=Path, default=Path("data/guide_direction_constraints.csv"))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--particles", type=int, default=250)
    parser.add_argument("--target-ess-fraction", type=float, default=0.70)
    parser.add_argument("--rejuvenation-steps", type=int, default=1)
    parser.add_argument("--seeds", type=int, nargs="+", default=(20260705, 20260706))
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
    )
    results: list[dict[str, object]] = []
    for flower_set in build_flower_length_sets(evidence, args.flower):
        smc = run_tempered_smc_comparison(
            flower_set.evidence,
            island_summary_path=args.island_summary,
            guide_constraints=constraints,
            config=config,
            seeds=tuple(args.seeds),
        )
        summary = summarize_tempered_smc(smc)
        deltas = bridge_order_deltas(smc)
        order = _find(summary, "isolation_order")
        bridge = _find(summary, "ardens_bridge_loss")
        results.append({
            "set_id": flower_set.set_id,
            "description": flower_set.description,
            "retained_labels": list(flower_set.retained_labels),
            "excluded_labels": list(flower_set.excluded_labels),
            "retained_flower_rows": len(flower_set.evidence.flower),
            "isolation_order": order,
            "ardens_bridge_loss": bridge,
            "bridge_order_deltas": list(deltas),
            "rank_summary": list(summary),
        })
    payload = {
        "schema_version": 1,
        "config": {
            "particles": config.particles,
            "target_ess_fraction": config.target_ess_fraction,
            "rejuvenation_steps": config.rejuvenation_steps,
            "seeds": list(args.seeds),
        },
        "boundary": (
            "Flower-length comparability screening. The singleton Nikko experiment "
            "is not treated as a calibrated cross-island anchor. Results test data "
            "pooling and leverage, not causal isolation, pollinator effectiveness, "
            "or an experiment-block effect that is absent from the source table."
        ),
        "sets": results,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Flower-length comparability and leverage screening", "", payload["boundary"], "",
        "| set | flower rows | isolation-order mean rank | bridge mean rank | order rank-one fraction | bridge rank-one fraction | mean order-minus-bridge |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in results:
        deltas = [float(item["order_minus_bridge"]) for item in row["bridge_order_deltas"]]
        mean_delta = sum(deltas) / len(deltas) if deltas else float("nan")
        order = row["isolation_order"]
        bridge = row["ardens_bridge_loss"]
        lines.append(
            f"| {row['set_id']} | {row['retained_flower_rows']} | {float(order['mean_rank']):.3f} | "
            f"{float(bridge['mean_rank']):.3f} | {float(order['rank_one_fraction']):.3f} | "
            f"{float(bridge['rank_one_fraction']):.3f} | {mean_delta:.3f} |"
        )
    lines.extend((
        "", "## Retained and excluded rows", "",
    ))
    for row in results:
        lines.append(f"### {row['set_id']}")
        lines.append("")
        lines.append(f"- retained: {', '.join(row['retained_labels'])}")
        lines.append(f"- excluded: {', '.join(row['excluded_labels']) or '(none)'}")
        lines.append("")
    args.output_md.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
