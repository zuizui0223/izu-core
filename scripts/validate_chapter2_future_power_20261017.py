"""Pre-execution source-bound power review for NEW Chapter2 confirmatory studies.

Do not apply retroactively to completed Q2 384; not biological authorization.
A GO here only permits independent method review before an explicit approval.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
from statistics import NormalDist

ROOT=Path(__file__).resolve().parents[1]
REGISTERED=ROOT/"docs/protocols"
FROZEN_Q2="ch2_q2_I_support_order_20261016"


def sha(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()


def mde_normal_proxy(var:dict,nf:int,nv:int,alpha:float,prob:float,k:int)->float:
    """Conservative joint discovery sensitivity proxy, NOT exact power."""
    if (nf<3 or nv<3 or k<1 or not 0<alpha<=.05
        or not .8<=prob<1 or set(var)!=set(("founder","visitor","interaction"))):
        raise ValueError("HOLD: invalid 2-axis/multiplicity settings")
    vv=list(var.values())
    if any(type(x) not in (int,float) or not math.isfinite(x) or x<0 for x in vv):
        raise ValueError("HOLD: variance cannot be negative/missing")
    v=var["founder"]/nf+var["visitor"]/nv+var["interaction"]/(nf*nv)
    critical=NormalDist().inv_cdf(1-alpha/(2*k))
    per_test_power=1-(1-prob)/k
    return float((critical+NormalDist().inv_cdf(per_test_power))*math.sqrt(v))


def evaluate(plan:dict,pilot:bytes)->dict:
    """Fail closed if power, provenance, independent axes or budget absent."""
    if (plan.get("schema")!="chapter2_future_crossed_power_contract_v1"
        or plan.get("status")!="PRE_EXECUTION_POWER_PLAN_NOT_EXECUTED"
        or plan.get("study_id") in (None,"",FROZEN_Q2)
        or plan.get("pilot_study_id") in (None,"",plan.get("study_id"))
        or plan.get("pilot_sha256")!=sha(pilot)
        or plan.get("pilot_precedes_registration") is not True
        or plan.get("pilot_cohort_nonoverlap_confirmed") is not True
        or not isinstance(plan.get("pilot_stream_namespace"),str)
        or not isinstance(plan.get("future_stream_namespace"),str)
        or not plan.get("pilot_stream_namespace")
        or not plan.get("future_stream_namespace")
        or plan["pilot_stream_namespace"]==plan["future_stream_namespace"]
        or plan.get("new_biological_runs_started") is not False
        or plan.get("endpoint_rule_frozen_before_new_outcomes") is not True
        or plan.get("finite_cost_budget_documented") is not True):
        raise ValueError("HOLD: independent pre-execution source/stream provenance missing")
    keys=("founder_count","visitor_history_count","number_of_environments",
          "number_of_policies","updates_per_case","declared_full_paths",
          "declared_total_updates","number_of_coprimary_outcomes")
    if any(type(plan.get(x)) is not int or plan[x]<1 for x in keys):
        raise ValueError("HOLD: missing crossed biological cases and budget")
    nf,nv,ne,np_,h,n,k=(plan[x] for x in keys)
    if nf<3 or nv<3 or n!=nf*nv*ne*np_ or n*h!=plan["declared_total_updates"]:
        raise ValueError("HOLD: mismatch in factorial cases/independent source axes")
    alpha=plan.get("familywise_alpha")
    power=plan.get("minimum_joint_directional_power")
    if (type(alpha) not in (int,float) or type(power) not in (int,float)
        or not 0<alpha<=.05 or not .8<=power<1):
        raise ValueError("HOLD: familywise alpha or minimum joint power missing")
    outcomes=plan.get("outcomes")
    if (not isinstance(outcomes,list) or len(outcomes)!=k
        or any(not isinstance(x,dict) or not x.get("name") for x in outcomes)
        or len(set(x["name"] for x in outcomes))!=k):
        raise ValueError("HOLD: require all distinct co-primary endpoints")
    for o in outcomes:
        sesoi=o.get("minimum_scientifically_meaningful_abs_effect")
        if (type(sesoi) not in (int,float) or not math.isfinite(sesoi)
            or not 0<sesoi<=2 or not str(o.get("sesoi_scientific_justification","")).strip()):
            raise ValueError("HOLD: meaningful effect and its preregistered rationale required")
    scenarios=plan.get("variance_uncertainty_scenarios")
    if (not isinstance(scenarios,list) or len(scenarios)!=2
        or any(not isinstance(x,dict) or not x.get("name") or
               not isinstance(x.get("by_endpoint"),dict) for x in scenarios)
        or {x["name"] for x in scenarios}!={"baseline","adverse"}):
        raise ValueError("HOLD: both baseline AND adverse scenario are mandatory")
    by={s["name"]:s["by_endpoint"] for s in scenarios}
    names={o["name"] for o in outcomes}
    if any(set(p)!=names for p in by.values()):
        raise ValueError("HOLD: endpoint-specific variance scenarios incomplete")
    all_pass=True
    checks={}
    for sname,scenario in by.items():
        checks[sname]={}
        for endpoint in outcomes:
            key=endpoint["name"]
            b=by["baseline"][key]
            worst=by["adverse"][key]
            if (set(b)!={"founder","visitor","interaction"}
                or set(worst)!={"founder","visitor","interaction"}
                or any(type(b[x]) not in (int,float) or type(worst[x]) not in (int,float)
                       or b[x]<0 or worst[x]<b[x] for x in b)):
                raise ValueError("HOLD: missing or non-adverse variance components")
            md=mde_normal_proxy(scenario[key],nf,nv,alpha,power,k)
            is_possible=endpoint["minimum_scientifically_meaningful_abs_effect"]>=md
            checks[sname][key]={
                "SESOI":endpoint["minimum_scientifically_meaningful_abs_effect"],
                "MDE_proxy":md,"adequate_proxy":bool(is_possible)}
            all_pass=all_pass and is_possible
    return {
        "status":"GO_FOR_METHOD_REVIEW_NOT_EXECUTION" if all_pass else "HOLD_PRECISION_INADEQUATE",
        "design_cases":n,"design_updates":n*h,
        "all_endpoints_all_scenarios_adequate_proxy":bool(all_pass),
        "source_pilot_sha256":sha(pilot),
        "execution_authorized":False,
        "method":"Two-axis variance proxy and Bonferroni/union-bound joint >=80% directional probability; not exact power. Simulate operating characteristics separately if outcome distributions invalidate Normal approximation.",
        "checks":checks}


def validate_registry(directory:Path=REGISTERED)->dict:
    """Only NEW files with reserved name opt into mandatory CI registration."""
    names=sorted(Path(directory).glob("chapter2_future_registered_*.json"))
    statuses={}
    for path in names:
        plan=json.loads(path.read_text(encoding="utf-8"))
        pilot_ref=plan.get("pilot_source_repo_path")
        if (not isinstance(pilot_ref,str)
            or not pilot_ref.startswith("docs/")
            or ".." in Path(pilot_ref).parts):
            raise ValueError("HOLD: pilot must be declared by safe tracked repository path")
        pilot=ROOT/pilot_ref
        if not pilot.is_file():
            raise ValueError("HOLD: pilot data file missing")
        result=evaluate(plan,pilot.read_bytes())
        if result["status"]!="GO_FOR_METHOD_REVIEW_NOT_EXECUTION":
            raise ValueError("HOLD: underpowered confirmatory registration "+path.name)
        statuses[path.name]=result["status"]
    return {"status":"PASS_NO_NEW_STUDIES" if not names else "PASS_ALL_NEW_POWER_CONTRACTS",
            "registered_new_power_contracts":len(names),"per_protocol":statuses}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--plan",type=Path)
    p.add_argument("--pilot",type=Path)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    if a.out.exists():p.error("Refuse overwrite of source-bound audit")
    if a.plan:
        if not a.pilot:p.error("--pilot is required with --plan")
        result=evaluate(json.loads(a.plan.read_text(encoding="utf-8")),a.pilot.read_bytes())
    else:result=validate_registry()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"out":str(a.out)}))
if __name__=="__main__":
    main()
