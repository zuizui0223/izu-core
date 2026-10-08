"""Apply both frozen gates only after ALL unified prehistory/postshock cases exist.

The 64 VISITOR HISTORIES are the independent bootstrap units; all repeats,
four settings, historical arms, shocks and 7 budgets are paired within history.
No favourite stress levels or survivor-only samples may be selected.
"""
from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np

from scripts.plan_chapter2_unified_payoff_evolution_persistence import (
    DESIGN, load_design, prehistory_tasks, log_trapezoid_weights
)
from scripts.run_chapter2_unified_payoff_prehistories import (
    key, source_hashes,
)


def load_and_audit(pre_dir: Path, post_dir: Path, d: dict):
    expected_hash = hashlib.sha256(DESIGN.read_bytes()).hexdigest()
    hashes = source_hashes()
    pres, post = {}, {}
    expected_grid = {
        (r["id"], future, float(budget))
        for r in d["postshock"]["regimes"]
        for future in d["postshock"]["visitor_environments"]
        for budget in d["postshock"]["budgets"]
    }
    for task in prehistory_tasks(d):
        k = key(task)
        file_pre = pre_dir / f"{k}.json"
        file_post = post_dir / f"{k}.json"
        state_file = pre_dir / f"{k}.npz"
        post_receipt = post_dir / f"{k}.sha256"
        if (not file_pre.is_file() or not file_post.is_file()
                or not state_file.is_file() or not post_receipt.is_file()):
            raise FileNotFoundError("missing matched cohort, genotype or post receipt " + k)
        if (hashlib.sha256(file_post.read_bytes()).hexdigest()
                != post_receipt.read_text().strip()):
            raise AssertionError("postshock 42-cell raw receipt changed " + k)
        old = json.loads(file_pre.read_text(encoding="utf-8"))
        if hashlib.sha256(state_file.read_bytes()).hexdigest() != old["state_sha256"]:
            raise AssertionError("prehistory full genotype hash changed after future forks " + k)
        row = json.loads(file_post.read_text(encoding="utf-8"))
        if (old["task"] != asdict(task) or row["task"] != asdict(task)
            or old["source_hashes"] != hashes or row["source_hashes"] != hashes
            or old["design_sha256"] != expected_hash
            or row["design_sha256"] != expected_hash
            or row["prehistory_state_sha256"] != old["state_sha256"]
            or old["status"] != "complete_prehistory_unadjudicated"
            or row["status"] != "complete_postshock_raw_not_adjudicated"):
            raise AssertionError("design, state or source mismatch: " + k)
        snaps = {r["t"]: r for r in old["snapshots"]}
        if set(snaps) != set(d["prehistory"]["occupancy_census_times"]):
            raise AssertionError("missing investment checkpoint " + k)
        if len(row["postshock"]) != 42:
            raise AssertionError("incomplete postshock group " + k)
        observed = {(r["regime"], r["future_environment"], r["ovule_budget"])
                    for r in row["postshock"]}
        if observed != expected_grid:
            raise AssertionError("missing/repeated postshock cell " + k)
        for c in row["postshock"]:
            if (c["occupied"] != int(c["end_population"] > 0)
                    or c["future_assurance_mode"] != "evolving"
                    or c["first_extinction"] is not None and
                       c["occupied"] != 0):
                raise AssertionError("bad postshock occupancy or treatment " + k)
        pres[task] = old
        post[task] = {(c["regime"], c["future_environment"], c["ovule_budget"]): c
                      for c in row["postshock"]}
    return pres, post


