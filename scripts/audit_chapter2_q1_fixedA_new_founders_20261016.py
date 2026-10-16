"""Source-only re-admission of new-founder Q1 fixed-assurance nonnecessity.

Inputs: the 32 untouched GitHub Actions shard ZIPs from run 38853989138.
Checks SHA-256 on every original 1,088 case, checks complete 8x8x4x2x2
treatment crossing and original t0 diploid genotype pairing, then calculates
far-minus-near investment in mode=fixed and the far-minus-founder change.

No new model simulations, bootstrap tuning or mutable historical output.
The original 4-setting interaction must match the registered source readout.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

import numpy as np

from scripts.run_chapter2_q1_fresh_founders_20261016 import (
    DESIGN, declared_tasks, load_frozen, sha, source_manifest, task_key,
)

SETTINGS = ("delayed_control", "prior_selfing", "pollen_discount", "assurance_cost")
MAIN = re.compile(
    r"^main_(delayed_control|prior_selfing|pollen_discount|assurance_cost)"
    r"_u0\.01_f(\d+)_v(\d+)_r560401_(near|far)_(fixed|evolving)$"
)


def read_original_shards(root: Path) -> tuple[np.ndarray, np.ndarray, dict]:
    """Return terminal I and founder t0 mean I for the crossed design.

    Every NPZ is authenticated against its own original paired JSON receipt,
    not just its container. Whole-t0-diploid bytes must match for each founder.
    """
    d, _ = load_frozen()
    if d["main_cases"] != 1024 or d["total_cases"] != 1088:
        raise ValueError("Original registered case denominator changed")
    expected = {task_key(t): t for t in declared_tasks(d)}
    seen = {}
    manifest = source_manifest()
    final = np.full((4, 8, 8, 2, 2), np.nan)
    starting = np.full_like(final, np.nan)
    first_diploid = {}
    zero_controls = {}
    source_zip_sha = {}
    for shard in range(32):
        source = root / f"q1-new-founder-shard-{shard}.zip"
        if not source.is_file():
            raise ValueError(f"Missing original shard {shard}: {source}")
        source_zip_sha[source.name] = sha(source.read_bytes())
        with zipfile.ZipFile(source) as archive:
            # Required original source manifest is linked to exact currently
            # checked-out biological code, not just identical across shards.
            raw_manifest = [x for x in archive.namelist()
                            if x.endswith("/sources.json")]
            if len(raw_manifest) != 1:
                raise ValueError("Missing/duplicate source manifest in " + source.name)
            if json.loads(archive.read(raw_manifest[0])) != manifest:
                raise ValueError("Source snapshot differs from archived frozen producer")
            source_digest = sha(json.dumps(
                manifest, sort_keys=True, separators=(",", ":")
            ).encode())
            entries = archive.namelist()
            names = {
                Path(member).stem: member
                for member in entries if member.endswith(".npz")
            }
            receipts = {Path(member).stem: member for member in entries
                        if member.endswith(".json")
                        and not member.endswith("sources.json")
                        and not Path(member).name.startswith("shard_")}
            if names.keys() != receipts.keys():
                raise ValueError("A case is missing its original receipt/NPZ")
            for key, member in names.items():
                if key not in expected or key in seen:
                    raise ValueError("Unexpected or repeated original case: " + key)
                task = expected[key]
                receipt = json.loads(archive.read(receipts[key]))
                raw_npz = archive.read(member)
                if (receipt["task"] != list(task)
                        or receipt["sha256"] != sha(raw_npz)
                        or receipt.get("status") != "complete"
                        or receipt.get("endpoint") != d["updates"]
                        or receipt.get("manifest_sha256") != source_digest):
                    raise ValueError("Original NPZ/receipt pair differs: " + key)
                seen[key] = source.name
                with np.load(io.BytesIO(raw_npz), allow_pickle=False) as file:
                    tr = file["trace"]
                    if (tr.shape != (1001, 10) or tr[0, 0] != 48
                            or tr[-1, 0] <= 0 or not np.isfinite(tr[-1, 2])):
                        raise ValueError("Missing/terminal-extinct origin for " + key)
                    if task[0] == "main":
                        m = MAIN.fullmatch(key)
                        if m is None:
                            raise ValueError("Registered main key shape differs: " + key)
                        setting, founder, visitor, env, mode = m.groups()
                        i = (SETTINGS.index(setting), int(founder) - 560201,
                             int(visitor) - 560301,
                             0 if env == "near" else 1,
                             0 if mode == "fixed" else 1)
                        if (not all(0 <= z < bound for z, bound in
                                    zip(i, final.shape)) or not np.isnan(final[i])):
                            raise ValueError("Invalid or duplicated registered main cell")
                        geno = np.ascontiguousarray(file["state_0"])
                        if (geno.shape != (48, 3, 2) or
                                not np.all(geno[:, 2, :] == .5)):
                            raise ValueError("Original founder assurance alleles differ")
                        gsha = hashlib.sha256(geno.tobytes()).hexdigest()
                        before = first_diploid.setdefault(int(founder), gsha)
                        if gsha != before:
                            raise ValueError("Same founder has different starting genomes")
                        val = float(geno.mean(axis=(0, 2))[1])
                        if not np.isclose(tr[0, 2], val, rtol=0, atol=1e-12):
                            raise ValueError("Original trace t0 != founder diploid I")
                        final[i] = tr[-1, 2]
                        starting[i] = val
                    else:
                        zero_controls[task] = (tr, {
                            name: file[name].copy() for name in file.files
                            if name.startswith("state_")
                        })
    if set(seen) != set(expected) or len(first_diploid) != 8:
        raise ValueError("Not all original 1088 trajectories/8 founders admitted")
    if not np.isfinite(final).all() or not np.isfinite(starting).all():
        raise ValueError("Missing or nonfinite full crossing")
    if len(zero_controls) != 64:
        raise ValueError("Incomplete original zero-mutation technical controls")
    for t, (trace, states) in zero_controls.items():
        if t[-1] != "fixed":
            continue
        paired = t[:-1] + ("evolving",)
        other, other_states = zero_controls[paired]
        if (not np.array_equal(trace, other, equal_nan=True)
                or states.keys() != other_states.keys()
                or any(not np.array_equal(states[k], other_states[k])
                       for k in states)):
            raise ValueError("Fixed/evolvable zero-mutation pair mismatch")
    return final, starting, {
        "source_run": 38853989138,
        "original_cases": len(seen),
        "main_cases": int(np.isfinite(final).sum()),
        "null_pairs_exact": 32,
        "full_initial_founder_genomes": len(first_diploid),
        "original_zip_sha256": source_zip_sha,
        "registered_design_sha256": sha(DESIGN.read_bytes()),
    }


def crossed_ci(grid: np.ndarray, founder_draws: np.ndarray,
               visitor_draws: np.ndarray) -> list[float]:
    vals = grid[founder_draws[:, :, None],
                visitor_draws[:, None, :]].mean(axis=(1, 2))
    return [float(x) for x in np.quantile(vals, [0.025, 0.975])]


def evaluate(final: np.ndarray, t0: np.ndarray, d: dict) -> dict:
    rng = np.random.default_rng(5606162026)
    fi = rng.integers(0, 8, size=(9999, 8))
    vi = rng.integers(0, 8, size=(9999, 8))
    results = []
    for k, setting in enumerate(SETTINGS):
        fixed = final[k, :, :, 1, 0] - final[k, :, :, 0, 0]
        far_drop = final[k, :, :, 1, 0] - t0[k, :, :, 1, 0]
        E = final[k, :, :, 1, 1] - final[k, :, :, 0, 1]
        D = E - fixed
        results.append({
            "setting": setting,
            "fixed_far_minus_near_mean": float(fixed.mean()),
            "fixed_far_minus_near_two_way_bootstrap95": crossed_ci(fixed, fi, vi),
            "fixed_negative_cells_of_64": int((fixed < 0).sum()),
            "fixed_positive_cells_of_64": int((fixed > 0).sum()),
            "fixed_negative_founder_means_of_8": int((fixed.mean(axis=1) < 0).sum()),
            "fixed_negative_visitor_means_of_8": int((fixed.mean(axis=0) < 0).sum()),
            "fixed_far_absolute_change_from_founders_mean": float(far_drop.mean()),
            "fixed_far_absolute_decline_cells_of_64": int((far_drop < 0).sum()),
            "evolutionary_interaction_D_mean": float(D.mean()),
        })
    return {
        "status": "ORIGINAL_Q1_1088_FIXED_A_NONNECESSITY_RECHECK",
        "provenance": d,
        "settings": results,
        "scientific_limit": (
            "A capacity fixed 0.5 still allows realized selfing. These results "
            "test A-evolution nonnecessity for specified endpoint contrasts, "
            "not natural-island causation or selfing-absence nonnecessity."
        ),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--shards", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    if args.out.exists():
        raise FileExistsError("Refuse to overwrite source-bound new-founder audit")
    a, t0, provenance = read_original_shards(args.shards)
    out = evaluate(a, t0, provenance)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"], "source_admitted": provenance["original_cases"],
        "per_setting": [{k: row[k] for k in (
            "setting", "fixed_far_minus_near_mean",
            "fixed_negative_cells_of_64",
            "fixed_far_absolute_decline_cells_of_64",
            "evolutionary_interaction_D_mean")}
            for row in out["settings"]]
    }, indent=2))


if __name__ == "__main__":
    main()
