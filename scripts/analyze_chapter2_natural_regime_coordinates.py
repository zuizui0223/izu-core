from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import median

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "data/design/chapter2_natural_regime_analysis_plan_20260913.json"
DEFAULT_OUT = ROOT / "data/results/chapter2_natural_regime_coordinates.json"

REQUIRED_COLUMNS = {
    "source_study_id",
    "archipelago_id",
    "system_id",
    "time_bin",
    "partner_id",
    "value",
    "effort",
}


def _hill_d1(values: np.ndarray) -> float:
    total = float(values.sum())
    if total <= 0:
        return float("nan")
    p = values[values > 0] / total
    return float(math.exp(-float(np.sum(p * np.log(p)))))


def _sample_sd(values: np.ndarray) -> float:
    if len(values) < 2:
        return float("nan")
    return float(np.std(values, ddof=1))


def _phi(matrix: np.ndarray) -> tuple[float, list[int]]:
    sds = np.std(matrix, axis=0, ddof=1)
    eligible = [int(i) for i, sd in enumerate(sds) if math.isfinite(float(sd)) and float(sd) > 0]
    if len(eligible) < 3:
        return float("nan"), eligible
    denom = float(np.sum(sds[eligible])) ** 2
    if denom <= 0:
        return float("nan"), eligible
    total = matrix[:, eligible].sum(axis=1)
    return float(np.var(total, ddof=1) / denom), eligible


def _mean_pairwise_r(matrix: np.ndarray, eligible: list[int]) -> float:
    if len(eligible) < 2:
        return float("nan")
    sub = matrix[:, eligible]
    corr = np.corrcoef(sub, rowvar=False)
    values: list[float] = []
    for i in range(len(eligible)):
        for j in range(i + 1, len(eligible)):
            r = float(corr[i, j])
            if math.isfinite(r):
                r = min(max(r, -(1.0 - 1e-12)), 1.0 - 1e-12)
                values.append(math.atanh(r))
    if not values:
        return float("nan")
    return float(math.tanh(sum(values) / len(values)))


def _stable_seed(base: int, key: str) -> int:
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    offset = int.from_bytes(digest[:8], "big") % 1_000_000_000
    return int(base) + offset


def _weighted_quantile(values: np.ndarray, weights: np.ndarray, q: float) -> float:
    order = np.argsort(values, kind="mergesort")
    v = values[order]
    w = weights[order]
    cumulative = np.cumsum(w) / float(np.sum(w))
    idx = int(np.searchsorted(cumulative, q, side="left"))
    idx = min(idx, len(v) - 1)
    return float(v[idx])


def _midranks(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=float)
    i = 0
    while i < len(values):
        j = i + 1
        while j < len(values) and values[order[j]] == values[order[i]]:
            j += 1
        rank = (i + 1 + j) / 2.0
        ranks[order[i:j]] = rank
        i = j
    return ranks


def _weighted_corr(x: np.ndarray, y: np.ndarray, weights: np.ndarray) -> float:
    w = weights / float(np.sum(weights))
    mx = float(np.sum(w * x))
    my = float(np.sum(w * y))
    dx = x - mx
    dy = y - my
    cov = float(np.sum(w * dx * dy))
    vx = float(np.sum(w * dx * dx))
    vy = float(np.sum(w * dy * dy))
    if vx <= 0 or vy <= 0:
        return float("nan")
    return float(cov / math.sqrt(vx * vy))


def _source_balanced_weights(rows: list[dict]) -> np.ndarray:
    by_source: dict[str, list[int]] = defaultdict(list)
    for i, row in enumerate(rows):
        by_source[row["source_study_id"]].append(i)
    n_sources = len(by_source)
    weights = np.zeros(len(rows), dtype=float)
    for indices in by_source.values():
        per_system = 1.0 / (n_sources * len(indices))
        for i in indices:
            weights[i] = per_system
    return weights


