"""Validate a tagged-flower geometry manifest and write plant-first summaries."""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.field_flower_geometry import (
    read_field_geometry_manifest,
    summarize_field_geometry,
    write_field_geometry_summary,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--geometry", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        rows = read_field_geometry_manifest(args.geometry)
        write_field_geometry_summary(args.output_dir, summarize_field_geometry(rows))
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
