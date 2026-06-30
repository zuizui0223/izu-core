# Empirical anchors for spot-trait gradient simulation

## Purpose

This module connects the current empirical study to the constrained-simulation
repository without pretending that the empirical summaries identify a mechanism.
It is intended for the following evidence structure:

1. a population-level spot trait shows differentiation relative to neutral
   genomic structure through a P_ST--F_ST sensitivity analysis;
2. selfed and outcrossed offspring differ in fitness on a declared common census
   interval;
3. focal pollinator guilds are detected or not detected under recorded
   observation effort.

The anchor layer converts those results into a **declared virtual trait axis**,
an optional late-inbreeding-depression parameter, and bracketing environmental
service cases. It does not estimate a visit effect, handling effect, realised
selfing rate, or selection coefficient from those summaries.

## What is observed versus assumed

| Quantity | Source | How the repository uses it |
|---|---|---|
| Population mean spot trait | Your population-level measurements | Orders virtual sites along a min--max-scaled trait axis. It is not geography. |
| P_ST and F_ST | Your sensitivity analysis | Reports whether the point P_ST comparison exceeds F_ST. It does not set a mechanism effect. |
| Selfed/outcrossed fitness | Your crossing or offspring study | Maps to late post-seed survival **only** if the census interval is explicitly post-seed. |
| Guild detection and effort | Your visitation observations | Retains availability context. It never becomes a numerical visit rate. |
| Low/high pollinator service | Declared sensitivity assumption | Defines flat, trait-aligned, and trait-opposed virtual service cases. |
| Trait-to-guide mapping | Declared sensitivity assumption | Scales observed spot means onto the model's 0--1 guide-contrast axis. |

This distinction is the point of the layer. The empirical study can support
selection-compatible trait divergence and a cost of selfing without claiming
that spots have already been shown to affect pollinator behavior.

## Input templates

Create the canonical files:

```bash
python scripts/generate_empirical_anchor_report.py \
  --write-templates data/empirical_anchor
```

Then fill the following files.

### `population_traits.csv`

```text
population_id,spot_trait_mean,spot_trait_sd,trait_n
```

Use one summary per population. The trait can be total spot fraction, a spot
PC1, or another predeclared scalar. All summaries must use the same scale.

### `pst_fst.csv`

```text
trait_name,pst,fst,critical_c_over_h2
```

Supply exactly one row. `critical_c_over_h2` is optional but recommended when
your P_ST analysis reports the sensitivity boundary at which P_ST exceeds F_ST.
The module reports it; it does not decide that a single point estimate proves
selection.

### `inbreeding_fitness.csv`

```text
census_interval,selfed_mean_fitness,outcrossed_mean_fitness
```

Use `post_seed` only when the comparison is specifically over a post-seed
interval such as germination-to-recruit survival. In that case the software can
set:

\[
\delta = 1 - \frac{w_{self}}{w_{outcross}}
\]

as the existing `late_inbreeding_depression` parameter. Use `total_lifetime`
when your comparison combines seed-set and later performance; it remains a
reported anchor but is intentionally not mapped into the post-seed layer.

### `pollinator_availability.csv`

```text
population_id,guild,detected,effort_minutes
```

`detected=false` means that the guild was not detected during the stated
observation effort. It is not a zero visit rate and not proof of ecological
absence. Include every effort block you want retained; the loader summarizes
within population × guild.

## Generate the anchor audit

```bash
python scripts/generate_empirical_anchor_report.py \
  --input-dir data/empirical_anchor \
  --focal-guild bumblebee \
  --service-low 0.25 \
  --service-high 0.75 \
  --output artifacts/empirical_spot_anchor.md
```

The report has three service cases over the exact same observed spot axis:

- `flat_pollinator_service`: no trait-correlated service gradient;
- `service_increases_with_spot_axis`: a declared positive service gradient;
- `service_decreases_with_spot_axis`: the opposite declared gradient.

Neither directional case is chosen from presence/absence records. They bracket
the mechanism interpretation that the current empirical data cannot identify.

## Use the anchored cases in the existing virtual workflow

```python
from channel_id.empirical_gradient_anchor import (
    EmpiricalGradientAssumptions,
    apply_inbreeding_anchor,
    empirical_gradient_cases,
    load_empirical_anchor_bundle,
)
from channel_id.izu_sensitivity_report import (
    default_izu_virtual_worlds,
    run_izu_sensitivity_report,
)

anchors = load_empirical_anchor_bundle("data/empirical_anchor")
assumptions = EmpiricalGradientAssumptions(
    focal_guild="bumblebee",
    pollinator_service_low=0.25,
    pollinator_service_high=0.75,
)
settings = apply_inbreeding_anchor(template_settings, anchors.inbreeding)

for case in empirical_gradient_cases(anchors, assumptions):
    worlds = default_izu_virtual_worlds(case.landscape)
    report = run_izu_sensitivity_report(
        worlds=worlds,
        plans=plans,
        template_settings=settings,
        sites=case.sites,
        replicates=200,
        seed=20260630,
    )
```

The `template_settings` still contains declared guide-to-visit and
guide-to-handling effect sizes. Sweep those values separately. The empirical
anchor layer does not estimate them.

## Correct interpretation in a manuscript

Appropriate wording:

> We used population-level spot differentiation, an inbreeding-fitness estimate,
> and pollinator-guild availability records to constrain a virtual trait-gradient
> sensitivity analysis. The analysis evaluated the identifiability of alternative
> visit, handling, and assurance mechanisms under declared parameter ranges; it
> did not infer the field mechanism from the simulation.

Inappropriate wording:

> The simulation showed that spotted flowers evolved through increased bumblebee
> visitation.

That latter statement would require direct flower-level behavioral or mating
observations, not the anchors supplied here.
