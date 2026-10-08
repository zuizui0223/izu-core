"""Independent, fail-closed Chapter 2 budget-window follow-up.

No new independent visitor history may be simulated by import, plan mode, PR CI,
or manual preflight. Production is only reachable with --execute-frozen-cohort.
Reuses the unchanged 2026-10-08 expression-order biology and raw-genotype audits.
The old 64-history readout is NEVER read to estimate the new confirmatory effect.
"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
import argparse
import hashlib
import json
import math

import numpy as np

from scripts.plan_chapter2_order_expression_identification import (
    SPEC as OLD_SPEC, Prehistory, load_protocol, prehistories,
)
from scripts.chapter2_order_prehistory_runner import (
    case_key, persist_one as persist_prehistory, source_hashes,
)
from scripts.chapter2_order_postshock_runner import (
    persist_one as persist_postshock,
)
from scripts.chapter2_order_confirmatory_readout import admit_all
from scripts.run_chapter2_assurance_generality import DEFAULT_DESIGN, load_design

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "data/design/chapter2_order_budget_window_independent_20261009.json"
PRIMARY = "eight_founders_capacity8"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_followup() -> tuple[dict, dict]:
    s = json.loads(SPEC.read_text(encoding="utf-8"))
    if s["status"] != "PROSPECTIVE_DESIGN_ONLY_NO_NEW_OUTCOMES":
        raise AssertionError("Post-outcome protocol is forbidden")
    if sha256(OLD_SPEC) != s["frozen_source"]["old_protocol_sha256"]:
        raise AssertionError("Biological source protocol has changed")
    if s["frozen_source"]["prior_result_status"] != "equivalent_within_predeclared_ROPE":
        raise AssertionError("Previous null/equivalence gate cannot be promoted")
    old = load_protocol()
    if (s["cohort"]["first_history"] != 38110901
        or s["cohort"]["last_history"] != 38110964
        or s["cohort"]["n_histories"] != 64
        or s["cohort"]["demographic_repeats"] != [38111901, 38111902]
        or s["cohort"]["allowed_arms"] != ["assurance_first", "investment_first"]
        or s["cohort"]["outcomes_exposed"] is not False
        or not (s["cohort"]["last_history"] < old["independent_histories"]["first"]
                or s["cohort"]["first_history"] > old["independent_histories"]["last"])):
        raise AssertionError("Unexpected, overlapping or exposed confirmatory visitor histories")
    e = s["estimand"]
    if (e["low_flank"] != 2 or e["window"] != [3, 4] or e["high_flank"] != 5
        or e["primary_min_abs_effect"] != 0.05
        or e["bootstrap"] != {"unit": "visitor_history", "n_draws": 9999,
                              "seed": 3811092026, "interval": "percentile95",
                              "sign": "two-sided"}
        or e["smooth_comparator"] != {
            "basis": "cubic polynomial in centered natural-log ovule budget",
            "alternative": "same cubic basis plus one prespecified budget-3-or-4 indicator",
            "validation": "8-fold holdout by visitor-history identity, all 7 budgets carried together",
            "loss": "per-history mean squared error of DID across 7 budgets",
            "ridge": 0.0001,
            "minimum_mean_improvement": 0.0001,
            "criterion": "95% history-bootstrap interval of held-out (smooth loss minus smooth-plus-window loss) entirely above zero and mean >=0.0001",
        }):
        raise AssertionError("Window/decision or smooth-null changed")
    if (s["future"]["budgets"] != [0.5, 1, 2, 3, 4, 5, 8]
        or s["future"]["primary_regime"] != PRIMARY
        or s["future"]["regimes"] != ["eight_founders_capacity8",
                                      "unbottlenecked_capacity48"]
        or s["future"]["visitor_environments"] != ["near", "far"]
        or s["declared_counts"] != {
            "prehistories": 2048, "postshock_branches_per_source": 28,
            "postshock_trajectories": 57344, "independent_histories": 64,
        }):
        raise AssertionError("Future grid not frozen")
    d = deepcopy(old)
    d["independent_histories"] = {
        "first": s["cohort"]["first_history"],
        "last": s["cohort"]["last_history"],
        "count": 64, "unit": "visitor_history", "new_not_reused": True,
    }
    d["nested_demographic_repeats"] = s["cohort"]["demographic_repeats"]
    d["path_perturbation"]["arms"] = {
        arm: old["path_perturbation"]["arms"][arm]
        for arm in s["cohort"]["allowed_arms"]
    }
    if (d["postshock"]["budgets"] != s["future"]["budgets"]
            or set(d["postshock"]["arms"]) != set(s["future"]["regimes"])
            or d["postshock"]["future_environments"] != s["future"]["visitor_environments"]):
        raise AssertionError("Legacy biological future changed")
    tasks = prehistories(d)
    if (len(tasks) != 2048 or len(set(tasks)) != 2048
            or len({t.visitor_history for t in tasks}) != 64):
        raise AssertionError("Incomplete independent source plan")
    return s, d


def history_shard(tasks: list[Prehistory], first: int, shard: int, count: int) -> list[Prehistory]:
    if count != 64 or not 0 <= shard < count:
        raise ValueError("Expected 64 distinct complete history shards")
    selected = [t for t in tasks if t.visitor_history - first == shard]
    if len(selected) != 32:
        raise AssertionError("Each shard must retain all 32 paired groups for one history")
    return selected


def plan(s: dict, d: dict) -> dict:
    return {
        "status": "design_only_no_new_biological_outcomes",
        "new_visitor_histories_sampled": 0,
        "independent_histories": 64,
        "prehistories": len(prehistories(d)),
        "postshock_cases": len(prehistories(d)) * 28,
        "arms": list(d["path_perturbation"]["arms"]),
        "budgets": d["postshock"]["budgets"],
        "new_protocol_sha256": sha256(SPEC),
        "underlying_biological_protocol_sha256": sha256(OLD_SPEC),
        "source_hashes": source_hashes(),
    }


def _run_cases(fn, tasks: list[Prehistory], workers: int, *extra):
    if not 1 <= workers <= 4:
        raise ValueError("Unsupported worker count")
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(fn, *extra, task) for task in tasks]
        names = sorted(f.result() for f in as_completed(futures))
    if names != sorted(case_key(task) for task in tasks):
        raise AssertionError("Case output count, identity or uniqueness mismatch")
    return names


def pre_case(out: Path, d: dict, biology: dict, hashes: dict, task: Prehistory) -> str:
    return persist_prehistory(out, task, d, biology, hashes)


def post_case(out: Path, pre: Path, d: dict, biology: dict, hashes: dict,
              task: Prehistory) -> str:
    return persist_postshock(out, pre, task, d, biology, hashes)


def _receipt(out: Path, stage: str, shard: int, names: list[str]) -> None:
    row = {
        "stage": stage, "shard": shard, "case_keys": names,
        "new_protocol_sha256": sha256(SPEC),
        "underlying_biological_protocol_sha256": sha256(OLD_SPEC),
        "source_hashes": source_hashes(),
        "status": "raw_unadjudicated",
    }
    (out / f"window_{stage}_shard_{shard:02}.json").write_text(
        json.dumps(row, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def audit_shards(folder: Path, stage: str, tasks: list[Prehistory], first: int) -> None:
    expected = set()
    for shard in range(64):
        path = folder / f"window_{stage}_shard_{shard:02}.json"
        row = json.loads(path.read_text(encoding="utf-8"))
        cohort = history_shard(tasks, first, shard, 64)
        required = sorted(case_key(t) for t in cohort)
        if (row["stage"] != stage or row["shard"] != shard
                or row["status"] != "raw_unadjudicated"
                or row["case_keys"] != required
                or row["new_protocol_sha256"] != sha256(SPEC)
                or row["underlying_biological_protocol_sha256"] != sha256(OLD_SPEC)
                or row["source_hashes"] != source_hashes()):
            raise AssertionError("Missing/incorrect complete shard receipt " + str(shard))
        expected.update(required)
    if len(expected) != 2048:
        raise AssertionError("Incomplete 2048-case coverage")


def history_window_residual(values: np.ndarray, budgets: list[float]) -> np.ndarray:
    """64-by-7 history-level DID -> 64 independent fixed-window residuals."""
    a = np.asarray(values, dtype=float)
    if a.shape != (64, 7) or budgets != [0.5, 1, 2, 3, 4, 5, 8]:
        raise ValueError("Wrong independent-history, budget or shape denominator")
    if not np.isfinite(a).all():
        raise ValueError("Non-finite history DID")
    w = lambda b: math.log(b / 2) / math.log(5 / 2)
    linear = lambda b: a[:, 2] + (a[:, 5] - a[:, 2]) * w(b)
    return 0.5 * ((a[:, 3] - linear(3)) + (a[:, 4] - linear(4)))


def smooth_cv_losses(values: np.ndarray, budgets: list[float],
                     ridge: float = 0.0001) -> np.ndarray:
    """Out-of-history prediction only; [smooth MSE - window MSE] per history."""
    v = np.asarray(values, dtype=float)
    if v.shape != (64, 7) or budgets != [0.5, 1, 2, 3, 4, 5, 8]:
        raise ValueError("Incorrect smooth-model prediction grid")
    x = np.log(np.array(budgets, dtype=float) / 3.0)
    smooth = np.column_stack([np.ones(7), x, x*x, x*x*x])
    enhanced = np.column_stack([smooth, [int(b in (3, 4)) for b in budgets]])
    def predict(design, train_ids):
        y = v[train_ids].reshape(-1)
        X = np.tile(design, (len(train_ids), 1))
        penalty = np.eye(design.shape[1]) * ridge
        penalty[0, 0] = 0.0
        beta = np.linalg.solve(X.T @ X + penalty, X.T @ y)
        return design @ beta
    improvement = np.empty(64)
    for fold in range(8):
        test = np.arange(fold, 64, 8)
        train = np.array([i for i in range(64) if i % 8 != fold])
        p0 = predict(smooth, train)
        p1 = predict(enhanced, train)
        improvement[test] = ((v[test] - p0)**2).mean(axis=1) - (
            (v[test] - p1)**2).mean(axis=1)
    return improvement


def inference(values: np.ndarray, budgets: list[float], seed=3811092026) -> dict:
    """Two-sided fixed gate; the 64 visitor histories, not forks, are resampled."""
    a = history_window_residual(values, budgets)
    gain = smooth_cv_losses(values, budgets)
    rng = np.random.default_rng(seed)
    draw = rng.integers(0, 64, size=(9999, 64))
    mean, gmean = float(a.mean()), float(gain.mean())
    ci = np.percentile(a[draw].mean(axis=1), [2.5, 97.5]).tolist()
    gci = np.percentile(gain[draw].mean(axis=1), [2.5, 97.5]).tolist()
    local = (abs(mean) >= 0.05 and (ci[0] > 0 or ci[1] < 0))
    smooth = (gmean >= 0.0001 and gci[0] > 0)
    if local and smooth:
        conclusion = "fixed_window_confirmed_beyond_specified_cubic_smooth"
    elif ci[0] > -0.05 and ci[1] < 0.05:
        conclusion = "window_residual_practically_equivalent"
    else:
        conclusion = "inconclusive_or_not_distinguished_from_smooth"
    return {
        "window_residual_mean": mean, "history_bootstrap95": ci,
        "smooth_cv_mse_improvement_mean": gmean,
        "smooth_cv_history_bootstrap95": gci,
        "window_gate_passed": bool(local), "smooth_gate_passed": bool(smooth),
        "predeclared_joint_decision": conclusion,
        "histories": 64,
        "criterion": "Two-sided 64-visitor-history bootstrap + heldout cubic smooth comparator",
    }


def evaluate_all(d: dict, post: dict) -> dict:
    histories = range(38110901, 38110965)
    settings = d["reproductive_settings"]
    budgets = d["postshock"]["budgets"]
    arms = ["assurance_first", "investment_first"]
    regimes = d["postshock"]["arms"]
    all_output = {}
    for regime in regimes:
        # Independent history x mating rule x pre environment x schedule x budget.
        cells = np.empty((64, 4, 2, 2, 7))
        for hi, h in enumerate(histories):
            for si, setting in enumerate(settings):
                for ei, env in enumerate(["near", "far"]):
                    for ai, arm in enumerate(arms):
                        for bi, b in enumerate(budgets):
                            cells[hi, si, ei, ai, bi] = np.mean([
                                post[Prehistory(setting, env, arm, h, rep)][
                                    (regime, float(b), fv)]["occupied"]
                                for rep in d["nested_demographic_repeats"]
                                for fv in d["postshock"]["future_environments"]
                            ])
        # Matched far-minus-near A-first-minus-I-first; settings average inside history.
        did = ((cells[:, :, 1, 0, :] - cells[:, :, 1, 1, :])
               - (cells[:, :, 0, 0, :] - cells[:, :, 0, 1, :])).mean(axis=1)
        by_budget = did.mean(axis=0)
        window = inference(did, budgets)
        all_output[regime] = {
            "history_average_DID_by_budget": {str(b): float(by_budget[bi])
                                             for bi, b in enumerate(budgets)},
            "fixed_window_diagnostic": window,
            "by_setting": {
                setting: {
                    "did_by_budget": {
                        str(b): float(((cells[:, si, 1, 0, bi]
                                        - cells[:, si, 1, 1, bi])
                                       - (cells[:, si, 0, 0, bi]
                                          - cells[:, si, 0, 1, bi])).mean())
                        for bi, b in enumerate(budgets)
                    }
                } for si, setting in enumerate(settings)
            },
            "absolute_occupancy_by_pre_environment_and_arm": {
                env: {
                    arm: {str(b): float(cells[:, :, ei, ai, bi].mean())
                          for bi, b in enumerate(budgets)}
                    for ai, arm in enumerate(arms)
                } for ei, env in enumerate(["near", "far"])
            },
        }
    return {
        "status": "all_2048_new_sources_57344_futures_admitted",
        "independent_visitor_histories": 64,
        "prehistories": 2048, "future_branches": 57344,
        "new_protocol_sha256": sha256(SPEC),
        "underlying_biological_protocol_sha256": sha256(OLD_SPEC),
        "source_hashes": source_hashes(),
        "primary": all_output[PRIMARY]["fixed_window_diagnostic"],
        "by_regime": all_output,
        "limits": [
            "Only assigned phenotype-expression sequence is randomized; naturally realized genetic order is post-treatment.",
            "The fixed window was selected from the earlier 64 exposed histories; only this new independent cohort confirms it.",
            "A cubic log-budget baseline is a prespecified finite competitor, not every possible smooth resource mechanism.",
            "Synthetic persistence stress, not natural island viability or ecological extinction risk.",
            "The prior pooled practical equivalence and failed independent16 mutation-priority claim remain unchanged.",
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mode", choices=["plan", "pre", "post", "readout"], required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--prehistory", type=Path)
    p.add_argument("--postshock", type=Path)
    p.add_argument("--shard", type=int)
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--execute-frozen-cohort", action="store_true")
    args = p.parse_args()
    spec, d = load_followup()
    tasks = prehistories(d)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.mode == "plan":
        args.out.write_text(json.dumps(plan(spec, d), indent=2) + "\n",
                            encoding="utf-8")
        print("plan_only: 0 new histories simulated")
        return
    if not args.execute_frozen_cohort:
        raise PermissionError("Fresh independent histories require explicit production approval")
    if args.mode in ("pre", "post"):
        if args.shard is None:
            raise ValueError("Explicit history shard required")
        group = history_shard(tasks, spec["cohort"]["first_history"],
                              args.shard, 64)
        args.out.mkdir(parents=True, exist_ok=True)
        biology = load_design(DEFAULT_DESIGN)
        hashes = source_hashes()
        if args.mode == "pre":
            keys = _run_cases(pre_case, group, args.workers,
                              args.out, d, biology, hashes)
        else:
            if args.prehistory is None:
                raise ValueError("Postshock needs existing t400 source state")
            keys = _run_cases(post_case, group, args.workers,
                              args.out, args.prehistory, d, biology, hashes)
        _receipt(args.out, args.mode, args.shard, keys)
        print(json.dumps({"mode": args.mode, "shard": args.shard,
                          "sources": len(keys),
                          "futures": len(keys)*28 if args.mode == "post" else 0}))
        return
    if args.prehistory is None or args.postshock is None:
        raise ValueError("Full readout needs both raw source and future archives")
    audit_shards(args.prehistory, "pre", tasks, spec["cohort"]["first_history"])
    audit_shards(args.postshock, "post", tasks, spec["cohort"]["first_history"])
    before, after = admit_all(args.prehistory, args.postshock, d,
                              tasks=tasks, require_full=False)
    if (len(before) != 2048 or len(after) != 2048 or
        sum(len(x) for x in after.values()) != 57344):
        raise AssertionError("Whole new cohort is not admissible")
    result = evaluate_all(d, after)
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n",
                        encoding="utf-8")
    print(json.dumps({"complete": True, "decision":
                      result["primary"]["predeclared_joint_decision"]}))


if __name__ == "__main__":
    main()
