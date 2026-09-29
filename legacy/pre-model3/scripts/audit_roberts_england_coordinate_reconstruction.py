from __future__ import annotations

import importlib.util
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "scripts/adapt_roberts_england_natural_regime.py"
COORD_PATH = ROOT / "data/results/chapter2_roberts_england_natural_regime_coordinates_20260915.json"
OUT = ROOT / "data/results/chapter2_roberts_england_coordinate_reconstruction_audit_20260915.json"


def load_adapter():
    spec = importlib.util.spec_from_file_location("roberts_adapter_validation", ADAPTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load Roberts adapter")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def hill_d1(values: np.ndarray) -> float:
    total = float(values.sum())
    p = values[values > 0] / total
    return float(math.exp(-float(np.sum(p * np.log(p)))))


def phi(matrix: np.ndarray) -> tuple[float, int]:
    sds = np.std(matrix, axis=0, ddof=1)
    eligible = np.where(np.isfinite(sds) & (sds > 0))[0]
    if len(eligible) < 3:
        raise RuntimeError("fewer than three nonconstant partner series")
    denom = float(np.sum(sds[eligible])) ** 2
    total = matrix[:, eligible].sum(axis=1)
    return float(np.var(total, ddof=1) / denom), int(len(eligible))


def main() -> None:
    adapter = load_adapter()
    interactions = adapter.load_bytes(adapter.INTERACTION_URL, adapter.INTERACTION_SHA256)
    flowers = adapter.load_bytes(adapter.FLOWER_URL, adapter.FLOWER_SHA256)
    rows = adapter.adapt(interactions, flowers)
    committed = json.loads(COORD_PATH.read_text(encoding="utf-8"))
    committed_by_system = {row["system_id"]: row for row in committed["systems"]}

    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[str(row["system_id"])].append(row)

    systems = []
    for system in sorted(grouped):
        current = grouped[system]
        time_bins = sorted({str(row["time_bin"]) for row in current})
        partners = sorted({str(row["partner_id"]) for row in current})
        ti = {value: i for i, value in enumerate(time_bins)}
        pi = {value: i for i, value in enumerate(partners)}
        matrix = np.zeros((len(time_bins), len(partners)), dtype=float)
        for row in current:
            matrix[ti[str(row["time_bin"])], pi[str(row["partner_id"])]] += float(row["value"]) / float(row["effort"])

        pooled = matrix.sum(axis=0)
        d1 = hill_d1(pooled)
        primary_phi, eligible = phi(matrix)
        totals = matrix.sum(axis=1)
        zero_mask = totals == 0
        positive = matrix[~zero_mask]
        positive_phi = None
        positive_eligible = None
        if positive.shape[0] >= 2:
            try:
                positive_phi, positive_eligible = phi(positive)
            except RuntimeError:
                pass

        expected = committed_by_system[system]
        d1_delta = float(d1 - float(expected["breadth_D1"]))
        phi_delta = float(primary_phi - float(expected["phi"]))
        if abs(d1_delta) > 1e-12 or abs(phi_delta) > 1e-12:
            raise RuntimeError(f"{system}: independent coordinate mismatch D1={d1_delta} phi={phi_delta}")
        if len(time_bins) != 8:
            raise RuntimeError(f"{system}: expected eight frozen time bins")

        systems.append({
            "system_id": system,
            "time_bins": time_bins,
            "partner_count": len(partners),
            "eligible_partner_series": eligible,
            "zero_interaction_bins": [time_bins[i] for i, flag in enumerate(zero_mask) if flag],
            "zero_interaction_bin_count": int(np.sum(zero_mask)),
            "positive_interaction_bin_count": int(np.sum(~zero_mask)),
            "per_bin_total_rate": {time_bins[i]: float(totals[i]) for i in range(len(time_bins))},
            "reconstructed_D1": d1,
            "committed_D1": float(expected["breadth_D1"]),
            "D1_delta": d1_delta,
            "reconstructed_phi": primary_phi,
            "committed_phi": float(expected["phi"]),
            "phi_delta": phi_delta,
            "positive_bins_only_phi_diagnostic": positive_phi,
            "positive_bins_only_eligible_partner_series": positive_eligible,
        })

    result = {
        "schema_version": "1.0",
        "analysis": "chapter2_roberts_england_coordinate_reconstruction_audit",
        "status": "independent_formula_reconstruction_matches_committed_coordinates",
        "evaluated_on": "2026-09-15",
        "systems": systems,
        "primary_zero_bin_rule": (
            "All eight source-native flower-count schedule rounds remain in the primary matrix, including sampled rounds with zero retained interactions. "
            "The positive-bin-only phi is reported only as a diagnostic and does not replace the frozen primary estimand."
        ),
        "claim_boundary": (
            "The audit independently rebuilds time-by-partner matrices from the frozen adapter output and recomputes Hill D1 and Loreau-de Mazancourt phi without importing the common coordinate analyzer. "
            "It verifies numerical identity to the committed coordinates and reports how many source-native zero-interaction rounds contribute to the primary synchrony estimate. It does not alter admission, coordinates or the NEE promotion rule."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
