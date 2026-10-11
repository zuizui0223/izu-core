"""Retrospective immutable-cohort accounting; no biological history execution."""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
import math
import os
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import audit_chapter2_sequence_tempo_results_20261011 as integrity
from scripts import run_chapter2_sequence_abrupt_gradual_functional_loss_20261011 as native
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import PlantState

SCHEMA = 'chapter2_tempo_realization_accounting_v1'
EVIDENCE_RANK = 'RETROSPECTIVE_EXISTING_COHORT_ACCOUNTING_NOT_CAUSAL_MEDIATION'
TOL = 1e-11
COMPONENTS = ('observed_change', 'expected_response', 'parent_sampling',
              'segregation_mutation_remainder')
WINDOWS = {'early': (0, 100), 'late': (100, 400), 'full': (0, 400)}
TRAITS = {'I': 1, 'A': 2}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def number(value, context):
    require(type(value) in (int, float) and math.isfinite(value), context + ': nonfinite/nonnumber')
    return float(value)


def check_close(saved, calculated, context, errors=None):
    if calculated is None:
        require(saved is None, context + ': undefined value must be null')
        return
    error = abs(number(saved, context) - calculated)
    require(error <= TOL, f'{context}: mismatch {saved} versus {calculated}')
    if errors is not None:
        errors[context] = max(errors.get(context, 0.), error)


def state_from_census(census):
    ids = census['adult_ids']
    require(isinstance(ids, list) and all(type(x) is int and x >= 0 for x in ids), 'adult_ids invalid')
    require(len(set(ids)) == len(ids), 'duplicate adult_ids')
    require(len(ids) <= 48, 'census exceeds capacity')
    alleles = np.asarray(census['diploid_alleles'], dtype=float)
    if not ids:
        require(alleles.size == 0, 'empty census has alleles')
        alleles = np.empty((0,3,2), dtype=float)
    return PlantState(alleles=alleles, ids=np.asarray(ids,dtype=np.int64),
        allele_origin=np.zeros((len(ids),3,2),dtype=np.int64),
        mutation_flags=np.zeros((len(ids),3,2),dtype=bool),
        birth_years=np.zeros(len(ids),dtype=np.int64))


def poisson_capacity_kernel(intensity, capacity=48):
    """Conditional saved-state Poisson recruitment with no history risk product."""
    lam = number(intensity, 'seed intensity')
    require(lam >= 0 and type(capacity) is int and capacity > 0, 'invalid Poisson kernel')
    if lam == 0:
        return {'p_zero': 1., 'p_below_K': 1., 'expected_next_N': 0.,
                'expected_capacity_shortfall': float(capacity)}
    # Log PMFs preserve tiny lower tails when exp(-lambda) itself underflows.
    pmf = [math.exp(-lam + r*math.log(lam) - math.lgamma(r+1)) for r in range(capacity)]
    shortfall = math.fsum((capacity-r)*p for r,p in enumerate(pmf))
    expected_next = float(capacity)-shortfall
    if lam < capacity:
        # Direct upper tail avoids cancellation for very small positive means.
        term = math.exp(-lam + capacity*math.log(lam)-math.lgamma(capacity+1))
        tail_terms = [term]
        for r in range(capacity+1,capacity+1025):
            term *= lam/r
            tail_terms.append(term)
            if term <= math.fsum(tail_terms)*1e-16:
                break
        expected_next = math.fsum(r*p for r,p in enumerate(pmf)) + capacity*math.fsum(tail_terms)
    return {'p_zero': math.exp(-lam), 'p_below_K': min(1.,math.fsum(pmf)),
            'expected_next_N': expected_next,
            'expected_capacity_shortfall': shortfall}


