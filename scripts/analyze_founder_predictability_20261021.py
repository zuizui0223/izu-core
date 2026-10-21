"""Exploratory saved-cohort predictability; no simulation imports."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def scores(y):
    y = np.asarray(y, dtype=float)
    if y.ndim != 2 or min(y.shape) < 2 or not np.isfinite(y).all():
        raise ValueError('finite crossed matrix with at least two rows/columns required')
    f, v = y.shape
    grand = y.mean()
    row = y.mean(axis=1, keepdims=True)
    col = y.mean(axis=0, keepdims=True)
    residual = y - row - col + grand
    total = float(np.sum((y-grand)**2))
    parts = dict(founder=float(v*np.sum((row-grand)**2)), history=float(f*np.sum((col-grand)**2)), interaction_plus_stochastic=float(np.sum(residual**2)))
    if not np.isclose(sum(parts.values()), total, atol=1e-12):
        raise ValueError('sum of squares does not close')
    h = 1/f + 1/v - 1/(f*v)
    predictions = dict(intercept=(y.sum()-y)/(y.size-1), founder=(v*row-y)/(v-1), history=(f*col-y)/(f-1), additive=(row+col-grand-h*y)/(1-h))
    errors = {k:float(np.sum((y-p)**2)) for k,p in predictions.items()}
    zero = total <= 1e-28
    return dict(mean=float(grand), total_ss=total, ss=parts, ss_fraction={k:None if zero else val/total for k,val in parts.items()}, loo_sse=errors, loo_skill={k:None if zero else 1-val/errors['intercept'] for k,val in errors.items() if k!='intercept'}, n_founders=f, n_histories=v)

def extract(archive):
    inventory=json.loads((ROOT/'docs/audits/CHAPTER2_CONFIRM160_ASSET_SHA256_20261019.json').read_text(encoding='utf-8'))
    code=digest((ROOT/'scripts/variation_clock_readback_20261019.py').read_bytes())
    matrices=np.full((160,160,2,2,3),np.nan) # founder,history,policy,census(0,80),trait
    receipts=[];seen=set()
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        if len(names)!=len(set(names)):raise ValueError('duplicate archive member')
        def member(base):
            matches=[n for n in names if n.rsplit('/',1)[-1]==base]
            if len(matches)!=1:raise ValueError('missing/duplicate '+base)
            return z.read(matches[0])
        for shard in range(32):
            receipt=json.loads(member(f'shard-{shard}.json'));raw=member(f'shard-{shard}.npz')
            if receipt['analysis_sha256']!=code or receipt['source_sha256']!=inventory[f'raw-shard-{shard}.zip'] or receipt['output_sha256']!=digest(raw):raise ValueError('provenance mismatch')
            receipts.append(receipt)
            with np.load(io.BytesIO(raw),allow_pickle=False) as a:
                coords=a['coordinates']; means=a['means']; extinction=a['extinction']
                for i,coord in enumerate(coords):
                    fi,vi=map(int,coord)
                    if not(0<=fi<160 and 0<=vi<160) or (fi,vi) in seen:raise ValueError('invalid/duplicate coordinate')
                    seen.add((fi,vi))
                    if np.any(extinction[i,:,0]>=0):raise ValueError('B8 extinction')
                    matrices[fi,vi,:,0,:]=means[i,:,0,0,:]
                    matrices[fi,vi,:,1,:]=means[i,:,0,80,:]
    if len(seen)!=25600 or not np.isfinite(matrices).all():raise ValueError('incomplete matrices')
    if not np.allclose(matrices[:,:,:,0,:],matrices[:,0:1,:,0,:],atol=1e-14,rtol=0):raise ValueError('initial means differ across histories')
    if not np.allclose(matrices[:,:,0,0,:],matrices[:,:,1,0,:],atol=1e-14,rtol=0):raise ValueError('initial means differ across policies')
    return matrices,dict(artifact_id=12174875191,run_id=39226906489,archive_sha256=digest(Path(archive).read_bytes()),producer_sha256=code,receipts=receipts)

def report(matrices):
    out={}
    for pi,policy in enumerate(('fixed','evolving')):
        for outcome in ('change','endpoint'):
            y=matrices[:,:,pi,1,1]
            if outcome=='change':y=y-matrices[:,:,pi,0,1]
            out[f'{policy}_I_{outcome}']=scores(y)
    for ti,trait in ((0,'M'),(2,'A')):
        out[f'evolving_{trait}_change']=scores(matrices[:,:,1,1,ti]-matrices[:,:,1,0,ti])
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path);p.add_argument('--matrix',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    provenance_path=args.matrix.with_suffix('.json')
    if args.archive:
        m,provenance=extract(args.archive);np.savez_compressed(args.matrix,means=m)
        provenance['matrix_sha256']=digest(args.matrix.read_bytes());provenance_path.write_bytes((json.dumps(provenance,indent=2)+'\n').encode())
    else:
        provenance=json.loads(provenance_path.read_text(encoding='utf-8'))
        inventory=json.loads((ROOT/'docs/audits/CHAPTER2_CONFIRM160_ASSET_SHA256_20261019.json').read_text(encoding='utf-8'))
        code=digest((ROOT/'scripts/variation_clock_readback_20261019.py').read_bytes())
        if provenance['producer_sha256']!=code or len(provenance['receipts'])!=32:raise ValueError('cached provenance mismatch')
        for i,r in enumerate(provenance['receipts']):
            if r['analysis_sha256']!=code or r['source_sha256']!=inventory[f'raw-shard-{i}.zip']:raise ValueError('cached source mismatch')
        if digest(args.matrix.read_bytes())!=provenance['matrix_sha256']:raise ValueError('matrix hash mismatch')
        with np.load(args.matrix,allow_pickle=False) as a:m=a['means']
    if m.shape!=(160,160,2,2,3):raise ValueError('matrix shape')
    result=dict(scope='post-outcome B8 existing-source pairing prediction; not causal variance attribution',primary='evolving_I_change founder-only leave-cell-out skill',unresolved='residual combines interaction and stochastic realization; no novel-founder generalization',matrix_sha256=provenance['matrix_sha256'],results=report(m))
    args.output.write_bytes((json.dumps(result,indent=2,allow_nan=False)+'\n').encode())

if __name__=='__main__':main()
