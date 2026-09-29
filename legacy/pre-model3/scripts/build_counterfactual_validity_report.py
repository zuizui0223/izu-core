import argparse
import csv
from pathlib import Path

VALID = {"active", "partial", "blocked"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/counterfactual_validity_conditions.csv"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = list(csv.DictReader(args.input.open(newline="", encoding="utf-8")))
    if not rows:
        raise SystemExit("empty counterfactual validity matrix")
    unknown = sorted({row["status"] for row in rows} - VALID)
    if unknown:
        raise SystemExit("unknown status: " + ", ".join(unknown))
    counts = {status: sum(row["status"] == status for row in rows) for status in sorted(VALID)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Counterfactual validity scope", "", "The staged pollinator-collapse counterfactual is usable only inside these declared conditions.", "", "| status | n |", "|---|---:|"]
    lines += [f"| {status} | {n} |" for status, n in counts.items()]
    lines += ["", "| condition | scope | status | decision if invalidated |", "|---|---|---|---|"]
    for row in rows:
        lines.append(f"| {row['condition_id']} | {row['claim_scope']} | {row['status']} | {row['decision']} |")
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
