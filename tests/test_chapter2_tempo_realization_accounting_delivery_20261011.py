"""Delivery evidence uses asymmetric synthetic summaries, never new histories."""
import copy
import gzip
import importlib
from itertools import product
import json
from pathlib import Path

import pytest

NAME = 'scripts.tabulate_chapter2_tempo_realization_accounting_20261011'


@pytest.fixture
def delivery():
    return importlib.import_module(NAME)


def pair_fixture(d):
    """Small scalar summaries for the exact identity grid; annual arrays are tiny."""
    proof = {'design_sha256':d.DESIGN_SHA,'source_identity_sha256':d.SOURCE_SHA,
             'founder_identity':{'digest':'f'*64},'runtime_identity':{'runtime':'original'},
             'source_file_sha256':{'scripts/native.py':'a'*64},
             'completed_shard_manifest_sha256':{f'shard_{i:02d}_complete.json':f'{i:064x}' for i in range(16)}}
    native = {'schema':d.NATIVE_SCHEMA,'status':d.NATIVE_STATUS,'provenance':proof,
              'case_count':1024,'updates_per_case':400,'profile_count':16,'repeats_per_profile':4,
              'setting_schedule_count':16,'paired_setting_count':8,
              'valid_source_child_transitions_by_locus':{'I':409600,'A':409600},
              'case_summaries':[], 'profile_means':[], 'setting_schedule_summaries':[],
              'paired_abrupt_minus_gradual':[], 'custom_preserved_field':{'keep':'all fields'},
              'demography':{'overall':{},'setting_schedule_arms':[]}}
    independent = {'schema':d.INDEPENDENT_SCHEMA,'status':d.INDEPENDENT_STATUS,
        'frozen_design_sha256':d.DESIGN_SHA,'execution_source_identity_sha256':d.SOURCE_SHA,
        'manifest_sha256':proof['completed_shard_manifest_sha256'],
        'uniform_source_founder_runtime':{'design_sha256':d.DESIGN_SHA,'source_identity_sha256':d.SOURCE_SHA,
            'founder_identity_sha256':'f'*64,'runtime_sha256':d.stable_sha(proof['runtime_identity']),
            'source_file_map_sha256':d.stable_sha(proof['source_file_sha256'])},
        'scope':{'raw_case_sha256_verified_count':1024,'case_receipts':1024,'profile_units':16,
                 'nested_repeats_per_profile':4,'arms':16,'source_updates':409600,'trait_update_accountings':819200,
                 'missing_accounting_updates':0,'missing_or_filtered_cases':0},
        'cases':[],'profile_arm_summaries':[],'arm_summaries':[],
        'abrupt_minus_gradual':[],'paired_profile_contrasts':[]}

    def windows(base, kind='case'):
        a,b = {},{}
        for name,ind_name in d.WINDOW_MAP.items():
            a[name],b[ind_name] = {},{}
            length = d.WINDOW_LENGTH[name]
            for locus_index,locus in enumerate(d.TRAITS):
                values = [base*length*(1+locus_index*.7)*(1+component_index*.13) for component_index in range(4)]
                a[name][locus] = dict(zip(d.COMPONENT_MAP,values))
                b[ind_name][locus] = dict(zip(d.COMPONENT_MAP.values(),values))
                if kind=='case': a[name][locus].update(available=True,valid_transitions=length)
                else: a[name][locus].update(available=True,valid_transition_count=length*(4 if kind=='profile' else 64))
        return a,b

    for key in d.expected_cases():
        p,r,t,c,m,s = key
        base = ((p-48271000)*.011+(r-49271000)*.003+(s=='abrupt')*(.02+(p-48271000)*.001)+c*.07+m*.11+(t=='prior')*.013)
        a,b = windows(base)
        case_key = d.case_key(key)
        hashes = {'raw_sha256':d.sha256(('raw'+case_key).encode()).hexdigest(),
                  'receipt_sha256':d.sha256(('receipt'+case_key).encode()).hexdigest()}
        native['case_summaries'].append({'case':list(key),'case_key':case_key,**hashes,'windows':a,
            'censuses':[[0,48,.5,.5,.5]],'updates':[[0,48,48]],'demography':{'preserve':p}})
        independent['cases'].append({'case':list(key),'case_key':case_key,**hashes,'windows':b,
            'availability':{'complete_accounting_updates':400,'missing_accounting_updates':0,
                            'source_updates':400,'genomic_censuses':401}})
    for p,t,c,m,s in product(d.PROFILES,d.TIMINGS,d.COSTS,d.MUTATIONS,d.SCHEDULES):
        base = (p-48271000)*.011+2.5*.003+(s=='abrupt')*(.02+(p-48271000)*.001)+c*.07+m*.11+(t=='prior')*.013
        a,b = windows(base,'profile')
        native['profile_means'].append({'profile_seed':p,'setting':[t,c,m],'schedule':s,'repeats':4,'windows':a})
        independent['profile_arm_summaries'].append({'history_profile_seed':p,'mating_timing':t,
            'direct_assurance_cost':c,'mutation_rate':m,'schedule':s,'n_nested_repeats':4,'windows':b})
    for t,c,m,s in product(d.TIMINGS,d.COSTS,d.MUTATIONS,d.SCHEDULES):
        base = 8.5*.011+2.5*.003+(s=='abrupt')*.0285+c*.07+m*.11+(t=='prior')*.013
        a,b = windows(base,'arm')
        native['setting_schedule_summaries'].append({'setting':[t,c,m],'schedule':s,'profiles':16,'windows':a})
        independent['arm_summaries'].append({'mating_timing':t,'direct_assurance_cost':c,'mutation_rate':m,
            'schedule':s,'n_profiles':16,'n_cases':64,'n_updates_per_trait':25600,'windows':b})
    for t,c,m in product(d.TIMINGS,d.COSTS,d.MUTATIONS):
        a,b = windows(.0285,'arm')
        native['paired_abrupt_minus_gradual'].append({'setting':[t,c,m],'profile_seeds':list(d.PROFILES),
            'windows':{w:{l:{component:{'available':True,'mean_abrupt_minus_gradual':a[w][l][component],
                'profile_differences':[windows(.02+(p-48271000)*.001,'arm')[0][w][l][component] for p in d.PROFILES]} for component in d.COMPONENT_MAP}
                for l in d.TRAITS} for w in d.WINDOW_MAP}})
        independent['abrupt_minus_gradual'].append({'mating_timing':t,'direct_assurance_cost':c,'mutation_rate':m,
            'n_paired_profiles':16,'n_paired_repeats':64,'contrast':'abrupt_minus_gradual','windows':b})
        for p in d.PROFILES:
            independent['paired_profile_contrasts'].append({'history_profile_seed':p,'mating_timing':t,
                'direct_assurance_cost':c,'mutation_rate':m,'n_paired_repeats':4,'contrast':'abrupt_minus_gradual','windows':windows(.02+(p-48271000)*.001,'arm')[1]})
    return native,independent


