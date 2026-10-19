import numpy as np
import pytest
from scripts.variation_clock_readback_20261019 import trajectory, join_states, crossed


def state(values, counts=None):
    a=np.asarray(values,dtype=float)
    if a.ndim==2:a=np.repeat(a[:,:,None,None],3,axis=2);a=np.repeat(a,2,axis=3)
    return a,np.asarray(counts if counts is not None else [a.shape[1]]*len(a),dtype=int)


def test_fixation_then_extinction_remains_separate():
    a,n=state([[.25,.75],[.5,.5],[0,0]],[2,2,0])
    r=trajectory(a,n)
    assert r['first_fix'].tolist()==[1,1,1]
    assert r['fixed_value'].tolist()==[.5,.5,.5]
    assert r['extinction']==2
    assert r['richness'].tolist()==[[2,2,2],[1,1,1],[0,0,0]]


def test_extinction_is_not_fixation_and_padding_is_ignored():
    a,n=state([[.25,.75],[.25,0],[0,0]],[2,1,0])
    r=trajectory(a,n)
    assert r['fixed_value'].tolist()==[.25]*3
    a,n=state([[.25,.75],[0,0]],[2,0])
    assert trajectory(a,n)['first_fix'].tolist()==[-1]*3


def test_constant_heterozygotes_keep_allelic_variation():
    a=np.tile([.25,.75],(2,2,3,1));n=np.array([2,2])
    r=trajectory(a,n)
    assert np.all(r['richness']==2)
    assert np.all(r['genotype_variance']==0)
    assert np.all(r['first_fix']==-1)


def test_no_reappearance_after_extinction():
    a,n=state([[.5,.5],[0,0],[.5,.5]],[2,0,2])
    with pytest.raises(ValueError,match='extinction'):trajectory(a,n)


def test_fork_continuity_and_duplicate_removed():
    a,n=state([[.25,.75],[.5,.5]])
    b,m=state([[.5,.5],[.5,0]],[2,1])
    joined,counts=join_states((a,n),(b,m))
    assert len(joined)==3 and counts.tolist()==[2,2,1]
    b[0,0,0,0]=.25
    with pytest.raises(ValueError,match='fork'):join_states((a,n),(b,m))


def test_crossed_uncertainty_uses_axes_not_cell_iid():
    x=np.tile(np.array([-1.,0.,1.,2.])[:,None],(1,5))
    r=crossed(x)
    assert r['estimate']==.5
    assert r['variance']==pytest.approx(5/16)
    assert r['degrees_of_freedom']==3
    assert r['simultaneous_interval'][0]<r['pointwise_interval'][0]


def test_receipt_cannot_relabel_old_analysis_or_source(tmp_path):
    import json
    from scripts.variation_clock_readback_20261019 import verify_receipt, file_hash
    data=tmp_path/'s.npz';data.write_bytes(b'bytes')
    receipt=tmp_path/'s.json'
    receipt.write_text(json.dumps(dict(analysis_sha256='old',source_sha256='source',output_sha256=file_hash(data))))
    with pytest.raises(ValueError,match='analysis'):verify_receipt(data,receipt,'new','source')
    with pytest.raises(ValueError,match='source'):verify_receipt(data,receipt,'old','other')
    verify_receipt(data,receipt,'old','source')
    data.write_bytes(b'changed')
    with pytest.raises(ValueError,match='output'):verify_receipt(data,receipt,'old','source')


def test_vectorized_counts_match_direct_unique_for_ragged_states():
    a=np.zeros((3,3,3,2))
    a[0]=np.array([[[.25,.75]]*3,[[.25,.25]]*3,[[.75,.75]]*3])
    a[1,:2]=a[0,:2];a[2,0]=a[0,1]
    n=np.array([3,2,1]);r=trajectory(a,n)
    for c,size in enumerate(n):
        for l in range(3):
            assert r['richness'][c,l]==len(np.unique(a[c,:size,l]))
            assert r['mean'][c,l]==pytest.approx(a[c,:size,l].mean())
            assert r['genotype_variance'][c,l]==pytest.approx(a[c,:size,l].mean(axis=1).var())


def test_reader_has_no_simulator_import_or_rng_call():
    import ast
    from pathlib import Path
    source=Path('scripts/variation_clock_readback_20261019.py').read_text()
    tree=ast.parse(source)
    for n in ast.walk(tree):
        if isinstance(n,ast.ImportFrom):
            assert not (n.module or '').startswith('scripts')
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute):
            assert n.func.attr not in ('default_rng','random','normal','choice','integers','advance','inherit')
