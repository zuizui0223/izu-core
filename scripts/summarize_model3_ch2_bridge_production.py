"""Prospective summary for the frozen Model 3 Chapter 2 bridge campaign.

This script is outcome-agnostic. It verifies every completed case receipt and
summarizes the predeclared far-minus-near inherited-investment contrast for:
natural, annual richness-matched, pooled visitor environment, and large plant
capacity arms, separately for finite ABM and deterministic genotype density.
"""
from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path

import numpy as np

from scripts.model3_island.design import canonical, digest
from scripts.model3_island.summarize import decompose_crossed


INTERVENTIONS = {
    "natural": ("near", "far"),
    "richness_matched": ("matched_near", "matched_far"),
    "visitor_pooled": ("pool_near", "pool_far"),
    "large_plant_capacity": ("large_near", "large_far"),
}
MODES = {
    "individual": ("trait_mean", "population"),
    "density": ("density_traits", "density_mass"),
}


def _label(v: np.ndarray, eps: float) -> str:
    if not np.isfinite(v).all():
        return "undefined"
    pos = bool(np.any(v > eps))
    neg = bool(np.any(v < -eps))
    return "mixed" if pos and neg else "positive" if pos else "negative" if neg else "neutral"


def _history_labels(x: np.ndarray, eps: float) -> dict:
    """Classify starts x histories x repeats with prespecified repeat diagnostics."""
    x = np.asarray(x, float)
    if x.ndim != 3 or x.shape[0] < 2 or x.shape[1] < 1 or x.shape[2] < 2:
        raise ValueError("need starts x histories x repeats")
    if not np.isfinite(eps) or eps < 0:
        raise ValueError("epsilon must be nonnegative")

    mean_labels = []
    first_labels = []
    last_labels = []
    repeat_labels = [[] for _ in range(x.shape[2])]
    any_repeat_disagreement = 0
    first_last_disagreement = 0

    split = x.shape[2] // 2
    for h in range(x.shape[1]):
        block = x[:, h, :]
        mean_label = _label(block.mean(axis=1), eps) if np.isfinite(block).all() else "undefined"
        mean_labels.append(mean_label)
        first = block[:, :split]
        last = block[:, split:]
        fl = _label(first.mean(axis=1), eps) if np.isfinite(first).all() else "undefined"
        ll = _label(last.mean(axis=1), eps) if np.isfinite(last).all() else "undefined"
        first_labels.append(fl)
        last_labels.append(ll)
        if fl != "undefined" and ll != "undefined" and fl != ll:
            first_last_disagreement += 1

        labels_h = []
        for d in range(x.shape[2]):
            col = block[:, d]
            lab = _label(col, eps)
            repeat_labels[d].append(lab)
            labels_h.append(lab)
        defined = {z for z in labels_h if z != "undefined"}
        if len(defined) > 1:
            any_repeat_disagreement += 1

    def counts(labels):
        return {k: labels.count(k) for k in ("mixed", "positive", "negative", "neutral", "undefined")}

    mc = counts(mean_labels)
    eligible = len(mean_labels) - mc["undefined"]
    frac = None if eligible == 0 else mc["mixed"] / eligible
    half = None if eligible == 0 else float(np.sqrt(np.log(40.0) / (2.0 * eligible)))
    return {
        "epsilon": float(eps),
        "mean8_counts": mc,
        "mean8_mixed_fraction": frac,
        "mean8_mixed_fraction_hoeffding95": None if frac is None else [max(0.0, frac-half), min(1.0, frac+half)],
        "repeat_specific_counts": [counts(z) for z in repeat_labels],
        "first4_counts": counts(first_labels),
        "last4_counts": counts(last_labels),
        "first4_last4_label_disagreements": first_last_disagreement,
        "any_repeat_label_disagreements": any_repeat_disagreement,
        "scope": "three starting populations within each independent history; descriptive demographic-repeat labels, not latent branching probabilities",
    }


def _bootstrap_mean(x: np.ndarray, resamples: np.ndarray) -> dict:
    """History-cluster bootstrap with shared resample indices across analyses."""
    x = np.asarray(x, float)
    history_means = np.nanmean(x, axis=(0, 2))
    finite = np.isfinite(history_means)
    if not finite.any():
        return {"status": "not_evaluable", "n_histories": int(len(history_means))}
    observed = float(np.nanmean(history_means))
    vals = []
    for ix in resamples:
        v = history_means[ix]
        vals.append(float(np.nanmean(v)) if np.isfinite(v).any() else np.nan)
    vals = np.asarray(vals, float)
    vals = vals[np.isfinite(vals)]
    if len(vals) == 0:
        return {"status": "not_evaluable", "n_histories": int(len(history_means))}
    lo, hi = np.quantile(vals, [0.025, 0.975])
    return {
        "status": "evaluated",
        "mean": observed,
        "interval95": [float(lo), float(hi)],
        "half_width": float((hi-lo)/2),
        "n_histories": int(len(history_means)),
        "n_finite_history_means": int(finite.sum()),
        "interpretation": "1999 bootstrap resamples of independent histories; same resample indices used for all starts/interventions/modes",
    }


