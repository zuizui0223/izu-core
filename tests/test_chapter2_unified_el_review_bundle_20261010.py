"""EL one-paper review packaging cannot silently deliver the historical draft."""
import gzip
import hashlib
import json
from pathlib import Path
import zipfile

import pytest
from pypdf import PdfWriter

import scripts.build_chapter2_unified_el_submission_bundle as builder

from scripts.build_chapter2_unified_el_submission_bundle import (
    OUT, PDF_FIGURES, FROZEN_RESULTS, blind_paper, build,
)

ROOT=Path(__file__).resolve().parents[1]


def test_minimal_resolution_delivery_is_source_bound():
    members, derivations = builder.minimal_resolution_materials()
    value=json.loads(members['EVIDENCE/INITIAL_MEAN_READOUT.json'])
    assert value['new_native_futures']==4096
    assert [p['decision'] for p in value['primary']]==['positive','unresolved','positive','unresolved']
    original=gzip.decompress(members['EVIDENCE/INITIAL_MEAN_ORIGINAL.json.gz'])
    assert hashlib.sha256(original).hexdigest()==value['original_readout_sha256']
    assert json.loads(members['EVIDENCE/GENOME_RESPONSE_READOUT.json'])['updates']==64000
    assert json.loads(members['EVIDENCE/DURATION_READOUT.json'])['kernels']==96
    assert len(derivations)==4


def test_minimal_resolution_delivery_rejects_changed_mean_results(tmp_path, monkeypatch):
    import shutil
    copied=tmp_path/'results'
    receipt='minimal_resolution_delivery_20261013.json'
    names=json.loads((builder.MINIMAL_RESULTS/receipt).read_bytes())['sha256']
    for name in [receipt,*names]:
        p=copied/name;p.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(builder.MINIMAL_RESULTS/name,p)
    p=copied/'initial_assurance_mean_20261013/readout.json'
    p.write_bytes(p.read_bytes()+b' ')
    monkeypatch.setattr(builder,'MINIMAL_RESULTS',copied)
    with pytest.raises(ValueError,match='minimal resolution source hash mismatch'):
        builder.minimal_resolution_materials()


def test_minimal_resolution_explicit_text_newline_derivation_is_portable(tmp_path, monkeypatch):
    copied=tmp_path/'portable';copied.mkdir()
    receipt='minimal_resolution_delivery_20261013.json'
    names=json.loads((builder.MINIMAL_RESULTS/receipt).read_bytes())['sha256']
    for name in [receipt,*names]:
        p=copied/name;p.parent.mkdir(parents=True,exist_ok=True)
        raw=(builder.MINIMAL_RESULTS/name).read_bytes()
        p.write_bytes(raw if name.endswith('.gz') else raw.replace(b'\r\n',b'\n'))
    expected,_=builder.minimal_resolution_materials()
    monkeypatch.setattr(builder,'MINIMAL_RESULTS',copied)
    actual,_=builder.minimal_resolution_materials()
    assert actual==expected


def test_mechanism_delivery_is_source_bound_and_reports_predeclared_interaction():
    members, derivations = builder.mechanism_materials()
    value = json.loads(members["EVIDENCE/MECHANISM_READOUT.json"])
    assert value["status"] == "complete_archive_verified"
    assert value["verified_cases"] == 20480
    assert [r["factorial_interaction"] for r in value["partition"]] == [-0.0068359375, 0.0048828125]
    assert [r["decision"] for r in value["primary"]] == ["attenuation", "unresolved", "attenuation", "unresolved"]
    assert value["independent_arithmetic"]["npz_cases"] == 20480
    assert value["scope"]["lifelong_expression_policy"] is True
    assert value["scope"]["low_challenge_terminal_floor"] is True
    assert "EVIDENCE/MECHANISM_READOUT.json" in derivations


def test_mechanism_delivery_rejects_source_drift(tmp_path, monkeypatch):
    import shutil
    copied=tmp_path/"mechanism"
    shutil.copytree(builder.MECHANISM_DATA,copied)
    p=copied/"readout.json"
    p.write_bytes(p.read_bytes()+b" ")
    monkeypatch.setattr(builder,"MECHANISM_DATA",copied)
    with pytest.raises(ValueError, match="mechanism source hash mismatch"):
        builder.mechanism_materials()


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
    assert "[source file in blinded archive]" not in paper


