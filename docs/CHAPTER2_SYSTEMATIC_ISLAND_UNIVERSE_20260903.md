# Chapter 2 systematic island-universe audit

Updated: 2026-09-03

## Decision

Chapter 2 now separates three different objects:

1. the frozen **25-entry identifiability audit**;
2. the current **36-entry descriptive global confrontation**;
3. a new **systematic search universe** used to drive exhaustive source review without changing either earlier denominator.

The systematic search universe currently contains **110 named geographic targets across 8 macroregions**. The 110 targets are not an estimate of the number of island systems on Earth. They are a reproducible search frame covering named archipelagos, island groups and selected large/sentinel islands relevant to terrestrial flowering-plant pollination, breeding systems, reproductive assurance and plant-pollinator networks.

Machine-readable files:

- `data/design/chapter2_systematic_island_universe_v1_20260903.csv`
- `scripts/audit_chapter2_systematic_island_universe.py`
- `data/results/chapter2_systematic_island_universe_audit_v1_20260903.json`

## Current coverage state

The v1 audit gives:

- 110 geographic targets;
- 8 macroregions;
- 42 targets already resolved, source-covered or indexed by an umbrella source;
- 68 targets requiring further source work;
- 56 targets not yet directly source-gated;
- 7 targets where a relevant source has already been found but still needs explicit ledger admission/de-duplication review;
- 5 nested targets that need their own source gate rather than inheriting a broad regional source automatically.

The high-priority unresolved/search pool contains 37 rows.

## Umbrella sources that change the search strategy

The systematic programme is no longer driven only by one-paper-at-a-time discovery. Several global or multi-archipelago sources can be used as indexes and then expanded back to their source-native sites.

### Global quantitative pollination networks

Traveset et al. (2016; DOI `10.1111/geb.12362`) compiled 52 quantitative plant-pollinator networks: 23 continental-island, 18 oceanic-island and 11 mainland networks. Its Supporting Information Table S1 identifies network sampling locations and Table S2 contains oceanic-island traits. This paper is treated as an **index source**, not as 41 independent island-system validation events.

Trøjelsgaard & Olesen (2013; DOI `10.1111/j.1466-8238.2012.00777.x`) compiled 54 community-wide pollination networks. Seventeen were island networks: four New Zealand, four Canarian, two Jamaican, one Dominican, one Mauritian, three Galápagos, one Azorean and one Amami/Japanese-island network. This is a second index source for recovering historically used network sites and original references.

The Web of Life database is retained as a network-recovery route because it stores network identifiers, references, locations and interaction matrices. A network appearing in a global database is not automatically promoted to the Chapter 2 evidence ledger; the original source still must be checked.

### Southern Ocean

Lord (2015; DOI `10.1093/aobpla/plv095`) provides a single comparative source across 11 Southern Ocean island groups and 321 flowering plant species. The island groups are Crozet, Prince Edward/Marion, Snares, Kerguelen, Antipodes, Auckland, Falklands, Campbell, Heard/McDonald, South Georgia and Macquarie. This source directly informs floral-trait and breeding-system coverage but does not establish a matched historical community-transition contract.

### Macaronesia and Caribbean

The Macaronesia review framework identifies Azores, Madeira, Selvagens, Canary Islands and Cabo Verde as the five main Macaronesian archipelagos. Current Chapter 2 evidence already covers Azores, Madeira and Canary Islands; Selvagens and Cabo Verde therefore remain explicit search targets instead of disappearing from the universe.

Caribbean Gesneriaceae work spans Cuba, Hispaniola, Jamaica, Puerto Rico and the Lesser Antilles and is kept as an umbrella source. Individual island targets still require their own gate when a claim depends on a particular transition or local pollinator realization.

## First-wave sources found outside the current 36-entry confrontation

The systematic search has already identified several sources that merit explicit gating:

- **Aegean Archipelago** — plant-pollinator networks along a small-scale climate gradient (`10.1111/plb.12593`);
- **Ryukyu / Amami** — Kato (2000) community-wide anthophilous-insect and plant-pollinator data on Amami; additional Psychotria breeding/pollination studies in Okinawa and Iriomote;
- **Yakushima** — island pollination-system work retained as a separate exact target;
- **Lord Howe Island** — Howea pollination/speciation studies provide a process-oriented island system;
- **Grenada** — modern vertebrate-pollination network compilations identify island network data, requiring recovery of the original source;
- **Rodrigues** — direct breeding-system evidence exists for the critically rare endemic Ramosmania heterophylla, but this is a focal-species reproductive record rather than a community-reorganization transition.

These are **source-found targets**, not yet additions to the 36-entry confrontation.

## Search order

The next pass is priority-based rather than convenience-based.

### Tier 1 — high-priority geographic gaps

Search and source-gate first:

- Cabo Verde;
- São Tomé and Príncipe;
- Ascension and Tristan da Cunha;
- Comoros/Mayotte, Rodrigues and Socotra;
- Palau, Marshall, Solomon, Samoa, Tonga and Cook Islands;
- Pitcairn, Rapa Nui and Revillagigedo;
- Chatham, Kermadec, Norfolk and Lord Howe;
- Aegean and Ryukyu/Amami/Yakushima, where relevant sources are already known.

### Tier 2 — medium-priority geographic completion

Work through continental-island and nested regional targets such as Corsica, Sardinia, Sicily, Malta, Crete, Cyprus, additional Lesser Antillean islands, Maldives, Chagos, Andaman/Nicobar, Taiwan, Philippines and French-Polynesian sub-archipelagos.

### Tier 3 — low-priority or low-information systems

Retain sparse systems in the search universe even if the current search finds no eligible pollination/reproductive source. A documented `no eligible source found under current search` state is preferable to silently omitting the geography.

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

A source may still be useful for **global confrontation** even if it fails the full contract. Full-contract failure must remain explicit.

## Promotion rule

No target is added to the current 36-entry descriptive confrontation simply because a search result exists. Promotion requires:

- primary or authoritative source verification;
- an explicit evidence role;
- geographic overlap/de-duplication review;
- a recorded full-contract pass/fail state;
- preservation of the frozen 25-entry identifiability denominator.

## Claim boundary

Do not describe the 110-target search universe as 110 independent archipelagos, as a complete census of every island on Earth, or as 110 empirical tests of the synthetic model. It is the **search denominator** for the next exhaustive phase.

The purpose of this phase is to replace convenience sampling with a transparent coverage process: every named target is either source-resolved, indexed by an umbrella source, source-found and awaiting admission review, explicitly nested, or still awaiting source gating.