def test_exact_asymmetric_cohort_comparison_counts(delivery):
    a,b = pair_fixture(delivery)
    result = delivery.compare_accountings(a,b)
    assert result['status'] == 'PASS_COMPLETE_NATIVE_TO_INDEPENDENT_ACCOUNTING_COMPARISON'
    assert result['checked_counts'] == {'cases':1024,'case_sha256_pairs':1024,'case_identity_values':6144,
        'case_component_values':24576,'profile_means':256,'profile_component_values':6144,
        'setting_schedule_arms':16,'arm_component_values':384,'paired_setting_means':8,
        'paired_mean_component_values':192,'paired_profile_contrasts':128,'paired_profile_component_values':3072,
        'total_component_values':34368}
    assert result['max_absolute_error'] < 1e-11


@pytest.mark.parametrize('damage', ['case_value','profile_value','arm_value','paired_mean','paired_profile',
    'missing_case','duplicate_case','extra_case','missing_profile','duplicate_arm','missing_pair',
    'missing_profile_pair','missing_window','extra_window','missing_trait','extra_component','unavailable','hash','identifier','source','manifest'])
def test_missing_altered_duplicate_or_unavailable_evidence_fails(delivery,damage):
    a,b = pair_fixture(delivery)
    if damage=='case_value': b['cases'][0]['windows']['updates_0_99']['I']['stored_source_expectation_sum'] += .1
    elif damage=='profile_value': b['profile_arm_summaries'][0]['windows']['full400']['A']['realized_parent_allocation_sum'] += .1
    elif damage=='arm_value': b['arm_summaries'][0]['windows']['updates_100_399']['I']['observed_change'] += .1
    elif damage=='paired_mean': b['abrupt_minus_gradual'][0]['windows']['full400']['I']['observed_change'] += .1
    elif damage=='paired_profile': b['paired_profile_contrasts'][0]['windows']['updates_0_99']['A']['segregation_mutation_remainder_sum'] += .1
    elif damage=='missing_case': b['cases'].pop()
    elif damage=='duplicate_case': b['cases'][-1] = b['cases'][0]
    elif damage=='extra_case': b['cases'].append(copy.deepcopy(b['cases'][0]))
    elif damage=='missing_profile': b['profile_arm_summaries'].pop()
    elif damage=='duplicate_arm': b['arm_summaries'][-1] = b['arm_summaries'][0]
    elif damage=='missing_pair': b['abrupt_minus_gradual'].pop()
    elif damage=='missing_profile_pair': b['paired_profile_contrasts'].pop()
    elif damage=='missing_window': b['cases'][0]['windows'].pop('updates_0_99')
    elif damage=='extra_window': b['cases'][0]['windows']['additional'] = {}
    elif damage=='missing_trait': b['cases'][0]['windows']['full400'].pop('A')
    elif damage=='extra_component': b['profile_arm_summaries'][0]['windows']['full400']['I']['unregistered_component'] = 0.
    elif damage=='unavailable': a['case_summaries'][0]['windows']['full']['I']['available'] = False
    elif damage=='hash': b['cases'][0]['receipt_sha256'] = '0'*64
    elif damage=='identifier': b['cases'][0]['case'][0] = 48271999
    elif damage=='source': b['uniform_source_founder_runtime']['source_file_map_sha256'] = '0'*64
    else: b['manifest_sha256'] = dict(b['manifest_sha256'],shard_00_complete='0'*64)
    with pytest.raises((ValueError,KeyError)): delivery.compare_accountings(a,b)


