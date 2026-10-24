"""Original R2 lowest-I allele transmission, with exact native parentage.

Uses only original t30 diploid genomes and deterministic one-year reproductive
ledger under two activities. The original t80 source outcomes are independently
SHA-verified by the parent #635 auditor; no NEW biological future is generated.
Retrospective 22 source cells from 11 original founders. This audit is not an
experiment estimating allele-frequency thresholds, drift fractions, or natural
island selection.
"""
from __future__ import annotations

from collections import Counter
import json
import numpy as np

from scripts.audit_chapter2_r2_original_I_accessibility_20261024 import (
    replay_original_native, STRONG
)
from scripts.audit_chapter2_r2_shock_genome_expected_I_20261023 import (
    load_roster, expected_genetic_I
)
from scripts.chapter2_pollen_baseline_factorial_20261019 import (
    admit, founders, streams, visitors, config, step, fingerprint
)
from scripts.model3_island.reproduction import reproduce

STATUS = "R2_ORIGINAL_LOWEST_I_EXPECTED_ALLELIC_TRANSMISSION_NOT_NEW_BIOLOGY"
EPS = 1e-12


def expected_alleles(state, ledger) -> dict:
    """Expected numerical-I allele frequencies among newborn resident offspring.

    For a given I allele value, each outcross offspring has expected allele
    fraction (h_father+h_mother)/2, where h_i is the frequency of that allele
    among the parent's two homologs. Selfed offspring draw both homologs from
    the same parent and have expected fraction h_i. The original outcross
    matrix is [father,mother] and native self_viable is by maternal plant.

    This calculation assumes the ORIGINAL no-mutation, no-immigration source.
    It is conditional on current genome and positive viable resident offspring.
    """
    a=np.asarray(state.alleles[:,1,:],dtype=float)
    n=len(state.ids)
    O=np.asarray(ledger.outcross,dtype=float)
    S=np.asarray(ledger.self_viable,dtype=float)
    V=np.asarray(ledger.ovules,dtype=float)
    if (a.shape!=(n,2) or n!=48 or O.shape!=(n,n) or S.shape!=(n,)
            or V.shape!=(n,) or not np.isfinite(a).all()
            or not np.isfinite(O).all() or not np.isfinite(S).all()
            or (O<0).any() or (S<0).any() or np.any(a<0) or np.any(a>1)):
        raise AssertionError("invalid frozen original source genotype or parental ledger")
    total=float(O.sum()+S.sum())
    if total<=0 or not np.isfinite(total):
        raise AssertionError("invalid original source viable offspring total")
    parent_weights=0.5*O.sum(axis=0)+0.5*O.sum(axis=1)+S
    levels=np.unique(a)
    if len(levels)<2:
        raise AssertionError("original source I must segregate at treatment")
    freqs={}
    for allele in levels:
        fraction=(a==allele).mean(axis=1)
        p0=float(fraction.mean())
        pnext=float(np.dot(parent_weights,fraction)/total)
        # A second, ordered-parent computation does not share the weights code.
        independent=float(
            (O*((fraction[:,None]+fraction[None,:])/2)).sum()+
            np.dot(S,fraction)
        )/total
        if (not np.isclose(independent,pnext,atol=1e-13,rtol=0)
                or not 0<p0<1 or not 0<=pnext<=1):
            raise AssertionError("original parental-copy transmission inconsistent")
        freqs[str(float(allele))]={
            "allele_value":float(allele),
            "count_at_original_census30":int(np.count_nonzero(a==allele)),
            "frequency_at_original_census30":p0,
            "expected_frequency_in_resident_offspring":pnext,
            "expected_frequency_shift":pnext-p0,
        }
    if sum(x["count_at_original_census30"] for x in freqs.values())!=96:
        raise AssertionError("source allele count conservation failed")
    if not np.isclose(sum(x["expected_frequency_in_resident_offspring"]
                          for x in freqs.values()),1,atol=2e-13,rtol=0):
        raise AssertionError("expected Mendelian transmission failed to sum to one")
    from_alleles=float(sum(x["allele_value"]*x["expected_frequency_in_resident_offspring"]
                           for x in freqs.values()))
    source_shift, source_q, source_mean = expected_genetic_I(state,ledger)
    if not np.isclose(source_mean,from_alleles,atol=2e-13,rtol=0):
        raise AssertionError("source phenotypic I expectation differs from allele frequencies")
    return {
        "numerical_I_allele_frequencies":freqs,
        "expected_mean_offspring_I":from_alleles,
        "expected_offspring_I_shift":source_shift,
        "original_native_outcross_fraction":source_q,
        "expected_viable_resident_offspring_total":total,
    }


