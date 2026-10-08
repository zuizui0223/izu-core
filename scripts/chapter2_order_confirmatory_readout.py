"""Admit 3,072 verified t400 sources + 86,016 futures, then apply frozen ITT.

Do not use trait-crossing order as a selector. Bootstrapping uses only the 64
visitor histories; demographic repeats, budgets, future visitor environments,
and mating settings remain paired within each ecological history.
"""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import argparse
import hashlib
import json

import numpy as np

from scripts.plan_chapter2_order_expression_identification import (
    SPEC, Prehistory, decision, load_protocol, log_budget_weights,
    prehistories,
)
from scripts.chapter2_order_prehistory_runner import (
    case_key, source_hashes,
)
from scripts.chapter2_order_postshock_runner import (
    restore_prehistory, sampled_eight,
)


def _genetic_order_from_censuses(annual, threshold: float) -> dict:
    """Independently recompute order from the full annual inherited summaries."""
    if len(annual) != 401 or [r["year"] for r in annual] != list(range(401)):
        raise AssertionError("missing/duplicate annual genetic censuses")
    founder = annual[0]["inherited_means"]
    if annual[0]["n"] < 1 or founder is None:
        raise AssertionError("no recorded full founder population")
    observed = {"A": None, "I": None}
    first_extinction = None
    for t, row in enumerate(annual):
        n = row["n"]
        value = row["inherited_means"]
        if (not isinstance(n, int) or isinstance(n, bool)
                or n < 0 or (n == 0) != (value is None)):
            raise AssertionError("census count/missing genotype mismatch")
        if first_extinction is not None and n:
            raise AssertionError("resurrection after extinction in no-migration cohort")
        if n == 0:
            if first_extinction is None:
                first_extinction = t
            continue
        if len(value) != 3 or not np.isfinite(value).all():
            raise AssertionError("invalid observed inherited traits")
        for trait, index in (("A", 2), ("I", 1)):
            if observed[trait] is None and abs(value[index]-founder[index]) >= threshold:
                observed[trait] = t
    a, i = observed["A"], observed["I"]
    if a is None and i is None:
        label = "neither"
    elif i is None:
        label = "A_only"
    elif a is None:
        label = "I_only"
    elif a == i:
        label = "tie"
    elif a < i:
        label = "A_before_I"
    else:
        label = "I_before_A"
    return {
        "classification": label, "inherited_A_first_crossing": a,
        "inherited_I_first_crossing": i, "first_extinction_year": first_extinction,
        "extinct_by_t400": annual[-1]["n"] == 0,
    }


def _audit_postshock_cell(cell, source_n: int, d: dict) -> None:
    regime = cell["regime"]
    cap = 48 if regime == "unbottlenecked_capacity48" else 8
    t0 = source_n if cap == 48 else min(8, source_n)
    occupied = cell["occupied"]
    final = cell["end_population"]
    extinction = cell["first_extinction"]
    if (cell["t0_population"] != t0 or t0 > cap
            or not isinstance(final, int) or isinstance(final, bool)
            or not 0 <= final <= cap
            or type(occupied) is not int or occupied not in (0,1)
            or occupied != int(final > 0)):
        raise AssertionError("postshock population or capacity inconsistency")
    if (t0 == 0 and extinction != 0
            or t0 > 0 and occupied and extinction is not None
            or t0 > 0 and not occupied and extinction is None):
        raise AssertionError("invalid first extinction event")
    if (extinction is not None and
            (type(extinction) is not int or not 0 <= extinction <=
             d["postshock"]["updates"] or t0 > 0 and extinction == 0)):
        raise AssertionError("impossible extinction timing")
    if ((cell["immediate_reproductive_payoff"] is None) != (t0 == 0)
            or (cell["surviving_genetic_endpoint"] is None) != (final == 0)
            or cell["future_assurance_mode"] != "evolving"
            or cell["future_expression_offsets"] != [0, 0]):
        raise AssertionError("future biology or genetic endpoint inconsistency")
    for key in ("selfed_recruits","outcross_recruits"):
        n = cell[key]
        if type(n) is not int or n < 0 or t0 == 0 and n:
            raise AssertionError("invalid postshock realized recruitment")