def bootstrap_summary(matrix, index):
    """matrix shape histories × setting; use shared history resampling."""
    values = np.asarray(matrix, dtype=float)
    if values.ndim != 2:
        raise ValueError("history × setting matrix required")
    n_history, n_setting = values.shape
    if n_history != index.shape[1]:
        raise ValueError("wrong ecological sample count")
    estimates = []
    for i in range(n_setting):
        vector = values[:, i]
        eligible = np.isfinite(vector)
        n = int(eligible.sum())
        if n < 60:
            estimates.append({
                "mean": float(np.mean(vector[eligible])) if n else None,
                "bootstrap95": None, "n_complete_histories": n,
                "conditional_on_endpoint_survival": True,
            })
        else:
            eligible_values = vector[eligible]
            if n == n_history:
                sampled = eligible_values[index].mean(axis=1)
            else:
                # The frozen gate admits >=60/64 complete histories. When
                # fewer than 64 have trait endpoints, bootstrap ONLY the
                # observed eligible *visitor histories*, never 8 nested
                # demographic repeats or nonexistent post-extinction traits.
                local = np.random.default_rng(3611082026 + i)
                indices = local.integers(0, n, size=(len(index), n))
                sampled = eligible_values[indices].mean(axis=1)
            estimates.append({
                "mean": float(eligible_values.mean()),
                "bootstrap95": [float(x) for x in np.percentile(
                    sampled, [2.5, 97.5])],
                "n_complete_histories": n,
                "conditional_on_endpoint_survival": n != n_history,
            })
    return estimates


