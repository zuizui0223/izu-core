"""Independent read-only arithmetic audit; imports no runner/Model3/inference.

Verifies saved five-field arrays and derives both paired endpoints directly.
This is not an independent implementation of the biological process.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.stats import t as student

FIELDS=('alleles','allele_origin','mutation_flags','ids','birth_years')


def encoded(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def unpack(path,contract_hash):
    with np.load(path,allow_pickle=False) as z:
        m=json.loads(z['_meta'].tobytes())
        a={k:np.array(z[k]) for k in z.files if k!='_meta'}
    h=hashlib.sha256(encoded({k:v for k,v in m.items() if k!='payload_sha256'}))
    for k in sorted(a):
        x=a[k];h.update(encoded([k,x.dtype.str,list(x.shape)]));h.update(x.tobytes())
    if h.hexdigest()!=m['payload_sha256']:raise ValueError('raw archive hash mismatch')
    if m['contract_sha256']!=contract_hash:raise ValueError('raw contract mismatch')
    if set(a)!=set(FIELDS)|{'counts'}:raise ValueError('wrong five-field schema')
    if len(a['counts'])!=m['task']['end']-m['task']['start']+1 or m['current']!=m['task']['end']:
        raise ValueError('incomplete checkpoint')
    if a['counts'].dtype!=np.dtype('int64') or np.any((a['counts']<0)|(a['counts']>48)):
        raise ValueError('invalid census counts')
    for k in FIELDS:
        shape=(len(a['counts']),48,3,2) if k in FIELDS[:3] else (len(a['counts']),48)
        if a[k].shape!=shape:raise ValueError('wrong array shape')
    return m,a


def audit(root,summary=None):
    root=Path(root);manifest=json.loads((root/'RUN.json').read_text());p=manifest['plan']
    check=hashlib.sha256(encoded({k:v for k,v in manifest.items() if k!='contract_sha256'})).hexdigest()
    if check!=manifest['contract_sha256'] or p['mode']!='technical' or p['confirmation_authorized']:
        raise ValueError('not the source-bound technical contract')
    nf,nv=len(p['founders']),len(p['visitors']);records={};files=0;states=0;fork_matches=0
    expected_names=set()
    genetic=np.zeros((nf,nv,2),np.int64);alive=np.zeros((nf,nv,2,2),np.int64)
    for fi,f in enumerate(p['founders']):
        for vi,v in enumerate(p['visitors']):
            original=None
            for pi,policy in enumerate(p['policies']):
                pre=None
                for stage,b,start,end in [('prefix',8.,0,35),('B8',8.,35,80),('B4p5',4.5,35,80)]:
                    name=f'{f}_{v}_{policy}_{stage}.npz';expected_names.add(name)
                    m,a=unpack(root/'states'/name,check);files+=1;states+=len(a['counts'])
                    if m['task']!=dict(founder=f,visitor=v,policy=policy,stage=stage,budget=b,start=start,end=end):
                        raise ValueError('wrong stage identity')
                    key=f"{p['namespace']}|{'prefix' if stage=='prefix' else 'fork'}|{f}|{v}".encode()
                    if m['master']!=int.from_bytes(hashlib.sha256(key).digest()[:16],'big'):
                        raise ValueError('unmatched stage streams')
                    if stage=='prefix':
                        if original is None:original={k:a[k][0].copy() for k in FIELDS}
                        if any(not np.array_equal(a[k][0],original[k]) for k in FIELDS):
                            raise ValueError('unmatched initial policy genotypes')
                        if a['counts'][0]!=48 or not np.all(a['alleles'][0,:,2,:].mean(axis=1)==.5):
                            raise ValueError('initial A expression is not paired')
                        if not np.var(a['alleles'][0,:,2,:]):raise ValueError('missing standing A variation')
                        pre=(m,a)
                    else:
                        pm,pa=pre
                        if m['parent_payload_sha256']!=pm['payload_sha256']:
                            raise ValueError('fork provenance mismatch')
                        if any(not np.array_equal(a[k][0],pa[k][-1]) for k in FIELDS):
                            raise ValueError('fork clone mismatch')
                        fork_matches+=1
                    target=float(original['alleles'][:,1,:].mean())
                    if m['target_I']!=target:raise ValueError('founder target changed')
                    prev=None
                    for i,n in enumerate(a['counts']):
                        if n:
                            if not np.all(a['birth_years'][i,:n]==start+i):raise ValueError('birth year mismatch')
                            if not np.array_equal(a['ids'][i,:n],np.arange((start+i)*48,(start+i)*48+n)):
                                raise ValueError('individual IDs invalid')
                            if a['mutation_flags'][i,:n].any():raise ValueError('new mutation in closed source')
                            origins=a['allele_origin'][i,:n]
                            if np.any((origins<0)|(origins>=288)):raise ValueError('foreign allele origin')
                            if not np.array_equal(a['alleles'][i,:n],original['alleles'].reshape(-1)[origins]):
                                raise ValueError('genotype/origin inconsistency')
                            loc=(origins%6)//2
                            if not np.array_equal(loc,np.broadcast_to(np.arange(3)[None,:,None],loc.shape)):
                                raise ValueError('allele translocated across loci')
                        now=[set(a['alleles'][i,:n,k,:].ravel()) for k in range(3)]
                        if prev is not None and any(not now[k]<=prev[k] for k in range(3)):
                            raise ValueError('new inherited allele after closure')
                        prev=now
                    if stage!='prefix':
                        pa=pre[1]
                        counts=np.concatenate((pa['counts'],a['counts'][1:]))
                        alleles=np.concatenate((pa['alleles'],a['alleles'][1:]))
                        if len(counts)!=81:raise ValueError('incomplete full history')
                        tg=te=None
                        for year,n in enumerate(counts):
                            if n==0:
                                if te is None:te=year
                            else:
                                if te is not None:raise ValueError('resurrection')
                                if tg is None and alleles[year,:n,1,:].max()<target-1e-12:tg=year
                        status='extinct' if counts[-1]==0 else ('alive_closed' if tg is not None else 'alive_accessible')
                        records[f,v,policy,stage]=dict(status=status,G=tg is not None,E=(te is not None and tg is None))
                        bi=0 if stage=='B8' else 1
                        if bi==0:genetic[fi,vi,pi]=int(tg is not None)
                        alive[fi,vi,pi,bi]=int(counts[-1]>0)
    if {x.name for x in (root/'states').glob('*.npz')}!=expected_names:raise ValueError('unexpected extra state file')
    arrays=np.stack((genetic[:,:,1]-genetic[:,:,0],
        alive[:,:,1,1]-alive[:,:,0,1]-alive[:,:,1,0]+alive[:,:,0,0]),axis=-1).astype(float)
    centers=arrays.mean(axis=(0,1));row=arrays.mean(axis=1);col=arrays.mean(axis=0)
    interaction=arrays-row[:,None,:]-col[None,:,:]+centers
    var=((row-centers)**2).sum(axis=0)/nf**2+((col-centers)**2).sum(axis=0)/nv**2+(interaction**2).sum(axis=(0,1))/(nf*nv)**2
    critical=student.ppf(1-.025/2,min(nf,nv)-1)
    if summary is not None:
        if summary['genetic_loss_inputs']!=genetic.tolist() or summary['occupancy_inputs']!=alive.tolist():
            raise ValueError('upstream event matrix mismatch')
        if summary['status']!='TECHNICAL_PIPELINE_ONLY_NOT_SCIENTIFIC_EVIDENCE':raise ValueError('evidence status changed')
        for k,x in enumerate(summary['endpoint_analysis']['endpoints']):
            if not np.isclose(x['estimate'],centers[k],rtol=0,atol=1e-12) or not np.isclose(x['variance'],var[k],rtol=0,atol=1e-12):
                raise ValueError('endpoint arithmetic mismatch')
            if var[k]>1e-15:
                ci=[centers[k]-critical*np.sqrt(var[k]),centers[k]+critical*np.sqrt(var[k])]
                if not np.allclose(ci,x['interval'],rtol=0,atol=1e-12):raise ValueError('candidate interval mismatch')
                sign='positive' if ci[0]>0 else 'negative' if ci[1]<0 else 'unresolved'
                if x['classification']!=sign:raise ValueError('direction classification mismatch')
            elif x['interval'] is not None:raise ValueError('degenerate interval invented')
        for row in summary['arms']:
            stage='B8' if row['budget']==8 else 'B4p5'
            rs=[records[f,v,row['policy'],stage] for f in p['founders'] for v in p['visitors']]
            for status in ('alive_accessible','alive_closed','extinct'):
                if row[status]!=sum(x['status']==status for x in rs):raise ValueError('state count mismatch')
            if row['genetic_first']!=sum(x['G'] for x in rs) or row['extinction_first']!=sum(x['E'] for x in rs):
                raise ValueError('competing event mismatch')
    return dict(status='TECHNICAL_RAW_PIPELINE_AUDIT_PASS',files=files,saved_states=states,
        fork_start_matches=fork_matches,fields_per_state=5,confirmation_seeds_consumed=0,
        candidate_inference_matched=summary is not None,
        scope='Independent raw-array and endpoint arithmetic; not independently coded biology or effect confirmation')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True)
    p.add_argument('--summary',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    if a.out.exists():p.error('refuse overwrite')
    result=audit(a.root,json.loads(a.summary.read_text()))
    a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result))
