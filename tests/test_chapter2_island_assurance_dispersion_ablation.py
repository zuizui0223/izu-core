"""Boundary tests for a mean-preserving assay; never promote old failures."""
import json
from pathlib import Path
import numpy as np
from scripts.run_chapter2_island_assurance_dispersion_ablation import (
    load_protocol,historical_groups,simulate_group
)

ROOT=Path(__file__).resolve().parents[1]


def test_design_has_exact_factorial_and_exposed_not_independent_histories():
    d,parent,source=load_protocol()
    assert d["history_seeds"]==[35100801,35100802,35100803,35100804]
    assert d["historical_demographic_repeat"]==35101801
    assert d["n_poststress_trajectories"]==3072
    assert d["n_matched_stress_cells"]==1024
    assert d["assurance_dispersion_scale"]==[0.0,0.5,1.0]
    assert d["post_mutation_rate"]==[0.0,0.01]
    assert set(d["settings"])==set(source["settings"])
    assert len(historical_groups(d))==16


def test_live_mini_genetic_dispersal_ablation_keeps_mean_and_q_squared_variance():
    d,parent,source=load_protocol()
    mini={**d,"post_updates":2,"post_rng_repeats":[0]}
    rows=simulate_group(historical_groups(d)[0],mini,parent,source)
    assert len(rows)==48
    assert all(x["occupied"]==int(x["end_n"]>0) for x in rows)
    for bg in mini["backgrounds"]:
        sub=[r for r in rows if r["background"]==bg]
        means={round(r["a_mean"],12) for r in sub}
        assert len(means)==1
        initial={r["q"]:r["a_var_initial"] for r in sub}
        assert initial[0.0]==0.0
        assert abs(initial[0.5]-initial[1.0]/4)<1e-12
        assert all(r["a_var_end"] is None or abs(r["a_var_end"])<1e-12
                   for r in sub if r["q"]==0 and r["mutation"]==0)


def test_recorded_ablation_remains_an_exploratory_heterogeneous_effect():
    result=json.loads((ROOT/
        "data/results/chapter2_island_assurance_dispersion_ablation_20261008.json"
    ).read_text())
    assert result["status"].startswith("completed_exploratory")
    assert result["n_trajectories"]==3072
    assert result["independent_visitor_histories"]==4
    assert len(result["per_setting_background_mutation"])==16
    assert len(result["source_provenance"]["offline_shard_sha256"])==4
    assert result["source_provenance"]["github_actions_reproduction"] is False
    effects=[r["q0_minus_q1"] for r in result["per_setting_background_mutation"]]
    assert any(x<0 for x in effects) and any(x>0 for x in effects)
    assert any(x==0 for x in effects)
    prior=json.loads((ROOT/
        "data/results/chapter2_island_genetic_state_transplant_independent16_20261008.json"
    ).read_text())
    assert prior["frozen_primary"]["passed"] is False
    assert any("covariance" in s.lower() for s in result["boundaries"])
    # The equally weighted pooled contrast is descriptive over four reused histories.
    effects=result["per_setting_background_mutation"]
    occupancy_0=sum(x["terminal_occupancy_by_dispersion_scale"]["0"] for x in effects)/16
    occupancy_1=sum(x["terminal_occupancy_by_dispersion_scale"]["1"] for x in effects)/16
    assert abs((occupancy_0-occupancy_1)-0.0048828125) < 1e-12
    pollen=[x for x in effects if x["setting"]=="pollen_discount"]
    assert abs(sum(x["q0_minus_q1"] for x in pollen)) < 1e-12
    assert any(x["q0_minus_q1"]>0 for x in pollen)
    assert any(x["q0_minus_q1"]<0 for x in pollen)
