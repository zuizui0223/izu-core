"""Summarize all declared mutation-memory cases without choosing favourable seeds."""
import hashlib,json,zipfile
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
original=ROOT/'outputs/model3_mutation_memory_20261004'
fv=ROOT/'outputs/model3_mutation_memory_heat_fv_20261004'
result={'status':'completed_diagnostic_not_attractor_test','abm':[],'density':[]}
rng=np.random.default_rng(10042026)
resamples=rng.integers(0,8,size=(10000,8))
for n in [48,192]:
 for u in [0.,.01]:
  arrays=[np.stack([np.load(original/f'abm_n{n}_u{u}_s{s}_{past}.npz')['trace'] for s in range(6101,6109)]) for past in ['present','absent']]
  a,b=arrays
  for t in [200,400,1000]:
   differences=a[:,t,1]-b[:,t,1]
   occupied=(a[:,t,0]>0)&(b[:,t,0]>0)
   ci=np.quantile(differences[resamples].mean(axis=1),[.025,.975]) if occupied.all() else [None,None]
   result['abm'].append(dict(capacity=n,mutation_rate=u,common_environment_periods=t-200,
     n_pairs=8,occupied_pairs=int(occupied.sum()),mean_past_present=float(np.nanmean(a[:,t,1])),
     mean_past_absent=float(np.nanmean(b[:,t,1])),paired_mean_gap=float(np.nanmean(differences)),
     descriptive_paired_bootstrap_95=list(ci),individual_paired_gaps=differences.tolist(),
     mean_allele_counts=[float(np.nanmean(v[:,t,3])) for v in arrays],
     last100_mean_change=[float(np.nanmean(v[:,t,1]-v[:,max(0,t-100),1])) for v in arrays]))
for folder,schemes in [(original,['jump','heat']),(fv,['heat_fv'])]:
 for n in [11,21,41,81]:
  for scheme in schemes:
   for u in [0.,.01]:
    for past in ['present','absent']:
     path=folder/f'density_n{n}_{scheme}_u{u}_{past}.npz'
     if not path.exists():
      if n==81:continue
      raise FileNotFoundError(path)
     d=np.load(path);trace=d['trace']
     result['density'].append(dict(nodes=n,scheme=scheme,mutation_rate=u,past=past,
       means=trace[[200,400,1000],1].tolist(),variances=trace[[200,400,1000],2].tolist(),
       last100_mean_change=float(trace[-1,1]-trace[-101,1]),minimum_mass=float(trace[:,0].min())))
def val(n,scheme,u,past):
 return next(r['means'][-1] for r in result['density'] if (r['nodes'],r['scheme'],r['mutation_rate'],r['past'])==(n,scheme,u,past))
result['precision']={}
for past in ['present','absent']:
 result['precision'][past]=dict(exact_grid_21_to_41=abs(val(41,'jump',.01,past)-val(21,'jump',.01,past)),
  fv_grid_21_to_41=abs(val(41,'heat_fv',.01,past)-val(21,'heat_fv',.01,past)),
  point_heat_grid_21_to_41=abs(val(41,'heat',.01,past)-val(21,'heat',.01,past)),
  fv_vs_jump_41=abs(val(41,'heat_fv',.01,past)-val(41,'jump',.01,past)))
result['precision']['continuation_rows']=[r for r in result['density'] if r['nodes']==81]
result['precision']['gates']={
 'point_heat_grid_pass':all(result['precision'][k]['point_heat_grid_21_to_41']<.005 for k in ['present','absent']),
 'finite_volume_grid_pass':all(result['precision'][k]['fv_grid_21_to_41']<.005 for k in ['present','absent']),
 'jump_grid_pass':all(result['precision'][k]['exact_grid_21_to_41']<.005 for k in ['present','absent']),
 'exact_vs_diffusion_pass':all(result['precision'][k]['fv_vs_jump_41']<.005 for k in ['present','absent'])}
result['claim_boundary']=['one evolving investment locus; access and assurance fixed',
 'synthetic rate .01 and width .05, not natural mutation estimates',
 'eight paired repeats; exploratory intervals, not confirmatory power or attractor evidence',
 'present-versus-absent200period past, followed by identical800period environment',
 'persistence of a gap at finite time does not establish alternative equilibria',
 'point-projected diffusion failure retained; finite-volume approximation not declared exactly equivalent to jump model']
result['source_sha256']={'scripts/summarize_model3_mutation_memory.py':hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()}
# Preserve every raw trajectory and both execution manifests in one small immutable archive.
archive=ROOT/'data/results/model3_mutation_memory_20261004.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for folder,label in [(original,'point_kernel_and_abm'),(fv,'finite_volume')]:
  for p in sorted(folder.glob('*')):
   if p.suffix in ['.json','.npz']:z.write(p,label+'/'+p.name)
result['archive_sha256']=hashlib.sha256(archive.read_bytes()).hexdigest()
result['original_source_commit']='877f213'
(ROOT/'data/results/model3_mutation_memory_20261004.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
print(json.dumps(result['precision'],indent=2))
for r in result['abm']:
 if r['common_environment_periods']==800:print(r)
