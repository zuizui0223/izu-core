"""Independent per-history raw-case reconstruction; refuses partial campaigns."""
from pathlib import Path
import hashlib
import json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/model3_replenishment_evolution_20261005'


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    plan=json.loads((ROOT/'data/design/model3_replenishment_evolution_20261005.json').read_text())
    progress=json.loads((OUT/'progress.json').read_text())
    if progress['status']!='complete' or progress['completed']!=plan['new_cases']:
        raise RuntimeError('Raw verification requires the complete declared campaign')
    curve_path=OUT/'evolution_curves.npz'
    with np.load(curve_path) as archive:
        curves={k:archive[k] for k in archive.files}
    cases=0;coordinates=0; max_error=0.
    for setting in plan['settings']:
        for h_index,seed in enumerate(plan['history_seeds']):
            reference=None
            for distance in plan['distance_coordinates']:
                traces=[]
                for rep in plan['demographic_repeats']:
                    if distance==0:
                        base=ROOT/'outputs/model3_full_mutation_20261004'
                        name=f'core_{setting}_u0.01_h{seed}_r{rep}_near'
                        task=['abm',setting,.01,seed,rep,'near',0,'jump',False]
                    elif distance==3:
                        base=ROOT/'outputs/model3_persistent_isolation_20261005'
                        name=f'persistent_core_{setting}_u0.01_h{seed}_r{rep}_far'
                        task=['abm',setting,.01,seed,rep,'far',0,'jump',False]
                    else:
                        base=OUT;name=f'{setting}_d{distance:.2f}_h{seed}_r{rep}'
                        task=[setting,distance,seed,rep]
                    path=base/(name+'.npz')
                    receipt=json.loads(path.with_suffix('.json').read_text())
                    assert receipt['task']==task and receipt['sha256']==digest(path)
                    with np.load(path) as z:t=z['trace'].copy()
                    assert t.shape==(1001,10)
                    assert np.isfinite(t[:,0]).all() and (t[:,0]>=0).all()
                    occupied=t[:,0]>0
                    assert np.isfinite(t[occupied]).all() and np.isnan(t[~occupied,1:]).all()
                    traces.append(t);cases+=1
                stack=np.array(traces)
                if distance==0:reference=stack.copy()
                assert reference is not None
                alive=stack[:,:,0]>0;paired=alive&(reference[:,:,0]>0)
                key=f'{setting}_d{distance:.2f}'
                np.testing.assert_array_equal(curves[key+'_occupancy'][h_index],alive.sum(axis=0))
                np.testing.assert_array_equal(curves[key+'_paired_occupancy'][h_index],paired.sum(axis=0))
                for suffix,mask in [('from_founders',alive),('minus_high_supply',paired)]:
                    rebuilt=np.full((1001,3),np.nan)
                    # Explicit live-repeat selection at each time, rather than production vectorized reductions.
                    for time in range(1001):
                        indices=np.flatnonzero(mask[:,time])
                        if len(indices):
                            current=stack[indices,time,1:4]
                            base=stack[indices,0,1:4] if suffix=='from_founders' else reference[indices,time,1:4]
                            rebuilt[time]=(current-base).mean(axis=0)
                    saved=curves[key+'_'+suffix][h_index]
                    np.testing.assert_allclose(saved,rebuilt,atol=1e-14,rtol=0,equal_nan=True)
                    valid=np.isfinite(rebuilt)
                    if valid.any():max_error=max(max_error,float(np.abs(saved[valid]-rebuilt[valid]).max()))
                    coordinates+=rebuilt.size
    assert cases==13312 and coordinates==9993984
    result=dict(status='verified_all_raw_case_to_curve_mappings',cases=cases,
                trait_coordinates=coordinates,max_numeric_difference=max_error,
                curves_sha256=digest(curve_path),verifier_sha256=digest(Path(__file__)),
                scope='Independent live-repeat reconstruction, per-case hashes and condition identities. No independent reimplementation of the biological simulator.')
    path=ROOT/'data/results/model3_replenishment_raw_curves_verified_20261005.json'
    path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':main()
