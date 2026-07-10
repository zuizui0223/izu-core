# Campanula prediction contract v1

## Purpose

This document freezes the empirical pattern and the prospective cross-lineage
prediction **before** a validated specialist holdout is analysed.

The lock separates three things that must not be merged:

1. source-locked patterns already reported for the focal *Campanula* system;
2. a theory-facing prediction that has not yet been observed for the focal
   island guide/visible-signal channel; and
3. the open-generalist negative control used to detect false visual thresholds.

The machine-readable source is
`data/predictive_meta/campanula_channel_shape_v1.csv`. Its semantic agreement
with the scenario and public-image contracts is checked by
`scripts/validate_prediction_contract_v1.py`.

## Frozen focal pattern

| Channel | Evidence status | Empirical shape | large Bombus → *B. ardens* | *B. ardens* → no effective Bombus |
|---|---|---|---|---|
| floral size | source locked | continuous erosion | decrease | decrease or plateau |
| multilocus outcrossing | source locked | continuous erosion | flat or decrease within the declared interval/tolerance | decrease |
| autonomous reproductive capacity | source locked | second-transition step | flat | increase |
| guide / visible signal | blocked and unmeasured | not estimated | not scored | not scored |

Only autonomous reproductive capacity is declared as an observed sharp second
transition. Floral size and outcrossing must not both be described as two sharp
steps: the interval-aware joint profile treats them as continuous island-order
responses. Bagged capsule set is an autonomous-capacity proxy, not realised
selfing.

## Frozen prospective prediction

For specialist-like holdout lineages, the visible-signal prediction is:

```text
large Bombus → B. ardens:        flat or weak decrease
B. ardens → no effective Bombus: decrease
```

This is a **prospective theory prediction**, not a source-locked focal
Campanula result. It can enter the analysis only through a source-native trait
or an observation operator that has passed both negative- and positive-control
calibration.

For open-generalist negative controls, both transitions are predicted to be
flat at the shared visual-signal level. The existing *Ajania pacifica* result is
one C-rank lineage used to calibrate false positives; it is not a universal
estimate for generalist flowers.

## Competing scenarios

`data/predictive_meta/two_breakpoint_prediction_contract.csv` retains four
predeclared scenarios:

- `environment_only`;
- `body_size_only`;
- `small_bee_substitution`;
- `ardens_replacement_loss`.

The environment-only scenario remains `not_identified` in the regime-only
scorer. It cannot be called supported or contradicted until the explicit
climate, area, isolation and history likelihood is implemented.

## Amendment policy

Version 1.0.0 is frozen for the present holdout programme.

A scientific change to a locked direction, evidence status or empirical shape
requires all of the following:

1. a new versioned shape file rather than silently replacing v1;
2. a written reason tied to newly recovered source-native evidence or a stated
   correction;
3. updated semantic-lock tests;
4. a declaration of which taxa or images had already been inspected; and
5. demotion of any previously inspected evaluation lineage to calibration data
   if the changed rule was informed by its result.

Changing wording without changing the semantic fields does not require a new
version. Changing the prediction after viewing holdout results does.
