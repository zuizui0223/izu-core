# Campanula guide-scan contract v1.1 — post-freeze provenance correction

## Historical purpose of v1.1

Contract v1.0.0 was frozen before an independent specialist holdout was opened.
A later audit found a numerical island summary in
`zuizui0223/shimahotarubukuro`, so v1.1 recorded the visible-signal channel as a
measured scan summary before any evaluated holdout lineage was opened.

The original v1.1 files remain unchanged as audit history. The 2026-07-15 source
audit found that the numerical table was an **initial automated segmentation
summary**, not the final aggregate of the later reviewed sheet outputs. Its
current claim use is therefore demoted to provisional direction evidence.

See `docs/CAMPANULA_GUIDE_SOURCE_AUDIT_20260715.md` and
`data/predictive_meta/campanula_guide_scan_provenance.csv`.

## Locked source

- source repository: `zuizui0223/shimahotarubukuro`
- locked source commit: `6343d152a743c240348c736baf5c65768c9b7020`
- source table: `results/per_island_summary.csv`
- source blob SHA: `822fb14d8bb7cc481800d58be503eb9308687304`
- measurement basis: flattened corollas scanned at 300 DPI
- operational trait: strict-purple pigment area as percentage of segmented
  corolla area

The public-safe transcription is
`data/predictive_meta/campanula_guide_scan_summary.csv`. The transcription is
exact for the locked table.

## Locked initial pattern

| island | regime | corollas | initial mean guide coverage | guide present | degraded fraction |
|---|---|---:|---:|---:|---:|
| Oshima | *B. ardens* | 88 | 28.39% | 1.00 | 0.15 |
| Toshima | no effective Bombus | 63 | 5.27% | 0.83 | 0.10 |
| Niijima | no effective Bombus | 35 | 12.15% | 0.77 | 0.26 |
| Shikinejima | no effective Bombus | 5 | 2.00% | 0.20 | 0.20 |
| Kozushima | no effective Bombus | 18 | 4.31% | 0.94 | 0.11 |

The arithmetic equal-island mean across the four no-Bombus islands is 5.9325%,
and the locked Oshima-to-no-Bombus difference is -22.4575 percentage points
when written as focal minus reference.

These numbers are not transcription errors. They are also not final reviewed
effect estimates.

## Why the evidence was demoted

The source repository is 92 commits beyond the locked commit and now contains
reviewed masks, split/exclusion corrections, improved scale/orientation logic,
reviewed spot detection, and a separate oxidised-inclusive guide trait. The old
island summary retains its original blob and was not rebuilt from those reviewed
outputs. At least one row count changed: Shikinejima is five corollas in the
locked table but six in the reviewed sheet output.

Consequently:

```text
v1.1 frozen metadata: measured_scan_summary / second-transition decline
current claim use:      provisional initial auto-summary / reaggregation required
```

A new scientific contract version is required after reviewed plant-level
reaggregation. v1.1 must not be silently rewritten into the future result.

## What remains permissible

The locked table can be cited as evidence that the initial automated analysis
produced a negative Oshima-to-no-Bombus direction. It cannot currently supply a
final effect size, a definitive island mean, or a validated causal calibration.

The first guide transition remains unobserved because no matching mainland scan
reference exists. The public-photo specialist holdout also remains unopened.