def account_transition(source, child, saved, ledger, *, mutation_rate):
    """ID-linked expected, realized-parent and observed genotype means."""
    require(type(source['t']) is int and child['t'] == source['t']+1
            and saved['t'] == source['t'], 'transition timestamps inconsistent')
    parents, children = state_from_census(source), state_from_census(child)
    n, nc = len(parents.ids), len(children.ids)
    require(type(saved['N']) is int and saved['N'] == n, 'saved N mismatch')
    require(ledger.outcross.shape == (n,n) and ledger.self_viable.shape == (n,), 'ledger shape')
    errors = {}
    for name, calculated in [('delivered',float(ledger.delivered.sum())),
                             ('outcross',float(ledger.outcross.sum())),
                             ('viable_self',float(ledger.self_viable.sum()))]:
        check_close(saved[name],calculated,name,errors)
    parentage = saved['parentage']
    require(isinstance(parentage,list) and len(parentage) == nc, 'each child needs retained parentage')
    require(all(isinstance(p,list) and len(p)==3 and all(type(x) is int for x in p)
                for p in parentage), 'invalid parentage IDs')
    require(len({p[0] for p in parentage}) == nc and {p[0] for p in parentage} == set(children.ids),
            'duplicate or missing child linkage')
    positions = {int(identifier): j for j,identifier in enumerate(parents.ids)}
    require(all(m in positions and f in positions for _,m,f in parentage), 'missing source parent ID')
    selfed = sum(m == f for _,m,f in parentage)
    for name,count in [('resident_selfed_recruits',selfed),('resident_outcross_recruits',nc-selfed)]:
        require(type(saved[name]) is int and saved[name] == count, name + ' mismatch')
    genes = parents.alleles.mean(axis=2)
    weight = native.genetic_return(ledger)
    intensity = float(ledger.outcross.sum()+ledger.self_viable.sum())
    total_weight = float(weight.sum())
    check_close(total_weight,intensity,'weight_intensity',errors)
    expected = genes.T @ weight / total_weight if total_weight > 0 else None
    # A distinct parent-pair calculator, with donor rows and maternal columns.
    pair_expected = None
    if intensity > 0:
        pair_means = .5*(genes[:,None,:]+genes[None,:,:])
        pair_expected = (np.einsum('ij,ijk->k',ledger.outcross,pair_means)
                         + ledger.self_viable @ genes)/intensity
    retained = np.asarray([.5*(genes[positions[m]]+genes[positions[f]])
                           for _,m,f in parentage]).mean(axis=0) if nc else None
    observed = children.alleles.mean(axis=(0,2)) if nc else None
    adult = genes.mean(axis=0) if n else None
    traits = {}
    for name,locus in TRAITS.items():
        g = float(adult[locus]) if adult is not None else None
        m = float(expected[locus]) if expected is not None else None
        check_close(m,float(pair_expected[locus]) if pair_expected is not None else None,
                    'pair_expectation_'+name,errors)
        response = m-g if m is not None and g is not None else None
        check_close(saved['expected_'+name+'_change_pre_mutation'],response,
                    'expected_'+name+'_change_pre_mutation',errors)
        q = float(retained[locus]) if retained is not None else None
        y = float(observed[locus]) if observed is not None else None
        available = all(x is not None for x in (g,m,q,y))
        components = {'observed_change': y-g if available else None,
                      'expected_response': response,
                      'parent_sampling': q-m if available else None,
                      'segregation_mutation_remainder': y-q if available else None}
        if available:
            check_close(components['observed_change'],math.fsum(components[c] for c in COMPONENTS[1:]),
                        'transition_closure_'+name,errors)
        traits[name] = {'available':available,'adult_mean':g,'expected_child_mean':m,
                        'retained_pair_child_mean':q,'observed_child_mean':y,**components}
    return {'t':source['t'],'source_N':n,'next_N':nc,'traits':traits,'max_errors':errors,
            'retained_selfed':selfed,'retained_outcross':nc-selfed,
            'expected_seed_intensity':intensity,'kernel':poisson_capacity_kernel(intensity),
            'remainder_interpretation':('MENDELIAN_SEGREGATION' if mutation_rate == 0
                                        else 'COMBINED_SEGREGATION_AND_MUTATION')}


