"""Source-locked original 2304-history audit to plan *exploratory* A-access x I-hidden pilot.

This script NEVER executes model biology, samples pilot seeds, alters the preregistered
factorial, estimates its as-yet-unobserved genetic intervention effect, or authorizes
200-update pilot execution.  Data input: nine previously frozen ecological-order
provider ZIPs.  Each original NPZ is byte-hash checked and its A/I events rederived.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from io import BytesIO
import json
from math import ceil, erf, sqrt
from pathlib import Path
import re
from statistics import mean, stdev
import zipfile

import numpy as np

SOURCE_BLOB='5608ad2cdcbef167fe9062ab5f26318abf2e1bd9'
SOURCE_COMMIT='328548612e93469fcc8663f24548530a57399b9a'
ORIGINAL_SHARDS=(
 ('5b850eaad6104f572f56df2a37da00fbc8473503a827703c82f6870a87e9a881',21210876),
 ('bc675e9eb231ec7f6ac4cb7c26a762cd55d75ad8fff51eae0aa8e28568172280',25105436),
 ('3673b1b07ed2742669f1ba43494ba814d7968cb200c6832c62a5a1c1640fe554',24011622),
 ('676e84ff0729ba88dcd91cb161efeb2dc63f10b6679458695c5d2909c017e9c2',28260780),
 ('900d3d22a36fa59241a933b8efc4b2fb8f320e4b25637e592640f31c529314fe',25372222),
 ('b45f10aae6ec8fa437179285eb50cb3b98a35e3cc3e8610f6e8d36358daeb6e8',32701303),
 ('03d9dcc3b7b993fcba9486bb543e01b8dcd75e40bbb0d5684c6cf72292105a42',29543709),
 ('7a304cab06107d3a48d18bd033f07c046dad5c4ecb95eb2a1a4916ebd9d51876',33820408),
 ('35a6c2da91bb02d50806a919777e21a2c855ab55b5fccc95f917a7af7d77bf62',31634199),
)
CATEGORIES=('assurance_first','investment_first','near_simultaneous','assurance_only','investment_only','neither')
FOUNDER=('main','confirmation')
PILOT_CONTEXTS=(0,3,4)
CASE=re.compile(r'^(main|confirmation)_c([0-8])_r(\d{1,3})\.npz$')
Z975=1.959963984540054;Z80=.8416212335729143


def events(means:np.ndarray, pop:np.ndarray, threshold:float=.05, sustain:int=20, tie:int=5)->dict:
    """Independent original 20-occupied-census first-passage classifier."""
    if means.shape!=(201,3) or pop.shape!=(201,) or int(pop[0])!=48:
        raise ValueError('original 201-census source shape/founder changed')
    alive=pop>0
    if not np.all(np.isfinite(means[alive])) or not np.all(np.isnan(means[~alive])):
        raise ValueError('original extinct genotype means missingness changed')
    if np.any(~alive) and np.any(alive[np.flatnonzero(~alive)[0]:]):
        raise ValueError('original zero-immigration extinction must be absorbing')
    onsets=[]
    for idx,sgn in ((2,1),(1,-1)):
        above=alive & (sgn*(means[:,idx]-means[0,idx])>=threshold)
        runs=np.convolve(above.astype(int),np.ones(sustain,dtype=int),'valid')
        first=np.flatnonzero(runs==sustain)
        onsets.append(int(first[0]) if len(first) else None)
    A,I=onsets
    if A is None:
        category='neither' if I is None else 'investment_only'
    elif I is None:category='assurance_only'
    elif abs(A-I)<=tie:category='near_simultaneous'
    else:category='assurance_first' if A<I else 'investment_first'
    return {'A':A,'I':I,'category':category}


def first_individual_support(alleles:np.ndarray, mutation_flags:np.ndarray,
                             offsets:np.ndarray, means:np.ndarray, pop:np.ndarray,
                             threshold:float=.05)->dict:
    """Retrospective individual-level support, NOT future-blind clock inference.

    Distinguishes standing/segregating non-flagged F1 A genotypes from cases
    where observed support would require a flagged mutant.  Original mutation
    flag semantics are trusted as archived; this is no causal mutation experiment.
    """
    if (alleles.ndim!=3 or alleles.shape[1:]!=(3,2)
        or mutation_flags.shape!=alleles.shape or offsets.shape!=(202,)
        or offsets[0]!=0 or int(offsets[-1])!=len(alleles)
        or not np.array_equal(np.diff(offsets),pop)):
        raise ValueError('invalid original full-genome census/flag inventory')
    A0=float(means[0,2]);I0=float(means[0,1])
    first_A=None;first_I=None;first_A_variance=None;first_nonflag_A=None
    f1_support_count=0;f1_without_flag_count=0
    for year in range(201):
        l,h=offsets[year:year+2]
        if h==l:continue
        body=alleles[l:h];phen=body.mean(axis=2)
        at_A=phen[:,2]>=A0+threshold
        at_I=phen[:,1]<=I0-threshold
        no_flag=(~mutation_flags[l:h,2,:].any(axis=1))
        if first_A is None and at_A.any():first_A=year
        if first_I is None and at_I.any():first_I=year
        if first_A_variance is None and float(phen[:,2].var())>1e-12:first_A_variance=year
        if first_nonflag_A is None and np.any(at_A & no_flag):first_nonflag_A=year
        if year==1:
            f1_support_count=int(at_A.sum())
            f1_without_flag_count=int(np.sum(at_A & no_flag))
    return {'first_A_individual_at_least_founder_mean_plus_005':first_A,
            'first_I_individual_at_most_founder_mean_minus_005':first_I,
            'first_positive_expressed_A_variance':first_A_variance,
            'first_A_individual_support_with_no_A_mutation_flag':first_nonflag_A,
            'F1_A_support_individuals':f1_support_count,
            'F1_A_support_individuals_without_A_mutation_flag':f1_without_flag_count}


def norm_cdf(x):return .5*(1+erf(x/sqrt(2)))


def scenario_power(n:int,delta:float,sigma:float):
    """Power for directional success (two-sided nominal 95% lower bound >0)."""
    if n<=0 or delta<=0 or sigma<=0:raise ValueError('positive assumptions required')
    return norm_cdf(delta*sqrt(n)/sigma-Z975)


def target_delta(n:int,sigma:float,power_target=.8):
    if power_target!=.8:raise ValueError('only frozen 80% illustration')
    return (Z975+Z80)*sigma/sqrt(n)


def audit(root:Path)->dict:
    results={}; provenance=[]; support={}
    for shard_idx,(wanted_sha,wanted_bytes) in enumerate(ORIGINAL_SHARDS):
        path=root/f'ecological-original-shard-{shard_idx}.zip'
        archive=path.read_bytes()
        if len(archive)!=wanted_bytes or sha256(archive).hexdigest()!=wanted_sha:
            raise ValueError(f'shard {shard_idx} byte SHA256/size not original')
        with zipfile.ZipFile(BytesIO(archive)) as z:
            try:complete=json.loads(z.read('_COMPLETION.json'))
            except KeyError as e:raise ValueError('missing original provider completion') from e
            if complete['status']!='COMPLETE_FROZEN_ECOLOGICAL_SHARD' or complete['cases']!=256 or len(complete['records'])!=256:
                raise ValueError('original provider expected 256 original cases')
            seen=set()
            for row in complete['records']:
                task=row['task']
                if task['block'] not in FOUNDER or task['context'] not in range(9) or task['replicate'] not in range(128):
                    raise ValueError('unregistered original raw case')
                key=(task['block'],int(task['context']),int(task['replicate']))
                if key in results or key in seen:raise ValueError('original case repeated')
                seen.add(key)
                member=f'{key[0]}_c{key[1]}_r{key[2]}.npz'
                binary=z.read(member)
                if sha256(binary).hexdigest()!=row['sha256']:
                    raise ValueError('original NPZ sha mismatch '+member)
                with np.load(BytesIO(binary),allow_pickle=False) as npz:
                    means=npz['means'];pop=npz['population']
                    recomputed=events(means,pop)
                    if key[1] in PILOT_CONTEXTS:
                        support[key]=first_individual_support(npz['alleles'],npz['mutation_flags'],
                            npz['offsets'],means,pop)
                if recomputed!=row['events']['0.05']:
                    raise ValueError('original source record and independently re-derived event mismatch: '+member)
                results[key]=recomputed
            provenance.append({'shard':shard_idx,'sha256':wanted_sha,'bytes':wanted_bytes,'cases':len(seen)})
    if len(results)!=2304 or {k[1] for k in results}!=set(range(9)):
        raise ValueError('incomplete original 2304-history cohort')
    # Historical 2304 source verdict checked against the archived original reader.
    all_counts=Counter(v['category'] for v in results.values())
    expected=dict(assurance_first=335,investment_first=435,near_simultaneous=358,assurance_only=895,investment_only=10,neither=271)
    if all_counts!=expected:raise ValueError('original 2304 source outcome distribution no longer matches')
    pilot_subset={k:v for k,v in results.items() if k[1] in PILOT_CONTEXTS}
    if len(pilot_subset)!=768:raise ValueError('expected 2 founders × 3 env × 128 old histories')
    tcounts=Counter(v['category'] for v in pilot_subset.values())
    def D(e):return int(e['category']=='assurance_first')-int(e['category']=='investment_first')
    rows=[]
    for block in FOUNDER:
        for env in PILOT_CONTEXTS:
            z=[pilot_subset[(block,env,i)] for i in range(128)]
            counts=Counter(v['category'] for v in z)
            rows.append({'founder_block':block,'ecological_context':env,'old_genotype_starts':128,
                'six_class_counts':{lab:counts[lab] for lab in CATEGORIES},
                'p_A_event':sum(v['A'] is not None for v in z)/128,
                'p_I_event':sum(v['I'] is not None for v in z)/128,
                'D_all_start':sum(D(v) for v in z)/128})
    old_clusters=[]
    for block in FOUNDER:
        for i in range(128):
            z=[pilot_subset[block,c,i] for c in PILOT_CONTEXTS]
            old_clusters.append({'block':block,'replicate':i,'D':sum(D(v) for v in z)/3,
                                 'A':sum(v['A'] is not None for v in z)/3,
                                 'I':sum(v['I'] is not None for v in z)/3})
    legacy_SD={label:{'mean':mean(x[label] for x in old_clusters),
                     'sd_across_256_old_founder_seed_clusters':stdev(x[label] for x in old_clusters)}
               for label in ('A','I','D')}
    if len(support)!=768:raise ValueError('missing original raw genetic-access support records')
    support_fields=('first_A_individual_at_least_founder_mean_plus_005',
                    'first_I_individual_at_most_founder_mean_minus_005',
                    'first_positive_expressed_A_variance',
                    'first_A_individual_support_with_no_A_mutation_flag')
    supply={name:{str(k):int(c) for k,c in Counter(v[name] for v in support.values()).items()} for name in support_fields}
    # Only compare realized response latency after first individual support.
    # Stratification by observed future order class is post-selection/descriptive!
    from statistics import median
    observed_latency={}
    for cat in CATEGORIES:
        d=[int(results[k]['A']-support[k]['first_A_individual_at_least_founder_mean_plus_005'])
           for k in support if results[k]['category']==cat and results[k]['A'] is not None
           and support[k]['first_A_individual_at_least_founder_mean_plus_005'] is not None]
        if any(v<0 for v in d):raise ValueError('mean A response before individual A-support')
        observed_latency[cat]={'observed_A_event_starts':len(d),
                                'median_response_update_after_individual_support':median(d) if d else None}
    powers=[]
    for sigma in (.25,.5,.8,1.):
        for delta in (.05,.1,.2,.3):
            powers.append({'hypothetical_effect':delta,'hypothetical_cluster_SD':sigma,
                           'n_pilot_history_clusters':128,
                           'directional_success_probability_under_normal_95pct_interval':scenario_power(128,delta,sigma),
                           'required_clusters_for_nominal_80pct':ceil(((Z975+Z80)*sigma/delta)**2)})
    detect=[{'hypothetical_paired_contrast_SD':sigma,
             'delta_needed_for_approx_80pct_power_pilot_n128':target_delta(128,sigma),
             'delta_needed_for_approx_80pct_power_per_founder_n64':target_delta(64,sigma)}
            for sigma in (.25,.5,.8,1.)]
    return {
        'schema':'chapter2_clock_pilot_prelaunch_original_outcome_and_power_review_v1',
        'analysis_date':'2026-10-14',
        'status':'ACTUAL_OLD2304_REPLAYED__NEW1536_NOT_RUN__PILOT_POWER_ONLY_HYPOTHETICAL',
        'original_source_git_blob':SOURCE_BLOB,
        'original_model3_biology_commit':SOURCE_COMMIT,
        'original_source_shards_exact_sha256':provenance,
        'original_cases_verified_from_actual_npz':len(results),
        'raw_original_case_checksums_verified':2304,
        'all_original_2304_six_class':{k:all_counts[k] for k in CATEGORIES},
        'old_matching_pilot_ecological_contexts':list(PILOT_CONTEXTS),
        'original_fixed_access_comparator':{'n_existing_histories':len(pilot_subset),
            'n_original_paired_clusters':len(old_clusters),
            'A_event_count':sum(v['A'] is not None for v in pilot_subset.values()),
            'I_event_count':sum(v['I'] is not None for v in pilot_subset.values()),
            'six_class_counts':{k:tcounts[k] for k in CATEGORIES},
            'six_founder_ecology_rows':rows,
            'old_seed_cluster_summary':legacy_SD,
            'retrospective_genotype_support_at_individual_level':{
                'n_original_cases_full_diploid_alleles_examined':768,
                'first_support_and_expressed_variation_year_counts':supply,
                'F1_A_supporting_individuals_across_all_starts':sum(v['F1_A_support_individuals'] for v in support.values()),
                'F1_A_supporting_individuals_without_A_mutation_flag':sum(v['F1_A_support_individuals_without_A_mutation_flag'] for v in support.values()),
                'first_support_to_A_sustained_population_event_by_postselected_class':observed_latency,
                'interpretation':'Old w=.0625: segregating individual A support by t1 in every existing 3-context case, yet population mean order remains diverse. Genetic support is necessary not sufficient; postselected timing by label is descriptive not causal.'}},
        'new_pilot':{'n_scheduled_trajectories':1536,
                     'n_scheduled_independent_founder_seed_clusters':128,
                     'observed_new_genetic_treatment_effects':None,
                     'n_new_pilot_biological_histories_executed_by_this_audit':0},
        'hypothetical_power_for_future_genetic_factorial_cluster_contrasts':{
            'normal_approx_scenarios':powers,'minimum_detectable_effect_scenarios':detect,
            'nominal_two_sided_alpha':0.05,'power_target':0.8,
            'missing_actual_new_intervention_paired_SD':True,
            'old_cluster_D_SD_is_not_new_genetic_treatment_contrast_SD':True},
        'scope_limits':[
            'Old original 2304 events independently recomputed from exact NPZ censuses, and old 768 3-context diploid genomes scanned for individual support; no original reproductive genome pedigree reexecution claimed here.',
            'Observed A support in first-generation nonmutation-flagged individuals is not a direct randomized segregation-versus-mutation intervention; do not infer natural-population mechanisms or post-event subgroup causality.',
            'Three old ecological contexts reused from exposed cohort are contextual planning evidence, not genetically manipulated pilot results.',
            'The old A 767/768 event incidence is specific to its old A allele-width and original mutation process, and is not projected to new A-width arms.',
            'Any power from hypothetical sigma is an assumption, not observed pilot SD; the five planned contrast effect sizes have not been seen.',
            'I hidden homolog collapse h=0 preserves between-plant expressed variation; it is not total elimination of genetic I access.',
            'A lower halfwidth is inaccessible by standing allele support alone at 0.05, but A mutation at rate 0.01 remains possible.',
            'Two original founder blocks and three prechosen ecological contexts do not provide generalization to all island populations.',
            'Pilot is exploratory, not independent confirmatory test of t0 Price clock versus flexible nonlinear null.',
            'Original source execution and new pilot source/run authorization/preservation remain separate gates.'
        ]
    }


def main():
    p=argparse.ArgumentParser();p.add_argument('--archive-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();result=audit(a.archive_root);a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open('x',encoding='utf-8',newline='\n') as z:json.dump(result,z,ensure_ascii=False,indent=2,allow_nan=False);z.write('\n')
    print(json.dumps({'status':result['status'],'source_cases':result['original_cases_verified_from_actual_npz'],
                      'old_A_event':result['original_fixed_access_comparator']['A_event_count'],
                      'old_I_event':result['original_fixed_access_comparator']['I_event_count']}))

if __name__=='__main__':main()
