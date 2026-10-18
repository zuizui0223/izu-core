"""Pure-statistics competing-event and fault-buffer contract tests.

No new biological simulation. Synthetic fixtures are NOT island evidence.
"""
import copy

import pytest

from scripts.chapter2_assurance_access_competing_risks_20261018 import (
    maternal_fault_floor, history_events, compare_historical_policies,
)


def make_case(founder,visitor,policy,upper,*,dead=None):
    rows=[]
    for t, val in enumerate(upper):
        occupied=dead is None or t < dead
        rows.append(dict(t=t,occupied=occupied,
                         max_I_allele=float(val) if occupied else None))
    return dict(founder_id=founder,visitor_id=visitor,replicate_id="r0",
                policy=policy,
                founder_genome_sha256="synthetic-founder-"+founder,
                visitor_history_sha256="synthetic-visitor-"+visitor,
                historical_demographic_seed=1234+int(founder[-1])*2+int(visitor[-1]),
                target_I=.5,censuses=rows)


def crossed_fixture():
    u=[.7,.66,.61,.58,.58]
    records=[]
    for f in ("f0","f1"):
        for v in ("v0","v1"):
            records.append(make_case(f,v,"fixed",u if (f,v)!=("f1","v0")
                                     else [.7,.65,.59,.45,.45]))
            if (f,v)==("f0","v0"):
                ev=make_case(f,v,"evolving",[.7,.6,.45,.42,.42],dead=4)
            elif (f,v)==("f0","v1"):
                ev=make_case(f,v,"evolving",u,dead=3)
            else:
                ev=make_case(f,v,"evolving",u)
            records.append(ev)
    return records


def test_unconditional_competing_incidence_and_current_survival_partition():
    result=compare_historical_policies(crossed_fixture())
    assert result["crossed_founder_visitor_cells"]==4
    assert result["independent_founder_count"]==2
    assert result["independent_visitor_history_count"]==2
    assert result["histories_per_historical_A_policy"]==4
    assert result["nested_demographic_repeats_per_cell"]==1
    t2=result["time_series"][2]["arms"]
    assert t2["evolving"]["CIF_high_I_genetic_loss"]==.25
    assert t2["fixed"]["CIF_high_I_genetic_loss"]==0.
    t4=result["time_series"][4]["arms"]
    assert t4["evolving"]["CIF_high_I_genetic_loss"]==.25
    assert t4["fixed"]["CIF_high_I_genetic_loss"]==.25
    assert t4["evolving"]["CIF_extinction_before_genetic_loss"]==.25
    assert t4["evolving"]["P_extinct"]==.5
    assert t4["evolving"]["P_alive_but_high_I_closed"]==0.
    assert t4["fixed"]["P_alive_but_high_I_closed"]==.25
    assert t4["evolving"]["P_alive_and_high_I_access"]==.5
    assert t4["fixed"]["P_alive_and_high_I_access"]==.75
    assert result["restricted_accessible_census_time"]=={"fixed":4.5,"evolving":3.75}
    assert result["restricted_accessible_time_difference_evolving_minus_fixed"]==-.75
    for year in result["time_series"]:
        for arm in year["arms"].values():
            assert abs(arm["CIF_high_I_genetic_loss"]+
                       arm["CIF_extinction_before_genetic_loss"]+
                       arm["P_alive_and_high_I_access"]-1.)<1e-12
            assert abs(arm["P_alive_and_high_I_access"]+
                       arm["P_alive_but_high_I_closed"]+
                       arm["P_extinct"]-1.)<1e-12


def test_fault_floor_is_ovule_weighted_and_not_population_survival():
    assert maternal_fault_floor([1.,3.],[0.,1.],.5)==.375
    assert maternal_fault_floor([4.,4.],[.5,.5],.5)==.25
    assert maternal_fault_floor([1.,1.],[1.,1.],0.)==1.
    with pytest.raises(ValueError):
        maternal_fault_floor([0.,0.],[0.,0.],.5)
    with pytest.raises(ValueError):
        maternal_fault_floor([1.],[float("nan")],.5)


def test_support_does_not_reopen_and_extinct_population_cannot_resurrect():
    a=make_case("f0","v0","fixed",[.7,.45,.55,.45,.43])
    with pytest.raises(ValueError,match="support rose"):
        history_events(a)
    b=make_case("f0","v0","fixed",[.7,.6,.55,.5,.45],dead=3)
    b["censuses"][4]["occupied"]=True
    b["censuses"][4]["max_I_allele"]=.4
    with pytest.raises(ValueError,match="demographic rescue"):
        history_events(b)
    c=make_case("f0","v0","fixed",[.7,.6,.55,.5,.45],dead=3)
    c["censuses"][3]["max_I_allele"]=0.0
    with pytest.raises(ValueError,match="undefined"):
        history_events(c)


def test_missing_crossed_cells_policy_stream_mismatch_and_duplicate_fail_closed():
    original=crossed_fixture()
    with pytest.raises(ValueError,match="crossed founder"):
        compare_historical_policies([r for r in original
                                     if not (r["founder_id"]=="f1" and r["visitor_id"]=="v1")])
    mismatch=copy.deepcopy(original)
    mismatch[1]["historical_demographic_seed"]+=1
    with pytest.raises(ValueError,match="share original"):
        compare_historical_policies(mismatch)
    duplicate=copy.deepcopy(original)+[copy.deepcopy(original[0])]
    with pytest.raises(ValueError,match="duplicate historical"):
        compare_historical_policies(duplicate)


def test_source_first_event_extinction_after_loss_remains_genetic_first():
    r=make_case("f0","v0","evolving",[.7,.6,.45,.4,.4],dead=4)
    e=history_events(r)
    assert e["first_competing_event"]=="genetic_loss"
    assert e["loss_t"]==2 and e["extinction_t"]==4
    assert e["status_by_year"]==[
        "alive_accessible","alive_accessible",
        "alive_closed","alive_closed","extinct"]
