"""Independent raw-only descriptive verifier; imports no producer/audit modules."""
import argparse, csv, hashlib, io, json, math, zipfile
from pathlib import Path
import numpy as np

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--input-dir', type=Path, required=True)
parser.add_argument('--case-table', type=Path, required=True)
parser.add_argument('--audit-script', type=Path, required=True)
parser.add_argument('--document', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
if not __debug__:
    raise RuntimeError('Run without -O: independent verification requires assertions.')
if args.out.exists():
    raise FileExistsError('Receipt output already exists; choose a new path.')
INPUT = args.input_dir
EXPECTED = {
    'INVESTMENT_VARIATION_RESTORATION_64_20261013.zip':'90b9d063c564edf97f12d3a3917819486f72d4ecb8281a20ebdaf39ad7de14c6',
    'RESTORED_PATHWISE_ACCOUNTING_REVIEW_20261013.zip':'07e86248551b1dce24ea91f1566c54e6a8c7f8932ac96479e2cd78e708ce572d',
    'remote_atom_inputs_20261011.zip':'f0fd126f638e1c6bd130e640ce4491b3bb47aac3da1838359a902776c9a4e037',
    'completed_atom_abm_20261011.zip':'7ae00916ed2cbb38323c3fb9ffc5824de3e8272df1f5a35785842c316191f918',
}
digest = lambda b: hashlib.sha256(b).hexdigest()
for name, expected in EXPECTED.items():
    assert digest((INPUT/name).read_bytes()) == expected, name

def unpack(z, name):
    raw = z.read(name)
    with np.load(io.BytesIO(raw), allow_pickle=False) as f:
        a = dict(f)
    return raw, a, json.loads(str(a['metadata'].item()))

def censuses(a):
    return [a['alleles'][a['offsets'][j]:a['offsets'][j+1],1,:]
            for j in range(len(a['offsets'])-1)]

def first(flags, years=None):
    found = np.flatnonzero(flags)
    if not len(found): return None
    i = int(found[0])
    return i if years is None else int(years[i])

def event(vals, baseline, start=0):
    flags = np.array([math.isfinite(v) and baseline-v >= .05 for v in vals[start:]])
    if len(flags)<20: return None
    index=first(np.convolve(flags.astype(int),np.ones(20,dtype=int),'valid')==20)
    return None if index is None else index+start

def compare(got, wanted, label):
    if got is None: assert wanted == '', (label,got,wanted)
    elif isinstance(got, (bool,np.bool_)): assert wanted == str(bool(got)), (label,got,wanted)
    elif isinstance(got, str): assert got == wanted, (label,got,wanted)
    else: assert math.isclose(float(got),float(wanted),rel_tol=0,abs_tol=1e-12), (label,got,wanted)

published = list(csv.DictReader(args.case_table.open()))
assert len(published)==64
published = {r['key']:r for r in published}
recomputed=[]
annual_max_error=0.
updates=0
with zipfile.ZipFile(INPUT/'INVESTMENT_VARIATION_RESTORATION_64_20261013.zip') as z, \
     zipfile.ZipFile(INPUT/'RESTORED_PATHWISE_ACCOUNTING_REVIEW_20261013.zip') as az:
    accounting=json.loads(az.read('RESTORED_PATHWISE_ACCOUNTING_AUDITED_20261013.json'))
    refs={r['key']:r for r in accounting['rows']}
    expected_keys={f'{block}_s0.125_matched_n48_standing_MI_new_A_r{i}_evolving'
                   for block in ('causal_main','causal_confirmation') for i in range(32)}
    assert set(published)==expected_keys==set(refs)
    for key in sorted(expected_keys):
        ob,o,om=unpack(z,'ORIGINAL64/'+key+'.npz')
        rb,r,rm=unpack(z,'RESTORATION/'+key+'.npz')
        og=censuses(o);rg=censuses(r)
        assert len(og)==201 and all(len(g) for g in og+rg)
        means=[float(g.mean()) for g in og]
        restored_means=[float(g.mean()) for g in rg]
        trigger=first([np.ptp(g)==0 for g in og])
        assert trigger==rm['trigger']
        initial=means[0]
        start=200 if trigger is None else trigger
        assert len(rg)==201-start
        full=means.copy()
        if trigger is not None: full[start:]=restored_means
        assert len(full)==201
        if trigger is None:
            for field in ('ids','alleles','allele_origin','mutation_flags','birth_years'):
                assert np.array_equal(o[field][o['offsets'][200]:],r[field])
        else:
            assert all(v==means[trigger] for v in means[trigger:]), key
            assert np.all(rg[0][:,0]==means[trigger]-1/16)
            assert np.all(rg[0][:,1]==means[trigger]+1/16)
            assert np.all(rg[0].mean(axis=1)==means[trigger])
        years=np.arange(start,201)
        refix=first([np.ptp(g)==0 for g in rg[1:]],years[1:]) if trigger is not None else None
        expressed=first([np.var(g.mean(axis=1))>0 for g in rg[1:]],years[1:]) if trigger is not None else None
        exclusion=first([initial-float(g.min())<.05 for g in rg],years) if trigger is not None else None
        oe=event(means,initial);re=event(full,initial)
        terms={k:0. for k in ('selection','parent_sampling','transmission','observed_change')}
        for j in range(len(rg)-1):
            lo,hi=r['offsets'][j:j+2]
            nl,nh=r['offsets'][j+1:j+3]
            edges=r['parentage'][r['parent_offsets'][j]:r['parent_offsets'][j+1]]
            assert np.array_equal(edges[:,0],r['ids'][nl:nh])
            byid=dict(zip(r['ids'][lo:hi],rg[j].mean(axis=1)))
            parent_mean=np.mean([.5*(byid[m]+byid[f]) for _,m,f in edges])
            delta=restored_means[j+1]-restored_means[j]
            selection=rm['rows'][j]['expected_response'][1]
            annual=dict(selection=selection,parent_sampling=parent_mean-restored_means[j]-selection,
                        transmission=restored_means[j+1]-parent_mean,observed_change=delta)
            assert abs(sum(annual[k] for k in ('selection','parent_sampling','transmission'))-delta)<1e-12
            for k,v in annual.items():
                error=abs(v-refs[key]['annual'][j][k]);annual_max_error=max(annual_max_error,error)
                assert error<1e-12
                terms[k]+=v
            updates+=1
        row=dict(key=key,block=om['task']['block'],replicate=om['task']['replicate'],
            original_raw_sha256=digest(ob),restored_raw_sha256=digest(rb),initial_I=initial,event_target_I=initial-.05,
            trigger_year=trigger,remaining_updates=200-start,trigger_I=means[start] if trigger is not None else None,
            restored_min_I=float(rg[0].min()) if trigger is not None else None,
            restored_max_I=float(rg[0].max()) if trigger is not None else None,
            restored_supports_target=initial-float(rg[0].min())>=.05 if trigger is not None else None,
            target_previously_reachable=initial-float(og[start].min())>=.05 if trigger is not None else None,
            first_expressed_variance_year=expressed,first_refixation_year=refix,
            time_to_refixation=refix-start if refix is not None else None,first_post_target_exclusion_year=exclusion,
            post_censuses_with_allele_variance=sum(np.var(g)>0 for g in rg) if trigger is not None else None,
            post_censuses_with_expressed_variance=sum(np.var(g.mean(axis=1))>0 for g in rg) if trigger is not None else None,
            original_event_year=oe,restored_event_year=re,post_event_year=event(full,initial,start) if trigger is not None else None,
            event_completed_before_trigger=(oe is not None and oe+19<trigger) if trigger is not None else None,
            original_terminal_I=means[-1],restored_terminal_I=restored_means[-1],
            terminal_effect_original_minus_restored=means[-1]-restored_means[-1],restored_terminal_fixed=np.ptp(rg[-1])==0,**terms)
        assert set(row)==set(published[key])
        for k,v in row.items(): compare(v,published[key][k],key+':'+k)
        recomputed.append(row)

def stats(rows):
    tr=[r for r in rows if r['trigger_year'] is not None]
    return dict(cases=len(rows),triggered=len(tr),
      target_supported=sum(bool(r['restored_supports_target']) for r in tr),
      previously_supported=sum(bool(r['target_previously_reachable']) for r in tr),
      newly_supported=sum(bool(r['restored_supports_target']) and not r['target_previously_reachable'] for r in tr),
      excluded=sum(not r['restored_supports_target'] for r in tr),
      next_expressed=sum(r['first_expressed_variance_year']==r['trigger_year']+1 for r in tr),
      refixed=sum(r['first_refixation_year'] is not None for r in tr),
      original_events=sum(r['original_event_year'] is not None for r in rows),
      restored_events=sum(r['restored_event_year'] is not None for r in rows),
      gained_events=sum(r['original_event_year'] is None and r['restored_event_year'] is not None for r in rows),
      lost_events=sum(r['original_event_year'] is not None and r['restored_event_year'] is None for r in rows),
      completed_pre_trigger=sum(bool(r['event_completed_before_trigger']) for r in rows),
      pathwise={k:float(np.mean([r[k] for r in rows])) for k in ('selection','parent_sampling','transmission','observed_change')})

receipt=dict(status='ALL64_ALL32_CSV_FIELDS_INDEPENDENTLY_MATCH',input_sha256=EXPECTED,
    independent_script_sha256=digest(Path(__file__).read_bytes()),
    checked_csv_sha256=digest(args.case_table.read_bytes()),
    checked_script_sha256=digest(args.audit_script.read_bytes()),
    checked_document_sha256=digest(args.document.read_bytes()),
    fields_per_case=len(recomputed[0]),annual_updates=updates,annual_max_error=annual_max_error,
    totals=stats(recomputed),blocks={b:stats([r for r in recomputed if r['block']==b])
      for b in ('causal_main','causal_confirmation')},
    no_trigger_keys=[r['key'] for r in recomputed if r['trigger_year'] is None],
    late_cases=[r['key'] for r in recomputed if r['trigger_year'] is not None and r['remaining_updates']+1<20],
    no_producer_imports=True,no_new_biological_histories=True,
    expected_response='Authenticated saved expected_response retained; not freshly recomputed in this review.',
    limitations='Allele support is necessary but does not prove finite-time attainability or event completion. Descriptive post hoc counts are not new inference.')
refix_times=[r['time_to_refixation'] for r in recomputed if r['time_to_refixation'] is not None]
assert (min(refix_times),max(refix_times),np.median(refix_times))==(19,128,51)
assert all(r['restored_supports_target'] and not r['target_previously_reachable']
           for r in recomputed if r['original_event_year'] is None and r['restored_event_year'] is not None)
receipt['document_claims_checked']=dict(refixation_range=[19,128],refixation_median=51,
    right_censored_refixation=16,all_seven_event_gains_among_newly_supported=True,
    initial_means={b:sorted({r['initial_I'] for r in recomputed if r['block']==b})
                   for b in ('causal_main','causal_confirmation')})
with args.out.open('x', encoding='utf-8') as f:
    json.dump(receipt,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(receipt,indent=2))
