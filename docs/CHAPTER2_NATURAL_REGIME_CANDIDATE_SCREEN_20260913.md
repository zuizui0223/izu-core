# Natural breadth–synchrony regime candidate screen — 2026-09-13

Status: **source-structure screen under frozen admission gate; no natural `(D1, phi)` coordinates have been computed.**

Governing gate: `data/design/chapter2_natural_regime_admission_gate_20260913.json`.

This screen records only whether public source structure can support the frozen outcome-independent breadth/synchrony analysis. It does not inspect or rank candidates by their eventual coordinate values.

## Priority extraction set

| Source / system | Island scope | Source-native temporal replication | Effort / quantitative structure | Public raw status | Frozen-gate status | Role |
|---|---|---:|---|---|---|---|
| Kaiser-Bunbury et al. 2017, Mahé | Seychelles, 8 inselberg communities | 8 monthly networks/site (64 total) | Public `visitfreq` matrix is standardized as visits/flower/hour × floral abundance | Interaction Web Database Excel files | **ADMIT_FOR_EXTRACTION** | primary source 1 |
| Lázaro et al. 2022, Mallorca | Mallorca, 20 communities | 7 sampling days/site (5 spring + 2 autumn) | source protocol uses repeated standardized sampling; synchrony was an original study quantity | Dryad `10.5061/dryad.m905qfv2p` | **PENDING_FILE_STRUCTURE_CONFIRMATION** | primary source 2 |
| Alameda et al. 2025, Lomas de Galindo | Cuba, one community | 12 monthly matrices, each pooling two consecutive sampling days | cell = interaction frequency; source-native monthly bins | journal article states 12 matrices are the basic dataset; machine-readable appendix retrieval not yet verified | **PENDING_MONTHLY_MATRIX_RETRIEVAL** | candidate source 3 |
| Aslan et al. 2019, Hawaii Island dryland | Hawaii Island | observations Mar 2015–May 2016 | 576.36 h systematic flower observations; raw workbook public | Dryad `10.5061/dryad.tm575v4` | **PENDING_DATE_AND_EFFORT_COLUMNS** | backup source 3+ |
| Zackenberg 1996/1997 | Greenland | 24/26 observed days; daily matrices public | daily plant–pollinator matrices; quantitative/count interpretation and tentative-date handling require source check | Dryad `10.5061/dryad.3pk73`, plus repeated-network archive `10.5061/dryad.mh0qs` | **PENDING_MEASUREMENT_INTERPRETATION** | backup source 3+ |

## Additional candidates / exclusions

| Source / system | Replication | Status | Reason |
|---|---:|---|---|
| Kent Island 2019/2022/2023 | date-resolved event rows | **PENDING_EFFORT_NORMALIZATION** | public event dates and partner IDs exist, but date-specific observation effort is not yet shown to be equal or normalizable |
| Thousand Island Lake, China | 20 surveys/site over 3 years in study design | **PENDING_PUBLIC_RAW_TEMPORAL_RECONSTRUCTION** | field design is excellent, but surfaced public packages do not yet establish reconstructible survey-level interaction matrices |
| Aride Island, Seychelles | 3 temporal matrices | **FAIL_LT6_TIME_BINS** | frozen floor is six aligned time bins |
| Ogasawara multi-island network | 3 seasonal bins | **FAIL_LT6_TIME_BINS** | frozen floor is six aligned time bins |
| Yongxing / Paracel seasonal networks | 4 published seasonal networks | **PENDING_RAW_MONTHLY_RECONSTRUCTION** | two monthly samplings per season are described, but six or more public source-native matrices have not yet been established |
| Cycladic/Aegean static network surveys | multiple sites/islands but no verified ≥6 bins/site | **FAIL_UNLESS_TEMPORAL_RAW_FOUND** | spatial replication cannot substitute for temporal replication within a system |
| CaraDonna Colorado subalpine network | weekly repeated networks | **CONTEXT_ONLY_NON_ISLAND** | useful processor validation, excluded from NEE island promotion count by frozen source scope |
| Olito Canadian Rockies | 32 sampling days | **CONTEXT_ONLY_NON_ISLAND** | useful processor validation, excluded from NEE island promotion count |

## Evidence notes

### Mahé — admitted for extraction

The Interaction Web Database describes 64 monthly networks from eight isolated Mahé inselbergs, sampled from September 2012 through April 2013. Its public tables include treatment, site, month, network ID, floral abundance and plant/pollinator matrices. The `64 networks_visitfreq` sheet contains a fully quantified standardized visitation measure (`visits / flower / hour × floral abundance`). This meets the frozen requirements for stable system identity, ≥6 aligned bins, reconstructible partner matrices and effort-normalizable quantitative interactions.

Source: Kaiser-Bunbury et al. 2017, *Nature*, DOI `10.1038/nature21071`; Interaction Web Database dataset page.

### Mallorca — strong pending

Dryad DOI `10.5061/dryad.m905qfv2p` publicly provides `Dryad_dataStability.xlsx` and a README for 20 Mallorca communities. The associated study was explicitly about within-year stability, portfolio effects and temporal synchrony of plants, pollinators and interactions. Source methods use repeated days within each site. Admission remains pending only until the public workbook is checked to confirm that the seven source-native days can be reconstructed as the time × partner matrix required by the frozen gate, rather than only as precomputed stability summaries.

### Cuba — strong third-source candidate

The Lomas de Galindo study monitored interactions for two days each month through one year. Its methods state that the two days of each month were combined into one monthly adjacency matrix, that cells contain interaction frequency and that **12 matrices compose the basic dataset**. The sampling design therefore passes the temporal floor. Admission is pending because machine-readable recovery of those 12 matrices from the public article/appendix surface has not yet been demonstrated.

Source: Alameda, Martínez-Adriano & Barro Cañamero 2025, *Journal of Pollination Ecology*, DOI `10.26786/1920-7603(2025)835`.

### Zackenberg — useful but not automatically admitted

Dryad DOI `10.5061/dryad.3pk73` explicitly provides daily matrices for 1996 and 1997. A second Dryad archive (`10.5061/dryad.mh0qs`) contains temporally replicated 1996, 1997, 2010 and 2011 interaction material. The source is not admitted yet because the analysis requires quantitative count/rate series and must avoid treating tentatively dated or interpolated link presence as observed interaction intensity.

## Feasibility checkpoint before coordinates open

The public-data route is already materially more feasible than the failed historical transition-validation programme because it asks only for repeated outcome-independent interaction context.

- Mahé alone contributes 8 admitted systems from one independent source.
- Mallorca can contribute up to 20 additional systems if its public workbook exposes the source-native daily matrices.
- The NEE promotion rule still requires a **third independent source study**; Cuba is currently the cleanest candidate, with Hawaii and Zackenberg as backups pending raw-structure checks.

No NEE promotion criterion is considered met until the canonical processor has generated the frozen coordinates and the source-balanced dispersion / leave-one-source-out rules have been evaluated.
