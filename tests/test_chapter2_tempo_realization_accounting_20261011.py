"""Bounded tests: retained IDs, archived expectations, admission and count kernel."""
import copy
import importlib
from itertools import product
import math
from pathlib import Path

import numpy as np
import pytest
from scipy.stats import poisson

NAME = 'scripts.audit_chapter2_tempo_realization_accounting_20261011'


def test_accounting_module_exists():
    assert Path(NAME.replace('.', '/') + '.py').exists(), 'accounting implementation is absent'


@pytest.fixture
def audit():
    if not Path(NAME.replace('.', '/') + '.py').exists():
        pytest.skip('implementation absent; see explicit presence test')
    return importlib.import_module(NAME)


def census(t, ids, traits):
    genes = np.repeat(np.asarray(traits, dtype=float)[:, :, None], 2, axis=2)
    return {'t': t, 'adult_ids': ids, 'diploid_alleles': genes.tolist()}


def known_example(audit):
    from scripts.model3_island.types import Ledger
    source = census(0, [90, 11, 57], [[.5,.2,.9],[.5,.8,.1],[.5,.5,.3]])
    child = census(1, [205, 301], [[.5,.7,.4],[.5,.3,.8]])
    cross = np.array([[0.,2.,0.],[0.,0.,0.],[1.,0.,0.]])
    ledger = Ledger(outcross=cross, self_raw=np.array([0.,2.,0.]),
                    self_viable=np.array([0.,1.,0.]), ovules=np.ones(3)*8,
                    exported=np.ones(3), delivered=np.zeros((3,3)), lost=np.ones(3),
                    maternal=cross.sum(axis=0)+[0,1,0], paternal=cross.sum(axis=1)+[0,1,0])
    row = {'t':0,'N':3,'delivered':0.,'outcross':3.,'viable_self':1.,
           'expected_I_change_pre_mutation':.0375,
           'expected_A_change_pre_mutation':.425-1.3/3,
           'parentage':[[301,90,90],[205,11,57]],
           'resident_selfed_recruits':1,'resident_outcross_recruits':1}
    return source, child, row, ledger


def test_shuffled_nonsequential_ids_use_retained_pairs(audit):
    source, child, row, ledger = known_example(audit)
    result = audit.account_transition(source, child, row, ledger, mutation_rate=0.)
    i, a = result['traits']['I'], result['traits']['A']
    assert i['adult_mean'] == pytest.approx(.5)
    assert i['expected_child_mean'] == pytest.approx(.5375)
    assert i['retained_pair_child_mean'] == pytest.approx(.425)
    assert i['observed_child_mean'] == pytest.approx(.5)
    assert i['parent_sampling'] == pytest.approx(-.1125)
    assert i['segregation_mutation_remainder'] == pytest.approx(.075)
    assert a['retained_pair_child_mean'] == pytest.approx(.55)
    assert a['segregation_mutation_remainder'] == pytest.approx(.05)
    assert result['remainder_interpretation'] == 'MENDELIAN_SEGREGATION'


@pytest.mark.parametrize('corruption', ['source_duplicate','missing_parent','child_duplicate','missing_child','count'])
def test_invalid_parent_or_child_linkage_fails_closed(audit, corruption):
    source, child, row, ledger = known_example(audit)
    if corruption == 'source_duplicate': source['adult_ids'][1] = 90
    elif corruption == 'missing_parent': row['parentage'][0][1] = 99
    elif corruption == 'child_duplicate': row['parentage'][1][0] = 301
    elif corruption == 'missing_child': row['parentage'][0][0] = 999
    else: row['resident_selfed_recruits'] = 0
    with pytest.raises(ValueError):
        audit.account_transition(source, child, row, ledger, mutation_rate=0.)


