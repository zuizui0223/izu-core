# Galápagos source-published summary analysis

## Scope

The raw Dryad package for DOI `10.5061/dryad.0c3cn5f` remains the required source for plant-by-pollinator matrices, species identities, interaction weights, and shared-plant partner turnover. Public file transport has returned delivery/authorization errors in GitHub Actions.

To avoid treating that transport failure as an absence of evidence, the repository now retains a separate, source-published summary layer based only on Tables 1 and 2 of Nnakenyi et al. (`10.1111/oik.06053`). The checked source table contains ten island rows and the following published quantities:

- plant and pollinator richness;
- interaction count and weighted connectance;
- sampling hours;
- island isolation, area, and age;
- observed nestedness;
- AIS and null prediction means and reported 95% interval half-widths.

No raw plant-pollinator edge is reconstructed from these values.

## Reproduced model-performance result

Using the ten published island means:

| diagnostic | value |
|---|---:|
| observed–AIS Pearson `r` | `0.82837` |
| observed–AIS `r²` | `0.68620` |
| observed–null Pearson `r` | `0.79036` |
| observed–null `r²` | `0.62467` |
| AIS MAE | `0.0268` |
| null MAE | `0.0367` |
| AIS RMSE | `0.03561` |
| null RMSE | `0.05173` |

The AIS association therefore reproduces the article-level statement of approximately 69% explained variation.

That result does not imply consistent island-level superiority:

- AIS has lower absolute error on `4/10` islands;
- the mean absolute-error improvement over the null is `0.0099`;
- the median improvement is `-0.0165`;
- the exact paired sign-flip test is `p = 0.5723`;
- both reported AIS and null intervals cover the observed value on `6/10` islands.

The supported reading is that AIS predictions track the broad ten-island pattern and have lower aggregate error, while island-specific improvement is heterogeneous and not consistently positive.

## Descriptive covariate screen

Observed nestedness is described against the fixed published island values. Every result remains descriptive and includes a leave-one-island correlation range rather than a standard error.

Examples:

| predictor | Pearson `r` | leave-one-island range |
|---|---:|---:|
| interaction count | `+0.712` | `+0.610 .. +0.940` |
| log sampling hours | `+0.764` | `+0.633 .. +0.898` |
| weighted connectance | `−0.737` | `−0.880 .. −0.515` |
| isolation | `−0.406` | `−0.660 .. −0.285` |
| age | `+0.251` | `−0.076 .. +0.459` |

The strong sampling association is a warning against reading richness or nestedness as a simple island-biogeographic response. Age is especially unstable to removal of one island.

## Admission boundary

These outputs are deliberately excluded from the cross-archipelago effect registry because:

- ten islands are nested within one archipelago;
- the AIS/null intervals are prediction intervals, not sampling uncertainty for a compatible biological effect;
- raw interaction matrices and shared-plant contrasts are unavailable;
- neither pollinator effectiveness nor effective plant dependency is measured;
- island-level correlations do not identify area, isolation, age, or adaptive switching causally.

The next source gate remains recovery of `data_galapagos_islands.zip` or an author/institutional copy with matching provenance.
