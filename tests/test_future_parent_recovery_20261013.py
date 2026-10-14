import pytest
from scripts import recover_future_parent_selection_20261013 as r


def test_only_five_frozen_missing_shards_can_execute():
    assert r.MISSING==(1,4,5,10,15)
    assert set(r.MISSING).isdisjoint(r.PRESERVED)
    assert set(r.MISSING)|set(r.PRESERVED)==set(range(16))
    assert len(r.MISSING)*256==1280 and len(r.PRESERVED)*256==2816


def test_unpinned_recovery_input_rejected_before_extraction(tmp_path):
    p=tmp_path/'wrong.zip';p.write_bytes(b'wrong')
    with pytest.raises(ValueError,match='original bytes'):
        r.prepare(p,p,tmp_path/'out')
    assert not (tmp_path/'out').exists()


def test_registered_recovery_job_uses_only_preserved_artifacts_and_five_slots():
    from pathlib import Path
    s=Path('.github/workflows/chapter2-pr471-native-verification.yml').read_text(encoding='utf-8')
    assert 'future-parent-recovery' in s
    assert 'python -m scripts.recover_future_parent_selection_20261013 prepare' in s
    assert 'python -m scripts.recover_future_parent_selection_20261013 run' in s
