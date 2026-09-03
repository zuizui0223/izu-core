# Chapter 2 systematic island-universe audit

Updated: 2026-09-03

## Decision

Chapter 2 now separates three different objects:

1. the frozen **25-entry identifiability audit**;
2. the current **36-entry descriptive global confrontation**;
3. a new **systematic search universe** used to drive exhaustive source review without changing either earlier denominator.

The seed search frame contained **110 named geographic targets across 8 macroregions**. Source-native recovery from the current Southwest Pacific morphology entry then exposed one missing named archipelago, the **Three Kings Islands**, so the effective search universe is now **111 targets**.

Neither 110 nor 111 is an estimate of the number of island systems on Earth. The search universe is an evolving, reproducible frame of named archipelagos, island groups and selected large/sentinel islands relevant to terrestrial flowering-plant pollination, breeding systems, reproductive assurance and plant-pollinator networks.

Machine-readable files:

- `data/design/chapter2_systematic_island_universe_v1_20260903.csv`
- `data/design/chapter2_systematic_source_native_overlap_corrections_20260903.csv`
- `data/design/chapter2_systematic_first_wave_source_gate_20260903.csv`
- `data/design/chapter2_systematic_first_wave_dedup_review_20260903.csv`
- `data/design/chapter2_systematic_second_wave_search_gate_20260903.csv`
- `data/design/chapter2_systematic_second_wave_dedup_review_20260903.csv`
- `scripts/audit_chapter2_systematic_island_universe.py`
- `data/results/chapter2_systematic_island_universe_audit_v1_20260903.json`

## Current coverage state

After the two search waves plus source-native overlap correction:

- effective search universe: **111 targets**;
- macroregions: **8**;
- targets with documented direct search, prior source coverage or umbrella coverage: **69**;
- targets not yet directly reviewed or prior-covered: **42**;
- targets requiring any additional source work, including reviewed-but-incomplete targets: **55**;
- original `target_not_yet_source_gated` rows still untouched after both waves: **37**;
- original `source_found_needs_ledger_gate` rows still ungated: **0**;
- nested targets still requiring their own specific source gate: **5**.

The systematic programme therefore no longer treats the current 36 entries as if they were the global search denominator. The 36 remain the currently admitted descriptive confrontation; the 111-target frame determines what still has to be searched.

## Source-native overlap correction

Ciarle et al. 2025 (`10.1093/aob/mcaf005`) explicitly sampled ten Southwest Pacific archipelagos:

- Lord Howe;
- Norfolk;
- Kermadec;
- Three Kings;
- Chatham;
- Snares;
- Antipodes;
- Auckland;
- Campbell;
- Macquarie.

Because the Ciarle study is already one of the current 36 research entries, these archipelagos are already represented geographically by that research layer even when a separate process-oriented source has not yet been gated. This correction changes the search bookkeeping, not the 36-entry research-entry count.

It also corrects an earlier first-wave interpretation: **Lord Howe is not a new geographic group relative to the current 36**. The first-wave candidate geography is therefore reduced from four to **three confirmed new higher-level groups**: Aegean, Ryukyu and Yakushima.

## Umbrella sources that change the search strategy

The programme is not driven only by one-paper-at-a-time discovery. Global or multi-archipelago sources are used as indexes and then expanded back to source-native sites.

### Global quantitative pollination networks

Traveset et al. 2016 (`10.1111/geb.12362`) compiled 52 quantitative plant-pollinator networks: 23 continental-island, 18 oceanic-island and 11 mainland networks. Supporting information identifies network sampling locations. This is an **index source**, not 41 independent island-system validation events.

Trøjelsgaard & Olesen 2013 (`10.1111/j.1466-8238.2012.00777.x`) compiled 54 community-wide pollination networks, including 17 island networks. The Web of Life database is retained as a recovery route. Database presence alone never promotes a target; the original source still must be checked.

### Southern Ocean

Lord 2015 (`10.1093/aobpla/plv095`) provides a comparative source across 11 Southern Ocean island groups and 321 flowering plant species: Crozet, Prince Edward/Marion, Snares, Kerguelen, Antipodes, Auckland, Falklands, Campbell, Heard/McDonald, South Georgia and Macquarie. It directly informs floral-trait and breeding-system breadth but not a matched historical community transition.

### Southwest Pacific morphology

Ciarle et al. 2025 provides 129 phylogenetically independent colonisation events across the ten source-native archipelagos listed above. This layer is important for geography and response-shape coverage, but it does not supply the matched community-reorganisation chain required for the Chapter 2 full contract.

## First-wave source gate

Seven targets were inspected with the same channel-level gate used elsewhere in Chapter 2.

