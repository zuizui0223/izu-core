#!/usr/bin/env python3
"""Summarize empirical pilot coverage/loss without inventing reliability."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.effective_dependency_pilot_assumptions import build_pilot_assumption_audit
from channel_id.effective_pollinator_dependency import (
    read_dependency_plant_registry,
    read_pollination_treatments,
    read_svd_manifest,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plants", type=Path, required=True)
    parser.add_argument("--svd", type=Path, required=True)
    parser.add_argument("--treatments", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = build_pilot_assumption_audit(
            read_dependency_plant_registry(args.plants),
            read_svd_manifest(args.svd),
            read_pollination_treatments(args.treatments),
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
