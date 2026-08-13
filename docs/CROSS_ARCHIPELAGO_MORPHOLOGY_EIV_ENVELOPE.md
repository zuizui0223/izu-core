# Cross-archipelago morphology errors-in-variables envelope

## Purpose

The checked morphology response-shape audit finds the same source-native OLS
direction in two independent island systems:

| system | direct OLS slope `log(island) ~ log(mainland)` | island-cluster interval |
|---|---:|---:|
| Southwest Pacific animal flower size | 0.84901 | [0.69164, 0.92580] |
| Hendriks 2019 flower area | 0.58334 | [0.21279, 0.77849] |

Both intervals are below the isometry slope of 1. The open question is how much
classical measurement error in the mainland predictor would be sufficient to
remove that below-isometry interpretation.

This document describes a **partial-identification sensitivity**, not an
estimate of measurement reliability.

## Declared classical x-error model

Let

```text
beta_observed = reliability_x * beta_true
```

where `reliability_x` is the reliability of the observed mainland log-trait.
If reliability is at least `r`, the largest attenuation-corrected slope allowed
by this simple model is `beta_observed / r`.

For a point estimate or the upper end of an island-cluster interval to remain
below isometry after correction, its observed value must therefore be smaller
than `r`.

The scenario value `r` is used as a **lower bound in both systems**. This does
not assume that the two reliabilities are numerically equal.

## System-specific thresholds

### Southwest Pacific animal flower size

- point estimate remains below isometry if reliability > **0.849005**;
- island-cluster interval remains wholly below isometry if reliability >
  **0.925899**.

### Hendriks 2019 flower area

- point estimate remains below isometry if reliability > **0.583336**;
- island-cluster interval remains wholly below isometry if reliability >
  **0.778493**.

Southwest Pacific is therefore the binding system for both the joint point and
joint cluster-interval conditions.

## Joint lower-bound envelope

For both independent systems simultaneously:

- both corrected point estimates stay below isometry if both mainland-trait
  reliabilities are > **0.849005**;
- both corrected island-cluster intervals stay wholly below isometry if both
  reliabilities are > **0.925899**.

Selected scenarios make the distinction explicit:

| reliability lower bound | both points < 1 | both cluster intervals < 1 | interpretation |
|---:|---|---|---|
| 0.85 | yes | no | point-direction replication survives, interval-level exclusion does not |
| 0.90 | yes | no | same |
| 0.925 | yes | no | Southwest Pacific upper bound is still just above 1 after correction |
| 0.93 | yes | yes | both cluster intervals remain below isometry under the declared model |
| 1.00 | yes | yes | observed/no-attenuation case |

At `r = 0.90`, the corrected Southwest Pacific cluster upper bound is about
`1.0287`, while Hendriks remains below one. At `r = 0.93`, the corresponding
Southwest Pacific upper bound is about `0.9955`, so both systems remain below
isometry under this classical model.

## Why this does not open formal synthesis

The envelope quantifies what must be assumed; it does not establish that the
assumption is true.

1. Neither source empirically identifies mainland-trait reliability at the
   required level.
2. The model is classical x-error only; correlated, nonclassical, taxon-specific,
   or source-specific measurement error can behave differently.
3. Hendriks' island-cluster SMA interval is `[0.72967, 1.07310]` and includes
   isometry. SMA is not a uniquely correct error model, but it demonstrates that
   a symmetric-axis structural sensitivity is less decisive than OLS.
4. Hendriks' underlying thesis/data artifact is not yet checksum locked.
5. Southwest Pacific uses source-defined flower size while Hendriks uses flower
   area. They are related response shapes, not identical raw effect scales.

Therefore the EIV envelope remains:

```text
effect_registry_eligible = false
formal_same_family_meta_analysis_ready = false
```

## Current interpretation

The strongest supported statement is:

> Two independent systems reproduce a below-isometry island floral response
> shape under source-native OLS and island-cluster resampling. Under a classical
> x-error model, that 2/2 interval-level recurrence would remain below isometry
> if mainland-trait reliability were above about 0.926 in both systems. That
> reliability is a required condition, not an observed quantity.

This is stronger than a single-system pattern, but weaker than a universal
island-rule coefficient or a measurement-error-resolved meta-analysis.

## Next empirical gate

The most informative next information is not another OLS p-value. It is one of:

1. repeated mainland-trait measurements that estimate reliability;
2. source-native measurement-error/precision metadata;
3. a stable Hendriks source artifact plus raw measurement replication; or
4. a third independent paired-flower system with a design that permits an
   explicit errors-in-variables analysis.

The checked machine-readable outputs are:

- `data/results/cross_archipelago_morphology_eiv_envelope_summary.json`
- `data/results/cross_archipelago_morphology_eiv_envelope.csv`
