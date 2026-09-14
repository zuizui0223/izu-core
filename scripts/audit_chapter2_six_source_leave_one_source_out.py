from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "data/design/chapter2_natural_regime_analysis_plan_20260913.json"
ANALYZER = ROOT / "scripts/analyze_chapter2_natural_regime_coordinates.py"
OUT = ROOT / "data/results/chapter2_natural_regime_six_source_all_loo_diagnostic_20260915.json"
SOURCES = [
    ROOT / "data/results/chapter2_hawaii_natural_regime_coordinate_20260914.json",
    ROOT / "data/results/chapter2_mallorca_natural_regime_coordinates_20260914.json",
    ROOT / "data/results/chapter2_tenerife_natural_regime_coordinates_20260914.json",
    ROOT / "data/results/chapter2_cabrera_natural_regime_coordinates_20260914.json",
    ROOT / "data/results/chapter2_martinique_natural_regime_coordinates_20260914.json",
    ROOT / "data/results/chapter2_roberts_england_natural_regime_coordinates_20260915.json",
]


def load_analyzer():
    spec = importlib.util.spec_from_file_location("chapter2_regime_analyzer_loo", ANALYZER)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load natural-regime analyzer")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def rows_from_result(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw_rows = payload.get("systems") or [payload["coordinate"]]
    source = payload.get("source")
    rows = []
    for raw in raw_rows:
        row = dict(raw)
        if source is not None:
            row["source_study_id"] = source["source_study_id"]
            row["archipelago_id"] = source["archipelago_id"]
        if not row.get("source_study_id") or not row.get("archipelago_id"):
            raise RuntimeError(f"missing source identity in {path}")
        rows.append(row)
    return rows


def finite_summary(summary: dict) -> bool:
    keys = ["D1_q90_q10_ratio", "phi_q90_q10_span", "weighted_spearman_logD1_phi", "interior_occupancy"]
    return all(summary.get(key) is not None and math.isfinite(float(summary[key])) for key in keys)


def main() -> None:
    module = load_analyzer()
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    thresholds = plan["route_thresholds"]["nee_candidate"]
    rows: list[dict] = []
    for path in SOURCES:
        rows.extend(rows_from_result(path))

    full_summary = module._dispersion_summary(rows)
    sources = sorted({row["source_study_id"] for row in rows})
    diagnostics = []
    for source in sources:
        subset = [row for row in rows if row["source_study_id"] != source]
        summary = module._dispersion_summary(subset)
        diagnostics.append({
            "excluded_source": source,
            "systems_remaining": len(subset),
            "source_studies_remaining": len({row["source_study_id"] for row in subset}),
            "archipelago_groups_remaining": len({row["archipelago_id"] for row in subset}),
            "summary": summary,
            "nee_dispersion_criteria_pass": bool(finite_summary(summary) and module._nee_dispersion_pass(summary, thresholds)),
        })

    result = {
        "schema_version": "1.0",
        "analysis": "chapter2_natural_regime_six_source_all_leave_one_source_out_diagnostic",
        "status": "post_promotion_diagnostic_not_route_redefinition",
        "evaluated_on": "2026-09-15",
        "analysis_plan": str(PLAN.relative_to(ROOT)),
        "frozen_route_checkpoint": "data/results/chapter2_natural_regime_six_source_checkpoint_20260915.json",
        "full_summary": full_summary,
        "all_source_leave_one_out": diagnostics,
        "interpretation_rule": (
            "The preregistered NEE promotion rule requires robustness after leaving out the single largest source study, not every source. "
            "This all-source leave-one-out table is an additional transparency diagnostic and cannot retroactively change the frozen promotion criterion or trigger candidate hunting after the early-stop condition has been met."
        ),
        "claim_boundary": (
            "No source, system, threshold, time bin, partner or coordinate is modified. This diagnostic only recomputes the frozen dispersion summary after deleting each already-admitted source in turn."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "full_summary": full_summary,
        "leave_one_out": [
            {
                "excluded_source": row["excluded_source"],
                "phi_span": row["summary"]["phi_q90_q10_span"],
                "D1_ratio": row["summary"]["D1_q90_q10_ratio"],
                "interior": row["summary"]["interior_occupancy"],
                "pass": row["nee_dispersion_criteria_pass"],
            }
            for row in diagnostics
        ],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
