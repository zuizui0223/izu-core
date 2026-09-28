"""Write blank Izu raw-record CSV templates for field and laboratory use."""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.izu_raw_record_protocol import write_izu_raw_record_templates


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/izu_raw_record_templates"),
        help="directory for the six CSV templates and README",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    written = write_izu_raw_record_templates(args.output_dir)
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
