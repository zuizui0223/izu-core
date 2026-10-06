"""Central-allele one-birth moment diagnostic, not trajectory convergence."""
import json
from pathlib import Path
import numpy as np
from scripts.model3_island.density import birth_mutation_matrix


def audit():
    rows=[]
    for n in [5,9,13,17,33,65]:
        x=np.linspace(0,1,n)
        for scheme in ['jump','heat_fv']:
            kernel=birth_mutation_matrix(x,.01,.05,scheme)
            variance=float(kernel[n//2]@((x-.5)**2))
            reference=.01*.05**2
            rows.append(dict(nodes=n,scheme=scheme,central_variance=variance,
                local_unbounded_reference=reference,ratio=variance/reference,
                max_row_mass_error=float(np.max(np.abs(kernel.sum(axis=1)-1)))))
    return dict(rows=rows,scope='One birth at central allele .5. Boundary tails are negligible for this reference. Matching variance does not establish distribution or trajectory accuracy.')


if __name__=='__main__':
    target=Path('data/results/model3_mutation_grid_moments_20261004.json')
    target.write_text(json.dumps(audit(),indent=2)+'\n')
    print(target)
