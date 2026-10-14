"""Source-faithful finite-mutant beta vs collective seed-gamma map.

Post-outcome *engineering* map with predeclared complete synthetic grid.
No prospective ecological visitor histories, field islands, demographic
trajectories, inferred extinction probability, or evolution experiment.

At finite N, "mutant" is ONE individual among N and NOT a true rare-mutant
invasion gradient as N->infinity. Reproduction uses the original explicit
diploid Model 3 Ledger via the existing fixed-B reproduce_kb routine.
"""
from __future__ import annotations
from dataclasses import replace
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.types import PlantState, VisitorState
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_beta_gamma_seed_engineering_grid_20261010.json"
STATUS = "FINITE_BETA_GAMMA_SEED_SOURCE_ENGINEERING_NOT_PERSISTENCE"
ALLOWED_SETTINGS = ("delayed_control","prior_selfing","pollen_discount","assurance_cost")
ALLOWED_TRAITS = ("investment","assurance")
ALLOWED_REGIMES = ("none","matched4","shifted4")
TRAIT_INDEX = {"investment": 1, "assurance": 2}


def load_contract(path=DESIGN):
    blob = Path(path).read_bytes()
    d = json.loads(blob)
    if (d.get("status") != "OUTCOME_UNSEEN_ENGINEERING_GRID_NOT_PROSPECTIVELY_REGISTERED"
            or d.get("source_history_count") != 0
            or d.get("capacity_K") != [8,48]
            or d.get("pollen_background_B") != 48
            or d.get("central_difference_steps") != [0.005,0.0025]
            or d.get("classification_deadband_absolute_log_derivative") != 0.02
            or tuple(d["reproductive_settings"]) != ALLOWED_SETTINGS
            or tuple(d["perturbed_traits"]) != ALLOWED_TRAITS
            or tuple(d["visitor_regimes"]) != ALLOWED_REGIMES
            or d["traits"] != {
                "matching":[0.2,0.5],
                "investment":[0.35,0.65],
                "assurance":[0.35,0.65]
            }
            or d.get("expected_rows") != 384):
        raise ValueError("unexpected engineering source contract")
    return d, hashlib.sha256(blob).hexdigest()


def state_of_clones(traits, n):
    """Entire joint three-locus diploid genotype, not marginal trait proxies."""
    z = np.asarray(traits,dtype=float)
    if z.shape != (3,) or not np.isfinite(z).all() or ((z<=0)|(z>=1)).any():
        raise ValueError("finite resident state must be interior")
    if n not in (8,48):
        raise ValueError("restricted finite K")
    alleles = np.broadcast_to(z[None,:,None],(n,3,2)).copy()
    return PlantState(
        alleles=alleles,
        allele_origin=np.arange(n*6,dtype=np.int64).reshape(n,3,2),
        mutation_flags=np.zeros((n,3,2),dtype=bool),
        ids=np.arange(n,dtype=np.int64),
        birth_years=np.zeros(n,dtype=np.int64),
    )


def changed_state(source, trait_index, signed_step, *, whole):
    """Change the designated locus *expression encoded in genotype* for all
    or one experimental individual, leaving all background clones unchanged."""
    a=np.array(source.alleles,copy=True)
    if whole:
        a[:,trait_index,:] += signed_step
    else:
        a[0,trait_index,:] += signed_step
    return replace(source,alleles=a)


def visitors_for(label, design):
    if label not in ALLOWED_REGIMES:
        raise ValueError("unknown artificial visitor regime")
    s=design["visitor_regimes"][label]
    n=len(s["optima"])
    return VisitorState(
        ids=np.arange(100,100+n,dtype=np.int64),
        optima=np.array(s["optima"],dtype=float),
        breadths=np.array(s["breadths"],dtype=float),
        effectiveness=np.array(s["effectiveness"],dtype=float),
    )


