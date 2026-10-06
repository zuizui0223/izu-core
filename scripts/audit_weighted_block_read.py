"""Timing diagnostic at observed weighted-core dimensions; no biology inference."""
from pathlib import Path
import hashlib,json,time
import numpy as np
from scripts.model3_weighted_core_stream import exact_core
from scripts.model3_weighted_block_read import read_columns


def main():
    root=Path(__file__).resolve().parents[1]
    out=root/'outputs/model3_precision_feasibility/weighted_block_read_benchmark.json'
    if out.exists():raise ValueError('preserve previous benchmark')
    rng=np.random.default_rng(517)
    core=rng.normal(size=(131,103,66))
    left=rng.normal(size=(611,131,6));right=rng.normal(size=(8,103,6))
    timings={'rowwise':[],'batched':[]};values={}
    for repeat in range(3):
        for name in (['rowwise','batched'] if repeat%2==0 else ['batched','rowwise']):
            start=time.perf_counter()
            if name=='rowwise':
                value=np.concatenate([exact_core(core,left,right[j:j+1],budget=16_000_000) for j in range(8)],axis=1).reshape(611,-1)
            else:value=read_columns(core,left,right,0,8*66,budget=16_000_000)
            timings[name].append(time.perf_counter()-start);values[name]=value
    delta=values['rowwise']-values['batched']
    relative=float(np.linalg.norm(delta)/np.linalg.norm(values['rowwise']))
    assert relative<1e-12
    files=['scripts/audit_weighted_block_read.py','scripts/model3_weighted_block_read.py','scripts/model3_weighted_core_stream.py']
    receipt=dict(scope='synthetic signed input at observed dimensions; exact block arithmetic timing only',
        seed=517,core_shape=list(core.shape),left_shape=list(left.shape),right_shape=list(right.shape),
        seconds=timings,speedup=float(np.median(timings['rowwise'])/np.median(timings['batched'])),
        relative_frobenius_difference=relative,max_absolute_difference=float(np.abs(delta).max()),
        sources={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in files})
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
