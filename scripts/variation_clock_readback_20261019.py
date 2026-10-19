"""Read stored alleles only. No simulator imports or random draws."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile
import numpy as np
from scipy.stats import t

ROOT=Path(__file__).resolve().parents[1]
TRAITS=('M','I','A')
POLICIES=('fixed','evolving')
STAGES=('B8','B4p5')

def digest(raw):return hashlib.sha256(raw).hexdigest()
def file_hash(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
    return h.hexdigest()
def save_json(path,value):
    Path(path).write_bytes((json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode())
def require(value,message):
    if not value:raise ValueError(message)

def verify_receipt(data,receipt,code,source):
    r=json.loads(Path(receipt).read_text())
    require(r['analysis_sha256']==code,'receipt analysis mismatch')
    require(r['source_sha256']==source,'receipt source mismatch')
    require(r['output_sha256']==file_hash(data),'receipt output mismatch')
    return r

def trajectory(a,n):
    a=np.asarray(a);n=np.asarray(n)
    require(a.ndim==4 and a.shape[2:]==(3,2) and n.shape==(len(a),),'state shape')
    require(n.dtype.kind in 'iu' and np.all((n>=0)&(n<=a.shape[1])),'population counts')
    occupied=n>0
    require(not np.any(np.diff(occupied.astype(int))>0),'reappearance after extinction')
    mask=np.arange(a.shape[1])[None,:]<n[:,None]
    require(np.isfinite(a).all() and not np.any(a[~mask]),'nonfinite or nonzero padding')
    flat=a.transpose(0,2,1,3).reshape(len(a),3,-1)
    valid=np.arange(flat.shape[-1])[None,None,:]<(2*n)[:,None,None]
    ordered=np.sort(np.where(valid,flat,np.inf),axis=-1)
    richness=(np.sum((ordered[:,:,1:]!=ordered[:,:,:-1]) & np.isfinite(ordered[:,:,1:]),axis=-1)+occupied[:,None]).astype(np.int16)
    require(not np.any(np.diff(richness,axis=0)>0),'allele richness increased')
    mean=np.sum(a,axis=(1,3))/np.maximum(2*n[:,None],1)
    expressed=a.mean(axis=-1)
    variance=np.sum(np.where(mask[:,:,None],(expressed-mean[:,None,:])**2,0),axis=1)/np.maximum(n[:,None],1)
    first=np.array([np.flatnonzero(richness[:,l]==1)[0] if np.any(richness[:,l]==1) else -1 for l in range(3)],dtype=np.int16)
    value=np.array([ordered[first[l],l,0] if first[l]>=0 else np.nan for l in range(3)])
    extinct=np.flatnonzero(~occupied)
    return dict(richness=richness,mean=mean,genotype_variance=variance,first_fix=first,fixed_value=value,extinction=int(extinct[0]) if len(extinct) else -1)

def join_states(prefix,future):
    a,n=prefix;b,m=future
    require(np.array_equal(a[-1],b[0]) and n[-1]==m[0],'fork mismatch')
    return np.concatenate((a,b[1:])),np.concatenate((n,m[1:]))

def crossed(d):
    d=np.asarray(d,dtype=float);nf,nv=d.shape
    require(nf>1 and nv>1 and np.isfinite(d).all(),'crossed matrix')
    mean=float(d.mean());row=d.mean(axis=1)-mean;col=d.mean(axis=0)-mean
    residual=d-mean-row[:,None]-col[None,:]
    var=float(np.sum(row**2)/nf**2+np.sum(col**2)/nv**2+np.sum(residual**2)/(nf*nv)**2)
    df=min(nf,nv)-1
    def interval(alpha):
        radius=float(t.ppf(1-alpha/2,df)*np.sqrt(var))
        return [mean-radius,mean+radius] if var>0 else None
    return dict(estimate=mean,variance=var,degrees_of_freedom=df,pointwise_interval=interval(.05),simultaneous_interval=interval(.05/12),founder_marginal_range=[float(d.mean(axis=1).min()),float(d.mean(axis=1).max())],visitor_marginal_range=[float(d.mean(axis=0).min()),float(d.mean(axis=0).max())])

def read_state(z,name,manifest):
    raw=z.read(name);require(digest(raw)==manifest[name],'member hash '+name)
    with np.load(io.BytesIO(raw),allow_pickle=False) as data:
        return data['alleles'],data['counts']

def extract(root,out):
    root=Path(root);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    inventory=json.loads((ROOT/'docs/audits/CHAPTER2_CONFIRM160_ASSET_SHA256_20261019.json').read_text())
    require({p.name for p in root.iterdir()}==set(inventory),'source asset inventory')
    for name,sha in inventory.items():require(file_hash(root/name)==sha,'source asset hash '+name)
    print('All97 original asset hashes verified',flush=True)
    code=file_hash(Path(__file__))
    inputs=dict(source_assets=inventory,analysis_sha256=code,scope='post-outcome read-only, zero simulation')
    if (out/'INPUTS.json').exists():require(json.loads((out/'INPUTS.json').read_text())==inputs,'existing input provenance mismatch')
    else:save_json(out/'INPUTS.json',inputs)
    for shard in range(32):
        dest=out/f'shard-{shard}.npz';receipt=out/f'shard-{shard}.json'
        if receipt.exists():
            verify_receipt(dest,receipt,code,inventory[f'raw-shard-{shard}.zip'])
            print('Verified completed shard',shard,flush=True);continue
        require(not dest.exists(),'unreceipted shard output; preserve and investigate')
        coordinates=np.array([(fi,vi) for fi in range(160) for vi in range(160) if (fi*160+vi)%32==shard])
        shape=(len(coordinates),2,2,81,3)
        richness=np.zeros(shape,dtype=np.int16);means=np.zeros(shape);variances=np.zeros(shape)
        first=np.full(shape[:3]+(3,),-1,dtype=np.int16);values=np.full(first.shape,np.nan)
        extinction=np.full(shape[:3],-1,dtype=np.int16)
        with zipfile.ZipFile(root/f'raw-shard-{shard}.zip') as z:
            require(len(z.namelist())==len(set(z.namelist())),'duplicate archive members')
            manifest=json.loads(z.read('ARCHIVE_MANIFEST.json'))
            require(set(z.namelist())==set(manifest)|{'ARCHIVE_MANIFEST.json'},'archive inventory')
            for ci,(fi,vi) in enumerate(coordinates):
                for pi,policy in enumerate(POLICIES):
                    prefix=read_state(z,f'states/{501001+fi}_{502001+vi}_{policy}_prefix.npz',manifest)
                    require(prefix[0].shape==(36,48,3,2),'prefix shape')
                    for bi,stage in enumerate(STAGES):
                        future=read_state(z,f'states/{501001+fi}_{502001+vi}_{policy}_{stage}.npz',manifest)
                        require(future[0].shape==(46,48,3,2),'future shape')
                        a,n=join_states(prefix,future);r=trajectory(a,n)
                        richness[ci,pi,bi]=r['richness'];means[ci,pi,bi]=r['mean'];variances[ci,pi,bi]=r['genotype_variance']
                        first[ci,pi,bi]=r['first_fix'];values[ci,pi,bi]=r['fixed_value'];extinction[ci,pi,bi]=r['extinction']
        with dest.open('xb') as f:np.savez_compressed(f,coordinates=coordinates,richness=richness,means=means,genotype_variances=variances,first_fix=first,fixed_value=values,extinction=extinction)
        save_json(receipt,dict(analysis_sha256=code,source_sha256=inventory[f'raw-shard-{shard}.zip'],output_sha256=file_hash(dest),crossings=len(coordinates)))
        print('Completed shard',shard,'crossings',len(coordinates),flush=True)

def distribution(x):
    x=np.asarray(x);x=x[np.isfinite(x)]
    return dict(n=len(x),minimum=float(x.min()) if len(x) else None,median=float(np.median(x)) if len(x) else None,maximum=float(x.max()) if len(x) else None,mean=float(x.mean()) if len(x) else None)

def summarize(out):
    out=Path(out)
    inputs=json.loads((out/'INPUTS.json').read_text())
    inventory=json.loads((ROOT/'docs/audits/CHAPTER2_CONFIRM160_ASSET_SHA256_20261019.json').read_text())
    code=file_hash(Path(__file__))
    require(inputs['analysis_sha256']==code and inputs['source_assets']==inventory,'summary input provenance mismatch')
    first=np.full((160,160,2,2,3),-2,dtype=np.int16);values=np.full(first.shape,np.nan)
    duration=np.zeros(first.shape);extinction=np.full(first.shape[:-1],-2,dtype=np.int16)
    curves=np.zeros((2,2,81,3,5));seen=set();founder_means=np.zeros((160,3))
    for shard in range(32):
        path=out/f'shard-{shard}.npz';verify_receipt(path,out/f'shard-{shard}.json',code,inventory[f'raw-shard-{shard}.zip'])
        with np.load(path,allow_pickle=False) as saved:
            z={k:saved[k] for k in saved.files}
            for ci,(fi,vi) in enumerate(z['coordinates']):
                require((int(fi),int(vi)) not in seen,'duplicate crossing');seen.add((int(fi),int(vi)))
                rich=z['richness'][ci];first[fi,vi]=z['first_fix'][ci];values[fi,vi]=z['fixed_value'][ci];extinction[fi,vi]=z['extinction'][ci]
                duration[fi,vi]=np.sum(rich[:,:,:80]>1,axis=2)
                founder_means[fi]=z['means'][ci,0,0,0]
                for pi in range(2):
                    for bi in range(2):
                        rr=rich[pi,bi];occupied=rr>0
                        curves[pi,bi,:,:,0]+=rr>1;curves[pi,bi,:,:,1]+=rr==1;curves[pi,bi,:,:,2]+=rr==0
                        curves[pi,bi,:,:,3]+=rr
                        curves[pi,bi,:,:,4]+=z['genotype_variances'][ci,pi,bi]
    require(seen=={(f,v) for f in range(160) for v in range(160)} and np.all(first>=-1),'incomplete crossing matrix')
    results=[];contrasts=[]
    for bi,stage in enumerate(STAGES):
        for li,locus in enumerate(TRAITS):
            for pi,policy in enumerate(POLICIES):
                ff=first[:,:,pi,bi,li];vv=values[:,:,pi,bi,li];ee=extinction[:,:,pi,bi]
                fixed=ff>=0;alive=ee<0;curve=curves[pi,bi,:,li]
                result=dict(budget=stage,trait=locus,policy=policy,n=25600,fixed_before_extinction=int(fixed.sum()),extinct_without_fixation=int(((~fixed)&(~alive)).sum()),alive_unfixed=int(((~fixed)&alive).sum()),fixed_then_extinct=int((fixed&(~alive)).sum()),fixation_time_among_events=distribution(ff[fixed]),fixed_value=distribution(vv),fixed_below_founder=int(np.sum(fixed&(vv<founder_means[:,li,None]))),fixed_equal_founder=int(np.sum(fixed&(vv==founder_means[:,li,None]))),fixed_above_founder=int(np.sum(fixed&(vv>founder_means[:,li,None]))),occupied_polymorphic_duration_mean=float(duration[:,:,pi,bi,li].mean()),curves=dict(occupied_polymorphic=curve[:,0].astype(int).tolist(),occupied_monomorphic=curve[:,1].astype(int).tolist(),extinct=curve[:,2].astype(int).tolist(),cumulative_fixation=[int(np.sum(fixed&(ff<=c))) for c in range(81)],mean_richness_among_occupied=np.divide(curve[:,3],25600-curve[:,2],out=np.zeros(81),where=curve[:,2]<25600).tolist(),mean_genotype_variance_among_occupied=np.divide(curve[:,4],25600-curve[:,2],out=np.zeros(81),where=curve[:,2]<25600).tolist()))
                if locus!='M':
                    u,counts=np.unique(vv[fixed],return_counts=True);result['fixed_value_counts']=[dict(value=float(v),count=int(n)) for v,n in zip(u,counts)]
                results.append(result)
            for label,d in [('fixation_by80',(first[:,:,1,bi,li]>=0).astype(float)-(first[:,:,0,bi,li]>=0)),('occupied_polymorphic_duration',duration[:,:,1,bi,li]-duration[:,:,0,bi,li])]:
                contrasts.append(dict(budget=stage,trait=locus,endpoint=label,**crossed(d)))
    order=[]
    for bi,stage in enumerate(STAGES):
        for pi,policy in enumerate(POLICIES):
            aa=first[:,:,pi,bi,2];ii=first[:,:,pi,bi,1];both=(aa>=0)&(ii>=0)
            order.append(dict(budget=stage,policy=policy,both_A_first=int((both&(aa<ii)).sum()),both_I_first=int((both&(ii<aa)).sum()),both_tied=int((both&(aa==ii)).sum()),A_only=int(((aa>=0)&(ii<0)).sum()),I_only=int(((ii>=0)&(aa<0)).sum()),neither=int(((aa<0)&(ii<0)).sum())))
    save_json(out/'SUMMARY.json',dict(status='COMPLETE_READ_ONLY_POST_OUTCOME',crossings=25600,source_task_files=153600,stored_state_records=6553600,distinct_saved_states_excluding_duplicate_forks=6451200,source_sha256=json.loads((out/'INPUTS.json').read_text())['source_assets'],analysis_sha256=file_hash(Path(__file__)),results=results,contrasts=contrasts,A_I_order=order,inference='post-outcome paired two-axis variance; t159; pointwise95 and Bonferroni12 family95; no iid cell inference; no universal coverage',limits=['Fixed A expression .5 does not equal absence of latent A alleles','M/I/A initial allele counts differ','B4.5 duration mixes extinction and fixation','No new transition simulation or causal mediation']))
    print('Summary complete',flush=True)

def seed_transfer(out,archive):
    out=Path(out);archive=Path(archive)
    receipt=json.loads((ROOT/'docs/audits/CHAPTER2_READAPTATION_RELEASE_READBACK_20261019.json').read_text())
    require(file_hash(archive)==receipt['sha256'],'seed archive hash')
    donors={}
    for shard in (0,8,16,24):
        with np.load(out/f'shard-{shard}.npz',allow_pickle=False) as saved:
            z={k:saved[k] for k in saved.files}
        for ci,(fi,vi) in enumerate(z['coordinates']):
            if fi not in (0,40,80,120) or vi not in (0,40,80,120):continue
            for pi,policy in enumerate(POLICIES):
                donors[int(fi),int(vi),policy]=(z['richness'][ci,pi,0,-1],z['means'][ci,pi,0,-1],z['means'][ci,pi,0,0])
    rows=[]
    with zipfile.ZipFile(archive) as z:
        manifest=json.loads(z.read('cohorts/manifest.json'))
        for item in manifest['files']:
            raw=z.read('cohorts/'+item['file']);require(digest(raw)==item['sha256'],'seed cohort hash')
            with np.load(io.BytesIO(raw),allow_pickle=False) as saved:a=saved['alleles']
            n=len(a);require(n>0,'empty cohort requires explicit denominator handling')
            cr=np.array([len(np.unique(a[:,l,:])) for l in range(3)])
            cm=a.mean(axis=(0,2));dr,dm,fm=donors[tuple(item['key'][:3])]
            require(np.all(cr<=dr),'cohort richness exceeds donor')
            rows.append(dict(key=item['key'],size=n,donor_richness=dr.tolist(),cohort_richness=cr.tolist(),donor_mean=dm.tolist(),cohort_mean=cm.tolist(),founder_mean=fm.tolist(),new_monomorphism_at_transfer=((dr>1)&(cr==1)).tolist(),entry_I_at_or_above_founder=bool(cm[1]>=fm[1])))
    require(len(rows)==64 and len({tuple(r['key']) for r in rows})==64,'cohort inventory')
    groups=[]
    for policy in POLICIES:
        rr=[r for r in rows if r['key'][2]==policy]
        groups.append(dict(policy=policy,cohorts=len(rr),new_monomorphism_at_transfer=np.sum([r['new_monomorphism_at_transfer'] for r in rr],axis=0).tolist(),donor_polymorphic_cohort_sources=np.sum([np.array(r['donor_richness'])>1 for r in rr],axis=0).tolist(),cohort_polymorphic=np.sum([np.array(r['cohort_richness'])>1 for r in rr],axis=0).tolist(),entry_I_at_or_above_founder=sum(r['entry_I_at_or_above_founder'] for r in rr)))
    save_json(out/'SEED_TRANSFER.json',dict(scope='64 nested cohorts from32 donors; no additional independent founding evidence',trait_order=TRAITS,source_archive_sha256=receipt['sha256'],groups=groups,rows=rows))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--summary-only',action='store_true');p.add_argument('--seed-archive',type=Path);args=p.parse_args()
    if not args.summary_only:extract(args.source,args.output)
    summarize(args.output)
    if args.seed_archive:seed_transfer(args.output,args.seed_archive)
