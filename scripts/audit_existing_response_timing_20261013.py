"""Retrospective clocks of realized-path expected response; no invasion gradients."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import zipfile
import numpy as np

INPUT_SHA='115636a338c847fdf1f80ae9e39cdfc622fcf38c7f70575e37d245bf7c41b098'
TERMS=('selection','parent_sampling','transmission','birth_mutation')

def window(flags):
    run=0
    for i,flag in enumerate(flags):
        run=run+1 if flag else 0
        if run==20:return i-18
    return None

def classify(a,i):
    if a is None:return 'neither' if i is None else 'investment_only'
    if i is None:return 'assurance_only'
    if abs(a-i)<=5:return 'near_simultaneous'
    return 'assurance_first' if a<i else 'investment_first'

def case(r):
    rows=r['rows']
    if r['status']!='original_birth_and_ledger_replayed' or r['updates']!=200 or len(rows)!=200:
        raise ValueError('Incomplete original case')
    a={k:np.asarray([x[k] for x in rows],dtype=float) for k in TERMS+('observed_change',)}
    s=np.asarray([x['sexual_selection_components'] for x in rows],dtype=float)
    if any(v.shape!=(200,3) or not np.isfinite(v).all() for v in a.values()) or s.shape!=(200,3,3) or not np.isfinite(s).all():
        raise ValueError('Invalid original vector')
    if any(x['year']!=t or not x['eligible'] for t,x in enumerate(rows)):
        raise ValueError('Annual state admission')
    if np.max(np.abs(sum(a[k] for k in TERMS)-a['observed_change']))>1e-10 or np.max(np.abs(s.sum(axis=1)-a['selection']))>1e-10:
        raise ValueError('Original component closure')
    result={'task':r['task'],'case_sha256':r.get('case_sha256')}
    for name,j,direction in [('A',2,1),('I',1,-1)]:
        selection=direction*a['selection'][:,j]
        cumulative=np.cumsum(selection)
        actual=np.cumsum(direction*a['observed_change'][:,j])
        favorable=selection>1e-12
        result[name]={'initial_selection_response':float(selection[0]),
            'favorable_updates':int(favorable.sum()),
            'unfavorable_updates':int((selection < -1e-12).sum()),
            'roundoff_zero_updates':int((np.abs(selection)<=1e-12).sum()),
            'first_favorable_window':window(favorable),
            'selection_crossing':window(cumulative>=.05),
            'actual_crossing':window(actual>=.05),
            'snapshots':{str(t):{'selection_contribution':float(cumulative[t-1]),
                'observed_change':float(actual[t-1])} for t in (1,20,100,200)}}
    for key,label in [('first_favorable_window','response_window_order'),('selection_crossing','selection_contribution_order'),('actual_crossing','actual_order')]:
        result[label]=classify(result['A'][key],result['I'][key])
    return result

def audit(path):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=INPUT_SHA:raise ValueError('Immutable input SHA')
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        if len(names)!=len(set(names)):raise ValueError('Duplicate original member')
        results=[case(json.loads(z.read(n))) for n in sorted(names) if n.endswith('_evolving.json')]
    if len(results)!=320:raise ValueError('Original320 inventory')
    grouped=defaultdict(list)
    for r in results:
        t=r['task'];grouped[(t['block'],t['supply'],t['composition'])].append(r)
    if len(grouped)!=10:raise ValueError('Original10 contexts')
    groups=[]
    for (b,s,c),rs in sorted(grouped.items()):
        if {r['task']['replicate'] for r in rs}!=set(range(32)) or len(rs)!=32:raise ValueError('History inventory')
        groups.append({'block':b,'supply':s,'composition':c,'starts':32,
            **{k:dict(Counter(r[k] for r in rs)) for k in ('response_window_order','selection_contribution_order','actual_order')},
            'initial_response':{name:{'positive':sum(r[name]['initial_selection_response']>1e-12 for r in rs),
                'negative':sum(r[name]['initial_selection_response'] < -1e-12 for r in rs),
                'zero':sum(abs(r[name]['initial_selection_response'])<=1e-12 for r in rs)} for name in ('A','I')}})
    return {'status':'ALL320_EXISTING_RESPONSE_CLOCKS_ACCOUNTED','input_sha256':INPUT_SHA,
        'cases':320,'updates':64000,'groups':groups,'records':results,
        'scope':'Retrospective realized-path expected response; not invasion-gradient onset, no-noise trajectory, ecological root or natural-order benefit.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--out',required=True)
    args=p.parse_args();out=Path(args.out)
    if out.exists():raise ValueError('Refuse output replacement')
    result=audit(args.input);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
