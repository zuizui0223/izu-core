"""Offline, source-locked admission of Chapter 2 Q2 supplementary S29.

No biological evolution, offspring sampling, release upload, DOI action or
new model parameter. Exact Git blob pins + cross-family numerical consistency
protect a post hoc source-only mechanistic explanation from claim promotion.
"""
from __future__ import annotations

from hashlib import sha1
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCES={
    "original": ("data/design/chapter2_clock_original_t0_typed_fixture_20261013.json",
                 "4b529cce12bc44e06d43a22b10c325a52bbd967b"),
    "f1": ("docs/audits/chapter2_Q2_original_confirmation_m0_m6_F1_20261015.json",
           "27077b320532f2585ec598140593485f254d563c"),
    "sign": ("docs/audits/chapter2_Q2_original_F1_signed_tail_negative_control_20261015.json",
             "46f62a81d36802b2e26f29d70725ef7ae7a0ebc4"),
    "returns": ("docs/audits/chapter2_Q2_original_F1_focal_return_filter_20261015.json",
                "91600a87c47ba4f1cadc90f3ac7de0c480fa6583"),
}
SI="docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md"
PAPER="docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md"
EVENTS=("A_up_I_down","A_up_I_up","A_down_I_down","A_down_I_up")
CONTEXTS=(0,3,4)
EPS=1e-12


def git_blob(raw:bytes)->str:
    return sha1(b"blob "+str(len(raw)).encode("ascii")+b"\0"+raw).hexdigest()


def signed_section(si:str)->str:
    title="## S29. Original-I-constrained F1 genetic access versus conditional reproductive returns"
    if si.count(title)!=1:
        raise ValueError("S29 absent or duplicated")
    section=si.split(title,1)[1]
    if "\n## S" in section:
        section=section.split("\n## S",1)[0]
    return section


