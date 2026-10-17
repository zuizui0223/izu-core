"""Adversarial source-arithmetic review; all original biological producers are frozen."""
import json
import shutil

import pytest

from scripts.audit_chapter2_paper_arithmetic_20261017 import (
    EvidenceMismatch, MANUSCRIPT, SOURCES, reconcile,
)


def isolate_sources(tmp_path):
    """Make a self-contained, editable copy of the original signed receipts."""
    from scripts.audit_chapter2_paper_arithmetic_20261017 import ROOT
    for relative, _pin in SOURCES.values():
        dest = tmp_path / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, dest)
    destination = tmp_path / MANUSCRIPT
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / MANUSCRIPT, destination)
    return tmp_path


def edit_json(root, name, transform):
    path = root / SOURCES[name][0]
    payload = json.loads(path.read_text(encoding="utf-8"))
    transform(payload)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def test_original_source_arithmetic_and_git_pins_pass():
    result = reconcile()
    assert result["status"] == "PASS_SOURCE_ARITHMETIC_ONLY"
    assert result["new_biological_runs"] == 0
    assert result["independent_raw_genome_replay"] is False
    assert result["checks"]["q1"]["fresh_founder_compression_supported"] == 3
    assert result["checks"]["q2"]["both_coprimary"] == "INCONCLUSIVE"
    assert result["checks"]["q3"]["pre_fixation_support_losses"] == 703


def test_q1_did_rejects_misreported_sign_even_without_blob_guard(tmp_path):
    root = isolate_sources(tmp_path)
    edit_json(root, "q1", lambda q: q["settings"][0]["attenuation_evolving_minus_fixed"].update(mean=.5))
    with pytest.raises(EvidenceMismatch, match="Q1 difference-in-differences"):
        reconcile(root, check_identity=False)


def test_q2_rejects_unreported_category_change(tmp_path):
    root = isolate_sources(tmp_path)
    edit_json(root, "q2",
              lambda q: q["original_six_class_cells"]["far"]["dense_reachable"]["counts"].__setitem__(0, 15))
    with pytest.raises(EvidenceMismatch, match="six-category"):
        reconcile(root, check_identity=False)


def test_q2_rejects_posthoc_significance_promotion(tmp_path):
    root = isolate_sources(tmp_path)
    edit_json(root, "q2",
              lambda q: q["coprimary"]["carrier_order_score_delta"].update(
                  simultaneous_familywise_CI=[.001, .34], excludes_zero=True))
    with pytest.raises(EvidenceMismatch, match="Q2 simultaneous"):
        reconcile(root, check_identity=False)


def test_q3_rejects_missing_source_cell(tmp_path):
    root = isolate_sources(tmp_path)
    edit_json(root, "q3", lambda q: q["cells"].pop())
    with pytest.raises(EvidenceMismatch, match="Q3 source case inventory"):
        reconcile(root, check_identity=False)


def test_q4_rejects_pooled_arithmetic_change(tmp_path):
    root = isolate_sources(tmp_path)
    edit_json(root, "q4",
              lambda q: q["predeclared_pooled_primary"].update(mean=.18))
    with pytest.raises(EvidenceMismatch, match="Q4 pooled"):
        reconcile(root, check_identity=False)


def test_manuscript_boundary_and_immutable_receipts(tmp_path):
    root = isolate_sources(tmp_path)
    paper = root / MANUSCRIPT
    paper.write_text(paper.read_text(encoding="utf-8").replace(
        "Both co-primary intervals included zero",
        "Both co-primary intervals excluded zero"), encoding="utf-8")
    with pytest.raises(EvidenceMismatch, match="Original paper changed"):
        reconcile(root)
    with pytest.raises(EvidenceMismatch, match="missing scope guard"):
        reconcile(root, check_identity=False)


def test_source_blob_guard_is_distinct_from_arithmetic(tmp_path):
    root = isolate_sources(tmp_path)
    edit_json(root, "q1", lambda q: q.update(date="2099-01-01"))
    with pytest.raises(EvidenceMismatch, match="Frozen source changed"):
        reconcile(root)
    assert reconcile(root, check_identity=False)["status"] == "PASS_SOURCE_ARITHMETIC_ONLY"
