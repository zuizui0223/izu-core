"""Check historical GitHub Actions artifact inventory, not raw data itself.

Static read-only metadata validation. Does not fetch files, train or simulate.
"""
import json
import re
from pathlib import Path


ROOT=Path(__file__).resolve().parents[1]
INVENTORY=ROOT/"data/design/chapter2_raw_actions_artifact_inventory_20261009.json"
EXPECTED={
    37887039116: {"diploid-t400-source":64, "source-admission":1},
    37887290489: {"raw-future-shard":64, "other-result":1},
    37893126472: {"raw-future-shard":64, "diploid-t400-source":64,
                  "source-admission":1,"other-result":1},
    37896872795: {"raw-future-shard":64, "diploid-t400-source":64,
                  "source-admission":1,"other-result":1},
}


def test_all_four_original_runs_and_exact_390_artifact_metadata():
    d=json.loads(INVENTORY.read_text(encoding="utf-8"))
    assert d["status"]=="COMPLETE_GITHUB_ACTIONS_METADATA_ONLY_NOT_RAW_BYTE_PRESERVATION"
    assert d["expected_artifacts"]==390
    assert d["snapshot_date_utc"]=="2026-10-09"
    assert d["repository"]=="zuizui0223/izu-core"
    assert {c["run_id"] for c in d["campaigns"]}==set(EXPECTED)
    ids=[]
    total=0
    for campaign in d["campaigns"]:
        assert campaign["types"]==EXPECTED[campaign["run_id"]]
        assert len(campaign["artifacts"])==campaign["expected_artifacts"]
        assert len({a["name"] for a in campaign["artifacts"]})==len(campaign["artifacts"])
        assert sum(a["artifact_zip_bytes"] for a in campaign["artifacts"])==campaign["stored_artifact_zip_bytes"]
        for a in campaign["artifacts"]:
            ids.append(a["id"])
            assert re.fullmatch(r"[0-9a-f]{64}",a["github_archive_sha256"])
            assert a["artifact_zip_bytes"]>0
            assert a["created_at"]<a["expires_at"]
            assert a["expired_as_of_inventory"] is False
            total+=a["artifact_zip_bytes"]
    assert len(ids)==len(set(ids))==390
    assert total==d["total_stored_artifact_zip_bytes"]
    assert total>600*1024*1024


def test_metadata_not_misrepresented_as_byte_preservation():
    d=json.loads(INVENTORY.read_text(encoding="utf-8"))
    text=" ".join(d["limitations"]).lower()
    assert "not preserve" in text
    assert "not an independent local re-download checksum" in text
    assert "artifact" in text and "expire" in text
