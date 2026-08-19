from __future__ import annotations

import csv
import importlib.util
import json
import math
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRADIENT_SCRIPT = ROOT / "scripts/run_abm_v4_global_continuous_isolation_gradient.py"
GEO = ROOT / "data/results/frozen_candidate_gift_geography_match.json"
TARGETS = ROOT / "data/results/frozen_dore_network_targets.csv"
OUT = ROOT / "data/results/abm_v4_dore_named_system_prediction.json"
SATURATIONS = (1.0, 1.5, 2.0, 2.5, 3.0)


def load_gradient():
    spec = importlib.util.spec_from_file_location("abm_v4_named_prediction", GRADIENT_SCRIPT)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    assert spec.loader is not None
    spec.loader.exec_module(m)
    return m


def solve(a, b):
    n = len(b)
    x = [list(map(float, a[i])) + [float(b[i])] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(x[r][c]))
        if abs(x[p][c]) < 1e-10:
            x[p][c] += 1e-8
        x[c], x[p] = x[p], x[c]
        d = x[c][c]
        x[c] = [v / d for v in x[c]]
        for r in range(n):
            if r == c:
                continue
            f = x[r][c]
            x[r] = [x[r][j] - f * x[c][j] for j in range(n + 1)]
    return [x[i][-1] for i in range(n)]


def ols_beta(rows, y, predictors):
    p = len(predictors(rows[0]))
    xtx = [[0.0] * p for _ in range(p)]
    xty = [0.0] * p
    for r, yy in zip(rows, y):
        xx = predictors(r)
        for i in range(p):
            xty[i] += xx[i] * yy
            for j in range(p):
                xtx[i][j] += xx[i] * xx[j]
    for i in range(p):
        xtx[i][i] += 1e-8
    return solve(xtx, xty)


def predict(beta, row, predictors):
    x = predictors(row)
    return sum(a*b for a,b in zip(beta,x))


def midrank_ecdf(values):
    unique = sorted(set(values))
    if len(unique) == 1:
        return {unique[0]: 0.5}
    return {v: i / (len(unique)-1) for i,v in enumerate(unique)}


def load_rows():
    geo = json.loads(GEO.read_text())
    by_region = {}
    for m in geo["matches"]:
        if m.get("kind") != "dore_network_location" or not m.get("auto_lock") or not m.get("region_pub"):
            continue
        top = m["top_candidates"][0]
        if top.get("distance_to_mainland_km") is None:
            continue
        by_region[m["region_pub"]] = top
    rows = []
    with TARGETS.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["region_pub"] not in by_region:
                continue
            g = by_region[r["region_pub"]]
            rows.append({
                "region_pub": r["region_pub"],
                "system": r["system"],
                "stratum": r["stratum"],
                "sampling_time": float(r["sampling_time"]),
                "annual_time_span": float(r["annual_time_span"]),
                "sampling_type_TO": 1.0 if r["sampling_type"] == "TO" else 0.0,
                "pollinator_richness": float(r["pollinator_richness"]),
                "link_richness": float(r["link_richness"]),
                "entity_ID": str(g["entity_ID"]),
                "gift_entity": g["geo_entity"],
                "dist": float(g["distance_to_mainland_km"]),
                "area": None if g.get("area_km2") is None else float(g["area_km2"]),
                "elev": None if g.get("max_elevation_m") is None else float(g["max_elevation_m"]),
            })
    ecdf = midrank_ecdf([r["dist"] for r in rows]) if rows else {}
    for r in rows:
        r["z_distance"] = ecdf[r["dist"]]
    return geo, rows


def sampling_design(r):
    # Mirrors the source richness-model measurement layer: ln_time + ln_ATS + Sampling_type.
    return [1.0, math.log1p(r["sampling_time"]), math.log1p(r["annual_time_span"]), r["sampling_type_TO"]]


def model_predictors(kind, abm_key=None):
    if kind == "effort_only":
        return lambda r: sampling_design(r)
    if kind == "distance_quadratic":
        return lambda r: sampling_design(r) + [r["z_distance"], r["z_distance"]**2]
    if kind == "abm":
        return lambda r: sampling_design(r) + [math.log1p(r[abm_key])]
    raise ValueError(kind)