def test_empty_child_is_unavailable_and_mutation_label_is_combined(audit):
    source, child, row, ledger = known_example(audit)
    active = audit.account_transition(source, child, row, ledger, mutation_rate=.01)
    assert active['remainder_interpretation'] == 'COMBINED_SEGREGATION_AND_MUTATION'
    child = {'t':1,'adult_ids':[],'diploid_alleles':[]}
    row.update(parentage=[], resident_selfed_recruits=0, resident_outcross_recruits=0)
    empty = audit.account_transition(source, child, row, ledger, mutation_rate=.01)
    for trait in empty['traits'].values():
        assert trait['available'] is False
        assert trait['observed_change'] is None
        assert trait['segregation_mutation_remainder'] is None
        assert trait['expected_child_mean'] is not None


@pytest.mark.parametrize('field', ['expected_I_change_pre_mutation','delivered','outcross','viable_self'])
def test_source_expectation_or_used_quantity_corruption_fails(audit, field):
    source, child, row, ledger = known_example(audit)
    row[field] += .001
    with pytest.raises(ValueError, match=field):
        audit.account_transition(source, child, row, ledger, mutation_rate=0.)


@pytest.mark.parametrize('intensity', [0., 1., 36., 48., 75., 160., 320., 1200.])
def test_kernel_matches_independent_scipy_pmf(audit, intensity):
    result = audit.poisson_capacity_kernel(intensity)
    r = np.arange(48)
    pmf = poisson.pmf(r, intensity)
    shortfall = math.fsum(((48-r)*pmf).tolist())
    expected = math.fsum((r*pmf).tolist()) + 48*poisson.sf(47, intensity)
    assert result['p_zero'] == pytest.approx(math.exp(-intensity), rel=1e-13, abs=0)
    assert result['p_below_K'] == pytest.approx(poisson.cdf(47,intensity), rel=2e-12, abs=0)
    assert result['expected_capacity_shortfall'] == pytest.approx(shortfall, rel=2e-12, abs=0)
    assert result['expected_next_N'] == pytest.approx(expected, abs=2e-12)
    if intensity == 320:
        assert result['expected_next_N'] == 48.
        assert result['expected_capacity_shortfall'] > 0.


def test_unequal_phase_lengths_preserve_trait_unit_totals(audit):
    rows = []
    for t in range(400):
        observed = .001 if t < 100 else -.0002
        traits = {locus:dict(available=True, observed_change=observed,
            expected_response=observed/2, parent_sampling=observed/4,
            segregation_mutation_remainder=observed/4) for locus in ['I','A']}
        rows.append({'t':t,'traits':traits})
    result = audit.summarize_windows(rows)
    assert result['early']['I']['observed_change'] == pytest.approx(.1)
    assert result['late']['I']['observed_change'] == pytest.approx(-.06)
    assert result['full']['I']['observed_change'] == pytest.approx(.04)
    assert result['full']['I']['valid_transitions'] == 400
    assert result['late']['I']['valid_transitions'] == 300


def test_cohort_admission_rejects_missing_and_duplicate_combinations(audit):
    keys = list(product(range(48271001,48271017), range(49271001,49271005),
                        ['delayed','prior'],[0,.5],[0,.01],['abrupt','gradual']))
    assert audit.admit_cohort(keys) == 1024
    with pytest.raises(ValueError, match='cohort'): audit.admit_cohort(keys[:-1])
    with pytest.raises(ValueError, match='cohort'): audit.admit_cohort(keys[:-1]+[keys[0]])


