"""Read-only design arithmetic. No model import, RNG draw, or biological update."""
import argparse
import hashlib
import io
import json
import math
from pathlib import Path
import statistics
import zipfile

import numpy as np

ARCHIVE_SHA = '90b9d063c564edf97f12d3a3917819486f72d4ecb8281a20ebdaf39ad7de14c6'
NAMESPACE = 'izu-q3-conditional-restoration-v1-20261014'
R = 64


def preflight(path):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != ARCHIVE_SHA:
        raise ValueError('Unregistered archive')
    cases, seconds, seeds = [], [], set()
    state_bytes = parent_bytes = None
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for name in sorted(z.namelist()):
            if not (name.startswith('RESTORATION/') and name.endswith('.npz')):
                continue
            key = Path(name).stem
            with np.load(io.BytesIO(z.read(name)), allow_pickle=False) as a:
                m = json.loads(str(a['metadata']))
                trigger = m['trigger']
                if trigger is not None:
                    current = sum(a[k].dtype.itemsize * math.prod(a[k].shape[1:])
                                  for k in ('ids', 'alleles', 'allele_origin', 'mutation_flags', 'birth_years')) * 48
                    parents = a['parentage'].dtype.itemsize * 3 * 48
                    if state_bytes is not None and (current != state_bytes or parents != parent_bytes):
                        raise ValueError('Inconsistent raw layout')
                    state_bytes, parent_bytes = current, parents
            receipt = json.loads(z.read('ORIGINAL64/' + key + '.json'))
            seconds.append(receipt['seconds'])
            case = dict(key=key, block=m['task']['block'], trigger=trigger,
                        remaining_updates=0 if trigger is None else 200-trigger,
                        original_npz_sha256=hashlib.sha256(z.read('ORIGINAL64/'+key+'.npz')).hexdigest(),
                        restoration_npz_sha256=hashlib.sha256(z.read(name)).hexdigest())
            case['pair_seeds'] = []
            if trigger is not None:
                for r in range(R):
                    seed = int.from_bytes(hashlib.sha256(f'{NAMESPACE}\0{key}\0{r}'.encode('utf-8')).digest()[:16], 'big')
                    if seed in seeds:
                        raise ValueError('Seed collision')
                    seeds.add(seed)
                    case['pair_seeds'].append(str(seed))
            cases.append(case)
        frozen_source = {n:hashlib.sha256(z.read(n)).hexdigest() for n in sorted(z.namelist())
                         if n.startswith('FROZEN_SOURCE/') and not n.endswith('/')}
    assert len(cases) == 64 and sum(c['trigger'] is not None for c in cases) == 61
    remaining = sum(c['remaining_updates'] for c in cases)
    assert remaining == 7740 and len(seeds) == 3904
    precision = {}
    for block in ('all64', 'causal_main', 'causal_confirmation'):
        rows = cases if block == 'all64' else [c for c in cases if c['block'] == block]
        n, t = len(rows), sum(c['trigger'] is not None for c in rows)
        coefficient = (1/16)**2 * 2*t*math.log(120)/(n*n)
        precision[block] = dict(slots=n, triggered=t, simultaneous_half_width=math.sqrt(coefficient/R),
                                minimum_R_for_half_width_0_005=math.ceil(coefficient/.005**2))
    updates = 2*R*remaining
    censuses = 2*R*(remaining+61)
    return dict(status='design_only_no_biology', archive_sha256=ARCHIVE_SHA, namespace=NAMESPACE,
                replicates_per_state=R, new_trajectories=2*len(seeds), maximum_scheduled_updates=updates,
                maximum_saved_censuses=censuses, state_bytes_per_full_census=state_bytes,
                parent_bytes_per_full_update=parent_bytes,
                raw_state_and_parent_bytes_upper=censuses*state_bytes+updates*parent_bytes,
                historical_original_200_update_seconds=dict(min=min(seconds), median=statistics.median(seconds), max=max(seconds)),
                serial_seconds_historical_linear_projection=dict(min=updates*min(seconds)/200,
                    median=updates*statistics.median(seconds)/200, max=updates*max(seconds)/200),
                cost_caveat='Historical host timings; excludes new serialization/verification; not a benchmark or guarantee.',
                precision=precision, cases=cases, frozen_source_sha256=frozen_source)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--archive', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    result = preflight(args.archive)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('cases','frozen_source_sha256')}, indent=2))
