# Global island geographic coverage audit — 2026-08-19

## Decision

The repository has broad inter-ocean coverage, but it is **not yet geographically even enough to describe the deep-dive evidence layer as a balanced global survey**.

Two different claims must remain separate:

1. **Global macroecology source coverage:** strong. Traveset et al. (2016) contains 52 quantitative networks spanning 41°S–82°N and 91°W–149°E, including 18 oceanic-island networks.
2. **Repository deep-dive mechanistic coverage:** broad but uneven. Existing source-locked systems overrepresent well-studied North Atlantic, western Indian Ocean, eastern/central Pacific and NW Pacific archipelagos.

## Current deep-dive coverage

| geographic sector | current repo examples | present depth |
|---|---|---|
| North Atlantic / Macaronesia | Canary Islands; Azores | network + reproductive-function examples |
| western Indian Ocean | Mauritius; Seychelles | network / single-visit effectiveness / breeding evidence |
| eastern tropical Pacific | Galápagos | multi-island network + effectiveness / morphology evidence |
| central North Pacific | Hawaii | replacement + bagging / reproductive-function evidence |
| NW Pacific | Izu; Ogasawara | functional diversity / matching / reproduction; replacement mismatch |
| western tropical Pacific / South China Sea | Wanshan–Yongxing | continental-vs-oceanic network comparison |
| SW Pacific temperate | New Zealand | functional-extinction natural experiment |
| Caribbean | insular vs mainland Gesneriaceae | pollination architecture + breeding-system comparison |

## Geographic gaps identified by targeted search

The following sectors were underrepresented in the repository deep-dive layer and must be recorded explicitly rather than silently treated as sampled:

- **SE Pacific:** Juan Fernández Islands. Published field work covers breeding systems / floral visitors for 25 endemic species and broader archipelago floral-trait surveys.
- **Southern Ocean / subantarctic:** published synthesis covers 321 species across 11 island groups at approximately 46–55°S.
- **South Atlantic:** St Helena / Ascension / Tristan da Cunha remain weak or absent for quantitative pollination-network evidence in the current repository search.
- **SW tropical Pacific:** Fiji / Samoa / New Caledonia remain weak in the current quantitative pollination-network deep-dive layer.
- **SW Indian Ocean beyond Mauritius/Seychelles:** Réunion / Madagascar are not yet represented as matched oceanic-island pollination-network gradient systems; Madagascar has flower-visitation-web literature but is a continental island and must not be pooled as an oceanic island.

## What “global” may mean in the repository

Allowed now:

> `global-source-supported directional pattern`

because the Traveset et al. macroecology dataset is genuinely world-wide and the repository has independent mechanistic examples from multiple ocean basins.

Not allowed yet:

> `geographically balanced global mechanistic replication`

because the deep-dive mechanistic systems are not evenly distributed across all oceanic-island regions and cold/subantarctic systems are sparse.

## Consequence for the ABM

The first continuous-gradient ABM target remains Traveset et al. (2016), because it supplies a standardized, world-wide quantitative-network frame rather than a hand-picked collection of famous archipelagos.

The ABM must therefore proceed in two stages:

1. **Directional recovery:** continuous isolation should recover the reported sign/shape of species richness, link richness, interaction diversity and plant niche overlap without fitting observed coefficients.
2. **Island-level recovery:** recover Tables S1–S3, map each of the 18 oceanic islands to its measured area / age / elevation / isolation and observed network metrics, then predict each island without island-specific tuning.

The second stage is the decisive test. Regional case studies remain external validation / falsification, not calibration targets for the 18-island curve.

## Admission rule for new regions

A new region enters the quantitative global-gradient validation only if it has:

- an identifiable oceanic-island unit;
- source-native island geography or isolation;
- a quantitative pollination-network metric comparable to the global dataset, or an explicitly separate reproductive-function endpoint;
- enough source metadata to distinguish sampling effort from biological richness.

Breeding-system-only or floral-trait-only studies are retained as independent biological-response validation but are not silently converted into network metrics.
