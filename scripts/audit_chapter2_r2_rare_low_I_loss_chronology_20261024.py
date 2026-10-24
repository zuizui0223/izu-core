"""Read original rare low-I loss chronologies from source-exact Model 3 histories.

The parent exact-path audit reconstructs all 24 source t30 genomes and all 48
original t80 terminal full-genome SHA fingerprints; here we add ZERO new
independent futures. The two exceptions were identified *after* examining the
original 384-path exploratory cohort, and cannot validate a universal allele
frequency threshold or a causal selection-versus-drift contribution.

For two original biallelic I loci, allele frequencies can be reconstructed
without invented individual genotypes from the source genotype-means and
diploid census sizes: p_low = (I_high - mean(I))/(I_high - I_low).
Expected low-I frequency change = -source expected I shift / allele gap.
The realized residual difference is likewise the negative mean-I residual
divided by the allele gap. Source states and offspring ledger were separately
authenticated through the native SHA-locked Model 3 replay.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_r2_original_pathwise_I_accounting_20261024 import (
    replay_source_pathwise,
)

ROOT=Path(__file__).resolve().parents[1]
STANDING=ROOT/"docs/audits/CHAPTER2_R2_STANDING_I_ALLELE_ACCESS_20261024.json"
STATUS="PASS_ORIGINAL_R2_RARE_LOW_I_LOSS_WHILE_EXPECTED_TO_INCREASE_SOURCE_ONLY"
SOURCE_ZIP_SHA256="10bb8bdd52b53b32429e350c2f392ed2aeaa791683ede1d563ae6627c5ecb35e"
EXPECTED={
    (0.3,810102,4):{
        "low":0.50,"high":0.75,"initial_count":6,
        "terminal_high":0.75,
        "fixed_census":{"control":45,"decline":35},
        "n_segregating_source_generations":{"control":15,"decline":5},
        "cumulative_expected_low_frequency":{
            "control":0.006402198659706926,"decline":0.03167544147471579
        },
        "cumulative_realization_low_frequency":{
            "control":-0.06890219865970693,"decline":-0.0941754414747158
        },
    },
    (0.5,810110,3):{
        "low":0.25,"high":0.5,"initial_count":4,
        "terminal_high":0.5,
        "fixed_census":{"control":42,"decline":51},
        "n_segregating_source_generations":{"control":12,"decline":21},
        "cumulative_expected_low_frequency":{
            "control":0.004053188011446274,"decline":0.10083914506154934
        },
        "cumulative_realization_low_frequency":{
            "control":-0.045719854678113014,"decline":-0.14250581172821608
        },
    },
}


def annual_copy_accounting(y: dict, low: float, high: float) -> dict:
    """Source t->t+1 I allele copies and expected-versus-realized fractions."""
    gap=high-low
    if not (0<gap<=1 and 0<=low<high<=1):
        raise AssertionError("invalid source numerical allelic levels")
    n0,n1=y["N_before_reproduction"],y["N_after_recruitment"]
    values=y["current_I_allele_values"]
    if (not isinstance(n0,int) or not isinstance(n1,int)
            or not (1<=n0<=48 and 1<=n1<=48)
            or values not in ([low,high],[high])
            or y["year_from_original_founding"] not in range(30,80)):
        raise AssertionError("source yearly state does not support biallelic I readback")
    count_before=2*n0*(high-y["current_I"])/gap
    count_after=2*n1*(high-y["next_I"])/gap
    cb,ca=int(round(count_before)),int(round(count_after))
    if (abs(count_before-cb)>1e-9 or abs(count_after-ca)>1e-9
            or not (0<=cb<=2*n0 and 0<=ca<=2*n1)
            or (cb==0)!=(values==[high])):
        raise AssertionError("source biallelic diploid copy count not an exact integer")
    expected=-y["expected_I_shift_from_parentage"]/gap
    residual=-y["realization_residual"]/gap
    observed=-y["realized_I_shift"]/gap
    if (not all(np.isfinite(z) for z in (expected,residual,observed))
            or abs(expected+residual-observed)>1e-10
            or abs(observed-(ca/(2*n1)-cb/(2*n0)))>1e-10):
        raise AssertionError("original one-generation Mendelian I copy-flow does not telescope")
    return {
        "census_start":int(y["year_from_original_founding"]),
        "N_before":n0,"N_after":n1,
        "low_I_copies_before":cb,"low_I_copies_after":ca,
        "conditional_expected_low_I_fraction_shift":float(expected),
        "realized_low_I_fraction_shift":float(observed),
        "realization_residual_low_I_fraction":float(residual),
        "source_I_allele_support":values,
    }


def audit_original() -> dict:
    source=replay_source_pathwise() # SHA verifies all 24 original t30 and 48 original t80
    frozen=json.loads(STANDING.read_text(encoding="utf-8"))
    if (source["status"]!="SOURCE_EXACT_24_ORIGINAL_FUTURES_PATHWISE_EXPECTATION_RESIDUAL_NO_NEW_EXPERIMENT"
            or source["original_zip_sha256"]!=SOURCE_ZIP_SHA256
            or source["source_genomes_exactly_recovered_and_terminal_hashes_matched"]!=24
            or source["replayed_original_stored_future_updates"]!=2400
            or source["new_independent_biological_futures"]!=0
            or frozen["status"]!="PASS_ORIGINAL_R2_STANDING_I_ALLELES_EXPLORATORY_NOT_FREQUENCY_THRESHOLD"
            or frozen["source_zip_sha256"]!=SOURCE_ZIP_SHA256):
        raise AssertionError("original full-genotype/source-provenance verification changed")
    exceptions=frozen["exceptions"]
    if len(exceptions)!=2:
        raise AssertionError("the original two low-copy source exceptions changed")
    output=[]
    for entry in exceptions:
        key=(entry["initial_A"],entry["original_founder_seed"],entry["nested_demographic_repeat"])
        if key not in EXPECTED:
            raise AssertionError("unexpected original source rare-low-I exception identity")
        spec=EXPECTED[key]
        rows=[r for r in source["rows"] if (
            r["initial_A"],r["founder_seed"],r["demographic_repeat"])==key]
        if len(rows)!=1 or rows[0]["baseline"]!="strong_baseline_limitation":
            raise AssertionError("original pathwise source exception not found")
        r=rows[0]
        if (r["original_prefix_full_state_sha256"]!=entry["source_original_prefix_genome_sha256"]
                or entry["original_I_allele_values_at_shock"]!=[spec["low"],spec["high"]]
                or entry["original_I_allele_counts_at_shock"]!=[
                    spec["initial_count"],96-spec["initial_count"]]
                or entry["decline_terminal_fixed_I_value"]!=spec["terminal_high"]
                or r["paired_terminal_I_decline_minus_control"]!=0
                or abs(r["I_at_shock"]-
                       (spec["high"]-(spec["high"]-spec["low"])*spec["initial_count"]/96))>1e-13):
            raise AssertionError("original allele frequency/source checkpoint failed")
        arms={}
        for arm in ("control","decline"):
            original=r["arms"][arm]
            if abs(original["I_end"]-spec["terminal_high"])>1e-13:
                raise AssertionError("original terminal fixed I numerical allele differs")
            trace=[annual_copy_accounting(y,spec["low"],spec["high"])
                   for y in original["generations"]]
            if len(trace)!=50 or any(trace[i]["census_start"]!=30+i
                                     for i in range(50)):
                raise AssertionError("original year-by-year source chronology incomplete")
            if any(trace[i]["low_I_copies_after"]!=trace[i+1]["low_I_copies_before"]
                   for i in range(49)):
                raise AssertionError("original low-I diploid copy trajectories mismatch")
            if trace[0]["low_I_copies_before"]!=spec["initial_count"] or trace[-1]["low_I_copies_after"]!=0:
                raise AssertionError("source rare low-I allele did not start low and finish absent")
            zero_censuses=[t["census_start"] for t in trace if t["low_I_copies_before"]==0]
            if not zero_censuses:
                raise AssertionError("source fixed value reached only after sampled time")
            first_fixed=min(zero_censuses)
            segregating=[t for t in trace if t["low_I_copies_before"]>0]
            if (first_fixed!=spec["fixed_census"][arm]
                    or len(segregating)!=spec["n_segregating_source_generations"][arm]
                    or any(t["low_I_copies_after"]==0 for t in trace
                           if t["low_I_copies_before"]==0 and t["low_I_copies_after"]!=0)):
                raise AssertionError("original allele loss/fixation timing changed")
            if not all(t["conditional_expected_low_I_fraction_shift"]>1e-12
                       for t in segregating):
                raise AssertionError("source low-I allele was not positively expected while segregating")
            if not all(abs(t["conditional_expected_low_I_fraction_shift"])<=1e-12
                       for t in trace if t["low_I_copies_before"]==0):
                raise AssertionError("monomorphic original source has nonzero expected allele shift")
            expect=sum(t["conditional_expected_low_I_fraction_shift"] for t in trace)
            residual=sum(t["realization_residual_low_I_fraction"] for t in trace)
            realized=sum(t["realized_low_I_fraction_shift"] for t in trace)
            if (abs(expect-spec["cumulative_expected_low_frequency"][arm])>1e-12
                    or abs(residual-spec["cumulative_realization_low_frequency"][arm])>1e-12
                    or abs(expect+residual+spec["initial_count"]/96)>1e-12
                    or abs(realized+spec["initial_count"]/96)>1e-12):
                raise AssertionError("source expectation+realization allele accounting failed")
            arms[arm]={
                "source_original_terminal_full_state_sha256":
                    original["original_terminal_full_state_sha256"],
                "first_original_census_low_I_allele_lost":first_fixed,
                "n_censuses_I_segregating":len(segregating),
                "last_low_I_copy_count_before_loss":segregating[-1]["low_I_copies_before"],
                "n_segregating_years_expected_low_I_frequency_positive":len(segregating),
                "n_segregating_years_realized_low_I_fraction_increase":sum(
                    t["realized_low_I_fraction_shift"]>1e-12 for t in segregating),
                "n_segregating_years_realized_low_I_fraction_decrease":sum(
                    t["realized_low_I_fraction_shift"]<-1e-12 for t in segregating),
                "sum_original_path_expected_low_I_frequency_shift":expect,
                "sum_original_path_realization_low_I_fraction_residual":residual,
                "original_path_total_realized_low_I_fraction_shift":realized,
                "original_years_until_fixation":[
                    t for t in trace if t["census_start"]<first_fixed
                ],
            }
        output.append({
            "initial_A":key[0],"original_founder_seed":key[1],
            "demographic_repeat":key[2],
            "source_original_prefix_sha256":r["original_prefix_full_state_sha256"],
            "lowest_I_numerical_allele":spec["low"],
            "higher_I_numerical_allele":spec["high"],
            "original_low_I_copies_at_shock":spec["initial_count"],
            "total_allele_copies_at_shock":96,
            "arms":arms,
        })
    if len(output)!=2:
        raise AssertionError("original exception count unexpectedly changed")
    return {
        "status":STATUS,
        "source_original_actions_run_id":39233450099,
        "source_original_ZIP_sha256":SOURCE_ZIP_SHA256,
        "source_archived_pathwise_actions_run_id":40057254260,
        "source_genomes_SHA_verified_original_paired_cells":24,
        "n_original_strong_prior_pollen_limitation_exception_cells":2,
        "distinct_original_founders_in_exceptions":2,
        "original_fixed_AM_and_initially_segregating_I":True,
        "original_native_24_prefix_and_48_terminal_full_genome_checks":True,
        "new_independent_biological_futures":0,
        "new_preregistered_statistical_tests":0,
        "episodes":output,
        "claim_rank":"RETROSPECTIVE_EXACT_ORIGINAL_GENOME_PATHWISE_NO_CAUSAL_SELECTION_DRIFT_SHARE",
        "interpretation_boundary":"Within each original two-allele population, negative conditional I sorting at every polymorphic update corresponds to positive expected low-I transmission, but this does not guarantee positive realized change or eventual fixation. Conditional expectations follow already-realized genotypes. Realization residual is not uniquely neutral drift.",
    }


if __name__=="__main__":
    print(json.dumps(audit_original(),sort_keys=True,indent=2,ensure_ascii=False))
