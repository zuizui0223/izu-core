# Chapter 2 world-breadth extension

Updated: 2026-09-04

## Decision

The frozen Chapter 2 identifiability audit remains **25 research entries**. It is not reopened or renormalized.

A separate post-freeze breadth layer now contains **14 source-verified research entries spanning 13 exact geographic groups** that were absent from the frozen ledger's exact `geographic_overlap_group` labels. The combined descriptive universe is therefore **39 research entries before cross-layer de-duplication** and **34 exact overlap labels before higher-level archipelago de-duplication**.

Neither 39 nor 34 is an independent-archipelago denominator.

A second, deliberately separate breadth context records one multi-group synthesis covering **11 Southern Ocean island groups and 321 flowering plant species**. That synthesis is not added to the 25-entry formal audit or to the 13 exact-group extension denominator because its source-native unit is a multi-island regional synthesis rather than one matched transition system.

Machine-readable surfaces:

- `data/design/chapter2_world_breadth_extension_20260902.csv`
- `data/design/chapter2_world_breadth_synthesis_context_20260904.csv`
- deterministic audit: `scripts/audit_chapter2_world_breadth_extension.py`
- audit result: `data/results/chapter2_world_breadth_extension_audit_20260903.json`

## Why this is a separate layer

The 25-entry audit was frozen to test whether existing studies jointly measure the outcome-independent coordinates required to distinguish the synthetic response geometry. Its current results remain:

- response outcome directly measured in 21/25 entries;
- partner arrival/replacement directly measured in 2/25 entries under the frozen measurement audit;
- 0/25 entries meet the full Chapter 2 contract;
- formal external prediction remains `not_evaluable`.

Adding literature after that freeze and silently recalculating those fractions would change the denominator after inspection. The extension therefore answers a different question: **how much wider is the empirical island universe, and can additional systems strengthen coverage of process dimensions that were sparse in the frozen audit?**

## Post-freeze exact-group extension

| Exact geographic group | Research entry | Source | Main added information | Arrival/replacement status | Full Chapter 2 contract |
|---|---|---|---|---|---|
| Azores | Flores pollination network | Olesen et al. 2002, `10.1046/j.1472-4642.2002.00148.x` | endemic/native/introduced interaction network and invader integration | introduced presence; no matched transition | fail |
| Azores | Terceira disturbed vs preserved forest networks | Boieiro et al. 2025, `10.3390/insects16010014` | disturbance-associated composition and network change; introduced bees important in disturbed sites | introduced presence; no matched arrival time | fail |
| Madeira | *Echium candicans* visitor assemblage | Esposito et al. 2021, `10.3390/insects12060488` | visitor performance, pollen loads and non-native bee contribution | introduced presence; no matched arrival time | fail |
| New Caledonia | 99-plant community survey | Kato & Kawakita 2004, `10.3732/ajb.91.11.1814` | introduced honeybee dominance in a highly endemic flora | **historical arrival documented after the 1950s**; displacement inferred | fail |
| Fiji | *Braunsapis puangensis* invasion | Groom et al. 2015, `10.1111/1744-7917.12136` | distribution and nesting after a recent pollinator introduction | **direct recent arrival: first recorded 2007** | fail: no linked plant response |
| French Polynesia | origins of apid bees | Groom et al. 2017, `10.1111/ens.12230` | historical records plus mitochondrial evidence for introduced bee fauna | **direct/phylogeographic introduction evidence** | fail: no linked plant response |
| Juan Fernández | 25 endemic plant species | Anderson et al. 2001, PMID `11222245` | breeding systems, self-compatibility, floral visitors, rare native insect visitation | introduced bee and ant observed; no matched transition | fail |
| St Helena | *Commidendrum* pollination | Paajanen & Cronk 2020, `10.3897/BDJ.8.e52057` | contrasting fly- and moth-associated pollination in fragmented endemic taxa | none | fail |
| Réunion | bird-pollinated *Angraecum* | Micheneau et al. 2006, `10.1093/aob/mcl056` | pollen removal, deposition and fruit set under an insular pollinator-mode shift | none | fail |
| Pohnpei | breeding systems of 28 species | Yomai & Williams 2021, `10.1093/aobpla/plab038` | hand-pollination, autonomous selfing, pollen limitation and reproductive assurance | none | fail |
| Vanuatu | wild giant taro reproductive biology | Quero Garcia et al. 2008, `10.1080/00288250809509762` | direct self-incompatibility tests, rare sexual reproduction and reported absence of efficient pollinators | no matched transition; current effective-pollinator absence direct | fail |
| Samoa | southwest-Pacific apid origins | Groom et al. 2014, `10.1007/s10530-014-0664-7` | DNA barcodes and historical records support predominantly human-mediated apid arrivals | **direct/phylogeographic introduction evidence; honeybee exotic by 1924** | fail: no linked plant response |
| Lower Florida Keys | *Chamaecrista keyensis* | Liu & Koptur 2003, `10.3732/ajb.90.8.1180` | controlled breeding-system work plus direct buzz-pollinator visitation across urban-edge and forest contexts | no arrival transition; anthropogenic local filtering relevant | fail |
| Socotra | *Dracaena cinnabari*–gecko interaction | García & Vasconcelos 2017, `10.1016/j.jnc.2016.11.005` | three endemic gecko species carried *D. cinnabari* pollen across 11 surveyed tree populations | none | fail: reproductive service not experimentally quantified |

