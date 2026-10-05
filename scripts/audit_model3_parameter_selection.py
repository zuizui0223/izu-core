"""Bounded exploratory parameter diagnostic; never changes the main experiment."""
from pathlib import Path
from dataclasses import replace
from itertools import product
import hashlib
import json
import numpy as np
from scripts.model3_island.types import Config
from scripts.model3_island.selection import syndrome_thresholds
from scripts.audit_model3_unified_reduction import _visitors
from scripts.audit_model3_joint_syndrome_vector import _log_fitness_batch

ROOT = Path(__file__).resolve().parents[1]


def run():
    read = lambda p: json.loads((ROOT/p).read_text(encoding='utf-8'))
    design_path = ROOT/'data/design/model3_parameter_selection_20261005.json'
    design = json.loads(design_path.read_text(encoding='utf-8'))
    for name, expected in design['source_hashes'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected, name
    base = Config.from_dict(read('data/design/model3_ch2_bridge_20260927.json')['base_config'])
    communities = read('data/design/model3_unified_reduction_audit_20260927.json')['communities']
    starts = read('data/design/model3_joint_syndrome_rare_mutant_20261004.json')['resident_states']
    states = np.array(list(product(starts['access'], starts['investment'], starts['assurance'])))
    names = ['assurance_timing', 'depression', 'investment_cost', 'assurance_cost', 'pollen_discount']
    parameters = list(product(*(design[n] for n in names)))
    values = np.empty((len(parameters), len(communities), len(states), 4))
    finite_errors = []; cross_error = 0.; sign_disagreements = 0
    tol = design['readout']['gradient_deadband']
    sign = lambda x: np.where(x > tol, 1, np.where(x < -tol, -1, 0))
    for pi, pars in enumerate(parameters):
        cfg = replace(base, assurance_mode='evolving', **dict(zip(names, pars)))
        for ci, optima in enumerate(communities.values()):
            visitors = _visitors(optima)
            terms = syndrome_thresholds(states, visitors, cfg)
            for ki, (field, trait) in enumerate([('investment_gradient', 1), ('assurance_gradient', 2)]):
                actual = terms[field]; values[pi, ci, :, ki] = actual
                h = design['readout']['independent_gradient_step']
                plus = states.copy(); minus = states.copy()
                plus[:, trait] += h; minus[:, trait] -= h
                independent = (_log_fitness_batch(states, plus, visitors, cfg) -
                               _log_fitness_batch(states, minus, visitors, cfg))/(2*h)
                finite_errors.append(float(np.max(np.abs(independent-actual))))
                estimates = []
                for h in design['readout']['cross_derivative_steps']:
                    plus = states.copy(); minus = states.copy()
                    other = 3-trait
                    plus[:, other] += h; minus[:, other] -= h
                    estimates.append((syndrome_thresholds(plus, visitors, cfg)[field] -
                                      syndrome_thresholds(minus, visitors, cfg)[field])/(2*h))
                cross_error = max(cross_error, float(np.max(np.abs(estimates[0]-estimates[1]))))
                sign_disagreements += int(np.sum(sign(estimates[0]) != sign(estimates[1])))
                values[pi, ci, :, ki+2] = estimates[-1]
    assert np.isfinite(values).all()
    max_error = max(finite_errors)
    assert max_error <= design['readout']['independent_gradient_max_abs_error'], max_error
    directions = sign(values[..., :2])
    regime_counts = {f'investment_{i}_capacity_{a}': int(np.sum((directions[...,0]==i)&(directions[...,1]==a)))
                     for i, a in product([-1,0,1], repeat=2)}
    cross_counts = {label: {str(s): int(np.sum(sign(values[...,k]) == s)) for s in [-1,0,1]}
                    for k,label in [(2,'capacity_on_investment'),(3,'investment_on_capacity')]}
    # Retain each parameter setting, rather than only successful corners.
    rows = []
    for pi, pars in enumerate(parameters):
        row = dict(zip(names, pars))
        row['joint_direction_count'] = int(np.sum((directions[pi,...,0]<0)&(directions[pi,...,1]>0)))
        row['states_communities'] = len(communities)*len(states)
        rows.append(row)
    out = ROOT/'outputs/model3_parameter_selection_20261005'; out.mkdir(parents=True, exist_ok=True)
    target = out/'fields.npz'
    np.savez_compressed(target, values=values, states=states,
                        parameter_names=np.array(names), parameters=np.array(parameters, dtype=str),
                        communities=np.array(list(communities)))
    receipt = {'classification': design['classification'], 'status':'passed_gradient_checks',
               'parameter_combinations':len(parameters),'state_community_parameter_cases':int(np.prod(values.shape[:-1])),
               'independent_gradients_checked':len(finite_errors)*len(states),
               'independent_max_abs_error':max_error,'cross_step_max_abs_difference':cross_error,
               'cross_step_sign_disagreements':sign_disagreements,'regime_counts':regime_counts,
               'cross_derivative_sign_counts':cross_counts,'rows':rows,
               'design_sha256':hashlib.sha256(design_path.read_bytes()).hexdigest(),
               'array_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
               'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'scope':'Designed grid counts, not probability or natural prevalence. No evolution trajectory or order tested.'}
    path = ROOT/'data/results/model3_parameter_selection_20261005.json'
    path.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in receipt.items() if k != 'rows'},indent=2))


if __name__ == '__main__':
    run()