def admit_all(pre_dir: Path, post_dir: Path, d: dict, *,
              tasks: list[Prehistory] | None = None,
              require_full: bool = True):
    """Read exact raw receipts; never infer an absent case from other sources."""
    all_tasks = prehistories(d) if tasks is None else tasks
    if require_full and len(all_tasks) != d["counts"]["prehistories"]:
        raise AssertionError("cannot adjudicate partial prospective dataset")
    proto_sha = hashlib.sha256(SPEC.read_bytes()).hexdigest()
    hashes = source_hashes()
    pre, post = {}, {}
    expected_grid = {
        (r, float(b), e) for r in d["postshock"]["arms"]
        for b in d["postshock"]["budgets"]
        for e in d["postshock"]["future_environments"]
    }
    for task in all_tasks:
        key = case_key(task)
        state, source_sha = restore_prehistory(pre_dir, task, d, hashes)
        recorded_pre = json.loads((Path(pre_dir) / f"{key}.json").read_text())
        annual = recorded_pre["annual_inherited_censuses"]
        label = _genetic_order_from_censuses(annual, 0.05)
        prior = recorded_pre["realized_genetic_order"]
        if prior is None or any(prior[k] != value for k,value in label.items()):
            raise AssertionError("raw annual genetic order differs from state summary")
        checkpoints = recorded_pre["checkpoints"]
        if [r["t"] for r in checkpoints] != d["prehistory"]["snapshot_times"]:
            raise AssertionError("bad/repeated source checkpoints")
        trait = state.alleles.mean(axis=2)
        expected_final = trait.mean(axis=0).tolist() if len(state.ids) else None
        if (checkpoints[-1]["n"] != len(state.ids)
                or checkpoints[-1]["means"] is None and expected_final is not None
                or checkpoints[-1]["means"] is not None and expected_final is None
                or expected_final is not None and not np.allclose(
                    checkpoints[-1]["means"], expected_final, rtol=0, atol=1e-12)):
            raise AssertionError("t400 checkpoint differs from exact allele archive")
        post_file = Path(post_dir) / f"{key}.json"
        receipt_file = Path(post_dir) / f"{key}.sha256"
        if not post_file.is_file() or not receipt_file.is_file():
            raise FileNotFoundError("missing complete future fork " + key)
        if hashlib.sha256(post_file.read_bytes()).hexdigest() != receipt_file.read_text().strip():
            raise AssertionError("unverified future receipt " + key)
        row = json.loads(post_file.read_text())
        chosen = sampled_eight(task, state, d)
        if (row["status"] != "raw_postshock_unadjudicated"
                or row["task"] != asdict(task)
                or row["protocol_sha256"] != proto_sha
                or row["source_hashes"] != hashes
                or row["prehistory_state_sha256"] != source_sha
                or row["sampled_eight_allele_sha256"] != hashlib.sha256(
                    chosen.alleles.tobytes()).hexdigest()):
            raise AssertionError("incorrect genotype fork, protocol or source")
        cells = row["postshock"]
        seen = {(r["regime"],float(r["budget"]),r["future_visitor"]) for r in cells}
        if len(cells) != 28 or seen != expected_grid:
            raise AssertionError("incomplete or duplicate 28-fork grid")
        for cell in cells:
            _audit_postshock_cell(cell, len(state.ids), d)
        pre[task] = recorded_pre
        post[task] = {(r["regime"],float(r["budget"]),r["future_visitor"]):r
                      for r in cells}
    if require_full and (len(pre) != 3072 or len(post) != 3072
                         or sum(len(r) for r in post.values()) != 86016):
        raise AssertionError("complete raw cohort count not met")
    return pre, post


