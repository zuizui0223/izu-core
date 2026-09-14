from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "data/design/chapter2_natural_regime_analysis_plan_20260913.json"
DEFAULT_OUT = ROOT / "data/results/chapter2_natural_regime_six_source_checkpoint_20260915.json"
ANALYZER = ROOT / "scripts/analyze_chapter2_natural_regime_coordinates.py"

SOURCES = [
    ROOT / "data/results/chapter2_hawaii_natural_regime_coordinate_20260914.json",
    ROOT / "data/results/chapter2_mallorca_natural_regime_coordinates_20260914.json",
    ROOT / "data/results/chapter2_tenerife_natural_regime_coordinates_20260914.json",
    ROOT / "data/results/chapter2_cabrera_natural_regime_coordinates_20260914.json",
    ROOT / "data/results/chapter2_martinique_natural_regime_coordinates_20260914.json",
    ROOT / "data/results/chapter2_roberts_england_natural_regime_coordinates_20260915.json",
]


def load_classify_route():
    spec = importlib.util.spec_from_file_location("chapter2_natural_regime_analyzer", ANALYZER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load analyzer module from {ANALYZER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.classify_route


def rows_from_result(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw_rows = payload.get("systems")
    if raw_rows is None:
        raw_rows = [payload["coordinate"]]
    source = payload.get("source")
    rows = []
    for raw in raw_rows:
        row = dict(raw)
        if source is not None:
            row["source_study_id"] = source["source_study_id"]
            row["archipelago_id"] = source["archipelago_id"]
        if not row.get("source_study_id") or not row.get("archipelago_id"):
            raise RuntimeError(f"{path}: coordinate row lacks source/archipelago identity")
        rows.append(row)
    if not rows:
        raise RuntimeError(f"{path}: no coordinate rows")
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

    classify_route = load_classify_route()
    route = classify_route(rows, plan)
    result = {
        "schema_version": "1.0",
        "analysis": "chapter2_natural_regime_six_source_checkpoint",
        "status": "frozen_route_evaluation_after_six_admitted_sources",
        "evaluated_on": "2026-09-15",
        "analysis_plan": str(PLAN.relative_to(ROOT)),
        "source_result_files": source_files,
        "source_system_counts": source_counts,
        "systems": len(rows),
        "source_studies": len({row["source_study_id"] for row in rows}),
        "archipelago_groups": len({row["archipelago_id"] for row in rows}),
        "archipelago_ids": sorted({row["archipelago_id"] for row in rows}),
        "route_decision": route,
        "claim_boundary": (
            "The route is computed mechanically from the frozen natural-regime plan after the England STEP admission was committed before coordinates were opened. "
            "The England source is retained as a Great Britain continental-island group because EuPPollNet's manuscript pre-classified study 31_Roberts as an island study; this classification is not altered based on D1, phi or route effect. "
            "Mallorca and Cabrera remain separate source studies sharing the Balearic archipelago group. No threshold, source weight, site, time bin or taxon is changed after opening coordinates."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(route, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
