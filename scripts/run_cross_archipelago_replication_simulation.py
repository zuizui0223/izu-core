#!/usr/bin/env python3
"""Run prospective cross-archipelago nested-replication simulations."""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from channel_id.cross_archipelago_design import run_replication_simulation


def flatten_rows(report: dict[str, object]) -> list[dict[str, object]]:
    rows = []
    for row in report["scenario_results"]:
        naive = row["naive_island_level"]
        system = row["system_level"]
        rows.append(
            {
                "scenario_id": row["scenario_id"],
                "n_archipelagos": row["n_archipelagos"],
                "islands_per_archipelago": row["islands_per_archipelago"],
                "total_island_units": row["total_island_units"],
                "population_mean": row["population_mean"],
                "between_archipelago_sd": row["between_archipelago_sd"],
                "within_archipelago_sd": row["within_archipelago_sd"],
                "naive_coverage": naive["coverage_of_population_mean"],
                "system_coverage": system["coverage_of_population_mean"],
                "naive_positive_detection": naive["positive_detection_probability"],
                "system_positive_detection": system["positive_detection_probability"],
                "naive_false_direction": naive["type_s_false_direction_probability"],
                "system_false_direction": system["type_s_false_direction_probability"],
                "naive_mean_reported_se": naive["mean_reported_se"],
                "system_mean_reported_se": system["mean_reported_se"],
                "naive_empirical_sd": naive["empirical_sd_of_estimates"],
                "system_empirical_sd": system["empirical_sd_of_estimates"],
                "reported_se_ratio_naive_to_system": row["reported_se_ratio_naive_to_system"],
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("data/design/cross_archipelago_replication_scenarios.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/cross_archipelago_replication/report.json"),
    )
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=Path("artifacts/cross_archipelago_replication/scenario_summary.csv"),
    )
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    report = run_replication_simulation(config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    rows = flatten_rows(report)
    write_csv(args.csv_output, rows)
    print(f"scenario rows: {len(rows)}")
    print(f"output: {args.output}")


if __name__ == "__main__":
    main()
