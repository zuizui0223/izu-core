"""Compile strict, table-transcribed primary evidence for the holdout scorer."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.primary_source_holdout import (
    compile_holdout_observations,
    load_native_evidence,
    summarize,
    write_holdout_observations,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        records = load_native_evidence(args.registry)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
    observations = compile_holdout_observations(records)
    write_holdout_observations(args.out, observations)
    report = {**summarize(records), "emitted_holdout_rows": len(observations)}
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