def ledger_stats(source,visitors,config,B):
    ledger=reproduce_kb(source,visitors,config,
                        background_denominator_capacity=B)
    F=ledger.outcross.sum(axis=0)  # maternal/recipient
    P=ledger.outcross.sum(axis=1)  # paternal/donor
    S=ledger.self_viable
    if not np.isclose(F.sum(),P.sum(),atol=1e-12,rtol=0):
        raise AssertionError("group paternal/maternal outcross mass not conserved")
    total=float((F+S).sum())
    if not np.isclose(total,ledger.outcross.sum()+ledger.self_viable.sum(),
                      atol=1e-12,rtol=0):
        raise AssertionError("total viable seeds not conserved")
    W=.5*(F+P)+S
    if np.any(W<=0) or total<=0:
        raise ValueError("resident or mutant fecundity nonpositive")
    return {"F":F, "P":P,"S":S,"W":W,"total":total,
            "total_outcross":float(F.sum()),"total_self":float(S.sum())}


def log_mean(a,b):
    if not a>0 or not b>0:
        raise ValueError("positive fecundity required")
    if abs(a-b)<1e-13*max(a,b):
        return .5*(a+b)
    return (a-b)/(np.log(a)-np.log(b))


def local_slopes(resident,visitors,config,trait_index,h):
    n=len(resident.ids)
    p=ledger_stats(changed_state(resident,trait_index,+h,whole=False),
                   visitors,config,48)
    m=ledger_stats(changed_state(resident,trait_index,-h,whole=False),
                   visitors,config,48)
    # One-mutant W is maternal/2 + paternal/2 + self at index zero.
    Wp=float(p["W"][0]);Wm=float(m["W"][0])
    beta=float((np.log(Wp)-np.log(Wm))/(2*h))
    denom=log_mean(Wp,Wm)
    components={
        "maternal_outcross_F": float(.5*(p["F"][0]-m["F"][0])/(2*h*denom)),
        "paternal_outcross_P": float(.5*(p["P"][0]-m["P"][0])/(2*h*denom)),
        "viable_self_S":float((p["S"][0]-m["S"][0])/(2*h*denom)),
    }
    if not np.isclose(sum(components.values()),beta,atol=1e-11,rtol=0):
        raise AssertionError("F/P/S source finite-log-gradient not additive")
    gp=ledger_stats(changed_state(resident,trait_index,+h,whole=True),
                    visitors,config,48)
    gm=ledger_stats(changed_state(resident,trait_index,-h,whole=True),
                    visitors,config,48)
    gamma=float((np.log(gp["total"])-np.log(gm["total"]))/(2*h))
    return {"beta_one_individual":beta,"gamma_group_seed":gamma,
            "beta_components":components,
            "group_F_plus":gp["total_outcross"],
            "group_F_minus":gm["total_outcross"],
            "group_S_plus":gp["total_self"],
            "group_S_minus":gm["total_self"],
            "n_individuals":n}


def classify(beta,gamma,secondary_beta,secondary_gamma,deadband):
    def stable_sign(a,b):
        if (not np.isfinite([a,b]).all()
                or abs(a-b) > 0.02+0.05*max(abs(a),abs(b))):
            return "unresolved"
        if abs(a)<=deadband or abs(b)<=deadband:
            return "unresolved"
        if a*b<=0:
            return "unresolved"
        return "+" if a>0 else "-"
    b=stable_sign(beta,secondary_beta)
    g=stable_sign(gamma,secondary_gamma)
    if "unresolved" in (b,g):
        return "inconclusive", b, g
    if b==g:
        return "aligned",b,g
    return ("individual_advantage_group_harm"
            if b=="+" else "individual_disadvantage_group_benefit"),b,g


