"""Audit field guide, geometry, effort, and visitor-contact coverage by tagged plant."""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.field_flower_geometry import read_field_geometry_manifest
from channel_id.field_guide_photo_review import read_field_manifest
from channel_id.field_legitimate_contact import read_effort_manifest, read_visit_manifest
from channel_id.field_multichannel_coverage import (
    build_field_multichannel_coverage,
    write_field_multichannel_coverage,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--guide-photos", type=Path, required=True)
    parser.add_argument("--geometry", type=Path, required=True)
    parser.add_argument("--effort", type=Path, required=True)
    parser.add_argument("--visits", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        coverage = build_field_multichannel_coverage(
            read_field_manifest(args.guide_photos),
            read_field_geometry_manifest(args.geometry),
            read_effort_manifest(args.effort),
            read_visit_manifest(args.visits),
        )
        write_field_multichannel_coverage(args.output_dir, coverage)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
