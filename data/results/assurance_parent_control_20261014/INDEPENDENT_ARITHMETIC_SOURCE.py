"""Reconstruct all-start endpoints and independently recompute the fixed four tests."""
from pathlib import Path
import hashlib,json,math
import numpy as np
W=Path(__file__).resolve().parents[1];root=W/'work/assurance_parent_control_independent_20261014'
admission=json.loads((root/'ALL4096_INDEPENDENT_ADMISSION_V2.json').read_bytes())
assert admission['status']=='ALL4096_PUBLIC_CONTROLLED_FUTURES_INDEPENDENTLY_REPLAYED_DOMAIN_VERIFIED' and admission['cases']==4096
out=W/'work/assurance_parent_control_readout_20261014'
primary=json.loads((out/'readout.json').read_bytes())
assert primary['bootstrap_count']==19999 and primary['primary_family']==4 and primary['bootstrap_seed_base']==2026101407
assert primary['independent_admission_sha256']==hashlib.sha256((root/'ALL4096_INDEPENDENT_ADMISSION_V2.json').read_bytes()).hexdigest()
oldpath=W/'work/four_question_unresolved_20261013/parent_selection_reference_admission_v1/verified/all_start_outcomes.npz'
assert hashlib.sha256(oldpath.read_bytes()).hexdigest()=='fbf0f1d43aaf3483320feb8edbfc86912c1a951688c4edc0518ba2acb20a8b85'
with np.load(oldpath,allow_pickle=False) as z:old=z['occupied'].copy()
x=np.empty((2,512,2,3,2),np.int8);x[:,:,:,0]=old[:,:,:,1];x[:,:,:,2]=old[:,:,:,2]
seen=set()
for row in admission['records']:
 raw=(root/row['receipt']).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sha256']
 for record in json.loads(raw)['records']:
  t=record['task'];key=(t['block'],t['replicate'],t['origin'],t['target'])
  assert key not in seen;seen.add(key)
  ix=(('main','confirmation').index(t['block']),t['replicate'],(1.05,1.5).index(t['target']),1,
      ('A_access_first','I_access_first').index(t['origin']))
  assert len(record['occupancy_curve'])==201 and bool(record['occupancy_curve'][-1])==record['terminal_occupied']
  x[ix]=int(record['terminal_occupied'])
assert len(seen)==4096
with np.load(out/'all_start_outcomes.npz',allow_pickle=False) as z:np.testing.assert_array_equal(x,z['occupied'])
np.testing.assert_array_equal(x.sum(axis=(0,1)),primary['occupied_counts'])
d=x[...,0].astype(float)-x[...,1].astype(float)
np.testing.assert_array_equal(d.mean(axis=(0,1)),primary['policy_route_differences'])
radius=4*math.sqrt(math.log(160)/(2*1024));results=[]
for target_index,target in enumerate((1.05,1.5)):
 for contrast_index in range(2):
  i=target_index*2+contrast_index
  pair=d[:,:,target_index,contrast_index]-d[:,:,target_index,contrast_index+1]
  estimate=float(np.mean(pair));rng=np.random.default_rng(2026101407+i)
  simulated=np.zeros(19999)
  for block in range(2):
   indices=rng.integers(0,512,(19999,512))
   simulated+=np.mean(pair[block][indices],axis=1)*.5
  interval=np.quantile(simulated,[.00625,.99375])
  record=primary['primary'][i]
  assert record['target']==target and record['estimate']==estimate
  np.testing.assert_allclose(record['simultaneous_bootstrap_interval'],interval,rtol=0,atol=1e-15)
  np.testing.assert_allclose(record['distribution_free_interval'],[max(-2,estimate-radius),min(2,estimate+radius)],rtol=0,atol=1e-15)
  np.testing.assert_array_equal(record['block_estimates'],pair.mean(axis=1))
  decision='positive' if interval[0]>0 else 'negative' if interval[1]<0 else 'unresolved'
  assert record['decision']==decision
  results.append(dict(target=target,index=i,estimate=estimate,decision=decision))
receipt=dict(status='ALL4096_ENDPOINTS_AND_FOUR_FIXED_COMPARISONS_INDEPENDENTLY_MATCH',cases=4096,
 bootstrap_count=19999,primary_family=4,analysis_helper_imported=False,
 independent_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 primary_readout_sha256=hashlib.sha256((out/'readout.json').read_bytes()).hexdigest(),results=results)
with (out/'INDEPENDENT_ARITHMETIC.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(receipt,indent=2))