def loo_scores(rows, target, model_kind, abm_key=None):
    systems = sorted({r["system"] for r in rows})
    errors = []
    per_system = {}
    pred_fn = model_predictors(model_kind, abm_key)
    for hold in systems:
        train = [r for r in rows if r["system"] != hold]
        test = [r for r in rows if r["system"] == hold]
        if not train or not test:
            continue
        y = [math.log1p(r[target]) for r in train]
        beta = ols_beta(train, y, pred_fn)
        fold = []
        for r in test:
            pred_log = predict(beta, r, pred_fn)
            obs_log = math.log1p(r[target])
            e = pred_log - obs_log
            errors.append(e)
            fold.append(e)
        per_system[hold] = {
            "n_rows": len(fold),
            "mae_log": statistics.mean(abs(e) for e in fold),
            "rmse_log": math.sqrt(statistics.mean(e*e for e in fold)),
        }
    return {
        "n_rows": len(errors),
        "n_systems": len(per_system),
        "mae_log": statistics.mean(abs(e) for e in errors) if errors else None,
        "rmse_log": math.sqrt(statistics.mean(e*e for e in errors)) if errors else None,
        "per_system": per_system,
    }


def run_abm_predictions(rows, saturation, replicates=80, seed=20260819):
    grad = load_gradient()
    m = grad.load_v4()
    cache = {}
    for r in rows:
        key = (r["entity_ID"], r["z_distance"])
        if key in cache:
            continue
        sims = [grad.run_one(m, r["z_distance"], seed+i, saturation=saturation) for i in range(replicates)]
        cache[key] = {
            "abm_partner_types": statistics.mean(x["final_partner_types"] for x in sims),
            "abm_effective_links": statistics.mean(x["effective_links"] for x in sims),
        }
    for r in rows:
        r.update(cache[(r["entity_ID"], r["z_distance"])])
    return rows


def build():
    geo, base_rows = load_rows()
    systems = sorted({r["system"] for r in base_rows})
    coverage = {
        "frozen_dore_targets": sum(1 for m in geo["matches"] if m.get("kind") == "dore_network_location"),
        "auto_locked_dore_targets_with_dist": len(base_rows),
        "systems_with_usable_rows": systems,
        "n_systems": len(systems),
    }
    results = {}
    for sat in SATURATIONS:
        rows = run_abm_predictions([dict(r) for r in base_rows], sat)
        targets = {}
        for target, abm_key in (("pollinator_richness", "abm_partner_types"), ("link_richness", "abm_effective_links")):
            effort = loo_scores(rows, target, "effort_only")
            dist = loo_scores(rows, target, "distance_quadratic")
            abm = loo_scores(rows, target, "abm", abm_key)
            targets[target] = {
                "effort_only": effort,
                "distance_quadratic": dist,
                "abm_plus_effort": abm,
                "abm_improves_over_effort_mae": abm["mae_log"] < effort["mae_log"] if abm["mae_log"] is not None else False,
                "abm_improves_over_distance_quadratic_mae": abm["mae_log"] < dist["mae_log"] if abm["mae_log"] is not None else False,
            }
        results[str(sat)] = targets

    robust = {}
    for target in ("pollinator_richness", "link_richness"):
        over_effort = sum(results[str(s)][target]["abm_improves_over_effort_mae"] for s in SATURATIONS)
        over_distance = sum(results[str(s)][target]["abm_improves_over_distance_quadratic_mae"] for s in SATURATIONS)
        robust[target] = {
            "saturations_beating_effort_only": over_effort,
            "saturations_beating_distance_quadratic": over_distance,
            "robust_predictive_gain_over_distance": over_distance >= 4,
        }
    full_robust = all(v["robust_predictive_gain_over_distance"] for v in robust.values())
    return {
        "analysis": "abm_v4_dore_named_system_leave_one_system_out_prediction",
        "mapping_preregistered_before_target_extraction": "data/design/global_abm_geography_to_constraint_mapping_v1.json",
        "primary_mapping": "distance_ecdf",
        "measurement_covariates": "Doré source-richness design: log1p(Sampling_time) + log1p(Annual_time_span) + Sampling_type(T vs TO)",
        "coverage": coverage,
        "saturation_results": results,
        "summary": robust,
        "decision": "robust_mechanistic_predictive_gain_over_quadratic_distance_baseline" if full_robust else "no_robust_mechanistic_predictive_advantage_over_quadratic_distance_baseline",
        "interpretation_rule": "Failure to beat the quadratic distance baseline does not invalidate directional compatibility; it means the current v4 mechanism has not earned predictive advantage over a non-mechanistic geography curve on this held-out-system test.",
        "claim_boundary": "This first named-system test is limited to Doré candidate systems whose GIFT island geography is source-locked. Pollinator/link richness retain the source sampling-design layer; Data_type is not substituted for Sampling_type. Matrix-derived diversity/niche-overlap and the western-Pacific stratum remain later gates. No system may be replaced based on fit, and no saturation value is selected post hoc.",
    }


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(build(), indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
