"""Independent read-only reconstruction from saved five-field genotype arrays.

Does not import the companion runner, source reproduction, or transmission.
It is arithmetic validation of stored outcomes, not independent biological code.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np

FIELDS=('alleles','allele_origin','mutation_flags','ids','birth_years')

def audit(root):
    cohort=json.loads((root/'FUTURES.json').read_text())
    source=root.parent/'replayed_checkpoints'
    old=json.loads((source/'SOURCE_REPLAY.json').read_text())
    source_by_id={r['id']:r for r in old['records']}
    counts={};n_arrays=0;seen=set();valid_seeds={};equal_starts=0
    for row in cohort['records']:
        key=(row['fi'],row['vi'],row['rep'],row['policy'],row['budget'])
        if key in seen:raise AssertionError('duplicate case')
        seen.add(key)
        sid=f"f{row['fi']}v{row['vi']}r{row['rep']}_{row['policy']}"
        hist=source_by_id[sid]
        path=root/row['raw_npz']
        if hashlib.sha256(path.read_bytes()).hexdigest()!=row['raw_sha256']:raise AssertionError('raw file hash')
        seedkey=key[:3]
        if seedkey in valid_seeds and valid_seeds[seedkey]!=row['future_seed']:raise AssertionError('treatment seed mismatch')
        valid_seeds[seedkey]=row['future_seed']
        with np.load(path,allow_pickle=False) as z, np.load(source/(sid+'.npz'),allow_pickle=False) as orig:
            sizes=z['n']; target=row['target']; series=[];closed=[]
            assert sizes.shape==(46,) and np.all((sizes>=0)&(sizes<=48))
            for name in FIELDS:
                np.testing.assert_array_equal(z[name][0,:sizes[0]],orig[name])
            equal_starts+=1
            prev=None;dead=False
            for k,n0 in enumerate(sizes):
                n=int(n0);t=k+35;n_arrays+=1
                if dead:assert n==0
                dead |= n==0
                a=z['alleles'][k,:n]
                ids=z['ids'][k,:n]
                assert np.isfinite(a).all() and np.all((a>=0)&(a<=1))
                assert len(set(ids.tolist()))==n
                if n:
                    assert np.all(z['birth_years'][k,:n]==t)
                    assert np.all(ids//48==t)
                if prev is not None:
                    for j in range(3):assert set(np.unique(a[:,j,:]))<=set(np.unique(prev[:,j,:]))
                prev=a
                access=bool(a[:,1,:].max()>=target-1e-12) if n else None
                A=float(a[:,2,:].mean()) if n and row['policy']=='evolving' else .5 if n else None
                d=dict(t=t,n=n,alive=bool(n),mean_I=float(a[:,1,:].mean()) if n else None,
                    max_I=float(a[:,1,:].max()) if n else None,mean_A=A,accessible=access)
                given=row['series'][k]
                for field,value in d.items():
                    if type(value) is float:
                        assert abs(value-given[field])<1e-12
                    else:assert value==given[field]
                series.append(d)
                if n and not access:closed.append(t)
            histg=hist['first_I_loss']
            inherited_g=histg if histg is not None and histg<=35 else None
            g=inherited_g if inherited_g is not None else min(closed) if closed else None
            death=next((t+35 for t,n in enumerate(sizes) if n==0),None)
            event=('genetic_loss' if g is not None and (death is None or g<death)
                   else 'extinction' if death is not None else None)
            assert g==row['first_I_loss'] and death==row['first_extinction'] and event==row['first_competing_event']
            assert sum(bool(x['alive'] and x['accessible']) for x in series)==row['alive_accessible_censuses']
            final=series[-1]; arm=row['policy']+'_B'+str(row['budget'])
            acc=bool(final['alive'] and final['accessible'])
            c=counts.setdefault(arm,dict(paths=0,alive=0,alive_accessible=0,alive_closed=0,extinct=0,genetic_loss_first=0,extinction_first=0))
            c['paths']+=1;c['alive']+=int(final['alive']);c['alive_accessible']+=int(acc)
            c['alive_closed']+=int(final['alive'] and not acc);c['extinct']+=int(not final['alive'])
            c['genetic_loss_first']+=int(event=='genetic_loss');c['extinction_first']+=int(event=='extinction')
    assert len(seen)==288 and len(valid_seeds)==72 and equal_starts==288
    for c in counts.values():
        assert c['paths']==72
        assert c['alive_accessible']+c['alive_closed']+c['extinct']==72
        assert c['genetic_loss_first']+c['extinction_first']+c['alive_accessible']==72
    return dict(status='RAW_GENOTYPE_AND_DENOMINATOR_AUDIT_PASS',cases=len(seen),
        genotype_censuses_verified=n_arrays,matched_source_checkpoints=equal_starts,
        future_seed_blocks=len(valid_seeds),fields_per_state=5,counts=counts,
        future_summary_sha256=hashlib.sha256((root/'FUTURES.json').read_bytes()).hexdigest(),
        scope='Arithmetic/source identity check from raw arrays, not independent biological operator validation.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if a.out.exists():p.error('refuse overwrite')
    d=audit(a.root);a.out.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