| Target | Direct information recovered | Full contract | Current geographic decision |
|---|---|---|---|
| Aegean Archipelago | 39 plant-pollinator networks on eight islands; richness and network structure across climate gradient | fail | confirmed new higher-level group candidate |
| Amami Islands | 164 flowering plants and 610 anthophilous insect species across vegetation types | fail | share one Ryukyu group |
| Okinawa and Iriomote | visitor identity, controlled pollination/bagging and fruit-set outcomes in *Psychotria manillensis* | fail | share one Ryukyu group |
| Yakushima | community pollination-system structure and floral-architecture associations | fail | confirmed new higher-level group candidate |
| Lord Howe Island | *Howea* pollination-mode experiments, fruit set, recruitment and genetic structure | fail | existing current-36 geography via Ciarle 2025 |
| Rodrigues | ex-situ breeding-system diagnosis in *Ramosmania heterophylla* | fail | retain search record; do not promote |
| Grenada | hummingbird/insect assemblages, floral phenotype and climate-associated network composition | fail | existing Lesser Antilles/Caribbean layer |

Six research entries remain evidence-rich enough for later manuscript-value consideration, but they map to five higher-level groups and only **three** are confirmed new geography relative to the current 36.

## Second-wave search gate

Nineteen additional high-priority targets were explicitly searched. Search failure was recorded rather than silently dropping the geography.

### Direct or strong source candidates

- **Mayotte / Comoros** — *Vanilla humblotii* reproductive biology: pollinator-dependent, self-compatible, approximately 1% natural fruit set despite bee and sunbird visits; strong direct reproductive/pollination evidence, but broader Comoros coverage remains incomplete.
- **Socotra** — eleven *Dracaena cinnabari* populations with endemic gecko pollen carriage documented directly.
- **Samoa** — field observations, experiments and pollen evidence identify flying fox and starling pollination of *Freycinetia reineckei*.
- **Cook Islands** — *Ficus prolixa* retains species-specific fig-wasp pollinators despite other vertebrate mutualist extinctions; habitat loss better explains the observed boundary, making this a useful falsification system.
- **Kermadec** — historical primary observations directly record pollen-bearing tui and lacewing flower visitation; geography is already represented in the current 36 through Ciarle 2025.

### Geography resolved but not a new process entry

- **Cabo Verde** — direct flower-shape morphometrics, no measured pollinator-community transition.
- **Revillagigedo** — direct flower-size response already belongs to the existing Pacific morphology research layer.
- **Ryukyu Islands** — broad target resolved by the separately gated Amami and Okinawa/Iriomote sources.

### Source insufficient or still incomplete

- **Palau** — pollination descriptions remain largely syndrome/hypothesis based in the recovered sources.
- **Norfolk** — direct government conservation observation exists, but a stronger peer-reviewed mechanism source is still preferred; geography itself is already covered by Ciarle 2025.
- **Solomon Islands** — feeding/ecology sources were recovered, but feeding was not converted into pollination evidence.
- **São Tomé and Príncipe, Ascension, Tristan da Cunha, Marshall Islands, Tonga, Pitcairn, Rapa Nui and Chatham** — initial search was inconclusive for a qualifying direct source. This means literature coverage is unresolved, not that the biological process is absent. Chatham geography is already represented by Ciarle 2025.

All 19 second-wave targets still fail the full Chapter 2 source-state → transition → local-realization → plant-response contract.

## Second-wave de-duplication

Five second-wave rows were strong enough to enter explicit geographic de-duplication review.

- **Comoros/Mayotte** — confirmed new higher-level group candidate relative to the current 36;
- **Socotra** — confirmed new higher-level group candidate;
- **Kermadec** — existing current-36 geography through Ciarle 2025;
- **Samoa** — hold: potential overlap with the unresolved source-native geography of the current Pacific multi-system morphology entry;
- **Cook Islands** — hold for the same unresolved Pacific-overlap reason.

This step still **does not modify the 36-entry confrontation**.

## Remaining search order

The next waves should work through the remaining 42 never-reviewed/prior-covered targets rather than adding only convenient positive examples.

### Priority geographic gaps

Continue with unresolved Atlantic, Mediterranean, Indian Ocean, Caribbean and Pacific targets, including Selvagens, Bermuda, Corsica, Sardinia, Sicily, Malta, Crete, Cyprus, additional Lesser Antillean islands, Maldives, Chagos, Andaman/Nicobar, Taiwan, Philippines, additional Micronesian/Melanesian/Polynesian groups and the nested French-Polynesian sub-archipelagos.

### Nested-target rule

A regional or multi-island source does not automatically resolve every nested island. Nested targets receive their own gate when Chapter 2 would make a local transition or pollinator-realization claim about that island.

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

Do not describe the effective 111-target search universe as 111 independent archipelagos, as a complete census of every island on Earth, or as 111 empirical tests of the synthetic model. It is the **current systematic search denominator** and may expand when source-native multi-archipelago studies expose omitted named systems.

The purpose is to replace convenience sampling with transparent coverage. Every named target is source-resolved, umbrella-indexed, directly searched, explicitly nested, or still awaiting source work. A documented inconclusive search remains a coverage gap and is never converted into evidence of biological absence.
