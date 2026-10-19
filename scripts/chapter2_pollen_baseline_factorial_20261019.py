"""Frozen exploratory baseline pollen limitation x activity decline pilot."""
from __future__ import annotations
import argparse, copy, hashlib, json, os
from pathlib import Path
import numpy as np
from scripts.model3_island.types import ArrivalConfig, Config, PlantState, VisitorState
from scripts.model3_island.population import advance
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.randomness import stream
from scripts.model3_island.history import reflect_unit

FROZEN=Path('docs/protocols/CHAPTER2_BASELINE_POLLEN_LIMIT_2X2_FROZEN_20261019.json')
HASH='87af92484af9988181b4f3bed6760d39325de70cca8c0b4e1cec19c47b8c9849'
NATIVE={
 'scripts/model3_island/types.py':'0bc427b3261e7baf1651648ee879b368f9bf935b',
 'scripts/model3_island/population.py':'20e90f249f63e9f37e8801d19d9b75cade2fe193',
 'scripts/model3_island/randomness.py':'46f1ee55899e729cdd09d9dbb9332694ef1e2071',
 'scripts/model3_island/reproduction.py':'95314698a3296b6f13b8c053c36f2df0b7b744ca',
 'scripts/model3_island/history.py':'0c58aee6f73ae133d96d8da4dd6678886ff3061c'}
STREAMS=('survival','parents','segregation','mutation','recruitment','seed_settlement')

def admit():
 if hashlib.sha256(FROZEN.read_bytes()).hexdigest()!=HASH:
  raise ValueError('frozen protocol changed')
 for f,sha in NATIVE.items():
  b=Path(f).read_bytes()
  if hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=sha:
   raise ValueError('native model operator differs: '+f)
 return json.loads(FROZEN.read_text())

def config(d,lev,activity):
 m=d['model']
 zero=ArrivalConfig(0.,1.,1.,'exponential',.5,0.)
 return Config(1,'reproduce-survive-arrive-recruit-v1','reproductive_year',
  m['capacity'],d['factorial']['total_updates_per_trajectory'],m['adult_survival'],
  m['ovule_budget'],m['pollen_budget'],m['investment_cost'],m['pollen_scale'],
  m['inbreeding_depression'],m['mutation_rate'],.025,m['assurance_mode'],.5,
  m['assurance_timing'],m['pollen_discount'],m['assurance_cost'],activity,'fixed',
  4.,1.,1.,zero,zero,'founding',6,.2,d['factorial']['effectiveness'][lev],
  (.5,.5,.5),.15)

def visitors(d,lev):
 n=d['factorial']['visitors']['count']
 return VisitorState(np.arange(100,100+n,dtype=np.int64),
  np.full(n,d['factorial']['visitors']['matching_optimum']),
  np.full(n,d['factorial']['visitors']['breadth']),
  np.full(n,d['factorial']['effectiveness'][lev]))

def founders(d,seed,A0):
 n=d['cohort']['founder_population_count']
 t=np.array([d['factorial']['initial_M_mean'],d['factorial']['initial_I_mean'],A0])
 g=stream(seed,'founders',0)
 a=reflect_unit(t[None,:,None]+g.normal(0,d['cohort']['founder_allele_sd'],(n,3,2)))
 grid=np.array(d['cohort']['founder_projection_grid'])
 a=grid[np.argmin(np.abs(a[...,None]-grid),axis=-1)]
 return PlantState(a,np.arange(n*6,dtype=np.int64).reshape(n,3,2),
  np.zeros((n,3,2),dtype=bool),np.arange(n,dtype=np.int64),
  np.zeros(n,dtype=np.int64))

def snap(s):
 n=len(s.ids)
 if not n:return dict(n=0,M=None,I=None,A=None,max_I=None,min_A=None)
 m=s.alleles.mean(axis=(0,2))
 return dict(n=n,M=float(m[0]),I=float(m[1]),A=float(m[2]),
  max_I=float(s.alleles[:,1,:].max()),min_A=float(s.alleles[:,2,:].min()))

