# Izu pollinator proboscis-length recovery

## Current state

The functional-exposure construct is now fixed, but the source-native numeric trait table needed to reconstruct it is **not yet in the repository**.

Hiraiwa & Ushimaru (2017) measured pollinator proboscis length in millimetres with digital calipers and report mean values by species × site in electronic supplementary Table S2. The paper reports **211 pollinator species**.

The frozen 2024 source artifact currently used by `izu-core` contains **209 unique named pollinator taxa** in `data_sp_pollinator.csv`, but no raw `proboscis_length_mm` column. It contains standardized functional columns used by the later analysis, which are not silently reverse-transformed into millimetres.

Therefore:

```text
current named visitor taxa in 2024 artifact = 209
source-native numeric proboscis values recovered in repo = 0
FDQ trait coverage = 0 / 209
2017 paper species count = 211
211 - 209 name/count discrepancy = unresolved
```

The 209 and 211 sets are **not assumed to be identical**.

## Source target

Primary targets:

- 2017 paper DOI: `10.1098/rspb.2016.2218`
- Dryad dataset: `10.5061/dryad.pm29d`
- Dryad file: `primary_data.xlsx`
- supplementary collection: `10.6084/m9.figshare.c.3647738`
- supplementary figures/tables item: `10.6084/m9.figshare.4479803.v2`
- numeric target: electronic supplementary **Table S2**

The paper states that at each site five pollinator individuals per species were measured, or all individuals when fewer than five were available, and that mean proboscis length was calculated per species × site.

The Dryad landing page exposes `primary_data.xlsx`, but direct workbook retrieval returns HTTP 403 in the current execution environment. This is an acquisition block, not evidence that the data are absent.

## Why functional bins are insufficient

The 2017 source also classifies pollinators as:

- short-tongued: `< 4.5 mm`
- medium-tongued: `4.5–9 mm`
- long-tongued: `> 9 mm`

Those bins are biologically useful but cannot reconstruct the Izu FDQ distance matrix. FDQ uses pairwise **numeric** proboscis-length distances, so assigning a group midpoint would add invented information.

Primary analysis therefore prohibits:

- group-midpoint imputation;
- family-level mean substitution;
- body-size allometry used as if source-native;
- inferred values from taxonomic/guild labels;
- choosing a trait estimate after examining SVD, dependency or reproductive outcomes.

## Join rule after Table S2 recovery

The first join key is:

```text
exact pollinator taxon name × exact site
```

because the original source reports site-specific mean proboscis lengths.

A taxon-only mean across sites is not automatically substituted. If a future transfer rule is needed, it must be declared prospectively and sensitivity-tested separately.

The two-species difference between the paper count (211) and current named table (209) must be resolved by source identity, not fuzzy matching.

## Issue #91 field rule

The existing field experiment does not change. Visitor observations should preserve taxon identity and link to:

`templates/field_pollinator_trait_lookup_template.csv`

Allowed trait states are:

- `source_exact_site` — exact source taxon × site value;
- `source_transfer_prespecified` — a separately justified source transfer rule;
- `measured_new` — new direct measurement with measurement `n` and provenance;
- `trait_missing` — no defensible numeric trait yet.

`trait_missing` rows stay missing. They are not given family/guild midpoint values just to make FDQ calculable.

## Turn-opening condition

FDQ reconstruction from source-native traits opens only after:

1. numeric Table S2 values are lawfully recovered;
2. source bytes/rows and checksums are frozen;
3. exact taxon × site mapping to the 2024 visitor table is audited;
4. the 211-versus-209 discrepancy is resolved or retained explicitly;
5. missing-trait handling is declared before examining downstream dependency/SVD results.

Until then the scientific state is `blocked_until_source_native_proboscis_values_recovered`.
