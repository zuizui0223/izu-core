from __future__ import annotations

import importlib.util
import json
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V4_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v4_fixed_visit_budget.py"
SCREEN = ROOT / "data/design/world_island_replication_screen.json"
OUT = ROOT / "data/results/abm_v4_world_architecture_support.json"
SATURATION_VALUES = (1.0, 1.5, 2.0, 2.5, 3.0)
DEFAULT_LINEAGES = 16
DEFAULT_STEPS = 120


def load_v4():
    spec = importlib.util.spec_from_file_location("constraint_mechanism_abm_v4_support", V4_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def architecture_label(m, pollinators, lineages):
    if not pollinators:
        return "assurance_dominated"
    broad = sum(p.breadth >= 0.4 for p in pollinators) / len(pollinators)
    introduced = sum(p.introduced for p in pollinators) / len(pollinators)
    if introduced >= 0.5:
        return "novel_partner_replacement"
    if broad >= 0.5:
        return "complementary_or_redundant_generalism"
    best_ids = []
    for lin in lineages:
        scores = [m.encounter_score(lin, p) for p in pollinators]
        best_ids.append(max(range(len(scores)), key=scores.__getitem__))
    top_share = max(best_ids.count(i) for i in set(best_ids)) / len(best_ids)
    return "concentrated_dependency" if top_share >= 0.6 else "species_specific_mosaic"


def run_oceanic_with_architecture(
    m,
    seed: int,
    saturation: float,
    n_lineages: int = DEFAULT_LINEAGES,
    steps: int = DEFAULT_STEPS,
):
    s = m.scenarios()[1]
    rng = random.Random(seed)
    templates = m.make_lineages(random.Random(seed), n_lineages)
    lineages = [m.LineageState(template=t, trait=t.trait) for t in templates]
    pollinators = [m.make_pollinator(rng, s) for _ in range(s.n_pollinator_types)]
    for _ in range(steps):
        pollinators = [p for p in pollinators if rng.random() >= s.partner_loss]
        if rng.random() < s.partner_arrival:
            pollinators.append(m.make_pollinator(rng, s))
        for lin in lineages:
            scores = [m.encounter_score(lin, p) for p in pollinators]
            pollination = m.fixed_budget_pollination(scores, saturation)
            d = lin.template.pollinator_dependency
            autonomous = lin.template.assurance_ceiling * lin.assurance
            lin.reproduction = m.clamp(
                1.0 - (1.0 - d * pollination) * (1.0 - (1.0 - d) * autonomous)
            )
            if pollinators and pollination < 0.45:
                best = max(pollinators, key=lambda p: m.encounter_score(lin, p))
                lin.trait = m.clamp(
                    lin.trait + lin.template.trait_adjustment * (best.trait - lin.trait)
                )
            if lin.reproduction < 0.50:
                lin.assurance = min(
                    lin.template.assurance_ceiling,
                    lin.assurance + lin.template.assurance_responsiveness,
                )
    return architecture_label(m, pollinators, lineages)


def build_support(replicates: int = 200, seed: int = 20260819):
    m = load_v4()
    screen = json.loads(SCREEN.read_text())
    observed = sorted({x["architecture_macroclass"] for x in screen["systems"]})
    envelope = {}
    for saturation in SATURATION_VALUES:
        counts = Counter(
            run_oceanic_with_architecture(m, seed + i, saturation)
            for i in range(replicates)
        )
        generated = sorted(
            k for k, v in counts.items() if v > 0 and k != "assurance_dominated"
        )
        envelope[str(saturation)] = {
            "architecture_counts": dict(sorted(counts.items())),
            "observed_macroclasses_covered": sorted(set(observed) & set(generated)),
            "all_observed_macroclasses_covered": set(observed).issubset(generated),
        }
    robust = all(x["all_observed_macroclasses_covered"] for x in envelope.values())
    return {
        "analysis": "abm_v4_world_architecture_support_coverage",
        "observed_world_macroclasses": observed,
        "run_design": {
            "oceanic_runs_per_saturation": replicates,
            "lineages_per_run": DEFAULT_LINEAGES,
            "steps": DEFAULT_STEPS,
            "seed": seed,
            "saturation_values": list(SATURATION_VALUES),
        },
        "saturation_envelope": envelope,
        "test": "pass" if robust else "fail",
        "decision": (
            "v4_has_robust_generative_support_for_all_observed_world_architecture_macroclasses"
            if robust
            else "v4_lacks_support_for_at_least_one_observed_macroclass"
        ),
        "interpretation": "This is a necessary generative-adequacy check only: the same frozen oceanic mechanism can produce every architecture macroclass already observed in the world island screen across the whole saturation envelope. It does not predict which named archipelago should occupy which class.",
        "next_gate": "For prediction rather than support coverage, use source-native architecture inputs from training systems and leave one island system out at a time; never use the held-out system's reproductive outcome to choose its parameters.",
        "claim_boundary": "Architecture-class coverage is not a prevalence estimate and not system-specific prediction. Descriptive classifier thresholds are inherited from ABM v1 and are not refit to the world screen.",
    }


def main():
    OUT.write_text(json.dumps(build_support(), indent=2) + "\n")


if __name__ == "__main__":
    main()
