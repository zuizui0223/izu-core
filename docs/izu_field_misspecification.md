# Izu field-misspecification stress tests

## Question

The pooled Izu scorer passed the ideal virtual benchmark because the generator
and scorer shared the same observation assumptions. That is necessary, but not
sufficient for field readiness.

This module asks a harsher question:

> When the field process departs from the ideal camera/seed/paternity model,
> how often does the ideal pooled scorer still put the true route first?

The departure is introduced **only in the generator**. The scorer continues to
assume the original calibrated detection, annotation, and paternity processes.
A drop in true-route top-rank recovery is therefore interpretable as sensitivity
to an omitted process.

## Stress processes

| Case | Generator-only departure | What a failure means operationally |
|---|---|---|
| `site_maternal_variation` | Site residuals in visitation/handling and maternal seed-fate variation | Preserve site, camera, maternal, and fruit IDs; aggregate counts are insufficient. |
| `wind_light_detection_loss` | Detection is lower on average and varies among collapsed site/day/window conditions | Record camera exposure, weather/light state, and calibration clips. |
| `handling_dependent_detection_loss` | Legitimate contacts are less detectable than other visits | Validate detection separately for legitimate and non-legitimate events. |
| `outcross_biased_unresolved` | Outcross seed calls are more likely to be unresolved | Track call confidence/failure reason and validate parentage resolution by cross type. |
| `combined_field_stress` | All departures occur together | Do not rely on the ideal aggregate pooled scorer for a field conclusion. |

The default numerical levels are deliberately moderate stress assumptions, not
estimates for any island. They are placeholders for pilot-calibrated ranges.

## What the generator changes

At a virtual site, the generator can apply:

```text
visit rate              × mean-one lognormal site residual
legitimate fraction      + logit-scale site residual
seed fate                × mean-one lognormal maternal residual
camera detection         × wind/light multiplier + site residual
legitimate detection     × relative detection multiplier
outcross unresolved odds × cross-type bias multiplier
```

The existing score does not receive those latent values. It still uses a
Poisson model for detected visits, a binomial model for handling calls, and
multinomial models for seed fates and paternity calls.

## Read the artifact

The workflow **Virtual Izu Field Stress** writes an artifact named
`izu-field-misspecification-stress`. It reports, for every virtual mechanism
world, observation plan, and stress case:

- `truth top`: fraction of virtual datasets where the true route is tied for
  highest pooled score;
- `unique truth top`: fraction where it alone is highest;
- `mean truth rank`: average rank of the true route;
- `mean truth log-likelihood gap`: truth score minus the strongest alternative;
- `no finite candidate`: datasets for which the ideal scorer assigns no finite
  score to any candidate.

A low `unique truth top` or a negative likelihood gap is not evidence that a
specific field mechanism is absent. It is evidence that the planned analysis is
not robust to the tested unmeasured process.

## Field consequences

The stress report does not say to increase all sample sizes. It distinguishes
what needs calibration from what needs replication.

- Loss under wind/light stress: add weather/light metadata and calibration
  windows; more uncalibrated video alone may preserve the bias.
- Loss under handling-dependent detection: annotate a validation subset from
  high-quality clips or independent human scores; raw visit total cannot repair
  contact-classification bias.
- Loss under outcross-biased unresolved calls: record every genotype failure
  and create an external parentage calibration subset; adding unresolved calls
  to the same likelihood is not enough.
- Loss under site/maternal variation: retain camera-window, day, plant,
  maternal, fruit, and seed identifiers so the empirical likelihood can use
  random effects or overdispersion rather than one count per island.

## Run locally

```bash
python scripts/generate_izu_field_stress_report.py \
  --replicates 25 \
  --output artifacts/izu_field_misspecification_stress.md
```

For sensitivity work, change one stress magnitude at a time and increase the
replicate count. Do not overwrite the default artifact silently and describe
any pilot-derived values as observed calibrations rather than assumptions.
