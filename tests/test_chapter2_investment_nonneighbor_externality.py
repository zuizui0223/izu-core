"""Focal-investment indirect effects: Model3 source ledger and null controls."""
import json
from dataclasses import replace
import numpy as np

from scripts.audit_chapter2_investment_nonneighbor_externality import (
    STATUS,contract,ledger_partition,run_all,direction
)
from scripts.audit_chapter2_beta_gamma_seed_map import (
    load_contract as original_contract,state_of_clones,visitors_for
)
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN,config as source_config,load_design
)


def test_source_contract_and_zero_visitors_have_zero_nonfocal_effect():
    _,h=contract()
    d,_=original_contract()
    assert len(h)==64
    cfg=replace(source_config(load_design(DEFAULT_DESIGN),
                               "prior_selfing",0.0,"evolving"),
                capacity=8,ovule_budget=8.)
    state=state_of_clones((.2,.35,.35),8)
    visitor=visitors_for("none",d)
    for width in (.005,.0025):
        rec=ledger_partition(state,visitor,cfg,width)
        assert rec["nonfocal_total_viable_seeds"]==0
        assert rec["nonfocal_from_focal_father"]==0
        assert rec["nonfocal_from_other_fathers"]==0


def test_outcross_father_decomposition_is_accounting_not_public_goods_assumption():
    d,_=original_contract()
    cfg=replace(source_config(load_design(DEFAULT_DESIGN),
                              "delayed_control",0.0,"evolving"),
                capacity=8,ovule_budget=8.)
    state=state_of_clones((.2,.35,.35),8)
    r=ledger_partition(state,visitors_for("matched4",d),cfg,.005)
    assert np.isclose(
        r["nonfocal_total_viable_seeds"],
        r["nonfocal_from_focal_father"]+
        r["nonfocal_from_other_fathers"]+
        r["nonfocal_self"],
        atol=1e-10,rtol=0)
    assert np.isclose(
        r["entire_group_unilateral_seed_slope"] if "entire_group_unilateral_seed_slope" in r
        else r["group_total_viable_seeds"],
        r["focal_maternal_viable_seeds"]+r["nonfocal_total_viable_seeds"],
        atol=1e-10,rtol=0)


def test_classification_refuses_to_equate_conflict_with_positive_externality():
    assert direction(.1,.1)=="positive"
    assert direction(-.1,-.1)=="negative"
    assert direction(0.,0.)=="numerically_zero"
    assert direction(.1,-.1)=="inconclusive"


def test_entire_original_grid_retains_all_14_unfavorable_selection_cells():
    data=run_all()
    assert data["status"]==STATUS
    assert data["n_full_investment_conditions"]==192
    assert data["n_original_investment_discordances"]==14
    assert sum(data["externality_sign_counts_all"].values())==192
    assert sum(data["externality_sign_counts_in_original_14_conflicts"].values())==14
    assert all(r["original_beta"]<0 and r["original_gamma_collective"]>0
               for r in data["original_conflict_externalities"])
    json.dumps(data,allow_nan=False)
