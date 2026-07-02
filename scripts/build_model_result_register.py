"""Build a guarded cross-model register for the Izu analysis artifacts.

This command compares conclusions and assumptions, not raw score magnitudes.
The input analyses use different model families and therefore must not be pooled
or converted into a single winner.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.model_result_register import build_register, load_json, write_register


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-level", type=Path, required=True)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--sensitivity", type=Path, required=True)
    parser.add_argument("--stage-pattern", type=Path, required=True)
    parser.add_argument("--ardens-envelope", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    try:
        register = build_register(
            load_json(args.source_level),
            load_json(args.profile),
            load_json(args.sensitivity),
            load_json(args.stage_pattern),
            load_json(args.ardens_envelope),
        )
        write_register(register, args.output_json, args.output_csv, args.output_md)
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
