"""Rare-mutant joint selection-vector audit for Model 3.

Selection on reproductive assurance is evaluated through invasion fitness.
For a rare mutant m in a monomorphic resident r,

    w_m = 0.5 F_m + 0.5 P_m + S_m,

where F_m is mutant maternal outcross seed, P_m is mutant paternal outcross
success on resident mothers, and S_m is viable selfed seed. A selfed seed
carries both maternal and paternal copies from the focal parent and therefore
counts as one full parental-genome equivalent.

The resident pollen pool and resident female return are held fixed to first
order in mutant frequency. Gradients are central derivatives of log(w_m)
with mutant traits varied while resident traits remain fixed.

Decision rules are frozen in
data/design/model3_joint_syndrome_rare_mutant_20261004.json.
"""
from __future__ import annotations

from dataclasses import replace
from functools import lru_cache
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.types import Config
from scripts.model3_island_bridge_ops import prepare_arms

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DESIGN = ROOT / "data/design/model3_ch2_bridge_20260927.json"
DECISION_DESIGN = ROOT / "data/design/model3_joint_syndrome_rare_mutant_20261004.json"


def _affinity(access: float, investment: float, visitors):
    return (0.1 + investment) * np.exp(
        -((access - visitors.optima) / visitors.breadths) ** 2
    )


def _export(affinity, assurance: float, visitors, config: Config):
    if not len(visitors.ids) or config.activity == 0:
        return 0.0, np.zeros(0, dtype=float)
    total = float(affinity.sum())
    if total <= 0:
        return 0.0, np.zeros_like(affinity)
    channels = affinity / total
    activity = config.activity
    if config.activity_mode == "count_scaled":
        activity *= len(visitors.ids) / config.reference_visitor_count
    removed = (
        config.pollen_budget
        * np.exp(-config.pollen_discount * assurance)
        * (1.0 - np.exp(-activity * float(affinity.mean())))
    )
    return float(removed), channels


def rare_mutant_components(resident, mutant, visitors, config: Config):
    """Rare-mutant maternal, paternal and self contributions."""
    xr, ir, ar = map(float, resident)
    xm, im, am = map(float, mutant)

    ov_r = config.ovule_budget * np.exp(
        -config.investment_cost * ir**2
        - config.assurance_cost * ar**2
    )
    ov_m = config.ovule_budget * np.exp(
        -config.investment_cost * im**2
        - config.assurance_cost * am**2
    )

    if not len(visitors.ids) or config.activity == 0:
        female_r = 0.0
        female_m = 0.0
        paternal_m = 0.0
    else:
        A_r = _affinity(xr, ir, visitors)
        A_m = _affinity(xm, im, visitors)
        R_r, q_r = _export(A_r, ar, visitors, config)
        R_m, q_m = _export(A_m, am, visitors, config)

        denom = A_r + config.background_ratio
        resident_match = np.divide(
            A_r, denom, out=np.zeros_like(A_r), where=denom > 0
        )
        mutant_match = np.divide(
            A_m, denom, out=np.zeros_like(A_m), where=denom > 0
        )

        rho_r = float(
            R_r * np.sum(q_r * visitors.effectiveness * resident_match)
        )
        rho_m = float(
            R_r * np.sum(q_r * visitors.effectiveness * mutant_match)
        )

        available_r = (
            ov_r * (1.0 - ar)
            if config.assurance_timing == "prior"
            else ov_r
        )
        available_m = (
            ov_m * (1.0 - am)
            if config.assurance_timing == "prior"
            else ov_m
        )
        female_r = float(
            available_r
            * (1.0 - np.exp(-rho_r / (2.0 * config.pollen_scale)))
        )
        female_m = float(
            available_m
            * (1.0 - np.exp(-rho_m / (2.0 * config.pollen_scale)))
        )

        if rho_r > 0:
            mutant_to_residents = float(
                R_m
                * np.sum(
                    q_m
                    * visitors.effectiveness
                    * resident_match
                )
            )
            paternal_m = female_r * mutant_to_residents / rho_r
        else:
            paternal_m = 0.0

    self_raw_m = (
        ov_m * am
        if config.assurance_timing == "prior"
        else am * (ov_m - female_m)
    )
    self_viable_m = float(self_raw_m * (1.0 - config.depression))
    w = float(0.5 * female_m + 0.5 * paternal_m + self_viable_m)

    return {
        "maternal_outcross": float(female_m),
        "paternal_outcross": float(paternal_m),
        "self_viable": self_viable_m,
        "parental_genome_contribution": w,
    }


def log_invasion_fitness(resident, mutant, visitors, config: Config):
    w = rare_mutant_components(resident, mutant, visitors, config)[
        "parental_genome_contribution"
    ]
    if w <= 0:
        return -np.inf
    return float(np.log(w))


def invasion_gradient(
    resident,
    visitors,
    config: Config,
    *,
    trait_index: int,
    step: float,
):
    resident = np.asarray(resident, dtype=float)
    if trait_index not in (0, 1, 2):
        raise ValueError("trait_index must be access, investment or assurance")
    if not 0 < step < 0.1:
        raise ValueError("invalid finite-difference step")
    if not step < resident[trait_index] < 1.0 - step:
        raise ValueError("resident state too close to unit boundary")
    plus = resident.copy()
    minus = resident.copy()
    plus[trait_index] += step
    minus[trait_index] -= step
    lp = log_invasion_fitness(resident, plus, visitors, config)
    lm = log_invasion_fitness(resident, minus, visitors, config)
    if not np.isfinite([lp, lm]).all():
        raise ArithmeticError("nonfinite mutant invasion fitness")
    return float((lp - lm) / (2.0 * step))


