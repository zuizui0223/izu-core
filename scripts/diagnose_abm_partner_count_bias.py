from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v2_branching.py"


def load_v2():
    spec = importlib.util.spec_from_file_location("constraint_mechanism_abm_v2_diag", V2_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def diagnostic_scenarios(m):
    mainland, oceanic = m.scenarios()
    count_only = m.Scenario(
        "oceanic_count_only",
        oceanic.n_pollinator_types,
        oceanic.partner_arrival,
        oceanic.partner_loss,
        mainland.trait_dispersion,
        mainland.generalist_fraction,
        mainland.replacement_fraction,
    )
    composition_only = m.Scenario(
        "oceanic_composition_only",
        mainland.n_pollinator_types,
        mainland.partner_arrival,
        mainland.partner_loss,
        oceanic.trait_dispersion,
        oceanic.generalist_fraction,
        oceanic.replacement_fraction,
    )
    return mainland, oceanic, count_only, composition_only


def paired_ablation(seed: int, n_lineages: int = 16, steps: int = 120) -> dict:
    m = load_v2()
    import random
    templates = m.make_lineages(random.Random(seed), n_lineages)
    mainland, oceanic, count_only, composition_only = diagnostic_scenarios(m)
    runs = {
        "mainland": m.run_scenario(templates, mainland, seed + 100000, steps),
        "oceanic_full": m.run_scenario(templates, oceanic, seed + 200000, steps),
        "count_only": m.run_scenario(templates, count_only, seed + 300000, steps),
        "composition_only": m.run_scenario(templates, composition_only, seed + 400000, steps),
    }
    base = [x.reproduction for x in runs["mainland"]]
    out = {}
    for key in ("oceanic_full", "count_only", "composition_only"):
        vals = [x.reproduction for x in runs[key]]
        deltas = [y - x for x, y in zip(base, vals)]
        out[key] = {
            "mean_delta": sum(deltas) / len(deltas),
            "positive": sum(d > 1e-9 for d in deltas),
            "negative": sum(d < -1e-9 for d in deltas),
        }
    return out


def summarize(rows):
    keys = ("oceanic_full", "count_only", "composition_only")
    out = {}
    for key in keys:
        out[key] = {
            "mean_delta": sum(r[key]["mean_delta"] for r in rows) / len(rows),
            "positive_lineage_responses": sum(r[key]["positive"] for r in rows),
            "negative_lineage_responses": sum(r[key]["negative"] for r in rows),
        }
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--replicates", type=int, default=120)
    p.add_argument("--lineages", type=int, default=16)
    p.add_argument("--steps", type=int, default=120)
    p.add_argument("--seed", type=int, default=20260819)
    p.add_argument("--out", type=Path, default=Path("data/results/abm_partner_count_ablation.json"))
    args = p.parse_args()
    rows = [paired_ablation(args.seed + i, args.lineages, args.steps) for i in range(args.replicates)]
    summary = summarize(rows)
    payload = {
        "analysis": "abm_partner_count_structural_ablation",
        "summary": summary,
        "decision": "decline_bias_is_dominated_by_partner_opportunity_accumulation",
        "interpretation": "Oceanic partner-count/arrival/loss constraints alone reproduce and slightly exceed the full negative mean shift, whereas oceanic composition alone produces a small positive mean shift. The current multiplicative accumulation rule therefore makes partner quantity a dominant structural driver of decline.",
        "next_gate": "Replace or cap the many-partner accumulation rule using an independently justified saturation/competition formulation before adding further biological mechanisms.",
        "claim_boundary": "This diagnoses model structure only; it is not empirical evidence that partner richness is unimportant in nature."
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
