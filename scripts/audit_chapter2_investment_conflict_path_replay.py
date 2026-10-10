"""Replay all original 384 investment-only pilots and audit realized conflict exposure.

Reuses EVERY exposed pilot visitor and demographic RNG ID, with no new
population paths or confirmatory outcomes. Rebuilds the original 384 per-path
results and requires their exact canonical JSON sha256. Under native genomic
investment expression, checks actual mixed-genotype F/P/S selection and
all-individual group viable-seed responses ONLY at N in {6,7,8,9}.
Each plant's local finite W derivative uses its own genetic state; no assumed
monomorphic source β label is assigned automatically to a dynamic trajectory.
"""
from __future__ import annotations

from dataclasses import replace
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np

from scripts.audit_chapter2_beta_gamma_seed_map import ledger_stats
from scripts.audit_chapter2_investment_commons_pilot_power import (
    BUDGETS,CAPS,PILOT_SEEDS,POLICIES,VISITOR_REGIMES,contract as original_contract,
    initial_genotypes, config, visitors, expressed_genome, demographic_streams,
)
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.population import advance

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"data/design/chapter2_investment_conflict_path_replay_20261010.json"
STATUS="EXPOSED_PILOT_EXACT_PATH_REPLAY_AND_ACTUAL_MIXED_GENOTYPE_WINDOW_AUDIT"
ORIGINAL_384_PATH_SHA256="0f39b237ecfd115fff34de9dad8090d2a7fdf89f54af39a821016bc3a0a0d0a6"
WINDOW=(6,7,8,9)
H=.005
DEADBAND=.02


def contract():
    b=DESIGN.read_bytes()
    d=json.loads(b)
    if (d.get("status")!="RETROSPECTIVE_SOURCE_LOCKED_PILOT_REPLAY_NO_NEW_INDEPENDENT_ECOLOGICAL_HISTORIES"
            or d["previous_raw_json_sha256"]!="3f528fcbe7585b6c4a5e713780d7260201630e7f8d4c752c6b5f65d1e1f5a459"
            or d["cohort"]["seeds_first"]!=9701201
            or d["cohort"]["seeds_last"]!=9701216
            or d["cohort"]["n_paths"]!=384
            or d["dynamic_conflict"]["structural_conflict_window_N"]!=list(WINDOW)
            or d["dynamic_conflict"]["actual_beta_deadband"]!=DEADBAND
            or d["dynamic_conflict"]["actual_gamma_deadband"]!=DEADBAND):
        raise ValueError("original-exposed path-replay protocol changed")
    return d,hashlib.sha256(b).hexdigest()


def investment_perturb(state,j,delta):
    a=np.array(state.alleles,copy=True)
    a[j,1,:]+=delta
    if np.min(a)<0 or np.max(a)>1:
        raise AssertionError("investment central finite step crosses phenotype support")
    return replace(state,alleles=a)


def actual_mixed_window(state,visitor,cfg):
    """Full native standing-variation genetic and nonfocal ledger at N=6..9."""
    n=len(state.ids)
    if n not in WINDOW:
        raise ValueError("actual mixed-genotype diagnostic only for N6..9")
    p=state.alleles.copy();m=p.copy()
    p[:,1,:]+=H;m[:,1,:]-=H
    collective_plus=ledger_stats(replace(state,alleles=p),visitor,cfg,48)
    collective_minus=ledger_stats(replace(state,alleles=m),visitor,cfg,48)
    gamma=float((np.log(collective_plus["total"])-
                 np.log(collective_minus["total"]))/(2*H))
    beta=[]
    outside=[]
    for j in range(n):
        plus=ledger_stats(investment_perturb(state,j,+H),visitor,cfg,48)
        minus=ledger_stats(investment_perturb(state,j,-H),visitor,cfg,48)
        b=float((np.log(plus["W"][j])-np.log(minus["W"][j]))/(2*H))
        other_plus=plus["total"]-plus["F"][j]-plus["S"][j]
        other_minus=minus["total"]-minus["F"][j]-minus["S"][j]
        ext=float((other_plus-other_minus)/(2*H))
        beta.append(b);outside.append(ext)
    negative=sum(x< -DEADBAND for x in beta)
    positive=sum(x>DEADBAND for x in beta)
    unresolved=n-negative-positive
    return {
        "gamma_collective_log_seed":gamma,
        "gamma_positive":bool(gamma>DEADBAND),
        "gamma_negative":bool(gamma<-DEADBAND),
        "focal_beta_negative_count":negative,
        "focal_beta_positive_count":positive,
        "focal_beta_unresolved_count":unresolved,
        "focal_beta_median":float(np.median(beta)),
        "positive_nonneighbor_externality_focal_count":sum(v>1e-8 for v in outside),
        "negative_nonneighbor_externality_focal_count":sum(v< -1e-8 for v in outside),
        "nonfocal_effect_median":float(np.median(outside)),
        "mixed_genotype_majority_conflict":bool(
            gamma>DEADBAND and negative*2>=n),
        "not_rare_mutant_and_not_genetic_time_series_selection":True,
    }


