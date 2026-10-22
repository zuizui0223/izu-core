"""Read-only synthesis: directional reproductive bias vs allele fixation in A.

Uses already admitted compact artifacts from distinct experiments.
No biological simulation, no population transition, no new significance tests.
Fixation is an outcome of directional and finite inheritance, NOT a
separate independent causal force. This cannot assign causal percentages.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "confirmation": "docs/audits/CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json",
    "variation": "docs/audits/CHAPTER2_VARIATION_CLOCK_RESULTS_20261019.json",
    "neutral_k32": "data/results/model3_k32_neutral_matched_census_20261009.json",
    "pathwise_k32": "data/results/model3_k32_pathwise_direction_sampling_20261009.json",
    "mean_matched_k32": "data/results/model3_k32_mean_matched_ceiling_20261009.json",
    "matched_repeatability": "docs/audits/CHAPTER2_MATCHED_AI_REPEATABILITY_20261019.json",
}
STATUS = "READ_ONLY_DISTINCT_COHORTS_DIRECTION_FIXATION_BOUNDARY_SYNTHESIS"


def insist(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def run(root: Path = ROOT) -> dict:
    source = {}
    provenance = {}
    for key, rel in SOURCES.items():
        raw = (root / rel).read_bytes()
        source[key] = json.loads(raw)
        provenance[rel] = hashlib.sha256(raw).hexdigest()

    confirm, clock = source["confirmation"], source["variation"]
    insist(confirm["crossings"] == clock["crossings"] == 25_600,
           "different crossed population inventory")
    insist(clock["status"] == "COMPLETE_READ_ONLY_POST_OUTCOME",
           "genome readback not admitted")
    insist(confirm["independent_axes"] == [160, 160],
           "independent axes not 160 x 160")
    for policy in ("fixed", "evolving"):
        insist(confirm["arms"][policy + "_B8"]["alive"] == 25_600,
               "unobserved survival censoring at B8")

    def allele_row(policy):
        row, = [x for x in clock["results"] if
                x["trait"] == "A" and x["budget"] == "B8"
                and x["policy"] == policy]
        values = {float(x["value"]): int(x["count"])
                  for x in row["fixed_value_counts"]}
        insist(row["n"] == 25_600 and row["extinct_without_fixation"] == 0,
               "B8 denominator changed")
        insist(sum(values.values()) == row["fixed_before_extinction"]
               and row["alive_unfixed"] + row["fixed_before_extinction"] == row["n"],
               "fixation outcome categories do not conserve starts")
        insist(set(values) <= {0.25, 0.5, 0.75},
               "A allele support grid changed")
        return dict(
            policy=policy, all_start=25_600,
            fixed_any=row["fixed_before_extinction"],
            fixed_values={str(k): v for k, v in sorted(values.items())},
            fixed_at_high_A_0p75=values.get(0.75, 0),
            unfixed_at_census80=row["alive_unfixed"],
            fixed_any_percent=100 * row["fixed_before_extinction"] / 25_600,
            high_A_fixed_percent=100 * values.get(0.75, 0) / 25_600,
            median_fixation_census_among_events=row["fixation_time_among_events"]["median"],
            mean_occupied_polymorphic_censuses=row["occupied_polymorphic_duration_mean"])

    fixed = allele_row("fixed")
    evolving = allele_row("evolving")
    insist(fixed["fixed_values"] == {"0.25": 5332, "0.5": 5187, "0.75": 5145}
           and evolving["fixed_values"] == {"0.5": 275, "0.75": 25307},
           "reported 160x160 B8 A fixation inventory changed")

    # Archived K32 experiments were separate runs with one common archived
    # visitor environment. Do not pool their 512 paths as ecological histories.
    neutral = source["neutral_k32"]
    pathwise = source["pathwise_k32"]
    meanmatch = source["mean_matched_k32"]
    insist(neutral["conditions"]["independent_visitor_histories"] == 1
           and pathwise["design"]["independent_visitor_histories"] == 1,
           "K32 independent visitor-history count changed")
    assert not neutral["conditions"]["canonical_source_operator_edited"]
    assert not pathwise["design"]["canonical_model3_source_modified"]
    n, = [x for x in neutral["cases"] if x["budget"] == 8]
    p, = [x for x in pathwise["cases"] if x["ovule_budget"] == 8]
    m, = [x for x in meanmatch["experiments"] if x["budget"] == 8]
    idx = 2  # assurance high-allele frequency, M/I/A order
    insist(n["n_source_survivors"] == p["n_survived"] == m["n_source_survivors"] == 512,
           "K32 survivor counts changed")
    insist(n["source_endpoint_mean"][idx] > n["neutral_endpoint_mean"][idx],
           "K32 source not above neutral high-A allele frequency")
    assert abs(n["source_endpoint_mean"][idx] -
               n["neutral_endpoint_mean"][idx] -
               n["paired_source_minus_neutral_mean"][idx]) < 1e-12
    directed = p["cumulative_mean_source_reproductive_filtering"][idx]
    sampling = p["cumulative_mean_finite_offspring_sampling"][idx]
    observed = p["realized_mean_eight_generation_high_allele_frequency_change"][idx]
    insist(math.isclose(directed + sampling, observed, abs_tol=1e-12),
           "pathwise conditional expectation identity broken")
    insist(m["source_endpoint_variance"] > 0
           and m["comparator_endpoint_variance"] > 0
           and m["comparator_endpoint_variance"] < m["source_endpoint_variance"],
           "mean-and-census-matched ceiling comparison changed")

    repeatability = source["matched_repeatability"]["settings"]["delayed_control"]["central"]
    insist(repeatability["paired_eligible_contexts"] == 128
           and repeatability["A"]["far_identical_endpoint_contexts"] == 107
           and repeatability["I"]["far_identical_endpoint_contexts"] == 17,
           "central-setting matched endpoint agreement changed")
    rA = repeatability["A"]["contrast_labels"]["0.0"]
    insist(rA["unanimous_contexts"] == rA["all_neutral_contexts"] == 103,
           "identical A contrasts no longer zero")

    # Exact fixed-state functional payoff when no visitors deliver pollen,
    # using native Model3 ovule and delayed-selfing definitions:
    # viable self = B exp(-c_I I^2 - c_A A^2) * A * (1-depression).
    # The derivative of log W wrt A, for c_A=0.5, is 1/A - A.
    def viable_self(a, i=0.5):
        return 8 * math.exp(-0.5 * i * i - 0.5 * a * a) * a * (1 - 0.5)
    assurance_values = {str(a): viable_self(a) for a in (0.25, 0.5, 0.75)}
    insist(assurance_values["0.75"] > assurance_values["0.5"] >
           assurance_values["0.25"] > 0, "analytical visitor-free A direction invalid")

    return dict(
        status=STATUS, new_biological_updates=0, new_statistical_tests=0,
        independent_source_cohorts_are_not_pooled=True,
        source_sha256=provenance,
        main_B8_160x160=dict(
            fixed_expression=fixed, evolving_expression=evolving,
            high_A_fixation_policy_difference_percentage_points=(
                evolving["high_A_fixed_percent"] - fixed["high_A_fixed_percent"]),
            fixation_any_policy_difference_percentage_points=(
                evolving["fixed_any_percent"] - fixed["fixed_any_percent"]),
            interpretation="A-expression policy affects realized genotypes; "
                           "the fixed-A latent locus still drifts, segregates, "
                           "and can associate with selected M/I backgrounds. "
                           "No pure selection coefficient is identified."),
        K32_one_history=dict(
            historical_visitor_histories=1, nested_demographic_runs=512,
            source_end_high_A_allele_frequency=n["source_endpoint_mean"][idx],
            neutral_same_N_end_high_A_allele_frequency=n["neutral_endpoint_mean"][idx],
            source_minus_neutral_A_frequency=n["paired_source_minus_neutral_mean"][idx],
            paired_MC_95_interval_A_frequency=n["paired_approximate_MC_95_interval"][idx],
            separate_pathwise_run=dict(
                expected_reproductive_filtering=directed,
                finite_inheritance_sampling_residual=sampling,
                realized_change=observed),
            separate_mean_and_census_matched_comparator=dict(
                source_end_variance=m["source_endpoint_variance"],
                synthetic_control_end_variance=m["comparator_endpoint_variance"],
                source_fixation_fraction=m["source_fixation_fraction"],
                synthetic_control_fixation_fraction=m["comparator_fixation_fraction"]),
            interpretation="Direction beyond neutral expectation is demonstrated "
                           "in the source model. Small endpoint variance and negative "
                           "direction/sampling covariance are also produced by an "
                           "externally tilted comparator with matched means and N; "
                           "a unique stabilizing-selection contribution is unidentified."),
        distinct_128_by_four_repeat_cohort=dict(
            setting="delayed_control", start="central",
            eligible_contexts=128,
            far_four_repeats_identical_A=107,
            far_four_repeats_identical_I=17,
            unanimous_far_minus_near_A=103,
            unanimous_A_contrasts_equal_to_zero=103,
            interpretation="Repeated A endpoint equality often reflects saturation, "
                           "not a repeatable positive far-minus-near response."),
        analytical_no_visitor_case=dict(
            budget=8, I=0.5, direct_A_cost=0.5, inbreeding_depression=0.5,
            assurance_timing="delayed", pollen_service=0,
            viable_self_production_by_A=assurance_values,
            derivative_of_log_payoff="1/A - A > 0 for 0 < A < 1",
            interpretation="Directional maternal reproductive benefit at matched I, "
                           "not a fitted per-allele selection coefficient."),
        inferential_boundary=[
            "Selection and fixation are not independent additive causes: selection can drive fixation.",
            "The 160x160 fixed-expression arm is not a complete neutral-genome counterfactual.",
            "K32 comparisons are only one engineered visitor-history environment and eight generations.",
            "Mean-matched control is retrospectively calibrated and does not prove what produced source variance.",
            "No unique causal percentages for directional selection, fixation ceiling, and stochastic history.",
            "No confirmation about natural island colonization, recovery probabilities or speciation."])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
        f.write("\n")
    print(json.dumps({"status": STATUS,
                      "new_biological_updates": 0,
                      "high_A_fixation_diff_pp":
                      result["main_B8_160x160"]["high_A_fixation_policy_difference_percentage_points"]}))


if __name__ == "__main__":
    main()
