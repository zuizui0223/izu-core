"""Create a geography-first, double-blind guide-photo review bundle.

The source queue is a candidate index, not trait evidence. This command writes
review templates only; no public photo is scored automatically.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.guide_photo_review import (
    ReviewBundleConfig,
    build_review_bundle,
    read_proxy_queue,
    write_review_bundle,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proxy-queue", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--target-id", default="campanula_microdonta")
    parser.add_argument("--max-positional-accuracy-m", type=float, default=100.0)
    parser.add_argument("--min-proxy-gap-km", type=float, default=20.0)
    parser.add_argument("--seed", type=int, default=20260702)
    args = parser.parse_args()
    try:
        rows, _ = read_proxy_queue(args.proxy_queue)
        config = ReviewBundleConfig(
            target_id=args.target_id,
            max_positional_accuracy_m=args.max_positional_accuracy_m,
            min_proxy_gap_km=args.min_proxy_gap_km,
            seed=args.seed,
        )
        geographic, trait_a, trait_b, key = build_review_bundle(rows, config)
        write_review_bundle(args.output_dir, geographic, trait_a, trait_b, key, config)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
