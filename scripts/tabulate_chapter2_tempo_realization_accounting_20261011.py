"""Compare complete archived accounting evidence and deliver bounded summaries."""
from __future__ import annotations

import argparse
import gzip
from hashlib import sha256
from itertools import product
import json
import math
from pathlib import Path

NATIVE_SCHEMA = 'chapter2_tempo_realization_accounting_v1'
NATIVE_STATUS = 'PASS_COMPLETE_ARCHIVED_COHORT_ACCOUNTING'
INDEPENDENT_SCHEMA = 'independent_tempo_archive_genetic_accounting_v1'
INDEPENDENT_STATUS = 'PASS_COMPLETE_ARCHIVE_TO_ACCOUNTING_AND_PROFILE_AGGREGATION'
DESIGN_SHA = '207a3a0ad3decf096c65f296bebeee69e7f80d5b644abb2318105e50474774d0'
SOURCE_SHA = '9302c9740a1f5ac91cb1c1c39093f358c6fd745d4c5b768980e78d893aade80b'
PROFILES = tuple(range(48271001,48271017))
REPEATS = tuple(range(49271001,49271005))
TIMINGS, COSTS, MUTATIONS, SCHEDULES = ('delayed','prior'), (0,.5), (0,.01), ('abrupt','gradual')
TRAITS = ('I','A')
WINDOW_MAP = {'early':'updates_0_99','late':'updates_100_399','full':'full400'}
WINDOW_LENGTH = {'early':100,'late':300,'full':400}
COMPONENT_MAP = {'observed_change':'observed_change',
    'expected_response':'stored_source_expectation_sum',
    'parent_sampling':'realized_parent_allocation_sum',
    'segregation_mutation_remainder':'segregation_mutation_remainder_sum'}
TOLERANCE = 1e-11
FILE_BUDGET = 2*1024*1024


def require(condition,message):
    if not condition: raise ValueError(message)


def stable_sha(value):
    return sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()


def expected_cases():
    return tuple(product(PROFILES,REPEATS,TIMINGS,COSTS,MUTATIONS,SCHEDULES))


def case_key(case):
    p,r,t,c,m,s = case
    return f'p{p}_r{r}_{t}_cost{int(c*100)}_mu{int(m*10000)}_{s}'


def indexed(rows,key,expected,context):
    require(isinstance(rows,list) and len(rows)==len(expected),context+': missing/extra rows')
    result = {}
    for row in rows:
        k = key(row)
        require(k in expected and k not in result,context+': unexpected/duplicate identity')
        result[k] = row
    require(set(result)==set(expected),context+': missing identities')
    return result


def setting(row):
    return (row['mating_timing'],row['direct_assurance_cost'],row['mutation_rate'])


def numeric(value,context):
    require(type(value) in (int,float) and math.isfinite(value),context+': unavailable/nonfinite number')
    return float(value)


def verify_window_shape(windows,names,context):
    require(isinstance(windows,dict) and set(windows)==set(names),context+': missing/extra windows')
    for name in names:
        require(set(windows[name])==set(TRAITS),context+': missing/extra traits')


