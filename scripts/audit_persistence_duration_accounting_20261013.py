"""Source-admitted regeneration, not authentication of missing conversation ZIPs."""
import argparse
import csv
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import runpy
import sys

import numpy as np


CLASSES = ('low_fixed_alive', 'high_fixed_alive', 'segregating_alive')
TOL = 1e-12
LIFETIME_CSV_SHA='e0abe2aee00a538c0c6b5adaba9057e858188db147ecd446d5c88e6997b94d61'


def first_entry_by_census(T,states,p0,horizon):
    census=states.sum(1)
    low=(states[:,0]>0)&(states[:,1:]==0).all(1)
    high=(states[:,2]>0)&(states[:,:2]==0).all(1)
    seg=(census>0)&~(low|high)
    entry=np.zeros((horizon+1,2,int(census.max())))
    q=p0[seg].copy()
    for j,g in enumerate((low,high)):
        np.add.at(entry[0,j],census[g]-1,p0[g])
    for t in range(1,horizon+1):
        for j,g in enumerate((low,high)):
            np.add.at(entry[t,j],census[g]-1,q@T[np.ix_(seg,g)])
        q=q@T[np.ix_(seg,seg)]
    return entry


def compare_compact_lifetime(pairs, path):
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=LIFETIME_CSV_SHA:
        raise ValueError('original48 lifetime CSV byte identity differs')
    key=lambda r:(float(r['mismatch_fraction']),r['setting'],float(r['budget']),r['visitor_arm'])
    with path.open(newline='',encoding='utf-8') as stream:expected=list(csv.DictReader(stream))
    original={key(r):r for r in expected};actual={key(r):r for r in pairs}
    if len(original)!=48 or len(actual)!=48 or len(pairs)!=48 or set(original)!=set(actual):
        raise ValueError('original48 lifetime contrast domain differs')
    maximum={k:0. for k in ('endpoint_difference','restricted_duration_difference','low_first_entry_difference')}
    for context,r in actual.items():
        for field,column,tol in (
            ('endpoint_difference','delta_P_H_occupied',1e-12),
            ('restricted_duration_difference','delta_restricted_mean_time_to_extinction',1e-10),
            ('low_first_entry_difference','delta_P_low_fixed_ever_by_H',1e-12)):
            error=abs(float(r[field])-float(original[context][column]))
            if not np.isfinite(error) or error>tol:raise ValueError('original48 lifetime contrast mismatch: '+field)
            maximum[field]=max(maximum[field],error)
        flag=r['endpoint_difference']>1e-12 and r['restricted_duration_difference']< -1e-12
        if original[context]['positive_endpoint_negative_lifetime']!=str(flag):
            raise ValueError('original reversal classification differs')
    return dict(comparisons=144,pairs=48,max_errors=maximum,original_csv_sha256=LIFETIME_CSV_SHA)


def contrast_curves(native, fixed):
    if len(native) != len(fixed) or len(native) < 2:
        raise ValueError('matching consecutive updates required')
    for curve in (native, fixed):
        if [r['update'] for r in curve] != list(range(len(curve))):
            raise ValueError('matching consecutive updates required')
        for r in curve:
            values = np.array([r['occupied'], *(r[k] for k in CLASSES)], dtype=float)
            if not np.isfinite(values).all() or (values < -TOL).any() or (values > 1 + TOL).any():
                raise ValueError('invalid occupied partition')
            if abs(values[0]-values[1:].sum()) > 1e-10:
                raise ValueError('occupied class partition does not close')
    delta = np.array([a['occupied']-b['occupied'] for a,b in zip(native,fixed)])
    class_delta = {k: np.array([a[k]-b[k] for a,b in zip(native,fixed)]) for k in CLASSES}
    if np.max(abs(sum(class_delta.values())-delta)) > 1e-10:
        raise ArithmeticError('contrast partition does not close')
    switches=[];previous=0
    for t,x in enumerate(delta):
        sign=1 if x>TOL else -1 if x < -TOL else 0
        if sign:
            if previous and sign != previous:switches.append(t)
            previous=sign
    return dict(endpoint_difference=float(delta[-1]), restricted_duration_difference=float(delta[:-1].sum()),
                positive_curve_area=float(np.maximum(delta[:-1],0).sum()),
                negative_curve_area=float(np.minimum(delta[:-1],0).sum()),
                sign_change_updates=switches,
                class_duration_contributions={k:float(v[:-1].sum()) for k,v in class_delta.items()},
                class_endpoint_contributions={k:float(v[-1]) for k,v in class_delta.items()},
                survival_curve_difference=delta.tolist())


