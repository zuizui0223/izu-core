# Additional response-rule factorial — 2026-09-25

Parent: c788c740. Additional frozen diagnostic; not replacement of the original result.
Eight rules plus fixed state; 6 seeds × 5 k × 96 histories × 21 starts. Histories shared across rules.
All 270 rule/seed/k rows, 360 paired conditional contrasts and 30 NPZ cell-array files are retained.

Primary/smooth reported median replay maximum absolute error: 1.11e-16.

## All conditions at k=16

t: service threshold enabled; d: response damping by (1-service); best/centroid: response target.
Fractions are separately computed six-seed medians, not causal contributions or guaranteed to sum to 100%.

| Rule | S % | C % | I % | Initial-terminal slope, mainland | island |
|---|---:|---:|---:|---:|---:|
| fixed | 13.48 | 28.93 | 56.85 | 1.00 | 1.00 |
| t0_best_d0 | 63.03 | 10.58 | 26.19 | 0.99 | 0.70 |
| t0_best_d1 | 54.27 | 14.01 | 31.38 | 1.00 | 0.77 |
| t0_centroid_d0 | 2.74 | 90.35 | 6.62 | 0.20 | 0.09 |
| t0_centroid_d1 | 4.09 | 48.93 | 46.83 | 0.46 | 0.39 |
| t1_best_d0 | 53.53 | 14.05 | 32.03 | 1.00 | 0.83 |
| t1_best_d1 | 47.78 | 16.59 | 35.78 | 1.00 | 0.84 |
| t1_centroid_d0 | 4.17 | 30.55 | 65.23 | 0.79 | 0.78 |
| t1_centroid_d1 | 6.15 | 30.28 | 63.41 | 0.80 | 0.79 |

## Median winner at every audited k

| Rule | 1 | 2 | 4 | 8 | 16 |
|---|---|---|---|---|---|
| fixed | C | I | I | I | I |
| t0_best_d0 | C | C | S | S | S |
| t0_best_d1 | C | I | I | S | S |
| t0_centroid_d0 | C | C | C | C | C |
| t0_centroid_d1 | C | C | I | C | C |
| t1_best_d0 | C | I | I | I | S |
| t1_best_d1 | C | I | I | I | S |
| t1_centroid_d0 | C | I | I | I | I |
| t1_centroid_d1 | C | I | I | I | I |

## Interpretation

At k=16, best→centroid reduces S fraction in 24/24 conditional contrasts (4 settings × 6 seeds; these are not 24 independent seeds). Range: -0.6428 to -0.3829.
Removing the threshold alone does not remove S dominance. Under the tested parameters, target choice is the clearest determinant of high-k S dominance.
This does not prove that loss of initial-trait memory causes loss of S: fixed state has slope 1 but is I-dominated. S concerns expected service contrasts, not trait retention.
Continuous centroid movement without damping remains C-dominated by median at every audited k. C/I reversal is therefore not universal across all response operators; preserve this additional narrowing.
These are within-model interventions, not evidence for historical regional selection, genetic evolution, or a calibrated plasticity mechanism.

## Replay and integrity

`python -m scripts.audit_chapter2_update_factorial --out <new-directory> --workers 3`
Output directory must be new. Resolved configuration and canonical-LF source hashes are checked before and after execution and in each batch.
The integrity maintenance modifies no biological equations; prior source correction identifiers remain archived. Changed files require explicit revised locks, never name-only exemptions.
Terminal arrays: layer 0 service difference, layer 1 mainland final trait, layer 2 island final trait; axes layers × starts × histories.
