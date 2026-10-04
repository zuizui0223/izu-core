"""Rare-mutant joint selection-vector audit for Model 3.

Selection on floral investment i and reproductive assurance a is evaluated by
rare-mutant invasion fitness in a monomorphic resident background.

For a rare mutant m,

    w_m = 0.5 F_m + 0.5 P_m + S_m,

where F_m is maternal outcross seed production, P_m is paternal outcross
success on resident mothers, and S_m is viable selfed seed.  Selfed offspring
therefore count as one full parental-genome equivalent.

The resident pollen pool and resident female return are held fixed to first
order in mutant frequency.  This avoids the incorrect monomorphic-population
derivative for assurance.  Decision rules were frozen before full execution in

  data/design/model3_joint_syndrome_rare_mutant_20261004.json
  data/design/model3_joint_syndrome_rare_mutant_gate_addendum_20261004.json
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
GATE_ADDENDUM = ROOT / "data/design/model3_joint_syndrome_rare_mutant_gate_addendum_20261004.json"


def _settings(base: Config, decision: dict):
    return {
        name: replace(
            base,
            assurance_mode="evolving",
            assurance_timing=patch["assurance_timing"],
            pollen_discount=float(patch["pollen_discount"]),
            assurance_cost=float(patch["assurance_cost"]),
        )
        for name, patch in decision["settings"].items()
    }


def _log_fitness_batch(resident, mutant, visitors, config: Config):
    """Rare-mutant log parental-genome fitness for aligned state arrays.

    resident and mutant are S x 3 arrays. The resident environment is
    monomorphic for each row and is held fixed while the mutant row changes.
    """
    resident = np.asarray(resident, dtype=float)
    mutant = np.asarray(mutant, dtype=float)
    if resident.shape != mutant.shape or resident.ndim != 2 or resident.shape[1] != 3:
        raise ValueError("resident/mutant arrays must both be S x 3")

    xr, ir, ar = resident.T
    xm, im, am = mutant.T

    ov_r = config.ovule_budget * np.exp(
        -config.investment_cost * ir**2 - config.assurance_cost * ar**2
    )
    ov_m = config.ovule_budget * np.exp(
        -config.investment_cost * im**2 - config.assurance_cost * am**2
    )

    if not len(visitors.ids) or config.activity == 0:
        female_r = np.zeros(len(resident))
        female_m = np.zeros(len(resident))
        paternal_m = np.zeros(len(resident))
    else:
        A_r = (0.1 + ir[:, None]) * np.exp(
            -((xr[:, None] - visitors.optima[None, :]) / visitors.breadths[None, :]) ** 2
        )
        A_m = (0.1 + im[:, None]) * np.exp(
            -((xm[:, None] - visitors.optima[None, :]) / visitors.breadths[None, :]) ** 2
        )
        sum_r = A_r.sum(axis=1, keepdims=True)
        sum_m = A_m.sum(axis=1, keepdims=True)
        q_r = np.divide(A_r, sum_r, out=np.zeros_like(A_r), where=sum_r > 0)
        q_m = np.divide(A_m, sum_m, out=np.zeros_like(A_m), where=sum_m > 0)

        activity = config.activity
        if config.activity_mode == "count_scaled":
            activity *= len(visitors.ids) / config.reference_visitor_count

        R_r = (
            config.pollen_budget
            * np.exp(-config.pollen_discount * ar)
            * (1.0 - np.exp(-activity * A_r.mean(axis=1)))
        )
        R_m = (
            config.pollen_budget
            * np.exp(-config.pollen_discount * am)
            * (1.0 - np.exp(-activity * A_m.mean(axis=1)))
        )

        # In a monomorphic resident at carrying capacity, K cancels between
        # resident donor mass and recipient denominator.
        denom = A_r + config.background_ratio
        resident_match = np.divide(
            A_r, denom, out=np.zeros_like(A_r), where=denom > 0
        )
        mutant_match = np.divide(
            A_m, denom, out=np.zeros_like(A_m), where=denom > 0
        )

        eff = visitors.effectiveness[None, :]
        rho_r = R_r * np.sum(q_r * eff * resident_match, axis=1)
        rho_m = R_r * np.sum(q_r * eff * mutant_match, axis=1)

        available_r = ov_r * (1.0 - ar) if config.assurance_timing == "prior" else ov_r
        available_m = ov_m * (1.0 - am) if config.assurance_timing == "prior" else ov_m

        female_r = available_r * (
            1.0 - np.exp(-rho_r / (2.0 * config.pollen_scale))
        )
        female_m = available_m * (
            1.0 - np.exp(-rho_m / (2.0 * config.pollen_scale))
        )

        mutant_to_residents = R_m * np.sum(q_m * eff * resident_match, axis=1)
        paternal_m = np.divide(
            female_r * mutant_to_residents,
            rho_r,
            out=np.zeros_like(rho_r),
            where=rho_r > 0,
        )

    self_raw_m = (
        ov_m * am
        if config.assurance_timing == "prior"
        else am * (ov_m - female_m)
    )
    self_viable_m = self_raw_m * (1.0 - config.depression)
    w = 0.5 * female_m + 0.5 * paternal_m + self_viable_m
    if np.any(w <= 0) or not np.isfinite(w).all():
        raise ArithmeticError("nonpositive or nonfinite rare-mutant fitness")
    return np.log(w)


def rare_mutant_components(resident, mutant, visitors, config: Config):
    """Scalar decomposition retained for source-locked low-frequency tests."""
    resident = np.asarray(resident, dtype=float)
    mutant = np.asarray(mutant, dtype=float)
    if resident.shape != (3,) or mutant.shape != (3,):
        raise ValueError("resident and mutant must be length-3 vectors")

    # Re-evaluate the same algebra while retaining components for auditability.
    xr, ir, ar = resident
    xm, im, am = mutant
    ov_r = config.ovule_budget * np.exp(
        -config.investment_cost * ir**2 - config.assurance_cost * ar**2
    )
    ov_m = config.ovule_budget * np.exp(
        -config.investment_cost * im**2 - config.assurance_cost * am**2
    )
    if not len(visitors.ids) or config.activity == 0:
        female_r = female_m = paternal_m = 0.0
    else:
        A_r = (0.1 + ir) * np.exp(-((xr - visitors.optima) / visitors.breadths) ** 2)
        A_m = (0.1 + im) * np.exp(-((xm - visitors.optima) / visitors.breadths) ** 2)
        q_r = A_r / A_r.sum()
        q_m = A_m / A_m.sum()
        activity = config.activity
        if config.activity_mode == "count_scaled":
            activity *= len(visitors.ids) / config.reference_visitor_count
        R_r = (
            config.pollen_budget
            * np.exp(-config.pollen_discount * ar)
            * (1.0 - np.exp(-activity * A_r.mean()))
        )
        R_m = (
            config.pollen_budget
            * np.exp(-config.pollen_discount * am)
            * (1.0 - np.exp(-activity * A_m.mean()))
        )
        denom = A_r + config.background_ratio
        resident_match = A_r / denom
        mutant_match = A_m / denom
        rho_r = R_r * np.sum(q_r * visitors.effectiveness * resident_match)
        rho_m = R_r * np.sum(q_r * visitors.effectiveness * mutant_match)
        available_r = ov_r * (1.0 - ar) if config.assurance_timing == "prior" else ov_r
        available_m = ov_m * (1.0 - am) if config.assurance_timing == "prior" else ov_m
        female_r = available_r * (1.0 - np.exp(-rho_r / (2.0 * config.pollen_scale)))
        female_m = available_m * (1.0 - np.exp(-rho_m / (2.0 * config.pollen_scale)))
        mutant_to_residents = R_m * np.sum(
            q_m * visitors.effectiveness * resident_match
        )
        paternal_m = female_r * mutant_to_residents / rho_r if rho_r > 0 else 0.0

    self_raw_m = (
        ov_m * am
        if config.assurance_timing == "prior"
        else am * (ov_m - female_m)
    )
    self_viable_m = self_raw_m * (1.0 - config.depression)
    return {
        "maternal_outcross": float(female_m),
        "paternal_outcross": float(paternal_m),
        "self_viable": float(self_viable_m),
        "parental_genome_contribution": float(
            0.5 * female_m + 0.5 * paternal_m + self_viable_m
        ),
    }


def log_invasion_fitness(resident, mutant, visitors, config: Config):
    return float(_log_fitness_batch(
        np.asarray(resident, dtype=float)[None, :],
        np.asarray(mutant, dtype=float)[None, :],
        visitors,
        config,
    )[0])


def invasion_gradient(resident, visitors, config: Config, *, trait_index: int, step: float):
    resident = np.asarray(resident, dtype=float)
    plus = resident.copy()
    minus = resident.copy()
    plus[trait_index] += step
    minus[trait_index] -= step
    return (
        log_invasion_fitness(resident, plus, visitors, config)
        - log_invasion_fitness(resident, minus, visitors, config)
    ) / (2.0 * step)


def _gradient_and_gamma_batch(
    states,
    visitors,
    config: Config,
    beta_step: float,
    gamma_step: float,
):
    states = np.asarray(states, dtype=float)
    ip = states.copy(); ip[:, 1] += beta_step
    im = states.copy(); im[:, 1] -= beta_step
    ap = states.copy(); ap[:, 2] += beta_step
    am = states.copy(); am[:, 2] -= beta_step

    beta_i = (
        _log_fitness_batch(states, ip, visitors, config)
        - _log_fitness_batch(states, im, visitors, config)
    ) / (2.0 * beta_step)
    beta_a = (
        _log_fitness_batch(states, ap, visitors, config)
        - _log_fitness_batch(states, am, visitors, config)
    ) / (2.0 * beta_step)

    pp = states.copy(); pp[:, 1] += gamma_step; pp[:, 2] += gamma_step
    pm = states.copy(); pm[:, 1] += gamma_step; pm[:, 2] -= gamma_step
    mp = states.copy(); mp[:, 1] -= gamma_step; mp[:, 2] += gamma_step
    mm = states.copy(); mm[:, 1] -= gamma_step; mm[:, 2] -= gamma_step
    gamma = (
        _log_fitness_batch(states, pp, visitors, config)
        - _log_fitness_batch(states, pm, visitors, config)
        - _log_fitness_batch(states, mp, visitors, config)
        + _log_fitness_batch(states, mm, visitors, config)
    ) / (4.0 * gamma_step**2)
    return beta_i, beta_a, gamma


def _gamma_batch(states, visitors, config: Config, step: float):
    states = np.asarray(states, dtype=float)
    pp = states.copy(); pp[:, 1] += step; pp[:, 2] += step
    pm = states.copy(); pm[:, 1] += step; pm[:, 2] -= step
    mp = states.copy(); mp[:, 1] -= step; mp[:, 2] += step
    mm = states.copy(); mm[:, 1] -= step; mm[:, 2] -= step
    return (
        _log_fitness_batch(states, pp, visitors, config)
        - _log_fitness_batch(states, pm, visitors, config)
        - _log_fitness_batch(states, mp, visitors, config)
        + _log_fitness_batch(states, mm, visitors, config)
    ) / (4.0 * step**2)


def _paired_bootstrap_ci(values, indices):
    values = np.asarray(values, dtype=float)
    means = values[indices].mean(axis=1)
    return [float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))]


@lru_cache(maxsize=1)
def run_audit():
    source = json.loads(SOURCE_DESIGN.read_text(encoding="utf-8"))
    decision = json.loads(DECISION_DESIGN.read_text(encoding="utf-8"))
    gate = json.loads(GATE_ADDENDUM.read_text(encoding="utf-8"))
    base = Config.from_dict(source["base_config"])
    settings = _settings(base, decision)
    h = float(decision["invasion_fitness"]["finite_difference_step"])
    gamma_h = 1e-4
    gamma_low = 5e-5
    gamma_high = 2e-4
    deadband = float(decision["vector_definitions"]["gradient_shift_deadband"])

    states = np.asarray([
        (float(x), float(i), float(a))
        for x in decision["resident_states"]["access"]
        for i in decision["resident_states"]["investment"]
        for a in decision["resident_states"]["assurance"]
    ])
    nstate = len(states)
    nhistory = len(source["history_seeds"])

    store = {
        name: {
            key: np.zeros((nhistory, nstate), dtype=float)
            for key in (
                "near_i", "far_i", "near_a", "far_a",
                "near_gamma", "far_gamma",
                "near_gamma_low", "far_gamma_low",
                "near_gamma_high", "far_gamma_high",
            )
        }
        for name in settings
    }

    for hix, seed in enumerate(source["history_seeds"]):
        arms = prepare_arms(base, seed=int(seed), pool_size=int(source["pool_size"]))
        _, near_history = arms["near"]
        _, far_history = arms["far"]

        for setting_name, config in settings.items():
            for arm_name, history in (("near", near_history), ("far", far_history)):
                acc_i = np.zeros(nstate)
                acc_a = np.zeros(nstate)
                acc_g = np.zeros(nstate)
                acc_g_low = np.zeros(nstate)
                acc_g_high = np.zeros(nstate)
                for visitor_state in history.visitors:
                    bi, ba, ga = _gradient_and_gamma_batch(
                        states, visitor_state, config, h, gamma_h
                    )
                    ga_low = _gamma_batch(
                        states, visitor_state, config, gamma_low
                    )
                    ga_high = _gamma_batch(
                        states, visitor_state, config, gamma_high
                    )
                    acc_i += bi
                    acc_a += ba
                    acc_g += ga
                    acc_g_low += ga_low
                    acc_g_high += ga_high
                scale = 1.0 / len(history.visitors)
                store[setting_name][f"{arm_name}_i"][hix] = acc_i * scale
                store[setting_name][f"{arm_name}_a"][hix] = acc_a * scale
                store[setting_name][f"{arm_name}_gamma"][hix] = acc_g * scale
                store[setting_name][f"{arm_name}_gamma_low"][hix] = acc_g_low * scale
                store[setting_name][f"{arm_name}_gamma_high"][hix] = acc_g_high * scale

    rng = np.random.default_rng(1004)
    bootstrap_indices = rng.integers(
        0, nhistory, size=(1999, nhistory), dtype=np.int64
    )
    rows = []
    for setting_name in settings:
        data = store[setting_name]
        for six, (x, i, a) in enumerate(states):
            near_i = data["near_i"][:, six]
            far_i = data["far_i"][:, six]
            near_a = data["near_a"][:, six]
            far_a = data["far_a"][:, six]
            near_g = data["near_gamma"][:, six]
            far_g = data["far_gamma"][:, six]
            near_g_low = data["near_gamma_low"][:, six]
            far_g_low = data["far_gamma_low"][:, six]
            near_g_high = data["near_gamma_high"][:, six]
            far_g_high = data["far_gamma_high"][:, six]
            di = far_i - near_i
            da = far_a - near_a
            joint = (di <= -deadband) & (da >= deadband)
            classic = (
                (near_i >= deadband)
                & (near_a <= -deadband)
                & (far_i <= -deadband)
                & (far_a >= deadband)
            )
            ci_i = _paired_bootstrap_ci(di, bootstrap_indices)
            ci_a = _paired_bootstrap_ci(da, bootstrap_indices)
            mean_di = float(di.mean())
            mean_da = float(da.mean())
            joint_pass = bool(
                mean_di <= -deadband
                and mean_da >= deadband
                and float(joint.mean()) >= 0.90
                and ci_i[1] < 0
                and ci_a[0] > 0
            )
            rows.append({
                "setting": setting_name,
                "access": float(x),
                "investment": float(i),
                "assurance": float(a),
                "history_count": nhistory,
                "mean_near_beta_i": float(near_i.mean()),
                "mean_far_beta_i": float(far_i.mean()),
                "mean_near_beta_a": float(near_a.mean()),
                "mean_far_beta_a": float(far_a.mean()),
                "mean_far_minus_near_beta_i": mean_di,
                "mean_far_minus_near_beta_a": mean_da,
                "beta_i_shift_ci95": ci_i,
                "beta_a_shift_ci95": ci_a,
                "joint_shift_fraction": float(joint.mean()),
                "joint_shift_gate_pass": joint_pass,
                "classic_sign_reversal_fraction": float(classic.mean()),
                "mean_near_gamma_ia": float(near_g.mean()),
                "mean_far_gamma_ia": float(far_g.mean()),
                "negative_gamma_near_fraction": float(np.mean(near_g < 0)),
                "negative_gamma_far_fraction": float(np.mean(far_g < 0)),
                "gamma_sign_stable_near_fraction": float(np.mean(
                    (np.sign(near_g_low) == np.sign(near_g))
                    & (np.sign(near_g) == np.sign(near_g_high))
                )),
                "gamma_sign_stable_far_fraction": float(np.mean(
                    (np.sign(far_g_low) == np.sign(far_g))
                    & (np.sign(far_g) == np.sign(far_g_high))
                )),
            })

    summaries = {}
    for setting_name, patch in decision["settings"].items():
        sub = [r for r in rows if r["setting"] == setting_name]
        summaries[setting_name] = {
            "role": patch["role"],
            "states": len(sub),
            "joint_shift_gate_pass_states": int(sum(r["joint_shift_gate_pass"] for r in sub)),
            "minimum_joint_shift_fraction": float(min(r["joint_shift_fraction"] for r in sub)),
            "mean_joint_shift_fraction": float(np.mean([r["joint_shift_fraction"] for r in sub])),
            "maximum_classic_sign_reversal_fraction": float(max(r["classic_sign_reversal_fraction"] for r in sub)),
            "mean_classic_sign_reversal_fraction": float(np.mean([r["classic_sign_reversal_fraction"] for r in sub])),
            "minimum_negative_gamma_fraction": float(min(
                min(r["negative_gamma_near_fraction"], r["negative_gamma_far_fraction"])
                for r in sub
            )),
            "minimum_gamma_sign_stability_fraction": float(min(
                min(r["gamma_sign_stable_near_fraction"], r["gamma_sign_stable_far_fraction"])
                for r in sub
            )),
        }

    central = {
        setting_name: next(
            r for r in rows
            if r["setting"] == setting_name
            and r["access"] == 0.5
            and r["investment"] == 0.5
            and r["assurance"] == 0.5
        )
        for setting_name in settings
    }

    return {
        "status": "rare_mutant_joint_selection_complete",
        "decision_design": str(DECISION_DESIGN.relative_to(ROOT)),
        "gate_addendum": str(GATE_ADDENDUM.relative_to(ROOT)),
        "history_count": nhistory,
        "state_count": nstate,
        "settings": list(settings),
        "deadband": deadband,
        "gamma_steps": {
            "primary": gamma_h,
            "stability_low": gamma_low,
            "stability_high": gamma_high,
        },
        "summaries": summaries,
        "central_state": central,
        "rows": rows,
        "claim_boundary": [
            "assurance selection is rare-mutant invasion fitness, not a monomorphic population derivative",
            "male outcross success and double transmission of selfed seed are explicit",
            "beta shift, G-mediated response, and finite trajectory are adjudicated separately",
            "gamma_ia is correlational selection on mutant traits and does not by itself prove multiple attractors",
            "delta is fixed; purging feedback is absent",
            "delayed zero-cost control is not independent evidence for assurance evolution",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
