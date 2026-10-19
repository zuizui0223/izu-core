"""Frozen baseline-limitation pilot checks; no pretense of island confirmation."""
from copy import deepcopy
import json
from pathlib import Path
import numpy as np
import pytest
from scripts.chapter2_pollen_baseline_factorial_20261019 import (
 admit,founders,visitors,config,calibration,run_pair,fingerprint,clone,streams)

def test_pinned_original_operator_and_frozen_settings():
 d=admit()
 assert d['budget']['complete_trajectories']==384
 assert d['budget']['reserved_confirmation_seeds_consumed']==0
 assert d['model']['mutation_rate']==d['model']['seed_immigration']==0
 assert d['factorial']['freeze_prefix_updates']==30
 assert d['factorial']['future_updates']==50

def test_manipulation_of_delivery_not_visitor_number():
 d=admit()
 o=calibration(d)
 assert o['strong_baseline_limitation']['control']==pytest.approx(.14504,abs=1e-4)
 assert o['strong_baseline_limitation']['decline']==pytest.approx(.01726,abs=1e-4)
 assert o['weak_baseline_limitation']['control']==pytest.approx(.99461,abs=1e-4)
 assert o['weak_baseline_limitation']['decline']==pytest.approx(.44038,abs=1e-4)
 assert len(visitors(d,'strong_baseline_limitation').ids)==len(visitors(d,'weak_baseline_limitation').ids)==6

def test_synthetic_founding_genotypes_share_M_and_I_across_A_start():
 d=admit()
 a=founders(d,810101,.3)
 b=founders(d,810101,.5)
 assert (a.alleles[:,:2,:]==b.alleles[:,:2,:]).all()
 assert not (a.alleles[:,2,:]==b.alleles[:,2,:]).all()
 assert len(a.ids)==48
 assert set(np.unique(a.alleles)).issubset({0.,.25,.5,.75,1.})

def test_matched_fork_has_identical_initial_genomes_and_prefix_and_final_is_finite():
 d=deepcopy(admit())
 d['factorial']['freeze_prefix_updates']=3
 d['factorial']['future_updates']=4
 d['factorial']['total_updates_per_trajectory']=7
 for lev in d['factorial']['effectiveness']:
  a,b=run_pair(d,lev,.3,810101,1)
  assert (a['arm'],b['arm'])==('control','decline')
  assert a['initial_state_hash']==b['initial_state_hash']
  assert a['prefix_state_hash']==b['prefix_state_hash']
  assert a['t_prefix']==b['t_prefix']
  assert a['updates']==b['updates']==7
  assert a['alive_at_end']==(a['n_terminal']>0)
  assert b['alive_at_end']==(b['n_terminal']>0)
  from scripts.audit_chapter2_pollen_baseline_factorial_20261019 import check_observations
  check_observations(a);check_observations(b)
  broken=deepcopy(a);broken['reproduction_records'].pop()
  with pytest.raises(ValueError,match='missing reproduction'):check_observations(broken)


def test_observation_records_preserve_native_transition_and_genetic_support():
 from scripts.chapter2_pollen_baseline_factorial_20261019 import step, snap, empty
 from scripts.model3_island.population import advance
 from scripts.model3_island.reproduction import reproduce
 d=admit(); lev='weak_baseline_limitation'
 s=founders(d,810101,.3); v=visitors(d,lev); c=config(d,lev,.4)
 r=streams(810101,1); r2=clone(r); records=[]
 result,q=step(s,v,c,r,0,records=records)
 direct,info=advance(s,reproduce(s,v,c),empty(),c,r2,year=0,mutation_traits=(False,False,False))
 assert fingerprint(result)==fingerprint(direct)
 row=records[0]
 assert row['resident_selfed_recruits']+row['resident_outcross_recruits']==len(result.ids)
 assert row['q']==q
 for j,trait in enumerate(('M','I','A')):
  assert snap(s)['genetic_support'][trait]['allele_values']==np.unique(s.alleles[:,j,:]).tolist()
 assert snap(empty())['genetic_support']['A']['allele_values']==[]


