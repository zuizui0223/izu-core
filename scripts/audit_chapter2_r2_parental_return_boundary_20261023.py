"""Source-exact R2 parental-genome versus maternal-payoff sign boundaries.

This is a deterministic fixed-state read-only assay: no population advance,
segregation, mutation, new evolutionary response or retrospective registration.
The no-pollen-discount, delayed-selfing original baseline-384 source is admitted
with its original protocol and original native-kernel source locks.
"""
from __future__ import annotations

from dataclasses import replace
from math import log
import json

import numpy as np

from scripts.chapter2_pollen_baseline_factorial_20261019 import admit, config, visitors
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import PlantState

STATUS = "EXPLORATORY_FIXED_STATE_PARENTAL_RETURN_NOT_EVOLUTIONARY_CONFIRMATION"
CANDIDATE_A = (0.3, 0.5)
EFFECTIVENESS = ("strong_baseline_limitation", "weak_baseline_limitation")
FUTURES = (("control", 0.4), ("decline", 0.04))


def reporter(n: int, a: float) -> PlantState:
    if n != 48 or not (0 < a < 1):
        raise ValueError("fixed source reporter must have 48 plants and interior A")
    alleles = np.full((n, 3, 2), 0.5, dtype=float)
    alleles[:, 2, :] = a
    return PlantState(
        alleles=alleles,
        allele_origin=np.arange(n * 6, dtype=np.int64).reshape(n, 3, 2),
        mutation_flags=np.zeros((n, 3, 2), dtype=bool),
        ids=np.arange(n, dtype=np.int64),
        birth_years=np.zeros(n, dtype=np.int64),
    )


def parental_payoff(ledger, focal: int = 0) -> tuple[float, float, float, float]:
    """Focal genetic success = half maternal outcross + half paternal + viable self.

    Donor rows and recipient columns follow the exact original Model 3 Ledger.
    """
    maternal_cross = float(ledger.outcross[:, focal].sum())
    paternal_cross = float(ledger.outcross[focal, :].sum())
    self_viable = float(ledger.self_viable[focal])
    genetic = 0.5 * maternal_cross + 0.5 * paternal_cross + self_viable
    return genetic, maternal_cross, paternal_cross, self_viable


def mathematical_boundary(a: float, q: float, *, v: float = 0.5,
                          assurance_cost: float = 0.5) -> dict:
    """Local A gradients in the frozen delayed no-discount mating model.

    The derivative of FULL genetic contribution holds paternal pollen export
    and resident mother allocation fixed and varies the FOCAL A only.
    Maternal offspring alone is a different estimand.
    """
    if not (0 < a < 1 and 0 <= q <= 1 and 0 < v <= 1 and assurance_cost > 0):
        raise ValueError("invalid fixed-state source parameters")
    t = v * a * (1 - q)
    scale = q + t
    if scale <= 0:
        raise ArithmeticError("expected parental source return is zero")
    cost = 2 * assurance_cost * a
    maternal = v * (1 - q) / scale - cost
    parental = (v * (1 - q) - cost * (0.5 * q + t)) / scale
    exact_gap = assurance_cost * a * q / scale
    if not np.isclose(parental - maternal, exact_gap, atol=1e-13, rtol=0):
        raise AssertionError("non-paternal maternal/parental difference identity failed")
    b = v * (1 - 2 * assurance_cost * a * a)
    maternal_cutoff = b / (b + 2 * assurance_cost * a) if b > 0 else None
    parental_cutoff = b / (b + assurance_cost * a) if b > 0 else None
    return {
        "maternal_gradient": maternal,
        "parental_genome_gradient": parental,
        "parental_minus_maternal": exact_gap,
        "maternal_sign_q_cutoff": maternal_cutoff,
        "parental_sign_q_cutoff": parental_cutoff,
        "full_parental_return_includes_both_maternal_and_paternal_outcross_halves": True,
    }