def test_projection_preserves_every_field_except_named_annual_arrays(delivery,tmp_path):
    a,b = pair_fixture(delivery)
    original = copy.deepcopy(a)
    projection = delivery.summary_projection(a,'9'*64,123456)
    assert a == original
    assert projection['schema'] == 'chapter2_tempo_realization_summary_v1'
    assert projection['delivery_projection']['omitted_fields'] == ['case_summaries[*].censuses','case_summaries[*].updates']
    assert projection['delivery_projection']['full_accounting_json_sha256'] == '9'*64
    assert projection['delivery_projection']['annual_arrays_reconstructible_from_summary_alone'] is False
    for field in a:
        if field not in ('schema','case_summaries'): assert projection[field] == a[field]
    for source,row in zip(a['case_summaries'],projection['case_summaries']):
        assert row == {k:v for k,v in source.items() if k not in ('censuses','updates')}
    first,second = tmp_path/'a.gz',tmp_path/'b.gz'
    delivery.write_deterministic_gzip(projection,first)
    delivery.write_deterministic_gzip(projection,second)
    assert first.read_bytes() == second.read_bytes()
    assert json.loads(gzip.decompress(first.read_bytes())) == projection
    assert first.read_bytes()[4:8] == b'\x00'*4
    with pytest.raises(FileExistsError): delivery.write_deterministic_gzip(projection,first)


def table_fixture(d):
    a,b = pair_fixture(d)
    for j,row in enumerate(b['cases']):
        row['saved_order_unmodified'] = {'order':d.CATEGORIES[j%6],'order_by100':d.CATEGORIES[(j+1)%6]}
        row['terminal_I_descriptors_not_new_categories'] = {name:bool((j+i)%3==0) for i,name in enumerate(d.TERMINAL_FIELDS)}
    for row in b['arm_summaries']:
        selected = [c for c in b['cases'] if c['case'][2:] == [*d.setting(row),row['schedule']]]
        row['saved_full400_order_counts'] = {name:sum(c['saved_order_unmodified']['order']==name for c in selected) for name in d.CATEGORIES}
        row['saved_by100_order_counts'] = {name:sum(c['saved_order_unmodified']['order_by100']==name for c in selected) for name in d.CATEGORIES}
        row['terminal_I_descriptor_counts_not_new_categories'] = {name:sum(c['terminal_I_descriptors_not_new_categories'][name] for c in selected) for name in d.TERMINAL_FIELDS}

    def demographics(cases=64):
        return {'cases':cases,'total_censuses_including_founder':401*cases,'post_update_censuses':400*cases,
            'below_capacity_censuses':2,'post_update_below_capacity_censuses':2,'minimum_N':46,
            'cases_ever_below_capacity':1,'post_update_missing_recruit_slots':3,
            'minimum_expected_seed_intensity':47.,'mean_expected_seed_intensity':140.,
            'updates_expected_seed_intensity_below_capacity':1,
            'retained_selfed_total':400*cases*12,'retained_outcross_total':400*cases*36,
            'retained_recruit_total':400*cases*48,'pooled_retained_selfed_fraction':.25,
            'mean_case_retained_selfed_fraction':.27,'cases_with_defined_selfed_fraction':cases,
            'conditional_kernel':{name:{'minimum':.0001,'maximum':.1,'mean':.005,
                'sum_over_saved_states':.005*400*cases} for name in d.KERNEL_FIELDS},
            'fixed_state_zero_pollen_bound':{'available':True,'minimum':24.,'mean':88.,'updates_below_capacity':3}}
    a['demography']['overall'] = demographics(1024)
    a['demography']['setting_schedule_arms'] = [{'setting':[t,c,m],'schedule':s,**demographics()}
        for t,c,m,s in product(d.TIMINGS,d.COSTS,d.MUTATIONS,d.SCHEDULES)]
    return a,b