def summarize_windows(rows):
    require(len(rows)==400 and [r['t'] for r in rows] == list(range(400)), 'exact 400-update window required')
    result = {}
    for window,(start,end) in WINDOWS.items():
        result[window] = {}
        for locus in TRAITS:
            values = [r['traits'][locus] for r in rows[start:end]]
            valid = sum(v['available'] for v in values)
            sums = {c:math.fsum(v[c] for v in values) if valid==end-start else None for c in COMPONENTS}
            result[window][locus] = {'start':start,'end_exclusive':end,'updates':end-start,
                                   'valid_transitions':valid,'available':valid==end-start,**sums}
    for locus in TRAITS:
        for component in COMPONENTS:
            if result['full'][locus]['available']:
                check_close(result['full'][locus][component],
                            result['early'][locus][component]+result['late'][locus][component],
                            'phase_additivity_'+locus+'_'+component)
    return result


def admit_cohort(keys):
    expected = set(product(integrity.PROFILES,integrity.REPEATS,integrity.TIMINGS,
                           integrity.COSTS,integrity.MUTATIONS,integrity.SCHEDULES))
    require(len(keys)==len(expected) and len(set(keys))==len(expected) and set(keys)==expected,
            'cohort missing, duplicate, or unexpected identity combinations')
    return len(expected)

UPDATE_COLUMNS = ('t','source_N','next_N','expected_seed_intensity','retained_selfed',
                  'retained_outcross','p_zero','p_below_K','expected_next_N',
                  'expected_capacity_shortfall','fixed_state_zero_pollen_seed_intensity')
CENSUS_COLUMNS = ('t','N','X_mean','I_mean','A_mean')


def merge_errors(target, source):
    for name,value in source.items():
        target[name] = max(target.get(name,0.),value)


def demography_summary(censuses, updates):
    n = [c[1] for c in censuses]
    post = [c[1] for c in censuses[1:]]
    intensity = [r[3] for r in updates]
    selfed = sum(r[4] for r in updates)
    outcross = sum(r[5] for r in updates)
    total = selfed+outcross
    result = {'total_censuses_including_founder':len(n), 'post_update_censuses':len(post),
        'below_capacity_censuses':sum(v<48 for v in n),
        'post_update_below_capacity_censuses':sum(v<48 for v in post),
        'minimum_N':min(n),'ever_below_capacity':any(v<48 for v in n),
        'post_update_missing_recruit_slots':sum(48-v for v in post),
        'minimum_expected_seed_intensity':min(intensity),
        'mean_expected_seed_intensity':math.fsum(intensity)/len(intensity),
        'updates_expected_seed_intensity_below_capacity':sum(v<48 for v in intensity),
        'retained_selfed_total':selfed,'retained_outcross_total':outcross,
        'retained_recruit_total':total,
        'pooled_retained_selfed_fraction':selfed/total if total else None,
        'conditional_kernel':{name:{'minimum':min(r[j] for r in updates),
            'maximum':max(r[j] for r in updates),
            'mean':math.fsum(r[j] for r in updates)/len(updates),
            'sum_over_saved_states':math.fsum(r[j] for r in updates)}
            for j,name in enumerate(UPDATE_COLUMNS) if 6 <= j <= 9},
        'fixed_state_zero_pollen_bound':{'available':True,
            'minimum':min(r[10] for r in updates),
            'mean':math.fsum(r[10] for r in updates)/len(updates),
            'updates_below_capacity':sum(r[10]<48 for r in updates)}}
    return result


