#!/usr/bin/env python3
"""Run supplemental Izu acquisition with transport-safe GBIF queries.

The underlying acquisition module keeps the scientific extraction and aggregation
logic. This entry point applies transport-only safeguards:

- simplify the GSHHG query ring to at most 120 vertices;
- orient exterior rings counterclockwise as required by the GBIF geometry parser;
- normalize the occurrence-status query value; and
- preserve the GBIF HTTP response body and query dimensions when rejected.
"""
from __future__ import annotations

import importlib.util
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Sequence


MODULE_PATH = Path(__file__).with_name("acquire_supplemental_izu_gbif.py")
SPEC = importlib.util.spec_from_file_location("_izu_supplemental_acquisition", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

_ORIGINAL_SIMPLIFY = MODULE._simplify_closed_ring


def _signed_area(ring: Sequence[tuple[float, float]]) -> float:
    points = list(ring)
    if len(points) > 1 and points[0] == points[-1]:
        points = points[:-1]
    return 0.5 * sum(
        points[index][0] * points[(index + 1) % len(points)][1]
        - points[(index + 1) % len(points)][0] * points[index][1]
        for index in range(len(points))
    )


def _counterclockwise(ring: Sequence[tuple[float, float]]) -> list[tuple[float, float]]:
    points = list(ring)
    if points[0] == points[-1]:
        points = points[:-1]
    if _signed_area(points) < 0.0:
        points.reverse()
    points.append(points[0])
    return points


def _transport_safe_simplify(ring, maximum_points=700):
    del maximum_points
    simplified = _ORIGINAL_SIMPLIFY(ring, maximum_points=120)
    return _counterclockwise(simplified)


def _diagnostic_query_page(base_url: str, parameters: dict[str, object]) -> dict[str, object]:
    normalized = dict(parameters)
    if "occurrence_status" in normalized:
        normalized["occurrence_status"] = str(normalized["occurrence_status"]).lower()
    query = urllib.parse.urlencode(normalized)
    url = f"{base_url}?{query}"
    request = urllib.request.Request(url, headers={"User-Agent": MODULE.USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        geometry = str(normalized.get("geometry", ""))
        raise RuntimeError(
            "GBIF occurrence search rejected the polygon query: "
            f"status={exc.code}; url_length={len(url)}; "
            f"geometry_length={len(geometry)}; response={body[:4000]}"
        ) from exc


MODULE._simplify_closed_ring = _transport_safe_simplify
MODULE._query_page = _diagnostic_query_page


if __name__ == "__main__":
    MODULE.main()
