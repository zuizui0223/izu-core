# Natural breadth–synchrony regime candidate screen — 2026-09-14

Status: **source-structure screen under frozen admission gate; no natural `(D1, phi)` coordinates have been opened.**

Governing gate: `data/design/chapter2_natural_regime_admission_gate_20260913.json`.

This screen records only whether public source structure can support the frozen outcome-independent breadth/synchrony analysis. Candidate status is decided without inspecting eventual coordinate values. A source is not admitted merely because a paper reports synchrony, richness, or a repeated design: the public bytes must reconstruct the frozen time × partner input and its effort normalization.

## Priority extraction set

| Source / system | Island scope | Source-native temporal replication | Effort / quantitative structure | Public/raw verification | Frozen-gate status | Role |
|---|---|---:|---|---|---|---|
| Kaiser-Bunbury et al. 2017, Mahé | Seychelles, 8 inselberg communities | 8 monthly networks/site (64 total) | IWDB advertises raw `no.visits` and standardized `visitfreq = visits/flower/hour × floral abundance` | source page and schema verified; partner-level workbook bytes not yet recovered in the present extraction lane | **SCHEMA_PASS__PRIMARY_RAW_TRANSPORT_PENDING** | primary source 1 candidate |
| Lázaro et al. 2022, Mallorca | Mallorca, 20 communities | 7 source-native sampling days/site | repeated standardized sampling; synchrony is an original study quantity | Dryad workbook public; seven-day partner matrix has not yet been reconstructed from workbook bytes | **DESIGN_PASS__RAW_DAILY_MATRIX_STRUCTURE_PENDING** | primary source 2 candidate |
| Aslan et al. 2019, Hawaii Island dryland | Hawaii Island | 240 raw observation sessions across 8 focal-plant sheets; dates retained | raw source has Site, Date, Start Time, Observer and visitor identity; article total = 576.36 h | source-native Dryad workbook was previously acquired and SHA256-locked in this repository | **RAW_TEMPORAL_SCHEMA_CONFIRMED__EFFORT_NORMALIZATION_PENDING** | high-priority independent source |
| Lara-Romero et al. 2019, Tenerife | Tenerife, 4 fixed sites | 57 observation days across 2014–2015 | 15-min censuses; quantitative flower-visitor observations | public Dryad/Zenodo package exists; date-level raw structure inside package still to be demonstrated | **HIGH_PRIORITY_PENDING_RAW_DATE_STRUCTURE** | high-priority independent source |
| Alameda et al. 2025, Lomas de Galindo | Cuba, one community | study generated 12 monthly matrices | interaction frequencies | surfaced public appendices are aggregated/global or seasonal; 12 reconstructible monthly matrices have not been recovered | **FAIL_ONLY_DERIVED_OR_AGGREGATED_PUBLIC** | excluded unless pre-hard-stop raw bytes are located |
| Zackenberg 1996/1997 | Greenland | 24/26 observation days | public daily interaction material | available repeated matrices rely on link-presence/phenological reconstruction rather than a verified source-native quantitative count/rate series for this gate | **FAIL_NONQUANTITATIVE_OR_INFERRED_LINK_PRESENCE** | excluded |

## Additional candidates / exclusions

| Source / system | Replication | Status | Reason |
|---|---:|---|---|
| Kent Island 2019/2022/2023 | date-resolved event rows | **PENDING_EFFORT_NORMALIZATION** | public event dates and partner IDs exist, but date-specific observation effort is not yet shown to be equal or normalizable |
| Thousand Island Lake, China | 20 surveys/site over 3 years in study design | **PENDING_PUBLIC_RAW_TEMPORAL_RECONSTRUCTION** | field design is strong, but surfaced public packages do not yet establish reconstructible survey-level interaction matrices |
| Aride Island, Seychelles | 3 temporal matrices | **FAIL_LT6_TIME_BINS** | frozen floor is six aligned time bins |
| Ogasawara multi-island network | 3 seasonal bins | **FAIL_LT6_TIME_BINS** | frozen floor is six aligned time bins |
| Yongxing / Paracel seasonal networks | 4 published seasonal networks | **PENDING_RAW_MONTHLY_RECONSTRUCTION** | two monthly samplings per season are described, but six or more public source-native quantitative matrices have not been established |
| Aegean/Cycladic repeated network survey | 3 source-native rounds/site in the surfaced design | **FAIL_LT6_TIME_BINS** | spatial replication cannot substitute for the frozen within-system temporal floor |
| CaraDonna Colorado subalpine network | weekly repeated networks | **CONTEXT_ONLY_NON_ISLAND** | useful processor validation, excluded from NEE island promotion count by frozen source scope |
| Olito Canadian Rockies | 32 sampling days | **CONTEXT_ONLY_NON_ISLAND** | useful processor validation, excluded from NEE island promotion count |

