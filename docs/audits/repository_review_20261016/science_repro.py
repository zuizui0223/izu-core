"""Small synthetic review probes. Does not execute a scientific campaign."""
import json
import sys
from pathlib import Path
from unittest.mock import patch
import numpy as np

ROOT = Path(__file__).resolve().parents[2] / 'work/repository_review_20261016'
sys.path.insert(0, str(ROOT))
from scripts.run_chapter2_assurance_generality import config, load_design, DEFAULT_DESIGN
import scripts.summarize_chapter2_assurance_generality as old
from scripts.model3_island.selection import investment_invasion_terms
from scripts.model3_island.types import VisitorState
from scripts.run_chapter2_assurance_generality import founders
from scripts.model3_island.reproduction import reproduce
from dataclasses import replace

d = load_design(DEFAULT_DESIGN)
c = config(d, 'assurance_cost', .01, 'fixed')
v = VisitorState(np.arange(4), np.array([.35,.45,.55,.65]), np.full(4,.18), np.ones(4))
gradients = []
ledgers = []
for a in [.1,.5,.9]:
    gradients.append(float(investment_invasion_terms([.2,.5,a],v,c)['gradient']))
    p = founders(d)
    alleles = p.alleles.copy()
    alleles[:,0,:] = .2
    alleles[:,1,:] = .5
    alleles[:,2,:] = a
    ledgers.append(reproduce(replace(p,alleles=alleles),v,c))
identical = all(np.array_equal(ledgers[0].maternal, x.maternal) and
                np.array_equal(ledgers[0].paternal, x.paternal) for x in ledgers[1:])
assert identical and gradients[0] > 0 and gradients[1] < 0
with patch.object(old, 'load_endpoint', return_value=(False,.5,float('nan'))):
    row = old.setting_readout(d, {}, 'delayed_control', 0)
assert row['admissible'] is False and row['passes_frozen_rule'] is False
try:
    json.dumps(row, allow_nan=False)
except ValueError as exc:
    serialization = str(exc)
else:
    raise AssertionError('Expected observed serialization failure')
print(json.dumps({'fixed_A_gradient_by_ignored_allele': gradients,
 'native_fixed_A_ledgers_identical': identical,
 'all_extinct_summary_serialization_error': serialization}, indent=2))

# A valid population supported only on A=0 has zero selfed births, but viable outcross births.
from scripts.model3_island.tensor_density import make_tensor_grid
from scripts.model3_island.density import density_step
from scripts.model3_island.types import PlantState
from scripts.model3_compressed_step import compressed_step, mass
from importlib import import_module
axes = ([0., .5, 1.],)*3
factors = [np.zeros((6,1)) for _ in range(3)]
factors[0][3,0] = factors[1][3,0] = factors[2][0,0] = 1.
state = (np.full((1,1,1),48.), factors)
evolving = replace(c, assurance_mode='evolving', mutation_rate=0.)
empty = PlantState(np.empty((0,3,2)), np.empty((0,3,2),dtype=int),
 np.empty((0,3,2),dtype=bool), np.empty(0,dtype=int), np.empty(0,dtype=int))
counts = np.einsum('abc,ia,jb,kc->ijk',state[0],*factors).ravel()
expected, _ = density_step(counts,make_tensor_grid(axes),v,empty,evolving,inheritance_backend='tensor')
exact = compressed_step(state,axes,v,evolving)
assert abs(mass(exact)-expected.sum())<1e-9 and expected.sum()>0
failures = {}
for suffix in ['bounded','batched_weight','binary_reader','checked_weight','complete',
 'exact_gamete','fast_streamed','gamete','rounded_gamete','sharp','streamed',
 'streamed_weight','sum','tiled']:
    module = 'scripts.model3_'+suffix+'_integration'
    try:
        import_module(module).bounded_step(state,axes,v,evolving)
    except ArithmeticError as exc:
        failures[module] = str(exc)
assert len(failures)==14
print(json.dumps({'dense_next_mass':float(expected.sum()),'exact_compressed_next_mass':mass(exact),
 'zero_selfed_valid_population_rejections':failures},indent=2))
