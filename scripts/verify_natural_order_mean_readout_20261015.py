"""Read saved genomes only; independent all-start arithmetic and inheritance audit."""
import argparse
from collections import defaultdict
import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np

BLOCKS=('main','confirmation')
TARGETS=(1.05,1.5)
CLASSES=('assurance_first','investment_first','near_simultaneous','assurance_only','investment_only','neither')
FIELDS=('alleles','allele_origin','mutation_flags','ids','birth_years')
sha=lambda b:hashlib.sha256(b).hexdigest()


def independent_summary(rows):
    sums=defaultdict(lambda:[0,0,0,0,0,0,0])
    for r in rows:
        if r['block'] not in BLOCKS or r['target'] not in TARGETS or r['category'] not in CLASSES:
            raise ValueError('unregistered original group')
        for block in (r['block'],'pooled_descriptive'):
            x=sums[(block,r['target'],r['category'])]
            x[0]+=1;x[1]+=r['native'];x[2]+=r['normalized']
            x[3]+=r['native_duration'];x[4]+=r['normalized_duration']
            x[5]+=int(r['native']==0 and r['normalized']==1)
            x[6]+=int(r['native']==1 and r['normalized']==0)
    groups=[]
    for b in (*BLOCKS,'pooled_descriptive'):
        for t in TARGETS:
            for c in CLASSES:
                n,old,new,od,nd,gain,loss=sums[(b,t,c)]
                groups.append(dict(block=b,target=t,category=c,starts=n,native_survivors=old,
                    normalized_survivors=new,native_fraction=old/n if n else None,
                    normalized_fraction=new/n if n else None,native_duration_sum=od,
                    normalized_duration_sum=nd,native_mean_duration=od/n if n else None,
                    normalized_mean_duration=nd/n if n else None,paired_gains=gain,paired_losses=loss,
                    occupancy_change=new/n-old/n if n else None,duration_change=nd/n-od/n if n else None))
    index={(r['block'],r['target'],r['category']):r for r in groups};gaps=[]
    for b in (*BLOCKS,'pooled_descriptive'):
        for t in TARGETS:
            a=index[b,t,'assurance_first'];i=index[b,t,'investment_first']
            row=dict(block=b,target=t,assurance_first_n=a['starts'],investment_first_n=i['starts'])
            for endpoint,field in [('occupancy','fraction'),('duration','mean_duration')]:
                valid=bool(a['starts'] and i['starts'])
                for p in ('native','normalized'):
                    row[p+'_'+endpoint+'_gap']=a[p+'_'+field]-i[p+'_'+field] if valid else None
                row[endpoint+'_attenuation']=row['native_'+endpoint+'_gap']-row['normalized_'+endpoint+'_gap'] if valid else None
            gaps.append(row)
    return groups,gaps


def load(path):
    raw=Path(path).read_bytes()
    with np.load(io.BytesIO(raw),allow_pickle=False) as z:
        meta=json.loads(str(z['metadata'].item()))
        arrays={f:z[f].copy() for f in z.files if f!='metadata'}
    return raw,meta,arrays


def audit_inheritance(d):
    n=d['population'];off=d['offsets']
    if n.shape!=(201,) or off.shape!=(202,) or not np.array_equal(np.diff(off),n):
        raise ValueError('all201censuses required')
    if len(d['parentage'])!=sum(n[1:]) or d['parentage'].shape[1:]!=(3,):
        raise ValueError('complete native parentage required')
    ptr=0;rows=0
    for t in range(201):
        a,b=map(int,off[t:t+2]);size=int(n[t]);rows+=size
        if size:
            if not np.isfinite(d['alleles'][a:b]).all():raise ValueError('nonfinite genome')
            np.testing.assert_allclose(d['means'][t],d['alleles'][a:b].mean(axis=(0,2)),atol=1e-12,rtol=0)
        elif not np.isnan(d['means'][t]).all() or n[t:].any():raise ValueError('absorbing extinction')
        if t==0:continue
        pa,pb=map(int,off[t-1:t+1]);parents=d['parentage'][ptr:ptr+size];ptr+=size
        np.testing.assert_array_equal(parents[:,0],d['ids'][a:b])
        if not (d['birth_years'][a:b]==200+t).all():raise ValueError('birth clock')
        lookup={int(v):j for j,v in enumerate(d['ids'][pa:pb])}
        for copy,column in [(0,1),(1,2)]:
            which=np.array([lookup[int(v)] for v in parents[:,column]],dtype=int)
            origins=d['allele_origin'][a:b,:,copy,None]==d['allele_origin'][pa:pb][which]
            same=origins&(d['alleles'][a:b,:,copy,None]==d['alleles'][pa:pb][which])
            same &= d['mutation_flags'][a:b,:,copy,None]==d['mutation_flags'][pa:pb][which]
            if not origins.any(2).all():raise ValueError('parental allele origin missing')
            if not same[:,0].any(1).all():raise ValueError('nonmutating matching locus transmission')
            if not (same.any(2)|d['mutation_flags'][a:b,:,copy]).all():
                raise ValueError('unflagged inherited-value change')
    return rows,ptr


