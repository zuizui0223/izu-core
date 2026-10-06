"""Independent artifact checks for one strict n65 reproduction step."""
from pathlib import Path
from itertools import combinations_with_replacement
import hashlib,json,zipfile,numpy as np
from scripts.model3_joint_distance import joint_distance

def verify(candidate):
    c=Path(candidate);d=c/'sum_checkpoint_finish'
    v=json.loads((d/'summary.json').read_text())
    if v['status']!='passed_marginals':raise ValueError('strict step has not passed')
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    sources=json.loads((d/'sources.json').read_text())
    with zipfile.ZipFile(d/'sources.zip') as z:
        for p,h in sources.items():
            if sha(c/p)!=h or hashlib.sha256(z.read(p)).hexdigest()!=h:raise ValueError('source mismatch: '+p)
    if sha(d/'state.npz')!=v['npz_sha256']:raise ValueError('state hash mismatch')
    with np.load(d/'state.npz') as z:
        state=(z['core'],tuple(z[f'factor{k}'] for k in range(3)));expected=z['expected'];stored=z['actual']
    core,fs=state;sums=[f.sum(axis=0) for f in fs];actual=[]
    for k in range(3):
        axis='abc'[k];other=[j for j in range(3) if j!=k]
        vec=np.einsum('abc,'+','.join('abc'[j] for j in other)+'->'+axis,core,*[sums[j] for j in other],optimize=True)
        actual.append(fs[k]@vec)
    np.testing.assert_allclose(actual,stored,rtol=1e-12,atol=1e-12)
    means=np.array([(a+b)/2 for a,b in combinations_with_replacement(np.linspace(0,1,65),2)])
    l1=max(float(np.abs(a-b).sum()/b.sum()) for a,b in zip(actual,expected))
    trait=max(float(abs(a@means/a.sum()-b@means/b.sum())) for a,b in zip(actual,expected))
    old=c/'stream_second65';ov=json.loads((old/'summary.json').read_text())
    if sha(old/'state.npz')!=ov['npz_sha256']:raise ValueError('baseline hash mismatch')
    with np.load(old/'state.npz') as z:baseline=(z['core'],tuple(z[f'factor{k}'] for k in range(3)))
    gap=joint_distance(baseline,state,budget=16_000_000);joint=gap['l1_upper']/float(actual[0].sum())
    if not np.isfinite([l1,trait,joint]).all() or l1>1e-5 or trait>1e-6 or joint>1e-5:raise ValueError('independent precision failure')
    return dict(scope='n65 second step only; not grid or long-horizon convergence',marginal_l1=l1,trait_gap=trait,normalized_joint_l1_upper=joint,source_hashes_verified=len(sources),state_sha256=v['npz_sha256'],baseline_sha256=ov['npz_sha256'])

if __name__=='__main__':
    r=Path(__file__).resolve().parents[1];c=r/'outputs/model3_precision_feasibility/fastpath_candidate'
    result=verify(c)
    target=r/'data/results/model3_checkpoint_strict_verified_20261005.json'
    if target.exists():raise ValueError('preserve existing verification')
    target.write_text(json.dumps(result,indent=2));print(result)
