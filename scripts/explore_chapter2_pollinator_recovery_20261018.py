"""Exploratory Q3 visitor-return micro-pilot; imports unchanged Model3 finite operators.

NOT confirmatory, NOT a new dioecy model. The 2026-10-18 protocol is frozen
independently of exploratory results, and no historical Chapter2 result is edited.
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.model3_island.history import reflect_unit
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import Config, PlantState, VisitorState

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs/protocols/CHAPTER2_ISLAND_BRANCH_RECOVERY_PILOT_20261018.md"
DESIGN = ROOT / "data/design/model3_island_v2.json"
MODEL_SOURCES = (
    "scripts/model3_island/types.py",
    "scripts/model3_island/reproduction.py",
    "scripts/model3_island/population.py",
    "scripts/model3_island/history.py",
    "scripts/model3_island/randomness.py",
)
PILOT_ID = "chapter2_q3_pollinator_return_exploratory_20261018_v1"
FOUNDER_IDS = (181001, 181002)
VISITOR_IDS = (182001, 182002)
CHECKPOINTS = (10, 30, 45)
EXTIRPATION = 35
HISTORICAL_HORIZON = 45
FUTURE_HORIZON = 25
FUTURE_REPLICATES = 2
SUSTAINED = 5
FUTURE_ENVIRONMENTS = ("functional_pollinators_restored", "continued_pollinator_loss")
POLICIES = ("fixed", "evolving")


def seeded(*tokens: int) -> int:
    return int(np.random.SeedSequence([20261018, *tokens]).generate_state(1)[0])


def empty_plants(birth: int) -> PlantState:
    return PlantState(
        np.empty((0, 3, 2), dtype=float),
        np.empty((0, 3, 2), dtype=np.int64),
        np.empty((0, 3, 2), dtype=bool),
        np.empty((0,), dtype=np.int64),
        np.empty((0,), dtype=np.int64),
    )


def empty_visitors() -> VisitorState:
    return VisitorState(
        np.empty(0, dtype=np.int64), np.empty(0, dtype=float),
        np.empty(0, dtype=float), np.empty(0, dtype=float),
    )


def make_founders(seed: int) -> PlantState:
    rng = stream(seed, "founders", 0)
    count = 48
    a = reflect_unit(np.array([.5, .5, .5])[None, :, None]
                     + rng.normal(0, .08, (count, 3, 2)))
    # Three original standing I-allele values. A is heritable but starts variable.
    a[:, 1, :] = rng.choice(np.array([.375, .5, .625]), size=(count, 2))
    a[:, 2, :] = rng.choice(np.array([.25, .5, .75]), size=(count, 2))
    return PlantState(
        a, np.arange(count * 6, dtype=np.int64).reshape(count, 3, 2),
        np.zeros((count, 3, 2), dtype=bool),
        np.arange(count, dtype=np.int64), np.zeros(count, dtype=np.int64),
    )


def make_visitors(seed: int) -> tuple[VisitorState, VisitorState]:
    rng = stream(seed, "visitor_initial", 0)
    n = 6
    ids = np.arange(n, dtype=np.int64) + (seed + 1) * 100
    optima = rng.uniform(.3, .7, n)
    full = VisitorState(ids, optima, np.full(n, .2), np.ones(n))
    sparse = VisitorState(ids[:1], optima[:1], np.full(1, .2), np.ones(1))
    return full, sparse


def configuration(policy: str) -> Config:
    if policy not in POLICIES:
        raise ValueError("unknown historical assurance policy")
    base = json.loads(DESIGN.read_text(encoding="utf-8"))["base_config"]
    base.update(
        years=HISTORICAL_HORIZON, assurance_mode=policy, fixed_assurance=.5,
        assurance_timing="delayed", assurance_cost=.5,
        mutation_rate=0., survival=0., activity=.4,
        activity_mode="count_scaled",
    )
    base["seed_arrival"]["supply"] = 0.
    base["visitor_arrival"]["supply"] = 0.
    return Config.from_dict(base)


def streams(seed: int) -> dict:
    return {component: stream(seed, component, 0) for component in STREAM_IDS}


def investment_mean(state: PlantState) -> float | None:
    return float(state.alleles[:, 1, :].mean()) if len(state.ids) else None


def support_bound(state: PlantState, target: float) -> bool | None:
    """Only sufficient impossibility test when I mutation/seed immigration are zero."""
    return bool(state.alleles[:, 1, :].max() < target - 1e-12) if len(state.ids) else None


def step(state: PlantState, visitors: VisitorState, config: Config,
         rng: dict, *, year: int) -> PlantState:
    ledger = reproduce(state, visitors, config)
    if ledger.delivered.sum() > ledger.exported.sum() + 1e-8:
        raise AssertionError("pollen conservation failed")
    prior_max = float(state.alleles[:, 1, :].max()) if len(state.ids) else None
    child, _ = advance(
        state, ledger, empty_plants(year + 1), config, rng, year=year,
        mutation_traits=(False, False, False),
    )
    if prior_max is not None and len(child.ids):
        if child.alleles[:, 1, :].max() > prior_max + 1e-12:
            raise AssertionError("closed I-allele support increased")
    if prior_max is None and len(child.ids):
        raise AssertionError("rescue from extinction without immigration")
    return child


def historical_snapshots(founders: PlantState, full: VisitorState,
                         sparse: VisitorState, policy: str,
                         historical_seed: int) -> dict[int, PlantState]:
    cfg = configuration(policy)
    rng = streams(historical_seed)
    state = founders
    result = {}
    vacant = empty_visitors()
    for year in range(HISTORICAL_HORIZON):
        if year in CHECKPOINTS:
            result[year] = state
        visitor = full if year < 5 else sparse if year < EXTIRPATION else vacant
        state = step(state, visitor, cfg, rng, year=year)
    result[HISTORICAL_HORIZON] = state
    if set(result) != set(CHECKPOINTS):
        raise AssertionError("missing prespecified checkpoint")
    return result


def investment_selection_probe(state: PlantState, visitors: VisitorState,
                               config: Config) -> float | None:
    """One-plant numerical marginal total allele-copy return; NOT a fitted gradient."""
    if len(state.ids) < 2:
        return None
    usable = np.flatnonzero(np.all(state.alleles[:, 1, :] <= .97, axis=1))
    if not len(usable):
        return None
    idx = int(usable[len(usable) // 2])
    baseline = reproduce(state, visitors, config)
    a = state.alleles.copy()
    a[idx, 1, :] += .02
    perturbed = reproduce(replace(state, alleles=a), visitors, config)
    def score(ledger):
        # Per focal gene-copy return: maternal + paternal, selfing counts twice.
        return float((ledger.maternal[idx] + ledger.paternal[idx]) / 2)
    return (score(perturbed) - score(baseline)) / .02


def future(state: PlantState, visitors: VisitorState, config: Config,
           seed: int, checkpoint: int, target: float) -> dict:
    rng = streams(seed)
    streak = 0
    ever_sustained = False
    current = state
    for k in range(FUTURE_HORIZON):
        current = step(current, visitors, config, rng, year=checkpoint + k)
        mean_i = investment_mean(current)
        streak = (streak + 1) if mean_i is not None and mean_i >= target - 1e-12 else 0
        ever_sustained |= streak >= SUSTAINED
    return {
        "occupied_final": bool(len(current.ids)),
        "high_I_sustained_and_occupied_final": bool(len(current.ids) and ever_sustained),
        "final_mean_I": investment_mean(current),
        "final_census": int(len(current.ids)),
    }


def source_identity() -> dict:
    sources = (str(PROTOCOL.relative_to(ROOT)),
               str(DESIGN.relative_to(ROOT)),
               str(Path(__file__).relative_to(ROOT))) + MODEL_SOURCES
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in sources}


def execute_micro_pilot(*, founder_ids=FOUNDER_IDS, visitor_ids=VISITOR_IDS,
                        checkpoints=CHECKPOINTS, future_replicates=FUTURE_REPLICATES) -> dict:
    if not checkpoints or any(t not in CHECKPOINTS for t in checkpoints):
        raise ValueError("only prespecified checkpoints may be used")
    if future_replicates < 1 or future_replicates > FUTURE_REPLICATES:
        raise ValueError("only predeclared pilot replicate budget")
    rows = []
    for f_index, founder_seed in enumerate(founder_ids):
        founder = make_founders(founder_seed)
        target = investment_mean(founder)
        for v_index, visitor_seed in enumerate(visitor_ids):
            full, sparse = make_visitors(visitor_seed)
            # Same historical demographic stream namespace for the two policies.
            historical_seed = seeded(1, f_index, v_index)
            for p_index, policy in enumerate(POLICIES):
                snapshots = historical_snapshots(founder, full, sparse, policy,
                                                 historical_seed)
                cfg = configuration(policy)
                for checkpoint in checkpoints:
                    saved = snapshots[checkpoint]
                    current_i = investment_mean(saved)
                    bound = support_bound(saved, target)
                    gradient = investment_selection_probe(saved, full, cfg)
                    for future_index, environment in enumerate(FUTURE_ENVIRONMENTS):
                        vreturn = full if future_index == 0 else empty_visitors()
                        for replicate in range(future_replicates):
                            # Future streams are matched across policy labels.
                            future_seed = seeded(2, f_index, v_index, checkpoint,
                                                 future_index, replicate)
                            out = future(saved, vreturn, cfg, future_seed,
                                         checkpoint, target)
                            rows.append({
                                "founder_index": f_index, "visitor_index": v_index,
                                "policy": policy, "checkpoint": checkpoint,
                                "future_environment": environment,
                                "future_replicate": replicate,
                                "historical_occupied": bool(len(saved.ids)),
                                "historical_population": int(len(saved.ids)),
                                "target_founder_mean_I": target,
                                "checkpoint_mean_I": current_i,
                                "declined_by_0p05_at_checkpoint": (
                                    current_i is not None and current_i <= target - .05),
                                "high_I_support_structurally_excluded": bound,
                                "positive_investment_probe_after_restore": (
                                    None if gradient is None else gradient > 0),
                                "selection_probe_numeric_slope": gradient,
                                **out,
                            })
    expected = len(founder_ids)*len(visitor_ids)*len(POLICIES)*len(checkpoints)*len(FUTURE_ENVIRONMENTS)*future_replicates
    if len(rows) != expected:
        raise AssertionError("pilot case inventory incomplete")
    by_arm = []
    for checkpoint in checkpoints:
        for policy in POLICIES:
            for environment in FUTURE_ENVIRONMENTS:
                sub = [r for r in rows if r["checkpoint"] == checkpoint
                       and r["policy"] == policy
                       and r["future_environment"] == environment]
                by_arm.append({
                    "checkpoint": checkpoint, "policy": policy, "environment": environment,
                    "conditional_stream_paths": len(sub),
                    "independent_founder_visitor_blocks": len(founder_ids) * len(visitor_ids),
                    "survived_final": sum(r["occupied_final"] for r in sub),
                    "high_I_target_successes_unconditional": sum(
                        r["high_I_sustained_and_occupied_final"] for r in sub),
                    "historic_extinctions_counted_as_failures": sum(
                        not r["historical_occupied"] for r in sub),
                    "high_I_support_closures_in_occupied_snapshots": sum(
                        r["high_I_support_structurally_excluded"] is True for r in sub) // (len(FUTURE_ENVIRONMENTS) if False else future_replicates),
                })
    return {
        "status": "EXPLORATORY_PILOT_ONLY_NO_CONFIRMATORY_CLAIM",
        "pilot_id": PILOT_ID, "new_biological_histories": len(founder_ids)*len(visitor_ids)*len(POLICIES),
        "future_trajectories": len(rows),
        "scientific_unit": "independent founder by visitor history; future streams nested",
        "independent_crossed_blocks": len(founder_ids)*len(visitor_ids),
        "extirpation_time_TE": EXTIRPATION,
        "historical_horizon": HISTORICAL_HORIZON,
        "restoration_checkpoints": list(checkpoints),
        "future_horizon": FUTURE_HORIZON, "sustained_censuses": SUSTAINED,
        "source_sha256": source_identity(),
        "by_arm": by_arm, "paths": rows,
        "not_estimated": ["T_R", "ratchet_vs_lifeboat", "causal_genetic_mediation",
                          "post_extirpation_in_nature", "dioecy_origin",
                          "population_statistical_power"],
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--exploratory-pilot", action="store_true")
    args = p.parse_args()
    if not args.exploratory_pilot:
        p.error("explicit --exploratory-pilot acknowledgment is required")
    if args.out.exists():
        p.error("no overwrite: choose a new output path")
    result = execute_micro_pilot()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True, allow_nan=False)
        f.write("\n")
    print(json.dumps({
        "status": result["status"], "paths": result["future_trajectories"],
        "crossed_blocks": result["independent_crossed_blocks"], "by_arm": result["by_arm"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
