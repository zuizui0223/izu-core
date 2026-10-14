"""Pre-execution decision audit for the registered Model3 clock pilot.

Calculates *hypothetical* sensitivity, never the expected biological effect,
and refuses to authorize/run the pilot. Recomputes from immutable design and
registered case IDs; no source outcome arrays are used or generated.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from math import ceil, erf, sqrt
from pathlib import Path
from statistics import NormalDist

DESIGN_BLOB = '75d49de2781a240c14bdc3f9106212b0dbbda6aa'
REGISTRY_BLOB = 'f18eae09e3f569ae7edefe970ea17d93c64b1bd5'
POWER_BLOB = 'e322106afec60f1e08d476ad35f1819673e6b7e5'
ALPHA = .05
TARGET_POWER = .8
EFFECT = .02
CLUSTER_ROUND = 128
MIN_CONFIRM = 512
MAX_CONFIRM = 1024
SIGMA_FLOOR = .15
HYPOTHETICAL_SIGMAS = (.10, .15, .20, .25)


def git_blob(raw:bytes)->str:
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def fixed_json(path:Path, want_blob:str)->dict:
    raw = path.read_bytes()
    if git_blob(raw) != want_blob:
        raise ValueError('Frozen research input Git blob changed: ' + str(path))
    return json.loads(raw)


def norm_cdf(x:float)->float:
    return (1+erf(x/sqrt(2)))/2


def power_two_sided_normal(n:int, delta:float, sigma:float, alpha:float=ALPHA)->float:
    if n<2 or sigma<=0 or delta<0 or not 0<alpha<1:
        raise ValueError('invalid purely hypothetical power scenario')
    z=NormalDist().inv_cdf(1-alpha/2)
    noncentral=delta*sqrt(n)/sigma
    return norm_cdf(noncentral-z)+norm_cdf(-noncentral-z)


def confirm_n_from_sd(sigma:float)->dict:
    if sigma<=0:
        raise ValueError('hypothetical variance must be positive')
    z=NormalDist().inv_cdf(1-ALPHA/2)+NormalDist().inv_cdf(TARGET_POWER)
    planned=ceil(max(MIN_CONFIRM,(z*max(sigma,SIGMA_FLOOR)/EFFECT)**2)/CLUSTER_ROUND)*CLUSTER_ROUND
    if planned>MAX_CONFIRM:
        return {'n_confirm_clusters':None,'decision':'NO_GO_OVER_1024', 'raw_required_clusters_rounded':planned}
    return {'n_confirm_clusters':planned,'decision':'POSSIBLE_IF_FUTURE_PILOT_SD_AND_FROZEN_CLOCK_ALLOW',
            'raw_required_clusters_rounded':planned,
            'n_original_model3_paths_if_launched':planned*12}


def wilson_interval_95(successes:int,n:int)->list[float]:
    if not (0<=successes<=n) or n<1:raise ValueError('invalid hypothetical binomial cell')
    z=NormalDist().inv_cdf(.975);p=successes/n
    denom=1+z*z/n
    center=(p+z*z/(2*n))/denom
    half=z*sqrt(p*(1-p)/n+z*z/(4*n*n))/denom
    return [center-half,center+half]


def audit(design:dict,registry:dict,power:dict)->dict:
    if (design.get('schema')!='chapter2_clock_A_access_by_I_hidden_homolog_pilot_design_v2'
        or design['pilot']['total_trajectories']!=1536
        or design['pilot']['independent_stochastic_clusters']!=128
        or design['pilot']['updates_per_trajectory']!=200
        or design['pilot']['replicates_per_founder']!=64
        or design['pilot']['founder_blocks']!=2
        or design['factorial']['treatments_per_founder_seed']!=12
        or design['factorial']['I_mutation_allowed'] is not False
        or design['factorial']['mutation_traits']!=[False,False,True]
        or design['pilot']['original_outcome_threshold']!=.05
        or design['pilot']['event_sustain_censuses']!=20
        or design['pilot']['tie_window_updates']!=5):
        raise ValueError('prospective pilot scientific design no longer matches admitted source')
    if (registry['status']!='PRE_BIOLOGICAL_EXPLICIT_PILOT_INPUTS_RECORDED_NO_EXECUTION'
        or registry['total_input_trajectories']!=1536
        or registry['independent_stochastic_stream_clusters']!=128
        or len(registry['case_identifiers'])!=1536
        or len(set(registry['case_identifiers']))!=1536
        or len(registry['stochastic_history_cluster_master_seeds_decimal'])!=128
        or registry['new_biological_histories']!=0):
        raise ValueError('pilot stochastic identity or execution state drift')
    if (power['schema']!='chapter2_clock_power_envelope_assumption_sensitivity_v1'
        or power['status']!='DESIGN_ONLY_HYPOTHETICAL_NORMAL_POWER_NOT_EMPIRICAL'
        or power['pilot']['clusters']!=128 or power['pilot']['trajectories']!=1536
        or power['confirmation_selection_rule']['effect_used']!=EFFECT
        or power['confirmation_selection_rule']['sigma_floor']!=SIGMA_FLOOR
        or power['confirmation_selection_rule']['max_clusters']!=MAX_CONFIRM):
        raise ValueError('original hypothetical power record changed')
    rows=[]
    for sigma in HYPOTHETICAL_SIGMAS:
        gate=confirm_n_from_sd(sigma)
        rows.append({'assumed_per_history_logloss_sd':sigma,
                     'hypothetical_128_cluster_pilot_power_if_tested':power_two_sided_normal(128,EFFECT,sigma),
                     'hypothetical_512_cluster_confirm_power':power_two_sided_normal(512,EFFECT,sigma),
                     'hypothetical_896_cluster_confirm_power':power_two_sided_normal(896,EFFECT,sigma),
                     'hypothetical_1024_cluster_confirm_power':power_two_sided_normal(1024,EFFECT,sigma),
                     **gate})
    # Regression: test the old registered power envelope's n=512,.02,.15 cell.
    relevant=[x for x in power['design_grid']
              if x['assumed_delta_log_loss']==EFFECT
              and x['assumed_paired_history_sd']==SIGMA_FLOOR and x['clusters']==512]
    if len(relevant)!=1 or abs(relevant[0]['asymptotic_normal_power']-rows[1]['hypothetical_512_cluster_confirm_power'])>2e-4:
        raise ValueError('independent recomputation disagrees with previous registered power worksheet')
    sigma_break=EFFECT*sqrt(MAX_CONFIRM)/(NormalDist().inv_cdf(.975)+NormalDist().inv_cdf(.8))
    return {
      'schema':'chapter2_clock_pilot_preexecution_power_review_v1',
      'status':'EXPLORATORY_PILOT_SAMPLE_PLAN_COHERENT__SCIENCE_RUN_NOT_AUTHORIZED',
      'basis':{'pilot_design_git_blob':DESIGN_BLOB,'pilot_registry_git_blob':REGISTRY_BLOB,
               'previous_assumption_power_git_blob':POWER_BLOB},
      'pilot':{'registered_paths':1536,'registered_original_model_updates':307200,
               'paired_history_clusters':128,'factorial_cells':24,'n_each_cell':64,
               'independent_natural_island_systems':0,'registered_pilot_histories_executed':0},
      'power_contract':{'assumed_logloss_difference':EFFECT,'two_sided_alpha':ALPHA,
                        'target_power_for_future_confirmation':TARGET_POWER,
                        'min_future_confirm_clusters':MIN_CONFIRM,
                        'max_future_confirm_clusters':MAX_CONFIRM,'sd_floor':SIGMA_FLOOR,
                        'GO_ONLY_IF_ASSUMED_SD_AT_OR_BELOW':sigma_break},
      'hypothetical_sensitivity':rows,
      'maximally_uncertain_64_case_six_class_one_vs_rest_probability_wilson_95':wilson_interval_95(32,64),
      'scientific_interpretation':[
          'The 128-cluster pilot is for phenotype-matched two-axis access effects and estimating variability, not for testing a 0.02 log-loss gain against a not-yet-defined clock/null.',
          'A single 64-case cell with 50 percent events has a wide illustrative Wilson interval; 24 cells and six uneven class probabilities require retaining zero and rare categories.',
          'Do not treat 1536 matched treatment×ecology paths as 1536 independent ecological systems.',
          'Original A-low threshold unreachability without mutation is coupled to the width intervention; mutation remains enabled, so not a clean scalar genetic variance effect.',
          'Hidden I-homolog removal leaves all founding expressed I and between-adult I variance intact.',
          'The pilot is not evidence of a universal Q1-Q2 two-stage response clock; a fully frozen predictive model and equally flexible null require later completely new seeds.'
      ],
      'science_executed_here':False,'execution_approved_here':False,
      'required_before_pilot_execution':['source model and raw output/replay technical CI success (already confirmed on PR504)',
              'reviewed immutable author/reviewer-approved original model 200-update execution receipt',
              'reviewed separate-provider primary/mirror preservation and license/custody',
              'single producer rather than pooled comparator branch'],
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--design',type=Path,required=True)
    p.add_argument('--registry',type=Path,required=True)
    p.add_argument('--previous-power',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    if args.out.exists():raise FileExistsError('original power review receipt exists')
    out=audit(fixed_json(args.design,DESIGN_BLOB),fixed_json(args.registry,REGISTRY_BLOB),
              fixed_json(args.previous_power,POWER_BLOB))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('x',encoding='utf-8') as fh:
        json.dump(out,fh,indent=2,ensure_ascii=False);fh.write('\n')
    print(json.dumps({'status':out['status'],'pilot':out['pilot']},indent=2))

if __name__=='__main__':main()