def test_fully_extinct_prefix_aggregate_is_json_serializable():
 from scripts.chapter2_pollen_baseline_factorial_20261019 import aggregate, snap, empty, HASH
 d=admit(); packs=[]
 for lev in d['factorial']['effectiveness']:
  rows=[]
  for a in (.3,.5):
   for seed in range(810101,810113):
    for rep in (1,2,3,4):
     for arm in ('control','decline'):
      rows.append(dict(baseline=lev,start_A=a,founder_seed=seed,demography_repeat=rep,arm=arm,
       prefix_state_hash='extinct',initial_state_hash='initial',t_prefix=snap(empty()),
       t_end=snap(empty()),t0=snap(empty()),source_contract_sha256=HASH,updates=80,alive_at_end=False))
  packs.append(dict(level=lev,rows=rows))
 result=aggregate(d,packs)
 json.dumps(result,allow_nan=False)
 assert all(x['pre_decline_A_change_mean'] is None and x['survived_to_prefix']==0 for x in result['summary'])


def test_extinction_in_prefix_records_actual_first_census(monkeypatch):
 import scripts.chapter2_pollen_baseline_factorial_20261019 as m
 d=deepcopy(admit())
 d['factorial'].update(freeze_prefix_updates=3,future_updates=4,total_updates_per_trajectory=7)
 def extinct_step(s,v,c,r,year,records=None):
  return m.empty(),None
 monkeypatch.setattr(m,'step',extinct_step)
 assert all(x['first_extinction_census']==1 for x in run_pair(d,'weak_baseline_limitation',.3,810101,1))


def synthetic_pollen_observations():
 # Arithmetic-only fixture: distinct q values identify each endpoint's census.
 snapshot=dict(n=1,M=.5,I=.5,A=.5,max_I=.5,min_A=.5,
  genetic_support={t:dict(allele_values=[.5],allele_counts=[2],
   genotype_mean_variance=0.) for t in ('M','I','A')})
 records=[dict(year=y,q=(y+1)/100,occupancy=1,ovules=100.,
  outcross_expected=float(y+1),self_raw_expected=0.,self_viable_expected=0.,
  resident_selfed_recruits=0,resident_outcross_recruits=1) for y in range(80)]
 return dict(t0=deepcopy(snapshot),t_prefix=deepcopy(snapshot),t_end=deepcopy(snapshot),
  updates=80,prefix_updates=30,reproduction_records=records,
  q_first=.01,q_pre_last=.30,q_future_first=.31,q_future_last=.80)


@pytest.mark.parametrize('field,index',[
 ('q_first',0),('q_pre_last',29),('q_future_first',30),('q_future_last',79)])
@pytest.mark.parametrize('corruption',['value','missing','undefined','nan'])
def test_pollen_endpoint_must_match_ledger(field,index,corruption):
 from scripts.audit_chapter2_pollen_baseline_factorial_20261019 import check_observations
 row=synthetic_pollen_observations()
 check_observations(row)
 if corruption=='value':row[field]=.99
 elif corruption=='missing':row[field]=None
 elif corruption=='nan':row[field]=float('nan')
 else:
  row['reproduction_records'][index].update(ovules=0.,outcross_expected=0.,q=None)
 with pytest.raises(ValueError,match='q endpoint ledger mismatch'):
  check_observations(row)


def test_pollen_endpoint_accepts_matching_undefined_and_roundoff():
 from scripts.audit_chapter2_pollen_baseline_factorial_20261019 import check_observations
 row=synthetic_pollen_observations()
 row['q_first']+=5e-13
 row['q_future_last']=None
 row['reproduction_records'][79].update(ovules=0.,outcross_expected=0.,q=None)
 check_observations(row)
