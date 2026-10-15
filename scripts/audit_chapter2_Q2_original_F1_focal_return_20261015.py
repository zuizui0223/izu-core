"""Q2 native fixed-resident F1 sign-phenotype return screen; NO population futures.

Hypothetical first-offspring genotype phenotypes already shown accessible in
the original-I-preserving/ARTIFICIAL-A m6 confirmation source are introduced
as ONE adult replacing an identical-phenotype original resident. For each of
the three native original visitor contexts and all three Mendelian M outcomes,
compare four signed A/I trait phenotypes using EXACT original Model3
reproduction.reproduce. The estimand is immediate expected parental genome
contribution W=(F+P)/2+S in a held-fixed N=48 resident community.
This is NOT observed offspring fitness, conditional F1 recruitment, an
evolutionary selection coefficient, sustained six-class order or persistence.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
from hashlib import sha1
import json
from pathlib import Path

import numpy as np

from scripts.model3_island import reproduction, types
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    original_fixture, source_state, original_context, archive_return_gate, CONTEXTS,
)
from scripts.audit_chapter2_original_confirmation_m0_m6_F1_20261015 import (
    source_carriers,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SIGNED = ROOT / "docs/audits/chapter2_Q2_original_F1_signed_tail_negative_control_20261015.json"
OUTPUT = ROOT / "docs/audits/chapter2_Q2_original_F1_focal_return_filter_20261015.json"
SOURCE_SIGNED_BLOB = "46f62a81d36802b2e26f29d70725ef7ae7a0ebc4"
FOCAL_ID = 1
M_SUPPORT = ((.5,.25),(.5625,.5),(.625,.25))
SIGN_VALUES = {
    "A_up_I_down": (.5625,.375),
    "A_up_I_up": (.5625,.625),
    "A_down_I_down": (.4375,.375),
    "A_down_I_up": (.4375,.625),
}
GENOTYPE_PROJECTION_NS = 91_000_000_000_000
TOL = 1e-10


def _git_blob(raw: bytes) -> str:
    return sha1(b"blob "+str(len(raw)).encode("ascii")+b"\0"+raw).hexdigest()


def read_original_signed_access() -> dict:
    raw=SOURCE_SIGNED.read_bytes()
    if _git_blob(raw)!=SOURCE_SIGNED_BLOB:
        raise ValueError("Original signed four-quadrant F1 readout Git blob changed")
    item=json.loads(raw)
    if (item.get("status")!="SOURCE_AUTHENTICATED_NATIVE_T0_SIGN_NULL_NO_NEW_BIOLOGY"
            or item.get("base_source_json_git_blob")
                !="27077b320532f2585ec598140593485f254d563c"
            or item.get("new_biological_trajectories")!=0
            or item.get("new_offspring_births")!=0
            or [row["context"] for row in item.get("contexts",[])]!=list(CONTEXTS)):
        raise ValueError("Original signed access admission/genealogy drift")
    for row in item["contexts"]:
        p=row["m6_signed_events"]
        if set(p)!=set(SIGN_VALUES) or p["A_up_I_down"]<=0:
            raise ValueError("Original F1 sign access is incomplete")
        if any(abs(x-p["A_up_I_down"])>1e-12 for x in p.values()):
            raise ValueError("Original F1 four-signed access ceased to be equal")
        if any(abs(x)>1e-12 for x in row["m0_signed_events"].values()):
            raise ValueError("Original m0 F1 signed access ceased to be zero")
    return item


def original_M_access(original: types.PlantState) -> dict:
    if len(original.ids)!=48:
        raise ValueError("Original original source F0 census changed")
    carrier_ids=source_carriers(original)["m6"]
    if tuple(carrier_ids)!=(1,3,6,9,11,14):
        raise ValueError("Original I-heterozygote carrier source changed")
    # EACH original selected A/I double carrier has M homologs .5 and .625.
    # Given BOTH parents are in this set for either A sign ±.05,
    # every one-child M phenotype follows .5/.5625/.625 with 1/4,1/2,1/4,
    # irrespective of selected parent IDs and of A/I sign.
    for idx in carrier_ids:
        x=original.alleles[idx]
        if (not np.array_equal(np.sort(x[0]),[.5,.625])
                or not np.array_equal(np.sort(x[1]),[.375,.625])
                or not np.array_equal(np.sort(x[2]),[.4375,.5625])):
            raise ValueError("Original source Mendelian M/I/A carriers changed")
    trait=original.alleles.mean(axis=2)
    if not np.array_equal(trait[np.asarray(carrier_ids,dtype=np.int64)],
                          np.tile(np.array([.5625,.5,.5]),(6,1))):
        raise ValueError("Original source selected adults have distinct phenotype")
    return {
        "m6_original_carrier_ids":list(carrier_ids),
        "M_F1_conditional_support":[{"M":m,"probability":w} for m,w in M_SUPPORT],
        "M_F1_same_for_all_four_signed_A_I_events":True,
    }


def focal_state(original: types.PlantState, m:float, A:float, I:float,
                *, focal_id:int=FOCAL_ID) -> types.PlantState:
    if (type(focal_id) is not int or not 0<=focal_id<48
            or not any(m==v for v,_ in M_SUPPORT)
            or not any((A,I)==v for v in SIGN_VALUES.values())):
        raise ValueError("Only original F1 four-tail phenotype support admitted")
    base_traits=original.alleles.mean(axis=2)
    if not np.array_equal(base_traits[focal_id],[.5625,.5,.5]):
        raise ValueError("Focal slot must be an authentic original same-phenotype resident")
    alleles=original.alleles.copy()
    # Exact possible first-child diploid combinations on the original F1 grid.
    # This is a potential adult genotype inserted statically in place of one
    # F0 resident, not a realized offspring or an additional 49th adult.
    if m==.5:
        alleles[focal_id,0,:]=[.5,.5]
    elif m==.5625:
        alleles[focal_id,0,:]=[.5,.625]
    else:
        alleles[focal_id,0,:]=[.625,.625]
    alleles[focal_id,1,:]=I
    alleles[focal_id,2,:]=A
    origins=original.allele_origin.copy()
    origins[focal_id,:,:]=(
        GENOTYPE_PROJECTION_NS+focal_id*10+np.arange(6).reshape(3,2))
    state=replace(original,alleles=alleles,allele_origin=origins)
    if (len(state.ids)!=48 or
            not np.array_equal(state.alleles.mean(axis=2)[focal_id],[m,I,A])
            or not np.array_equal(state.alleles[np.arange(48)!=focal_id],
                                  original.alleles[np.arange(48)!=focal_id])
            or not np.array_equal(state.ids,original.ids)
            or not np.array_equal(state.birth_years,original.birth_years)
            or not np.array_equal(state.mutation_flags,original.mutation_flags)):
        raise ValueError("Focal substitution affected controls or genetic identity")
    return state


def one_focal_W(ledger:types.Ledger,focal_id:int=FOCAL_ID) -> dict:
    if not isinstance(ledger,types.Ledger):
        raise ValueError("Original Model3 ledger required")
    F=float(ledger.outcross[:,focal_id].sum())
    P=float(ledger.outcross[focal_id,:].sum())
    S=float(ledger.self_viable[focal_id])
    W=(F+P)/2+S
    if not np.isfinite([F,P,S,W]).all() or min(F,P,S)<0:
        raise ValueError("Invalid expected parental-genome contribution")
    return {"female_outcross_F":F,"male_outcross_P":P,"viable_self_S":S,
            "parental_genome_W":W,
            "intrinsic_ovule_budget":float(ledger.ovules[focal_id])}


def audit() -> dict:
    signed=read_original_signed_access()
    fixture=original_fixture()  # Pins original F0 source and native biology.
    state=source_state(fixture,"confirmation")
    proven=original_M_access(state)
    if not np.array_equal(state.alleles.mean(axis=2)[FOCAL_ID],[.5625,.5,.5]):
        raise ValueError("Original focal adult phenotype changed")
    rows=[]
    for context in CONTEXTS:
        cfg,vis=original_context(fixture,"confirmation",context)
        archive_return_gate(fixture,state,"confirmation",context,cfg,vis)
        baseline=one_focal_W(reproduction.reproduce(state,vis,cfg))
        for m,weight in M_SUPPORT:
            scores={}
            for sign,(A,I) in SIGN_VALUES.items():
                projection=focal_state(state,m,A,I)
                score=one_focal_W(reproduction.reproduce(projection,vis,cfg))
                if context==0:
                    # Exact no-pollinator independent formula from the native
                    # delayed-selfing, 50% inbreeding-depression model.
                    no_pollen=(cfg.ovule_budget
                        *np.exp(-cfg.investment_cost*I*I-cfg.assurance_cost*A*A)
                        *A*(1-cfg.depression))
                    if (abs(score["parental_genome_W"]-no_pollen)>TOL
                            or abs(score["female_outcross_F"])>TOL
                            or abs(score["male_outcross_P"])>TOL):
                        raise ValueError("No-visitor Model3 return formula drifted")
                scores[sign]=score
            best=max(scores,key=lambda z:scores[z]["parental_genome_W"])
            second=max(scores[z]["parental_genome_W"]
                       for z in scores if z!="A_up_I_down")
            gap=scores["A_up_I_down"]["parental_genome_W"]-second
            if best!="A_up_I_down" or gap<=TOL:
                raise ValueError("Predicted static maximum absent: "+str((context,m,scores)))
            rows.append({
                "context":int(context),
                "focal_original_id_replaced":FOCAL_ID,
                "one_possible_F1_M":m,
                "M_probability_conditional_on_any_signed_double_tail":weight,
                "frozen_resident_focal_baseline_W":baseline["parental_genome_W"],
                "static_focal_expected_returns_by_sign":scores,
                "highest_focal_W_sign":best,
                "top_W_minus_runner_up":gap,
                "pollinator_community_held_at_original_t0":True,
                "other_47_original_adult_phenotypes_unchanged":True,
            })
    summary=[]
    for context in CONTEXTS:
        cell=[x for x in rows if x["context"]==context]
        weighted={}
        for sign in SIGN_VALUES:
            weighted[sign]=sum(
                row["M_probability_conditional_on_any_signed_double_tail"]*
                row["static_focal_expected_returns_by_sign"][sign]["parental_genome_W"]
                for row in cell)
        if abs(sum(row["M_probability_conditional_on_any_signed_double_tail"]
                   for row in cell)-1)>TOL:
            raise ValueError("Conditional F1 matching M distribution incomplete")
        if max(weighted,key=weighted.get)!="A_up_I_down":
            raise ValueError("F1 averaged static return sign ordering did not hold")
        sign_chance=next(x for x in signed["contexts"] if x["context"]==context)
        summary.append({
            "context":int(context),
            "equal_first_child_access_per_signed_class_m6":
                float(sign_chance["m6_signed_events"]["A_up_I_down"]),
            "source_supported_conditional_M_averaged_focal_W_by_sign":weighted,
            "max_expected_return_sign":"A_up_I_down",
            "W_A_up_I_down_minus_second_highest":(
                weighted["A_up_I_down"]-max(v for k,v in weighted.items()
                                            if k!="A_up_I_down")),
            "same_initial_sign_access_but_different_hypothetical_adult_returns":True,
        })
    return {
        "schema":"chapter2_q2_original_f1_native_focal_static_return_filter_v1",
        "status":"AUTHENTICATED_T0_FOCAL_ONE_ADULT_RETURN_DIAGNOSTIC_NO_EVOLUTION",
        "original_confirmation_genotype_from_authenticated_fixture":True,
        "original_f0_biology_operator":"scripts/model3_island/reproduction.py::reproduce",
        "source_signed_four_tail_git_blob":SOURCE_SIGNED_BLOB,
        "independent_genetic_source_backgrounds":1,
        "matched_source_t0_adult_count":48,
        "only_one_original_adult_phenotype_replaced_at_a_time":True,
        "focal_phenotype_is_exact_possible_first_child_not_observed_adult":True,
        "focal_expected_return_estimand":"W=(maternal_outcross_F+paternal_outcross_P)/2 + viable_self_S",
        "m6_signed_A_I_tail_probability_equal_across_four_signs":True,
        "M_mendelian_support":proven,
        "four_signs":list(SIGN_VALUES),
        "context_mean_W_summary":summary,
        "native_four_corner_rows":rows,
        "n_contexts":len(CONTEXTS),
        "n_M_levels":len(M_SUPPORT),
        "n_focal_trait_comparisons":len(rows)*len(SIGN_VALUES),
        "new_offspring_births":0,
        "new_population_advance_calls":0,
        "new_evolutionary_histories":0,
        "claim_ceiling":[
            "This is an instantaneous one-adult-in-original-48 background expected parental-genome-return screen; it is not observed genotype frequency change or selection coefficient.",
            "A high/low A/I corner is accessible under artificially constructed m6 F1, with a conditional 3-point M support, not a naturally documented new adult.",
            "Each potential genotype replaces a focal site; other 47 adult phenotypes and the original visitor community are fixed but pollen transfer and density recipient totals are recomputed.",
            "Differences in static reproductive W do not quantify actual F1 recruitment, stochastic inheritance, density feedback, later selection, 20-census ordering or Q4 survival.",
            "The native result is conditional on one original confirmation source and its three source-authenticated artificial visitor contexts; no source-level sampling uncertainty.",
            "Artificial A-homolog reconstruction (42 original A-heterozygotes reset per arm) is a separate source intervention, not original natural I mutation renewal or a natural island measurement.",
            "The four equal Mendelian first-offspring access probabilities do NOT imply four equal fixed-state return values; the latter still does not prove long-term adaptive fixation.",
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check",action="store_true")
    p.add_argument("--out",type=Path,default=None)
    args=p.parse_args()
    result=audit()
    if args.check:
        saved=json.loads(OUTPUT.read_text(encoding="utf-8"))
        if saved["schema"]!=result["schema"] or saved["status"]!=result["status"]:
            raise SystemExit("Original native return screening contract mismatch")
        if (saved["n_focal_trait_comparisons"]!=36
                or saved["new_evolutionary_histories"]!=0
                or len(saved["native_four_corner_rows"])!=len(result["native_four_corner_rows"])):
            raise SystemExit("Original static return full grid is incomplete")
        for a,b in zip(saved["native_four_corner_rows"],result["native_four_corner_rows"]):
            if (a["context"],a["one_possible_F1_M"])!=(b["context"],b["one_possible_F1_M"]):
                raise SystemExit("Original signed source rows have been rearranged")
            for sign in SIGN_VALUES:
                for stat in ("parental_genome_W","female_outcross_F",
                             "male_outcross_P","viable_self_S","intrinsic_ovule_budget"):
                    if abs(a["static_focal_expected_returns_by_sign"][sign][stat]-
                           b["static_focal_expected_returns_by_sign"][sign][stat])>TOL:
                        raise SystemExit("Original native source W diagnostic changed")
        print("PASS: all original native focal W return contributions reproduce")
    elif args.out:
        if args.out==OUTPUT and OUTPUT.exists():
            raise FileExistsError("Do not rewrite an admitted source record")
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n",
                            encoding="utf-8")
    else:
        print(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))


if __name__=="__main__":
    main()