def compare_accountings(native,independent):
    """Explicit correspondence of the two independently generated result schemas."""
    require(native['schema']==NATIVE_SCHEMA and native['status']==NATIVE_STATUS,'native schema/status')
    require(independent['schema']==INDEPENDENT_SCHEMA and independent['status']==INDEPENDENT_STATUS,
            'independent schema/status')
    for name,value in {'case_count':1024,'updates_per_case':400,'profile_count':16,'repeats_per_profile':4,
                       'setting_schedule_count':16,'paired_setting_count':8}.items():
        require(type(native[name]) is int and native[name]==value,'native coverage '+name)
    require(native['valid_source_child_transitions_by_locus']=={'I':409600,'A':409600},'unavailable native transitions')
    for name,value in {'raw_case_sha256_verified_count':1024,'case_receipts':1024,'profile_units':16,
        'nested_repeats_per_profile':4,'arms':16,'source_updates':409600,'trait_update_accountings':819200,
        'missing_accounting_updates':0,'missing_or_filtered_cases':0}.items():
        require(type(independent['scope'][name]) is int and independent['scope'][name]==value,
                'independent coverage '+name)
    proof = native['provenance']
    require(proof['design_sha256']==independent['frozen_design_sha256']==DESIGN_SHA,'frozen design proof mismatch')
    require(proof['source_identity_sha256']==independent['execution_source_identity_sha256']==SOURCE_SHA,
            'original source proof mismatch')
    common = independent['uniform_source_founder_runtime']
    expected_common = {'design_sha256':proof['design_sha256'],'source_identity_sha256':proof['source_identity_sha256'],
        'founder_identity_sha256':proof['founder_identity']['digest'],
        'runtime_sha256':stable_sha(proof['runtime_identity']),
        'source_file_map_sha256':stable_sha(proof['source_file_sha256'])}
    require(common==expected_common,'uniform original source/design/founder/runtime proof mismatch')
    manifests = proof['completed_shard_manifest_sha256']
    require(set(manifests)=={f'shard_{j:02d}_complete.json' for j in range(16)}
            and manifests==independent['manifest_sha256'],'original manifest proof mismatch')
    maximum,counts = 0.,{}

    def compare_value(a,b,context):
        nonlocal maximum
        error = abs(numeric(a,context)-numeric(b,context))
        require(error<=TOLERANCE,f'{context}: numerical discrepancy {error} > {TOLERANCE}')
        maximum = max(maximum,error)

    def compare_windows(a,b,context,kind):
        verify_window_shape(a,WINDOW_MAP,context+' native')
        verify_window_shape(b,WINDOW_MAP.values(),context+' independent')
        for w,iw in WINDOW_MAP.items():
            for locus in TRAITS:
                entry = a[w][locus]
                allowed = set(COMPONENT_MAP)|({'available','valid_transitions','start','end_exclusive','updates','endpoint_difference'}
                                             if kind=='case' else {'available','valid_transition_count'})
                independent_allowed = set(COMPONENT_MAP.values())|({'component_closure_error','end_mean','start_mean','telescoping_error'}
                                                                   if kind=='case' else set())
                require(set(COMPONENT_MAP)<=set(entry)<=allowed
                        and set(COMPONENT_MAP.values())<=set(b[iw][locus])<=independent_allowed,
                        context+': missing/extra component coverage')
                require(entry['available'] is True,context+': unavailable '+w+'/'+locus)
                denominator = WINDOW_LENGTH[w]*(1 if kind=='case' else 4 if kind=='profile' else 64)
                count_name = 'valid_transitions' if kind=='case' else 'valid_transition_count'
                require(type(entry[count_name]) is int and entry[count_name]==denominator,
                        context+': incomplete contributing transitions')
                for component,ic in COMPONENT_MAP.items():
                    compare_value(entry[component],b[iw][locus][ic],context+'/'+w+'/'+locus+'/'+component)

    cases = set(expected_cases())
    a = indexed(native['case_summaries'],lambda r:tuple(r['case']),cases,'native cases')
    b = indexed(independent['cases'],lambda r:tuple(r['case']),cases,'independent cases')
    for case in sorted(cases):
        for row in (a[case],b[case]):
            require(type(row['case'][0]) is int and type(row['case'][1]) is int
                    and all(type(row['case'][j]) in (int,float) for j in (3,4)), 'incorrect case identifier types')
            require(row['case_key']==case_key(case),'case key/six identifiers mismatch')
        for name in ('raw_sha256','receipt_sha256'):
            require(isinstance(a[case][name],str) and len(a[case][name])==64
                    and a[case][name]==b[case][name],case_key(case)+': '+name+' mismatch')
        availability = b[case]['availability']
        require(availability['complete_accounting_updates']==availability['source_updates']==400
                and availability['genomic_censuses']==401 and availability['missing_accounting_updates']==0,
                'independent case availability mismatch')
        compare_windows(a[case]['windows'],b[case]['windows'],case_key(case),'case')
    counts.update(cases=1024,case_sha256_pairs=1024,case_identity_values=6144,case_component_values=24576)

    profile_keys = set(product(PROFILES,TIMINGS,COSTS,MUTATIONS,SCHEDULES))
    a = indexed(native['profile_means'],lambda r:(r['profile_seed'],*r['setting'],r['schedule']),profile_keys,'native profiles')
    b = indexed(independent['profile_arm_summaries'],lambda r:(r['history_profile_seed'],*setting(r),r['schedule']),
                profile_keys,'independent profiles')
    for key in sorted(profile_keys):
        require(a[key]['repeats']==b[key]['n_nested_repeats']==4,'profile four-repeat denominator')
        compare_windows(a[key]['windows'],b[key]['windows'],str(key),'profile')
    counts.update(profile_means=256,profile_component_values=6144)

    arm_keys = set(product(TIMINGS,COSTS,MUTATIONS,SCHEDULES))
    a = indexed(native['setting_schedule_summaries'],lambda r:(*r['setting'],r['schedule']),arm_keys,'native arms')
    b = indexed(independent['arm_summaries'],lambda r:(*setting(r),r['schedule']),arm_keys,'independent arms')
    for key in sorted(arm_keys):
        require(a[key]['profiles']==b[key]['n_profiles']==16 and b[key]['n_cases']==64
                and b[key]['n_updates_per_trait']==25600,'arm denominator')
        compare_windows(a[key]['windows'],b[key]['windows'],str(key),'arm')
    counts.update(setting_schedule_arms=16,arm_component_values=384)

    settings = set(product(TIMINGS,COSTS,MUTATIONS))
    a = indexed(native['paired_abrupt_minus_gradual'],lambda r:tuple(r['setting']),settings,'native paired means')
    b = indexed(independent['abrupt_minus_gradual'],setting,settings,'independent paired means')
    profile_pairs = indexed(independent['paired_profile_contrasts'],lambda r:(r['history_profile_seed'],*setting(r)),
                            set(product(PROFILES,TIMINGS,COSTS,MUTATIONS)),'independent paired profiles')
    for key in sorted(settings):
        row = a[key]
        require(row['profile_seeds']==list(PROFILES),'paired profile seed ordering')
        require(b[key]['n_paired_profiles']==16 and b[key]['n_paired_repeats']==64
                and b[key]['contrast']=='abrupt_minus_gradual','paired mean denominator/contrast')
        verify_window_shape(row['windows'],WINDOW_MAP,'paired native')
        verify_window_shape(b[key]['windows'],WINDOW_MAP.values(),'paired independent')
        for p in PROFILES:
            pair = profile_pairs[(p,*key)]
            require(pair['n_paired_repeats']==4 and pair['contrast']=='abrupt_minus_gradual', 'paired profile denominator/contrast')
            verify_window_shape(pair['windows'],WINDOW_MAP.values(),'paired profile')
            require(all(set(pair['windows'][iw][locus])==set(COMPONENT_MAP.values())
                        for iw in WINDOW_MAP.values() for locus in TRAITS), 'paired profile component coverage')
        for w,iw in WINDOW_MAP.items():
            for locus in TRAITS:
                require(set(row['windows'][w][locus])==set(COMPONENT_MAP)
                        and set(b[key]['windows'][iw][locus])==set(COMPONENT_MAP.values()), 'paired component coverage')
                for component,ic in COMPONENT_MAP.items():
                    entry = row['windows'][w][locus][component]
                    require(entry['available'] is True and len(entry['profile_differences'])==16,'paired unavailable coverage')
                    compare_value(entry['mean_abrupt_minus_gradual'],b[key]['windows'][iw][locus][ic],str(key)+'/paired mean')
                    for j,p in enumerate(PROFILES):
                        compare_value(entry['profile_differences'][j],profile_pairs[(p,*key)]['windows'][iw][locus][ic],
                                      str(key)+'/'+str(p)+'/paired profile')
    counts.update(paired_setting_means=8,paired_mean_component_values=192,
                  paired_profile_contrasts=128,paired_profile_component_values=3072,total_component_values=34368)
    return {'schema':'chapter2_tempo_realization_independent_comparison_v1',
        'status':'PASS_COMPLETE_NATIVE_TO_INDEPENDENT_ACCOUNTING_COMPARISON',
        'evidence_rank':'RETROSPECTIVE_EXISTING_COHORT_ACCOUNTING_NOT_CAUSAL_MEDIATION',
        'absolute_tolerance':TOLERANCE,'max_absolute_error':maximum,'checked_counts':counts,
        'window_mapping':WINDOW_MAP,'component_mapping':COMPONENT_MAP,
        'matched_original_proof':{'common_identity':expected_common,'manifest_sha256':manifests},
        'interpretation':'Independent checker uses stored source expectations; native replay separately verifies those expectations. Agreement verifies retained-parent realization and aggregation, not causal mediation.'}


