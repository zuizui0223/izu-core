# Izu source-native signed-position triangulation — 2026-08-27

## Current state

The previously blocked Izu signed-position route is now partially open at the **community functional-center** level.

The source-native pollinator trait table was recovered from Hiraiwa & Ushimaru (2017) supplementary Table S2 before the target fit. The mapping was then frozen in commit `646f5236fca6144ce73a69ac3fe81b2d825afe17` before `TM_sp` response coefficients were estimated.

This is same-network mechanistic triangulation, not independent validation.

## Source recovery

2017 supplement:

- DOI: `10.1098/rspb.2016.2218`
- Figshare file id: `7336688`
- source PDF SHA256: `0386acd110c53a8b089aa79325a6f7889e8176c804bdd2a7ebfa104e972abe8e`
- Table S2: 211 pollinator species
- total source-recorded visits: 6,257
- proboscis range: 0.1–32.8 mm

The 2024 source-native network archive has 209 named pollinator taxa. Under the fail-closed name rule, 202/209 taxa are safely linked to 2017 numeric proboscis values using exact names or whitespace-only normalization. Seven current taxa remain unresolved; no fuzzy, family, guild, body-size or midpoint substitution is used.

For the 202 shared taxa, aggregation over the 2024 pollinator species × site × season table gives **532/532 identical site presences** relative to positive Table S2 site-visit cells, with zero presence discordances. This confirms that the recovered trait table and the 2024 archive refer to the same underlying eight-site pollinator system for the safely joined taxa.

## Frozen community centers

Visit-weighted mean proboscis length from Table S2:

| site | visits | center (mm) |
|---|---:|---:|
| Hitachi | 620 | 5.76435 |
| Hitachinaka | 820 | 6.51841 |
| Tateyama | 1,175 | 8.71506 |
| Oshima | 697 | 4.33300 |
| Niijima | 774 | 5.04457 |
| Kozu | 709 | 6.07348 |
| Miyake | 881 | 5.16266 |
| Hachijo | 581 | 2.73838 |

The **primary source regime** was frozen before the target fit as the pooled three continental sites:

```text
continental center = 7.326653919694071 mm
```

This uses all 2,615 source-recorded continental visits and avoids selecting one mainland site after inspecting the target.

Oshima (`4.332998565279771 mm`) was retained only as the already-predeclared bridge-state sensitivity.

## Frozen predictor

For plants present at at least one continental site and at least one Izu island:

```text
source_tube_mm = equal-weight mean of unique continental plant × site tube means
initial_signed_position_mm = source_tube_mm - continental_center_mm
island_center_shift_mm = island_center_mm - continental_center_mm
predicted_matching_change_mm
  = abs(initial_signed_position_mm)
    - abs(initial_signed_position_mm - island_center_shift_mm)
```

Thirty plant species are eligible. Their initial positions span `-7.32665` to `+19.38001 mm` (20 negative, 10 positive), so the empirical mapping covers both sides of the source functional center.

## Target

The target is upstream species-level trait matching, not reproduction:

```text
delta_TM_sp
  = mean island-site TM_sp across available seasons
    - equal-weight continental plant-site TM_sp mean
```

`TM_sp` is the source-native negative interaction-frequency-weighted absolute proboscis–tube mismatch; higher values indicate better realized matching.

Primary frozen model:

```text
delta_TM_sp ~ predicted_matching_change_mm + island fixed effects
```

Inference uses plant-cluster-robust standard errors.

## Materialized run

Dedicated workflow:

- run `33039478288`
- validated head `f9c3d25b8003d4be95b0b195bbca8312e264adf4`
- artifact `izu-signed-position-triangulation-33039478288`
- artifact id `9633297259`
- digest `sha256:2fb746789640aba09c364740dd248f09ab457cd51d894d99de41db6d6f554e95`

The workflow reacquired the frozen 2024 Figshare files, recovered and byte-checked the 2017 supplement, passed four synthetic tests, ran the frozen target fit and uploaded the result artifact.