def _dispersion_summary(rows: list[dict]) -> dict:
    if not rows:
        return {
            "systems": 0,
            "source_studies": 0,
            "archipelago_groups": 0,
            "D1_q90_q10_ratio": None,
            "phi_q90_q10_span": None,
            "weighted_spearman_logD1_phi": None,
            "interior_occupancy": None,
        }
    d1 = np.asarray([float(row["breadth_D1"]) for row in rows], dtype=float)
    phi = np.asarray([float(row["phi"]) for row in rows], dtype=float)
    weights = _source_balanced_weights(rows)
    q10_d1 = _weighted_quantile(d1, weights, 0.10)
    q90_d1 = _weighted_quantile(d1, weights, 0.90)
    q10_phi = _weighted_quantile(phi, weights, 0.10)
    q90_phi = _weighted_quantile(phi, weights, 0.90)
    logd1 = np.log(d1)
    spearman = _weighted_corr(_midranks(logd1), _midranks(phi), weights)
    x25, x75 = np.quantile(logd1, [0.25, 0.75])
    y25, y75 = np.quantile(phi, [0.25, 0.75])
    interior = float(np.mean((logd1 >= x25) & (logd1 <= x75) & (phi >= y25) & (phi <= y75)))
    return {
        "systems": len(rows),
        "source_studies": len({row["source_study_id"] for row in rows}),
        "archipelago_groups": len({row["archipelago_id"] for row in rows}),
        "D1_q10": q10_d1,
        "D1_q90": q90_d1,
        "D1_q90_q10_ratio": float(q90_d1 / q10_d1) if q10_d1 > 0 else None,
        "phi_q10": q10_phi,
        "phi_q90": q90_phi,
        "phi_q90_q10_span": float(q90_phi - q10_phi),
        "weighted_spearman_logD1_phi": spearman,
        "interior_occupancy": interior,
    }


def _nee_dispersion_pass(summary: dict, thresholds: dict) -> bool:
    values = (
        summary.get("D1_q90_q10_ratio"),
        summary.get("phi_q90_q10_span"),
        summary.get("weighted_spearman_logD1_phi"),
        summary.get("interior_occupancy"),
    )
    if any(value is None or not math.isfinite(float(value)) for value in values):
        return False
    return bool(
        summary["D1_q90_q10_ratio"] >= thresholds["D1_q90_q10_ratio_min"]
        and summary["phi_q90_q10_span"] >= thresholds["phi_q90_q10_span_min"]
        and abs(summary["weighted_spearman_logD1_phi"]) <= thresholds["abs_weighted_spearman_max"]
        and summary["interior_occupancy"] >= thresholds["interior_occupancy_min"]
    )


def classify_route(rows: list[dict], plan: dict) -> dict:
    summary = _dispersion_summary(rows)
    fallback = plan["route_thresholds"]["fallback_minimum"]
    nee = plan["route_thresholds"]["nee_candidate"]
    if (
        summary["systems"] < fallback["systems"]
        or summary["source_studies"] < fallback["source_studies"]
        or summary["archipelago_groups"] < fallback["archipelago_groups"]
    ):
        return {"route": "fallback_Oikos_plus_EL", "summary": summary, "leave_largest_source_out": None}

    count_pass = bool(
        summary["systems"] >= nee["systems"]
        and summary["source_studies"] >= nee["source_studies"]
        and summary["archipelago_groups"] >= nee["archipelago_groups"]
    )
    dispersion_pass = _nee_dispersion_pass(summary, nee)

    counts = defaultdict(int)
    for row in rows:
        counts[row["source_study_id"]] += 1
    largest_source = sorted(counts, key=lambda source: (-counts[source], source))[0]
    loo_rows = [row for row in rows if row["source_study_id"] != largest_source]
    loo_summary = _dispersion_summary(loo_rows)
    loo_pass = _nee_dispersion_pass(loo_summary, nee)

    if count_pass and dispersion_pass and loo_pass:
        route = "NEE_candidate"
    else:
        route = "Ecology_Letters_combined"
    return {
        "route": route,
        "summary": summary,
        "leave_largest_source_out": {
            "excluded_source": largest_source,
            "summary": loo_summary,
            "dispersion_criteria_pass": loo_pass,
        },
        "nee_count_criteria_pass": count_pass,
        "nee_dispersion_criteria_pass": dispersion_pass,
    }


def load_canonical_csv(path: Path) -> dict[tuple[str, str, str], dict]:
    systems: dict[tuple[str, str, str], dict] = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not REQUIRED_COLUMNS.issubset(set(reader.fieldnames)):
            missing = sorted(REQUIRED_COLUMNS - set(reader.fieldnames or []))
            raise ValueError(f"missing required columns: {missing}")
        for line_number, raw in enumerate(reader, start=2):
            source = raw["source_study_id"].strip()
            archipelago = raw["archipelago_id"].strip()
            system = raw["system_id"].strip()
            time_bin = raw["time_bin"].strip()
            partner = raw["partner_id"].strip()
            if not all((source, archipelago, system, time_bin, partner)):
                raise ValueError(f"blank identifier at line {line_number}")
            value = float(raw["value"])
            effort = float(raw["effort"])
            if value < 0 or not math.isfinite(value):
                raise ValueError(f"invalid value at line {line_number}")
            if effort <= 0 or not math.isfinite(effort):
                raise ValueError(f"invalid effort at line {line_number}")
            key = (source, archipelago, system)
            record = systems.setdefault(key, {"time_bins": set(), "partners": set(), "values": defaultdict(float)})
            record["time_bins"].add(time_bin)
            record["partners"].add(partner)
            record["values"][(time_bin, partner)] += value / effort
    return systems