def verify_f1_bridge(source:dict, f1:dict, sign:dict, returns:dict, si:str, paper:str)->dict:
    section=signed_section(si)
    if (source.get("original_biological_commit")!="328548612e93469fcc8663f24548530a57399b9a"
            or source.get("new_biological_histories")!=0
            or sorted(source.get("original_founders",{}))!=["confirmation","main"]):
        raise ValueError("historical two-founder typed source drift")
    if (f1.get("status")!="ORIGINAL_I_UNMODIFIED_F1_ANALYTICAL_ONLY_NOT_EVOLUTION"
            or f1.get("original_t0_fixture_git_blob")!=SOURCES["original"][1]
            or f1.get("source_founder_background")!="confirmation"
            or f1.get("independent_source_genome_realizations")!=1
            or f1.get("original_A_heterozygote_adults")!=48
            or f1.get("original_A_heterozygosity_reset_in_each_arm")!=42
            or f1.get("original_I_allele_copies_preserved") is not True
            or f1.get("arm_m0_vs_m6_I_A_co_carrier_counts")!=[0,6]
            or any(f1.get(k)!=0 for k in ("new_biological_born_offspring",
                                         "new_Model3_future_updates",
                                         "new_sustained_6class_response_histories"))):
        raise ValueError("F1 original-I control/gate not retained")
    if (sign.get("status")!="SOURCE_AUTHENTICATED_NATIVE_T0_SIGN_NULL_NO_NEW_BIOLOGY"
            or sign.get("base_source_json_git_blob")!=SOURCES["f1"][1]
            or sign.get("new_biological_trajectories")!=0
            or sign.get("new_offspring_births")!=0):
        raise ValueError("F1 four-sign null source changed")
    if (returns.get("status")!="AUTHENTICATED_T0_FOCAL_ONE_ADULT_RETURN_DIAGNOSTIC_NO_EVOLUTION"
            or returns.get("source_signed_four_tail_git_blob")!=SOURCES["sign"][1]
            or returns.get("independent_genetic_source_backgrounds")!=1
            or returns.get("n_focal_trait_comparisons")!=36
            or returns.get("n_contexts")!=3 or returns.get("n_M_levels")!=3
            or returns.get("only_one_original_adult_phenotype_replaced_at_a_time") is not True
            or any(returns.get(k)!=0 for k in ("new_offspring_births",
                                               "new_population_advance_calls",
                                               "new_evolutionary_histories"))):
        raise ValueError("F1 fixed-background W source no longer valid")
    fr=f1.get("contexts",[]);sr=sign.get("contexts",[])
    wr=returns.get("context_mean_W_summary",[])
    allrows=returns.get("native_four_corner_rows",[])
    if (list(x.get("context") for x in fr)!=list(CONTEXTS)
            or list(x.get("context") for x in sr)!=list(CONTEXTS)
            or list(x.get("context") for x in wr)!=list(CONTEXTS)
            or len(allrows)!=9):
        raise ValueError("original visitor contexts missing/reassigned")
    for a,b,c in zip(fr,sr,wr):
        ctx=a["context"]
        if (a["entire_F1_A_marginal_max_bin_error"]>EPS
                or a["entire_F1_I_marginal_max_bin_error"]>EPS
                or abs(a["F1_joint_A_I_total_variation"]-
                       b["one_child_joint_A_I_TV"])>EPS):
            raise ValueError("matched one-trait marginals or F1 joint probability drift")
        p=b["m6_signed_events"]
        if set(p)!=set(EVENTS) or set(b["m0_signed_events"])!=set(EVENTS):
            raise ValueError("four signed F1 classes missing")
        if any(abs(b["m0_signed_events"][event])>EPS for event in EVENTS):
            raise ValueError("original m0 F1 double-tail probabilities not zero")
        if not 0<p["A_up_I_down"]<=1 or any(
                abs(v-p["A_up_I_down"])>EPS for v in p.values()):
            raise ValueError("original equal-sign Mendelian F1 opportunity unsupported")
        if (abs(a["P_one_child_Aup_Itdown_relative_to_original_founder_mean"]["m6"]-
                p["A_up_I_down"])>EPS
                or abs(c["equal_first_child_access_per_signed_class_m6"]-
                       p["A_up_I_down"])>EPS):
            raise ValueError("old positive-direction source intake disagrees")
        weighted=c["source_supported_conditional_M_averaged_focal_W_by_sign"]
        if set(weighted)!=set(EVENTS) or c["max_expected_return_sign"]!="A_up_I_down":
            raise ValueError("focal W four-sign source missing")
        rows=[r for r in allrows if r["context"]==ctx]
        if ([r["one_possible_F1_M"] for r in rows]!=[.5,.5625,.625]
                or [r["M_probability_conditional_on_any_signed_double_tail"]
                    for r in rows]!=[.25,.5,.25]):
            raise ValueError("conditional M inheritance support changed")
        for r in rows:
            if (r["highest_focal_W_sign"]!="A_up_I_down"
                    or r["focal_original_id_replaced"]!=1
                    or r["other_47_original_adult_phenotypes_unchanged"] is not True):
                raise ValueError("focal-original background not held")
            for event in EVENTS:
                w=r["static_focal_expected_returns_by_sign"][event]
                calc=(w["female_outcross_F"]+w["male_outcross_P"])/2+w["viable_self_S"]
                if abs(calc-w["parental_genome_W"])>EPS:
                    raise ValueError("native source W=F/2+P/2+S fails")
        for event in EVENTS:
            val=sum(r["M_probability_conditional_on_any_signed_double_tail"]*
                    r["static_focal_expected_returns_by_sign"][event]["parental_genome_W"]
                    for r in rows)
            if abs(val-weighted[event])>EPS:
                raise ValueError("M-weighted static W not supported")
        runner=max(weighted[event] for event in EVENTS if event!="A_up_I_down")
        if (weighted["A_up_I_down"]<=runner
                or abs(c["W_A_up_I_down_minus_second_highest"]-
                       (weighted["A_up_I_down"]-runner))>EPS):
            raise ValueError("unsupported highest source W")
        # Require the text table to agree with numerical source to six decimals.
        item=next((l for l in section.splitlines()
                   if l.startswith("| "+str(ctx)+" ")),None)
        if item is None:
            raise ValueError("S29 source W row missing for context "+str(ctx))
        values=[v.strip().replace("*","") for v in item.strip("|").split("|")][1:]
        expected=[format(weighted[event],".6f") for event in EVENTS]
        expected.append("+"+format(c["W_A_up_I_down_minus_second_highest"],".6f"))
        if values!=expected:
            raise ValueError("S29 native W table disagrees with frozen source in context "+str(ctx))
    all_w=[r for r in allrows if r["highest_focal_W_sign"]=="A_up_I_down"]
    if len(all_w)!=9 or len({(r["context"],r["one_possible_F1_M"]) for r in allrows})!=9:
        raise ValueError("S29 nine-cell focal sign maximum not reproduced")
    if (not all(tag in section for tag in (
            "post hoc","42 of the 48","hypothetical adult",
            "The F1 access probabilities and static W scores must not be combined",
            "no new evolutionary simulation","source-conditioned"))
            or "S29" not in paper
            or "sustained evolutionary order" not in paper):
        raise ValueError("S29 interpretation and in-paper disclaimer incomplete")
    return {
        "status":"PASS_SOURCE_PINNED_S29_NO_NEW_BIOLOGY",
        "historical_original_genome_sources":2,
        "hypothetical_mechanism_source_backgrounds":1,
        "original_F1_visitor_contexts":list(CONTEXTS),
        "four_signed_F1_classes":list(EVENTS),
        "possible_M_values":3,
        "native_focal_W_analytical_cells":36,
        "native_Model3_population_updates":0,
        "new_DOI_deposit":False,
        "not_a_persistence_or_evolutionary_order_effect":True,
    }


def verify(root:Path=ROOT)->dict:
    sources={}
    for key,(path,sha) in SOURCES.items():
        raw=(root/path).read_bytes()
        if git_blob(raw)!=sha:
            raise ValueError("source Git blob drift: "+path)
        sources[key]=json.loads(raw)
    return verify_f1_bridge(sources["original"],sources["f1"],sources["sign"],
                            sources["returns"],(root/SI).read_text(encoding="utf-8"),
                            (root/PAPER).read_text(encoding="utf-8"))


if __name__=="__main__":
    print(json.dumps(verify(),indent=2,ensure_ascii=False))
