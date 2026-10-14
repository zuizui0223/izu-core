"""Independent scipy/moment reconstruction; no producer imports."""
import argparse
import hashlib
import io
import math
import json
from pathlib import Path
import numpy as np
from scipy.stats import multinomial, poisson


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input-dir', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--receipt', type=Path, required=True)
    p.add_argument('--frozen-manifest',type=Path,required=True)
    args = p.parse_args()
    if args.receipt.exists():
        raise ValueError('refuse existing receipt')
    frozen=json.loads(args.frozen_manifest.read_bytes())
    def source_gate():
        if set(frozen) != {'audit_channels.py','verify_channels.py','test_channels.py','PROTOCOL.md'}:
            raise ValueError('frozen manifest inventory differs')
        for name,identity in frozen.items():
            if sha(Path(__file__).with_name(name).read_bytes())!=identity:
                raise ValueError('frozen source/protocol differs')
    source_gate()
    raw = (args.input_dir/'native_regenerated_kernels_and_state_curves.npz').read_bytes()
    dr = (args.input_dir/'duration_accounting.json').read_bytes()
    if sha(raw) != 'd34fc60c389775f88fa8a54051fdfe90a76ef7864b8f5a813b99d5f0b68ca172' or sha(dr) != 'cd4c2f8fc8584fce1b453d31a6a4bee9f96d7d22853831ccce95caf8c7253ba2':
        raise ValueError('original input differs')
    with np.load(io.BytesIO(raw),allow_pickle=False) as z:
        keys,states,ts = z['keys'].copy(),z['states'].copy(),z['kernels'].copy()
        probabilities=z['probabilities'].copy()
    if not np.all(np.isfinite(ts)) or not np.all(np.isfinite(probabilities)):
        raise ValueError('nonfinite original source')
    readout_raw = (args.output_dir/'READOUT.json').read_bytes()
    r = json.loads(readout_raw)
    def finite(value):
        if isinstance(value,dict):return all(finite(x) for x in value.values())
        if isinstance(value,list):return all(finite(x) for x in value)
        return not isinstance(value,(int,float)) or math.isfinite(value)
    if not finite(r):raise ValueError('nonfinite readout')
    ar = (args.output_dir/'HYBRID_KERNELS_AND_CURVES.npz').read_bytes()
    if (sha(ar) != r['arrays_sha256'] or r['original_kernels'] != 96 or r['pairs'] != 48
        or r['hybrid_laws'] != 192 or r['horizon'] != 80 or r['new_biological_histories'] != 0
        or sha(Path(__file__).with_name('audit_channels.py').read_bytes()) != r['source_sha256']
        or sha(Path(__file__).with_name('PROTOCOL.md').read_bytes()) != r['protocol_sha256']):
        raise ValueError('producer scope or source identity differs')
    with np.load(io.BytesIO(ar),allow_pickle=False) as z:
        hkeys,ht,hcurves = z['keys'].copy(),z['kernels'].copy(),z['occupancy'].copy()
        if not np.array_equal(z['states'],states):
            raise ValueError('state order changed')
    if not np.all(np.isfinite(ht)) or not np.all(np.isfinite(hcurves)):
        raise ValueError('nonfinite hybrid source')
    n=states.sum(axis=1)
    groups=[np.flatnonzero(n==count) for count in range(9)]
    channels={}
    for key,t in zip(keys,ts):
        if np.any(t[1:,0]<=0) or np.any(t[1:,0]>=1):
            raise ValueError('nonidentifiable intensity')
        mu=np.zeros(165);mu[1:]=np.log(1./t[1:,0])
        q=np.zeros((165,3));q[0]=[1,0,0]
        q[1:]=np.einsum('ij,jk->ik',t[1:],states)/(t[1:]@n)[:,None]
        if not np.all(np.isfinite(mu)) or not np.all(np.isfinite(q)) or np.any(q<0) or np.max(np.abs(q.sum(axis=1)-1))>1e-12:
            raise ValueError('moment simplex differs')
        channels[str(key)]=(mu,q)

    def matrix(mu,q):
        result=np.zeros((165,165));result[0,0]=1
        recruitment=np.column_stack([poisson.pmf(k,mu) for k in range(8)]+[poisson.sf(7,mu)])
        for k,cols in enumerate(groups):
            for i in range(1,165):
                result[i,cols]=recruitment[i,k]*multinomial.pmf(states[cols],n=k,p=q[i])
        if not np.all(np.isfinite(result)) or np.max(np.abs(result.sum(axis=1)-1))>1e-12:
            raise ValueError('nonfinite or nonstochastic independent matrix')
        return result

    max_original=max_hybrid=max_curve=max_scalar=0.
    for key,t in zip(keys,ts):
        rebuilt=matrix(*channels[str(key)])
        max_original=max(max_original,float(np.max(np.abs(rebuilt-t))))
    idx=int(np.flatnonzero(np.all(states==[0,8,0],axis=1))[0])
    originals=json.loads(dr)['pairs']
    if len(r['comparisons'])!=48 or ht.shape!=(192,165,165) or hcurves.shape!=(192,81):
        raise ValueError('output inventory differs')
    seen=set()
    original_curves={str(key):stored[:,1:].sum(axis=1) for key,stored in zip(keys,probabilities)}
    for old,row in zip(originals,r['comparisons']):
        for field in ['mismatch_fraction','setting','budget','visitor_arm']:
            if row[field]!=old[field]:raise ValueError('comparison metadata differs')
        prefix=f"{old['mismatch_fraction']}_{old['setting']}_{old['budget']}_"
        mn,qn=channels[prefix+'native_'+old['visitor_arm']]
        mf,qf=channels[prefix+'fixed_expression_'+old['visitor_arm']]
        values={}
        for lab,mu,q in [('00',mf,qf),('10',mn,qf),('01',mf,qn),('11',mn,qn)]:
            label=prefix+old['visitor_arm']+'|'+lab
            hits=np.flatnonzero(hkeys==label)
            if len(hits)!=1:raise ValueError('missing or duplicate hybrid')
            j=int(hits[0]);seen.add(j)
            t=matrix(mu,q)
            max_hybrid=max(max_hybrid,float(np.max(np.abs(t-ht[j]))))
            alive=(n>0).astype(float);v=alive.copy();curve=[]
            for k in range(81):
                curve.append(float(v[idx]));v=t@v
            max_curve=max(max_curve,float(np.max(np.abs(np.asarray(curve)-hcurves[j]))))
            if not np.all(np.isfinite(curve)):raise ValueError('nonfinite independent curve')
            values[lab]={'endpoint':curve[-1],'duration':float(np.sum(curve[:-1]))}
            if lab in ('00','11'):
                original_key=prefix+('native_' if lab=='11' else 'fixed_expression_')+old['visitor_arm']
                saved=original_curves[original_key]
                max_curve=max(max_curve,float(np.max(np.abs(np.asarray(curve)-saved))))
                max_scalar=max(max_scalar,abs(curve[-1]-saved[-1]),abs(values[lab]['duration']-float(np.sum(saved[:-1]))))
            for kind in values[lab]:max_scalar=max(max_scalar,abs(values[lab][kind]-row['corners'][lab][kind]))
        for kind,oldfield in [('endpoint','endpoint_difference'),('duration','restricted_duration_difference')]:
            a,b,c,d=[values[lab][kind] for lab in ['00','10','01','11']]
            expected=dict(recruitment_only=b-a,genotype_only=c-a,interaction=d-b-c+a,
                          full=d-a,recruitment_native_reference=d-c,genotype_native_reference=d-b)
            for field,value in expected.items():max_scalar=max(max_scalar,abs(value-row[kind][field]))
            max_scalar=max(max_scalar,abs(expected['full']-old[oldfield]))
        if row['original_reversal']!=(old['endpoint_difference']>0 and old['restricted_duration_difference']<0):
            raise ValueError('original reversal label changed')
    source_gate()
    if not all(math.isfinite(x) for x in [max_original,max_hybrid,max_curve,max_scalar]):
        raise ValueError('nonfinite independent metrics')
    if len(seen)!=192 or max(max_original,max_hybrid,max_curve,max_scalar)>1e-12:
        raise ValueError(f'independent gate failed: {max_original,max_hybrid,max_curve,max_scalar}')
    result=dict(status='ALL_ORIGINAL_AND_HYBRID_LAWS_INDEPENDENTLY_VERIFIED',original_row_checks=96*165*165,
                hybrid_row_checks=192*165*165,occupancy_checks=192*81,comparisons=48,
                max_original_error=max_original,max_hybrid_error=max_hybrid,max_curve_error=max_curve,
                max_scalar_error=max_scalar,readout_sha256=sha(readout_raw),arrays_sha256=sha(ar),
                verifier_sha256=sha(Path(__file__).read_bytes()),producer_imported=False,new_biological_histories=0)
    with args.receipt.open('x',encoding='utf-8',newline='\n') as f:
        json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
