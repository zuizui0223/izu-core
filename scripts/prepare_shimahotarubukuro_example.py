#!/usr/bin/env python3
"""Aggregate the shimahotarubukuro corolla_master table for scenario analysis."""
from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

ISLAND_ORDER = {"oshima": 0, "toshima": 1, "niijima": 2, "shikinejima": 3, "kozushima": 4}
DEFAULT_TRAITS = (
    "corolla_length_mm",
    "throat_width_mm",
    "mouth_width_mm",
    "style_length_mm",
    "guide_coverage_pct",
    "n_guide_spots",
)


def aggregate(input_path: Path, output_path: Path, traits: tuple[str, ...]) -> None:
    values: dict[tuple[str, str], list[float]] = defaultdict(list)
    with input_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = {"island", *traits} - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"missing columns: {sorted(missing)}")
        for row in reader:
            island = str(row["island"]).strip().lower()
            if island not in ISLAND_ORDER:
                continue
            for trait in traits:
                raw = str(row.get(trait, "")).strip()
                if not raw:
                    continue
                try:
                    value = float(raw)
                except ValueError:
                    continue
                if math.isfinite(value):
                    values[(trait, island)].append(value)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        fields = ["trait", "regime_id", "order", "bombus_loss_state", "mean", "se", "n"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for trait in traits:
            for island, order in ISLAND_ORDER.items():
                cell = values.get((trait, island), [])
                if len(cell) < 2:
                    continue
                sd = statistics.stdev(cell)
                writer.writerow({
                    "trait": trait,
                    "regime_id": island,
                    "order": order,
                    "bombus_loss_state": 0 if island == "oshima" else 1,
                    "mean": f"{statistics.mean(cell):.8g}",
                    "se": f"{sd / math.sqrt(len(cell)):.8g}",
                    "n": len(cell),
                })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="corolla_master.csv from shimahotarubukuro")
    parser.add_argument("--output", type=Path, default=Path("results/shimahotarubukuro_summary.csv"))
    parser.add_argument("--traits", nargs="*", default=list(DEFAULT_TRAITS))
    args = parser.parse_args()
    aggregate(args.input, args.output, tuple(args.traits))
    print(args.output)


if __name__ == "__main__":
    main()
