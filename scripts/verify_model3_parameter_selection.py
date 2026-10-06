"""Reconstruct coverage/counts and independently check every positive cross effect."""
from pathlib import Path
from dataclasses import replace
import hashlib
import json
import numpy as np
from scripts.model3_island.types import Config
from scripts.audit_model3_unified_reduction import _visitors
from scripts.audit_model3_joint_syndrome_vector import _log_fitness_batch

ROOT = Path(__file__).resolve().parents[1]


def main():
    read = lambda p: json.loads((ROOT/p).read_text(encoding='utf-8'))
    receipt = read('data/results/model3_parameter_selection_20261005.json')
    source = ROOT/'outputs/model3_parameter_selection_20261005/fields.npz'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == receipt['array_sha256']
    with np.load(source) as d:
        values, states, params, communities = [d[k] for k in ['values','states','parameters','communities']]
    assert values.shape == (500,5,45,4)
    assert np.isfinite(values).all()
    counts = {}
    for i in [-1,0,1]:
        for a in [-1,0,1]:
            signs = np.where(values[...,:2]>1e-7,1,np.where(values[...,:2]<-1e-7,-1,0))
            counts[f'investment_{i}_capacity_{a}'] = int(np.sum((signs[...,0]==i)&(signs[...,1]==a)))
    assert counts == receipt['regime_counts']
    base = Config.from_dict(read('data/design/model3_ch2_bridge_20260927.json')['base_config'])
    pools = read('data/design/model3_unified_reduction_audit_20260927.json')['communities']
    examples = []; errors = []
    for pi, ci, si in np.argwhere(values[...,2]>1e-7):
        timing, depression, invcost, capcost, discount = params[pi]
        cfg = replace(base,assurance_mode='evolving',assurance_timing=str(timing),
                      depression=float(depression),investment_cost=float(invcost),
                      assurance_cost=float(capcost),pollen_discount=float(discount))
        visitors = _visitors(pools[str(communities[ci])]); z = states[si:si+1]
        # Differentiate independently calculated rare-mutant gradients over residents.
        estimates = []
        for outer in [1e-3,5e-4]:
            gradients = []
            for direction in [-1,1]:
                resident = z.copy(); resident[:,2] += direction*outer
                plus = resident.copy(); minus = resident.copy(); h=1e-5
                plus[:,1]+=h; minus[:,1]-=h
                gradients.append(float((_log_fitness_batch(resident,plus,visitors,cfg)-
                                        _log_fitness_batch(resident,minus,visitors,cfg))[0]/(2*h)))
            estimates.append((gradients[1]-gradients[0])/(2*outer))
        assert min(estimates)>0, estimates
        error = abs(estimates[-1]-values[pi,ci,si,2]); errors.append(error)
        assert error<1e-5, error
        examples.append({'parameters':params[pi].tolist(),'community':str(communities[ci]),
                         'state':states[si].tolist(),'stored_cross':float(values[pi,ci,si,2]),
                         'independent_cross':estimates})
    result={'status':'verified_stored_counts_and_all_positive_cross_exceptions',
            'array_sha256':receipt['array_sha256'],'shape':list(values.shape),
            'positive_cross_exceptions':len(examples),'max_independent_cross_error':max(errors),
            'exceptions':examples,'scope':'No independent full trajectory or biological calibration claimed.'}
    (ROOT/'data/results/model3_parameter_selection_verified_20261005.json').write_text(
        json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print({k:v for k,v in result.items() if k!='exceptions'})


if __name__=='__main__':
    main()
