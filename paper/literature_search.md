# Systematic literature & data search record (PRISMA-style)

Auditable record of how Tier-1 (literature) and Tier-3 (occurrence) evidence was
gathered, so the meta-analysis is systematic, not cherry-picked. Searched to the
limit of accessible public sources (2026-07-03).

## Sources searched

- Web / scholarly search (English + Japanese) for Izu island–mainland floral
  trait and pollinator studies.
- GBIF occurrence API (per-island facets over the Izu envelope) — candidate pool.
- iNaturalist observation API — photo tier availability + phenology.

## Search strings (representative)

- "Izu Islands plant selfing evolution pollinator loss Campanula reproductive assurance"
- "island syndrome selfing rate evolution pollinator loss meta-analysis specialist generalist"
- "Izu Islands island mainland comparison floral trait pollinator Bombus loss"
- 伊豆諸島 送粉 花 島 本土 比較 マルハナバチ 訪花昆虫 自家和合性 / 固有種 形態
- "Ligustrum ovalifolium Izu island mainland flower corolla"

## Included studies (Tier-1)

| Taxon | Functional group | Direction (mainland→island) | Rank | Source |
|---|---|---|---|---|
| *Campanula microdonta* | specialist | corolla ↓, outcrossing ↓, selfing ↑ (step) | A | Inoue 1990 Plant Species Biol.; repo data |
| *Campanula punctata* | specialist | SI→SC (step at bumblebee loss) | B | Inoue 1986 Plant Species Biol. |
| *Ligustrum ovalifolium* | intermediate-tubular | corolla tube ↓, stamen ↓ (↑ with isolation) | B | Kato et al. 2014 Bot. J. Linn. Soc. 174:489 |
| *Chionographis japonica* | specialist | floral tube ↓ under bumblebee absence (Kōzu) | B | Suetsugu et al. 2024 New Phytol. (nph.19325) |
| *Lilium auratum* (Sakuyuri) | large-flower | flower **enlarged** (counter-direction) | B | Nakajima 2018 Plant Species Biol. 33 |
| *Rhododendron kaempferi* (Ōshima form) | large-flower | flower **enlarged** (counter-direction) | D | park/flora descriptions |
| *Clerodendrum izuinsulare* vs *trichotomum* | specialist | direction pending full text | B | Mizusawa et al. 2014 Plant Species Biol. 29 |

Three independent specialist/intermediate lineages (Campanula, Ligustrum,
Chionographis) show floral reduction; two large-flowered non-bee taxa enlarge —
the directional split predicted by the flower-size island rule.

## Excluded (with reason)

- *Prunus speciosa* (Ōshima cherry): **island origin**, later moved to the
  mainland — inverts the mainland→island polarity. Not a valid gradient case.
- Generalist floral series: **no peer-reviewed mainland↔island quantitative
  study found** despite targeted search → the generalist negative control cannot
  be populated from literature (see photo-tier ceiling).
- Occurrence-only species (bulk of the 156 pool): availability evidence, not a
  response data point (rank E).

## Related frameworks (context, not Izu data)

- Flower-size "island rule": Annals of Botany 2025 commentary (doi:10.1093/aob/mcaf053); bioRxiv 2023 "Flower size evolution in the Southwest Pacific".
- Pollinator-loss → rapid selfing-syndrome evolution: Evolution 2022; convergent selfing syndrome 2023.

## Completeness statement

Accessible literature was searched in both languages to the point of
diminishing returns; the binding limit is **paywalled full texts** (direction is
recoverable from abstracts; effect sizes often are not) and the **genuine
absence of generalist quantitative series**. The meta-analysis is therefore
complete as a *systematic, reproducibly-graded synthesis run to the public-data
ceiling*, with that ceiling documented here rather than hidden.
