# Model 3 Reproduction and Exposure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Implement independently verifiable reproductive accounting and life-history exposure, the first unit of the separately declared model 3.

**Architecture:** Two pure numerical modules supply a reproductive ledger and an exposure schedule/variance diagnostic. A deterministic verification script emits an auditable receipt; there is no evolutionary update or biological outcome campaign in this unit.

**Tech Stack:** Python >=3.10, NumPy >=1.24, pytest >=8.0; no new dependencies.

**Spec:** `docs/superpowers/specs/2026-09-25-model3-reproduction-exposure.md`.

## Global Constraints

- Never modify archived simulation equations, source locks or result files.
- Expected offspring counts may be fractional; do not silently renormalize failed reproduction.
- Accounting tolerances: absolute 1e-10, relative 1e-12. Correlation checks: 1e-10.
- Zero exposure is not_evaluable; malformed/nonfinite inputs are errors.
- No result from this unit is a finding about evolution, drift, natural k or regional floral mechanisms.

## Review Focus

1. Selfed offspring counted twice or viability loss applied twice: pin genome/offspring identity in Task 1.
2. Male success mistaken for pollen export: pin donor allocation to actual outcross offspring in Task 1.
3. Probability shapes broadcast silently: dimension/nonfinite/error tests in Tasks 1 and 2.
4. Long lifespan confused with many independent opportunities: compare perfectly correlated and independent schedules in Task 2.
5. Zero reproduction or zero exposure silently rescued: preserve zeros/statuses in Tasks 1–3.

## Task 1: Reproductive ledger

Files: create `scripts/model3_reproduction.py`; create `tests/test_model3_reproduction.py`.

Interface: `reproductive_ledger(transfer, ovules, pollen_scale, autonomous_selfing, inbreeding_depression) -> dict[str, numpy.ndarray]`. Return keys `female_outcross`, `male_outcross`, `outcross_by_donor_recipient`, `selfed_raw`, `selfed_viable`, `maternal_viable`, `genome_equivalents`.

- [x] Write the following first test and run it to observe the missing-module failure:

```python
import numpy as np
from scripts.model3_reproduction import reproductive_ledger

def test_outcross_accounting():
    r = reproductive_ledger(np.array([[0., 2.], [1., 0.]]),
                           np.array([10., 20.]), np.ones(2),
                           np.zeros(2), np.zeros(2))
    expected = np.array([10 * -np.expm1(-1), 20 * -np.expm1(-2)])
    np.testing.assert_allclose(r['female_outcross'], expected)
    np.testing.assert_allclose(r['male_outcross'], expected[::-1])
    np.testing.assert_allclose(r['genome_equivalents'].sum(), expected.sum())
```

- [x] Implement the exact formulas and validation in the spec. Use `np.divide(..., where=P>0, out=zeros)` for donor shares, `np.expm1` for stable saturation, and reject a nonzero transfer diagonal.
- [x] Add no-pollen tests: O=[10], a=[0.5], delta=[0.2] gives selfed_raw=[5], selfed_viable=[4], zero outcross and genome_equivalents=[4]. a=0 and delta=1 each independently produce the appropriate zero viable contribution.
- [x] Add tests for an asymmetric three-donor matrix, zero ovules, saturation, negative/nonfinite transfer, mismatched vector lengths, invalid probabilities and nonpositive pollen scale. Assert donor/recipient totals and ovule bounds.
- [x] Run `python -m pytest -o addopts='' --basetemp .model3-tests tests/test_model3_reproduction.py -q` and commit only module/tests after passing.

## Task 2: Life-history exposure

Files: create `scripts/model3_exposure.py`; create `tests/test_model3_exposure.py`.

Interfaces: `flowering_schedule(effort, flowering_probability, interval_survival) -> dict`; `effective_exposure(weights, correlation) -> dict`.

Schedule output keys: `alive_probability`, `expected_effort`, `total_expected_effort`, `normalized_weights` (None when total zero), `status`. Exposure keys: `variance_multiplier`, `k_eff` (None for zero exposure/zero diagnostic variance), `status`.

- [x] Write and run failing tests:

```python
import numpy as np
from scripts.model3_exposure import flowering_schedule, effective_exposure

def test_survival_schedule():
    r = flowering_schedule([1., 1., 1.], [1., 1., 1.], [.5, .5])
    np.testing.assert_allclose(r['expected_effort'], [1., .5, .25])
    assert r['total_expected_effort'] == 1.75

def test_independence_is_not_lifespan():
    assert effective_exposure([.5, .5], np.eye(2))['k_eff'] == 2
    assert effective_exposure([.5, .5], np.ones((2, 2)))['k_eff'] == 1
```

- [x] Implement survival as a cumulative product with initial survival 1, then multiply by flowering probability and effort. Return explicit zero-effort status without division.
- [x] Implement covariance diagnostic after validating shape, finite entries, symmetry, unit diagonal and PSD with `np.linalg.eigvalsh`; do not project invalid matrices to a nearest PSD matrix.
- [x] Test one episode; unequal weights [.9,.1] under independence yield 1/.82; zero effort; no flowering before maturity; zero survival; malformed/negative inputs; non-PSD R; R=[[1,-1],[-1,1]] with equal weights yields zero_variance_diagnostic and no finite k_eff.
- [x] Run both test files, then commit only the two new files and tests.

## Task 3: Verification receipt and scope documentation

Files: create `scripts/verify_model3_reproduction_exposure.py`; create `tests/test_model3_receipt.py`; create generated `data/results/model3_reproduction_exposure_verification_20260925.json`; update the life-history design document with implementation status.

Interface: `build_receipt() -> dict`, containing status `mathematical_verification_only`, canonical-LF SHA256 of the two implementation modules and spec, names/outcomes of analytic checks, and explicit `evolutionary_simulation_run: false`.

- [x] Write a failing test asserting the receipt status, required hash keys, no evolutionary-run claim and identity-check errors below the declared tolerance.
- [x] Implement independent two-plant hand-calculation and schedule examples from Tasks 1 and 2. A failed identity raises an error; never write a passing receipt after a mismatch.
- [x] CLI output must use exclusive creation for the requested output path. Test an existing path produces an error without modifying its bytes.
- [x] Run the focused suite, artifact-integrity regression tests and `git diff --check`. Confirm all archived locks/results remain unchanged.
- [x] Commit/push the independently verified first unit; report its exact scope. Do not claim the entire model 3 is finished. The next implementation plan must cover transfer generation and inheritance before any comparative evolutionary run.

## Execution and review gate

Recommended execution method: native, in the current isolated simulation-review checkout, with independent review of the completed unit after implementation. User approved all implementation tasks. The calculation unit is implemented and locally verified; remote verification is tracked in the execution ledger and task. No evolutionary model-3 outcome has been generated. Task commits were grouped atomically under a recorded ruling.