def test_unmapped_internal_reference_requires_explicit_package_routing(monkeypatch):
    source=builder.render_manuscript()
    source=source.replace("# Results", "# Results\n\nSee `docs/unpackaged_evidence.md`.",1)
    monkeypatch.setattr(builder,"render_manuscript",lambda:source)
    with pytest.raises(ValueError,match="unmapped internal reference"):
        blind_paper()


def fake_pdfs(tmp_path):
    out={}
    for i,label in enumerate(PDF_FIGURES,1):
        p=tmp_path/label
        writer=PdfWriter()
        writer.add_blank_page(width=300,height=200)
        writer.write(p)
        out[label]=p
    return out


def supplementary_figures(tmp_path):
    p=tmp_path/"SupplementaryFigureS1.pdf"
    writer=PdfWriter()
    writer.add_blank_page(width=300,height=200)
    writer.write(p)
    return {
        "SupplementaryFigureS1.pdf":p,
        "SupplementaryFigureS2.svg":ROOT/"figures/chapter2_functional_loss_tempo_20261011/crossing_by100.svg",
    }


def test_review_package_has_four_main_and_three_supplementary_figures(tmp_path):
    out=tmp_path/"EL_ONE_PAPER_REVIEW.zip"
    receipt=build(out,figures=fake_pdfs(tmp_path),
                  supplementary_figures=supplementary_figures(tmp_path))
    assert receipt["n_figures"]==4
    assert receipt["n_supplementary_figures"]==3
    assert receipt["submitted"] is False
    assert receipt["doi_deposit_complete"] is False
    with zipfile.ZipFile(out) as z:
        names=z.namelist()
        assert names.count("MANUSCRIPT.md")==1
        assert names.count("SUPPORTING_INFORMATION.md")==1
        assert [x for x in names if x.startswith("Figure")]==[
           "Figure1.pdf","Figure2.pdf","Figure3.pdf","Figure4.svg"]
        assert "Figure4.pdf" not in names
        assert sorted(x for x in names if x.startswith("SupplementaryFigure"))==[
            "SupplementaryFigureS1.pdf","SupplementaryFigureS2.svg","SupplementaryFigureS3.pdf"]
        assert "ATOM_FULL_TABLES.csv" in names
        assert "TEMPO_FULL_TABLES.md" in names
        assert sorted(x for x in names if x.startswith("EVIDENCE/"))==[
           "EVIDENCE/ATOM_ABM_COMPARISON.json",
           "EVIDENCE/CAPACITY_RESULTS.json",
           "EVIDENCE/DURATION_READOUT.json",
           "EVIDENCE/EVOLUTION_DESIGN.json",
           "EVIDENCE/EVOLUTION_RESULTS.json",
           "EVIDENCE/GENOME_RESPONSE_READOUT.json",
           "EVIDENCE/INITIAL_MEAN_ORIGINAL.json.gz",
           "EVIDENCE/INITIAL_MEAN_READOUT.json",
           "EVIDENCE/MECHANISM_DESIGN.md",
           "EVIDENCE/MECHANISM_ORIGINAL.json.gz",
           "EVIDENCE/MECHANISM_READOUT.json",
           "EVIDENCE/RESOLUTION_DESIGN.md",
           "EVIDENCE/RESOLUTION_READOUT.json",
           "EVIDENCE/TEMPO_AUDIT_SUMMARY.json",
           "EVIDENCE/TEMPO_DESIGN.json",
           "EVIDENCE/TEMPO_RESULTS.json.gz",
        ]
        m=json.loads(z.read("MANIFEST.json"))
        assert m["source_active_manuscript"].startswith("CHAPTER2_UNIFIED")
        assert m["doi_deposit_complete"] is False
        assert m["n_figures"]==4
        assert m["n_supplementary_figures"]==3
        assert len(m["members"])==27
        for name,record in m["members"].items():
            raw=z.read(name)
            assert record=={"size":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
        paper=z.read("MANUSCRIPT.md").decode("utf-8")
        assert paper==blind_paper()
        assert "0.007746" in paper
        assert "(Figure4.svg)" in paper and "Figure4.svg" in names
        assert "See Supporting Information S3 and Figure 4." in paper
        assert "## S3." in z.read("SUPPORTING_INFORMATION.md").decode()
        assert "[source file in blinded archive]" not in paper
        counts={
            "abstract":len(paper.split("## Abstract",1)[1].split("## Keywords",1)[0].split()),
            "main_text":len(paper.split("# Introduction",1)[1].split("# Primary figure assembly and captions",1)[0].split()),
        }
        assert m["word_counts"]==receipt["word_counts"]==counts
    saved=json.loads(out.with_suffix(".receipt.json").read_text())
    assert saved["manuscript_sha256"]==receipt["manuscript_sha256"]
    assert len(saved["build_source"]["commit"])==40
    assert len(saved["build_source"]["tree"])==40


def test_atom_supplement_preserves_all_contexts_and_relocates_si_links(tmp_path):
    out=tmp_path/"atom_review.zip"
    receipt=build(out,figures=fake_pdfs(tmp_path),supplementary_figures=supplementary_figures(tmp_path))
    source=ROOT/"data/results/atom_cell_completed_20261011/matched_comparison.json"
    with zipfile.ZipFile(out) as z:
        delivered=json.loads(z.read("EVIDENCE/ATOM_ABM_COMPARISON.json"))
        assert delivered["artifact_role"]=="derived_anonymous_comparison_not_original_readout"
        assert delivered["original_comparison_sha256"]==hashlib.sha256(source.read_bytes()).hexdigest()
        assert delivered["rows"]==json.loads(source.read_text(encoding="utf-8"))["rows"]
        assert delivered["scope"]["abm_archives"]==320
        assert delivered["scope"]["event_checks"]==990
        assert delivered["scope"]["checkpoint_checks"]==40
        assert delivered["scope"]["new_raw_genome_reconstruction"] is False
        assert len(delivered["admission_contexts"])==10
        assert z.read("ATOM_FULL_TABLES.csv")==(
            ROOT/"docs/atom_comparison_20261011/ATOM_ABM_COMPARISON_TABLE_20261011.csv").read_bytes()
        si=z.read("SUPPORTING_INFORMATION.md").decode("utf-8")
        assert "(ATOM_FULL_TABLES.csv)" in si
        assert "(SupplementaryFigureS3.pdf)" in si
        assert "atom_comparison_20261011/" not in si
        assert "data/results/atom_cell_completed_20261011/" not in si
    assert "EVIDENCE/ATOM_ABM_COMPARISON.json" in receipt["source_derivations"]


def test_atom_evidence_drift_refuses_delivery(tmp_path,monkeypatch):
    import scripts.build_chapter2_unified_el_submission_bundle as builder
    import shutil
    source=ROOT/"data/results/atom_cell_completed_20261011"
    changed=tmp_path/"atom_data"
    shutil.copytree(source,changed)
    p=changed/"matched_comparison.json"
    value=json.loads(p.read_text(encoding="utf-8"))
    value["rows"][0]["events"][0]["abm_counts"]["assurance_first"]=999
    p.write_text(json.dumps(value),encoding="utf-8")
    monkeypatch.setattr(builder,"ATOM_DATA",changed)
    with pytest.raises(ValueError,match="atom source hash mismatch"):
        build(tmp_path/"bad_atom.zip",figures=fake_pdfs(tmp_path),supplementary_figures=supplementary_figures(tmp_path))


def test_resolution_scope_intervals_and_design_are_in_reviewer_package(tmp_path):
    out=tmp_path/"four_question_review.zip"
    build(out,figures=fake_pdfs(tmp_path),supplementary_figures=supplementary_figures(tmp_path))
    data=ROOT/"data/results/four_question_resolution_20261011"
    with zipfile.ZipFile(out) as z:
        delivered=json.loads(z.read("EVIDENCE/RESOLUTION_READOUT.json"))
        assert delivered["boundary"]==json.loads((data/"boundary_readout.json").read_text(encoding="utf-8"))
        assert delivered["history"]==json.loads((data/"history_readout.json").read_text(encoding="utf-8"))
        assert delivered["scope"]["source_closed_cohort_counts"]=={"boundary":6144,"preparation":3072,"future":6144}
        assert delivered["scope"]["new_inference_computed_for_delivery"] is False
        assert delivered["history"]["first_stage"]["intended_shift"] is True
        assert [a["both_events"] for a in delivered["achieved_state_diagnostic"]["arms"][:2]]==[42,43]
        for context in delivered["history"]["contexts"]:
            for metric in context["primary"].values():
                assert metric["bootstrap_interval"][0]>0
                assert metric["hoeffding_interval"][0]<0<metric["hoeffding_interval"][1]
        assert z.read("EVIDENCE/RESOLUTION_DESIGN.md")==(
            ROOT/"docs/four_question_resolution_20261011/DESIGN.md").read_bytes()
        si=z.read("SUPPORTING_INFORMATION.md").decode("utf-8")
        assert "(EVIDENCE/RESOLUTION_DESIGN.md)" in si
        assert "data/results/four_question_resolution_20261011/" not in si
        assert "[0.0023192749,0.0326467896]" in si


def test_resolution_readout_drift_refuses_delivery(tmp_path,monkeypatch):
    import scripts.build_chapter2_unified_el_submission_bundle as builder
    import shutil
    copied=tmp_path/"resolution_data"
    shutil.copytree(ROOT/"data/results/four_question_resolution_20261011",copied)
    p=copied/"history_readout.json"
    value=json.loads(p.read_text(encoding="utf-8"));value["first_stage"]["order_score_difference"]=999
    p.write_text(json.dumps(value),encoding="utf-8")
    monkeypatch.setattr(builder,"RESOLUTION_DATA",copied)
    with pytest.raises(ValueError,match="resolution source hash mismatch"):
        build(tmp_path/"bad_resolution.zip",figures=fake_pdfs(tmp_path),supplementary_figures=supplementary_figures(tmp_path))


def test_package_refuses_missing_unrendered_figures(tmp_path):
    figures=fake_pdfs(tmp_path)
    supplement=supplementary_figures(tmp_path)
    figures["Figure2.pdf"]=tmp_path/"no-such-figure.pdf"
    with pytest.raises(FileNotFoundError):
        build(tmp_path/"bad.zip",figures=figures,supplementary_figures=supplement)
    figures=fake_pdfs(tmp_path)
    figures["Figure2.pdf"].write_bytes(b"garbage")
    with pytest.raises(ValueError,match="invalid PDF"):
        build(tmp_path/"bad2.zip",figures=figures,supplementary_figures=supplement)
    figures=fake_pdfs(tmp_path)
    figures["Figure2.pdf"].write_bytes(b"%PDF-1.4\n"+b"x"*1200+b"\n%%EOF\n")
    with pytest.raises(ValueError,match="invalid PDF"):
        build(tmp_path/"header-only.zip",figures=figures,supplementary_figures=supplement)
    figures=fake_pdfs(tmp_path)
    supplement["SupplementaryFigureS1.pdf"]=tmp_path/"missing-supplement.pdf"
    with pytest.raises(FileNotFoundError):
        build(tmp_path/"missing-supplement.zip",figures=figures,supplementary_figures=supplement)
    with pytest.raises(ValueError,match="supplementary figures"):
        build(tmp_path/"no-supplement.zip",figures=figures,supplementary_figures={})
    with pytest.raises(ValueError,match="exactly Figure1"):
        build(tmp_path/"bad3.zip",figures={"Figure1.pdf":tmp_path/"x"})


def test_tempo_archive_preserves_results_and_every_table_row_without_identifiers(tmp_path):
    out=tmp_path/"review.zip"
    build(out,figures=fake_pdfs(tmp_path),
          supplementary_figures=supplementary_figures(tmp_path))
    with zipfile.ZipFile(out) as z:
        raw=z.read("EVIDENCE/TEMPO_RESULTS.json.gz")
        assert raw==(ROOT/"data/results/chapter2_sequence_abrupt_gradual_functional_loss_20261011.json.gz").read_bytes()
        official=json.loads(gzip.decompress(raw))
        assert official["n_independent_synthetic_visitor_profiles"]==16
        assert official["total_verified_trajectory_cases"]==1024
        derived=z.read("TEMPO_FULL_TABLES.md").decode()
        original=(ROOT/"docs/CHAPTER2_SEQUENCE_ABRUPT_GRADUAL_FULL_TABLES_20261011.md").read_text()
        rows=lambda text:[line for line in text.splitlines() if line.startswith("|")]
        assert rows(derived)==rows(original)
        assert "(EVIDENCE/TEMPO_RESULTS.json.gz)" in derived
        audit=json.loads(z.read("EVIDENCE/TEMPO_AUDIT_SUMMARY.json"))
        assert audit["artifact_role"]=="derived_anonymous_audit_summary_not_original_audit"
        assert audit["audit_scope_origin"]=="original event/order/occupancy audit"
        assert audit["censuses_checked"]==410624
        assert audit["setting_outcome_comparisons"]==128
        assert audit["compared_scalar_values"]==640
        assert audit["verification_scope"]["independently_recomputed_secondary_fields"]==0
        assert audit["verification_scope"]["official_secondary_fields_per_setting"]==156
        assert len(audit["setting_results"])==8
        for name in z.namelist():
            if name.endswith(".pdf"):
                continue
            content=z.read(name)
            text=(gzip.decompress(content) if name.endswith(".gz") else content).decode().lower()
            assert not any(token in text for token in ("zuizui0223","github.com","/workspace/","/home/","/root/")),name
    receipt=json.loads(out.with_suffix(".receipt.json").read_text())
    mapping=receipt["source_derivations"]["TEMPO_FULL_TABLES.md"]
    assert mapping["original_path"].endswith("CHAPTER2_SEQUENCE_ABRUPT_GRADUAL_FULL_TABLES_20261011.md")
    assert mapping["original_sha256"]==hashlib.sha256(original.encode()).hexdigest()


def test_same_verified_inputs_produce_identical_archive_bytes(tmp_path):
    figures=fake_pdfs(tmp_path)
    supplement=supplementary_figures(tmp_path)
    first=tmp_path/"first.zip"
    second=tmp_path/"second.zip"
    build(first,figures=figures,supplementary_figures=supplement)
    build(second,figures=figures,supplementary_figures=supplement)
    assert first.read_bytes()==second.read_bytes()


def test_tempo_source_hash_mismatch_prevents_delivery(tmp_path,monkeypatch):
    original=builder.TEMPO_ADMISSION
    admission=json.loads(original.read_text())
    admission["complete_readout"]["gzip_sha256"]="0"*64
    changed=tmp_path/"invalid-admission.json"
    changed.write_text(json.dumps(admission))
    monkeypatch.setattr(builder,"TEMPO_ADMISSION",changed)
    out=tmp_path/"must-not-exist.zip"
    with pytest.raises(ValueError,match="source hash mismatch"):
        build(out,figures=fake_pdfs(tmp_path),
              supplementary_figures=supplementary_figures(tmp_path))
    assert not out.exists()


def test_evidence_receipts_are_identified_and_not_pooled():
    assert len(FROZEN_RESULTS)==3
    route=json.loads((ROOT/"data/design/chapter2_one_paper_route_20261010.json").read_text())
    assert route["active_manuscript_count"]==1
    assert route["review_package_builder"]=="scripts/build_chapter2_unified_el_submission_bundle.py"
    assert route["review_package_expected_figures"]==[
        "Figure1.pdf","Figure2.pdf","Figure3.pdf","Figure4.svg"]
    assert route["review_package_expected_supplementary_figures"]==[
        "SupplementaryFigureS1.pdf","SupplementaryFigureS2.svg","SupplementaryFigureS3.pdf"]
    supplement=route["evidence_contract"]["supplementary_tempo"]
    assert supplement["independent_synthetic_profiles"]==16
    assert supplement["pooled_with_primary_studies"] is False
    source=(ROOT/route["active_manuscript"]).read_text()
    main_words=len(source.split("# Introduction",1)[1].split("# Primary figure assembly and captions",1)[0].split())
    abstract_words=len(source.split("## Abstract",1)[1].split("## Keywords",1)[0].split())
    fit=route["journal_fit"]
    assert fit["current_integrated_main_words"]==fit["current_main_text_words"]==main_words
    assert fit["current_integrated_abstract_words"]==fit["current_abstract_words"]==abstract_words
    assert "historical only" in route["legacy_process_builder"]
    evo=json.loads((ROOT/FROZEN_RESULTS["EVOLUTION_RESULTS.json"]).read_text())
    assert evo["adjudication"]["status"]=="all_four_confirmed"
    assert evo["independent_visitor_histories"]==64
    assert all(x["passes_frozen_rule"] for x in evo["settings"])
    cap=json.loads((ROOT/FROZEN_RESULTS["CAPACITY_RESULTS.json"]).read_text())
    assert cap["primary_verdict"]=="supported_controlled_demographic_K_moderation_at_fixed_B48"