def evaluate(d: dict, post: dict) -> dict:
    """All 64 history pairs contribute, including pre-extinct sources."""
    histories = range(d["independent_histories"]["first"],
                      d["independent_histories"]["last"] + 1)
    repeats = d["nested_demographic_repeats"]
    weights = log_budget_weights(d)
    settings = d["reproductive_settings"]
    regimes = d["postshock"]["arms"]
    preenvs = d["environmental_settings"]
    treatments = list(d["path_perturbation"]["arms"])
    summaries = {}
    for regime in regimes:
        # visitor history x mating setting x historical environment x treatment
        matrix = np.empty((64,4,2,3), dtype=float)
        for hi, h in enumerate(histories):
            for si, setting in enumerate(settings):
                for ei, env in enumerate(preenvs):
                    for ti, arm in enumerate(treatments):
                        vals = []
                        for repeat in repeats:
                            key = Prehistory(setting,env,arm,h,repeat)
                            cellset = post[key]
                            for future in d["postshock"]["future_environments"]:
                                vals.append(sum(
                                    weights[b]*cellset[(regime,b,future)]["occupied"]
                                    for b in weights
                                ))
                        matrix[hi,si,ei,ti] = float(np.mean(vals))
        # Historical far–near contrast between A-first and I-first.
        af, ifirst = treatments.index("assurance_first"), treatments.index("investment_first")
        delta = ((matrix[:,:,1,af]-matrix[:,:,1,ifirst])
                 -(matrix[:,:,0,af]-matrix[:,:,0,ifirst]))
        summaries[regime] = {
            "history_setting_order_contrast": delta,
            "history_averaged": delta.mean(axis=1),
            "arm_survival_mean": matrix.mean(axis=0),
        }
    primary = summaries[d["postshock"]["primary_regime"]]
    values = primary["history_averaged"]
    rng = np.random.default_rng(d["estimation"]["bootstrap"]["seed"])
    draws = rng.integers(0,64,size=(
        d["estimation"]["bootstrap"]["draws"],64))
    sampled = values[draws].mean(axis=1)
    mean = float(values.mean())
    interval = [float(x) for x in np.percentile(sampled,[2.5,97.5])]
    result = {
        "status": "all_full_raw_cases_admitted_and_frozen_itt_adjudicated",
        "n_independent_visitor_histories": 64,
        "n_nested_demographic_repeats": 2,
        "declared_prehistories": 3072,
        "declared_postshock_trajectories": 86016,
        "main_order_history_DID": {
            "pooled_mean":mean,
            "history_bootstrap95":interval,
            "decision":decision(mean,tuple(interval)),
        },
        "all_regime_aggregate": {},
        "claim_boundaries": [
            "The randomized intervention is assigned transient phenotype-expression order, NOT realized inherited first-crossing order.",
            "No post-treatment survival selection or genotype mediation is inferred.",
            "Stress envelopes are synthetic and do not identify natural island extinction probability.",
            "Historic failed mutation-access priority confirmation remains FAILED.",
        ],
    }
    for regime, r in summaries.items():
        contrasts = r["history_setting_order_contrast"]
        result["all_regime_aggregate"][regime] = {
            "setting_order_effects": {
                setting: float(contrasts[:, i].mean())
                for i,setting in enumerate(settings)
            },
            "pooled_order_effect": float(r["history_averaged"].mean()),
            "mean_occupancy_by_setting_pre_environment_treatment": {
                setting: {
                    env: {
                        arm: float(r["arm_survival_mean"][i, j, k])
                        for k,arm in enumerate(treatments)
                    } for j,env in enumerate(preenvs)
                } for i,setting in enumerate(settings)
            },
        }
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prehistory", type=Path, required=True)
    p.add_argument("--postshock", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    d = load_protocol()
    before, after = admit_all(args.prehistory,args.postshock,d)
    result = evaluate(d,after)
    result["source_hashes"] = source_hashes()
    result["protocol_sha256"] = hashlib.sha256(SPEC.read_bytes()).hexdigest()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps({
        "complete_raw":len(before)==3072,
        "independent_histories":64,
        "primary_decision":result["main_order_history_DID"]["decision"],
    }))


if __name__=="__main__":
    main()
