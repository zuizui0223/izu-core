"""Read-only reconciliation of two recorded Q3 budget-companion seed families.

No native evolutionary operator is imported, no old result is overwritten,
and no added descendant draw is treated as a new founder or visitor sample.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from scripts.audit_chapter2_equalA_precision_20261018 import (
    exact_pigeonhole, variance_components, mde_proxy, review as review_old,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/"docs/audits/CHAPTER2_BUDGET_COMPANION_STREAM_RECONCILIATION_20261018.json"
OLD_SOURCE = ROOT/"docs/audits/CHAPTER2_EQUALA_PILOT_EVENT_SOURCE_20261018.json"
ARMS = ("fixed_B8","evolving_B8","fixed_B4.5","evolving_B4.5")


def review(data, old):
    shared = data.get("shared_source", {})
    if (data.get("schema") != "chapter2_budget_companion_stream_reconciliation_v1"
        or shared.get("existing_founder_ids") != list(range(301001,301007))
        or shared.get("existing_visitor_ids") != list(range(302001,302007))
        or shared.get("historical_repeats") != 2
        or shared.get("checkpoint") != 35 or shared.get("end_census") != 80
        or set(data.get("streams",{})) != {"90","104"}):
        raise ValueError("wrong source, crossed axes or follow-up")
    old_review = review_old(old)
    result = {}
    for prefix, entry in data["streams"].items():
        if entry.get("seed_prefix") != [20261018,int(prefix)]:
            raise ValueError("stream namespace mismatch")
        codes = entry.get("terminal_status_codes", {})
        if set(codes) != set(ARMS):
            raise ValueError("missing policy-by-budget arms")
        decoded = {}
        arms = {}
        for name, code in codes.items():
            if not isinstance(code,str) or len(code)!=72 or set(code)-set("012"):
                raise ValueError("wrong source count or terminal-state code")
            a = np.array([int(x) for x in code],dtype=int).reshape(6,6,2)
            decoded[name] = a
            arms[name] = dict(alive=int((a>0).sum()), extinct=int((a==0).sum()),
                alive_closed=int((a==1).sum()), alive_accessible=int((a==2).sum()))
            if arms[name]["alive"]+arms[name]["extinct"] != 72:
                raise AssertionError("current-state partition failed")
        block = dict(arms=arms)
        for outcome, predicate in (("survival",lambda a:a>0),
                                    ("access",lambda a:a==2)):
            y = {name:predicate(x).astype(int) for name,x in decoded.items()}
            contrast = ((y["evolving_B4.5"]-y["fixed_B4.5"])
                        -(y["evolving_B8"]-y["fixed_B8"]))
            block[outcome+"_interaction"] = dict(
                estimate=float(contrast.mean()),
                exploratory_percentile=exact_pigeonhole(contrast),
                variance_components=variance_components(contrast))
        result[prefix] = block
    genetic_var = old_review["paired_risk_variance_components"]
    # Both baseline survival inputs are reported; no favorable one is selected.
    # Same #585 normal/Bonferroni screen as the existing source helper.
    stress = dict(founder=.05,visitor=.05,interaction=.20,within_cell=.40)
    frontier = []
    for n in (6,16,32,64):
        frontier.append(dict(F=n,V=n,historical_repeats=2,
            genetic_loss_mde=mde_proxy(genetic_var,n,n,2),
            survival_mde_by_stream={p:mde_proxy(
                b["survival_interaction"]["variance_components"],n,n,2)
                for p,b in result.items()},
            assumed_stress_mde=mde_proxy(stress,n,n,2)))
    return dict(
        status="POST_OUTCOME_SOURCE_RECONCILIATION_AND_POWER_INPUTS_NOT_CONFIRMATION",
        independent_axes=dict(founders=6,visitors=6), shared_historical_pairs=72,
        reported_descendant_seed_families=2, new_unique_biological_histories=0,
        by_stream=result,
        old_genetic_loss=dict(
            fixed=old_review["counts"]["fixed_high_I_loss"],
            evolving=old_review["counts"]["evolving_high_I_loss"],
            variance_components=genetic_var,unchanged_old_result=True),
        power_screen_only=frontier,
        stress_is_sensitivity_assumption_not_estimated_upper_bound=True,
        selected_SESOI=None,new_confirmatory_sample_size=None,
        power_screen_is_not_approval=True,confirmation_authorized=False,
        limits=[
            "Two descendant stream families reuse the SAME historical 72 pairs.",
            "No combined independence claim or new biological confirmation.",
            "Prefix90 agrees with the GitHub receipt after same-seed native replay; remote raw-byte identity is not asserted.",
            "Prefix104 raw check covers 1152 stored genotypes and 13248 census summaries, not unarchived intermediate whole genomes.",
            "Positive budget-rescue interactions are not actual post-pollinator-return floral recovery.",
            "No causal mediation by final A or universally faster HIGH-I loss is established.",
            "MDEs use pilot moments and a Normal approximation; no exact joint power or scientific effect margin has been approved.",
        ])


if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    if args.out.exists(): p.error("refuse overwrite")
    result=review(json.loads(SOURCE.read_text()),json.loads(OLD_SOURCE.read_text()))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
