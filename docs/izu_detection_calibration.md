# Finite detection-calibration validation

## What this virtual test adds

The #23 field-stress report found a specific failure mode: when effective camera
detection falls with wind/light but the likelihood holds detection fixed, a
visit-mediated route can be mis-ranked. More camera exposure does not fix that
problem by itself.

This module tests the narrow remediation that the raw-record protocol makes
possible:

1. generate camera observations with a hidden, condition-specific detection
   probability;
2. collect an **independent finite reference-visit sample** for the same
   virtual site-condition;
3. estimate detection with a beta-smoothed binomial proportion;
4. replace the nominal rate only in the Poisson visit-count likelihood;
5. compare ranking recovery with and without calibration.

The calibration stream is treated as revealing known visit opportunities. That
is an optimistic virtual assumption. It represents independent high-quality
review, a validated reference camera, or another prespecified standard—not the
same primary annotation being judged.

## What is calibrated, and what is not

| Component | In this test | Still uncorrected |
|---|---|---|
| Visit counts | Site-condition-specific detection estimated from reference visits | Reference-stream error and exposure mismeasurement |
| Handling labels | Retained in the likelihood | Legitimate-specific detection and annotation error |
| Seed fate | Retained in the likelihood | Maternal/fruit overdispersion |
| Paternity | Retained in the likelihood | Cross-type-dependent unresolved calls |

Therefore a recovery gain under `wind_light_detection_loss` says that the visit
count mismatch is addressable by detection calibration. It does **not** validate
handling classification or parentage calibration.

## Calibration estimate

For `d` primary detections among `n` independent known reference visits, the
software uses a beta posterior mean:

```text
(d + alpha) / (n + alpha + beta)
```

with default `alpha = beta = 1`. This avoids impossible 0 or 1 likelihood rates
from finite calibration samples. The prior is a numerical small-sample
stabiliser, not field evidence.

## Run the fixed report

```bash
python scripts/generate_izu_detection_calibration_report.py \
  --replicates 25 \
  --output artifacts/izu_detection_calibration.md
```

The report focuses on the two visit-containing virtual worlds, four illustrative
observation plans, two field stresses, and 10 / 50 / 200 reference visits per
virtual site-condition.

## Read the comparison

- `nominal truth top`: recovery when the pooled scorer incorrectly retains the
  camera design's nominal detection probability.
- `calibrated truth top`: recovery after the finite reference sample estimates
  a site-condition-specific effective detection rate.
- `Δ unique top`: added probability of the true route being the sole top-ranked
  structurally distinct candidate.
- `mean rank`: lower is better; 1 means the true route is top-ranked.

A positive calibration effect is an argument to collect reference data. It is
not a licence to use arbitrary targeted clips: calibration clips must retain
selection method and cover the observed wind × light strata, as defined by the
raw-record protocol.

## Direct field translation

The virtual site-condition is a compact stand-in for field condition strata.
For the actual study, estimate detection by compatible groups of:

```text
wind_class × light_class × device/camera configuration
```

and retain the actual exposure time plus clip-selection method. Do not fit a
separate rate for every sparse cell; prespecify pooling or a hierarchical
calibration model once pilot data show which strata have enough independent
reference visits.