def summary_projection(native,full_sha256,full_size):
    require(native['schema']==NATIVE_SCHEMA,'projection needs native full schema')
    require(all('censuses' in r and 'updates' in r for r in native['case_summaries']), 'annual arrays missing from full source')
    result = {**native,'schema':'chapter2_tempo_realization_summary_v1',
        'case_summaries':[{k:v for k,v in row.items() if k not in ('censuses','updates')}
                          for row in native['case_summaries']]}
    result['delivery_projection'] = {'original_full_accounting_schema':native['schema'],
        'omitted_fields':['case_summaries[*].censuses','case_summaries[*].updates'],
        'full_accounting_json_sha256':full_sha256,'full_accounting_json_size_bytes':full_size,
        'all_other_original_fields_preserved':True,'annual_arrays_embedded':False,
        'annual_arrays_reconstructible_from_summary_alone':False,
        'annual_array_recovery':'Use the separately delivered full accounting JSON identified by its exact byte SHA256; regenerate deterministically from the unchanged original raw cohort and receipted native source if necessary.'}
    return result


def write_deterministic_gzip(value,path):
    path = Path(path)
    raw = path.open('xb')
    try:
        with raw:
            with gzip.GzipFile(fileobj=raw,filename='',mode='wb',mtime=0,compresslevel=9) as compressed:
                for chunk in json.JSONEncoder(sort_keys=True,separators=(',',':'),allow_nan=False).iterencode(value):
                    compressed.write(chunk.encode())
                compressed.write(b'\n')
        require(path.stat().st_size<=FILE_BUDGET,'summary gzip exceeds 2 MiB artifact budget')
    except BaseException:
        path.unlink(missing_ok=True)
        raise

