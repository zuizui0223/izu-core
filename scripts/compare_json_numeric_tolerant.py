#!/usr/bin/env python3
"""Compare JSON documents exactly except for negligible floating-point drift."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


def assert_json_close(observed: Any, expected: Any, *, atol: float = 1e-12) -> None:
    if isinstance(observed, bool) or isinstance(expected, bool):
        if observed != expected:
            raise AssertionError(f"value mismatch: {observed!r} != {expected!r}")
        return
    if isinstance(observed, (int, float)) and isinstance(expected, (int, float)):
        if not math.isclose(float(observed), float(expected), rel_tol=0.0, abs_tol=atol):
            raise AssertionError(f"numeric mismatch: {observed!r} != {expected!r}")
        return
    if isinstance(observed, dict) and isinstance(expected, dict):
        if set(observed) != set(expected):
            raise AssertionError(
                f"key mismatch: {sorted(observed)} != {sorted(expected)}"
            )
        for key in expected:
            try:
                assert_json_close(observed[key], expected[key], atol=atol)
            except AssertionError as exc:
                raise AssertionError(f"at {key!r}: {exc}") from exc
        return
    if isinstance(observed, list) and isinstance(expected, list):
        if len(observed) != len(expected):
            raise AssertionError(f"length mismatch: {len(observed)} != {len(expected)}")
        for index, (left, right) in enumerate(zip(observed, expected)):
            try:
                assert_json_close(left, right, atol=atol)
            except AssertionError as exc:
                raise AssertionError(f"at index {index}: {exc}") from exc
        return
    if observed != expected:
        raise AssertionError(f"value mismatch: {observed!r} != {expected!r}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("observed", type=Path)
    parser.add_argument("expected", type=Path)
    parser.add_argument("--atol", type=float, default=1e-12)
    args = parser.parse_args()
    observed = json.loads(args.observed.read_text(encoding="utf-8"))
    expected = json.loads(args.expected.read_text(encoding="utf-8"))
    assert_json_close(observed, expected, atol=args.atol)
    print("JSON documents match within numeric tolerance")


if __name__ == "__main__":
    main()
