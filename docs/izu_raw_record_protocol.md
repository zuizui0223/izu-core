# Izu raw-record protocol and calibration plan

## Why this exists

The virtual field-stress test identified a concrete risk: recording more video
is not automatically safer when wind/light changes detection and the analysis
holds detection fixed.  The remedy is not to store a larger island-level visit
total.  It is to preserve the IDs and calibration records needed to estimate or
model the bias later.

This protocol is deliberately a **data architecture**, not an empirical model.
It defines what must survive field collection, video annotation, fruit
processing, and parentage calling before a hierarchical analysis can be honest.

## Generate the templates

```bash
python scripts/write_izu_raw_record_templates.py \
  --output-dir artifacts/izu_raw_record_templates
```

The command writes six blank CSV files plus a compact README:

```text
camera_windows.csv
visit_annotations.csv
camera_calibration_clips.csv
fruits.csv
paternity_calls.csv
paternity_validation.csv
README.md
```

Do not rename identifiers after records from later tables have been linked.
Use opaque, stable IDs rather than a mixture of handwritten names and row
numbers.

## The six tables

### 1. `camera_windows.csv`

One row per usable camera exposure interval on one focal flower.  Required
identifiers are `window_id`, `site_id`, `plant_id`, `flower_id`, and `device_id`.

`exposure_seconds` means usable observation time, not merely the number of
minutes the device was deployed.  Exclude intervals where the flower is absent,
blocked, too blurred to score, or the camera has failed.  Record `wind_class`
and `light_class` for every window, including `unknown` when the state was not
observed.  A missing condition should never be silently reclassified as calm or
bright.

### 2. `visit_annotations.csv`

One row per detected visit event.  `event_offset_seconds` locates the event
within its source window.  The primary handling label is one of:

```text
legitimate | non_legitimate | uncertain | not_assessable
```

Keep `uncertain` and `not_assessable` explicitly.  Do not force them into either
biological category just to make a binary table.  For a prespecified subset,
collect independent `secondary_*` labels; use
`adjudicated_handling_label` only after reviewing a disagreement.

### 3. `camera_calibration_clips.csv`

One row per clip selected to assess video detection and annotation quality.
`reference_*` counts must come from an independent reference scorer or a
predefined higher-quality reference procedure.  The table is count-level by
clip; event-level handling agreement remains in `visit_annotations.csv`.

Selection must be recorded as `random`, `stratified_random`, or `targeted`.
Only random or stratified-random clips should estimate ordinary detection
performance. Targeted clips are valuable for difficult events but must not be
mistaken for an unbiased detection sample.

### 4. `fruits.csv`

One row per fruit, retaining `site_id` and `maternal_id`.  Preserve the observed
`mature_seed_count`, the planned `genotyped_seed_target`, and the realised
`genotyped_seed_count`.  The latter must match the number of linked seed rows in
`paternity_calls.csv`.

### 5. `paternity_calls.csv`

One row per genotyped mature seed.  Each seed links to `fruit_id` and records a
call as:

```text
outcross | self | unresolved
```

For every unresolved call, `unresolved_reason` is required.  The allowed reason
set distinguishes low DNA, low coverage, ambiguous parentage, no candidate
parent, contamination, technical failure, and other.  This is essential: a
single unresolved count cannot reveal whether failure differs between outcrossed
and selfed seeds.

### 6. `paternity_validation.csv`

This is an external calibration subset: the `true_cross_type` must be known from
a controlled cross or another independent validation source, never inferred from
the paternity call being checked.  Preserve resolved and unresolved outcomes
for both true outcross and true self classes.

## Calibration protocol

### Camera detection: wind × light coverage

Before field interpretation, audit coverage separately for every wind × light
stratum that actually occurred.  The default software targets are deliberately
modest and editable:

```text
5 calibration clips / observed stratum
20 reference visits / observed stratum
10 reference legitimate events / observed stratum
```

Those are reporting thresholds, not proof that a detection estimate is precise
enough.  Sparse or rare strata should be reported as sparse rather than folded
into an untested global detection rate.

```python
from channel_id.izu_raw_record_protocol import (
    CameraCalibrationRequirements,
    assess_camera_calibration_coverage,
)

coverage = assess_camera_calibration_coverage(
    camera_windows,
    calibration_clips,
    CameraCalibrationRequirements(),
)
for stratum in coverage.uncovered_strata:
    print(stratum.stratum_label, stratum.reference_visits)
```

### Legitimate handling: independent double scoring

Use independent secondary scoring for a prespecified subset of events, with
special attention to clips around the legitimate/non-legitimate boundary.  The
field goal is not an impressive agreement percentage; it is to retain every
disagreement and its adjudication history.

```python
from channel_id.izu_raw_record_protocol import assess_handling_annotation_agreement

agreement = assess_handling_annotation_agreement(visit_annotations)
print(agreement.exact_agreement_rate, agreement.unresolved_disagreements)
```

### Parentage: resolution must be checked by true cross type

The #23 stress test specifically challenged an analysis where outcrossed seeds
are more likely to be unresolved.  A validation set that reports only overall
call success cannot detect that problem.

```python
from channel_id.izu_raw_record_protocol import assess_paternity_validation

report = assess_paternity_validation(paternity_validation)
print(report.summary_for("outcross").unresolved_rate)
print(report.summary_for("self").unresolved_rate)
print(report.outcross_minus_self_unresolved_rate)
```

## Validate before analysis

Build an `IzuRawRecordBundle` from the imported CSV rows and run:

```python
from channel_id.izu_raw_record_protocol import validate_izu_raw_record_bundle

validation = validate_izu_raw_record_bundle(bundle)
for issue in validation.issues:
    print(issue.severity, issue.code, issue.record_id, issue.message)
assert validation.valid
```

The validator checks duplicate IDs, links between tables, time/exposure bounds,
independent scorer IDs, count partitions, fruit/seed accounting, unresolved
reason completeness, and external parentage-validation metadata.

## Non-negotiable retention rule

Keep the raw rows even after making a site-level summary.  The future analysis
needs at least:

```text
site_id, plant_id, flower_id, device_id, window_id, timestamp, exposure,
wind/light/rain state, event ID, scorer IDs, handling labels,
maternal_id, fruit_id, seed_id, mature seed count, genotype status,
paternity call, unresolved reason, call confidence, replicate count.
```

Without those rows, site/day/camera/plant random effects and measurement-error
models are not recoverable later, no matter how sophisticated the final
statistical code becomes.
