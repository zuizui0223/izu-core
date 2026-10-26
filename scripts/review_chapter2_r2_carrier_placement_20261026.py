"""R2 design-only: equal current phenotype, unequal latent allele transmission.

Construct *artificial* diploid PlantState templates, not naturally evolved
populations and not a new biological campaign. Original Model3 reproduce()
is read-only and deterministic. No RNG, advance(), new histories, offspring
sampling, artificial adaptation claims, or authorization/dispatch.

Goal: falsify an assumption that initial low-I copy frequency plus matched
adult phenotypes/current pollen ledger suffices to identify an allele's
immediate expected transmission. Carrier placement across different
paternal/maternal/self reproductive backgrounds remains an independent axis.
"""
from __future__ import annotations

import json
import numpy as np

from scripts.chapter2_pollen_baseline_factorial_20261019 import admit, config, visitors
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import PlantState
from scripts.audit_chapter2_r2_low_I_allele_transmission_20261024 import expected_alleles
from scripts.review_chapter2_r2_independent_feasibility_20261025 import (
    checked_sources, diploid_phenotype_preserving_I_recode,
)

STATUS="R2_DESIGN_ONLY_SAME_PHENOTYPE_SAME_LEDGER_DIFFERENT_LOW_I_CARRIER_RETURN"
N=48
RECODABLE=24
N_CARRIERS=8
RECODE_FROM=(.5,.5)
RECODE_TO=(.25,.75)
LEDGER_FIELDS=(
    "outcross","self_raw","self_viable","ovules","exported",
    "delivered","lost","maternal","paternal",
)


def artificial_source_state() -> PlantState:
    """Labelled theoretical genomes, NOT inherited or realized founder data."""
    a=np.full((N,3,2),.5,dtype=float)
    a[RECODABLE:,1,:]=.75
    for idx in range(RECODABLE):
        # Both genotype-specific reproductive pathways and pollen matching
        # vary across adult carriers. The *same* adult genotype positions
        # are held fixed across the two proposed recoding allocations.
        m=.05+.90*idx/(RECODABLE-1)
        assurance=.15+.70*((idx*7)%RECODABLE)/(RECODABLE-1)
        a[idx,0,:]=m
        a[idx,2,:]=assurance
    return PlantState(
        alleles=a,
        allele_origin=np.arange(N*3*2,dtype=np.int64).reshape((N,3,2)),
        mutation_flags=np.zeros((N,3,2),dtype=bool),
        ids=np.arange(N,dtype=np.int64),
        birth_years=np.zeros(N,dtype=np.int64),
    )


def recode_I_only(source:PlantState, selected:list[int]) -> PlantState:
    if (len(selected)!=N_CARRIERS or len(set(selected))!=N_CARRIERS
            or any(type(v) is not int or not 0<=v<RECODABLE for v in selected)):
        raise ValueError("need exactly eight different eligible synthetic carrier IDs")
    a=source.alleles.copy()
    for i in selected:
        if tuple(a[i,1,:])!=RECODE_FROM:
            raise AssertionError("cannot rewrite non-homozygous I carrier")
        a[i,1,:]=RECODE_TO
    changed=PlantState(
        alleles=a,
        allele_origin=source.allele_origin,
        mutation_flags=source.mutation_flags,
        ids=source.ids,birth_years=source.birth_years,
    )
    if (not np.array_equal(changed.alleles.mean(axis=2),source.alleles.mean(axis=2))
            or not np.array_equal(changed.alleles[:,0,:],source.alleles[:,0,:])
            or not np.array_equal(changed.alleles[:,2,:],source.alleles[:,2,:])
            or not np.array_equal(changed.ids,source.ids)
            or not np.array_equal(changed.birth_years,source.birth_years)):
        raise AssertionError("synthetic latent recode changed expressed M/I/A or population")
    return changed


def expected_gene_weight(ledger) -> np.ndarray:
    """Expected share in newborn allele pool attributable to each parent."""
    O=np.asarray(ledger.outcross)
    S=np.asarray(ledger.self_viable)
    if O.shape!=(N,N) or S.shape!=(N,):
        raise AssertionError("original synthetic native parentage has wrong dimensions")
    w=.5*O.sum(axis=0)+.5*O.sum(axis=1)+S
    if not (np.isfinite(w).all() and (w>=0).all() and float(w.sum())>0):
        raise AssertionError("invalid source genetic-parental return")
    if not np.isclose(w.sum(),O.sum()+S.sum(),atol=1e-12,rtol=0):
        raise AssertionError("paternal+maternal+self gene return not conserved")
    return w


