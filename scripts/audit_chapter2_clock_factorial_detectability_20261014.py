"""Pre-outcome *hypothetical* sensitivity audit for the Chapter 2 2x2 pilot.

No original model imported, no biological computation, no pilot predictions or
empirical variance inferred. Does NOT authorize or dispatch the pilot. The
normal-approximation criterion is directional positivity of the lower end of a
nominal two-sided-95% CI for a paired-history effect, conditional on a supplied
SD; it is a DESIGN sensitivity device, not a p-value from any cohort.
"""
from __future__ import annotations

import argparse
import json
from math import ceil, erf, isfinite, sqrt
from pathlib import Path

Z_975 = 1.959963984540054
Z_80 = 0.8416212335729143
N_PILOT = 128
N_PER_FOUNDER = 64
ARMS_PER_CLUSTER = 12
N_TRAJECTORIES = 1536
SIGMA_SCENARIOS = (0.1, 0.15, 0.2, 0.3, 0.5, 1.0)
EFFECT_SCENARIOS = (0.02, 0.05, 0.1, 0.2)
CONFIRMATION_EFFECT = 0.02
CONFIRMATION_SIGMA_FLOOR = 0.15
CONFIRMATION_MIN = 512
CONFIRMATION_MAX = 1024
CONFIRMATION_ROUND = 128


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


def one_direction_ci_positive_probability(effect: float, sd: float, n_clusters: int) -> float:
    """Only the *positive-sign* side of a lower 95% confidence bound.

    This mirrors the earlier `chapter2_clock_power_envelope_20261013.json`'s
    directional success expression. It is not full two-tail rejection power.
    """
    if not (isfinite(effect) and effect >= 0 and isfinite(sd) and sd > 0 and
            isinstance(n_clusters, int) and n_clusters >= 2):
        raise ValueError('nonnegative effect, positive assumed SD and >=2 independent paired clusters required')
    return normal_cdf(effect * sqrt(n_clusters) / sd - Z_975)


def hypothetical_effect_for_80pct(sd: float, n_clusters: int) -> float:
    if not (isfinite(sd) and sd > 0 and isinstance(n_clusters, int) and n_clusters >= 2):
        raise ValueError('assumed SD must be finite/positive and sample size >=2')
    return (Z_975 + Z_80) * sd / sqrt(n_clusters)


def hypothetical_later_confirmation(sd: float) -> dict:
    """Reproduce the *earlier* registered sigma-only n rule, not a new one."""
    if not isfinite(sd) or sd <= 0:
        raise ValueError('strictly positive finite assumed SD required')
    planning_sd = max(sd, CONFIRMATION_SIGMA_FLOOR)
    exact_n = ((Z_975 + Z_80) * planning_sd / CONFIRMATION_EFFECT) ** 2
    rounded_n = max(CONFIRMATION_MIN, ceil(exact_n / CONFIRMATION_ROUND) * CONFIRMATION_ROUND)
    no_go = rounded_n > CONFIRMATION_MAX
    return {
        'assumed_score_difference_cluster_sd': sd,
        'planning_sd_with_previously_frozen_floor': planning_sd,
        'unrounded_required_clusters_approximate': exact_n,
        'rounded_required_clusters': rounded_n,
        'decision_if_models_were_frozen_and_sd_were_valid': 'NO_GO_EXCEEDS_1024_CLUSTER_CAP' if no_go else 'FURTHER_MODEL_AND_SOURCE_REVIEW_REQUIRED',
        'would_require_trajectories': rounded_n * ARMS_PER_CLUSTER if not no_go else None,
        'scientific_confirmation_authorized': False,
        'model_based_sigma_measured_from_current_pilot': False,
    }