def archived_constant_case(audit):
    # Deterministic reproduction only; no simulation, inheritance or advance.
    from scripts.model3_island.reproduction import reproduce
    d, _ = audit.native.contract()
    cfg = audit.native.original_model_config('delayed',.5,.01,d)
    plan = audit.native.profile_plan(48271001)
    record = {'mutation_rate':.01,'mating_timing':'delayed','direct_assurance_cost':.5,
              'schedule':'gradual','history_profile_seed':48271001,
              'nested_demography_seed':49271001,'years':400,
              'genetic_state_series':[], 'pollen_and_price_series':[], 'trace':[]}
    for t in range(401):
        c = census(t,[90+t*100,11+t*100,57+t*100],[[.5,.2,.9],[.5,.8,.1],[.5,.5,.3]])
        record['genetic_state_series'].append(c)
        record['trace'].append([3.,.5,.5,1.3/3,0,0,0,0,0,0])
        if t == 400: break
        state = audit.state_from_census(c)
        lam = plan['ramp_lambdas'][t] if t < 100 else 1.
        visitors = audit.native.functional_visitors(np.array(plan['start_optima']),np.array(plan['end_optima']),lam)
        ledger = reproduce(state,visitors,cfg)
        e_i,e_a = audit.native.expected_source_allele_response(state,ledger)
        record['pollen_and_price_series'].append({'t':t,'N':3,'lambda':lam,
            'delivered':float(ledger.delivered.sum()),'outcross':float(ledger.outcross.sum()),
            'viable_self':float(ledger.self_viable.sum()),'expected_I_change_pre_mutation':e_i,
            'expected_A_change_pre_mutation':e_a,
            'parentage':[[90+(t+1)*100,90+t*100,90+t*100],
                         [11+(t+1)*100,11+t*100,11+t*100],
                         [57+(t+1)*100,57+t*100,57+t*100]],
            'resident_selfed_recruits':3,'resident_outcross_recruits':0})
    return record,cfg,plan


def test_complete_case_native_replay_demographic_denominators_and_bound(audit):
    record,cfg,plan = archived_constant_case(audit)
    result = audit.analyze_case(record,cfg,plan)
    assert result['windows']['full']['I']['observed_change'] == 0.
    assert result['windows']['early']['I']['endpoint_difference'] == 0.
    assert result['demography']['total_censuses_including_founder'] == 401
    assert result['demography']['post_update_censuses'] == 400
    assert result['demography']['below_capacity_censuses'] == 401
    assert result['demography']['post_update_missing_recruit_slots'] == 400*45
    assert result['demography']['retained_selfed_total'] == 1200
    assert result['demography']['pooled_retained_selfed_fraction'] == 1.
    assert result['demography']['fixed_state_zero_pollen_bound']['available'] is True
    assert result['max_errors']['bound_excess'] == 0.
    assert len(result['updates']) == 400
    assert len(result['censuses']) == 401


@pytest.mark.parametrize('corruption', ['trace_mean','schedule','timestamp','nonfinite'])
def test_case_rejects_trace_schedule_timestamp_and_nonfinite_corruption(audit,corruption):
    record,cfg,plan = archived_constant_case(audit)
    if corruption == 'trace_mean': record['trace'][3][2] += .01
    elif corruption == 'schedule': record['pollen_and_price_series'][3]['lambda'] += .01
    elif corruption == 'timestamp': record['genetic_state_series'][3]['t'] = 4
    else: record['genetic_state_series'][3]['diploid_alleles'][0][1][0] = float('nan')
    with pytest.raises(ValueError): audit.analyze_case(record,cfg,plan)


def test_aggregate_four_repeats_then_profiles_and_paired_support(audit):
    rows = []
    for profile,repeat,schedule in product(range(48271001,48271017),range(49271001,49271005),['abrupt','gradual']):
        value = (profile-48271000)*.01 + (repeat-49271000)*.001 + (.2 if schedule=='abrupt' else 0.)
        windows = {name:{locus:{'available':True,'valid_transitions':end-start,
            **{c:value*(end-start) for c in audit.COMPONENTS}} for locus in ['I','A']}
            for name,(start,end) in audit.WINDOWS.items()}
        rows.append({'case':[profile,repeat,'delayed',0.,0.,schedule],'windows':windows})
    profiles,settings,pairs = audit.aggregate_genetics(rows)
    assert len(profiles) == 32 and len(settings) == 2 and len(pairs) == 1
    assert settings[0]['profiles'] == 16
    assert pairs[0]['windows']['full']['I']['observed_change']['mean_abrupt_minus_gradual'] == pytest.approx(80.)
    assert len(pairs[0]['windows']['full']['I']['observed_change']['profile_differences']) == 16
    assert pairs[0]['windows']['full']['I']['observed_change']['positive_profiles'] == 16
    assert pairs[0]['windows']['late']['I']['observed_change']['mean_abrupt_minus_gradual'] == pytest.approx(60.)