def review()->dict:
    provenance=checked_sources() # Old formal run_gate must remain all false.
    d=admit() # SHA-bound native original source contract and operators.
    math=diploid_phenotype_preserving_I_recode(N_CARRIERS)
    if (d["status"]!="FROZEN_EXPLORATORY_MECHANISM_PILOT_NOT_INDEPENDENT_CONFIRMATION"
            or math["new_population_or_offspring_updates"]!=0
            or math["changed_I_numeric_allele_copy_counts"]!={"0.25":8,"0.5":32,"0.75":56}):
        raise AssertionError("source or hypothetical carrier math changed")
    original=artificial_source_state()
    first=reproduce(original,visitors(d,"strong_baseline_limitation"),
                    config(d,"strong_baseline_limitation",.4))
    weights=expected_gene_weight(first)
    order=np.argsort(weights[:RECODABLE],kind="stable")
    low=[int(x) for x in order[:N_CARRIERS]]
    high=[int(x) for x in order[-N_CARRIERS:]]
    if (set(high)&set(low) or
            not sum(weights[high])>sum(weights[low])+1e-10):
        raise AssertionError("synthetic carrier parental backgrounds are not distinct")
    placements={
        "high_current_parental_return":recode_I_only(original,high),
        "low_current_parental_return":recode_I_only(original,low),
    }
    if len({tuple(p.alleles[:,1,:].flatten()) for p in placements.values()})!=2:
        raise AssertionError("carrier positions not distinct despite identical allele counts")
    all_settings=[]
    for baseline in ("strong_baseline_limitation","weak_baseline_limitation"):
        visitor_state=visitors(d,baseline)
        for activity in (.4,.04):
            cfg=config(d,baseline,activity)
            base_ledger=reproduce(original,visitor_state,cfg)
            w=expected_gene_weight(base_ledger)
            row={
                "baseline":baseline,
                "original_model_external_activity":activity,
                "original_model_current_expected_parental_return_total":float(w.sum()),
                "recode_allocations":{},
            }
            for name,state in placements.items():
                ledger=reproduce(state,visitor_state,cfg)
                if any(not np.array_equal(getattr(base_ledger,f),getattr(ledger,f))
                       for f in LEDGER_FIELDS):
                    raise AssertionError("artificial recoding altered current native reproduction ledger")
                a=expected_alleles(state,ledger)
                low_freq=a["numerical_I_allele_frequencies"]["0.25"]
                if (low_freq["count_at_original_census30"]!=N_CARRIERS
                        or not np.isclose(low_freq["frequency_at_original_census30"],
                                          N_CARRIERS/(2*N),atol=1e-14,rtol=0)):
                    raise AssertionError("carrier placements altered low-I allele frequency")
                positions=high if name.startswith("high") else low
                independently=float(.5*w[positions].sum()/w.sum())
                if not np.isclose(independently,
                                  low_freq["expected_frequency_in_resident_offspring"],
                                  atol=2e-13,rtol=0):
                    raise AssertionError("source Mendelian carrier-fitness association did not match")
                row["recode_allocations"][name]={
                    "synthetic_carrier_indices":positions,
                    "low_I_allele_copies":N_CARRIERS,
                    "starting_low_I_fraction":low_freq["frequency_at_original_census30"],
                    "expected_low_I_fraction_in_newborns":
                        low_freq["expected_frequency_in_resident_offspring"],
                    "expected_low_I_allele_frequency_shift":
                        low_freq["expected_frequency_shift"],
                    "mathematically_expected_from_weighted_gene_return":independently,
                    "current_parentage_ledger_equals_original_byte_for_byte":True,
                }
            x=row["recode_allocations"]
            delta=(x["high_current_parental_return"]["expected_low_I_fraction_in_newborns"]-
                   x["low_current_parental_return"]["expected_low_I_fraction_in_newborns"])
            row["difference_in_low_I_newborn_fraction_from_carrier_placement"]=float(delta)
            row["original_current_reproductive_ledger_exactly_identical_across_placements"]=True
            all_settings.append(row)
    ref=next(z for z in all_settings if z["baseline"]=="strong_baseline_limitation"
             and z["original_model_external_activity"]==.4)
    if not ref["difference_in_low_I_newborn_fraction_from_carrier_placement"]>1e-12:
        raise AssertionError("native causal arithmetic carrier-placement counterexample missing")
    return {
        "status":STATUS,
        "source_provenance":provenance,
        "original_native_model_source_contract_sha":d.get("source_contract_sha256"),
        "population":"ARTIFICIAL_48_DIPLOID_LABELLED_TEMPLATE_NOT_AUTHENTIC_FOUNDER",
        "parental_carrier_ranking_fixed_from":"strong_baseline_limitation activity=0.4",
        "carrier_indices_at_higher_native_genetic_return":high,
        "carrier_indices_at_lower_native_genetic_return":low,
        "all_adult_current_expressed_M_I_A_identical":True,
        "same_current_native_reproductive_ledger_in_each_source_environment":True,
        "same_low_I_copy_count_and_allelic_value_variance":True,
        "current_low_I_copy_count_per_96":N_CARRIERS,
        "current_mean_I_phenotype":.625,
        "current_phenotypic_I_variance":.015625,
        "native_static_reproduction_settings_checked":all_settings,
        "source_version_identifiability_limit":"Current M/I/A expression and immediate ecological return held constant, but correlations of low-I carrier labels with genetic backgrounds and current parental contributions differ; neither ancestry nor later evolution is identified.",
        "new_biological_population_updates":0,
        "new_offspring_draws":0,
        "new_random_seed_reservations":0,
        "prospective_founder_histories":0,
        "not_registered_not_authorized":True,
        "should_dispatch_actions":False,
        "natural_island_causal_claim":False,
    }


if __name__=="__main__":
    print(json.dumps(review(),sort_keys=True,indent=2,ensure_ascii=False,allow_nan=False))