def admitted_freeze(path,expected_sha):
    raw=Path(path).read_bytes()
    if sha(raw)!=expected_sha:
        raise ValueError('external published freeze digest mismatch')
    return json.loads(raw)


def verify(output,bank,original,out,expected_freeze_sha):
    root=Path(output)
    official=json.loads((root/'READOUT.json').read_text())
    if official['status']!='ALL2048_PRODUCTION_AND_INDEPENDENT_REPLAY_VERIFIED':
        raise ValueError('complete production/replay gate required before inspection')
    frozen=admitted_freeze(root/'EXECUTION_FREEZE.json',expected_freeze_sha)
    if official['source_freeze_sha256']!=sha((root/'EXECUTION_FREEZE.json').read_bytes()):
        raise ValueError('freeze identity')
    raw=Path(bank).read_bytes()
    if sha(raw)!=frozen['bank_sha256']:raise ValueError('bank identity')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        m=json.loads(z.read('MANIFEST.json'))
        with np.load(io.BytesIO(z.read('states.npz')),allow_pickle=False) as z2:
            states={f:z2[f].copy() for f in FIELDS}
    replay=json.loads((root/'REPLAY_COMPLETE.json').read_text())
    if replay['paths']!=2048:raise ValueError('all2048full-replay receipts required')
    replay_hashes={tuple(sorted(r['task'].items())):r['sha256'] for r in replay['records']}
    rows=[];seen=set();genome_rows=parent_rows=0;archive_hashes={}
    for ix,case in enumerate(m['cases']):
        for target in TARGETS:
            task=dict(block=case['task']['block'],replicate=case['task']['replicate'],target=target)
            key=sha(json.dumps(task,sort_keys=True).encode())[:24]
            b,meta,d=load(root/'paths'/(key+'.npz'));archive_hashes[key]=sha(b)
            if meta['task']!=task or meta['category']!=case['category'] or meta['bank_sha256']!=sha(raw):
                raise ValueError('controlled archive identity')
            if replay_hashes[tuple(sorted(task.items()))]!=sha(b):raise ValueError('replayed archive changed')
            starting={f:d[f][:8] for f in FIELDS};expected=states['alleles'][ix].copy()
            expected[:,2,:]+=.5-float(expected[:,2,:].mean())
            np.testing.assert_array_equal(starting['alleles'],expected)
            for f in FIELDS[1:]:np.testing.assert_array_equal(starting[f],states[f][ix])
            master_task=dict(study='history',block=task['block'],replicate=task['replicate'])
            seed=int.from_bytes(hashlib.sha256(('resolution-v1-20261011:challenge'+json.dumps(master_task,sort_keys=True)).encode()).digest()[:16],'big')
            if meta['master_seed']!=seed:raise ValueError('original seed coupling')
            g,p=audit_inheritance(d);genome_rows+=g;parent_rows+=p
            oldtask=dict(case['task'],target=target);oldkey=sha(json.dumps(oldtask,sort_keys=True).encode())[:24]
            oldraw,oldmeta,old=load(Path(original)/'archives/challenge'/(oldkey+'.npz'))
            if sha(oldraw)!=case['original_futures'][str(target)] or oldmeta['task']!=oldtask:
                raise ValueError('original future identity')
            rows.append(dict(task,category=case['category'],native=int(old['population'][200]>0),
                normalized=int(d['population'][200]>0),native_duration=int(sum(old['population'][1:]>0)),
                normalized_duration=int(sum(d['population'][1:]>0))))
            seen.add((task['block'],task['replicate'],target))
    if len(seen)!=2048 or len(archive_hashes)!=2048:raise ValueError('complete unique all-start inventory')
    groups,gaps=independent_summary(rows)
    if groups!=official['groups'] or gaps!=official['strict_gaps']:
        raise ValueError('independent arithmetic differs')
    if official['completed_updates']!=820804 or official['cumulative_reserved_updates']!=820804:
        raise ValueError('frozen native accounting')
    result=dict(status='ALL2048_RAW_GENOME_SEED_PARENTAGE_AND36_GROUPS_INDEPENDENTLY_VERIFIED',
        source_sha256=sha(Path(__file__).read_bytes()),readout_sha256=sha((root/'READOUT.json').read_bytes()),
        source_freeze_sha256=official['source_freeze_sha256'],archives=2048,genome_rows=genome_rows,
        parent_rows=parent_rows,groups=36,strict_gaps=6,new_biological_updates=0,archive_sha256=archive_hashes,
        scope='Reads saved arrays only. Matching locus transmission exact; I/A origin/flag constraints checked. Independent native replay is the separate preceding gate. No unique historical mediation or natural-order causal benefit.')
    with Path(out).open('x',encoding='utf8') as f:json.dump(result,f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='archive_sha256'}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('output','bank','original','out'):p.add_argument('--'+name,required=True,type=Path)
    p.add_argument('--expected-freeze-sha',required=True)
    a=p.parse_args();verify(a.output,a.bank,a.original,a.out,a.expected_freeze_sha)
