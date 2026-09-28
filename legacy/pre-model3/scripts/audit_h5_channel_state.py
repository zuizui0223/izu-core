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

from channel_id.h5_channel_state import audit_channel_state_file


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit outcome-blind Izu H5 pollination-channel retained/disrupted states."
    )
    parser.add_argument("--channel-state-csv", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "h5_channel_state_audit")
    args = parser.parse_args()

    audit = audit_channel_state_file(args.channel_state_csv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows_path = args.output_dir / "channel_state_audit.csv"
    if audit.rows:
        with rows_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(audit.rows[0].keys()))
            writer.writeheader()
            writer.writerows(audit.rows)
    else:
        rows_path.write_text("", encoding="utf-8")
    (args.output_dir / "summary.json").write_text(
        json.dumps(audit.summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(audit.summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
