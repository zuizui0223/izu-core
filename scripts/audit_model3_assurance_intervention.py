"""Outcome-blind integrity checks while intervention campaign is running."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import zipfile
import numpy as np
from scripts.run_model3_assurance_intervention import tasks, founders


def audit(root):
    out=root/'outputs/model3_assurance_intervention_20261005'
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    manifest=json.loads((out/'sources.json').read_text(encoding='utf-8'))
    with zipfile.ZipFile(out/'sources.zip') as archive:
        for name,sha in manifest.items():
            assert digest(root/name)==sha==hashlib.sha256(archive.read(name)).hexdigest()
    expected={f'{s}_u{u}_h{h}_r{r}_{a}_{m}':(s,u,h,r,a,m) for s,u,h,r,a,m in tasks()}
    receipts=[p for p in out.glob('*.json') if p.stem in expected]
    checked={};negative_pairs=0
    initial=founders().alleles
    for receipt in receipts:
        saved=json.loads(receipt.read_text(encoding='utf-8'))
        task=expected[receipt.stem]
        assert saved['task']==list(task)
        path=receipt.with_suffix('.npz')
        assert digest(path)==saved['sha256']
        with np.load(path) as data:
            trace=data['trace']
            assert trace.shape==(1001,10)
            assert np.array_equal(data['state_0'],initial)
            occupied=trace[:,0]>0
            assert np.isfinite(trace[occupied]).all()
            assert np.isnan(trace[~occupied,1:]).all()
            if task[-1]=='fixed':
                assert np.all(trace[occupied,3]==.5)
                for key in ['state_0','state_200','state_400','state_1000']:
                    assert np.all(data[key][:,2,:]==.5)
        checked[receipt.stem]=task
    for key,task in checked.items():
        if task[1]==0 and task[-1]=='fixed':
            other=key[:-5]+'evolving'
            if other in checked:
                with np.load(out/(key+'.npz')) as a,np.load(out/(other+'.npz')) as b:
                    assert set(a.files)==set(b.files)
                    for name in a.files:assert np.array_equal(a[name],b[name],equal_nan=True)
                negative_pairs+=1
    return dict(status='integrity_passed',checked_cases=len(checked),declared_cases=len(expected),
        zero_mutation_matched_pairs_identical=negative_pairs,
        source_manifest_sha256=digest(out/'sources.json'),
        complete_marker_present=(out/'complete.json').exists(),
        claim_ceiling='Integrity only; partial campaigns do not authorize biological comparisons.')


def main():
    root=Path(__file__).resolve().parents[1]
    result=audit(root)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    path=root/f'data/results/model3_assurance_integrity_{stamp}.json'
    path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':main()
