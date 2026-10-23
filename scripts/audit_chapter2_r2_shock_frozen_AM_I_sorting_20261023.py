"""Source-exact strict A/M-fixed I polymorphism readback (no biological rerun).

The authenticated original 384-path ZIP is kept EXTERNAL to the repository.
Requires source readback from PR #630 and cross-locus guards from PR #631.
Counts are post-outcome exploratory; 24 pairs share only 11 founder seeds.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import statistics
import zipfile

from scripts.audit_chapter2_r2_cross_locus_outcomes_20261023 import (
    analyze as parent_readback, classify_cross_locus,
)
from scripts.audit_chapter2_r2_original_384_pair_convergence_20261023 import (
    ZIP_SHA, SOURCE_SHA, PROTOCOL_SHA,
)

STATUS = "EXPLORATORY_STRICT_FIXED_A_M_SORTING_IN_ORIGINAL_384_NO_NEW_BIOLOGY"
EXPECTED = {
    (0.3, "strong_baseline_limitation"): (16, 9, 16, 10, 0, 6, 7, 3, -0.11686197916666667),
    (0.3, "weak_baseline_limitation"): (1, 0, 0, 1, 0, 0, 0, 0, -0.05989583333333326),
    (0.5, "strong_baseline_limitation"): (6, 4, 6, 2, 0, 4, 2, 0, -0.015190972222222219),
    (0.5, "weak_baseline_limitation"): (1, 1, 1, 0, 1, 0, 0, 1, 0.25),
}


def _support(row: dict, name: str) -> tuple:
    support = row["genetic_support"][name]
    vals, counts = support["allele_values"], support["allele_counts"]
    if (not vals or vals != sorted(vals) or len(vals) != len(counts)
            or sum(counts) != 2 * row["n"] or row["n"] != 48):
        raise AssertionError("invalid diploid source support at original census")
    return tuple(vals)


def classify_strict(c: dict, d: dict) -> dict | None:
    checked = classify_cross_locus(c, d)
    pre = c["t_prefix"]
    if (len(_support(pre, "A")) != 1
            or len(_support(pre, "M")) != 1
            or len(_support(pre, "I")) <= 1):
        return None
    if not (checked["A_fixed_at_shock"] and checked["M_fixed_at_shock"]
            and checked["I_polymorphic_at_shock"]):
        raise AssertionError("cross-locus source checked fixation disagrees")
    for t in ("A", "M"):
        for end in (c["t_end"], d["t_end"]):
            if _support(end, t) != _support(pre, t) or end[t] != pre[t]:
                raise AssertionError(f"pre-shock genetically fixed {t} changed")
    ci = c["t_end"]["I"];di = d["t_end"]["I"];pi=pre["I"]
    cf=len(_support(c["t_end"], "I")) == 1
    df=len(_support(d["t_end"], "I")) == 1
    return {
        "initial_A": c["start_A"], "baseline": c["baseline"],
        "founder_seed": c["founder_seed"], "demographic_repeat": c["demography_repeat"],
        "I_before_shock": pi, "I_control": ci, "I_decline": di,
        "I_decline_minus_control": di-ci,
        "I_decreased_from_prefix_control": ci < pi,
        "I_decreased_from_prefix_decline": di < pi,
        "I_fixed_control": cf, "I_fixed_decline": df,
        "I_fixed_same": cf and df and _support(c["t_end"], "I") == _support(d["t_end"], "I"),
        "I_fixed_different": cf and df and _support(c["t_end"], "I") != _support(d["t_end"], "I"),
        "I_polymorphic_control_fixed_decline": not cf and df,
        "I_both_polymorphic": not cf and not df,
        "q_control_first_future": c["q_future_first"],
        "q_decline_first_future": d["q_future_first"],
    }


def audit(raw_zip: Path) -> dict:
    parent = parent_readback(raw_zip)
    if (parent["status"] != "PASS_ARCHIVED_384_PAIR_CROSS_LOCUS_DESCRIPTIVE_READBACK"
            or parent["source_zip_sha256"] != ZIP_SHA
            or parent["source_commit"] != SOURCE_SHA
            or parent["protocol_sha256"] != PROTOCOL_SHA):
        raise AssertionError("authenticated original 384 parent cross-locus admission failed")
    paired = defaultdict(dict)
    with zipfile.ZipFile(raw_zip) as z:
        for name in ("strong.json", "weak.json"):
            for row in json.loads(z.read(name))["rows"]:
                key=(row["start_A"],row["baseline"],row["founder_seed"],row["demography_repeat"])
                if row["arm"] in paired[key]:
                    raise AssertionError("duplicate original treatment arm")
                paired[key][row["arm"]] = row
    if len(paired)!=192 or any(set(x) != {"control","decline"} for x in paired.values()):
        raise AssertionError("not the original 192 complete native treatment pairs")
    rows=[]
    for arm in paired.values():
        r=classify_strict(arm["control"],arm["decline"])
        if r is not None:
            rows.append(r)
    grouped=defaultdict(list)
    for r in rows:
        grouped[(r["initial_A"],r["baseline"])].append(r)
    if set(grouped)!=set(EXPECTED):
        raise AssertionError("strict source has unexpected A×pollen baseline strata")
    strata=[]
    for key in sorted(grouped):
        rs=grouped[key]
        n=len(rs)
        count=lambda name:sum(bool(row[name]) for row in rs)
        neg=sum(row["I_decline_minus_control"]<0 for row in rs)
        pos=sum(row["I_decline_minus_control"]>0 for row in rs)
        data=(n,count("I_fixed_control"),count("I_fixed_decline"),
              neg,pos,count("I_fixed_same"),
              count("I_polymorphic_control_fixed_decline"),
              count("I_fixed_different"))
        mean=statistics.mean(row["I_decline_minus_control"] for row in rs)
        if data!=EXPECTED[key][:8] or abs(mean-EXPECTED[key][8])>1e-12:
            raise AssertionError("pre-shock A/M-frozen I-sorting source endpoint changed")
        strata.append({
            "initial_A":key[0], "baseline":key[1],
            "n_pairs":n, "n_distinct_founders":len({r["founder_seed"] for r in rs}),
            "I_fixed_at_end_control":data[1], "I_fixed_at_end_decline":data[2],
            "I_treatment_negative":neg, "I_treatment_zero":n-neg-pos,
            "I_treatment_positive":pos, "I_both_fixed_same":data[5],
            "I_control_polymorphic_decline_fixed":data[6],
            "I_both_fixed_different":data[7],
            "I_both_polymorphic":count("I_both_polymorphic"),
            "I_decreased_from_shock_control":count("I_decreased_from_prefix_control"),
            "I_decreased_from_shock_decline":count("I_decreased_from_prefix_decline"),
            "mean_signed_I_treatment_contrast":mean,
            "mean_first_future_q_control":statistics.mean(r["q_control_first_future"] for r in rs),
            "mean_first_future_q_decline":statistics.mean(r["q_decline_first_future"] for r in rs),
        })
    strong=[r for r in rows if r["baseline"]=="strong_baseline_limitation"]
    weak=[r for r in rows if r["baseline"]=="weak_baseline_limitation"]
    by_founder=defaultdict(list)
    for r in strong:
        by_founder[r["founder_seed"]].append(r["I_decline_minus_control"])
    means=[statistics.mean(v) for v in by_founder.values()]
    totals={
        "all_strict_pairs":len(rows),
        "all_strict_distinct_founders":len({r["founder_seed"] for r in rows}),
        "strong_pairs":len(strong),
        "strong_distinct_founders":len(by_founder),
        "strong_I_treatment_negative":sum(r["I_decline_minus_control"]<0 for r in strong),
        "strong_I_treatment_zero":sum(r["I_decline_minus_control"]==0 for r in strong),
        "strong_I_treatment_positive":sum(r["I_decline_minus_control"]>0 for r in strong),
        "strong_I_fixed_control":sum(r["I_fixed_control"] for r in strong),
        "strong_I_fixed_decline":sum(r["I_fixed_decline"] for r in strong),
        "strong_I_decrease_from_shock_control":sum(r["I_decreased_from_prefix_control"] for r in strong),
        "strong_I_decrease_from_shock_decline":sum(r["I_decreased_from_prefix_decline"] for r in strong),
        "strong_founder_mean_I_difference_negative":sum(m<0 for m in means),
        "strong_founder_mean_I_difference_zero":sum(m==0 for m in means),
        "strong_founder_mean_I_difference_positive":sum(m>0 for m in means),
        "strong_mean_I_contrast":statistics.mean(r["I_decline_minus_control"] for r in strong),
        "strong_q_control":statistics.mean(r["q_control_first_future"] for r in strong),
        "strong_q_decline":statistics.mean(r["q_decline_first_future"] for r in strong),
        "weak_pairs":len(weak),
    }
    if totals != {
        "all_strict_pairs":24,"all_strict_distinct_founders":11,
        "strong_pairs":22,"strong_distinct_founders":11,
        "strong_I_treatment_negative":12,"strong_I_treatment_zero":10,
        "strong_I_treatment_positive":0,"strong_I_fixed_control":13,
        "strong_I_fixed_decline":22,
        "strong_I_decrease_from_shock_control":11,
        "strong_I_decrease_from_shock_decline":20,
        "strong_founder_mean_I_difference_negative":9,
        "strong_founder_mean_I_difference_zero":2,
        "strong_founder_mean_I_difference_positive":0,
        "strong_mean_I_contrast":-0.08913352272727272,
        "strong_q_control":0.13920994216147997,
        "strong_q_decline":0.01689527391924731,
        "weak_pairs":2,
    }:
        # Floating means can be rounded at 1e-16; compare floats tolerantly.
        expect={
            "strong_mean_I_contrast":-0.08913352272727272,
            "strong_q_control":0.13920994216147997,
            "strong_q_decline":0.01689527391924731,
        }
        if any(abs(totals[k]-v)>1e-12 for k,v in expect.items()) or any(
                v!=totals[k] for k,v in {
                    "all_strict_pairs":24,"all_strict_distinct_founders":11,
                    "strong_pairs":22,"strong_distinct_founders":11,
                    "strong_I_treatment_negative":12,"strong_I_treatment_zero":10,
                    "strong_I_treatment_positive":0,"strong_I_fixed_control":13,
                    "strong_I_fixed_decline":22,
                    "strong_I_decrease_from_shock_control":11,
                    "strong_I_decrease_from_shock_decline":20,
                    "strong_founder_mean_I_difference_negative":9,
                    "strong_founder_mean_I_difference_zero":2,
                    "strong_founder_mean_I_difference_positive":0,
                    "weak_pairs":2,
                }.items()):
            raise AssertionError("source strictly frozen A/M cohort summary mismatch")
    return {
        "status":STATUS,"source_zip_sha256":ZIP_SHA,"source_sha":SOURCE_SHA,
        "source_protocol_sha256":PROTOCOL_SHA,"source_actions_run_id":39233450099,
        "independent_founders_in_original_study":12,
        "n_original_paths":384,"n_original_pairs":192,
        "strata":strata,"totals":totals,
        "reporting_unit":"source founder; four nested demographic repeats; source subset selected after original results",
        "claim_rank":"RETROSPECTIVE_SOURCE_MODEL_NEGATIVE_CONTROL_ONLY",
        "causal_boundary":"Fixed A/M at census30 is an observed prior evolved state, not independently randomized; visitor activity differs within matched futures, but selection-versus-drift shares are not identified",
        "new_biological_population_updates":0,
        "new_statistical_tests":0,
    }


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--zip",required=True,type=Path)
    args=p.parse_args()
    print(json.dumps(audit(args.zip),indent=2,sort_keys=True))
