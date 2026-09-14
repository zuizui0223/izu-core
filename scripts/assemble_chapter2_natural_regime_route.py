from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.analyze_chapter2_natural_regime_coordinates import classify_route

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "data/design/chapter2_natural_regime_analysis_plan_20260913.json"
DEFAULT_OUT = ROOT / "data/results/chapter2_natural_regime_four_source_checkpoint_20260914.json"

SOURCES = [
    ROOT / "data/results/chapter2_hawaii_natural_regime_coordinate_20260914.json",
    ROOT / "data/results/chapter2_mallorca_natural_regime_coordinates_20260914.json",
    ROOT / "data/results/chapter2_tenerife_natural_regime_coordinates_20260914.json",
    ROOT / "data/results/chapter2_cabrera_natural_regime_coordinates_20260914.json",
]


def rows_from_result(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    source = payload["source"]
    source_id = source["source_study_id"]
    archipelago_id = source["archipelago_id"]
    raw_rows = payload.get("systems")
    if raw_rows is None:
        raw_rows = [payload["coordinate"]]
    rows = []
    for raw in raw_rows:
        row = dict(raw)
        row["source_study_id"] = source_id
        row["archipelago_id"] = archipelago_id
        rows.append(row)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    rows: list[dict] = []
    source_counts: dict[str, int] = {}
    source_files = []
    for path in SOURCES:
        current = rows_from_result(path)
        rows.extend(current)
        source_counts[current[0]["source_study_id"]] = len(current)
        source_files.append(str(path.relative_to(ROOT)))

    route = classify_route(rows, plan)
    result = {
        "schema_version": "1.0",
        "analysis": "chapter2_natural_regime_four_source_checkpoint",
        "status": "frozen_route_evaluation_after_four_admitted_sources",
        "evaluated_on": "2026-09-14",
        "analysis_plan": str(PLAN.relative_to(ROOT)),
        "source_result_files": source_files,
        "source_system_counts": source_counts,
        "systems": len(rows),
        "source_studies": len({row["source_study_id"] for row in rows}),
        "archipelago_groups": len({row["archipelago_id"] for row in rows}),
        "archipelago_ids": sorted({row["archipelago_id"] for row in rows}),
        "route_decision": route,
        "claim_boundary": (
            "The route is computed mechanically from the frozen natural-regime plan. "
            "Mallorca and Cabrera are separate source studies but share the Balearic archipelago group. "
            "No source is reweighted, removed or added based on its D1 or phi values."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(route, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
