"""Summarize the frozen prospective Model 3 Chapter-2 bridge campaign."""
from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path

import numpy as np

from scripts.audit_model3_ch2_bridge import classify_histories
from scripts.model3_island.design import canonical, digest


PAIR_ARMS = {
    "natural": ("near", "far"),
    "richness_matched": ("matched_near", "matched_far"),
    "pooled_visitors": ("pool_near", "pool_far"),
    "large_plants": ("large_near", "large_far"),
}


def _change(arrays, *, density: bool) -> float:
    key = "density_traits" if density else "trait_mean"
    pop = "density_mass" if density else "population"
    x = arrays[key]
    if not (arrays[pop][-1] > 0 and np.isfinite(x[[0, -1], 1]).all()):
        return np.nan
    return float(x[-1, 1] - x[0, 1])


def _cluster_mean_ci(values: np.ndarray, *, seed: int = 927032) -> list[float] | None:
    """Bootstrap independent histories after averaging starts/repeats within history."""
    x = np.asarray(values, float)
    if x.ndim != 3:
        raise ValueError("expected starts x histories x repeats")
    by_history = np.array([
        np.nanmean(x[:, i, :]) if np.isfinite(x[:, i, :]).any() else np.nan
        for i in range(x.shape[1])
    ])
    finite = np.isfinite(by_history)
    y = by_history[finite]
    if len(y) < 2:
        return None
    rng = np.random.default_rng(seed)
    draws = rng.integers(0, len(y), (1999, len(y)))
    means = y[draws].mean(axis=1)
    return np.quantile(means, [0.025, 0.975]).tolist()


def _sign_agreement(a: np.ndarray, b: np.ndarray, eps: float = 0.0) -> float | None:
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    ok = np.isfinite(aa) & np.isfinite(bb) & (np.abs(aa) > eps) & (np.abs(bb) > eps)
    if not ok.any():
        return None
    return float(np.mean(np.sign(aa[ok]) == np.sign(bb[ok])))


