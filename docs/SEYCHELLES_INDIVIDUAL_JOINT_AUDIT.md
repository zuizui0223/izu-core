# Seychelles individual joint-linkage audit

## Result first

The previous panel-level joint-identifiability matrix was deliberately conservative, but it hid a real lower-level linkage in the source-native Seychelles data.

For *Thespesia populnea*:

- census plant IDs are stored as `ID{integer}`;
- breeding plant IDs are stored as `{integer}`;
- exact prefix normalization gives **12** census/breeding plant overlaps;
- **8 plants** have census exposure plus both `Aut` and `X` breeding treatments;
- the existing source parser maps `Aut -> Auto` and `X -> Xenogamy`.

Therefore **raw individual-level exposure + direct reproductive-dependency ingredients do coexist** in one external lineage.

This is an upgrade of raw linkage, not an upgrade to an FDQ-equivalent cross-system moderation test.

## Direct dependency on the source scale

Across the full *T. populnea* breeding table:

- Auto fruit set = **3 / 39 = 0.0769**;
- Xenogamy fruit set = **15 / 30 = 0.5000**;
- Auto / Xenogamy = **0.1538**;
- source-scale dependency shortfall `1 - Auto/Xenogamy` = **0.8462**.

This is much closer to the Issue #91 `bagged_autonomous / supplemental_outcross` logic than the earlier generic `Auto` context label suggested.

The value remains a Seychelles *Thespesia* source-scale estimand. It is not numerically transported to *Campanula microdonta*.

## Linked eight-plant diagnostic

The eight jointly covered plants contain source census counts for four broad visitor groups:

- insects;
- sunbirds;
- fodies;
- skinks.

From those counts the audit reports:

- visits per flower-hour — direct census quantity;
- visitor-group Shannon diversity — derived exploratory metric;
- visitor-group Gini-Simpson diversity — derived exploratory metric;
- vertebrate visit share — derived exploratory metric.

The dependency diagnostic is plant-level `Xenogamy fruit proportion - Auto fruit proportion` because ratio-based dependency is undefined whenever Xenogamy fruit set is zero.

Exact two-sided permutation diagnostics over the 8 plants are:

| exposure diagnostic | Spearman rho | exact p |
|---|---:|---:|
| visits per flower-hour | 0.172 | 0.682 |
| visitor-group Shannon | 0.052 | 0.896 |
| visitor-group Gini-Simpson | 0.144 | 0.711 |
| vertebrate visit share | -0.209 | 0.609 |

No clear within-lineage exposure/dependency association is detected. This **does not falsify** the dependency-moderation hypothesis: `n=8`, treatment counts are sparse, several plants have zero Xenogamy fruit success, and the broad visitor-group metrics are not the Izu FDQ estimand.

## What changed scientifically

Before this audit:

```text
Seychelles panel
    -> partial exposure
    -> partial dependency
    -> partial same-population overlap
```

After inspecting the frozen raw artifact:

```text
Thespesia individual layer
    -> exact census/breeding plant linkage
    -> exact Auto and Xenogamy source treatments
    -> exact raw joint measurement ingredients
    -> exploratory broad visitor-group exposure metrics
    -> no harmonized FDQ-like exposure estimand
```

So the correct distinction is now:

1. **raw individual joint measurement: identified**;
2. **harmonized functional-exposure estimand comparable with Izu FDQ: not identified**;
3. **cross-lineage dependency x functional-exposure coefficient: not identified**.

## Consequence for Issue #91

Issue #91 remains the prospective mainline rather than being replaced by Seychelles.

The Seychelles audit is useful as an external architecture prototype because it shows that census exposure and Auto/Xenogamy experiments can be linked at the plant level. It also shows why the Izu pilot should preserve plant IDs across visitor exposure and reproductive treatments from the start.

For a future cross-lineage moderation test, do **not** reconstruct an FDQ analogue from the four coarse Seychelles visitor groups after inspecting the outcome. A common exposure estimand must be declared independently and made comparable across systems before a cross-lineage slope is fitted.

## Source provenance

- article DOI: `10.1002/ajb2.1499`
- Figshare dataset: `10.6084/m9.figshare.12029580.v2`
- GitHub workflow run: `31944425554`
- artifact: `9262914774`
- artifact digest: `sha256:c335b92482ee65774904d5c1296cf7a12f95d1ebb7977e155e22bc861d73fa78`

The primary paper defines pollination quantity from visitor observations, quality from single-visit fruit/seed outcomes, and the invasive-ant disturbed/undisturbed contrast. The present audit does not alter those source definitions.
