"""TECHNICAL-ONLY source-lineage → arrival → establishment → persistence → A/I response.

This is a source-compatible Model 3 engineering fixture, NOT a confirmed
island-assembly experiment, natural-island result, or scientific preregistration.
Lineages occupy separate independent Model 3 plots; their aggregation is a
NONINTERACTING island-flora control, not a competitive multi-species community.

All biological reproduction / parentage / finite inheritance uses the unchanged
scripts.model3_island engine. Post-establishment A/I expression clamps are
synthetic counterfactual interventions; they do not manipulate SC or disable
drift at the underlying locus. There is no immigration or mutation.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from scripts.model3_island.history import reflect_unit
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import STREAM_IDS, stream
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import Config, PlantState, VisitorState

SOURCE_VERSION = "two-origins-technical-20261019-v2"  # stable genotype/arrival RNG namespace
PROTOCOL_VERSION = "two-origins-technical-20261019-v3"
FIELDS = ("alleles", "allele_origin", "mutation_flags", "ids", "birth_years")
POLICIES = ("native", "clamp_A", "clamp_I", "clamp_A_I")
ESTABLISHMENT_MODES = ("native", "neutral_A", "neutral_I", "neutral_A_I", "trait_neutral")
TRAITS = ("A", "I")
CAPACITY = 12
HORIZON = 6
REPEATS = 2


@dataclass(frozen=True)
class SourceLineage:
    lineage_id: int
    a_hint: float
    i_hint: float
    source_seed: int
    arrival_probability: float
    propagules: int = 2

    def __post_init__(self):
        if type(self.lineage_id) is not int or self.lineage_id < 0:
            raise ValueError("lineage ID must be a nonnegative integer")
        if type(self.source_seed) is not int or self.source_seed < 0:
            raise ValueError("source seed must be a nonnegative integer")
        if type(self.propagules) is not int or not 1 <= self.propagules <= 8:
            raise ValueError("technical founding propagule count outside 1..8")
        for x in (self.a_hint, self.i_hint, self.arrival_probability):
            if isinstance(x, bool) or not isinstance(x, (float, int)) or not math.isfinite(x) or not 0 <= x <= 1:
                raise ValueError("source trait hints and arrival probability must be finite 0..1")


@dataclass(frozen=True)
class Island:
    island_id: str
    ovule_budget: float
    visitors: int
    arrival_multiplier: float = 1.

    def __post_init__(self):
        if not isinstance(self.island_id, str) or not self.island_id or "|" in self.island_id:
            raise ValueError("invalid island ID")
        if self.visitors not in (0, 4) or type(self.visitors) is not int:
            raise ValueError("technical visitor choices are 0 or 4")
        if self.ovule_budget not in (4.5, 8.) or type(self.ovule_budget) not in (int, float):
            raise ValueError("technical resource choices are 4.5 or 8")
        if not isinstance(self.arrival_multiplier, (int, float)) or isinstance(self.arrival_multiplier, bool) or not 0 <= self.arrival_multiplier <= 1:
            raise ValueError("invalid arrival multiplier")


def _seed(*items):
    key = (SOURCE_VERSION + "|" + "|".join(map(str, items))).encode("utf8")
    return int.from_bytes(hashlib.sha256(key).digest()[:16], "big")


def _streams(*items):
    master = _seed(*items)
    return {name: stream(master, name, 0) for name in STREAM_IDS}


def source_genotype(lineage: SourceLineage) -> PlantState:
    """One declared finite mainland SOURCE genotype per lineage across technical resets."""
    rng = np.random.default_rng(_seed("source", lineage.source_seed, lineage.lineage_id))
    n = lineage.propagules
    means = np.array([.5, lineage.i_hint, lineage.a_hint], dtype=float)
    alleles = reflect_unit(means[None, :, None] + rng.normal(0., .035, (n, 3, 2)))
    alleles = alleles.astype(float)
    origin = np.arange(n * 6, dtype=np.int64).reshape(n, 3, 2)
    return PlantState(alleles, origin, np.zeros((n, 3, 2), dtype=bool),
                      np.arange(n, dtype=np.int64), np.zeros(n, dtype=np.int64))


def _visitors(island: Island) -> VisitorState:
    n = island.visitors
    return VisitorState(
        np.arange(n, dtype=np.int64),
        np.linspace(.35, .65, n) if n else np.empty(0, dtype=float),
        np.full(n, .2, dtype=float),
        np.ones(n, dtype=float),
    )


def _config(island: Island, *, assurance_mode: str, initial_a: float) -> Config:
    """Native source parameters; no immigration/mutation. Technical horizon only."""
    return Config.from_dict(dict(
        schema_version=1, event_order="reproduce-survive-arrive-recruit-v1",
        time_unit="reproductive_year", capacity=CAPACITY, years=HORIZON,
        survival=0., ovule_budget=float(island.ovule_budget),
        pollen_budget=20., investment_cost=.5, pollen_scale=1.,
        depression=.5, mutation_rate=0., mutation_sd=.025,
        assurance_mode=assurance_mode, fixed_assurance=float(initial_a),
        assurance_timing="delayed", pollen_discount=0., assurance_cost=.5,
        activity=.4, activity_mode="count_scaled", reference_visitor_count=4.,
        background_ratio=1., background_resources=1., island_history="founding",
        initial_visitors=island.visitors, visitor_breadth=.2, visitor_effectiveness=1.,
        source_allele_means=[.5, .5, .5], source_allele_sd=.08,
        seed_arrival=dict(supply=0., distance=1., scale=1., kernel="exponential",
                          establishment=.5, loss_hazard=0.),
        visitor_arrival=dict(supply=0., distance=1., scale=1., kernel="exponential",
                             establishment=.8, loss_hazard=0.),
    ))


def _empty(state: PlantState) -> PlantState:
    return PlantState(**{name: getattr(state, name)[:0].copy() for name in FIELDS})


def _expressed_state(state: PlantState, source_i: float, freeze_i: bool) -> PlantState:
    """Investment-expression clamp ONLY inside the native reproduction ledger.

    Mendelian transmission below always receives the unaltered, inherited state.
    This is not a claim about a mapped causal flower-size locus or SC.
    """
    if not freeze_i:
        return state
    values = state.alleles.copy()
    values[:, 1, :] = source_i
    return replace(state, alleles=values)


def _neutral_establishment_state(state: PlantState) -> PlantState:
    """Stage-1 trait-neutral phenotype only; true alleles transmit unchanged.

    All initial M/I expressed means and expressed A are set to .5 solely for
    reproduction. Mother/father sampling and the offspring genotype remain
    those of the source state. This excludes establishment fitness contrasts
    attributable to Model3 M/I/A traits; it does not equal pure geographic
    arrival randomization or a natural neutral community.
    """
    x = state.alleles.copy()
    x[:, :, :] = .5
    return replace(state, alleles=x)


def source_traits(state: PlantState) -> dict:
    if not len(state.ids):
        raise ValueError("source genotype must not be empty")
    return dict(A=float(state.alleles[:, 2, :].mean()),
                I=float(state.alleles[:, 1, :].mean()))


def attempt(lineage: SourceLineage, island: Island, reset_id: int, *,
            establishment_mode="native", policies=POLICIES) -> list[dict]:
    """Identical candidate, arrival draw and establishment fork in all policies."""
    if type(reset_id) is not int or reset_id < 0:
        raise ValueError("reset ID must be a nonnegative integer")
    if len(set(policies)) != len(policies) or not set(policies) <= set(POLICIES):
        raise ValueError("unknown/duplicate policy")
    if establishment_mode not in ESTABLISHMENT_MODES:
        raise ValueError("unknown establishment intervention")
    initial = source_genotype(lineage)
    src = source_traits(initial)
    chance = lineage.arrival_probability * island.arrival_multiplier
    rng = np.random.default_rng(_seed("arrival", island.island_id, reset_id, lineage.lineage_id))
    arrived = bool(rng.random() < chance)
    observed = _visitors(island)
    freeze_a = establishment_mode in ("neutral_A", "neutral_A_I", "trait_neutral")
    freeze_i = establishment_mode in ("neutral_I", "neutral_A_I", "trait_neutral")
    cfg = _config(island, assurance_mode="fixed" if freeze_a else "evolving",
                  initial_a=.5 if freeze_a else src["A"])
    expressed = (_neutral_establishment_state(initial) if establishment_mode == "trait_neutral"
                 else _expressed_state(initial, .5, freeze_i))
    # Evaluate every candidate even when the arrival lottery fails. Because
    # survival=0, immigration=0, and capacity>0, exactly one native first
    # reproduction update establishes iff Poisson(expected viable recruits)>0.
    # This is a probability identity, not evidence of deterministic colonization.
    first_ledger = reproduce(expressed, observed, cfg)
    expected_recruits = float(first_ledger.outcross.sum() +
                              first_ledger.self_viable.sum())
    if not math.isfinite(expected_recruits) or expected_recruits < 0:
        raise ValueError("invalid nonnegative expected establishment fecundity")
    conditional_establishment = -math.expm1(-expected_recruits)
    first = initial
    established = False
    if arrived:
        first, _ = advance(
            initial, first_ledger, _empty(initial), cfg,
            _streams("establishment", island.island_id, reset_id, lineage.lineage_id),
            year=0, mutation_traits=(False, False, False),
        )
        established = bool(len(first.ids))
    # Policy and neutral/native filter share the same master stream seed.
    # The generators are instantiated separately for each arm; after histories
    # diverge, consumption may differ, so events are NOT synchronized.
    descendant_master = _seed("descendants", island.island_id, reset_id,
                              lineage.lineage_id)
    rows = []
    for policy in policies:
        frozen_a = policy in ("clamp_A", "clamp_A_I")
        frozen_i = policy in ("clamp_I", "clamp_A_I")
        state = first
        if established:
            cfg = _config(island, assurance_mode="fixed" if frozen_a else "evolving",
                          initial_a=src["A"])
            rngs = _streams("descendants", island.island_id, reset_id,
                            lineage.lineage_id)
            for year in range(1, HORIZON):
                parental = _expressed_state(state, src["I"], frozen_i)
                state, _ = advance(
                    state, reproduce(parental, observed, cfg), _empty(state),
                    cfg, rngs, year=year, mutation_traits=(False, False, False),
                )
                if not len(state.ids):
                    break
        alive = bool(established and len(state.ids))
        final_traits = None if not alive else {
            "A": src["A"] if frozen_a else float(state.alleles[:, 2, :].mean()),
            "I": src["I"] if frozen_i else float(state.alleles[:, 1, :].mean()),
        }
        rows.append(dict(
            island_id=island.island_id, reset_id=reset_id,
            lineage_id=lineage.lineage_id, establishment_mode=establishment_mode,
            policy=policy,
            candidate=True, arrived=arrived, established=established, persisted=alive,
            arrival_probability=chance, source_traits=src,
            expected_recruits_if_arrived=expected_recruits,
            establishment_probability_if_arrived=conditional_establishment,
            descendant_rng_master_hex=f"{descendant_master:032x}",
            final_expressed_traits=final_traits,
            terminal_abundance=len(state.ids) if alive else 0,
            technical_fixture_only=True,
        ))
    return rows


def stage_accounting(rows: list[dict], trait: str) -> dict:
    """Exact conditional telescoping of species-weighted means.

    Means are UNDEFINED when a required stage is empty (never impute zero).
    Origin baseline for an established/surviving lineage is its original
    source genotype, including its first native establishment reproduction.
    These terms are not causal mediation or neutral tests.
    """
    if trait not in TRAITS or not rows:
        raise ValueError("one supported trait and nonempty single-policy rows required")
    if len({r["lineage_id"] for r in rows}) != len(rows):
        raise ValueError("one record per source lineage required")
    if len({(r["island_id"], r["reset_id"], r["establishment_mode"], r["policy"])
            for r in rows}) != 1:
        raise ValueError("crossed island, reset, establishment or policy records")
    current = list(rows)
    arrived = [r for r in current if r["arrived"]]
    established = [r for r in arrived if r["established"]]
    retained = [r for r in established if r["persisted"]]
    if any(r["persisted"] and not r["established"] for r in rows):
        raise ValueError("persisted cannot predate establishment")

    def mean(values):
        return float(np.mean(values)) if values else None

    pooled = [
        mean([r["source_traits"][trait] for r in chunk])
        for chunk in (current, arrived, established, retained)
    ]
    final = mean([r["final_expressed_traits"][trait] for r in retained])
    counts = dict(candidate=len(current), arrived=len(arrived),
                  established=len(established), persisted=len(retained))
    if not retained or not established or not arrived:
        return dict(trait=trait, status="EMPTY_STAGE_UNDEFINED_MEAN",
                    counts=counts, means=dict(source=pooled[0], arrived=pooled[1],
                                              established=pooled[2], retained_source=pooled[3],
                                              retained_final=final),
                    contributions=None, total_change=None)
    arrival_component = pooled[1] - pooled[0]
    establishment_component = pooled[2] - pooled[1]
    persistence_component = pooled[3] - pooled[2]
    within_lineage_component = final - pooled[3]
    contributions = dict(arrival=arrival_component,
                         establishment=establishment_component,
                         persistence_filter=persistence_component,
                         within_retained_lineage=within_lineage_component)
    total = final - pooled[0]
    if abs(math.fsum(contributions.values()) - total) > 1e-12:
        raise ValueError("trait means fail exact selection/evolution accounting")
    return dict(trait=trait, status="DESCRIPTIVE_IDENTITY_NOT_CAUSAL",
                counts=counts,
                means=dict(source=pooled[0], arrived=pooled[1],
                           established=pooled[2], retained_source=pooled[3],
                           retained_final=final),
                contributions=contributions, total_change=total)


def score_binary(outcomes, probabilities) -> dict:
    """Strictly held-out predictions may use these proper scores in a future trial."""
    y = np.asarray(outcomes, dtype=float)
    p = np.asarray(probabilities, dtype=float)
    if (y.ndim != 1 or p.shape != y.shape or not len(y)
            or not np.isfinite(y).all() or not np.isfinite(p).all()
            or not np.isin(y, [0., 1.]).all() or (p < 0).any() or (p > 1).any()):
        raise ValueError("binary scores require aligned valid outcomes and probabilities")
    q = np.clip(p, 1e-12, 1. - 1e-12)
    return {"brier": float(np.mean((p - y) ** 2)),
            "log_loss": float(np.mean(-y * np.log(q) - (1. - y) * np.log1p(-q))),
            "n": int(len(y)), "calibration_mean": float(p.mean()),
            "event_rate": float(y.mean())}


def technical_fixture() -> dict:
    """Only six source genotypes, two islands, two stochastic archipelago resets."""
    lineages = [
        SourceLineage(k, a, i, source_seed=73000 + k, arrival_probability=.80)
        for k, (a, i) in enumerate((a, i) for a in (.25, .50, .75) for i in (.35, .65))
    ]
    islands = (Island("no_visitors_harsh", 4.5, 0),
               Island("visitors_milder", 8., 4))
    records = []
    for island in islands:
        for reset in range(REPEATS):
            for lineage in lineages:
                for establishment_mode in ESTABLISHMENT_MODES:
                    records.extend(attempt(lineage, island, reset,
                                           establishment_mode=establishment_mode))
    frames = []
    for island in islands:
        for reset in range(REPEATS):
            for establishment_mode in ESTABLISHMENT_MODES:
                for policy in POLICIES:
                    sub = [r for r in records if r["island_id"] == island.island_id
                           and r["reset_id"] == reset
                           and r["establishment_mode"] == establishment_mode
                           and r["policy"] == policy]
                    frames.append(dict(island=island.island_id, reset_id=reset,
                                       establishment_mode=establishment_mode,
                                       policy=policy,
                                       A=stage_accounting(sub, "A"),
                                       I=stage_accounting(sub, "I")))
    return dict(
        status="TECHNICAL_SMOKE_ONLY_NOT_SCIENTIFIC_EVIDENCE",
        protocol=PROTOCOL_VERSION, source_rng_namespace=SOURCE_VERSION,
        engine="scripts.model3_island reproduction+population (unaltered)",
        lineages=len(lineages), islands=len(islands), archipelago_resets=REPEATS,
        policies=list(POLICIES), establishment_modes=list(ESTABLISHMENT_MODES),
        horizon=HORIZON, mutation=False, immigration=False,
        competition=False, dispersal_species_independent=True,
        definition="one native reproductive update defines establishment; continued occupancy defines persistence",
        source_genotypes_are_not_measured_mainland_taxa=True,
        registered_scientific_endpoints=False,
        publication_claim_allowed=False,
        records=records, exact_stage_accounting=frames,
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--technical-smoke", action="store_true",
                    help="required to run the bounded, nonconfirmatory fixture")
    ap.add_argument("--output", type=Path, default=None)
    args = ap.parse_args()
    if not args.technical_smoke:
        ap.error("production campaign disabled; only --technical-smoke is permitted")
    result = technical_fixture()
    body = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(body, encoding="utf8")
    else:
        print(body, end="")


if __name__ == "__main__":
    main()