def analyze_case(record, cfg, plan):
    """Replay only native deterministic reproduction over this one saved case."""
    require(record['years']==400 and len(record['genetic_state_series'])==401
            and len(record['pollen_and_price_series'])==400 and len(record['trace'])==401,
            'incomplete 400-update case')
    require(cfg.capacity==48 and cfg.survival==0 and cfg.seed_arrival.supply==0
            and cfg.ovule_budget==8 and cfg.investment_cost==.5 and cfg.depression==.5
            and cfg.assurance_mode=='evolving', 'native demographic/bound constants changed')
    states = record['genetic_state_series']
    schedule = record['schedule']
    require(schedule in ('abrupt','gradual'), 'unregistered schedule')
    lambdas = plan['abrupt_lambdas'] if schedule=='abrupt' else plan['ramp_lambdas']
    start,end = np.asarray(plan['start_optima']),np.asarray(plan['end_optima'])
    censuses, transitions, updates, errors = [], [], [], {}
    for t,census in enumerate(states):
        require(type(census['t']) is int and census['t']==t, 'census timestamp mismatch')
        state = state_from_census(census)
        means = state.alleles.mean(axis=(0,2)) if len(state.ids) else None
        trace = record['trace'][t]
        require(isinstance(trace,list) and len(trace)==10, 'recorded census trace shape')
        check_close(trace[0],float(len(state.ids)),'trace_N',errors)
        for locus,name in enumerate(('X','I','A')):
            check_close(trace[1+locus],float(means[locus]) if means is not None else None,
                        'trace_mean_'+name,errors)
        censuses.append([t,len(state.ids),*([float(v) for v in means] if means is not None else [None]*3)])
        if t == 400:
            break
        saved = record['pollen_and_price_series'][t]
        lam = lambdas[t] if t<100 else 1.
        check_close(saved['lambda'],lam,'schedule_lambda',errors)
        ledger = reproduce(state,native.functional_visitors(start,end,lam),cfg)
        transition = account_transition(census,states[t+1],saved,ledger,
                                        mutation_rate=record['mutation_rate'])
        merge_errors(errors,transition['max_errors'])
        genes = state.alleles.mean(axis=2)
        bound = float(.5*np.sum(genes[:,2]*8*np.exp(-.5*genes[:,1]**2-cfg.assurance_cost*genes[:,2]**2)))
        check_close(bound,float(np.sum(genes[:,2]*ledger.ovules*(1-cfg.depression))),
                    'bound_native_ovules',errors)
        excess = max(0.,bound-transition['expected_seed_intensity'])
        require(excess<=TOL,'fixed-state zero-pollen bound exceeds native total intensity')
        errors['bound_excess'] = max(errors.get('bound_excess',0.),excess)
        updates.append([t,transition['source_N'],transition['next_N'],
            transition['expected_seed_intensity'],transition['retained_selfed'],transition['retained_outcross'],
            *[transition['kernel'][name] for name in UPDATE_COLUMNS[6:10]],bound])
        transitions.append(transition)
    windows = summarize_windows(transitions)
    for window,(begin,endtime) in WINDOWS.items():
        for locus,index in TRAITS.items():
            available = censuses[begin][index+2] is not None and censuses[endtime][index+2] is not None
            endpoint = censuses[endtime][index+2]-censuses[begin][index+2] if available else None
            entry = windows[window][locus]
            entry['endpoint_difference'] = endpoint
            if entry['available']:
                check_close(entry['observed_change'],endpoint,'window_endpoint_'+window+'_'+locus,errors)
                check_close(entry['observed_change'],math.fsum(entry[c] for c in COMPONENTS[1:]),
                            'window_component_closure_'+window+'_'+locus,errors)
    for locus in TRAITS:
        if windows['full'][locus]['available']:
            for component in COMPONENTS:
                check_close(windows['full'][locus][component],
                    windows['early'][locus][component]+windows['late'][locus][component],
                    'phase_additivity_'+locus+'_'+component,errors)
    return {'case':[record[field] for field in integrity.CASE_FIELDS],
        'windows':windows,'demography':demography_summary(censuses,updates),
        'censuses':censuses,'updates':updates,'max_errors':errors,
        'remainder_interpretation':transitions[0]['remainder_interpretation']}


def genetic_average(rows):
    result = {}
    for window in WINDOWS:
        result[window] = {}
        for locus in TRAITS:
            values = [r['windows'][window][locus] for r in rows]
            available = all(v['available'] for v in values)
            result[window][locus] = {'available':available,
                'valid_transition_count':sum(v.get('valid_transitions',v.get('valid_transition_count',0)) for v in values),
                **{c:math.fsum(v[c] for v in values)/len(values) if available else None for c in COMPONENTS}}
    return result


