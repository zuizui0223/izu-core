"""Post-outcome decomposition of Chapter 2 assigned-expression-order outcomes.

Reuses ONLY the completed 2026-10-09 independent visitor-history futures.
No new visitor histories, no biological simulation, no survivor-conditioned
causal mediation claim. Full source receipt verification is delegated to the
already validated occupancy parser, and 64 visitor histories are bootstrapped.
"""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import argparse
import json

import numpy as np

from scripts.chapter2_order_absolute_posthoc import (
    DRAWS, EXPECTED_RUN, EXPECTED_SOURCE_SHA, load_verified_futures,
    paired_percentile,
)
from scripts.chapter2_order_budget_window_followup import load_followup
from scripts.chapter2_order_prehistory_runner import case_key
from scripts.plan_chapter2_order_expression_identification import (
    Prehistory, log_budget_weights, prehistories,
)

METRICS = (
    "occupied",
    "t0_present",
    "t0_population",
    "cumulative_selfed_recruits",
    "cumulative_outcross_recruits",
    "cumulative_total_recruits",
    "t0_maternal_viable_population",
    "t0_female_outcross_population",
    "t0_viable_selfed_population",
    "t0_paternal_export_population",
)
PAYOFF_FIELDS = {
    "t0_maternal_viable_population": "maternal_viable_per_plant",
    "t0_female_outcross_population": "female_outcross_per_plant",
    "t0_viable_selfed_population": "viable_selfed_per_plant",
    "t0_paternal_export_population": "paternal_export_per_plant",
}


def read_metrics(root: Path) -> tuple[dict, dict[str, np.ndarray]]:
    """Admit all 57,344 original cells before reading any optional payoff."""
    d, occupied = load_verified_futures(root)
    if occupied.shape != (64,4,2,2,2,7,2,2):
        raise AssertionError("Original complete future-grid shape changed")
    arrays = {name: np.full(occupied.shape, np.nan, dtype=float)
              for name in METRICS}
    arrays["occupied"] = occupied.copy()
    regimes = d["postshock"]["arms"]
    settings = d["reproductive_settings"]
    futures = d["postshock"]["future_environments"]
    budgets = d["postshock"]["budgets"]
    repeats = d["nested_demographic_repeats"]
    arms = ("assurance_first", "investment_first")
    source_counts = 0
    for task in prehistories(d):
        history_index = task.visitor_history - 38110901
        folder = root / f"budget-window-post-shard-{history_index}"
        row = json.loads((folder / f"{case_key(task)}.json").read_text())
        if row["task"] != asdict(task) or len(row["postshock"]) != 28:
            raise AssertionError("Future record changed after verified receipt")
        base = (
            history_index,
            settings.index(task.setting),
            ("near", "far").index(task.environment),
            arms.index(task.expression_order),
            repeats.index(task.demographic_repeat),
        )
        source_counts += 1
        for cell in row["postshock"]:
            idx = base + (
                budgets.index(float(cell["budget"])),
                futures.index(cell["future_visitor"]),
                regimes.index(cell["regime"]),
            )
            if float(cell["occupied"]) != arrays["occupied"][idx]:
                raise AssertionError("Second pass and independent occupancy audit disagree")
            initial = cell["t0_population"]
            selfed = cell["selfed_recruits"]
            outcross = cell["outcross_recruits"]
            payoff = cell["immediate_reproductive_payoff"]
            cap = 8 if cell["regime"] == "eight_founders_capacity8" else 48
            if (type(initial) is not int or not 0 <= initial <= cap
                    or type(selfed) is not int or selfed < 0
                    or type(outcross) is not int or outcross < 0
                    or (payoff is None) != (initial == 0)
                    or (initial == 0 and (selfed or outcross))):
                raise AssertionError("Invalid initial population or recruitment receipt")
            arrays["t0_present"][idx] = int(initial > 0)
            arrays["t0_population"][idx] = initial
            arrays["cumulative_selfed_recruits"][idx] = selfed
            arrays["cumulative_outcross_recruits"][idx] = outcross
            arrays["cumulative_total_recruits"][idx] = selfed + outcross
            for name, field in PAYOFF_FIELDS.items():
                if initial:
                    val = payoff[field]
                    if (not isinstance(val, (int, float))
                            or not np.isfinite(val) or val < 0):
                        raise AssertionError("Invalid immediate reproductive payoff")
                    arrays[name][idx] = initial * float(val)
                else:
                    # This is a well-defined population TOTAL (zero plants),
                    # not a fabricated per-capita payoff after extinction.
                    arrays[name][idx] = 0.0
    if source_counts != 2048:
        raise AssertionError("Incomplete source-group accounting")
    for name, arr in arrays.items():
        if not np.isfinite(arr).all():
            raise AssertionError("Missing/invalid source or future cell: "+name)
    if not np.allclose(
            arrays["cumulative_total_recruits"],
            arrays["cumulative_selfed_recruits"]+
            arrays["cumulative_outcross_recruits"],rtol=0,atol=0):
        raise AssertionError("Cumulative recruitment count mismatch")
    return d, arrays