def fingerprint(s):
 h=hashlib.sha256()
 for k in ('alleles','allele_origin','mutation_flags','ids','birth_years'):
  a=np.ascontiguousarray(getattr(s,k))
  h.update(k.encode());h.update(str(a.shape).encode());h.update(str(a.dtype).encode())
  h.update(a.tobytes())
 return h.hexdigest()

def clone(v):
 z={}
 for k,rng in v.items():
  g=np.random.default_rng()
  g.bit_generator.state=copy.deepcopy(rng.bit_generator.state)
  z[k]=g
 return z

def streams(seed,rep):
 return {name:stream(seed,name,rep) for name in STREAMS}

def empty():
 return PlantState(np.empty((0,3,2)),np.empty((0,3,2),dtype=np.int64),
  np.empty((0,3,2),dtype=bool),np.empty(0,dtype=np.int64),
  np.empty(0,dtype=np.int64))

def step(s,v,c,r,year):
 ledger=reproduce(s,v,c)
 ov=float(ledger.ovules.sum())
 q=float(ledger.outcross.sum()/ov) if ov else None
 next_state,_=advance(s,ledger,empty(),c,r,year=year,mutation_traits=(False,False,False))
 return next_state,q

def calibration(d):
 z=np.full((48,3,2),.5)
 s=PlantState(z,np.arange(z.size,dtype=np.int64).reshape(z.shape),
  np.zeros_like(z,dtype=bool),np.arange(48,dtype=np.int64),np.zeros(48,dtype=np.int64))
 out={}
 for lev in d['factorial']['effectiveness']:
  out[lev]={}
  for arm,activity in [('control',.4),('decline',.04)]:
   l=reproduce(s,visitors(d,lev),config(d,lev,activity))
   out[lev][arm]=float(l.outcross.sum()/l.ovules.sum())
   p=d['native_preexecution_homogeneous_q_diagnostic']
   k=lev.replace('_limitation','_limit')+('_control_initial_outcross_fraction' if arm=='control' else '_after_decline_initial_outcross_fraction')
   if abs(out[lev][arm]-p[k])>1e-4:raise ValueError('native calibration mismatch')
 return out

def run_pair(d,lev,A0,seed,rep):
 f=d['factorial'];prefix=f['freeze_prefix_updates'];future=f['future_updates']
 v=visitors(d,lev);c=config(d,lev,.4)
 s=founders(d,seed,A0);initial=snap(s);h0=fingerprint(s)
 r=streams(seed,rep);qs=[]
 for year in range(prefix):
  s,q=step(s,v,c,r,year);qs.append(q)
 pre=snap(s);hs=fingerprint(s)
 saved=clone(r)
 out=[]
 for arm,activity in [('control',.4),('decline',.04)]:
  st=s; r2=clone(saved); cfg=config(d,lev,activity);future_q=[]
  extinct_at=prefix if not len(st.ids) else None
  for year in range(prefix,prefix+future):
   st,q=step(st,v,cfg,r2,year);future_q.append(q)
   if extinct_at is None and not len(st.ids):extinct_at=year+1
  out.append(dict(schema='chapter2_2x2_trajectory_v1',source_contract_sha256=HASH,
   founder_seed=seed,demography_repeat=rep,start_A=A0,baseline=lev,arm=arm,
   initial_state_hash=h0,prefix_state_hash=hs,t0=initial,t_prefix=pre,
   t_end=snap(st),n_terminal=len(st.ids),alive_at_end=bool(len(st.ids)),
   first_extinction_census=extinct_at,q_first=qs[0],q_pre_last=qs[-1],
   q_future_first=future_q[0],q_future_last=future_q[-1],
   prefix_updates=prefix,updates=prefix+future,terminal_state_hash=fingerprint(st)))
 return out

def sharded(d,lev):
 rows=[]
 for A0 in d['factorial']['initial_A_means']:
  for seed in range(d['cohort']['independent_founder_seed_start'],
                    d['cohort']['independent_founder_seed_start']+d['cohort']['independent_founder_seed_count']):
   for rep in d['cohort']['nested_demography_stream_ids']:
    rows.extend(run_pair(d,lev,A0,seed,rep))
 assert len(rows)==192
 return dict(level=lev,source_contract_sha256=HASH,rows=rows)

