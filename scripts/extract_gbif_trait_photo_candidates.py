"""Extract source-linked flower-photo candidates from a raw GBIF snapshot.

This command only builds a review queue. It does not infer island membership,
trait values, or pollination from GBIF media.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.gbif_trait_photos import extract_snapshot, write_candidates


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot-root", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    try:
        rows = extract_snapshot(args.snapshot_root)
        write_candidates(rows, args.output_csv, args.output_md)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
