"""Do not lose precise transient raw-source identity or overstate publication."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INVENTORY=ROOT/"docs/deposit/chapter2_far_asymmetry_source_artifact_inventory_20261015.json"


def test_source_artifact_inventory_is_complete_and_not_published():
    d=json.loads(INVENTORY.read_text(encoding="utf-8"))
    assert d["status"]=="SOURCE_BYTES_CHECKED_IN_ACTIONS_NOT_EXTERNAL_ARCHIVED"
    assert d["total_artifact_zip_count"]==22
    assert d["total_zip_bytes"]==302565495
    assert len(d["new_workflows"])==2
    counts=sorted(x["artifact_count"] for x in d["new_workflows"])
    assert counts==[5,17]
    names=[];ids=[]
    for campaign in d["new_workflows"]:
        assert campaign["all_zip_bytes"]==sum(a["zip_bytes"] for a in campaign["artifacts"])
        for a in campaign["artifacts"]:
            names.append(a["name"])
            ids.append(a["artifact_id"])
            assert a["expired"] is False
            assert a["expires_at"].startswith("2027-01-13T")
            assert re.fullmatch(r"sha256:[0-9a-f]{64}",a["sha256_of_artifact_zip"])
            assert a["zip_bytes"]>0
    assert len(set(ids))==len(ids)==22
    assert len(set(names))==22
    assert "not" in d["claim"].lower()
    assert d["source_original_evolution_run_id"]==37458098483
    assert len(d["source_original_evolution_archive_ids"])==4