def module_from_file(path):
    spec=importlib.util.spec_from_file_location('_duration_existing_accounting',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def run(source_root, baseline, lifetime_csv, out):
    out=out.resolve()
    if out.exists():raise ValueError('refuse to replace diagnostic output')
    source_root=source_root.resolve()
    if source_root in out.parents:raise ValueError('output must be outside source')
    here=Path(__file__).resolve().parent
    old_argv=sys.argv.copy()
    # Direct script CLI keeps the pinned native scripts namespace isolated.
    sys.argv=[str(here/'verify_chapter2_pr471_native_20261012.py'),
              '--source-root',str(source_root),'--expected-csv',str(baseline.resolve()),'--out',str(out/'native_admission')]
    try:runpy.run_path(str(here/'verify_chapter2_pr471_native_20261012.py'),run_name='__main__')
    finally:sys.argv=old_argv
    admission=json.loads((out/'native_admission/comparison.json').read_bytes())
    assert admission['comparisons']==480 and admission['native_source_executed']
    native=sys.modules['scripts.audit_chapter2_q3q4_statewise_pollen_equalized_20261011']
    accounting=module_from_file(here/'audit_pr471_fixation_lifetime_20261012.py')
    states=np.asarray(native.states());p0=np.zeros(len(states));p0[np.flatnonzero((states==[0,8,0]).all(1))[0]]=1.
    outputs={};keys=[];kernels=[];probabilities=[];entries=[]
    for frac,setting,budget,policy,arm in itertools.product(native.FRACTIONS,native.SETTINGS,native.BUDGETS,native.POLICIES,native.VISITOR_ARMS):
        key=f'{frac}_{setting}_{budget}_{policy}_{arm}'
        T=native.transition(setting,budget,frac,policy,arm)
        outputs[key]=accounting.analyze_kernel(T,states,p0)
        entry=first_entry_by_census(T,states,p0,80)
        recorded=np.array([[r['low_first_entry'],r['high_first_entry']] for r in outputs[key]['timeseries']])
        if np.max(abs(entry.sum(2)-recorded))>1e-10:raise ArithmeticError('first-entry time/census partition mismatch')
        entries.append(entry)
        pp=np.zeros((81,len(states)));pp[0]=p0
        for t in range(80):pp[t+1]=pp[t]@T
        if np.max(abs(pp.sum(1)-1))>1e-10:raise ArithmeticError('state probability mass')
        keys.append(key);kernels.append(T);probabilities.append(pp)
    pairs=[];standardized=[];pair_keys=[]
    for frac,setting,budget,arm in itertools.product(native.FRACTIONS,native.SETTINGS,native.BUDGETS,native.VISITOR_ARMS):
        a=outputs[f'{frac}_{setting}_{budget}_native_{arm}'];b=outputs[f'{frac}_{setting}_{budget}_fixed_expression_{arm}']
        contrast=contrast_curves(a['timeseries'],b['timeseries'])
        if abs(contrast['restricted_duration_difference']-(a['summary']['restricted_mean_time_to_extinction']-b['summary']['restricted_mean_time_to_extinction']))>1e-10:
            raise ArithmeticError('duration reward contrast mismatch')
        pairs.append(dict(mismatch_fraction=frac,setting=setting,budget=budget,visitor_arm=arm,
                          low_first_entry_difference=a['summary']['P_low_fixed_ever_by_H']-b['summary']['P_low_fixed_ever_by_H'],**contrast))
        Tn=native.transition(setting,budget,frac,'native',arm)
        Tf=native.transition(setting,budget,frac,'fixed_expression',arm)
        low,high,_=accounting.masks_and_validate(Tn,states,p0,80)
        pointwise=np.zeros((2,80,8,3))
        for j,g in enumerate((low,high)):
            assert np.array_equal(states[g].sum(1),np.arange(1,9))
            vn=np.ones(8);vf=np.ones(8)
            for t in range(80):
                vn=Tn[np.ix_(g,g)]@vn;vf=Tf[np.ix_(g,g)]@vf
                pointwise[j,t,:,0]=vn;pointwise[j,t,:,1]=vf;pointwise[j,t,:,2]=vn-vf
        standardized.append(pointwise);pair_keys.append(f'{frac}_{setting}_{budget}_{arm}')
    assert len(outputs)==96 and len(pairs)==48
    compact_admission=compare_compact_lifetime(pairs,lifetime_csv)
    np.savez_compressed(out/'native_regenerated_kernels_and_state_curves.npz',keys=np.asarray(keys),states=states,kernels=np.asarray(kernels),probabilities=np.asarray(probabilities))
    np.savez_compressed(out/'first_entry_time_and_census.npz',keys=np.asarray(keys),updates=np.arange(81),
                        fixed_class=np.asarray(['low','high']),census=np.arange(1,9),entry_probabilities=np.asarray(entries))
    np.savez_compressed(out/'pointwise_postfixation_comparisons.npz',pair_keys=np.asarray(pair_keys),
                        fixed_class=np.asarray(['low','high']),remaining_updates=np.arange(1,81),
                        census=np.arange(1,9),fields=np.asarray(['native_survival','fixed_expression_survival','difference']),
                        comparisons=np.asarray(standardized))
    result=dict(status='NATIVE_REGENERATED_96_KERNEL_TEMPORAL_ACCOUNTING',original_conversation_archive_authenticated=False,
                native_admission=admission,original48_compact_admission=compact_admission,
                kernels=96,pairs=pairs,all_arm_accounting=outputs,new_random_histories=0,
                scope='Retrospective signed temporal/state occupancy accounting; not causal fixation mediation or a new primary endpoint.')
    (out/'duration_accounting.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    # Source contents and imported identities must still match after the diagnostic.
    verifier=module_from_file(here/'verify_chapter2_pr471_native_20261012.py')
    assert verifier.check_checkout(source_root,verifier.SOURCE_COMMIT)==admission['source']
    for relative,item in admission['imported_source_files'].items():
        if hashlib.sha256((source_root/relative).read_bytes()).hexdigest()!=item['sha256']:
            raise ValueError('source changed during duration diagnostic')
    files={str(p.relative_to(out).as_posix()):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob('*')) if p.is_file()}
    (out/'_COMPLETION.json').write_text(json.dumps(dict(status=result['status'],kernels=96,paired_contrasts=48,
                original_archive_authenticated=False,new_random_histories=0,files=files,
                auditor_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n',encoding='utf-8')
    print(result['status'],len(pairs),max(x['verification']['max_error'] for x in outputs.values()))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',type=Path,required=True);p.add_argument('--expected-csv',type=Path,required=True)
    p.add_argument('--lifetime-csv',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();run(a.source_root,a.expected_csv,a.lifetime_csv,a.out)
