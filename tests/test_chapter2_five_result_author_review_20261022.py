"""Read-only packet tests; no biological runner imported or advanced."""
import json
from pathlib import Path
import shutil
import zipfile

import pytest

from scripts.build_chapter2_five_result_author_review_20261022 import (
    ALL, EXPECTED_STATUS, FIGURES, MAIN, ROOT,
    assemble, check_manuscript, collect, publish,
)


def test_actual_current_manuscript_and_six_figures_are_admitted():
    members, manifest = collect(ROOT, source_commit="test-source-ref")
    assert len(manifest["figures"]) == 6
    assert set(FIGURES).issubset(members)
    assert manifest["status"] == EXPECTED_STATUS
    assert 100 <= manifest["manuscript_counts"]["abstract_whitespace_words"] <= 200
    assert 2500 <= manifest["manuscript_counts"]["main_whitespace_words_including_headings"] <= 3500
    assert manifest["registered_evidence_check"]["crossed_cells"] == 25600
    assert manifest["registered_evidence_check"]["B8_every_population_occupied"]
    assert manifest["registered_evidence_check"]["G_high_I_support_loss_difference_pp"] == pytest.approx(8.328125)
    assert manifest["registered_evidence_check"]["S_policy_by_budget_survival_interaction_pp"] == pytest.approx(92.70703125)
    assert manifest["manuscript_counts"]["main_figure_count"] == 6
    assert any("/figure_04_predictability.svg" in p for p in manifest["figures"])
    assert not any("/figure_04_access_survival.svg" in p for p in manifest["figures"])


def test_packet_deterministic_source_exact_and_never_relabels_el(tmp_path):
    ref = "a" * 40
    packet_a = assemble(ROOT, ref)
    packet_b = assemble(ROOT, ref)
    assert packet_a == packet_b
    target = tmp_path / "AUTHOR_REVIEW.zip"
    receipt = publish(ROOT, target, ref)
    assert receipt["status"] == EXPECTED_STATUS
    assert target.read_bytes() == packet_a
    assert receipt["sha256"] in (tmp_path / "AUTHOR_REVIEW.zip.sha256").read_text()
    with zipfile.ZipFile(target) as archive:
        manifest = json.loads(archive.read("MANIFEST.json"))
        assert manifest["source_commit"] == ref
        assert archive.read(MAIN) == (ROOT / MAIN).read_bytes()
        assert all(path in archive.namelist() for path in FIGURES)
        assert "EL_ONE_PAPER_REVIEW.zip" not in archive.namelist()
        assert all("chapter2_nee_five_results" in f for f in manifest["figures"])
        assert manifest["schema"] == "izu_core_chapter2_r1_r5_author_review_v2"
        assert "docs/CHAPTER2_R1_R5_SOURCE_RECOVERY_AUDIT_20261022.md" in archive.namelist()
        assert "docs/CHAPTER2_A_DIRECTION_VS_FIXATION_EVIDENCE_20261022.md" in archive.namelist()
        assert "docs/CHAPTER2_R1_R5_COMPUTATIONAL_REPORTING_SUMMARY_20261022.md" in archive.namelist()
        assert "docs/deposit/CHAPTER2_FIVE_RESULTS_DOI_HANDOFF_20261021.md" in archive.namelist()
        assert "scripts/verify_chapter2_computational_reporting_20261022.py" in archive.namelist()
        assert "CHAPTER2_R1_R5_COMPUTATIONAL_REPORTING_SUMMARY_20261022.md" in archive.read(MAIN).decode("utf8")
        assert "NOT" in archive.read("README_AUTHOR_REVIEW.md").decode()
    with pytest.raises(ValueError, match="refusing to overwrite"):
        publish(ROOT, target, ref)


def test_fails_closed_if_one_figure_or_manuscript_head_disagrees(tmp_path):
    for rel in ALL:
        dest = tmp_path / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, dest)
    replacement = (tmp_path / MAIN).read_text(encoding="utf-8")
    (tmp_path / MAIN).write_text(replacement.replace(
        "## Abstract", "## Proposed results", 1), encoding="utf-8")
    with pytest.raises(ValueError, match="boundary"):
        collect(tmp_path)
    (tmp_path / MAIN).write_text(replacement, encoding="utf-8")
    (tmp_path / FIGURES[0]).write_text("<svg/>", encoding="utf-8")
    with pytest.raises(ValueError, match="source-marked SVG"):
        collect(tmp_path)


def test_reject_unauthorized_pending_results_even_with_valid_main_text():
    source = (ROOT / MAIN).read_bytes()
    assert check_manuscript(source)["main_figure_count"] == 6
    bad = source.replace(b"## Discussion\n", b"## Planned new decisive Results\n\n## Discussion\n", 1)
    with pytest.raises(ValueError, match="historic unexecuted"):
        check_manuscript(bad)


def test_previous_narrative_or_unregistered_GS_change_is_rejected(tmp_path):
    for rel in ALL:
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, target)
    manuscript = tmp_path / MAIN
    t = manuscript.read_text(encoding="utf-8")
    t = t.replace("Founding constraints and the predictability of reproductive evolution in an island plant model",
                  "Reproductive assurance differentially affects floral genetic accessibility and persistence under pollinator limitation", 1)
    manuscript.write_text(t, encoding="utf-8")
    with pytest.raises(ValueError, match="title mismatch"):
        collect(tmp_path)

    manuscript.write_bytes((ROOT / MAIN).read_bytes())
    summary = tmp_path / "docs/audits/CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json"
    j = json.loads(summary.read_text(encoding="utf-8"))
    j["primary"]["endpoints"][0]["estimate"] = .2
    summary.write_text(json.dumps(j), encoding="utf-8")
    with pytest.raises(ValueError, match="registered scientific result"):
        collect(tmp_path)
