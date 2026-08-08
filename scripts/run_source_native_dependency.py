#!/usr/bin/env python3
"""Write the source-native pollinator-dependency readiness report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.source_native_dependency import load_dependency_evidence, summarize


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("data/predictive_meta/source_native_dependency_registry.csv"),
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("artifacts/source_native_directional_holdout/dependency_summary.json"),
    )
    args = parser.parse_args()
    summary = summarize(load_dependency_evidence(args.registry))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(summary["independent_bombus_holdout_status"])
    print(args.out)


if __name__ == "__main__":
    main()
