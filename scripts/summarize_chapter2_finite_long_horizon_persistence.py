"""Summarize prospective finite-population long-horizon persistence shards."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def _mean(x):
    vals = [float(v) for v in x if v is not None and np.isfinite(v)]
    return None if not vals else float(np.mean(vals))


def summarize(design, folder):
    files = sorted(Path(folder).glob("finite-shard-*.json"))
    if not files:
        raise ValueError("no finite persistence shards")
    rows = []
    for path in files:
        doc = json.loads(path.read_text(encoding="utf-8"))
        if doc["status"] != "complete_finite_long_horizon_persistence_shard":
            raise ValueError(f"incomplete shard {path}")
        rows.extend(doc["rows"])

    checkpoints = [int(x) for x in design["horizons"]]
    reports = []
    extinction = []
    for dep in [float(x) for x in design["depressions"]]:
        drows = [r for r in rows if float(r["depression"]) == dep]
        for arm in ("near", "far"):
            ar = [r for r in drows if r["arm"] == arm]
            ext = [r["extinction_year"] for r in ar]
            extinction.append({
                "depression": dep,
                "arm": arm,
                "n": len(ar),
                "ever_extinct_by_6400_fraction": float(np.mean([x is not None for x in ext])),
                "median_extinction_year_among_extinct": (
                    None if not any(x is not None for x in ext)
                    else float(np.median([x for x in ext if x is not None]))
                ),
            })

        # Pair by depression/history/start/demo.
        keys = sorted({
            (int(r["history_seed"]), float(r["start_investment"]), int(r["demographic_seed"]))
            for r in drows
        })
        lookup = {
            (int(r["history_seed"]), float(r["start_investment"]), int(r["demographic_seed"]), r["arm"]): r
            for r in drows
        }
        for year in checkpoints:
            near_occ = []
            far_occ = []
            pair_occ = []
            effects = []
            for hs, start, ds in keys:
                nr = lookup[(hs, start, ds, "near")]
                fr = lookup[(hs, start, ds, "far")]
                nrep = next(q for q in nr["reports"] if int(q["year"]) == year)
                frep = next(q for q in fr["reports"] if int(q["year"]) == year)
                no = bool(nrep["occupied"])
                fo = bool(frep["occupied"])
                near_occ.append(no)
                far_occ.append(fo)
                pair_occ.append(no and fo)
                if no and fo:
                    effects.append(float(frep["investment_change"] - nrep["investment_change"]))
            reports.append({
                "depression": dep,
                "year": year,
                "n_pairs": len(keys),
                "near_occupancy": float(np.mean(near_occ)),
                "far_occupancy": float(np.mean(far_occ)),
                "paired_occupancy": float(np.mean(pair_occ)),
                "survivor_conditioned_mean_far_minus_near": _mean(effects),
                "n_paired_survivors": len(effects),
                "trait_stationarity_eligible": bool(
                    year in (3200, 6400) and float(np.mean(pair_occ)) >= 0.80
                ),
            })

    eligibility = {}
    for dep in [float(x) for x in design["depressions"]]:
        late = [r for r in reports if r["depression"] == dep and r["year"] in (3200, 6400)]
        eligibility[str(dep)] = bool(
            len(late) == 2 and all(r["paired_occupancy"] >= 0.80 for r in late)
        )

    return {
        "status": "complete_prospective_finite_long_horizon_persistence",
        "n_trajectories": len(rows),
        "reports": reports,
        "extinction_summary": extinction,
        "trait_stationarity_eligible_by_depression": eligibility,
        "interpretation": {
            str(dep): (
                "trait_stationarity_evaluable"
                if eligibility[str(dep)]
                else "persistence_gate_failed_trait_stationarity_survivor_conditioned_only"
            )
            for dep in [float(x) for x in design["depressions"]]
        },
        "claim_boundary": design["claim_boundary"],
        "source_shards": [p.name for p in files],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--design", required=True)
    p.add_argument("--input-dir", required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    design = json.loads(Path(a.design).read_text(encoding="utf-8"))
    result = summarize(design, Path(a.input_dir))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
