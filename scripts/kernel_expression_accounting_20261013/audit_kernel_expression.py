"""Exact saved-kernel controlled expression accounting; no simulation or imports of producers."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np

KERNEL_SHA='d34fc60c389775f88fa8a54051fdfe90a76ef7864b8f5a813b99d5f0b68ca172'
DURATION_SHA='cd4c2f8fc8584fce1b453d31a6a4bee9f96d7d22853831ccce95caf8c7253ba2'
PROTOCOL_SHA='da872d49bf57119ed8da2e50a66a7b3f494809a3fefa4fcbfc6e1f20199526fd'
H=80


def check(value,message):
    if not value:raise ValueError(message)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def decompose(native,fixed,p0,alive,horizon,prefix,future):
    check(type(horizon) is int and horizon>0,'Invalid horizon')
    n=len(p0)
    check(all(t.shape==(n,n) and np.isfinite(t).all() for t in (native,fixed,prefix,future)),'Invalid matrix')
    values=np.zeros((horizon+1,n));values[0]=alive
    for k in range(horizon):values[k+1]=future@values[k]
    sums=np.zeros_like(values)
    for k in range(horizon):sums[k+1]=sums[k]+values[k]
    delta=native-fixed;end=np.zeros((horizon,n));duration=np.zeros_like(end);p=p0.copy()
    for t in range(horizon):
        end[t]=p*(delta@values[horizon-1-t])
        duration[t]=p*(delta@sums[horizon-1-t])
        p=p@prefix
    return end,duration


def signed(values):
    return dict(total=float(values.sum()),positive=float(np.maximum(values,0).sum()),negative=float(np.minimum(values,0).sum()))


def audit(kernel_path,duration_path):
    check(sha(kernel_path.read_bytes())==KERNEL_SHA,'Kernel identity differs')
    check(sha(duration_path.read_bytes())==DURATION_SHA,'Duration readout identity differs')
    baseline=json.loads(duration_path.read_bytes())
    with np.load(kernel_path,allow_pickle=False) as saved:
        keys=saved['keys'].tolist();states=saved['states'];kernels=saved['kernels'];prob=saved['probabilities']
    check(len(set(keys))==96 and kernels.shape==(96,165,165) and states.shape==(165,3) and prob.shape==(96,81,165),'Original dimensions differ')
    census=states.sum(1);alive=(census>0).astype(float)
    low=(states[:,0]>0)&(states[:,1:]==0).all(1)
    high=(states[:,2]>0)&(states[:,:2]==0).all(1)
    masks={'low_fixed':low,'high_fixed':high,'segregating':(census>0)&~(low|high),'extinct':census==0}
    check(np.all(sum(m.astype(int) for m in masks.values())==1),'Class partition differs')
    check(np.isfinite(kernels).all() and np.all(kernels>=0) and np.max(abs(kernels.sum(2)-1))<1e-11,'Invalid probabilities')
    check(np.all(kernels[:,0]==np.eye(165)[0]),'Extinction not absorbing')
    index={key:i for i,key in enumerate(keys)};outputs=[];all_end=[];all_duration=[];maximum=0.;reversals=0
    check(len(baseline['pairs'])==48,'Original pair count differs')
    for pair in baseline['pairs']:
        meta={k:pair[k] for k in ('mismatch_fraction','setting','budget','visitor_arm')}
        stem=f"{meta['mismatch_fraction']}_{meta['setting']}_{meta['budget']}"
        ni=index[stem+'_native_'+meta['visitor_arm']];fi=index[stem+'_fixed_expression_'+meta['visitor_arm']]
        native,fixed=kernels[ni],kernels[fi];p0=prob[ni,0]
        check(np.array_equal(p0,prob[fi,0]) and p0[np.flatnonzero((states==[0,8,0]).all(1))[0]]==1,'Initial distribution differs')
        endpoint=float((prob[ni,-1]-prob[fi,-1])@alive)
        lifetime=float(((prob[ni,:-1]-prob[fi,:-1])@alive).sum())
        check(abs(endpoint-pair['endpoint_difference'])<1e-10 and abs(lifetime-pair['restricted_duration_difference'])<1e-10,'Old contrasts differ')
        reversal=endpoint>1e-12 and lifetime < -1e-12;reversals+=int(reversal)
        comparisons=[];endpoints=[];durations=[]
        for label,prefix,future in [('native_prefix_fixed_future',native,fixed),('fixed_prefix_native_future',fixed,native)]:
            end,duration=decompose(native,fixed,p0,alive,H,prefix,future)
            errors=[abs(end.sum()-endpoint),abs(duration.sum()-lifetime)]
            maximum=max(maximum,*errors)
            check(max(errors)<1e-10,'Controlled replacement identity fails')
            check(np.max(abs(duration[-1]))==0 and np.max(abs(end[:,census==0]))==0,'Wrong last update or extinct source contribution')
            classes={name:{'endpoint':signed(end[:,mask]),'duration':signed(duration[:,mask])} for name,mask in masks.items()}
            by_n={str(n):{'endpoint':signed(end[:,census==n]),'duration':signed(duration[:,census==n])} for n in range(9)}
            class_census={name:{str(n):{'endpoint':signed(end[:,mask&(census==n)]),'duration':signed(duration[:,mask&(census==n)])} for n in range(9)} for name,mask in masks.items()}
            comparisons.append(dict(reference=label,closure_errors=errors,classes=classes,census=by_n,class_census=class_census,
                endpoint=signed(end),duration=signed(duration),
                endpoint_by_update=end.sum(1).tolist(),duration_by_update=duration.sum(1).tolist()))
            endpoints.append(end);durations.append(duration)
        all_end.append(endpoints);all_duration.append(durations)
        differences={name:{quantity:comparisons[0]['classes'][name][quantity]['total']-comparisons[1]['classes'][name][quantity]['total'] for quantity in ('endpoint','duration')} for name in masks}
        outputs.append(dict(**meta,endpoint_difference=endpoint,restricted_duration_difference=lifetime,
            original_reversal=reversal,references=comparisons,reference_difference=differences))
    check(reversals==12,'Original reversal count differs')
    result=dict(status='ALL48_SAVED_KERNEL_EXPRESSION_REPLACEMENT_IDENTITIES_CLOSE',kernels=96,pairs=48,
        horizon=H,source_states=165,original_reversals=reversals,max_closure_error=maximum,
        kernel_sha256=KERNEL_SHA,duration_sha256=DURATION_SHA,protocol_sha256=PROTOCOL_SHA,
        executed_source_sha256=sha(Path(__file__).read_bytes()),new_biological_histories=0,
        units={'endpoint':'occupancy probability','duration':'expected occupied censuses0..79'},
        policy='expressed investment clamped to0.35; genomic inheritance unchanged',
        comparisons=outputs,
        limits=['Restricted three-investment-genotype K8 model, not the2304 full-genome cohort.',
            'Same-state single-update expression replacement under stated prefix/future; not unique fixation mediation.',
            'Both reference orders retained; no causal fraction, significance or pure natural-order benefit.'])
    return result,dict(endpoint=np.asarray(all_end),duration=np.asarray(all_duration),states=states,
        pair_keys=np.asarray([str((r['mismatch_fraction'],r['setting'],r['budget'],r['visitor_arm'])) for r in outputs]),
        references=np.asarray(['native_prefix_fixed_future','fixed_prefix_native_future']))


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--kernels',type=Path,required=True);p.add_argument('--duration',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();check(sha(Path(__file__).with_name('PROTOCOL.md').read_bytes())==PROTOCOL_SHA,'Protocol identity differs')
    result,arrays=audit(args.kernels,args.duration)
    args.out.mkdir(parents=True,exist_ok=False)
    with (args.out/'READOUT.json').open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(result,indent=2,allow_nan=False)+'\n')
    np.savez_compressed(args.out/'ALL_STATE_TIME_CONTRIBUTIONS.npz',**arrays)
    print(json.dumps({k:v for k,v in result.items() if k not in ('comparisons','limits')}))


if __name__=='__main__':main()
