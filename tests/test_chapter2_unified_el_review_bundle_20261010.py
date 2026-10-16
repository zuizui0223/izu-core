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
    assert len(derivations)==10
    parent=json.loads(members['EVIDENCE/FUTURE_PARENT_READOUT.json'])
    assert parent['status']=='ACTUAL_RAW_BIRTH_AND_FOUR_DECISIONS_INDEPENDENTLY_VERIFIED'
    assert parent['cases']==4096 and parent['updates']==819200
    assert parent['independent']['raw_replay_checks']==9031680
    assert parent['independent']['producer_imports'] is False
    assert len(parent['primary'])==4
    assert all(p['decision']=='unresolved' for p in parent['primary'])
    assert parent['occupied_counts'][1][:2]==[[864,863],[790,757]]
    ecological=json.loads(members['EVIDENCE/ECOLOGICAL_ORDER_READOUT.json'])
    assert ecological['cases']==2304 and ecological['updates']==460800
    assert len(ecological['cells'])==18 and ecological['supported_supply_pairs']==[]
    assert ecological['supported_composition_pairs']==[]
    assert all(lo<=0<=hi for lo,hi in [c['simultaneous_interval'] for c in ecological['cells']])
    assert json.loads(members['EVIDENCE/OPERATOR_GAP_READOUT.json'])['updates']==64000
    intake=json.loads(members['EVIDENCE/DISCOVERY_ARCHIVE_INTAKE.json'])
    assert intake['verification']['archive_identity_verified']
    assert intake['counts']['discovery_cases_verified']==2048
    assert intake['verification']['original_discovery_full_replay_completed'] is False


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


def test_minimal_resolution_rejects_pending_parent_verification_even_with_matching_hash(tmp_path, monkeypatch):
    import shutil
    copied=tmp_path/'results'
    receipt='minimal_resolution_delivery_20261013.json'
    value=json.loads((builder.MINIMAL_RESULTS/receipt).read_bytes())
    for name in [receipt,*value['sha256']]:
        p=copied/name;p.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(builder.MINIMAL_RESULTS/name,p)
    name='future_parent_selection_readout_20261013.json'
    p=copied/name;parent=json.loads(p.read_bytes())
    parent['independent']['status']='PENDING'
    raw=(json.dumps(parent,indent=2)+'\n').encode('utf-8');p.write_bytes(raw)
    digest=hashlib.sha256(raw).hexdigest()
    value['sha256'][name]=digest;value['source_raw_sha256'][name]=[digest]
    (copied/receipt).write_text(json.dumps(value),encoding='utf-8')
    monkeypatch.setattr(builder,'MINIMAL_RESULTS',copied)
    with pytest.raises(ValueError,match='future parent independent admission differs'):
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


def test_restoration_is_portable_and_keeps_independently_verified_unresolved_decision():
    members,_=builder.minimal_resolution_materials()
    value=json.loads(members['EVIDENCE/INVESTMENT_VARIATION_READOUT.json'])
    assert value['histories']==64 and value['triggers']==61 and value['no_trigger']==3
    assert value['primary']['decision']=='unresolved'
    assert value['primary']['ci95'][0]<0<value['primary']['ci95'][1]
    assert value['primary']['block_estimates']['causal_main']>0
    assert value['primary']['block_estimates']['causal_confirmation']<0
    assert value['independent_state_parent_checks']==123880
    assert len(value['cases'])==64
    assert builder.sha(members['EVIDENCE/INVESTMENT_VARIATION_PROTOCOL.md'])==value['protocol_sha256']
    accounting=value['pathwise_accounting']
    assert accounting['status']=='INDEPENDENT_ALL7740_RESTORED_PATHWISE_TERMS_MATCH'
    assert accounting['updates']==7740 and accounting['new_histories']==0
    assert all(v['selection']<0 for v in accounting['blocks'].values())
    assert accounting['blocks']['causal_confirmation']['observed_change']>0