CATEGORIES = ('assurance_first','investment_first','near_simultaneous','assurance_only','investment_only','neither')
TERMINAL_FIELDS = ('I400_above_actual_founder','I400_at_or_beyond_registered_decrease_threshold',
    'saved_I_event_by400_but_terminal_I_above_threshold','saved_I_event_by400_but_terminal_I_above_founder',
    'saved_A_only_by400_and_terminal_I_above_founder')
KERNEL_FIELDS = ('p_zero','p_below_K','expected_next_N','expected_capacity_shortfall')


def supplementary_descriptors(independent):
    """Copy saved categories/descriptors, checking their existing case-to-arm totals."""
    cases = indexed(independent['cases'],lambda r:tuple(r['case']),set(expected_cases()),'descriptor cases')
    arm_keys = set(product(TIMINGS,COSTS,MUTATIONS,SCHEDULES))
    arms = indexed(independent['arm_summaries'],lambda r:(*setting(r),r['schedule']),arm_keys,'descriptor arms')
    for row in cases.values():
        order = row['saved_order_unmodified']
        require(order['order'] in CATEGORIES and order['order_by100'] in CATEGORIES,'unknown saved categories')
        descriptors = row['terminal_I_descriptors_not_new_categories']
        require(set(descriptors)==set(TERMINAL_FIELDS) and all(type(v) is bool for v in descriptors.values()),
                'terminal descriptor availability/type/coverage')
    result = []
    for key in sorted(arm_keys):
        selected = [row for case,row in cases.items() if case[2:]==key]
        require(len(selected)==64,'descriptor arm denominator')
        arm = arms[key]
        for field,source in [('saved_full400_order_counts','order'),('saved_by100_order_counts','order_by100')]:
            calculated = {name:sum(row['saved_order_unmodified'][source]==name for row in selected) for name in CATEGORIES}
            require(arm[field]==calculated,'copied saved category counts differ from independent cases')
        calculated = {name:sum(row['terminal_I_descriptors_not_new_categories'][name] for row in selected)
                      for name in TERMINAL_FIELDS}
        require(arm['terminal_I_descriptor_counts_not_new_categories']==calculated,
                'copied terminal counts differ from independent cases')
        result.append({'setting':list(key[:3]),'schedule':key[3],'cases':64,
            **{field:dict(arm[field]) for field in ('saved_full400_order_counts','saved_by100_order_counts',
                                                  'terminal_I_descriptor_counts_not_new_categories')}})
    return result


