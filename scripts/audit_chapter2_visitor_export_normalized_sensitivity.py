"""Model3 visitor optimum-shift effect after matching total pollen export.

Exploratory POST-DISCOVERY source-operator sensitivity, not independent
visitor histories, not reproductive selection over time, not field islands.
All parent genotypes, visitor IDs, functional breadth/effectiveness and
N/K/B remain fixed *within each three-arm comparison*. The shifted arm's
activity may be rescaled by a deterministic scalar root to match baseline
total source pollen export. No original Model3 biology is edited.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import json
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from scripts.audit_chapter2_beta_gamma_seed_map import ledger_stats
from scripts.audit_chapter2_investment_conflict_path_replay import actual_mixed_window
from scripts.audit_chapter2_visitor_richness_composition_factorial import (
    config as baseline_config, parental_state,
)
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.model3_island.types import VisitorState

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_visitor_export_normalized_sensitivity_20261010.json"
STATUS = "EXPLORATORY_PRE_RESULT_SENSITIVITY_AFTER_PR452_POSITIVE_DISCOVERY"
GENOTYPES = ("monomorphic", "mixed_diploid")
MATCHING = (.2, .5, .8)
BREADTH = (.12, .18, .30)
EFFECTIVENESS = (.5, 1.)
REFERENCE = (.15, .35, .55, .75)
SHIFTED = (.35, .55, .75, .95)
ARMS = ("reference_original_activity", "shifted_original_activity",
        "shifted_export_matched")

ORIGINAL_RESULTS = {
    "monomorphic": {
        "reference_original_activity": (11.992565534924456, -0.063173669540878, 0.15822876051396761),
        "shifted_original_activity": (10.882505800430955, -0.2731145042262406, -0.2117876747791847),
    },
    "mixed_diploid": {
        "reference_original_activity": (11.931506679026661, -0.06868910508269488, 0.14050823583708905),
        "shifted_original_activity": (10.888561409910444, -0.2717145450920999, -0.2102057069211849),
    },
}


def contract():
    d = json.loads(DESIGN.read_text())
    if (d.get("status") != STATUS
            or d.get("parental_states") != list(GENOTYPES)
            or d.get("parent_matching_means") != list(MATCHING)
            or d.get("visitor_breadths") != list(BREADTH)
            or d.get("visitor_effectiveness") != list(EFFECTIVENESS)
            or d.get("fixed_visitor_optima") != list(REFERENCE)
            or d.get("shifted_visitor_optima") != list(SHIFTED)
            or d.get("comparison_arms") != list(ARMS)
            or d.get("expected_rows") != 108
            or d.get("total_matched_blocks") != 36
            or d.get("activity_mode") != "fixed"
            or d.get("source_reference_activity") != .4
            or d.get("K") != 8 or d.get("B") != 48):
        raise ValueError("source visitor-export sensitivity contract altered")
    return d


def parent(label, matching):
    if label not in GENOTYPES or matching not in MATCHING:
        raise ValueError("unregistered three-locus genotype source state")
    original = parental_state(label)
    a = original.alleles.copy()
    a[:, 0, :] += matching - .2
    return replace(original, alleles=a)


def visitor(optima, breadth, effectiveness):
    if (tuple(optima) not in (REFERENCE, SHIFTED)
            or breadth not in BREADTH
            or effectiveness not in EFFECTIVENESS):
        raise ValueError("unregistered visitor parameter")
    return VisitorState(
        ids=np.arange(600, 604, dtype=np.int64),
        optima=np.array(optima, dtype=float),
        breadths=np.full(4, breadth),
        effectiveness=np.full(4, effectiveness),
    )


def pollen_export_total(state, v, cfg, activity):
    ledger = reproduce_kb(
        state, v, replace(cfg, activity=float(activity)),
        background_denominator_capacity=48,
    )
    return float(ledger.exported.sum())


def activity_for_matching_export(state, shifted, cfg, reference_export):
    if not reference_export > 0:
        raise ValueError("positive reference pollen export required")
    hi = max(1., cfg.activity)
    while pollen_export_total(state, shifted, cfg, hi) < reference_export:
        hi *= 2.
        if hi > 1e6:
            raise RuntimeError("unattainable total pollen-export matching target")
    x = brentq(
        lambda value: pollen_export_total(state, shifted, cfg, value) -
                      reference_export,
        0., hi, xtol=1e-12, rtol=1e-12,
    )
    error = pollen_export_total(state, shifted, cfg, x) - reference_export
    if not np.isfinite(x) or x < 0 or abs(error) > 1e-8:
        raise AssertionError("failed to hold total pollen export equal")
    return float(x), float(error)


def row(state, visitors, cfg, *, parent_label, matching, breadth, effectiveness,
        arm, activity):
    adjusted = replace(cfg, activity=float(activity))
    ledger = reproduce_kb(
        state, visitors, adjusted, background_denominator_capacity=48
    )
    s = ledger_stats(state, visitors, adjusted, 48)
    g = actual_mixed_window(state, visitors, adjusted)
    return {
        "parental_state": parent_label, "parent_matching_mean": matching,
        "visitor_breadth": breadth, "visitor_effectiveness": effectiveness,
        "visitor_arm": arm, "activity": float(activity),
        "n_parent": len(state.ids), "n_visitor_types": len(visitors.ids),
        "total_pollen_export": float(ledger.exported.sum()),
        "total_pollen_delivered": float(ledger.delivered.sum()),
        "total_viable_seed": s["total"],
        "maternal_outcross_viable_seeds": s["total_outcross"],
        "viable_self_seeds": s["total_self"],
        "focal_beta_median": g["focal_beta_median"],
        "collective_gamma_log_seed": g["gamma_collective_log_seed"],
        "n_focal_beta_negative": g["focal_beta_negative_count"],
        "beta_negative_gamma_positive_conflict":
            g["mixed_genotype_majority_conflict"],
    }


def run_all():
    d = contract()
    rows, contrasts = [], []
    for label in GENOTYPES:
        for matching in MATCHING:
            s = parent(label, matching)
            for breadth in BREADTH:
                for effectiveness in EFFECTIVENESS:
                    cfg = baseline_config("fixed")
                    if cfg.activity != d["source_reference_activity"]:
                        raise AssertionError("source fixed activity changed")
                    ref = visitor(REFERENCE, breadth, effectiveness)
                    shift = visitor(SHIFTED, breadth, effectiveness)
                    target = pollen_export_total(s, ref, cfg, cfg.activity)
                    matched, error = activity_for_matching_export(s, shift, cfg, target)
                    base = row(s, ref, cfg, parent_label=label, matching=matching,
                               breadth=breadth, effectiveness=effectiveness,
                               arm=ARMS[0], activity=cfg.activity)
                    raw = row(s, shift, cfg, parent_label=label, matching=matching,
                              breadth=breadth, effectiveness=effectiveness,
                              arm=ARMS[1], activity=cfg.activity)
                    corrected = row(s, shift, cfg, parent_label=label, matching=matching,
                                    breadth=breadth, effectiveness=effectiveness,
                                    arm=ARMS[2], activity=matched)
                    if abs(corrected["total_pollen_export"] -
                           base["total_pollen_export"]) > 1e-8:
                        raise AssertionError("export volume differs after matching")
                    for v in (base, raw, corrected):
                        if (v["n_parent"] != 8 or v["n_visitor_types"] != 4 or
                                not np.isfinite(v["collective_gamma_log_seed"])):
                            raise AssertionError("source state or gradient invalid")
                    if matching == .2 and breadth == .18 and effectiveness == 1.:
                        for arm, row_value in ((ARMS[0], base), (ARMS[1], raw)):
                            total, beta, gamma = ORIGINAL_RESULTS[label][arm]
                            np.testing.assert_allclose(
                                (row_value["total_viable_seed"],
                                 row_value["focal_beta_median"],
                                 row_value["collective_gamma_log_seed"]),
                                (total, beta, gamma), atol=1e-9, rtol=1e-9,
                            )
                    rows.extend((base, raw, corrected))
                    contrasts.append({
                        "parental_state": label, "parent_matching_mean": matching,
                        "visitor_breadth": breadth,
                        "visitor_effectiveness": effectiveness,
                        "export_match_activity": matched,
                        "export_match_error": error,
                        "raw_export_delta": raw["total_pollen_export"] -
                                            base["total_pollen_export"],
                        "corrected_export_delta": corrected["total_pollen_export"] -
                                                  base["total_pollen_export"],
                        "raw_viable_seed_delta": raw["total_viable_seed"] -
                                                base["total_viable_seed"],
                        "corrected_viable_seed_delta": corrected["total_viable_seed"] -
                                                      base["total_viable_seed"],
                        "raw_conflict_flip": raw["beta_negative_gamma_positive_conflict"] !=
                                             base["beta_negative_gamma_positive_conflict"],
                        "corrected_conflict_flip": corrected["beta_negative_gamma_positive_conflict"] !=
                                                   base["beta_negative_gamma_positive_conflict"],
                        "base_conflict": base["beta_negative_gamma_positive_conflict"],
                        "raw_shift_conflict": raw["beta_negative_gamma_positive_conflict"],
                        "corrected_shift_conflict": corrected["beta_negative_gamma_positive_conflict"],
                    })
    if len(rows) != 108 or len(contrasts) != 36:
        raise AssertionError("missing prospective exploratory cells")
    return {
        "status": STATUS, "design": d, "source": "canonical Model3 reproduce_kb",
        "n_visitor_histories": 0, "n_real_islands": 0,
        "n_synthetic_parent_fixture_settings": 36,
        "n_rows": len(rows), "rows": rows,
        "within_fixture_paired_contrasts": contrasts,
        "max_abs_corrected_export_difference": max(
            abs(x["corrected_export_delta"]) for x in contrasts
        ),
        "source_16_condition_fixture_parity": True,
        "scientific_boundary": (
            "Instant source ledger only. Matching total exported pollen is "
            "not matching visitation, deposited pollen, paternal parentage "
            "or maternal seed success. Source activity-normalization is "
            "a forced numerical intervention, not natural causal mediation."
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
        "status": result["status"], "n_rows": result["n_rows"],
        "n_matched_blocks": len(result["within_fixture_paired_contrasts"]),
        "max_abs_corrected_export_difference":
            result["max_abs_corrected_export_difference"],
        "raw_conflict_flips": sum(x["raw_conflict_flip"] for x in
                                  result["within_fixture_paired_contrasts"]),
        "export_normalized_conflict_flips": sum(
            x["corrected_conflict_flip"] for x in
            result["within_fixture_paired_contrasts"]),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