def audit() -> dict:
    scenarios = [{
        'assumed_cluster_sd': sd,
        'pilot_128_cluster_normal_95pct_directional_80pct_effect_threshold': hypothetical_effect_for_80pct(sd, N_PILOT),
        'pilot_64_one_founder_cluster_normal_95pct_directional_80pct_effect_threshold': hypothetical_effect_for_80pct(sd, N_PER_FOUNDER),
        'pilot_128_cluster_standard_error_if_assumed_sd': sd/sqrt(N_PILOT),
        'effect_sensitivity': [{
            'assumed_effect': effect,
            'directional_lower_95pct_bound_gt_zero_probability_normal': one_direction_ci_positive_probability(effect, sd, N_PILOT),
        } for effect in EFFECT_SCENARIOS],
    } for sd in SIGMA_SCENARIOS]
    score_plan = [hypothetical_later_confirmation(s) for s in (0.15, 0.2, 0.225, 0.25)]
    return {
        'schema': 'chapter2_clock_pilot_factorial_power_and_confirmation_boundary_v1',
        'status': 'ASSUMPTION_ONLY_PRE_OUTCOME_POWER_AUDIT_NO_BIOLOGICAL_RUN',
        'as_of_date': '2026-10-14',
        'source_frozen_design': {
            'path': 'data/design/chapter2_clock_factorial_pilot_protocol_20261013.json',
            'git_blob': '75d49de2781a240c14bdc3f9106212b0dbbda6aa',
        },
        'source_frozen_analysis': {
            'path': 'data/design/chapter2_clock_factorial_pilot_analysis_contract_20261013.json',
            'git_blob': '06c343b6e20a08c0575ddbe6ace5ef5fbdeb85ed',
            'five_predeclared_descriptive_contrasts': [
                'Awidth_to_A_incidence', 'Ihidden_to_I_incidence',
                'Awidth_to_D', 'Ihidden_to_D', 'Awidth_x_Ihidden_to_D',
            ],
        },
        'source_existing_power_envelope': {
            'path': 'data/results/chapter2_clock_power_envelope_20261013.json',
            'original_procedure': 'one_direction_ci_positive_probability matches original prospective six-class paired-history log-loss assumption envelope',
            'uses_effect_from_pilot_for_confirmation_n': False,
        },
        'pilot_grain': {
            'original_founder_blocks': 2,
            'paired_streams_per_founder': N_PER_FOUNDER,
            'independent_founder_stream_clusters': N_PILOT,
            'contexts_per_cluster': 3,
            'genotype_arms_per_context': 4,
            'trajectories_per_cluster': ARMS_PER_CLUSTER,
            'registered_trajectories': N_TRAJECTORIES,
            'updates_per_trajectory_if_later_authorized': 200,
            'actual_new_model3_histories_generated_in_this_audit': 0,
        },
        'bounded_factorial_contrast_support': {
            'A_incidence_and_I_incidence_main_factor_contrasts': [-1, 1],
            'D_all_start_order_score': [-1, 1],
            'D_main_factor_contrasts': [-2, 2],
            'D_Awidth_x_Ihidden_interaction': [-4, 4],
            'D_definition': 'indicator(assurance_first)-indicator(investment_first); ties and single/no events contribute zero, all included in six-class denominator',
        },
        'normal_approximation': {
            'two_sided_95pct_ci_lower_bound_z': Z_975,
            'target_directional_success_probability': 0.80,
            'z_for_80pct_directional_success': Z_80,
            'method': 'P(estimated mean - z0.975*assumedSD/sqrt(n)>0) assuming Normal distribution of paired-cluster effect estimator',
            'not_5_comparisons_familywise_adjusted': True,
            'not_actual_confirmatory_power': True,
            'not_empirical_SD_from_new_genotype_intervention': True,
        },
        'illustrative_pilot_scenarios': scenarios,
        'existing_future_prediction_score_rule_if_fully_reviewed': {
            'target_mean_six_class_logloss_gain': CONFIRMATION_EFFECT,
            'planning_sigma_floor': CONFIRMATION_SIGMA_FLOOR,
            'minimum_independent_clusters': CONFIRMATION_MIN,
            'maximum_independent_clusters': CONFIRMATION_MAX,
            'round_to_clusters': CONFIRMATION_ROUND,
            'assumed_logloss_cluster_sd_grid': score_plan,
            'predictive_clock_and_equal_or_more_flexible_null_currently_frozen': False,
            'post_pilot_prediction_model_specific_sigma_currently_identified': False,
            'pilot_factorial_contrast_sd_cannot_substitute_for_prediction_logloss_difference_sd': True,
        },
        'scientific_judgement': [
            'Pilot n=128 founder×seed streams is a feasibility and exploratory factorial effect-variance study, not 1,536 independent ecological-history observations.',
            'The two founder blocks and three environments are fixed design contexts, not six random independently sampled natural islands or model families.',
            'Within-simulation genotype interventions can describe model-specific effect of A allelic support and hidden I homolog accessibility; they do not alone identify natural-island historical selection.',
            'The five outcome summaries have no preregistered formal hypothesis-testing multiplicity correction; normal thresholds here are illustrative, not 5 claimed p-values.',
            'For future log-loss confirmation, the two-stage genetic-access clock and at-least-equally-flexible ecological×genetic null are NOT frozen; model-based sigma cannot be treated as already measured.',
            'The original producer remains authorization-locked; all six genuine raw ZIPs and independent primary+mirror readback absent at the time of this design audit.',
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    result = audit()
    if args.out.exists():
        raise FileExistsError('refuse to overwrite an earlier prereg design audit')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(result, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')
    print(json.dumps({'status': result['status'], 'pilot_clusters': N_PILOT,
                      'assumed_model_sd_015_future': hypothetical_later_confirmation(.15),
                      'assumed_model_sd_025_future': hypothetical_later_confirmation(.25)}))


if __name__ == '__main__':
    main()
