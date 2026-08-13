#!/usr/bin/env python3
"""Audit acquisition readiness for priority independent primary sources."""
from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.independent_source_acquisition import run_audit, write_report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("data/design/independent_primary_source_acquisition.json"),
    )
    parser.add_argument(
        "--native-evidence",
        type=Path,
        default=Path("data/predictive_meta/primary_source_native_evidence.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/independent_source_acquisition/summary.json"),
    )
    args = parser.parse_args()
    try:
        write_report(args.output, run_audit(args.manifest, args.native_evidence))
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
