"""Post-failure diagnosis for Model3R-v3 assembly filtering.

This does not alter or rescue the frozen v3 test. It decomposes the best frozen
v3 draw into arrival-only, reproductive-establishment-only, and combined
occupancy filters to identify why regional H2 trait sorting was weak/negative.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from scripts.model3r_v3_assembly_emulator import (
    _ols,
    _prepare_world,
    _reproduction,
    _visitor_weights,
    _z,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/design/chapter2_model3r_v3_assembly_emulation_20261003.json"
DEFAULT_RESULT = ROOT / "data/results/chapter2_model3r_v3_empirical_preflight_20261003.json"


def _components(world: dict, viable_fraction: np.ndarray, p: dict):
    delta = (
        world["climate"][:, None, :]
        - world["species_climate_center"][None, :, :]
    )
    widths = (
        world["species_climate_width"][None, :, None]
        * float(p["plant_climate_scale"])
    )
    climate_suit = np.exp(-0.5 * np.sum((delta / widths) ** 2, axis=2))
    seed_reach = np.exp(
        -world["distance_km"][:, None]
        / (
            world["seed_scale"][None, :]
            * float(p["seed_dispersal_multiplier"])
        )
    )
    area_factor = np.exp(
        float(p["area_exponent"])
        * _z(world["cov"]["log_island_area_km2"].to_numpy(float))[:, None]
    )
    arrival = (
        float(p["seed_arrival_intensity"])
        * world["source_abundance"][None, :]
        * seed_reach
        * climate_suit
        * area_factor
    )
    establish = -np.expm1(
        -float(p["establishment_strength"]) * viable_fraction
    )
    combined = -np.expm1(-arrival * establish)
    arrival_only = -np.expm1(-arrival)
    establish_only = establish
    return arrival, establish, combined, arrival_only, establish_only


def _weighted_trait(weights: np.ndarray, trait: np.ndarray) -> np.ndarray:
    denom = np.maximum(weights.sum(axis=1), 1e-12)
    return weights @ trait / denom


def _context_slopes(world: dict, values: np.ndarray) -> dict:
    cov = world["cov"]
    controls = [
        cov["log_island_area_km2"].to_numpy(float),
        cov["climate_pc1"].to_numpy(float),
        cov["climate_pc2"].to_numpy(float),
        cov["climate_pc3"].to_numpy(float),
        cov["climate_pc4"].to_numpy(float),
    ]
    out = {}
    for ci, context in enumerate(world["contexts"]):
        mask = world["context_id"] == ci
        zdist = _z(world["log_distance"][mask])
        zcontrols = [_z(x[mask]) for x in controls]
        out[context] = float(_ols(values[mask], [zdist, *zcontrols])[1])
    return out


def _context_generalization_conditional(
    world: dict, assurance: np.ndarray, generalization: np.ndarray
) -> dict:
    cov = world["cov"]
    controls = [
        cov["log_island_area_km2"].to_numpy(float),
        cov["climate_pc1"].to_numpy(float),
        cov["climate_pc2"].to_numpy(float),
        cov["climate_pc3"].to_numpy(float),
        cov["climate_pc4"].to_numpy(float),
    ]
    out = {}
    for ci, context in enumerate(world["contexts"]):
        mask = world["context_id"] == ci
        zdist = _z(world["log_distance"][mask])
        zcontrols = [_z(x[mask]) for x in controls]
        out[context] = float(
            _ols(
                generalization[mask],
                [zdist, _z(assurance[mask]), *zcontrols],
            )[1]
        )
    return out


def _quantile_summary(x: np.ndarray) -> dict:
    return {
        "min": float(np.min(x)),
        "q05": float(np.quantile(x, 0.05)),
        "median": float(np.median(x)),
        "q95": float(np.quantile(x, 0.95)),
        "max": float(np.max(x)),
        "mean": float(np.mean(x)),
    }


def run(design: dict, frozen: dict) -> dict:
    params = dict(frozen["best"]["params"])
    world = _prepare_world(design, mode="preflight")
    visitor_weights = _visitor_weights(world, params)
    _, viable_fraction, pl = _reproduction(world, visitor_weights, params)
    arrival, establish, combined, arrival_only, establish_only = _components(
        world, viable_fraction, params
    )

    traits = world["species_traits"]
    source_a = traits[:, 3]
    source_g = traits[:, 1]
    source_mean_a = float(source_a.mean())
    source_mean_g = float(source_g.mean())

    filters = {
        "arrival_only": arrival_only,
        "establishment_only": establish_only,
        "combined": combined,
    }
    filter_reports = {}
    for name, weights in filters.items():
        a = _weighted_trait(weights, source_a)
        g = _weighted_trait(weights, source_g)
        filter_reports[name] = {
            "assurance_isolation_slopes": _context_slopes(world, a),
            "generalization_given_assurance_isolation_slopes":
                _context_generalization_conditional(world, a, g),
            "mean_assurance_shift_from_source": float(np.mean(a) - source_mean_a),
            "mean_generalization_shift_from_source": float(np.mean(g) - source_mean_g),
            "mean_expected_richness": float(np.mean(weights.sum(axis=1))),
        }

    # Does pollen limitation itself increase with distance within each context?
    occ_denom = np.maximum(combined.sum(axis=1), 1e-12)
    pl_island = np.sum(combined * pl, axis=1) / occ_denom
    pl_slopes = _context_slopes(world, pl_island)

    # Trait sorting strength within low/high isolation quartiles.
    q = world["distance_quantile"]
    low = q <= 0.25
    high = q >= 0.75
    def trait_selection(weights, trait, mask):
        w = weights[mask]
        vals = _weighted_trait(w, trait)
        return float(np.mean(vals) - np.mean(trait))

    selectivity = {}
    for name, weights in filters.items():
        selectivity[name] = {
            "assurance_low_isolation_shift": trait_selection(weights, source_a, low),
            "assurance_high_isolation_shift": trait_selection(weights, source_a, high),
            "generalization_low_isolation_shift": trait_selection(weights, source_g, low),
            "generalization_high_isolation_shift": trait_selection(weights, source_g, high),
        }

    # Establishment saturation diagnostic.
    saturation = {
        "arrival_intensity": _quantile_summary(arrival),
        "reproductive_establishment_probability": _quantile_summary(establish),
        "combined_occupancy_probability": _quantile_summary(combined),
        "establishment_fraction_gt_0_9": float(np.mean(establish > 0.9)),
        "establishment_fraction_gt_0_75": float(np.mean(establish > 0.75)),
        "establishment_fraction_lt_0_25": float(np.mean(establish < 0.25)),
    }

    return {
        "status": "complete_postfailure_model3r_v3_filter_diagnosis",
        "source_result": "data/results/chapter2_model3r_v3_empirical_preflight_20261003.json",
        "best_draw": int(frozen["best"]["draw"]),
        "source_trait_means": {
            "assurance": source_mean_a,
            "generalization": source_mean_g,
        },
        "context_pollen_limitation_isolation_slopes": pl_slopes,
        "filters": filter_reports,
        "isolation_quartile_selectivity": selectivity,
        "saturation": saturation,
        "claim_boundary": [
            "This is a post-failure diagnostic and cannot convert the failed v3 preflight into a pass.",
            "No parameter values are changed from the frozen best v3 draw.",
            "Its purpose is to decide whether the next experiment should alter arrival filtering, reproductive-establishment filtering, or neither."
        ],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--design", default=str(DEFAULT_DESIGN))
    p.add_argument("--result", default=str(DEFAULT_RESULT))
    p.add_argument("--out")
    a = p.parse_args()
    design = json.loads(Path(a.design).read_text(encoding="utf-8"))
    frozen = json.loads(Path(a.result).read_text(encoding="utf-8"))
    result = run(design, frozen)
    encoded = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if a.out:
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(encoded, encoding="utf-8")
    print(encoded)


if __name__ == "__main__":
    main()
