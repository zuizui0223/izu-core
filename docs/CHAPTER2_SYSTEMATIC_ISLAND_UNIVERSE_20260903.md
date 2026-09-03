# Chapter 2 systematic island-universe audit

Updated: 2026-09-03

## Decision

Chapter 2 now separates three different objects:

1. the frozen **25-entry identifiability audit**;
2. the current **36-entry descriptive global confrontation**;
3. a new **systematic search universe** used to drive exhaustive source review without changing either earlier denominator.

The systematic search universe contains **110 named geographic targets across 8 macroregions**. The 110 targets are not an estimate of the number of island systems on Earth. They are a reproducible search frame covering named archipelagos, island groups and selected large/sentinel islands relevant to terrestrial flowering-plant pollination, breeding systems, reproductive assurance and plant-pollinator networks.

Machine-readable files:

- `data/design/chapter2_systematic_island_universe_v1_20260903.csv`
- `data/design/chapter2_systematic_first_wave_source_gate_20260903.csv`
- `data/design/chapter2_systematic_first_wave_dedup_review_20260903.csv`
- `scripts/audit_chapter2_systematic_island_universe.py`
- `data/results/chapter2_systematic_island_universe_audit_v1_20260903.json`

## Current coverage state

The seed universe contained:

- 110 geographic targets;
- 8 macroregions;
- 42 targets already resolved, source-covered or indexed by an umbrella source;
- 68 targets requiring further source work;
- 56 targets not yet directly source-gated;
- 7 targets with a relevant source already found but still requiring explicit source admission/de-duplication review;
- 5 nested targets requiring their own source gate.

The first-wave gate has now reviewed seven additional targets. After that gate:

- **49/110** targets are source-resolved, source-covered or umbrella-indexed;
- **61/110** still require additional source work;
- **55** remain directly ungated;
- only **1** of the original source-found rows remains ungated at the broad-target level (`Ryukyu Islands`; its Amami and Okinawa/Iriomote subtargets are now directly gated);
- all seven first-wave studies still fail the full Chapter 2 source-state → transition → local-realization → plant-response contract.

Six first-wave research entries are sufficiently direct to be **eligible for later breadth promotion after de-duplication review**. One, the Rodrigues *Ramosmania* breeding-system paper, is retained as a search record but not promoted because its core experiment is ex situ.

The high-priority seed search pool contains 37 rows. Priority is now worked down systematically rather than by convenience.

## Umbrella sources that change the search strategy

The programme is no longer driven only by one-paper-at-a-time discovery. Global or multi-archipelago sources are used as indexes and then expanded back to source-native sites.

### Global quantitative pollination networks

Traveset et al. (2016; DOI `10.1111/geb.12362`) compiled 52 quantitative plant-pollinator networks: 23 continental-island, 18 oceanic-island and 11 mainland networks. Supporting Information Table S1 identifies network sampling locations and Table S2 gives oceanic-island traits. This is an **index source**, not 41 independent island-system validation events.

Trøjelsgaard & Olesen (2013; DOI `10.1111/j.1466-8238.2012.00777.x`) compiled 54 community-wide pollination networks. Seventeen were island networks: four New Zealand, four Canarian, two Jamaican, one Dominican, one Mauritian, three Galápagos, one Azorean and one Amami/Japanese-island network. This is a second index for recovering historically used network sites and original references.

The Web of Life database is retained as a recovery route because it stores network identifiers, references, locations and interaction matrices. Database presence alone never promotes a target; the original source still must be checked.

### Southern Ocean

Lord (2015; DOI `10.1093/aobpla/plv095`) provides a comparative source across 11 Southern Ocean island groups and 321 flowering plant species: Crozet, Prince Edward/Marion, Snares, Kerguelen, Antipodes, Auckland, Falklands, Campbell, Heard/McDonald, South Georgia and Macquarie. It directly informs floral-trait and breeding-system breadth but not a matched historical community transition.

### Macaronesia and Caribbean

The Macaronesia review framework identifies Azores, Madeira, Selvagens, Canary Islands and Cabo Verde as the five main Macaronesian archipelagos. Current Chapter 2 evidence covers Azores, Madeira and Canary Islands; Selvagens and Cabo Verde remain explicit search targets.

Caribbean Gesneriaceae work spans Cuba, Hispaniola, Jamaica, Puerto Rico and the Lesser Antilles and is treated as an umbrella source. Individual island targets still require their own gate when a claim depends on a particular transition or local pollinator realization.

## First-wave source gate

Seven targets were inspected with the same channel-level gate used elsewhere in Chapter 2.