@pytest.mark.parametrize('field',['status','pathwise_accounting.status'])
def test_restoration_rejects_pending_independent_status_with_updated_byte_receipt(tmp_path,monkeypatch,field):
    import shutil
    root=tmp_path/'results';receipt='minimal_resolution_delivery_20261013.json'
    value=json.loads((builder.MINIMAL_RESULTS/receipt).read_bytes())
    for name in [receipt,*value['sha256']]:
        p=root/name;p.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(builder.MINIMAL_RESULTS/name,p)
    name='investment_variation_restoration_readout_20261013.json';p=root/name
    assert p.exists(),'restoration readout missing from scientific evidence inventory'
    result=json.loads(p.read_bytes())
    if field=='status':result['status']='PENDING'
    else:result['pathwise_accounting']['status']='PENDING'
    raw=(json.dumps(result,indent=2)+'\n').encode();p.write_bytes(raw)
    value['sha256'][name]=builder.sha(raw);value['source_raw_sha256'][name]=[builder.sha(raw)]
    (root/receipt).write_text(json.dumps(value),encoding='utf-8')
    monkeypatch.setattr(builder,'MINIMAL_RESULTS',root)
    with pytest.raises(ValueError,match='investment variation independent admission differs'):
        builder.minimal_resolution_materials()


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
    assert paper.startswith("# Selection, sequence and finite realization of floral evolution")
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
    p3=tmp_path/"SupplementaryFigureS3.pdf"
    writer3=PdfWriter()
    writer3.add_blank_page(width=300,height=200)
    writer3.write(p3)
    return {
        "SupplementaryFigureS1.pdf":p,
        "SupplementaryFigureS2.svg":ROOT/"figures/chapter2_functional_loss_tempo_20261011/crossing_by100.svg",
        "SupplementaryFigureS3.pdf":p3,
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
           "EVIDENCE/ASSURANCE_PARENT_ALL4096_INDEPENDENT_ADMISSION_V2.json",
           "EVIDENCE/ASSURANCE_PARENT_ANALYSIS_SOURCE.py",
           "EVIDENCE/ASSURANCE_PARENT_DOMAIN_COLLECTOR_SOURCE.py",
           "EVIDENCE/ASSURANCE_PARENT_DOMAIN_CORRECTION.md",
           "EVIDENCE/ASSURANCE_PARENT_EXECUTION_BINDINGS.json",
           "EVIDENCE/ASSURANCE_PARENT_INDEPENDENT_ARITHMETIC.json",
           "EVIDENCE/ASSURANCE_PARENT_INDEPENDENT_ARITHMETIC_SOURCE.py",
           "EVIDENCE/ASSURANCE_PARENT_INDEPENDENT_READER_SOURCE.py",
           "EVIDENCE/ASSURANCE_PARENT_NATIVE8_ADMISSION.json",
           "EVIDENCE/ASSURANCE_PARENT_OUTCOMES.npz",
           "EVIDENCE/ASSURANCE_PARENT_PROTOCOL.md",
           "EVIDENCE/ASSURANCE_PARENT_PUBLIC_ADMISSION.json",
           "EVIDENCE/ASSURANCE_PARENT_READOUT.json",
           "EVIDENCE/ASSURANCE_PARENT_REFERENCE_ADMISSION.json",
           "EVIDENCE/ASSURANCE_PARENT_RUN_COMPLETION.json",
           "EVIDENCE/ATOM_ABM_COMPARISON.json",
           "EVIDENCE/CAPACITY_RESULTS.json",
           "EVIDENCE/DIRECTIONAL_ACCESS_ARRAYS.npz",
           "EVIDENCE/DIRECTIONAL_ACCESS_CASES.csv",
           "EVIDENCE/DIRECTIONAL_ACCESS_FROZEN_SOURCES.json",
           "EVIDENCE/DIRECTIONAL_ACCESS_INDEPENDENT_REVIEW.json",
           "EVIDENCE/DIRECTIONAL_ACCESS_INDEPENDENT_SOURCE.py",
           "EVIDENCE/DIRECTIONAL_ACCESS_ORIGINAL_COMPACT.json",
           "EVIDENCE/DIRECTIONAL_ACCESS_POPULATION_SOURCE.py",
           "EVIDENCE/DIRECTIONAL_ACCESS_PROTOCOL.md",
           "EVIDENCE/DIRECTIONAL_ACCESS_README.md",
           "EVIDENCE/DIRECTIONAL_ACCESS_READOUT.json",
           "EVIDENCE/DIRECTIONAL_ACCESS_SOURCE.py",
           "EVIDENCE/DIRECTIONAL_ACCESS_TEST_SOURCE.py",
           "EVIDENCE/DISCOVERY_ARCHIVE_INTAKE.json",
           "EVIDENCE/DURATION_READOUT.json",
           "EVIDENCE/ECOLOGICAL_ORDER_READOUT.json",
           "EVIDENCE/EVOLUTION_DESIGN.json",
            "EVIDENCE/EVOLUTION_RESULTS.json",
            "EVIDENCE/FIRST_MEIOSIS_FROZEN_SOURCE_PINS.json",
           "EVIDENCE/FIRST_MEIOSIS_INDEPENDENT_PROTOCOL.md",
           "EVIDENCE/FIRST_MEIOSIS_INDEPENDENT_RAW_REVIEW.json",
           "EVIDENCE/FIRST_MEIOSIS_INDEPENDENT_SOURCE.py",
           "EVIDENCE/FIRST_MEIOSIS_ORIGINAL_CASES.csv",
           "EVIDENCE/FIRST_MEIOSIS_ORIGINAL_RESULT.json",
           "EVIDENCE/FIRST_MEIOSIS_V1_SERIALIZATION_STOP.md",
           "EVIDENCE/FUTURE_PARENT_READOUT.json",
           "EVIDENCE/GENETIC_ACCESS_ALL_SIX_ORIGINAL_SOURCE_READBACK.json",
           "EVIDENCE/GENETIC_ACCESS_EXTERNAL_SOURCE_AND_MIRROR_RECEIPT.json",
           "EVIDENCE/GENETIC_ACCESS_FROZEN_EXPLORATORY_READOUT.json",
           "EVIDENCE/GENETIC_ACCESS_INDEPENDENT_DEMOGRAPHY_CEILING_REVIEW.json",
           "EVIDENCE/GENETIC_ACCESS_INDEPENDENT_EXPLORATORY_ARITHMETIC_REVIEW.json",
           "EVIDENCE/GENETIC_ACCESS_confirmation_c0_independently_verified.json",
           "EVIDENCE/GENETIC_ACCESS_confirmation_c3_independently_verified.json",
           "EVIDENCE/GENETIC_ACCESS_confirmation_c4_independently_verified.json",
           "EVIDENCE/GENETIC_ACCESS_main_c0_independently_verified.json",
           "EVIDENCE/GENETIC_ACCESS_main_c3_independently_verified.json",
           "EVIDENCE/GENETIC_ACCESS_main_c4_independently_verified.json",
           "EVIDENCE/GENETIC_ACCESS_verify_exploratory_arithmetic_independent.py",
           "EVIDENCE/GENOME_RESPONSE_READOUT.json",
           "EVIDENCE/INITIAL_CLOCK_IDENTIFIABILITY.json",
           "EVIDENCE/INITIAL_CLOCK_INDEPENDENT_REVIEW.json",
           "EVIDENCE/INITIAL_CLOCK_RAW.json",
           "EVIDENCE/INITIAL_MEAN_ORIGINAL.json.gz",
           "EVIDENCE/INITIAL_MEAN_READOUT.json",
           "EVIDENCE/INVESTMENT_VARIATION_PROTOCOL.md",
           "EVIDENCE/INVESTMENT_VARIATION_READOUT.json",
           "EVIDENCE/KERNEL_CHANNEL_ARRAYS_MANIFEST.json",
           "EVIDENCE/KERNEL_CHANNEL_INDEPENDENT_REVIEW.json",
           "EVIDENCE/KERNEL_CHANNEL_INDEPENDENT_SOURCE.py",
           "EVIDENCE/KERNEL_CHANNEL_PROTOCOL.md",
           "EVIDENCE/KERNEL_CHANNEL_READOUT.json",
           "EVIDENCE/KERNEL_CHANNEL_SOURCE.py",
           "EVIDENCE/KERNEL_CHANNEL_V2_BINDINGS.json",
           "EVIDENCE/KERNEL_CHANNEL_V2_TECHNICAL_STOP.json",
           "EVIDENCE/KERNEL_CHANNEL_V3_BINDINGS.json",
           "EVIDENCE/KERNEL_CHANNEL_V3_CORRECTION.md",
           "EVIDENCE/KERNEL_EXPRESSION_ARRAYS_MANIFEST.json",
           "EVIDENCE/KERNEL_EXPRESSION_INDEPENDENT_REVIEW.json",
           "EVIDENCE/KERNEL_EXPRESSION_INDEPENDENT_SOURCE.py",
           "EVIDENCE/KERNEL_EXPRESSION_PROTOCOL.md",
           "EVIDENCE/KERNEL_EXPRESSION_READOUT.json",
           "EVIDENCE/KERNEL_EXPRESSION_SOURCE.py",
           "EVIDENCE/LOW_ALLELE_LOSS_CASES.csv",
           "EVIDENCE/LOW_ALLELE_LOSS_INDEPENDENT_REVIEW.json",
           "EVIDENCE/LOW_ALLELE_LOSS_PROTOCOL.md",
           "EVIDENCE/LOW_ALLELE_LOSS_READOUT.json",
           "EVIDENCE/LOW_ALLELE_LOSS_SCOPE.md",
           "EVIDENCE/LOW_ALLELE_LOSS_SOURCE_READBACK_NOTE.md",
           "EVIDENCE/MECHANISM_DESIGN.md",
           "EVIDENCE/MECHANISM_ORIGINAL.json.gz",
           "EVIDENCE/MECHANISM_READOUT.json",
           "EVIDENCE/NATURAL_ORDER_INDEPENDENT_REVIEW.json",
           "EVIDENCE/NATURAL_ORDER_MEAN_INDEPENDENT_ADMISSION.json",
           "EVIDENCE/NATURAL_ORDER_MEAN_PUBLIC_READBACK.json",
           "EVIDENCE/NATURAL_ORDER_MEAN_READOUT.json.gz",
           "EVIDENCE/NATURAL_ORDER_PUBLIC_READBACK.json",
           "EVIDENCE/NATURAL_ORDER_SUMMARY.json",
           "EVIDENCE/OPERATOR_GAP_READOUT.json",
           "EVIDENCE/PR490_ORIGINAL_AUDITOR.py",
           "EVIDENCE/PR490_ORIGINAL_DIRECT_ADMISSION.json",
           "EVIDENCE/PR490_ORIGINAL_INDEPENDENT_REVIEW.json",
           "EVIDENCE/PR490_ORIGINAL_NUMERICAL_AUDITOR.py",
           "EVIDENCE/Q2_S29_FOUR_SIGN_MENDELIAN_F1.json",
           "EVIDENCE/Q2_S29_ORIGINAL_I_M0_M6_F1.json",
           "EVIDENCE/Q2_S29_ORIGINAL_T0_TYPED_SOURCE.json",
           "EVIDENCE/Q2_S29_STATIC_FOCAL_W.json",
           "EVIDENCE/Q3_CONDITIONAL_EXECUTION.json",
           "EVIDENCE/Q3_CONDITIONAL_EXTERNAL_READBACK.json",
           "EVIDENCE/Q3_CONDITIONAL_IDENTIFICATION_REVIEW.md",
           "EVIDENCE/Q3_CONDITIONAL_INDEPENDENT_READOUT.json",
           "EVIDENCE/Q3_CONDITIONAL_INDEPENDENT_REPLAY.json",
           "EVIDENCE/Q3_CONDITIONAL_INDEPENDENT_SAVED_ARRAYS.json",
           "EVIDENCE/Q3_CONDITIONAL_INDEPENDENT_VERIFIER_SOURCE.py",
           "EVIDENCE/Q3_CONDITIONAL_PROTOCOL.md",
           "EVIDENCE/Q3_CONDITIONAL_PUBLICATION_RECEIPT.json",
           "EVIDENCE/Q3_CONDITIONAL_PUBLIC_ADMISSION.json",
           "EVIDENCE/Q3_CONDITIONAL_READOUT.json",
           "EVIDENCE/Q3_CONDITIONAL_RESOURCES.json",
           "EVIDENCE/Q3_CONDITIONAL_RESULTS.md",
           "EVIDENCE/Q3_EVENT_FRESH_RAW_REVIEW.json",
           "EVIDENCE/Q3_EVENT_PROVENANCE.json",
           "EVIDENCE/Q3_EVENT_PUBLIC_ADMISSION.json",
           "EVIDENCE/Q3_EVENT_PUBLIC_READBACK.json",
           "EVIDENCE/Q3_EVENT_SUMMARY.json",
           "EVIDENCE/Q3_TRIANGLE_CAMPAIGN_MANIFEST.json",
           "EVIDENCE/Q3_TRIANGLE_INDEPENDENT_VERIFICATION.json",
           "EVIDENCE/Q3_TRIANGLE_READOUT.json",
           "EVIDENCE/Q4_32_DESIGN.json",
           "EVIDENCE/Q4_32_ORIGINAL_RUNNER.py",
           "EVIDENCE/Q4_32_REPLAY_RECEIPT.json",
           "EVIDENCE/Q4_32_RESULT.json",
           "EVIDENCE/RESOLUTION_DESIGN.md",
           "EVIDENCE/RESOLUTION_READOUT.json",
           "EVIDENCE/RESPONSE_ONSET_ALL_CASES.csv",
           "EVIDENCE/RESPONSE_ONSET_INDEPENDENT_REVIEW.json",
           "EVIDENCE/RESPONSE_ONSET_INDEPENDENT_SOURCE.py",
           "EVIDENCE/RESPONSE_ONSET_PROTOCOL.md",
           "EVIDENCE/RESPONSE_ONSET_READOUT.json",
           "EVIDENCE/RESPONSE_ONSET_SOURCE.py",
           "EVIDENCE/RESTORATION_ACCESS_AUDIT_SOURCE.py",
           "EVIDENCE/RESTORATION_ACCESS_CASES.csv",
           "EVIDENCE/RESTORATION_ACCESS_FRESH_INDEPENDENT.json",
           "EVIDENCE/RESTORATION_ACCESS_INDEPENDENT_SOURCE.py",
           "EVIDENCE/RESTORATION_ACCESS_PUBLIC_ADMISSION.json",
           "EVIDENCE/RESTORATION_ACCESS_READOUT.json",
           "EVIDENCE/RESTORATION_ACCESS_SOURCE_SCOPE.md",
           "EVIDENCE/TEMPO_AUDIT_SUMMARY.json",
           "EVIDENCE/TEMPO_DESIGN.json",
           "EVIDENCE/TEMPO_RESULTS.json.gz",
        ]
        m=json.loads(z.read("MANIFEST.json"))
        assert m["source_active_manuscript"].startswith("CHAPTER2_UNIFIED")
        assert m["doi_deposit_complete"] is False
        assert m["n_figures"]==4
        assert m["n_supplementary_figures"]==3
        assert len(m["members"])==156
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
    transformation = receipt["source_derivations"]["SUPPORTING_INFORMATION.md"]["transformation"]
    assert "original-mutation ten-context comparison to main Fig3" in transformation
    assert "finite-realization to Supplementary S3" in transformation
    assert "finite-realization to main Fig3" not in transformation


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
            if name.endswith('.npz'):
                builder.validate_member(name, content)
                continue
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


