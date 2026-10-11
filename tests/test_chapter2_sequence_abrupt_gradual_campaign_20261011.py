"""Full-vs-smoke provenance safeguards for abrupt/gradual Model3 campaign."""
import json
import numpy as np
import pytest

from scripts.run_chapter2_sequence_abrupt_gradual_batch_20261011 import (
    tasks,key,run_one,run_shard
)
from scripts.summarize_chapter2_sequence_abrupt_gradual_functional_loss_20261011 import (
    read_all,clustered_summary
)


def test_every_declared_pair_is_present_once_and_nested():
    full=tasks()
    assert len(full)==len(set(full))==1024
    assert len({key(c) for c in full})==1024
    assert len({c[0] for c in full})==16
    assert len({c[1] for c in full})==4
    settings={(c[2],c[3],c[4]) for c in full}
    assert len(settings)==8
    assert all(sum(c[0]==p for c in full)==64
               for p in range(48271001,48271017))
    for p in range(48271001,48271017):
        for r in range(49271001,49271005):
            for setting in settings:
                scoped=[c for c in full if c[0]==p and c[1]==r and c[2:5]==setting]
                assert len(scoped)==2
                assert {c[-1] for c in scoped}=={"abrupt","gradual"}


def test_smoke_outputs_are_sha_verified_but_never_biological_readout(tmp_path):
    c=tasks()[0]
    result=run_one(tmp_path,c,smoke_years=3)
    assert result.endswith("_SMOKE")
    rc=tmp_path/(result+".receipt.json")
    payload=json.loads(rc.read_text())
    assert payload["full_declared_case"] is False
    assert payload["years"]==3
    assert len(payload["source_identity_sha256"])==64
    assert "scripts/model3_island/reproduction.py" in payload["source_file_sha256"]
    assert "scripts/summarize_chapter2_sequence_abrupt_gradual_functional_loss_20261011.py" in payload["source_file_sha256"]
    assert run_one(tmp_path,c,smoke_years=3)==result
    case_json=tmp_path/(result+".json")
    scientific=json.loads(case_json.read_text())
    assert scientific["full_declared_case"] is False
    assert scientific["years"]==3
    with pytest.raises(FileNotFoundError):
        read_all(tmp_path)
    with pytest.raises(ValueError):
        run_shard(tmp_path,shard_index=0,shard_count=16,case_limit=1)
    with pytest.raises(ValueError):
        run_shard(tmp_path,shard_index=16,shard_count=16,
                  smoke_years=3,case_limit=1)
    with pytest.raises(ValueError):
        run_shard(tmp_path,shard_index=0,shard_count=8,
                  smoke_years=3,case_limit=1)


def test_partial_shard_manifest_is_marked_smoke_and_cannot_fake_completion(tmp_path):
    m=run_shard(tmp_path,shard_index=0,shard_count=16,
                smoke_years=2,case_limit=1)
    assert m["status"]=="INCOMPLETE_SMOKE_NO_BIOLOGICAL_READOUT"
    assert m["case_count"]==1
    assert m["expected_full_case_count"]==64
    assert len(m["source_identity_sha256"])==64
    assert not (tmp_path/"shard_00_complete.json").exists()
    with pytest.raises(FileNotFoundError):
        read_all(tmp_path)


def test_clustered_readout_rejects_incomplete_or_wrong_biological_unit():
    assert len(tasks())==1024
    with pytest.raises(AssertionError):
        clustered_summary({})
