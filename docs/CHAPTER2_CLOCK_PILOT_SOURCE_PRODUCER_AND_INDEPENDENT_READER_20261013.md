# Chapter 2 Q1→Q2: immutable original Model 3 pilot producer/reader pre-execution contract

**2026-10-13. Source/test implementation, not the new 1,536 biological histories.** This note belongs to draft PR #498 stacked on the reviewed original-operator technical PR #496. No pre-existing Q1/Q2/Q3/Q4 result, threshold, model implementation, or manuscript assertion is changed.

## Input and exact source

The 1,536 case IDs and the 128 paired founder×seed master random streams are frozen in the [input manifest](../data/design/chapter2_clock_factorial_pilot_registered_inputs_20261013.json) and admitted against three original preserved GitHub Actions provider archives with SHA256 checks. The original source commit is `328548612e93469fcc8663f24548530a57399b9a`, and **all five Model 3 source files** must match their historical Git blob IDs. The original source typed t0 fixture is Git blob `4b529cce12bc44e06d43a22b10c325a52bbd967b`. The input registry is Git blob `0721517f7bf69eee1c2daf040f4781873ba3c3ea`. **Full biological runs must use NumPy2.2.6**, the original runtime, or fail closed. Only original canonical `reproduce`, `advance`, `inherit`, `PlantState`, `Config`, `VisitorState`, `randomness.stream` and mutation reflection are allowed.

- Two founding genotype templates, each with 48 diploid adults at t0. Three static visitor environments: supply0/empty, 0.125/matched and 0.125/separated.
- Cross A allele half-width 0.046875/0.078125 with I within-adult homolog deviation scale 0/1, keeping every founder's **individual expressed M/I/A traits** and t0 F/P/S/flower/pollen ledger fixed. Only A birth mutation is enabled at original rate0.01 and original reflected Gaussian SD0.05. No M/I mutation, adult survival or seed immigration.
- Exactly 64 new independent master RNG histories per founder, each reused across its 12 nested arms. No old original demographic or three-update technical random seed may appear in the pilot. Treat a `(founder, history)` as the inferential resampling unit, **never 1,536 ecological replicates**.

## Prewritten prospective producer (not dispatched)

[`scripts/run_chapter2_clock_factorial_pilot_20261013.py`](../scripts/run_chapter2_clock_factorial_pilot_20261013.py) registers all six shards *before* starting any reproduction. Each shard is one founder×visitor context with **256 cases = four genotypes ×64 paired stream repetitions**. The complete bounded budget is **six shards, 1,536 cases and 307,200 reproductive updates**.

For each case the only mutable state is the original `PlantState` passed to original `population.advance`. All 201 annual censuses are retained: `ids`, two-homolog `alleles`, `allele_origin`, `mutation_flags`, `birth_years`, exact numeric offsets, population size and means; all 200 original female/male/self/pollen return vectors and full three-locus genotype-weighted parental selection matrix; all original father/mother/child parent pairs and offsets. Extinction means are stored missing, never zero. Exactly the original six mutually exclusive outcomes, using founder-relative A increase/I decrease threshold0.05 sustained 20 censuses and tie5, are recorded along with pre-existing .025/.1 sensitivity labels. No selected special environment, shorter horizon, or favorable history is allowed.

Each shard is an immutable source/seed/producer-stamped `REGISTRATION.json` + 256 checksum-addressed `.npz` files + `_COMPLETION.json` + `EXECUTION_COMMIT.txt`. An existing output directory/case cannot be replaced, and failed/partial shards must remain independently distinguishable rather than silently re-run. This code does *not* launch itself; any full run needs a separately reviewed explicit dispatch.

**Technical-only mode** (`--technical`) uses *different* salted random streams, exactly four source variants per selected shard and only three updates per variant. It does not count toward the 1,536 research histories. The source-specific tests exercise this path, the original typed biological operator and the outcome-category arithmetic, without launching a 200-update case in CI. An additional original-operator smoke archive runs four ×3-update technical fixtures, passes their ZIP to the separate independent reader, and verifies every census, reproductive return, parentage and five genotype fields through a second native replay. A deliberate forged parentID is rejected even after the attacker updates the raw NPZ hash in the source receipt. **Passing these short tests does not certify the unrun 200-update cohort.**

## Independent original-genotype reader (not yet used on a 1,536-path output)

[`scripts/read_chapter2_clock_factorial_pilot_20261013.py`](../scripts/read_chapter2_clock_factorial_pilot_20261013.py) intentionally **does not import the producer or its event code**. It checks exact ZIP member sets, all 256 registered case IDs and SHA256, source/runtime/config/geno provenance and that one original source stream determines all 12 paired arms. Every census and mutation/origin state is replayed from the original model's `reproduce` + `advance` and compared to saved arrays. It independently recomputes parentage, eight reproductive returns, three-locus parental fitness components and first 20-census sustained threshold-crossing times. It requires the original NumPy2.2.6 for exact all-genome replay.

A whole-campaign result is **not admitted** until each of all six 256-case shards passes this source reader and independent categorical inventory, all 1,536 original starts remain present, all registered six categories are preserved, and the corresponding actual execution-source commit and user-visible raw archive are durably identifiable. A passing 3-update producer smoke test is not a passing 1,536-case run.

## Scientific inference and stop rules

The pilot is a **new exploratory factorial**, not confirmation of the retrospective initial-clock predictor, not an empirical island system, not proof of natural evolutionary sequence benefits or extinction, and not an opportunity to change original frozen negative results. Its observations are allowed to estimate prospective *uncertainty* and check model feasibility, but they must never select favorable cells or replace already exposed data. Later independent confirmation requires a fully frozen, mathematically explicit two-stage clock, a **fair equal-or-greater-flexibility ecological×genetic null**, a single proper score, independent new seeds, a separate history-level power calculation and original input/source hashes before executing any confirmatory history.

**Current pre-dispatch conditions:** original CI 38356542933 successfully established the 48×3 source native technical gate in three Python versions, but the new prospective producer/reader source code and pilot registration need their **own** current-head CI, technical-only smoke and independent review. There is no biological permission to silently turn draft PR #498 into an executed 1,536-case result. Stop if model source, archive registration, event definitions, exact hash/case count or technical original genetics disagree.

## Proposed next technical-only command (no real pilot seeds)

```bash
python scripts/run_chapter2_clock_factorial_pilot_20261013.py --shard 0 --technical --out /tmp/source-clock-technical-only
```

Do not supply `--technical` for any real 200-update case until the full producer, raw reader, source locks, archive retention and necessary approval gates have been independently accepted.
