"""Validate and summarize the manual guide evidence registry."""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.guide_evidence_registry import (
    read_guide_evidence_registry,
    summarize_guide_evidence_registry,
    write_guide_evidence_registry_summary,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=Path("data/guide_evidence_registry.csv"))
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        rows = read_guide_evidence_registry(args.registry)
        write_guide_evidence_registry_summary(args.output_dir, summarize_guide_evidence_registry(rows))
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