def key(r):return (r['baseline'],r['start_A'],r['founder_seed'],r['demography_repeat'],r['arm'])

def aggregate(d,packs):
 if len(packs)!=2 or {p['level'] for p in packs}!=set(d['factorial']['effectiveness']):
  raise ValueError('complete two-level batches required')
 rows=[r for p in packs for r in p['rows']]
 expect={(lev,A,seed,rep,arm) for lev in d['factorial']['effectiveness']
  for A in d['factorial']['initial_A_means']
  for seed in range(810101,810113)
  for rep in d['cohort']['nested_demography_stream_ids']
  for arm in ('control','decline')}
 keys=[key(x) for x in rows]
 if len(keys)!=384 or len(set(keys))!=384 or set(keys)!=expect:
  raise ValueError('complete predeclared factorial required')
 ix={key(r):r for r in rows}
 for lev,A,seed,rep,arm in expect:
  x=ix[lev,A,seed,rep,arm];y=ix[lev,A,seed,rep,'decline' if arm=='control' else 'control']
  if (x['prefix_state_hash']!=y['prefix_state_hash'] or
      x['initial_state_hash']!=y['initial_state_hash'] or
      x['t_prefix']!=y['t_prefix'] or x['source_contract_sha256']!=HASH or
      x['updates']!=80):raise ValueError('paired prefix/source mismatch')
 result=[]
 for A in d['factorial']['initial_A_means']:
  for lev in d['factorial']['effectiveness']:
   q=[ix[lev,A,f,r,'control'] for f in range(810101,810113) for r in (1,2,3,4)]
   w=[ix[lev,A,f,r,'decline'] for f in range(810101,810113) for r in (1,2,3,4)]
   keep=[(a,b) for a,b in zip(q,w) if a['t_prefix']['n'] and a['t_end']['n'] and b['t_end']['n']]
   val=lambda t:float(np.mean([b['t_end'][t]-a['t_end'][t] for a,b in keep])) if keep else None
   pr=lambda t:float(np.mean([a['t_prefix'][t]-a['t0'][t] for a in q if a['t_prefix']['n']]))
   result.append(dict(start_A=A,baseline=lev,allocated_pairs=48,both_survived=len(keep),
    terminal_survival_count_control=sum(a['alive_at_end'] for a in q),
    terminal_survival_count_decline=sum(b['alive_at_end'] for b in w),
    pre_decline_A_change_mean=pr('A'),pre_decline_I_change_mean=pr('I'),
    terminal_decline_minus_control_A=val('A'),terminal_decline_minus_control_I=val('I')))
 return dict(status='EXPLORATORY_BOUNDED_FACTORIAL_ALL_ALLOCATIONS_ADMITTED',
  source_contract_sha256=HASH,
  counts=dict(rows=384,paired_contrasts=192,independent_founders=12,demographic_repeats=4),
  summary=result,confirmation_claim=False)

def write(path,data):
 p=Path(path)
 if p.exists():raise ValueError('refuse existing result: '+str(p))
 p.write_text(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+'\n')

def main():
 p=argparse.ArgumentParser()
 p.add_argument('mode',choices=('calibrate','run','aggregate'))
 p.add_argument('--level',choices=('strong_baseline_limitation','weak_baseline_limitation'))
 p.add_argument('--out',required=True)
 p.add_argument('--input',nargs='*')
 a=p.parse_args();d=admit()
 if a.mode=='calibrate':write(a.out,dict(status='NATIVE_PREEXECUTION_MANIPULATION_PASS',values=calibration(d)))
 if a.mode=='run':
  if not a.level:raise ValueError('level required')
  calibration(d);write(a.out,sharded(d,a.level))
 if a.mode=='aggregate':
  if not a.input or len(a.input)!=2:raise ValueError('two shard files required')
  write(a.out,aggregate(d,[json.loads(Path(i).read_text()) for i in a.input]))

if __name__=='__main__':main()