def test_initial_clock_materials_preserve_scope_and_remove_repo_routing():
    members, derivations = builder.initial_clock_materials()
    assert len(members) == len(derivations) == 3
    value = json.loads(members['EVIDENCE/INITIAL_CLOCK_RAW.json'])
    assert value['original_starts'] == 2304
    assert len(value['original_raw_t0_feature_rows']) == 18
    assert 'repo' not in value['execution']
    assert 'branch' not in value['execution']
    for name, raw in members.items():
        builder.validate_member(name, raw)


def test_initial_clock_materials_reject_changed_unverified_source(tmp_path, monkeypatch):
    root = tmp_path / 'data'; root.mkdir()
    for filename in ['chapter2_initial_clock_identifiability_20261013.json',
                     'chapter2_initial_clock_t0_raw_20261013.json',
                     'chapter2_initial_clock_independent_review_20261013.json']:
        (root / filename).write_bytes((builder.MINIMAL_RESULTS / filename).read_bytes())
    p = root / 'chapter2_initial_clock_t0_raw_20261013.json'
    value = json.loads(p.read_text()); value['original_starts'] = 2303
    p.write_text(json.dumps(value))
    monkeypatch.setattr(builder, 'MINIMAL_RESULTS', root)
    with pytest.raises(ValueError, match='initial clock source hash'):
        builder.initial_clock_materials()


