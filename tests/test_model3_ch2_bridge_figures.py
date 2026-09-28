"""Figure eligibility and artifact-integrity checks, independent of biology."""
import json
from hashlib import sha256
import numpy as np
import pytest
from scripts.plot_model3_ch2_bridge import history_points,load_verified


def test_plot_does_not_average_away_undefined_replicates():
    a=np.ones((3,4,8));a[0,0,0]=np.nan
    points=history_points(a)
    assert np.isnan(points[0,0])
    assert np.isfinite(points).sum()==11


def test_figure_loader_rejects_changed_audited_inputs(tmp_path):
    (tmp_path/'summary.json').write_text(json.dumps({'status':'complete_audited_summary'}))
    np.savez(tmp_path/'derived_tensors.npz',test=np.ones((3,4,8)))
    hashes={p.name:sha256(p.read_bytes()).hexdigest() for p in tmp_path.iterdir()}
    (tmp_path/'provenance.json').write_text(json.dumps({'artifacts':hashes}))
    assert load_verified(tmp_path)[0]['status']=='complete_audited_summary'
    (tmp_path/'summary.json').write_text('{}')
    with pytest.raises(ValueError,match='checksum'):load_verified(tmp_path)
