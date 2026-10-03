"""Aggregate prospective long-horizon stationarity shards."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def _rel_change(a, b):
    if a is None or b is None or not np.isfinite([a, b]).all():
        return None
    denom = max(abs(float(a)), abs(float(b)), 1e-12)
    return float(abs(float(b) - float(a)) / denom)


def _label(values, eps):
    vals = [v for v in values if v is not None and np.isfinite(v)]
    if len(vals) != len(values):
        return "undefined"
    pos = any(v > eps for v in vals)
    neg = any(v < -eps for v in vals)
    if pos and neg:
        return "mixed"
    if pos:
        return "positive"
    if neg:
        return "negative"
    return "neutral"


def _load_shards(folder, prefix):
    rows = []
    files = sorted(Path(folder).glob(f"{prefix}*.json"))
    if not files:
        raise ValueError(f"no shards for {prefix}")
    for path in files:
        doc = json.loads(path.read_text(encoding="utf-8"))
        rows.extend(doc["rows"])
    return rows, files


def _summarize_backbone(rows, design):
    checkpoints = [int(x) for x in design["checkpoints"]]
    histories = sorted({int(r["history_seed"]) for r in rows})
    starts = sorted({float(r["start_investment"]) for r in rows})
    eps = float(design["backbone"]["deadband"])
    reports = []
    labels_by_year = {}
    for year in checkpoints:
        yr = [r for r in rows if int(r["year"]) == year]
        effects = [r["effect_far_minus_near"] for r in yr if r["effect_far_minus_near"] is not None]
        mean = None if not effects else float(np.mean(effects))
        labels = {}
        for hs in histories:
            vals = [
                next(
                    r["effect_far_minus_near"]
                    for r in yr
                    if int(r["history_seed"]) == hs and float(r["start_investment"]) == start
                )
                for start in starts
            ]
            labels[str(hs)] = _label(vals, eps)
        labels_by_year[year] = labels
        counts = {k: list(labels.values()).count(k) for k in ("negative", "mixed", "positive", "neutral", "undefined")}
        eligible = len(histories) - counts["undefined"]
        reports.append({
            "year": year,
            "overall_mean_effect": mean,
            "mean_effect_by_start": {
                str(start): float(np.mean([
                    r["effect_far_minus_near"]
                    for r in yr
                    if float(r["start_investment"]) == start and r["effect_far_minus_near"] is not None
                ]))
                for start in starts
            },
            "history_label_counts_eps_0_01": counts,
            "mixed_fraction": None if eligible <= 0 else float(counts["mixed"] / eligible),
            "history_labels": labels,
        })

    transitions = []
    for a, b in zip(checkpoints[:-1], checkpoints[1:]):
        la, lb = labels_by_year[a], labels_by_year[b]
        eligible = [h for h in la if la[h] != "undefined" and lb[h] != "undefined"]
        same = None if not eligible else float(np.mean([la[h] == lb[h] for h in eligible]))
        ra = next(r for r in reports if r["year"] == a)
        rb = next(r for r in reports if r["year"] == b)
        ma, mb = ra["overall_mean_effect"], rb["overall_mean_effect"]
        abs_change = None if ma is None or mb is None else float(abs(mb - ma))
        rel_change = _rel_change(ma, mb)
        mixed_change = (
            None
            if ra["mixed_fraction"] is None or rb["mixed_fraction"] is None
            else float(abs(rb["mixed_fraction"] - ra["mixed_fraction"]))
        )
        transitions.append({
            "from": a,
            "to": b,
            "mean_abs_change": abs_change,
            "mean_relative_change": rel_change,
            "mean_sign_unchanged": None if ma is None or mb is None else bool(np.sign(ma) == np.sign(mb)),
            "history_label_agreement": same,
            "mixed_fraction_abs_change": mixed_change,
        })

    late = {(t["from"], t["to"]): t for t in transitions}
    checks = []
    for pair in ((1600, 3200), (3200, 6400)):
        t = late[pair]
        mean_ok = bool(
            t["mean_sign_unchanged"]
            and (
                (t["mean_abs_change"] is not None and t["mean_abs_change"] <= 0.01)
                or (t["mean_relative_change"] is not None and t["mean_relative_change"] <= 0.05)
            )
        )
        label_ok = bool(
            t["history_label_agreement"] is not None
            and t["history_label_agreement"] >= 0.95
            and t["mixed_fraction_abs_change"] is not None
            and t["mixed_fraction_abs_change"] <= 0.05
        )
        checks.append({"interval": list(pair), "coarse_mean_ok": mean_ok, "history_labels_ok": label_ok})
    stable = bool(all(x["coarse_mean_ok"] and x["history_labels_ok"] for x in checks))
    final = next(r for r in reports if r["year"] == 6400)
    return {
        "n_rows": len(rows),
        "n_histories": len(histories),
        "n_starts": len(starts),
        "reports": reports,
        "transitions": transitions,
        "late_stationarity_checks": checks,
        "finite_horizon_stationary_by_6400": stable,
        "final_aggregate_negative": bool(final["overall_mean_effect"] is not None and final["overall_mean_effect"] < 0),
        "final_history_nonparallelism_present": bool(
            final["history_label_counts_eps_0_01"]["mixed"] > 0
            or final["history_label_counts_eps_0_01"]["positive"] > 0
        ),
    }


def _mean(values):
    vals = [v for v in values if v is not None and np.isfinite(v)]
    return None if not vals else float(np.mean(vals))


def _summarize_mutation(rows, design):
    checkpoints = [int(x) for x in design["checkpoints"]]
    reports = []
    for year in checkpoints:
        high = []
        low = []
        low_va_by_cell = {}
        for row in rows:
            rep = next(r for r in row["reports"] if int(r["year"]) == year)
            response = rep["investment_response"]
            if row["standing_regime"] == "high_reference":
                if response is not None:
                    high.append(abs(response))
            elif row["standing_regime"] == "low":
                if response is not None:
                    low.append(abs(response))
                key = f'N{row["capacity"]}|{row["visitor_history"]}'
                low_va_by_cell.setdefault(key, []).append(rep["investment_va_proxy"])
        high_mean = _mean(high)
        low_mean = _mean(low)
        ratio = None if high_mean is None or low_mean is None or low_mean <= 0 else float(high_mean / low_mean)
        reports.append({
            "year": year,
            "high_standing_abs_response": high_mean,
            "low_standing_r0_01_abs_response": low_mean,
            "high_low_response_ratio": ratio,
            "low_standing_va_by_cell": {k: _mean(v) for k, v in sorted(low_va_by_cell.items())},
        })

    by_year = {r["year"]: r for r in reports}
    checks = []
    for a, b in ((1600, 3200), (3200, 6400)):
        ra, rb = by_year[a], by_year[b]
        ratio_change = _rel_change(ra["high_low_response_ratio"], rb["high_low_response_ratio"])
        ratio_ok = bool(ratio_change is not None and ratio_change <= 0.10)
        va = []
        for key in sorted(ra["low_standing_va_by_cell"]):
            change = _rel_change(ra["low_standing_va_by_cell"][key], rb["low_standing_va_by_cell"][key])
            va.append({"cell": key, "relative_change": change, "ok": bool(change is not None and change <= 0.10)})
        checks.append({
            "interval": [a, b],
            "response_ratio_relative_change": ratio_change,
            "response_ratio_ok": ratio_ok,
            "va_checks": va,
            "all_va_ok": bool(va and all(x["ok"] for x in va)),
        })
    stable = bool(all(x["response_ratio_ok"] and x["all_va_ok"] for x in checks))
    final = by_year[6400]
    return {
        "n_trajectories": len(rows),
        "reports": reports,
        "late_stationarity_checks": checks,
        "finite_horizon_stationary_by_6400": stable,
        "standing_gap_persists_at_6400": bool(
            final["high_low_response_ratio"] is not None
            and final["high_low_response_ratio"] > 1.0
        ),
    }


def summarize(design, folder):
    backbone_rows, backbone_files = _load_shards(folder, "backbone-shard-")
    mutation_rows, mutation_files = _load_shards(folder, "mutation-shard-")
    backbone = _summarize_backbone(backbone_rows, design)
    mutation = _summarize_mutation(mutation_rows, design)

    if backbone["finite_horizon_stationary_by_6400"]:
        if backbone["final_aggregate_negative"] and backbone["final_history_nonparallelism_present"]:
            backbone_interpretation = "stationary_coarse_recurrence_with_persistent_trajectory_nonparallelism"
        elif backbone["final_aggregate_negative"]:
            backbone_interpretation = "stationary_coarse_recurrence_with_history_convergence"
        else:
            backbone_interpretation = "stationary_but_coarse_direction_not_preserved"
    else:
        backbone_interpretation = "not_stationary_by_6400"

    if mutation["finite_horizon_stationary_by_6400"]:
        mutation_interpretation = (
            "stationary_standing_gap_persists"
            if mutation["standing_gap_persists_at_6400"]
            else "stationary_standing_gap_disappears"
        )
    else:
        mutation_interpretation = "not_stationary_by_6400"

    return {
        "status": "complete_prospective_long_horizon_stationarity",
        "design_status": design["status"],
        "max_horizon": int(design["max_horizon"]),
        "time_unit": design["time_interpretation"]["unit"],
        "backbone": backbone,
        "mutation_accessibility": mutation,
        "interpretation": {
            "backbone": backbone_interpretation,
            "mutation_accessibility": mutation_interpretation,
        },
        "source_shards": {
            "backbone": [p.name for p in backbone_files],
            "mutation": [p.name for p in mutation_files],
        },
        "claim_boundary": design["claim_boundary"],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--design", required=True)
    p.add_argument("--input-dir", required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    design = json.loads(Path(a.design).read_text(encoding="utf-8"))
    result = summarize(design, Path(a.input_dir))
    encoded = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