def summarize(design: dict, campaign: Path) -> dict:
    campaign = Path(campaign)
    if not (campaign / "campaign_status.json").exists():
        raise FileNotFoundError("campaign_status.json")
    status = json.loads((campaign / "campaign_status.json").read_text())
    if not status.get("complete"):
        raise ValueError(f"campaign incomplete: {status}")
    if status["expected"] != design["cases"] or status["completed"] != design["cases"]:
        raise ValueError("case denominator differs from frozen design")
    if json.loads((campaign / "manifest.json").read_text()) != design:
        raise ValueError("campaign manifest differs from frozen design")
    manifest_hash = digest(design)
    if status["manifest_hash"] != manifest_hash:
        raise ValueError("manifest hash mismatch")

    starts = list(design["starts"])
    histories = list(design["history_seeds"])
    demos = list(design["demographic_seeds"])
    shape = (len(starts), len(histories), len(demos))
    arm_values = {
        (arm, mode): np.full(shape, np.nan)
        for arm in design["arms"] for mode in MODES
    }
    terminal_occupancy = {
        (arm, mode): np.zeros(shape, dtype=float)
        for arm in design["arms"] for mode in MODES
    }
    visitor_counts = {}
    receipt_root = sha256()

    for si, start in enumerate(starts):
        sid = int(round(start*10))
        for hi, hs in enumerate(histories):
            for di, ds in enumerate(demos):
                for arm in design["arms"]:
                    case_id = f"{arm}-s{sid}-h{hs}-d{ds}"
                    folder = campaign / case_id
                    receipt = json.loads((folder / "receipt.json").read_text())
                    raw = (folder / "arrays.npz").read_bytes()
                    if receipt.get("status") != "complete" or receipt["manifest_hash"] != manifest_hash:
                        raise ValueError(f"invalid receipt: {case_id}")
                    if sha256(raw).hexdigest() != receipt["arrays_sha256"]:
                        raise ValueError(f"array hash mismatch: {case_id}")
                    inp = json.loads((folder / "input.json").read_text())
                    if canonical(inp) != canonical({
                        **inp,
                    }):
                        raise AssertionError("canonical input failed self identity")
                    receipt_root.update(case_id.encode())
                    receipt_root.update(receipt["arrays_sha256"].encode())

                    with np.load(folder / "arrays.npz", allow_pickle=False) as a:
                        vc = np.asarray(a["visitor_count"])
                        vk = (arm, hi)
                        if vk in visitor_counts:
                            if not np.array_equal(visitor_counts[vk], vc):
                                raise ValueError(f"visitor history differs across starts/repeats: {arm} h{hs}")
                        else:
                            visitor_counts[vk] = vc.copy()
                        for mode, (trait_key, pop_key) in MODES.items():
                            tr = np.asarray(a[trait_key])
                            pop = np.asarray(a[pop_key])
                            valid = bool(pop[0] > 0 and pop[-1] > 0 and np.isfinite(tr[[0, -1], 1]).all())
                            terminal_occupancy[arm, mode][si, hi, di] = float(pop[-1] > 0)
                            if valid:
                                arm_values[arm, mode][si, hi, di] = float(tr[-1, 1] - tr[0, 1])

    rng = np.random.default_rng(927032)
    resamples = rng.integers(0, len(histories), size=(1999, len(histories)))

    reports = []
    tensors = {}
    for intervention, (near, far) in INTERVENTIONS.items():
        # response-blind richness matching must be exact year by year in stored histories
        if intervention == "richness_matched":
            for hi in range(len(histories)):
                if not np.array_equal(visitor_counts[(near, hi)], visitor_counts[(far, hi)]):
                    raise ValueError(f"richness matching failed in history index {hi}")

        for mode in MODES:
            tensor = arm_values[far, mode] - arm_values[near, mode]
            tensors[intervention, mode] = tensor
            report = {
                "intervention": intervention,
                "model": mode,
                "paired_far_minus_near": _bootstrap_mean(tensor, resamples),
                "mean_by_start": np.nanmean(tensor, axis=(1, 2)).tolist(),
                "finite_cells": int(np.isfinite(tensor).sum()),
                "total_cells": int(tensor.size),
                "classification": [_history_labels(tensor, eps) for eps in design["thresholds"]],
                "decomposition": decompose_crossed(
                    tensor,
                    {
                        "S": (np.ones(len(starts))/len(starts)).tolist(),
                        "C": (np.ones(len(histories))/len(histories)).tolist(),
                    },
                ),
                "near_terminal_occupancy": float(terminal_occupancy[near, mode].mean()),
                "far_terminal_occupancy": float(terminal_occupancy[far, mode].mean()),
            }
            reports.append(report)

    visitor_summary = {}
    for arm in design["arms"]:
        xs = [visitor_counts[(arm, hi)] for hi in range(len(histories))]
        visitor_summary[arm] = {
            "mean_count": float(np.mean([x.mean() for x in xs])),
            "empty_year_fraction": float(np.mean([np.mean(x == 0) for x in xs])),
            "mean_history_cv": float(np.mean([
                np.std(x) / np.mean(x) if np.mean(x) > 0 else np.nan for x in xs
            ])),
        }

    comparisons = {}
    for mode in MODES:
        natural = next(r for r in reports if r["intervention"] == "natural" and r["model"] == mode)
        matched = next(r for r in reports if r["intervention"] == "richness_matched" and r["model"] == mode)
        pooled = next(r for r in reports if r["intervention"] == "visitor_pooled" and r["model"] == mode)
        large = next(r for r in reports if r["intervention"] == "large_plant_capacity" and r["model"] == mode)
        comparisons[mode] = {
            "natural_vs_richness_matched_mixed_fraction": {
                str(eps): [
                    natural["classification"][i]["mean8_mixed_fraction"],
                    matched["classification"][i]["mean8_mixed_fraction"],
                ]
                for i, eps in enumerate(design["thresholds"])
            },
            "natural_vs_visitor_pooled_mixed_fraction": {
                str(eps): [
                    natural["classification"][i]["mean8_mixed_fraction"],
                    pooled["classification"][i]["mean8_mixed_fraction"],
                ]
                for i, eps in enumerate(design["thresholds"])
            },
            "natural_vs_large_plant_mixed_fraction": {
                str(eps): [
                    natural["classification"][i]["mean8_mixed_fraction"],
                    large["classification"][i]["mean8_mixed_fraction"],
                ]
                for i, eps in enumerate(design["thresholds"])
            },
        }

    return {
        "schema_version": "1.0",
        "status": "complete_prospective_bridge_summary",
        "design_manifest_hash": manifest_hash,
        "cases_verified": int(design["cases"]),
        "receipt_arrays_hash_root": receipt_root.hexdigest(),
        "endpoint": "paired far-minus-near terminal-minus-initial inherited investment change",
        "reports": reports,
        "comparisons": comparisons,
        "visitor_summary": visitor_summary,
        "question_status": {
            "dynamic_response_blind_realized_richness_matching": "evaluated",
            "finite_visitor_environment_vs_finite_plant_population": "evaluated_by_pooled_visitor_and_large_capacity_arms",
            "density_vs_individual_under_each_intervention": "evaluated",
        },
        "claim_boundaries": design["claim_exclusions"] + [
            "annual richness matching changes identity persistence as well as count",
            "pooled visitor histories average functional composition and nonlinear environment; they are not island count or lifespan",
            "large plant capacity changes finite demographic realization but is not a visitor-community control",
            "mixed fractions are descriptive history labels, not latent natural branching probabilities",
            "no result direction or rank is a success criterion",
        ],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--design", required=True)
    p.add_argument("--campaign", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    d = json.loads(Path(a.design).read_text())
    result = summarize(d, Path(a.campaign))
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(canonical(result))
    compact = {
        "status": result["status"],
        "cases_verified": result["cases_verified"],
        "reports": [
            {
                "intervention": r["intervention"],
                "model": r["model"],
                "mean": r["paired_far_minus_near"].get("mean"),
                "mixed": [q["mean8_counts"]["mixed"] for q in r["classification"]],
                "eligible": [sum(q["mean8_counts"][k] for k in ("mixed","positive","negative","neutral")) for q in r["classification"]],
                "repeat_disagreement": [q["any_repeat_label_disagreements"] for q in r["classification"]],
            }
            for r in result["reports"]
        ],
    }
    print(json.dumps(compact, indent=2))


if __name__ == "__main__":
    main()
