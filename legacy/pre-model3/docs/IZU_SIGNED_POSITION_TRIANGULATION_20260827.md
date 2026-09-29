# Izu source-native signed-position triangulation — 2026-08-27

## Current state

The previously blocked Izu signed-position route is now partially open at the **community functional-center** level.

The 2017 supplementary source was recovered before the target fit. The primary mapping was then frozen in commit `646f5236fca6144ce73a69ac3fe81b2d825afe17` before any new `TM_sp` response coefficient was estimated.

This is same-network mechanistic triangulation, not independent validation.

## Source recovery

2017 supplement:

- DOI: `10.1098/rspb.2016.2218`
- Figshare file id: `7336688`
- source PDF SHA256: `0386acd110c53a8b089aa79325a6f7889e8176c804bdd2a7ebfa104e972abe8e`
- Table S2: 211 pollinator species
- total source-recorded visits: 6,257
- reported species-level proboscis range: 0.1–32.8 mm

The 2024 source-native network archive has 209 named pollinator taxa. Under the fail-closed name rule, 202/209 taxa are safely linked to Table S2 using exact names or whitespace-only normalization. Seven current taxa remain unresolved; no fuzzy, family, guild, body-size or midpoint substitution is used.

For the 202 safely shared taxa, aggregation over the 2024 pollinator species × site × season table gives **532/532 identical site presences** relative to positive Table S2 visit cells, with zero presence discordances. This confirms that the recovered 2017 source and the 2024 archive refer to the same underlying eight-site pollinator system for those taxa.

### Important trait-resolution boundary

The original field protocol measured pollinator proboscis at each site and calculated species × site means. But Table S2 exposes one numeric proboscis value per species plus site-specific visit counts. The primary center therefore uses a **prospectively frozen transfer of the Table S2 species-level reported value across sites**, not a claim that Table S2 is a complete site-exact numeric matrix.

Table S4 explicitly supplies site-specific numeric values for five pollinator taxa whose functional-group classification changes among sites. A separate post-target sensitivity corrects those five cases only.

## Frozen community centers

Primary Table S2 species-mean-transfer centers:

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

The **primary source regime** was frozen as the pooled three continental sites:

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

Thirty plant species are eligible. Their initial positions span `-7.32665` to `+19.38001 mm` (20 negative, 10 positive), so both sides of the frozen source center are represented.

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

## Materialized primary run

Dedicated workflow:

- run `33039478288`
- validated head `f9c3d25b8003d4be95b0b195bbca8312e264adf4`
- artifact `izu-signed-position-triangulation-33039478288`
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

Leave-one-island-out slopes:

- omit Hachijo: `+0.5161`
- omit Kozu: `+0.5749`
- omit Miyake: `+0.5634`
- omit Niijima: `+0.4919`
- omit Oshima: `+0.6971`

All five remain positive.

### Reading

With the study-defined continental source as baseline, the response expected from **initial signed tube position × community functional-center shift** tracks the observed change in realized plant-level trait matching across Izu islands.

This is the first Izu result in the repository that preserves the side of the functional center instead of replacing position with an unsigned matching/FDQ summary.

## Table S4 partial site-value correction

After the primary result was frozen, run `33039695653` added a sensitivity that changes only the five pollinator taxa for which Table S4 explicitly reports site-specific numeric proboscis means.

- artifact: `izu-signed-position-triangulation-33039695653`
- artifact id: `9633374987`
- digest: `sha256:627abed63e957dc1c1c0c1c6dff628f46b5677bb37dbeefe8ee50db774a056e9`
- corrected continental center: `7.3297896749522 mm`
- corrected primary slope: **+0.565909**
- cluster robust SE: **0.131472**
- one-sided p: **8.70 × 10^-5**
- sign concordance: **63/83**
- leave-one-island slopes: **+0.4910 to +0.6969**, all positive

Thus the primary result is not generated by leaving those five explicitly site-variable taxa at their Table S2 species-level values.

This sensitivity still does **not** create a complete site-exact numeric proboscis matrix for the remaining taxa.

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

The source regime is not interchangeable. This supports a conditional source-state interpretation rather than a universal trait coordinate for which any nearby island can be substituted as the starting environment.

That connects directly to the `island` Chapter 1 result: source-pool and regional lineage assembly must be resolved before assigning a pollination mechanism.

## Dryad plant × pollinator weight status

The legacy Dryad metadata are now fully resolved:

- dataset version: `11003`
- file id: `45693`
- path: `primary_data.xlsx`
- size: `93,457` bytes
- MD5: `bec80ba4f3929517af0ca711bd5b1cb0`
- description: plant–pollinator interaction data used in the analysis

Anonymous metadata are public, but the exact individual-file API route remains HTTP 401 and public file-stream routes remain HTTP 403 in the current runner environment.

Therefore a **plant-specific partner-weighted functional center** is still not reconstructed. The present result uses the separately frozen community-center transfer estimand.

## Claim boundary

Supported:

- Table S2 source-native species-level numeric proboscis data are recovered;
- 202/209 current named taxa can be safely linked without proxy filling;
- a prospectively frozen Table S2 species-mean community-center transfer gives a positive continental-source signed-position projection;
- the result is distributed across all five Izu islands;
- correcting the five Table S4 site-specific numeric taxa leaves the result essentially unchanged;
- Oshima is not an equivalent source baseline under the predeclared sensitivity.

Not supported:

- a complete site-exact numeric proboscis matrix for all taxa;
- historical Bombus loss as the cause;
- a plant-specific partner-center mechanism;
- independent held-out validation;
- causal floral evolution;
- reproductive or seed-output branching from signed position;
- use of Oshima as a universal bridge source;
- replacement of the prospective Issue #91 effective-service/dependency field gate.

## Next empirical gate

Do **not** retune this projection.

The decisive next Izu step is prospective:

```text
new field plant / visitor identity
  -> source-exact or newly measured proboscis
  -> plant-specific realized visitor weights
  -> source-frozen signed position
  -> single-visit pollen deposition
  -> direct reproductive dependency
```

That test can separate community-center geometry from plant-specific partner context and can test whether the signed-position branch propagates into effective service and reproduction.
