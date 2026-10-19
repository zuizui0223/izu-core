# Source-safe Model 3 diagnostic successors — 2026-10-16

**Basis:** source review [commit 62b20b5](https://github.com/zuizui0223/izu-core/commit/62b20b5b9f0d791b52ed3cb7ebdb6a3384a61233). This is software hardening, **not new biological experiments, independent founder replications, or changed historical Q1–Q4 endpoints**. Developed separately from the now-merged PR #570.

## Repaired interfaces

1. `scripts/model3_island/selection_expressed_v2.py` is a versioned, opt-in local gradient evaluator. Under fixed-A, reproduction expresses `config.fixed_assurance`, not potentially different non-expressed stored A alleles. The successor validates input and substitutes the expressed A only for diagnostic calculation. Evolving-mode formula remains the historical analytic evaluator; fixed-A joint A/I evolutionary thresholds are rejected.
2. `scripts/kernel_expression_accounting_20261013/verify_kernel_expression_independent_v2.py` requires **48 unique declared comparisons**, **96 native/fixed-expression kernels**, the original 165 K8 genotype-census states, 81-point curves, and the original **48×2×80×165** signed contributions. It binds each signed-array row to its metadata, pins the source-kernel SHA and computes both reference-order identities. Empty, duplicated, truncated or foreign inputs cannot produce an `ALL48` verdict.

Historical source files, producers, archived data, and SHA-pinned `INDEPENDENT_REVIEW.json` remain unchanged. The successor is a new read-only source check, not a rewrite of an older receipt. A green unit-test run does **not** authenticate the externally retained full native source NPZ.

## Validation and reproducibility

```bash
pytest -q tests/test_model3_selection_expressed_v2.py tests/test_kernel_expression_independent_v2.py
python -m scripts.kernel_expression_accounting_20261013.verify_kernel_expression_independent_v2 \
  --kernels /path/to/native_regenerated_kernels_and_state_curves.npz \
  --readout /path/to/extracted/READOUT.json \
  --contributions /path/to/extracted/ALL_STATE_TIME_CONTRIBUTIONS.npz \
  --out /new/path/INDEPENDENT_REVIEW_V2.json
```

Do not overwrite the original receipt. Old source readback remains separate from biological inference. Linux CI for the exact submitted commit must finish before merge.

## Remaining empirical/source gate

The original signed contribution arrays and native 96-kernel NPZ are retained outside the Git checkout. Until those bytes have been retrieved and this new verifier has been run on them, **full original-array v2 re-admission is pending**. The main scientific outcomes are unchanged. The historical gradient helper remains pinned, so migrate only compatible new diagnostic callers after checking their estimands/source contracts.
