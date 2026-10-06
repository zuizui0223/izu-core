"""Conservative finite-volume continuation of the declared mutation diagnostic."""
import hashlib,json
from pathlib import Path
import numpy as np
from scripts.run_model3_mutation_memory import run_density,ROOT

out=ROOT/'outputs/model3_mutation_memory_heat_fv_20261004'
out.mkdir(parents=True,exist_ok=True)
rows=[]
for n in [11,21,41]:
 for u in [0.,.01]:
  for past in ['present','absent']:
   name=f'density_n{n}_heat_fv_u{u}_{past}'
   result=run_density(n,'heat_fv',u,past)
   np.savez_compressed(out/(name+'.npz'),**result)
   rows.append(dict(name=name,terminal_mean=float(result['trace'][-1,1])))
   print(name,rows[-1]['terminal_mean'],flush=True)
for past in ['present','absent']:
 def end(n):return next(r['terminal_mean'] for r in rows if r['name']==f'density_n{n}_heat_fv_u0.01_{past}')
 if abs(end(41)-end(21))>.005:
  name=f'density_n81_heat_fv_u0.01_{past}'
  result=run_density(81,'heat_fv',.01,past)
  np.savez_compressed(out/(name+'.npz'),**result)
  rows.append(dict(name=name,terminal_mean=float(result['trace'][-1,1])))
  print(name,rows[-1]['terminal_mean'],flush=True)
sources=['scripts/run_model3_mutation_memory_heat_fv.py','scripts/run_model3_mutation_memory.py','scripts/model3_island/birth_diffusion.py','scripts/model3_island/density.py','docs/superpowers/plans/2026-10-04-model3-mutation-memory-numerical-addendum.md']
result=dict(status='completed',rows=rows,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in sources},evidence_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.npz')})
(out/'manifest.json').write_text(json.dumps(result,indent=2)+'\n')
