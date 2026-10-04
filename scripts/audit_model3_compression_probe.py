"""Dense-update/Tucker-roundtrip diagnostic; NOT a scalable compressed solver."""
import hashlib
import json
import time
from pathlib import Path
import numpy as np
from scripts.run_model3_full_mutation import ROOT, config, exposure, atomic_json
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.density import density_step, project_state
from scripts.model3_island.tensor_density import make_tensor_grid


def transform(x, matrix, axis):
    return np.moveaxis(np.moveaxis(x, axis, -1) @ matrix, -1, axis)


def roundtrip(value, epsilon):
    x = np.asarray(value, dtype=float)
    if (x.ndim != 3 or not x.size or not np.isfinite(x).all()
            or np.min(x) < 0 or not 0 < epsilon < 1):
        raise ValueError('finite nonnegative 3D density and tolerance in (0,1) required')
    mass = x.sum()
    if mass == 0:
        return x.copy(), dict(relative_l1=0., negative_mass=0., ranks=[0]*3, stored_values=0)
    factors = []
    budget = (epsilon * mass / 6)**2 / x.size
    for axis in range(3):
        unfolding = np.moveaxis(x, axis, 0).reshape(x.shape[axis], -1)
        u, s, _ = np.linalg.svd(unfolding, full_matrices=False)
        tails = np.r_[np.cumsum((s*s)[::-1])[::-1], 0.]
        rank = max(1, int(np.flatnonzero(tails <= budget)[0]))
        factors.append(u[:, :rank])
    core = x
    for axis, factor in enumerate(factors):
        core = transform(core, factor, axis)
    y = core
    for axis, factor in enumerate(factors):
        y = transform(y, factor.T, axis)
    negative = float(-y[y < 0].sum())
    y = np.maximum(y, 0)
    y *= mass/y.sum()
    error = float(np.abs(y-x).sum()/mass)
    if error > epsilon:
        raise ValueError(f'roundtrip exceeds declared L1 tolerance: {error}')
    return y, dict(relative_l1=error, negative_mass=negative,
                  ranks=[f.shape[1] for f in factors],
                  stored_values=int(core.size + sum(f.size for f in factors)))


def main():
    out = ROOT/'outputs/model3_precision_feasibility/propagation40'
    out.mkdir(parents=True, exist_ok=True)
    files = list((ROOT/'scripts/model3_island').glob('*.py')) + [Path(__file__),
        ROOT/'scripts/run_model3_full_mutation.py',
        ROOT/'data/design/model3_ch2_bridge_20260927.json',
        ROOT/'docs/superpowers/plans/2026-10-04-model3-compression-probe.md']
    sources = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    manifest = out/'sources.json'
    if manifest.exists() and json.loads(manifest.read_text()) != sources:
        raise ValueError('probe sources changed')
    atomic_json(manifest, sources)
    founders = founders_from_spec(dict(count=48,draw_count=48,means=[.5]*3,sd=.15,birth_year=0),74001)
    founders, _ = project_state(founders, make_tensor_grid(([0,.25,.5,.75,1],)*3))
    grid = make_tensor_grid((tuple(np.linspace(0,1,9)),)*3)
    _, initial = project_state(founders, grid)
    traits = grid.genotypes.mean(axis=2)
    results = []
    for setting in ['assurance_cost','prior_selfing']:
      for arm in ['near','far']:
       for scheme in ['jump','heat_fv']:
        key = f'{setting}_{arm}_{scheme}'
        c = config(setting,.01)
        h = exposure(76001,arm)
        baseline = initial.copy(); compressed = initial.copy()
        records = []; start = time.monotonic()
        for t in range(40):
            baseline, _ = density_step(baseline,grid,h.visitors[t],h.seed_candidates[t],c,
                mutation_scheme=scheme,inheritance_backend='tensor')
            raw, _ = density_step(compressed,grid,h.visitors[t],h.seed_candidates[t],c,
                mutation_scheme=scheme,inheritance_backend='tensor')
            joint, info = roundtrip(raw.reshape(45,45,45),1e-8)
            compressed = joint.ravel()
            bmass = float(baseline.sum()); cmass = float(compressed.sum())
            occupied = bmass > 0 and cmass > 0
            records.append(dict(period=t+1, **info,
                path_l1=float(np.abs(baseline-compressed).sum()/max(bmass,1e-300)),
                mass_gap=abs(bmass-cmass),
                trait_gap=float(np.max(np.abs(baseline@traits/bmass-compressed@traits/cmass))) if occupied else None,
                occupancy_mismatch=bool((bmass>0)!=(cmass>0))))
        result = dict(key=key,seconds=time.monotonic()-start,records=records)
        result['passed'] = all(r['path_l1']<=1e-5 and r['mass_gap']<=1e-5
            and not r['occupancy_mismatch'] and (r['trait_gap'] is None or r['trait_gap']<=1e-6) for r in records)
        atomic_json(out/(key+'.json'),result)
        results.append(result)
        print(key, result['passed'], 'max L1',max(r['path_l1'] for r in records),flush=True)
    atomic_json(out/'summary.json',dict(scope='40-period dense propagation diagnostic only',results=results))


if __name__ == '__main__':
    main()
