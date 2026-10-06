"""Diagnostic only: compress actual first-channel joint gamete distributions."""
from pathlib import Path
import hashlib,json,zipfile,time
import numpy as np
import scripts.model3_binary_reader_integration as integration
from scripts.model3_gamete_basis import gamete_basis
from scripts.model3_sharp_rounding import rounded
from scripts.run_model3_full_mutation import config,exposure
c=Path.cwd();out=c/'gamete_rank_probe';out.mkdir(exist_ok=True)
if (out/'sources.json').exists():raise ValueError('preserve existing diagnostic')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=list((c/'scripts').glob('*.py'))+list((c/'scripts/model3_island').glob('*.py'))+[c/'data/design/model3_ch2_bridge_20260927.json']
(out/'sources.json').write_text(json.dumps({p.relative_to(c).as_posix():sha(p) for p in files},indent=2),encoding='utf-8')
with zipfile.ZipFile(out/'sources.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,p.relative_to(c).as_posix())
p=c/'complete_ten65/assurance_cost_near_jump.npz';v=json.loads(p.with_suffix('.json').read_text(encoding='utf-8'));assert sha(p)==v['npz_sha256'] and v['failure_period']==3
with np.load(p) as z:state=(z['core'],tuple(z[f'factor{k}'] for k in range(3)))
rows=[];start=time.monotonic()
class Captured(Exception):pass
def capture(donor,recipient,axes,rate,sd,scheme,**kwargs):
 for name,parent in [('donor',donor),('recipient',recipient)]:
  gamete=gamete_basis(parent,axes,rate,sd,scheme,budget=16_000_000)
  full=np.einsum('abc,ia,jb,kc->ijk',gamete[0],*gamete[1],optimize=True)
  reduced,info=rounded(gamete,relative_l1=1e-10,budget=16_000_000)
  approx=np.einsum('abc,ia,jb,kc->ijk',reduced[0],*reduced[1],optimize=True)
  np.savez_compressed(out/(name+'.npz'),full=full,core=reduced[0],**{f'factor{k}':f for k,f in enumerate(reduced[1])})
  rows.append(dict(parent=name,full_shape=list(full.shape),ranks=list(reduced[0].shape),mass=float(full.sum()),absolute_l1=float(np.abs(full-approx).sum()),rounding=info,npz_sha256=sha(out/(name+'.npz'))))
 raise Captured()
integration.bounded_outcross=capture
try:integration.bounded_step(state,(np.linspace(0,1,65),)*3,exposure(76001,'near').visitors[2],config('assurance_cost',.01),budget=16_000_000)
except Captured:pass
result=dict(scope='joint gamete compressibility only; not integrated offspring admission',input_sha256=sha(p),rows=rows,seconds=time.monotonic()-start)
(out/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(result,flush=True)
