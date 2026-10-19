"""Strict, versioned ALL48 original-kernel expression verifier.

The historical verifier and SHA-pinned receipt remain immutable. Reject
missing/repeated/foreign comparison records BEFORE certifying any numeric
identity. No new biological simulation or changed 80-update horizon.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np

ORIGINAL_KERNEL_SHA256 = "d34fc60c389775f88fa8a54051fdfe90a76ef7864b8f5a813b99d5f0b68ca172"
SETTINGS = ("delayed_control", "prior_selfing", "pollen_discount", "assurance_cost")
ARMS = ("shifted4", "original4_statewise_equal_delivery")
FRACTIONS = (0.25, 0.5, 1.0)
BUDGETS = (6.0, 8.0)
POLICIES = ("native", "fixed_expression")
HORIZON = 80
N_STATES = 165
ATOL = 1e-10


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def expected_cases():
    return set(itertools.product(FRACTIONS, SETTINGS, BUDGETS, ARMS))


def _pair_id(row):
    if not isinstance(row, dict):
        raise ValueError("invalid comparison record")
    labels = ("mismatch_fraction", "setting", "budget", "visitor_arm")
    if any(k not in row for k in labels):
        raise ValueError("comparison metadata missing")
    for k in ("mismatch_fraction", "budget"):
        v = row[k]
        if type(v) not in (int, float) or not np.isfinite(v):
            raise ValueError("nonfinite or nonnumeric comparison metadata")
    return (float(row["mismatch_fraction"]), row["setting"],
            float(row["budget"]), row["visitor_arm"])


def expected_kernel_key(pair, policy):
    frac, setting, budget, arm = pair
    return f"{frac}_{setting}_{budget}_{policy}_{arm}"


def validate_metadata(comparisons, kernel_keys):
    """Require 48 unique declared pairs and 96 unique declared policy keys."""
    if not isinstance(comparisons, list) or len(comparisons) != 48:
        raise ValueError("ALL48 requires exactly 48 comparisons")
    pairs = [_pair_id(row) for row in comparisons]
    if len(set(pairs)) != 48 or set(pairs) != expected_cases():
        raise ValueError("missing, duplicated or foreign ALL48 comparison")
    if len(kernel_keys) != 96 or len(set(kernel_keys)) != 96:
        raise ValueError("ALL96 kernel keys are missing or repeated")
    expected_keys = {expected_kernel_key(pair, policy)
                     for pair in expected_cases() for policy in POLICIES}
    if set(kernel_keys) != expected_keys:
        raise ValueError("kernel keys are not the complete original 96")
    return pairs


def validate_pair_keys(saved_pair_keys, pairs):
    """Bind signed-array row order to the 48 original metadata contexts."""
    expected = [str(tuple(pair)) for pair in pairs]
    actual = list(saved_pair_keys)
    if len(actual) != 48 or actual != expected:
        raise ValueError("signed contribution rows do not match original 48 pair labels")


def _require_finite_array(array, name, shape):
    x = np.asarray(array)
    if x.shape != shape or not np.isfinite(x).all():
        raise ValueError(f"invalid shape or nonfinite values in {name}")
    return x


def validate_arrays(matrices, states, probabilities, endpoint, duration):
    matrices = _require_finite_array(matrices, "kernels", (96, N_STATES, N_STATES))
    states = _require_finite_array(states, "states", (N_STATES, 3))
    probabilities = _require_finite_array(probabilities, "probabilities",
                                           (96, HORIZON + 1, N_STATES))
    endpoint = _require_finite_array(endpoint, "endpoint",
                                     (48, 2, HORIZON, N_STATES))
    duration = _require_finite_array(duration, "duration",
                                     (48, 2, HORIZON, N_STATES))
    if not np.all(states == np.floor(states)) or np.any(states < 0) or np.any(states.sum(1) > 8):
        raise ValueError("invalid K8 genotype census states")
    expected_states = {(a, b, c) for a in range(9) for b in range(9-a)
                       for c in range(9-a-b)}
    if set(map(tuple, states.astype(int))) != expected_states:
        raise ValueError("incomplete or duplicated 165-state census grid")
    if np.any(matrices < -1e-12) or np.max(np.abs(matrices.sum(axis=2) - 1)) > ATOL:
        raise ValueError("invalid stochastic kernels")
    if np.any(probabilities < -1e-12) or np.max(np.abs(probabilities.sum(axis=2) - 1)) > ATOL:
        raise ValueError("invalid saved probability curves")
    return matrices, states, probabilities, endpoint, duration


def verify(kernel_path, readout_path, contributions_path):
    """Authenticate source, validate the grid, recalculate ALL48×2×80."""
    kernel_path, readout_path, contributions_path = map(
        Path, (kernel_path, readout_path, contributions_path))
    if _sha(kernel_path) != ORIGINAL_KERNEL_SHA256:
        raise ValueError("original native kernel SHA256 mismatch")
    readout = json.loads(readout_path.read_text(encoding="utf-8"))
    with np.load(kernel_path, allow_pickle=False) as z:
        keys = [str(k) for k in z["keys"].tolist()]
        matrices, states, probs = z["kernels"], z["states"], z["probabilities"]
    with np.load(contributions_path, allow_pickle=False) as z:
        endpoint, duration = z["endpoint"], z["duration"]
        pair_keys = z["pair_keys"].tolist()
    pairs = validate_metadata(readout["comparisons"], keys)
    validate_pair_keys(pair_keys, pairs)
    matrices, states, probs, endpoint, duration = validate_arrays(
        matrices, states, probs, endpoint, duration)
    index = {k: i for i, k in enumerate(keys)}
    alive = (states.sum(axis=1) > 0).astype(float)
    max_state_error = max_switch_error = 0.0
    state_terms = switch_terms = 0
    for case_no, pair in enumerate(pairs):
        ni = index[expected_kernel_key(pair, "native")]
        fi = index[expected_kernel_key(pair, "fixed_expression")]
        native, fixed = matrices[ni], matrices[fi]
        p0 = probs[ni, 0]
        if not np.allclose(p0, probs[fi, 0], atol=ATOL, rtol=0):
            raise ValueError("native/fixed initial distributions differ")
        p, v, g = [], [], []
        for matrix, archived_curve in ((native, probs[ni]), (fixed, probs[fi])):
            pp = np.zeros((HORIZON + 1, N_STATES))
            pp[0] = p0
            vv = np.zeros_like(pp)
            vv[0] = alive
            for t in range(HORIZON):
                pp[t+1] = pp[t] @ matrix
                vv[t+1] = matrix @ vv[t]
            if np.max(np.abs(pp - archived_curve)) > ATOL:
                raise ValueError("saved curve differs from propagated kernels")
            gg = np.zeros_like(pp)
            gg[1:] = np.cumsum(vv[:-1], axis=0)
            p.append(pp)
            v.append(vv)
            g.append(gg)
        for ref in (0, 1):
            prefix, future = ref, 1-ref
            direction = 1 if ref == 0 else -1
            prefix_rewards = np.r_[0., np.cumsum(p[prefix][:-1] @ alive)]
            hybrid_e = np.asarray([p[prefix][t] @ v[future][HORIZON-t]
                                   for t in range(HORIZON+1)])
            hybrid_d = np.asarray([prefix_rewards[t] + p[prefix][t] @ g[future][HORIZON-t]
                                   for t in range(HORIZON+1)])
            err = max(np.max(np.abs(direction*np.diff(hybrid_e)-endpoint[case_no,ref].sum(axis=1))),
                      np.max(np.abs(direction*np.diff(hybrid_d)-duration[case_no,ref].sum(axis=1))))
            if not np.isfinite(err) or err > ATOL:
                raise ValueError(f"switch-time identity failed for case {case_no} reference {ref}")
            max_switch_error = max(max_switch_error, float(err))
            switch_terms += 2*HORIZON
            for t in range(HORIZON):
                local_e = p[prefix][t] * ((native-fixed) @ v[future][HORIZON-1-t])
                local_d = p[prefix][t] * ((native-fixed) @ g[future][HORIZON-1-t])
                err = max(np.max(np.abs(local_e-endpoint[case_no,ref,t])),
                          np.max(np.abs(local_d-duration[case_no,ref,t])))
                if not np.isfinite(err) or err > ATOL:
                    raise ValueError(f"state-time identity failed for case {case_no} reference {ref} at {t}")
                max_state_error = max(max_state_error, float(err))
                state_terms += 2*N_STATES
    return {
        "status": "ALL48_V2_SOURCE_PINNED_AND_FULL_INVENTORY_RECHECKED",
        "pairs": len(pairs), "state_time_checks": state_terms,
        "switch_time_checks": switch_terms, "max_state_error": max_state_error,
        "max_switch_error": max_switch_error,
        "original_kernel_sha256": ORIGINAL_KERNEL_SHA256,
        "readout_sha256": _sha(readout_path),
        "contributions_sha256": _sha(contributions_path),
        "verifier_sha256": _sha(__file__),
        "new_biological_histories": 0,
        "scope": "source-pinned kernel arithmetic, not new biological-model validation",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kernels", type=Path, required=True)
    parser.add_argument("--readout", type=Path, required=True)
    parser.add_argument("--contributions", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise ValueError("Refuse historical or previous receipt replacement")
    result = verify(args.kernels, args.readout, args.contributions)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write("\n")
    print(json.dumps({k:v for k,v in result.items() if k != "scope"}))


if __name__ == "__main__":
    main()
