# Design power for nectar-guide scenario recovery

## Question answered

Before collecting field data, a measurement plan should answer more than
“would a difference be statistically significant?” The relevant question here
is:

> With this set of intermediate observations, their expected variation, and
> their effective sample size, how often would the planned study retain the
> virtual true guide mechanism while excluding its declared alternatives?

`channel_id.guide_design_power` evaluates that question against the restricted
scenario classes in `guide_scenarios`.

## Error model

For a planned observable with total individual-level SD \(\sigma\) and
effective independent sample size \(n\), the current simulator draws a virtual
mean using

```text
SE = sigma / sqrt(n)
observed mean ~ Normal(expected model value, SE)
```

and supplies the scenario engine an interval

```text
observed mean ± interval_multiplier × SE
```

clipped at zero because all currently supported quantities are non-negative.
The default interval multiplier is 1.96.

This is an intentionally transparent first approximation. It is appropriate
only when the sampled mean is reasonably approximated by a normal distribution
on the declared scale. Rare visits, binary handling scores, paternity counts,
and strongly zero-inflated outcomes need a likelihood-specific extension
(Poisson, binomial, beta-binomial, or hierarchical model) before their final
field design is trusted.

## What a design result reports

For every plan, the simulator returns:

| Output | Meaning |
|---|---|
| `truth_retention_rate` | fraction of virtual datasets retaining the declared true scenario |
| `unique_truth_recovery_rate` | fraction retaining only the true scenario; the strict discrimination target |
| `unique_truth_given_retained_rate` | strict recovery conditional on not rejecting the truth |
| `mean_compatible_scenarios` | average number of scenario classes still surviving |
| `mean_false_survivors` | average count of surviving false classes |
| `scenario_survival_rates` | survival probability of each candidate class |
| `no_compatible_scenario_rate` | rate at which measurement intervals reject every declared scenario |

A plan that has high unique recovery but poor truth retention is not good: it
is merely overconfident. Read strict recovery together with truth retention.

## Effective sample size, not raw count

`sample_size` means the number of approximately independent units underlying a
measurement mean. It is **not** automatically the number of flowers or videos.
For example, 20 flowers from one plant on one calm afternoon share plant state,
local pollinator conditions, and observer conditions. Treating them as 20
independent replicates will overstate power.

For a balanced cluster design with \(m\) observations per cluster and
within-cluster correlation \(\rho\), a common rough conversion is:

```text
n_effective ≈ n_raw / (1 + (m - 1) × rho)
```

Use pilot data to estimate variance components or an intraclass correlation.
Where this is not available, sweep conservative values of `n_effective` and
individual-level SD rather than presenting a single optimistic number.

## Recommended first sweep for Izu

Start with the smallest mechanism set that matches first-year field data:

```text
M0 null
M1 visit-attraction
M2 handling / pollen placement
M4 assurance compensation
```

Build plans that vary three things:

1. **measurement set**: guild-resolved visits alone; visits plus per-visit
   handling or stigma pollen; visits plus outcross/selfed seed component;
2. **effective sample size**: e.g. 10, 30, 60, 90 independent plant-day or
   plant-flower observation units, subject to the actual sampling hierarchy;
3. **total individual-level SD**: optimistic, pilot-estimated, and conservative
   values for every observable.

`examples/guide_design_power_sweep.py` contains a virtual example. Its numbers
are illustrative only and must be replaced by pilot estimates before being
used to set a field target.

## Decision rule before fieldwork

Predeclare a design criterion. For example:

```text
truth retention rate >= 0.90
unique truth recovery rate >= 0.80
mean compatible scenarios <= 1.25
```

These are planning targets, not universal thresholds. Choose them before
viewing field outcomes and state the candidate scenarios, parameter ranges,
error assumptions, and census window alongside them.

## What this does not solve

A high simulated recovery rate only says that the plan can recover a virtual
truth under its own declared model and measurement-error assumptions. It does
not establish that the truth is biologically realistic, that guide contrast is
heritable, or that unmeasured pathways are absent. It is a guard against an
underpowered or non-discriminating field design, not evidence of evolution by
itself.
