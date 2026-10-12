"""Numerical agreement must never silently replace the frozen byte identity gate."""
import hashlib
import json
from pathlib import Path

import pytest

from scripts.audit_independent32_replay_admission_20261013 import audit


def inputs(tmp_path):
    d={"settings":["s0","s1","s2","s3"],
       "independent_visitor_histories":{"first":20,"last":51},
       "demographic_repeat_seeds":[9],"post_environments":["near","far"],
       "stress_ovule_budgets":[2,3,4,5],"total_groups":512,
       "bootstrap":{"seed":3010082026,"draws":9999}}
    rows=[]
    for s in d["settings"]:
        for mode in ("fixed","evolving"):
            for h in range(20,52):
                for pre in ("near","far"):
                    occupied=int(mode=="evolving" and pre=="far")
                    rows.append({"group":[s,mode,h,9,pre],"pre_survivors":8,
                                 "post_cases":[{"post":p,"ovule_budget":b,
                                    "occupied":occupied,"terminal_N":occupied}
                                    for p in d["post_environments"] for b in d["stress_ovule_budgets"]]})
    hashes={}
    for shard in range(8):
        p=tmp_path/f"demographic_independent32_shard_{shard:02d}.json"
        raw=(json.dumps(rows[shard::8],sort_keys=True)+"\n").encode()
        p.write_bytes(raw);hashes[p.name]=hashlib.sha256(raw).hexdigest()
    f={"independent_histories":32,"historical_pre_groups":512,"post_switch_trajectories":4096,
       "predeclared_pooled_primary":{"mean":1.,"bootstrap95":[1.,1.]},
       "per_setting":[{"setting":s,"interaction":1.} for s in d["settings"]],
       "archive":{"offline_shard_sha256":hashes}}
    return d,f


def change(directory, edit):
    p=directory/"demographic_independent32_shard_00.json"
    rows=json.loads(p.read_bytes());edit(rows)
    p.write_text(json.dumps(rows),encoding="utf-8")


def test_complete_inventory_statistics_and_byte_agreement(tmp_path):
    d,f=inputs(tmp_path);r=audit(tmp_path,d,f)
    assert r["groups"]==512 and r["post_trajectories"]==4096
    assert r["numerical_agreement"] and r["declared_byte_agreement"]
    assert r["pooled_primary"]["mean"]==1.


def test_serialization_change_retains_original_identity_failure(tmp_path):
    d,f=inputs(tmp_path)
    p=tmp_path/"demographic_independent32_shard_00.json"
    p.write_bytes(p.read_bytes()+b" ")
    r=audit(tmp_path,d,f)
    assert r["numerical_agreement"] and not r["declared_byte_agreement"]
    assert r["status"]=="NUMERICS_MATCH_DECLARED_BYTES_DIVERGE_NOT_ORIGINAL_ADMISSION"
    assert len(r["byte_mismatches"])==1


@pytest.mark.parametrize("edit,match",[
    (lambda rows:rows.append(rows[0]),"duplicate"),
    (lambda rows:rows[0]["post_cases"].pop(),"grid"),
    (lambda rows:rows[0]["post_cases"][0].update(occupied=2),"occupancy"),
    (lambda rows:rows[0]["post_cases"][0].update(terminal_N=1),"census"),
])
def test_corrupt_cases_fail_closed(tmp_path,edit,match):
    d,f=inputs(tmp_path);change(tmp_path,edit)
    with pytest.raises(ValueError,match=match):audit(tmp_path,d,f)


def test_changed_frozen_target_is_reported_not_tuned(tmp_path):
    d,f=inputs(tmp_path);f["predeclared_pooled_primary"]["mean"]=0.9
    r=audit(tmp_path,d,f)
    assert not r["numerical_agreement"]
    assert r["status"]=="NUMERICAL_DISAGREEMENT_NOT_ADMITTED"


def test_missing_shard_refuses_audit(tmp_path):
    d,f=inputs(tmp_path);(tmp_path/"demographic_independent32_shard_07.json").unlink()
    with pytest.raises(ValueError,match="eight"):audit(tmp_path,d,f)
