"""R2 *non-executable* independent-source design and identifiability review.

Pure mathematical calculations and authenticated EXISTING audit/proposal readback.
Does not import Model 3 operators, reserve random seeds, run biological histories,
estimate empirical power, authorize Actions or upgrade exploratory outcomes.

Crossed-source variance components and the I-access population distribution are
hypothetical sensitivity assumptions; not observed variance estimates or a
pre-registered future experiment. Use source-independent axes, never treat
founder x visitor x demographic repetitions as independent islands.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from statistics import NormalDist

ROOT=Path(__file__).resolve().parents[1]
PROTOCOL=ROOT/"docs/protocols/CHAPTER2_R2_HISTORY_POLLEN_STATE_NEXT_STUDY_PROPOSAL_20261023.json"
PARENT=ROOT/"docs/audits/CHAPTER2_R2_LOWEST_I_PARENTAGE_RECEIPT_20261024.json"
CHRONOLOGY=ROOT/"docs/audits/CHAPTER2_R2_RARE_LOW_I_LOSS_CHRONOLOGY_20261024.json"
SOURCE_BLOBS={
    PROTOCOL.name:"5e7448b4b428879acbfdd2097044a2adc1839add",
    PARENT.name:"28fa9c8837796c7d0c20546cf6eab10b1c2df84c",
    CHRONOLOGY.name:"a490bf69d9a82ba1bcf7a39ba9d4c00f96c0862c",
}
STATUS="R2_DESIGN_PRECISION_AND_GENETIC_ACCESS_FEASIBILITY_REVIEW_HOLD"
N_PLANTS=48
N_DIPLOID=2*N_PLANTS
I_LEVELS=(.25,.50,.75)
# Hypothetical compensation states; neither the old 4/96, 6/96 or 16/96
# post-outcome cases are adopted as a new 'critical allele copy threshold'.
LOW_COPIES=(12,24,36)
FUTURE_AXES=(8,16,32,64)
REPEATS=(1,2,4)
HISTORICAL_REGIMES=2
ACCESS_ARMS=len(LOW_COPIES)
VISITOR_ACTIVITY_ARMS=2
PREFIX_UPDATES=30
FUTURE_UPDATES=50
CO_PRIMARY_COUNT=2
ALPHA=.05

# Component entries are assumption scenarios for a SOURCE-CELL matched
# contrast, not data-estimated variance or a confidence upper bound.
# Endpoint 1 D=loss_decline-loss_maintained is in [-1,1].
# Endpoint 2 DD=D_high_access-D_low_access is in [-2,2].
# No assumption that a current realized path gives unbiased components.
VARIANCE_SCENARIOS={
    "moderate_hypothetical":{
        "paired_low_I_loss_risk_difference":{"founder":.03,"visitor":.03,"interaction":.10,"nested":.20},
        "access_by_visitor_difference_of_differences":{"founder":.12,"visitor":.12,"interaction":.30,"nested":.80},
    },
    "adverse_hypothetical":{
        "paired_low_I_loss_risk_difference":{"founder":.12,"visitor":.12,"interaction":.20,"nested":.35},
        "access_by_visitor_difference_of_differences":{"founder":.35,"visitor":.35,"interaction":.60,"nested":1.50},
    },
}
ENDPOINT_RANGES={
    "paired_low_I_loss_risk_difference":(-1,1),
    "access_by_visitor_difference_of_differences":(-2,2),
}


def git_blob_sha(path:Path)->str:
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()


def checked_sources()->dict:
    if set(SOURCE_BLOBS)!={PROTOCOL.name,PARENT.name,CHRONOLOGY.name}:
        raise AssertionError("original source provenance set changed")
    for p in (PROTOCOL,PARENT,CHRONOLOGY):
        if git_blob_sha(p)!=SOURCE_BLOBS[p.name]:
            raise AssertionError("original source/prospective no-dispatch blob SHA changed: "+p.name)
    p=json.loads(PROTOCOL.read_text(encoding="utf8"))
    old=json.loads(PARENT.read_text(encoding="utf8"))
    loss=json.loads(CHRONOLOGY.read_text(encoding="utf8"))
    if (p["schema"]!="chapter2_r2_independent_history_service_identification_design_proposal_v1"
        or p["status"]!="DESIGN_ONLY_NOT_AUTHORIZED_NOT_PREREGISTERED"
        or any(value is not False for value in p["run_gate"].values())
        or p["independent_sampling"]["future_founder_source_count"] is not None
        or p["independent_sampling"]["future_visitor_history_source_count"] is not None
        or p["independent_sampling"]["sample_size_power_and_precision_contract"] is not None
        or p["independent_sampling"]["registered_minimum_biologically_meaningful_A_change"] is not None
        or not p["independent_sampling"]["source_axes_disjoint_from_older_exposed_campaigns"]
        or not p["independent_sampling"]["founder_visitors_crossed"]
        or not p["existing_evidence"]["old_384_outcomes_will_not_be_reused_for_new_confirmation"]
        or p["existing_evidence"]["fresh_founder_r2_four_setting_status"]!="INCONCLUSIVE"):
        raise AssertionError("existing R2 pending study cannot be marked authorized")
    q=old["native_one_year_parental_expected_low_I"]
    if (old["status"]!="SOURCE_SHA_VERIFIED_ORIGINAL_LOW_I_PARENTAGE_22_CELLS_NOT_NEW_BIOLOGY"
        or old["original_source_actions_run"]!=39233450099
        or old["distinct_original_founders"]!=11
        or q["n_absolute_source_frequency_shift_positive_decline"]!=22
        or q["original_source_lowest_I_fixed_in_decline_futures"]!=20
        or q["original_source_lower_I_lost_in_decline_futures"]!=2
        or loss["status"]!="PASS_ORIGINAL_R2_RARE_LOW_I_LOSS_WHILE_EXPECTED_TO_INCREASE_SOURCE_ONLY"
        or loss["n_original_founder_ids_in_exceptions"]!=2
        or loss["new_independent_population_updates"]!=0):
        raise AssertionError("original post-outcome R2 conditional source identity changed")
    return {"proposal_source_blob":SOURCE_BLOBS[PROTOCOL.name],
            "expected_parental_source_blob":SOURCE_BLOBS[PARENT.name],
            "rare_loss_source_blob":SOURCE_BLOBS[CHRONOLOGY.name],
            "original_384_source_run_id":39233450099,
            "old_source_founder_count":12,
            "old_22_selected_source_founder_count":11,
            "source_status":"ORIGINAL_384_POST_OUTCOME_EXPLORATORY_ONLY",
            "new_biological_experiment_authorized":False}


def biallelic_population_mean(low:float,high:float,low_copy_count:int)->float:
    if (not 0<=low<high<=1 or type(low_copy_count) is not int
            or not 0<=low_copy_count<=N_DIPLOID):
        raise ValueError("invalid no-mutation two-allele source frequencies")
    return (low*low_copy_count + high*(N_DIPLOID-low_copy_count))/N_DIPLOID


def compensated_triallelic_counts(low_copy_count:int)->dict:
    if type(low_copy_count) is not int or not 1<=low_copy_count<=N_DIPLOID//2:
        raise ValueError("two-sided mean-compensation needs feasible integer copies")
    lo,mid,hi=I_LEVELS
    copies=(low_copy_count,N_DIPLOID-2*low_copy_count,low_copy_count)
    mean=sum(a*n for a,n in zip(I_LEVELS,copies))/N_DIPLOID
    var=sum(n*(a-mean)**2 for a,n in zip(I_LEVELS,copies))/N_DIPLOID
    if (sum(copies)!=N_DIPLOID or abs(mean-mid)>1e-14
            or copies[1]<0 or not var>0):
        raise AssertionError("three-allele mean matching failed")
    return dict(low_I_copies=copies[0],middle_I_copies=copies[1],
                high_I_copies=copies[2],allele_copy_total=N_DIPLOID,
                expected_allele_mean=mean,allele_value_variance=var,
                low_I_fraction=copies[0]/N_DIPLOID,
                genetic_allocation_status="FREQUENCY_ONLY_NOT_A_DIPLOID_GENOTYPE_INTERVENTION")



def diploid_phenotype_preserving_I_recode(n_heterozygotes:int)->dict:
    """Exact artificial copy recoding at t30, with NO model population run.

    For 24 labeled plants with I=(.5,.5) and 24 with I=(.75,.75),
    exchange exactly k of the first 24 I pairs from (.5,.5) to
    (.25,.75). Their individual expressed I=(allele1+allele2)/2
    remains .5; all other original M/A loci and visitor environments
    are assumed held fixed. Only a mathematical artificial-allele
    specification is produced, not a valid reconstructed PlantState
    with independently authenticated inherited allele origins.
    """
    if type(n_heterozygotes) is not int or not 0<=n_heterozygotes<=24:
        raise ValueError("invalid number of artificial I heterozygotes among 24 recodable plants")
    original=[(.5,.5)]*24+[(.75,.75)]*24
    candidate=[(.25,.75) if i<n_heterozygotes else genotype
               for i,genotype in enumerate(original)]
    before=[sum(g)/2 for g in original]
    after=[sum(g)/2 for g in candidate]
    if before!=after or len(candidate)!=N_PLANTS:
        raise AssertionError("hypothetical genotype-access recode changed plant I expression")
    population_mean=sum(after)/N_PLANTS
    phenotype_var=sum((x-population_mean)**2 for x in after)/N_PLANTS
    copies={str(float(v)):sum(sum(x==v for x in genotype)
                              for genotype in candidate)
            for v in I_LEVELS}
    if (copies!={"0.25":n_heterozygotes,
                 "0.5":48-2*n_heterozygotes,
                 "0.75":48+n_heterozygotes}
        or sum(copies.values())!=N_DIPLOID
        or population_mean!=.625
        or phenotype_var!=.015625):
        raise AssertionError("t30 phenotype-preserving latent allele support invalid")
    a_var=sum(n*(float(allele)-population_mean)**2
              for allele,n in copies.items())/N_DIPLOID
    return {
       "artificial_I_heterozygous_recodes":n_heterozygotes,
       "N_mathematical_plants_not_simulated":N_PLANTS,
       "source_genotype_template_pairs":"24 I=(0.5,0.5) and 24 I=(0.75,0.75)",
       "recode_each_eligible_pair":"(0.5,0.5) -> (0.25,0.75)",
       "original_and_candidate_expressed_I_equal_for_every_plant":True,
       "original_and_candidate_phenotype_mean":population_mean,
       "original_and_candidate_phenotype_variance":phenotype_var,
       "changed_I_numeric_allele_copy_counts":copies,
       "changed_I_numeric_allele_value_variance":a_var,
       "full_genotype_origin_pairing_and_future_Mendelian_outcomes_not_identified":True,
       "current_native_phenotype_dependent_reproductive_ledger_would_match_if_M_A_visitors_unchanged":True,
       "changed_existing_original_R2_population":False,
       "new_population_or_offspring_updates":0,
    }


def scenario_variance(comps:dict,founders:int,visitors:int,repeats:int,
                      endpoint:str)->float:
    if (endpoint not in ENDPOINT_RANGES or
            any(type(x) is not int or x<2 for x in (founders,visitors)) or
            type(repeats) is not int or repeats<1 or
            set(comps)!={"founder","visitor","interaction","nested"} or
            any(type(v) not in (int,float) or not math.isfinite(v) or v<0
                for v in comps.values())):
        raise ValueError("unreviewed independent crossed-source precision inputs")
    half=max(map(abs,ENDPOINT_RANGES[endpoint]))
    if sum(comps.values())>half**2+1e-12:
        raise ValueError("variance scenario exceeds outcome range max variance")
    return (comps["founder"]/founders + comps["visitor"]/visitors
        + comps["interaction"]/(founders*visitors)
        + comps["nested"]/(founders*visitors*repeats))


def static_cost(founders:int,visitors:int,repeats:int)->dict:
    if (any(type(n) is not int or n<2 for n in (founders,visitors))
            or type(repeats) is not int or repeats<1):
        raise ValueError("source axes and nested replicates not declared")
    prefix=founders*visitors*repeats*HISTORICAL_REGIMES
    future=prefix*ACCESS_ARMS*VISITOR_ACTIVITY_ARMS
    return dict(independent_founder_labels=founders,
      independent_visitor_history_labels=visitors,
      nested_demographic_repeats_per_cell=repeats,
      historical_prior_service_regimes=HISTORICAL_REGIMES,
      hypothetical_genetic_access_arms=ACCESS_ARMS,
      future_service_arms=VISITOR_ACTIVITY_ARMS,
      shared_original_history_prefixes=prefix,
      paired_t30_future_forks=future,
      history_prefix_updates_if_later_authorized=prefix*PREFIX_UPDATES,
      future_population_updates_if_later_authorized=future*FUTURE_UPDATES,
      hypothetical_total_population_updates_if_later_authorized=
        prefix*PREFIX_UPDATES+future*FUTURE_UPDATES,
      biological_population_updates_executed=0,
      prospective_source_seed_reservations_created=0,
      no_biology_dispatched=True)


def review()->dict:
    provenance=checked_sources()
    # Both the tri-allelic and two-allelic calculations are exact for these
    # finite numerical copy supports. They do not generate any PlantState.
    access=[compensated_triallelic_counts(c) for c in LOW_COPIES]
    binary=[dict(low_copies=c,
                 allele_mean_if_low_025_high_050=
                     biallelic_population_mean(.25,.50,c))
            for c in LOW_COPIES]
    if len({x["allele_mean_if_low_025_high_050"] for x in binary})!=len(binary):
        raise AssertionError("two-allele mean must change if initial copy count changes")
    if len({x["expected_allele_mean"] for x in access})!=1:
        raise AssertionError("mean-compensation design did not preserve initial mean I")
    if len({x["allele_value_variance"] for x in access})!=len(access):
        raise AssertionError("copy-matched mean still cannot preserve allele variance")
    nominal=NormalDist().inv_cdf(1-ALPHA/(2*CO_PRIMARY_COUNT))
    candidates=[]
    for f in FUTURE_AXES:
        for r in REPEATS:
            costs=static_cost(f,f,r)
            bounds={}
            for name,scenario in VARIANCE_SCENARIOS.items():
                one={}
                for endpoint,comps in scenario.items():
                    v=scenario_variance(comps,f,f,r,endpoint)
                    one[endpoint]={"hypothetical_variance_of_crossed_mean":v,
                                   "normal_97_5pct_marginal_halfwidth_proxy":
                                        nominal*math.sqrt(v)}
                bounds[name]=one
            candidates.append({"candidate":costs,"precision_sensitivity":bounds})
    if not candidates or any(x["candidate"]["biological_population_updates_executed"] for x in candidates):
        raise AssertionError("design-only grid must not run biology")
    return {
      "status":STATUS,
      "evidence_rank":"MATHEMATICAL_DESIGN_REVIEW_NOT_A_REGISTERED_STUDY",
      "sources":provenance,
      "scope":"Independent founder×visitor crossing; three hypothetical I-access levels, two prior visitor regimes, two matched future service arms",
      "original_model_population_K":N_PLANTS,
      "genotype_source_alleles_per_population":N_DIPLOID,
      "two_allele_confounding_demonstration":binary,
      "three_allele_constant_mean_illustrative_design":access,
      "diploid_per_plant_phenotype_preserving_access_illustration":[
          diploid_phenotype_preserving_I_recode(k) for k in (8,16,24)
      ],
      "initial_phenotypic_mean_and_variance_can_be_held_fixed_under_artificial_I_recode":True,
      "mean_invariant_I_access_requires_unassessed_genotype_reallocation":True,
      "three_allele_copy_compensation_changes_allelic_variance":True,
      "other_M_A_genotype_covariance_or_ancestry_preserved":False,
      "source_genotype_construction_method_approved":False,
      "precision_method":"crossed independent founder and visitor source axes; one nested component averaged over repeats; Normal proxy only, not valid finite-sample coverage/power",
      "source_contrast_outcome_support":{
        e:{"min":bounds[0],"max":bounds[1]} for e,bounds in ENDPOINT_RANGES.items()
      },
      "nominal_familywise_alpha_sensitivity_only":ALPHA,
      "hypothetical_co_primary_count":CO_PRIMARY_COUNT,
      "normal_quantile_proxy":nominal,
      "variance_scenarios_hypothetical_not_data_estimated":VARIANCE_SCENARIOS,
      "candidate_allocation_grid":candidates,
      "independent_founder_visitor_source_counts_finalized":False,
      "SESOI_minimum_important_I_or_loss_risk_contrast":None,
      "population_power_validated":False,
      "sample_size_authorized":False,
      "future_genotype_seed_namespace_registered":False,
      "prospectively_registered":False,
      "author_signoff":False,
      "new_biological_simulation_updates":0,
      "dispatched_actions":0,
      "new_statistical_experiments":0,
      "may_dispatch_biological_futures":False,
      "blocking_reasons":[
        "Original exploratory source outcome counts may motivate hypotheses but cannot calibrate prospective power/SESOI as if independent",
        "Unknown actual crossed founder and visitor variance components for planned contrast and genetic access construction",
        "Tri-allelic copy compensation can keep mean I but necessarily changes allele variance and unspecified diploid genotype covariances; a separate artificial per-plant phenotype-preserving I recode also changes latent heterozygosity and allele origins",
        "Low I initial access and past visitor history must be independently varied or explicitly treated as non-identifiable",
        "Unspecified prospective founder/visitor seed pools, compute budget authorization, SESOI, power/precision, reviewer signoff",
        "Original source proposal all run gates false; never dispatch Actions or silently overwrite it",
      ]
    }


if __name__=="__main__":
    print(json.dumps(review(),ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False))
