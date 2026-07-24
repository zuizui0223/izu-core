#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from channel_id.candidate_registry import audit_candidates, load_candidates


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Izu specialist-generalist candidate registry")
    parser.add_argument("input")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    result = audit_candidates(load_candidates(args.input))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
