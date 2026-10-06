"""Read-only completeness and provenance audit of the full mutation campaign."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

import numpy as np

from scripts.run_model3_full_mutation import ROOT, tasks


def verify_campaign(out):
    out = Path(out)
    sources = json.loads((out / 'sources.json').read_text())
    with zipfile.ZipFile(out / 'sources.zip') as archive:
        if set(archive.namelist()) != set(sources) or len(archive.namelist()) != len(sources):
            raise ValueError('archived source member mismatch')
        for name, expected in sources.items():
            if hashlib.sha256(archive.read(name)).hexdigest() != expected:
                raise ValueError('archived source mismatch: ' + name)
            if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
                raise ValueError('working source mismatch: ' + name)
    cases = tasks(out, 'core', 64, 8) + tasks(out, 'benchmark') + tasks(out, 'density')
    missing = [task[1] for task in cases if not (out / (task[1] + '.json')).exists()]
    if missing:
        raise ValueError(f'incomplete campaign: {len(missing)} missing receipts')
    fingerprints = {}
    for task in cases:
        key = task[1]
        receipt = json.loads((out / (key + '.json')).read_text())
        path = out / (key + '.npz')
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != receipt['sha256'] or receipt['task'] != list(task[2:]):
            raise ValueError('case provenance mismatch: ' + key)
        with np.load(path) as archive:
            trace = archive['trace']
            if trace.shape != (1001, 10) or not np.isfinite(trace[:, 0]).all() or (trace[:, 0] < 0).any():
                raise ValueError('invalid population trace: ' + key)
            occupied = trace[:, 0] > 0
            if not np.isfinite(trace[occupied, 1:7]).all():
                raise ValueError('nonfinite occupied traits: ' + key)
            if ((trace[occupied, 1:4] < -1e-10) | (trace[occupied, 1:4] > 1 + 1e-10)).any():
                raise ValueError('out-of-range traits: ' + key)
            for t in (0, 200, 400, 1000):
                state = archive['state_' + str(t)]
                mass = state.sum() if task[2] == 'density' else len(state)
                if not np.isclose(mass, trace[t, 0], atol=1e-9, rtol=1e-12):
                    raise ValueError('checkpoint population mismatch: ' + key)
        fingerprints[path.name] = digest
    return dict(status='verified', case_count=len(cases), source_count=len(sources),
                case_sha256=fingerprints,
                scope='all declared cases, source identity, task receipts and basic trajectory/checkpoint integrity; numerical fidelity is a separate gate')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    result = verify_campaign(args.out)
    target = Path(args.out) / 'verified_manifest.json'
    target.write_text(json.dumps(result, indent=2) + '\n')
    print({k: v for k, v in result.items() if k != 'case_sha256'})