def aggregate_genetics(rows):
    grouped = {}
    for row in rows:
        profile,repeat,timing,cost,mutation,schedule = row['case']
        grouped.setdefault((profile,timing,cost,mutation,schedule),[]).append(row)
    profiles = []
    for key,values in sorted(grouped.items()):
        require(len(values)==4 and {v['case'][1] for v in values}==set(integrity.REPEATS),
                'profile needs exactly four repeats')
        profile,timing,cost,mutation,schedule = key
        profiles.append({'profile_seed':profile,'setting':[timing,cost,mutation],
            'schedule':schedule,'repeats':4,'windows':genetic_average(values)})
    grouped_settings = {}
    for row in profiles:
        grouped_settings.setdefault((*row['setting'],row['schedule']),[]).append(row)
    settings = []
    for key,values in sorted(grouped_settings.items()):
        require(len(values)==16 and {v['profile_seed'] for v in values}==set(integrity.PROFILES),
                'setting needs exactly sixteen profiles')
        settings.append({'setting':list(key[:3]),'schedule':key[3],'profiles':16,
                         'windows':genetic_average(values)})
    indexed = {(p['profile_seed'],*p['setting'],p['schedule']):p for p in profiles}
    pairs = []
    for setting in sorted({tuple(s['setting']) for s in settings}):
        windows = {}
        for window in WINDOWS:
            windows[window] = {}
            for locus in TRAITS:
                windows[window][locus] = {}
                for component in COMPONENTS:
                    differences = []
                    for p in integrity.PROFILES:
                        a = indexed[(p,*setting,'abrupt')]['windows'][window][locus][component]
                        g = indexed[(p,*setting,'gradual')]['windows'][window][locus][component]
                        differences.append(a-g if a is not None and g is not None else None)
                    available = all(v is not None for v in differences)
                    windows[window][locus][component] = {'available':available,
                        'mean_abrupt_minus_gradual':math.fsum(differences)/16 if available else None,
                        'profile_differences':differences,
                        'positive_profiles':sum(v>0 for v in differences) if available else None,
                        'negative_profiles':sum(v<0 for v in differences) if available else None,
                        'zero_profiles':sum(v==0 for v in differences) if available else None}
        pairs.append({'setting':list(setting),'profile_seeds':list(integrity.PROFILES),'windows':windows})
    return profiles,settings,pairs


def aggregate_demography(rows):
    values = [r['demography'] for r in rows]
    totals = ('total_censuses_including_founder','post_update_censuses','below_capacity_censuses',
              'post_update_below_capacity_censuses','post_update_missing_recruit_slots',
              'updates_expected_seed_intensity_below_capacity','retained_selfed_total',
              'retained_outcross_total','retained_recruit_total')
    result = {name:sum(v[name] for v in values) for name in totals}
    updates = result['post_update_censuses']
    case_fractions = [v['pooled_retained_selfed_fraction'] for v in values]
    result.update(cases=len(values),cases_ever_below_capacity=sum(v['ever_below_capacity'] for v in values),
        minimum_N=min(v['minimum_N'] for v in values),
        minimum_expected_seed_intensity=min(v['minimum_expected_seed_intensity'] for v in values),
        mean_expected_seed_intensity=math.fsum(v['mean_expected_seed_intensity']*v['post_update_censuses'] for v in values)/updates,
        pooled_retained_selfed_fraction=(result['retained_selfed_total']/result['retained_recruit_total']
                                         if result['retained_recruit_total'] else None),
        mean_case_retained_selfed_fraction=(math.fsum(case_fractions)/len(case_fractions)
                                            if all(v is not None for v in case_fractions) else None),
        cases_with_defined_selfed_fraction=sum(v is not None for v in case_fractions))
    result['conditional_kernel'] = {}
    for name in UPDATE_COLUMNS[6:10]:
        k = [v['conditional_kernel'][name] for v in values]
        total = math.fsum(v['sum_over_saved_states'] for v in k)
        result['conditional_kernel'][name] = {'minimum':min(v['minimum'] for v in k),
            'maximum':max(v['maximum'] for v in k),'mean':total/updates,'sum_over_saved_states':total}
    b = [v['fixed_state_zero_pollen_bound'] for v in values]
    result['fixed_state_zero_pollen_bound'] = {'available':all(v['available'] for v in b),
        'minimum':min(v['minimum'] for v in b),
        'mean':math.fsum(v['mean']*row['post_update_censuses'] for v,row in zip(b,values))/updates,
        'updates_below_capacity':sum(v['updates_below_capacity'] for v in b)}
    return result


