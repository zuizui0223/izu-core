# PR471: complete stored equal-pollen readout

Date: 2026-10-12. This is delivery and verification of the existing restricted-model diagnostic, not a new biological experiment. The source baseline is main `bb150519507c82d75c1ba4bef1d7e9b3d5889b7c`, which merged PR471.

## Result and limits

Across all 24 previously declared combinations, the largest absolute native-expression P80 residual after statewise total-pollen matching is **0.004470588129878994 percentage points**. The matched-pollen residual is small in this tested domain; it is not a formal equivalence result or a natural mediation fraction.

| Visitor-optimum interpolation coefficient | Shifted minus unscaled reference P80, range (percentage points) | Largest absolute statewise-equalized residual (percentage points) |
|---:|---:|---:|
| 0.25 | -9.2982610556 to -0.1549133520 | 0.004470588130 |
| 0.50 | -26.8912309389 to -0.2388885184 | 0.003944008493 |
| 1.00 | -29.0213149046 to -0.2449215069 | 0.000000240999 |

Each row includes all eight mating-rule/budget combinations. The interpolation coefficient changes visitor optima; it is not a percentage of visitor loss. There are four visitor types in every arm. P80 denotes the model probability that a population is occupied at update 80, not an observed survival frequency. CSV probability columns are on [0,1]; columns ending in `_pp` are percentage-point contrasts.

The largest residual occurs under assurance cost, budget 8, coefficient 0.25. P80 is 0.7539745475344649 in the unscaled matched reference, 0.6609919369784903 under shifted visitor optima, and 0.6610366428597891 in the statewise-equalized reference. These are three distinct interventions; their contrasts cannot be converted into a natural mediation percentage.

## Why the fixed-expression control agrees

Every plant has the same matching trait x=0.20. Affinity therefore separates as `(0.1 + I_i) * g_k`. For distinct donor i and recipient j, transfer has the form `E_i * (0.1 + I_j) * C`, where C is a common visitor factor. When every investment expression is also fixed to 0.35, off-diagonal transfer entries are equal. Matching aggregate pollen then matches the whole transfer matrix. Self-transfer is excluded, and both singleton transfers are zero. The ovules, viable seeds, parent-pair lottery and full next-state kernel consequently coincide under this fixed-expression control. This is a property of these imposed homogeneous traits, not a result for heterogeneous natural plant populations.

The native-expression arm retains segregating investment alleles 0.20/0.50. Its small residual must not be assigned uniquely to paternal routing: aggregate equalization does not separately fix all recipient and parent contributions. Scope is K8/B48, 80 updates, fixed assurance 0.35, no mutation, adult survival or seed immigration, and state-dependent visitor effectiveness. The latter is an artificial operator intervention, not one static replacement community.

## Stored evidence and provenance

- [Complete 24-row numerical table](../data/results/chapter2_statewise_pollen_readout_20261012.csv).
- [Provenance, original artifact hashes and direct source pins](../data/results/chapter2_statewise_pollen_readout_receipt_20261012.json).
- [Existing native source audit](../scripts/audit_chapter2_q3q4_statewise_pollen_equalized_20261011.py).
- [Stored-table and native-source regression tests](../tests/test_chapter2_statewise_pollen_readout_20261012.py).
- [Original diagnostic scope](CHAPTER2_Q3Q4_STATEWISE_EQUAL_POLLEN_FUNCTIONAL_CONTROL_20261011.md).

The CSV is the original independently reconstructed table with only CRLF converted to LF; no row, column or numeric token changed. Its earlier full conversation ZIP remains distinct from tracked files and is not represented as a release asset or external DOI deposit.

Fresh local equation recomputation used the preserved standalone matrix and separable-kernel implementations, explicit homolog enumeration, and independent Poisson/multinomial arithmetic. All 24 numeric readouts and the unscaled-reference CSV were exactly unchanged. Coverage was 96 equalized/shifted kernels plus 16 unscaled-reference kernels; 165 states per kernel. The maximum discrepancy between independent equalized kernel entries was 1.7208456881689926e-15. These arithmetic checks share the same declared biology and are not independent ecological replication.

Local native-repository execution was unavailable because source archive download failed. Native execution is a separate CI obligation, not inferred from that local recomputation. The new test invokes the existing native audit for all 24 contexts, recomputes eight native unscaled-reference kernels, and compares 72 saved occupancy probabilities plus 24 fixed-expression contrasts at absolute tolerance 1e-12. A separate test checks four declared direct input blobs, not a complete transitive environment lock. Read exact-head CI to determine whether this native check has passed.

## Reproduce without changing stored evidence

From a repository checkout:

```bash
python -m pip install -e '.[dev]'
python -m scripts.audit_chapter2_q3q4_statewise_pollen_equalized_20261011 --out /tmp/pr471_native.json
python -m pytest -q tests/test_chapter2_statewise_pollen_readout_20261012.py
```

The first command prepares the existing declared development dependencies; the native runner writes outside the tracked result table. The test additionally evaluates the unscaled reference through the existing functional-mismatch module. The frozen primary cohorts, active manuscript, historical discovery-original admission and external data-deposition task are unchanged.
