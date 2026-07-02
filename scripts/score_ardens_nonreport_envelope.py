"""Enumerate the *Bombus ardens* non-report coding envelope.

This keeps the original counterfactual scorer intact while checking whether its
pollinator-hierarchy ranking depends on interpreting all non-positive historical
rate-table states as zero availability/context.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from channel_id.ardens_nonreport_envelope import (
    configuration_rows,
    derive_uncertain_ardens_islands,
    enumerate_ardens_context_envelope,
    summarize_envelope,
)
from channel_id.pollinator_hierarchy_counterfactual import load_records
from channel_id.pollinator_regime_evidence_audit import (
    build_audit,
    load_effort_rows,
    load_model_indicators,
    load_rate_rows,
)


FIELDS = (
    "configuration_id",
    "ardens_context_coded_one_islands",
    "ardens_context_coded_zero_islands",
    "pollinator_hierarchy_mae",
    "environment_only_mae",
    "isolation_order_mae",
    "pollinator_hierarchy_rank",
    "pollinator_hierarchy_is_co_winner",
    "pollinator_hierarchy_is_unique_winner",
)


def write_markdown(summary: dict[str, object], rows: list[dict[str, str]], path: Path) -> None:
    lines = [
        "# *Bombus ardens* non-report uncertainty envelope",
        "",
        str(summary["boundary"]),
        "",
        "## Declared uncertain context codings",
        "",
        "| item | value |",
        "|---|---|",
        f"| islands varied | {'; '.join(summary['uncertain_ardens_context_islands']) or 'none'} |",
        f"| configurations | {summary['configuration_count']} |",
        f"| hierarchy co-winner configurations | {summary['pollinator_hierarchy_co_winner_count']} ({summary['pollinator_hierarchy_co_winner_fraction']:.3f}) |",
        f"| hierarchy unique-winner configurations | {summary['pollinator_hierarchy_unique_winner_count']} ({summary['pollinator_hierarchy_unique_winner_fraction']:.3f}) |",
        f"| hierarchy rank range | {summary['pollinator_hierarchy_best_rank']}–{summary['pollinator_hierarchy_worst_rank']} |",
        "",
        "## Configuration results",
        "",
        "| id | B. ardens context = 1 | B. ardens context = 0 | hierarchy MAE | environment MAE | isolation MAE | hierarchy rank | co-winner |",
        "|---|---|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['configuration_id']} | {row['ardens_context_coded_one_islands'] or 'none'} | "
            f"{row['ardens_context_coded_zero_islands'] or 'none'} | {row['pollinator_hierarchy_mae']} | "
            f"{row['environment_only_mae']} | {row['isolation_order_mae']} | {row['pollinator_hierarchy_rank']} | "
            f"{row['pollinator_hierarchy_is_co_winner']} |"
        )
    lines.extend((
        "",
        "## Interpretation",
        "",
        "This table is not an occupancy model and does not say that any context=1 configuration is biologically present, equally plausible, or effective at pollination. It asks only whether the original pattern ranking remains compatible with every declared handling of non-report / no-effort states.",
    ))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/inoue_literature_island_traits.csv"))
    parser.add_argument("--pollinator-rates", type=Path, default=Path("data/two_breakpoint_evidence/inoue1986_pollinator_rates.csv"))
    parser.add_argument("--observation-effort", type=Path, default=Path("data/two_breakpoint_evidence/inoue1986_observation_effort.csv"))
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    try:
        records = load_records(args.input)
        audit = build_audit(
            load_model_indicators(args.input),
            load_rate_rows(args.pollinator_rates),
            load_effort_rows(args.observation_effort),
        )
        uncertain = derive_uncertain_ardens_islands(records, audit)
        configurations = enumerate_ardens_context_envelope(records, uncertain)
        summary = summarize_envelope(configurations, uncertain)
        rows = configuration_rows(configurations)
        args.output_csv.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        payload = {**summary, "configurations": rows}
        args.output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        write_markdown(summary, rows, args.output_md)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
