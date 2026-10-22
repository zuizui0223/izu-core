"""Read-only, post-outcome crossed-axis audit of living high-I genetic options.

Consumes the *original* 2026-10-19 Actions summary artifact and all 32
source-sealed endpoint records. No Model 3 import, evolutionary update, new
random biological sample, new registered test or external DOI claim.

Usage:
  python -m scripts.audit_chapter2_crossed_access_sign_20261023 \
    --artifact ORIGINAL_q3-confirm160-summary.zip \
    --out NEW_CROSSED_ACCESS.json
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import zipfile

import numpy as np
from scipy.stats import t as student_t

ROOT = Path(__file__).resolve().parents[1]
COMPACT = ROOT / "docs/audits/CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json"
SUMMARY_SHA256 = "6a1ede3caa62a13f1c3be8b38c66d5d6985000f2f0a4369a6f1f89c7c8bb91c6"
ORIGINAL_ACTIONS_ARTIFACT_SHA256 = "a83e5aae7c067b27f2b0c6320fcf4157764e70efd7dfc5bdd251e94209e82075"
RUN_ID = 39193074847
ARTIFACT_ID = 12161199381
F = V = 160
SHARDS = 32
EPSILON_INDEX = 0
POLICIES = ("fixed", "evolving")
BUDGETS = ("B8", "B4p5")
STATUS = "POST_OUTCOME_CROSSED_DESCRIPTIVE_NOT_REGISTERED"


def fail(msg: str) -> None:
    raise ValueError("crossed high-I source audit: " + msg)


def require(ok: bool, msg: str) -> None:
    if not ok:
        fail(msg)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode()


def strict_json(payload: bytes):
    def pairs(items):
        d = {}
        for key, val in items:
            require(key not in d, "duplicate JSON key " + key)
            d[key] = val
        return d
    return json.loads(payload, object_pairs_hook=pairs,
                      parse_constant=lambda v: fail("non-finite literal " + v))


def frozen_report(source: dict, compact: dict) -> bool:
    require(source["status"] == compact["status"]
            == "COMPLETE_MODEL_CONDITIONAL_CONFIRMATION", "status")
    require(source["independent_axes"] == compact["independent_axes"] == [F, V]
            and source["crossings"] == compact["crossings"] == F * V,
            "crossed source size")
    require(source["actual_restoration_tested"] is False
            and compact["actual_restoration_tested"] is False, "not a return test")
    require(source["shard_seals"] == compact["shard_seals"],
            "original seal registry")
    require(compact["retained_source_summary_sha256"] == SUMMARY_SHA256,
            "retained original summary pointer")
    require(source["arms"] == compact["arms"], "source arm totals")
    require(source["primary"] == compact["primary"], "registered primary result")
    require(source["files"] == compact["files"] == 153600, "native task counts")
    require(source["saved_states"] == compact["saved_states"] == 6553600,
            "native saved-state counts")
    return True


def read_original(archive: Path, compact_path: Path = COMPACT):
    """Return crossed F×V×budget×policy current alive-and-accessible indicators.

    Unlike the genetic-first CIF this endpoint is current state at census80.
    The original source SHA and every seal's canonical source digest are
    checked. The full genotype archive had already been separately audited
    in its admission report; no full-genome replay is claimed here.
    """
    raw_zip = Path(archive).read_bytes()
    require(sha256(raw_zip) == ORIGINAL_ACTIONS_ARTIFACT_SHA256,
            "original Actions artifact ZIP transport checksum")
    compact = strict_json(Path(compact_path).read_bytes())
    with zipfile.ZipFile(archive) as z:
        expected = {"SUMMARY160.json"}
        expected |= {f"seals/seal-{i}.json" for i in range(SHARDS)}
        expected |= {f"seals/hashes-{i}.txt" for i in range(SHARDS)}
        require(set(z.namelist()) == expected and len(z.namelist()) == len(expected),
                "original summary archive member inventory")
        original = z.read("SUMMARY160.json")
        require(sha256(original) == SUMMARY_SHA256, "original SUMMARY160 sha")
        source = strict_json(original)
        frozen_report(source, compact)
        require(len(source["genetic_loss_inputs"]) == F
                and len(source["occupancy_inputs"]) == F, "source input matrix")

        grid = np.full((F, V, 2, 2), -1, dtype=np.int8)
        g = np.full((F, V, 2), -1, dtype=np.int8)
        occupancy = np.full((F, V, 2, 2), -1, dtype=np.int8)
        counts = {f"{p}_{b}": dict(alive=0, alive_accessible=0,
                genetic_first=0, extinction_first=0)
                  for p in POLICIES for b in BUDGETS}
        seen = set()
        seal_sha_list = []
        for shard in range(SHARDS):
            seal = strict_json(z.read(f"seals/seal-{shard}.json"))
            require(seal["contract"]["shard"] == shard
                    and seal["contract"]["shards"] == SHARDS
                    and seal["complete"] is True
                    and len(seal["records"]) == F * V // SHARDS,
                    "original sealed shard assignment")
            require(sha256(canonical({k: v for k, v in seal.items()
                    if k != "seal_sha256"})) == seal["seal_sha256"],
                    "sealed record canonical source checksum")
            seal_sha_list.append(seal["seal_sha256"])
            require(sha256(canonical({k: v for k, v in seal["contract"].items()
                    if k != "contract_sha256"}))
                    == seal["contract"]["contract_sha256"],
                    "frozen source contract checksum")
            plan = seal["contract"]["plan"]
            require(plan["founders"] == list(range(501001, 501161))
                    and plan["visitors"] == list(range(502001, 502161))
                    and plan["policies"] == list(POLICIES)
                    and plan["budgets"] == [8., 4.5]
                    and plan["fork"] == 35 and plan["end"] == 80,
                    "frozen founder visitor policy horizon")
            for record in seal["records"]:
                f = record["founder"] - 501001
                v = record["visitor"] - 502001
                require(0 <= f < F and 0 <= v < V and (f, v) not in seen
                        and (f * V + v) % SHARDS == shard,
                        "source cell uniqueness and frozen shard assignment")
                seen.add((f, v))
                arms = {(item["policy"], item["stage"]): item
                        for item in record["arms"]}
                require(len(arms) == 4
                        and set(arms) == {(p, b) for p in POLICIES
                                         for b in BUDGETS},
                        "paired source policy-by-budget arms")
                for bi, budget in enumerate(BUDGETS):
                    for pi, policy in enumerate(POLICIES):
                        x = arms[policy, budget]
                        require(type(x["alive"]) is bool
                                and all(len(x[name]) == 5 for name in
                                        ("final_access", "genetic_first",
                                         "extinction_first")),
                                "source arm indicators")
                        available = x["final_access"][EPSILON_INDEX]
                        genetic = x["genetic_first"][EPSILON_INDEX]
                        extinct = x["extinction_first"][EPSILON_INDEX]
                        require(all(type(y) is bool for y in
                                    (available, genetic, extinct)),
                                "source status boolean")
                        require(int(available) + int(genetic) + int(extinct) == 1
                                and (not available or x["alive"]),
                                "competing first events and current state")
                        require(all(x["final_access"][j] <= x["final_access"][j + 1]
                                    for j in range(4)),
                                "declared epsilon sensitivity monotonicity")
                        require(budget != "B8" or x["alive"], "B8 survival premise")
                        grid[f, v, bi, pi] = int(available)
                        # SOURCE SUMMARY160 occupancy axes: founder,visitor,policy,budget.
                        # Derived endpoint grid intentionally uses founder,visitor,budget,policy.
                        occupancy[f, v, pi, bi] = int(x["alive"])
                        if budget == "B8":
                            g[f, v, pi] = int(genetic)
                        for field, observed in (
                                ("alive", x["alive"]),
                                ("alive_accessible", available),
                                ("genetic_first", genetic),
                                ("extinction_first", extinct)):
                            counts[f"{policy}_{budget}"][field] += int(observed)
        require(len(seen) == F * V and all((grid >= 0).flat)
                and all((g >= 0).flat) and all((occupancy >= 0).flat),
                "complete grid coverage")
        require(sorted(seal_sha_list) == sorted(source["shard_seals"]),
                "seal registry complete")
        require(g.tolist() == source["genetic_loss_inputs"]
                and occupancy.tolist() == source["occupancy_inputs"],
                "original crossed matrices (not just marginal counts)")
        require(counts == source["arms"], "all four complete arm totals")
    return grid, dict(
        original_summary_sha256=SUMMARY_SHA256,
        original_actions_artifact_sha256=ORIGINAL_ACTIONS_ARTIFACT_SHA256,
        source_run=RUN_ID, source_artifact_id=ARTIFACT_ID,
        sealed_source_shards=SHARDS, original_cell_count=F * V,
        complete_arm_totals=counts)


def ph_summary(grid: np.ndarray) -> dict:
    """Same conditional pigeonhole variance as the original registered code.

    Applying it to this newly *selected* joint endpoint gives a descriptive
    sensitivity interval only; it is not a preregistered confirmatory CI.
    """
    x = np.asarray(grid, dtype=np.float64)
    require(x.ndim == 2 and x.shape == (F, V)
            and np.isfinite(x).all(), "complete finite F×V contrast")
    mean = float(x.mean())
    row = x.mean(axis=1)
    col = x.mean(axis=0)
    rr = row - mean
    cc = col - mean
    residual = x - mean - rr[:, None] - cc[None, :]
    var = float(np.sum(rr ** 2) / F ** 2
                + np.sum(cc ** 2) / V ** 2
                + np.sum(residual ** 2) / (F * V) ** 2)
    critical = float(student_t.ppf(.9875, min(F, V)-1))
    signs = lambda values: {name: int((np.sign(values) == target).sum())
                            for name, target in (("positive", 1), ("zero", 0),
                                                 ("negative", -1))}
    vals, nums = np.unique(x.astype(int), return_counts=True)
    return dict(
        estimate_pp=mean * 100, pigeonhole_conditional_variance=var,
        pigeonhole_se_pp=100 * np.sqrt(var),
        nominal_97p5_t_interval_pp=[float(100 * (mean - critical*np.sqrt(var))),
                                   float(100 * (mean + critical*np.sqrt(var)))],
        founder_marginal_signs=signs(row),
        visitor_marginal_signs=signs(col),
        founder_marginal_range_pp=[float(row.min()*100),float(row.max()*100)],
        visitor_marginal_range_pp=[float(col.min()*100),float(col.max()*100)],
        paired_cell_effect_counts={str(int(k)): int(n) for k, n in zip(vals, nums)})


def crossed_bootstrap(diffs: dict, draws: int = 10_000,
                      seed: int = 20261023) -> dict:
    """Resample 160 founder and 160 visitor IDs independently; same weights
    for both budgets/policies, no new biological trajectories or p-values."""
    require(type(draws) is int and 100 <= draws <= 50_000
            and type(seed) is int and 0 <= seed < 2**32,
            "bootstrap sensitivity configuration")
    rng = np.random.default_rng(seed)
    w_f = rng.multinomial(F, [1/F]*F, size=draws).astype(float)
    w_v = rng.multinomial(V, [1/V]*V, size=draws).astype(float)
    out = {}
    for name, grid in diffs.items():
        values = (np.einsum("bi,ij,bj->b", w_f, grid.astype(float), w_v,
                           optimize=True) / (F*V))*100
        out[name] = dict(
            seed=seed, crossed_resamples=draws,
            percentile95_pp=np.quantile(values, [.025, .975]).tolist(),
            percentile97p5_pp=np.quantile(values, [.0125, .9875]).tolist(),
            bootstrap_sd_pp=float(values.std(ddof=1)),
            interval_is_exploratory_post_outcome=True)
    return out


def derive(grid: np.ndarray, provenance: dict, *, draws=10000, seed=20261023):
    require(grid.shape == (F, V, 2, 2)
            and np.isin(grid, [0, 1]).all(), "full source binary state grid")
    b8 = grid[:, :, 0, 1].astype(int) - grid[:, :, 0, 0].astype(int)
    b45 = grid[:, :, 1, 1].astype(int) - grid[:, :, 1, 0].astype(int)
    interaction = b45 - b8
    diffs = {"B8": b8, "B4p5": b45, "interaction": interaction}
    results = {k: ph_summary(v) for k, v in diffs.items()}
    counts = {f"{i}_{j}": int(n) for (i, j), n in
              sorted(Counter(zip(b8.flat, b45.flat)).items())}
    require(sum(counts.values()) == F*V and counts["-1_1"] == 995
            and counts["1_-1"] == 6,
            "paired source budget-sign reversal counts")
    require(abs(results["B8"]["estimate_pp"] + 8.328125) < 1e-12
            and abs(results["B4p5"]["estimate_pp"] - 35.56640625) < 1e-12
            and abs(results["interaction"]["estimate_pp"] - 43.89453125) < 1e-12,
            "independently derived composite effect totals")
    return dict(status=STATUS, original_provenance=provenance,
                endpoint="P(alive AND founder-relative high-I allele support at census80)",
                paired_effect="(evolving minus fixed) within each original founder/visitor cell",
                independent_sampling_axes=["160 synthetic founder sources",
                                            "160 synthetic visitor-history sources"],
                n_crossed_cells_not_independent_islands=F*V,
                source_bound_post_outcome=True, new_biological_simulations=0,
                new_preregistered_endpoints=0, independent_biological_reimplementation=False,
                new_confirmatory_test=False, no_causal_mediation_identified=True,
                source_marginal_signs_not_independent_sign_tests=True,
                pointwise=results, paired_budget_effects=counts,
                crossed_bootstrap=crossed_bootstrap(diffs, draws, seed),
                limitations=[
                    "Same synthetic model and source cohort; resource conditions B8 and B4.5 only.",
                    "One stochastic realization per crossed founder/visitor/policy/budget cell.",
                    "Post-outcome composite; intervals are conditional sensitivity conventions, not confirmatory coverage guarantees.",
                    "Positive net accessible-and-alive effect under B4.5 largely reflects reduced extinction.",
                    "Neither first-event CIF difference nor survivor access measures a direct genetic mediator.",
                    "Allelic support is necessary but not sufficient for actual ancestral recovery or new-environment adaptation."])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--artifact", type=Path, required=True,
                   help="Original Actions 12161199381 q3-confirm160-summary ZIP")
    p.add_argument("--compact", type=Path, default=COMPACT)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    grid, provenance = read_original(args.artifact, args.compact)
    result = derive(grid, provenance)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf8") as file:
        json.dump(result, file, sort_keys=True, indent=2,
                  ensure_ascii=False, allow_nan=False)
        file.write("\n")
    print(json.dumps({"status": result["status"],
                      "seals": provenance["sealed_source_shards"],
                      "n": result["n_crossed_cells_not_independent_islands"],
                      "new_simulations": 0}))


if __name__ == "__main__":
    main()
