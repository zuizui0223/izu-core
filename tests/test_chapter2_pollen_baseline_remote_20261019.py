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
