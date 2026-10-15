"""Independent-source cohort in native frozen Model 3, t0..200.

Prospectively fixed before execution:
docs/protocols/chapter2_far_early_independent_visitor_knockout_20261015.json

Runner must execute ONLY when explicitly given the verified frozen original
repository source and the frozen protocol. This file does not redefine the
reproductive, Mendelian, mutation or demographic source operators. It creates
new independent visitor histories and two new founder backgrounds. Distinct
from old source replays and post-outcome t200 conditional futures.

Expected full: 64 visitor histories × 2 founders × 4 mating rules × 2
visitor manipulations × 2 A policies = 2048 native paths / 409600 updates.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

from scripts.model3_island.types import VisitorState
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.randomness import stream, STREAM_IDS
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.run_model3_persistent_isolation import exposure
from scripts.run_chapter2_assurance_generality import (
    config, load_design, DEFAULT_DESIGN,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs/protocols/chapter2_far_early_independent_visitor_knockout_20261015.json"
SOURCE_MANIFEST = ROOT / "frozen_source_manifest.json"
YEAR_END = 200
CHECKPOINTS = (0, 50, 100, 200)
SETTINGS = ("delayed_control", "prior_selfing", "pollen_discount", "assurance_cost")
VISITOR_REGIMES = ("far_original_mechanism", "zero_visitors_from_t0")
MODES = ("fixed", "evolving")
FOUNDERS = (28111601, 28111602)
DEMOGRAPHY = (28112601, 28112602)
FIRST, LAST = 28110601, 28110664


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def preflight():
    p = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    d = load_design(DEFAULT_DESIGN)
    f = p["factorization"]
    if (p["status"] != "PROSPECTIVELY_FROZEN_BEFORE_NEW_INDEPENDENT_MODEL_RUN"
        or f["settings"] != list(SETTINGS)
        or f["visitor_regimes"] != list(VISITOR_REGIMES)
        or f["assurance_modes"] != list(MODES)
        or f["founder_seeds"] != list(FOUNDERS)
        or f["paired_demographic_seeds_by_founder"] != list(DEMOGRAPHY)
        or f["visitor_history_seed_first"] != FIRST
        or f["visitor_history_seed_last"] != LAST
        or f["n_paths"] != 2048
        or f["total_native_updates"] != 409600
        or f["years"] != YEAR_END
        or f["mutation_probability"] != .01
        or f["founder_count"] != 48
        or f["mutation_sd"] != .05):
        raise AssertionError("frozen independent trial manifest disagrees")
    # The source archive includes a sha manifest; only original operators and
    # original model designs are admitted. They MUST match bytes exactly.
    if not SOURCE_MANIFEST.is_file():
        raise FileNotFoundError("extract and SHA-verify original 2026-10-06 sources.zip")
    manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    for name, expected in manifest.items():
        path = ROOT / name
        if not path.exists() or sha(path.read_bytes()) != expected:
            raise AssertionError("frozen source path SHA violation " + name)
    return p, d, sha(PROTOCOL.read_bytes()), sha(SOURCE_MANIFEST.read_bytes())


def founder_pair(seed):
    p = founders_from_spec(
        dict(count=48, draw_count=48, means=[.5,.5,.5], sd=.15, birth_year=0),
        seed,
    )
    a = p.alleles.copy()
    a[:, 2, :] = .5
    return replace(p, alleles=a)


def price_ensemble(state, ledger):
    I = state.alleles[:,1,:].mean(axis=1)
    W = .5*(ledger.outcross.sum(axis=0) + ledger.outcross.sum(axis=1)) + ledger.self_viable
    if len(I)==0 or float(W.sum())<=0:
        return np.nan
    return float(np.dot(W,I)/W.sum() - I.mean())


def one_case(design, setting, history_seed, founder_seed, dem_seed, regime, mode):
    cfg = config(design, setting, .01, mode)
    cfg = replace(cfg, years=YEAR_END)
    f = founder_pair(founder_seed)
    h = exposure(history_seed, "far")
    empty = VisitorState(
        np.empty(0,dtype=np.int64),
        np.empty(0,dtype=float),
        np.empty(0,dtype=float),
        np.empty(0,dtype=float),
    )
    rseed = int(np.random.SeedSequence([history_seed, dem_seed]).generate_state(1)[0])
    streams = {name: stream(rseed,name,0) for name in STREAM_IDS}
    # annual columns: census, I, A expressed, I variance, visitors, expected
    # parent-genetic Price response, realised I update, Price contribution to
    # new-census I, realised transmission residual, nonresident offspring,
    # selfed offspring, outcross offspring.
    annual = np.full((YEAR_END + 1,12),np.nan,dtype=float)
    checkpoint = np.full((len(CHECKPOINTS),48,3,2),np.nan,dtype=float)
    state = f
    for t in range(YEAR_END+1):
        n = len(state.ids)
        if n>0:
            gen = state.alleles
            I = gen[:,1,:].mean()
            AA = gen[:,2,:].mean() if mode=="evolving" else cfg.fixed_assurance
            annual[t,0:4] = [n,I,AA,float(gen[:,1,:].mean(axis=1).var())]
        else:
            annual[t,0] = 0
        if t in CHECKPOINTS:
            checkpoint[CHECKPOINTS.index(t),:n] = state.alleles
        if t == YEAR_END:break
        v = h.visitors[t] if regime=="far_original_mechanism" else empty
        annual[t,4] = len(v.ids)
        ledger = reproduce(state,v,cfg)
        shift = price_ensemble(state,ledger)
        annual[t,5] = shift
        newer,info = advance(
            state,ledger,h.seed_candidates[t],cfg,streams,year=t,
            mutation_traits=(True,True,mode=="evolving"),
        )
        nxt = newer.alleles[:,1,:].mean() if len(newer.ids)>0 else np.nan
        delta=nxt-annual[t,1] if np.isfinite(nxt) and n>0 else np.nan
        annual[t,6] = delta
        # Original Config has survival=0; verify source identity at each step.
        if info["survivors"] != 0 or info["immigrant_recruits"] != 0:
            raise AssertionError("unexpected source adult survival/seed immigrant")
        annual[t,7] = shift if info["resident_recruits"] else 0.
        annual[t,8] = delta - annual[t,7] if np.isfinite(delta) else np.nan
        annual[t,9:12] = [
            info["resident_recruits"],
            info["resident_selfed_recruits"],
            info["resident_outcross_recruits"],
        ]
        if np.isfinite(delta):
            assert abs(delta-(annual[t,7]+annual[t,8])) < 1e-12
        state = newer
    if mode == "fixed":
        assert all(abs(a-.5)<1e-12 for a in annual[:,2] if np.isfinite(a))
    assert annual.shape == (201,12) and checkpoint.shape == (4,48,3,2)
    return annual, checkpoint


def evaluate_subset(history_first: int, history_last: int, *, output: Path):
    if output.exists():
        raise FileExistsError("source result exists: refuse overwrite")
    p,d,protocol_sha,source_sha=preflight()
    if not FIRST<=history_first<=history_last<=LAST:
        raise ValueError("outside preregistered new-history seed bounds")
    records=[]
    all_annual=[]
    checkpoints=[]
    for seed in range(history_first,history_last+1):
        for founder,dem in zip(FOUNDERS,DEMOGRAPHY):
            for setting in SETTINGS:
                for visitors in VISITOR_REGIMES:
                    for assurance in MODES:
                        a,c=one_case(d,setting,seed,founder,dem,visitors,assurance)
                        records.append(dict(history=seed,founder=founder,
                                            demographic=dem,setting=setting,
                                            visitors=visitors,assurance=assurance,
                                            I_initial=float(a[0,1]),
                                            I_t200=float(a[-1,1]) if np.isfinite(a[-1,1]) else None,
                                            A_t200=float(a[-1,2]) if np.isfinite(a[-1,2]) else None,
                                            t200_N=int(a[-1,0])))
                        all_annual.append(a);checkpoints.append(c)
        print("completed independent visitor history",seed,flush=True)
    annual=np.stack(all_annual)
    checkpoint=np.stack(checkpoints)
    # New outcomes are biological model trajectories; freeze exact complete
    # original source fingerprints, and do NOT add these cases to the old 64.
    output.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(output, annual=annual, checkpoint_alleles=checkpoint)
    receipt={
      "status":"NEW_INDEPENDENT_MODEL3_SUBSET",
      "protocol_sha256":protocol_sha,
      "frozen_source_manifest_sha256":source_sha,
      "cases":records,
      "n_paths":len(records),
      "new_updates":len(records)*YEAR_END,
      "subset_history_seeds":[history_first,history_last],
      "array_npz_sha256":sha(output.read_bytes()),
      "source_original_vs_new_independence":"original histories 26110601..26110664, newly proposed histories 28110601..28110664",
      "claim_ceiling":"Exploratory/confirmatory status follows PRE-FROZEN design; partial subsets not independent confirmation."
    }
    marker=output.with_suffix(".json")
    if marker.exists():
        raise FileExistsError("readout receipt exists")
    marker.write_text(json.dumps(receipt,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    return receipt


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--history-first",type=int,default=FIRST)
    ap.add_argument("--history-last",type=int,default=LAST)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    r=evaluate_subset(args.history_first,args.history_last,output=args.output)
    print(json.dumps({"status":r["status"],"cases":r["n_paths"],"updates":r["new_updates"]}))


if __name__ == "__main__":
    main()
