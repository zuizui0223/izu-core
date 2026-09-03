# Chapter 2 world-breadth extension

Updated: 2026-09-03

## Decision

The frozen Chapter 2 identifiability audit remains **25 research entries**. It is not reopened or renormalized.

A separate, post-freeze breadth layer adds **10 source-verified research entries spanning 9 exact geographic groups** that were not represented by the frozen ledger's `geographic_overlap_group` labels. The combined descriptive universe is therefore **35 research entries before cross-layer de-duplication** and **30 exact overlap labels before higher-level archipelago de-duplication**.

Neither 35 nor 30 is an independent-archipelago denominator.

The machine-readable extension is:

- `data/design/chapter2_world_breadth_extension_20260902.csv`
- deterministic audit: `scripts/audit_chapter2_world_breadth_extension.py`
- audit result: `data/results/chapter2_world_breadth_extension_audit_20260903.json`

## Why this is a separate layer

The 25-entry audit was frozen to test whether existing studies jointly measure the outcome-independent coordinates required to distinguish the synthetic response geometry. Its current results remain:

- response outcome directly measured in 21/25 entries;
- partner arrival/replacement directly measured in 2/25 entries under the frozen measurement audit;
- 0/25 entries meet the full Chapter 2 contract;
- formal external prediction remains `not_evaluable`.

Adding literature after that freeze and silently recalculating those fractions would change the denominator after inspection. The extension therefore answers a different question: **how much wider is the empirical island universe, and can additional systems strengthen coverage of process dimensions that were sparse in the frozen audit?**

## Post-freeze extension

| Exact geographic group | Research entry | Source | Main added information | Arrival/replacement status | Full Chapter 2 contract |
|---|---|---|---|---|---|
| Azores | Flores pollination network | Olesen et al. 2002, `10.1046/j.1472-4642.2002.00148.x` | endemic/native/introduced interaction network and invader integration | introduced presence; no matched transition | fail |
| Azores | Terceira disturbed vs preserved forest networks | Boieiro et al. 2025, `10.3390/insects16010014` | disturbance-associated composition and network change; introduced bees important in disturbed sites | introduced presence; no matched arrival time | fail |
| Madeira | *Echium candicans* visitor assemblage | Esposito et al. 2021, `10.3390/insects12060488` | visitor performance, pollen loads, and non-native bee contribution | introduced presence; no matched arrival time | fail |
| New Caledonia | 99-plant community survey | Kato & Kawakita 2004, `10.3732/ajb.91.11.1814` | introduced honeybee dominance in a highly endemic flora | **historical arrival documented after the 1950s**; displacement inferred | fail |
| Fiji | *Braunsapis puangensis* invasion | Groom et al. 2015, `10.1111/1744-7917.12136` | distribution and nesting after a recent pollinator introduction | **direct recent arrival: first recorded 2007** | fail: no linked plant response |
| French Polynesia | origins of apid bees | Groom et al. 2017, `10.1111/ens.12230` | historical records plus mitochondrial evidence for introduced bee fauna | **direct/phylogeographic introduction evidence** | fail: no linked plant response |
| Juan Fernández | 25 endemic plant species | Anderson et al. 2001, PMID `11222245` | breeding systems, self-compatibility, floral visitors, rare native insect visitation | introduced bee and ant observed; no matched transition | fail |
| St Helena | *Commidendrum* pollination | Paajanen & Cronk 2020, `10.3897/BDJ.8.e52057` | contrasting fly- and moth-associated pollination in fragmented endemic taxa | none | fail |
| Réunion | bird-pollinated *Angraecum* | Micheneau et al. 2006, `10.1093/aob/mcl056` | pollen removal, deposition and fruit set under an insular pollinator-mode shift | none | fail |
| Pohnpei | breeding systems of 28 species | Yomai & Williams 2021, `10.1093/aobpla/plab038` | hand-pollination, autonomous selfing, pollen limitation and reproductive assurance | none | fail |

The 2002 Olesen paper also contains the Mauritian Ile aux Aigrettes network. That secondary site is not counted as a new exact geographic group here because Mauritius is already represented in the frozen 25-entry universe; the extension row is explicitly scoped to Azores-Flores.

## What genuinely improved

### 1. Geographic breadth

The extension adds exact geographic groups in the North Atlantic, South Atlantic, eastern and western Pacific, southwest Indian Ocean and Micronesia that were absent from the frozen overlap labels. This makes it incorrect to describe the empirical programme as only 25 island systems.

The defensible counts are now:

- **25 frozen research entries** for the formal identifiability audit;
- **10 additional post-freeze research entries** for breadth/process extension;
- **35 research entries** in the combined descriptive universe before cross-layer de-duplication;
- **21 frozen exact overlap labels + 9 extension exact geographic groups = 30 exact labels** before higher-level archipelago de-duplication;
- no claimed independent-archipelago `n`.

### 2. Partner-arrival evidence

The largest process gap in the frozen audit was partner arrival/replacement. The extension adds three especially useful records:

1. **New Caledonia:** the primary article states that *Apis mellifera* was introduced after the 1950s and subsequently became extremely abundant; the study directly measures its dominance in the contemporary pollination community.
2. **Fiji:** *Braunsapis puangensis* was first recorded in 2007 and its subsequent distribution and nesting biology were surveyed, giving unusually direct recent-arrival evidence.
3. **French Polynesia:** historical records and mitochondrial data support a predominantly introduced bee fauna, including purposeful introduction of *Apis mellifera* and human-mediated arrival of other bees.

These strengthen the reality of the model's arrival axis, but none supplies the linked source-state → community-transition → plant-response contract required for formal prediction.

### 3. Response breadth

Other new systems strengthen different parts of the response vocabulary:

- Pohnpei directly measures autonomous selfing and pollen limitation;
- Réunion directly measures pollen removal, pollen deposition and fruit set under a bird-pollination system;
- Juan Fernández shows extremely sparse native insect visitation alongside widespread self-compatibility and mixed breeding systems;
- Madeira measures visitor-specific foraging and pollen loads, including non-native bees;
- Azores and New Caledonia document community/network restructuring involving introduced pollinators;
- St Helena adds contrasting pollinator-mode realization in fragmented endemic sister taxa.

## What did not improve

No extension entry passes the full Chapter 2 predictor–outcome contract. Therefore the extension does **not** justify:

- recalculating the frozen 21/25 or 2/25 measurement fractions;
- changing 0/25 full contracts;
- fitting `H0`–`H4` on an enlarged denominator;
- leave-one-archipelago-out prediction;
- describing 35 entries as 35 independent island systems;
- treating introduced status alone as a measured before/after replacement process.

## Manuscript use

The active paper should keep the 25-entry audit as the quantitative identifiability result. The extension can be used to make the global-confrontation language more accurate:

> The formal identifiability audit was frozen at 25 research entries, but a post-freeze breadth screen identified 10 additional source-verified entries spanning nine exact geographic groups, including unusually direct pollinator-arrival records from Fiji, French Polynesia and New Caledonia. These additional systems broaden the empirical universe without altering the frozen 0/25 full-contract result.

This distinction preserves chronology while removing the misleading impression that the programme considered only 25 island systems worldwide.
