"""Build a proxy-only reviewer queue for GBIF flower-photo candidates.

Nearest proxy distance is navigation metadata, not an island assignment or a
population label. Reviewers must verify original GBIF geometry and uncertainty.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.inaturalist_photo_proxy_queue import load_proxy_points, queue_rows, read_candidates, write_queue


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--proxy-config", type=Path, default=Path("configs/izu_island_proxy_points.json"))
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    try:
        candidates, columns = read_candidates(args.candidates)
        rows = queue_rows(candidates, load_proxy_points(args.proxy_config))
        write_queue(rows, columns, args.output_csv, args.output_md)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