def rehash_source_files(source_files, root=ROOT):
    hashes = {}
    for name,expected in sorted(source_files.items()):
        path = Path(name)
        require(not path.is_absolute() and '..' not in path.parts, 'unsafe source-relative path')
        digest = sha256((root/path).read_bytes()).hexdigest()
        require(digest==expected,'archived/current source mismatch: '+name)
        hashes[name] = digest
    return hashes


def validate_case_identity(record, receipt, case, raw_hash, proof):
    key = integrity.case_key(case)
    require(all(type(record[field]) is int for field in integrity.CASE_FIELDS[:2])
            and all(type(record[field]) in (int,float) for field in integrity.CASE_FIELDS[3:5])
            and all(type(record[field]) is str for field in ('mating_timing','schedule')),
            key+': incorrectly typed case identity')
    require(receipt['schema']=='chapter2_sequence_abrupt_gradual_case_receipt_v1'
            and receipt['sha256']==raw_hash and receipt['case']==list(case),key+': original receipt mismatch')
    for field in ('design_sha256','source_identity_sha256','source_file_sha256','runtime_identity'):
        require(receipt[field]==proof[field],key+': receipt '+field+' mismatch')
    founder = proof['founder_identity']
    require(receipt['founder_identity_sha256']==founder['digest'],key+': receipt founder mismatch')
    require(record['schema']=='chapter2_abrupt_gradual_original_model3_genetic_history_v1'
            and record['case_key']==key and [record[field] for field in integrity.CASE_FIELDS]==list(case),
            key+': archived case identity mismatch')
    require(record['frozen_design_sha256']==proof['design_sha256']
            and record['runtime_identity']==proof['runtime_identity'] and record['founder_identity']==founder,
            key+': case design/runtime/founder mismatch')
    require(record['years']==receipt['years']==400 and record['full_declared_case'] is True
            and receipt['full_declared_case'] is True,key+': incomplete/smoke case')
    initial = record['genetic_state_series'][0]
    require(initial['t']==0 and initial['adult_ids']==founder['arrays']['ids']
            and initial['diploid_alleles']==founder['arrays']['alleles'],key+': founder census mismatch')


