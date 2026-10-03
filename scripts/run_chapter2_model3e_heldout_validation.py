"""Held-out H2/H4 validation for frozen Model 3E H1/H3-selected parameter sets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from threadpoolctl import threadpool_limits

from scripts.model3_island.density import make_grid
from scripts.model3e_empirical import make_stratum_context
from scripts.run_chapter2_model3e_empirical_screening import (
    _run_pseudo_island,
    _standardized_log_distance,
    _to_params,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/design/chapter2_model3e_empirical_screening_20261003.json"
DEFAULT_TARGETS = ROOT / "data/design/chapter2_model3e_chapter1_empirical_targets_20261003.json"
DEFAULT_SCREENING = ROOT / "data/results/chapter2_model3e_h1_h3_screening_20261003.json"


def _coef(y, columns) -> np.ndarray:
    y = np.asarray(y, dtype=float)
    X = np.column_stack([np.ones(len(y)), *[np.asarray(c, dtype=float) for c in columns]])
    if not np.isfinite(y).all() or not np.isfinite(X).all():
        raise ValueError("held-out regression contains non-finite values")
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta


def _simulate_rows(design: dict, accepted: dict, contexts: dict, grid) -> list[dict]:
    params = _to_params(accepted["params"])
    xmap = _standardized_log_distance(design["pseudo_islands"]["distances"])
    rows = []
    for stratum in design["pseudo_islands"]["strata"]:
        for distance in design["pseudo_islands"]["distances"]:
            for history_seed in design["pseudo_islands"]["history_seeds"]:
                row = _run_pseudo_island(
                    design,
                    params,
                    contexts[stratum],
                    stratum=stratum,
                    distance=float(distance),
                    history_seed=int(history_seed),
                    x_distance=xmap[float(distance)],
                    grid=grid,
                )
                if not row["defined"]:
                    raise ValueError(
                        f"accepted parameter set became undefined in held-out rerun: {accepted['parameter_id']}"
                    )
                rows.append(row)
    return rows


def _h2(rows: list[dict], design: dict) -> dict:
    out = {}
    for stratum in design["pseudo_islands"]["strata"]:
        rr = [r for r in rows if r["stratum"] == stratum]
        x = [r["x_distance"] for r in rr]
        a = [r["assurance"] for r in rr]
        g = [r["accessibility"] for r in rr]
        d = [r["display_dulling"] for r in rr]
        assurance_beta = float(_coef(a, [x])[1])
        accessibility_beta = float(_coef(g, [x, a])[1])
        display_beta = float(_coef(d, [x, a])[1])
        out[stratum] = {
            "selfing_core_proxy_isolation_beta": assurance_beta,
            "accessibility_given_assurance_isolation_beta": accessibility_beta,
            "display_dulling_given_assurance_isolation_beta": display_beta,
        }
    return out


def _h4(rows: list[dict], design: dict) -> dict:
    strata = list(design["pseudo_islands"]["strata"])
    y = [r["pollen_limitation"] for r in rows]
    x = [r["x_distance"] for r in rows]
    dummies = [
        [1.0 if r["stratum"] == s else 0.0 for r in rows]
        for s in strata[1:]
    ]
    assurance = [r["assurance"] for r in rows]
    accessibility = [r["accessibility"] for r in rows]
    beta = _coef(y, [x, *dummies, assurance, accessibility])
    assurance_idx = 2 + len(dummies)
    accessibility_idx = assurance_idx + 1
    return {
        "distance_beta": float(beta[1]),
        "assurance_beta": float(beta[assurance_idx]),
        "accessibility_beta": float(beta[accessibility_idx]),
    }


def _diagnostics(h2: dict, h4: dict, targets: dict) -> dict:
    strata = list(h2)
    target_h2 = targets["held_out_targets"]["H2_all_analysis"]
    access_model = np.asarray(
        [h2[s]["accessibility_given_assurance_isolation_beta"] for s in strata],
        dtype=float,
    )
    access_target = np.asarray(
        [target_h2[s]["accessibility_given_selfing"] for s in strata],
        dtype=float,
    )
    display_model = np.asarray(
        [h2[s]["display_dulling_given_assurance_isolation_beta"] for s in strata],
        dtype=float,
    )
    display_target = np.asarray(
        [target_h2[s]["plain_colour_given_selfing"] for s in strata],
        dtype=float,
    )
    h4_target = targets["held_out_targets"]["H4_exact_H2_score"]

    access_positive = {s: bool(h2[s]["accessibility_given_assurance_isolation_beta"] > 0) for s in strata}
    display_sign_match = {
        s: bool(
            np.sign(h2[s]["display_dulling_given_assurance_isolation_beta"])
            == np.sign(target_h2[s]["plain_colour_given_selfing"])
        )
        for s in strata
    }
    pass_h2 = bool(
        sum(access_positive.values()) >= 3
        and access_positive.get("northern_high_latitude", False)
        and access_positive.get("tropical", False)
    )
    pass_h4 = bool(h4["assurance_beta"] < 0 and h4["accessibility_beta"] < 0)

    return {
        "h2_access_positive_by_stratum": access_positive,
        "h2_access_positive_count": int(sum(access_positive.values())),
        "h2_display_sign_match_by_stratum": display_sign_match,
        "h2_display_sign_match_count": int(sum(display_sign_match.values())),
        "h2_access_vector_correlation": (
            None
            if np.std(access_model) == 0 or np.std(access_target) == 0
            else float(np.corrcoef(access_model, access_target)[0, 1])
        ),
        "h2_display_vector_correlation": (
            None
            if np.std(display_model) == 0 or np.std(display_target) == 0
            else float(np.corrcoef(display_model, display_target)[0, 1])
        ),
        "h4_target_assurance_beta": float(h4_target["assurance_on_current_pollen_limitation"]),
        "h4_target_accessibility_beta": float(h4_target["accessibility_on_current_pollen_limitation"]),
        "h4_assurance_negative": bool(h4["assurance_beta"] < 0),
        "h4_accessibility_negative": bool(h4["accessibility_beta"] < 0),
        "parameter_set_success": bool(pass_h2 and pass_h4),
    }


def run(design: dict, targets: dict, screening: dict) -> dict:
    if screening["status"] != "complete_first_model3e_h1_h3_screening":
        raise ValueError("held-out validation requires the frozen first screening result")
    if screening.get("held_out_H2_H4_opened") is not False:
        raise ValueError("screening result must document that H2/H4 were unopened")
    accepted = screening["accepted_parameter_sets"]
    if [r["parameter_id"] for r in accepted] != screening["accepted_parameter_ids"]:
        raise ValueError("accepted parameter ordering changed")

    contexts = {
        s: make_stratum_context(design, s)
        for s in design["pseudo_islands"]["strata"]
    }
    if contexts != screening["contexts"]:
        raise ValueError("prospective stratum contexts changed before held-out validation")
    grid = make_grid(design["common_operator"]["grid_axes"])

    results = []
    with threadpool_limits(limits=1):
        for item in accepted:
            rows = _simulate_rows(design, item, contexts, grid)
            h2 = _h2(rows, design)
            h4 = _h4(rows, design)
            diag = _diagnostics(h2, h4, targets)
            results.append(
                {
                    "parameter_id": item["parameter_id"],
                    "training_score": item["score"],
                    "h2": h2,
                    "h4": h4,
                    "diagnostics": diag,
                }
            )

    success_ids = [
        r["parameter_id"]
        for r in results
        if r["diagnostics"]["parameter_set_success"]
    ]
    best_id = screening["accepted_parameter_ids"][0]
    overall = bool(len(success_ids) >= 3 and best_id in success_ids)
    return {
        "status": "complete_model3e_heldout_H2_H4_validation",
        "screening_result": "data/results/chapter2_model3e_h1_h3_screening_20261003.json",
        "held_out_H2_H4_opened": True,
        "n_frozen_parameter_sets": len(results),
        "parameter_results": results,
        "successful_parameter_ids": success_ids,
        "n_successful_parameter_sets": len(success_ids),
        "best_training_parameter_id": best_id,
        "best_training_parameter_passes": best_id in success_ids,
        "overall_heldout_success": overall,
        "success_rule": design["held_out"]["overall_success"],
        "display_role": design["held_out"]["display_role"],
        "claim_boundary": targets["claim_boundary"],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--design", default=str(DEFAULT_DESIGN))
    p.add_argument("--targets", default=str(DEFAULT_TARGETS))
    p.add_argument("--screening", default=str(DEFAULT_SCREENING))
    p.add_argument("--out")
    a = p.parse_args()
    design = json.loads(Path(a.design).read_text(encoding="utf-8"))
    targets = json.loads(Path(a.targets).read_text(encoding="utf-8"))
    screening = json.loads(Path(a.screening).read_text(encoding="utf-8"))
    result = run(design, targets, screening)
    encoded = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if a.out:
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
