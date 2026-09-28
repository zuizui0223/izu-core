"""Render the locked pre-field known-data closure report.

Usage:
    python scripts/build_known_data_phase_closure.py \
      --repository-root . \
      --output artifacts/PRE_FIELD_KNOWN_DATA_CLOSURE.md
"""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.known_data_phase_closure import (
    read_known_data_phase_lock,
    render_known_data_phase_closure_markdown,
    validate_known_data_phase_lock,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    parser.add_argument("--lock", type=Path, default=Path("data/known_data_phase_lock.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.repository_root.resolve()
    lock_path = args.lock if args.lock.is_absolute() else root / args.lock
    output_path = args.output if args.output.is_absolute() else root / args.output
    try:
        lock = read_known_data_phase_lock(lock_path)
        closure = validate_known_data_phase_lock(lock, root)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(render_known_data_phase_closure_markdown(lock, closure), encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
