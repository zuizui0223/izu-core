import argparse
import csv
from pathlib import Path

REQUIRED = [
    "observation_id",
    "island_id",
    "locality_id",
    "source_type",
    "source_id",
    "species",
    "taxon_role",
    "flower_id",
    "guide_region",
    "spot_metric",
    "spot_value",
    "measurement_scale",
]
VALID_ISLANDS = {"Oshima", "Toshima", "Niijima", "Kozushima", "Miyake", "Hachijo"}
VALID_METRICS = {"spot_fraction", "spot_count", "guide_contrast", "guide_presence"}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit("guide spot table is empty")
    missing = [name for name in REQUIRED if name not in rows[0]]
    if missing:
        raise SystemExit("missing required columns: " + ", ".join(missing))
    return rows


def validate(rows):
    errors = []
    informative = []
    for index, row in enumerate(rows, start=2):
        if row["island_id"] not in VALID_ISLANDS:
            errors.append(f"line {index}: unknown island_id {row['island_id']}")
        if row["spot_metric"] not in VALID_METRICS:
            errors.append(f"line {index}: unknown spot_metric {row['spot_metric']}")
        value = row["spot_value"].strip()
        if value:
            try:
                float(value)
            except ValueError:
                errors.append(f"line {index}: spot_value is not numeric")
            informative.append(row)
    return errors, informative


def write_report(rows, informative, output):
    islands = sorted({row["island_id"] for row in informative})
    lines = [
        "# Island guide spot channel report",
        "",
        "This report validates the island-resolved guide/spot observation channel.",
        "Template rows without spot_value do not unlock guide-loss inference.",
        "",
        f"Rows: {len(rows)}",
        f"Informative rows: {len(informative)}",
        f"Informative islands: {', '.join(islands) if islands else 'none'}",
        "",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/island_guide_spot_observations_template.csv"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--require-informative", action="store_true")
    args = parser.parse_args()
    rows = load_rows(args.input)
    errors, informative = validate(rows)
    if args.require_informative and not informative:
        errors.append("no informative spot_value rows present")
    if errors:
        raise SystemExit("\n".join(errors))
    write_report(rows, informative, args.output)


if __name__ == "__main__":
    main()
