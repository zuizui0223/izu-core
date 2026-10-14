# Q3 distribution triangle implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Make the prospective three-policy experiment concrete, reviewable and fail-closed before requesting biological execution approval.

**Architecture:** Separate pure planning/statistics from activated native production/replay and raw-only publication verification. Reuse archived biological kernels unchanged, but create a new seed namespace, authorization contract and cumulative budget. No existing scientific file is overwritten.

**Tech Stack:** Python 3.11.14, NumPy 2.2.6, pytest, GitHub Actions, existing raw NPZ schema.

**Spec:** `docs/CHAPTER2_Q3_TRIANGLE_EXECUTION_DESIGN_20261014.md`.

## Global constraints

- 61 triggered states, 64 original slots, 144 triplets per trigger, three policies A/B/C.
- Namespace `izu-q3-distribution-triangle-v1-20261014`; no old approval reuse.
- 26,352 new futures only after approval; <=6,687,392 native updates including replay/fixtures.
- Six GiB free local admission; 64 GiB remote; <=300 hosted-runner minutes.
- Archive and preflight SHA identities are those in the spec; original source kernels stay unchanged.
- All eight intervals require complete records and joint survival for every triplet; never survivor-select.

## Review focus

- A valid-looking manifest with wrong namespace, seeds or state membership must fail before kernels load.
- Extinction must remain a biological outcome with full records and an explicit not-evaluable inferential gate.
- Partial shards and duplicates must not pass aggregation or reset cumulative reservations.
- File size, source and seed identities must bind archived raw fields rather than only aggregate JSON.
- Transport retry must not cause a second biological execution.

### Task 1: pure contract and precision/resource preflight

Create `scripts/q3_triangle_contract_20261014.py` and `tests/test_q3_triangle_contract_20261014.py`.

Interfaces: `seed_for(key, replicate, purpose) -> int`; `build_plan(cases) -> dict`; `summarize(records, cases) -> dict`. Input records are one triplet with arm terminal mean/null, survival bool and full-history event bool. The contract never imports native kernels or calls RNG.

- [x] Test namespaced purpose-separated seeds, full state/replicate inventory, exact sample/resource totals, bounds and margin decisions; run RED.
- [x] Implement pure deterministic seed/plan generation and statistics, including no-trigger policy zeros and all-or-none joint-survival gate.
- [x] Test missing/duplicate/foreign triplets, invalid support, inconsistent survival/null values, unequal block patterns and any extinction; run GREEN.
- [x] Independently review conditional target and confidence-family interpretation, and publish source-bound prospective design/plan as a draft PR.

### Task 2: activated producer and independent replay

Create `scripts/run_q3_triangle_20261014.py`, `scripts/verify_q3_triangle_paths_20261014.py`, and dedicated tests. Consume Task 1 seeds/plan; use the validated PR #515 constructor and frozen archived native modules.

- [x] Test absent/old/altered approval, namespace and source manifest failures before any kernel import; test cumulative counters and retries.
- [x] Implement 18 disjoint shards, explicit carrier permutations, original prefix/trigger binding, three arm futures, immutable raw writes and partial HOLD preservation.
- [x] Implement independent reconstruction of assignments and replay of every saved field/parentage; fixture call counter <=32. Actual scientific replay remains Task 4.
- [x] Run only synthetic/mock tests before approval; reserve native fixtures for the approved campaign.
- [x] Review all executable source and failure paths before publishing the inert workflow and manifest builder; three Important findings fixed with regression tests.

### Task 3: archive readback, workflow and concrete approval package

Create `scripts/verify_q3_triangle_archives_20261014.py`, `.github/workflows/q3-distribution-triangle-20261014.yml`, a manifest builder and tests. The workflow's trigger must obey the repository policy; any one-time branch activation must be registered narrowly without weakening unrelated workflow restrictions.

- [x] Test raw metadata, member hashes, shard coverage, full independent endpoint/statistic equality and one-archive-at-a-time handling with synthetic records.
- [x] Implement bounded upload/publication, stable release manifest and external byte readback; all-or-nothing scientific summaries. Actual publication remains Task 4.
- [x] Complete pure preflight and CI; bind reviewed source/workflow hashes and resources in an unapproved manifest.
- [x] Request approval for exactly the concrete campaign and costs. Keep all biological entry points closed until approval.

### Task 4: approved execution and scientific closeout

- [x] Activate each separately approved run once: initial zero-science HOLD and the explicitly approved repaired continuation; preserve both identities and cumulative accounting.
- [x] Follow live run handles, preserve partial results and prohibit automatic biological restarts.
- [x] Verify all trajectories/parents, raw publication, family decisions and independent receipts.
- [x] Answer the central question within the assigned-policy and joint-survivor limits; retain opposed, equivalent, unresolved and not-evaluable outcomes.
- [ ] Audit the full active goal against scientific evidence; do not complete it based only on the design or green tests.
