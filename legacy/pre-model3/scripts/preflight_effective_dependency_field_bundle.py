#!/usr/bin/env python3
"""Preflight the Issue #91 field bundle before freeze and analysis."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.effective_dependency_preflight import CHANNEL_TEMPLATES, build_preflight


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in CHANNEL_TEMPLATES:
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument(
        "--templates-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "templates",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    paths = {name: getattr(args, name) for name in CHANNEL_TEMPLATES}
    result = build_preflight(paths, args.templates_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