## Evidence notes

### Mahé — biological/data schema passes; byte transport remains the gate

The Interaction Web Database source describes 64 monthly networks from eight isolated Mahé inselbergs, sampled from September 2012 through April 2013. It advertises raw visit matrices, a standardized `visitfreq` representation, flowering plants with zero visitors, floral abundance, site and month identifiers. This is exactly the right source design for the frozen coordinate analysis.

However, earlier work in this repository already encountered transport failure for the primary IWDB workbook. A secondary public mirror contains network-level Mahé summaries (`site`, `month`, nestedness, mean visits, mean visitation rate), but those summaries cannot replace the partner-level time × partner matrix. Therefore Mahé is not called admitted until the primary/source-equivalent partner matrix bytes are actually recovered and checked.

Source: Kaiser-Bunbury et al. 2017, *Nature*, DOI `10.1038/nature21071`; Interaction Web Database source definition; repository source contract `config/seychelles_restoration_network_iwdb_source.json`.

### Mallorca — design passes; raw daily reconstruction is the only remaining question

The Mallorca study sampled 20 communities repeatedly within the same year and was explicitly designed around temporal stability, portfolio effects and synchrony. Related source documentation specifies seven standardized sampling days per site. Dryad provides the study workbook and README.

That is sufficient to pass the design screen but not the extraction gate: the workbook still must expose partner identities and quantitative observations at the seven source-native days rather than only precomputed stability summaries. No coordinate is computed before that check.

Source: Lázaro et al. 2022; Dryad `10.5061/dryad.m905qfv2p` and related raw network package.

### Hawaii — source-native temporal schema is confirmed

This repository previously acquired the Aslan et al. Dryad workbook and locked the exact source bytes (`579979` bytes; SHA256 `2b0ff40226b2a6d511a111ead8a00660532de3d799aed217e4dc30f00c2b3c27`). The existing parser reads eight focal-plant sheets and uses `Site`, `Date`, `Start Time`, and `Observer` to identify observation sessions. It recovered 4,499 raw rows, 240 sessions, 1,799 focal visitor-event rows and 197 source-native visitor labels.

Thus public byte retrieval, dates, site identity and partner labels are not hypothetical: they were already demonstrated against the source-native workbook. The remaining admission question is narrower—whether session/time-bin exposure is equal by design or can be normalized from the workbook/README without using outcome information. Until that is proven, Hawaii remains pending rather than admitted.

Source: Aslan et al. 2019, DOI `10.1002/ajb2.1233`; Dryad `10.5061/dryad.tm575v4`; repository result `data/results/hawaii_native_pollination_summary.json`.

### Tenerife — newly promoted high-priority source

The Tenerife study used four fixed sites on El Teide, sampled through the flowering season in 2014 and 2015 over 57 observation days and 868 h. Source methods describe standardized 15-minute censuses of flower visitors. The public data package is therefore unusually promising for this gate because both temporal replication and per-census effort are source-defined.

Admission remains pending only because the current audit has not yet opened the public package to verify that date/census and visitor identity are retained in machine-readable raw form rather than collapsed to site-level matrices.

Source: Lara-Romero et al. 2019, Dryad `10.5061/dryad.b23v8nn` (public archive also mirrored on Zenodo).

### Cuba — excluded under the frozen public-data rule

The paper states that two observation days per month were combined into 12 monthly matrices, so the field design itself exceeds the six-bin floor. But the surfaced public supplementary layer does not currently provide those 12 quantitative matrices in reconstructible machine-readable form. Under the frozen gate, a design described in Methods is not enough. The system is excluded unless the pre-existing raw public file is located before the hard stop.

### Zackenberg — excluded from the quantitative coordinate analysis

Daily repeated networks are public, but the surfaced repeated-network construction is based on phenological/link-presence reconstruction rather than a verified source-native quantitative count/rate series aligned with the frozen `value / effort` contract. Presence reconstruction is useful for temporal network topology but is not silently converted into interaction intensity here.

## Feasibility checkpoint before coordinates open

The public-data route remains substantially more feasible than the old historical transition-validation programme, but **no NEE promotion count is credited yet**. Current evidence supports the following extraction order:

1. recover Mahé partner-level workbook bytes;
2. open Mallorca workbook and verify seven-day quantitative partner rows;
3. resolve Hawaii session effort from its already verified raw workbook/README;
4. open Tenerife raw package and verify date-level visitor rows;
5. use Kent Island / Thousand Island Lake only if one of the four priority sources fails.

The NEE route still requires at least 12 admitted island systems from at least 3 independent sources and 2 archipelago groups, plus the predeclared two-dimensional dispersion and leave-one-source-out criteria. No route criterion is considered met until the canonical processor produces the frozen coordinates.