def _settings(base: Config, decision: dict):
    out = {}
    for name, patch in decision["settings"].items():
        out[name] = replace(
            base,
            assurance_mode="evolving",
            assurance_timing=patch["assurance_timing"],
            pollen_discount=float(patch["pollen_discount"]),
            assurance_cost=float(patch["assurance_cost"]),
        )
    return out


@lru_cache(maxsize=1)
def run_audit():
    source = json.loads(SOURCE_DESIGN.read_text(encoding="utf-8"))
    decision = json.loads(DECISION_DESIGN.read_text(encoding="utf-8"))
    base = Config.from_dict(source["base_config"])
    settings = _settings(base, decision)
    h = float(decision["invasion_fitness"]["finite_difference_step"])
    deadband = float(decision["vector_definitions"]["gradient_shift_deadband"])

    states = [
        (float(x), float(i), float(a))
        for x in decision["resident_states"]["access"]
        for i in decision["resident_states"]["investment"]
        for a in decision["resident_states"]["assurance"]
    ]
    store = {
        (setting, state): {
            "near_i": [], "far_i": [], "near_a": [], "far_a": []
        }
        for setting in settings
        for state in states
    }

    for seed in source["history_seeds"]:
        arms = prepare_arms(
            base,
            seed=int(seed),
            pool_size=int(source["pool_size"]),
        )
        _, near_history = arms["near"]
        _, far_history = arms["far"]

        for setting_name, config in settings.items():
            for state in states:
                ni = np.mean([
                    invasion_gradient(state, v, config, trait_index=1, step=h)
                    for v in near_history.visitors
                ])
                fi = np.mean([
                    invasion_gradient(state, v, config, trait_index=1, step=h)
                    for v in far_history.visitors
                ])
                na = np.mean([
                    invasion_gradient(state, v, config, trait_index=2, step=h)
                    for v in near_history.visitors
                ])
                fa = np.mean([
                    invasion_gradient(state, v, config, trait_index=2, step=h)
                    for v in far_history.visitors
                ])
                cell = store[(setting_name, state)]
                cell["near_i"].append(float(ni))
                cell["far_i"].append(float(fi))
                cell["near_a"].append(float(na))
                cell["far_a"].append(float(fa))

    rows = []
    for (setting, state), cell in store.items():
        x, i, a = state
        near_i = np.asarray(cell["near_i"])
        far_i = np.asarray(cell["far_i"])
        near_a = np.asarray(cell["near_a"])
        far_a = np.asarray(cell["far_a"])
        di = far_i - near_i
        da = far_a - near_a
        joint = (di <= -deadband) & (da >= deadband)
        classic = (
            (near_i >= deadband)
            & (near_a <= -deadband)
            & (far_i <= -deadband)
            & (far_a >= deadband)
        )
        rows.append({
            "setting": setting,
            "access": x,
            "investment": i,
            "assurance": a,
            "history_count": len(di),
            "mean_near_beta_i": float(near_i.mean()),
            "mean_far_beta_i": float(far_i.mean()),
            "mean_near_beta_a": float(near_a.mean()),
            "mean_far_beta_a": float(far_a.mean()),
            "mean_far_minus_near_beta_i": float(di.mean()),
            "mean_far_minus_near_beta_a": float(da.mean()),
            "joint_shift_fraction": float(joint.mean()),
            "classic_sign_reversal_fraction": float(classic.mean()),
        })

    summaries = {}
    for setting in settings:
        sub = [r for r in rows if r["setting"] == setting]
        summaries[setting] = {
            "states": len(sub),
            "mean_joint_shift_fraction": float(np.mean(
                [r["joint_shift_fraction"] for r in sub]
            )),
            "minimum_joint_shift_fraction": float(np.min(
                [r["joint_shift_fraction"] for r in sub]
            )),
            "mean_classic_sign_reversal_fraction": float(np.mean(
                [r["classic_sign_reversal_fraction"] for r in sub]
            )),
            "maximum_classic_sign_reversal_fraction": float(np.max(
                [r["classic_sign_reversal_fraction"] for r in sub]
            )),
        }

    central = {
        setting: next(
            r for r in rows
            if r["setting"] == setting
            and r["access"] == 0.5
            and r["investment"] == 0.5
            and r["assurance"] == 0.5
        )
        for setting in settings
    }
    return {
        "status": "rare_mutant_joint_selection_complete",
        "decision_design": str(DECISION_DESIGN.relative_to(ROOT)),
        "history_count": len(source["history_seeds"]),
        "state_count": len(states),
        "settings": list(settings),
        "deadband": deadband,
        "summaries": summaries,
        "central_state": central,
        "rows": rows,
        "claim_boundary": [
            "assurance selection is rare-mutant invasion fitness, not a monomorphic population derivative",
            "male outcross success and double transmission of selfed seed are explicit",
            "delta is fixed; purging feedback is absent",
            "selection-vector shift and absolute sign reversal are reported separately",
            "delayed zero-cost control is not independent evidence for assurance evolution",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
