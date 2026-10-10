"""EL one-paper review packaging cannot silently deliver the historical draft."""
import json
from pathlib import Path
import zipfile

import pytest

from scripts.build_chapter2_unified_el_submission_bundle import (
    OUT, PDF_FIGURES, FROZEN_RESULTS, blind_paper, build,
)

ROOT=Path(__file__).resolve().parents[1]


def test_current_blinded_paper_is_correct_and_within_EL_limits():
    paper=blind_paper()
    source=(ROOT/"docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md").read_text()
    historical=(ROOT/"docs/CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md").read_text()
    assert paper.startswith("# Reproductive assurance compresses floral-investment divergence")
    assert paper != historical
    assert paper != source
    assert len(paper.split("## Abstract",1)[1].split("## Keywords",1)[0].split())<=150
    assert len(paper.split("# Introduction",1)[1].split("# Primary figure assembly and captions",1)[0].split())<=5000
    assert paper.count("**Figure 4.")==1
    assert "Demographic-capacity" in paper or "demographic-capacity" in paper
    assert "0.007746" in paper and "inconclusive" in paper
    assert "not a natural mediation analysis" in paper.lower()
    assert "Issue #436" not in paper
    assert "PR #452" not in paper
    assert "zuizui0223" not in paper.lower()
    assert "DOI-backed raw-data archive has not yet been deposited" in paper
    assert "521 original biological-trajectory ZIP archives" not in paper


def fake_pdfs(tmp_path):
    out={}
    for i,label in enumerate(PDF_FIGURES,1):
        p=tmp_path/label
        p.write_bytes((b"%PDF-1.4\n"+bytes([65+i])*1200+
                       b"\nstartxref\n0\n%%EOF\n"))
        out[label]=p
    return out


def test_review_package_has_correct_four_figures_only(tmp_path):
    out=tmp_path/"EL_ONE_PAPER_REVIEW.zip"
    receipt=build(out,figures=fake_pdfs(tmp_path))
    assert receipt["n_figures"]==4
    assert receipt["submitted"] is False
    assert receipt["doi_deposit_complete"] is False
    with zipfile.ZipFile(out) as z:
        names=z.namelist()
        assert names.count("MANUSCRIPT.md")==1
        assert names.count("SUPPORTING_INFORMATION.md")==1
        assert [x for x in names if x.startswith("Figure")]==[
           "Figure1.pdf","Figure2.pdf","Figure3.pdf","Figure4.svg"]
        assert "Figure4.pdf" not in names
        assert sorted(x for x in names if x.startswith("EVIDENCE/"))==[
           "EVIDENCE/CAPACITY_RESULTS.json",
           "EVIDENCE/EVOLUTION_DESIGN.json",
           "EVIDENCE/EVOLUTION_RESULTS.json",
        ]
        m=json.loads(z.read("MANIFEST.json"))
        assert m["source_active_manuscript"].startswith("CHAPTER2_UNIFIED")
        assert m["doi_deposit_complete"] is False
        assert m["n_figures"]==4
        assert len(m["members"])==9
        paper=z.read("MANUSCRIPT.md").decode("utf-8")
        assert paper==blind_paper()
        assert "0.007746" in paper
    saved=json.loads(out.with_suffix(".receipt.json").read_text())
    assert saved["manuscript_sha256"]==receipt["manuscript_sha256"]


def test_package_refuses_missing_unrendered_figures(tmp_path):
    figures=fake_pdfs(tmp_path)
    figures["Figure2.pdf"]=tmp_path/"no-such-figure.pdf"
    with pytest.raises(FileNotFoundError):
        build(tmp_path/"bad.zip",figures=figures)
    figures=fake_pdfs(tmp_path)
    figures["Figure2.pdf"].write_bytes(b"garbage")
    with pytest.raises(ValueError,match="invalid PDF"):
        build(tmp_path/"bad2.zip",figures=figures)
    with pytest.raises(ValueError,match="exactly Figure1"):
        build(tmp_path/"bad3.zip",figures={"Figure1.pdf":tmp_path/"x"})


def test_evidence_receipts_are_identified_and_not_pooled():
    assert len(FROZEN_RESULTS)==3
    route=json.loads((ROOT/"data/design/chapter2_one_paper_route_20261010.json").read_text())
    assert route["active_manuscript_count"]==1
    assert route["review_package_builder"]=="scripts/build_chapter2_unified_el_submission_bundle.py"
    assert route["review_package_expected_figures"]==[
        "Figure1.pdf","Figure2.pdf","Figure3.pdf","Figure4.svg"]
    assert "historical only" in route["legacy_process_builder"]
    evo=json.loads((ROOT/FROZEN_RESULTS["EVOLUTION_RESULTS.json"]).read_text())
    assert evo["adjudication"]["status"]=="all_four_confirmed"
    assert evo["independent_visitor_histories"]==64
    assert all(x["passes_frozen_rule"] for x in evo["settings"])
    cap=json.loads((ROOT/FROZEN_RESULTS["CAPACITY_RESULTS.json"]).read_text())
    assert cap["primary_verdict"]=="supported_controlled_demographic_K_moderation_at_fixed_B48"