def test_response_onset_evidence_keeps_all_starts_and_counterexample_scope():
    members, derivations = builder.response_onset_materials()
    assert len(members) == len(derivations) == 6
    value = json.loads(members['EVIDENCE/RESPONSE_ONSET_READOUT.json'])
    assert value['cases'] == 2304
    assert value['original_categories']['assurance_first'] == 335
    assert value['assurance_first_despite_earlier_I_point'] == 299
    assert value['assurance_first_despite_earlier_I_sustained'] == 216
    for name, raw in members.items(): builder.validate_member(name, raw)


def test_response_onset_materials_reject_changed_executed_source(tmp_path, monkeypatch):
    results = tmp_path / 'data/results/expected_response_onset_20261013'
    code = tmp_path / 'scripts/expected_response_onset_20261013'
    results.mkdir(parents=True); code.mkdir(parents=True)
    for name in ['READOUT.json', 'ALL_CASES.csv', 'INDEPENDENT_REVIEW.json']:
        (results / name).write_bytes((builder.MINIMAL_RESULTS / 'expected_response_onset_20261013' / name).read_bytes())
    for name in ['audit_response_onset.py', 'PROTOCOL.md', 'verify_response_onset_independent.py']:
        (code / name).write_bytes((builder.ROOT / 'scripts/expected_response_onset_20261013' / name).read_bytes())
    target = code / 'audit_response_onset.py'
    target.write_bytes(target.read_bytes() + b'\n# changed after execution\n')
    monkeypatch.setattr(builder, 'ROOT', tmp_path)
    monkeypatch.setattr(builder, 'MINIMAL_RESULTS', tmp_path / 'data/results')
    with pytest.raises(ValueError, match='response onset independent source admission'):
        builder.response_onset_materials()


