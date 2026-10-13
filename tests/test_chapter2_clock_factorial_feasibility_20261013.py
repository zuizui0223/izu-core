from pathlib import Path
import hashlib
import importlib.util
import io
import json
import zipfile

import numpy as np
import pytest

SRC=Path(__file__).resolve().parents[1]/'scripts'/'audit_chapter2_clock_factorial_feasibility_20261013.py'
spec=importlib.util.spec_from_file_location('clock_factorial_preflight',SRC)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def template():
    a=np.full((48,3,2),0.5,dtype=float)
    a[:,1,:]=np.tile([[.375,.625],[.5,.5],[.625,.375],[.5,.5]],(12,1))
    a[:,2,:]=[.4375,.5625]
    return a


@pytest.mark.parametrize('width',m.A_HALF_WIDTHS)
@pytest.mark.parametrize('scale',m.I_ALLELE_SCALE)
def test_transform_is_source_exact_mean_preserving_and_access_safe(width,scale):
    src=template()
    old=src.copy()
    new,summary=m.transform(src,width,scale)
    np.testing.assert_array_equal(src,old)
    np.testing.assert_array_equal(new[:,0,:],src[:,0,:])
    assert summary['I_scale']==scale
    assert summary['A_width']==width
    assert summary['I_can_reach_decline_without_mutation']
    assert summary['I_variance_relative_to_source']==pytest.approx(scale*scale,abs=1e-13)
    assert summary['I_allele_copy_mean']==pytest.approx(src[:,1,:].mean(),abs=1e-14)
    assert summary['A_expected_F1_segregation_variance_no_mutation']==pytest.approx(width**2/2)
    assert summary['A_founding_expressed_variance']==0
    assert summary['A_can_reach_threshold_without_mutation']==(width>=0.05)


def test_bad_synthetic_factor_or_founder_fails():
    a=template()
    with pytest.raises(ValueError):m.transform(a,.0625,1)
    with pytest.raises(ValueError):m.transform(a,.046875,0)
    with pytest.raises(ValueError):m.transform(a[:47],.046875,.5)
    a[:,1,:]=.5
    with pytest.raises(ValueError):m.transform(a,.078125,1.0)


def test_original_shard_must_be_sha_matched(tmp_path):
    p=tmp_path/'fake.zip'
    with zipfile.ZipFile(p,'w') as z:z.writestr('dummy','not original')
    with pytest.raises(ValueError,match='SHA256 mismatch'):m.audit(p)


def test_t0_feature_hashes_are_immutable_when_source_available():
    path=Path('/mnt/data/ecological-original-shard-0.zip')
    if not path.exists():pytest.skip('original source ZIP not packaged into repository test checkout')
    if hashlib.sha256(path.read_bytes()).hexdigest()!=m.SOURCE_SHARD0_SHA256:
        pytest.skip('ambient path is not immutable source')
    o=m.audit(path)
    assert o['new_biological_histories']==0
    assert len(o['factorial_t0_genotype_records'])==8
    blocks={b:[x for x in o['factorial_t0_genotype_records'] if x['block']==b] for b in ('main','confirmation')}
    assert all(len(r)==4 for r in blocks.values())
    for rs in blocks.values():
        assert len({r['I_allele_copy_mean'] for r in rs})==1
        assert len({r['A_founding_expressed_variance'] for r in rs})==1
        assert {r['I_variance_relative_to_source'] for r in rs}=={.25,1.}