def formatted(value):
    if type(value) is int: return str(value)
    return format(numeric(value,'table value'),'.10g')


def markdown_table(headers,rows):
    lines = ['| '+' | '.join(headers)+' |','| '+' | '.join('---' for _ in headers)+' |']
    lines.extend('| '+' | '.join(str(v) if isinstance(v,str) else formatted(v) for v in row)+' |' for row in rows)
    return '\n'.join(lines)+'\n'


def render_tables(native,independent):
    arms = indexed(native['setting_schedule_summaries'],lambda r:(*r['setting'],r['schedule']),
                   set(product(TIMINGS,COSTS,MUTATIONS,SCHEDULES)),'table genetic arms')
    pairs = indexed(native['paired_abrupt_minus_gradual'],lambda r:tuple(r['setting']),
                    set(product(TIMINGS,COSTS,MUTATIONS)),'table paired settings')
    descriptors = supplementary_descriptors(independent)
    demography = indexed(native['demography']['setting_schedule_arms'],lambda r:(*r['setting'],r['schedule']),
                         set(arms),'table demographic arms')
    pieces = ['# Existing tempo cohort: realization accounting tables\n',
        'Retrospective accounting of the unchanged synthetic cohort. Genetic totals use signed trait units: '
        'the arithmetic mean over 4 nested repeats within each profile, then an equal mean over 16 profiles. '
        'Early [0,100) contains 100 updates; late [100,400) contains 300; full [0,400) is their sum. '
        'No confidence intervals or p-values. Parent sampling is a descriptive lottery realization; '
        'these sums do not establish controlled causal mediation. Mutation-zero residual is Mendelian '
        'segregation; mutation-active residual combines segregation and mutation.\n',
        'Genetic table values are displayed with ten significant digits; full precision is retained in JSON. '
        'Cost denotes direct assurance cost; mutation is the frozen rate applied to each inherited allele copy. '
        'The source expected response is pre-mutation.\n']
    labels = {'early':'[0,100)','late':'[100,400)','full':'[0,400)'}
    component_headers = ['Observed change','Expected response','Parent sampling','Segregation + mutation remainder']
    for locus in TRAITS:
        for window in WINDOW_MAP:
            pieces.append(f'## Genetic arm means: {locus}, {window} {labels[window]}\n')
            rows = [[*key,*[arms[key]['windows'][window][locus][c] for c in COMPONENT_MAP]] for key in sorted(arms)]
            pieces.append(markdown_table(['Timing','Cost','Mutation','Schedule',*component_headers],rows))
    for locus in TRAITS:
        for window in WINDOW_MAP:
            pieces.append(f'## Paired abrupt minus gradual: {locus}, {window} {labels[window]}\n')
            pieces.append('Sixteen paired profile differences, each based on the same four nested repeats per schedule.\n')
            rows = [[*key,*[pairs[key]['windows'][window][locus][c]['mean_abrupt_minus_gradual']
                           for c in COMPONENT_MAP]] for key in sorted(pairs)]
            pieces.append(markdown_table(['Timing','Cost','Mutation',*component_headers],rows))
    pieces.append('## Full demography: observed census and retained recruitment\n')
    pieces.append('All-census totals include founders; post-update totals contain 400 censuses per case. '
                  'Missing recruit slots count 48 minus actual retained recruits at each update.\n')
    ordered = [('overall',native['demography']['overall'])]+[(f'{k[0]}; c={k[1]:g}; mu={k[2]:g}; {k[3]}',demography[k])
                                                           for k in sorted(demography)]
    census_fields = ('cases','total_censuses_including_founder','post_update_censuses','below_capacity_censuses',
        'post_update_below_capacity_censuses','minimum_N','cases_ever_below_capacity','post_update_missing_recruit_slots')
    pieces.append(markdown_table(['Arm','Cases','All censuses','Post-update censuses','All N<48','Post N<48',
        'Minimum N','Cases ever N<48','Missing recruit slots'],[[name,*[r[f] for f in census_fields]] for name,r in ordered]))
    pieces.append('## Full demography: seed intensity and retained mating counts\n')
    pieces.append('Expected viable seed intensity is distinct from retained recruits. Selfed fraction is the ratio of '
                  'pooled retained counts; mean case selfed fraction gives cases equal weight. The fraction denominator '
                  'is retained selfed plus retained outcross recruits. Intensity means/counts use source updates.\n')
    seed_fields = ('minimum_expected_seed_intensity','mean_expected_seed_intensity',
        'updates_expected_seed_intensity_below_capacity','retained_selfed_total','retained_outcross_total',
        'retained_recruit_total','pooled_retained_selfed_fraction','mean_case_retained_selfed_fraction',
        'cases_with_defined_selfed_fraction')
    pieces.append(markdown_table(['Arm','Min intensity','Mean intensity','Updates intensity<48','Selfed recruits',
        'Outcross recruits','Total recruits','Pooled self fraction','Mean case self fraction','Defined cases'],
        [[name,*[r[f] for f in seed_fields]] for name,r in ordered]))
    pieces.append('## Conditional saved-state recruitment kernels\n')
    pieces.append('The conditional one-step law is R ~ Poisson(expected viable seed intensity), next N = min(R,48); '
                  'it is not multigeneration survival. Minimum, maximum, mean and sum summarize the saved source states. '
                  'Risk sums are sums of conditional diagnostics, not a probability of loss over a history. '
                  'Capacity shortfall is directly calculated from the finite Poisson lower tail.\n')
    for quantity in KERNEL_FIELDS:
        pieces.append(f'### {quantity}\n')
        pieces.append(markdown_table(['Arm','Minimum','Maximum','Mean','Sum over source states'],
            [[name,*[r['conditional_kernel'][quantity][f] for f in ('minimum','maximum','mean','sum_over_saved_states')]]
             for name,r in ordered]))
    pieces.append('## Fixed-state zero-pollen seed-intensity bound\n')
    pieces.append('S0 = 0.5 sum A_i * 8 exp(-0.5 I_i² - c A_i²). This is an algebraic lower bound on '
                  'the current native total viable seed intensity. It is not a run zero-pollen future or an '
                  'observed retained-self count; no universal S0 >= 48 claim is implied.\n')
    for _,row in ordered:
        require(row['fixed_state_zero_pollen_bound']['available'] is True,'unavailable fixed-state bound')
    pieces.append(markdown_table(['Arm','Available','Minimum S0','Mean S0','Updates S0<48'],
        [[name,'yes',*[r['fixed_state_zero_pollen_bound'][f] for f in ('minimum','mean','updates_below_capacity')]]
         for name,r in ordered]))
    pieces.append('## Supplementary terminal-I descriptors: original saved categories\n')
    pieces.append('These counts are copied from the independent archive checker and crosschecked against its 1,024 '
                  'case records. They are supplementary terminal descriptors, not new event classes. '
                  'The original A-only and I-event definitions, onsets and confirmations remain unchanged. '
                  'Every arm has 64 cases. Threshold denotes the registered 0.05 decrease from each actual founder mean; '
                  'terminal comparisons use census 400.\n')
    pieces.append(markdown_table(['Timing','Cost','Mutation','Schedule','I400 > founder','I400 <= founder-0.05',
        'Saved I event, I400 > threshold','Saved I event, I400 > founder','Saved A-only, I400 > founder'],
        [[*r['setting'],r['schedule'],*[r['terminal_I_descriptor_counts_not_new_categories'][f] for f in TERMINAL_FIELDS]]
         for r in descriptors]))
    for field,title in [('saved_full400_order_counts','Full 400 updates'),('saved_by100_order_counts','By 100 updates')]:
        pieces.append('### Copied original saved categories: '+title+'\n')
        pieces.append(markdown_table(['Timing','Cost','Mutation','Schedule',*CATEGORIES],
            [[*r['setting'],r['schedule'],*[r[field][f] for f in CATEGORIES]] for r in descriptors]))
    return '\n'.join(pieces).rstrip()+'\n'


