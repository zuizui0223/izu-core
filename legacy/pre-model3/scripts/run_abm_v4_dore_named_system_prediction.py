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
    return sum(a*b for a,b in zip(beta, predictors(row)))


def midrank_ecdf(values):
    unique = sorted(set(values))
    if len(unique) == 1:
        return {unique[0]: 0.5}
    return {v: i / (len(unique)-1) for i, v in enumerate(unique)}


def standardize_matrix(x):
    means = [statistics.mean(row[j] for row in x) for j in range(len(x[0]))]
    sds = []
    for j, mean in enumerate(means):
        sd = math.sqrt(statistics.mean((row[j]-mean)**2 for row in x))
        sds.append(sd if sd > 1e-12 else 1.0)
    return [[(row[j]-means[j])/sds[j] for j in range(len(row))] for row in x], means, sds


def pc1_scores(rows):
    unique = {}
    for r in rows:
        if r["area"] is None or r["elev"] is None or r["elev"] < 0:
            continue
        unique.setdefault(r["entity_ID"], [
            math.log1p(r["dist"]),
            -math.log1p(r["area"]),
            -math.log1p(r["elev"]),
        ])
    ids = sorted(unique)
    if len(ids) < 3:
        return {}, {"status": "insufficient_geography_rows"}
    z, means, sds = standardize_matrix([unique[i] for i in ids])
    p = 3
    cov = [[statistics.mean(row[i]*row[j] for row in z) for j in range(p)] for i in range(p)]
    v = [1/math.sqrt(p)] * p
    for _ in range(200):
        w = [sum(cov[i][j]*v[j] for j in range(p)) for i in range(p)]
        norm = math.sqrt(sum(q*q for q in w)) or 1.0
        w = [q/norm for q in w]
        if max(abs(a-b) for a,b in zip(w,v)) < 1e-12:
            v = w
            break
        v = w
    raw = [sum(row[j]*v[j] for j in range(p)) for row in z]
    dist_z = [row[0] for row in z]
    if sum(a*b for a,b in zip(raw, dist_z)) < 0:
        v = [-q for q in v]
        raw = [-q for q in raw]
    lo, hi = min(raw), max(raw)
    scaled = [0.5] * len(raw) if hi-lo < 1e-12 else [(q-lo)/(hi-lo) for q in raw]
    return dict(zip(ids, scaled)), {
        "status": "complete",
        "unique_entities": len(ids),
        "input_order": ["log1p(dist)", "-log1p(area)", "-log1p(max_elevation)"],
        "means": means,
        "sds": sds,
        "pc1_vector_oriented_to_positive_distance": v,
    }


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
    pcmap, pcmeta = pc1_scores(rows)
    for r in rows:
        r["z_geo_pc1"] = pcmap.get(r["entity_ID"])
    return geo, rows, pcmeta


def sampling_design(r):
    return [1.0, math.log1p(r["sampling_time"]), math.log1p(r["annual_time_span"]), r["sampling_type_TO"]]


def model_predictors(kind, z_key=None, abm_key=None):
    if kind == "effort_only":
        return lambda r: sampling_design(r)
    if kind == "geography_quadratic":
        return lambda r: sampling_design(r) + [r[z_key], r[z_key]**2]
    if kind == "abm":
        return lambda r: sampling_design(r) + [math.log1p(r[abm_key])]
    raise ValueError(kind)


def loo_scores(rows, target, model_kind, z_key=None, abm_key=None):
    systems = sorted({r["system"] for r in rows})
    errors = []
    per_system = {}
    pred_fn = model_predictors(model_kind, z_key, abm_key)
    for hold in systems:
        train = [r for r in rows if r["system"] != hold]
        test = [r for r in rows if r["system"] == hold]
        if not train or not test:
            continue
        beta = ols_beta(train, [math.log1p(r[target]) for r in train], pred_fn)
        fold = [predict(beta, r, pred_fn) - math.log1p(r[target]) for r in test]
        errors.extend(fold)
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


