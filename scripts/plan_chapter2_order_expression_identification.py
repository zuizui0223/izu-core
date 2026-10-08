"""Non-peeking compiler for the prospective ecological expression-order protocol.

This file enumerates planned experimental units. It does NOT simulate visitor
histories, select plants, evaluate biological payoffs or create scientific data.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path
import argparse
import csv
import json
import math

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "data/design/chapter2_order_expression_identification_20261008.json"


@dataclass(frozen=True)
class Prehistory:
    setting: str
    environment: str
    expression_order: str
    visitor_history: int
    demographic_repeat: int


@dataclass(frozen=True)
class Future:
    source: Prehistory
    regime: str
    budget: float
    future_visitor: str


def load_protocol(path: Path = SPEC) -> dict:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_protocol(d)
    return d


def validate_protocol(d: dict) -> None:
    if d["status"] != "PROSPECTIVE_DESIGN_ONLY_NO_BIOLOGICAL_OUTCOMES":
        raise ValueError("This is not the frozen pre-outcome protocol")
    source = ROOT / d["source"]["frozen_result"]
    if not source.is_file():
        raise FileNotFoundError("Cannot verify the already confirmed biology")
    established = json.loads(source.read_text(encoding="utf-8"))
    if (established["adjudication"]["status"] != "all_four_confirmed"
            or established["declared_cases"] != 8448):
        raise AssertionError("Wrong source biology confirmation")
    if "FAILED" not in d["source"]["earlier_failure"]:
        raise AssertionError("Historical failed priority test must remain failed")
    if d["reproductive_settings"] != [
        "delayed_control", "prior_selfing", "pollen_discount", "assurance_cost"
    ] or d["environmental_settings"] != ["near", "far"]:
        raise ValueError("Biological blocks changed")
    h = d["independent_histories"]
    if h != {
        "first": 37110801, "last": 37110864, "count": 64,
        "unit": "visitor_history", "new_not_reused": True,
    } or d["nested_demographic_repeats"] != [37111801, 37111802]:
        raise ValueError("Unexpected or reused visitor-history cohort")
    if (d["prehistory"]["updates"] != 400
            or d["prehistory"]["release_start"] != 300
            or d["prehistory"]["genetic_mutation_probability"] != 0.01
            or d["prehistory"]["snapshot_times"] != [0, 100, 200, 300, 400]):
        raise ValueError("Evolutionary observation horizon changed")
    if not d["prehistory"]["no_immigrant_seed"]:
        raise ValueError("Undeclared plant immigration")
    treatment = d["path_perturbation"]
    if (treatment["type"] !=
            "transient phenotype-only logit offset applied inside reproductive payoff function"
            or treatment["size_logit"] != 0.45
            or set(treatment["arms"]) != {
                "assurance_first", "investment_first", "synchronous_time_control"
            }):
        raise ValueError("Treatment assignment changed")
    expected_phases = {
        "assurance_first": [(0.45, 0.0), (0.45, -0.45),
                            (0.0, -0.45), (0.0, 0.0)],
        "investment_first": [(0.0, -0.45), (0.45, -0.45),
                             (0.45, 0.0), (0.0, 0.0)],
        "synchronous_time_control": [(0.45, -0.45), (0.0, 0.0),
                                     (0.45, -0.45), (0.0, 0.0)],
    }
    for arm, expected in expected_phases.items():
        phases = treatment["arms"][arm]
        if len(phases) != 4:
            raise ValueError("Missing exposure phase")
        for index, (phase, (a, i)) in enumerate(zip(phases, expected)):
            if (phase["from"] != index * 100
                    or phase["to"] != (index + 1) * 100
                    or phase["A"] != a or phase["I"] != i):
                raise ValueError("Focal timing changed: " + arm)
        for trait in ("A", "I"):
            exposed = sum(
                phase["to"] - phase["from"] for phase in phases if phase[trait]
            )
            if exposed != 200:
                raise AssertionError("Unequal focal exposure dose")
    overlap_counts = {
        name: sum(
            step["to"] - step["from"]
            for step in d["path_perturbation"]["arms"][name]
            if step["A"] != 0 and step["I"] != 0
        )
        for name in expected_phases
    }
    if (overlap_counts != {
        "assurance_first": 100, "investment_first": 100,
        "synchronous_time_control": 200,
    } or treatment["joint_exposure_update_counts"] != overlap_counts):
        raise AssertionError("Co-expression window changed")
    if "NOT a matched overlap negative control" not in treatment["control_caveat"]:
        raise AssertionError("Synchronous comparator scope expanded")
    future = d["postshock"]
    if (future["updates"] != 80 or future["arms"] !=
        ["unbottlenecked_capacity48", "eight_founders_capacity8"]
        or future["budgets"] != [0.5, 1, 2, 3, 4, 5, 8]
        or future["future_environments"] != ["near", "far"]
        or future["primary_regime"] != "eight_founders_capacity8"
        or not future["no_immigration"]):
        raise ValueError("Future shock or main stress target changed")
    est = d["estimation"]
    if (est["bootstrap"] != {
        "draws": 9999, "seed": 3711082026, "interval": "percentile95",
        "unit": "visitor_history", "shared_index_all_settings": True,
    } or est["meaningful_difference_absolute"] != 0.05):
        raise ValueError("Inference contract changed")
    if d["threshold_and_pde"]["pde"].startswith("Required"):
        raise ValueError("Unvalidated PDE cannot be made the primary gate")


def prehistories(d: dict) -> list[Prehistory]:
    hs = d["independent_histories"]
    return [
        Prehistory(s, e, a, h, r)
        for s, e, a, h, r in product(
            d["reproductive_settings"], d["environmental_settings"],
            d["path_perturbation"]["arms"],
            range(hs["first"], hs["last"] + 1),
            d["nested_demographic_repeats"]
        )
    ]


def futures(d: dict, histories: list[Prehistory] | None = None):
    histories = prehistories(d) if histories is None else histories
    for source, regime, budget, visitors in product(
        histories, d["postshock"]["arms"],
        d["postshock"]["budgets"],
        d["postshock"]["future_environments"],
    ):
        yield Future(source, regime, float(budget), visitors)


def log_budget_weights(d: dict) -> dict[float, float]:
    bs = d["postshock"]["budgets"]
    xs = [math.log(x) for x in bs]
    span = xs[-1] - xs[0]
    weights = [
        ((xs[i] - xs[i - 1] if i else 0) +
         (xs[i + 1] - xs[i] if i < len(xs) - 1 else 0)) / (2 * span)
        for i in range(len(xs))
    ]
    if not math.isclose(sum(weights), 1.0, abs_tol=1e-12):
        raise AssertionError("Bad log-budget integration")
    return dict(zip(bs, weights))


def decision(mean: float, confidence_interval: tuple[float, float],
             minimum: float = 0.05) -> str:
    """Interpret only a supplied estimate; generate no synthetic outcome."""
    low, high = confidence_interval
    if not (math.isfinite(mean) and math.isfinite(low)
            and math.isfinite(high) and low <= high):
        raise ValueError("Invalid estimate or interval")
    if abs(mean) >= minimum and (low > 0 or high < 0):
        return "nonzero_order_protocol_effect"
    if -minimum < low and high < minimum:
        return "equivalent_within_predeclared_ROPE"
    return "inconclusive"


def compile_protocol(d: dict) -> dict:
    planned = prehistories(d)
    n_forks = (len(d["postshock"]["arms"]) *
               len(d["postshock"]["budgets"]) *
               len(d["postshock"]["future_environments"]))
    expected = d["counts"]
    if (len(planned) != expected["prehistories"]
            or n_forks != expected["branches_per_prehistory"]
            or len(planned) * n_forks != expected["postshock_trajectories"]
            or len(set(planned)) != len(planned)
            or len({x.visitor_history for x in planned}) != 64):
        raise AssertionError("Frozen cohort has incomplete or duplicate tasks")
    return {
        "status": d["status"],
        "biological_outcomes_generated": False,
        "independent_visitor_histories": 64,
        "nested_repeats": 2,
        "prehistory_groups": len(planned),
        "postshock_forks_per_group": n_forks,
        "declared_postshock_trajectories": len(planned) * n_forks,
        "budget_weights": log_budget_weights(d),
        "explicit_estimate": d["estimation"]["contrast_type"],
    }


def write_manifest(d: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow([
            "setting", "pre_visitor_environment", "order_assignment",
            "visitor_history", "nested_demographic_repeat", "regime",
            "ovule_budget", "future_visitor_environment"
        ])
        for item in futures(d):
            p = item.source
            writer.writerow([
                p.setting, p.environment, p.expression_order,
                p.visitor_history, p.demographic_repeat,
                item.regime, item.budget, item.future_visitor
            ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path,
                        help="Optional case plan CSV; not a biological result")
    parser.add_argument("--receipt", type=Path,
                        help="Optional JSON design-validation receipt")
    args = parser.parse_args()
    d = load_protocol()
    report = compile_protocol(d)
    if args.manifest:
        write_manifest(d, args.manifest)
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(report, indent=2) + "\n",
                                encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
