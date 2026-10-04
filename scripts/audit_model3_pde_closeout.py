"""Post-hoc numerical and closure audit; no change to frozen biology."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scripts.audit_model3_reduced_pde_selection import parental_fitness
from scripts.audit_model3_reduced_pde_trajectory import _initial_phenotype_support
from scripts.audit_model3_unified_reduction import _config, _empty_state, _founders, _visitors
from scripts.model3_island.density import density_step, make_grid, project_state

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / 'data/design/model3_unified_reduction_audit_20260927.json'


def stats(values, mass):
    p = mass / mass.sum()
    mean = float(values @ p)
    return mean, float((values - mean)**2 @ p)


def closure_counterexample():
    design = json.loads(DESIGN.read_text(encoding='utf-8'))
    cfg = _config(design)
    grid = make_grid(([.5], [.4, .5, .6], [.5]))
    values = grid.genotypes.mean(axis=2)[:, 1]
    rows = []
    for name, pair in [('homozygous', [.5, .5]), ('heterozygous', [.4, .6])]:
        _, counts = project_state(_founders(.5, [pair]*3), grid)
        next_counts, _ = density_step(counts, grid, _visitors([.35,.45,.55,.65]),
                                     _empty_state(1), cfg, immigration_mode='source')
        initial = stats(values, counts)
        after = stats(values, next_counts)
        rows.append(dict(genotype=name, initial_mean=initial[0], initial_variance=initial[1],
                         next_mean=after[0], next_variance=after[1]))
    return rows


def controlled_audit(accesses=None, communities=None, horizons=(60, 200, 800)):
    design = json.loads(DESIGN.read_text(encoding='utf-8'))
    cfg = _config(design)
    accesses = design['starting_access_states'] if accesses is None else accesses
    communities = list(design['communities']) if communities is None else communities
    horizons = sorted(set(horizons))
    rows, weak_rows = [], []
    for access in accesses:
        grid = make_grid(([access], [.4,.5,.6], [.5]))
        _, initial = project_state(_founders(access, design['initial_investment_genotypes']), grid)
        exact_values = grid.genotypes.mean(axis=2)[:, 1]
        values, p0 = _initial_phenotype_support(grid, initial)
        for community in communities:
            optima = np.asarray(design['communities'][community])
            visitors = _visitors(optima)
            def rhs(_t, p):
                # No clipping: numerical positivity/mass are measured, not hidden.
                mass = p / p.sum()
                w = parental_fitness(values, mass, access=access, visitor_optima=optima)
                return mass * (w / (mass @ w) - 1)
            solves = []
            for rtol, atol in [(1e-8,1e-10),(1e-10,1e-12)]:
                sol = solve_ivp(rhs, (0,max(horizons)), p0, t_eval=horizons,
                                rtol=rtol, atol=atol, max_step=1.)
                if not sol.success or not np.isfinite(sol.y).all():
                    raise ArithmeticError(sol.message)
                solves.append(sol.y)
            exact, mapped = initial.copy(), p0.copy()
            initial_mean = stats(values, p0)[0]
            for period in range(1, max(horizons)+1):
                exact, _ = density_step(exact, grid, visitors, _empty_state(period),
                                        cfg, immigration_mode='source')
                w = parental_fitness(values, mapped, access=access, visitor_optima=optima)
                mapped *= w / (mapped @ w)
                if period in horizons:
                    j = horizons.index(period)
                    ode = solves[1][:,j]
                    em, ev = stats(exact_values, exact)
                    mm, mv = stats(values, mapped)
                    om, ov = stats(values, ode)
                    rows.append(dict(access=access, community=community, periods=period,
                        initial_mean=initial_mean, exact_mean=em, exact_variance=ev,
                        map_mean=mm, map_variance=mv, ode_mean=om, ode_variance=ov,
                        ode_vs_exact_mean_error=om-em, map_vs_exact_mean_error=mm-em,
                        ode_vs_map_mean_error=om-mm,
                        ode_tolerance_mean_gap=abs(stats(values,solves[0][:,j])[0]-om),
                        ode_mass_error=float(ode.sum()-1), ode_min_mass=float(ode.min()),
                        sign_match=bool(abs(om-initial_mean)<1e-10 and abs(em-initial_mean)<1e-10
                                        or np.sign(om-initial_mean)==np.sign(em-initial_mean))))
            # Weak-update continuous-time limit of the phenotype map only.
            time = 60
            ref = solve_ivp(rhs,(0,time),p0,rtol=1e-10,atol=1e-12,max_step=1.)
            if not ref.success:
                raise ArithmeticError(ref.message)
            for h in (1., .5, .25, .125):
                p = p0.copy()
                for k in range(round(time/h)):
                    p += h*rhs(k*h,p)
                weak_rows.append(dict(access=access,community=community,h=h,time=time,
                    mean_error=abs(stats(values,p)[0]-stats(values,ref.y[:,-1])[0]),
                    mass_l1_error=float(np.abs(p-ref.y[:,-1]).sum())))
    summaries = []
    for t in horizons:
        selected = [r for r in rows if r['periods']==t]
        summaries.append(dict(periods=t,n=len(selected),
            sign_matches=sum(r['sign_match'] for r in selected),
            ode_mean_absolute_error=float(np.mean([abs(r['ode_vs_exact_mean_error']) for r in selected])),
            ode_max_absolute_error=max(abs(r['ode_vs_exact_mean_error']) for r in selected),
            map_mean_absolute_error=float(np.mean([abs(r['map_vs_exact_mean_error']) for r in selected]))))
    return dict(rows=rows, summaries=summaries, weak_time_rows=weak_rows)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',required=True)
    args=parser.parse_args()
    result=controlled_audit()
    result['closure_counterexample']=closure_counterexample()
    result['status']='completed_posthoc_approximation_audit'
    result['claim_boundary']=[
        'D=0: normalized phenotype replicator ODE, not a diffusion-driven PDE',
        'finite atomic initial support; no proof of continuous-founder grid convergence',
        'fixed access, fixed assurance, fixed visitors; no empirical-year calibration',
        '800 periods do not establish equilibrium or island branching',
        'weak-time convergence belongs to the reduced map, not the full sexual model']
    paths=[Path(__file__),DESIGN,ROOT/'scripts/audit_model3_reduced_pde_selection.py',
           ROOT/'scripts/model3_island/density.py',ROOT/'docs/superpowers/plans/2026-10-04-model3-pde-closeout.md']
    result['source_sha256']={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes().replace(b'\r\n', b'\n')).hexdigest() for p in paths}
    Path(args.out).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps(result['summaries'],indent=2))

if __name__=='__main__':
    main()
