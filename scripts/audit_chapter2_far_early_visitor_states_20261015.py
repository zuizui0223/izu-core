"""Retrospective visit-present/absent partition of original far t0..200 I response.

Reads SHA-locked original-replay GitHub Action ZIPs (4 shards, 512 cases).
History is the inferential unit (64 shared visitor sequences), not 256
independent trials. Conditional on realized visitor and genotype trajectories:
this is descriptive algebra, not do(visitor=0), causal mediation, or fresh
ecological replication.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "docs/deposit/chapter2_far_asymmetry_source_artifact_inventory_20261015.json"
PROTOCOL = ROOT / "docs/protocols/chapter2_far_original_0_200_accounting_20261015.json"
SETTINGS = ("delayed_control", "prior_selfing", "pollen_discount", "assurance_cost")
MODES = ("fixed", "evolving")
TERMS = ("realized_delta_I", "weighted_parental_Price_I", "recruit_transmission_residual_I", "survivor_sampling_I")
BOOTSTRAPS = 4096
YEAR_END = 200
FIRST, LAST = 26110601, 26110664
REGISTERED_T200_EF = dict(
    delayed_control=0.05535860437663109,
    prior_selfing=0.059925395926339234,
    pollen_discount=0.030348554117056982,
    assurance_cost=0.027221577411020725,
)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def expected_shards():
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    old = next(x for x in inventory["new_workflows"]
               if x["name"] == "exact_original_t0_200")
    assert old["run_id"] == 38712511100
    assert old["source_original_cases"] == 512
    items = {
        x["name"]: x for x in old["artifacts"]
        if x["name"].startswith("far-original-0-200-genomes-shard-")
    }
    assert len(items) == 4
    return [
        items[f"far-original-0-200-genomes-shard-{i}"]["sha256_of_artifact_zip"].removeprefix("sha256:")
        for i in range(4)
    ]


def read_source(archive_paths):
    if len(archive_paths) != 4:
        raise ValueError("exact four frozen source archives required")
    expected = expected_shards()
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    protocol_digest = sha(PROTOCOL.read_bytes())
    if protocol["source_horizon_end"] != YEAR_END or protocol["settings"] != list(SETTINGS):
        raise AssertionError("original source contract changed")
    records = {}
    for shard, source in enumerate(archive_paths):
        raw = Path(source).read_bytes()
        if sha(raw) != expected[shard]:
            raise AssertionError("original GitHub Actions shard ZIP checksum mismatch")
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            manifest = json.loads(z.read("readout.json"))
            seeds = [s for s in range(FIRST, LAST + 1) if (s - FIRST) % 4 == shard]
            if (manifest["status"] != "EXACT_ORIGINAL_T0_T200_SOURCE_REPLAY_SHARD"
                    or manifest["shard_index"] != shard
                    or manifest["shard_count"] != 4
                    or manifest["history_seeds"] != seeds
                    or manifest["n_cases"] != 128
                    or not manifest["original_source_t200_complete_genotype_parity"]):
                raise AssertionError("replay source manifest invalid")
            for record in manifest["cases"]:
                key = (record["setting"], record["history_seed"], record["mode"])
                if key in records:
                    raise AssertionError("duplicate original source case")
                case_raw = z.read(record["key"] + ".npz")
                if (sha(case_raw) != record["npz_sha256"]
                        or json.loads(z.read(record["key"] + ".json")) != record
                        or record["source_contract_sha256"] != protocol_digest
                        or not record["source_original_t200_exact_allele_parity"]):
                    raise AssertionError("case receipt/allele audit mismatch")
                with np.load(io.BytesIO(case_raw), allow_pickle=False) as values:
                    arr = {k: values[k].copy() for k in
                           ("n_visitors", "N", "mean_I", "mean_A_expressed") + TERMS}
                if (arr["n_visitors"].shape != (YEAR_END,)
                        or arr["mean_I"].shape != (YEAR_END+1,)
                        or (arr["N"] <= 0).any()
                        or not np.allclose(np.diff(arr["mean_I"]), arr["realized_delta_I"],
                                           atol=1e-12, rtol=0)
                        or not np.allclose(arr["realized_delta_I"],
                            arr["weighted_parental_Price_I"] +
                            arr["recruit_transmission_residual_I"] +
                            arr["survivor_sampling_I"], atol=1e-12, rtol=0)):
                    raise AssertionError("source-genetic annual identity mismatch")
                records[key] = arr
    expect = {(setting, h, mode) for setting in SETTINGS for h in range(FIRST, LAST + 1)
              for mode in MODES}
    if set(records) != expect:
        raise AssertionError("missing original source-history treatment")
    return records


def partition_pair(e, f):
    if (not np.array_equal(e["n_visitors"], f["n_visitors"])
            or abs(e["mean_I"][0]-f["mean_I"][0]) > 1e-12):
        raise AssertionError("mismatched paired visitor / original genotype states")
    visitor_count = e["n_visitors"]
    masks = {"absent": visitor_count == 0, "present": visitor_count > 0}
    if not (masks["absent"].any() and masks["present"].any()):
        raise AssertionError("division undefined: one visitation stratum missing")
    result = {
        "zero_visitor_years": int(masks["absent"].sum()),
        "present_visitor_years": int(masks["present"].sum()),
        "terminal_I_EminusF": float(e["mean_I"][-1]-f["mean_I"][-1]),
        "terminal_A_EminusF": float(e["mean_A_expressed"][-1]-f["mean_A_expressed"][-1]),
    }
    for label, mask in masks.items():
        for term in TERMS:
            result[f"{label}_{term}"] = float(
                np.sum(e[term][mask]-f[term][mask])
            )
        if abs(result[f"{label}_realized_delta_I"]
               - sum(result[f"{label}_{t}"] for t in TERMS[1:])) > 1e-11:
            raise AssertionError("visitor-state additive source partition failed")
    if abs(result["terminal_I_EminusF"]
           - result["absent_realized_delta_I"]
           - result["present_realized_delta_I"]) > 1e-11:
        raise AssertionError("decomposed I response does not telescope")
    result["annual_absent_minus_present_EF"] = (
        result["absent_realized_delta_I"]/result["zero_visitor_years"]
        - result["present_realized_delta_I"]/result["present_visitor_years"]
    )
    return result


def interval(x, *, seed):
    a = np.asarray(x, dtype=float)
    if a.shape != (64,) or not np.isfinite(a).all():
        raise AssertionError("64 complete source histories required")
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, 64, size=(BOOTSTRAPS, 64))
    ci = np.quantile(a[indices].mean(axis=1), [.025, .975])
    return {
        "mean": float(a.mean()),
        "history_bootstrap95_descriptive": [float(ci[0]), float(ci[1])],
        "positive": int((a > 0).sum()),
        "negative": int((a < 0).sum()),
        "n_histories": 64,
    }


def correlation(x, y, *, seed):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.shape != (64,) or y.shape != (64,):
        raise AssertionError("invalid history clusters")
    rho = float(spearmanr(x, y).statistic)
    rng = np.random.default_rng(seed)
    estimates = []
    for _ in range(BOOTSTRAPS):
        take = rng.integers(0, 64, size=64)
        r = spearmanr(x[take], y[take]).statistic
        if np.isfinite(r):
            estimates.append(float(r))
    if len(estimates) != BOOTSTRAPS:
        raise AssertionError("undefined history-rank correlation bootstrap")
    lo, hi = np.quantile(estimates, [.025, .975])
    return {"rho": rho,
            "history_bootstrap95_descriptive": [float(lo), float(hi)],
            "n_histories": 64}


def run(shards):
    raw = read_source(shards)
    result = {}
    source_free = None
    for i, setting in enumerate(SETTINGS):
        histories = []
        for h in range(FIRST, LAST + 1):
            pair = partition_pair(raw[setting,h,"evolving"], raw[setting,h,"fixed"])
            pair["history"] = h
            histories.append(pair)
        zero = [r["zero_visitor_years"] for r in histories]
        if source_free is None:
            source_free = zero
        elif zero != source_free:
            raise AssertionError("same 64 source visitor histories differ by mating rule")
        total = [r["terminal_I_EminusF"] for r in histories]
        if abs(np.mean(total)-REGISTERED_T200_EF[setting]) > 1e-12:
            raise AssertionError("original t200 E-F sign/mean identity changed")
        summary = {
            "visitor_free_years_min": min(zero),
            "visitor_free_years_mean": float(np.mean(zero)),
            "visitor_free_years_max": max(zero),
            "EminusF_I_t200": interval(total, seed=20261015+i*100),
            "absence_count_vs_t200_investment": correlation(zero, total, seed=20261015+i*100+1),
            "absence_count_vs_t200_A": correlation(
                zero, [r["terminal_A_EminusF"] for r in histories],
                seed=20261015+i*100+2),
            "states": {},
            "annual_absence_minus_presence_EF": interval(
                [r["annual_absent_minus_present_EF"] for r in histories],
                seed=20261015+i*100+3),
        }
        for j, state in enumerate(("absent", "present")):
            summary["states"][state] = {
                term: interval([r[f"{state}_{term}"] for r in histories],
                               seed=20261015+i*100+10+j*10+k)
                for k,term in enumerate(TERMS)
            }
        if abs(summary["states"]["absent"]["realized_delta_I"]["mean"]
               + summary["states"]["present"]["realized_delta_I"]["mean"]
               - summary["EminusF_I_t200"]["mean"]) > 1e-12:
            raise AssertionError("mean visitor-state sums changed")
        result[setting] = summary
    return {
        "status": "RETROSPECTIVE_SOURCE_ONLY_VISITOR_STATE_PARTITION",
        "original_history_clusters": 64,
        "source_original_cases": 512,
        "new_simulation_updates": 0,
        "original_source_first_of_eight_demographic_repeats": 26111601,
        "original_visitor_history_seeds": [FIRST, LAST],
        "source_reconstruction_workflow": 38712511100,
        "n_cluster_bootstraps_descriptive": BOOTSTRAPS,
        "four_settings": result,
        "boundary": [
            "This is partitioning realized time steps by zero vs nonzero visitor count; not an intervention that changes visitor supply.",
            "The zero-visitor local gradient remains -2*c_I*I, not zero.",
            "No causal shares, no independent ecological replicate, no source-identified drift coefficient.",
            "Correlations are post-outcome screening; bootstrap intervals are descriptive and not multiplicity-adjusted."
        ]
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--shards", type=Path, nargs=4, required=True,
                   help="four authentic archive ZIPs in shard order 0,1,2,3")
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    if a.out.exists():
        raise FileExistsError("refuse overwriting original source diagnostic")
    result = run(a.shards)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+"\n",
                     encoding="utf-8")
    print(json.dumps({"status": result["status"],
                      "source_cases": result["source_original_cases"],
                      "new_simulation_updates": 0,
                      "histories": result["original_history_clusters"]}))


if __name__ == "__main__":
    main()