def provenance_example(audit):
    source,child,saved,ledger = known_example(audit)
    key = (48271001,49271001,'delayed',0.,0.,'abrupt')
    founder = {'digest':'founder','arrays':{'ids':source['adult_ids'],'alleles':copy.deepcopy(source['diploid_alleles'])}}
    proof = {'design_sha256':'design','source_identity_sha256':'source','source_file_sha256':{'scripts/x.py':'x'},
             'runtime_identity':{'python':'archived'},'founder_identity':founder}
    record = {'schema':'chapter2_abrupt_gradual_original_model3_genetic_history_v1',
              'case_key':audit.integrity.case_key(key),'frozen_design_sha256':'design',
              'founder_identity':founder,'runtime_identity':proof['runtime_identity'],
              'years':400,'full_declared_case':True,'genetic_state_series':[source],
              **dict(zip(audit.integrity.CASE_FIELDS,key))}
    receipt = {'schema':'chapter2_sequence_abrupt_gradual_case_receipt_v1','case':list(key),
              'sha256':'raw','design_sha256':'design','source_identity_sha256':'source',
              'source_file_sha256':proof['source_file_sha256'],'runtime_identity':proof['runtime_identity'],
              'founder_identity_sha256':'founder','years':400,'full_declared_case':True}
    return record,receipt,key,proof


def test_receipt_and_initial_founder_identity_are_checked(audit):
    record,receipt,key,proof = provenance_example(audit)
    audit.validate_case_identity(record,receipt,key,'raw',proof)
    receipt['sha256'] = 'other'
    with pytest.raises(ValueError): audit.validate_case_identity(record,receipt,key,'raw',proof)
    receipt['sha256'] = 'raw'
    record['genetic_state_series'][0]['diploid_alleles'][0][1][0] += .01
    with pytest.raises(ValueError): audit.validate_case_identity(record,receipt,key,'raw',proof)


def test_demographic_aggregate_distinguishes_pooled_and_mean_case_fractions(audit):
    rows = []
    for s,o in [(1,1),(9,0)]:
        census_rows = [[0,2,.5,.5,.5],[1,s+o,.5,.5,.5]]
        update_rows = [[0,2,s+o,48.,s,o,.01,.1,47.,1.,30.]]
        rows.append({'demography':audit.demography_summary(census_rows,update_rows)})
    result = audit.aggregate_demography(rows)
    assert result['pooled_retained_selfed_fraction'] == pytest.approx(10/11)
    assert result['mean_case_retained_selfed_fraction'] == pytest.approx(.75)
    assert result['cases_ever_below_capacity'] == 2
    assert result['total_censuses_including_founder'] == 4
    assert result['post_update_censuses'] == 2


def test_unsafe_or_corrupt_source_fingerprint_is_rejected(audit,tmp_path):
    (tmp_path/'safe.py').write_text('source')
    digest = audit.sha256(b'source').hexdigest()
    assert audit.rehash_source_files({'safe.py':digest},tmp_path) == {'safe.py':digest}
    with pytest.raises(ValueError): audit.rehash_source_files({'../escape':digest},tmp_path)
    with pytest.raises(ValueError): audit.rehash_source_files({'safe.py':'wrong'},tmp_path)


@pytest.mark.parametrize('field', ['history_profile_seed','nested_demography_seed','direct_assurance_cost','mutation_rate'])
def test_boolean_or_float_seed_case_identity_fails_closed(audit,field):
    record,receipt,key,proof = provenance_example(audit)
    record[field] = float(record[field]) if field.endswith('_seed') else False
    with pytest.raises(ValueError): audit.validate_case_identity(record,receipt,key,'raw',proof)


def test_kernel_preserves_tiny_positive_expected_census(audit):
    result = audit.poisson_capacity_kernel(1e-30)
    assert result['expected_next_N'] == pytest.approx(1e-30,rel=1e-12,abs=0)
