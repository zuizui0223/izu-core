"""Score counterfactual pattern compatibility for Izu Campanula island traits.

The scoring implementation lives in `channel_id.pollinator_hierarchy_counterfactual`
so it can also be reused by declared uncertainty-envelope checks.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.pollinator_hierarchy_counterfactual import IslandRecord, load_records, score, write_markdown

__all__ = ("IslandRecord", "load_records", "score", "write_markdown")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/inoue_literature_island_traits.csv"))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    result = score(load_records(args.input))
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_markdown(result, args.output_md)


if __name__ == "__main__":
    main()