def calculate_contrasts(d: dict, arrays: dict[str, np.ndarray]) -> dict:
    budgets = d["postshock"]["budgets"]
    weights = log_budget_weights(d)
    weight_vector = np.array([weights[float(b)] for b in budgets])
    if (len(weight_vector) != 7 or not np.isclose(weight_vector.sum(),1)):
        raise AssertionError("Invalid original log-budget weights")
    draw = np.random.default_rng(2026100918).integers(0,64,size=(DRAWS,64))
    out={}
    for gi,regime in enumerate(d["postshock"]["arms"]):
        result={}
        for metric, raw in arrays.items():
            # history x mating setting x historical environment x arm x budget
            mean = raw[:,:,:,:,:,:,:,gi].mean(axis=(4,6))
            if mean.shape!=(64,4,2,2,7):
                raise AssertionError("Corrupt history pairing")
            weighted = np.tensordot(mean,weight_vector,axes=([4],[0]))
            effects = weighted[:,:,:,0]-weighted[:,:,:,1]
            pooled = effects.mean(axis=1)
            near,far=pooled[:,0],pooled[:,1]
            result[metric]={
                "near":paired_percentile(near,draw),
                "far":paired_percentile(far,draw),
                "common_mean":paired_percentile((near+far)/2,draw),
                "far_minus_near":paired_percentile(far-near,draw),
                "by_setting":{
                    setting:{
                        "near":paired_percentile(effects[:,si,0],draw),
                        "far":paired_percentile(effects[:,si,1],draw),
                    }
                    for si,setting in enumerate(d["reproductive_settings"])
                },
                "budget_effects":{
                    str(b):{
                        "near":float((mean[:,:,:,0,bi]-mean[:,:,:,1,bi])[:,:,0].mean()),
                        "far":float((mean[:,:,:,0,bi]-mean[:,:,:,1,bi])[:,:,1].mean()),
                    }
                    for bi,b in enumerate(budgets)
                },
            }
        out[regime]=result
    return {
        "status":"POST_OUTCOME_DESCRIPTIVE_CHANNEL_DECOMPOSITION_NOT_CAUSAL_MEDIATION",
        "source_run":EXPECTED_RUN,
        "source_commit_sha":EXPECTED_SOURCE_SHA,
        "n_independent_visitor_histories":64,
        "source_groups_verified":2048,
        "future_branches_verified":57344,
        "bootstrap_unit":"visitor_history",
        "bootstrap_draws":DRAWS,
        "bootstrap_seed":2026100918,
        "integrated_budgets":list(budgets),
        "metrics":out,
        "limits":[
            "This is post-outcome exploration of previously observed complete futures.",
            "Immediate payoff is the per-plant reproductive output at the first future visitor census TIMES actual t0 population; zero for a truly empty source, never a made-up per-capita measurement.",
            "Cumulative resident recruit counts are measured across the full 80-step future and are influenced by demographic persistence and extinction; they are not independent mediators.",
            "Contrasting t0 payoffs, lifetime recruits, and final occupancy does not identify genetic or demographic causal mediation.",
            "Source pre-extinction is retained as zero occupancy/zero population-level payoff and zero recruits in the unconditional 64-history ITT-style summaries.",
            "The preregistered practically equivalent original DID and failed independent fixed resource-window test remain unchanged.",
            "No biological new histories, interventions, or synthetic natural-island risk calibration."
        ],
    }


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--post-dir",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    d,arrays=read_metrics(args.post_dir)
    answer=calculate_contrasts(d,arrays)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(answer,indent=2,allow_nan=False)+"\n",
                        encoding="utf-8")
    primary=answer["metrics"]["eight_founders_capacity8"]
    print(json.dumps({
        "status":answer["status"],
        "source_groups":answer["source_groups_verified"],
        "future_branches":answer["future_branches_verified"],
        "primary_common_occupancy":primary["occupied"]["common_mean"]["mean"],
        "primary_common_total_recruitment":primary["cumulative_total_recruits"]["common_mean"]["mean"],
    }))


if __name__=="__main__":
    main()