def summarize(design: dict, results: Path) -> dict:
    if design.get("status") != "frozen":
        raise ValueError("frozen design required")
    expected = int(design["cases"])
    histories = [int(x) for x in design["history_seeds"]]
    starts = [float(x) for x in design["starts"]]
    demos = [int(x) for x in design["demographic_seeds"]]
    arms = list(design["arms"])
    hix = {x: i for i, x in enumerate(histories)}
    six = {x: i for i, x in enumerate(starts)}
    dix = {x: i for i, x in enumerate(demos)}

    shape = (len(starts), len(histories), len(demos))
    tensors = {
        (arm, mode): np.full(shape, np.nan)
        for arm in arms
        for mode in ("individual", "density")
    }
    occupied = {arm: np.zeros(shape, dtype=float) for arm in arms}
    visitor_counts: dict[tuple[str, int], np.ndarray] = {}
    receipts = 0

    for folder in sorted(p for p in results.iterdir() if p.is_dir()):
        inp = folder / "input.json"
        receipt = folder / "receipt.json"
        arrays = folder / "arrays.npz"
        if not (inp.exists() and receipt.exists() and arrays.exists()):
            continue
        case = json.loads(inp.read_text(encoding="utf-8"))
        rec = json.loads(receipt.read_text(encoding="utf-8"))
        if rec.get("status") != "complete" or rec.get("case_hash") != digest(case):
            raise ValueError(f"invalid receipt: {folder.name}")
        raw = arrays.read_bytes()
        if sha256(raw).hexdigest() != rec.get("arrays_sha256"):
            raise ValueError(f"array digest mismatch: {folder.name}")
        if canonical(case) != canonical(json.loads(inp.read_text(encoding="utf-8"))):
            raise ValueError(f"input identity mismatch: {folder.name}")

        arm = case["id"].split("-s", 1)[0]
        start = float(case["cell"]["founders"]["means"][1])
        hs = int(case["history_seed"])
        ds = int(case["demographic_seed"])
        idx = (six[start], hix[hs], dix[ds])
        with np.load(arrays, allow_pickle=False) as a:
            tensors[arm, "individual"][idx] = _change(a, density=False)
            tensors[arm, "density"][idx] = _change(a, density=True)
            occupied[arm][idx] = float(a["population"][-1] > 0)
            vk = (arm, hs)
            vc = a["visitor_count"].copy()
            if vk in visitor_counts and not np.array_equal(visitor_counts[vk], vc):
                raise ValueError(f"visitor history differs across plant replicates: {vk}")
            visitor_counts[vk] = vc
        receipts += 1

    if receipts != expected:
        raise ValueError(f"campaign incomplete: {receipts}/{expected}")

    reports = []
    raw_effects = {}
    for intervention, (near_arm, far_arm) in PAIR_ARMS.items():
        for mode in ("individual", "density"):
            effect = tensors[far_arm, mode] - tensors[near_arm, mode]
            raw_effects[intervention, mode] = effect
            reports.append({
                "intervention": intervention,
                "model": mode,
                "mean_far_minus_near": float(np.nanmean(effect)),
                "mean_by_start": np.nanmean(effect, axis=(1, 2)).tolist(),
                "cluster_bootstrap_95": _cluster_mean_ci(effect),
                "classifications": [classify_histories(effect, e) for e in design["thresholds"]],
                "pair_occupancy": float(np.mean(occupied[near_arm] * occupied[far_arm])),
            })

    matched_equal = True
    matched_empty_years = 0
    for hs in histories:
        a = visitor_counts["matched_near", hs]
        b = visitor_counts["matched_far", hs]
        matched_equal &= np.array_equal(a, b)
        matched_empty_years += int(np.sum((a == 0) & (b == 0)))

    visitor_summary = {}
    for intervention, (near_arm, far_arm) in PAIR_ARMS.items():
        near = np.concatenate([visitor_counts[near_arm, h] for h in histories])
        far = np.concatenate([visitor_counts[far_arm, h] for h in histories])
        visitor_summary[intervention] = {
            "mean_near_count": float(np.mean(near)),
            "mean_far_count": float(np.mean(far)),
            "mean_far_minus_near_count": float(np.mean(far - near)),
        }

    comparisons = {}
    for threshold in design["thresholds"]:
        key = str(threshold)
        comparison = {}
        for intervention in PAIR_ARMS:
            ind = next(
                r for r in reports
                if r["intervention"] == intervention and r["model"] == "individual"
            )
            den = next(
                r for r in reports
                if r["intervention"] == intervention and r["model"] == "density"
            )
            ii = next(x for x in ind["classifications"] if x["epsilon"] == float(threshold))
            dd = next(x for x in den["classifications"] if x["epsilon"] == float(threshold))
            comparison[intervention] = {
                "individual_mixed_fraction": ii["mixed_fraction"],
                "density_mixed_fraction": dd["mixed_fraction"],
                "individual_mixed_count": ii["counts"]["mixed"],
                "density_mixed_count": dd["counts"]["mixed"],
                "individual_repeat_disagreements": ii["repeat_disagreements"],
                "density_individual_sign_agreement": _sign_agreement(
                    raw_effects[intervention, "individual"],
                    raw_effects[intervention, "density"],
                    eps=float(threshold),
                ),
            }
        comparisons[key] = comparison

    return {
        "status": "prospective_bridge_summary_complete",
        "design_hash": digest(design),
        "cases_checked": receipts,
        "support": {
            "starts": starts,
            "histories": len(histories),
            "demographic_repeats": len(demos),
            "arms": arms,
        },
        "annual_richness_matching": {
            "near_far_counts_identical_all_years": bool(matched_equal),
            "empty_matched_years_across_histories": int(matched_empty_years),
            "interpretation": (
                "response-blind annual matching equalizes visitor count but also changes "
                "identity persistence; it is not a pure field richness intervention"
            ),
        },
        "visitor_counts": visitor_summary,
        "reports": reports,
        "comparisons_by_deadband": comparisons,
        "claim_boundary": [
            "prospective synthetic bridge, not natural prevalence",
            "grid5 is a frozen intermediate numerical design, not the final 24576-case campaign",
            "pooling visitor histories changes composition and environmental averaging, not lifespan",
            "large-plant arm changes plant-population finiteness while retaining the natural visitor history",
            "mixed labels are descriptive across three starts and finite demographic repeats",
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--design", required=True)
    p.add_argument("--results", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    design = json.loads(Path(a.design).read_text(encoding="utf-8"))
    report = summarize(design, Path(a.results))
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(canonical(report))
    print(json.dumps({
        "status": report["status"],
        "cases_checked": report["cases_checked"],
        "annual_richness_matching": report["annual_richness_matching"],
        "comparisons_by_deadband": report["comparisons_by_deadband"],
    }, indent=2))


if __name__ == "__main__":
    main()
