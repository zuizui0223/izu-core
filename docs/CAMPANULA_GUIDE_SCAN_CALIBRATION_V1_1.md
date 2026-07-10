# Campanula guide-scan calibration and contract v1.1

## Why v1.1 exists

Contract v1.0.0 was frozen before an independent specialist holdout was opened.
It correctly recorded that `izu-core` itself did not then contain a measured
island guide series. A subsequent audit found an already measured focal dataset
in the private companion repository `zuizui0223/shimahotarubukuro`.

The discovery occurred before running the holdout. Version 1.0.0 is therefore
retained unchanged as the audit trail, and version 1.1.0 records the newly
recovered calibration evidence. No evaluated holdout lineage informed this
amendment.

## Source

- source repository: `zuizui0223/shimahotarubukuro`
- locked source commit: `6343d152a743c240348c736baf5c65768c9b7020`
- source table: `results/per_island_summary.csv`
- measurement basis: flattened corollas scanned at 300 DPI
- guide trait: purple-guide area as percentage of segmented corolla area

The public-safe transcription is
`data/predictive_meta/campanula_guide_scan_summary.csv`. Raw scans remain outside
`izu-core`; the numerical rows retain the source commit and table path.

## Measured pattern

| island | regime | corollas | mean guide coverage | guide present | degraded fraction |
|---|---|---:|---:|---:|---:|
| Oshima | *B. ardens* | 88 | 28.39% | 1.00 | 0.15 |
| Toshima | no effective Bombus | 63 | 5.27% | 0.83 | 0.10 |
| Niijima | no effective Bombus | 35 | 12.15% | 0.77 | 0.26 |
| Shikinejima | no effective Bombus | 5 | 2.00% | 0.20 | 0.20 |
| Kozushima | no effective Bombus | 18 | 4.31% | 0.94 | 0.11 |

Using islands—not individual flowers—as the comparative units, the equal-island
mean across the four no-Bombus islands is 5.9325%. Relative to Oshima, the
second-transition difference is -22.4575 percentage points. Every no-Bombus
island is below Oshima, and every leave-one-no-Bombus-island-out difference
remains negative.

## Contract amendment

`data/predictive_meta/campanula_channel_shape_v1_1.csv` changes only the focal
visible-signal evidence status:

```text
v1.0.0: blocked_unmeasured / not estimated
v1.1.0: measured_scan_summary / second-transition decline
```

The first guide transition remains `not_observed` because no matching mainland
large-Bombus scan reference is available. The cross-lineage prospective
prediction remains unchanged: specialist-like visible signal may be flat or
weakly declining at the first transition and should decrease at the second;
open-generalist negative controls should remain flat.

## What this does and does not establish

This dataset now supplies a genuine biological calibration anchor for the
**direction** of the focal second-transition guide pattern. It is stronger than
a public-photo pixel proxy.

It does not by itself:

- identify Bombus loss as the causal mechanism;
- estimate selection on the guide;
- establish a first-transition guide response;
- remove preservation or unequal-sample-size concerns;
- validate the public-photo ROI operator across domains; or
- count as an independent cross-lineage replication.

The public-photo specialist holdout therefore remains unopened. Its observation
operator still needs independent biological validation on images that were not
used to formulate the final holdout result.
