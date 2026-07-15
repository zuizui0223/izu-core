"""Render the current claim/readiness state from committed evidence tables."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.current_evidence_state import render_markdown, summarize_current_evidence

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--markdown-out", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    state = summarize_current_evidence(args.root)
    markdown = render_markdown(state)
    if args.markdown_out:
        args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_out.write_text(markdown, encoding="utf-8")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(
            json.dumps(state.to_dict(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(markdown)


if __name__ == "__main__":
    main()
