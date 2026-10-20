"""TECHNICAL-ONLY age-matched retention of original Model3 A-mutation tokens.

Replays precisely the same 16 original-source, 12-update, source-parity Q1
technical runs previously admitted; no NEW founder, visitor, population
trajectory, biological operator, or ecological inference. Event ID retention
is not fitness, physical A-I linkage, a true allele-sweep time, or a
causal mutation-birth-background effect.

Unlike naive terminal-12 retention, each event must be observed for
EXACTLY h updates to enter the fixed-age denominator. Later mutation
births are correctly excluded from longer h comparisons rather than
mistaken for higher-fitness A variants.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.audit_chapter2_ai_mutation_origin_20261020 import (
    STATUS as SOURCE_STATUS, audit_bounded
)

STATUS = "TECHNICAL_Q1_SOURCE_MUTATION_AGE_LANDMARKS_NOT_CAUSAL"
HORIZONS = (0,1,3,6)
A_SIGN = ("A_increased","A_decreased","A_no_change")
I_BACKGROUND = ("I_above_founder","I_below_founder","I_equal_founder")
TOL = 1e-12


def _label_A(x):
    return "A_increased" if x > 0 else "A_decreased" if x < 0 else "A_no_change"


def _label_I(x):
    return ("I_above_founder" if x > TOL else
            "I_below_founder" if x < -TOL else "I_equal_founder")


def _aggregate(records, horizon):
    eligible=[r for r in records if horizon in r["retention_by_age"]]
    survivor_count=sum(r["retention_by_age"][horizon]["present"] for r in eligible)
    copies=sum(r["retention_by_age"][horizon]["copies"] for r in eligible)
    return dict(
        birth_events_eligible=len(eligible),
        event_IDs_still_present=int(survivor_count),
        event_ID_retention_fraction=survivor_count/len(eligible) if eligible else None,
        original_A_token_copies=int(copies),
        mean_token_copies_per_eligible_birth=copies/len(eligible) if eligible else None,
        interpretation="fixed-age original A token survival; not cumulative mutation ancestry",
    )


def age_matched_source_readout():
    base=audit_bounded()
    if base["status"]!=SOURCE_STATUS or len(base["cases"])!=16:
        raise ValueError("source-Q1 parity cohort missing")
    rows=[]
    for case in base["cases"]:
        by_census={v["census"]:v for v in case["per_census"]}
        if set(by_census)!=set(range(13)):
            raise AssertionError("each technical case must contain 13 complete censuses")
        founder_I=by_census[0]["mean_I"]
        for event in case["raw_A_mutation_event_births"]:
            birth=event["mutation_census"]
            id_=event["event_id"]
            if not isinstance(id_,str) or not 1<=birth<=12:
                raise ValueError("malformed mutation origin event")
            cov=float(event["child_born_with_I_mean"]-founder_I)
            age_out={}
            loss_seen=False
            for h in range(13-birth):
                copy_count=int(by_census[birth+h]["A_mutation_token_copies_present"].get(id_,0))
                if h==0 and copy_count<1:
                    raise AssertionError("mutation token absent at original birth")
                if copy_count<0:
                    raise AssertionError("negative token census")
                if loss_seen and copy_count:
                    raise AssertionError("original A mutation token reappeared after loss")
                if copy_count==0:
                    loss_seen=True
                if h in HORIZONS:
                    age_out[h]=dict(present=int(copy_count>0),copies=copy_count)
            rows.append(dict(
                case_id=case["case_id"],
                founder_seed=case["founder_seed"],
                visitor_seed=case["visitor_seed"],
                visitor_arm=case["arm"], mating_setting=case["setting"],
                event_id=id_, birth_year=birth,
                possible_followup_updates=12-birth,
                A_sign=_label_A(event["mutation_effect"]),
                I_background=_label_I(cov),
                actual_I_birth_minus_source_mean=cov,
                same_birth_I_mutation=bool(event["same_birth_I_mutation"]),
                retention_by_age=age_out,
            ))
    if len(rows)!=base["source_mutation_births_total"] or len(rows)!=216:
        raise AssertionError("source mutation birth total changed")
    if any(r["same_birth_I_mutation"] for r in rows):
        raise AssertionError("original source had co-occurring I mutations: update documented null")
    out={}
    for sign in A_SIGN:
        for bg in I_BACKGROUND:
            group=[r for r in rows if r["A_sign"]==sign and r["I_background"]==bg]
            out[f"{sign}|{bg}"]={str(h):_aggregate(group,h) for h in HORIZONS}
    by_arm={}
    for arm in ("near","far"):
        arm_records=[r for r in rows if r["visitor_arm"]==arm]
        by_arm[arm]={str(h):_aggregate(arm_records,h) for h in HORIZONS}
    by_age={str(h):_aggregate(rows,h) for h in HORIZONS}
    # Eligibility must shrink monotonically as the exact observation window
    # grows; no replicate is counted as an independent biological population.
    for block in [by_age,*out.values(),*by_arm.values()]:
        eligible=[block[str(h)]["birth_events_eligible"] for h in HORIZONS]
        if eligible!=sorted(eligible,reverse=True):
            raise AssertionError("age landmark denominators do not nest")
    if by_age["0"]["birth_events_eligible"]!=216 or by_age["0"]["event_IDs_still_present"]!=216:
        raise AssertionError("all original mutation births must enter age zero")
    return dict(
        status=STATUS,
        source_status=SOURCE_STATUS,
        original_source_case_count=16,
        original_A_mutation_births=216,
        original_Q1_1000_update_campaign_was_not_rerun=True,
        original_native_genome_parity_verified=True,
        new_biological_mutations_or_trajectories_created=False,
        mutation_birth_year_max=12,
        exact_horizon_steps=list(HORIZONS),
        by_A_sign_and_actual_birth_I_background=out,
        by_visitor_arm=by_arm,
        all_births=by_age,
        no_iid_event_assumption=True,
        no_genetic_hitchhiking_confirmation=True,
        boundaries=[
            "Fixed-age retention corrects unequal opportunity for later-born A mutants to disappear before the shared terminal census.",
            "Even fixed-age groups mix different source founders, visitor histories, mating settings and background distributions.",
            "A positive/negative mutation effect is NOT an estimate of its selective fitness benefit.",
            "Token disappearance can be caused by demographic failure, Mendelian loss or a second A mutation replacing the latest-tag ID.",
            "The I genotype associated with one A-mutant homolog is a same-individual background, not a physically phased linked I allele.",
            "Direct I effects on reproduction remain active; no indirect-only counterfactual is identified.",
            "Original founder/visitor histories and random streams are duplicated among the 16 cases; events are not iid units.",
            "This readout cannot explain the original full 1000-update PR569 I-response sign variation.",
        ],
    )


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-readback",action="store_true")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    if not args.source_readback:
        parser.error("explicit --source-readback required; no new production available")
    s=json.dumps(age_matched_source_readout(),indent=2,sort_keys=True,
                 allow_nan=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        if args.output.exists():
            raise FileExistsError("original technical A-token age record must not be overwritten")
        args.output.write_text(s,encoding="utf8")
    else:
        print(s,end="")


if __name__=="__main__":
    main()
