"""Old-history integration test for t400 archive → 28 future arms → audit.

The ONLY biological history seed used is the archived 26110601. The new 64
prospective histories 37110801-37110864 are never sampled by these tests.
"""
from dataclasses import replace
import json
import numpy as np
import pytest

from scripts.plan_chapter2_order_expression_identification import (
    Prehistory, load_protocol, decision,
)
from scripts.chapter2_order_prehistory_runner import (
    case_key, persist_one as persist_pre, source_hashes,
)
from scripts.chapter2_order_postshock_runner import (
    persist_one as persist_post, restore_prehistory, paired_streams,
)
from scripts.chapter2_order_confirmatory_readout import admit_all
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, load_design as source_biology,
)


@pytest.fixture(scope="module")
def protocol():
    return load_protocol()


def old_task():
    return Prehistory(
        "delayed_control", "near", "assurance_first", 26110601, 26111601
    )


def test_persist_and_restore_400_inherited_updates_old_history(tmp_path, protocol):
    task = old_task()
    pre = tmp_path / "prehistory"
    future = tmp_path / "future"
    pre.mkdir()
    future.mkdir()
    biology = source_biology(DEFAULT_DESIGN)
    hashes = source_hashes()
    name = persist_pre(pre, task, protocol, biology, hashes)
    assert name == case_key(task)
    state, sha = restore_prehistory(pre, task, protocol, hashes)
    assert sha and len(sha) == 64
    assert state.alleles.shape[1:] == (3, 2)
    metadata = json.loads((pre / f"{name}.json").read_text())
    assert metadata["completed_updates"] == 400
    assert len(metadata["annual_inherited_censuses"]) == 401
    assert metadata["annual_inherited_censuses"][-1]["n"] == len(state.ids)
    assert metadata["realized_genetic_order"]["expression_offsets_not_used"] is True
    with np.load(pre / f"{name}.npz", allow_pickle=False) as archive:
        genealogy = archive["parentage_edges"]
        assert genealogy.ndim == 2 and genealogy.shape[1] == 4
        assert len(genealogy) == metadata["parentage_link_count"]
        assert genealogy.dtype.kind in "iu"

    persist_post(future, pre, task, protocol, biology, hashes)
    row = json.loads((future / f"{name}.json").read_text())
    assert row["status"] == "raw_postshock_unadjudicated"
    assert len(row["postshock"]) == 28
    assert set(c["future_assurance_mode"] for c in row["postshock"]) == {"evolving"}
    assert all(c["future_expression_offsets"] == [0,0] for c in row["postshock"])

    pre_results, post_results = admit_all(
        pre, future, protocol, tasks=[task], require_full=False
    )
    assert len(pre_results) == len(post_results) == 1
    assert len(post_results[task]) == 28

    # The parentage chronology is revalidated independently of NPZ checksum.
    pedigree_corrupt = json.loads((pre / f"{name}.json").read_text())
    pedigree_corrupt["parentage_link_count"] += 1
    (pre / f"{name}.json").write_text(json.dumps(pedigree_corrupt))
    with pytest.raises(AssertionError, match="parentage archive"):
        admit_all(pre, future, protocol, tasks=[task], require_full=False)
    (pre / f"{name}.json").write_text(json.dumps(metadata))

    # SHA protects content, but the auditor must independently catch a changed
    # t400 genotype or an impossible fork even if a JSON receipt is recomputed.
    receipt = json.loads((pre / f"{name}.json").read_text())
    receipt["annual_inherited_censuses"][-1]["inherited_means"] = [0.1, 0.1, 0.1]
    (pre / f"{name}.json").write_text(json.dumps(receipt))
    with pytest.raises(AssertionError, match="source inherited means"):
        admit_all(pre, future, protocol, tasks=[task], require_full=False)


def test_common_demographic_streams_do_not_include_order_or_pre_environment(protocol):
    a = old_task()
    b = replace(a, expression_order="investment_first", environment="far")
    ra = paired_streams(a, protocol, "eight_founders_capacity8", "near", 3)
    rb = paired_streams(b, protocol, "eight_founders_capacity8", "near", 3)
    for name in ("survival", "parents", "recruitment", "segregation", "mutation"):
        assert ra[name].random() == rb[name].random()


def test_nonpeeking_production_gate_and_ITT_bounds(protocol):
    # No new biological histories are used for these algebraic decisions.
    assert decision(0.08, (0.02, 0.14)) == "nonzero_order_protocol_effect"
    assert decision(0.015, (-0.02, 0.04)) == "equivalent_within_predeclared_ROPE"
    assert decision(0.08, (-0.02, 0.17)) == "inconclusive"
    assert protocol["counts"]["prehistories"] == 3072
    assert protocol["counts"]["postshock_trajectories"] == 86016
    assert protocol["independent_histories"]["first"] > 37000000