def readback() -> dict:
    frozen = admit()
    f, m = frozen["factorial"], frozen["model"]
    if not (
        frozen["status"] == "FROZEN_EXPLORATORY_MECHANISM_PILOT_NOT_INDEPENDENT_CONFIRMATION"
        and f["initial_A_means"] == list(CANDIDATE_A)
        and m["capacity"] == 48
        and m["assurance_mode"] == "evolving"
        and m["assurance_timing"] == "delayed"
        and m["pollen_discount"] == 0
        and m["assurance_cost"] == 0.5
        and m["inbreeding_depression"] == 0.5
        and m["mutation_rate"] == 0
        and m["seed_immigration"] == 0
        and m["visitor_immigration"] == 0
        and m["pollen_scale"] == 0.15
    ):
        raise AssertionError("unexpected old source model settings")
    rows = []
    v = 1 - m["inbreeding_depression"]
    for a in CANDIDATE_A:
        state = reporter(48, a)
        for level in EFFECTIVENESS:
            vv = visitors(frozen, level)
            for future, activity in FUTURES:
                if f["pollinator_activity"]["control_future" if future == "control" else "decline_future"] != activity:
                    raise AssertionError("activity intervention not original")
                cfg = config(frozen, level, activity)
                base = reproduce(state, vv, cfg)
                o = float(base.ovules[0])
                g0, F, P, S = parental_payoff(base)
                q = F / o
                if not (o > 0 and g0 > 0 and 0 <= q <= 1):
                    raise AssertionError("invalid source maternal ovules or outcross")
                if not np.isclose(F, P, atol=1e-12, rtol=0):
                    raise AssertionError("symmetric source reporter must match F and P")
                pred = mathematical_boundary(a, q, v=v, assurance_cost=m["assurance_cost"])
                h = 1e-6
                actual_genetic = []
                actual_maternal = []
                actual_paternal = []
                for new_a in (a-h, a+h):
                    changed = state.alleles.copy()
                    changed[0, 2, :] = new_a  # change one focal plant ONLY
                    new = reproduce(replace(state, alleles=changed), vv, cfg)
                    g, Fmut, Pmut, Smut = parental_payoff(new)
                    actual_genetic.append(log(g))
                    actual_maternal.append(log(Fmut + Smut))
                    actual_paternal.append(Pmut)
                    if not np.isclose(Fmut / float(new.ovules[0]), q, atol=1e-12, rtol=0):
                        raise AssertionError("pollen fraction changed with focal A despite no pollen discount")
                genetic_fd = (actual_genetic[1]-actual_genetic[0])/(2*h)
                maternal_fd = (actual_maternal[1]-actual_maternal[0])/(2*h)
                if max(abs(x-P) for x in actual_paternal) > 1e-12:
                    raise AssertionError("paternal export must be A-invariant with zero pollen discount")
                if not np.isclose(genetic_fd, pred["parental_genome_gradient"], atol=2e-7, rtol=0):
                    raise AssertionError("native focal genetic gradient differs from source algebra")
                if not np.isclose(maternal_fd, pred["maternal_gradient"], atol=2e-7, rtol=0):
                    raise AssertionError("native focal maternal gradient differs from source algebra")
                if pred["maternal_sign_q_cutoff"] is None or pred["parental_sign_q_cutoff"] is None:
                    raise AssertionError("interior q thresholds expected in frozen grid")
                if not pred["parental_sign_q_cutoff"] > pred["maternal_sign_q_cutoff"]:
                    raise AssertionError("selfing transmission value did not widen positive-return q region")
                row = {
                    "A_reporter": a,
                    "baseline": level,
                    "future": future,
                    "source_q": q,
                    "expected_parental_genome_return": g0,
                    "native_fd_parental_gradient": genetic_fd,
                    "native_fd_maternal_gradient": maternal_fd,
                    "native_focal_paternal_outcross_invariant": True,
                    "maternal_gradient_positive": pred["maternal_gradient"] > 0,
                    "parental_gradient_positive": pred["parental_genome_gradient"] > 0,
                }
                row.update(pred)
                rows.append(row)
    contrast = next(x for x in rows if x["A_reporter"] == 0.5 and
                    x["baseline"] == "weak_baseline_limitation" and x["future"] == "decline")
    if not (contrast["maternal_gradient"] < 0 < contrast["parental_genome_gradient"]):
        raise AssertionError("the source-distinguishing maternal/parental sign contrast failed")
    return {
        "status": STATUS,
        "original_frozen_source_protocol_sha256": "87af92484af9988181b4f3bed6760d39325de70cca8c0b4e1cec19c47b8c9849",
        "rows": rows,
        "key_counterexample": {
            "A_reporter": contrast["A_reporter"],
            "baseline": contrast["baseline"],
            "future": contrast["future"],
            "q": contrast["source_q"],
            "maternal_gradient": contrast["maternal_gradient"],
            "parental_genome_gradient": contrast["parental_genome_gradient"],
            "description": "maternal negative yet one-year inherited parental-genome return positive",
        },
        "scope": [
            "Static one-generation source parental-genome accounting, not a true evolutionary invasion probability",
            "Full source genotype fixed except one focal A and no A pollen discount",
            "No A locus evolution, no finite-population sampling or genotype fixation is simulated",
            "No causal mediation of original R2 384 paths and no independent natural-island verification",
        ],
        "new_biological_population_updates": 0,
        "new_preregistered_tests": 0,
    }


if __name__ == "__main__":
    print(json.dumps(readback(), indent=2, ensure_ascii=False))
