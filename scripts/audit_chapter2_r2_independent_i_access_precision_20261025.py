"""R2 future independent I-access study: analytic crossed-source precision design ONLY.

This audit reads the still-UNAPPROVED R2 proposal, rejects any execution/
authorization state, and computes *distribution-free* bounded-difference
precision radii for hypothetical new founder × visitor × nested-demography
allocations. It runs NO biological population steps, reads NO future outcomes,
uses NO RNG, and does NOT approve a source commit or sample size.

For F independent founders and V independent visitor histories crossed with
R independently sampled demographic streams per crossed cell, let H_fvr be
the matched access × activity difference-in-differences of a binary low-I
allele loss indicator. H belongs to [-2, 2]; a within-I-access paired activity
loss difference D belongs to [-1, 1]. Resampling an entire founder, visitor
history, or cell-specific demographic primitive changes grand-average H by
at most 4/F, 4/V or 4/(F*V*R). McDiarmid implies

P(|avg H - E[avg H]| > h) <= 2 exp(-2h² /
                  (16*(1/F + 1/V + 1/(F*V*R)))).

This is conservative illustrative *precision*, not statistical POWER. It
assumes independently sampled founders and visitor histories and conditionally
independent per-cell demographic streams; violation voids the bound. Crossed
cell observations are NOT F×V×R independent island replicates.
"""
from __future__ import annotations

import argparse
import json
from math import isfinite, log, sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "docs/protocols/CHAPTER2_R2_INDEPENDENT_I_ACCESS_PRECISION_DESIGN_20261025.json"
PARENT = ROOT / "docs/protocols/CHAPTER2_R2_HISTORY_POLLEN_STATE_NEXT_STUDY_PROPOSAL_20261023.json"
STATUS = "DESIGN_ONLY_NOT_AUTHORIZED_NOT_PREREGISTERED"
RESULT_STATUS = "PASS_ANALYTIC_DESIGN_PRECISION_NO_NEW_BIOLOGY_NO_DISPATCH"
SOURCE_ZIP = "10bb8bdd52b53b32429e350c2f392ed2aeaa791683ede1d563ae6627c5ecb35e"


def _positive_integer(value: object, name: str) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{name} must be a positive, exact integer")
    return value


def crossed_source_precision_radius(
    founders: int, visitors: int, repeats: int, *, range_width: float, alpha: float
) -> float:
    """Two-sided McDiarmid precision radius, NOT a power/sample-size approval."""
    F=_positive_integer(founders,"founders")
    V=_positive_integer(visitors,"visitors")
    R=_positive_integer(repeats,"nested demographic repeats")
    if (type(range_width) not in (float,int) or type(alpha) not in (float,int)
        or not isfinite(range_width) or not isfinite(alpha)
        or range_width <= 0 or not 0 < alpha < 1):
        raise ValueError("finite positive outcome range and alpha in (0,1) required")
    independent_axes=1/F + 1/V + 1/(F*V*R)
    return float(range_width*sqrt(log(2/alpha)*independent_axes/2))


def nominal_state_updates(
    founders:int,visitors:int,repeats:int, *,
    prefix:int=30,future:int=50, access_arms:int=2, activity_arms:int=2
) -> dict:
    """Number of design-allocated native state updates, NOT runtime/cost claim."""
    F=_positive_integer(founders,"founders")
    V=_positive_integer(visitors,"visitors")
    R=_positive_integer(repeats,"nested demographic repeats")
    P=_positive_integer(prefix,"prefix")
    T=_positive_integer(future,"future")
    A=_positive_integer(access_arms,"access policies")
    B=_positive_integer(activity_arms,"activity policies")
    independent_prefix_cells=F*V*R
    future_paths=independent_prefix_cells*A*B
    return {
        "crossed_founder_visitor_cells":F*V,
        "independent_founder_source_axis":F,
        "independent_visitor_history_axis":V,
        "nested_demographic_prefixes":independent_prefix_cells,
        "access_activity_future_paths":future_paths,
        "nominal_original_prefix_updates":independent_prefix_cells*P,
        "nominal_future_updates":future_paths*T,
        "nominal_total_model_update_equivalents":
            independent_prefix_cells*P + future_paths*T,
    }