def test_all_tables_have_complete_arm_setting_demographic_and_original_descriptor_rows(delivery):
    a,b = table_fixture(delivery)
    text = delivery.render_tables(a,b)
    assert text.count('## Genetic arm means:') == 6
    assert text.count('## Paired abrupt minus gradual:') == 6
    assert '4 nested repeats' in text and '16 profiles' in text
    assert 'signed trait units' in text and 'No confidence intervals' in text
    assert 'controlled causal mediation' in text
    assert 'ratio of pooled retained counts' in text and 'mean case selfed fraction' in text
    assert 'conditional one-step' in text and 'not multigeneration survival' in text
    assert 'Supplementary terminal-I descriptors' in text
    assert 'saved categories' in text and 'new event classes' in text
    for t,c,m,s in product(delivery.TIMINGS,delivery.COSTS,delivery.MUTATIONS,delivery.SCHEDULES):
        assert f'| {t} | {c:g} | {m:g} | {s} |' in text
    assert 'overall' in text


def test_terminal_counts_are_copied_and_crosschecked_without_reclassifying_events(delivery):
    a,b = table_fixture(delivery)
    rows = delivery.supplementary_descriptors(b)
    assert len(rows)==16
    assert rows[0]['terminal_I_descriptor_counts_not_new_categories'] == b['arm_summaries'][0]['terminal_I_descriptor_counts_not_new_categories']
    b['arm_summaries'][0]['terminal_I_descriptor_counts_not_new_categories'][delivery.TERMINAL_FIELDS[0]] += 1
    with pytest.raises(ValueError): delivery.supplementary_descriptors(b)


def test_tables_fail_on_missing_demographic_arm_or_copied_categories(delivery):
    a,b = table_fixture(delivery)
    a['demography']['setting_schedule_arms'].pop()
    with pytest.raises(ValueError): delivery.render_tables(a,b)
    a,b = table_fixture(delivery)
    b['cases'][0]['saved_order_unmodified']['order'] = 'new_category'
    with pytest.raises(ValueError): delivery.render_tables(a,b)


def test_gzip_budget_failure_removes_the_new_incomplete_artifact(delivery,tmp_path,monkeypatch):
    monkeypatch.setattr(delivery,'FILE_BUDGET',10)
    path = tmp_path/'too-big.gz'
    with pytest.raises(ValueError,match='budget'):
        delivery.write_deterministic_gzip({'payload':'x'*1000},path)
    assert not path.exists()


def test_duplicate_or_nonfinite_json_is_rejected(delivery,tmp_path):
    path = tmp_path/'invalid.json'
    for content in ['{"a":1,"a":2}','{"a":NaN}']:
        path.write_text(content)
        with pytest.raises(ValueError): delivery.read_strict_json(path)


def test_cli_delivers_only_three_new_files_and_preserves_source_hash(delivery,tmp_path,monkeypatch,capsys):
    a,b = table_fixture(delivery)
    accounting,independent = tmp_path/'accounting.json',tmp_path/'independent.json'
    accounting.write_text(json.dumps(a,sort_keys=True))
    independent.write_text(json.dumps(b,sort_keys=True))
    output = [tmp_path/'summary.gz',tmp_path/'comparison.json',tmp_path/'tables.md']
    monkeypatch.setattr('sys.argv',['delivery','--accounting',str(accounting),'--independent',str(independent),
        '--summary-gzip',str(output[0]),'--comparison-json',str(output[1]),'--tables-md',str(output[2])])
    delivery.main()
    comparison = json.loads(output[1].read_text())
    summary = json.loads(gzip.decompress(output[0].read_bytes()))
    assert comparison['input_files']['full_accounting_json']['sha256'] == delivery.sha256(accounting.read_bytes()).hexdigest()
    assert summary['delivery_projection']['full_accounting_json_size_bytes'] == accounting.stat().st_size
    assert comparison['checked_counts']['total_component_values'] == 34368
    assert comparison['supplementary_original_categories']['new_event_classes'] is False
    assert {p.name for p in tmp_path.iterdir()} == {'accounting.json','independent.json','summary.gz','comparison.json','tables.md'}
    assert all(p.stat().st_size < 2*1024*1024 for p in output)
    with pytest.raises(ValueError,match='existing'): delivery.main()