The 2002 Olesen paper also contains the Mauritian Ile aux Aigrettes network. That secondary site is not counted as a new exact geographic group because Mauritius is already represented in the frozen 25-entry universe; the extension row is explicitly scoped to Azores-Flores.

## Separate multi-group breadth context

Lord (2015; `10.1093/aobpla/plv095`) synthesized floral traits and breeding systems for **321 flowering plant species across 11 Southern Ocean island groups**: Crozet, Prince Edward/Marion, Snares, Kerguelen, Antipodes, Auckland, Falklands, Campbell, Heard/McDonald, South Georgia and Macquarie. The study reports 34.3% of the regional flora with floral traits consistent with anemophily and 92.6% of species with known compatibility as partially or fully self-compatible.

This synthesis is useful because it substantially broadens the geographic and reproductive-strategy context, but it is not a matched community-transition study. It is therefore recorded separately rather than inflated into eleven independent prediction replicates.

## What genuinely improved

### 1. Geographic breadth

The defensible counts are now:

- **25 frozen research entries** for the formal identifiability audit;
- **14 additional post-freeze research entries** for exact-group breadth/process extension;
- **39 research entries** in the combined descriptive universe before cross-layer de-duplication;
- **21 frozen exact overlap labels + 13 extension exact geographic groups = 34 exact labels** before higher-level archipelago de-duplication;
- a separate **11-island-group Southern Ocean synthesis** that is not folded into those denominators;
- no claimed independent-archipelago `n`.

### 2. Partner-arrival evidence

The largest process gap in the frozen audit was partner arrival/replacement. The extension now adds four especially useful records:

1. **New Caledonia:** *Apis mellifera* was introduced after the 1950s and later became extremely abundant in the pollination community.
2. **Fiji:** *Braunsapis puangensis* was first recorded in 2007 and its subsequent distribution and nesting biology were surveyed.
3. **French Polynesia:** historical records and mitochondrial data support a predominantly introduced bee fauna.
4. **Samoa:** historical records plus DNA-barcode evidence place the local apid fauna in the same recent human-mediated southwest-Pacific introduction process.

These strengthen the empirical reality of the model's arrival axis, but none supplies the linked source-state → community-transition → plant-response contract required for formal prediction.

### 3. Local-filtering and response breadth

The Lower Florida Keys study adds a particularly relevant different process layer: controlled breeding-system experiments, direct bee visitation and an urban-edge context in which buzz-pollinator composition differed, with mosquito control identified as an additional plausible pollinator filter. This is closer to the model's local-filtering stage than most breadth entries, but it still lacks an outcome-independent source-state/community-transition vector.

Other new systems strengthen different response vocabulary components:

- Pohnpei directly measures autonomous selfing and pollen limitation;
- Vanuatu directly tests self-incompatibility and documents rare sexual reproduction under reported effective-pollinator absence;
- Réunion directly measures pollen removal, pollen deposition and fruit set under bird pollination;
- Juan Fernández shows extremely sparse native insect visitation alongside widespread self-compatibility and mixed breeding systems;
- Socotra adds a non-insect mutualistic pollination route, with geckos carrying *Dracaena* pollen;
- the Southern Ocean synthesis shows how breeding-system and pollination-mode constraints recur across a much broader climatic island domain.

## What did not improve

No exact-group extension entry passes the full Chapter 2 predictor–outcome contract. Therefore the extension does **not** justify:

- recalculating the frozen 21/25 or 2/25 measurement fractions;
- changing 0/25 full contracts;
- fitting `H0`–`H4` on an enlarged denominator;
- leave-one-archipelago-out prediction;
- describing 39 entries or 34 labels as independent island systems;
- treating introduced status alone as a measured before/after replacement process;
- counting the Southern Ocean synthesis as eleven independent prediction replicates.

## Manuscript use

The active paper should keep the 25-entry audit as the quantitative identifiability result. The broader programme can be described more accurately as follows:

> The formal identifiability audit was frozen at 25 research entries. A separate post-freeze breadth screen subsequently added 14 source-verified entries spanning 13 new exact geographic groups, including unusually direct pollinator-arrival records from New Caledonia, Fiji, French Polynesia and Samoa, and a Lower Florida Keys study linking local pollinator filtering to plant reproductive measurements. A separately tracked synthesis covers 321 flowering plant species across 11 Southern Ocean island groups. These additions broaden the empirical universe without altering the frozen 0/25 full-contract result.

This distinction preserves chronology while removing the misleading impression that the programme considered only 25 island systems worldwide.
