from pathlib import Path
from itertools import combinations_with_replacement
import numpy as np,json,time,hashlib,zipfile
from scripts.model3_batched_weight_integration import bounded_step
from scripts.model3_birth_marginal_reference import exact_next_marginals
from scripts.run_model3_full_mutation import config,exposure
c=Path.cwd();src=c/'batched_weight_fourth65';v=json.loads((src/'summary.json').read_text());p=src/'state.npz';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert v['status']=='passed_marginals' and sha(p)==v['npz_sha256']
out=c/'batched_weight_fifth65';out.mkdir(exist_ok=True)
if (out/'sources.json').exists():raise ValueError('preserve output')
files=list((c/'scripts').glob('*.py'))+list((c/'scripts/model3_island').glob('*.py'))+[c/'data/design/model3_ch2_bridge_20260927.json']
(out/'sources.json').write_text(json.dumps({f.relative_to(c).as_posix():sha(f) for f in files},indent=2))
with zipfile.ZipFile(out/'sources.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in files:z.write(f,f.relative_to(c).as_posix())
with np.load(p) as z:state=(z['core'],tuple(z[f'factor{k}'] for k in range(3)))
axis=np.linspace(0,1,65);means=np.array([(a+b)/2 for a,b in combinations_with_replacement(axis,2)]);cfg=config('assurance_cost',.01);visitors=exposure(76001,'near').visitors[4];start=time.monotonic();result=dict(input_sha256=sha(p),scope='fifth step from verified fourth-step state; local marginal/resource probe only')
import scripts.model3_binary_reader_projection as projection
original_basis=projection.project_basis
def observed_basis(read,shape,**kwargs):
 calls=0
 def observed_read(a,b):
  nonlocal calls
  calls+=1
  if calls==1 or calls%64==0:print('projection block',calls,'shape',shape,'columns',a,b,flush=True)
  return read(a,b)
 return original_basis(observed_read,shape,**kwargs)
projection.project_basis=observed_basis
try:
 print('reference marginal check',flush=True)
 expected=exact_next_marginals(state,(axis,)*3,visitors,cfg)
 print("reproduction step",flush=True)
 state,receipts=bounded_step(state,(axis,)*3,visitors,cfg,budget=16_000_000)
 core,fs=state;sums=[f.sum(axis=0) for f in fs];actual=[]
 for k in range(3):
  other=[j for j in range(3) if j!=k];vec=np.einsum('abc,'+','.join('abc'[j] for j in other)+'->'+'abc'[k],core,*[sums[j] for j in other],optimize=True);actual.append(fs[k]@vec)
 l1=max(float(np.abs(a-b).sum()/b.sum()) for a,b in zip(actual,expected));trait=max(float(abs(a@means/a.sum()-b@means/b.sum())) for a,b in zip(actual,expected))
 p=out/'state.npz';np.savez_compressed(p,core=core,**{f'factor{k}':f for k,f in enumerate(fs)},actual=actual,expected=expected)
 result.update(status='passed_marginals' if np.isfinite([l1,trait]).all() and l1<=1e-5 and trait<=1e-6 else 'failed',relative_marginal_l1=l1,trait_gap=trait,ranks=list(core.shape),records=receipts,npz_sha256=sha(p))
except (MemoryError,ArithmeticError,ValueError) as e:result.update(status='failed',error=str(e))
result['seconds']=time.monotonic()-start;(out/'summary.json').write_text(json.dumps(result,indent=2));print({k:v for k,v in result.items() if k!='records'},flush=True)
