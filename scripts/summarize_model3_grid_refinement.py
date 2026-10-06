"""Compare every completed 13-node continuation with its frozen nine-node case."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scripts.run_model3_grid_refinement import refinement_tasks
from scripts.summarize_model3_full_mutation import read_case, sanitize


def summarize(out, original):
    out,original=Path(out),Path(original)
    declared=refinement_tasks(out)
    missing=[t[1] for t in declared if not (out/(t[1]+'.json')).exists()]
    if missing:raise ValueError(f'incomplete refinement: {len(missing)} cases')
    rows=[]
    for task in declared:
        key=task[1]
        receipt=json.loads((out/(key+'.json')).read_text())
        path=out/(key+'.npz')
        if receipt['task']!=list(task[2:]) or hashlib.sha256(path.read_bytes()).hexdigest()!=receipt['sha256']:
            raise ValueError('invalid refinement receipt: '+key)
        with np.load(path) as archive:refined=archive['trace'].copy()
        coarse=read_case(original,key.replace('_n13_','_n9_'))
        if refined.shape != coarse.shape or not np.allclose(refined[0,:7],coarse[0,:7],atol=1e-12,rtol=0):
            raise ValueError('inconsistent initial distributions: '+key)
        signed=refined[:,1:4]-coarse[:,1:4]
        terminal=float(np.nanmax(np.abs(signed[-1])))
        rows.append(dict(key=key,setting=task[3],history_seed=task[5],arm=task[7],scheme=task[9],
            terminal_signed_difference=signed[-1].tolist(),terminal_max_gap=terminal,
            terminal_pass=bool(np.isfinite(terminal) and terminal<.01),
            trajectory_max_gap=float(np.nanmax(np.abs(signed))),
            refined_terminal_traits=refined[-1,1:4].tolist(),
            refined_terminal_mass=float(refined[-1,0]),
            refined_last100_changes=(refined[-1,1:4]-refined[-101,1:4]).tolist()))
    return dict(n_cases=len(rows),passing=sum(r['terminal_pass'] for r in rows),rows=rows,
      claim_boundary='same-founder 9-to-13 refinement; terminal mean precision diagnostic, not proof of a continuum limit or stable attractors')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--original',required=True)
    a=p.parse_args();result=summarize(a.out,a.original)
    (Path(a.out)/'summary.json').write_text(json.dumps(sanitize(result),indent=2,allow_nan=False)+'\n')
    print({k:v for k,v in result.items() if k!='rows'})
