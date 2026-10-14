"""Source-audited synthetic founder-draw allocation, with no simulation."""
import json
from pathlib import Path
import pytest

from scripts.audit_chapter2_source_assignment_candidate_QA_20261014 import (
    CONTRACT, SEEDS_PER_BLOCK, qa_seed, check_committed,
)


def test_exact_technical_source_and_draw_inventory_and_biology_no_go():
    a=check_committed()
    assert a["status"]=="NO_EXECUTION_TECHNICAL_SOURCE_ASSIGNMENT_ONLY"
    assert a["nested_source_draw_seed_groups"]==64
    assert a["n_source_assignment_m_x_n_cases"]==1024
    assert a["independent_natural_founder_pools"]==0
    assert a["n_biological_evolutionary_histories"]==0
    assert len(a["technical_source_draw_receipts"])==64
    assert len(a["observed_synthetic_source_assignment_summary"])==32
    assert all(r["biological_future_seed"] is None
               for r in a["technical_source_draw_receipts"])
    assert len({r["source_assignment_seed"] for r in a["technical_source_draw_receipts"]})==64
    assert len({r["founder_draw_seed"] for r in a["technical_source_draw_receipts"]})==64
    mismatched_a=sum(x["I_no_symmetric_heterozygotes_but_support"]
                      for x in a["observed_synthetic_source_assignment_summary"])
    mismatched_b=sum(x["I_symmetric_heterozygotes_but_no_support"]
                      for x in a["observed_synthetic_source_assignment_summary"])
    assert (mismatched_a,mismatched_b)==(83,20)


def test_seeds_have_separate_roles_and_no_reuse_between_founder_blocks():
    for i in range(SEEDS_PER_BLOCK):
        main={kind:qa_seed("main",i,kind) for kind in ("source","draw","recipient")}
        confirmation={kind:qa_seed("confirmation",i,kind)
                      for kind in ("source","draw","recipient")}
        assert len(set(main.values()))==3
        assert len(set(confirmation.values()))==3
        assert set(main.values()).isdisjoint(set(confirmation.values()))
        assert all(0<=value<2**63 for value in main.values())


@pytest.mark.parametrize("block,rep,axis",[
    ("main",-1,"source"),("main",32,"source"),("main",True,"source"),
    ("nonexistent",0,"source"),("main",0,"biological_future"),
])
def test_unregistered_source_seed_identity_stops(block,rep,axis):
    with pytest.raises(ValueError,match="Unregistered"):
        qa_seed(block,rep,axis)


def test_no_biological_future_may_be_authorized_by_technical_contract():
    c=json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert c["status"]=="UNAPPROVED_NO_BIOLOGY_TECHNICAL_RANDOMISATION_ONLY"
    assert c["no_biological_history_generated"] is True
    assert c["author_run_approval"] is False
    assert c["allow_pilot_execution"] is False
    assert c["source_randomizations_are_natural_independent_populations"] is False
    assert c["phenotype_backgrounds_are_independent_source_populations"] is False
    assert c["future_history_seed_status"]=="NULL_NOT_AUTHORIZED"