def replay_path(d,founder,h,seed,regime,K,budget,policy,*,diagnose):
    if (policy not in POLICIES or K not in CAPS or budget not in BUDGETS
            or regime not in VISITOR_REGIMES):
        raise ValueError("not an original pilot arm")
    cfg=config(d,K,budget)
    current=founder
    target=float(founder.alleles[:,1,:].mean())
    streams=demographic_streams(seed)
    source_ledger0=None;t1_state_sha=None
    n20=0;mean20=None;first_extinction=None
    years=[]
    for t in range(80):
        n=len(current.ids)
        present=bool(n)
        external=None
        if present and diagnose and n in WINDOW:
            external=actual_mixed_window(current,h.visitors[t],cfg)
        years.append({
            "t":t,"N":n,
            "investment_allele_mean_if_alive":(
                float(current.alleles[:,1,:].mean()) if present else None),
            "investment_allele_variance_if_alive":(
                float(current.alleles[:,1,:].var()) if present else None),
            "visitor_type_count":len(h.visitors[t].ids),
            "structural_N6_to9":bool(n in WINDOW),
            "actual_native_mixed_genotype_window":external,
        })
        if present:
            if not (np.all(current.alleles[:,0,:]==.2)
                    and np.all(current.alleles[:,2,:]==.35)):
                raise AssertionError("noninvestment genomic variants appeared")
            ledger=reproduce_kb(
                expressed_genome(current,target,policy),
                h.visitors[t],cfg,background_denominator_capacity=48)
            if t==0:
                source_ledger0=float(ledger.outcross.sum()+ledger.self_viable.sum())
            current,_=advance(current,ledger,h.seed_candidates[t],cfg,streams,year=t)
            if len(current.ids)==0 and first_extinction is None:
                first_extinction=t+1
        if t==0:
            t1_state_sha=hashlib.sha256(
                current.alleles.tobytes()+current.ids.tobytes()).hexdigest()
        if t==19:
            n20=len(current.ids)
            mean20=float(current.alleles[:,1,:].mean()) if len(current.ids) else None
    original={
        "K":K,"allele_mean20_if_alive":mean20,
        "allele_mean80_if_alive":(
            float(current.alleles[:,1,:].mean()) if len(current.ids) else None),
        "budget":budget,"first_extinction":first_extinction,
        "initial_expected_viable_seeds":source_ledger0,
        "investment_gene_copy_mass80":(
            float(current.alleles[:,1,:].sum()) if len(current.ids) else 0.),
        "n20":n20,"n80":int(len(current.ids)),
        "occupied20":int(n20>0),"occupied80":int(len(current.ids)>0),
        "policy":policy,"regime":regime,"seed":int(seed),
        "t1_genomic_state_sha256":t1_state_sha,
    }
    n_window=sum(y["structural_N6_to9"] for y in years)
    mixed=[y["actual_native_mixed_genotype_window"] for y in years
           if y["actual_native_mixed_genotype_window"] is not None]
    if policy=="native" and len(mixed)!=n_window:
        raise AssertionError("missing original mixed-state gradient in N-window")
    if policy!="native" and mixed:
        raise AssertionError("control unexpectedly re-evaluated native selection")
    first_below=next((y["t"] for y in years if 0<y["N"]<=5),None)
    first_above=next((y["t"] for y in years if y["N"]>=10),None)
    max_streak=streak=0
    for y in years:
        if y["structural_N6_to9"]:
            streak+=1
            max_streak=max(max_streak,streak)
        else:
            streak=0
    return {
        "original_pilot_result":original,
        "source_conflict_window_years":n_window,
        "max_consecutive_window_years":max_streak,
        "ever_in_N6_to9":bool(n_window),
        "first_t_at_N1_to5":first_below,
        "first_t_at_N10_or_above":first_above,
        "actually_mixed_genotype_conflict_years":sum(
            z["mixed_genotype_majority_conflict"] for z in mixed),
        "mixed_genotype_assessed_years":len(mixed),
        "mixed_genotype_gamma_positive_years":sum(
            z["gamma_positive"] for z in mixed),
        "mixed_genotype_externality_positive_focals":sum(
            z["positive_nonneighbor_externality_focal_count"] for z in mixed),
        "mixed_genotype_total_assessed_focals":sum(
            y["N"] for y in years if y["actual_native_mixed_genotype_window"] is not None),
        "complete_native_or_centered_80_annual_states":years,
    }


