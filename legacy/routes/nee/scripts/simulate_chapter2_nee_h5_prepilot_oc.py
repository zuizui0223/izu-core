from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_nee_h5_prepilot_oc_freeze_20260912.json"
OUT = ROOT / "data/results/chapter2_nee_h5_prepilot_oc_20260912.json"


def _shares(x: np.ndarray, z: np.ndarray, y: np.ndarray) -> np.ndarray:
    X = np.column_stack([np.ones(len(x)), x, z, x * z])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    components = np.column_stack([beta[1] * x, beta[2] * z, beta[3] * x * z])
    variances = np.var(components, axis=0, ddof=1)
    return variances / variances.sum()


def _one_level(
    rng: np.random.Generator,
    *,
    n_blocks: int,
    plants_per_block: int,
    retention: float,
    rho: float,
    aggregation: int,
    a: float,
    b: float,
    c: float,
    block_sd: float,
    residual_sd: float,
) -> tuple[np.ndarray, int]:
    var_zbar = rho + (1.0 - rho) / aggregation
    xs: list[np.ndarray] = []
    zs: list[np.ndarray] = []
    ys: list[np.ndarray] = []
    for _ in range(n_blocks):
        z_block = rng.normal(0.0, math.sqrt(var_zbar))
        block_intercept = rng.normal(0.0, block_sd)
        x = rng.normal(size=plants_per_block)
        keep = rng.random(plants_per_block) < retention
        x = x[keep]
        if not len(x):
            continue
        z = np.full(len(x), z_block)
        y = a * x + b * z + c * x * z + block_intercept + rng.normal(0.0, residual_sd, len(x))
        xs.append(x)
        zs.append(z)
        ys.append(y)
    x = np.concatenate(xs)
    z = np.concatenate(zs)
    y = np.concatenate(ys)
    return _shares(x, z, y), len(x)


def _trial(rng: np.random.Generator, *, cfg: dict, n_blocks: int, plants_per_block: int, retention: float, rho: float) -> np.ndarray:
    common = dict(
        rng=rng,
        n_blocks=n_blocks,
        plants_per_block=plants_per_block,
        retention=retention,
        rho=rho,
        a=float(cfg["a"]),
        b=float(cfg["b"]),
        c=float(cfg["c"]),
        block_sd=float(cfg["block_sd"]),
        residual_sd=float(cfg["residual_sd"]),
    )
    low, n_low = _one_level(aggregation=1, **common)
    high, n_high = _one_level(aggregation=16, **common)
    return np.array(
        [
            high[0] - low[0],
            low[1] - high[1],
            high[0] - high[1],
            n_low,
            n_high,
            low[0],
            low[1],
            high[0],
            high[1],
        ],
        dtype=float,
    )


def _scenario(*, cfg: dict, screen: dict, n_blocks: int, plants_per_block: int, retention: float, rho: float, replicates: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    draws = np.vstack(
        [
            _trial(
                rng,
                cfg=cfg,
                n_blocks=n_blocks,
                plants_per_block=plants_per_block,
                retention=retention,
                rho=rho,
            )
            for _ in range(replicates)
        ]
    )
    contrast_sd = draws[:, :3].std(axis=0, ddof=1)
    margin = float(screen["directional_margin_z"]) * contrast_sd
    crossover = (
        (draws[:, 0] > margin[0])
        & (draws[:, 1] > margin[1])
        & (draws[:, 2] > margin[2])
    )
    no_crossover = draws[:, 2] < -margin[2]
    return {
        "blocks": n_blocks,
        "plants_per_block": plants_per_block,
        "recruited_plants_per_aggregation_level": n_blocks * plants_per_block,
        "retention": retention,
        "rho_benchmark": rho,
        "monte_carlo_replicates": replicates,
        "median_complete_plants_per_aggregation_level": int(round(float(np.median((draws[:, 3] + draws[:, 4]) / 2.0)))),
        "low_dependence_crossover_separation_rate": float(crossover.mean()),
        "high_dependence_no_crossover_separation_rate": float(no_crossover.mean()),
        "mean_state_share_increase": float(draws[:, 0].mean()),
        "mean_community_share_decrease": float(draws[:, 1].mean()),
        "mean_state_minus_community_at_high_aggregation": float(draws[:, 2].mean()),
        "sd_state_share_increase": float(contrast_sd[0]),
        "sd_community_share_decrease": float(contrast_sd[1]),
        "sd_state_minus_community_at_high_aggregation": float(contrast_sd[2]),
    }


def build() -> dict:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    cfg = design["benchmark_model"]
    screen = design["design_grid"]
    primary = []
    for rho in cfg["shared_dependence_benchmarks"]:
        for n_blocks in screen["blocks"]:
            primary.append(
                _scenario(
                    cfg=cfg,
                    screen=screen,
                    n_blocks=int(n_blocks),
                    plants_per_block=int(screen["plants_per_block_primary"]),
                    retention=float(screen["primary_retention"]),
                    rho=float(rho),
                    replicates=int(screen["monte_carlo_replicates"]),
                    seed=100 + int(n_blocks) + int(float(rho) * 1000),
                )
            )
        primary.append(
            _scenario(
                cfg=cfg,
                screen=screen,
                n_blocks=64,
                plants_per_block=int(screen["plants_per_block_upper_benchmark"]),
                retention=float(screen["primary_retention"]),
                rho=float(rho),
                replicates=int(screen["monte_carlo_replicates"]),
                seed=500 + int(float(rho) * 1000),
            )
        )

    sensitivity = []
    for retention in screen["retention_sensitivity"]:
        for rho in cfg["shared_dependence_benchmarks"]:
            sensitivity.append(
                _scenario(
                    cfg=cfg,
                    screen=screen,
                    n_blocks=64,
                    plants_per_block=int(screen["plants_per_block_upper_benchmark"]),
                    retention=float(retention),
                    rho=float(rho),
                    replicates=500,
                    seed=900 + int(float(retention) * 100) + int(float(rho) * 1000),
                )
            )

    return {
        "schema_version": "1.0",
        "status": "prepilot_synthetic_order_of_magnitude_screen_complete",
        "design": DESIGN.relative_to(ROOT).as_posix(),
        "primary_grid": primary,
        "retention_sensitivity": sensitivity,
        "decision": {
            "H5_is_precision_bottleneck": True,
            "independent_block_count_is_primary_design_lever": True,
            "near_boundary_shared_dependence_is_hardest_region": True,
            "single_fixed_sample_size_cannot_resolve_all_dependence_regimes": True,
            "final_R3_requires_empirical_pilot": True,
            "do_not_weaken_H5_if_R3_infeasible": True,
        },
        "claim_boundary": "These rates are synthetic separation operating characteristics for order-of-magnitude triage only. They are not empirical power and cannot replace pilot-frozen R3 precision planning.",
    }


def main() -> None:
    payload = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["decision"], indent=2))


if __name__ == "__main__":
    main()