| Target | Direct information recovered | Full contract | Source-gate decision |
|---|---|---|---|
| Aegean Archipelago | 39 plant-pollinator networks on eight islands; richness and network structure across climate gradient | fail | eligible after de-dup review |
| Amami Islands | 164 flowering plants and 610 anthophilous insect species across vegetation types | fail | eligible after de-dup review |
| Okinawa and Iriomote | *Psychotria manillensis* visitor identity, controlled pollination/bagging and fruit-set outcomes | fail | eligible after de-dup review |
| Yakushima | community pollination-system structure and floral-architecture associations | fail | eligible after de-dup review |
| Lord Howe Island | *Howea* pollination-mode experiments, fruit set, recruitment and genetic structure | fail | eligible after de-dup review |
| Rodrigues | ex-situ breeding-system diagnosis in *Ramosmania heterophylla* | fail | retain search record; do not promote |
| Grenada | hummingbird/insect assemblages, floral phenotype and climate-associated network composition | fail | eligible after de-dup review |

Primary anchors include Petanidou et al. 2018 (`10.1111/plb.12593`), Kato 2000 (Kyoto University repository), Watanabe et al. 2021 (`10.7717/peerj.12318`), Yumoto 1987, Babik et al. 2009 (`10.1111/j.1365-294X.2009.04306.x`), Owens et al. 1993 (`10.1111/j.1095-8339.1993.tb00330.x`) and the Grenada/Dominica/Puerto Rico network studies (`10.1007/s00442-008-1255-z`; `10.1017/S0266467409990034`).

## First-wave de-duplication result

Research-entry count and geographic independence are deliberately separated.

- six research entries remain eligible after source gating;
- those six map to **five higher-level geographic groups**;
- only **four higher-level groups** would be new relative to the current 36-entry confrontation;
- Amami and Okinawa/Iriomote must share a single `ryukyu_archipelago` higher-level group rather than being counted as two independent archipelagos;
- Grenada is a distinct island research entry but overlaps the existing Lesser Antilles/Caribbean layer;
- Rodrigues overlaps the Mascarene region and is not promoted in any case.

Therefore this audit **does not change the current 36-entry confrontation**. Promotion is a separate step after explicit manuscript-value review.

## Search order

### Tier 1 — high-priority geographic gaps

Search and source-gate first:

- Cabo Verde;
- São Tomé and Príncipe;
- Ascension and Tristan da Cunha;
- Comoros/Mayotte and Socotra;
- Palau, Marshall, Solomon, Samoa, Tonga and Cook Islands;
- Pitcairn, Rapa Nui and Revillagigedo;
- Chatham, Kermadec and Norfolk;
- the remaining broad Ryukyu overlap decision.

The Aegean, Amami, Okinawa/Iriomote, Yakushima and Lord Howe source gates are now completed and should not stay in the unresolved queue.

### Tier 2 — medium-priority geographic completion

Work through continental-island and nested regional targets such as Corsica, Sardinia, Sicily, Malta, Crete, Cyprus, additional Lesser Antillean islands, Maldives, Chagos, Andaman/Nicobar, Taiwan, Philippines and French-Polynesian sub-archipelagos.

### Tier 3 — low-priority or low-information systems

Retain sparse systems even if no eligible source is found. A documented `no eligible source found under current search` state is preferable to silent geographic omission.

## Per-target evidence gate

Every target is reviewed against the same fields:

1. source functional state;
2. partner loss;
3. partner arrival/replacement;
4. realized community or functional shift;
5. local filtering;
6. reproductive assurance / breeding-system state;
7. plant response outcome;
8. source accessibility and directness;
9. geographic overlap with existing Chapter 2 entries;
10. full source-state → transition → realization → response contract.

A source may still be useful for **global confrontation** even when it fails the full contract. Full-contract failure remains explicit.

## Promotion rule

No target enters the current 36-entry descriptive confrontation simply because a source was found. Promotion requires:

- primary or authoritative source verification;
- an explicit evidence role;
- geographic overlap/de-duplication review;
- a recorded full-contract pass/fail state;
- a separate manuscript-value promotion decision;
- preservation of the frozen 25-entry identifiability denominator.

## Claim boundary

Do not describe the 110-target search universe as 110 independent archipelagos, as a complete census of every island on Earth, or as 110 empirical tests of the synthetic model. It is the **search denominator** for the exhaustive phase.

The purpose is to replace convenience sampling with transparent coverage: every named target is source-resolved, umbrella-indexed, source-found and gated, explicitly nested, or still awaiting source work. The systematic phase is allowed to conclude that a geography has no qualifying source under the documented search without converting that absence into biological evidence.