def test_kernel_expression_materials_preserve_two_references_and_scope():
    members, derivations = builder.kernel_expression_materials()
    assert len(members) == len(derivations) == 6
    value = json.loads(members['EVIDENCE/KERNEL_EXPRESSION_READOUT.json'])
    assert value['pairs'] == 48 and value['original_reversals'] == 12
    assert len(value['comparisons']) == 48
    assert all(len(row['references']) == 2 for row in value['comparisons'])
    assert value['policy'].startswith('expressed investment')
    assert value['new_biological_histories'] == 0
    for name, raw in members.items():
        if not name.endswith('.npz'): builder.validate_member(name, raw)


def test_kernel_expression_materials_reject_changed_signed_terms(tmp_path, monkeypatch):
    data = tmp_path / 'data/results/kernel_expression_accounting_20261013'
    code = tmp_path / 'scripts/kernel_expression_accounting_20261013'
    data.mkdir(parents=True); code.mkdir(parents=True)
    for name in ['READOUT.json.gz', 'INDEPENDENT_REVIEW.json', 'ARRAYS_MANIFEST.json']:
        (data / name).write_bytes((builder.MINIMAL_RESULTS / 'kernel_expression_accounting_20261013' / name).read_bytes())
    (data / 'ALL_STATE_TIME_CONTRIBUTIONS.npz').write_bytes(b'changed signed terms')
    for name in ['audit_kernel_expression.py', 'PROTOCOL.md', 'verify_kernel_expression_independent.py']:
        (code / name).write_bytes((builder.ROOT / 'scripts/kernel_expression_accounting_20261013' / name).read_bytes())
    monkeypatch.setattr(builder, 'ROOT', tmp_path)
    monkeypatch.setattr(builder, 'MINIMAL_RESULTS', tmp_path / 'data/results')
    with pytest.raises(ValueError, match='kernel expression verified source admission'):
        builder.kernel_expression_materials()