## Primary mainland-source result

- 83 plant × island-site rows
- 30 plant clusters
- 5 islands
- slope: **+0.566904**
- plant-cluster robust SE: **0.131615**
- 95% CI: **+0.29772 to +0.83609**
- one-sided positive p: **8.64 × 10^-5**
- Pearson `r = 0.5701`
- Spearman `rho = 0.5269`
- predicted/observed sign concordance: **63/83 = 75.9%**; one-sided binomial `p = 1.22 × 10^-6`

Leave-one-island-out primary slopes:

- omit Hachijo: `+0.5161`
- omit Kozu: `+0.5749`
- omit Miyake: `+0.5634`
- omit Niijima: `+0.4919`
- omit Oshima: `+0.6971`

All five remain positive; the slope range is `+0.4919` to `+0.6971`.

### Reading

With the study-defined continental source as baseline, the response expected from **initial signed tube position × community functional-center shift** tracks the observed change in realized plant-level trait matching across Izu islands.

This is the first source-native Izu result that keeps the sign of plant position instead of replacing it with unsigned TM/FDQ summaries.

## Prespecified Oshima bridge sensitivity

Oshima was not substituted as primary after the result.

Among plants present on Oshima and at least one post-Oshima island:

- 62 plant × island-site rows
- 22 plant clusters
- 4 target islands
- slope: `+0.280825`
- cluster robust SE: `0.326408`
- 95% CI: `-0.39798 to +0.95963`
- one-sided positive p: `0.1997`
- sign concordance: `30/62 = 48.4%`
- one leave-one-island slope is slightly negative (`-0.00073`)

Therefore the Oshima-source projection is **not supported**.

## Integrated decision

```text
mainland_source_projection_supported
+
oshima_bridge_projection_not_supported
```

The source regime is therefore not interchangeable. The result supports a conditional source-state interpretation rather than a universal trait coordinate with any nearby island as an equivalent baseline.

This matches the direction of the `island` Chapter 1 source-pool work: source definition and region-specific lineage assembly matter before a pollination mechanism is assigned.

## Dryad plant × pollinator weight status

The legacy Dryad metadata are now fully resolved:

- dataset version: `11003`
- file id: `45693`
- path: `primary_data.xlsx`
- size: `93,457` bytes
- MD5: `bec80ba4f3929517af0ca711bd5b1cb0`
- description: plant–pollinator interaction data used in the analysis

Anonymous metadata are public, but the exact individual-file API route remains HTTP 401 and public file-stream routes remain HTTP 403 in the current runner environment.

Therefore a **plant-specific partner-weighted functional center** is still not reconstructed. The current result uses a prespecified community-level source center, which was explicitly allowed by the existing v12 empirical gate as a separate estimand.

## Claim boundary

Supported:

- source-native numeric proboscis data are recovered;
- safe numeric coverage is 202/209 current named pollinator taxa without proxy filling;
- continental-source signed position plus community center shift predicts same-network `TM_sp` response;
- the primary result is distributed across all five Izu islands;
- Oshima is not an equivalent source baseline under the predeclared sensitivity.

Not supported:

- historical Bombus loss as the cause;
- a plant-specific partner-center mechanism;
- independent held-out validation;
- causal floral evolution;
- reproductive or seed-output branching from signed position;
- use of Oshima as a universal bridge source;
- replacement of the prospective Issue #91 effective-service/dependency field gate.

## Next empirical gate

Do **not** retune this projection.

The next decisive Izu step is prospective:

```text
new field plant / visitor identity
  -> directly measured or source-exact proboscis
  -> plant-specific realized visitor weights
  -> source-frozen signed position
  -> single-visit pollen deposition
  -> direct reproductive dependency
```

That test can separate community-center geometry from plant-specific partner context and can finally test whether the signed-position branch propagates into effective service and reproduction.
