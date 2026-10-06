"""Admission and recomputation of frozen joint-syndrome result records."""
import json
import math
from pathlib import Path

from scripts.run_model3_joint_syndrome_finite_followup import _classify, _summarize_start

ROOT = Path(__file__).resolve().parents[1]


def validate_selection(selection):
    price = selection.get("exact_multivariate_price", {})
    error = price.get("max_abs_error", float("inf"))
    if (price.get("passed") is not True or price.get("cells") != 48
            or not isinstance(error, (int, float)) or isinstance(error, bool) or not math.isfinite(error)
            or error > 1e-12):
        raise ValueError("Price validation failed or incomplete")
    response = selection.get("full_G_beta_response")
    if not isinstance(response, dict) or response.get("cells") != 48:
        raise ValueError("missing or incomplete response validation")
    passed = response.get("frozen_gate_pass_cells")
    if not isinstance(passed, int) or isinstance(passed, bool) or not 0 <= passed <= 48:
        raise ValueError("invalid response pass count")
    # No new tolerated-failure fraction is introduced after observing 46/48.
    return passed == 48


def validate_finite(result, design):
    """Check all raw pairs, then reconstruct eligibility, classes and summaries."""
    if not isinstance(result.get("records"), list):
        raise ValueError("finite records missing")
    bridge = json.loads((ROOT / design["source_bridge"]).read_text(encoding="utf-8"))
    history_ids = set(bridge["history_seeds"])
    seeds = set(design["demographic_seeds"])
    starts = {x["id"]: x for x in design["initial_states"]}
    records = result["records"]
    if len(records) != len(starts) or {r["initial_state"]["id"] for r in records} != set(starts):
        raise ValueError("initial-state set incomplete")
    expected_cases = len(starts)*len(history_ids)*len(seeds)*2
    if result.get("cases") != expected_cases:
        raise ValueError("case count differs from frozen design")
    occupied = []
    summaries = {}
    for rec in records:
        st = rec["initial_state"]
        if st != starts[st["id"]]:
            raise ValueError("initial-state values differ")
        histories = rec["histories"]
        if len(histories) != len(history_ids) or {h["history_seed"] for h in histories} != history_ids:
            raise ValueError("history set incomplete")
        rebuilt = []
        for h in histories:
            pairs = h["per_repeat"]
            if len(pairs) != len(seeds) or {p["demographic_seed"] for p in pairs} != seeds:
                raise ValueError("demographic repeats incomplete")
            differences = []
            for pair in pairs:
                arm_alive = []
                for arm in ("near", "far"):
                    i, a = pair[arm+"_investment"], pair[arm+"_assurance"]
                    if (i is None) != (a is None):
                        raise ValueError("inconsistent missing endpoint")
                    alive = i is not None
                    if alive and any(not isinstance(v,(int,float)) or isinstance(v,bool)
                                     or not math.isfinite(v) or not 0 <= v <= 1 for v in (i,a)):
                        raise ValueError("invalid endpoint")
                    occupied.append(alive)
                    arm_alive.append(alive)
                if pair["paired_occupied"] is not all(arm_alive):
                    raise ValueError("occupancy flag inconsistent")
                if all(arm_alive):
                    differences.append((pair["far_investment"]-pair["near_investment"],
                                        pair["far_assurance"]-pair["near_assurance"]))
            eligible = len(differences)==len(seeds)
            di = sum(x[0] for x in differences)/len(seeds) if eligible else None
            da = sum(x[1] for x in differences)/len(seeds) if eligible else None
            klass = _classify(di,da) if eligible else None
            if h["eligible"] is not eligible or h["class"] != klass:
                raise ValueError("endpoint classification inconsistent")
            for key,value in (("far_minus_near_investment",di),("far_minus_near_assurance",da)):
                original=h[key]
                if (original is None)!=(value is None) or (value is not None and not math.isclose(original,value,abs_tol=1e-12,rel_tol=0)):
                    raise ValueError("history mean inconsistent")
            rebuilt.append(dict(h, eligible=eligible, **{"class": klass}))
        summary = _summarize_start(rebuilt,design["branching"]["split_halves"])
        if summary != result["summary_by_initial_state"][st["id"]]:
            raise ValueError("summary inconsistent with records")
        summaries[st["id"]] = summary
    occupancy = sum(occupied)/len(occupied)
    if not math.isclose(occupancy,result["terminal_occupancy_fraction_all_trajectories"],abs_tol=1e-12,rel_tol=0):
        raise ValueError("overall occupancy inconsistent")
    any_branch = any(s["history_branching"] for s in summaries.values())
    any_rep = any(s["history_branching"] and s["split_half_agreement_gate_pass"] for s in summaries.values())
    if result["any_history_branching"] is not any_branch or result["any_reproducible_history_branching"] is not any_rep:
        raise ValueError("branching flag inconsistent")
    return summaries
