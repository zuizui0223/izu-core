"""Run the prediction-locked two-threshold analysis for one data partition."""
from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.predictive_meta import (
    Scenario,
    assess_contrasts,
    aggregate_observations,
    build_contrasts,
    load_observations,
    load_prediction_rules,
    render_markdown,
    score_scenarios,
    write_assessments_csv,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--observations", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--partition", choices=("calibration", "holdout"), required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    observations = load_observations(args.observations)
    rules = load_prediction_rules(args.contract)
    scores = score_scenarios(observations, rules, args.partition)
    contrasts = build_contrasts(aggregate_observations(observations))
    assessments = tuple(
        item
        for scenario in Scenario
        for item in assess_contrasts(contrasts, rules, scenario, args.partition)
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / f"{args.partition}_prediction_score.md").write_text(
        render_markdown(scores, assessments, args.partition), encoding="utf-8"
    )
    write_assessments_csv(args.output_dir / f"{args.partition}_contrast_assessments.csv", assessments)
    print(f"wrote prediction-locked report for {args.partition} to {args.output_dir}")


if __name__ == "__main__":
    main()
