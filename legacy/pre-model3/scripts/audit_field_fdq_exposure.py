#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from channel_id.field_fdq_exposure import audit_field_fdq_from_files


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Issue #91 field visitor data for strict Izu-compatible FDQ.")
    parser.add_argument("--plants", type=Path, required=True)
    parser.add_argument("--effort", type=Path, required=True)
    parser.add_argument("--visits", type=Path, required=True)
    parser.add_argument("--traits", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "field_fdq_audit")
    args = parser.parse_args()

    audit = audit_field_fdq_from_files(
        plants_path=args.plants,
        effort_path=args.effort,
        visits_path=args.visits,
        traits_path=args.traits,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows_path = args.output_dir / "fdq_exposure_units.csv"
    if audit.exposure_rows:
        with rows_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(audit.exposure_rows[0].keys()))
            writer.writeheader()
            writer.writerows(audit.exposure_rows)
    else:
        rows_path.write_text("", encoding="utf-8")

    summary_path = args.output_dir / "summary.json"
    summary_path.write_text(json.dumps(audit.summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(audit.summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
