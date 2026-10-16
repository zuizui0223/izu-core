"""Read-only acceptance tests for the completed Q2 384 original-source study.

These assert a published original-source-admitted receipt; tests DO NOT execute
new Model3 biological histories or reclassify uncommitted original NPZs.
The original Actions archive, lineage replay and separate raw rereadback remain
the provenance of the numeric receipt.
"""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/"docs/audits/CHAPTER2_Q2_I_SUPPORT_384_ORIGINAL_READOUT_20261016.json"
PAPER=ROOT/"docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md"
RESULTS_NOTE=ROOT/"docs/CHAPTER2_Q2_I_SUPPORT_384_REGISTERED_RESULT_20261016.md"
LABELS=["assurance_first","investment_first","near_simultaneous","assurance_only","investment_only","neither"]


def test_q2_384_source_identity_and_registered_no_retuning():
    doc=json.loads(RESULT.read_text(encoding="utf-8"))
    run=doc["original_run"]
    assert doc["scientific_status"]=="complete_preregistered_both_coprimary_inconclusive"
    assert run["run_id"]==38918737325
    assert run["original_raw_shards"]==32 and run["original_cases"]==384
    assert run["crossed_founder_labels"]==run["crossed_visitor_history_labels"]==8
    assert run["updates_per_case"]==200 and run["expected_original_updates"]==76800
    assert run["source_head_sha"]=="f760f936b164df3dd3dceb9d9942d6b9805304eb"
    assert run["independent_readout_artifact_id"]==12054486425
    assert run["original_design_sha256"]=="f4edc17fcda3b76e3274d10538c152faa46d67c7c56486f9c679aebe3e70d709"
    assert run["original_source_manifest_sha256"]=="69e6c2b789ff610214a46cbffd79e34c46ab0ee335ab20bc4e147443dd032030"
    assert doc["registered_inference"]["bootstraps"]==9999
    assert doc["registered_inference"]["bootstrap_seed"]==910763
    assert doc["registered_inference"]["result"]=="both_inconclusive"
    assert doc["independent_original_archive_readback"]["original_npz_and_case_receipts"]==384
    assert doc["independent_original_archive_readback"]["typed_I_homologs_independently_mapped_to_parents"]==7372754


def test_q2_all_six_classes_and_both_primary_intervals_are_conservative():
    d=json.loads(RESULT.read_text(encoding="utf-8"))
    assert d["six_class_labels"]==LABELS
    for arm in ("near","far"):
        for pol in ("dense_reachable","sparse_reachable","dense_unreachable"):
            row=d["original_six_class_cells"][arm][pol]
            x=row["counts"]
            assert len(x)==6 and all(isinstance(v,int) and v>=0 for v in x)
            assert sum(x)==row["occupied_200"]==64
            assert sum(x[i] for i in (0,1,2,4))==row["I_events"]
            assert sum(x[i] for i in (0,1,2,3))==row["A_events"]
            if pol=="dense_unreachable":
                assert row["I_events"]==0
    f=d["original_six_class_cells"]["far"]
    score=lambda row:(row["counts"][0]-row["counts"][1])/64
    observed=(score(f["dense_reachable"])-score(f["sparse_reachable"]))
    event=(f["dense_reachable"]["I_events"]-f["sparse_reachable"]["I_events"])/64
    assert observed==d["coprimary"]["carrier_order_score_delta"]["estimate"]==0.109375
    assert event==d["coprimary"]["carrier_I_event_delta"]["estimate"]==0.1875
    assert f["dense_reachable"]["I_events"]==20
    assert f["sparse_reachable"]["I_events"]==8
    for row in d["coprimary"].values():
        lo,hi=row["simultaneous_familywise_CI"]
        assert lo<=0<=hi and not row["excludes_zero"]
    changes=d["far_within_paired_I_event_transition_counts"]
    assert sum(changes[k] for k in ("both_absent","gained_in_dense","lost_in_dense","both_present"))==64
    assert changes["gained_in_dense"]-changes["lost_in_dense"]==12


def test_one_letter_reports_inconclusive_without_overstating_order_causation():
    paper=PAPER.read_text(encoding="utf-8")
    note=RESULTS_NOTE.read_text(encoding="utf-8")
    abstract=paper.split("## Abstract",1)[1].split("## Keywords",1)[0]
    main=paper.split("# Introduction",1)[1].split("# Primary figure assembly",1)[0]
    assert len(abstract.split())<=150 and len(main.split())<=5000
    assert "384-path" in abstract and "remained inconclusive" in abstract
    assert "Bonferroni interval" in paper and "Both co-primary intervals included zero" in paper
    assert "CHAPTER2_Q2_I_SUPPORT_384_REGISTERED_RESULT_20261016.md" in paper
    assert "both_inconclusive" in note and "17/64 gained" in note
    assert "DOI-backed external raw-data deposit remains unverified" in note
    assert "no identified common mediation chain" in note
