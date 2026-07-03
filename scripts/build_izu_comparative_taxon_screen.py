"""Validate and summarize the Stage-A Izu comparative-taxon evidence map."""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.izu_comparative_taxon_screen import (
    build_izu_comparative_taxon_screen,
    read_izu_comparative_taxon_screen,
    write_izu_comparative_taxon_screen,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screen", type=Path, default=Path("data/izu_comparative_taxon_screen.csv"))
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        rows = read_izu_comparative_taxon_screen(args.screen)
        write_izu_comparative_taxon_screen(args.output_dir, build_izu_comparative_taxon_screen(rows))
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
