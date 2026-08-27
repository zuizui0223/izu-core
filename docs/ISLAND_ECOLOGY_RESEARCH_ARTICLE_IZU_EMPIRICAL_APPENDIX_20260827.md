# Empirical Appendix — Izu source-state matching triangulation

**Companion to:** `docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md`  
**Role:** focal secondary analysis; not validation of synthetic thresholds  
**Updated:** 2026-08-27

## A1. Source lock and eligibility

The Izu analysis uses two source-defined datasets from the same coastal plant–pollinator network system.

- Pollinator functional traits: Hiraiwa & Ushimaru (2017), DOI `10.1098/rspb.2016.2218`; recovered supplementary Figshare file id `7336688`; PDF SHA256 `0386acd110c53a8b089aa79325a6f7889e8176c804bdd2a7ebfa104e972abe8e`.
- Plant tube length and species-level trait matching: Hiraiwa & Ushimaru (2024) source archive, DOI `10.6084/m9.figshare.25025000.v1`.

Of 209 named pollinator taxa in the 2024 archive, 202 (96.65%) receive a safe numeric proboscis join by exact name or whitespace-only normalization. No fuzzy, family, guild, body-size or functional-bin midpoint substitution is used. Among safely joined taxa, all 532 positive taxon × site presences agree between the 2017 and 2024 sources.

The source mapping was frozen before the target fit in commit `646f5236fca6144ce73a69ac3fe81b2d825afe17`. The primary source regime is the three study-defined continental sites pooled by all source-recorded visits. Its visit-weighted pollinator functional centre is `7.326653919694071 mm`.

For each eligible plant:

```text
initial_signed_position_mm = continental_source_tube_mean - continental_pollinator_center
```

Thirty plant species occur in the continental source and at least one Izu island. Their frozen positions span `-7.32665` to `+19.38001 mm`.

For each island:

```text
center_shift_mm = island_pollinator_center - continental_pollinator_center
predicted_matching_change_mm
  = abs(initial_signed_position_mm)
    - abs(initial_signed_position_mm - center_shift_mm)
```

The primary raw model is

```text
delta_TM_sp ~ predicted_matching_change_mm + island fixed effects
```

with plant-cluster-robust inference. No reproductive outcome is used to select or tune the mapping.

## A2. Raw realized matching result

The frozen projection uses 83 plant × island-site rows, 30 plant clusters and five Izu islands.

- slope `+0.566904`
- cluster-robust SE `0.131615`
- 95% CI `+0.297722 .. +0.836087`
- Pearson `r = 0.5701`
- Spearman `rho = 0.5269`
- sign concordance `63/83 = 75.9%`
- all five leave-one-island slopes positive

A 10,000-draw permutation of plant source positions gives `0/10,000` null slopes at least as large as the observed slope; empirical one-sided probability is `1/10001`. Correct source plant identity therefore matters for the raw association.

A sensitivity replacing Table S2 values only for the five taxa with explicitly reported site-specific Table S4 means yields an essentially unchanged slope (`+0.565909`).

The prespecified Oshima-source sensitivity is not supported (`slope +0.280825`, 95% CI `-0.39798 .. +0.95963`, sign concordance `48.4%`). Source regime is therefore not interchangeable.

## A3. Structural attacks

The raw result does not uniquely identify a pollinator-centre mechanism.

### A3.1 Island-centre assignment

All `5! = 120` assignments of the five observed island centre shifts were enumerated while plant starting positions and target responses were held fixed.

- observed assignment slope `+0.566904`
- assignment range `+0.413293 .. +0.607778`
- `13/120` assignments are at least as large as observed

The broad directional shift in community functional composition is better supported than the exact five centre magnitudes/order.

### A3.2 Source-position-only comparator

On the same rows and island fixed effects:

```text
delta_TM_sp_raw ~ initial_signed_position + island fixed effects
```

has `R² = 0.409056`, AIC `362.109`, whereas the full centre-shift geometry has `R² = 0.364938`, AIC `368.085`.

The strongest raw information therefore resides in source floral state plus broad community composition; precise island-centre geometry does not add clear identification.

### A3.3 Background-community-corrected matching

Hiraiwa & Ushimaru (2024) use a 10,000-randomization null preserving interaction-matrix marginal sums and infer from the corrected species-level matching response `TM_sp_z`. Applying the exact same frozen predictor to this stricter target gives:

- slope `+0.033285`
- cluster-robust SE `0.147315`
- 95% CI `-0.268008 .. +0.334578`
- two-sided `p = 0.822831`
- Pearson `r = 0.0609`
- Spearman `rho = 0.0991`
- sign concordance `42/83 = 50.6%`
- plant-position permutation one-sided `p = 0.391861`

The frozen projection therefore does not explain non-random matching beyond the source paper's background-community null.

## A4. Inference boundary

Supported:

> Source floral starting state and broad pollinator-community composition organize realized raw functional matching across Izu.

Not supported:

- unique island-specific centre magnitudes/order;
- plant-specific partner-weighted functional centres;
- non-random partner sorting beyond background community composition;
- historical Bombus loss as the cause;
- causal floral evolution;
- propagation from signed position to single-visit pollen deposition, fruit or mature seed;
- independent held-out validation;
- validation or calibration of the synthetic Chapter 2 `[0,1]` coordinate.

The decisive prospective gate remains:

```text
visitor identity + exact/new proboscis + plant-specific visitor weights
  -> frozen plant-specific signed position
  -> single-visit pollen deposition
  -> direct reproductive dependency / mature seed outcome
```

## A5. Reproducibility files

- `data/design/izu_pollinator_proboscis_recovery_status.json`
- `data/design/izu_signed_position_source_gate_20260827.json`
- `docs/IZU_POLLINATOR_PROBOSCIS_RECOVERY.md`
- `docs/IZU_SIGNED_POSITION_TRIANGULATION_20260827.md`
- `docs/IZU_SIGNED_POSITION_STRUCTURAL_AUDIT_20260827.md`
- `scripts/analyze_izu_signed_position_triangulation.py`
- `scripts/audit_izu_signed_position_table_s4_sensitivity.py`
- `scripts/audit_izu_signed_position_structural_independence.py`
- `scripts/recover_hiraiwa_ushimaru_2017_supplement.py`
- `scripts/recover_hiraiwa_ushimaru_2017_dryad_file.py`