def preflight(raw_root):
    """Small metadata and filename checks precede archived-state calculations."""
    root = Path(raw_root)
    design,design_hash = native.contract()
    require(design_hash==integrity.FROZEN_DESIGN_SHA256,'frozen design bytes changed')
    cases = integrity.expected_cases(design)
    admit_cohort(cases)
    official,official_hash = integrity.load_json(root/'readout/chapter2_functional_loss_tempo_readout.json')
    require(official['schema']=='chapter2_sequence_abrupt_gradual_full_source_readout_v1'
            and official['status']=='COMPLETE_SYNTHETIC_TEMPORAL_SEQUENCE_OUTCOME_SOURCE_ONLY_NOT_NATURAL_ECOLOGY'
            and official['total_verified_trajectory_cases']==1024
            and official['n_independent_synthetic_visitor_profiles']==16
            and official['n_nested_demographic_replicates_per_profile']==4
            and official['n_paired_setting_blocks']==8 and official['n_natural_plant_islands']==0,
            'official complete-cohort identity mismatch')
    require(official['design_sha256']==design_hash
            and official['verified_source_identity_sha256']==integrity.APPROVED_SOURCE_SHA256,
            'official design/source identity mismatch')
    sources = official['verified_source_file_sha256']
    require(integrity.mapping_digest(sources)==integrity.APPROVED_SOURCE_SHA256,'source mapping fingerprint mismatch')
    current_sources = rehash_source_files(sources)
    runtime,founder = official['execution_runtime_identity'],official['founder_identity']
    integrity.check_runtime(runtime)
    integrity.check_founder_identity(founder,runtime)
    execution,execution_hash = integrity.load_json(root/'execution_receipt.json')
    gate = execution['gate_evidence']
    require(execution['schema']=='chapter2_tempo_local_committed_main_execution_v1'
            and execution['expected_cases']==execution['receipted_case_count']==1024
            and execution['expected_updates_per_case']==400 and execution['expected_shards']==16
            and execution['runtime_identity']==runtime
            and gate['execution_source_identity_sha256']==integrity.APPROVED_SOURCE_SHA256
            and gate['frozen_design_sha256']==design_hash
            and gate['execution_source_commit']==integrity.REVIEWED_MAIN_COMMIT
            and gate['execution_source_tree']==integrity.REVIEWED_MAIN_TREE,
            'original execution receipt identity mismatch')
    require(len(execution['shards'])==16 and {s['shard_index'] for s in execution['shards']}==set(range(16))
            and all(s['exit_code']==0 for s in execution['shards']), 'original execution shards incomplete')
    manifest_names = {f'shard_{j:02d}_complete.json' for j in range(16)}
    expected_names = {integrity.case_key(c)+suffix for c in cases for suffix in ('.json','.receipt.json')}
    require({p.name for p in (root/'cases').glob('*.json')}==expected_names|manifest_names,
            'cohort case/receipt/manifest filenames missing, extra, or duplicated')
    manifests = {}
    for j in range(16):
        name = f'shard_{j:02d}_complete.json'
        manifest,digest = integrity.load_json(root/'cases'/name)
        require(manifest['schema']=='chapter2_sequence_abrupt_gradual_shard_manifest_v1'
                and manifest['status']=='COMPLETE_FROZEN_SHARD' and manifest['shard_index']==j
                and manifest['shard_count']==16 and manifest['case_count']==manifest['expected_full_case_count']==64
                and manifest['case_keys']==[integrity.case_key(c) for i,c in enumerate(cases) if i%16==j]
                and manifest['design_sha256']==design_hash
                and manifest['source_identity_sha256']==integrity.APPROVED_SOURCE_SHA256
                and manifest['runtime_identity']==runtime and manifest['founder_identity_sha256']==founder['digest'],
                'complete shard manifest mismatch: '+name)
        manifests[name] = digest
    require(manifests==execution['completed_shard_manifest_sha256'],'execution manifest hashes mismatch')
    proof = {'design_sha256':design_hash,'source_identity_sha256':integrity.APPROVED_SOURCE_SHA256,
        'source_file_sha256':sources,'runtime_identity':runtime,'founder_identity':founder,
        'original_readout_sha256':official_hash,'original_execution_receipt_sha256':execution_hash,
        'completed_shard_manifest_sha256':manifests,'rehashed_native_source_file_sha256':current_sources,
        'accounting_script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_integrity_helper_sha256':sha256(Path(integrity.__file__).read_bytes()).hexdigest(),
        'accounting_runtime_identity':native.runtime_identity()}
    return cases,proof


@lru_cache(maxsize=8)
def cached_config(timing,cost,mutation):
    return native.original_model_config(timing,cost,mutation,native.contract()[0])


def process_case(job):
    root,case,proof = job
    key = integrity.case_key(case)
    record,raw_hash = integrity.load_json(Path(root)/'cases'/(key+'.json'))
    receipt,receipt_hash = integrity.load_json(Path(root)/'cases'/(key+'.receipt.json'))
    validate_case_identity(record,receipt,case,raw_hash,proof)
    result = analyze_case(record,cached_config(*case[2:5]),native.profile_plan(case[0]))
    return {'case_key':key,'raw_sha256':raw_hash,'receipt_sha256':receipt_hash,**result}


