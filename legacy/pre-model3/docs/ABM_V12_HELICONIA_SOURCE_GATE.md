# ABM v12 empirical test: Eastern Caribbean *Heliconia*

## Current decision

`heliconia_signed_position_projection_fails_declared_negative_direction`

The exact prospective projection is now complete. The frozen Dominica two-anchor mapping predicted a negative cross-unit relationship between signed corolla position and direct selection on corolla length. The recovered plant-level data instead give a positive point estimate:

- primary unweighted slope: `+0.052308`;
- descriptive 95% CI: `[-0.035251, +0.139868]`;
- Pearson correlation: `+0.387960`;
- predicted/observed sign concordance: `6/12` units.

The declared negative direction therefore fails. The mapping is not retuned.

## Source recovery and audit

Temeles et al. 2013, *Journal of Evolutionary Biology*, DOI `10.1111/jeb.12053`.

Dryad: `10.5061/dryad.64835`.

The individual public `file_stream` requests remain blocked in this environment, preserving the earlier route-specific negative recovery result. The official Dryad landing page's **Download full dataset** control exposed a distinct package route and recovered the complete archive:

- package: `doi_10_5061_dryad_64835__v20121024.zip`;
- bytes: `174400`;
- SHA-256: `9813060432d788cc46c49268b09b70a6eb2df8b9483814be3272c769c2143218`;
- target XLS files: `3`, each verified against API byte and MD5 metadata plus a frozen SHA-256 lock.

The workbooks contain 281 plant rows in 12 population × year × morph units. The analysis reconstructs the paper's within-unit standardization, relative seed fitness and multivariate direct selection gradient controlling mean bract number. All 12 published corolla-gradient/standard-error pairs are reproduced within the frozen absolute tolerance of `0.015`:

- maximum beta difference: `0.004990`;
- maximum standard-error difference: `0.007161`.

## Frozen mapping and visit weights

Martén-Rodríguez et al. 2011, *Oecologia*, DOI `10.1007/s00442-011-2043-8`, supplied the independent calibration:

- female *Eulampis jugularis* bill length: `26.6 mm`;
- male bill length: `19.8 mm`;
- female-associated *H. bihai* corolla: `47.8 mm`;
- male-associated *H. caribaea* corolla: `35.8 mm`.

These anchors defined, before the new exact target was calculated:

```text
expected corolla (mm)
  = 0.8588235294 + 1.7647058824 × pollinator bill center (mm)
```

The pollinator center uses the source-native sex-specific visit mixture for each admitted *H. caribaea* unit. Female *E. jugularis* were the sole recorded visitors of *H. bihai*; the pooled `N=14` is not duplicated into unit-specific counts. Signed position is:

```text
unit mean corolla - expected corolla
```

The primary target was frozen as an equal-unit OLS regression:

```text
source-method beta_multi_corolla ~ signed_position_mm
```

with a predeclared supported direction of **negative**.

## Sensitivity results

None of the declared secondary analyses rescues the negative prediction:

| Analysis | Result |
|---|---:|
| Primary equal-unit slope | `+0.052308` |
| Inverse-variance-weighted slope | `+0.066397` |
| Univariate corolla-selection slope | `+0.050670` |
| Leave-one-unit slopes | 11 positive, 1 slightly negative |
| Leave-one-lineage slopes | 2 positive, 1 negative |
| Sign concordance | `6/12` |

The lineage-omission sign change is a warning against treating the 12 units as independent cross-lineage replication. The conventional intervals are descriptive.

## Scientific interpretation

This is an informative failure of the exact empirical projection. A visit-weighted, two-anchor mean position is not sufficient to predict direct female-fitness selection across these *Heliconia* units. Plausible unresolved distinctions include lineage-level biology, other fitness axes such as bract number, temporal selection variation, and the difference between cross-sectional natural selection and an island-transition response.

The result does **not** show that starting state is generally irrelevant, and it does not falsify the v12 synthetic sufficiency result. It does narrow the empirical claim: v12 currently identifies a mechanism inside the declared ABM, but this first frozen signed-position projection does not validate that mechanism in a real system.

## Reproduction

The source package remains an ignored local artifact. With the exact Dryad package at the frozen path, run:

```text
python scripts/analyze_abm_v12_heliconia_signed_position.py
```

The committed result records source locks, all 12 derived units, reconstruction checks, the primary test and declared sensitivities in `data/results/abm_v12_heliconia_signed_position_test_frozen.json`.

## Boundary

Do not alter the 2011 mapping using the 2013 outcome, choose pollinator identity from floral phenotype, drop disagreeing units, or call this a fully literature-blind validation. The outcome pattern was known in the literature before raw recovery. The test is cross-sectional, includes repeated populations and years across three lineage/morph classes, and does not estimate a universal floral optimum or historical island-transition effect.
