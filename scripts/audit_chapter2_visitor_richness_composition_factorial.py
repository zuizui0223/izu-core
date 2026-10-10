"""Exploratory Model3 visitor-count versus functional-composition control.

Pure ephemeral reproductive-ledger intervention at a fixed source diploid
parental state, not a new visitor history or a demographic experiment. The
'four_clone' arm gives each of TWO unique visitor optima two independently
identified but functionally identical types. This is an exact *redundant-type*
negative control; four distinct types instead change functional composition.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import json
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_beta_gamma_seed_map import ledger_stats, state_of_clones
from scripts.audit_chapter2_investment_conflict_path_replay import actual_mixed_window
from scripts.model3_island.types import VisitorState
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config as source_config, load_design,
)

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_visitor_richness_composition_factorial_20261010.json"
STATUS = "EXPLORATORY_ORTHOGONAL_VISITOR_LEDGER_NEGATIVE_CONTROL_NOT_CONFIRMATORY"
OPTIMA = {
    "two_unique": (.15, .55),
    "four_clones": (.15, .15, .55, .55),
    "four_distinct": (.15, .35, .55, .75),
    "four_shifted": (.35, .55, .75, .95),
}
ACTIVITY = ("fixed", "count_scaled")
GENOTYPES = ("monomorphic", "mixed_diploid")


def contract():
    d = json.loads(DESIGN.read_text())
    if (d.get("status") != STATUS
            or d.get("visitor_optima") != {k: list(v) for k, v in OPTIMA.items()}
            or d.get("activity_modes") != list(ACTIVITY)
            or d.get("parental_states") != list(GENOTYPES)
            or d.get("N") != 8 or d.get("K") != 8 or d.get("B") != 48
            or d.get("classification_deadband") != .02):
        raise ValueError("visitor factorial exploratory contract changed")
    return d


def visitor(label):
    if label not in OPTIMA:
        raise ValueError("unregistered visitor intervention")
    o = np.asarray(OPTIMA[label], dtype=float)
    return VisitorState(
        ids=np.arange(500, 500 + len(o), dtype=np.int64),
        optima=o,
        breadths=np.full(len(o), .18),
        effectiveness=np.ones(len(o)),
    )


def parental_state(label):
    if label not in GENOTYPES:
        raise ValueError("unregistered parental state")
    state = state_of_clones((.2, .35, .35), 8)
    if label == "monomorphic":
        return state
    # Deliberate fixed, synthetic standing diploid variation (NOT a sampled
    # native pilot state). All alleles and all parental IDs remain unchanged
    # across visitor-context interventions.
    a = state.alleles.copy()
    shifts = np.array((-.055, -.035, -.020, -.008, .008, .020, .035, .055))
    a[:, 0, :] += shifts[:, None]
    a[:, 1, 0] += shifts
    a[:, 1, 1] -= .5 * shifts
    a[:, 2, 0] += .4 * shifts
    a[:, 2, 1] -= .2 * shifts
    return replace(state, alleles=a)


def config(activity_mode):
    if activity_mode not in ACTIVITY:
        raise ValueError("unregistered visitor activity law")
    return replace(
        source_config(load_design(DEFAULT_DESIGN), "delayed_control", 0.0,
                      "evolving"),
        capacity=8, ovule_budget=8., activity_mode=activity_mode,
        reference_visitor_count=4.,
    )


def readout(state, visitors, cfg):
    out = ledger_stats(state, visitors, cfg, 48)
    signs = actual_mixed_window(state, visitors, cfg)
    return {
        "total_viable_seed": out["total"],
        "maternal_outcross_seed": out["total_outcross"],
        "viable_self_seed": out["total_self"],
        "beta_focal_median": signs["focal_beta_median"],
        "gamma_log_collective": signs["gamma_collective_log_seed"],
        "beta_negative_n": signs["focal_beta_negative_count"],
        "gamma_positive": signs["gamma_positive"],
        "majority_beta_negative_gamma_positive": signs[
            "mixed_genotype_majority_conflict"
        ],
        "nonfocal_externality_positive_n": signs[
            "positive_nonneighbor_externality_focal_count"
        ],
    }


def contrasts(rows):
    idx = {(r["parental_state"], r["activity_mode"], r["visitor_arm"]): r
           for r in rows}
    out = []
    for genetic in GENOTYPES:
        for activity in ACTIVITY:
            base = idx[genetic, activity, "two_unique"]
            clone = idx[genetic, activity, "four_clones"]
            distinct = idx[genetic, activity, "four_distinct"]
            shifted = idx[genetic, activity, "four_shifted"]
            out.append({
                "parental_state": genetic,
                "activity_mode": activity,
                "redundant_type_count_2_to_4_total_seed_delta":
                    clone["total_viable_seed"] - base["total_viable_seed"],
                "novel_optima_at_same_four_count_seed_delta":
                    distinct["total_viable_seed"] - clone["total_viable_seed"],
                "shifted_optima_at_same_four_count_seed_delta":
                    shifted["total_viable_seed"] - distinct["total_viable_seed"],
                "redundant_type_count_conflict_flip":
                    clone["majority_beta_negative_gamma_positive"] !=
                    base["majority_beta_negative_gamma_positive"],
                "composition_at_same_count_conflict_flip":
                    distinct["majority_beta_negative_gamma_positive"] !=
                    clone["majority_beta_negative_gamma_positive"],
                "shift_at_same_count_conflict_flip":
                    shifted["majority_beta_negative_gamma_positive"] !=
                    distinct["majority_beta_negative_gamma_positive"],
            })
    return out


def run_all():
    d = contract()
    rows = []
    for genetic in GENOTYPES:
        state = parental_state(genetic)
        for mode in ACTIVITY:
            cfg = config(mode)
            for arm in OPTIMA:
                v = visitor(arm)
                rows.append({
                    "parental_state": genetic,
                    "activity_mode": mode,
                    "visitor_arm": arm,
                    "visitor_type_count": len(v.ids),
                    "distinct_optimum_count": len(set(v.optima.tolist())),
                    **readout(state, v, cfg),
                })
    # Formal negative control: for fixed activity and otherwise identical
    # visitor functions, duplicating each type MUST leave the ledger intact.
    idx = {(r["parental_state"], r["activity_mode"], r["visitor_arm"]): r
           for r in rows}
    for genetic in GENOTYPES:
        x = idx[genetic, "fixed", "two_unique"]
        y = idx[genetic, "fixed", "four_clones"]
        for field in ("total_viable_seed", "maternal_outcross_seed",
                      "viable_self_seed", "beta_focal_median",
                      "gamma_log_collective"):
            if not np.isclose(x[field], y[field], rtol=1e-9, atol=1e-10):
                raise AssertionError(f"redundant visitor negative control failed: {field}")
        if (x["beta_negative_n"] != y["beta_negative_n"] or
                x["majority_beta_negative_gamma_positive"] !=
                y["majority_beta_negative_gamma_positive"]):
            raise AssertionError("redundant visitor control changed classification")
    return {
        "status": STATUS, "source": "Model3 unchanged reproduce_kb; B=48",
        "design": d, "n_new_visitor_histories": 0,
        "n_real_island_population_samples": 0,
        "n_fixed_synthetic_diploid_states": 2,
        "rows": rows, "paired_same_genotype_contrasts": contrasts(rows),
        "negative_control_fixed_activity_duplicate_invariance": True,
        "scientific_boundary": (
            "All results are instantaneous finite-genotype source-ledger "
            "interventions, not independent histories, richness causal "
            "effects in nature, evolved allele trajectories or persistence."
        ),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    result = run_all()
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, sort_keys=True, indent=2,
                                allow_nan=False) + "\n")
    print(json.dumps({
        "status": result["status"],
        "negative_control_passed":
            result["negative_control_fixed_activity_duplicate_invariance"],
        "contrasts": result["paired_same_genotype_contrasts"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
