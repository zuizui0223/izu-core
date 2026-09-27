"""Extract a compact, auditable shard from the frozen Model 3 Ch2 bridge campaign."""
from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path

import numpy as np

from scripts.model3_island.design import canonical, digest


MODES = {
    "individual": ("trait_mean", "population"),
    "density": ("density_traits", "density_mass"),
}


def _scientific_projection(d: dict) -> dict:
    x = json.loads(json.dumps(d))
    x.pop("history_seeds", None)
    x.pop("cases", None)
    return x


def extract(full_design: dict, shard_design: dict, campaign: Path) -> dict:
    if _scientific_projection(full_design) != _scientific_projection(shard_design):
        raise ValueError("shard design differs from frozen design beyond execution partition")
    full_hist = list(full_design["history_seeds"])
    shard_hist = list(shard_design["history_seeds"])
    if not shard_hist or len(set(shard_hist)) != len(shard_hist):
        raise ValueError("empty or duplicate shard histories")
    if any(h not in full_hist for h in shard_hist):
        raise ValueError("shard contains undeclared history")
    if shard_hist != [h for h in full_hist if h in set(shard_hist)]:
        raise ValueError("shard history order differs from frozen design")
    expected = len(shard_hist) * len(shard_design["demographic_seeds"]) * len(shard_design["starts"]) * len(shard_design["arms"])
    if shard_design["cases"] != expected:
        raise ValueError("shard case count mismatch")

    campaign = Path(campaign)
    status = json.loads((campaign / "campaign_status.json").read_text())
    if not status.get("complete") or status["completed"] != expected or status["expected"] != expected:
        raise ValueError(f"incomplete shard campaign: {status}")
    if json.loads((campaign / "manifest.json").read_text()) != shard_design:
        raise ValueError("shard manifest mismatch")
    shard_hash = digest(shard_design)
    if status["manifest_hash"] != shard_hash:
        raise ValueError("shard manifest hash mismatch")

    starts = list(shard_design["starts"])
    demos = list(shard_design["demographic_seeds"])
    arms = list(shard_design["arms"])
    shape = (len(starts), len(shard_hist), len(demos))
    changes = {(arm, mode): np.full(shape, np.nan) for arm in arms for mode in MODES}
    occupancy = {(arm, mode): np.zeros(shape, float) for arm in arms for mode in MODES}
    visitors = {}
    receipt_root = sha256()

    for si, start in enumerate(starts):
        sid = int(round(start * 10))
        for hi, hs in enumerate(shard_hist):
            for di, ds in enumerate(demos):
                for arm in arms:
                    case_id = f"{arm}-s{sid}-h{hs}-d{ds}"
                    folder = campaign / case_id
                    receipt = json.loads((folder / "receipt.json").read_text())
                    inp = json.loads((folder / "input.json").read_text())
                    raw = (folder / "arrays.npz").read_bytes()
                    if receipt.get("status") != "complete":
                        raise ValueError(f"incomplete receipt: {case_id}")
                    if receipt["manifest_hash"] != shard_hash or inp.get("manifest_hash") != shard_hash:
                        raise ValueError(f"manifest identity mismatch: {case_id}")
                    if inp.get("id") != case_id or digest(inp) != receipt["case_hash"]:
                        raise ValueError(f"case identity mismatch: {case_id}")
                    if sha256(raw).hexdigest() != receipt["arrays_sha256"]:
                        raise ValueError(f"array hash mismatch: {case_id}")
                    receipt_root.update(case_id.encode())
                    receipt_root.update(receipt["arrays_sha256"].encode())

                    with np.load(folder / "arrays.npz", allow_pickle=False) as a:
                        vc = np.asarray(a["visitor_count"], int)
                        vk = (arm, hi)
                        if vk in visitors:
                            np.testing.assert_array_equal(visitors[vk], vc)
                        else:
                            visitors[vk] = vc.copy()
                        for mode, (trait_key, pop_key) in MODES.items():
                            tr = np.asarray(a[trait_key], float)
                            pop = np.asarray(a[pop_key], float)
                            occupancy[arm, mode][si, hi, di] = float(pop[-1] > 0)
                            valid = bool(pop[0] > 0 and pop[-1] > 0 and np.isfinite(tr[[0, -1], 1]).all())
                            if valid:
                                changes[arm, mode][si, hi, di] = float(tr[-1, 1] - tr[0, 1])

    return {
        "schema_version": "1.0",
        "status": "complete_verified_shard",
        "full_design_hash": digest(full_design),
        "shard_design_hash": shard_hash,
        "histories": shard_hist,
        "starts": starts,
        "demographic_seeds": demos,
        "arms": arms,
        "modes": list(MODES),
        "cases_verified": expected,
        "receipt_arrays_hash_root": receipt_root.hexdigest(),
        "changes": {f"{a}|{m}": changes[a, m].tolist() for a in arms for m in MODES},
        "terminal_occupancy": {f"{a}|{m}": occupancy[a, m].tolist() for a in arms for m in MODES},
        "visitor_count": {
            f"{arm}|{shard_hist[hi]}": visitors[arm, hi].tolist()
            for arm in arms for hi in range(len(shard_hist))
        },
        "claim_boundary": "execution shard only; scientific cohort is the union of all histories in the frozen full design",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--full-design", required=True)
    p.add_argument("--shard-design", required=True)
    p.add_argument("--campaign", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    full = json.loads(Path(a.full_design).read_text())
    shard = json.loads(Path(a.shard_design).read_text())
    result = extract(full, shard, Path(a.campaign))
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(canonical(result))
    print(json.dumps({
        "status": result["status"],
        "histories": result["histories"],
        "cases_verified": result["cases_verified"],
        "receipt_arrays_hash_root": result["receipt_arrays_hash_root"],
    }))


if __name__ == "__main__":
    main()
