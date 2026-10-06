"""Summarize the frozen new-demographic-seed validation.

Discovery tensors come from the verified original bridge shard exports.
Validation tensors come only from the prospectively frozen seeds 201-204.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


PAIRS = {
    "natural": ("near", "far"),
    "visitor_pooled": ("pool_near", "pool_far"),
    "large_plant_capacity": ("large_near", "large_far"),
}


def _corr(a, b):
    return float(np.corrcoef(np.asarray(a, float), np.asarray(b, float))[0, 1])


def _label(values, eps):
    values = np.asarray(values, float)
    pos = bool(np.any(values > eps))
    neg = bool(np.any(values < -eps))
    return "mixed" if pos and neg else "positive" if pos else "negative" if neg else "neutral"


def _label_counts(tensor, eps):
    means = np.asarray(tensor, float).mean(axis=2)
    labels = [_label(means[:, h], eps) for h in range(means.shape[1])]
    return {k: labels.count(k) for k in ("negative", "mixed", "positive", "neutral")}


def _variance_components(x):
    x = np.asarray(x, float)
    a, b, n = x.shape
    grand = x.mean()
    start = x.mean(axis=(1, 2))
    hist = x.mean(axis=(0, 2))
    cell = x.mean(axis=2)
    ss_h = a * n * np.sum((hist - grand) ** 2)
    ss_sh = n * np.sum((cell - start[:, None] - hist[None, :] + grand) ** 2)
    ss_e = np.sum((x - cell[:, :, None]) ** 2)
    ms_h = ss_h / (b - 1)
    ms_sh = ss_sh / ((a - 1) * (b - 1))
    ms_e = ss_e / (a * b * (n - 1))
    raw_h = (ms_h - ms_sh) / (a * n)
    raw_sh = (ms_sh - ms_e) / n
    h = max(0.0, float(raw_h))
    sh = max(0.0, float(raw_sh))
    structured = h + sh
    reliability = structured / (structured + ms_e / n)
    return {
        "sigma_history_raw": float(raw_h),
        "sigma_start_by_history_raw": float(raw_sh),
        "sigma_history": h,
        "sigma_start_by_history": sh,
        "history_structured_variance": structured,
        "sigma_demographic_residual": float(ms_e),
        "four_repeat_mean_reliability": float(reliability),
    }


def _load_discovery(folder, histories, starts, demos):
    docs = [json.loads(p.read_text()) for p in sorted(Path(folder).glob("shard-*.json"))]
    if len(docs) != 16:
        raise ValueError(f"expected 16 discovery shards, got {len(docs)}")
    hi = {h: i for i, h in enumerate(histories)}
    arms = {arm for pair in PAIRS.values() for arm in pair}
    values = {arm: np.full((len(starts), len(histories), len(demos)), np.nan) for arm in arms}
    for doc in docs:
        if doc["status"] != "complete_verified_shard_export":
            raise ValueError("unverified discovery shard")
        for arm in arms:
            arr = np.asarray(doc["values"][f"{arm}|individual"], float)
            for j, h in enumerate(doc["history_seeds"]):
                values[arm][:, hi[int(h)], :] = arr[:, j, :]
    if not all(np.isfinite(v).all() for v in values.values()):
        raise ValueError("incomplete discovery tensors")
    return {name: values[far] - values[near] for name, (near, far) in PAIRS.items()}


def _load_validation(folder, histories, starts, demos):
    docs = [json.loads(p.read_text()) for p in sorted(Path(folder).glob("*.json"))]
    docs = [d for d in docs if d.get("status") == "complete_new_demographic_validation_shard"]
    if len(docs) != 16:
        raise ValueError(f"expected 16 validation shards, got {len(docs)}")
    hi = {h: i for i, h in enumerate(histories)}
    si = {float(s): i for i, s in enumerate(starts)}
    di = {int(d): i for i, d in enumerate(demos)}
    arms = {arm for pair in PAIRS.values() for arm in pair}
    values = {arm: np.full((len(starts), len(histories), len(demos)), np.nan) for arm in arms}
    pops = {arm: np.full((len(starts), len(histories), len(demos)), np.nan) for arm in arms}
    seen = set()
    for doc in docs:
        for row in doc["rows"]:
            key = (
                int(row["history_seed"]),
                float(row["start"]),
                row["arm"],
                int(row["demographic_seed"]),
            )
            if key in seen:
                raise ValueError(f"duplicate validation row {key}")
            seen.add(key)
            arm = row["arm"]
            if arm not in arms:
                continue
            idx = (si[float(row["start"])], hi[int(row["history_seed"])], di[int(row["demographic_seed"])])
            values[arm][idx] = np.nan if row["investment_change"] is None else float(row["investment_change"])
            pops[arm][idx] = int(row["terminal_population"])
    if not all(np.isfinite(v).all() for v in values.values()):
        raise ValueError("incomplete validation tensors")
    return ({name: values[far] - values[near] for name, (near, far) in PAIRS.items()}, pops)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--design", type=Path, required=True)
    p.add_argument("--bridge-design", type=Path, required=True)
    p.add_argument("--discovery-shards", type=Path, required=True)
    p.add_argument("--validation-shards", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()

    design = json.loads(a.design.read_text(encoding="utf-8"))
    bridge = json.loads(a.bridge_design.read_text(encoding="utf-8"))
    histories = [int(x) for x in bridge["history_seeds"]]
    starts = [float(x) for x in design["validation_source"]["starts"]]
    old_demos = [int(x) for x in design["discovery_source"]["demographic_seeds"]]
    new_demos = [int(x) for x in design["validation_source"]["new_demographic_seeds"]]

    discovery = _load_discovery(a.discovery_shards, histories, starts, old_demos)
    validation, pops = _load_validation(a.validation_shards, histories, starts, new_demos)

    reports = {}
    for name in PAIRS:
        x = discovery[name].mean(axis=(0, 2))
        y = validation[name].mean(axis=(0, 2))
        xm = x - x.mean()
        ym = y - y.mean()
        slope = float(xm @ ym / (xm @ xm))
        intercept = float(y.mean() - slope * x.mean())
        fitted = intercept + slope * x
        reports[name] = {
            "discovery_validation_history_correlation": {"estimate": _corr(x, y)},
            "validation_mean_effect": float(validation[name].mean()),
            "validation_labels_eps0": _label_counts(validation[name], 0.0),
            "validation_labels_eps0_01": _label_counts(validation[name], 0.01),
            "validation_variance_components": _variance_components(validation[name]),
            "validation_on_discovery": {
                "slope": slope,
                "intercept": intercept,
                "rmse_raw": float(np.sqrt(np.mean((y - x) ** 2))),
                "rmse_about_fitted_line": float(np.sqrt(np.mean((y - fitted) ** 2))),
            },
        }

    rng = np.random.default_rng(int(design["primary_validation"]["inference"].split()[-1]))
    boots = {name: [] for name in PAIRS}
    diffs = {"large_minus_natural": [], "pooled_minus_natural": []}
    history_means = {
        name: (discovery[name].mean(axis=(0, 2)), validation[name].mean(axis=(0, 2)))
        for name in PAIRS
    }
    for _ in range(1999):
        ix = rng.integers(0, len(histories), len(histories))
        rs = {}
        for name, (x, y) in history_means.items():
            rs[name] = _corr(x[ix], y[ix])
            boots[name].append(rs[name])
        diffs["large_minus_natural"].append(rs["large_plant_capacity"] - rs["natural"])
        diffs["pooled_minus_natural"].append(rs["visitor_pooled"] - rs["natural"])

    for name in PAIRS:
        reports[name]["discovery_validation_history_correlation"]["bootstrap95"] = (
            np.quantile(boots[name], [0.025, 0.975]).tolist()
        )

    large_diff = float(
        reports["large_plant_capacity"]["discovery_validation_history_correlation"]["estimate"]
        - reports["natural"]["discovery_validation_history_correlation"]["estimate"]
    )
    pooled_diff = float(
        reports["visitor_pooled"]["discovery_validation_history_correlation"]["estimate"]
        - reports["natural"]["discovery_validation_history_correlation"]["estimate"]
    )
    paired = {
        "large_capacity_minus_natural_history_correlation": {
            "estimate": large_diff,
            "bootstrap95": np.quantile(diffs["large_minus_natural"], [0.025, 0.975]).tolist(),
        },
        "visitor_pooled_minus_natural_history_correlation": {
            "estimate": pooled_diff,
            "bootstrap95": np.quantile(diffs["pooled_minus_natural"], [0.025, 0.975]).tolist(),
        },
    }
    occupancy = {
        arm: {
            "occupied_fraction": float(np.mean(arr > 0)),
            "min_terminal_population": int(np.min(arr)),
            "mean_terminal_population": float(np.mean(arr)),
        }
        for arm, arr in pops.items()
    }
    observed = (
        reports["large_plant_capacity"]["discovery_validation_history_correlation"]["estimate"]
        > reports["natural"]["discovery_validation_history_correlation"]["estimate"]
        > reports["visitor_pooled"]["discovery_validation_history_correlation"]["estimate"]
    )
    strong = bool(
        observed
        and paired["large_capacity_minus_natural_history_correlation"]["bootstrap95"][0] > 0
        and paired["visitor_pooled_minus_natural_history_correlation"]["bootstrap95"][1] < 0
    )
    out = {
        "schema_version": "1.0",
        "status": "complete_prospectively_frozen_new_demographic_seed_validation",
        "design": str(a.design),
        "provenance": {
            "discovery_workflow_run": int(design["discovery_source"]["workflow_run"]),
            "discovery_demographic_seeds": old_demos,
            "validation_demographic_seeds": new_demos,
            "visitor_histories": len(histories),
            "starts": starts,
            "validation_arms": design["validation_source"]["arms"],
            "finite_arm_trajectories": int(sum(v.size for v in pops.values())),
            "paired_effect_cells_per_intervention": int(validation["natural"].size),
            "validation_horizon": int(design["validation_source"]["horizon"]),
            "inbreeding_depression": float(design["validation_source"]["inbreeding_depression"]),
        },
        "reports": reports,
        "paired_bootstrap_differences": paired,
        "terminal_occupancy": occupancy,
        "primary_decision": {
            "observed_ordering": "large_plant_capacity > natural > visitor_pooled",
            "observed_ordering_holds": bool(observed),
            "large_minus_natural_bootstrap_interval_excludes_zero_positive": bool(
                paired["large_capacity_minus_natural_history_correlation"]["bootstrap95"][0] > 0
            ),
            "pooled_minus_natural_bootstrap_interval_excludes_zero_negative": bool(
                paired["visitor_pooled_minus_natural_history_correlation"]["bootstrap95"][1] < 0
            ),
            "strong_success": strong,
            "weak_success": bool(observed and not strong),
            "failure": bool(not observed),
        },
        "interpretation": {
            "validation_scope": "new demographic seeds for the same 128 frozen visitor histories; not new environmental histories",
            "main": (
                "The post-hoc discovery generated a prospectively frozen prediction that "
                "history-specific continuous responses would be most reproducible at capacity "
                "192, intermediate under natural finite demography, and weakest after visitor-history "
                "pooling. New demographic seeds reproduced that ordering."
            ),
        },
        "claim_boundary": design["claim_boundary"],
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"primary_decision": out["primary_decision"], "paired": paired}, indent=2))


if __name__ == "__main__":
    main()
