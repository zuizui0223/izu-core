"""Source-locked editorial figure-rank and one-paper claim limits (no simulation)."""
import hashlib
import json
from pathlib import Path

from scripts.build_chapter2_unified_el_submission_bundle import (
    PDF_FIGURES, SUPPLEMENTARY_FIGURES,
    derive_review_si_figure_roles,
)

ROOT=Path(__file__).resolve().parents[1]
PAPER=ROOT/"docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md"
SI=ROOT/"docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md"
ROUTE=ROOT/"data/design/chapter2_one_paper_route_20261010.json"
SOURCE=ROOT/"data/results/atom_cell_completed_20261011/ATOM_ABM_FINAL_READOUT_20261011.json"
ABM=ROOT/"data/results/atom_cell_completed_20261011/matched_comparison.json"
NOTE=ROOT/"docs/CHAPTER2_Q3_ATOM_MAIN_FIGURE_20261016.md"
OLD_RENDERER=ROOT/"scripts/figure_model3_genetic_realization.py"


def test_main_q3_original_mutation_pdf_is_source_pinned():
    original=PDF_FIGURES["Figure3.pdf"]
    assert original==ROOT/"docs/atom_comparison_20261011/resolution_figures_20261011/atom_abm.pdf"
    raw=original.read_bytes()
    expected=json.loads(SOURCE.read_text(encoding="utf-8"))["outputs"]["atom_abm.pdf"]
    assert hashlib.sha256(raw).hexdigest()==expected
    assert expected=="51c65d51b242834a51bab1a9f84b87c6dcfcb8e5ad30d875b6620b391ccb2997"
    assert SUPPLEMENTARY_FIGURES["SupplementaryFigureS3.pdf"]==(
        ROOT/"outputs/figures/model3_genetic_realization_20261005/genetic_realization.pdf")
    assert SUPPLEMENTARY_FIGURES["SupplementaryFigureS1.pdf"].name=="trait_pollen_snapshot400.pdf"
    assert SUPPLEMENTARY_FIGURES["SupplementaryFigureS2.svg"].name=="crossing_by100.svg"
    assert len(PDF_FIGURES)==3 and len(SUPPLEMENTARY_FIGURES)==3
    # The old plot generator remains a real source-backed script, not altered.
    assert "model3_ch2_bridge_summary_20260927/summary.json" in OLD_RENDERER.read_text()


def test_full_ten_contexts_and_original_order_counts_not_pooled():
    source=json.loads(ABM.read_text(encoding="utf-8"))
    assert source["status"]=="all_ten_contexts_accounted"
    assert len(source["rows"])==10 and len(source["abm_archive_sha256"])==320
    events={r["context"]: next(e for e in r["events"] if e["threshold"]==.05)
            for r in source["rows"]}
    assert all(sum(z["abm_counts"].values())==32 for z in events.values())
    contexts=(
       "causal_main_s0.125_matched_n48_standing_MI_new_A_r0_evolving",
       "causal_confirmation_s0.125_matched_n48_standing_MI_new_A_r0_evolving",
    )
    for i,context in enumerate(contexts):
        row=next(r for r in source["rows"] if r["context"]==context)
        event=events[context]
        assert event["density"]["category"]=="assurance_first"
        assert event["abm_counts"]["assurance_first"]==[3,2][i]
        assert event["abm_counts"]["assurance_only"]==[15,7][i]
        assert all(c["all_starts"]==32 and c["abm_occupied_fraction"]==1
                   for c in row["checkpoints"])
    assert source["design"]["responses"]=={
        "horizon":200,"sustained":20,"thresholds":[.025,.05,.1],"tie":5,
    }


def test_original_si_immutable_but_review_copy_has_correct_figures():
    original=SI.read_bytes()
    blob=hashlib.sha1(b"blob "+str(len(original)).encode()+b"\0"+original).hexdigest()
    assert blob=="fdecc89abaee3479ae5eef3f476d5ba937505690"
    derived=derive_review_si_figure_roles(original)
    assert "The original-mutation ten-context genetic-order comparison" in derived
    assert "3/32 and 2/32 counts" in derived
    assert "`Figure3.pdf`" in derived
    assert "`SupplementaryFigureS3.pdf`" in derived
    assert "`SupplementaryFigureS1.pdf`" in derived
    assert "The original-mutation ten-context genetic-order comparison" not in original.decode()


def test_one_letter_new_main_fig3_cites_original_and_s3_is_distinct():
    source=PAPER.read_text(encoding="utf-8")
    main=source.split("# Introduction",1)[1].split("# Primary figure assembly and captions",1)[0]
    abstract=source.split("## Abstract",1)[1].split("## Keywords",1)[0]
    route=json.loads(ROUTE.read_text(encoding="utf-8"))
    assert len(main.split())==route["journal_fit"]["current_main_text_words"]<=route["journal_fit"]["ecology_letters_letter_main_max"]
    assert len(abstract.split())==route["journal_fit"]["current_abstract_words"]<=route["journal_fit"]["ecology_letters_letter_abstract_max"]
    assert route["active_manuscript_count"]==1
    assert route["status"]=="active_unified_manuscript_not_submitted"
    assert "only 3/32 and 2/32 ABM histories realized that category at the 0.05/20-census threshold (Fig. 3)" in main
    assert "Increasing plant capacity from 48 to 192 reduced finite mixed labels from 12/128 to 1/128 (Fig. S3)" in main
    assert "**Figure 3. Finite inherited response order can differ" in source
    assert "**Supplementary Figure S3. Two separate diagnostics" in source
    assert "Density is **not** the ABM stochastic expectation" in source
    assert "Issue #436" in NOTE.read_text(encoding="utf-8")
