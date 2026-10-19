"""Read-only, post-outcome three-state editorial decomposition of confirm160.

This is *not* a new registered outcome, a new simulation, a confidence-interval
calculation, or independent ecological replication. Original primary G/S
estimands, cohort identities and source provenance remain authoritative.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/audits/CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json"


def derive(source):
    if (source.get("status") != "COMPLETE_MODEL_CONDITIONAL_CONFIRMATION"
            or source.get("independent_axes") != [160, 160]
            or source.get("crossings") != 25600
            or source.get("actual_restoration_tested") is not False):
        raise ValueError("wrong/incomplete confirm160 source")
    primary = source["primary"]
    if primary["familywise_alpha"] != .05 or primary["df"] != 159:
        raise ValueError("registered inferential convention changed")
    endpoints = {x["name"]: x for x in primary["endpoints"]}
    if set(endpoints) != {"genetic_loss", "survival_interaction"}:
        raise ValueError("primary endpoint inventory changed")
    n = source["crossings"]
    by_budget = {}
    for budget in ("B8", "B4p5"):
        arms = {}
        for policy in ("fixed", "evolving"):
            original = source["arms"][policy + "_" + budget]
            accessible = int(original["alive_accessible"])
            alive = int(original["alive"])
            closed = alive - accessible
            extinct = n - alive
            competing = [int(original["genetic_first"]),
                         int(original["extinction_first"]), accessible]
            if (not 0 <= accessible <= alive <= n
                    or min(competing) < 0 or sum(competing) != n
                    or closed < 0 or extinct < 0
                    or accessible + closed + extinct != n):
                raise ValueError("invalid current-state/competing-risk decomposition")
            if budget == "B8" and original["genetic_first"] != closed:
                raise ValueError("B8 full-survival access closure conflict")
            arms[policy] = {
                "alive_and_target_accessible": accessible,
                "alive_but_target_closed": closed,
                "extinct": extinct,
                "denominator": n,
                "percent_all_start": {
                    "alive_and_target_accessible": accessible * 100 / n,
                    "alive_but_target_closed": closed * 100 / n,
                    "extinct": extinct * 100 / n,
                },
            }
        d = (arms["evolving"]["alive_and_target_accessible"]
             - arms["fixed"]["alive_and_target_accessible"]) * 100 / n
        by_budget[budget] = {"arms": arms, "evolving_minus_fixed_accessible_alive_pp": d}
    by_budget["B4p5"]["evolving_minus_fixed_accessible_alive_pp"]
    diff = (by_budget["B4p5"]["evolving_minus_fixed_accessible_alive_pp"]
            - by_budget["B8"]["evolving_minus_fixed_accessible_alive_pp"])
    # Reg G is a first-event CIF only under B8, not final availability at B4p5.
    g = ((source["arms"]["evolving_B8"]["genetic_first"]
          - source["arms"]["fixed_B8"]["genetic_first"]) / n)
    s = (((source["arms"]["evolving_B4p5"]["alive"]
           - source["arms"]["fixed_B4p5"]["alive"])
          - (source["arms"]["evolving_B8"]["alive"]
             - source["arms"]["fixed_B8"]["alive"])) / n)
    if (abs(g - endpoints["genetic_loss"]["estimate"]) > 1e-12
            or abs(s - endpoints["survival_interaction"]["estimate"]) > 1e-12
            or abs(by_budget["B8"]["evolving_minus_fixed_accessible_alive_pp"]
                   + 100 * g) > 1e-12):
        raise ValueError("derived states disagree with registered G/S")
    return {
        "status": "POST_OUTCOME_DESCRIPTIVE_READONLY_NOT_REGISTERED",
        "source": "docs/audits/CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json",
        "n_founders": 160,
        "n_visitor_histories": 160,
        "crossed_cells_not_independent_islands": n,
        "endpoint": "P(alive and current maximum I allele reaches initial founder mean I at census 80)",
        "mutation_and_immigration_for_I": "absent in source experiment",
        "budgets": by_budget,
        "descriptive_budget_interaction_pp": diff,
        "registered_G_estimate": g,
        "registered_S_estimate": s,
        "new_uncertainty_estimated": False,
        "independent_confirmation": False,
        "limitations": [
            "Not a registered third primary endpoint; no new confidence interval, p value, or significance gate.",
            "B4p5 positive joint endpoint is largely shaped by differential extinction, not evidence that A directly preserves I alleles.",
            "B8 loss and B4p5 survival occur in different environments; neither mediation nor a biological SESOI is identified.",
            "Founder and visitor are 160 crossed axes, not 25600 independent island systems.",
            "Genetic upper support is only necessary, not sufficient for attained floral adaptation or recovery."
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    d = derive(json.loads(args.source.read_text(encoding="utf-8")))
    payload = json.dumps(d, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