def evaluate(d, pre, post):
    hcfg = d["histories"]
    histories = list(range(hcfg["first"], hcfg["last"] + 1))
    repeats = d["nested_demographic_repeat_seeds"]
    settings = d["reproductive_settings"]
    from scripts.plan_chapter2_unified_payoff_evolution_persistence import Prehistory
    rng = np.random.default_rng(d["inference"]["bootstrap"]["seed"])
    samples = rng.integers(0, len(histories), size=(
        d["inference"]["bootstrap"]["draws"], len(histories)))
    stage1_fixed = []
    stage1_atten = []
    eligible = []
    for h in histories:
        fixed_by_setting, atten_by_setting, counts = [], [], []
        for setting in settings:
            cells = {}
            for mode in d["evolutionary_access_modes"]:
                for env in d["pre_visitor_environments"]:
                    readings = []
                    for rep in repeats:
                        t = Prehistory(setting, mode, env, h, rep)
                        endpoint = pre[t]["snapshots"][-1]
                        if endpoint["n"] > 0:
                            readings.append(float(endpoint["means"][1]))
                    cells[mode, env] = readings
            all_eight = all(len(cells[mode, env]) == len(repeats)
                            for mode in d["evolutionary_access_modes"]
                            for env in d["pre_visitor_environments"])
            counts.append(all_eight)
            if all_eight:
                fixed = np.mean(cells["fixed", "far"]) - np.mean(cells["fixed", "near"])
                evolve = np.mean(cells["evolving", "far"]) - np.mean(cells["evolving", "near"])
                fixed_by_setting.append(float(fixed))
                atten_by_setting.append(float(evolve - fixed))
            else:
                fixed_by_setting.append(float("nan"))
                atten_by_setting.append(float("nan"))
        stage1_fixed.append(fixed_by_setting)
        stage1_atten.append(atten_by_setting)
        eligible.append(counts)
    stage1_fixed = np.asarray(stage1_fixed)
    stage1_atten = np.asarray(stage1_atten)
    fixed_result = bootstrap_summary(stage1_fixed, samples)
    atten_result = bootstrap_summary(stage1_atten, samples)
    stage1 = []
    for i, setting in enumerate(settings):
        fixed, atten = fixed_result[i], atten_result[i]
        allowed = (fixed["n_complete_histories"] >= 60 and
                   atten["n_complete_histories"] >= 60)
        # A 60–63 history bootstrap is conditional on complete survivor
        # histories and explicitly reports that changed denominator.
        accepted = bool(
            allowed and fixed["bootstrap95"] and atten["bootstrap95"]
            and fixed["mean"] < 0 and fixed["bootstrap95"][1] < 0
            and atten["mean"] > 0 and atten["bootstrap95"][0] > 0
        )
        stage1.append({
            "setting": setting, "fixed_far_minus_near": fixed,
            "attenuation": atten, "admissible": allowed,
            "passes_frozen_rule": accepted,
        })

    weights = log_trapezoid_weights(d["postshock"]["budgets"])
    stage2 = []
    for regime in [x["id"] for x in d["postshock"]["regimes"]]:
        matrix = []
        for h in histories:
            setting_effects = []
            for setting in settings:
                arms = {}
                for mode in ("fixed", "evolving"):
                    for env in ("near", "far"):
                        by_repeat = []
                        for rep in repeats:
                            t = Prehistory(setting, mode, env, h, rep)
                            future_values = []
                            for postenv in d["postshock"]["visitor_environments"]:
                                val = sum(weights[budget] * post[t][
                                    (regime, postenv, budget)
                                ]["occupied"] for budget in weights)
                                future_values.append(val)
                            by_repeat.append(float(np.mean(future_values)))
                        arms[mode, env] = float(np.mean(by_repeat))
                setting_effects.append(
                    (arms["evolving", "far"] - arms["evolving", "near"])
                    - (arms["fixed", "far"] - arms["fixed", "near"])
                )
            matrix.append(setting_effects)
        matrix = np.asarray(matrix)
        setting_result = bootstrap_summary(matrix, samples)
        pooled = matrix.mean(axis=1)
        pooled_boot = pooled[samples].mean(axis=1)
        overall = {
            "mean": float(pooled.mean()),
            "bootstrap95": [
                float(x) for x in np.percentile(pooled_boot, [2.5, 97.5])
            ],
        }
        overall["passes_frozen_rule"] = bool(
            overall["mean"] > 0 and overall["bootstrap95"][0] > 0)
        stage2.append({
            "regime": regime, "all_setting_equal_weight_pooled": overall,
            "per_setting": [
                {"setting": setting, **setting_result[i]}
                for i, setting in enumerate(settings)
            ],
        })
    s2main = next(s for s in stage2 if s["regime"] == d[
        "causal_estimates"]["primary_stage2_persistence"]["primary_regime"])
    stage1_ok = all(x["passes_frozen_rule"] for x in stage1)
    return {
        "status": "all_cases_admitted_joint_gate_evaluated",
        "independent_visitor_histories": 64,
        "nested_demographic_repeats": 2,
        "prehistories": len(pre),
        "postshock_trajectories": 42 * len(post),
        "postshock_budget_weights": {str(k): v for k, v in weights.items()},
        "stage1": {
            "all_four_pass": stage1_ok,
            "setting_results": stage1,
        },
        "stage2": {
            "primary_regime": s2main["regime"],
            "primary_gate": s2main["all_setting_equal_weight_pooled"],
            "all_regimes": stage2,
        },
        "joint_pass": bool(
            stage1_ok and s2main["all_setting_equal_weight_pooled"]["passes_frozen_rule"]
        ),
        "boundaries": [
            "The 400-update inherited evolution contrasts and 80-update common-future persistence use the SAME new cohort.",
            "Only past A-evolution access differs; future A-evolution ability is identical.",
            "Log-budget integration is a synthetic weighted risk window, not the natural distribution of shocks.",
            "PDE equivalence is not required or claimed.",
            "No real island, natural trait, or temporal-order phenotype intervention is inferred.",
        ],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prehistory", type=Path, required=True)
    p.add_argument("--postshock", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    d = load_design()
    before, after = load_and_audit(args.prehistory, args.postshock, d)
    result = evaluate(d, before, after)
    result["design_sha256"] = hashlib.sha256(DESIGN.read_bytes()).hexdigest()
    result["source_hashes"] = source_hashes()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({
        "stage1_all_four_pass": result["stage1"]["all_four_pass"],
        "stage2_primary_pass": result["stage2"]["primary_gate"]["passes_frozen_rule"],
        "joint_pass": result["joint_pass"],
    }))


if __name__ == "__main__":
    main()
