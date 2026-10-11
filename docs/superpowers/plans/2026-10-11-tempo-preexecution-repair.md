# Frozen tempo cohort pre-execution repair plan

> **For agentic workers:** Use superpowers:subagent-driven-development for the implementation and independent review. This plan completes the already authorized frozen experiment; it does not open a new biological design.

**Goal:** Make the existing 1,024-case abrupt/gradual experiment retain and report every declared endpoint before any full biological outcomes are generated.

**Architecture:** Keep native reproduction, inheritance, ecological schedules, seeds, thresholds and cohort size unchanged. Extend the wrapper's passive records and the strict complete-cohort readout. Preserve the registered paired 16-profile descriptive bootstrap.

**Tech stack:** Python 3.10–3.12, NumPy, existing Model3 sources, pytest.

**Spec:** `data/design/chapter2_sequence_abrupt_gradual_functional_loss_20261011.json` and `docs/CHAPTER2_SEQUENCE_ABRUPT_GRADUAL_FUNCTIONAL_LOSS_20261011.md`.

## Global constraints

- Exactly 16 profiles × four repeats × four timing/cost settings × two mutation rates × two schedules = 1,024 trajectories, 400 updates each.
- The original design JSON, model operators, biological parameters, RNG streams and primary event thresholds remain byte-unchanged.
- No full outcomes before reviewed code passes CI and scientific gates on main. Engineering smoke is at most 40 updates.
- All inference remains model-specific; profiles are the independent synthetic units. Missing/extinct trait values remain null.
- Bootstrap: 9,999 profile resamples, seed48272026, paired abrupt-minus-gradual, both percentile tails. No newly invented confirmatory p-value.

## Review focus

1. First sustained event t81..100 is confirmed by100; t82..101 is not. Emit separate by100/by400 order categories.
2. Extinction preserves observed zero occupancy but no numeric trait, selection gradient or conditional lag.
3. Parentage instrumentation and overlap recording consume no RNG and do not change trajectories.
4. Resume/readout rejects changed source, runtime, founders, smoke horizons, or rehashed inconsistent endpoint fields.
5. Conditional secondary differences expose their common-support count; nested replicates never become independent profile units.

## Task 1: Complete passive records and complete-cohort readout

**Files:** Modify the existing experiment runner, batch runner, summarizer and their tests. Add a focused `tests/test_chapter2_sequence_tempo_readout_contract_20261011.py` if helpful. Update the explanatory experiment document.

**Interfaces and requirements:**

- `simulate(...)` retains existing output fields; add actual founder-array hashes (and compact founder arrays), runtime identity, original `advance` parentage per update, and mean functional overlap defined as mean `exp(-((X_i-optimum_v)/breadth_v)**2)` over living adult×visitor pairs (null when no adults). Save realized source self/outcross recruit counts. Empty gradient samples include `n_near_zero: 0`.
- `source_identity()` includes all `scripts/model3_island/*.py` plus `scripts/model3_temporal_order.py` and the currently pinned orchestration/design files.
- Per-case receipts include and verify runtime/founder identities and declared horizon; existing full/smoke source isolation remains intact. `read_all()` requires a single consistent source/runtime/founder cohort and recomputes crossing/occupancy labels from original traces rather than trusting stale derived flags.
- Preserve existing full400 category fields with explicit horizon metadata. Add by100 categories derived only from events confirmed by100. State onset time and confirmation time distinctly.
- `clustered_summary()` exposes every original secondary endpoint: A-minus-I lag conditional on both crossings (by400), mean/variance for X/I/A at10/100/400, fixed-time sampled gradient summaries, pollen and overlap mean/range, native pre-mutation I/A expected responses, self/outcross recruitment and parentage availability. Retain 16 profile units and show eligible counts for conditional summaries. Show paired secondary contrasts only for paired eligible support.
- Keep two-sided descriptive bootstrap intervals as specified by the JSON method. Correct the prose promise of a separate 'difference test' to describe the two-sided interval actually registered; document that no new p-test is being introduced and the repair predates outcomes.

- [x] Write regression tests that fail on the missing records, the by100/full400 mix and source/provenance omissions.
- [x] Run those tests and record the expected failures.
- [x] Implement the bounded record/readout repairs and the pre-execution documentation clarification.
- [x] Run focused tests plus synthetic full-factorial readout checks with known expected differences and missingness; confirm no full Model3 outcomes were used.
- [x] Obtain independent code/scientific review and resolve material findings.

## Task 2: Integrate, execute and record

- [x] Integrate latest main into the PR branch without overwriting concurrent work.
- [ ] Run full pytest and verify latest-head CI/scientific gates; merge the reviewed PR under existing continuation authorization.
- [ ] Execute all frozen cases from the resulting main source; verify complete receipts and all16 manifests.
- [ ] Save compact results, source provenance and interpretation in the repository; retain the full raw archive durably.

## Progress and decisions

- Baseline observed: PR475 head4ac79b4; main904cad3; no full cohort execution recorded.
- Review confirmed: native parentage was discarded; visitor overlap was not recorded; secondary summaries were absent; primary by100 endpoints were shown with unlabeled full400 order categories.
- Decision: preserve the JSON's descriptive two-sided percentile interval; repair inconsistent prose, with no added confirmatory hypothesis test. Risk if misunderstood: an interval could be misread as a preregistered significance test, so the output labels it descriptive.
- Decision: record exact native parentage and reference overlap without altering model state or sampling. Verify against uninstrumented trajectories.
- Repair verification: six new targeted regression failures were reproduced before implementation. The repaired focused suite passed all29 tests in both the worker run and an independent root rerun (74.358 seconds). Native Model3 files, the temporal-order module and frozen design JSON are byte-unchanged. No full biological outcomes were generated during these engineering checks.
- Interpretation clarification: saturated occupancy or absent crossings can make an endpoint uninformative. A degenerate descriptive [0,0] interval is not evidence of practical equivalence or absence of any possible survival benefit.
- Independent review: approved for execution only after the existing full-suite, latest-head CI/scientific gates and merge to main. No material blockers remain; exact execution source digest is `9302c9740a1f5ac91cb1c1c39093f358c6fd745d4c5b768980e78d893aade80b`. All128 fixed-clonal profile/setting/schedule sign-clock checks matched an independent exhaustive scan; these generated no evolved full-cohort outcomes.