def audit(design_path:Path=DESIGN,parent_path:Path=PARENT) -> dict:
    x=json.loads(Path(design_path).read_text(encoding="utf-8"))
    p=json.loads(Path(parent_path).read_text(encoding="utf-8"))
    if (x.get("schema")!="izu_core_chapter2_r2_independent_i_access_precision_v1"
        or x.get("status")!=STATUS or p.get("status")!=STATUS
        or p.get("schema")!="chapter2_r2_independent_history_service_identification_design_proposal_v1"
        or x["provenance"]["canonical_unapproved_R2_proposal"] !=
           "docs/protocols/CHAPTER2_R2_HISTORY_POLLEN_STATE_NEXT_STUDY_PROPOSAL_20261023.json"
        or x["provenance"]["original_R2_exploratory_zip_sha256"]!=SOURCE_ZIP
        or x["provenance"]["parent_R2_registered_four_setting_decision"]!="INCONCLUSIVE"
        or p["existing_evidence"]["fresh_founder_r2_four_setting_status"]!="INCONCLUSIVE"
        or not x["provenance"]["registered_R4_G_S_unchanged"]
        or not p["existing_evidence"]["registered_confirm160_G_S_unchanged"]
        or not x["provenance"]["source_observed_384_trajectories_excluded_from_confirmation"]):
        raise AssertionError("proposal/evidence/source boundary was altered")
    if (any(v is not False for v in x["run_gate"].values())
        or any(v is not False for v in p["run_gate"].values())
        or x["new_biological_population_updates"]!=0
        or x["new_independent_confirmation_cases"]!=0):
        raise AssertionError("prospective biological dispatch or approval may not be inferred")
    requested=x["unresolved_review_requirements"]
    if set(requested) != {
        "independent_source_and_rng_seed_namespace",
        "fixed_target_I_allele_values_and_genetic_access_intervention",
        "matched_population_I_mean_variance_and_A_M_covariance_protocol",
        "genotype_and_pollen_q_feasibility_negative_controls",
        "founder_and_visitor_axis_sample_sizes",
        "nested_repeats",
        "minimum_biologically_important_effect",
        "multiplicity_and_estimand_hierarchy",
        "precision_and_power_approval",
        "compute_budget_approval",
        "frozen_source_sha",
        "frozen_protocol_sha",
        "author_signoff",
    } or any(value is not None for value in requested.values()):
        raise AssertionError("future I-access design decisions not yet authorized")
    allocation=x["experimental_allocation"]
    if (not allocation["crossed_independent_founder_visitor_axes"]
        or not allocation["paired_demographic_streams_nested_within_each_crossed_cell"]
        or len(allocation["genetic_access_levels"])!=2
        or len(allocation["native_activity_arms"])!=2
        or allocation["prefix_updates"]!=30
        or allocation["future_updates"]!=50
        or allocation["genetic_access_levels_selected_prior_to_new_outcomes"] is not False
        or allocation["genetic_access_intervention_feasibility_verified"] is not False
        or allocation["independent_rng_stream_plan_approved"] is not False
        or allocation["independent_founder_count"] is not None
        or allocation["independent_visitor_count"] is not None
        or allocation["nested_demographic_repeats_per_cell"] is not None):
        raise AssertionError("crossed biological design is not authorized or cannot be audited")
    endpoints=x["proposed_outcome_contract"]
    if (endpoints["first_event_states"] != [
        "low_I_allele_lost","low_I_allele_fixed",
        "population_extinct","still_polymorphic_at_horizon"]
        or endpoints["horizon_update"]!=80
        or endpoints["proposed_primary_interaction_range"]!=[-2,2]
        or endpoints["paired_activity_contrast_range"]!=[-1,1]
        or endpoints["zero_terminal_mean_contrast_not_no_selection"] is not True):
        raise AssertionError("event and paired contrast endpoint definitions changed")
    precision=x["design_only_precision"]
    if (precision["alpha_illustrative"]!=0.05
        or precision["not_power_without_effect_and_variance"] is not True
        or precision["precision_bound_is_conditional_on_design_independence"] is not True
        or precision["independent_two_axis_power_or_precision_approved"] is not False
        or precision["candidate_count_not_committed"] is not True
        or any(precision[k] is not None for k in [
             "minimum_biologically_meaningful_interaction",
             "target_precision_half_width",
             "empirical_crossed_source_variance_components"])):
        raise AssertionError("hypothetical precision was inappropriately promoted")
    rows=[]
    keys=set()
    for cell in precision["candidate_cells_not_chosen"]:
        if set(cell)!={"founders","visitors","repeats"}:
            raise AssertionError("invalid uncommitted crossed-source candidate structure")
        F,V,R=(cell[k] for k in ("founders","visitors","repeats"))
        F=_positive_integer(F,"founders")
        V=_positive_integer(V,"visitors")
        R=_positive_integer(R,"repeats")
        if (F,V,R) in keys:
            raise AssertionError("candidate source allocation duplicates another")
        keys.add((F,V,R))
        cost=nominal_state_updates(
            F,V,R,prefix=allocation["prefix_updates"],future=allocation["future_updates"],
            access_arms=len(allocation["genetic_access_levels"]),
            activity_arms=len(allocation["native_activity_arms"])
        )
        diff=crossed_source_precision_radius(F,V,R,range_width=2.,alpha=.05)
        interaction=crossed_source_precision_radius(F,V,R,range_width=4.,alpha=.05)
        if abs(interaction-2*diff)>1e-12:
            raise AssertionError("contrasts do not obey two-axis width bound")
        rows.append({
            "founder_axis":F,"visitor_axis":V,"nested_demographic_repeats":R,
            "uncapped_95pct_bounded_radius_paired_loss_risk_difference":diff,
            "uncapped_95pct_bounded_radius_I_access_by_activity_interaction":interaction,
            **cost,
        })
    if not rows:
        raise AssertionError("no hypothetical crossed source allocations")
    return {
        "status":RESULT_STATUS,
        "source_design_status":STATUS,
        "source_protocol_original_zip_sha256":SOURCE_ZIP,
        "method":"Conservative bounded McDiarmid two-axis source and nested demographic precision; NOT design power.",
        "alpha_illustrative":0.05,
        "primary_measurable_endpoint_proposed_not_frozen":
            endpoints["proposed_primary_interaction"],
        "primary_effect_size_or_minimum_important_difference_authorized":False,
        "independent_source_and_power_approved":False,
        "original_384_paths_reused_as_confirmatory_data":False,
        "new_biological_population_updates":0,
        "would_dispatch_actions":False,
        "candidate_designs_not_chosen":rows,
        "scientific_inference_ceiling":
            "Even with independent two-axis sampling, confidence radii are worst-case bounds, not expected CI widths or achieved power. All numerical grids are hypothetical; crossed founder × visitor × nested-demographic observations are not F×V×R independent island replicates.",
    }


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path)
    parser.add_argument("--design",type=Path,default=DESIGN)
    opts=parser.parse_args()
    result=json.dumps(audit(opts.design),indent=2,ensure_ascii=False,sort_keys=True)+"\n"
    if opts.out:
        opts.out.parent.mkdir(parents=True,exist_ok=True)
        opts.out.write_text(result,encoding="utf-8")
    else:
        print(result,end="")
