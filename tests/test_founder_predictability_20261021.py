import numpy as np
import pytest
from scripts.analyze_founder_predictability_20261021 import scores

def test_press_matches_explicit_refits():
    y=np.array([[0.,2.,1.,4.],[2.,1.,5.,3.],[4.,0.,3.,2.]])
    f,v=y.shape
    design=np.array([[1]+[int(i==k) for k in range(1,f)]+[int(j==k) for k in range(1,v)] for i in range(f) for j in range(v)])
    flat=y.ravel();sse=0
    for k in range(flat.size):
        keep=np.arange(flat.size)!=k
        beta=np.linalg.lstsq(design[keep],flat[keep],rcond=None)[0]
        sse+=(flat[k]-design[k]@beta)**2
    assert scores(y)['loo_sse']['additive']==pytest.approx(sse)

def test_pure_founder_and_history():
    y=np.repeat(np.arange(4.)[:,None],5,axis=1)
    assert scores(y)['loo_skill']['founder']==pytest.approx(1)
    assert scores(y.T)['loo_skill']['history']==pytest.approx(1)

def test_constant_and_interaction():
    assert scores(np.ones((3,4)))['loo_skill']['founder'] is None
    r=scores(np.array([[1.,-1.],[-1.,1.]]))
    assert r['ss_fraction']['interaction_plus_stochastic']==1
    assert r['loo_skill']['additive']<0

def test_permutation_and_offset():
    y=np.arange(12.).reshape(3,4)**2
    a=scores(y);b=scores(y[::-1,::-1]+3)
    assert a['loo_skill']==pytest.approx(b['loo_skill'])

@pytest.mark.parametrize('y',[np.zeros((1,4)),np.array([[0,np.nan],[1,2]]),np.zeros(3)])
def test_invalid(y):
    with pytest.raises(ValueError):scores(y)

def test_rejects_bad_provenance(tmp_path, monkeypatch):
    import json
    import zipfile
    import scripts.analyze_founder_predictability_20261021 as module
    (tmp_path/'docs/audits').mkdir(parents=True)
    (tmp_path/'scripts').mkdir()
    (tmp_path/'docs/audits/CHAPTER2_CONFIRM160_ASSET_SHA256_20261019.json').write_text(json.dumps({'raw-shard-0.zip':'source'}))
    (tmp_path/'scripts/variation_clock_readback_20261019.py').write_bytes(b'producer')
    archive=tmp_path/'bad.zip'
    with zipfile.ZipFile(archive,'w') as z:
        z.writestr('shard-0.json',json.dumps(dict(analysis_sha256='wrong',source_sha256='source',output_sha256='wrong')))
        z.writestr('shard-0.npz',b'not-an-array')
    monkeypatch.setattr(module,'ROOT',tmp_path)
    with pytest.raises(ValueError,match='provenance mismatch'):module.extract(archive)
