"""Validate and enumerate the *one-cohort* Chapter 2 ecological process protocol.

This module is a design compiler, not the biological simulator. Running it
generates no evolutionary or extinction results and does not peek at seeds.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path
import argparse
import csv
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_unified_payoff_evolution_persistence_20261008.json"


@dataclass(frozen=True)
class Prehistory:
    setting: str
    mode: str
    environment: str
    history: int
    repeat: int


@dataclass(frozen=True)
class Postshock:
    prehistory: Prehistory
    regime: str
    future_environment: str
    budget: float


def load_design(path: Path = DESIGN) -> dict:
    raw = Path(path).read_bytes()
    d = json.loads(raw)
    if d["status"] != "prospective_new_cohort_protocol_design_only_not_executed":
        raise ValueError("unanticipated protocol status")
    if d["histories"] != {
        "first": 36110801, "last": 36110864, "count": 64,
        "independent_unit": "visitor history",
    }:
        raise ValueError("history sampling contract changed")
    if d["nested_demographic_repeat_seeds"] != [36111801, 36111802]:
        raise ValueError("demographic replicate seeds changed")
    if set(d["reproductive_settings"]) != {
        "delayed_control", "prior_selfing", "pollen_discount", "assurance_cost"
    } or d["evolutionary_access_modes"] != ["fixed", "evolving"]:
        raise ValueError("unanticipated biology")
    if d["prehistory"]["updates"] != 400 or d["postshock"]["updates"] != 80:
        raise ValueError("unexpected time horizon")
    if d["postshock"]["budgets"] != [0.5, 1, 2, 3, 4, 5, 8]:
        raise ValueError("budgets were changed")
    if len(d["postshock"]["regimes"]) != 3:
        raise ValueError("the full shock counterfactual grid is required")
    if {r["id"] for r in d["postshock"]["regimes"]} != {
        "fecundity_only", "founder_bottleneck", "bottleneck_small_capacity",
    }:
        raise ValueError("shock regimen omitted")
    source = ROOT / d["source_biology"]["baseline_result"]
    if not source.is_file():
        raise FileNotFoundError("verified 4-setting source result missing")
    prior = json.loads(source.read_text(encoding="utf-8"))
    if (prior["adjudication"]["status"] != "all_four_confirmed"
            or prior["declared_cases"] != 8448):
        raise AssertionError("wrong source model confirmation")
    if prior["workflow_provenance"]["artifact_sha256"] != (
        d["source_biology"]["confirmed_artifact_sha256"]
    ):
        raise AssertionError("different historic biology/provenance artifact")
    if d["source_biology"]["source_commit_at_design"] != (
        "94c051850a43b89047e78e653edae25b043624ab"
    ):
        raise AssertionError("source-commit reference changed; re-audit required")
    if not d["postshock"]["no_plant_immigration"]:
        raise ValueError("cannot mix migration into declared counterfactual")
    if d["estimated_run_size"]["suggested_worker_shards"] != 64:
        raise ValueError("unexpected shard plan")
    return d


def log_trapezoid_weights(budgets: list[float]) -> dict[float, float]:
    if len(budgets) < 2 or any(b <= 0 for b in budgets):
        raise ValueError("budget coordinate invalid")
    logs = [math.log(b) for b in budgets]
    if any(right <= left for left, right in zip(logs, logs[1:])):
        raise ValueError("budgets must be strictly ascending")
    weights = []
    for i in range(len(logs)):
        left = (logs[i] - logs[i - 1]) / 2 if i else 0
        right = (logs[i + 1] - logs[i]) / 2 if i + 1 < len(logs) else 0
        weights.append((left + right) / (logs[-1] - logs[0]))
    if not math.isclose(sum(weights), 1, abs_tol=1e-12):
        raise ArithmeticError("quadrature weights do not sum to one")
    return dict(zip(budgets, weights))


def prehistory_tasks(d: dict) -> list[Prehistory]:
    h = d["histories"]
    tasks = [
        Prehistory(setting, mode, env, history, repeat)
        for setting, mode, env, history, repeat in product(
            d["reproductive_settings"], d["evolutionary_access_modes"],
            d["pre_visitor_environments"],
            range(h["first"], h["last"] + 1),
            d["nested_demographic_repeat_seeds"],
        )
    ]
    if len(tasks) != d["estimated_run_size"]["prehistory_groups"]:
        raise AssertionError("prehistory group count differs from frozen plan")
    if len(set(tasks)) != len(tasks):
        raise AssertionError("prehistory identity collision")
    return tasks


def shock_tasks(d: dict, pres: list[Prehistory] | None = None):
    pres = prehistory_tasks(d) if pres is None else pres
    regimes = [r["id"] for r in d["postshock"]["regimes"]]
    for pre, regime, environment, budget in product(
        pres, regimes, d["postshock"]["visitor_environments"],
        d["postshock"]["budgets"]
    ):
        yield Postshock(pre, regime, environment, float(budget))


def validate_counts(d: dict) -> dict:
    pres = prehistory_tasks(d)
    per = (len(d["postshock"]["regimes"]) *
           len(d["postshock"]["budgets"]) *
           len(d["postshock"]["visitor_environments"]))
    expected = len(pres) * per
    declared = d["estimated_run_size"]
    if declared["postshock_cases_per_prehistory"] != per or (
        declared["postshock_trajectories"] != expected
    ):
        raise AssertionError("full postshock case count inconsistent")
    actual = sum(1 for _ in shock_tasks(d, pres))
    if actual != expected:
        raise AssertionError("generator emitted wrong number of shock tasks")
    if len({t.history for t in pres}) != declared["total_independent_visitor_histories"]:
        raise AssertionError("history replication incorrect")
    if len({t.repeat for t in pres}) != declared["demographic_repeats_within_history"]:
        raise AssertionError("nested demographic replication incorrect")
    return {
        "protocol_status": d["status"],
        "independent_visitor_histories": len({t.history for t in pres}),
        "nested_demographic_repeats": len({t.repeat for t in pres}),
        "prehistories": len(pres),
        "postshock_branches_per_prehistory": per,
        "postshock_trajectories": actual,
        "budget_weights": log_trapezoid_weights(d["postshock"]["budgets"]),
        "sha256": hashlib.sha256(DESIGN.read_bytes()).hexdigest()
    }


def write_manifest(path: Path, d: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        out = csv.writer(handle)
        out.writerow([
            "setting", "assurance_mode", "pre_environment", "visitor_history_seed",
            "nested_demographic_repeat", "postshock_regime",
            "future_visitor_environment", "ovule_budget",
        ])
        for t in shock_tasks(d):
            p = t.prehistory
            out.writerow([
                p.setting, p.mode, p.environment, p.history, p.repeat,
                t.regime, t.future_environment, t.budget,
            ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    d = load_design()
    counts = validate_counts(d)
    if args.manifest:
        write_manifest(args.manifest, d)
        counts["manifest_sha256"] = hashlib.sha256(args.manifest.read_bytes()).hexdigest()
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(counts, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(counts, sort_keys=True))


if __name__ == "__main__":
    main()
