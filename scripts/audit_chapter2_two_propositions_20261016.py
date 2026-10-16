"""Read-only proof-scope gate for Model3 'precedence != necessity' and allele access.

Native Q1 fresh-founder zip artifacts are re-admitted using their original
source SHA manifest; no new evolution or changed biological assumptions.
The no-mutation allele-support theorem is mathematical, whereas the h-width
sensitivity rows actually have A mutation enabled and are NOT theorem trials.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from scripts.run_chapter2_q1_fresh_founders_20261016 import load_frozen
from scripts.summarize_chapter2_q1_fresh_founders_20261016 import (
    load_trace, null_gate, summarize, verify_complete,
)

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "docs/CHAPTER2_TWO_PROPOSITION_EVIDENCE_RECEIPT_20261016.json"
CONFIG = ROOT / "data/design/chapter2_q1_fresh_founder_generality_20261016.json"


def source_gate(root: Path = ROOT, receipt: dict | None = None) -> dict:
    """Recompute each cited historical count from its declared source file."""
    data = json.loads(RECEIPT.read_text()) if receipt is None else receipt
    if data["schema"] != "chapter2_two_propositions_original_evidence_v1":
        raise ValueError("Unknown proof evidence readout schema")
    historical = json.loads((root / data["original_same_mating_condition"]["source"]).read_text())
    old = data["original_same_mating_condition"]
    primary = historical["primary_sequence"]
    if (primary["setting"] != "assurance_cost"
            or primary["mutation_rate"] != .01
            or primary["counts"]["assurance_first"] != old["assurance_first"]["events"] != 51
            or historical["independent_visitor_histories"] != old["assurance_first"]["visitor_histories"] != 64):
        raise ValueError("Historical assurance precedence readout identity mismatch")
    if primary["assurance_first_bootstrap95"] != old["assurance_first"]["history_bootstrap95"]:
        raise ValueError("Historic assurance-first confidence interval drift")
    thresholds = {
        str(t["threshold"]): int(t["counts"]["assurance_first"])
        for t in historical["threshold_sensitivity"]
        if t["setting"] == "assurance_cost" and t["mutation_rate"] == .01
    }
    if thresholds != old["threshold_sensitivity"]["A_first_count_by_threshold"]:
        raise ValueError("Assurance-first threshold sensitivity no longer matches")
    # The 64-history fixed-A counterfactual is independently registered
    # in the SAME reproductive setting, not the same population histories.
    fixed = next(x for x in historical["fixed_assurance"] if (
        x["setting"]=="assurance_cost" and x["mutation_rate"]==.01
    ))
    if abs(fixed["far_minus_near_investment"]["mean"] -
           old["fixed_A_counterexample"]["mean_far_minus_near"]) > 1e-5:
        raise ValueError("Historical fixed-A investment response changed")

    source = json.loads((root / data["original_four_setting_shared_founder"]["source"]).read_text())
    old4 = data["original_four_setting_shared_founder"]
    if source["declared_cases"] != 8448 or source["independent_visitor_histories"] != 64:
        raise ValueError("Q1 original four-setting source denominator changed")
    for row in source["settings"]:
        name = row["setting"]
        if abs(row["fixed_far_minus_near"]["mean"]-old4["fixed_A_far_minus_near"][name])>1e-12:
            raise ValueError("Original source four-setting fixed-A contrast differs: "+name)
        if not row["passes_frozen_rule"]:
            raise ValueError("Original registered source success changed")

    boundary = data["allele_half_width_order_exploration"]
    raw_width = json.loads((root / boundary["source"]).read_text())
    if len(raw_width["rows"]) != boundary["source_rows"] != 36:
        raise ValueError("Genetic width source rows changed")
    for spec in boundary["halfw"]:
        group = [r for r in raw_width["rows"] if (
            r["allele_half_width"] == spec["h"] and
            r["threshold"] == boundary["threshold"]
        )]
        if len(group) != boundary["n_context_cells_per_width"]:
            raise ValueError("Incomplete original six founder-by-ecology cells")
        starts = sum(r["starts"] for r in group)
        reached = sum(r["reached_assurance_event"] for r in group)
        a = sum(r["categories"].get("assurance_first", 0) for r in group)
        i = sum(r["categories"].get("investment_first", 0) for r in group)
        if (starts != boundary["n_starts_per_width"] or
                reached != spec["assurance_event_reached"] or
                a != spec["assurance_first"] or
                i != spec["investment_first"] or
                any(not r["threshold_accessible_without_mutation"] for r in group) or
                any(abs(r["mutation_free_first_generation_assurance_variance"] -
                        (spec["h"] ** 2)/2) > 1e-14 for r in group) or
                abs((a-i)/starts-spec["all_start_D"])>1e-14):
            raise ValueError("Original h-width/threshold reachability or order calculation changed")
    access = data["support_loss"]
    allele = json.loads((root / access["source"]).read_text())
    losses = json.loads((root / access["last_loss_source"]).read_text())
    if (allele["cases"] != access["cases"] != losses["cases"] or
            allele["excluded_before_fixation"] != access["excluded_before_fixation"] != 703 or
            allele["excluded_with_expressed_variance"] != access[
                "excluded_before_fixation_with_positive_expressed_variance"] or
            losses["eligible_loss"] != access["first_exclusion_transitions"] != 1238 or
            losses["direction_counts"]["favouring_needed"] != access[
                "conditional_expected_low_I_allele_frequency_favouring_but_realized_zero"] != 315 or
            losses["direction_counts"]["opposing_needed"] != access[
                "conditional_expected_low_I_allele_frequency_opposing"] != 923):
        raise ValueError("Historical allele-access/last-loss evidence numerator changed")
    if allele["excluded_before_fixation"]-allele["missing_I_excluded_before_fixation"]!=1:
        raise ValueError("Prior achieved-I-event exclusion caveat disappeared")
    return {
        "historical_q1_first_crossing": primary["counts"]["assurance_first"],
        "historical_Q1_four_settings": len(source["settings"]),
        "source_bound_width_rows": len(raw_width["rows"]),
        "original_standing_access_histories": allele["cases"],
        "pre_fixation_exclusion": allele["excluded_before_fixation"],
        "loss_selected_transitions": losses["eligible_loss"],
        "favourably_weighted_but_realized_loss": losses["direction_counts"]["favouring_needed"],
        "evidence_level": "SOURCE_READOUT_CONSISTENT_NOT_INDEPENDENT_BIOLOGICAL_REEXECUTION",
    }


def fresh_founder_archive_gate(input_root: Path, reference: dict | None = None) -> dict:
    """Reread ALL full original NPZ receipts, then reconstruct fixed-A results."""
    data = json.loads(RECEIPT.read_text()) if reference is None else reference
    d, _ = load_frozen()
    paths = verify_complete(input_root, d)  # source manifest + per-NPZ SHA-256
    if len(paths) != data["fresh_founder_q1"]["original_32_shard_case_count"] != 1088:
        raise ValueError("Incomplete original independent-founder cohort")
    confirm = summarize(paths, d)
    if (confirm["adjudication"] != "fresh_founder_4setting_inconclusive"
            or not confirm["all_main_occupied"]
            or confirm["null_structural_gate"]["status"] != "passed"
            or confirm["null_structural_gate"]["matched_pairs"] != 32):
        raise ValueError("Original full 1088-path Q1 registered decision is different")
    rng = np.random.default_rng(d["bootstrap"]["seed"])
    count = d["bootstrap"]["draws"]
    fi = rng.integers(0,8,(count,8))
    vi = rng.integers(0,8,(count,8))
    record = []
    fslist=list(range(560201,560209))
    vslist=list(range(560301,560309))
    for row in data["fresh_founder_q1"]["settings"]:
        setting = row["setting"]
        near, far, delta, genomic = [], [], [], []
        for fs in fslist:
            nr, fr, dr, copies = [], [], [], []
            for vs in vslist:
                values=[]
                for arm in ("near","far"):
                    task=("main",setting,.01,fs,vs,560401,arm,"fixed")
                    alive, initial, end, genotype=load_trace(paths[task], d)
                    if not alive:
                        raise ValueError("Original 8-founder fixed-A case unexpectedly extinct")
                    values.append((initial,end,genotype))
                n,l=values
                if not np.array_equal(n[2],l[2]) or n[0]!=l[0]:
                    raise ValueError("Paired near/far originals must have same diploid founder")
                nr.append(n[1]);fr.append(l[1]);dr.append(l[1]-l[0]);copies.append(l[2].tobytes())
            near.append(nr);far.append(fr);delta.append(dr);genomic.append(copies)
        n=np.array(near);l=np.array(far);delta=np.array(delta)
        contrast=l-n
        ci=np.quantile(contrast[fi[:,:,None],vi[:,None,:]].mean(axis=(1,2)),[.025,.975])
        farci=np.quantile(delta[fi[:,:,None],vi[:,None,:]].mean(axis=(1,2)),[.025,.975])
        assertions={
            "fixed_far_minus_near_mean":float(contrast.mean()),
            "fixed_far_change_from_actual_founder_mean":float(delta.mean()),
            "negative_far_minus_near_cases":int((contrast<0).sum()),
            "negative_far_change_cases":int((delta<0).sum()),
            "negative_fixed_founder_means":int((contrast.mean(axis=1)<0).sum()),
        }
        for key,value in assertions.items():
            if abs(value-row[key])>1e-12:
                raise ValueError("Archived independently recomputed Q1 figure changed: "+key+" "+setting)
        np.testing.assert_allclose(ci,row["fixed_far_minus_near_bootstrap95"],atol=1e-12,rtol=0)
        np.testing.assert_allclose(farci,row["fixed_far_change_bootstrap95"],atol=1e-12,rtol=0)
        matching=next(x for x in confirm["settings"] if x["setting"]==setting)
        if abs(matching["D_mean"]-row["original_D"])>1e-12:
            raise ValueError("Original Q1 registered treatment-interaction D changed: "+setting)
        record.append({"setting":setting,**assertions,
                       "fixed_far_minus_near_bootstrap95":ci.tolist(),
                       "fixed_far_change_bootstrap95":farci.tolist()})
    return {
        "status":"ALL1088_ORIGINAL_GENOTYPE_ARCHIVES_WITH_MATCHED_FIXED_A_CONTRAST_RECOMPUTED",
        "source_run":38853989138,
        "admitted_cases":len(paths),
        "controls":confirm["null_structural_gate"]["matched_pairs"],
        "new_population_updates":0,
        "settings":record,
        "old_primary_D_adjudication":confirm["adjudication"],
        "claim_ceiling":"Retrospective 2-way crossed founder/history readback, no new biological simulation or proof of independent ecological operators",
    }


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-root",required=True,type=Path)
    parser.add_argument("--out",required=True,type=Path)
    opts=parser.parse_args()
    if opts.out.exists():
        raise FileExistsError("Refusing overwrite of evidence report")
    historic=source_gate()
    fresh=fresh_founder_archive_gate(opts.input_root)
    output={"historical":historic,"fresh_original_archive":fresh}
    opts.out.parent.mkdir(parents=True,exist_ok=True)
    opts.out.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":fresh["status"],"checked_case_count":fresh["admitted_cases"],
        "fixed_nonnecessity_far_decline":{r["setting"]:r["fixed_far_change_from_actual_founder_mean"] for r in fresh["settings"]},
        "width_order_contexts_checked":historic["source_bound_width_rows"],
        "all_predefined_Q1_D_unmodified":True,
    },ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
