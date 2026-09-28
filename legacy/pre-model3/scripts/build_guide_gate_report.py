import argparse
import csv
from pathlib import Path

VALID = {"locked", "partial", "blocked"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, default=Path("data/guide_loss_required_channels.csv"))
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    rows = list(csv.DictReader(a.input.open(newline="", encoding="utf-8")))
    if not rows:
        raise SystemExit("empty input")
    bad = sorted({r["current_status"] for r in rows} - VALID)
    if bad:
        raise SystemExit(f"bad status: {bad}")
    counts = {k: sum(r["current_status"] == k for r in rows) for k in sorted(VALID)}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Guide gate report", "", "| status | n |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in counts.items()]
    lines += ["", "| channel | status |", "|---|---|"]
    lines += [f"| {r['channel_id']} | {r['current_status']} |" for r in rows]
    a.output.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