def test_kernel_expression_materials_use_verified_companion_when_arrays_not_local(tmp_path, monkeypatch):
    data = tmp_path / 'data/results/kernel_expression_accounting_20261013'
    code = tmp_path / 'scripts/kernel_expression_accounting_20261013'
    data.mkdir(parents=True); code.mkdir(parents=True)
    for name in ['READOUT.json.gz', 'INDEPENDENT_REVIEW.json', 'ARRAYS_MANIFEST.json']:
        (data / name).write_bytes((builder.MINIMAL_RESULTS / 'kernel_expression_accounting_20261013' / name).read_bytes())
    for name in ['audit_kernel_expression.py', 'PROTOCOL.md', 'verify_kernel_expression_independent.py']:
        (code / name).write_bytes((builder.ROOT / 'scripts/kernel_expression_accounting_20261013' / name).read_bytes())
    monkeypatch.setattr(builder, 'ROOT', tmp_path)
    monkeypatch.setattr(builder, 'MINIMAL_RESULTS', tmp_path / 'data/results')
    members, _ = builder.kernel_expression_materials()
    value = json.loads(members['EVIDENCE/KERNEL_EXPRESSION_ARRAYS_MANIFEST.json'])
    assert value['bytes'] == 18547957
    assert value['sha256'] == '3a39c3d37dda4eba126e01ea83ea1ff667d7f99860471dc2e15e8114f13d748a'


