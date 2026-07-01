"""Build the direct-observation evidence-lock report.

Usage:
    python scripts/build_empirical_evidence_lock.py \
      --data-dir data/two_breakpoint_evidence \
      --output artifacts/empirical_evidence_lock.md
"""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.empirical_evidence_lock import render_empirical_evidence_markdown


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data/two_breakpoint_evidence"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        text = render_empirical_evidence_markdown(args.data_dir)
    except (OSError, ValueError, KeyError) as error:
        raise SystemExit(str(error)) from error
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
