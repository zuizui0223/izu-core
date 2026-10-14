"""Apply the four predeclared comparisons only after full independent admission."""
from pathlib import Path
import hashlib,json
import numpy as np
from scripts.assurance_parent_control_20261014 import analyze
W=Path(__file__).resolve().parents[1]
root=W/'work/assurance_parent_control_independent_20261014'
admission=json.loads((root/'ALL4096_INDEPENDENT_ADMISSION_V2.json').read_bytes())
assert admission['status']=='ALL4096_PUBLIC_CONTROLLED_FUTURES_INDEPENDENTLY_REPLAYED_DOMAIN_VERIFIED'
assert admission['cases']==4096 and admission['updates']==819200
reference_receipt=W/'work/clock-source-portability-20261014/data/results/assurance_parent_control_20261014/reference_full_birth_admission.json'
assert hashlib.sha256(reference_receipt.read_bytes()).hexdigest()=='3f107e2841cff502be422061b1b182e0798b7579e662f75a992d16b4d370d68d'
reference=json.loads(reference_receipt.read_bytes())
reference_outcomes=W/'work/four_question_unresolved_20261013/parent_selection_reference_admission_v1/verified/all_start_outcomes.npz'
assert hashlib.sha256(reference_outcomes.read_bytes()).hexdigest()==reference['outcome_npz_sha256']
with np.load(reference_outcomes,allow_pickle=False) as z:
 original=z['occupied'].copy();original_curves=z['curves'].copy()
x=np.empty((2,512,2,3,2),np.int8);curves=np.empty((2,512,2,3,2,201),np.int8)
x[:,:,:,0]=original[:,:,:,1];x[:,:,:,2]=original[:,:,:,2]
curves[:,:,:,0]=original_curves[:,:,:,1];curves[:,:,:,2]=original_curves[:,:,:,2]
seen=set()
for row in admission['records']:
 raw=(root/row['receipt']).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sha256']
 r=json.loads(raw);assert r['status']=='CONTROLLED256_INDEPENDENT_WEIGHT_AND_BIRTH_REPLAY' and r['cases']==256
 for record in r['records']:
  task=record['task'];key=(task['block'],task['replicate'],task['origin'],task['target'])
  assert key not in seen and task['policy']=='A_mean_equal_A_shadow_parents';seen.add(key)
  ix=(('main','confirmation').index(task['block']),task['replicate'],(1.05,1.5).index(task['target']),1,
      ('A_access_first','I_access_first').index(task['origin']))
  curve=np.asarray(record['occupancy_curve'],np.int8)
  assert curve.shape==(201,) and np.isin(curve,[0,1]).all()
  assert bool(curve[-1])==record['terminal_occupied']
  x[ix]=int(record['terminal_occupied']);curves[ix]=curve
assert len(seen)==4096
result=analyze(x,bootstrap_count=19999)
result.update(status='FOUR_FROZEN_COMPARISONS_AFTER_ALL4096_INDEPENDENT_REPLAY',
 cases=4096,source_commit=admission['source_commit'],
 independent_admission_sha256=hashlib.sha256((root/'ALL4096_INDEPENDENT_ADMISSION_V2.json').read_bytes()).hexdigest(),
 secondary_occupancy=curves.mean(axis=(0,1)).tolist(),
 secondary_restricted_duration=curves[...,:-1].sum(-1).mean(axis=(0,1)).tolist(),
 scope='Artificial genetic preparation-route contrasts under within-class assurance-expression parent-weight intervention; not natural evolutionary-order benefit.')
out=W/'work/assurance_parent_control_readout_20261014'
assert not out.exists();out.mkdir()
np.savez_compressed(out/'all_start_outcomes.npz',occupied=x,curves=curves)
with (out/'readout.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'status':result['status'],'primary':result['primary']},indent=2))