def test_kernel_expression_materials_reject_changed_compressed_readout(tmp_path, monkeypatch):
    import gzip
    data = tmp_path / 'data/results/kernel_expression_accounting_20261013'
    data.mkdir(parents=True)
    original = builder.MINIMAL_RESULTS / 'kernel_expression_accounting_20261013'
    (data / 'INDEPENDENT_REVIEW.json').write_bytes((original / 'INDEPENDENT_REVIEW.json').read_bytes())
    (data / 'ARRAYS_MANIFEST.json').write_bytes((original / 'ARRAYS_MANIFEST.json').read_bytes())
    changed = json.loads(gzip.decompress((original / 'READOUT.json.gz').read_bytes()))
    changed['pairs'] = 47
    (data / 'READOUT.json.gz').write_bytes(gzip.compress(json.dumps(changed).encode(), mtime=0))
    monkeypatch.setattr(builder, 'MINIMAL_RESULTS', tmp_path / 'data/results')
    with pytest.raises(ValueError, match='kernel expression verified source admission'):
        builder.kernel_expression_materials()


def test_kernel_channels_preserve_all_conditions_and_original_reversals():
    members, derivations = builder.kernel_channel_materials()
    assert len(members) == len(derivations) == 10
    r = json.loads(members['EVIDENCE/KERNEL_CHANNEL_READOUT.json'])
    assert len(r['comparisons']) == 48
    assert sum(row['original_reversal'] for row in r['comparisons']) == 12
    assert all(row['duration']['recruitment_only'] < 0 for row in r['comparisons'])
    assert all(row['duration']['interaction'] > 0 for row in r['comparisons'])
    assert max(abs(row['duration']['genotype_only']) for row in r['comparisons']) < 1e-12
    for name, raw in members.items():
        builder.validate_member(name, raw)


