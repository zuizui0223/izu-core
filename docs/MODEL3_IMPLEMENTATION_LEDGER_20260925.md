# Execution ledger — model3-reproduction-exposure plan

Plan: docs/superpowers/plans/2026-09-25-model3-reproduction-exposure.md
Base: 3e70582. User approved implementation of every plan item and result monitoring.

Pre-flight: Tasks 1/2 expose pure functions consumed by Task 3; signatures match. The zero-schedule case carries no normalized weights and must not be passed as None to the exposure function; the exposure API accepts an explicit zero vector.

Ruling: execute in the existing isolated simulation-review branch, using this durable ledger instead of shell-specific scratch helpers. No main-branch changes or frozen model modifications.

Ruling: all means all three approved plan tasks. Visitor transfer generation, inheritance and demographic evolution remain later units explicitly outside this plan. Verification results must say so.

Ruling: accept the float64 saturated limit for a finite positive pollen receipt divided by a tiny positive scale without overflowing; reject aggregate budgets that exceed the finite numerical range. This is numerical evaluation of the declared function, not biological retuning.

Task 1: complete. Tests observed missing-module RED, then GREEN for reproductive ledger and error/zero cases. Delayed selfing, paternal allocation and genome accounting are tested against hand calculations.

Task 2: complete. Tests observed missing-module RED, then GREEN for schedules, independent/correlated exposures, unequal weights, zero effort, negative correlations and invalid inputs.

Task 3: complete locally; remote verification pending. Receipt test observed missing-module RED then GREEN. Initial combined focused run: 48 passed, including archived factorial-artifact verification. Receipt checks are mathematical identities, not scientific outcome evidence.

Ruling: extend the existing manual structural-challenge workflow to execute the new foundation tests and upload a new source-matched receipt. This allows exact-branch remote verification while retaining the established frozen-model checks. It does not run model-3 evolution.

Independent final review and full-suite/remote results will be recorded before completion.

Independent review found two P2 issues: loss of declared schedule inputs and intermediate floating-point underflow. Added three regression cases, observed 3 failures, then fixed by returning input copies and retaining cumulative log survival until final effort evaluation. The focused suite now has 51 passing tests including three archived-artifact tests. The earlier receipt is preserved outside the checkout as work/model3-reproduction-pre-review-receipt.json; the regenerated source-matched receipt passes 17 analytic/status checks.

Ruling: group the three tightly connected task commits into one reviewed implementation commit so the receipt hashes and workflow land atomically. This changes commit granularity only; each task's missing-module RED and subsequent GREEN were observed separately as recorded above.

Second numerical review identified minimum-subnormal loss in a log roundtrip. A further RED-to-GREEN regression preserves nonzero direct products and uses log reconstruction only to rescue intermediate underflow. Final focused count: 52 passed (49 model-3 tests and 3 archived-artifact tests); receipt regenerated with 17 passing analytic/status checks.

Final independent review: no material blockers after boundary fixes; reviewer independently passed 26 exposure tests. First full run: 1696 passed, 1 skipped, 1 failure. The failure was a pre-existing manuscript text assertion requiring the overstrong “exact sufficiency boundary” phrase removed in commit 6fb6439. Updated the assertion to require the audited sufficient-but-not-necessary scope and forbid the old overstatement; no model equations or results were changed for this fix. Fresh whole-suite and exact-head CI follow this correction.
