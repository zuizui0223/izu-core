# Izu pollinator proboscis-length recovery

## Current state

The 2017 source-native supplementary PDF is now recovered and byte-locked. Table S2 supplies a numeric species-level proboscis value for 211 pollinator taxa together with visit counts at the eight study sites.

The old `0 / 209` state is obsolete.

Current safe linkage to the 2024 network archive:

```text
2024 named visitor taxa = 209
2017 Table S2 taxa = 211
safe exact / whitespace-only joined current taxa = 202 / 209 = 96.65%
unresolved current taxa = 7
unresolved 2017 taxa = 9
shared joined taxon x site presences = 532 / 532 identical
```

No fuzzy, family, guild, body-size or midpoint value is used.

## Recovered source

- article DOI: `10.1098/rspb.2016.2218`
- supplementary collection: `10.6084/m9.figshare.c.3647738`
- recovered Figshare file id: `7336688`
- file name: `rspb20162218_si_001.pdf`
- SHA256: `0386acd110c53a8b089aa79325a6f7889e8176c804bdd2a7ebfa104e972abe8e`
- Table S2 pollinator species: 211
- Table S2 total visits: 6,257
- Table S2 proboscis range: 0.1–32.8 mm

Dedicated recovery run `33038243186` successfully recovered the source PDF. Later source-run `33038891807` also resolved the legacy Dryad metadata while confirming that the workbook bytes remain transport-blocked.

## Important measurement distinction

The original study measured pollinator proboscis length at each site and calculated species × site means. However, Table S2 exposes one numeric proboscis value per species plus site-specific visit counts; it is therefore treated here as a **source-reported species-level numeric value**, not silently relabelled as a complete site-specific numeric table.

Table S4 explicitly reports site-specific numeric means for five pollinator species whose functional-group assignment changes among sites. Those values are used only in a separate sensitivity that corrects the five reported cases.

Therefore two routes must remain distinct:

1. **community-center transfer estimand** — Table S2 species values may be combined with site-specific source visit counts under a rule frozen before the target fit;
2. **exact site-specific FDQ / plant-specific partner center** — remains blocked unless complete compatible site-level traits or direct new measurements are available.

## Frozen signed-position transfer

Before the target `TM_sp` fit, commit `646f5236fca6144ce73a69ac3fe81b2d825afe17` froze the following primary rule:

```text
source pollinator center
  = visit-weighted mean Table S2 species proboscis
    pooled across Hitachi + Hitachinaka + Tateyama
  = 7.326653919694071 mm

initial signed position
  = continental source tube mean - source pollinator center
```

This was prospective relative to the new signed-position target fit. It does not make the transferred species value site-exact.

A post-target Table S4 sensitivity replaces the Table S2 value with the explicitly reported site-specific numeric value for the five affected taxa only. The rest remain source-reported species-level values.

## Current signed-position result

Dedicated run `33039478288` passed source-byte reacquisition, source checks, four synthetic tests and the frozen target analysis.

Primary continental-source projection:

- 83 plant × island-site rows
- 30 plant species
- slope `+0.5669`, plant-cluster SE `0.1316`
- one-sided positive `p = 8.64e-5`
- sign concordance `63 / 83 = 75.9%`
- all five leave-one-island slopes positive

Prespecified Oshima bridge sensitivity is unsupported (`slope +0.2808`, one-sided `p = 0.200`).

See `docs/IZU_SIGNED_POSITION_TRIANGULATION_20260827.md` for the complete interpretation and claim ceiling.

## Dryad plant × pollinator weight status

The legacy workbook is now identified exactly from public metadata:

- dataset DOI: `10.5061/dryad.pm29d`
- dataset version id: `11003`
- file id: `45693`
- file: `primary_data.xlsx`
- size: 93,457 bytes
- MD5: `bec80ba4f3929517af0ca711bd5b1cb0`
- description: plant–pollinator interaction data used in the analysis

The current anonymous file routes remain blocked:

- exact file API download: HTTP 401
- public file-stream routes: HTTP 403

Thus plant-specific interaction weights have **not** been recovered from this workbook.

## Why functional bins remain insufficient

The 2017 source classifies pollinators as short (`<4.5 mm`), medium (`4.5–9 mm`) and long (`>9 mm`) tongued. These bins remain biologically useful but are not numeric substitutes for continuous proboscis distance.

Primary analyses continue to prohibit:

- group-midpoint imputation;
- family-level mean substitution;
- body-size allometry used as if source-native;
- inferred values from taxonomic/guild labels;
- fuzzy taxon joins chosen to increase coverage.

## Field rule

Issue #91 visitor observations should preserve taxon identity and link to `templates/field_pollinator_trait_lookup_template.csv`.

Allowed states remain:

- `source_exact_site`
- `source_transfer_prespecified`
- `measured_new`
- `trait_missing`

The 2017 Table S2 community-center route is a `source_transfer_prespecified` use. It must not be relabelled `source_exact_site`.

## Remaining decisive work

For the direct mechanism test:

```text
plant-specific visitor observations
  -> exact-source or newly measured proboscis
  -> plant-specific visitor weights
  -> signed plant position relative to the prespecified functional center
  -> single-visit pollen deposition
  -> reproductive dependency / mature seed outcome
```

This prospective field route is required to distinguish a community-center geometric correspondence from realized partner-specific effective service and downstream reproduction.
