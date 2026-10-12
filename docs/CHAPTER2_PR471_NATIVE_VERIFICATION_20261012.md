# PR471: native-source versus independent-equation verification

## Purpose and evidence boundary

PR471 is merged at `bb150519507c82d75c1ba4bef1d7e9b3d5889b7c`. Its native Python 3.10, 3.11 and 3.12 tests and scientific/reviewer-package gates passed. Earlier local work reconstructed the retrieved equations independently and later propagated saved matrices; it did **not** execute the native repository audit locally. This companion closes that distinct execution check without changing biology or the original PR471 source.

The dedicated job checks out the immutable native revision separately from the comparison code. It imports and runs the original `scripts.audit_chapter2_q3q4_statewise_pollen_equalized_20261011.audit`, records its complete output and compares all 24 declared contexts against the independent baseline. The main working tree and the model source are not modified by this comparison.

## Frozen comparison inputs and acceptance rule

- Prior conversation-delivered ZIP: `izu_core_pr471_verification_20261012.zip`, 15,348,576 bytes; SHA-256 `1f58a0f0988d1215a53ea50aa30ece049a37da4a0cd459a72a44f2f05065a783`.
- Original member `pr471_independent_results.json`: SHA-256 `0e223d05f8d479ccd448681fa7671f0715ade3fdde9b21bd59f38bb6f82451a6`.
- [Derived baseline CSV](../data/results/chapter2_pr471_independent_baseline_20261012.csv): SHA-256 `5d725462c7c7cd3a91ea27bd922491476ccee4cfb4b81f4c4f7dd1f01089408a`.
- 24 unique conditions; eight scalar comparisons plus four arms with three endpoint values per condition: **480 numerical comparisons**.
- Absolute agreement tolerance `1e-12`, with no relative tolerance, specified before this native execution. This is a software agreement threshold, not a biological equivalence margin or a revision to previous scientific rules.

Baseline values are copied from the independent result member, not refitted or regenerated using the native program. All 24 contexts are required. Duplicate/unknown/missing contexts, missing arms or fields, nonfinite/coerced numbers, changed baseline bytes, a different source commit, a dirty source tree, or numerical disagreement stop the comparison. Imported source files are checked against Git blob identities. The output records package versions and the full source-tree identity.

## Execution and outputs

The [dedicated workflow](../.github/workflows/chapter2-pr471-native-verification.yml) runs for pull requests touching these companion files and can be dispatched manually after integration. It does not run new random ecological histories. Outputs are `native_output.json`, `comparison.json`, the exact independent baseline and a file manifest, retained as an Actions artifact for 90 days. This is not external DOI deposition.

```bash
python scripts/verify_chapter2_pr471_native_20261012.py \
  --source-root /path/to/clean/bb150519-checkout \
  --expected-csv data/results/chapter2_pr471_independent_baseline_20261012.csv \
  --out /path/outside/source/pr471-native
```

A run is successful only when its comparison receipt reports `NATIVE_OUTPUT_MATCHES_INDEPENDENT_BASELINE` with all 480 comparisons. This document is an execution contract, not a claim that an unobserved run succeeded. The exact run and artifact receipt must accompany the numerical handoff.

## Interpretation remains bounded

The independent calculation's maximum native-expression equalized P80 residual is about **0.004470588 percentage points**, across the 24 restricted synthetic conditions. Matching is fixed at 0.20, assurance at 0.35, K=8, pollen-background B=48, with two investment alleles, four visitor types, zero mutation/adult survival/immigration and an 80-update horizon. Effectiveness is recalibrated at every genetic/census/expression state. A native-source match establishes implementation agreement, not new natural replication, unique paternal mediation, universal pollen-quantity sufficiency or historical discovery-original authentication. Original primary-study and active-manuscript claims are unchanged.