def run_abm_predictions(rows, saturation, z_key, prefix, replicates=80, seed=20260819):
    grad = load_gradient()
    m = grad.load_v4()
    cache = {}
    for r in rows:
        key = (r["entity_ID"], r[z_key])
        if key not in cache:
            sims = [grad.run_one(m, r[z_key], seed+i, saturation=saturation) for i in range(replicates)]
            cache[key] = {
                f"{prefix}_partner_types": statistics.mean(x["final_partner_types"] for x in sims),
                f"{prefix}_effective_links": statistics.mean(x["effective_links"] for x in sims),
            }
        r.update(cache[key])
    return rows


def evaluate_mapping(base_rows, z_key, prefix):
    usable = [dict(r) for r in base_rows if r.get(z_key) is not None]
    results = {}
    for sat in SATURATIONS:
        rows = run_abm_predictions([dict(r) for r in usable], sat, z_key, prefix)
        targets = {}
        for target, abm_key in (("pollinator_richness", f"{prefix}_partner_types"), ("link_richness", f"{prefix}_effective_links")):
            effort = loo_scores(rows, target, "effort_only")
            geography = loo_scores(rows, target, "geography_quadratic", z_key=z_key)
            abm = loo_scores(rows, target, "abm", abm_key=abm_key)
            targets[target] = {
                "effort_only": effort,
                "geography_quadratic": geography,
                "abm_plus_sampling_design": abm,
                "abm_improves_over_effort_mae": abm["mae_log"] < effort["mae_log"],
                "abm_improves_over_geography_quadratic_mae": abm["mae_log"] < geography["mae_log"],
            }
        results[str(sat)] = targets
    summary = {}
    for target in ("pollinator_richness", "link_richness"):
        over_effort = sum(results[str(s)][target]["abm_improves_over_effort_mae"] for s in SATURATIONS)
        over_geography = sum(results[str(s)][target]["abm_improves_over_geography_quadratic_mae"] for s in SATURATIONS)
        summary[target] = {
            "saturations_beating_effort_only": over_effort,
            "saturations_beating_geography_quadratic": over_geography,
            "robust_predictive_gain_over_geography": over_geography >= 4,
        }
    return {
        "coverage": {"n_rows": len(usable), "systems": sorted({r["system"] for r in usable})},
        "saturation_results": results,
        "summary": summary,
        "both_targets_robust_over_geography": all(v["robust_predictive_gain_over_geography"] for v in summary.values()),
    }


def build():
    geo, base_rows, pcmeta = load_rows()
    overall_coverage = {
        "frozen_dore_targets": sum(1 for m in geo["matches"] if m.get("kind") == "dore_network_location"),
        "source_locked_dore_targets_with_dist": len(base_rows),
        "systems_with_usable_rows": sorted({r["system"] for r in base_rows}),
        "n_systems": len({r["system"] for r in base_rows}),
    }
    primary = evaluate_mapping(base_rows, "z_distance", "distance_ecdf")
    secondary = evaluate_mapping(base_rows, "z_geo_pc1", "geography_pc1")
    primary_pass = primary["both_targets_robust_over_geography"]
    return {
        "analysis": "abm_v4_dore_named_system_leave_one_system_out_prediction",
        "mapping_preregistered_before_target_extraction": "data/design/global_abm_geography_to_constraint_mapping_v1.json",
        "measurement_covariates": "Doré source-richness design: log1p(Sampling_time) + log1p(Annual_time_span) + Sampling_type(T vs TO)",
        "overall_coverage": overall_coverage,
        "primary_distance_ecdf": primary,
        "secondary_geography_only_pc1": secondary,
        "geography_pc1_metadata": pcmeta,
        "decision": "primary_distance_mapping_has_robust_mechanistic_predictive_gain" if primary_pass else "primary_distance_mapping_has_no_robust_mechanistic_predictive_advantage",
        "interpretation_rule": "The primary distance-ECDF result controls the headline. The preregistered geography-PC1 sensitivity is reported regardless of whether it performs better or worse; it cannot replace the primary mapping post hoc. Failure to beat the primary geography baseline preserves directional compatibility but withholds mechanistic predictive superiority.",
        "claim_boundary": "This named-system test is restricted to Doré candidate systems whose GIFT island geography is source-locked. It does not yet include matrix-derived diversity/niche overlap or the western-Pacific fourth stratum. Systems, mappings and saturation values are frozen independently of fit; no poor-fitting system is replaced and no preferred saturation is selected.",
    }


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(build(), indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