def read_strict_json(path):
    def unique_pairs(pairs):
        result = {}
        for key,value in pairs:
            require(key not in result,'duplicate JSON key: '+key)
            result[key] = value
        return result
    def nonfinite(token):
        raise ValueError('nonfinite JSON token: '+token)
    path = Path(path)
    with path.open('rb') as handle:
        digest = sha256()
        size = 0
        for chunk in iter(lambda:handle.read(1024*1024),b''):
            digest.update(chunk)
            size += len(chunk)
    with path.open(encoding='utf-8') as handle:
        value = json.load(handle,parse_constant=nonfinite,object_pairs_hook=unique_pairs)
    return value,digest.hexdigest(),size


def write_new_text(path,text):
    require(len(text.encode())<=FILE_BUDGET,'text output exceeds 2 MiB artifact budget')
    with Path(path).open('x',encoding='utf-8') as handle:
        handle.write(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--accounting',type=Path,required=True)
    parser.add_argument('--independent',type=Path,required=True)
    parser.add_argument('--summary-gzip',type=Path,required=True)
    parser.add_argument('--comparison-json',type=Path,required=True)
    parser.add_argument('--tables-md',type=Path,required=True)
    args = parser.parse_args()
    outputs = [args.summary_gzip,args.comparison_json,args.tables_md]
    require(len({p.resolve() for p in outputs})==3,'output paths must be distinct')
    require(all(not p.exists() for p in outputs),'preserve existing output; choose new paths')
    full,full_sha,full_size = read_strict_json(args.accounting)
    independent,ind_sha,ind_size = read_strict_json(args.independent)
    comparison = compare_accountings(full,independent)
    tables = render_tables(full,independent)
    comparison['input_files'] = {'full_accounting_json':{'sha256':full_sha,'size_bytes':full_size},
                               'independent_json':{'sha256':ind_sha,'size_bytes':ind_size}}
    comparison['supplementary_original_categories'] = {'status':'PASS_COPIED_CASE_TO_ARM_COUNTS',
        'case_records':1024,'arm_records':16,'new_event_classes':False}
    projection = summary_projection(full,full_sha,full_size)
    for path in outputs: path.parent.mkdir(parents=True,exist_ok=True)
    write_deterministic_gzip(projection,args.summary_gzip)
    write_new_text(args.comparison_json,json.dumps(comparison,sort_keys=True,indent=2,allow_nan=False)+'\n')
    write_new_text(args.tables_md,tables)
    print(json.dumps({'status':comparison['status'],'max_absolute_error':comparison['max_absolute_error'],
                      'summary_gzip_bytes':args.summary_gzip.stat().st_size,'checked_counts':comparison['checked_counts']},sort_keys=True))


if __name__ == '__main__':
    main()
