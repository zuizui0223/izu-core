# Dependency × FDQ prospective design simulation

## Question

The contemporary Izu network archive supports a positive relationship between
pollinator functional diversity (`FDQ`) and corrected flower–pollinator trait
matching. It does **not** contain a directly measured high-dependency Bombus
endpoint in the exact target populations.

The prospective question is therefore:

> Which new data structure is most likely to identify a future
> `effective dependency × FDQ` interaction: more rows at the current proxy
> support, more sites/seasons, one high-dependency endpoint, or a broader set of
> directly measured dependency values?

This is a design simulation, not a reanalysis that estimates the missing
biological interaction.

## Empirical structure used as an anchor

The source-native files in PR #90 supply only the design dimensions and current
evidence gap:

- 8 community sites;
- 5 seasons;
- 10 source-defined pollen-success targets;
- 9 taxa passing the existing proxy-moderation coverage gate;
- 105 eligible plant × site × season rows;
- 0 source-resolved high-dependency Bombus endpoints in those targets;
- 0 direct effective-dependency measurements in the exact 2024 Izu target
  populations.

The positive FDQ main relationship is retained as context. No observed
dependency value or empirical `dependency × FDQ` coefficient is available.

## Synthetic assumptions

Every scenario declares synthetic dependency values in `[0, 1]`. The values are
not species scores.

The two interaction alternatives are:

- `0.4` standardized outcome units per 1-SD FDQ change across a full `0 → 1`
  dependency contrast;
- `0.8` on the same scale.

The simulation also declares reliability, error variance and prospective
coverage assumptions. These are sensitivity settings, not pilot estimates.

The analysis fitted within each replicate is:

```text
outcome ~ FDQ + FDQ × observed_dependency
          + taxon fixed effects
          + site fixed effects
          + season fixed effects
```

Uncertainty is clustered by `site × season`, because all taxa sampled in a
site-season share the same FDQ value and cluster shock. A scenario-specific
critical absolute `t` value is calibrated from a synthetic null and checked in
an independent null-validation set.

Incomplete taxon coverage is redrawn in every replicate, subject to retaining
every taxon and every site-season cluster. This makes the result an envelope
over plausible sparse panels rather than a claim to reproduce the exact 105-row
incidence matrix.

## Scenarios

| scenario | purpose |
|---|---|
| `survivor_proxy_current` | 9 taxa, 8 sites × 5 seasons, 105 rows, narrow synthetic dependency support and proxy-like reliability |
| `survivor_proxy_more_seasons` | double seasons without repairing dependency support |
| `survivor_proxy_more_sites` | add four sites without repairing dependency support |
| `direct_narrow_9` | direct dependency measurement and denser coverage, but the same narrow support |
| `direct_add_high_endpoint` | add one high-dependency endpoint |
| `direct_full_span_10` | 10 taxa spanning almost the full dependency scale |
| `direct_narrow_16` | more taxa while dependency support remains narrow |
| `direct_full_span_16` | more taxa plus a broad dependency span |

## Reproducible result

Configuration:

- null calibration replicates: 250 per scenario;
- independent null validation replicates: 250;
- effect replicates: 400 per declared alternative;
- random seed: `20260810`.

| scenario | rows | dependency span | reliability | detection at 0.4 | detection at 0.8 | mean-estimate / truth at 0.4 |
|---|---:|---:|---:|---:|---:|---:|
| current proxy structure | 105 | 0.40 | 0.50 | 0.065 | 0.083 | 0.451 |
| proxy + more seasons | 210 | 0.40 | 0.50 | 0.075 | 0.183 | 0.597 |
| proxy + more sites | 158 | 0.40 | 0.50 | 0.085 | 0.218 | 0.648 |
| direct, narrow 9 | 180 | 0.40 | 0.85 | 0.125 | 0.240 | 0.858 |
| direct + one high endpoint | 200 | 0.80 | 0.85 | 0.248 | 0.685 | 0.877 |
| direct full span, 10 | 200 | 0.90 | 0.85 | 0.428 | 0.915 | 0.922 |
| direct narrow span, 16 | 320 | 0.40 | 0.85 | 0.213 | 0.508 | 0.878 |
| direct full span, 16 | 320 | 0.90 | 0.85 | 0.525 | 0.973 | 0.901 |

`detection` is the probability of exceeding the scenario-specific
null-calibrated threshold under the declared synthetic alternative. It is not
empirical power for the real system. Monte Carlo uncertainty is retained in the
machine-readable result.

## Interpretation

### More proxy rows do not repair missing predictor support

Doubling seasons increases the moderate-effect detection probability only from
`0.065` to `0.075`; adding four sites increases it to `0.085`. Under these
assumptions, more observations help the strong alternative somewhat, but the
estimated interaction remains heavily attenuated because dependency is noisy
and restricted to a narrow range.

This does not imply that additional seasons or sites are biologically
unimportant. They remain essential for environmental and temporal replication.
It means they cannot substitute for the missing biological predictor.

### Direct measurement reduces attenuation, but range still matters

Moving from proxy-like reliability `0.50` to direct-like reliability `0.85`,
while keeping a narrow dependency range, raises the mean-estimate/truth ratio
from about `0.45` to `0.86`. However, moderate-effect detection remains only
`0.125`. Better measurement alone cannot identify an interaction when all taxa
occupy similar positions on the predictor.

### One high endpoint is useful; a filled gradient is better

Adding one high-dependency endpoint raises moderate-effect detection to
`0.248`. At the same 10-taxon count and 200-row design, filling the dependency
gradient raises it further to `0.428`.

The endpoint is therefore high-value, but a single endpoint should not carry
the whole moderation claim. Multiple intermediate dependency values make the
slope less sensitive to one lineage.

### Dependency span matters even at fixed taxon count

With 16 taxa and identical coverage, broadening the synthetic dependency span
from `0.40` to `0.90` raises moderate-effect detection from `0.213` to `0.525`.
This is the cleanest design contrast: adding taxa inside a narrow survivor range
is less informative than sampling taxa that genuinely extend the dependency
axis.

## Field and source-recovery priority implied by the simulation

1. Measure effective dependency directly rather than assigning it from floral
   form, family, tube length or realized interaction breadth.
2. Obtain at least one credible high-dependency endpoint, but avoid relying on a
   single endpoint alone.
3. Seek a distributed dependency gradient across several independent lineages.
4. Preserve repeated site-season exposure so dependency values are observed
   across varying FDQ, rather than measuring each taxon at only one exposure.
5. Use pilot data to replace the declared reliability/error assumptions before
   locking a confirmatory design.
6. Keep non-establishment, hybrid replacement and interaction rewiring in the
   sampling frame; a survivor-only taxon set can truncate the predictor by
   construction.

## Run

```bash
python scripts/run_dependency_fdq_design_simulation.py \
  --config data/design/dependency_fdq_design_scenarios.json \
  --output artifacts/dependency_fdq_design_simulation/summary.json
```

Checked-in result:

```text
data/results/dependency_fdq_design_simulation.json
```

## Claim boundary

All dependency values, reliabilities, interaction effects and prospective
coverage fractions are synthetic. The simulation ranks design structures; it
does not estimate an empirical dependency × FDQ effect, historical selection,
historical Bombus loss, or a causal Oshima–Toshima boundary effect.
