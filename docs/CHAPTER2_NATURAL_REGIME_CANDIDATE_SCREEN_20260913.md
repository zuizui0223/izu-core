# Natural breadth–synchrony regime candidate screen — 2026-09-14

Status: **source-structure screen under the frozen admission gate; Hawaii admission is closed before any natural `(D1, phi)` coordinate is opened.**

Governing gate: `data/design/chapter2_natural_regime_admission_gate_20260913.json`.  
Coordinate implementation: `data/design/chapter2_natural_regime_analysis_plan_20260913.json`.

A source is not admitted because a paper reports synchrony, richness or repeated sampling. The public bytes must reconstruct a quantitative time × partner matrix with source-native or explicitly normalizable effort. Candidate status is decided without inspecting eventual coordinate values.

## Priority extraction set

| Source / system | Temporal structure | Public/raw verification | Frozen-gate status | NEE counting role |
|---|---:|---|---|---|
| **Aslan et al. 2019, Hawaii Island** | 58 source dates reconstructed from 3,551 unique scan events across eight focal-plant sampling sheets | exact Dryad workbook re-acquired; SHA256 matches prior source lock; scan effort is directly reconstructible | **ADMITTED_ONE_SYSTEM_FOR_COORDINATES** | 1 source / 1 archipelago / **1 system** |
| Kaiser-Bunbury et al. 2017, Mahé | 8 monthly networks at each of 8 communities | 64 site × month network rows verified; partner-level primary/source-equivalent matrix bytes still required | **SCHEMA_PASS__PRIMARY_RAW_TRANSPORT_PENDING** | up to 8 systems if raw partner matrices pass |
| Lázaro et al. 2022, Mallorca | 7 source-native sampling days at each of 20 communities | Dryad workbook public; daily quantitative partner matrix still must be reconstructed from bytes | **DESIGN_PASS__RAW_DAILY_MATRIX_STRUCTURE_PENDING** | up to 20 systems if raw structure passes |
| Lara-Romero et al. 2019, Tenerife | 57 observation days at 4 fixed sites | standardized 15-min censuses described; public package still must expose date-level visitor rows | **HIGH_PRIORITY_PENDING_RAW_DATE_STRUCTURE** | up to 4 systems if raw structure passes |
| Alameda et al. 2025, Cuba | 12 monthly matrices described | reconstructible machine-readable monthly matrices not recovered | **FAIL_ONLY_DERIVED_OR_AGGREGATED_PUBLIC** | excluded unless pre-hard-stop raw bytes are located |
| Zackenberg 1996/1997 | 24/26 observation days | surfaced repeated-network material does not establish the frozen quantitative count/rate + effort contract | **FAIL_NONQUANTITATIVE_OR_INFERRED_LINK_PRESENCE** | excluded |

## Hawaii admission — corrected system unit

The Hawaii workbook contains eight focal-plant sheets, but those sheets are **sampling strata within one Pohakuloa high-elevation dryland ecosystem**, not eight independent natural-regime systems. The raw `Site` column is a free-text within-ecosystem location descriptor with many spelling/location variants and is not converted post hoc into independent site identities.

The admitted system is therefore:

```text
source_study_id = aslan_etal_2019_hawaii_native_pollination
archipelago_id = hawaiian_islands
system_id = pohakuloa_high_elevation_dryland_pollination_community
admitted systems = 1
```

The exact source workbook is `579,979` bytes with SHA256 `2b0ff40226b2a6d511a111ead8a00660532de3d799aed217e4dc30f00c2b3c27`, matching the pre-existing source lock.

The source-native adapter is frozen in `scripts/adapt_hawaii_native_pollination_regime.py` and its admission record in `data/design/chapter2_hawaii_natural_regime_admission_20260914.json`. It uses:

- `Date` as the source-native time bin, without outcome-dependent merging or splitting;
- `Scan visitor spp` as partner identity after whitespace/case normalization only;
- `Scan # Inds` as the quantitative numerator;
- unique scan events, keyed by focal sheet × raw Site × Date × Start Time × Observer × Scan block start, as effort;
- structural zeros for partners absent from an observed date;
- no imputation for the two rows with identifiable scan visitor but missing `Scan # Inds`; those numerator records are excluded while their scan events remain in effort.

Before opening any regime coordinate, the resulting structure has **58 time bins**, **3,551 unique scan events**, **96 raw partner labels**, and **96 nonconstant effort-standardized partner series**. The frozen minimum is 6 time bins and 3 nonconstant partner series, so Hawaii passes the admission gate as one system.

This corrects the earlier provisional idea that the eight focal-plant sheets could contribute eight systems. Counting them separately would violate the frozen `site_or_source_native_local_community` unit and inflate the NEE denominator.

## Remaining priority sources

### Mahé

The source design is ideal: eight local communities measured over eight months, and the source advertises raw visits plus an effort-standardized visitation representation. The repository has already recovered the 64 network-level site × month summary, but that object does not contain the partner-level time × partner matrix required for `D1` and `phi`. Mahé remains pending until the primary or source-equivalent partner matrix bytes are recovered.

### Mallorca

The study directly targets temporal stability and synchrony across 20 communities and has seven standardized sampling days per community. This is the highest-value next extraction because one admitted source could supply twenty independently located systems. Admission requires the Dryad workbook to expose day-level quantitative partner observations rather than only derived stability summaries.

### Tenerife

Four fixed sites were sampled repeatedly across 57 observation days using standardized 15-minute censuses. The design comfortably exceeds the temporal floor. It remains pending only until the public package is shown to retain date/census and visitor identity in a reconstructible quantitative table.

## Additional candidates / exclusions

| Source / system | Status | Reason |
|---|---|---|
| Kent Island 2019/2022/2023 | `PENDING_EFFORT_NORMALIZATION` | event dates and partner IDs exist; date-specific exposure still must be normalized |
| Thousand Island Lake | `PENDING_PUBLIC_RAW_TEMPORAL_RECONSTRUCTION` | strong repeated design, but survey-level public matrix reconstruction is not yet established |
| Aride Island | `FAIL_LT6_TIME_BINS` | only 3 temporal matrices |
| Ogasawara | `FAIL_LT6_TIME_BINS` | only 3 seasonal bins |
| Yongxing / Paracel | `PENDING_RAW_MONTHLY_RECONSTRUCTION` | four published seasonal networks do not yet establish ≥6 source-native quantitative bins |
| Aegean/Cycladic repeated survey | `FAIL_LT6_TIME_BINS` | surfaced design has 3 rounds/site |
| CaraDonna Colorado | `CONTEXT_ONLY_NON_ISLAND` | processor validation only; does not count toward NEE promotion |
| Olito Canadian Rockies | `CONTEXT_ONLY_NON_ISLAND` | processor validation only; does not count toward NEE promotion |

## Feasibility checkpoint before coordinates open

Current formally admitted natural-regime evidence is **1 island system from 1 independent source and 1 archipelago**. Nothing else is credited until its raw data pass the same gate.

The next extraction order is now:

1. Mallorca — verify/reconstruct seven-day quantitative partner matrices;
2. Mahé — recover source-equivalent partner-level monthly matrices;
3. Tenerife — verify date-level visitor rows and census effort;
4. Kent Island / Thousand Island Lake only if one of the above fails.

The NEE route still requires at least 12 admitted systems from at least 3 independent sources and at least 2 archipelago groups, followed by the predeclared breadth dispersion, synchrony dispersion, two-dimensionality, interior occupancy and leave-one-source-out tests. No journal promotion decision is made from source counts alone.