def test_kernel_channels_reject_redirected_array_pointer(tmp_path, monkeypatch):
    import shutil
    src = builder.MINIMAL_RESULTS / 'kernel_channel_factorial_20261013'
    data = tmp_path / 'kernel_channel_factorial_20261013'
    shutil.copytree(src, data)
    p = data / 'ARRAYS_MANIFEST.json'
    value = json.loads(p.read_bytes()); value['companion_member'] = 'different.npz'
    p.write_text(json.dumps(value), encoding='utf-8')
    monkeypatch.setattr(builder, 'MINIMAL_RESULTS', tmp_path)
    with pytest.raises(ValueError, match='kernel channel verified evidence'):
        builder.kernel_channel_materials()


def test_s29_reviewer_archive_has_source_authenticated_anonymous_F1_and_W(tmp_path):
    from scripts.verify_chapter2_q2_s29_source_bridge_20261015 import (
        SOURCES, git_blob, verify,
    )
    assert verify()["native_focal_W_analytical_cells"]==36
    labels={
        "original":"EVIDENCE/Q2_S29_ORIGINAL_T0_TYPED_SOURCE.json",
        "f1":"EVIDENCE/Q2_S29_ORIGINAL_I_M0_M6_F1.json",
        "sign":"EVIDENCE/Q2_S29_FOUR_SIGN_MENDELIAN_F1.json",
        "returns":"EVIDENCE/Q2_S29_STATIC_FOCAL_W.json",
    }
    members,derivations=builder.q2_s29_mechanism_materials()
    assert set(members)==set(labels.values())==set(derivations)
    for field,label in labels.items():
        path,pin=SOURCES[field]
        source=(ROOT/path).read_bytes()
        assert git_blob(source)==pin
        assert members[label]==source
        assert derivations[label]["source_git_blob_sha1"]==pin
        assert derivations[label]["original_sha256"]==hashlib.sha256(source).hexdigest()
        assert derivations[label]["original_sha256"]==derivations[label]["derived_sha256"]
        builder.validate_member(label,members[label])
    output=tmp_path/"s29-review.zip"
    receipt=build(output,figures=fake_pdfs(tmp_path),
                  supplementary_figures=supplementary_figures(tmp_path))
    with zipfile.ZipFile(output) as z:
        assert set(labels.values()).issubset(set(z.namelist()))
        assert all(z.read(label)==members[label] for label in labels.values())
        manifest=json.loads(z.read("MANIFEST.json"))
        assert "q2_s29_mechanism_evidence" in manifest
        assert all(
            receipt["source_derivations"][label]==derivations[label]
            for label in labels.values()
        )
        si=z.read("SUPPORTING_INFORMATION.md").decode("utf-8")
        assert "EVIDENCE/Q2_S29_STATIC_FOCAL_W.json" in si
        assert "not independent source replication" in si
        assert manifest["doi_deposit_complete"] is False
