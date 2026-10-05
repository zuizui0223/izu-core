import importlib
import numpy as np
from scripts import run_model3_full_mutation as old


def equal(a,b):
 return all(np.array_equal(getattr(a,k),getattr(b,k)) for k in ['ids','optima','breadths','effectiveness'])


def test_persistent_exposure_preserves_initial_phase_but_does_not_equalize():
 new=importlib.import_module('scripts.run_model3_persistent_isolation')
 near=new.exposure(76001,'near');far=new.exposure(76001,'far')
 assert all(equal(a,b) for a,b in zip(near.visitors,old.exposure(76001,'near').visitors))
 assert all(equal(a,b) for a,b in zip(far.visitors[:200],old.exposure(76001,'far').visitors[:200]))
 assert any(not equal(a,b) for a,b in zip(far.visitors[200:],near.visitors[200:]))
 assert all(len(p.ids)==0 for p in far.seed_candidates)


def test_frozen_cases_and_biological_rules():
 new=importlib.import_module('scripts.run_model3_persistent_isolation')
 tasks=new.tasks('unused','core',64,8)
 assert len(tasks)==2048 and all(t[7]=='far' for t in tasks)
 assert len({t[1] for t in tasks})==2048
 for setting in ['assurance_cost','prior_selfing']:
  for rate in [0,.01]:
   assert new.config(setting,rate)==old.config(setting,rate)