def summarize(paths):
    index={(z["original_pilot_result"]["seed"],
            z["original_pilot_result"]["regime"],
            z["original_pilot_result"]["K"],
            z["original_pilot_result"]["budget"],
            z["original_pilot_result"]["policy"]):z for z in paths}
    if len(index)!=384:
        raise AssertionError("original piloted paths duplicated/missing")
    result=[]
    for regime in VISITOR_REGIMES:
        for K in CAPS:
            for budget in BUDGETS:
                native=[index[(seed,regime,K,budget,"native")] for seed in PILOT_SEEDS]
                centered=[index[(seed,regime,K,budget,"baseline_centered")] for seed in PILOT_SEEDS]
                result.append({
                    "visitor_regime":regime,"K":K,"budget":budget,
                    "source_independent_pilot_history_units":16,
                    "native_H80_occupied":sum(
                        x["original_pilot_result"]["occupied80"] for x in native),
                    "centered_H80_occupied":sum(
                        x["original_pilot_result"]["occupied80"] for x in centered),
                    "native_ever_N6_to9":sum(x["ever_in_N6_to9"] for x in native),
                    "native_annual_pre_repro_years_N6_to9":sum(
                        x["source_conflict_window_years"] for x in native),
                    "centered_annual_pre_repro_years_N6_to9":sum(
                        x["source_conflict_window_years"] for x in centered),
                    "native_actual_genotype_majority_conflict_years":sum(
                        x["actually_mixed_genotype_conflict_years"] for x in native),
                    "native_actual_mixed_gamma_positive_years":sum(
                        x["mixed_genotype_gamma_positive_years"] for x in native),
                    "native_mixed_gradients_n_years":sum(
                        x["mixed_genotype_assessed_years"] for x in native),
                    "native_actual_pollen_externality_positive_focals":sum(
                        x["mixed_genotype_externality_positive_focals"] for x in native),
                    "native_actual_pollen_externality_focal_total":sum(
                        x["mixed_genotype_total_assessed_focals"] for x in native),
                    "native_first_pass_N10_or_above":sum(
                        x["first_t_at_N10_or_above"] is not None for x in native),
                    "native_first_pass_N1_to5":sum(
                        x["first_t_at_N1_to5"] is not None for x in native),
                    "native_max_window_streak_across_16":max(
                        x["max_consecutive_window_years"] for x in native),
                })
    return result


def run_all():
    d,digest=contract()
    original,_=original_contract()
    founder,_=initial_genotypes(original)
    paths=[]
    for seed in PILOT_SEEDS:
        for regime in VISITOR_REGIMES:
            hist=visitors(original,seed,regime)
            for K in CAPS:
                for budget in BUDGETS:
                    for policy in POLICIES:
                        paths.append(replay_path(
                            original,founder,hist,seed,regime,K,budget,
                            policy,diagnose=(policy=="native")))
    if len(paths)!=384:
        raise AssertionError("original pilot not fully replayed")
    original_results=[x["original_pilot_result"] for x in paths]
    encoded=json.dumps(original_results,sort_keys=True,
                       separators=(",",":"),allow_nan=False).encode()
    original_digest=hashlib.sha256(encoded).hexdigest()
    if original_digest!=ORIGINAL_384_PATH_SHA256:
        raise AssertionError(
            f"original exact 384-pilot path parity failed: {original_digest}")
    return {
        "status":STATUS,
        "design_sha256":digest,
        "original_pathwise_canonical_sha256":original_digest,
        "source_reproduction_native_replay_exact":True,
        "new_ecological_histories":0,
        "n_original_paths":len(paths),
        "n_native_mixed_population_reproductive_gradients":sum(
            x["mixed_genotype_assessed_years"] for x in paths),
        "complete_12_environment_cell_summary":summarize(paths),
        "all_384_source_paths_and_80_year_demographic_and_genetic_trace":paths,
        "limitations":[
            "All visitor histories and founder genomes are the originally EXPOSED 16-path engineering pilot, no independent confirmation.",
            "The original 384 path outputs match a source SHA256 derived from the archived raw JSON, not just final occupancy counts.",
            "Mixed-genotype focal derivatives are entire observed-parent finite expression contrasts at N6..9, not mutation invasion fitness/realized genomic allele frequency changes.",
            "Annual observations within trajectories and N≤9 focal adults are NOT independent demographic/ecological replicates.",
            "Only native expression histories have actual selected source beta/gamma diagnostics, centered histories retain census trace for paired demographic comparison.",
            "N6..9 monomorphic source conflict window is NOT automatically equivalent to a majority actual-genotype conflict under dynamically changing visitors.",
            "No evolutionary suicide or natural island floral decline inferred from descriptive path occupancy."
        ],
    }


def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--out",type=Path,required=True)
    args=a.parse_args()
    r=run_all()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(r,indent=2,sort_keys=True,allow_nan=False)+"\n",
                        encoding="utf-8")
    print(json.dumps({
        "status":r["status"],
        "original_parity":r["original_pathwise_canonical_sha256"],
        "mixed_gradient_years":r["n_native_mixed_population_reproductive_gradients"],
        "summary":r["complete_12_environment_cell_summary"],
    },sort_keys=True))


if __name__=="__main__":
    main()
