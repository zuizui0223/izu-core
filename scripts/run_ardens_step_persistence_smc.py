"""Run a six-candidate tempered-SMC screen including ardens step persistence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.ardens_step_persistence_smc import (
    pairwise_deltas,
    run_six_candidate_comparison,
    summarize_six_candidate_comparison,
)
from channel_id.island_multichannel import EvidenceChannel, load_guide_order_constraints
from channel_id.island_source_level import load_source_level_evidence
from channel_id.source_level_ardens_step_persistence import ARDENS_STEP_PERSISTENCE_SCENARIO
from channel_id.source_level_tempered_smc import TemperedSMCConfig


def _markdown(summary: tuple[dict[str, object], ...], step_bridge: tuple[dict[str, object], ...], step_order: tuple[dict[str, object], ...]) -> str:
    lines = [
        "# Six-candidate source-level tempered-SMC screen",
        "",
        "The sixth candidate is a strict two-stage hypothesis: flower length drops at the declared Oshima bridge stage and is held constant downstream except for the declared environment term; reproductive channels may shift again post-bridge. It is a falsifiable compatibility model, not reconstructed history.",
        "",
        "| rank | scenario | mean log compatibility | SD | rank-one replicates | mean rank | minimum incremental ESS |",
        "|---:|---|---:|---:|---:|---:|---:|",
    ]
    for rank, row in enumerate(summary, start=1):
        lines.append(
            f"| {rank} | {row['scenario']} | {float(row['mean_log_marginal_compatibility']):.3f} | "
            f"{float(row['sd_log_marginal_compatibility']):.3f} | {row['rank_one_count']} / {row['replicates']} | "
            f"{float(row['mean_rank']):.3f} | {float(row['minimum_incremental_ess']):.1f} |"
        )
    for title, rows in (("Step persistence minus continuous bridge loss", step_bridge), ("Step persistence minus ordinal order proxy", step_order)):
        lines.extend(("", f"## {title}", "", "| seed | difference | step higher |", "|---:|---:|---|"))
        for row in rows:
            lines.append(f"| {row['seed']} | {float(row['left_minus_right']):+.3f} | {row['left_higher']} |")
    lines.extend((
        "", "## Boundary", "",
        "This screen holds the stage scaffold fixed before scoring. It does not prove that B. ardens occupied an ancestral bridge, that its loss caused flower reduction, that small bees were irrelevant, or that a guide evolved in any direction. Guide constraints remain zero until independently reviewed evidence is entered.",
    ))
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--island-summary", type=Path, default=Path("data/inoue_literature_island_traits.csv"))
    parser.add_argument("--stage-scaffold", type=Path, default=Path("data/ardens_step_persistence_stages.csv"))
    parser.add_argument("--outcrossing", type=Path, default=Path("data/two_breakpoint_evidence/inoue1990_outcrossing.csv"))
    parser.add_argument("--bagging", type=Path, default=Path("data/two_breakpoint_evidence/inoue1988_bagging.csv"))
    parser.add_argument("--flower", type=Path, default=Path("data/two_breakpoint_evidence/inoue1995_flower_length.csv"))
    parser.add_argument("--guide-constraints", type=Path, default=Path("data/guide_direction_constraints.csv"))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--particles", type=int, default=500)
    parser.add_argument("--target-ess-fraction", type=float, default=0.70)
    parser.add_argument("--rejuvenation-steps", type=int, default=1)
    parser.add_argument("--seeds", type=int, nargs="+", default=[20260711, 20260712, 20260713])
    args = parser.parse_args()
    try:
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
        results = run_six_candidate_comparison(
            evidence,
            island_summary_path=args.island_summary,
            stage_scaffold_path=args.stage_scaffold,
            guide_constraints=constraints,
            config=config,
            seeds=args.seeds,
            included_channels=tuple(EvidenceChannel),
        )
        summary = summarize_six_candidate_comparison(results)
        step_bridge = pairwise_deltas(
            results,
            left_scenario=ARDENS_STEP_PERSISTENCE_SCENARIO,
            right_scenario="ardens_bridge_loss",
        )
        step_order = pairwise_deltas(
            results,
            left_scenario=ARDENS_STEP_PERSISTENCE_SCENARIO,
            right_scenario="isolation_order",
        )
        payload = {
            "schema_version": 1,
            "candidate_scenarios": [row["scenario"] for row in summary],
            "retained_rows": {
                "outcrossing": len(evidence.outcrossing),
                "bagging": len(evidence.bagging),
                "flower": len(evidence.flower),
                "guide_constraints": len(constraints),
            },
            "stage_scaffold": str(args.stage_scaffold),
            "smc_config": {"particles": args.particles, "target_ess_fraction": args.target_ess_fraction, "rejuvenation_steps": args.rejuvenation_steps, "seeds": args.seeds},
            "summary": summary,
            "step_minus_continuous_bridge": step_bridge,
            "step_minus_isolation_order": step_order,
            "boundary": "Six-candidate source-level compatibility screen; not historical or causal inference.",
        }
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        args.output_md.write_text(_markdown(summary, step_bridge, step_order), encoding="utf-8")
    except (OSError, ValueError, RuntimeError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