def audit():
    contract,digest=load_contract()
    design=load_design(DEFAULT_DESIGN)
    rows=[]
    for setting in ALLOWED_SETTINGS:
        for regime in ALLOWED_REGIMES:
            visitor=visitors_for(regime,contract)
            for K in (8,48):
                cfg=replace(source_config(design,setting,0.0,"evolving"),
                            capacity=K,survival=0.,mutation_rate=0.,
                            ovule_budget=float(contract["ovule_budget"]))
                if cfg.seed_arrival.supply!=0:
                    raise AssertionError("seed immigration not permitted")
                for x in contract["traits"]["matching"]:
                    for i in contract["traits"]["investment"]:
                        for a in contract["traits"]["assurance"]:
                            original=state_of_clones((x,i,a),K)
                            reference=ledger_stats(original,visitor,cfg,48)
                            for trait in ALLOWED_TRAITS:
                                j=TRAIT_INDEX[trait]
                                s1=local_slopes(original,visitor,cfg,j,.005)
                                s2=local_slopes(original,visitor,cfg,j,.0025)
                                result,bs,gs=classify(
                                    s1["beta_one_individual"],s1["gamma_group_seed"],
                                    s2["beta_one_individual"],s2["gamma_group_seed"],
                                    contract["classification_deadband_absolute_log_derivative"]
                                )
                                rows.append({
                                    "setting":setting,"visitor_regime":regime,
                                    "K":K,"B":48,"resident":[float(x),float(i),float(a)],
                                    "trait":trait,
                                    "beta_one_individual":s1["beta_one_individual"],
                                    "gamma_group_seed":s1["gamma_group_seed"],
                                    "beta_F":s1["beta_components"]["maternal_outcross_F"],
                                    "beta_P":s1["beta_components"]["paternal_outcross_P"],
                                    "beta_S":s1["beta_components"]["viable_self_S"],
                                    "beta_refinement":s2["beta_one_individual"],
                                    "gamma_refinement":s2["gamma_group_seed"],
                                    "beta_sign":bs,"gamma_sign":gs,"classification":result,
                                    "group_viable_seed_reference":reference["total"],
                                    "group_outcross_reference":reference["total_outcross"],
                                    "group_self_reference":reference["total_self"],
                                    "no_visitor_strict_outcross_zero":
                                        (reference["total_outcross"]==0 if regime=="none" else None),
                                })
    if len(rows)!=contract["expected_rows"]:
        raise AssertionError("not all grid rows retained")
    classes=("aligned","individual_advantage_group_harm",
             "individual_disadvantage_group_benefit","inconclusive")
    counts={key:sum(r["classification"]==key for r in rows) for key in classes}
    by_setting={
        setting:{key:sum(r["classification"]==key and r["setting"]==setting for r in rows)
                 for key in classes} for setting in ALLOWED_SETTINGS
    }
    return {
        "status":STATUS,"design_sha256":digest,
        "source":"unmodified Model3 finite reproduction_kb full parental ledger",
        "n_rows":len(rows),"independent_visitor_histories":0,
        "full_grid_class_counts":counts,
        "per_setting_class_counts":by_setting,
        "rows":rows,
        "scientific_boundary":[
            "Beta is the effect of perturbing ONE individual in a finite N=8 or 48 population; it is NOT a true rare-mutant infinite-population derivative, especially at N=8.",
            "Gamma here is total viable-group seed output, NOT unconditional survival probability, finite-horizon Gamma_persist or fitness of the group.",
            "All fixed visitors are hand-authored synthetic functional types: no ecological replication, observed island data, evolutionary trajectories or preregistered confirmations.",
            "F/P/S components are exact additive accounting of focal genetic contribution, not separately manipulated causes; paternal transfer is zero-sum only at fixed total outcross.",
            "Deadband and finite-step stability are engineering choices and not independently biologically calibrated thresholds.",
            "Any cell showing a beta/gamma mismatch motivates a distinct prospectively frozen experiment; it is not an evolutionary-suicide result.",
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    result=audit()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n",
                     encoding="utf-8")
    print(json.dumps({"status":result["status"],"counts":result["full_grid_class_counts"],
                      "per_setting":result["per_setting_class_counts"],
                      "n_rows":result["n_rows"]},sort_keys=True))


if __name__=="__main__":
    main()
