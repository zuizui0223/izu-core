"""New, versioned Q2 intervention: I allele support vs six-class response order.

Technical smoke is NOT a research result. Full launch requires an independently
recorded, design-SHA-bound approval. Frozen biological operators are untouched.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.run_chapter2_assurance_generality import config as original_config
from scripts.run_chapter2_assurance_generality import load_design as original_design
from scripts.run_model3_persistent_isolation import exposure


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DESIGN = ROOT / "data/designs/chapter2_q2_i_support_order_20261016.json"
STATUS = "prospective_design_frozen_before_new_biological_outcomes_execution_hold"
CLASSES = ("assurance_first", "investment_first", "near_simultaneous",
           "assurance_only", "investment_only", "neither")
STATE_FIELDS = ("alleles", "allele_origin", "mutation_flags", "ids", "birth_years")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_protocol(path: Path = DEFAULT_DESIGN) -> dict:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    f, v = d["founders"], d["visitors"]
    p = d["policies"]
    if (d["status"] != STATUS or d["reproduction_setting"] != "assurance_cost"
            or d["horizon"] != 200 or f["plants"] != 48
            or f["count"] != f["last"] - f["first"] + 1 != 8
            or v["count"] != v["last"] - v["first"] + 1 != 8
            or set(v["arms"]) != {"far", "near"}
            or set(p) != {"dense_reachable", "sparse_reachable", "dense_unreachable"}
            or (p["dense_reachable"]["I_halfwidth"], p["dense_reachable"]["carrier_count"]) != (.078125, 24)
            or (p["sparse_reachable"]["I_halfwidth"], p["sparse_reachable"]["carrier_count"]) != (.078125, 12)
            or (p["dense_unreachable"]["I_halfwidth"], p["dense_unreachable"]["carrier_count"]) != (.046875, 24)
            or d["mutations"]["traits_enabled"] !=
            {"match": True, "investment": False, "assurance": True}
            or d["design_matrix"]["total_full_trajectories"] != 384
            or d["response"]["all_six_classes"] != list(CLASSES)):
        raise ValueError("Unadmitted prospective Q2 support/order design")
    return d


def declared_tasks(d: dict) -> list[tuple[int, int, str, str]]:
    f, v = d["founders"], d["visitors"]
    cases = [(fs, vs, arm, policy)
             for fs in range(f["first"], f["last"] + 1)
             for vs in range(v["first"], v["last"] + 1)
             for arm in v["arms"] for policy in d["policies"]]
    if len(cases) != d["design_matrix"]["total_full_trajectories"] or len(set(cases)) != len(cases):
        raise ValueError("Incomplete or duplicated 384-case inventory")
    return cases


def founder_state(d: dict, founder_seed: int, policy: str):
    f = d["founders"]
    if not f["first"] <= founder_seed <= f["last"] or policy not in d["policies"]:
        raise ValueError("undeclared founder seed or policy")
    origin = founders_from_spec(
        dict(count=f["plants"], draw_count=f["plants"], means=[.5, .5, .5],
             sd=f["sd_original_draw"], birth_year=0), founder_seed)
    a = origin.alleles.copy()
    a[:, 1, :] = f["expressed_I"]
    h_a = f["A_halfwidth"]
    a[:, 2, 0] = f["expressed_A"] - h_a
    a[:, 2, 1] = f["expressed_A"] + h_a
    rng = np.random.default_rng(np.random.SeedSequence(
        [founder_seed, f["carrier_assignment_salt"]]))
    chosen = rng.permutation(f["plants"])[:d["policies"][policy]["carrier_count"]]
    width = d["policies"][policy]["I_halfwidth"]
    a[chosen, 1, 0] -= width
    a[chosen, 1, 1] += width
    state = replace(origin, alleles=a)
    if not np.array_equal(state.alleles.mean(axis=2)[:, 1], np.full(f["plants"], .5)):
        raise AssertionError("I expression differs at initial intervention")
    if not np.array_equal(state.alleles.mean(axis=2)[:, 2], np.full(f["plants"], .5)):
        raise AssertionError("A expression differs at initial intervention")
    assert np.count_nonzero(state.alleles[:, 1, 0] < .5) == len(chosen)
    return state


def native_config(d: dict):
    source = original_design(ROOT / d["source_biology"])
    c = original_config(source, d["reproduction_setting"],
                        d["mutations"]["probability"], "evolving")
    c = replace(c, years=d["horizon"], mutation_sd=d["mutations"]["sd"])
    if c.seed_arrival.supply != 0 or c.capacity != d["founders"]["plants"]:
        raise ValueError("Experiment assumes no I immigration and fixed K=48")
    return c


def response_class(trace: np.ndarray, response: dict) -> dict:
    """Unconditional all-start classification with explicit censoring."""
    t = np.asarray(trace, dtype=float)
    if t.ndim != 2 or t.shape[1] != 5 or not np.isfinite(t[:, 0]).all():
        raise ValueError("Wrong or nonfinite trajectory census")
    if not np.isfinite(t[0, 1:3]).all() or t[0, 0] <= 0:
        raise ValueError("Invalid founder state")
    eligible = t[:, 0] > 0
    window = int(response["consecutive_occupied_censuses"])
    flags = {
        "A": eligible & np.isfinite(t[:, 1]) &
             (t[:, 1] - t[0, 1] >= response["A_positive"] - 1e-12),
        "I": eligible & np.isfinite(t[:, 2]) &
             (t[0, 2] - t[:, 2] >= response["I_negative"] - 1e-12),
    }
    starts = {}
    for key in ("A", "I"):
        hit = np.flatnonzero(np.convolve(flags[key].astype(int), np.ones(window, dtype=int),
                                         mode="valid") == window)
        starts[key] = int(hit[0]) if len(hit) else None
    a, i = starts["A"], starts["I"]
    tie = response["ties_within_updates"]
    label = ("neither" if a is None and i is None else
             "investment_only" if a is None else
             "assurance_only" if i is None else
             "near_simultaneous" if abs(a - i) <= tie else
             "assurance_first" if a < i else "investment_first")
    return {"label": label, "A_start": a, "I_start": i, "A_event": a is not None,
            "I_event": i is not None, "occupied_terminal": bool(eligible[-1]),
            "first_extinction": next((int(n) for n, live in enumerate(eligible) if not live), None)}


def simulate(d: dict, task: tuple, *, steps: int, capture_genomes: bool = True) -> dict:
    fs, vs, arm, policy = task
    if task not in declared_tasks(d):
        raise ValueError("undeclared Q2 matched task")
    if not 1 <= steps <= d["horizon"]:
        raise ValueError("Invalid number of steps")
    c = native_config(d)
    env = exposure(vs, arm)
    state = founder_state(d, fs, policy)
    initial_values = frozenset(float(x) for x in state.alleles[:, 1, :].ravel())
    master = int(np.random.SeedSequence(
        [fs, vs, d["randomization"]["master_seed_salt"]]).generate_state(1)[0])
    streams = {name: stream(master, name, 0) for name in STREAM_IDS}
    trace = np.full((steps + 1, 5), np.nan)
    states = {field: [] for field in STATE_FIELDS}
    parentage = []
    offsets = [0]
    parent_offsets = [0]
    for t in range(steps + 1):
        trace[t, 0] = len(state.ids)
        if len(state.ids):
            z = state.alleles.mean(axis=2)
            trace[t, 1:3] = z.mean(axis=0)[2], z.mean(axis=0)[1]  # A, I
            trace[t, 3] = state.alleles[:, 1, :].min()
            trace[t, 4] = np.sum(state.alleles[:, 1, :] < .45)
        if capture_genomes:
            for field in STATE_FIELDS:
                states[field].append(np.asarray(getattr(state, field)))
            offsets.append(offsets[-1] + len(state.ids))
        if t == steps:
            break
        ledger = reproduce(state, env.visitors[t], c)
        state, info = advance(
            state, ledger, env.seed_candidates[t], c, streams, year=t,
            mutation_traits=(True, False, True))
        if not set(map(float, state.alleles[:, 1, :].ravel())) <= initial_values:
            raise AssertionError("I alleles created without mutation/immigration")
        if capture_genomes:
            parentage.append(info["parentage"])
            parent_offsets.append(parent_offsets[-1] + len(info["parentage"]))
    result = {"task": task, "trace": trace, "status":
              "technical_smoke_no_biological_adjudication" if steps < d["horizon"]
              else "full_unadjudicated_trajectory"}
    if capture_genomes:
        result["offsets"] = np.asarray(offsets, dtype=np.int64)
        result["parentage_offsets"] = np.asarray(parent_offsets, dtype=np.int64)
        result["parentage"] = np.concatenate(parentage, axis=0) if parentage else np.empty((0, 3), dtype=np.int64)
        for field in STATE_FIELDS:
            result[field] = np.concatenate(states[field], axis=0)
    if steps == d["horizon"]:
        result["events"] = response_class(trace, d["response"])
    return result


def source_manifest(design_path: Path) -> dict:
    paths = [Path(__file__), design_path, ROOT / "scripts/run_model3_persistent_isolation.py",
             ROOT / "scripts/run_chapter2_assurance_generality.py",
             ROOT / "data/design/chapter2_assurance_generality_20261006.json",
             ROOT / "data/design/model3_ch2_bridge_20260927.json"]
    paths.extend(sorted((ROOT / "scripts/model3_island").glob("*.py")))
    return {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in paths}


def technical_smoke(d: dict, design_path: Path) -> dict:
    f, v = d["founders"]["first"], d["visitors"]["first"]
    c = native_config(d)
    proof = []
    for arm in d["visitors"]["arms"]:
        visitors = exposure(v, arm).visitors[0]
        founders = [founder_state(d, f, p) for p in d["policies"]]
        a = [reproduce(z, visitors, c) for z in founders]
        # The intervention is hidden from reproduction until Mendelian segregation.
        for other in a[1:]:
            for name in ("maternal", "paternal", "outcross", "self_raw", "self_viable", "ovules"):
                np.testing.assert_array_equal(getattr(a[0], name), getattr(other, name))
        for policy in d["policies"]:
            task = (f, v, arm, policy)
            n = min(d["technical_smoke"]["max_steps"], d["horizon"])
            run = simulate(d, task, steps=n)
            if (run["trace"][0, 1] != .5 or run["trace"][0, 2] != .5 or
                    len(run["offsets"]) != n + 2 or
                    len(run["parentage_offsets"]) != n + 1):
                raise AssertionError("Technical replay invariant failed")
            again = simulate(d, task, steps=n, capture_genomes=False)
            np.testing.assert_array_equal(run["trace"], again["trace"])
            proof.append({"task": list(task), "case_kind": "technical_only",
                          "censuses": n + 1, "initial_I_min": run["trace"][0, 3],
                          "terminal_N": int(run["trace"][-1, 0])})
    return {"status": "PASS_TECHNICAL_SMOKE_ONLY_NOT_SCIENTIFIC_RESULTS",
            "design_sha256": sha(design_path.read_bytes()), "sources": source_manifest(design_path),
            "cases": len(proof), "technical_cases": proof,
            "no_full_200_update_scientific_cases_executed": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--mode", choices=["technical-smoke"], default="technical-smoke")
    args = parser.parse_args()
    if args.out.exists():
        parser.error("Refuse output overwrite or mixed experiment")
    d = load_protocol(args.design)
    result = technical_smoke(d, args.design)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "cases": result["cases"]}))


if __name__ == "__main__":
    main()
