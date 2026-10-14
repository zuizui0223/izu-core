"""Prospective technical source/draw QA using ORIGINAL founder t0 diploids.

NOT a registered scientific experiment: 64 synthetic re-assignments conditional
on only two old source phenotype arrays. No future RNG seeds, reproduction,
population.advance/inherit, response events, or ecological extrapolation.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import numpy as np

from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    ORIGINAL_BLOB, DRAW_SALT, SOURCE_SALT,
    original_fixture, source_state, manipulate_homologs, matched_draw,
)

ROOT=Path(__file__).resolve().parents[1]
CONTRACT=ROOT / "data/design/chapter2_source_assignment_candidate_contract_20261014.json"
SALT="izu-core-pr512-founder-input-QA-nonbiological-v1"
BLOCKS=("main","confirmation")
SEEDS_PER_BLOCK=32
OVERLAPS=(0,3,6,12)
FOUNDERS=(2,8,24,48)
DELTA=Fraction(1,20)


def qa_seed(block:str,replicate:int,axis:str)->int:
    if (block not in BLOCKS or type(replicate) is not int
            or not 0<=replicate<SEEDS_PER_BLOCK or axis not in ("source","draw","recipient")):
        raise ValueError("Unregistered technical source-assignment seed key")
    raw=f"{SALT}|{block}|r{replicate:02d}|{axis}".encode()
    return int.from_bytes(sha256(raw).digest()[:7],"big")


def support_flags(state)->tuple[bool,bool]:
    """Necessary mutation-free population allele-bound support; no evolution."""
    a=state.alleles
    n=len(state.ids)
    if n not in FOUNDERS or a.shape!=(n,3,2):
        raise ValueError("Unregistered original founder counterfactual")
    realized_mean=np.array(a.mean(axis=2))
    # Convert exact binary source values to rationals before inequality decisions.
    def raw_fraction(v):
        return Fraction.from_float(float(v))
    aveA=sum(map(raw_fraction,realized_mean[:,2]))/n
    aveI=sum(map(raw_fraction,realized_mean[:,1]))/n
    maxA=max(map(raw_fraction,a[:,2,:].flat))
    minI=min(map(raw_fraction,a[:,1,:].flat))
    return maxA >= aveA + DELTA, minI <= aveI - DELTA


def audit()->dict:
    source=original_fixture()
    roster=[]
    rows=[]
    all_seeds=set()
    case_ids=set()
    for block in BLOCKS:
        original=source_state(source,block)
        for rep in range(SEEDS_PER_BLOCK):
            assigned={axis:qa_seed(block,rep,axis)
                      for axis in ("source","draw","recipient")}
            for seed in assigned.values():
                if seed in all_seeds:
                    raise AssertionError("Technical source/draw seed collision")
                all_seeds.add(seed)
            roster.append({"founder_background":block,"assignment_index":rep,
                           "source_assignment_seed":assigned["source"],
                           "founder_draw_seed":assigned["draw"],
                           "recipient_projection_seed":assigned["recipient"],
                           "biological_future_seed":None})
            fixed_A_ids=None
            base_draws={}
            for m in OVERLAPS:
                variant=manipulate_homologs(
                    original,block=block,overlap=m,source_seed=assigned["source"])
                A_ids,I_ids=set(variant.A_ids),set(variant.I_ids)
                if fixed_A_ids is not None and A_ids!=fixed_A_ids:
                    raise AssertionError("A assignment not paired across I overlap changes")
                fixed_A_ids=A_ids
                for n in FOUNDERS:
                    old_sel,assigned_sel=matched_draw(
                        original,variant.state,n,draw_seed=assigned["draw"])
                    selected=set(int(i) for i in assigned_sel.ids)
                    if n in base_draws and selected!=base_draws[n]:
                        raise AssertionError("Founder draws differ across co-carriage treatments")
                    base_draws[n]=selected
                    a_count=len(A_ids&selected)
                    i_count=len(I_ids&selected)
                    a_support,i_support=support_flags(assigned_sel)
                    if bool(a_count)!=a_support:
                        raise AssertionError("A source access support inconsistent with constructed A-only allele width")
                    key=f"{block}:{rep:02d}:m{m}:n{n}"
                    if key in case_ids:raise AssertionError("Duplicate candidate input")
                    case_ids.add(key)
                    rows.append({
                        "key":key,"founder_background":block,"assignment_index":rep,
                        "A_I_co_carriers_in_full48":m,"sample_n":n,
                        "selected_ids":sorted(selected),
                        "A_symmetric_heterozygotes_retained":a_count,
                        "I_symmetric_heterozygotes_retained":i_count,
                        "A_mutation_free_necessary_allele_support":a_support,
                        "I_mutation_free_necessary_allele_support":i_support,
                    })
            for n in FOUNDERS[:-1]:
                next_n=FOUNDERS[FOUNDERS.index(n)+1]
                if not base_draws[n].issubset(base_draws[next_n]):
                    raise AssertionError("Paired founder number comparison is not nested")

    if len(roster)!=2*SEEDS_PER_BLOCK or len(rows)!=2*SEEDS_PER_BLOCK*len(OVERLAPS)*len(FOUNDERS):
        raise AssertionError("Technical randomisation candidate coverage not complete")

    aggregated=[]
    for block in BLOCKS:
        for m in OVERLAPS:
            for n in FOUNDERS:
                group=[v for v in rows if v["founder_background"]==block and
                       v["A_I_co_carriers_in_full48"]==m and v["sample_n"]==n]
                if len(group)!=SEEDS_PER_BLOCK:raise AssertionError("Missing randomisations")
                aggregated.append({
                    "background":block,"m":m,"n":n,"draws":len(group),
                    "no_A_symmetric_heterozygotes":sum(x["A_symmetric_heterozygotes_retained"]==0 for x in group),
                    "no_I_symmetric_heterozygotes":sum(x["I_symmetric_heterozygotes_retained"]==0 for x in group),
                    "I_necessary_allele_support":sum(x["I_mutation_free_necessary_allele_support"] for x in group),
                    "I_no_symmetric_heterozygotes_but_support":
                        sum(x["I_symmetric_heterozygotes_retained"]==0 and
                            x["I_mutation_free_necessary_allele_support"] for x in group),
                    "I_symmetric_heterozygotes_but_no_support":
                        sum(x["I_symmetric_heterozygotes_retained"]>0 and
                            not x["I_mutation_free_necessary_allele_support"] for x in group),
                })
    payload=json.dumps(rows,sort_keys=True,separators=(",",":")).encode()
    return {
        "schema":"chapter2_founder_candidate_source_assignment_QA_v1",
        "status":"NO_EXECUTION_TECHNICAL_SOURCE_ASSIGNMENT_ONLY",
        "original_t0_fixture_git_blob":ORIGINAL_BLOB,
        "derived_seed_salt":SALT,
        "biological_simulation_authorized":False,
        "independent_natural_founder_pools":0,
        "fixed_original_founder_backgrounds":2,
        "synthetic_randomisations_per_background":SEEDS_PER_BLOCK,
        "nested_source_draw_seed_groups":len(roster),
        "n_source_assignment_m_x_n_cases":len(rows),
        "n_biological_evolutionary_histories":0,
        "inference_level":"technical synthetic reassignments conditional on two original founder backgrounds; NOT independent archipelagos",
        "technical_source_draw_receipts":roster,
        "observed_synthetic_source_assignment_summary":aggregated,
        "case_level_technical_digest_sha256":sha256(payload).hexdigest(),
        "all_cases_not_stored":"Case records reconstructed deterministically from source fixture and technical seeds; no response outcome exposed",
        "limitations":[
            "A/I carrier flags refer to synthetic homologs, not a historical or natural genome",
            "I mutation-free allele support is not equivalent to carrying I heterozygotes",
            "Actual future Model3 biological RNG streams remain NULL/unauthorized",
            "64 technical randomisations are nested within two original phenotype backgrounds",
            "Founding n changes census and genotype; fixed-N48 homolog projection is another artificial intervention",
        ],
    }


def check_committed()->dict:
    contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
    if (contract.get("status")!="UNAPPROVED_NO_BIOLOGY_TECHNICAL_RANDOMISATION_ONLY"
            or contract.get("original_t0_fixture_git_blob")!=ORIGINAL_BLOB
            or contract.get("derived_seed_salt")!=SALT
            or contract.get("technical_assignments_per_founder_background")!=SEEDS_PER_BLOCK
            or contract.get("founder_backgrounds")!=list(BLOCKS)
            or contract.get("source_co_carriage")!=list(OVERLAPS)
            or contract.get("founder_draw_sizes")!=list(FOUNDERS)
            or contract.get("future_history_seed_status")!="NULL_NOT_AUTHORIZED"
            or contract.get("allow_pilot_execution") is not False
            or contract.get("author_run_approval") is not False
            or contract.get("no_biological_history_generated") is not True):
        raise ValueError("Technical source/draw contract was modified or promoted to a biological execution")
    result=audit()
    if (result["case_level_technical_digest_sha256"]!=
            contract["expected_case_level_technical_digest_sha256"]
            or result["nested_source_draw_seed_groups"]!=64
            or result["n_source_assignment_m_x_n_cases"]!=1024):
        raise ValueError("Source assignment or paired founding-row identities drifted")
    mismatch=contract["observed_technical_mismatch_counts_not_evolution"]
    rows=result["observed_synthetic_source_assignment_summary"]
    left=sum(r["I_no_symmetric_heterozygotes_but_support"] for r in rows)
    right=sum(r["I_symmetric_heterozygotes_but_no_support"] for r in rows)
    if (left!=mismatch["I_carrier_absent_but_mutation_free_support_present"]
            or right!=mismatch["I_carrier_present_but_mutation_free_support_absent"]):
        raise ValueError("Original-source I carrier/support mismatch count changed")
    return result


if __name__=="__main__":
    print(json.dumps(check_committed(),indent=2,sort_keys=True))
