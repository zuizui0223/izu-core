"""Original frozen-genome Price accounting for the far-side assurance paradox.

Read-only, post-outcome source diagnosis. Reuses verified four 2026-10-06
GitHub Actions ZIPs (shards 0..3), one of eight demographic repeats, and
the actual source visitor RNG states at t200/t400. No new descendant,
mutation, ecological history, or demographic trajectory is generated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_original_evolved_pollen_service import (
    original_shards, parity, read_design, source_visitors, state_from_archive,
)
from scripts.run_chapter2_assurance_generality import (
    config, load_design, DEFAULT_DESIGN,
)
from scripts.model3_island.reproduction import reproduce

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data/design/chapter2_far_assurance_price_checkpoint_20261015.json"


def protocol():
    p = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    d = read_design()
    if (
        p["status"] != "SOURCE_ONLY_PROTOCOL_FIXED_BEFORE_THIS_AUDIT_EXECUTION"
        or p["source_workflow_run_id"] != d["original_workflow_run_id"]
        or p["original_shard_ids_ordered"] !=
            [row["artifact_id"] for row in d["artifact_shards"]]
        or p["original_nested_demographic_repeat"] != d["demographic_repeat_seed"]
        or p["reproduction_settings"] != d["settings"]
        or p["pollen_arms"] != d["arms"]
        or p["assurance_modes"] != ["fixed", "evolving"]
        or p["checkpoint_trait_periods"] != [0, 200, 400, 1000]
        or p["price_assay_periods"] != d["periods"]
        or p["original_independent_visitor_histories"] != {
            "first": d["history_seed_first"],
            "last": d["history_seed_last"],
            "count": 64,
        }
    ):
        raise ValueError("source protocol or frozen contract changed")
    return p, d


def full_parent_price(state, visitors, cfg):
    """Original full F/P/S parental lottery and exact next-mean identity.

    Conditional on any resident descendant being recruited, not an 80-year
    genetic/fecundity/exinction result. No new mutation is applied.
    """
    if len(state.ids) < 1:
        raise ValueError("expected occupied original checkpoint")
    led = reproduce(state, visitors, cfg)
    F = led.outcross.sum(axis=0)
    P = led.outcross.sum(axis=1)
    S = led.self_viable
    W = .5 * (F + P) + S
    mu = float(led.maternal.sum())
    if not (mu > 0 and np.isclose(mu, W.sum(), atol=2e-10, rtol=0)
            and np.isclose(F.sum(), P.sum(), atol=2e-10, rtol=0)):
        raise AssertionError("original parental ledger not conserved")
    I = state.alleles[:, 1, :].mean(axis=1)
    old = float(I.mean())
    genetic_next = float(np.dot(W, I) / mu)
    cov = float(np.mean((I - old) * (W - W.mean())))
    shift = float(cov / W.mean())
    parents = led.outcross.copy()
    parents[np.diag_indices(len(I))] += S
    direct = float((parents * .5 * (I[:, None] + I[None, :])).sum() / mu)
    if (
        abs(genetic_next - direct) > 1e-12
        or abs((genetic_next - old) - shift) > 1e-12
    ):
        raise AssertionError("Original price identity disagrees with parent pairs")
    result = {
        "genetic_mean_I": old,
        "genetic_variance_I": float(I.var()),
        "genetic_mean_A": float(state.alleles[:, 2, :].mean()),
        "genetic_cov_I_A": float(np.mean(
            (I-I.mean()) * (
                state.alleles[:, 2, :].mean(axis=1)
                - state.alleles[:, 2, :].mean()
            )
        )),
        "expected_next_I_if_occupied": genetic_next,
        "price_shift_I": shift,
        "source_genetic_price_cov_I_W": cov,
        "source_total_viable_mu": mu,
        "n_adults": len(I),
        "n_visitors": len(visitors.ids),
    }
    if len(visitors.ids) == 0:
        # Original source with no pollen transfer:
        # W_i ∝ exp(-c_I I_i²) * (A_i exp(-c_A A_i²)).
        # This is an algebraic within-source distribution counterfactual,
        # NOT a historical do(A-evolution) causal mediator.
        A = state.alleles[:, 2, :].mean(axis=1) if cfg.assurance_mode == "evolving" \
            else np.full(len(I), cfg.fixed_assurance)
        base = np.exp(-cfg.investment_cost * I**2)
        h = A * np.exp(-cfg.assurance_cost * A**2)
        if np.dot(base, h) <= 0:
            raise AssertionError("zero-pollen original genome lacks viable selfing")
        expected = float(np.dot(I, base*h) / np.dot(base, h))
        direct_Ionly = float(np.dot(I, base) / base.sum())
        if abs(genetic_next - expected) > 1e-12:
            raise AssertionError("zero-pollen source fitness factorization failed")
        result["zero_visitor"] = {
            "expected_next_I_from_source_factorization": expected,
            "expected_next_I_if_A_factor_constant": direct_Ionly,
            "A_weight_alignment_effect": expected - direct_Ionly,
            "Ionly_expected_shift": direct_Ionly - old,
            "A_factor_range": [float(h.min()), float(h.max())],
            "conditional_original_Price_shift": shift,
        }
        if cfg.assurance_mode == "fixed" and abs(expected-direct_Ionly) > 1e-12:
            raise AssertionError("fixed-A source should have zero factor alignment")
    return result


def source_readout(shard_paths):
    p, design = protocol()
    archives = original_shards(shard_paths, design)
    parity()
    source = load_design(DEFAULT_DESIGN)
    settings, arms, modes = p["reproduction_settings"], p["pollen_arms"], p["assurance_modes"]
    trait_times = p["checkpoint_trait_periods"]
    price_times = set(p["price_assay_periods"])
    all_records = []
    for setting in settings:
        for history in range(26110601, 26110665):
            for arm in arms:
                visitor = source_visitors(history, arm)
                states = {}
                for mode in modes:
                    shard = 0 if arm == "near" and mode == "fixed" else (
                        1 if arm == "near" else (2 if mode == "fixed" else 3)
                    )
                    original = archives[shard]
                    cfg = config(source, setting, .01, mode)
                    for t in trait_times:
                        state = state_from_archive(original, shard, setting, history, arm, mode, t)
                        I = float(state.alleles[:,1,:].mean())
                        A = float(state.alleles[:,2,:].mean()) if mode=="evolving" \
                            else cfg.fixed_assurance
                        if (mode == "fixed"
                                and not np.all(state.alleles[:, 2, :] == .5)):
                            raise AssertionError("fixed original assurance locus moved")
                        result = {
                            "original_setting":setting,
                            "original_history":history,
                            "original_repeat":26111601,
                            "arm":arm,
                            "mode":mode,
                            "t":t,
                            "source_mean_I":I,
                            "source_mean_A":A,
                            "original_checkpoint_N":len(state.ids),
                        }
                        if t in price_times:
                            result["price"] = full_parent_price(state,visitor[t],cfg)
                        states[mode,t] = result
                        all_records.append(result)
                for t in trait_times:
                    if t == 0 and abs(states["fixed",t]["source_mean_I"]
                                       - states["evolving",t]["source_mean_I"]) > 1e-12:
                        raise AssertionError("founder I differs between original arms")
        print("source authentication and Price calculations finished:",setting,flush=True)
    if len(all_records) != 4*64*2*2*4:
        raise AssertionError("original checkpoint inclusion incomplete")

    def metrics(vals):
        x=np.asarray(vals,dtype=float)
        return dict(mean=float(x.mean()),min=float(x.min()),
                    max=float(x.max()),positive=int((x>1e-12).sum()),
                    negative=int((x< -1e-12).sum()),zero=int((abs(x)<=1e-12).sum()),
                    n=len(x))

    summary = []
    for setting in settings:
        for arm in arms:
            for t in trait_times:
                group=[r for r in all_records
                       if r["original_setting"]==setting and r["arm"]==arm and r["t"]==t]
                fixed={r["original_history"]:r for r in group if r["mode"]=="fixed"}
                evolved={r["original_history"]:r for r in group if r["mode"]=="evolving"}
                if len(fixed)!=64 or len(evolved)!=64:
                    raise AssertionError("paired source case lost")
                diffs=[evolved[k]["source_mean_I"]-fixed[k]["source_mean_I"]
                       for k in sorted(fixed)]
                rec={
                    "setting":setting,"arm":arm,"t":t,
                    "original_histories":64,"original_nested_repeats_used":1,
                    "evolving_minus_fixed_I":metrics(diffs),
                    "evolving_I":metrics([r["source_mean_I"] for r in evolved.values()]),
                    "fixed_I":metrics([r["source_mean_I"] for r in fixed.values()]),
                }
                if t in price_times:
                    ep=[evolved[k]["price"] for k in sorted(fixed)]
                    fp=[fixed[k]["price"] for k in sorted(fixed)]
                    rec["zero_visitor_histories"]=sum(x["n_visitors"]==0 for x in ep)
                    rec["source_price_shift_evolving"]=metrics(
                        [r["price_shift_I"] for r in ep])
                    rec["source_price_shift_fixed"]=metrics(
                        [r["price_shift_I"] for r in fp])
                    rec["source_price_shift_E_minus_F"]=metrics(
                        [e["price_shift_I"]-f["price_shift_I"]
                         for e,f in zip(ep,fp)])
                    no_v=[r for r in ep if r["n_visitors"]==0]
                    if no_v:
                        rec["zero_visitor_evolving_A_alignment"]=metrics([
                            r["zero_visitor"]["A_weight_alignment_effect"] for r in no_v
                        ])
                        rec["zero_visitor_evolving_Ionly_shift"]=metrics([
                            r["zero_visitor"]["Ionly_expected_shift"] for r in no_v
                        ])
                        rec["zero_visitor_evolving_full_price_shift"]=metrics([
                            r["price_shift_I"] for r in no_v
                        ])
                summary.append(rec)
    return {
        "status":"ORIGINAL_FROZEN_GENOMES_RETROSPECTIVE_PRICE_ONLY",
        "claim_rank":"source_only_past_history_descriptive_not_independent_future_test",
        "protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
        "original_artifact_ids":p["original_shard_ids_ordered"],
        "original_archive_shas":[x["outer_zip_sha256"] for x in design["artifact_shards"]],
        "original_history_count":64,
        "original_nested_repeat_used":1,
        "original_genetic_checkpoints":len(all_records),
        "original_price_cells":sum("price" in x for x in all_records),
        "independent_new_evolutionary_histories":0,
        "summary":summary,
        "rows":all_records,
        "boundaries":[
            "The first of eight original demographic repeats cannot replace four-setting 8-repeat CI.",
            "Original t0/t200/t400/t1000 checkpoint contrasts are not annual inherited selection paths.",
            "The Price identity is a one-generation conditional expectation without contemporaneous mutation or immigration.",
            "A-weight alignment under zero visitors is original-genome cross-sectional accounting, not mediation of enabling A evolution.",
            "Positive far E-minus-F I endpoint at t1000 is not inferred from t200/t400 local gradients.",
            "All histories including zero-visitor source states retained; no group was selected after outcome.",
        ]
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shards",nargs=4,required=True,type=Path)
    parser.add_argument("--out",required=True,type=Path)
    args=parser.parse_args()
    report=source_readout(args.shards)
    if args.out.exists():
        raise ValueError("preserve existing source result")
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n",
                        encoding="utf-8")
    compact=[
        {"setting":r["setting"],"arm":r["arm"],"t":r["t"],
         "deltaI":r["evolving_minus_fixed_I"]["mean"],
         "deltaPrice":r.get("source_price_shift_E_minus_F",{}).get("mean"),
         "zeroV":r.get("zero_visitor_histories"),
         "alignment":r.get("zero_visitor_evolving_A_alignment",{}).get("mean"),
         "n":r["original_histories"]}
        for r in report["summary"]
    ]
    print("ORIGINAL_GENOME_PRICE_SUMMARY "+json.dumps(compact,sort_keys=True),flush=True)
    print("ORIGINAL_GENOME_PRICE_COMPLETE status="+report["status"]+
          " rows="+str(report["original_genetic_checkpoints"]),flush=True)


if __name__=="__main__":
    main()
