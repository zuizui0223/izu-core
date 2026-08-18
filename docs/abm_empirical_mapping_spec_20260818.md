# Empirical-to-ABM mapping specification — 2026-08-18

## Purpose

Predeclare how source-native empirical quantities may constrain the v1 mechanism model before any island system is used for calibration. This prevents post-hoc hand tuning to recover a preferred architecture.

## Mapping table

| ABM quantity | admissible empirical proxy | current evidence examples | calibration status |
|---|---|---|---|
| partner-pool size | effective pollinator richness or functional-group richness measured in the same system | Hiraiwa network richness; Traveset network richness; Wanshan–Yongxing visitor richness | range calibration allowed |
| trait dispersion | pollinator functional diversity / functional evenness or source-native matching-trait dispersion | Hiraiwa functional diversity | range calibration allowed where source-native |
| interaction breadth / generalist fraction | plant or pollinator specialization index, niche breadth, realized visitor breadth | Caribbean Gesneriaceae specialization; island network specialization metrics | transformation must be declared before fitting |
| replacement fraction | fraction of effective interactions or visits supplied by introduced / novel partners | Hawaii introduced visitor share; Ogasawara honeybee replacement | direct range calibration possible in matched systems |
| reproductive-assurance capacity | autonomous fruit/seed set, autofertility index, or bagged/open comparison | Caribbean autofertility; Izu breeding-system evidence | range calibration allowed; do not equate different estimands numerically |
| partner arrival | colonization / immigration opportunity proxy | island isolation, observed turnover, restoration/reintroduction histories | **not directly calibrated in v1** |
| partner loss | experimentally/temporally observed functional loss or extinction probability | New Zealand functional extinction; disturbance histories | **not directly calibrated in v1** |
| plant matching trait | source-native floral trait linked to visitor matching | tube length / visitor proboscis or equivalent matched trait | system-specific mapping required |
| reproduction | source-native fruit set, seed set, pollen deposition or compatible reproductive endpoint | Hiraiwa pollination success; Seychelles/Canary reproductive outcomes | validation target, never an input and output simultaneously |

## Non-equivalence rules

1. Species richness and functional diversity are not interchangeable.
2. Visitor frequency is not automatically pollinator effectiveness.
3. Autofertility, self-compatibility and realized selfing rate are distinct.
4. Introduced visitor frequency is not automatically effective replacement.
5. Fruit set, seed set and pollen deposition remain different reproductive endpoints.
6. Network specialization metrics from different definitions may be used as ordinal/range constraints only unless mathematically harmonized.

## Calibration sequence

1. Freeze the empirical system and source version.
2. Register which model parameters are informed by that system.
3. Translate empirical measurements only to broad parameter ranges, not exact point estimates, unless the mapping is direct.
4. Fit/calibrate on a designated training subset only.
5. Keep at least one geographically independent island system held out.
6. Predict held-out architecture class and reproductive-performance direction before inspecting the held-out outcome.

## First held-out design

The first useful test should avoid using Izu for both parameterization and validation because Izu currently supplies the strongest full pathway.

Preferred sequence:

- **training constraints:** global network geography + Caribbean architecture/breeding evidence + one replacement system;
- **held-out full pathway:** Izu / Hiraiwa, testing whether the model predicts lower matching/function under stronger opportunity constraint without Izu-specific tuning;
- **secondary held-out architecture classes:** Canary, Galápagos, Seychelles, Hawaii, Ogasawara.

The reverse split should also be run as a sensitivity check when enough source-native mappings are available.

## Failure criterion

The mechanism is not supported merely because some parameter combination reproduces each empirical system. A useful model must recover multiple held-out architecture/function patterns from common process rules and source-constrained parameter ranges. If each system requires separate hand-tuned rules or architecture-specific parameters, the proposed common mechanism fails.