def _matrix_for(record: dict) -> tuple[list[str], list[str], np.ndarray]:
    time_bins = sorted(record["time_bins"])
    partners = sorted(record["partners"])
    matrix = np.zeros((len(time_bins), len(partners)), dtype=float)
    t_index = {value: i for i, value in enumerate(time_bins)}
    p_index = {value: i for i, value in enumerate(partners)}
    for (time_bin, partner), value in record["values"].items():
        matrix[t_index[time_bin], p_index[partner]] = float(value)
    return time_bins, partners, matrix


def analyze_system(key: tuple[str, str, str], record: dict, plan: dict) -> dict:
    source, archipelago, system = key
    time_bins, partners, matrix = _matrix_for(record)
    minimum_bins = int(plan["preprocessing"]["minimum_time_bins"])
    minimum_series = int(plan["preprocessing"]["minimum_nonconstant_partner_series"])
    if len(time_bins) < minimum_bins:
        raise ValueError(f"{key}: fewer than {minimum_bins} time bins")
    phi, eligible = _phi(matrix)
    if len(eligible) < minimum_series or not math.isfinite(phi):
        raise ValueError(f"{key}: fewer than {minimum_series} nonconstant partner series")

    pooled = matrix.sum(axis=0)
    d1 = _hill_d1(pooled)
    richness = int(np.sum(pooled > 0))
    per_bin = [_hill_d1(matrix[i]) for i in range(len(time_bins)) if float(matrix[i].sum()) > 0]
    pairwise = _mean_pairwise_r(matrix, eligible)
    m = len(eligible)
    rho_eq = float((m * phi - 1.0) / (m - 1.0)) if m > 1 else float("nan")

    bootstrap = plan["bootstrap"]
    rng = np.random.default_rng(_stable_seed(int(bootstrap["seed"]), "|".join(key)))
    b_d1: list[float] = []
    b_phi: list[float] = []
    for _ in range(int(bootstrap["replicates"])):
        indices = rng.integers(0, len(time_bins), size=len(time_bins))
        sample = matrix[indices]
        bd1 = _hill_d1(sample.sum(axis=0))
        bphi, beligible = _phi(sample)
        if math.isfinite(bd1):
            b_d1.append(bd1)
        if len(beligible) >= minimum_series and math.isfinite(bphi):
            b_phi.append(bphi)
    min_valid = int(bootstrap["minimum_valid_phi_replicates"])
    if len(b_phi) < min_valid:
        raise ValueError(f"{key}: only {len(b_phi)} valid phi bootstrap replicates; require {min_valid}")

    return {
        "source_study_id": source,
        "archipelago_id": archipelago,
        "system_id": system,
        "time_bins": len(time_bins),
        "partner_count": len(partners),
        "eligible_synchrony_partners": m,
        "breadth_D1": d1,
        "breadth_D1_ci95": [float(np.quantile(b_d1, 0.025)), float(np.quantile(b_d1, 0.975))],
        "observed_partner_richness": richness,
        "D1_over_observed_partner_richness": float(d1 / richness) if richness else None,
        "median_time_bin_D1": float(median(per_bin)) if per_bin else None,
        "phi": phi,
        "phi_ci95": [float(np.quantile(b_phi, 0.025)), float(np.quantile(b_phi, 0.975))],
        "mean_pairwise_r": pairwise,
        "rho_eq": rho_eq,
        "bootstrap_valid_phi_replicates": len(b_phi),
    }


def run(input_path: Path, plan_path: Path = PLAN) -> dict:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    systems = load_canonical_csv(input_path)
    rows = [analyze_system(key, systems[key], plan) for key in sorted(systems)]
    route = classify_route(rows, plan)
    return {
        "schema_version": "1.0",
        "analysis": "chapter2_natural_regime_coordinates",
        "plan": str(plan_path.relative_to(ROOT)) if plan_path.is_relative_to(ROOT) else str(plan_path),
        "input": str(input_path),
        "systems": rows,
        "route_decision": route,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--plan", type=Path, default=PLAN)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    result = run(args.input, args.plan)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["route_decision"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