def replay() -> dict:
    d=admit()  # Original protocol/Model 3 native operator source SHA admission.
    if (d["status"]!="FROZEN_EXPLORATORY_MECHANISM_PILOT_NOT_INDEPENDENT_CONFIRMATION"
            or d["model"]["capacity"]!=48 or d["model"]["mutation_rate"]!=0
            or d["model"]["seed_immigration"]!=0
            or d["factorial"]["freeze_prefix_updates"]!=30):
        raise AssertionError("original R2 source model assumptions changed")
    parent=replay_original_native()  # validates both original t80 full-genome SHAs.
    if (parent["n_strict_AM_fixed_I_polymorphic_strong_history_source_cells"]!=22
            or parent["n_decline_fixed_to_lowest_I_allele_present_at_shock"]!=20
            or parent["n_distinct_founder_seeds"]!=11):
        raise AssertionError("wrong original source outcome cohort")
    original={(x["initial_A"],x["original_founder_seed"],x["nested_demographic_repeat"]):x
              for x in parent["rows"]}
    roster=[r for r in load_roster() if r["baseline"]==STRONG]
    if len(roster)!=22:
        raise AssertionError("original SHA-authenticated 22 t30 genomes unavailable")
    out=[]
    for cell in roster:
        key=(cell["initial_A"],cell["founder_seed"],cell["demographic_repeat"])
        if key not in original:
            raise AssertionError("source t30/t80 original roster mismatch")
        v=visitors(d,cell["baseline"])
        s=founders(d,cell["founder_seed"],cell["initial_A"])
        rng=streams(cell["founder_seed"],cell["demographic_repeat"])
        c=config(d,cell["baseline"],.4)
        for year in range(30):
            s,_=step(s,v,c,rng,year)
        if fingerprint(s)!=cell["prefix_sha"]:
            raise AssertionError("ORIGINAL t30 full genome mismatch")
        arms={}
        for name,activity in (("control",.4),("decline",.04)):
            cc=config(d,cell["baseline"],activity)
            arms[name]=expected_alleles(s,reproduce(s,v,cc))
        first=str(float(np.min(s.alleles[:,1,:])))
        if first not in arms["control"]["numerical_I_allele_frequencies"]:
            raise AssertionError("source t30 minimum I is missing")
        fc=arms["control"]["numerical_I_allele_frequencies"][first]
        fd=arms["decline"]["numerical_I_allele_frequencies"][first]
        delta_low=fd["expected_frequency_in_resident_offspring"]-fc["expected_frequency_in_resident_offspring"]
        delta_I=arms["decline"]["expected_offspring_I_shift"]-arms["control"]["expected_offspring_I_shift"]
        levels=np.unique(s.alleles[:,1,:])
        if len(levels)==2:
            independently=-delta_I/(float(levels[1])-float(levels[0]))
            if not np.isclose(delta_low,independently,atol=2e-13,rtol=0):
                raise AssertionError("two-allele I mean versus low allele frequency algebra failed")
        old=original[key]
        if (old["lowest_I_allele_count_out_of_96"]!=fd["count_at_original_census30"]
                or old["decline_terminal_fixed_I_value"] not in levels):
            raise AssertionError("source standing allele and observed endpoint disagree")
        out.append({
            "initial_A":key[0],
            "original_founder_seed":key[1],
            "nested_demographic_repeat":key[2],
            "original_census30_full_genome_sha256":cell["prefix_sha"],
            "original_I_numerical_allele_values":levels.tolist(),
            "lowest_I_allele_value":float(levels[0]),
            "lowest_I_count_at_shock":fd["count_at_original_census30"],
            "lowest_I_fraction_at_shock":fd["frequency_at_original_census30"],
            "initial_expected_lowest_I_fraction_control":fc["expected_frequency_in_resident_offspring"],
            "initial_expected_lowest_I_fraction_decline":fd["expected_frequency_in_resident_offspring"],
            "decline_minus_control_expected_lowest_I_fraction":delta_low,
            "source_lowest_I_allele_absolute_expected_shift_control":fc["expected_frequency_shift"],
            "source_lowest_I_allele_absolute_expected_shift_decline":fd["expected_frequency_shift"],
            "decline_minus_control_expected_mean_I_shift":delta_I,
            "original_decline_fixed_to_lowest_I":old["decline_fixed_to_lowest_accessible_I_value"],
            "original_decline_terminal_fixed_I":old["decline_terminal_fixed_I_value"],
            "allelic_expected_outcomes":arms,
        })
    if len(out)!=22 or len({x["original_founder_seed"] for x in out})!=11:
        raise AssertionError("original source 22/11 identity was not preserved")
    special={
        (0.3,810102,4):6,
        (0.5,810110,3):4,
    }
    seen=[]
    for r in out:
        k=(r["initial_A"],r["original_founder_seed"],r["nested_demographic_repeat"])
        if k in special:
            seen.append(k)
            if (r["lowest_I_count_at_shock"]!=special[k] or r["original_decline_fixed_to_lowest_I"]):
                raise AssertionError("original rare low-I allele loss exception changed")
    if set(seen)!=set(special):
        raise AssertionError("two original expected-transmission exceptions missing")
    lowdiff=np.asarray([x["decline_minus_control_expected_lowest_I_fraction"] for x in out],dtype=float)
    controlshift=np.asarray([x["source_lowest_I_allele_absolute_expected_shift_control"] for x in out],dtype=float)
    declineshift=np.asarray([x["source_lowest_I_allele_absolute_expected_shift_decline"] for x in out],dtype=float)
    return {
        "status":STATUS,
        "source_original_experiment_run":39233450099,
        "source_original_cases":384,
        "source_matched_original_future_pairs":192,
        "source_shock_genomes_exactly_hash_verified":22,
        "source_terminal_genomes_also_hash_verified_in_parent_replay":44,
        "n_original_founders":11,
        "n_orig_t30_genomes_biallelic_I":int(sum(len(x["original_I_numerical_allele_values"])==2 for x in out)),
        "n_orig_t30_genomes_triallelic_I":int(sum(len(x["original_I_numerical_allele_values"])==3 for x in out)),
        "n_lowest_I_parentage_treatment_positive":int((lowdiff>EPS).sum()),
        "n_lowest_I_parentage_treatment_negative":int((lowdiff<-EPS).sum()),
        "n_lowest_I_parentage_treatment_near_zero":int((np.abs(lowdiff)<=EPS).sum()),
        "n_lowest_I_absolute_expectation_decline_positive":int((declineshift>EPS).sum()),
        "n_lowest_I_absolute_expectation_decline_negative":int((declineshift<-EPS).sum()),
        "n_lowest_I_absolute_expectation_decline_near_zero":int((np.abs(declineshift)<=EPS).sum()),
        "mean_lowest_I_frequency_expected_treatment_contrast":float(lowdiff.mean()),
        "mean_lowest_I_frequency_absolute_shift_control":float(controlshift.mean()),
        "mean_lowest_I_frequency_absolute_shift_decline":float(declineshift.mean()),
        "special_low_copy_exceptions":[x for x in out if (
            x["initial_A"],x["original_founder_seed"],x["nested_demographic_repeat"]) in special],
        "rows":out,
        "claim_rank":"POST_OUTCOME_ORIGINAL_PARENTAGE_EXPECTATION_NO_CAUSAL_FIXATION_PROBABILITY",
        "new_biological_population_futures":0,
        "new_preregistered_experiments":0,
        "not_identified":[
            "Independent selective allele frequency advantage or subsequent fixation probability in new source populations",
            "Causal selection versus stochastic drift share over finite 50-generation futures",
            "Prospective 4/96 or 6/96 low-I allele-frequency threshold",
            "Natural island generality or field pollinator selection gradient",
        ]
    }


if __name__=="__main__":
    print(json.dumps(replay(),sort_keys=True,indent=2,ensure_ascii=False))
