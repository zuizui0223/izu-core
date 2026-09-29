# Pooled Izu-gradient evidence scoring

## Why a pooled score is needed after the interval benchmark

The interval benchmark asks whether each candidate is compatible with every
site's conservative intervals.  That is useful for falsification, but it has an
important limitation: all evidence is turned into a pass/fail statement before
islands are combined.

For an island gradient, the directional pattern matters.  The pooled scorer
therefore retains the raw virtual count data and adds their log probabilities
across sites:

```text
camera exposure × expected visit rate
  → detected visits                 : Poisson
  → called legitimate among detected: binomial

potential ovules
  → outcross / self / other fates   : multinomial
  → outcross / self / unresolved calls among genotyped mature seeds
                                   : conditional multinomial approximation
```

The candidate whose declared observation process assigns the greatest pooled
log likelihood is ranked first.  These values are **comparative scores within
the supplied candidate set**, not posterior probabilities, Bayes factors, or
proof of evolutionary history.

## What pooling changes

The earlier all-island interval rule can leave several candidates alive even
when the combined gradient contains directional evidence.  This scorer answers
a different question:

> Given the declared count and classification processes, which candidate best
> predicts the joint pattern over the selected islands?

It does not replace the interval benchmark.  The two diagnostics should be
reported together during virtual design:

- conservative compatibility / truth retention;
- pooled ranking / likelihood gap.

A candidate that wins only under pooling but fails conservative compatibility is
not automatically supported; it signals that the model and calibration deserve
closer inspection.

## Calibration assumptions inherited from the observation layers

The scorer treats the following protocol quantities as externally calibrated
inputs:

- camera visit-detection probability;
- legitimate-handling annotation sensitivity and specificity;
- probability of unresolved paternity calls;
- outcross-to-self and self-to-outcross paternity error.

It does not estimate those quantities from the same virtual data.  In a real
study, they require double scoring, calibration clips, validation parentage
sets, or an expanded joint measurement-error model.

## The paternity approximation

The virtual generator samples genotyped mature seeds within each fruit without
replacement.  The stored dataset keeps only site-level totals, so the pooled
scorer uses a conditional multinomial approximation for outcross, self, and
unresolved calls among the observed sampled mature seeds.

This is adequate to test the current *aggregate* data architecture.  It is not
a substitute for a final fruit-level parentage likelihood.  Preserve fruit ID,
maternal ID, mature seed count, number genotyped, and every paternity call in
the real data so the later model can retain that hierarchy exactly.

## What this is not yet

This is intentionally not called a hierarchical empirical model.  The current
virtual `IzuGradientDataset` contains one aggregate camera count and one
aggregate seed/paternity count per island.  Random effects for camera window,
flower, maternal plant, fruit, day, site, or year cannot be identified honestly
from those collapsed counts.

The next empirical-model stage needs data with at least:

```text
camera_window_id, flower_id, plant_id, site_id, date/time, exposure,
detected_visit_count, handling labels, scorer ID,
fruit_id, maternal_id, site_id, mature_seed_count,
genotyped_seed_count, paternity call, call confidence/replicate.
```

Only then should the Poisson, binomial, seed-fate, and paternity terms receive
plant/site/year random effects or overdispersion.

## Minimal virtual use

```python
from channel_id.izu_pooled_evidence import (
    benchmark_izu_pooled_evidence_recovery,
    score_izu_gradient_candidates,
)

# Score one already-simulated virtual dataset.
evidence = score_izu_gradient_candidates(
    candidates=candidates,
    dataset=dataset,
    template_settings=settings,
    landscape=landscape,
    camera_design=camera_design,
    seed_design=seed_design,
)
for candidate in evidence:
    print(candidate.scenario, candidate.total_log_likelihood)

# Estimate top-rank recovery across simulated datasets.
summary = benchmark_izu_pooled_evidence_recovery(
    truth=truth,
    candidates=candidates,
    template_settings=settings,
    landscape=landscape,
    camera_design=camera_design,
    seed_design=seed_design,
    replicates=1_000,
    seed=20260630,
)
print(summary)
```

Always repeat the virtual benchmark with `GradientAnalysisMode.FLAT_ENVIRONMENT`.
If the top-ranked route changes sharply when the background gradient is omitted,
field covariates must be measured rather than absorbed into the flower-trait
explanation.
