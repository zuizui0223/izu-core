from pathlib import Path
import json,hashlib,zipfile,itertools,numpy as np
r=Path.cwd();c=r/'outputs/model3_precision_feasibility/fastpath_candidate';d=c/'gate_n9_1000'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
h=json.loads((d/'sources.json').read_text())
with zipfile.ZipFile(d/'sources.zip') as z:
 for p,v in h.items():assert sha(c/p)==v==hashlib.sha256(z.read(p)).hexdigest(),p
rows=[]
for setting,arm,scheme in itertools.product(['assurance_cost','prior_selfing'],['near','far'],['jump','heat_fv']):
 key=f'{setting}_{arm}_{scheme}';v=json.loads((d/(key+'.json')).read_text());records=v['records'];assert v['failure'] is None and len(records)==1000
 assert [a['period'] for a in records]==list(range(1,1001))
 for a in records:
  assert a['path_l1']<=1e-5 and a['mass_gap']<=1e-5 and a['negative_mass']<=1e-10 and not a['occupancy_mismatch'] and (a['trait_gap'] is None or a['trait_gap']<=1e-6)
 p=d/(key+'.npz');assert sha(p)==v['checkpoint_sha256']
 with np.load(p) as z:
  dense=np.einsum('abc,ia,jb,kc->ijk',z['core'],*[z[f'factor{k}'] for k in range(3)],optimize=True).ravel()
  np.testing.assert_allclose(dense,z['compressed_1000'],rtol=1e-12,atol=1e-14)
  for t in [200,400,1000]:
   b=z[f'baseline_{t}'];a=z[f'compressed_{t}'];l1=float(np.abs(a-b).sum()/b.sum())
   assert abs(l1-records[t-1]['path_l1'])<1e-12
 rows.append(dict(key=key,max_l1=max(a['path_l1'] for a in records),max_trait=max(a['trait_gap'] or 0 for a in records),max_negative=max(a['negative_mass'] for a in records),npz_sha256=sha(p),seconds=v['seconds']))
out=r/'outputs/model3_precision_feasibility/n9_long_verified.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in d.iterdir():z.write(p,p.name)
v=dict(scope='n9 integrated solver versus same-grid exact density; not grid convergence',completed=8,planned=8,source_hashes_verified=len(h),rows=rows,archive_sha256=sha(out))
(r/'data/results/model3_n9_long_verified_20261005.json').write_text(json.dumps(v,indent=2));print(json.dumps(v,indent=2))
