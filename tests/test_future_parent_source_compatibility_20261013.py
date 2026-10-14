import pytest
from scripts import future_parent_source_compatibility_20261013 as c


def test_only_verification_change_is_compatible():
    old='X=1\ndef trajectory(): return X\ndef verify(): return 0\ndef technical_gate(): return 0\n'
    new=old.replace('return 0','return 1')
    assert c.generation_digest(old)==c.generation_digest(new)
    assert c.generation_digest(old)!=c.generation_digest(new.replace('X=1','X=2'))


def test_active_pool_rejects_unknown_source_and_wrong_old_hash():
    c.validate_active()
    r={'execution_commit':c.OLD_COMMIT,'runner_sha256':c.OLD_RUNNER_SHA}
    c.admit_source(r)
    with pytest.raises(ValueError):c.admit_source(dict(r,execution_commit='0'*40))
    with pytest.raises(ValueError):c.admit_source(dict(r,runner_sha256='0'*64))


def test_recipe_binding_inventory_cannot_be_dropped(tmp_path,monkeypatch):
    import json
    r=json.loads(c.REGISTRY.read_bytes());r['binding_sha256']={}
    file=tmp_path/'registry.json';file.write_text(json.dumps(r))
    monkeypatch.setattr(c,'REGISTRY',file)
    with pytest.raises(ValueError,match='binding inventory'):c.validate_active()