def run_accounting(raw_root, workers=1):
    require(type(workers) is int and 1<=workers<=16,'workers must be 1..16')
    cases,proof = preflight(raw_root)
    results = []
    # Submission is explicitly bounded; no unbounded executor.map result queue.
    if workers == 1:
        for j,case in enumerate(cases,1):
            results.append(process_case((str(raw_root),case,proof)))
            if j%64==0:
                print(json.dumps({'accounted_cases':j,'expected_cases':1024}),flush=True)
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            for start in range(0,len(cases),workers):
                jobs = [pool.submit(process_case,(str(raw_root),c,proof)) for c in cases[start:start+workers]]
                results.extend(job.result() for job in jobs)
                completed = start+len(jobs)
                if completed//64 > start//64:
                    print(json.dumps({'accounted_cases':completed,'expected_cases':1024}),flush=True)
    results.sort(key=lambda r:tuple(r['case']))
    admit_cohort([tuple(r['case']) for r in results])
    profiles,settings,pairs = aggregate_genetics(results)
    require(len(profiles)==256 and len(settings)==16 and len(pairs)==8,'aggregate coverage mismatch')
    errors = {}
    for row in results:
        merge_errors(errors,row['max_errors'])
    arms = []
    for setting in settings:
        arm = [r for r in results if r['case'][2:5]==setting['setting'] and r['case'][5]==setting['schedule']]
        arms.append({'setting':setting['setting'],'schedule':setting['schedule'],**aggregate_demography(arm)})
    available_by_locus = {locus:sum(r['windows']['full'][locus]['valid_transitions'] for r in results)
                           for locus in TRAITS}
    return {'schema':SCHEMA,'evidence_rank':EVIDENCE_RANK,'status':'PASS_COMPLETE_ARCHIVED_COHORT_ACCOUNTING',
        'provenance':proof,'case_count':len(results),'updates_per_case':400,'profile_count':16,
        'repeats_per_profile':4,'setting_schedule_count':16,'paired_setting_count':8,
        'valid_source_child_transitions_by_locus':available_by_locus,'max_numerical_errors':errors,
        'comparison_absolute_tolerance':TOL,
        'all_case_inputs_sha256':integrity.mapping_digest({r['case_key']:{'raw':r['raw_sha256'],'receipt':r['receipt_sha256']} for r in results}),
        'census_columns':list(CENSUS_COLUMNS),'update_columns':list(UPDATE_COLUMNS),
        'component_units':'signed diploid trait mean change; phase sums in trait units',
        'aggregation':'four-repeat arithmetic means within profile, then equal means across sixteen profiles',
        'windows':{name:list(bounds) for name,bounds in WINDOWS.items()},
        'interpretation_limits':[
            'Existing cohort accounting only; parent-pair sampling is descriptive, not a controlled causal effect.',
            'Nonzero-mutation residual combines Mendelian segregation and mutation; homolog draws and pre-mutation offspring are unavailable.',
            'Empty-population trait means/components are unavailable, never zero-filled; aggregates require all transitions.',
            'Poisson kernel is conditional on each saved source state, not a multigeneration survival probability; risks are not multiplied.',
            'Expected viable seed intensity differs from retained offspring counts; uncapped candidate counts were not retained.',
            'Fixed-state zero-pollen intensity is an algebraic lower bound on current native total intensity, not a run future or retained self count.',
            'No intervals, p-values, independent ecological replication, or natural-island interpretation.'],
        'demography':{'overall':aggregate_demography(results),'setting_schedule_arms':arms},
        'profile_means':profiles,'setting_schedule_summaries':settings,
        'paired_abrupt_minus_gradual':pairs,'case_summaries':results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw-root',type=Path,required=True)
    parser.add_argument('--output-json',type=Path,required=True)
    parser.add_argument('--workers',type=int,default=1)
    args = parser.parse_args()
    require(not args.output_json.exists(),'output already exists; preserve it and choose a new path')
    result = run_accounting(args.raw_root,args.workers)
    args.output_json.parent.mkdir(parents=True,exist_ok=True)
    temporary = args.output_json.with_suffix(args.output_json.suffix+'.tmp')
    with temporary.open('x',encoding='utf-8') as handle:
        json.dump(result,handle,sort_keys=True,separators=(',',':'),allow_nan=False)
        handle.write('\n')
    # Exclusive final creation prevents a concurrent writer from being overwritten.
    os.link(temporary,args.output_json)
    temporary.unlink()
    print(json.dumps({'status':result['status'],'output_json':str(args.output_json),'case_count':1024}),flush=True)


if __name__ == '__main__':
    main()
