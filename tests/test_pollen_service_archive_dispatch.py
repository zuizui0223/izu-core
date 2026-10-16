"""Bounded archive dispatch test; no visitor or plant histories are simulated."""
import io
import json
import zipfile
from types import SimpleNamespace

import numpy as np
import pytest

from scripts import audit_chapter2_original_evolved_pollen_service as audit


def test_source_audit_reads_each_arm_and_mode_from_its_own_shard(monkeypatch):
    design = dict(settings=["fixture"], history_seed_first=1,
                  history_seed_last=64, arms=["near", "far"], periods=[200],
                  artifact_shards=[dict(artifact_id=i) for i in range(4)])
    archives = {}
    investments = [.2, .4, .3, .7]
    for shard, investment in enumerate(investments):
        arm = "near" if shard < 2 else "far"
        mode = "fixed" if shard % 2 == 0 else "evolving"
        alleles = np.full((1, 3, 2), .5)
        alleles[:, 1, :] = investment
        trace = np.zeros((201, 10))
        trace[200, 1:4] = alleles.mean(axis=(0, 2))
        checkpoint = io.BytesIO()
        np.savez(checkpoint, state_200=alleles, trace=trace)
        payload = checkpoint.getvalue()
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            for seed in range(1, 65):
                prefix = (f"shard-{shard:02d}/main_fixture_u0.01_h{seed}"
                          f"_r26111601_{arm}_{mode}")
                archive.writestr(prefix + ".npz", payload)
                archive.writestr(prefix + ".json", json.dumps(dict(
                    sha256=audit._sha(payload),
                    task=["main", "fixture", .01, seed, 26111601, arm, mode])))
        archives[shard] = zipfile.ZipFile(io.BytesIO(buffer.getvalue()))

    monkeypatch.setattr(audit, "read_design", lambda: design)
    monkeypatch.setattr(audit, "original_shards", lambda paths, d: archives)
    monkeypatch.setattr(audit, "parity", lambda: None)
    monkeypatch.setattr(audit, "load_design", lambda path: {})
    monkeypatch.setattr(audit, "config", lambda *args: SimpleNamespace(pollen_discount=0))
    monkeypatch.setattr(audit, "source_visitors",
                        lambda *args: {200: SimpleNamespace(ids=np.array([1]))})

    def ledger(state, visitors, cfg):
        value = np.array([state.alleles[:, 1, :].mean()])
        return SimpleNamespace(delivered=value, outcross=value,
                               maternal=value, self_viable=value)

    monkeypatch.setattr(audit, "reproduce", ledger)
    try:
        report = audit.source_audit([])
    finally:
        for archive in archives.values():
            archive.close()
    assert report["original_case_checkpoints"] == 128
    assert report["n_new_histories"] == 0
    for row in report["raw"]:
        expected = .2 if row["arm"] == "near" else .4
        assert row["delta_I"] == pytest.approx(expected)
        assert row["evo_minus_fixed_delivered"] == pytest.approx(expected)
        assert row["evo_minus_I_clamped_delivered"] == pytest.approx(expected)
