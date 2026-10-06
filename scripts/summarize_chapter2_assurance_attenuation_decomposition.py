"""Arm-level decomposition of the confirmed assurance attenuation interaction.

This analysis reuses the hash-verified raw shards from the prospective four-setting
campaign. It does not rerun trajectories or change the frozen biological claim.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import json

import numpy as np

from scripts.run_chapter2_assurance_generality import case_key, load_design, seed_ranges
from scripts.summarize_chapter2_assurance_generality import verify_complete, bootstrap_interval


ROOT = Path(__file__).resolve().parents[1]


def load_traits(paths: dict[str, Path], task: tuple) -> tuple[bool, np.ndarray, np.ndarray]:
    key = case_key(task)
    with np.load(paths[key]) as z:
        trace = z["trace"]
        if trace.shape != (1001, 10):
            raise ValueError((key, trace.shape))
        alive = bool(trace[1000, 0] > 0)
        founder = trace[0, 1:4].astype(float)
        endpoint = trace[1000, 1:4].astype(float) if alive else np.full(3, np.nan)
    return alive, founder, endpoint


def estimate(values: list[float], draws: int, seed: int) -> dict:
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    return {
        "mean": float(x.mean()) if len(x) else None,
        "bootstrap95": bootstrap_interval(x.tolist(), draws, seed),
        "n_histories": int(len(x)),
    }


def summarize_setting(
    design: dict,
    paths: dict[str, Path],
    setting: str,
    setting_index: int,
    decomposition: dict,
) -> dict:
    histories, repeats = seed_ranges(design)
    main = design["main_campaign"]
    rate = float(main["mutation_probability"])

    names = [
        "fixed_near_investment_change",
        "fixed_far_investment_change",
        "evolving_near_investment_change",
        "evolving_far_investment_change",
        "evolving_near_assurance_change",
        "evolving_far_assurance_change",
        "evolution_effect_near",
        "evolution_effect_far",
        "near_side_contribution_to_attenuation",
        "far_side_contribution_to_attenuation",
        "attenuation",
    ]
    by_history = {name: [] for name in names}
    common_rep_counts = []
    identity_errors = []

    for history_seed in histories:
        rep_rows = {name: [] for name in names}
        for repeat_seed in repeats:
            rows = {}
            for mode in ("fixed", "evolving"):
                for arm in ("near", "far"):
                    task = ("main", setting, rate, history_seed, repeat_seed, arm, mode)
                    rows[(mode, arm)] = load_traits(paths, task)

            if not all(rows[key][0] for key in rows):
                continue

            changes = {
                key: rows[key][2] - rows[key][1]
                for key in rows
            }
            fn = float(changes[("fixed", "near")][1])
            ff = float(changes[("fixed", "far")][1])
            en = float(changes[("evolving", "near")][1])
            ef = float(changes[("evolving", "far")][1])
            an = float(changes[("evolving", "near")][2])
            af = float(changes[("evolving", "far")][2])

            near_effect = en - fn
            far_effect = ef - ff
            interaction = (ef - en) - (ff - fn)
            identity = far_effect - near_effect
            identity_errors.append(abs(interaction - identity))

            values = {
                "fixed_near_investment_change": fn,
                "fixed_far_investment_change": ff,
                "evolving_near_investment_change": en,
                "evolving_far_investment_change": ef,
                "evolving_near_assurance_change": an,
                "evolving_far_assurance_change": af,
                "evolution_effect_near": near_effect,
                "evolution_effect_far": far_effect,
                "near_side_contribution_to_attenuation": -near_effect,
                "far_side_contribution_to_attenuation": far_effect,
                "attenuation": interaction,
            }
            for name, value in values.items():
                rep_rows[name].append(value)

        common_rep_counts.append(len(rep_rows["attenuation"]))
        if rep_rows["attenuation"]:
            for name in names:
                by_history[name].append(float(np.mean(rep_rows[name])))

    if len(by_history["attenuation"]) != 64:
        raise ValueError((setting, "expected 64 eligible histories", len(by_history["attenuation"])))
    if min(common_rep_counts) < 1:
        raise ValueError((setting, "history without common four-cell replicate"))

    draws = int(decomposition["bootstrap"]["draws"])
    base_seed = int(decomposition["bootstrap"]["seed"]) + setting_index * 100
    estimates = {
        name: estimate(values, draws, base_seed + i)
        for i, (name, values) in enumerate(by_history.items())
    }

    near_effect = estimates["evolution_effect_near"]["mean"]
    far_effect = estimates["evolution_effect_far"]["mean"]
    near_contrib = estimates["near_side_contribution_to_attenuation"]["mean"]
    far_contrib = estimates["far_side_contribution_to_attenuation"]["mean"]
    attenuation = estimates["attenuation"]["mean"]

    if not np.isclose(near_contrib + far_contrib, attenuation, rtol=0, atol=1e-12):
        raise AssertionError((setting, near_contrib, far_contrib, attenuation))

    if near_effect < 0 and far_effect >= 0:
        localization = "near_decline_plus_far_relief"
    elif near_effect < far_effect:
        localization = "near_effect_more_negative_than_far"
    else:
        localization = "other"

    return {
        "setting": setting,
        "common_four_cell_histories": 64,
        "common_replicates_per_history_min": int(min(common_rep_counts)),
        "common_replicates_per_history_max": int(max(common_rep_counts)),
        "max_attenuation_identity_error": float(max(identity_errors, default=0.0)),
        "estimates": estimates,
        "localization": localization,
        "identity": "attenuation = far-side evolving-minus-fixed effect - near-side evolving-minus-fixed effect",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-design", type=Path, required=True)
    parser.add_argument("--decomposition-design", type=Path, required=True)
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    design = load_design(args.source_design)
    decomposition = json.loads(args.decomposition_design.read_text(encoding="utf-8"))
    if decomposition["status"] != "frozen_post_confirmation_before_arm_decomposition":
        raise ValueError("decomposition design is not frozen")
    if int(decomposition["source_campaign_cases"]) != 8448:
        raise ValueError("unexpected source campaign size")

    paths = verify_complete(args.input_root, args.source_design, design)
    rows = [
        summarize_setting(design, paths, setting, i, decomposition)
        for i, setting in enumerate(decomposition["settings"])
    ]

    result = {
        "schema_version": "1.0",
        "date": "2026-10-06",
        "status": "complete_arm_decomposition",
        "source_design_sha256": hashlib.sha256(args.source_design.read_bytes()).hexdigest(),
        "decomposition_design_sha256": hashlib.sha256(args.decomposition_design.read_bytes()).hexdigest(),
        "source_cases_verified": len(paths),
        "independent_visitor_histories": 64,
        "settings": rows,
        "mechanistic_anchor": decomposition["mechanistic_anchor"],
        "claim_boundary": decomposition["reporting"],
    }
    if args.out.exists():
        raise ValueError("preserve existing arm-decomposition result")
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
