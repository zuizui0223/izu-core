"""Build a standalone blind guide-review bundle from a first-party field manifest."""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.field_guide_photo_review import (
    FieldReviewBundleConfig,
    build_field_review_bundle,
    read_field_manifest,
    write_field_review_bundle,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--target-id", default="campanula_microdonta")
    parser.add_argument("--seed", type=int, default=20260703)
    args = parser.parse_args()
    try:
        rows = read_field_manifest(args.manifest)
        bundle = build_field_review_bundle(rows, FieldReviewBundleConfig(target_id=args.target_id, seed=args.seed))
        write_field_review_bundle(args.output_dir, bundle)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
