import json
import numpy as np
import pytest
from scripts.model3_restart_checkpoint import save_checkpoint, load_checkpoint


def state():
    return np.ones((1,1,1))*48, (np.eye(3,1),)*3


def test_roundtrip_preserves_period_and_state(tmp_path):
    save_checkpoint(tmp_path, state(), period=7, case='near_jump', source_hash='a'*64)
    restored, period=load_checkpoint(tmp_path, case='near_jump', source_hash='a'*64)
    assert period==7  # next visitor index is7, not6 or8
    np.testing.assert_array_equal(restored[0],state()[0])
    for a,b in zip(restored[1],state()[1]):np.testing.assert_array_equal(a,b)


def test_rejects_changed_identity_and_state(tmp_path):
    save_checkpoint(tmp_path,state(),period=7,case='near_jump',source_hash='a'*64)
    for case,source in [('far_jump','a'*64),('near_jump','b'*64)]:
        with pytest.raises(ValueError):load_checkpoint(tmp_path,case=case,source_hash=source)
    with (tmp_path/'state.npz').open('ab') as f:f.write(b'changed')
    with pytest.raises(ValueError):load_checkpoint(tmp_path,case='near_jump',source_hash='a'*64)


def test_incomplete_checkpoint_cannot_resume(tmp_path):
    np.savez(tmp_path/'state.npz',core=state()[0])
    with pytest.raises(ValueError):load_checkpoint(tmp_path,case='near_jump',source_hash='a'*64)


def test_preserves_existing_checkpoint(tmp_path):
    save_checkpoint(tmp_path,state(),period=7,case='near_jump',source_hash='a'*64)
    before=(tmp_path/'receipt.json').read_bytes()
    with pytest.raises(ValueError):save_checkpoint(tmp_path,state(),period=8,case='near_jump',source_hash='a'*64)
    assert (tmp_path/'receipt.json').read_bytes()==before


@pytest.mark.parametrize('period',[True,-1,1.5])
def test_invalid_period_rejected(tmp_path,period):
    with pytest.raises(ValueError):save_checkpoint(tmp_path,state(),period=period,case='near_jump',source_hash='a'*64)


def test_invalid_state_rejected(tmp_path):
    with pytest.raises(ValueError):save_checkpoint(tmp_path,(np.full((1,1,1),np.nan),state()[1]),period=7,case='near_jump',source_hash='a'*64)
