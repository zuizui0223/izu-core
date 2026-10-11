"""Post-outcome focal-investment nonfocal viable-seed externality audit.

Do NOT infer a pollinator attraction public good from beta/Gamma alone. Ask if
a unilateral focal investment change raises OTHER model conspecific mothers'
viable seed output in the unmodified Model3 source reproduction ledger.

The static visitor collection is unchanged: there is no visitor recruitment
or interspecific facilitation mechanism in these engineering fixtures.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_beta_gamma_seed_map import (
    ALLOWED_SETTINGS,ALLOWED_REGIMES, audit as original_beta_gamma_audit,
    changed_state,load_contract as load_original, state_of_clones, visitors_for,
)
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN,config as source_config,load_design,
)

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"data/design/chapter2_investment_nonneighbor_externality_audit_20261010.json"
STATUS="EXPLORATORY_FOCAL_TO_NONFOCAL_MODEL3_SEED_EXTERNALITY_LEDGER_AUDIT"
WIDTHS=(.005,.0025)


def contract():
    blob=DESIGN.read_bytes()
    d=json.loads(blob)
    if (d.get("status")!="POST_OUTCOME_SOURCE_LEDGER_DIAGNOSTIC_NOT_PREREGISTERED"
            or d.get("finite_perturbation_widths")!=list(WIDTHS)
            or d.get("fixed_B")!=48
            or "All original 4" not in d.get("complete_grid","")):
        raise ValueError("unregistered original source externality audit")
    return d,hashlib.sha256(blob).hexdigest()


def ledger_partition(original,visitor,cfg,h):
    """Outputs in absolute viable seeds per one trait-expression unit."""
    if h not in WIDTHS or len(original.ids) not in (8,48):
        raise ValueError("only source-matched central difference source")
    def components(sign):
        changed=changed_state(original,1,sign*h,whole=False)
        l=reproduce_kb(changed,visitor,cfg,background_denominator_capacity=48)
        F=l.outcross.sum(axis=0)
        S=l.self_viable
        focal=float(F[0]+S[0])
        nonfocal_from_focal_father=float(l.outcross[0,1:].sum())
        nonfocal_from_other_fathers=float(l.outcross[1:,1:].sum())
        nonfocal_self=float(S[1:].sum())
        nonfocal=(nonfocal_from_focal_father+
                  nonfocal_from_other_fathers+nonfocal_self)
        whole=float(l.outcross.sum()+S.sum())
        if not np.isclose(focal+nonfocal,whole,rtol=0,atol=1e-10):
            raise AssertionError("source nonfocal reproductive contribution lost")
        return {
            "focal_maternal_viable_seeds":focal,
            "nonfocal_from_focal_father":nonfocal_from_focal_father,
            "nonfocal_from_other_fathers":nonfocal_from_other_fathers,
            "nonfocal_self":nonfocal_self,
            "nonfocal_total_viable_seeds":nonfocal,
            "group_total_viable_seeds":whole,
        }
    hi=components(+1)
    lo=components(-1)
    change={k:(hi[k]-lo[k])/(2*h) for k in hi}
    if not np.isclose(
        change["nonfocal_total_viable_seeds"],
        sum(change[k] for k in (
            "nonfocal_from_focal_father",
            "nonfocal_from_other_fathers",
            "nonfocal_self")),
        rtol=0,atol=1e-10,
    ):
        raise AssertionError("nonfocal pollen-source component conservation failed")
    if not np.isclose(
        change["group_total_viable_seeds"],
        (change["focal_maternal_viable_seeds"]+
         change["nonfocal_total_viable_seeds"]),
        rtol=0,atol=1e-10
    ):
        raise AssertionError("focal plus nonfocal group output not conserved")
    return change


def direction(a,b):
    """Local numerical agreement is a model-computation diagnostic, not a CI."""
    if not (np.isfinite(a) and np.isfinite(b)):
        return "inconclusive"
    if abs(a-b)>.02+.05*max(abs(a),abs(b)):
        return "inconclusive"
    if a>1e-8 and b>1e-8:return "positive"
    if a< -1e-8 and b< -1e-8:return "negative"
    if abs(a)<=1e-8 and abs(b)<=1e-8:return "numerically_zero"
    return "inconclusive"


def run_all():
    _,digest=contract()
    grid,digest_orig=load_original()
    original=original_beta_gamma_audit()
    source={(r["setting"],r["visitor_regime"],r["K"],
             tuple(r["resident"])):r
            for r in original["rows"] if r["trait"]=="investment"}
    if len(source)!=192:
        raise AssertionError("original 384-grid investment subgrid not complete")
    blueprint=load_design(DEFAULT_DESIGN)
    report=[]
    for setting in ALLOWED_SETTINGS:
        for regime in ALLOWED_REGIMES:
            visitor=visitors_for(regime,grid)
            for K in (8,48):
                cfg=replace(source_config(blueprint,setting,0.0,"evolving"),
                            capacity=K,survival=0.,mutation_rate=0.,
                            ovule_budget=float(grid["ovule_budget"]))
                for x in grid["traits"]["matching"]:
                    for i in grid["traits"]["investment"]:
                        for a in grid["traits"]["assurance"]:
                            ident=(setting,regime,K,(x,i,a))
                            r=source[ident]
                            plant=state_of_clones((x,i,a),K)
                            coarse=ledger_partition(plant,visitor,cfg,.005)
                            refined=ledger_partition(plant,visitor,cfg,.0025)
                            key="nonfocal_total_viable_seeds"
                            state=direction(coarse[key],refined[key])
                            if regime=="none":
                                if (state!="numerically_zero"
                                        or coarse["nonfocal_from_focal_father"]!=0
                                        or refined["nonfocal_from_focal_father"]!=0):
                                    raise AssertionError("no-visitor other mothers cannot respond")
                            report.append({
                                "setting":setting,"regime":regime,"K":K,"B":48,
                                "traits":[float(x),float(i),float(a)],
                                "original_beta":r["beta_one_individual"],
                                "original_gamma_collective":r["gamma_group_seed"],
                                "original_classification":r["classification"],
                                "externality_sign":state,
                                "finite_focal_outside_seed_effect":coarse[key],
                                "refined_focal_outside_seed_effect":refined[key],
                                "pollen_and_self_externality_parts":{
                                    k:coarse[k] for k in (
                                        "nonfocal_from_focal_father",
                                        "nonfocal_from_other_fathers",
                                        "nonfocal_self")
                                },
                                "focal_maternal_viable_seed_slope":coarse["focal_maternal_viable_seeds"],
                                "entire_group_unilateral_seed_slope":coarse["group_total_viable_seeds"],
                            })
    if len(report)!=192:
        raise AssertionError("incomplete source engineering grid")
    conflicts=[r for r in report if
               r["original_classification"]=="individual_disadvantage_group_benefit"]
    if len(conflicts)!=14:
        raise AssertionError("original 14 beta-negative/group-positive conditions changed")
    classifications=("positive","negative","numerically_zero","inconclusive")
    return {
        "status":STATUS,
        "source_design_sha256":digest,
        "original_beta_gamma_design_sha256":digest_orig,
        "n_full_investment_conditions":len(report),
        "n_original_investment_discordances":len(conflicts),
        "externality_sign_counts_all":{
            k:sum(r["externality_sign"]==k for r in report)
            for k in classifications},
        "externality_sign_counts_in_original_14_conflicts":{
            k:sum(r["externality_sign"]==k for r in conflicts)
            for k in classifications},
        "original_conflict_externalities":conflicts,
        "all_192_rows":report,
        "interpretation_limits":[
            "This is a unilateral model-conspecific net viable seed response in the EXACT ORIGINAL reproduction ledger, not a direct test that additional pollinator individuals were recruited.",
            "Fixed static visitor types and numbers exclude dynamic pollinator attraction, and no among-species facilitation is represented.",
            "Pollen father changes include increases in focal-origin pollen and redistribution of other donors; total nonfocal mother F plus S is needed for a genuine net benefit.",
            "The original beta and Gamma_seed conflict alone does not prove positive nonfocal benefits; all 14 conflict rows are classified independently by the ledger.",
            "All 192 cells were constructed from one source model/trait grid and cannot supply ecological sampling uncertainty or evidence of population persistence.",
            "Genetic evolutionary suicide and island population floral decline are not tested."
        ]
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    d=run_all()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(d,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":d["status"],
        "all":d["externality_sign_counts_all"],
        "original_14":d["externality_sign_counts_in_original_14_conflicts"],
        "example":d["original_conflict_externalities"][0]
    },sort_keys=True))


if __name__=="__main__":
    main()
